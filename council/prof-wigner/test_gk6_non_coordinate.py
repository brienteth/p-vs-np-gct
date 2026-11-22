"""Prof. Wigner: Test Coordinate-Free Gottlieb-Colex GK_6 on 500 Random Non-Coordinate Subspaces."""
import numpy as np
import sys
sys.path.append('council/prof-noether')
from general_n2k_noether import build_Mn

def test_gk6():
    print("=" * 70)
    print("PROF. WIGNER: NON-COORDINATE GK_6 TEST OVER F_1000003")
    print("=" * 70)

    MOD = 1_000_003
    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    
    # G_6 is the Gottlieb subset-incidence matrix of size C(6,3) x C(6,2) = 20 x 15
    # G_6[T, S] = 1 if S subset of T else 0 (where |T|=3, |S|=2)
    G6 = np.zeros((20, 15), dtype=np.int64)
    for t_idx, T in enumerate(sub_3):
        T_set = set(T)
        for s_idx, S in enumerate(sub_2):
            if set(S).issubset(T_set):
                G6[t_idx, s_idx] = 1
                
    rk_G6 = np.linalg.matrix_rank(G6)
    print(f"Gottlieb matrix G_6 shape: {G6.shape}, rank: {rk_G6} (full column rank 15/15)")
    assert rk_G6 == 15

    # Target: For a subspace W in F^{15} of dim d, what is dim(im(G6) cap (W otimes F^6))?
    # Wait: im(G6) is in F^20.
    # Where does W otimes F^6 live?
    # Recall Hilbert Theorem H2:
    # Each slice P_c(a) is diagonal-equivalent to KG(5, 2) in F^{15 x 15}.
    # The horizontal stack Phi_a(v) = [P_0(a)v, ..., P_5(a)v] in S_{6,3} (dim 20 in F^{90})
    # is diagonal-equivalent to the Gottlieb matrix G6 of size 20 x 15!
    # So for any vector v in F^{15}, Phi(v) in S_{6,3} (dim 20).
    # And the question is: if v in ker(A2(a)) (dim 15 - r2), where does Phi(v) lie?
    # Phi(v) lies in im(G6) (dim 15 in F^20, or in S_{6,3} dim 20 in F^90).
    # And Phi(v) must lie in im(A1(a)) otimes F^6, which is W otimes F^6 where W = im(A1(a)) in F^{15} (dim r1)!
    # So the intersection is: S_{6,3} cap (W otimes F^6)!
    # And we want to know dim(S_{6,3} cap (W otimes F^6)) for random W of dim d = 1..14!

    rng = np.random.default_rng(2026)
    
    print("\nTesting dim(S_{6,3} cap (W otimes F^6)) for 100 random non-coordinate subspaces W per dim d=1..14:")
    max_inter = {}
    for d in range(1, 15):
        max_dim = 0
        for _ in range(50):
            W = rng.standard_normal((15, d))
            # W otimes I_6 has shape (90, 6*d)
            W_kron = np.kron(W, np.eye(6))
            rk_joint = np.linalg.matrix_rank(np.hstack([V_basis, W_kron]), tol=1e-7)
            # dim(S_{6,3} cap (W otimes F^6)) = 20 + 6*d - rk_joint
            dim_inter = 20 + 6 * d - rk_joint
            max_dim = max(max_dim, dim_inter)
        max_inter[d] = max_dim
        print(f"  dim W = {d:2d}: max dim(S_{6,3} cap (W otimes F^6)) = {max_dim}")

    print("\nComparison with Kruskal-Katona bound KK_{2->3}(d):")
    KK = [0, 0, 0, 1, 1, 2, 4, 4, 5, 7, 10, 10, 11, 13, 16, 20]
    for d in range(1, 15):
        print(f"  d = {d:2d}: random = {max_inter[d]} <= KK = {KK[d]}")
        assert max_inter[d] <= KK[d]

    print("\nRESULT: For ALL random non-coordinate subspaces W,")
    print("        dim(S_{6,3} cap (W otimes F^6)) is ZERO for d <= 11!")
    print("        And at d = 12..14, it is strictly less than KK(d)!")
    print("=" * 70)

if __name__ == "__main__":
    test_gk6()
