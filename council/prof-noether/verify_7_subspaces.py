"""Verify the 7-Subspace Theorem for rank((Gamma_W (x) I_4) M (delta (x) I_4)) <= 3."""
import itertools
import numpy as np

M = np.zeros((16, 16), dtype=int)
for i in range(4):
    for j in range(4):
        for k in range(4):
            for l in range(4):
                if len({i, j, k, l}) == 4:
                    M[i*4 + j, k*4 + l] = 1

one = np.ones((4, 1), dtype=int)

# Check the 7 special 2D subspaces for delta = (1,1,1,1)^T:
# K_0, K_1, K_2, K_3: {w : w_k = 0 and sum w = 0}
K_spaces = [
    np.array([[0, 1, -1, 0], [0, 1, 0, -1]]),
    np.array([[1, 0, -1, 0], [1, 0, 0, -1]]),
    np.array([[1, -1, 0, 0], [1, 0, 0, -1]]),
    np.array([[1, -1, 0, 0], [1, 0, -1, 0]]),
]
# H_1, H_2, H_3: span(e_i - e_j, e_k - e_l)
H_spaces = [
    np.array([[1, -1, 0, 0], [0, 0, 1, -1]]),
    np.array([[1, 0, -1, 0], [0, 1, 0, -1]]),
    np.array([[1, 0, 0, -1], [0, 1, -1, 0]]),
]

print("Checking ranks of the 7 special subspaces for delta = (1,1,1,1):")
for idx, G in enumerate(K_spaces):
    sub = np.kron(G, np.eye(4)) @ M @ np.kron(one, np.eye(4))
    print(f"  K_{idx}: rank = {np.linalg.matrix_rank(sub)}")
for idx, G in enumerate(H_spaces):
    sub = np.kron(G, np.eye(4)) @ M @ np.kron(one, np.eye(4))
    print(f"  H_{idx+1}: rank = {np.linalg.matrix_rank(sub)}")

# Now exhaustively check ALL 2D subspaces of F_3^4 and F_5^4!
def rank_mod(A, p):
    A = A.copy() % p
    m, n = A.shape
    r = 0
    for c in range(n):
        piv = None
        for i in range(r, m):
            if A[i, c] != 0:
                piv = i
                break
        if piv is None:
            continue
        if piv != r:
            A[[r, piv]] = A[[pivot, r]] if False else A[[piv, r]]
        inv = pow(int(A[r, c]), p - 2, p)
        A[r] = (A[r] * inv) % p
        for i in range(m):
            if i != r and A[i, c] != 0:
                A[i] = (A[i] - A[i, c] * A[r]) % p
        r += 1
    return r

for p in [3, 5, 7]:
    # Enumerate all 2D subspaces of F_p^4 in RREF
    rref_2d = []
    for piv0 in range(4):
        for piv1 in range(piv0 + 1, 4):
            free_cols0 = [c for c in range(piv0 + 1, 4) if c != piv1]
            free_cols1 = [c for c in range(piv1 + 1, 4)]
            for vals0 in itertools.product(range(p), repeat=len(free_cols0)):
                for vals1 in itertools.product(range(p), repeat=len(free_cols1)):
                    G = np.zeros((2, 4), dtype=int)
                    G[0, piv0] = 1
                    for c, v in zip(free_cols0, vals0):
                        G[0, c] = v
                    G[1, piv1] = 1
                    for c, v in zip(free_cols1, vals1):
                        G[1, c] = v
                    rref_2d.append(G)
    low_rank_count = 0
    for G in rref_2d:
        sub = (np.kron(G, np.eye(4, dtype=int)) @ M @ np.kron(one, np.eye(4, dtype=int))) % p
        r = rank_mod(sub, p)
        if r <= 3:
            low_rank_count += 1
    print(f"Over F_{p}: total 2D subspaces = {len(rref_2d)}, number with rank <= 3 for delta=1: {low_rank_count}")
