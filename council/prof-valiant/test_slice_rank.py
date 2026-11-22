"""Test the flattening rank of X P_6(a, b) for any 11-dimensional subspace X in C^15."""
import itertools
import numpy as np

n = 6
k = 3
subsets_km1 = list(itertools.combinations(range(n), k - 1)) # 15
m6 = len(subsets_km1)
subsets_k = list(itertools.combinations(range(n), k)) # 20

# Build M6: 90 x 90
M6 = np.zeros((m6 * n, m6 * n), dtype=np.float64)
for I_idx, I in enumerate(subsets_km1):
    for c1 in range(n):
        if c1 in I:
            continue
        S1 = tuple(sorted(I + (c1,)))
        for J_idx, J in enumerate(subsets_km1):
            for c2 in range(n):
                if c2 in J:
                    continue
                S2 = tuple(sorted(J + (c2,)))
                if set(S1).isdisjoint(set(S2)) and len(set(S1) | set(S2)) == n:
                    M6[I_idx * n + c1, J_idx * n + c2] = 1.0

# For any p x 15 matrix X of rank p (e.g. p = 11, 12, 13, 14):
# The flattening of X P_6(a, b) is (X (x) I_6) M6, which has size (p * 6) x (15 * 6) = (6p) x 90.
# What is the rank of (X (x) I_6) M6 for random X of rank p?
rng = np.random.default_rng(42)

for p in [11, 12, 13, 14]:
    ranks = []
    for trial in range(20):
        X = rng.integers(-5, 5, size=(p, 15)).astype(np.float64)
        while np.linalg.matrix_rank(X) < p:
            X = rng.integers(-5, 5, size=(p, 15)).astype(np.float64)
        
        # Compute (X (x) I_6) @ M6
        XI = np.kron(X, np.eye(6))
        XIM = XI @ M6
        r = np.linalg.matrix_rank(XIM)
        ranks.append(r)
    print(f"p = {p} rows: min rank((X (x) I_6) M6) = {min(ranks)}, max = {max(ranks)}")
