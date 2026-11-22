"""Landsberg-Ottaviani GL_N-equivariant Koszul flattening rank probe for perm_n vs det_m/ABPs."""
from __future__ import annotations

import itertools
import math
import random
from typing import Dict, List, Tuple

import numpy as np

from general_det6_probe import layered_abp_det_split, sum_of_two_det3
from multilinear_torus_probe import random_set_multilinear_abp4
from perm4_abp_frontier import MOD, random_abp4_det
from poly_exact import (
    Poly,
    add_poly,
    determinant_poly,
    mul_poly,
    partial_deriv,
    permanent_poly,
    var_poly,
)

GEN_MOD = 1_000_000_007


def recenter_poly_from_mod(p: Poly, src_mod: int = GEN_MOD) -> Poly:
    """Recover small signed integer coefficients from mod src_mod before reducing mod MOD."""
    half = src_mod // 2
    return {m: (c - src_mod if c > half else c) for m, c in p.items() if c % src_mod != 0}


def substitute_shear_x0_plus_2x1(p: Poly, num_vars: int) -> Poly:
    """Apply invertible GL_N shear: x_0 -> x_0 + 2*x_1, leaving other variables fixed."""
    res: Poly = {}
    for m, coeff in p.items():
        e0 = m[0]
        if e0 == 0:
            res[m] = res.get(m, 0) + coeff
            continue
        base = list(m)
        base[0] = 0
        for j in range(e0 + 1):
            # comb(e0, j) * x_0^{e0 - j} * (2 * x_1)^j
            factor = math.comb(e0, j) * (2 ** j) * coeff
            nm = list(base)
            nm[0] += e0 - j
            nm[1] += j
            t = tuple(nm)
            val = res.get(t, 0) + factor
            if val == 0:
                res.pop(t, None)
            else:
                res[t] = val
    return res


def rank_sparse_rows_mod(rows: List[Dict[int, int]], n_cols: int, mod: int = MOD) -> int:
    """Exact rank of sparse integer matrix over F_mod using NumPy int64 Gaussian elimination."""
    non_empty = [r for r in rows if r]
    if not non_empty or n_cols == 0:
        return 0
    n_rows = len(non_empty)

    # Transpose if significantly more rows than columns so elimination loops over fewer pivots
    if n_rows > n_cols:
        mat = np.zeros((n_cols, n_rows), dtype=np.int64)
        for r_idx, r in enumerate(non_empty):
            for c_idx, v in r.items():
                mat[c_idx, r_idx] = v % mod
        m_r, m_c = n_cols, n_rows
    else:
        mat = np.zeros((n_rows, n_cols), dtype=np.int64)
        for r_idx, r in enumerate(non_empty):
            for c_idx, v in r.items():
                mat[r_idx, c_idx] = v % mod
        m_r, m_c = n_rows, n_cols

    rank = 0
    for col in range(m_c):
        if rank >= m_r:
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


def diff_operators_of_order(num_vars: int, k: int) -> List[Tuple[int, ...]]:
    """All k-tuples of variable indices (non-decreasing) representing d_{i_1}...d_{i_k}."""
    return list(itertools.combinations_with_replacement(range(num_vars), k))


def apply_diff_tuple(p: Poly, ops: Tuple[int, ...]) -> Poly:
    cur = p
    for v in ops:
        cur = partial_deriv(cur, v)
        if not cur:
            return {}
    return cur


def koszul_rank(f: Poly, num_vars: int, k: int, p: int, mod: int = MOD) -> int:
    """
    Compute exact rank of Koszul flattening:
      K_{f, k, p}: S^k V^* \otimes \bigwedge^p V -> S^{d-k-1} V \otimes \bigwedge^{p+1} V
      D \otimes e_I  |->  sum_{i=0}^{N-1} d_i(D f) \otimes (e_i ^ e_I).
    """
    d_ops = diff_operators_of_order(num_vars, k)
    ext_p = list(itertools.combinations(range(num_vars), p))

    # Precompute D(f) and all d_i(D(f)) once per D
    d_partials: List[List[Poly]] = []
    for dop in d_ops:
        df = apply_diff_tuple(f, dop)
        if not df:
            d_partials.append([{} for _ in range(num_vars)])
        else:
            row_p = []
            for i in range(num_vars):
                di = partial_deriv(df, i)
                if di:
                    di = {m: c % mod for m, c in di.items() if c % mod != 0}
                row_p.append(di)
            d_partials.append(row_p)

    # Precompute wedge product (i, I_tuple) -> (sign, J_tuple) for i not in I
    wedge_map: List[List[Tuple[int, Tuple[int, ...]]]] = []
    for I in ext_p:
        I_set = set(I)
        entries = []
        for i in range(num_vars):
            if i in I_set:
                continue
            pos = sum(1 for x in I if x < i)
            sign = 1 if (pos % 2 == 0) else -1
            J = tuple(sorted(I + (i,)))
            entries.append((i, sign, J))
        wedge_map.append(entries)

    col_to_idx: Dict[Tuple[Tuple[int, ...], Tuple[int, ...]], int] = {}
    rows: List[Dict[int, int]] = []

    for d_idx in range(len(d_ops)):
        partials_i = d_partials[d_idx]
        if not any(partials_i):
            continue
        for I_entries in wedge_map:
            row: Dict[int, int] = {}
            for i, sign, J in I_entries:
                poly_i = partials_i[i]
                if not poly_i:
                    continue
                for m, c in poly_i.items():
                    key = (m, J)
                    col = col_to_idx.get(key)
                    if col is None:
                        col = len(col_to_idx)
                        col_to_idx[key] = col
                    val = (row.get(col, 0) + sign * c) % mod
                    if val == 0:
                        row.pop(col, None)
                    else:
                        row[col] = val
            if row:
                rows.append(row)

    return rank_sparse_rows_mod(rows, len(col_to_idx), mod=mod)


def main() -> None:
    p3 = permanent_poly(3)
    d3 = determinant_poly(3)

    # Built-in GL_N invariance check on perm_3 under x_0 -> x_0 + 2*x_1
    p3_sheared = substitute_shear_x0_plus_2x1(p3, 9)
    r_orig = koszul_rank(p3, 9, k=1, p=1)
    r_shear = koszul_rank(p3_sheared, 9, k=1, p=1)
    assert r_orig == r_shear, f"GL_N invariance failed: {r_orig} != {r_shear}"
    print(f"[GL_N Invariance Check] koszul_rank(perm_3, k=1, p=1) = {r_orig} == sheared {r_shear} (OK)\n")

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

    print("=== n=3 (N=9, d=3) Koszul Flattening Ranks (k=1) ===")
    print("Model           | p=1 (<=81) | p=2 (<=324) | p=3 (<=756)")
    print("-" * 58)
    for name, poly in n3_models:
        r1 = koszul_rank(poly, 9, k=1, p=1)
        r2 = koszul_rank(poly, 9, k=1, p=2)
        r3 = koszul_rank(poly, 9, k=1, p=3)
        print(f"{name:15s} | {r1:9d} | {r2:11d} | {r3:11d}")

    p4 = permanent_poly(4)
    d4 = determinant_poly(4)
    rng4 = random.Random(2026)
    n4_models = [
        ("det_4", d4),
        ("Set-ML m=10 (3,3,3)", random_set_multilinear_abp4(3, 3, 3, rng4)),
        ("Set-ML m=12 (3,5,3)", random_set_multilinear_abp4(3, 5, 3, rng4)),
        ("Set-ML m=15 (4,6,4)", random_set_multilinear_abp4(4, 6, 4, rng4)),
        ("Gen ABP m=9 (2,4,2)", random_abp4_det(2, 4, 2, 16, rng4)),
        ("Gen ABP m=10 (3,3,3)", random_abp4_det(3, 3, 3, 16, rng4)),
        ("perm_4", p4),
    ]

    print("\n=== n=4 (N=16, d=4) Koszul Flattening Ranks ===")
    print("Model                 | k=1,p=1 (<=256) | k=2,p=1 (<=1920)")
    print("-" * 60)
    for name, poly in n4_models:
        r11 = koszul_rank(poly, 16, k=1, p=1)
        r21 = koszul_rank(poly, 16, k=2, p=1)
        print(f"{name:21s} | {r11:15d} | {r21:16d}")


if __name__ == "__main__":
    main()
