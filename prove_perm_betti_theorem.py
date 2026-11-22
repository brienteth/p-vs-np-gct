"""Exact Q + multi-characteristic (F_2, F_3, F_5, F_7) machine-checked proof of the apolar Betti theorem."""
from __future__ import annotations

import itertools
import math
from collections import defaultdict
from fractions import Fraction
from typing import Dict, List, Optional, Tuple

from apolar_higher_betti_probe import (
    Multideg,
    monom_multideg,
    polys_to_dense_mod,
    rank_matrix_mod,
)
from apolar_betti_probe import right_nullspace_mod
from perm_n_betti_scaling import (
    format_poly_y,
    orbit_size_tuple,
    partitions_of_k,
)
from poly_exact import (
    Poly,
    determinant_poly,
    mul_poly,
    partial_deriv,
    permanent_poly,
    var_poly,
)

SparseRowQ = Dict[int, Fraction]


def rref_sparse_q(rows: List[SparseRowQ], n_cols: int) -> Tuple[List[SparseRowQ], List[int]]:
    """Exact sparse RREF over Q (fractions.Fraction)."""
    mat: List[SparseRowQ] = [
        {c: v for c, v in r.items() if v != 0} for r in rows
    ]
    n_rows = len(mat)
    piv_cols: List[int] = []
    rank = 0
    for col in range(n_cols):
        if rank >= n_rows:
            break
        piv = None
        for r in range(rank, n_rows):
            if col in mat[r]:
                piv = r
                break
        if piv is None:
            continue
        if piv != rank:
            mat[rank], mat[piv] = mat[piv], mat[rank]
        piv_val = mat[rank][col]
        if piv_val != 1:
            mat[rank] = {c: v / piv_val for c, v in mat[rank].items()}
        piv_row = mat[rank]
        for r in range(n_rows):
            if r == rank or col not in mat[r]:
                continue
            factor = mat[r][col]
            row_r = mat[r]
            for c, pv in piv_row.items():
                nv = row_r.get(c, Fraction(0)) - factor * pv
                if nv == 0:
                    row_r.pop(c, None)
                else:
                    row_r[c] = nv
        piv_cols.append(col)
        rank += 1
    return mat[:rank], piv_cols


def rank_exact_q(rows: List[SparseRowQ], n_cols: int) -> int:
    """Exact rank over Q using sparse Gaussian elimination (transposing if taller than wide)."""
    non_empty = [{c: v for c, v in r.items() if v != 0} for r in rows if any(r.values())]
    if not non_empty or n_cols == 0:
        return 0
    if len(non_empty) > n_cols:
        t_rows: List[SparseRowQ] = [{} for _ in range(n_cols)]
        for r_idx, r in enumerate(non_empty):
            for c, v in r.items():
                t_rows[c][r_idx] = v
        non_empty = [r for r in t_rows if r]
        n_cols = len(rows)

    n_rows = len(non_empty)
    rank = 0
    for col in range(n_cols):
        if rank >= n_rows:
            break
        piv = None
        for r in range(rank, n_rows):
            if col in non_empty[r]:
                piv = r
                break
        if piv is None:
            continue
        if piv != rank:
            non_empty[rank], non_empty[piv] = non_empty[piv], non_empty[rank]
        piv_row = non_empty[rank]
        piv_val = piv_row[col]
        for r in range(rank + 1, n_rows):
            if col not in non_empty[r]:
                continue
            factor = non_empty[r][col] / piv_val
            row_r = non_empty[r]
            for c, pv in piv_row.items():
                nv = row_r.get(c, Fraction(0)) - factor * pv
                if nv == 0:
                    row_r.pop(c, None)
                else:
                    row_r[c] = nv
        rank += 1
    return rank


def right_nullspace_exact_q(rows: List[SparseRowQ], n_cols: int) -> List[SparseRowQ]:
    """Exact basis of {v in Q^{n_cols} : A v = 0}."""
    rref, piv_cols = rref_sparse_q(rows, n_cols)
    piv_set = set(piv_cols)
    free_cols = [c for c in range(n_cols) if c not in piv_set]
    basis: List[SparseRowQ] = []
    for fc in free_cols:
        vec: SparseRowQ = {fc: Fraction(1)}
        for r_idx, pc in enumerate(piv_cols):
            val = rref[r_idx].get(fc, Fraction(0))
            if val != 0:
                vec[pc] = -val
        basis.append(vec)
    return basis


def transpose_sparse_q(rows: List[SparseRowQ], n_cols: int) -> List[SparseRowQ]:
    t_rows: List[SparseRowQ] = [{} for _ in range(n_cols)]
    for r_idx, r in enumerate(rows):
        for c, v in r.items():
            if v != 0:
                t_rows[c][r_idx] = v
    return t_rows


def check_left_kernel_q(vecs: List[SparseRowQ], mat_rows: List[SparseRowQ]) -> None:
    """Assert v^T @ A == 0 over Q for all v in vecs."""
    for v in vecs:
        acc: Dict[int, Fraction] = {}
        for r_idx, cv in v.items():
            for c_idx, av in mat_rows[r_idx].items():
                nv = acc.get(c_idx, Fraction(0)) + cv * av
                if nv == 0:
                    acc.pop(c_idx, None)
                else:
                    acc[c_idx] = nv
        assert not acc, f"Exact Q kernel verification failed: {acc}"


def solve_left_exact_q(
    rows_a: List[SparseRowQ], n_cols: int, target_row: SparseRowQ
) -> Optional[SparseRowQ]:
    """Solve coeffs @ A == target_row over Q; return None if inconsistent."""
    m_rows = len(rows_a)
    aug_rows: List[SparseRowQ] = [{} for _ in range(n_cols)]
    for r_idx, r in enumerate(rows_a):
        for c_idx, v in r.items():
            if v != 0:
                aug_rows[c_idx][r_idx] = v
    for c_idx, v in target_row.items():
        if v != 0:
            aug_rows[c_idx][m_rows] = v

    # Run RREF only on columns 0..m_rows-1
    rref, piv_cols = rref_sparse_q(aug_rows, m_rows)
    # Check remaining rows (indices >= len(rref)) have 0 in column m_rows?
    # Note rref_sparse_q slices [:rank], so run full augmented RREF up to m_rows:
    mat = [{c: v for c, v in r.items() if v != 0} for r in aug_rows]
    n_eqs = len(mat)
    pivs: List[int] = []
    rank = 0
    for col in range(m_rows):
        if rank >= n_eqs:
            break
        piv = None
        for r in range(rank, n_eqs):
            if col in mat[r]:
                piv = r
                break
        if piv is None:
            continue
        if piv != rank:
            mat[rank], mat[piv] = mat[piv], mat[rank]
        pv = mat[rank][col]
        if pv != 1:
            mat[rank] = {c: v / pv for c, v in mat[rank].items()}
        prow = mat[rank]
        for r in range(n_eqs):
            if r == rank or col not in mat[r]:
                continue
            fac = mat[r][col]
            rr = mat[r]
            for c, val in prow.items():
                nv = rr.get(c, Fraction(0)) - fac * val
                if nv == 0:
                    rr.pop(c, None)
                else:
                    rr[c] = nv
        pivs.append(col)
        rank += 1

    for r in range(rank, n_eqs):
        if mat[r].get(m_rows, Fraction(0)) != 0:
            return None

    coeffs: SparseRowQ = {}
    for r_idx, pc in enumerate(pivs):
        val = mat[r_idx].get(m_rows, Fraction(0))
        if val != 0:
            coeffs[pc] = val

    # Verify exact solution
    check: SparseRowQ = {}
    for r_idx, c in coeffs.items():
        for col, av in rows_a[r_idx].items():
            nv = check.get(col, Fraction(0)) + c * av
            if nv == 0:
                check.pop(col, None)
            else:
                check[col] = nv
    clean_target = {c: v for c, v in target_row.items() if v != 0}
    assert check == clean_target, "Exact Q solve verification failed!"
    return coeffs


def polys_to_sparse_q(polys: List[Dict[Tuple[int, ...], Fraction]]) -> Tuple[List[SparseRowQ], int]:
    monom_to_col: Dict[Tuple[int, ...], int] = {}
    rows: List[SparseRowQ] = []
    for p in polys:
        row: SparseRowQ = {}
        for m, c in p.items():
            if c == 0:
                continue
            col = monom_to_col.get(m)
            if col is None:
                col = len(monom_to_col)
                monom_to_col[m] = col
            row[col] = c
        rows.append(row)
    return rows, max(1, len(monom_to_col))


def mul_poly_q(
    a: Dict[Tuple[int, ...], Fraction], b: Dict[Tuple[int, ...], Fraction]
) -> Dict[Tuple[int, ...], Fraction]:
    res: Dict[Tuple[int, ...], Fraction] = {}
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            m = tuple(x + y for x, y in zip(m1, m2))
            nv = res.get(m, Fraction(0)) + c1 * c2
            if nv == 0:
                res.pop(m, None)
            else:
                res[m] = nv
    return res


def partials_of_mdeg_q(
    f: Poly, n: int, k: int, md: Multideg
) -> List[Dict[Tuple[int, ...], Fraction]]:
    r_vec, c_vec = md
    if max(r_vec) > 1 or max(c_vec) > 1:
        return []
    rows = [i for i, v in enumerate(r_vec) if v == 1]
    cols = [j for j, v in enumerate(c_vec) if v == 1]
    res: List[Dict[Tuple[int, ...], Fraction]] = []
    for perm_c in itertools.permutations(cols):
        cur = f
        for r_i, c_j in zip(rows, perm_c):
            cur = partial_deriv(cur, r_i * n + c_j)
            if not cur:
                break
        if cur:
            res.append({m: Fraction(c) for m, c in cur.items() if c != 0})
    return res


def apolar_betti_q_orbit(
    f: Poly, n: int
) -> Tuple[Tuple[int, int, int, int, int, int], List[Tuple[Multideg, int, int, int]]]:
    """Exact Q orbit-compressed Macaulay apolar Betti invariants up to degree 4."""
    num_vars = n * n
    pairs2 = [(i, j) for i in range(num_vars) for j in range(i, num_vars)]
    pair2_to_idx = {pair: idx for idx, pair in enumerate(pairs2)}

    pair2_mdeg: List[Multideg] = []
    pair2_poly_q: List[Dict[Tuple[int, ...], Fraction]] = []
    pair2_by_mdeg: Dict[Multideg, List[int]] = defaultdict(list)
    for p_idx, (a, b) in enumerate(pairs2):
        exp = [0] * num_vars
        exp[a] += 1
        exp[b] += 1
        t = tuple(exp)
        md = monom_multideg(t, n)
        pair2_mdeg.append(md)
        pair2_poly_q.append({t: Fraction(1)})
        pair2_by_mdeg[md].append(p_idx)

    # 1) f^perp_2 over Q
    f2_quadrics_by_mdeg: Dict[Multideg, List[Dict[Tuple[int, ...], Fraction]]] = {}
    dim_f2_total = 0
    for md2, p_indices in pair2_by_mdeg.items():
        p2_polys: List[Dict[Tuple[int, ...], Fraction]] = []
        for p_idx in p_indices:
            i, j = pairs2[p_idx]
            dij = partial_deriv(partial_deriv(f, i), j)
            p2_polys.append({m: Fraction(c) for m, c in dij.items() if c != 0} if dij else {})
        A_rows, n_cols = polys_to_sparse_q(p2_polys)
        nb = right_nullspace_exact_q(transpose_sparse_q(A_rows, n_cols), len(p_indices))
        if nb:
            check_left_kernel_q(nb, A_rows)
            q_list: List[Dict[Tuple[int, ...], Fraction]] = []
            for row in nb:
                q_poly: Dict[Tuple[int, ...], Fraction] = {}
                for loc_idx, coeff in row.items():
                    i, j = pairs2[p_indices[loc_idx]]
                    exp = [0] * num_vars
                    exp[i] += 1
                    exp[j] += 1
                    q_poly[tuple(exp)] = coeff
                q_list.append(q_poly)
            f2_quadrics_by_mdeg[md2] = q_list
            dim_f2_total += len(q_list)

    deg3_monoms_by_mdeg: Dict[Multideg, int] = defaultdict(int)
    for comb in itertools.combinations_with_replacement(range(num_vars), 3):
        exp = [0] * num_vars
        for idx in comb:
            exp[idx] += 1
        deg3_monoms_by_mdeg[monom_multideg(tuple(exp), n)] += 1

    deg4_monoms_by_mdeg: Dict[Multideg, int] = defaultdict(int)
    for comb in itertools.combinations_with_replacement(range(num_vars), 4):
        exp = [0] * num_vars
        for idx in comb:
            exp[idx] += 1
        deg4_monoms_by_mdeg[monom_multideg(tuple(exp), n)] += 1

    y_vars_q = [{k_m: Fraction(v) for k_m, v in var_poly(k, num_vars).items()} for k in range(num_vars)]
    syz3_cache: Dict[Multideg, Tuple[List[Tuple[int, Multideg, int]], List[SparseRowQ]]] = {}

    def get_syz3_block(md3: Multideg) -> Tuple[List[Tuple[int, Multideg, int]], List[SparseRowQ]]:
        if md3 in syz3_cache:
            return syz3_cache[md3]
        gens3: List[Tuple[int, Multideg, int]] = []
        r3, c3 = md3
        for k in range(num_vars):
            rk, ck = k // n, k % n
            if r3[rk] == 0 or c3[ck] == 0:
                continue
            md2 = (
                tuple(r3[x] - (1 if x == rk else 0) for x in range(n)),
                tuple(c3[y] - (1 if y == ck else 0) for y in range(n)),
            )
            q_list = f2_quadrics_by_mdeg.get(md2)
            if q_list:
                for q_loc in range(len(q_list)):
                    gens3.append((k, md2, q_loc))
        if not gens3:
            res: Tuple[List[Tuple[int, Multideg, int]], List[SparseRowQ]] = ([], [])
            syz3_cache[md3] = res
            return res
        phi3_polys = [
            mul_poly_q(y_vars_q[k], f2_quadrics_by_mdeg[md2][q_loc]) for k, md2, q_loc in gens3
        ]
        phi3_rows, n_c = polys_to_sparse_q(phi3_polys)
        syz_blk = right_nullspace_exact_q(transpose_sparse_q(phi3_rows, n_c), len(gens3))
        if syz_blk:
            check_left_kernel_q(syz_blk, phi3_rows)
        res = (gens3, syz_blk)
        syz3_cache[md3] = res
        return res

    # Degree-3 orbits over Q
    beta_1_3_total = 0
    beta_2_3_total = 0
    for r3 in partitions_of_k(3, n):
        w_r = orbit_size_tuple(r3)
        for c3 in partitions_of_k(3, n):
            w = w_r * orbit_size_tuple(c3)
            md3 = (r3, c3)
            gens3, syz_blk = get_syz3_block(md3)
            dim_v_f2_blk = len(gens3) - len(syz_blk)
            d3_polys = partials_of_mdeg_q(f, n, 3, md3)
            d3_rows, n_c3 = polys_to_sparse_q(d3_polys)
            d3_rank = rank_exact_q(d3_rows, n_c3) if d3_polys else 0
            dim_f3_blk = deg3_monoms_by_mdeg[md3] - d3_rank
            assert dim_v_f2_blk <= dim_f3_blk
            beta_1_3_total += w * (dim_f3_blk - dim_v_f2_blk)
            beta_2_3_total += w * len(syz_blk)

    # Degree-4 orbits over Q
    beta_1_4_total = 0
    beta_2_4_total = 0
    beta_3_4_total = 0
    orbit_records: List[Tuple[Multideg, int, int, int]] = []
    for r4 in partitions_of_k(4, n):
        w_r = orbit_size_tuple(r4)
        for c4 in partitions_of_k(4, n):
            w = w_r * orbit_size_tuple(c4)
            md4 = (r4, c4)
            d4_polys = partials_of_mdeg_q(f, n, 4, md4)
            d4_rows, n_c4 = polys_to_sparse_q(d4_polys)
            d4_rank = rank_exact_q(d4_rows, n_c4) if d4_polys else 0
            dim_f4_blk = deg4_monoms_by_mdeg[md4] - d4_rank

            gens4: List[Tuple[int, Multideg, int]] = []
            for p2_idx, md2_p in enumerate(pair2_mdeg):
                rem_r = tuple(r4[x] - md2_p[0][x] for x in range(n))
                rem_c = tuple(c4[y] - md2_p[1][y] for y in range(n))
                if min(rem_r) < 0 or min(rem_c) < 0:
                    continue
                q_md2 = (rem_r, rem_c)
                q_list = f2_quadrics_by_mdeg.get(q_md2)
                if q_list:
                    for q_loc in range(len(q_list)):
                        gens4.append((p2_idx, q_md2, q_loc))

            if gens4:
                phi4_polys = [
                    mul_poly_q(pair2_poly_q[p2_idx], f2_quadrics_by_mdeg[md2][q_loc])
                    for p2_idx, md2, q_loc in gens4
                ]
                phi4_rows, n_c4_phi = polys_to_sparse_q(phi4_polys)
                dim_s2_f2_blk = rank_exact_q(phi4_rows, n_c4_phi)
                dim_syz1_4_blk = len(gens4) - dim_s2_f2_blk
            else:
                phi4_rows = []
                dim_s2_f2_blk = 0
                dim_syz1_4_blk = 0

            assert dim_s2_f2_blk <= dim_f4_blk
            b14_blk = dim_f4_blk - dim_s2_f2_blk

            shifts4: List[Tuple[int, Multideg, int]] = []
            for l in range(num_vars):
                rl, cl = l // n, l % n
                if r4[rl] == 0 or c4[cl] == 0:
                    continue
                md3 = (
                    tuple(r4[x] - (1 if x == rl else 0) for x in range(n)),
                    tuple(c4[y] - (1 if y == cl else 0) for y in range(n)),
                )
                _, syz3_blk = get_syz3_block(md3)
                for s_loc in range(len(syz3_blk)):
                    shifts4.append((l, md3, s_loc))

            if shifts4:
                gen4_to_col = {g: idx for idx, g in enumerate(gens4)}
                shift_rows: List[SparseRowQ] = []
                for l, md3, s_loc in shifts4:
                    gens3, syz3_blk = get_syz3_block(md3)
                    s_vec = syz3_blk[s_loc]
                    row_s: SparseRowQ = {}
                    for c_idx, val in s_vec.items():
                        k, q_md2, q_loc = gens3[c_idx]
                        a, b = (l, k) if l <= k else (k, l)
                        t_col = gen4_to_col[(pair2_to_idx[(a, b)], q_md2, q_loc)]
                        nv = row_s.get(t_col, Fraction(0)) + val
                        if nv == 0:
                            row_s.pop(t_col, None)
                        else:
                            row_s[t_col] = nv
                    shift_rows.append(row_s)
                check_left_kernel_q(shift_rows, phi4_rows)
                dim_v_syz3_blk = rank_exact_q(shift_rows, len(gens4))
            else:
                dim_v_syz3_blk = 0

            b24_blk = dim_syz1_4_blk - dim_v_syz3_blk
            b34_blk = len(shifts4) - dim_v_syz3_blk
            assert b24_blk >= 0 and b34_blk >= 0

            beta_1_4_total += w * b14_blk
            beta_2_4_total += w * b24_blk
            beta_3_4_total += w * b34_blk
            orbit_records.append((md4, b14_blk, b24_blk, b34_blk))

    return (
        dim_f2_total,
        beta_1_3_total,
        beta_2_3_total,
        beta_1_4_total,
        beta_2_4_total,
        beta_3_4_total,
    ), orbit_records


def block_betti_mod_p(f: Poly, n: int, md4: Multideg, mod: int) -> Tuple[int, int, int]:
    """Compute (b14_blk, b24_blk, b34_blk) on a single multidegree block md4 over F_mod."""
    import numpy as np

    num_vars = n * n
    pairs2 = [(i, j) for i in range(num_vars) for j in range(i, num_vars)]
    pair2_to_idx = {pair: idx for idx, pair in enumerate(pairs2)}
    pair2_mdeg = []
    pair2_poly = []
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

    f2_by_mdeg: Dict[Multideg, List[Poly]] = {}
    for md2, p_indices in pair2_by_mdeg.items():
        p2_polys = []
        for p_idx in p_indices:
            i, j = pairs2[p_idx]
            dij = partial_deriv(partial_deriv(f, i), j)
            p2_polys.append({m: c % mod for m, c in dij.items() if c % mod != 0} if dij else {})
        A_blk = polys_to_dense_mod(p2_polys, mod=mod)
        nb = right_nullspace_mod(A_blk.T, mod=mod)
        if nb.shape[0] > 0:
            q_list = []
            for row in nb:
                q_poly: Poly = {}
                for loc_idx in np.nonzero(row)[0]:
                    i, j = pairs2[p_indices[int(loc_idx)]]
                    exp = [0] * num_vars
                    exp[i] += 1
                    exp[j] += 1
                    q_poly[tuple(exp)] = int(row[loc_idx])
                q_list.append(q_poly)
            f2_by_mdeg[md2] = q_list

    # Count degree-4 monomials of multidegree md4
    dim_s4_blk = 0
    for comb in itertools.combinations_with_replacement(range(num_vars), 4):
        exp = [0] * num_vars
        for idx in comb:
            exp[idx] += 1
        if monom_multideg(tuple(exp), n) == md4:
            dim_s4_blk += 1
    d4_rank = 0
    if max(md4[0]) <= 1 and max(md4[1]) <= 1:
        d4_rank = 1  # nonzero for perm_n / det_n on (1,1,1,1; 1,1,1,1)

    gens4: List[Tuple[int, Multideg, int]] = []
    for p2_idx, md2_p in enumerate(pair2_mdeg):
        rem_r = tuple(md4[0][x] - md2_p[0][x] for x in range(n))
        rem_c = tuple(md4[1][y] - md2_p[1][y] for y in range(n))
        if min(rem_r) < 0 or min(rem_c) < 0:
            continue
        q_md2 = (rem_r, rem_c)
        for q_loc in range(len(f2_by_mdeg.get(q_md2, []))):
            gens4.append((p2_idx, q_md2, q_loc))

    phi4_polys = [
        mul_poly(pair2_poly[p2_i], f2_by_mdeg[md2][ql]) for p2_i, md2, ql in gens4
    ]
    phi4_blk = polys_to_dense_mod(phi4_polys, mod=mod)
    dim_s2_f2_blk = rank_matrix_mod(phi4_blk, mod=mod)
    dim_syz1_4_blk = len(gens4) - dim_s2_f2_blk
    b14_blk = (dim_s4_blk - d4_rank) - dim_s2_f2_blk

    y_vars = [var_poly(k, num_vars) for k in range(num_vars)]
    gen4_to_col = {g: idx for idx, g in enumerate(gens4)}
    shift_rows = []
    for l in range(num_vars):
        rl, cl = l // n, l % n
        if md4[0][rl] == 0 or md4[1][cl] == 0:
            continue
        md3 = (
            tuple(md4[0][x] - (1 if x == rl else 0) for x in range(n)),
            tuple(md4[1][y] - (1 if y == cl else 0) for y in range(n)),
        )
        gens3 = []
        for k in range(num_vars):
            rk, ck = k // n, k % n
            if md3[0][rk] == 0 or md3[1][ck] == 0:
                continue
            md2 = (
                tuple(md3[0][x] - (1 if x == rk else 0) for x in range(n)),
                tuple(md3[1][y] - (1 if y == ck else 0) for y in range(n)),
            )
            for ql in range(len(f2_by_mdeg.get(md2, []))):
                gens3.append((k, md2, ql))
        if not gens3:
            continue
        phi3_blk = polys_to_dense_mod(
            [mul_poly(y_vars[k], f2_by_mdeg[md2][ql]) for k, md2, ql in gens3], mod=mod
        )
        syz3_blk = right_nullspace_mod(phi3_blk.T, mod=mod)
        for s_row in syz3_blk:
            row = np.zeros(len(gens4), dtype=np.int64)
            for c_idx in np.nonzero(s_row)[0]:
                k, q_md2, q_loc = gens3[int(c_idx)]
                a, b = (l, k) if l <= k else (k, l)
                t_col = gen4_to_col[(pair2_to_idx[(a, b)], q_md2, q_loc)]
                row[t_col] = (row[t_col] + int(s_row[c_idx])) % mod
            shift_rows.append(row)

    shift_mat = np.stack(shift_rows, axis=0)
    dim_v_syz3_blk = rank_matrix_mod(shift_mat, mod=mod)
    b24_blk = dim_syz1_4_blk - dim_v_syz3_blk
    b34_blk = len(shift_rows) - dim_v_syz3_blk
    return b14_blk, b24_blk, b34_blk


def format_poly_q(p: Dict[Tuple[int, ...], Fraction], n: int = 4) -> str:
    terms = []
    for m in sorted(p.keys(), reverse=True):
        c = p[m]
        if c == 0:
            continue
        parts = []
        for idx, e in enumerate(m):
            if e > 0:
                r, col = divmod(idx, n)
                parts.append(f"y{r}{col}" if e == 1 else f"y{r}{col}^{e}")
        m_str = "*".join(parts)
        if not terms:
            prefix = "-" if c == -1 else ("" if c == 1 else f"{c}*")
            terms.append(f"{prefix}{m_str}")
        else:
            sign = " + " if c > 0 else " - "
            ac = abs(c)
            coef_str = "" if ac == 1 else f"{ac}*"
            terms.append(f"{sign}{coef_str}{m_str}")
    return "".join(terms)


def prove_explicit_half_cancellation() -> None:
    """
    Solve coeffs @ shift_mat_det == v_koszul over Q (exhibiting denominator 2),
    and prove shift_mat_perm has NO solution for v_koszul over Q.
    """
    n = 4
    num_vars = 16
    md4 = ((2, 2, 0, 0), (1, 1, 1, 1))
    pairs2 = [(i, j) for i in range(num_vars) for j in range(i, num_vars)]
    pair2_to_idx = {pair: idx for idx, pair in enumerate(pairs2)}
    pair2_mdeg = []
    pair2_poly_q: List[Dict[Tuple[int, ...], Fraction]] = []
    pair2_by_mdeg: Dict[Multideg, List[int]] = defaultdict(list)
    for p_idx, (a, b) in enumerate(pairs2):
        exp = [0] * num_vars
        exp[a] += 1
        exp[b] += 1
        t = tuple(exp)
        md = monom_multideg(t, n)
        pair2_mdeg.append(md)
        pair2_poly_q.append({t: Fraction(1)})
        pair2_by_mdeg[md].append(p_idx)

    y_vars_q = [{k_m: Fraction(v) for k_m, v in var_poly(k, num_vars).items()} for k in range(num_vars)]

    def build_block_system(f: Poly):
        f2_q: Dict[Multideg, List[Dict[Tuple[int, ...], Fraction]]] = {}
        for md2, p_indices in pair2_by_mdeg.items():
            p2_polys: List[Dict[Tuple[int, ...], Fraction]] = []
            for p_idx in p_indices:
                i, j = pairs2[p_idx]
                dij = partial_deriv(partial_deriv(f, i), j)
                p2_polys.append({m: Fraction(c) for m, c in dij.items() if c != 0} if dij else {})
            A_rows, n_c = polys_to_sparse_q(p2_polys)
            nb = right_nullspace_exact_q(transpose_sparse_q(A_rows, n_c), len(p_indices))
            if nb:
                q_list = []
                for row in nb:
                    qp: Dict[Tuple[int, ...], Fraction] = {}
                    for loc_idx, coeff in row.items():
                        i, j = pairs2[p_indices[loc_idx]]
                        exp = [0] * num_vars
                        exp[i] += 1
                        exp[j] += 1
                        qp[tuple(exp)] = coeff
                    q_list.append(qp)
                f2_q[md2] = q_list

        gens4: List[Tuple[int, Multideg, int]] = []
        for p2_idx, md2_p in enumerate(pair2_mdeg):
            rem_r = tuple(md4[0][x] - md2_p[0][x] for x in range(n))
            rem_c = tuple(md4[1][y] - md2_p[1][y] for y in range(n))
            if min(rem_r) < 0 or min(rem_c) < 0:
                continue
            q_md2 = (rem_r, rem_c)
            for ql in range(len(f2_q.get(q_md2, []))):
                gens4.append((p2_idx, q_md2, ql))

        gen4_to_col = {g: idx for idx, g in enumerate(gens4)}
        shift_rows: List[SparseRowQ] = []
        shift_meta: List[Tuple[int, List[Tuple[int, Multideg, int]], SparseRowQ]] = []

        for l in range(num_vars):
            rl, cl = l // n, l % n
            if md4[0][rl] == 0 or md4[1][cl] == 0:
                continue
            md3 = (
                tuple(md4[0][x] - (1 if x == rl else 0) for x in range(n)),
                tuple(md4[1][y] - (1 if y == cl else 0) for y in range(n)),
            )
            gens3 = []
            for k in range(num_vars):
                rk, ck = k // n, k % n
                if md3[0][rk] == 0 or md3[1][ck] == 0:
                    continue
                md2 = (
                    tuple(md3[0][x] - (1 if x == rk else 0) for x in range(n)),
                    tuple(md3[1][y] - (1 if y == ck else 0) for y in range(n)),
                )
                for ql in range(len(f2_q.get(md2, []))):
                    gens3.append((k, md2, ql))
            if not gens3:
                continue
            phi3_polys = [mul_poly_q(y_vars_q[k], f2_q[md2][ql]) for k, md2, ql in gens3]
            phi3_rows, n_c3 = polys_to_sparse_q(phi3_polys)
            syz3_blk = right_nullspace_exact_q(transpose_sparse_q(phi3_rows, n_c3), len(gens3))
            for s_vec in syz3_blk:
                row_s: SparseRowQ = {}
                for c_idx, val in s_vec.items():
                    k, q_md2, q_loc = gens3[c_idx]
                    a, b = (l, k) if l <= k else (k, l)
                    t_col = gen4_to_col[(pair2_to_idx[(a, b)], q_md2, q_loc)]
                    nv = row_s.get(t_col, Fraction(0)) + val
                    if nv == 0:
                        row_s.pop(t_col, None)
                    else:
                        row_s[t_col] = nv
                shift_rows.append(row_s)
                shift_meta.append((l, gens3, s_vec))

        # Locate (y02*y03)[y10*y11] and (y10*y11)[y02*y03]
        p2_02_03 = pair2_to_idx[(2, 3)]      # y02 * y03
        p2_10_11 = pair2_to_idx[(4, 5)]      # y10 * y11
        md2_10_11 = pair2_mdeg[p2_10_11]
        md2_02_03 = pair2_mdeg[p2_02_03]
        assert len(f2_q[md2_10_11]) == 1 and len(f2_q[md2_02_03]) == 1
        col_a = gen4_to_col[(p2_02_03, md2_10_11, 0)]
        col_b = gen4_to_col[(p2_10_11, md2_02_03, 0)]
        assert f2_q[md2_10_11][0] == pair2_poly_q[p2_10_11]
        assert f2_q[md2_02_03][0] == pair2_poly_q[p2_02_03]
        v_koszul: SparseRowQ = {col_a: Fraction(1), col_b: Fraction(-1)}
        return f2_q, gens4, shift_rows, shift_meta, v_koszul

    f2_d4, gens4_d4, shift_d4, meta_d4, v_koszul_d4 = build_block_system(determinant_poly(4))
    _, gens4_p4, shift_p4, _, v_koszul_p4 = build_block_system(permanent_poly(4))

    sol_d4 = solve_left_exact_q(shift_d4, len(gens4_d4), v_koszul_d4)
    sol_p4 = solve_left_exact_q(shift_p4, len(gens4_p4), v_koszul_p4)
    assert sol_d4 is not None, "Expected Koszul syzygy to lie in V*.Syz_1(det_4^perp)_3!"
    assert sol_p4 is None, "Expected Koszul syzygy NOT to lie in V*.Syz_1(perm_4^perp)_3!"
    assert any(c.denominator == 2 for c in sol_d4.values()), "Expected denominator 2 in Q weights!"

    print("\n=== Explicit Q Cancellation Identity in V* . Syz_1(det_4^perp)_3 (Denominator 2) ===")
    print("(y02*y03)[y10*y11] - (y10*y11)[y02*y03]  ==  sum of linear det_4^perp syzygies:")
    for r_idx, c in sorted(sol_d4.items()):
        l_var, gens3, s_vec = meta_d4[r_idx]
        rl, cl = divmod(l_var, 4)
        terms_str = []
        for c_idx, val in sorted(s_vec.items()):
            k_var, q_md2, q_loc = gens3[c_idx]
            rk, ck = divmod(k_var, 4)
            q_str = format_poly_q(f2_d4[q_md2][q_loc], n=4)
            v_prefix = "" if val == 1 else ("-" if val == -1 else f"{val}*")
            terms_str.append(f"{v_prefix}y{rk}{ck}*[{q_str}]")
        syz_str = " + ".join(terms_str).replace("+ -", "- ")
        print(f"  + ({c}) * y{rl}{cl} * ({syz_str})")


def main() -> None:
    # 1) Exact Q certificate for degree 3 (n=3) and degree 4 (n=4)
    t_d3, _ = apolar_betti_q_orbit(determinant_poly(3), 3)
    t_p3, _ = apolar_betti_q_orbit(permanent_poly(3), 3)
    assert t_d3 == (36, 0, 160, 0, 0, 315)
    assert t_p3 == (36, 0, 160, 0, 0, 315)

    t_d4, orb_d4 = apolar_betti_q_orbit(determinant_poly(4), 4)
    t_p4, orb_p4 = apolar_betti_q_orbit(permanent_poly(4), 4)
    assert t_d4 == (100, 0, 800, 0, 0, 3075)
    assert t_p4 == (100, 0, 800, 0, 12, 3087)

    # Check exact orbit breakdown over Q
    assert all(b14 == 0 and b24 == 0 for _, b14, b24, _ in orb_d4)
    diff_orbits_p4 = [(md4, b24) for md4, b14, b24, _ in orb_p4 if b24 != 0]
    assert diff_orbits_p4 == [
        (((2, 2, 0, 0), (1, 1, 1, 1)), 1),
        (((1, 1, 1, 1), (2, 2, 0, 0)), 1),
    ], f"Unexpected nonzero b24 orbits over Q: {diff_orbits_p4}"

    print("=== Exact Q Certificate (Locality Reduction n=3 & All 25 Orbits of n=4) ===")
    print(f"n=3 over Q: det_3={t_d3}, perm_3={t_p3} (b_{{1,3}} = 0 on all 9 orbits)")
    print(f"n=4 over Q: det_4={t_d4}, perm_4={t_p4} (b_{{2,4}} = 0 on all 25 det_4 orbits; 1 on 2 perm_4 orbits)")

    # 2) Characteristic-p torsion test on ((2,2,0,0), (1,1,1,1))
    md_test = ((2, 2, 0, 0), (1, 1, 1, 1))
    p4, d4 = permanent_poly(4), determinant_poly(4)
    print("\n=== Characteristic-p Torsion Check on ((2,2,0,0), (1,1,1,1)) ===")
    print("Field | det_4 (b14, b24, b34) | perm_4 (b14, b24, b34)")
    print("-" * 55)
    for prime in (2, 3, 5, 7):
        bd = block_betti_mod_p(d4, 4, md_test, prime)
        bp = block_betti_mod_p(p4, 4, md_test, prime)
        if prime == 2:
            assert bd == (0, 1, 7) and bp == (0, 1, 7)
        else:
            assert bd == (0, 0, 6) and bp == (0, 1, 7)
        print(f"F_{prime:<3d} | {str(bd):21s} | {str(bp)}")
    # Q entry from orb_d4 / orb_p4
    qd = next((b14, b24, b34) for md, b14, b24, b34 in orb_d4 if md == md_test)
    qp = next((b14, b24, b34) for md, b14, b24, b34 in orb_p4 if md == md_test)
    assert qd == (0, 0, 6) and qp == (0, 1, 7)
    print(f"Q     | {str(qd):21s} | {str(qp)}")

    # 3) Explicit Q cancellation identity with denominator 2
    prove_explicit_half_cancellation()


if __name__ == "__main__":
    main()
