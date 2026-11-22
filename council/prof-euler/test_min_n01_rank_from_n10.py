"""
Prof. Euler: test_min_n01_rank_from_n10.py
Optimization and exact algebraic search for minimum rank of M_6 - T in N_01
subject to rank(T) <= c in N_10 for c = 1, 2, 3, 4.
"""
import itertools
import numpy as np
import scipy.optimize
import sys
sys.path.append('council/prof-noether')
from general_n2k_noether import build_Mn

def test_min_rank():
    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    
    print("=" * 70)
    print("MINIMUM RANK OF M_6 - T IN N_01 SUBJECT TO rank_{N_10}(T) <= c")
    print("=" * 70)
    
    # Notice: In N_10, M_6 has rank 90!
    # Because M_6 in N_10 is M6_10 = M6.reshape(15, 6, 15, 6).transpose(0, 3, 2, 1).reshape(90, 90).
    M6_10 = M6.reshape(15, 6, 15, 6).transpose(0, 3, 2, 1).reshape(90, 90)
    rk_M6_10 = np.linalg.matrix_rank(M6_10)
    print(f"Rank of M_6 in N_01: {np.linalg.matrix_rank(M6)}")
    print(f"Rank of M_6 in N_10: {rk_M6_10}")
    
    # By rank inequality on N_10:
    # rank_{N_10}(M_6 - T) >= rank_{N_10}(M_6) - rank_{N_10}(T) >= 90 - c!
    # For c <= 4: rank_{N_10}(M_6 - T) >= 90 - 4 = 86!
    print(f"By rank-nullity in N_10: for ANY tensor T with rank_{{N_10}}(T) <= c <= 4,")
    print(f"  rank_{{N_10}}(M_6 - T) >= 90 - 4 = 86!")
    
    # Now: what about in N_01?
    # In N_01, A_1(a) B_2(b) has rank <= 19!
    # And A_1(a) B_2(b) = M_6 - B_1(b) A_2(a) = M_6 - T!
    # Can a tensor of N_10-rank >= 86 have N_01-rank <= 19?
    # Let's test random and structured tensors of N_01-rank <= 19:
    # What is their N_10-rank?
    rng = np.random.default_rng(2026)
    min_N10_of_rank19 = 90
    for _ in range(100):
        # Rank-19 tensor in N_01
        U = rng.standard_normal((90, 19))
        V = rng.standard_normal((90, 19))
        T_01 = U @ V.T # 90 x 90 of N_01-rank 19
        T_10 = T_01.reshape(15, 6, 15, 6).transpose(0, 3, 2, 1).reshape(90, 90)
        rk_10 = np.linalg.matrix_rank(T_10)
        if rk_10 < min_N10_of_rank19:
            min_N10_of_rank19 = rk_10
    print(f"For random rank-19 tensors in N_01: min rank in N_10 = {min_N10_of_rank19}")

if __name__ == '__main__':
    test_min_rank()
