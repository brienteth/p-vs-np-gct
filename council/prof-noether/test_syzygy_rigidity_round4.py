"""Test Noether Degree-1 Syzygy Rigidity and Zariski-Closure Lemma for n = 6, w = 19."""
import itertools
import numpy as np
import sys
sys.path.append('p-vs-np-gct/council/prof-noether')
from general_n2k_noether import build_Mn

M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
# V_basis is 90 x 20 (each col is v_T reshaped from 15 x 6)

# 1. Verify Zariski-closure lemma:
# The space of r in R^90 such that [r(y1) | r(y2)] in span{[v_T(y1) | v_T(y2)]} for random (y1, y2)
# has EXACT dimension 20 = dim Sym_0(3; 6)!
rng = np.random.default_rng(2026)

# A vector r in R^90 defines r(y) = sum_c y_c R[:, c] in R^15.
# For fixed (y1, y2), eval_op(y1, y2) maps r in R^90 -> [r(y1); r(y2)] in R^30:
# Notice r(y) = (I_15 (x) y^T) r!
# So [r(y1); r(y2)] = [I_15 (x) y1^T; I_15 (x) y2^T] r (a 30 x 90 matrix E_Y).
# And span{[v_T(y1); v_T(y2)]} = im(E_Y @ V_basis) (dim 20 in R^30).
# Let N_Y (10 x 30) span the left nullspace of E_Y @ V_basis.
# Then [r(y1); r(y2)] in span{...} iff (N_Y @ E_Y) r = 0!
constraints = []
for _ in range(12):
    y1 = rng.standard_normal(6)
    y2 = rng.standard_normal(6)
    E_Y = np.vstack([np.kron(np.eye(15), y1.reshape(1, 6)),
                     np.kron(np.eye(15), y2.reshape(1, 6))])  # 30 x 90
    im_mat = E_Y @ V_basis  # 30 x 20
    u, s, _ = np.linalg.svd(im_mat)
    assert np.sum(s > 1e-9) == 20
    N_Y = u[:, 20:].T  # 10 x 30
    constraints.append(N_Y @ E_Y)  # 10 x 90

C_all = np.vstack(constraints)  # 120 x 90
rk_C = np.linalg.matrix_rank(C_all)
print(f"[PASS] Zariski-Closure Lemma: 90 - rank(C_all) = {90 - rk_C} == 20 = dim Sym_0(3; 6)")
assert 90 - rk_C == 20
assert np.linalg.norm(C_all @ V_basis) < 1e-10

# 2. Verify Degree-1 Syzygy Rigidity for B2(b)_{19x15} with (19 - t) rows in Sym_0(3;6) and t arbitrary rows in R^90!
def deg1_syzygy_dim(B2_tensor):
    # B2_tensor has shape (6, w, 15)
    w = B2_tensor.shape[1]
    eqs = []
    for J in range(15):
        for c1 in range(6):
            for c2 in range(c1, 6):
                row = np.zeros(6 * w, dtype=float)
                for ell in range(w):
                    row[c1 * w + ell] += B2_tensor[c2, ell, J]
                    if c1 != c2:
                        row[c2 * w + ell] += B2_tensor[c1, ell, J]
                eqs.append(row)
    E = np.array(eqs)  # 315 x (6*w)
    rk = np.linalg.matrix_rank(E)
    return 6 * w - rk

print("\n[Degree-1 Left Syzygy Dimension of B2(b)_{19x15} with (19-t) rows in Sym_0(3;6) and t rows outside]:")
for t in range(0, 6):
    # Random (19 - t) rows in Sym_0(3; 6) + t random rows in R^90
    B2_sym = (V_basis @ rng.standard_normal((20, 19 - t))).T  # (19-t) x 90
    B2_out = rng.standard_normal((t, 90))
    B2_rows = np.vstack([B2_sym, B2_out])  # 19 x 90
    # Reshape to (6, 19, 15): each row is 15 x 6 -> transpose to 6 x 15
    B2_tensor = np.zeros((6, 19, 15))
    for ell in range(19):
        B2_tensor[:, ell, :] = B2_rows[ell].reshape(15, 6).T
    sdim = deg1_syzygy_dim(B2_tensor)
    print(f"  t={t} rows outside Sym_0(3;6) (generic): dim(deg-1 left syzygies) = {sdim}")

# 3. Also test ADVERSARIAL t rows outside Sym_0(3;6) (e.g. rank-1 Koszul rows of the form b_i e_J^T)!
print("\n[Adversarial Koszul test: t rows of the form b_i e_J^T]:")
for t in [1, 2, 3, 4]:
    B2_sym = (V_basis @ rng.standard_normal((20, 19 - t))).T  # (19-t) x 90
    B2_out = np.zeros((t, 90))
    for i in range(t):
        # Single monomial b_i at column J = 0
        mat = np.zeros((15, 6))
        mat[0, i] = 1.0
        B2_out[i] = mat.reshape(90)
    B2_rows = np.vstack([B2_sym, B2_out])
    B2_tensor = np.zeros((6, 19, 15))
    for ell in range(19):
        B2_tensor[:, ell, :] = B2_rows[ell].reshape(15, 6).T
    sdim = deg1_syzygy_dim(B2_tensor)
    print(f"  t={t} adversarial Koszul rows (b_0..b_{t-1} on col 0): dim(deg-1 left syzygies) = {sdim} = C({t}, 2)")
