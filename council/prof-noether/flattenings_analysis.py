"""Investigate the 3 flattenings of the permanent tensor T."""
import numpy as np

# T is 4x4x4x4
T = np.zeros((4, 4, 4, 4), dtype=float)
for j0 in range(4):
    for c1 in range(4):
        for j3 in range(4):
            for c2 in range(4):
                if len({j0, c1, j3, c2}) == 4:
                    T[j0, c1, j3, c2] = 1.0

# Flattening 1: N_01 = (j0, c1) x (j3, c2)
F1 = T.reshape(16, 16)
print("Flattening 1 (j0, c1) x (j3, c2): rank =", np.linalg.matrix_rank(F1))

# Flattening 2: F_mat = (j0, j3) x (c1, c2)
F2 = np.transpose(T, (0, 2, 1, 3)).reshape(16, 16)
print("Flattening 2 (j0, j3) x (c1, c2): rank =", np.linalg.matrix_rank(F2))

# Flattening 3: F_cross = (j0, c2) x (j3, c1)
F3 = np.transpose(T, (0, 3, 2, 1)).reshape(16, 16)
print("Flattening 3 (j0, c2) x (j3, c1): rank =", np.linalg.matrix_rank(F3))

# Now let's examine an (a, b) wire in all 3 flattenings:
# A1(a) B2(b):
# Wire k: u_{j0, c1} * w_{j3, c2}
# Tensor: T_ab = u (outer) w where u is 4x4 (j0, c1), w is 4x4 (j3, c2)
rng = np.random.default_rng(101)
u = rng.standard_normal((4, 4))
w = rng.standard_normal((4, 4))

T_ab = np.einsum('ik,jl->ikjl', u, w)
# In F1:
f1_ab = T_ab.reshape(16, 16)
# In F2:
f2_ab = np.transpose(T_ab, (0, 2, 1, 3)).reshape(16, 16)
# In F3:
f3_ab = np.transpose(T_ab, (0, 3, 2, 1)).reshape(16, 16)

print("\n(a, b) wire ranks in the 3 flattenings:")
print("F1 rank:", np.linalg.matrix_rank(f1_ab))
print("F2 rank:", np.linalg.matrix_rank(f2_ab))
print("F3 rank:", np.linalg.matrix_rank(f3_ab))

# Now let's examine a (b, a) wire:
# B1(b) A2(a):
# B_{j0, c2} * V_{j3, c1}
B = rng.standard_normal((4, 4))
V = rng.standard_normal((4, 4))
T_ba = np.einsum('il,jk->ikjl', B, V)

f1_ba = T_ba.reshape(16, 16)
f2_ba = np.transpose(T_ba, (0, 2, 1, 3)).reshape(16, 16)
f3_ba = np.transpose(T_ba, (0, 3, 2, 1)).reshape(16, 16)

print("\n(b, a) wire ranks in the 3 flattenings:")
print("F1 rank:", np.linalg.matrix_rank(f1_ba))
print("F2 rank:", np.linalg.matrix_rank(f2_ba))
print("F3 rank:", np.linalg.matrix_rank(f3_ba))

# What about the sum of 3 (a, b) wires and 2 (b, a) wires in F2?!
# In F2:
# (a, b) wire has rank = rank(u) * rank(w) <= 16, BUT what structure does it have?
# Let's check!
