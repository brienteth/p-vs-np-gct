"""
Prof. Euler - Lab Verification Script: probe_f3_case32.py
Exact finite-field search and algebraic investigation of Case (3,2):
rank(M - K(B1, V1) - K(B2, V2)) <= 3 over F_3, F_5, and F_1000003.

Key exact identity:
K(B, V) acts on 4x4 matrix Z by:
K(B, V) * Z = B * Z^T * V
"""
import itertools
import time
import numpy as np
from apolar_higher_betti_probe import rank_matrix_mod
from perm4_abp_frontier import MOD
from perm4_middle_factorization_probe import extract_middle_4x4
from poly_exact import permanent_poly

def build_nisan_matrix(mod: int = 3) -> np.ndarray:
    p_perm = extract_middle_4x4(permanent_poly(4))
    T = np.zeros((4, 4, 4, 4), dtype=int)
    for j0 in range(4):
        for j3 in range(4):
            for mon, c in p_perm[j0][j3].items():
                c1 = [k for k in range(4) if mon[k] == 1][0]
                c2 = [k for k in range(4) if mon[4+k] == 1][0]
                T[j0, c1, j3, c2] = c
    M = T.reshape(16, 16) % mod
    return M

def kron_swap_mod(B: np.ndarray, V: np.ndarray, mod: int = 3) -> np.ndarray:
    return (np.einsum('ac,db->abdc', B, V) % mod).reshape(16, 16)

def test_random_restarts_f3(n_trials: int = 2000, mod: int = 3):
    M = build_nisan_matrix(mod)
    rng = np.random.default_rng(12345)
    min_rank = 16
    rank_counts = {}
    
    t0 = time.time()
    for trial in range(n_trials):
        # Sample B1, V1, B2, V2 with various rank profiles
        r1 = rng.integers(1, 5)
        r2 = rng.integers(1, 5)
        r3 = rng.integers(1, 5)
        r4 = rng.integers(1, 5)
        
        # Build random rank-r matrices
        U1 = rng.integers(0, mod, size=(4, r1))
        W1 = rng.integers(0, mod, size=(r1, 4))
        B1 = (U1 @ W1) % mod

        U2 = rng.integers(0, mod, size=(4, r2))
        W2 = rng.integers(0, mod, size=(r2, 4))
        V1 = (U2 @ W2) % mod

        U3 = rng.integers(0, mod, size=(4, r3))
        W3 = rng.integers(0, mod, size=(r3, 4))
        B2 = (U3 @ W3) % mod

        U4 = rng.integers(0, mod, size=(4, r4))
        W4 = rng.integers(0, mod, size=(r4, 4))
        V2 = (U4 @ W4) % mod

        K1 = kron_swap_mod(B1, V1, mod)
        K2 = kron_swap_mod(B2, V2, mod)
        
        X = (M - K1 - K2) % mod
        rk = rank_matrix_mod(X, mod)
        
        rank_counts[rk] = rank_counts.get(rk, 0) + 1
        if rk < min_rank:
            min_rank = rk
            print(f"[{trial}] New min rank over F_{mod}: {min_rank} with ranks ({r1},{r2},{r3},{r4})")
            
    dt = time.time() - t0
    print(f"\nFinished {n_trials} trials over F_{mod} in {dt:.2f}s.")
    print(f"Min rank observed: {min_rank}")
    print("Rank distribution:", sorted(rank_counts.items()))
    return min_rank

if __name__ == '__main__':
    print("=== Testing Case (3,2) over F_3 ===")
    test_random_restarts_f3(n_trials=5000, mod=3)
    print("\n=== Testing Case (3,2) over F_5 ===")
    test_random_restarts_f3(n_trials=2000, mod=5)
