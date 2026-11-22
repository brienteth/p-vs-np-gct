"""Padding survival (z^k * f) test for Macaulay apolar & Jacobian Betti invariants on n=3,4."""
from __future__ import annotations

import itertools
import math
import random
from collections import defaultdict
from typing import Dict, List, Tuple

import numpy as np

from apolar_betti_probe import right_nullspace_mod
from apolar_higher_betti_probe import (
    apolar_betti_deg4_ungraded,
    polys_to_dense_mod,
    rank_matrix_mod,
)
from general_det6_probe import layered_abp_det_split
from koszul_flattening_probe import recenter_poly_from_mod
from perm4_abp_frontier import MOD, rank_mod_numpy
from perm_n_betti_scaling import partials_of_mdeg
from poly_exact import (
    Poly,
    determinant_poly,
    mul_poly,
    partial_deriv,
    permanent_poly,
    var_poly,
)

ExtMdeg = Tuple[Tuple[int, ...], Tuple[int, ...], int]


def pad_poly_z(f: Poly, k_pad: int) -> Poly:
    """Multiply f(x_0..x_{N-1}) by z^{k_pad} where z is appended as variable index N."""
    return {m + (k_pad,): c for m, c in f.items()}


def substitute_shear_vars(p: Poly, src: int, dst: int, coeff: int = 2) -> Poly:
    """Apply invertible GL_N shear x_{src} -> x_{src} + coeff * x_{dst}."""
    res: Poly = {}
    for m, c in p.items():
        es = m[src]
        if es == 0:
            res[m] = res.get(m, 0) + c
            continue
        base = list(m)
        base[src] = 0
        for j in range(es + 1):
            factor = math.comb(es, j) * (coeff ** j) * c
            nm = list(base)
            nm[src] += es - j
            nm[dst] += j
            t = tuple(nm)
            val = res.get(t, 0) + factor
            if val == 0:
                res.pop(t, None)
            else:
                res[t] = val
    return res


def jacobian_syzygy_ungraded_general(
    f: Poly, num_vars: int, mod: int = MOD
) -> Tuple[int, int, int, int, int]:
    """
    Ungraded Jacobian ideal J(f) syzygies at linear & quadratic order for arbitrary degree d >= 3:
      (dim_g, dim_syz2, dim_v_g, beta_2_J, beta_3_J).
    """
    partials = [
        {m: c % mod for m, c in partial_deriv(f, i).items() if c % mod != 0}
        for i in range(num_vars)
    ]
    x_vars = [var_poly(j, num_vars) for j in range(num_vars)]

    psi1_polys = [mul_poly(x_vars[j], partials[i]) for j in range(num_vars) for i in range(num_vars)]
    psi1_mat = polys_to_dense_mod(psi1_polys, mod=mod)
    syz1_basis = right_nullspace_mod(psi1_mat.T, mod=mod)
    dim_g = syz1_basis.shape[0]
    if dim_g > 0:
        assert not np.any((syz1_basis @ psi1_mat) % mod)

    pairs2 = [(a, b) for a in range(num_vars) for b in range(a, num_vars)]
    pair2_to_idx = {pair: idx for idx, pair in enumerate(pairs2)}
    m2 = len(pairs2)
    x_quads = []
    for a, b in pairs2:
        exp = [0] * num_vars
        exp[a] += 1
        exp[b] += 1
        x_quads.append({tuple(exp): 1})

    psi2_polys = [mul_poly(x_quads[p2_i], partials[i]) for p2_i in range(m2) for i in range(num_vars)]
    psi2_mat = polys_to_dense_mod(psi2_polys, mod=mod)
    dim_j2 = rank_matrix_mod(psi2_mat, mod=mod)
    dim_syz2 = m2 * num_vars - dim_j2

    shifted_g = np.zeros((num_vars * dim_g, m2 * num_vars), dtype=np.int64)
    for s_idx in range(dim_g):
        nz_cols = np.nonzero(syz1_basis[s_idx])[0]
        for l in range(num_vars):
            row_idx = l * dim_g + s_idx
            for c_idx in nz_cols:
                j, i = divmod(int(c_idx), num_vars)
                a, b = (l, j) if l <= j else (j, l)
                t_col = pair2_to_idx[(a, b)] * num_vars + i
                shifted_g[row_idx, t_col] = (
                    shifted_g[row_idx, t_col] + int(syz1_basis[s_idx, c_idx])
                ) % mod

    if shifted_g.shape[0] > 0:
        assert not np.any((shifted_g @ psi2_mat) % mod)
    dim_v_g = rank_matrix_mod(shifted_g, mod=mod)
    beta_2_J = dim_syz2 - dim_v_g
    beta_3_J = num_vars * dim_g - dim_v_g
    assert beta_2_J >= 0 and beta_3_J >= 0
    return dim_g, dim_syz2, dim_v_g, beta_2_J, beta_3_J


def ext_mdeg(m: Tuple[int, ...], n: int) -> ExtMdeg:
    r = tuple(sum(m[i * n + j] for j in range(n)) for i in range(n))
    c = tuple(sum(m[i * n + j] for i in range(n)) for j in range(n))
    return (r, c, m[n * n])


def add_ext(a: ExtMdeg, b: ExtMdeg) -> ExtMdeg:
    return (
        tuple(x + y for x, y in zip(a[0], b[0])),
        tuple(x + y for x, y in zip(a[1], b[1])),
        a[2] + b[2],
    )


def apply_diff_tuple(p: Poly, ops: Tuple[int, ...]) -> Poly:
    cur = p
    for v in ops:
        cur = partial_deriv(cur, v)
        if not cur:
            return {}
    return cur


def apolar_betti_deg4_torus_padded(
    f: Poly, n: int, k_pad: int, mod: int = MOD
) -> Tuple[Tuple[int, int, int, int, int, int], int, int]:
    """
    Extended (row_deg, col_deg, z_deg) torus-multigraded apolar Betti numbers for z^{k_pad} * f.
    Returns (totals, b24_dz0, b24_dz_pos).
    """
    padded = pad_poly_z(f, k_pad)
    num_vars = n * n + 1
    pairs2 = [(i, j) for i in range(num_vars) for j in range(i, num_vars)]
    pair2_to_idx = {pair: idx for idx, pair in enumerate(pairs2)}

    var_mdeg: List[ExtMdeg] = []
    for k in range(num_vars):
        exp = [0] * num_vars
        exp[k] = 1
        var_mdeg.append(ext_mdeg(tuple(exp), n))

    pair2_mdeg: List[ExtMdeg] = []
    pair2_poly: List[Poly] = []
    pair2_by_mdeg: Dict[ExtMdeg, List[int]] = defaultdict(list)
    for p_idx, (a, b) in enumerate(pairs2):
        exp = [0] * num_vars
        exp[a] += 1
        exp[b] += 1
        t = tuple(exp)
        md = ext_mdeg(t, n)
        pair2_mdeg.append(md)
        pair2_poly.append({t: 1})
        pair2_by_mdeg[md].append(p_idx)

    # 1) Blockwise f^perp_2
    f2_quadrics_by_mdeg: Dict[ExtMdeg, List[Poly]] = {}
    dim_f2_total = 0
    for md2, p_indices in pair2_by_mdeg.items():
        p2_polys: List[Poly] = []
        for p_idx in p_indices:
            i, j = pairs2[p_idx]
            dij = partial_deriv(partial_deriv(padded, i), j)
            p2_polys.append({m: c % mod for m, c in dij.items() if c % mod != 0} if dij else {})
        A_blk = polys_to_dense_mod(p2_polys, mod=mod)
        nb = right_nullspace_mod(A_blk.T, mod=mod)
        if nb.shape[0] > 0:
            assert not np.any((nb @ A_blk) % mod)
            q_list: List[Poly] = []
            for row in nb:
                q_poly: Poly = {}
                for loc_idx in np.nonzero(row)[0]:
                    i, j = pairs2[p_indices[int(loc_idx)]]
                    exp = [0] * num_vars
                    exp[i] += 1
                    exp[j] += 1
                    q_poly[tuple(exp)] = int(row[loc_idx])
                q_list.append(q_poly)
            f2_quadrics_by_mdeg[md2] = q_list
            dim_f2_total += len(q_list)

    # Pre-group degree-3 and degree-4 monomials and nonzero partials directly from `padded`
    deg3_monoms_by_mdeg: Dict[ExtMdeg, int] = defaultdict(int)
    d3_partials_by_mdeg: Dict[ExtMdeg, List[Poly]] = defaultdict(list)
    for comb in itertools.combinations_with_replacement(range(num_vars), 3):
        exp = [0] * num_vars
        for idx in comb:
            exp[idx] += 1
        md = ext_mdeg(tuple(exp), n)
        deg3_monoms_by_mdeg[md] += 1
        if max(md[0]) <= 1 and max(md[1]) <= 1 and md[2] <= k_pad:
            dp = apply_diff_tuple(padded, comb)
            if dp:
                d3_partials_by_mdeg[md].append({m: c % mod for m, c in dp.items() if c % mod != 0})

    deg4_monoms_by_mdeg: Dict[ExtMdeg, int] = defaultdict(int)
    d4_partials_by_mdeg: Dict[ExtMdeg, List[Poly]] = defaultdict(list)
    for comb in itertools.combinations_with_replacement(range(num_vars), 4):
        exp = [0] * num_vars
        for idx in comb:
            exp[idx] += 1
        md = ext_mdeg(tuple(exp), n)
        deg4_monoms_by_mdeg[md] += 1
        if max(md[0]) <= 1 and max(md[1]) <= 1 and md[2] <= k_pad:
            dp = apply_diff_tuple(padded, comb)
            if dp:
                d4_partials_by_mdeg[md].append({m: c % mod for m, c in dp.items() if c % mod != 0})

    y_vars = [var_poly(k, num_vars) for k in range(num_vars)]

    # 2) Degree-3 blocks
    gens3_by_mdeg: Dict[ExtMdeg, List[Tuple[int, ExtMdeg, int]]] = defaultdict(list)
    for md2, q_list in f2_quadrics_by_mdeg.items():
        for q_loc in range(len(q_list)):
            for k in range(num_vars):
                gens3_by_mdeg[add_ext(var_mdeg[k], md2)].append((k, md2, q_loc))

    syz3_by_mdeg: Dict[ExtMdeg, Tuple[List[Tuple[int, ExtMdeg, int]], np.ndarray]] = {}
    beta_1_3_total = 0
    beta_2_3_total = 0
    for md3, dim_s3_blk in deg3_monoms_by_mdeg.items():
        d3_rank = rank_mod_numpy(d3_partials_by_mdeg.get(md3, []), mod=mod)
        dim_f3_blk = dim_s3_blk - d3_rank
        gens3 = gens3_by_mdeg.get(md3, [])
        if gens3:
            phi3_polys = [
                mul_poly(y_vars[k], f2_quadrics_by_mdeg[md2][q_loc]) for k, md2, q_loc in gens3
            ]
            phi3_blk = polys_to_dense_mod(phi3_polys, mod=mod)
            syz_blk = right_nullspace_mod(phi3_blk.T, mod=mod)
            if syz_blk.shape[0] > 0:
                assert not np.any((syz_blk @ phi3_blk) % mod)
                syz3_by_mdeg[md3] = (gens3, syz_blk)
            dim_v_f2_blk = len(gens3) - syz_blk.shape[0]
            beta_2_3_total += syz_blk.shape[0]
        else:
            dim_v_f2_blk = 0
        assert dim_v_f2_blk <= dim_f3_blk
        beta_1_3_total += dim_f3_blk - dim_v_f2_blk

    # 3) Degree-4 blocks
    gens4_by_mdeg: Dict[ExtMdeg, List[Tuple[int, ExtMdeg, int]]] = defaultdict(list)
    for md2, q_list in f2_quadrics_by_mdeg.items():
        for q_loc in range(len(q_list)):
            for p2_idx in range(len(pairs2)):
                gens4_by_mdeg[add_ext(pair2_mdeg[p2_idx], md2)].append((p2_idx, md2, q_loc))

    shifted3_by_mdeg: Dict[ExtMdeg, List[Tuple[int, ExtMdeg, int]]] = defaultdict(list)
    for md3, (_, syz_blk) in syz3_by_mdeg.items():
        for s_loc in range(syz_blk.shape[0]):
            for l in range(num_vars):
                shifted3_by_mdeg[add_ext(var_mdeg[l], md3)].append((l, md3, s_loc))

    beta_1_4_total = 0
    beta_2_4_total = 0
    beta_3_4_total = 0
    b24_dz0 = 0
    b24_dz_pos = 0

    for md4, dim_s4_blk in deg4_monoms_by_mdeg.items():
        d4_rank = rank_mod_numpy(d4_partials_by_mdeg.get(md4, []), mod=mod)
        dim_f4_blk = dim_s4_blk - d4_rank
        gens4 = gens4_by_mdeg.get(md4, [])
        shifts4 = shifted3_by_mdeg.get(md4, [])

        if gens4:
            phi4_polys = [
                mul_poly(pair2_poly[p2_idx], f2_quadrics_by_mdeg[md2][q_loc])
                for p2_idx, md2, q_loc in gens4
            ]
            phi4_blk = polys_to_dense_mod(phi4_polys, mod=mod)
            dim_s2_f2_blk = rank_matrix_mod(phi4_blk, mod=mod)
            dim_syz1_4_blk = len(gens4) - dim_s2_f2_blk
        else:
            phi4_blk = np.zeros((0, 1), dtype=np.int64)
            dim_s2_f2_blk = 0
            dim_syz1_4_blk = 0

        assert dim_s2_f2_blk <= dim_f4_blk
        b14_blk = dim_f4_blk - dim_s2_f2_blk

        if shifts4:
            gen4_to_col = {g: idx for idx, g in enumerate(gens4)}
            shift_mat = np.zeros((len(shifts4), len(gens4)), dtype=np.int64)
            for row_i, (l, md3, s_loc) in enumerate(shifts4):
                gens3, syz_blk = syz3_by_mdeg[md3]
                vec = syz_blk[s_loc]
                for c_idx in np.nonzero(vec)[0]:
                    k, q_md2, q_loc = gens3[int(c_idx)]
                    a, b = (l, k) if l <= k else (k, l)
                    t_col = gen4_to_col[(pair2_to_idx[(a, b)], q_md2, q_loc)]
                    shift_mat[row_i, t_col] = (shift_mat[row_i, t_col] + int(vec[c_idx])) % mod
            assert not np.any((shift_mat @ phi4_blk) % mod)
            dim_v_syz3_blk = rank_matrix_mod(shift_mat, mod=mod)
        else:
            dim_v_syz3_blk = 0

        b24_blk = dim_syz1_4_blk - dim_v_syz3_blk
        b34_blk = len(shifts4) - dim_v_syz3_blk
        assert b24_blk >= 0 and b34_blk >= 0

        beta_1_4_total += b14_blk
        beta_2_4_total += b24_blk
        beta_3_4_total += b34_blk
        if md4[2] == 0:
            b24_dz0 += b24_blk
        else:
            b24_dz_pos += b24_blk

    return (
        dim_f2_total,
        beta_1_3_total,
        beta_2_3_total,
        beta_1_4_total,
        beta_2_4_total,
        beta_3_4_total,
    ), b24_dz0, b24_dz_pos


def jacobian_syzygy_torus_padded(
    f: Poly, n: int, k_pad: int, mod: int = MOD
) -> Tuple[int, int, int, int, int]:
    """Extended torus-multigraded Jacobian ideal syzygy invariants for z^{k_pad} * f."""
    padded = pad_poly_z(f, k_pad)
    num_vars = n * n + 1
    full_mdeg: ExtMdeg = ((1,) * n, (1,) * n, k_pad)

    var_mdeg: List[ExtMdeg] = []
    for k in range(num_vars):
        exp = [0] * num_vars
        exp[k] = 1
        var_mdeg.append(ext_mdeg(tuple(exp), n))

    partials: List[Poly] = []
    partial_mdeg: List[ExtMdeg] = []
    for i in range(num_vars):
        dp = {m: c % mod for m, c in partial_deriv(padded, i).items() if c % mod != 0}
        partials.append(dp)
        vm = var_mdeg[i]
        partial_mdeg.append((
            tuple(x - y for x, y in zip(full_mdeg[0], vm[0])),
            tuple(x - y for x, y in zip(full_mdeg[1], vm[1])),
            full_mdeg[2] - vm[2],
        ))

    x_vars = [var_poly(j, num_vars) for j in range(num_vars)]

    gens1_by_mdeg: Dict[ExtMdeg, List[Tuple[int, int]]] = defaultdict(list)
    for j in range(num_vars):
        for i in range(num_vars):
            if min(partial_mdeg[i][0]) < 0 or min(partial_mdeg[i][1]) < 0 or partial_mdeg[i][2] < 0:
                continue
            md1 = add_ext(var_mdeg[j], partial_mdeg[i])
            gens1_by_mdeg[md1].append((j, i))

    syz1_by_mdeg: Dict[ExtMdeg, Tuple[List[Tuple[int, int]], np.ndarray]] = {}
    dim_g_total = 0
    for md1, gens1 in gens1_by_mdeg.items():
        psi1_polys = [mul_poly(x_vars[j], partials[i]) for j, i in gens1]
        psi1_blk = polys_to_dense_mod(psi1_polys, mod=mod)
        syz_blk = right_nullspace_mod(psi1_blk.T, mod=mod)
        if syz_blk.shape[0] > 0:
            assert not np.any((syz_blk @ psi1_blk) % mod)
            syz1_by_mdeg[md1] = (gens1, syz_blk)
            dim_g_total += syz_blk.shape[0]

    pairs2 = [(a, b) for a in range(num_vars) for b in range(a, num_vars)]
    pair2_to_idx = {pair: idx for idx, pair in enumerate(pairs2)}
    pair2_mdeg: List[ExtMdeg] = []
    pair2_poly: List[Poly] = []
    for a, b in pairs2:
        exp = [0] * num_vars
        exp[a] += 1
        exp[b] += 1
        t = tuple(exp)
        pair2_mdeg.append(ext_mdeg(t, n))
        pair2_poly.append({t: 1})

    gens2_by_mdeg: Dict[ExtMdeg, List[Tuple[int, int]]] = defaultdict(list)
    for p2_idx in range(len(pairs2)):
        for i in range(num_vars):
            if min(partial_mdeg[i][0]) < 0 or min(partial_mdeg[i][1]) < 0 or partial_mdeg[i][2] < 0:
                continue
            md2 = add_ext(pair2_mdeg[p2_idx], partial_mdeg[i])
            gens2_by_mdeg[md2].append((p2_idx, i))

    shifted1_by_mdeg: Dict[ExtMdeg, List[Tuple[int, ExtMdeg, int]]] = defaultdict(list)
    for md1, (_, syz_blk) in syz1_by_mdeg.items():
        for s_loc in range(syz_blk.shape[0]):
            for l in range(num_vars):
                shifted1_by_mdeg[add_ext(var_mdeg[l], md1)].append((l, md1, s_loc))

    dim_syz2_total = 0
    dim_v_g_total = 0
    beta_2_J_total = 0
    beta_3_J_total = 0

    for md2, gens2 in gens2_by_mdeg.items():
        psi2_polys = [mul_poly(pair2_poly[p2_idx], partials[i]) for p2_idx, i in gens2]
        psi2_blk = polys_to_dense_mod(psi2_polys, mod=mod)
        dim_j2_blk = rank_matrix_mod(psi2_blk, mod=mod)
        dim_syz2_blk = len(gens2) - dim_j2_blk

        shifts2 = shifted1_by_mdeg.get(md2, [])
        if shifts2:
            gen2_to_col = {g: idx for idx, g in enumerate(gens2)}
            shift_mat = np.zeros((len(shifts2), len(gens2)), dtype=np.int64)
            for row_i, (l, md1, s_loc) in enumerate(shifts2):
                gens1, syz_blk = syz1_by_mdeg[md1]
                vec = syz_blk[s_loc]
                for c_idx in np.nonzero(vec)[0]:
                    j, i = gens1[int(c_idx)]
                    a, b = (l, j) if l <= j else (j, l)
                    t_col = gen2_to_col[(pair2_to_idx[(a, b)], i)]
                    shift_mat[row_i, t_col] = (shift_mat[row_i, t_col] + int(vec[c_idx])) % mod
            assert not np.any((shift_mat @ psi2_blk) % mod)
            dim_v_g_blk = rank_matrix_mod(shift_mat, mod=mod)
        else:
            dim_v_g_blk = 0

        b2_blk = dim_syz2_blk - dim_v_g_blk
        b3_blk = len(shifts2) - dim_v_g_blk
        assert b2_blk >= 0 and b3_blk >= 0

        dim_syz2_total += dim_syz2_blk
        dim_v_g_total += dim_v_g_blk
        beta_2_J_total += b2_blk
        beta_3_J_total += b3_blk

    return dim_g_total, dim_syz2_total, dim_v_g_total, beta_2_J_total, beta_3_J_total


def main() -> None:
    p3 = permanent_poly(3)
    d3 = determinant_poly(3)
    rng = random.Random(123)
    # Advance RNG identically to general_det6_probe order to pick (2,3) split or create fresh deterministic one
    m6_23 = recenter_poly_from_mod(layered_abp_det_split(2, 3, 9, rng))

    # 1) GL_{10} shear check on z^1 * perm_3 mixing x_0 and z (var 0 -> var 0 + 2 * var 9)
    z1_p3 = pad_poly_z(p3, 1)
    z1_p3_shear = substitute_shear_vars(z1_p3, 0, 9, coeff=2)
    ap_orig = apolar_betti_deg4_ungraded(z1_p3, 10)
    ap_shear = apolar_betti_deg4_ungraded(z1_p3_shear, 10)
    assert ap_orig == ap_shear, f"GL_10 apolar shear check failed: {ap_orig} != {ap_shear}"

    j_orig = jacobian_syzygy_ungraded_general(z1_p3, 10)
    j_shear = jacobian_syzygy_ungraded_general(z1_p3_shear, 10)
    assert j_orig == j_shear, f"GL_10 Jacobian shear check failed: {j_orig} != {j_shear}"

    # 2) n=3 padded cross-checks: ungraded vs extended torus
    for k_pad in (1, 2):
        for poly in (p3, d3):
            u_ap = apolar_betti_deg4_ungraded(pad_poly_z(poly, k_pad), 10)
            t_ap, _, _ = apolar_betti_deg4_torus_padded(poly, 3, k_pad)
            assert u_ap == t_ap, f"n=3 k={k_pad} apolar cross-check failed: {u_ap} != {t_ap}"
        if k_pad == 1:
            for poly in (p3, d3):
                u_j = jacobian_syzygy_ungraded_general(pad_poly_z(poly, k_pad), 10)
                t_j = jacobian_syzygy_torus_padded(poly, 3, k_pad)
                assert u_j == t_j, f"n=3 k={k_pad} Jacobian cross-check failed: {u_j} != {t_j}"

    print(f"[Self-Checks] GL_10 shear invariance & n=3 padded cross-checks OK\n")

    print("=== n=3 (N=10) Padded Apolar Betti Table (deg 2..4) ===")
    print("Model          | dim(f^p_2) | b_{1,3} | b_{2,3} | b_{1,4} | b_{2,4} | b_{3,4}")
    print("-" * 76)
    for k_pad in (1, 2):
        for name, poly in [("det_3", d3), ("m=6 (2,3)", m6_23), ("perm_3", p3)]:
            df2, b13, b23, b14, b24, b34 = apolar_betti_deg4_ungraded(pad_poly_z(poly, k_pad), 10)
            print(f"z^{k_pad} * {name:9s} | {df2:10d} | {b13:7d} | {b23:7d} | {b14:7d} | {b24:7d} | {b34:7d}")

    print("\n=== n=3 (N=10) Padded Jacobian Ideal Syzygy Table (deg 1..2) ===")
    print("Model          | dim(g_f) | dim(Syz2) | dim(V*g_f) | b_2^J | b_3^J")
    print("-" * 70)
    for k_pad in (1, 2):
        for name, poly in [("det_3", d3), ("m=6 (2,3)", m6_23), ("perm_3", p3)]:
            dg, s2, dvg, b2j, b3j = jacobian_syzygy_ungraded_general(pad_poly_z(poly, k_pad), 10)
            print(f"z^{k_pad} * {name:9s} | {dg:8d} | {s2:9d} | {dvg:10d} | {b2j:5d} | {b3j:5d}")

    p4 = permanent_poly(4)
    d4 = determinant_poly(4)

    print("\n=== n=4 (N=17) Padded Apolar Betti Table (deg 2..4) ===")
    print("Model       | dim(f^p_2) | b_{1,3} | b_{2,3} | b_{1,4} | b_{2,4} (dz=0, dz>0) | b_{3,4}")
    print("-" * 92)
    for k_pad in (0, 1, 2):
        for name, poly in [("det_4", d4), ("perm_4", p4)]:
            tot, dz0, dzp = apolar_betti_deg4_torus_padded(poly, 4, k_pad)
            df2, b13, b23, b14, b24, b34 = tot
            b24_str = f"{b24:3d} ({dz0:2d}, {dzp:3d})"
            print(
                f"z^{k_pad} * {name:6s} | {df2:10d} | {b13:7d} | {b23:7d} | {b14:7d} | "
                f"{b24_str:20s} | {b34:7d}"
            )

    print("\n=== n=4 (N=17) Padded Jacobian Ideal Syzygy Table (deg 1..2) ===")
    print("Model       | dim(g_f) | dim(Syz2) | dim(V*g_f) | b_2^J | b_3^J")
    print("-" * 67)
    for k_pad in (0, 1, 2):
        for name, poly in [("det_4", d4), ("perm_4", p4)]:
            dg, s2, dvg, b2j, b3j = jacobian_syzygy_torus_padded(poly, 4, k_pad)
            print(f"z^{k_pad} * {name:6s} | {dg:8d} | {s2:9d} | {dvg:10d} | {b2j:5d} | {b3j:5d}")


if __name__ == "__main__":
    main()
