"""Prof. Wigner: Syzygy analysis of B2 = [B2_in; B2_out] with t_B in {2, 3, 4}."""
import numpy as np
import sys
sys.path.append('council/prof-noether')
from general_n2k_noether import build_Mn

def test_protruding_syzygy():
    print("=" * 70)
    print("PROF. WIGNER: PROTRUDING SYZYGY ANALYSIS FOR t_B in {2, 3, 4}")
    print("=" * 70)

    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    
    # B2_full has shape (6, 20, 15)
    B2_full = np.zeros((6, 20, 15), dtype=float)
    for ell in range(20):
        B2_full[:, ell, :] = V_basis[:, ell].reshape(15, 6).T

    rng = np.random.default_rng(2026)

    # For t_B in (2, 3, 4):
    # Keep 19 - t_B wires from B2_full (inside S_{6,3})
    # Add t_B random/protruding wires B2_out outside S_{6,3}
    for t_B in (2, 3, 4):
        n_in = 19 - t_B
        keep_indices = list(range(n_in))
        B2_in = B2_full[:, keep_indices, :] # (6, n_in, 15)
        
        max_syz = 0
        min_syz = 100
        for trial in range(20):
            # Protruding wires: random linear matrices of shape (6, t_B, 15)
            B2_out = rng.standard_normal((6, t_B, 15))
            
            # Full B2: shape (6, 19, 15)
            B2_cand = np.concatenate([B2_in, B2_out], axis=1)
            
            # Check degree-1 left syzygies: u(b) B2(b) == 0
            # u has 19 rows * 6 vars = 114 entries
            # Equations: 15 cols * 21 monomials = 315 equations
            eqs = []
            for J in range(15):
                for c1 in range(6):
                    for c2 in range(c1, 6):
                        row = np.zeros(6 * 19, dtype=float)
                        for ell in range(19):
                            row[c1 * 19 + ell] += B2_cand[c2, ell, J]
                            if c1 != c2:
                                row[c2 * 19 + ell] += B2_cand[c1, ell, J]
                        eqs.append(row)
            E_mat = np.array(eqs)
            rk = np.linalg.matrix_rank(E_mat, tol=1e-8)
            syz_dim = 114 - rk
            max_syz = max(max_syz, syz_dim)
            min_syz = min(min_syz, syz_dim)
            
        print(f"t_B = {t_B} protruding rows: syzygy dimension min = {min_syz}, max = {max_syz}")
        
    print("=" * 70)

if __name__ == "__main__":
    test_protruding_syzygy()
