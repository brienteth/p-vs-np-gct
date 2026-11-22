"""Compute Jacobian rank and investigate tangent space / variety dimension
for the system:
  (1) A1(a) A2(a) = 0  (160 eqs)
  (2) B1(b) B2(b) = 0  (160 eqs)
  (3) A1(a) B2(b) + B1(b) A2(a) = P(a,b)  (256 eqs)
Total: 576 equations in 320 variables.
"""
import numpy as np
import sys
import os

sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
from perm4_middle_factorization_probe import extract_middle_4x4
from poly_exact import permanent_poly
from perm4_w5_factorization_search import build_target_tensor, residual_and_jacobian

def test_jacobian_ranks():
    p_mat = extract_middle_4x4(permanent_poly(4))
    T, pairs2 = build_target_tensor(p_mat)
    
    # 576 equations, 320 variables
    # Let us sample several random points in C^320 and compute the rank of J (576 x 320)
    ranks = []
    for _ in range(5):
        theta = np.random.randn(320) + 1j * np.random.randn(320)
        r, J = residual_and_jacobian(theta, 5, T, pairs2)
        # J has shape (576, 320)
        s = np.linalg.svd(J, compute_uv=False)
        rank_J = int(np.sum(s > 1e-10))
        ranks.append(rank_J)
        
    print("Generic Jacobian rank of the full 576x320 system at random points:", ranks)
    print("Number of variables:", 320)
    print("Gauge group GL_5 dimension:", 25)
    print("Expected max rank:", 320 - 25, "= 295")

if __name__ == "__main__":
    test_jacobian_ranks()
