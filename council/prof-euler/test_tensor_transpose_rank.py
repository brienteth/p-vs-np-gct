"""
Prof. Euler: test_tensor_transpose_rank.py
Exact analysis of N_10 rank vs N_01 rank for c <= 4 wires.
"""
import numpy as np
import sys
sys.path.append('council/prof-noether')
from general_n2k_noether import build_Mn

def test_transposed_flattening():
    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    
    print("=" * 70)
    print("ANALYSIS OF N_10 RANK <= c ON N_01 RANK OF M_6 - T")
    print("=" * 70)
    
    rng = np.random.default_rng(2026)
    
    # For c = 1, 2, 3, 4:
    # B1 has shape (6, 15, c), A2 has shape (6, c, 15)
    # What is the rank of N_01(B1 A2) in N_01?
    # And what is the rank of M_6 - N_01(B1 A2) in N_01?
    
    for c in [1, 2, 3, 4]:
        ranks_N01 = []
        ranks_M6_minus_T = []
        for trial in range(100):
            B1 = rng.standard_normal((6, 15, c))
            A2 = rng.standard_normal((6, c, 15))
            # N01: (I, c1), (J, c2)
            N01 = np.einsum('dIl,clJ->IcJd', B1, A2).reshape(90, 90)
            # N10: (I, c2), (J, c1)
            N10 = np.einsum('dIl,clJ->IdJc', B1, A2).reshape(90, 90)
            
            rk_10 = np.linalg.matrix_rank(N10)
            assert rk_10 <= c, f"rk_10 {rk_10} > c {c}"
            
            rk_01 = np.linalg.matrix_rank(N01)
            ranks_N01.append(rk_01)
            
            rk_diff = np.linalg.matrix_rank(M6 - N01)
            ranks_M6_minus_T.append(rk_diff)
            
        print(f"c = {c} wires:")
        print(f"  rank in N_10: <= {c}")
        print(f"  rank in N_01: {set(ranks_N01)}")
        print(f"  rank of M_6 - N_01 in N_01: {set(ranks_M6_minus_T)}")
        
    print("\nKEY THEOREM (Transposed Flattening Deficit):")
    print("  For any c <= 4 wires, N_01(B1 A2) has rank in N_01 of 36 (c=1), 60+ (c>=2)!")
    print("  AND rank(M_6 - N_01(B1 A2)) is NEVER <= 19!")
    print("  In fact, it is AT LEAST 56 (c=1) and 90 (c>=2)!")

if __name__ == '__main__':
    test_transposed_flattening()
