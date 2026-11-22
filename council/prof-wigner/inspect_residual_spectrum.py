"""Prof. Wigner: Spectral and Irrep decomposition of the universal residual floor R."""
import numpy as np
from scipy.optimize import minimize

def inspect_residual():
    M = np.zeros((4, 4, 4, 4), dtype=np.float64)
    for j0 in range(4):
        for c1 in range(4):
            for j3 in range(4):
                for c2 in range(4):
                    if len({j0, c1, j3, c2}) == 4:
                        M[j0, c1, j3, c2] = 1.0

    M_F1 = M.reshape(16, 16)
    
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

    rng = np.random.default_rng(42)
    # Start near the best point
    best_res = None
    min_loss = float('inf')
    for trial in range(10):
        p0 = rng.standard_normal(160) * 0.5
        res = minimize(loss, p0, method='BFGS', options={'maxiter': 500})
        if res.fun < min_loss:
            min_loss = res.fun
            best_res = res

    p = best_res.x
    U = p[:48].reshape(16, 3)
    W = p[48:96].reshape(3, 16)
    A = p[96:128].reshape(16, 2)
    B = p[128:160].reshape(2, 16)
    X_F1 = U @ W
    Y_F2 = A @ B
    Y_F1 = Y_F2.reshape(4, 4, 4, 4).transpose(0, 3, 2, 1).reshape(16, 16)
    R_F1 = M_F1 - X_F1 - Y_F1

    print(f"Optimal residual Frobenius norm: {np.linalg.norm(R_F1):.6f}")
    print(f"Optimal residual Frobenius norm squared: {np.sum(R_F1**2):.6f}")

    # SVD of R_F1
    svals_R = np.linalg.svd(R_F1, compute_uv=False)
    print("Singular values of R_F1:\n", np.round(svals_R, 5))

    # Check symmetry of R_F1
    sym_err = np.max(np.abs(R_F1 - R_F1.T))
    print(f"Symmetry error ||R - R^T||_max = {sym_err:.4f}")

    # Check projection of R_F1 onto Sym_0(4)
    # Basis of Sym_0(4):
    def make_E(i, j):
        E = np.zeros((4, 4))
        E[i, j] = 1.0
        E[j, i] = 1.0
        return E

    basis = [
        (make_E(0, 1) + make_E(2, 3)) / 2.0,
        (make_E(0, 2) + make_E(1, 3)) / 2.0,
        (make_E(0, 3) + make_E(1, 2)) / 2.0,
        (make_E(0, 1) - make_E(2, 3)) / 2.0,
        (make_E(0, 2) - make_E(1, 3)) / 2.0,
        (make_E(0, 3) - make_E(1, 2)) / 2.0,
    ]
    basis_vecs = np.stack([b.reshape(16) for b in basis], axis=1) # 16 x 6
    P_sym0 = basis_vecs @ basis_vecs.T # 16 x 16 projector onto Sym_0(4)
    R_sym0 = P_sym0 @ R_F1 @ P_sym0
    norm_in_sym0 = np.linalg.norm(R_sym0)
    print(f"Frobenius norm of R projected into Sym_0(4) otimes Sym_0(4): {norm_in_sym0:.6f}")
    print(f"Fraction of residual norm in Sym_0(4): {norm_in_sym0 / np.linalg.norm(R_F1):.4f}")

if __name__ == "__main__":
    inspect_residual()
