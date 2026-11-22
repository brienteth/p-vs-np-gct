"""Probe whether A1(a) A2(a') must be zero in any solution to the 576-equation system.
We set up an optimization or Gröbner-style check over F_p or C.
"""
import numpy as np
import sys
import os

sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
from perm4_middle_factorization_probe import extract_middle_4x4
from poly_exact import permanent_poly
from perm4_w5_factorization_search import build_target_tensor

def check_skew_syzygies():
    p_mat = extract_middle_4x4(permanent_poly(4))
    T, pairs2 = build_target_tensor(p_mat)
    
    # Let us check Grenet w=6 first:
    # Does Grenet w=6 have A1(a) A2(a') == 0?
    from perm4_w5_factorization_search import grenet_w6_factors
    U, V = grenet_w6_factors()
    # U has shape (8, 4, 6), V has shape (8, 6, 4)
    # Vars 0..3 are a, 4..7 are b.
    # A1 is U[:4], A2 is V[:4]
    # Let us compute A1(a) A2(a') for random a, a':
    for _ in range(5):
        a = np.random.randn(4)
        aprime = np.random.randn(4)
        A1_a = sum(a[i] * U[i] for i in range(4))
        A2_aprime = sum(aprime[i] * V[i] for i in range(4))
        prod = A1_a @ A2_aprime
        norm = np.linalg.norm(prod)
        print("Grenet w=6: ||A1(a) A2(aprime)|| =", norm)
        
if __name__ == "__main__":
    check_skew_syzygies()
