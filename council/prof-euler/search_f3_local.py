"""
Prof. Euler - High-Speed Finite Field Local Search for Case (3,2)
Testing rank(M - K(B1,V1) - K(B2,V2)) <= 3 over F_3 and F_5.
Uses hill-climbing, coordinate descent, and random walks over F_p.
"""
import time
import numpy as np
from apolar_higher_betti_probe import rank_matrix_mod
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
    return T.reshape(16, 16) % mod

def kron_swap_mod(B: np.ndarray, V: np.ndarray, mod: int = 3) -> np.ndarray:
    return (np.einsum('ac,db->abdc', B, V) % mod).reshape(16, 16)

def run_local_search_fp(mod: int = 3, n_restarts: int = 50, steps_per_restart: int = 200):
    M = build_nisan_matrix(mod)
    rng = np.random.default_rng(2026)
    
    global_min_rank = 16
    best_config = None
    rank_hist = {}
    
    t0 = time.time()
    for restart in range(n_restarts):
        # Initialize random matrices B1, V1, B2, V2
        # Use low-rank initializations as well as random dense
        if restart % 2 == 0:
            # Low rank initialization
            r = rng.integers(1, 4, size=4)
            B1 = (rng.integers(0, mod, (4, r[0])) @ rng.integers(0, mod, (r[0], 4))) % mod
            V1 = (rng.integers(0, mod, (4, r[1])) @ rng.integers(0, mod, (r[1], 4))) % mod
            B2 = (rng.integers(0, mod, (4, r[2])) @ rng.integers(0, mod, (r[2], 4))) % mod
            V2 = (rng.integers(0, mod, (4, r[3])) @ rng.integers(0, mod, (r[3], 4))) % mod
        else:
            B1 = rng.integers(0, mod, (4, 4))
            V1 = rng.integers(0, mod, (4, 4))
            B2 = rng.integers(0, mod, (4, 4))
            V2 = rng.integers(0, mod, (4, 4))
            
        K1 = kron_swap_mod(B1, V1, mod)
        K2 = kron_swap_mod(B2, V2, mod)
        cur_rank = rank_matrix_mod((M - K1 - K2) % mod, mod)
        
        mats = [B1, V1, B2, V2]
        
        for step in range(steps_per_restart):
            # Pick a random matrix and a random entry to mutate
            m_idx = rng.integers(0, 4)
            i = rng.integers(0, 4)
            j = rng.integers(0, 4)
            old_val = mats[m_idx][i, j]
            new_val = (old_val + rng.integers(1, mod)) % mod
            
            mats[m_idx][i, j] = new_val
            
            # Recompute only affected K
            if m_idx < 2:
                new_K1 = kron_swap_mod(mats[0], mats[1], mod)
                new_rank = rank_matrix_mod((M - new_K1 - K2) % mod, mod)
                if new_rank <= cur_rank:
                    cur_rank = new_rank
                    K1 = new_K1
                else:
                    mats[m_idx][i, j] = old_val
            else:
                new_K2 = kron_swap_mod(mats[2], mats[3], mod)
                new_rank = rank_matrix_mod((M - K1 - new_K2) % mod, mod)
                if new_rank <= cur_rank:
                    cur_rank = new_rank
                    K2 = new_K2
                else:
                    mats[m_idx][i, j] = old_val
                    
            if cur_rank < global_min_rank:
                global_min_rank = cur_rank
                best_config = [m.copy() for m in mats]
                print(f"[F_{mod} Restart {restart}, Step {step}] New MIN RANK: {global_min_rank}")
                if global_min_rank <= 3:
                    print("!!! SOLUTION FOUND IN F_p !!!")
                    return global_min_rank
                    
        rank_hist[cur_rank] = rank_hist.get(cur_rank, 0) + 1
        
    dt = time.time() - t0
    print(f"\nCompleted {n_restarts} restarts ({n_restarts * steps_per_restart} steps) over F_{mod} in {dt:.2f}s.")
    print(f"Global minimum rank observed: {global_min_rank}")
    print(f"Terminal rank distribution: {sorted(rank_hist.items())}")
    return global_min_rank

if __name__ == '__main__':
    print("=== PROF. EULER F_3 LOCAL SEARCH ===")
    run_local_search_fp(mod=3, n_restarts=100, steps_per_restart=150)
    print("\n=== PROF. EULER F_5 LOCAL SEARCH ===")
    run_local_search_fp(mod=5, n_restarts=50, steps_per_restart=150)
