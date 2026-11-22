"""Check the rank of T(u) and whether rank(T(u)) <= 2 can ever happen."""
import numpy as np
from scipy.optimize import minimize

def check_min_rank_Tu():
    rng = np.random.default_rng(42)
    # Target tensor M
    M = np.zeros((4, 4, 4, 4), dtype=np.float64)
    for j0 in range(4):
        for c1 in range(4):
            for j3 in range(4):
                for c2 in range(4):
                    if len({j0, c1, j3, c2}) == 4:
                        M[j0, c1, j3, c2] = 1.0

    for test_idx in range(5):
        a = rng.standard_normal(4)
        a /= np.linalg.norm(a)
        
        # We want to minimize the 3rd and 4th singular values of T(u) over ||u|| = 1.
        # If rank <= 2 is possible, the 2nd smallest singular value sigma_2 (0-indexed: sigma_0 >= sigma_1 >= sigma_2 >= sigma_3)
        # must be 0!
        
        def loss(u):
            u_norm = u / np.linalg.norm(u)
            T_u = np.einsum("j,c,jckf->kf", u_norm, a, M)
            svals = np.linalg.svd(T_u, compute_uv=False)
            # return sum of smallest two singular values: sigma_2^2 + sigma_3^2
            return svals[2]**2 + svals[3]**2

        min_val = float('inf')
        for start in range(20):
            u0 = rng.standard_normal(4)
            u0 /= np.linalg.norm(u0)
            res = minimize(loss, u0, method='BFGS')
            if res.fun < min_val:
                min_val = res.fun
                best_u = res.x / np.linalg.norm(res.x)
                
        T_best = np.einsum("j,c,jckf->kf", best_u, a, M)
        svals_best = np.linalg.svd(T_best, compute_uv=False)
        print(f"Sample a #{test_idx}: min (sigma_2^2 + sigma_3^2) = {min_val:.6f}")
        print(f"Singular values at minimum: {svals_best}")

if __name__ == "__main__":
    check_min_rank_Tu()
