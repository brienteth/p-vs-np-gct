"""Prof. Hilbert - Algebraic analysis of unsplit factorizations and rank stratification.
Investigating the algebraic variety:
  A1(a) A2(a) = 0
  B1(b) B2(b) = 0
  A1(a) B2(b) + B1(b) A2(a) = P(a, b)
for 4x5 and 5x4 matrices over C.
"""
import itertools
import numpy as np
import sys
import os

# Add p-vs-np-gct path
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
from poly_exact import permanent_poly
from perm4_middle_factorization_probe import extract_middle_4x4

def main():
    p_mat = extract_middle_4x4(permanent_poly(4))
    print("Extracted P_mat 4x4 successfully.")
    
    # Check the tensor dimensions:
    # P(a, b) = sum_{c1, c2} a_{c1} b_{c2} P_{c1, c2}
    P_tensor = np.zeros((4, 4, 4, 4), dtype=int)
    for j0 in range(4):
        for j3 in range(4):
            for m, coeff in p_mat[j0][j3].items():
                # m is a tuple of 8 exponents: m[0..3] for a, m[4..7] for b
                nz_a = [k for k in range(4) if m[k] > 0]
                nz_b = [k for k in range(4) if m[4+k] > 0]
                if len(nz_a) == 1 and len(nz_b) == 1:
                    c1, c2 = nz_a[0], nz_b[0]
                    P_tensor[c1, c2, j0, j3] = coeff
                    
    print("P_tensor shape (c1, c2, j0, j3):", P_tensor.shape)
    
    # Check symmetry: P_{c1, c2, j0, j3} == P_{c2, c1, j0, j3}
    sym_ab = np.all(P_tensor == np.swapaxes(P_tensor, 0, 1))
    print("Is P symmetric in a <-> b (c1 <-> c2)?", sym_ab)
    
    # Check symmetry in j0 <-> j3
    sym_j = np.all(P_tensor == np.swapaxes(P_tensor, 2, 3))
    print("Is P symmetric in j0 <-> j3?", sym_j)
    
    # Check diagonal zero
    diag_zero = True
    for j in range(4):
        if np.any(P_tensor[:, :, j, j] != 0):
            diag_zero = False
    print("Is P zero on diagonal j0 == j3?", diag_zero)

if __name__ == "__main__":
    main()
