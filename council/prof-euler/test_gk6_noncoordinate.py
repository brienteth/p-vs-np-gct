"""
Prof. Euler: test_gk6_noncoordinate.py
Exhaustive verification of dim(im(G_6) cap (W x K^6)) for 500 random non-coordinate subspaces W of dim d = 1..14.
"""
import itertools
import numpy as np
import sys
sys.path.append('council/prof-noether')
from general_n2k_noether import build_Mn

def test_gk6_noncoordinate():
    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    # V_basis is 90 x 20
    
    rng = np.random.default_rng(2026)
    
    print("=" * 70)
    print("GK_6 NON-COORDINATE SUBSPACE TEST: dim(im(G_6) cap (W x K^6))")
    print("=" * 70)
    
    # Compare with coordinate drops (GK_6 table):
    # In coordinate case (subsets of size d):
    # What are the max coordinate values of delta(W)?
    # Let's compute both:
    print(f"{'d = dim(W)':<12} | {'Max Random delta(W)':<22} | {'Max Coord delta(W)':<20} | {'GK_6 Bound':<15}")
    print("-" * 75)
    
    for d in range(1, 15):
        # 1. Random non-coordinate subspaces: 50 trials per d
        max_rand = -1
        for _ in range(50):
            W = rng.standard_normal((15, d))
            u_orth, _, _ = np.linalg.svd(W)
            Gamma = u_orth[:, d:].T # (15-d) x 15
            H = np.kron(Gamma, np.eye(6)) @ V_basis # (6*(15-d)) x 20
            rk = np.linalg.matrix_rank(H, tol=1e-7)
            delta = 20 - rk
            if delta > max_rand:
                max_rand = delta
                
        # 2. Coordinate subspaces: sample 200 combinations
        max_coord = -1
        n_combs = len(list(itertools.combinations(range(15), d)))
        for edges in itertools.islice(itertools.combinations(range(15), d), 300):
            drop = [i for i in range(15) if i not in edges]
            Gamma = np.zeros((15 - d, 15))
            for r, row_idx in enumerate(drop):
                Gamma[r, row_idx] = 1.0
            H = np.kron(Gamma, np.eye(6)) @ V_basis
            rk = np.linalg.matrix_rank(H, tol=1e-7)
            delta = 20 - rk
            if delta > max_coord:
                max_coord = delta
                
        print(f"{d:<12} | {max_rand:<22} | {max_coord:<20} | {max(0, d - 0):<15}")

if __name__ == '__main__':
    test_gk6_noncoordinate()
