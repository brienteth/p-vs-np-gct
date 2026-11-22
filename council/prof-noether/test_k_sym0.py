"""Analyze symmetrizations of K(B, V) and projections to Sym_0(4)."""
import numpy as np

def make_M():
    M = np.zeros((16, 16), dtype=float)
    for j0 in range(4):
        for c1 in range(4):
            for j3 in range(4):
                for c2 in range(4):
                    if len({j0, c1, j3, c2}) == 4:
                        M[j0*4 + c1, j3*4 + c2] = 1.0
    return M

def make_K(B, V):
    K = np.zeros((16, 16), dtype=float)
    for j0 in range(4):
        for c1 in range(4):
            for j3 in range(4):
                for c2 in range(4):
                    K[j0*4 + c1, j3*4 + c2] = B[j0, c2] * V[j3, c1]
    return K

# Swap matrix Sigma
Sigma = np.zeros((16, 16), dtype=float)
for i in range(4):
    for j in range(4):
        Sigma[i*4 + j, j*4 + i] = 1.0

# Basis of Sym_0(4) as 16x6 matrix S0
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
S0 = np.zeros((16, 6), dtype=float)
for col, (i, j) in enumerate(pairs):
    S0[i*4 + j, col] = 1.0
    S0[j*4 + i, col] = 1.0
# Orthonormal basis for Sym_0(4):
# Notice each column has norm sqrt(2), columns are orthogonal
S0_ortho = S0 / np.sqrt(2.0)

# Projector onto Sym_0(4) in R^16:
P_Sym0 = S0_ortho @ S0_ortho.T

M = make_M()
print("M in Sym_0 basis:")
# M_in_Sym0: S0_ortho^T @ M @ S0_ortho
M_in_Sym0 = S0_ortho.T @ M @ S0_ortho
print(np.round(M_in_Sym0, 2))

# What is P_Sym0 @ K(B, V) @ P_Sym0?
# In Sym_0 basis, it is:
# K_in_Sym0(B, V) = S0_ortho^T @ K(B, V) @ S0_ortho (a 6x6 matrix!)
rng = np.random.default_rng(123)
for trial in range(3):
    B = rng.standard_normal((4, 4))
    V = rng.standard_normal((4, 4))
    K = make_K(B, V)
    K_sym0 = S0_ortho.T @ K @ S0_ortho
    print(f"\nTrial {trial}:")
    print("rank(K):", np.linalg.matrix_rank(K))
    print("rank(K_sym0):", np.linalg.matrix_rank(K_sym0))
    print("K_sym0 singular values:", np.round(np.linalg.svd(K_sym0, compute_uv=False), 3))
