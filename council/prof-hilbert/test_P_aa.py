"""Test if P(a, a) can be factored as L1(a)_{4x5} * L2(a)_{5x4}.
P(a, a) has entries P(a, a)_{j0, j3} = 2 (a0 a1 a2 a3)(1 - delta_{j0, j3}) / (a_{j0} a_{j3}).
"""
import numpy as np
import sys
import os

sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
from poly_exact import permanent_poly
from perm4_middle_factorization_probe import extract_middle_4x4

def get_P_aa_tensor():
    p_mat = extract_middle_4x4(permanent_poly(4))
    # 10 quadratic monomials in 4 variables a0..a3:
    # (i, j) for 0 <= i <= j < 4
    monoms = []
    for i in range(4):
        for j in range(i, 4):
            monoms.append((i, j))
    monom_to_idx = {m: idx for idx, m in enumerate(monoms)}
    
    T = np.zeros((10, 4, 4), dtype=np.float64)
    for j0 in range(4):
        for j3 in range(4):
            for m, coeff in p_mat[j0][j3].items():
                # m has 8 elements: m[0..3] for a, m[4..7] for b
                # setting b = a:
                # the monomial becomes a_c1 * a_c2
                nz_a = [k for k in range(4) if m[k] > 0]
                nz_b = [k for k in range(4) if m[4+k] > 0]
                if len(nz_a) == 1 and len(nz_b) == 1:
                    c1, c2 = sorted([nz_a[0], nz_b[0]])
                    idx = monom_to_idx[(c1, c2)]
                    T[idx, j0, j3] += coeff
    return T, monoms

def run_lm_aa(w=5, n_starts=15):
    T, monoms = get_P_aa_tensor()
    print(f"Testing factorization of P(a, a) with w = {w}...")
    # L1 has shape (4, 4, w): 4 vars, 4 rows, w cols
    # L2 has shape (4, w, 4): 4 vars, w rows, 4 cols
    # L1(a) L2(a) = sum_{k=0}^3 a_k L1_k sum_{l=0}^3 a_l L2_l
    # = sum_{k} a_k^2 L1_k L2_k + sum_{k < l} a_k a_l (L1_k L2_l + L1_l L2_k)
    
    dim_vars = 4 * 4 * w + 4 * w * 4 # 80 + 80 = 160
    best_res = float("inf")
    
    for start in range(n_starts):
        # Initialize randomly
        theta = np.random.randn(dim_vars) * 0.5
        lam = 1e-3
        for it in range(250):
            U = theta[:4*4*w].reshape(4, 4, w)
            V = theta[4*4*w:].reshape(4, w, 4)
            
            # Predict
            pred = np.zeros((10, 4, 4))
            for idx, (k, l) in enumerate(monoms):
                if k == l:
                    pred[idx] = U[k] @ V[k]
                else:
                    pred[idx] = U[k] @ V[l] + U[l] @ V[k]
            res = (pred - T).flatten()
            norm = np.linalg.norm(res)
            
            if norm < 1e-8:
                best_res = min(best_res, norm)
                print(f"Start {start}: SOLVED! norm = {norm:.4e}")
                return True
                
            # Jacobian: (160, 160)
            J_U = np.zeros((10, 4, 4, 4, 4, w))
            J_V = np.zeros((10, 4, 4, 4, w, 4))
            for idx, (k, l) in enumerate(monoms):
                if k == l:
                    for i in range(4):
                        J_U[idx, i, :, k, i, :] += V[k].T
                    for j in range(4):
                        J_V[idx, :, j, k, :, j] += U[k]
                else:
                    for i in range(4):
                        J_U[idx, i, :, k, i, :] += V[l].T
                        J_U[idx, i, :, l, i, :] += V[k].T
                    for j in range(4):
                        J_V[idx, :, j, l, :, j] += U[k]
                        J_V[idx, :, j, k, :, j] += U[l]
                        
            J = np.concatenate([J_U.reshape(160, 4*4*w), J_V.reshape(160, 4*w*4)], axis=1)
            
            g = J.T @ res
            H = J.T @ J + lam * np.eye(dim_vars)
            try:
                dtheta = np.linalg.solve(H, -g)
            except np.linalg.LinAlgError:
                break
                
            new_theta = theta + dtheta
            new_U = new_theta[:4*4*w].reshape(4, 4, w)
            new_V = new_theta[4*4*w:].reshape(4, w, 4)
            new_pred = np.zeros((10, 4, 4))
            for idx, (k, l) in enumerate(monoms):
                if k == l:
                    new_pred[idx] = new_U[k] @ new_V[k]
                else:
                    new_pred[idx] = new_U[k] @ new_V[l] + new_U[l] @ new_V[k]
            new_res = (new_pred - T).flatten()
            new_norm = np.linalg.norm(new_res)
            
            if new_norm < norm:
                theta = new_theta
                lam = max(lam * 0.5, 1e-8)
                if new_norm < 1e-8:
                    print(f"Start {start}: SOLVED! norm = {new_norm:.4e}")
                    return True
            else:
                lam = min(lam * 4.0, 1e6)
                
        best_res = min(best_res, norm)
        print(f"Start {start}: final norm = {norm:.4f}")
        
    print(f"Best residual for w={w}: {best_res:.4f}")
    return False

if __name__ == "__main__":
    np.random.seed(42)
    # First test w=6 (should be solvable by Grenet)
    run_lm_aa(w=6, n_starts=3)
    # Then test w=5
    run_lm_aa(w=5, n_starts=10)
