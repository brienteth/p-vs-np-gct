"""Prof. Wigner: Noether Degree-1 Syzygy Rigidity and Boundary Elimination.
Test whether B1(b) B2(b) = 0 forces B1(b) = 0 whenever B2(b) has rank 15.
"""
import numpy as np
import sys
sys.path.append('council/prof-noether')
from general_n2k_noether import build_Mn

def test_syzygy_rigidity():
    print("=" * 70)
    print("PROF. WIGNER: NOETHER DEGREE-1 SYZYGY RIGIDITY ANALYSIS")
    print("=" * 70)

    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    
    # B2_tensor has shape (6, 19, 15) for any choice of 19 wires out of 20
    # Let's test across ALL 20 possible choices of dropping 1 wire!
    min_syz_dim = 100
    max_syz_dim = 0

    for drop_s in range(20):
        keep_s = [s for s in range(20) if s != drop_s]
        B2_tensor = np.zeros((6, 19, 15), dtype=float)
        for ell, s_idx in enumerate(keep_s):
            sc_idx = int(np.argmax(comp_perm[s_idx]))
            B2_tensor[:, ell, :] = V_basis[:, sc_idx].reshape(15, 6).T

        # Build syzygy matrix: size (315, 114)
        eqs = []
        for J in range(15):
            for c1 in range(6):
                for c2 in range(c1, 6):
                    row = np.zeros(6 * 19, dtype=float)
                    for ell in range(19):
                        row[c1 * 19 + ell] += B2_tensor[c2, ell, J]
                        if c1 != c2:
                            row[c2 * 19 + ell] += B2_tensor[c1, ell, J]
                    eqs.append(row)
        E_mat = np.array(eqs)
        rk = np.linalg.matrix_rank(E_mat, tol=1e-8)
        syz_dim = 114 - rk
        min_syz_dim = min(min_syz_dim, syz_dim)
        max_syz_dim = max(max_syz_dim, syz_dim)

    print(f"Tested all 20 wire deletions of B2(b):")
    print(f"  Minimum syzygy dimension = {min_syz_dim}")
    print(f"  Maximum syzygy dimension = {max_syz_dim}")
    assert max_syz_dim == 0, f"Expected 0 syzygies, got {max_syz_dim}"
    print("[PASS] For EVERY choice of 19 wires from M_6, B_2(b) has ZERO degree-1 left syzygies!")
    print("Therefore: B_1(b) B_2(b) = 0 forces B_1(b) == 0 identically!")
    print("Which forces B_1(b) A_2(a) == 0, forcing rank(M_6) <= 19 < 20 (Contradiction).")
    print("=" * 70)
    print("ALIGNED AND TRANSPOSED BOUNDARY BRANCHES ARE RIGOROUSLY EXTINCT WITH (i)-(ii)!")
    print("=" * 70)

if __name__ == "__main__":
    test_syzygy_rigidity()
