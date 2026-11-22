"""Check Kronecker structure of F2."""
import numpy as np

rng = np.random.default_rng(202)
U = rng.standard_normal((4, 4))
W = rng.standard_normal((4, 4))
B = rng.standard_normal((4, 4))
V = rng.standard_normal((4, 4))

# (a, b) wire in F2:
# T_ab[j0, c1, j3, c2] = U[j0, c1] * W[j3, c2]
# F2 has row (j0, j3) and col (c1, c2)
F2_ab = np.zeros((16, 16))
for j0 in range(4):
    for j3 in range(4):
        for c1 in range(4):
            for c2 in range(4):
                F2_ab[j0*4 + j3, c1*4 + c2] = U[j0, c1] * W[j3, c2]

# Is F2_ab == np.kron(U, W) ?
# np.kron(U, W)[j0*4 + j3, c1*4 + c2] = U[j0, c1] * W[j3, c2]
kron_UW = np.kron(U, W)
print("F2_ab == kron(U, W):", np.allclose(F2_ab, kron_UW))

# (b, a) wire in F2:
# T_ba[j0, c1, j3, c2] = B[j0, c2] * V[j3, c1]
F2_ba = np.zeros((16, 16))
for j0 in range(4):
    for j3 in range(4):
        for c1 in range(4):
            for c2 in range(4):
                F2_ba[j0*4 + j3, c1*4 + c2] = B[j0, c2] * V[j3, c1]

# Notice F2_ba has col (c1, c2), where c1 couples with j3 (V) and c2 couples with j0 (B).
# If we swap c1 and c2 in col, it is kron(B, V)!
# Let Sigma be the column swap matrix:
Sigma = np.zeros((16, 16))
for c1 in range(4):
    for c2 in range(4):
        Sigma[c1*4 + c2, c2*4 + c1] = 1.0

# If we swap rows (j0, j3) -> (j3, j0) and cols (c1, c2):
# Let's check:
kron_VB = np.kron(B, V) # row (j0, j3), col (c2, c1)
print("F2_ba == kron(B, V) @ Sigma:", np.allclose(F2_ba, kron_VB @ Sigma))
