"""Analyze K(B, V) under S_4 and Sym_0(4) projectors."""
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

M = make_M()
print("Rank of M:", np.linalg.matrix_rank(M))

# Random B, V
rng = np.random.default_rng(42)
for trial in range(5):
    B1 = rng.standard_normal((4, 4))
    V1 = rng.standard_normal((4, 4))
    B2 = rng.standard_normal((4, 4))
    V2 = rng.standard_normal((4, 4))
    K1 = make_K(B1, V1)
    K2 = make_K(B2, V2)
    svals1 = np.linalg.svd(M - K1, compute_uv=False)
    svals2 = np.linalg.svd(M - K1 - K2, compute_uv=False)
    r1 = np.linalg.matrix_rank(M - K1)
    r2 = np.linalg.matrix_rank(M - K1 - K2)
    print(f"Trial {trial}: rank(M - K1) = {r1}, rank(M - K1 - K2) = {r2}")
