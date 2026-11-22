"""Compute dim(Sym_0(4) cap (W1 (x) Z1 + W2 (x) Z2)) for various subspace dimensions."""
import itertools
import numpy as np

def rank_matrix(A, mod=1000003):
    """Gaussian elimination mod p."""
    A = A.copy() % mod
    m, n = A.shape
    r = 0
    for c in range(n):
        pivot = None
        for i in range(r, m):
            if A[i, c] != 0:
                pivot = i
                break
        if pivot is None:
            continue
        if pivot != r:
            A[[r, pivot]] = A[[pivot, r]]
        inv = pow(int(A[r, c]), mod - 2, mod)
        A[r] = (A[r] * inv) % mod
        factors = A[:, c].copy()
        factors[r] = 0
        A = (A - np.outer(factors, A[r])) % mod
        r += 1
    return r

# Sym_0(4) basis (16 x 6)
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
S0 = np.zeros((16, 6), dtype=np.int64)
for col, (i, j) in enumerate(pairs):
    S0[i*4 + j, col] = 1
    S0[j*4 + i, col] = 1

MOD = 1000003

# Test over random subspaces W1, Z1, W2, Z2
rng = np.random.default_rng(42)

max_dims = {}

for rB1, rV1 in itertools.product(range(1, 5), repeat=2):
    for rB2, rV2 in itertools.product(range(1, 5), repeat=2):
        key = ((rB1, rV1), (rB2, rV2))
        max_d = 0
        for _ in range(50):
            # random W1 of dim rB1, Z1 of dim rV1
            W1 = rng.integers(0, MOD, size=(4, rB1), dtype=np.int64)
            Z1 = rng.integers(0, MOD, size=(4, rV1), dtype=np.int64)
            W2 = rng.integers(0, MOD, size=(4, rB2), dtype=np.int64)
            Z2 = rng.integers(0, MOD, size=(4, rV2), dtype=np.int64)
            # W1 (x) Z1 cols
            cols1 = np.einsum('ia,jb->ijab', W1, Z1).reshape(16, -1) % MOD
            cols2 = np.einsum('ia,jb->ijab', W2, Z2).reshape(16, -1) % MOD
            U = np.hstack([cols1, cols2]) % MOD
            
            # Intersection dim with S0:
            # dim(S0 cap U) = rank(S0) + rank(U) - rank([S0, U])
            rS0 = 6
            rU = rank_matrix(U, MOD)
            rBoth = rank_matrix(np.hstack([S0, U]) % MOD, MOD)
            inter = rS0 + rU - rBoth
            if inter > max_d:
                max_d = inter
        if max_d > 0:
            max_dims[key] = max_d

print("Max intersection dimensions observed for small ranks:")
for key, d in sorted(max_dims.items(), key=lambda x: x[1]):
    if key[0] <= (2, 2) and key[1] <= (2, 2):
        print(f"ranks {key}: dim(Sym_0 cap U) <= {d}")
