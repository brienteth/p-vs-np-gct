"""Prof. Wigner: Dual Flattening Rank Bounds for Case (3,2).
Can M = X + Y with rank_{F1}(X) <= 3 and rank_{F2}(Y) <= 2?
Let's test over R and C with optimization and linear algebraic probes.
"""
import numpy as np
from scipy.optimize import minimize

def test_dual_flattening():
    # Build M in (4, 4, 4, 4)
    # axes: 0: j0, 1: c1, 2: j3, 3: c2
    M = np.zeros((4, 4, 4, 4), dtype=np.float64)
    for j0 in range(4):
        for c1 in range(4):
            for j3 in range(4):
                for c2 in range(4):
                    if len({j0, c1, j3, c2}) == 4:
                        M[j0, c1, j3, c2] = 1.0

    # F1 flattening: rows (j0, c1), cols (j3, c2) -> shape (16, 16)
    M_F1 = M.reshape(16, 16)
    # F2 flattening: rows (j0, c2), cols (j3, c1) -> transpose axes (0, 3, 2, 1) then reshape (16, 16)
    M_F2 = np.transpose(M, (0, 3, 2, 1)).reshape(16, 16)
    
    assert np.allclose(M_F1, M_F2), "M must be invariant under F1 <-> F2!"
    print("M is identically symmetric under F1 <-> F2 exchange.")
    print(f"rank_{{F1}}(M) = {np.linalg.matrix_rank(M_F1)}, rank_{{F2}}(M) = {np.linalg.matrix_rank(M_F2)}")

    # Suppose M = X + Y where:
    # X has rank <= 3 in F1: X_F1 = U @ W where U is (16, 3), W is (3, 16)
    # Y has rank <= 2 in F2: Y_F2 = A @ B where A is (16, 2), B is (2, 16)
    # Then Y in F1 is obtained by transposing axes (0, 3, 2, 1):
    # Y_tensor = Y_F2.reshape(4, 4, 4, 4).transpose(0, 3, 2, 1)
    # Y_F1 = Y_tensor.reshape(16, 16)
    # Target: minimize || M_F1 - U @ W - Y_F1 ||_F^2
    
    rng = np.random.default_rng(42)
    
    def loss(p):
        U = p[:48].reshape(16, 3)
        W = p[48:96].reshape(3, 16)
        A = p[96:128].reshape(16, 2)
        B = p[128:160].reshape(2, 16)
        
        X_F1 = U @ W
        Y_F2 = A @ B
        Y_F1 = Y_F2.reshape(4, 4, 4, 4).transpose(0, 3, 2, 1).reshape(16, 16)
        
        res = M_F1 - X_F1 - Y_F1
        return np.sum(res**2)

    print("\nOptimizing M = X + Y over R (rank_F1(X) <= 3, rank_F2(Y) <= 2)...")
    min_loss = float('inf')
    best_res = None
    for trial in range(15):
        p0 = rng.standard_normal(160) * 0.5
        res = minimize(loss, p0, method='BFGS', options={'maxiter': 400})
        if res.fun < min_loss:
            min_loss = res.fun
            best_res = res
        print(f"  Trial {trial+1:2d}: loss = {res.fun:.4f}, norm_res = {np.sqrt(res.fun):.4f}")

    print(f"\nMinimum loss found: {min_loss:.6f} (residual norm = {np.sqrt(min_loss):.4f})")
    
    # Also test rank <= 3 in F1 and rank <= 3 in F2:
    def loss_33(p):
        U = p[:48].reshape(16, 3)
        W = p[48:96].reshape(3, 16)
        A = p[96:144].reshape(16, 3)
        B = p[144:192].reshape(3, 16)
        X_F1 = U @ W
        Y_F2 = A @ B
        Y_F1 = Y_F2.reshape(4, 4, 4, 4).transpose(0, 3, 2, 1).reshape(16, 16)
        res = M_F1 - X_F1 - Y_F1
        return np.sum(res**2)

    print("\nTesting rank_F1 <= 3 and rank_F2 <= 3 (Case (3,3) - width 6 Grenet regime):")
    res33 = minimize(loss_33, rng.standard_normal(192) * 0.5, method='BFGS', options={'maxiter': 500})
    print(f"Case (3,3) loss = {res33.fun:.6f} (residual norm = {np.sqrt(res33.fun):.4f})")

if __name__ == "__main__":
    test_dual_flattening()
