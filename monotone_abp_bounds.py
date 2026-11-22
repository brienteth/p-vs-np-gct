"""Degeneration-monotone singular-locus lower bounds for Corank s=1 layered ABPs (n=3, 4)."""
from __future__ import annotations

import random
from typing import List, Tuple

from corank_obstruction_proof import eval_poly_mod, hessian_nullity_at
from corank_schur_n3_probe import rand_lin_mod
from perm4_abp_frontier import MOD
from poly_exact import (
    Poly,
    add_poly,
    mul_poly,
    permanent_poly,
    zero_poly,
)


def set_x0_coeff(p: Poly, num_vars: int, val: int, mod: int = MOD) -> Poly:
    e0 = tuple(1 if i == 0 else 0 for i in range(num_vars))
    out = dict(p)
    v = val % mod
    if v == 0:
        out.pop(e0, None)
    else:
        out[e0] = v
    return out


def eval_vec_e0(vec: List[Poly], num_vars: int) -> List[int]:
    e0_pt = [1 if i == 0 else 0 for i in range(num_vars)]
    return [eval_poly_mod(p, e0_pt, mod=MOD) for p in vec]


def build_abp3_at_locus(
    w1: int, w2: int, locus: str, rng: random.Random, num_vars: int = 9
) -> Poly:
    """
    Construct generic degree-3 ABP f = v0^T M1 v2 engineered so e_0 lies smoothly on:
      - 'linear': {v0 = 0, v2 = 0} (codim <= w1 + w2)
      - 'cut1':   {v0 = 0, M1 v2 = 0} (codim <= 2 w1)
      - 'cut2':   {v0^T M1 = 0, v2 = 0} (codim <= 2 w2)
    """
    v0 = [rand_lin_mod(num_vars, rng) for _ in range(w1)]
    M1 = [[rand_lin_mod(num_vars, rng) for _ in range(w2)] for _ in range(w1)]
    v2 = [rand_lin_mod(num_vars, rng) for _ in range(w2)]

    if locus == "linear":
        v0 = [set_x0_coeff(p, num_vars, 0) for p in v0]
        v2 = [set_x0_coeff(p, num_vars, 0) for p in v2]
    elif locus == "cut1":
        v0 = [set_x0_coeff(p, num_vars, 0) for p in v0]
        v2[0] = set_x0_coeff(v2[0], num_vars, 1)
        v2_vals = eval_vec_e0(v2, num_vars)
        for a in range(w1):
            rest = sum(eval_poly_mod(M1[a][b], [1] + [0] * (num_vars - 1)) * v2_vals[b] for b in range(1, w2)) % MOD
            M1[a][0] = set_x0_coeff(M1[a][0], num_vars, -rest)
    elif locus == "cut2":
        v2 = [set_x0_coeff(p, num_vars, 0) for p in v2]
        v0[0] = set_x0_coeff(v0[0], num_vars, 1)
        v0_vals = eval_vec_e0(v0, num_vars)
        for b in range(w2):
            rest = sum(v0_vals[a] * eval_poly_mod(M1[a][b], [1] + [0] * (num_vars - 1)) for a in range(1, w1)) % MOD
            M1[0][b] = set_x0_coeff(M1[0][b], num_vars, -rest)
    else:
        raise ValueError(locus)

    # Evaluate f = sum_b (v0^T M1)_b * v2_b
    total = zero_poly()
    for b in range(w2):
        ql = zero_poly()
        for a in range(w1):
            ql = add_poly(ql, mul_poly(v0[a], M1[a][b]))
        total = add_poly(total, mul_poly(ql, v2[b]))
    return {m: c % MOD for m, c in total.items() if c % MOD != 0}


def build_abp4_at_locus(
    w1: int, w2: int, w3: int, locus: str, rng: random.Random, num_vars: int = 16
) -> Poly:
    """
    Construct generic degree-4 ABP f = v0^T M1 M2 v3 engineered so e_0 lies smoothly on:
      - 'linear': {v0 = 0, v3 = 0} (codim <= w1 + w3)
      - 'cut1':   {v0 = 0, M1 M2 v3 = 0} (codim <= 2 w1)
      - 'cut2':   {v0^T M1 = 0, M2 v3 = 0} (codim <= 2 w2)
      - 'cut3':   {v0^T M1 M2 = 0, v3 = 0} (codim <= 2 w3)
    """
    e0_pt = [1] + [0] * (num_vars - 1)
    v0 = [rand_lin_mod(num_vars, rng) for _ in range(w1)]
    M1 = [[rand_lin_mod(num_vars, rng) for _ in range(w2)] for _ in range(w1)]
    M2 = [[rand_lin_mod(num_vars, rng) for _ in range(w3)] for _ in range(w2)]
    v3 = [rand_lin_mod(num_vars, rng) for _ in range(w3)]

    if locus == "linear":
        v0 = [set_x0_coeff(p, num_vars, 0) for p in v0]
        v3 = [set_x0_coeff(p, num_vars, 0) for p in v3]
    elif locus == "cut2":
        v0[0] = set_x0_coeff(v0[0], num_vars, 1)
        v3[0] = set_x0_coeff(v3[0], num_vars, 1)
        v0_vals = eval_vec_e0(v0, num_vars)
        v3_vals = eval_vec_e0(v3, num_vars)
        for b in range(w2):
            s1 = sum(v0_vals[a] * eval_poly_mod(M1[a][b], e0_pt) for a in range(1, w1)) % MOD
            M1[0][b] = set_x0_coeff(M1[0][b], num_vars, -s1)
            s2 = sum(eval_poly_mod(M2[b][c], e0_pt) * v3_vals[c] for c in range(1, w3)) % MOD
            M2[b][0] = set_x0_coeff(M2[b][0], num_vars, -s2)
    elif locus == "cut1":
        v0 = [set_x0_coeff(p, num_vars, 0) for p in v0]
        v3[0] = set_x0_coeff(v3[0], num_vars, 1)
        v3_vals = eval_vec_e0(v3, num_vars)
        # Ensure (M2 v3)_0(e_0) = 1
        s_m2_0 = sum(eval_poly_mod(M2[0][c], e0_pt) * v3_vals[c] for c in range(1, w3)) % MOD
        M2[0][0] = set_x0_coeff(M2[0][0], num_vars, (1 - s_m2_0) % MOD)
        m2v3_vals = [
            sum(eval_poly_mod(M2[b][c], e0_pt) * v3_vals[c] for c in range(w3)) % MOD
            for b in range(w2)
        ]
        assert m2v3_vals[0] == 1
        for a in range(w1):
            rest = sum(eval_poly_mod(M1[a][b], e0_pt) * m2v3_vals[b] for b in range(1, w2)) % MOD
            M1[a][0] = set_x0_coeff(M1[a][0], num_vars, -rest)
    elif locus == "cut3":
        v3 = [set_x0_coeff(p, num_vars, 0) for p in v3]
        v0[0] = set_x0_coeff(v0[0], num_vars, 1)
        v0_vals = eval_vec_e0(v0, num_vars)
        # Ensure (v0^T M1)_0(e_0) = 1
        s_v0m1_0 = sum(v0_vals[a] * eval_poly_mod(M1[a][0], e0_pt) for a in range(1, w1)) % MOD
        M1[0][0] = set_x0_coeff(M1[0][0], num_vars, (1 - s_v0m1_0) % MOD)
        v0m1_vals = [
            sum(v0_vals[a] * eval_poly_mod(M1[a][b], e0_pt) for a in range(w1)) % MOD
            for b in range(w2)
        ]
        assert v0m1_vals[0] == 1
        for c in range(w3):
            rest = sum(v0m1_vals[b] * eval_poly_mod(M2[b][c], e0_pt) for b in range(1, w2)) % MOD
            M2[0][c] = set_x0_coeff(M2[0][c], num_vars, -rest)
    else:
        raise ValueError(locus)

    # Evaluate f = sum_b (v0^T M1)_b * (M2 v3)_b
    q_left: List[Poly] = []
    for b in range(w2):
        acc = zero_poly()
        for a in range(w1):
            acc = add_poly(acc, mul_poly(v0[a], M1[a][b]))
        q_left.append({m: c % MOD for m, c in acc.items() if c % MOD != 0})

    q_right: List[Poly] = []
    for b in range(w2):
        acc = zero_poly()
        for c in range(w3):
            acc = add_poly(acc, mul_poly(M2[b][c], v3[c]))
        q_right.append({m: c % MOD for m, c in acc.items() if c % MOD != 0})

    if locus == "cut2":
        assert all(eval_poly_mod(ql, e0_pt) == 0 for ql in q_left)
        assert all(eval_poly_mod(qr, e0_pt) == 0 for qr in q_right)

    total = zero_poly()
    for b in range(w2):
        total = add_poly(total, mul_poly(q_left[b], q_right[b]))
    return {m: c % MOD for m, c in total.items() if c % MOD != 0}


def main() -> None:
    rng = random.Random(202611)
    e0_9 = [1] + [0] * 8
    e0_16 = [1] + [0] * 15

    print("=== Part A (n=3): Border-Monotone Singular-Locus Bounds for All m <= 7 ABPs ===")
    print("m | (w1,w2) | linear | cut1 | cut2 | max_nullity | vs perm_3 (3)")
    print("-" * 66)
    for w1, w2 in [(1, 4), (2, 3), (3, 2), (4, 1), (3, 3)]:
        m = 1 + w1 + w2
        n_lin = hessian_nullity_at(build_abp3_at_locus(w1, w2, "linear", rng), 9, e0_9)
        n_c1 = hessian_nullity_at(build_abp3_at_locus(w1, w2, "cut1", rng), 9, e0_9)
        n_c2 = hessian_nullity_at(build_abp3_at_locus(w1, w2, "cut2", rng), 9, e0_9)
        mx = max(n_lin, n_c1, n_c2)
        if m <= 6:
            assert mx >= 5, f"Expected m={m} nullity >= 5, got {mx}"
        else:
            assert mx == 3, f"Expected m=7 (3,3) nullity == 3, got {mx}"
        status = "RULED OUT (>3)" if mx > 3 else "SURVIVES (==3)"
        print(f"{m:1d} | ({w1},{w2})   | {n_lin:6d} | {n_c1:4d} | {n_c2:4d} | {mx:11d} | {status}")

    print("\n=== Part B (n=4): Border-Monotone Singular-Locus Bounds for m=7..15 ABPs ===")
    print("m  | (w1,w2,w3) | linear | cut1 | cut2 | cut3 | max_nullity | vs perm_4 (8)")
    print("-" * 78)
    configs = [
        (2, 2, 2),
        (2, 4, 2),
        (3, 3, 3),
        (3, 4, 3),
        (3, 5, 3),
        (4, 3, 4),
        (4, 4, 4),
        (4, 5, 4),
        (4, 6, 4),
    ]
    for w1, w2, w3 in configs:
        m = 1 + w1 + w2 + w3
        n_lin = hessian_nullity_at(build_abp4_at_locus(w1, w2, w3, "linear", rng), 16, e0_16)
        n_c1 = hessian_nullity_at(build_abp4_at_locus(w1, w2, w3, "cut1", rng), 16, e0_16)
        n_c2 = hessian_nullity_at(build_abp4_at_locus(w1, w2, w3, "cut2", rng), 16, e0_16)
        n_c3 = hessian_nullity_at(build_abp4_at_locus(w1, w2, w3, "cut3", rng), 16, e0_16)
        mx = max(n_lin, n_c1, n_c2, n_c3)
        if m <= 12:
            assert mx >= 10, f"Expected m={m} ({w1},{w2},{w3}) nullity >= 10, got {mx}"
        else:
            assert mx <= 8, f"Expected m={m} ({w1},{w2},{w3}) nullity <= 8, got {mx}"
        if (w1, w2, w3) == (4, 3, 4):
            assert n_c2 >= 10, f"Expected cut2 nullity >= 10 for (4,3,4), got {n_c2}"
        status = "RULED OUT (>8)" if mx > 8 else "SURVIVES (<=8)"
        print(
            f"{m:2d} | ({w1},{w2},{w3})  | {n_lin:6d} | {n_c1:4d} | {n_c2:4d} | {n_c3:4d} | {mx:11d} | {status}"
        )


if __name__ == "__main__":
    main()
