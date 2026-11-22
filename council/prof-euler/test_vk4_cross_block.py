"""
Prof. Euler: test_vk4_cross_block.py
Analyze the Cross-Nisan subblock rank of M_6 on the complementary block of V_{K_4} (vertices {4, 5}).
"""
import itertools
import numpy as np
import sys
sys.path.append('council/prof-noether')
from general_n2k_noether import build_Mn

def test_vk4_block():
    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    sub2_to_idx = {s: i for i, s in enumerate(sub_2)}
    
    print("=" * 70)
    print("ANALYSIS OF V_{K_4} (k = 6) CROSS-BLOCK NISAN OBSTRUCTION")
    print("=" * 70)
    
    # Vertices {0, 1, 2, 3} form K_4. The 6 edges of K_4 are:
    edges_k4 = [sub2_to_idx[e] for e in itertools.combinations(range(4), 2)]
    # The complementary vertices are {4, 5}. The 9 remaining edges of K_6 are:
    edges_other = [i for i in range(15) if i not in edges_k4]
    
    print(f"K_4 edges ({len(edges_k4)}): {[sub_2[i] for i in edges_k4]}")
    print(f"Other edges ({len(edges_other)}): {[sub_2[i] for i in edges_other]}")
    
    # In Cross-Nisan flattening N_{10}(P_6):
    # row index: (I, c2) where I in C(6, 2), c2 in 0..5
    # col index: (J, c1) where J in C(6, 2), c1 in 0..5
    # For A_1 supported on W_{K_4} (10 dimensions, edges containing at least one vertex in {0,1,2,3}):
    # Notice: the ONLY edges disjoint from {0,1,2,3} is {4, 5}!
    # Edge {4, 5} is the unique edge strictly outside {0, 1, 2, 3}!
    idx_45 = sub2_to_idx[(4, 5)]
    
    # What is the submatrix of M_6 on row edge {4, 5} and column edges in K_4?
    # M_6 has rows (I, c1), cols (J, c2).
    # Submatrix on I = {4, 5} (6 rows for c1 in 0..5):
    sub_I45 = M6[idx_45 * 6 : (idx_45 + 1) * 6, :]
    rk_I45 = np.linalg.matrix_rank(sub_I45)
    print(f"Rank of M_6 on row edge {{4, 5}} (6 x 90): {rk_I45}")
    
    # And on col edge {4, 5} (6 cols for c2 in 0..5):
    sub_J45 = M6[:, idx_45 * 6 : (idx_45 + 1) * 6]
    rk_J45 = np.linalg.matrix_rank(sub_J45)
    print(f"Rank of M_6 on col edge {{4, 5}} (90 x 6): {rk_J45}")
    
    # Submatrix on row edges in K_4 and col edge {4, 5}:
    # Shape is (6 * 6, 6) = (36, 6)
    rows_k4 = []
    for e in edges_k4:
        rows_k4.extend(range(e * 6, (e + 1) * 6))
    cols_45 = list(range(idx_45 * 6, (idx_45 + 1) * 6))
    
    blk_k4_45 = M6[np.ix_(rows_k4, cols_45)]
    print(f"Shape of M_6[K_4 edges, {{4, 5}}]: {blk_k4_45.shape}, rank: {np.linalg.matrix_rank(blk_k4_45)}")
    print("Matrix entries:\n", blk_k4_45)

if __name__ == '__main__':
    test_vk4_block()
