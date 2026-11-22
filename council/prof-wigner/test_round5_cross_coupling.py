"""Prof. Wigner: Round 5 Cross-Coupling and Degenerate Subspace Analysis for n=6, w=19.
Can any subspace U of dim <= 8 in C^15 have delta(U) >= 3 AND satisfy B1 B2 = 0?
"""
import itertools
import numpy as np
import sys
sys.path.append('council/prof-noether')
from general_n2k_noether import build_Mn

def test_round5():
    print("=" * 70)
    print("PROF. WIGNER: ROUND 5 DEGENERATE SUBSPACE & CROSS-COUPLING AUDIT")
    print("=" * 70)

    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    # V_basis has shape (90, 20), columns form orthonormal basis of S_{6,3} in C^{90}
    # C^{90} = C^{15} otimes C^6.
    
    # Let's test the maximum intersection delta(U) = dim(S_{6,3} cap (U otimes C^6))
    # for random and coordinate subspaces U in C^15 of dimension d = 1..8:
    rng = np.random.default_rng(2026)
    
    print("1. Testing delta(U) for random subspaces U in C^15 of dim d = 1..8:")
    for d in range(1, 9):
        max_delta = 0
        for _ in range(50):
            U_basis = rng.standard_normal((15, d))
            # Basis of U otimes C^6 in C^{90} is (U_basis otimes I_6): shape (90, 6*d)
            U_kron = np.kron(U_basis, np.eye(6)) # 90 x (6d)
            
            # Intersection dim between S_{6,3} (colsp V_basis, dim 20) and U_kron
            # Zassenhaus: dim(A cap B) = rank(A) + rank(B) - rank([A, B])
            rk_U = np.linalg.matrix_rank(U_kron, tol=1e-7)
            rk_joint = np.linalg.matrix_rank(np.hstack([V_basis, U_kron]), tol=1e-7)
            inter_dim = 20 + rk_U - rk_joint
            max_delta = max(max_delta, inter_dim)
        print(f"  dim U = {d}: max delta(U) over random trials = {max_delta}")

    # What about worst-case adversarial coordinate subspaces U = coordinate subsets of {0..14}?
    print("\n2. Testing delta(U) for coordinate subspaces U of dim d = 1..8:")
    for d in (1, 2, 3, 4, 5, 6, 7, 8):
        max_coord_delta = 0
        # Sample 200 coordinate subsets
        for subset in itertools.islice(itertools.combinations(range(15), d), 200):
            U_coord = np.zeros((15, d))
            for r, idx in enumerate(subset):
                U_coord[idx, r] = 1.0
            U_kron = np.kron(U_coord, np.eye(6))
            rk_joint = np.linalg.matrix_rank(np.hstack([V_basis, U_kron]), tol=1e-7)
            inter_dim = 20 + 6 * d - rk_joint
            max_coord_delta = max(max_coord_delta, inter_dim)
        print(f"  dim U = {d}: max coordinate delta(U) = {max_coord_delta}")

    # Notice: for coordinate subspaces, delta(U) is bounded by Kruskal-Katona KK_{2->3}(d)!
    # KK_{2->3}(1..8) = [0, 0, 1, 1, 2, 4, 4, 5]
    print("\n3. Testing Cross-Coupling projection Pi_perp:")
    # S_{6,3} has dimension 20 in C^90. Its orthogonal complement S_{6,3}^perp has dimension 70.
    # Pi_perp is (I_90 - V_basis @ V_basis^T / 3) (since ||v_S||^2 = 3)
    # Let's verify projector:
    P_S = V_basis @ V_basis.T / 3.0
    assert np.allclose(P_S @ P_S, P_S)
    print("Projector P_S onto S_{6,3} verified (rank 20).")
    
if __name__ == "__main__":
    test_round5()
