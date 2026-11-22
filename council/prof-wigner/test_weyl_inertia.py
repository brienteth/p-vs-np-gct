"""Prof. Wigner: Spectral, Weyl, and Inertia analysis of M - K1 - K2."""
import numpy as np

def test_weyl_and_projections():
    # Construct M
    M = np.zeros((16, 16), dtype=np.float64)
    for j0 in range(4):
        for c1 in range(4):
            for j3 in range(4):
                for c2 in range(4):
                    if len({j0, c1, j3, c2}) == 4:
                        M[j0 * 4 + c1, j3 * 4 + c2] = 1.0

    evals, evecs = np.linalg.eigh(M)
    # Print sorted eigenvalues
    print("M eigenvalues:\n", np.round(evals, 4))
    
    # Eigenspaces:
    # V_minus: evals approx -2 (3 dimensions)
    # V_plus: evals approx +2 (3 dimensions)
    # V_zero: evals approx 0 (10 dimensions)
    idx_minus = np.where(np.abs(evals - (-2.0)) < 1e-4)[0]
    idx_plus = np.where(np.abs(evals - 2.0) < 1e-4)[0]
    
    V_minus = evecs[:, idx_minus] # 16 x 3
    V_plus = evecs[:, idx_plus]   # 16 x 3
    
    print(f"V_minus shape: {V_minus.shape}, V_plus shape: {V_plus.shape}")

    # For any K(B, V), what is the projection of K onto V_minus and V_plus?
    # K[(j0, c1), (j3, c2)] = B[j0, c2] * V[j3, c1]
    def make_K(B, V):
        return np.einsum("ac,db->abdc", B, V).reshape(16, 16)

    # Let's test random B1, V1, B2, V2
    rng = np.random.default_rng(2026)
    min_rank = 16
    n_samples = 1000
    for _ in range(n_samples):
        B1 = rng.standard_normal((4, 4))
        V1 = rng.standard_normal((4, 4))
        B2 = rng.standard_normal((4, 4))
        V2 = rng.standard_normal((4, 4))
        K = make_K(B1, V1) + make_K(B2, V2)
        diff = M - K
        rk = np.linalg.matrix_rank(diff, tol=1e-7)
        if rk < min_rank:
            min_rank = rk
    print(f"Random 4x4 B, V: min rank(M - K1 - K2) observed over {n_samples} trials = {min_rank}")

    # Now test: what if we OPTIMIZE B1, V1, B2, V2 to minimize the rank of M - K1 - K2?
    # In other words, minimize the 4th singular value of M - K1 - K2:
    # If rank <= 3 is possible, then sigma_3 (0-indexed: sigma_0 >= sigma_1 >= sigma_2 >= sigma_3) must be 0!
    # Even more: sigma_3, sigma_4, sigma_5 must all be 0!
    from scipy.optimize import minimize
    def loss(p):
        B1 = p[0:16].reshape(4, 4)
        V1 = p[16:32].reshape(4, 4)
        B2 = p[32:48].reshape(4, 4)
        V2 = p[48:64].reshape(4, 4)
        K = make_K(B1, V1) + make_K(B2, V2)
        diff = M - K
        svals = np.linalg.svd(diff, compute_uv=False)
        # Tail singular values sum from index 3 to 15
        return np.sum(svals[3:]**2)

    min_loss = float('inf')
    best_svals = None
    for restart in range(15):
        p0 = rng.standard_normal(64) * 0.5
        res = minimize(loss, p0, method='BFGS', options={'maxiter': 300})
        if res.fun < min_loss:
            min_loss = res.fun
            B1 = res.x[0:16].reshape(4, 4)
            V1 = res.x[16:32].reshape(4, 4)
            B2 = res.x[32:48].reshape(4, 4)
            V2 = res.x[48:64].reshape(4, 4)
            K = make_K(B1, V1) + make_K(B2, V2)
            best_svals = np.linalg.svd(M - K, compute_uv=False)
            
    print(f"\nOptimization results over R (minimizing tail singular values svals[3:]):")
    print(f"Minimum tail loss = {min_loss:.6f}")
    print(f"Singular values at minimum:\n{np.round(best_svals, 4)}")

if __name__ == "__main__":
    test_weyl_and_projections()
