"""
Prof. Euler: test_rank_reduction_c_wires.py
Can c <= 4 wires of B1(b) A2(a) ever reduce rank(M_6 - N_01(B1 A2)) to <= 19?
"""
import itertools
import numpy as np
import sys
sys.path.append('council/prof-noether')
from general_n2k_noether import build_Mn

def test_rank_reduction():
    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    sub2_to_idx = {s: i for i, s in enumerate(sub_2)}
    sub3_to_idx = {s: i for i, s in enumerate(sub_3)}
    
    print("=" * 70)
    print("CAN c <= 4 WIRES OF B1(b) A2(a) REDUCE rank(M_6 - N_01(B1 A2)) <= 19?")
    print("=" * 70)
    
    rng = np.random.default_rng(2026)
    
    # In Noether's Counterexample 1A:
    # 9 wires were used to create N_01(B1 A2) = v_{012} v_{345}^T (ONE DYAD in S_{6,3}!).
    # That was rank 1 in N_01, BUT it required 9 wires of B1 and A2!
    # What if B1 and A2 have c <= 4 wires?
    # For c <= 4 wires:
    # B1 has size (6, 15, c)
    # A2 has size (6, c, 15)
    # Then N_01(B1 A2)[(I, c1), (J, c2)] = sum_{l=0}^{c-1} B1[c2, I, l] * A2[c1, l, J]
    
    for c in [1, 2, 3, 4]:
        min_rk = 90
        for trial in range(500):
            B1 = rng.standard_normal((6, 15, c))
            A2 = rng.standard_normal((6, c, 15))
            # N01: row (I, c1), col (J, c2)
            N01 = np.einsum('dIl,clJ->IcJd', B1, A2).reshape(90, 90)
            rk = np.linalg.matrix_rank(M6 - N01)
            if rk < min_rk:
                min_rk = rk
        print(f"c = {c} wires (random): min rank(M_6 - N_01(B1 A2)) = {min_rk}")
        
    # What about structured/adversarial B1 and A2 of width c <= 4?
    # For example, what if B1 and A2 try to produce a dyad v_S v_{Sc}^T?
    # Can c <= 4 wires produce v_S v_{Sc}^T?
    # In CE1A, producing v_{012} v_{345}^T required 3 rows of B1 and 3 cols of A2,
    # which used 3 x 3 = 9 wires!
    # Can c <= 4 wires produce ANY non-zero component of M6?
    print("\nTesting whether c <= 4 wires can cancel ANY rank of M6:")
    for c in [1, 2, 3, 4]:
        # Optimize B1, A2 to minimize rank(M6 - N01) via SVD/least-squares
        # Target: cancel k dyads of M6
        # Let target be 1 dyad: v_S v_{Sc}^T
        target_dyad = np.outer(V_basis[:, 0], V_basis[:, int(np.argmax(comp_perm[0]))])
        # Best rank-c approximation in the tensor format B1 (x) A2:
        # B1 has 6*15*c = 90c params, A2 has 90c params.
        # Can N01(B1 A2) equal target_dyad for c <= 4?
        # Target dyad entry at ((I, c1), (J, c2)) is V_basis[I*6+c1, 0] * V_basis[J*6+c2, comp]
        # In N01, entry is sum_l B1[c2, I, l] A2[c1, l, J].
        # Notice: in target_dyad, variables c1 and c2 are DECOUPLED from I and J:
        # V_basis[I*6+c1, 0] is non-zero ONLY if I subset S and c1 in S.
        # For S = {0, 1, 2}, I in {(0,1), (0,2), (1,2)}, and c1 is the remaining element!
        # Thus c1 is DETERMINED by I: c1 = S \ I!
        # So target_dyad has ONLY 3 nonzero rows (I, c1) and 3 nonzero cols (J, c2)!
        # Its non-zero submatrix has shape 3 x 3, which has rank 1!
        # But in the full space, it has 9 entries.
        # How many wires does it require?
        # Wire l computes B1[c2, I, l] A2[c1, l, J].
        # Each wire l is a rank-1 outer product in ((I, c2), (J, c1))!
        # Since the 9 entries have rank 3 in ((I, c2), (J, c1)), it requires at least 3 wires?
        # Wait! In CE1A, it used 9 wires! Can it be done in 3 wires?
        pass

if __name__ == '__main__':
    test_rank_reduction()
