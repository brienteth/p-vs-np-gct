"""Analyze the operator Phi(Y) = B1 Y^T V1 + B2 Y^T V2.
Can Phi annihilate a 7-dimensional subspace of Skew(4) + Diag(4)
AND simultaneously agree with M on a 3-dimensional subspace of Sym_0(4)?"""
import numpy as np

# Basis of Skew(4) + Diag(4) (dim 10):
# 4 diagonals: E_ii
# 6 skews: E_ij - E_ji for i < j
basis_perp = []
for i in range(4):
    E = np.zeros((4, 4))
    E[i, i] = 1.0
    basis_perp.append(E)
for i in range(4):
    for j in range(i+1, 4):
        E = np.zeros((4, 4))
        E[i, j] = 1.0
        E[j, i] = -1.0
        basis_perp.append(E)

# Sym_0(4) basis (dim 6):
# E_ij + E_ji for i < j
basis_sym0 = []
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
for i, j in pairs:
    E = np.zeros((4, 4))
    E[i, j] = 1.0
    E[j, i] = 1.0
    basis_sym0.append(E)

print("Dim perp:", len(basis_perp))
print("Dim sym0:", len(basis_sym0))

# What is Phi restricted to Diag(4)?
# For Y = E_ii, Y^T = E_ii.
# Phi(E_ii) = B1 E_ii V1 + B2 E_ii V2 = (col i of B1)(row i of V1) + (col i of B2)(row i of V2).
# Notice: Phi(E_ii) is a sum of two rank-1 matrices!
# For Y = E_ij - E_ji, Y^T = -Y:
# Phi(E_ij - E_ji) = -(B1 (E_ij - E_ji) V1 + B2 (E_ij - E_ji) V2).
