"""Test whether P_{u^perp}(a,b) can factor as W(b)_{3x5} A2(a)_{5x4} for any u in C^4."""
import sys
sys.path.insert(0, '/Users/bl10buer/Desktop/matemk/p-vs-np-gct')
import numpy as np
from poly_exact import permanent_poly
from perm4_middle_factorization_probe import extract_middle_4x4
from apolar_higher_betti_probe import rank_matrix_mod
from perm4_abp_frontier import MOD

perm_poly = permanent_poly(4)
p_mat = extract_middle_4x4(perm_poly)

# C[j0, j3, c1, c2] = coeff of a_c1 b_c2 in P[j0, j3]
C = np.zeros((4, 4, 4, 4), dtype=np.int64)
for j0 in range(4):
    for j3 in range(4):
        for mon, coeff in p_mat[j0][j3].items():
            c1 = [k for k in range(4) if mon[k] == 1][0]
            c2 = [k for k in range(4) if mon[4+k] == 1][0]
            C[j0, j3, c1, c2] = coeff

# For any u != 0 in F_p^4, let u^perp be spanned by gamma1, gamma2, gamma3 (3x4 matrix Gamma).
# The 3x4 matrix P_Gamma(a,b) has entries:
# (P_Gamma)_{i, j3} = sum_{j0} Gamma[i, j0] P[j0, j3](a,b)
# If P_Gamma(a,b) = W(b)_{3x5} A2(a)_{5x4}, then:
# (P_Gamma)_{i, j3} = sum_{k=1}^5 W(b)_{i, k} A2(a)_{k, j3}.
# Let us look at the tensor of coefficients of P_Gamma:
# T_Gamma[i, j3, c1, c2] = sum_{j0} Gamma[i, j0] C[j0, j3, c1, c2].
# Here c1 is the index of a, c2 is the index of b.
# If it factors as W(b) A2(a), then:
# T_Gamma[i, j3, c1, c2] = sum_{k=1}^5 W_{i, k, c2} A2_{k, j3, c1}.
# Look at the grouping of indices:
# Group 1 (depends on b and row index i): (i, c2) in {0..2} x {0..3} -> 12 indices.
# Group 2 (depends on a and col index j3): (j3, c1) in {0..3} x {0..3} -> 16 indices.
# This is a matrix of size 12 x 16 (or 16 x 12)!
# In this matrix, entry ((i, c2), (j3, c1)) is:
# sum_{k=1}^5 W_{i, k, c2} A2_{k, j3, c1}.
# THIS MATRIX HAS INNER DIMENSION k in {1..5}, SO ITS RANK IS AT MOST 5!
# Let us check: for EVERY nonzero u in F_p^4, what is the rank of this 12x16 matrix?!

print("Testing rank of flattening across all u in F_p^4...")
# Let us test random u over MOD:
rng = np.random.default_rng(42)
min_rank_observed = 999
for trial in range(100):
    u = rng.integers(0, MOD, size=4)
    if np.all(u == 0):
        continue
    # Find basis for u^perp:
    # 1x4 matrix u^T, nullspace over MOD
    from euler_w5_obstruction_proof import kernel_left_basis
    gamma = kernel_left_basis(u, MOD) # 3x4 matrix
    assert gamma.shape == (3, 4)
    
    # Construct 12 x 16 matrix:
    # row index: (i, c2) = i*4 + c2, col index: (j3, c1) = j3*4 + c1
    mat_12x16 = np.zeros((12, 16), dtype=np.int64)
    for i in range(3):
        for c2 in range(4):
            for j3 in range(4):
                for c1 in range(4):
                    val = 0
                    for j0 in range(4):
                        val += gamma[i, j0] * C[j0, j3, c1, c2]
                    mat_12x16[i * 4 + c2, j3 * 4 + c1] = val % MOD
    
    r = rank_matrix_mod(mat_12x16, MOD)
    if r < min_rank_observed:
        min_rank_observed = r
    if trial < 5:
        print(f"Trial {trial}: rank = {r}")

print(f"Minimum rank observed across 100 random u: {min_rank_observed}")
