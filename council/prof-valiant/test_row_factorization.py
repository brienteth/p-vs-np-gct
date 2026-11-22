"""Test whether gamma^T P(a,b) can factor as w(b)^T A2(a)."""
import sys
sys.path.insert(0, '/Users/bl10buer/Desktop/matemk/p-vs-np-gct')
import numpy as np
from poly_exact import Poly, partial_deriv
from perm4_middle_factorization_probe import extract_middle_4x4
from poly_exact import permanent_poly

perm_poly = permanent_poly(4)
p_mat = extract_middle_4x4(perm_poly)

for j0 in range(4):
    print(f"Row {j0}:")
    for j3 in range(4):
        poly_ij = p_mat[j0][j3]
        terms = []
        for mon, coeff in poly_ij.items():
            a_vars = [f"a_{k}" for k in range(4) if mon[k] == 1]
            b_vars = [f"b_{k}" for k in range(4) if mon[4+k] == 1]
            terms.append(f"{coeff}*{a_vars[0]}*{b_vars[0]}")
        print(f"  P[{j0},{j3}] = {' + '.join(terms) if terms else '0'}")
