"""Test degree-1 left syzygy dimension of 19x15 linear matrices."""
import itertools
import numpy as np

n = 6
k = 3
subsets_km1 = list(itertools.combinations(range(n), k - 1)) # 15
subsets_k = list(itertools.combinations(range(n), k)) # 20

# Canonical B2_full(b): size 20 x 15
# row S in subsets_k, col J in subsets_km1
# entry is b_c if J U {c} = S, else 0
# A linear left syzygy is u(b)_{1 x 19} such that u(b) B2(b) = 0 for all b.
# Let u_i(b) = sum_{c=0}^5 u_{i, c} b_c.
# u(b) B2(b) is a 1 x 15 vector of quadratic forms in b.
# Number of quadratic monomials in b0..b5: C(6+1, 2) = 21.
# 15 columns * 21 monomials = 315 equations!
# Number of variables in u(b): 19 rows * 6 variables = 114 variables.

# Let us test random 19-dimensional projections of B2_full:
# B2(b) = P_mat @ B2_full(b) where P_mat is 19 x 20 of rank 19.
# For any linear projection P_mat:
rng = np.random.default_rng(42)

for trial in range(10):
    P_mat = rng.integers(-5, 5, size=(19, 20))
    while np.linalg.matrix_rank(P_mat) < 19:
        P_mat = rng.integers(-5, 5, size=(19, 20))
        
    # Build 315 x 114 equation matrix for u(b) (P_mat B2_full(b)) = 0
    # Let col J in 0..14, monomial (c1 <= c2) in 0..20
    eq_rows = []
    pairs = [(c1, c2) for c1 in range(6) for c2 in range(c1, 6)]
    pair_to_idx = {p: idx for idx, p in enumerate(pairs)}
    
    # eq_mat: 315 x 114
    eq_mat = np.zeros((15 * 21, 19 * 6), dtype=np.float64)
    
    # B2_full[S, J] is b_c if J U {c} == S
    # B2[i, J] = sum_S P_mat[i, S] b_c
    # u(b)_i = sum_l u_{i, l} b_l
    # (u(b) B2(b))_J = sum_i sum_l u_{i, l} b_l (sum_S P_mat[i, S] [J U {c} == S] b_c)
    #               = sum_i sum_l sum_S P_mat[i, S] [J U {c} == S] u_{i, l} b_l b_c
    for i in range(19):
        for S_idx, S in enumerate(subsets_k):
            for J_idx, J in enumerate(subsets_km1):
                # find c such that J U {c} == S
                diff = set(S) - set(J)
                if len(diff) == 1 and len(set(J)) == 2:
                    c = list(diff)[0]
                    # coefficient is P_mat[i, S_idx]
                    coeff = float(P_mat[i, S_idx])
                    if abs(coeff) > 1e-9:
                        for l in range(6):
                            # monomial is b_l b_c
                            m = (min(l, c), max(l, c))
                            mon_idx = pair_to_idx[m]
                            row_idx = J_idx * 21 + mon_idx
                            var_idx = i * 6 + l
                            eq_mat[row_idx, var_idx] += coeff

    rank_eq = np.linalg.matrix_rank(eq_mat)
    nullity = 114 - rank_eq
    print(f"Trial {trial}: rank(eq_mat) = {rank_eq} / 114, nullity = {nullity}")
