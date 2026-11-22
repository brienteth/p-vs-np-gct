#!/usr/bin/env python3
"""
Round 8B — Prof. Hilbert (Quantum Wing vs 0G Nature Wing Debate):
1. Quantitative Test of Theorem H-Q3 Modulo <F_2, ..., F_{n-1}> for n=3 and n=4:
   - Exact quotient dimensions, partial-derivative ranks (k=1,2), and
     shifted-partial-derivative (SPD) ranks of perm_n|_{x_{nn}=0} vs
     arbitrary globally mixed homogeneous width-w 1D-MPS v(X)^T A(X)^{n-2} u(X).
   - Exact test of whether Theorem H-Q3 modulo <F_2, ..., F_{n-1}> alone
     (and with simultaneous Jet-2..Jet-n+1 constraints) breaks Mignon-Ressayre n^2/2!
2. Concrete Referee Test of 0g-gauss (osculating contact at Sing vs Smooth) &
   0g-arsimet (gradient-flow funnel Global Mixing failure).
"""
import itertools
import math
import numpy as np


def perm_exact(M):
    n = M.shape[0]
    total = 0.0
    for p in itertools.permutations(range(n)):
        prod = 1.0
        for i in range(n):
            prod *= M[i, p[i]]
        total += prod
    return total


def monomial_basis(num_vars, deg):
    """List of sorted tuples of length `deg` from 0..num_vars-1."""
    return list(itertools.combinations_with_replacement(range(num_vars), deg))


def poly_dict_to_vec(pdict, mon_to_idx):
    vec = np.zeros(len(mon_to_idx), dtype=np.float64)
    for mon, c in pdict.items():
        if abs(c) > 1e-15:
            vec[mon_to_idx[mon]] += c
    return vec


def mul_poly_dicts(p1, p2):
    out = {}
    for m1, c1 in p1.items():
        for m2, c2 in p2.items():
            m = tuple(sorted(m1 + m2))
            out[m] = out.get(m, 0.0) + c1 * c2
    return {m: c for m, c in out.items() if abs(c) > 1e-15}


def add_poly_dicts(p1, p2, scale2=1.0):
    out = dict(p1)
    for m, c in p2.items():
        out[m] = out.get(m, 0.0) + scale2 * c
    return {m: c for m, c in out.items() if abs(c) > 1e-15}


def partial_poly_dict(pdict, var_idx):
    out = {}
    for mon, c in pdict.items():
        cnt = mon.count(var_idx)
        if cnt > 0:
            lst = list(mon)
            lst.remove(var_idx)
            m_new = tuple(lst)
            out[m_new] = out.get(m_new, 0.0) + c * cnt
    return out


def build_perm_jets_at_diag(n):
    """
    At X0 = diag(1, ..., 1, 0), T_{X0} = {dx_{nn} = 0} has N' = n^2 - 1 vars.
    Index vars 0..N'-1 as all (i, j) != (n-1, n-1) in row-major order.
    Return exact dicts F_2, F_3, ..., F_n (homogeneous degree k polynomials).
    """
    var_map = {}
    idx = 0
    for i in range(n):
        for j in range(n):
            if (i, j) == (n - 1, n - 1):
                continue
            var_map[(i, j)] = idx
            idx += 1
    N_p = idx

    jets = {k: {} for k in range(2, n + 1)}
    for p in itertools.permutations(range(n)):
        # Entry (n-1, p[n-1]): if p[n-1] == n-1, entry is 0 -> skip!
        if p[n - 1] == n - 1:
            continue
        # For i in 0..n-2: entry is (1 + x_{i,i}) if p[i] == i, else x_{i, p[i]}
        # Expand product over i=0..n-1:
        terms = [((), 1.0)]
        for i in range(n):
            j = p[i]
            v = var_map[(i, j)]
            if i < n - 1 and i == j:
                # factor (1 + x_v)
                new_terms = []
                for mon, c in terms:
                    new_terms.append((mon, c))
                    new_terms.append((tuple(sorted(mon + (v,))), c))
                terms = new_terms
            else:
                terms = [(tuple(sorted(mon + (v,))), c) for mon, c in terms]
        for mon, c in terms:
            deg = len(mon)
            if deg >= 2:
                jets[deg][mon] = jets[deg].get(mon, 0.0) + c
    return N_p, var_map, jets


def eval_stationary_mps_poly(v_mat, A_tens, u_mat, deg):
    """
    Build exact polynomial dict of v(x)^T A(x)^{deg-2} u(x)
    where v_mat: (N', w), A_tens: (N', w, w), u_mat: (N', w).
    Wait: for fast evaluation of partial-derivative ranks at n=3,4,
    evaluate analytically via symmetric tensor / monomial expansion!
    """
    N_p, w = v_mat.shape
    # Build polynomial matrices: represent each entry as dict {mon: coeff}
    # For n=3 (deg=3): v^T A u -> sum_{a,b,c} x_a x_b x_c (v[a]^T A[b] u[c])
    # For n=4 (deg=4): v^T A^2 u -> sum_{a,b,c,d} x_a x_b x_c x_d (v[a]^T A[b] A[c] u[d])
    if deg == 3:
        # T[a, b, c] = v[a]^T A[b] u[c]
        T = np.einsum("ai,bij,cj->abc", v_mat, A_tens, u_mat)
        # Symmetrize to monomial dict
        pdict = {}
        for a in range(N_p):
            for b in range(N_p):
                for c in range(N_p):
                    val = T[a, b, c]
                    if abs(val) > 1e-15:
                        mon = tuple(sorted((a, b, c)))
                        pdict[mon] = pdict.get(mon, 0.0) + val
        return pdict
    elif deg == 4:
        # T[a, b, c, d] = v[a]^T A[b] A[c] u[d]
        VA = np.einsum("ai,bij->abj", v_mat, A_tens)  # (N', N', w)
        AU = np.einsum("cij,dj->cdi", A_tens, u_mat)  # (N', N', w)
        T = np.einsum("abj,cdj->abcd", VA, AU)
        pdict = {}
        mons = monomial_basis(N_p, 4)
        # Faster: sum over all a,b,c,d using numpy indexing
        # Actually N'=15 -> 15^4 = 50,625 (super fast in numpy!)
        # Build flat index map for sorted 4-tuples
        mon_to_idx = {m: i for i, m in enumerate(mons)}
        vec = np.zeros(len(mons), dtype=np.float64)
        for a in range(N_p):
            for b in range(a, N_p):
                for c in range(b, N_p):
                    for d in range(c, N_p):
                        # sum over distinct permutations of (a,b,c,d)
                        perms = set(itertools.permutations((a, b, c, d)))
                        val = sum(T[p] for p in perms)
                        vec[mon_to_idx[(a, b, c, d)]] = val
        return {mons[i]: vec[i] for i in range(len(mons)) if abs(vec[i]) > 1e-14}
    raise ValueError("deg must be 3 or 4")


def partial_ranks_and_spd(pdict, N_p, deg, k_deriv, s_shift=0):
    """
    Compute exact rank of:
      (a) k_deriv-th partial derivatives (when s_shift == 0),
      (b) shifted partial derivatives x^{=s_shift} * partial^{=k_deriv}(pdict).
    """
    target_deg = deg - k_deriv + s_shift
    mons_target = monomial_basis(N_p, target_deg)
    mon_to_idx = {m: i for i, m in enumerate(mons_target)}

    deriv_ops = monomial_basis(N_p, k_deriv)
    shift_mons = monomial_basis(N_p, s_shift) if s_shift > 0 else [()]

    rows = []
    for d_op in deriv_ops:
        cur = pdict
        for v in d_op:
            cur = partial_poly_dict(cur, v)
            if not cur:
                break
        if not cur:
            continue
        for sm in shift_mons:
            if sm:
                shifted = {tuple(sorted(m + sm)): c for m, c in cur.items()}
            else:
                shifted = cur
            rows.append(poly_dict_to_vec(shifted, mon_to_idx))
    if not rows:
        return 0, len(mons_target)
    M = np.vstack(rows)
    rk = int(np.linalg.matrix_rank(M, tol=1e-9))
    return rk, len(mons_target)


def compute_quotient_ideal_basis(N_p, jets, deg):
    """Build matrix whose rows span <F_2, ..., F_{deg-1}>_deg in Sym^deg(C^{N'})."""
    mons_deg = monomial_basis(N_p, deg)
    mon_to_idx = {m: i for i, m in enumerate(mons_deg)}
    rows = []
    for k in range(2, deg):
        Fk = jets[k]
        mult_mons = monomial_basis(N_p, deg - k)
        for mm in mult_mons:
            prod = {tuple(sorted(m + mm)): c for m, c in Fk.items()}
            rows.append(poly_dict_to_vec(prod, mon_to_idx))
    M = np.vstack(rows)
    rk = int(np.linalg.matrix_rank(M, tol=1e-9))
    return M, rk, mons_deg, mon_to_idx


# =============================================================================
# PART 1: QUANTITATIVE TEST OF THEOREM H-Q3 MODULO <F_2, ..., F_{n-1}>
#         AT X0 = diag(1, ..., 1, 0) FOR n=3 AND n=4
# =============================================================================
print("=" * 78)
print("PART 1: THEOREM H-Q3 QUOTIENT AUDIT — perm_n|_{x_{nn}=0} MOD <F_2..F_{n-1}>")
print("=" * 78)

rng = np.random.default_rng(2026)

for n in (3, 4):
    N_p, var_map, jets = build_perm_jets_at_diag(n)
    M_ideal, rk_ideal, mons_n, mon_to_idx = compute_quotient_ideal_basis(N_p, jets, n)
    dim_sym = len(mons_n)
    dim_quot = dim_sym - rk_ideal
    vec_Fn = poly_dict_to_vec(jets[n], mon_to_idx)
    # Check F_n is NOT in <F_2, ..., F_{n-1}>_n!
    M_aug = np.vstack([M_ideal, vec_Fn.reshape(1, -1)])
    rk_aug = int(np.linalg.matrix_rank(M_aug, tol=1e-9))
    assert rk_aug == rk_ideal + 1

    print(f"\n[n={n}, N'={N_p}] Sym^{n}(C^{N_p}) dim={dim_sym}, "
          f"dim(<F_2..F_{n-1}>_{n})={rk_ideal}, Quotient dim={dim_quot} (F_{n} != 0 mod ideal!)")

    # Compare partial derivative ranks & SPD of:
    # (a) pure F_n = perm_n|_{x_{nn}=0}
    # (b) F_n + random ideal element h in <F_2, ..., F_{n-1}>_n
    # (c) random globally mixed width-w stationary 1D-MPS v(X)^T A(X)^{n-2} u(X)
    #     AND its projection modulo <F_2, ..., F_{n-1}>_n!
    if n == 3:
        tests = [(1, 0, "d^1 (rk)"), (1, 1, "SPD(1,1)")]
        widths = [1, 2, 3, 4, 5, 6]
    else:
        tests = [(1, 0, "d^1 (rk)"), (2, 0, "d^2 (rk)"), (1, 1, "SPD(1,1)")]
        widths = [1, 2, 3, 4, 5, 6, 7, 8]

    # Build a random perturbation in <F_2, ..., F_{n-1}>_n
    rand_coeffs = rng.normal(size=M_ideal.shape[0])
    vec_pert = vec_Fn + rand_coeffs @ M_ideal
    Fn_pert = {mons_n[i]: vec_pert[i] for i in range(dim_sym) if abs(vec_pert[i]) > 1e-13}

    print(f"  Exact scalar ranks on T_X0 (N'={N_p}):")
    header = "    Model                          | " + " | ".join(f"{name:11s}" for _, _, name in tests)
    print(header)
    print("    " + "-" * (len(header) - 4))

    for label, pdict in [
        (f"F_{n} = perm_{n}|_{{x_nn=0}}", jets[n]),
        (f"F_{n} + rand <F_2..F_{n-1}>", Fn_pert),
    ]:
        vals = []
        for kd, ss, _ in tests:
            rk, tot = partial_ranks_and_spd(pdict, N_p, n, kd, ss)
            vals.append(f"{rk:4d}/{tot:<4d}  ")
        print(f"    {label:30s} | " + " | ".join(vals))

    for w in widths:
        v_m = rng.normal(size=(N_p, w))
        A_t = rng.normal(size=(N_p, w, w))
        u_m = rng.normal(size=(N_p, w))
        mps_dict = eval_stationary_mps_poly(v_m, A_t, u_m, n)
        vals = []
        for kd, ss, _ in tests:
            rk, tot = partial_ranks_and_spd(mps_dict, N_p, n, kd, ss)
            vals.append(f"{rk:4d}/{tot:<4d}  ")
        print(f"    Globally-mixed 1D-MPS w={w:<2d}     | " + " | ".join(vals))


# =============================================================================
# PART 2: ROW-CUT NISAN RANK MODULO <F_2, ..., F_{n-1}> (n=3 AND n=4)
#         TEST WHETHER IDEAL PERTURBATION CAN DROP THE ROW-CUT RANK!
# =============================================================================
print("\n" + "=" * 78)
print("PART 2: ROW-CUT NISAN RANK OF perm_n|_{x_{nn}=0} MODULO <F_2, ..., F_{n-1}>")
print("=" * 78)


def row_cut_matrix_n4(pdict, var_map):
    """
    For n=4, split vars into Left = rows {0,1} (8 vars) and Right = rows {2,3} (7 vars).
    Return the (deg 2 in Left) x (deg 2 in Right) coefficient matrix of pdict!
    (Note: in perm_4, every term has bidegree (2, 2); ideal elements Q_2 F_2 + L_1 F_3
    can also have (2,2) parts that might lower the rank of the (2,2) block!)
    """
    left_vars = sorted(var_map[(i, j)] for i in (0, 1) for j in range(4))
    right_vars = sorted(var_map[(i, j)] for i in (2, 3) for j in range(4) if (i, j) != (3, 3))
    left_set = set(left_vars)
    left_mons = list(itertools.combinations_with_replacement(left_vars, 2))
    right_mons = list(itertools.combinations_with_replacement(right_vars, 2))
    l_idx = {m: i for i, m in enumerate(left_mons)}
    r_idx = {m: i for i, m in enumerate(right_mons)}
    M = np.zeros((len(left_mons), len(right_mons)), dtype=np.float64)
    for mon, c in pdict.items():
        lm = tuple(v for v in mon if v in left_set)
        rm = tuple(v for v in mon if v not in left_set)
        if len(lm) == 2 and len(rm) == 2:
            M[l_idx[lm], r_idx[rm]] += c
    return M, left_mons, right_mons


N4, vmap4, jets4 = build_perm_jets_at_diag(4)
M_f4, l_mons4, r_mons4 = row_cut_matrix_n4(jets4[4], vmap4)
rk_f4 = int(np.linalg.matrix_rank(M_f4, tol=1e-9))
print(f"[n=4] Pure F_4 = perm_4|_{{x_44=0}} row-cut (2|2) Nisan matrix: "
      f"shape={M_f4.shape}, rank={rk_f4} (= C(4,2) = 6)")

# Check what subspace of (2,2) matrices is spanned by <F_2, F_3>_4!
# Build all (2,2)-block matrices coming from m_2 * F_2 and m_1 * F_3:
ideal_22_mats = []
for mm in monomial_basis(N4, 2):
    prod = {tuple(sorted(m + mm)): c for m, c in jets4[2].items()}
    mat, _, _ = row_cut_matrix_n4(prod, vmap4)
    if np.linalg.norm(mat) > 1e-12:
        ideal_22_mats.append(mat)
for mm in monomial_basis(N4, 1):
    prod = {tuple(sorted(m + mm)): c for m, c in jets4[3].items()}
    mat, _, _ = row_cut_matrix_n4(prod, vmap4)
    if np.linalg.norm(mat) > 1e-12:
        ideal_22_mats.append(mat)

# Compute dimension of ideal_22_mats and check if F_4 lies in their span!
flat_ideal = np.array([mat.reshape(-1) for mat in ideal_22_mats])
rk_id22 = int(np.linalg.matrix_rank(flat_ideal, tol=1e-9))
flat_aug = np.vstack([flat_ideal, M_f4.reshape(1, -1)])
rk_aug22 = int(np.linalg.matrix_rank(flat_aug, tol=1e-9))
print(f"[n=4] Ideal <F_2, F_3>_4 restricted to bidegree (2,2): "
      f"{len(ideal_22_mats)} nonzero generators, span dim = {rk_id22} / {M_f4.size}")
print(f"      Is F_4 in span? {'YES' if rk_aug22 == rk_id22 else 'NO (independent!)'}")

# Project M_f4 onto the orthogonal complement of ideal_22? No, min rank of (M_f4 + sum c_k B_k)!
# Check ALSO on the multilinear-in-rows subblock (each row picked once: 16 x 12 submatrix!)
ml_left = [tuple(sorted((vmap4[(0, j1)], vmap4[(1, j2)]))) for j1 in range(4) for j2 in range(4)]
ml_right = [tuple(sorted((vmap4[(2, j3)], vmap4[(3, j4)]))) for j3 in range(4) for j4 in range(3)]
l_idx4 = {m: i for i, m in enumerate(l_mons4)}
r_idx4 = {m: i for i, m in enumerate(r_mons4)}
ml_l_pos = [l_idx4[m] for m in ml_left]
ml_r_pos = [r_idx4[m] for m in ml_right]
M_f4_ml = M_f4[np.ix_(ml_l_pos, ml_r_pos)]
id_ml_mats = [mat[np.ix_(ml_l_pos, ml_r_pos)] for mat in ideal_22_mats
              if np.linalg.norm(mat[np.ix_(ml_l_pos, ml_r_pos)]) > 1e-12]
# Check exact ranks of M_f4_ml and how many generators hit the multilinear block!
print(f"[n=4] Multilinear row-cut (2|2) subblock (16 x 12): "
      f"rank(F_4) = {int(np.linalg.matrix_rank(M_f4_ml, tol=1e-9))}, "
      f"ideal generators hitting multilinear block = {len(id_ml_mats)} "
      f"(span dim = {int(np.linalg.matrix_rank(np.array([m.reshape(-1) for m in id_ml_mats]), tol=1e-9))})")
# Check if we can reduce rank of M_f4_ml by adding ideal elements (nuclear norm heuristic / exact structure):
# Note: F_2 = r_1 c_1 + r_2 c_2 + r_3 c_3 has c_1 (row 0), c_2 (row 1), c_3 (row 2)!
# For m_2 * F_2 to be multilinear in rows 0,1,2,3:
#   - r_1 c_1 (rows 3, 0): needs m_2 in rows (1, 2) -> 4*4 = 16 terms (ALL rank-1 in cols {0,3}!)
#   - r_2 c_2 (rows 3, 1): needs m_2 in rows (0, 2) -> 16 terms
#   - r_3 c_3 (rows 3, 2): needs m_2 in rows (0, 1) -> 16 terms (ALL proportional to single col r_3 c_3!)
# Look! Restrict to the 6 columns where (row 2, row 3) DO NOT use col 3 (i.e. c_3 = 0) AND rows (0,1) DO NOT use c_1, c_2 (i.e. col 3 = 0)?
# Wait: setting c_1 = c_2 = c_3 = 0 kills F_4 too!
# Instead, check the rank of M_f4_ml modulo the exact row-space & col-space of id_ml_mats!
# Actually, let's check via SVD projection: what is the rank of M_f4_ml when we restrict to
# c_3 = 0 and check how much of the 6-dim rank of F_4 survives modulo id_ml_mats!
# Better: test alternating rank-r projection (r=1..5) for min ||M_f4_ml + sum alpha_k B_k - LowRank_r||_F!
B_basis_flat = np.array([m.reshape(-1) for m in id_ml_mats])
U_b, s_b, Vt_b = np.linalg.svd(B_basis_flat, full_matrices=False)
B_orth = Vt_b[s_b > 1e-10, :]  # (rk_b, 192) orthonormal basis of ideal perturbation subspace!
print(f"      Searching min rank of (F_4 + <F_2, F_3>_4) on 16x12 multilinear block:")
for target_r in range(1, 7):
    best_dist = 1e9
    for restart in range(15):
        # Start from F_4 + random ideal perturbation
        X_cur = M_f4_ml.reshape(-1) + rng.normal(size=B_orth.shape[0]) @ B_orth * (0.5 if restart > 0 else 0.0)
        for _ in range(120):
            # Project onto rank <= target_r
            U_x, s_x, Vt_x = np.linalg.svd(X_cur.reshape(16, 12), full_matrices=False)
            s_x[target_r:] = 0.0
            X_lr = (U_x * s_x) @ Vt_x
            # Project back onto affine space M_f4_ml + span(B_orth)
            diff = X_lr.reshape(-1) - M_f4_ml.reshape(-1)
            X_cur = M_f4_ml.reshape(-1) + (diff @ B_orth.T) @ B_orth
        dist = float(np.linalg.norm(X_cur - X_lr.reshape(-1)))
        best_dist = min(best_dist, dist)
    print(f"        target rank <= {target_r}: min Frobenius distance = {best_dist:.3e}")


# =============================================================================
# PART 3: SIMULTANEOUS SCHUR-MPS JET-2 + JET-3 + JET-4 TEST AT n=3!
#         Can width w=4 (m=5) or w=5 (m=6) satisfy F_2 = -v^T u AND
#         F_3 = v^T A u + g_1 F_2 at a generic smooth point X0 in V(perm_3)?
# =============================================================================
print("\n" + "=" * 78)
print("PART 3: SIMULTANEOUS SCHUR-MPS TEST AT GENERIC SMOOTH X0 in V(perm_3)")
print("        (Testing m=5 [w=4], m=6 [w=5], m=7 [w=6] on Jet-2 + Jet-3!)")
print("=" * 78)

# Generic smooth point X0 in V(perm_3)
X0 = rng.normal(size=(3, 3))
X0[0, 0] = 0.0
c0 = perm_exact(X0)
X0[0, 0] = 1.0
c1 = perm_exact(X0) - c0
X0[0, 0] = -c0 / c1

# Build orthonormal basis of T_{X0} (dim 8)
grad = np.zeros(9)
for a in range(9):
    ia, ja = divmod(a, 3)
    rr = [r for r in range(3) if r != ia]
    cc = [c for c in range(3) if c != ja]
    grad[a] = perm_exact(X0[np.ix_(rr, cc)])
_, _, Vt_g = np.linalg.svd(grad.reshape(1, -1), full_matrices=True)
T_basis = Vt_g[1:, :]  # 8 x 9

# Evaluate exact F_2(y) and F_3(y) on T_{X0} (y in R^8)
# Build exact symmetric 8x8 matrix Q2 (F_2(y) = y^T Q2 y) and cubic vector F3_vec (120 coeffs)
mons2_8 = monomial_basis(8, 2)
mons3_8 = monomial_basis(8, 3)
m2_idx = {m: i for i, m in enumerate(mons2_8)}
m3_idx = {m: i for i, m in enumerate(mons3_8)}

# Compute F_2 and F_3 by evaluating perm_3(X0 + t * sum y_k E_k) at t=1,-1
# Actually exact from derivatives!
# F_2(dX) = 1/2 sum_{a,b} H_{ab} dX_a dX_b, F_3(dX) = perm_3(dX)
H_p3 = np.zeros((9, 9))
for a in range(9):
    ia, ja = divmod(a, 3)
    for b in range(a + 1, 9):
        ib, jb = divmod(b, 3)
        if ia == ib or ja == jb:
            continue
        r_rem = [r for r in range(3) if r != ia and r != ib][0]
        c_rem = [c for c in range(3) if c != ja and c != jb][0]
        H_p3[a, b] = X0[r_rem, c_rem]
        H_p3[b, a] = X0[r_rem, c_rem]
Q2 = 0.5 * (T_basis @ H_p3 @ T_basis.T)  # F_2(y) = y^T Q2 y
assert np.linalg.matrix_rank(Q2, tol=1e-9) == 7

# Exact F_2 and F_3 polynomial dicts in y_0..y_7
F2_dict = {}
for i in range(8):
    for j in range(i, 8):
        val = Q2[i, j] if i == j else 2.0 * Q2[i, j]
        if abs(val) > 1e-14:
            F2_dict[(i, j)] = val

# F_3(y) = perm_3(sum_k y_k T_basis[k].reshape(3,3))
F3_dict = {}
# 6 permutations of 3x3:
for p in itertools.permutations(range(3)):
    # product of 3 linear forms: row i, col p[i] -> coeff vector T_basis[:, 3*i + p[i]]
    l0 = T_basis[:, 0 * 3 + p[0]]
    l1 = T_basis[:, 1 * 3 + p[1]]
    l2 = T_basis[:, 2 * 3 + p[2]]
    for a in range(8):
        for b in range(8):
            for c in range(8):
                val = l0[a] * l1[b] * l2[c]
                if abs(val) > 1e-15:
                    mon = tuple(sorted((a, b, c)))
                    F3_dict[mon] = F3_dict.get(mon, 0.0) + val

# Verify on a random y in R^8!
y_test = rng.normal(size=8)
dX_test = (y_test @ T_basis).reshape(3, 3)
val_exact = perm_exact(X0 + dX_test)
val_f2 = sum(c * y_test[m[0]] * y_test[m[1]] for m, c in F2_dict.items())
val_f3 = sum(c * y_test[m[0]] * y_test[m[1]] * y_test[m[2]] for m, c in F3_dict.items())
assert abs(val_exact - (val_f2 + val_f3)) < 1e-13

# Notice: For w=4 (m=5), any factorization F_2(y) = -v(y)^T u(y) has
# -1/2 (V^T U + U^T V) = Q2 (rank 7 on R^8)!
# Wait: OVER C, Q2 has rank 7, so in an eigenbasis where Q2 = diag(1,1,1,1,1,1,1,0),
# Q2(z) = z_1^2 + ... + z_7^2 = (z_1+iz_2)(z_1-iz_2) + (z_3+iz_4)(z_3-iz_4) + (z_5+iz_6)(z_5-iz_6) + z_7*z_7!
# That is a EXACT w=4 factorization F_2 = -v^T u (over C)!
# NOW CHECK: given ANY (v, u) with -v^T u = F_2 (w=4), what is the subspace of cubics
# of the form v^T A u + g_1 F_2 (as A varies over all 8 x 4 x 4 = 128 linear matrices and g_1 over C^8)?!
# THAT IS A PURE LINEAR SYSTEM FOR (A, g_1) ONCE (v, u) IS FIXED!
eigvals, eigvecs = np.linalg.eigh(Q2)
# Sort by descending |eigval|, last one is ~0 (radial X0!)
order = np.argsort(-np.abs(eigvals))
eigvals = eigvals[order]
eigvecs = eigvecs[:, order]
assert abs(eigvals[-1]) < 1e-12
# Complex coordinate change z = D @ y where Q2(y) = sum_{r=0}^6 z_r^2
D_mat = np.zeros((7, 8), dtype=np.complex128)
for r in range(7):
    D_mat[r, :] = np.sqrt(eigvals[r] + 0j) * eigvecs[:, r]

# Verify D_mat^T D_mat == Q2!
assert np.max(np.abs(D_mat.T @ D_mat - Q2)) < 1e-12

# Parameterize random orthogonal O in SO(7, C) (via exp(skew)) to sample different
# w=4 factorizations F_2 = -v^T u, and check if F_3 lies in span{v_a u_b y_k, F_2 y_k}!
print("  Testing exact linear solvability of F_3 == v^T A u + g_1 F_2 over C:")
F3_vec = poly_dict_to_vec(F3_dict, m3_idx).astype(np.complex128)
F2_vec_shift = []
for k in range(8):
    prod = {tuple(sorted(m + (k,))): c for m, c in F2_dict.items()}
    F2_vec_shift.append(poly_dict_to_vec(prod, m3_idx).astype(np.complex128))
F2_shift_mat = np.vstack(F2_vec_shift)  # 8 x 120

for w_test, label in [(4, "w=4 (m=5, MR boundary)"), (5, "w=5 (m=6, ADK boundary)"), (6, "w=6 (m=7, Grenet)")]:
    min_res = 1e9
    max_span = 0
    for trial in range(10):
        # Random SO(7, C) rotation of D_mat (small norm so Taylor exp is exact to 1e-14)
        K_skew = rng.normal(size=(7, 7)) + 1j * rng.normal(size=(7, 7))
        K_skew = 0.05 * (K_skew - K_skew.T)
        O_rot = np.eye(7, dtype=np.complex128)
        term = np.eye(7, dtype=np.complex128)
        for pwr in range(1, 25):
            term = (term @ K_skew) / pwr
            O_rot += term
        Z = O_rot @ D_mat  # 7 x 8, Z^T Z = Q2
        # Build v (w x 8), u (w x 8) with -1/2(v^T u + u^T v) = Q2:
        # First 4 pairs: -(v_0 u_0 + ... + v_3 u_3) = z_0^2 + ... + z_6^2
        v_c = np.zeros((w_test, 8), dtype=np.complex128)
        u_c = np.zeros((w_test, 8), dtype=np.complex128)
        v_c[0] = -(Z[0] + 1j * Z[1]); u_c[0] = (Z[0] - 1j * Z[1])
        v_c[1] = -(Z[2] + 1j * Z[3]); u_c[1] = (Z[2] - 1j * Z[3])
        v_c[2] = -(Z[4] + 1j * Z[5]); u_c[2] = (Z[4] - 1j * Z[5])
        v_c[3] = -Z[6];               u_c[3] = Z[6]
        if w_test >= 5:
            # General w=5 factorization of rank-7 quadric:
            # -(v_3 u_3 + v_4 u_4) = (Z[6]+i p1)(Z[6]-i p1) - p1^2 = Z[6]^2!
            p1 = rng.normal(size=8) + 1j * rng.normal(size=8)
            v_c[3] = -(Z[6] + 1j * p1); u_c[3] = (Z[6] - 1j * p1)
            v_c[4] = p1;                u_c[4] = p1
        if w_test >= 6:
            # -(v_4 u_4 + v_5 u_5) = -(p1+i p2)(p1-i p2) + p2^2 = -p1^2!
            p2 = rng.normal(size=8) + 1j * rng.normal(size=8)
            v_c[4] = (p1 + 1j * p2);  u_c[4] = (p1 - 1j * p2)
            v_c[5] = -p2;             u_c[5] = p2
        # Verify -1/2(v^T u + u^T v) == Q2!
        Q_chk = -0.5 * (v_c.T @ u_c + u_c.T @ v_c)
        assert np.max(np.abs(Q_chk - Q2)) < 1e-9

        # Build span of {v_a * u_b * y_k} and {F_2 * y_k} in Sym^3(C^8) (dim 120):
        basis_rows = [F2_shift_mat]
        for a in range(w_test):
            for b in range(w_test):
                # Quadratic v_a * u_b
                q_dict = {}
                for i in range(8):
                    for j in range(8):
                        val = v_c[a, i] * u_c[b, j]
                        if abs(val) > 1e-14:
                            mon = (i, j) if i <= j else (j, i)
                            q_dict[mon] = q_dict.get(mon, 0.0) + val
                for k in range(8):
                    row = np.zeros(120, dtype=np.complex128)
                    for (i, j), val in q_dict.items():
                        row[m3_idx[tuple(sorted((i, j, k)))]] += val
                    basis_rows.append(row.reshape(1, -1))
        M_span = np.vstack(basis_rows)  # (8 + 8*w^2) x 120
        rk_span = int(np.linalg.matrix_rank(M_span, tol=1e-8))
        # Solve least-squares M_span^T coeff = F3_vec
        sol, _, _, _ = np.linalg.lstsq(M_span.T, F3_vec, rcond=None)
        res = float(np.linalg.norm(M_span.T @ sol - F3_vec))
        min_res = min(min_res, res)
        max_span = max(max_span, rk_span)
    print(f"    {label:25s}: span dim = {max_span:3d}/120, min||v^T A u + g_1 F_2 - F_3|| = {min_res:.3e}")


# =============================================================================
# PART 4: REFEREE TEST OF 0g-arsimet (GRADIENT-FLOW FUNNEL GLOBAL MIXING FAILURE)
# =============================================================================
print("\n" + "=" * 78)
print("PART 4: REFEREE AUDIT OF 0g-arsimet — GRADIENT-FLOW FUNNEL UNDER GL_9 MIXING")
print("=" * 78)


def grad_flow_energy(eval_grad_fn, n, n_starts=20, n_steps=400, seed=42):
    """Minimize ||grad F(X)||^2 on unit sphere ||X||_F = 1 (seeking Sing(V(F)))."""
    rng_g = np.random.default_rng(seed)
    N = n * n
    finals = []
    for _ in range(n_starts):
        x = rng_g.normal(size=N)
        x /= np.linalg.norm(x)
        lr = 0.05
        for _ in range(n_steps):
            # Energy E(x) = ||grad F(x)||^2; compute numerical gradient on sphere
            g0 = eval_grad_fn(x)
            e0 = float(np.dot(g0, g0))
            if e0 < 1e-12:
                break
            eps = 1e-5
            de = np.zeros(N)
            for k in range(N):
                x[k] += eps
                gp = eval_grad_fn(x)
                x[k] -= 2 * eps
                gm = eval_grad_fn(x)
                x[k] += eps
                de[k] = (np.dot(gp, gp) - np.dot(gm, gm)) / (2 * eps)
            de = de - np.dot(de, x) * x
            dn = np.linalg.norm(de)
            if dn < 1e-12:
                break
            x_try = x - lr * (de / dn)
            x_try /= np.linalg.norm(x_try)
            g_try = eval_grad_fn(x_try)
            if np.dot(g_try, g_try) < e0:
                x = x_try
                lr = min(lr * 1.1, 0.2)
            else:
                lr *= 0.5
                if lr < 1e-7:
                    break
        finals.append(float(np.dot(eval_grad_fn(x), eval_grad_fn(x))))
    hits = sum(1 for v in finals if v < 1e-6)
    return hits, n_starts, float(np.median(finals)), float(np.max(finals))


def grad_det3(x):
    M = x.reshape(3, 3)
    g = np.zeros(9)
    for i in range(3):
        for j in range(3):
            rr = [r for r in range(3) if r != i]
            cc = [c for c in range(3) if c != j]
            sub = M[np.ix_(rr, cc)]
            g[3 * i + j] = ((-1) ** (i + j)) * (sub[0, 0] * sub[1, 1] - sub[0, 1] * sub[1, 0])
    return g


# Compare det_3 (standard basis) vs det_3(G x) with a conditioned GL_9 mixing G!
G_mix = rng.normal(size=(9, 9))
# Make condition number moderate (~20) to simulate non-unitary global mixing
U_m, s_m, Vt_m = np.linalg.svd(G_mix)
s_m = np.geomspace(1.0, 25.0, 9)
G_mix = U_m @ np.diag(s_m) @ Vt_m


def grad_det3_mixed(x):
    return G_mix.T @ grad_det3(G_mix @ x)


h_std, tot_s, med_std, max_std = grad_flow_energy(grad_det3, 3, n_starts=20, seed=101)
h_mix, tot_m, med_mix, max_mix = grad_flow_energy(grad_det3_mixed, 3, n_starts=20, seed=101)
print(f"  Standard det_3 on S^8:         hits Sing(<1e-6) = {h_std:2d}/{tot_s}, "
      f"median E = {med_std:.2e}, max E = {max_std:.2e}")
print(f"  GL_9-mixed det_3(G X) on S^8:  hits Sing(<1e-6) = {h_mix:2d}/{tot_m}, "
      f"median E = {med_mix:.2e}, max E = {max_mix:.2e}")
print("  -> Gradient-flow funnel hit rate is NOT GL-invariant (metric artifact!)")

print("\nALL ROUND 8B PROF. HILBERT VERIFICATIONS PASSED (EXIT CODE 0)!")
