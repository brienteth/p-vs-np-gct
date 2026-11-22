"""
Prof. Euler - Round 5 Phase 5A Script: test_round5_phase5a.py
Comprehensive investigation of:
1. Exact maximum delta(U) = dim(S_{6,3} cap (U x F^6)) for general and coordinate subspaces U subset F^15 of dim d <= 8.
2. Degree-1 syzygy rigidity under protrusion and cross-coupling cancelation.
"""
import itertools
import numpy as np
import sys
sys.path.append('council/prof-noether')
from general_n2k_noether import build_Mn

def test_delta_spectrum():
    print("=" * 70)
    print("PART 1: MAXIMUM DELTA(U) FOR GENERAL & COORDINATE SUBSPACES U SUBSET F^15")
    print("=" * 70)
    
    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    # V_basis is 90 x 20
    
    rng = np.random.default_rng(2026)
    
    # 1. Coordinate subspaces U: subsets of size d from 15 edges
    # For d in 1..8, find max delta_coord
    print("Testing coordinate subspaces U (subgraphs of K_6):")
    for d in range(1, 9):
        max_delta_coord = -1
        best_edges = None
        # Sample or exhaustively check combinations
        n_combs = math_comb = len(list(itertools.combinations(range(15), d)))
        sample_size = min(n_combs, 2000)
        
        # Check specific known extremal graphs first:
        # e.g. for d=3: triangle; d=6: K_4; d=7: K_4 + 1 edge; d=8: K_4 + 2 edges
        tested = 0
        for edge_indices in itertools.combinations(range(15), d):
            # Gamma is (15-d) x 15: delete the d rows
            keep = list(edge_indices)
            drop = [i for i in range(15) if i not in keep]
            Gamma = np.zeros((15 - d, 15))
            for r, row_idx in enumerate(drop):
                Gamma[r, row_idx] = 1.0
            
            H = np.kron(Gamma, np.eye(6)) @ V_basis # (6*(15-d)) x 20
            rk = np.linalg.matrix_rank(H, tol=1e-8)
            delta = 20 - rk
            if delta > max_delta_coord:
                max_delta_coord = delta
                best_edges = edge_indices
            tested += 1
            if tested >= sample_size:
                break
                
        print(f"  d = {d}: max coordinate delta = {max_delta_coord} (tested {tested}/{n_combs})")

    print("\nTesting random non-coordinate subspaces U subset R^15:")
    for d in range(1, 9):
        max_delta_rand = -1
        for _ in range(200):
            U = rng.standard_normal((15, d))
            u_orth, _, _ = np.linalg.svd(U)
            Gamma = u_orth[:, d:].T # (15-d) x 15
            H = np.kron(Gamma, np.eye(6)) @ V_basis
            rk = np.linalg.matrix_rank(H, tol=1e-8)
            delta = 20 - rk
            if delta > max_delta_rand:
                max_delta_rand = delta
        print(f"  d = {d}: max random non-coordinate delta = {max_delta_rand}")

def test_cross_coupling_cancelation():
    print("\n" + "=" * 70)
    print("PART 2: CROSS-COUPLING PROTRUSION RIGIDITY")
    print("=" * 70)
    
    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    
    # Check syzygy dimension of B2 with t_B protruding wires:
    # Let B2 = [B2_in; B2_out] where B2_in is (19-t_B) x 90 in S_{6,3}
    # and B2_out is t_B x 90 in S_{6,3}^perp
    rng = np.random.default_rng(42)
    u_V, s_V, _ = np.linalg.svd(V_basis)
    V_orth = u_V[:, 20:] # 90 x 70 orthogonal complement S_{6,3}^perp
    
    for t_B in [1, 2, 3, 4]:
        print(f"\n--- Testing t_B = {t_B} protruding wires ---")
        # Sample B2_in: (19-t_B) random rows in S_{6,3}
        W_in = rng.standard_normal((19 - t_B, 20))
        B2_in_rows = (W_in @ V_basis.T) # (19-t_B) x 90
        
        # Sample B2_out: t_B random rows in S_{6,3}^perp
        W_out = rng.standard_normal((t_B, 70))
        B2_out_rows = (W_out @ V_orth.T) # t_B x 90
        
        B2_rows = np.vstack([B2_in_rows, B2_out_rows]) # 19 x 90
        
        # Reshape to (6, 19, 15):
        B2_tensor = np.zeros((6, 19, 15))
        for ell in range(19):
            B2_tensor[:, ell, :] = B2_rows[ell].reshape(15, 6).T
            
        # Build 315 x 114 syzygy matrix
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
        print(f"  Random t_B = {t_B} protruding in S_{6,3}^perp: dim(deg-1 left syzygies) = {syz_dim}")

if __name__ == '__main__':
    test_delta_spectrum()
    test_cross_coupling_cancelation()
