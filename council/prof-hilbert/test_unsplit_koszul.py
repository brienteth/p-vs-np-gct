"""Test whether the alternating (Koszul) part of A1*A2 can be non-zero
in any solution to M1(a,b) M2(a,b) = P_perm(a,b).
We check whether A1_i A2_j = -A1_j A2_i can be non-zero when combined with:
  A1_i B2_j + B1_j A2_i = P_{i, j}.
"""
import numpy as np
import sys
import os

sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
from poly_exact import permanent_poly
from perm4_middle_factorization_probe import extract_middle_4x4
from perm4_w5_factorization_search import build_target_tensor

def main():
    p_mat = extract_middle_4x4(permanent_poly(4))
    T, pairs = build_target_tensor(p_mat)
    # T has shape (36, 4, 4) for the 36 pairs (a, b) with 0 <= a <= b < 8
    # Variables: 0..3 are a_0..a_3, 4..7 are b_0..b_3.
    # In P_perm, all entries for (a, a) pairs (0..3, 0..3) are ZERO!
    # All entries for (b, b) pairs (4..7, 4..7) are ZERO!
    # Only cross pairs (a_i, b_j) with i in 0..3, j in 4..7 have non-zero entries in T!
    
    print("Verifying target tensor T:")
    for k, (a, b) in enumerate(pairs):
        if (a < 4 and b < 4) or (a >= 4 and b >= 4):
            assert np.all(T[k] == 0), f"Expected 0 for pair {(a, b)}, got {T[k]}"
    print("Confirmed: T has ZERO on all pure (a, a) and pure (b, b) pairs!")

if __name__ == "__main__":
    main()
