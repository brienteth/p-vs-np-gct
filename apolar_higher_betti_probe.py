"""Exact minimal free resolution invariants of Macaulay's apolar ideal f^perp through degree 4."""
from __future__ import annotations

import itertools
import math
import random
from collections import defaultdict
from typing import Dict, List, Tuple

import numpy as np

from apolar_betti_probe import right_nullspace_mod
from general_det6_probe import layered_abp_det_split, sum_of_two_det3
from koszul_flattening_probe import recenter_poly_from_mod, substitute_shear_x0_plus_2x1
from perm4_abp_frontier import MOD, rank_mod_numpy
from poly_exact import (
    Poly,
    determinant_poly,
    kth_partial_space,
    mul_poly,
    partial_deriv,
    permanent_poly,
    var_poly,
)


def rank_matrix_mod(mat_in: np.ndarray, mod: int = MOD) -> int:
    """Exact rank of dense NumPy int64 matrix over F_mod."""
    if mat_in.size == 0:
        return 0
    mat = mat_in.copy() % mod
    n_rows, n_cols = mat.shape
    if n_rows > n_cols:
        mat = mat.T.copy()
        n_rows, n_cols = n_cols, n_rows
    rank = 0
    for col in range(n_cols):
        if rank >= n_rows:
            break
        nz = np.nonzero(mat[rank:, col])[0]
        if len(nz) == 0:
            continue
        piv = rank + int(nz[0])
        if piv != rank:
            mat[[rank, piv]] = mat[[piv, rank]]
        inv = pow(int(mat[rank, col]), mod - 2, mod)
        piv_row = (mat[rank, col:] * inv) % mod
        mat[rank, col:] = piv_row
        below = mat[rank + 1 :, col]
        nz_below = np.nonzero(below)[0]
        if len(nz_below) > 0:
            factors = below[nz_below][:, None]
            mat[rank + 1 + nz_below, col:] = (
                mat[rank + 1 + nz_below, col:] - factors * piv_row[None, :]
            ) % mod
        rank += 1
    return rank


def polys_to_dense_mod(polys: List[Poly], mod: int = MOD) -> np.ndarray:
    """Convert list of sparse polynomials to dense int64 matrix over F_mod."""
    monom_to_col: Dict[Tuple[int, ...], int] = {}
    for p in polys:
        for m, c in p.items():
            if c % mod != 0 and m not in monom_to_col:
                monom_to_col[m] = len(monom_to_col)
    n_cols = max(1, len(monom_to_col))
    mat = np.zeros((len(polys), n_cols), dtype=np.int64)
    for r_idx, p in enumerate(polys):
        for m, c in p.items():
            v = c % mod
            if v:
                mat[r_idx, monom_to_col[m]] = v
    return mat


def apolar_betti_deg4_ungraded(
    f: Poly, num_vars: int, mod: int = MOD
) -> Tuple[int, int, int, int, int, int]:
    """
    Compute exact ungraded invariants of f^perp up to degree 4:
      (dim_f2, beta_1_3, beta_2_3, beta_1_4, beta_2_4, beta_3_4).
    """
    pairs2 = [(i, j) for i in range(num_vars) for j in range(i, num_vars)]
    pair2_to_idx = {pair: idx for idx, pair in enumerate(pairs2)}
    m2 = len(pairs2)

    # 1) f^perp_2 basis
    p2_polys: List[Poly] = []
    for i, j in pairs2:
        dij = partial_deriv(partial_deriv(f, i), j)
        p2_polys.append({m: c % mod for m, c in dij.items() if c % mod != 0} if dij else {})
    A2 = polys_to_dense_mod(p2_polys, mod=mod)
    f2_basis = right_nullspace_mod(A2.T, mod=mod)
    dim_f2 = f2_basis.shape[0]
    if dim_f2 > 0:
        assert not np.any((f2_basis @ A2) % mod), "f^perp_2 kernel check failed"

    dual_quadrics: List[Poly] = []
    for row in f2_basis:
        q: Poly = {}
        for idx in np.nonzero(row)[0]:
            i, j = pairs2[int(idx)]
            exp = [0] * num_vars
            exp[i] += 1
            exp[j] += 1
            q[tuple(exp)] = int(row[idx])
        dual_quadrics.append(q)

    y_vars = [var_poly(k, num_vars) for k in range(num_vars)]

    # 2) phi_3: V^* \otimes f^perp_2 -> S^3 V^*
    phi3_polys = [mul_poly(y_vars[k], dual_quadrics[q]) for k in range(num_vars) for q in range(dim_f2)]
    phi3_mat = polys_to_dense_mod(phi3_polys, mod=mod)
    syz3_basis = right_nullspace_mod(phi3_mat.T, mod=mod)
    beta_2_3 = syz3_basis.shape[0]
    if beta_2_3 > 0:
        assert not np.any((syz3_basis @ phi3_mat) % mod), "Syz_1(f^perp)_3 kernel check failed"
    dim_v_f2 = num_vars * dim_f2 - beta_2_3

    d3_dim = rank_mod_numpy(kth_partial_space(f, num_vars, 3), mod=mod)
    dim_f3 = math.comb(num_vars + 2, 3) - d3_dim
    assert dim_v_f2 <= dim_f3
    beta_1_3 = dim_f3 - dim_v_f2

    # 3) phi_4: S^2 V^* \otimes f^perp_2 -> S^4 V^*
    y_quads = []
    for a, b in pairs2:
        exp = [0] * num_vars
        exp[a] += 1
        exp[b] += 1
        y_quads.append({tuple(exp): 1})

    phi4_polys = [mul_poly(y_quads[p2_i], dual_quadrics[q]) for p2_i in range(m2) for q in range(dim_f2)]
    phi4_mat = polys_to_dense_mod(phi4_polys, mod=mod)
    dim_s2_f2 = rank_matrix_mod(phi4_mat, mod=mod)
    dim_syz1_4 = m2 * dim_f2 - dim_s2_f2

    d4_polys = kth_partial_space(f, num_vars, 4)
    d4_dim = rank_mod_numpy(d4_polys, mod=mod) if d4_polys else 0
    dim_f4 = math.comb(num_vars + 3, 4) - d4_dim
    assert dim_s2_f2 <= dim_f4
    beta_1_4 = dim_f4 - dim_s2_f2

    # 4) V^* . Syz_1(f^perp)_3 inside S^2 V^* \otimes f^perp_2
    shifted_syz3 = np.zeros((num_vars * beta_2_3, m2 * dim_f2), dtype=np.int64)
    for s_idx in range(beta_2_3):
        nz_cols = np.nonzero(syz3_basis[s_idx])[0]
        for l in range(num_vars):
            row_idx = l * beta_2_3 + s_idx
            for c_idx in nz_cols:
                k, q = divmod(int(c_idx), dim_f2)
                a, b = (l, k) if l <= k else (k, l)
                t_col = pair2_to_idx[(a, b)] * dim_f2 + q
                shifted_syz3[row_idx, t_col] = (
                    shifted_syz3[row_idx, t_col] + int(syz3_basis[s_idx, c_idx])
                ) % mod

    if shifted_syz3.shape[0] > 0:
        assert not np.any((shifted_syz3 @ phi4_mat) % mod), "Shifted syz3 not in ker(phi_4)!"
    dim_v_syz3 = rank_matrix_mod(shifted_syz3, mod=mod)
    beta_2_4 = dim_syz1_4 - dim_v_syz3
    beta_3_4 = num_vars * beta_2_3 - dim_v_syz3
    assert beta_2_4 >= 0 and beta_3_4 >= 0
    return dim_f2, beta_1_3, beta_2_3, beta_1_4, beta_2_4, beta_3_4


Multideg = Tuple[Tuple[int, ...], Tuple[int, ...]]


def monom_multideg(m: Tuple[int, ...], n: int) -> Multideg:
    r = tuple(sum(m[i * n + j] for j in range(n)) for i in range(n))
    c = tuple(sum(m[i * n + j] for i in range(n)) for j in range(n))
    return (r, c)


def add_mdeg(a: Multideg, b: Multideg) -> Multideg:
    return (
        tuple(x + y for x, y in zip(a[0], b[0])),
        tuple(x + y for x, y in zip(a[1], b[1])),
    )


def apolar_betti_deg4_torus(
    f: Poly, n: int, mod: int = MOD
) -> Tuple[Tuple[int, int, int, int, int, int], Dict[Multideg, Tuple[int, int, int]]]:
    """
    Exact torus-multigraded apolar ideal Betti invariants through degree 4 for
    bihomogeneous polynomials (perm_n, det_n).
    Returns:
      totals = (dim_f2, beta_1_3, beta_2_3, beta_1_4, beta_2_4, beta_3_4)
      block_stats[mdeg4] = (beta_1_4_blk, beta_2_4_blk, beta_3_4_blk)
    """
    num_vars = n * n
    pairs2 = [(i, j) for i in range(num_vars) for j in range(i, num_vars)]
    pair2_to_idx = {pair: idx for idx, pair in enumerate(pairs2)}

    # Precompute multidegrees of y_k and y_a y_b
    var_mdeg: List[Multideg] = []
    for k in range(num_vars):
        exp = [0] * num_vars
        exp[k] = 1
        var_mdeg.append(monom_multideg(tuple(exp), n))

    pair2_mdeg: List[Multideg] = []
    pair2_poly: List[Poly] = []
    pair2_by_mdeg: Dict[Multideg, List[int]] = defaultdict(list)
    for p_idx, (a, b) in enumerate(pairs2):
        exp = [0] * num_vars
        exp[a] += 1
        exp[b] += 1
        t = tuple(exp)
        md = monom_multideg(t, n)
        pair2_mdeg.append(md)
        pair2_poly.append({t: 1})
        pair2_by_mdeg[md].append(p_idx)

    # 1) Blockwise f^perp_2
    f2_quadrics_by_mdeg: Dict[Multideg, List[Poly]] = {}
    dim_f2_total = 0
    for md2, p_indices in pair2_by_mdeg.items():
        p2_polys: List[Poly] = []
        for p_idx in p_indices:
            i, j = pairs2[p_idx]
            dij = partial_deriv(partial_deriv(f, i), j)
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

    y_vars = [var_poly(k, num_vars) for k in range(num_vars)]

    # Group all degree-3 monomials & 3rd partials by multidegree for beta_1_3
    deg3_monoms_by_mdeg: Dict[Multideg, int] = defaultdict(int)
    for comb in itertools.combinations_with_replacement(range(num_vars), 3):
        exp = [0] * num_vars
        for idx in comb:
            exp[idx] += 1
        deg3_monoms_by_mdeg[monom_multideg(tuple(exp), n)] += 1

    d3_partials_by_mdeg: Dict[Multideg, List[Poly]] = defaultdict(list)
    for comb in itertools.combinations_with_replacement(range(num_vars), 3):
        exp = [0] * num_vars
        for idx in comb:
            exp[idx] += 1
        md = monom_multideg(tuple(exp), n)
        if max(md[0]) > 1 or max(md[1]) > 1:
            continue
        cur = f
        for v in comb:
            cur = partial_deriv(cur, v)
            if not cur:
                break
        if cur:
            d3_partials_by_mdeg[md].append({m: c % mod for m, c in cur.items() if c % mod != 0})

    # 2) Blockwise phi_3 and Syz_1(f^perp)_3
    gens3_by_mdeg: Dict[Multideg, List[Tuple[int, Multideg, int]]] = defaultdict(list)
    for md2, q_list in f2_quadrics_by_mdeg.items():
        for q_loc in range(len(q_list)):
            for k in range(num_vars):
                md3 = add_mdeg(var_mdeg[k], md2)
                gens3_by_mdeg[md3].append((k, md2, q_loc))

    syz3_by_mdeg: Dict[Multideg, Tuple[List[Tuple[int, Multideg, int]], np.ndarray]] = {}
    beta_1_3_total = 0
    beta_2_3_total = 0
    all_md3 = set(deg3_monoms_by_mdeg.keys())
    for md3 in all_md3:
        gens3 = gens3_by_mdeg.get(md3, [])
        d3_rank = rank_mod_numpy(d3_partials_by_mdeg.get(md3, []), mod=mod)
        dim_f3_blk = deg3_monoms_by_mdeg[md3] - d3_rank
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

    # Group all degree-4 monomials & 4th partials by multidegree for beta_1_4
    deg4_monoms_by_mdeg: Dict[Multideg, int] = defaultdict(int)
    for comb in itertools.combinations_with_replacement(range(num_vars), 4):
        exp = [0] * num_vars
        for idx in comb:
            exp[idx] += 1
        deg4_monoms_by_mdeg[monom_multideg(tuple(exp), n)] += 1

    d4_rank_by_mdeg: Dict[Multideg, int] = defaultdict(int)
    if n == 4:
        # For perm_4 and det_4 (degree 4, multidegree (1,1,1,1; 1,1,1,1)), d^4 f is nonzero only at (1,1,1,1;1,1,1,1)
        full_md = ((1,) * 4, (1,) * 4)
        d4_rank_by_mdeg[full_md] = 1

    # 3) Blockwise phi_4 and V^* . Syz_1(f^perp)_3
    gens4_by_mdeg: Dict[Multideg, List[Tuple[int, Multideg, int]]] = defaultdict(list)
    for md2, q_list in f2_quadrics_by_mdeg.items():
        for q_loc in range(len(q_list)):
            for p2_idx in range(len(pairs2)):
                md4 = add_mdeg(pair2_mdeg[p2_idx], md2)
                gens4_by_mdeg[md4].append((p2_idx, md2, q_loc))

    shifted3_by_mdeg: Dict[Multideg, List[Tuple[int, Multideg, int]]] = defaultdict(list)
    for md3, (_, syz_blk) in syz3_by_mdeg.items():
        for s_loc in range(syz_blk.shape[0]):
            for l in range(num_vars):
                md4 = add_mdeg(var_mdeg[l], md3)
                shifted3_by_mdeg[md4].append((l, md3, s_loc))

    beta_1_4_total = 0
    beta_2_4_total = 0
    beta_3_4_total = 0
    block_stats: Dict[Multideg, Tuple[int, int, int]] = {}

    for md4, dim_s4_blk in deg4_monoms_by_mdeg.items():
        dim_f4_blk = dim_s4_blk - d4_rank_by_mdeg.get(md4, 0)
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
                    p2_idx = pair2_to_idx[(a, b)]
                    t_col = gen4_to_col[(p2_idx, q_md2, q_loc)]
                    shift_mat[row_i, t_col] = (shift_mat[row_i, t_col] + int(vec[c_idx])) % mod
            assert not np.any((shift_mat @ phi4_blk) % mod), f"Shifted syz3 failed ker check at {md4}"
            dim_v_syz3_blk = rank_matrix_mod(shift_mat, mod=mod)
        else:
            dim_v_syz3_blk = 0

        b24_blk = dim_syz1_4_blk - dim_v_syz3_blk
        b34_blk = len(shifts4) - dim_v_syz3_blk
        assert b24_blk >= 0 and b34_blk >= 0

        beta_1_4_total += b14_blk
        beta_2_4_total += b24_blk
        beta_3_4_total += b34_blk
        block_stats[md4] = (b14_blk, b24_blk, b34_blk)

    totals = (
        dim_f2_total,
        beta_1_3_total,
        beta_2_3_total,
        beta_1_4_total,
        beta_2_4_total,
        beta_3_4_total,
    )
    return totals, block_stats


def main() -> None:
    p3 = permanent_poly(3)
    d3 = determinant_poly(3)

    # Self-check 1: GL_9 shear invariance
    s_orig = apolar_betti_deg4_ungraded(p3, 9)
    s_shear = apolar_betti_deg4_ungraded(substitute_shear_x0_plus_2x1(p3, 9), 9)
    assert s_orig == s_shear, f"GL_9 shear invariance failed: {s_orig} != {s_shear}"

    # Self-check 2: ungraded vs torus-multigraded cross-check on perm_3 and det_3
    t_p3, _ = apolar_betti_deg4_torus(p3, 3)
    t_d3, _ = apolar_betti_deg4_torus(d3, 3)
    s_d3 = apolar_betti_deg4_ungraded(d3, 9)
    assert s_orig == t_p3, f"perm_3 torus cross-check failed: {s_orig} != {t_p3}"
    assert s_d3 == t_d3, f"det_3 torus cross-check failed: {s_d3} != {t_d3}"
    print(f"[Self-Checks] GL_9 shear invariance={s_orig}; torus cross-check perm_3 & det_3 OK\n")

    rng = random.Random(123)
    n3_models = [
        ("det_3", d3),
        ("m=4 (1,2)", recenter_poly_from_mod(layered_abp_det_split(1, 2, 9, rng))),
        ("m=5 (2,2)", recenter_poly_from_mod(layered_abp_det_split(2, 2, 9, rng))),
        ("m=6 (1,4)", recenter_poly_from_mod(layered_abp_det_split(1, 4, 9, rng))),
        ("m=6 (2,3)", recenter_poly_from_mod(layered_abp_det_split(2, 3, 9, rng))),
        ("perm_3", p3),
        ("m=7 (3,3)", recenter_poly_from_mod(layered_abp_det_split(3, 3, 9, rng))),
        ("det_3 + det_3", recenter_poly_from_mod(sum_of_two_det3(9, rng))),
    ]

    print("=== n=3 (N=9, d=3) Macaulay Apolar Ideal f^perp Betti Table (deg 2..4) ===")
    print("Model           | dim(f^p_2) | b_{1,3} | b_{2,3} | b_{1,4} | b_{2,4} | b_{3,4}")
    print("-" * 77)
    for name, poly in n3_models:
        df2, b13, b23, b14, b24, b34 = apolar_betti_deg4_ungraded(poly, 9)
        print(f"{name:15s} | {df2:10d} | {b13:7d} | {b23:7d} | {b14:7d} | {b24:7d} | {b34:7d}")

    p4 = permanent_poly(4)
    d4 = determinant_poly(4)
    tot_p4, blk_p4 = apolar_betti_deg4_torus(p4, 4)
    tot_d4, blk_d4 = apolar_betti_deg4_torus(d4, 4)

    print("\n=== n=4 (N=16, d=4) Macaulay Apolar Ideal f^perp Betti Table (deg 2..4) ===")
    print("Model   | dim(f^p_2) | b_{1,3} | b_{2,3} | b_{1,4} | b_{2,4} | b_{3,4}")
    print("-" * 71)
    for name, tot in [("det_4", tot_d4), ("perm_4", tot_p4)]:
        df2, b13, b23, b14, b24, b34 = tot
        print(f"{name:7s} | {df2:10d} | {b13:7d} | {b23:7d} | {b14:7d} | {b24:7d} | {b34:7d}")

    diffs = []
    for md4 in sorted(blk_p4.keys()):
        vp = blk_p4[md4]
        vd = blk_d4[md4]
        if vp != vd:
            diffs.append((md4, vp, vd))
    print(f"\nMultidegree blocks where perm_4 != det_4 in (b14, b24, b34): {len(diffs)}")
    for md4, vp, vd in diffs[:15]:
        print(f"  mdeg={md4}: perm_4={vp} vs det_4={vd}")


if __name__ == "__main__":
    main()
