"""Multilinear, rook-placement (torus), and set-multilinear ABP projections for n=4."""
from __future__ import annotations

import random
from typing import List

from perm4_abp_frontier import (
    MOD,
    random_abp4_det,
    rank_mod_numpy,
)
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


def project_multilinear(p: Poly) -> Poly:
    """Keep only square-free (multilinear) monomials (all exponents <= 1)."""
    return {m: c for m, c in p.items() if all(e <= 1 for e in m)}


def project_rook(p: Poly, n: int = 4) -> Poly:
    """Keep only monomials with at most 1 variable per row and per column (torus rook weight)."""
    res: Poly = {}
    for m, c in p.items():
        if any(e > 1 for e in m):
            continue
        ok = True
        row_cnt = [0] * n
        col_cnt = [0] * n
        for idx, e in enumerate(m):
            if e == 1:
                r, col = divmod(idx, n)
                row_cnt[r] += 1
                col_cnt[col] += 1
                if row_cnt[r] > 1 or col_cnt[col] > 1:
                    ok = False
                    break
        if ok:
            res[m] = c
    return res


def rand_row_lin(row: int, n: int, rng: random.Random) -> Poly:
    """Random linear form restricted to variables in row `row` (set-multilinear layer)."""
    num_vars = n * n
    p: Poly = {}
    for col in range(n):
        c = rng.randint(-5, 5)
        if c != 0:
            p = add_poly(p, var_poly(row * n + col, num_vars, c))
    return p


def random_set_multilinear_abp4(w1: int, w2: int, w3: int, rng: random.Random) -> Poly:
    """Set-multilinear degree-4 ABP where layer r uses only row r variables."""
    v1 = [rand_row_lin(0, 4, rng) for _ in range(w1)]
    v2 = []
    for _ in range(w2):
        acc = zero_poly()
        for i in range(w1):
            acc = add_poly(acc, mul_poly(v1[i], rand_row_lin(1, 4, rng)))
        v2.append({k: v % MOD for k, v in acc.items() if v % MOD != 0})
    v3 = []
    for _ in range(w3):
        acc = zero_poly()
        for i in range(w2):
            acc = add_poly(acc, mul_poly(v2[i], rand_row_lin(2, 4, rng)))
        v3.append({k: v % MOD for k, v in acc.items() if v % MOD != 0})
    total = zero_poly()
    for i in range(w3):
        total = add_poly(total, mul_poly(v3[i], rand_row_lin(3, 4, rng)))
    return {k: v % MOD for k, v in total.items() if v % MOD != 0}


def eval_projections(p: Poly, num_vars: int = 16, k: int = 2, shift_deg: int = 1) -> tuple[int, int, int]:
    """Return (full_dim, multilinear_dim, rook_dim) for x^{<=shift} d^{=k} p."""
    partials = kth_partial_space(p, num_vars, k)
    shifts = monomials_of_degree_le(num_vars, shift_deg)
    gens = [mul_poly(s, d) for s in shifts for d in partials]
    d_full = rank_mod_numpy(gens)
    d_ml = rank_mod_numpy([project_multilinear(g) for g in gens])
    d_rook = rank_mod_numpy([project_rook(g, 4) for g in gens])
    return d_full, d_ml, d_rook


def main() -> None:
    p4 = permanent_poly(4)
    d4 = determinant_poly(4)
    rng = random.Random(2026)

    print("Model                         | full | multilinear | rook (torus)")
    print("-" * 68)
    for name, poly in [("perm_4", p4), ("det_4", d4)]:
        df, dm, dr = eval_projections(poly)
        print(f"{name:29s} | {df:4d} | {dm:11d} | {dr:12d}")

    print("\n--- General random ABP det_m projected to multilinear / rook ---")
    for w1, w2, w3 in [(2, 4, 2), (3, 3, 3), (3, 4, 3), (4, 4, 4)]:
        m = 1 + w1 + w2 + w3
        poly = random_abp4_det(w1, w2, w3, 16, rng)
        df, dm, dr = eval_projections(poly)
        print(f"Gen ABP m={m:2d} ({w1},{w2},{w3})        | {df:4d} | {dm:11d} | {dr:12d}")

    print("\n--- Set-multilinear ABP det_m (row-layered, Nisan model) ---")
    for w1, w2, w3 in [(2, 3, 2), (3, 3, 3), (3, 5, 3), (4, 5, 4), (4, 6, 4)]:
        m = 1 + w1 + w2 + w3
        poly = random_set_multilinear_abp4(w1, w2, w3, rng)
        df, dm, dr = eval_projections(poly)
        print(f"Set-ML ABP m={m:2d} ({w1},{w2},{w3})     | {df:4d} | {dm:11d} | {dr:12d}")


if __name__ == "__main__":
    main()
