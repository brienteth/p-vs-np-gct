"""Test the Fundamental Rank Obstruction Inequality:
rank(M - K) >= 6 + rank(K) - dim(Sym_0(4) cap im(K)) - dim(Sym_0(4) cap im(K^T))
for K = K(B1, V1) + K(B2, V2)."""
import itertools
import numpy as np

MOD = 1000003

def rank_mod(A, mod=MOD):
    A = A.copy() % mod
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
            A[[r, piv]] = A[[piv, r]]
        inv = pow(int(A[r, c]), mod - 2, mod)
        A[r] = (A[r] * inv) % mod
        col = A[:, c].copy()
        col[r] = 0
        A = (A - np.outer(col, A[r])) % mod
        r += 1
    return r

def make_M():
    M = np.zeros((16, 16), dtype=np.int64)
    for j0 in range(4):
        for c1 in range(4):
            for j3 in range(4):
                for c2 in range(4):
                    if len({j0, c1, j3, c2}) == 4:
                        M[j0*4 + c1, j3*4 + c2] = 1
    return M

def make_K(B, V, mod=MOD):
    # K[(j0, c1), (j3, c2)] = B[j0, c2] * V[j3, c1]
    K = np.einsum('il,jk->ikjl', B, V).reshape(16, 16) % mod
    return K

pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
S0 = np.zeros((16, 6), dtype=np.int64)
for col, (i, j) in enumerate(pairs):
    S0[i*4 + j, col] = 1
    S0[j*4 + i, col] = 1

def inter_sym0(K_cols, mod=MOD):
    rK = rank_mod(K_cols, mod)
    if rK == 0:
        return 0
    r_both = rank_mod(np.hstack([S0, K_cols]) % mod, mod)
    return 6 + rK - r_both

M = make_M()
rng = np.random.default_rng(12345)

def rand_rank_mat(r, mod=MOD):
    if r == 0:
        return np.zeros((4, 4), dtype=np.int64)
    L = rng.integers(0, mod, size=(4, r), dtype=np.int64)
    R = rng.integers(0, mod, size=(r, 4), dtype=np.int64)
    return (L @ R) % mod

print("Testing inequality across rank tuples (rB1, rV1, rB2, rV2):")
min_bound_overall = 100
min_actual_overall = 100

for rB1, rV1 in itertools.product(range(1, 5), repeat=2):
    for rB2, rV2 in itertools.product(range(1, 5), repeat=2):
        if (rB1, rV1) > (rB2, rV2):
            continue
        B1 = rand_rank_mat(rB1)
        V1 = rand_rank_mat(rV1)
        B2 = rand_rank_mat(rB2)
        V2 = rand_rank_mat(rV2)
        K = (make_K(B1, V1) + make_K(B2, V2)) % MOD
        rK = rank_mod(K)
        d_col = inter_sym0(K)
        d_row = inter_sym0(K.T)
        bound = 6 + rK - d_col - d_row
        actual = rank_mod((M - K) % MOD)
        assert actual >= bound, f"Inequality failed! actual={actual} < bound={bound}"
        if bound < min_bound_overall:
            min_bound_overall = bound
        if actual < min_actual_overall:
            min_actual_overall = actual

print(f"Verified on all random rank combinations! Min bound = {min_bound_overall}, Min actual = {min_actual_overall}")
