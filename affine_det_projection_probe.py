"""Probe affine projections and degree-3 ABP/determinant realizations of det_m for m=3..7."""
from __future__ import annotations

import random
from typing import Dict, List

from grenet_verify import grenet_matrix_perm3
from poly_exact import (
    Poly,
    add_poly,
    const_poly,
    determinant_poly,
    kth_partial_space,
    mul_poly,
    permanent_poly,
    rank_mod_p,
    var_poly,
    zero_poly,
)
from shifted_pd_probe import monomials_of_degree_le

MOD = 1_000_000_007


def poly_det_mod(mat: List[List[Poly]], mod: int = MOD) -> Poly:
    """Exact determinant of a matrix of sparse polynomials over F_mod."""
    m = len(mat)
    if m == 1:
        return {k: v % mod for k, v in mat[0][0].items() if v % mod != 0}
    if m == 2:
        p1 = mul_poly(mat[0][0], mat[1][1])
        p2 = mul_poly(mat[0][1], mat[1][0])
        res = add_poly(p1, p2, sign=-1)
        return {k: v % mod for k, v in res.items() if v % mod != 0}

    total: Poly = {}
    for col in range(m):
        entry = mat[0][col]
        if not entry:
            continue
        sub = [row[:col] + row[col + 1 :] for row in mat[1:]]
        cofactor = poly_det_mod(sub, mod)
        term = mul_poly(entry, cofactor)
        total = add_poly(total, term, sign=1 if col % 2 == 0 else -1)
    return {k: v % mod for k, v in total.items() if v % mod != 0}


def random_abp_det(m: int, num_vars: int, rng: random.Random) -> Poly:
    """
    Construct an m x m cycle-cover determinant matrix for a layered DAG of length 3
    (root 0, layer1, layer2 -> back to 0) with random linear forms on edges,
    guaranteeing det(M(X)) is homogeneous of degree 3 (or <= 3).
    """
    # Partition 1..m-1 into layer1 and layer2
    l1_size = max(1, (m - 1) // 2)
    l1 = list(range(1, 1 + l1_size))
    l2 = list(range(1 + l1_size, m))
    if not l2:
        l2 = l1

    mat: List[List[Poly]] = [[zero_poly() for _ in range(m)] for _ in range(m)]
    for i in range(1, m):
        mat[i][i] = const_poly(1, num_vars)

    def rand_lin() -> Poly:
        p: Poly = {}
        for v in range(num_vars):
            c = rng.randint(-3, 3)
            if c != 0:
                p = add_poly(p, var_poly(v, num_vars, c))
        return p

    for u in l1:
        mat[0][u] = rand_lin()
    for u in l1:
        for v in l2:
            if u != v:
                mat[u][v] = rand_lin()
    for v in l2:
        mat[v][0] = rand_lin()

    return poly_det_mod(mat)


def syzygy_span(p: Poly, num_vars: int, k: int = 1, shift_deg: int = 1) -> tuple[int, int]:
    partials = kth_partial_space(p, num_vars, k)
    shifts = monomials_of_degree_le(num_vars, shift_deg)
    gens = [mul_poly(s, d) for s in shifts for d in partials]
    return rank_mod_p(gens), len(gens)


def main() -> None:
    rng = random.Random(42)
    p3 = permanent_poly(3)
    d3 = determinant_poly(3)
    g3 = poly_det_mod(grenet_matrix_perm3())

    print("Target / Model              | span(x<=1 d=1) | generators | syzygies")
    print("-" * 74)
    for name, poly in [("det_3", d3), ("perm_3", p3), ("Grenet_7x7 (==perm_3)", g3)]:
        span, gens = syzygy_span(poly, 9)
        print(f"{name:27s} | {span:14d} | {gens:10d} | {gens - span:8d}")

    print("\nRandom degree-3 ABP/det_m projections (best of 5 trials per m):")
    for m in (4, 5, 6, 7):
        best_span_1 = -1
        best_span_2 = -1
        for _ in range(5):
            poly = random_abp_det(m, 9, rng)
            s1, _ = syzygy_span(poly, 9, k=1, shift_deg=1)
            s2, _ = syzygy_span(poly, 9, k=1, shift_deg=2)
            best_span_1 = max(best_span_1, s1)
            best_span_2 = max(best_span_2, s2)
        print(
            f"m={m} (ABP det_{m})            | s1={best_span_1:2d}/90 | s2={best_span_2:3d}/495"
        )

    p3_s2, _ = syzygy_span(p3, 9, k=1, shift_deg=2)
    d3_s2, _ = syzygy_span(d3, 9, k=1, shift_deg=2)
    print(f"\nReference (k=1, shift=2): perm_3={p3_s2}/495 | det_3={d3_s2}/495")


if __name__ == "__main__":
    main()
