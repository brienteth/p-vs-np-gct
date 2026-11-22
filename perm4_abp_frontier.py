"""Scale to n=4: verify Grenet_15x15 for perm_4 and map (k=2, shift=1) frontier for m=7..15."""
from __future__ import annotations

import itertools
import random
from typing import Dict, List, Tuple

import numpy as np

from poly_exact import (
    Poly,
    add_poly,
    determinant_poly,
    kth_partial_space,
    mul_poly,
    permanent_poly,
    var_poly,
    zero_poly,
)
from shifted_pd_probe import monomials_of_degree_le

MOD = 1_000_003  # Prime < 2^20 so MOD*MOD < 2^40 fits safely in int64


def rank_mod_numpy(polys: List[Poly], mod: int = MOD) -> int:
    """Fast exact rank over F_mod using vectorized NumPy int64 Gaussian elimination."""
    monom_to_col: Dict[Tuple[int, ...], int] = {}
    rows_sparse: List[List[Tuple[int, int]]] = []
    for p in polys:
        if not p:
            continue
        r = []
        for m, c in p.items():
            v = c % mod
            if v:
                col = monom_to_col.get(m)
                if col is None:
                    col = len(monom_to_col)
                    monom_to_col[m] = col
                r.append((col, v))
        if r:
            rows_sparse.append(r)

    if not rows_sparse:
        return 0

    n_rows = len(rows_sparse)
    n_cols = len(monom_to_col)
    mat = np.zeros((n_rows, n_cols), dtype=np.int64)
    for i, r in enumerate(rows_sparse):
        for col, v in r:
            mat[i, col] = v

    rank = 0
    for col in range(n_cols):
        if rank >= n_rows:
            break
        # Find pivot in mat[rank:, col]
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


def grenet_perm4_via_abp() -> Poly:
    """Verify Grenet's 15-vertex (1 + 4 + 6 + 4) layered ABP computes perm_4 identically."""
    num_vars = 16
    s1 = [(j,) for j in range(4)]
    s2 = list(itertools.combinations(range(4), 2))
    s3 = list(itertools.combinations(range(4), 3))

    # Layer 0 -> 1: x_{0, j}
    v1 = [var_poly(0 * 4 + j, num_vars) for j in range(4)]

    # Layer 1 -> 2
    v2 = [zero_poly() for _ in range(len(s2))]
    for idx2, t2 in enumerate(s2):
        acc = zero_poly()
        for idx1, t1 in enumerate(s1):
            if t1[0] in t2:
                j = t2[1] if t2[0] == t1[0] else t2[0]
                acc = add_poly(acc, mul_poly(v1[idx1], var_poly(1 * 4 + j, num_vars)))
        v2[idx2] = acc

    # Layer 2 -> 3
    v3 = [zero_poly() for _ in range(len(s3))]
    for idx3, t3 in enumerate(s3):
        acc = zero_poly()
        for idx2, t2 in enumerate(s2):
            if set(t2).issubset(t3):
                j = (set(t3) - set(t2)).pop()
                acc = add_poly(acc, mul_poly(v2[idx2], var_poly(2 * 4 + j, num_vars)))
        v3[idx3] = acc

    # Layer 3 -> 0
    total = zero_poly()
    full = {0, 1, 2, 3}
    for idx3, t3 in enumerate(s3):
        j = (full - set(t3)).pop()
        total = add_poly(total, mul_poly(v3[idx3], var_poly(3 * 4 + j, num_vars)))
    return total


def rand_lin(num_vars: int, rng: random.Random) -> Poly:
    p: Poly = {}
    for v in range(num_vars):
        c = rng.randint(-3, 3)
        if c != 0:
            p = add_poly(p, var_poly(v, num_vars, c))
    return p


def random_abp4_det(w1: int, w2: int, w3: int, num_vars: int, rng: random.Random) -> Poly:
    """Homogeneous degree-4 ABP determinant with m = 1 + w1 + w2 + w3 vertices."""
    v1 = [rand_lin(num_vars, rng) for _ in range(w1)]
    v2 = []
    for _ in range(w2):
        acc = zero_poly()
        for i in range(w1):
            acc = add_poly(acc, mul_poly(v1[i], rand_lin(num_vars, rng)))
        v2.append({k: v % MOD for k, v in acc.items() if v % MOD != 0})
    v3 = []
    for _ in range(w3):
        acc = zero_poly()
        for i in range(w2):
            acc = add_poly(acc, mul_poly(v2[i], rand_lin(num_vars, rng)))
        v3.append({k: v % MOD for k, v in acc.items() if v % MOD != 0})
    total = zero_poly()
    for i in range(w3):
        total = add_poly(total, mul_poly(v3[i], rand_lin(num_vars, rng)))
    return {k: v % MOD for k, v in total.items() if v % MOD != 0}


def shifted_pd_dim_fast(p: Poly, num_vars: int, k: int, shift_deg: int) -> int:
    partials = kth_partial_space(p, num_vars, k)
    shifts = monomials_of_degree_le(num_vars, shift_deg)
    gens = [mul_poly(s, d) for s in shifts for d in partials]
    return rank_mod_numpy(gens)


def main() -> None:
    p4 = permanent_poly(4)
    d4 = determinant_poly(4)
    g4 = grenet_perm4_via_abp()
    print(f"perm_4 == Grenet_15x15: {g4 == p4} (terms={len(p4)})")

    ref_p4 = shifted_pd_dim_fast(p4, 16, k=2, shift_deg=1)
    ref_d4 = shifted_pd_dim_fast(d4, 16, k=2, shift_deg=1)
    print(f"Reference (k=2, shift=1): perm_4={ref_p4} | det_4={ref_d4} | gap={ref_p4 - ref_d4:+d}\n")

    rng = random.Random(77)
    configs = [
        (2, 2, 2),  # m = 7
        (2, 3, 2),  # m = 8
        (2, 4, 2),  # m = 9
        (3, 3, 3),  # m = 10
        (3, 4, 3),  # m = 11
        (3, 5, 3),  # m = 12
        (4, 4, 4),  # m = 13
        (4, 5, 4),  # m = 14
        (4, 6, 4),  # m = 15 (Grenet shape)
    ]
    print("m  | shape (w1,w2,w3) | dim(x<=1 d=2) | vs perm_4 (548)")
    print("-" * 58)
    for w1, w2, w3 in configs:
        m = 1 + w1 + w2 + w3
        poly = random_abp4_det(w1, w2, w3, 16, rng)
        dim = shifted_pd_dim_fast(poly, 16, k=2, shift_deg=1)
        print(f"{m:2d} | ({w1}, {w2}, {w3})        | {dim:13d} | {dim - ref_p4:+d}")


if __name__ == "__main__":
    main()
