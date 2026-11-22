"""Wall 1 probe: test middle 4x4 quadratic factorization P_perm(Y) vs P_det(Y) for m=13 (4,4,4)."""
from __future__ import annotations

import random
from collections import Counter
from typing import Dict, List, Tuple

import numpy as np

from apolar_higher_betti_probe import rank_matrix_mod
from corank_obstruction_proof import eval_poly_mod, hessian_nullity_at
from perm4_abp_frontier import MOD, rank_mod_numpy
from poly_exact import (
    Poly,
    determinant_poly,
    partial_deriv,
    permanent_poly,
    poly_det,
)


def extract_middle_4x4(f: Poly) -> List[List[Poly]]:
    """
    Extract the 4x4 matrix P(Y) of degree-2 polynomials in Y = X_{{1,2}} (8 vars)
    defined by f(X) = sum_{j0, j3} x_{0, j0} * P(Y)_{j0, j3} * x_{3, j3} + ...
    """
    mat: List[List[Poly]] = [[{} for _ in range(4)] for _ in range(4)]
    for j0 in range(4):
        d0 = partial_deriv(f, j0)
        for j3 in range(4):
            d03 = partial_deriv(d0, 12 + j3)
            comp: Poly = {}
            for m, c in d03.items():
                assert all(m[k] == 0 for k in (0, 1, 2, 3, 12, 13, 14, 15)), (
                    f"Unexpected outer variable in P({j0},{j3}): {m}"
                )
                comp[m[4:12]] = c
            mat[j0][j3] = comp
    return mat


def eval_mat_mod(mat: List[List[Poly]], pt: List[int], mod: int = MOD) -> np.ndarray:
    out = np.zeros((len(mat), len(mat[0])), dtype=np.int64)
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            out[i, j] = eval_poly_mod(mat[i][j], pt, mod=mod)
    return out


# ---- Univariate polynomial arithmetic over F_p (coeffs [c0, c1, ..., cd]) ----

def strip_p(a: List[int], p: int) -> List[int]:
    out = [c % p for c in a]
    while out and out[-1] == 0:
        out.pop()
    return out


def poly_add_p(a: List[int], b: List[int], p: int, sign: int = 1) -> List[int]:
    n = max(len(a), len(b))
    res = [0] * n
    for i in range(len(a)):
        res[i] = (res[i] + a[i]) % p
    for i in range(len(b)):
        res[i] = (res[i] + sign * b[i]) % p
    return strip_p(res, p)


def poly_mul_p(a: List[int], b: List[int], p: int) -> List[int]:
    if not a or not b:
        return []
    res = [0] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        if ca == 0:
            continue
        for j, cb in enumerate(b):
            res[i + j] = (res[i + j] + ca * cb) % p
    return strip_p(res, p)


def poly_divmod_p(a: List[int], b: List[int], p: int) -> Tuple[List[int], List[int]]:
    a = strip_p(a, p)
    b = strip_p(b, p)
    assert b, "Division by zero polynomial"
    db = len(b) - 1
    inv_lead = pow(b[-1], p - 2, p)
    rem = list(a)
    if len(rem) - 1 < db:
        return [], rem
    q = [0] * (len(rem) - db)
    while len(rem) - 1 >= db and rem:
        shift = (len(rem) - 1) - db
        coeff = (rem[-1] * inv_lead) % p
        q[shift] = coeff
        for i in range(db + 1):
            rem[shift + i] = (rem[shift + i] - coeff * b[i]) % p
        rem = strip_p(rem, p)
    return strip_p(q, p), rem


def poly_mod_p(a: List[int], m: List[int], p: int) -> List[int]:
    return poly_divmod_p(a, m, p)[1]


def poly_gcd_p(a: List[int], b: List[int], p: int) -> List[int]:
    a = strip_p(a, p)
    b = strip_p(b, p)
    while b:
        a, b = b, poly_mod_p(a, b, p)
    if not a:
        return []
    inv = pow(a[-1], p - 2, p)
    return [(c * inv) % p for c in a]


def poly_powmod_p(base: List[int], exp: int, mod_poly: List[int], p: int) -> List[int]:
    res = [1]
    cur = poly_mod_p(base, mod_poly, p)
    e = exp
    while e > 0:
        if e & 1:
            res = poly_mod_p(poly_mul_p(res, cur, p), mod_poly, p)
        e >>= 1
        if e > 0:
            cur = poly_mod_p(poly_mul_p(cur, cur, p), mod_poly, p)
    return res


def poly_deriv_p(a: List[int], p: int) -> List[int]:
    if len(a) <= 1:
        return []
    return strip_p([(i * a[i]) % p for i in range(1, len(a))], p)


def factor_degree_multiset_p(f: List[int], p: int) -> List[int]:
    """Exact sorted multiset of irreducible factor degrees of univariate f over F_p."""
    f = strip_p(f, p)
    if len(f) <= 1:
        return []
    inv = pow(f[-1], p - 2, p)
    f = [(c * inv) % p for c in f]
    df = poly_deriv_p(f, p)
    if not df:
        raise ValueError("p divides all exponents")
    g = poly_gcd_p(f, df, p)
    if len(g) - 1 > 0:
        q, r = poly_divmod_p(f, g, p)
        assert not r
        return sorted(factor_degree_multiset_p(q, p) + factor_degree_multiset_p(g, p))

    # Square-free Distinct-Degree Factorization (DDF)
    degs: List[int] = []
    cur = f
    x_pow = [0, 1]
    d = 1
    while len(cur) - 1 >= 2 * d:
        x_pow = poly_powmod_p(x_pow, p, cur, p)
        diff = poly_add_p(x_pow, [0, 1], p, sign=-1)
        gd = poly_gcd_p(cur, diff, p)
        dg = len(gd) - 1
        if dg > 0:
            assert dg % d == 0
            degs.extend([d] * (dg // d))
            cur, r = poly_divmod_p(cur, gd, p)
            assert not r
            x_pow = poly_mod_p(x_pow, cur, p)
        d += 1
    if len(cur) - 1 > 0:
        degs.append(len(cur) - 1)
    assert sum(degs) == len(f) - 1
    return sorted(degs)


def eval_line_slice(poly_8: Poly, y0: List[int], y1: List[int], p: int) -> List[int]:
    """Evaluate homogeneous degree-8 polynomial F(y0 + t * y1) as univariate polynomial in t mod p."""
    res = [0] * 9
    for m, coeff in poly_8.items():
        c = coeff % p
        if c == 0:
            continue
        cur = [c]
        for idx, exp in enumerate(m):
            if exp == 0:
                continue
            lin = [y0[idx] % p, y1[idx] % p]
            for _ in range(exp):
                cur = poly_mul_p(cur, lin, p)
        for k, ck in enumerate(cur):
            res[k] = (res[k] + ck) % p
    return strip_p(res, p)


def main() -> None:
    p4 = permanent_poly(4)
    d4 = determinant_poly(4)

    P_det = extract_middle_4x4(d4)
    P_perm = extract_middle_4x4(p4)

    det_P_det = poly_det(P_det, 8)
    det_P_perm = poly_det(P_perm, 8)
    assert det_P_det == {}, f"Expected det(P_det) == 0 identically, got {len(det_P_det)} terms"
    assert len(det_P_perm) > 0

    pt_test = [1, 1, 1, 1, 1, 2, 3, 4]
    rk_det = rank_matrix_mod(eval_mat_mod(P_det, pt_test), mod=MOD)
    rk_perm = rank_matrix_mod(eval_mat_mod(P_perm, pt_test), mod=MOD)
    val_test = eval_poly_mod(det_P_perm, pt_test, mod=MOD)
    # Also compute exact Z evaluation at pt_test
    val_z = 0
    for m, c in det_P_perm.items():
        term = c
        for idx, e in enumerate(m):
            if e:
                term *= pt_test[idx] ** e
        val_z += term
    assert rk_det == 2 and rk_perm == 4 and val_z != 0

    print("=== Middle 4x4 Quadratic Matrix P(Y) Summary ===")
    print(f"det(P_det(Y))  == 0 identically: True | rank at test pt = {rk_det}")
    print(
        f"det(P_perm(Y)) terms={len(det_P_perm)}, deg={max(sum(m) for m in det_P_perm)}, "
        f"rank at test pt = {rk_perm}, eval(1..1,1..4) = {val_z}"
    )

    # Self-checks on factor_degree_multiset_p
    # (t^2 + 1)(t - 2) mod 101: t^2 + 1 has 1^2 = -1 mod 101 -> (t-10)(t+10)! Use p=103 where -1 is non-square!
    # Check (t^2 + 1)(t - 2) = t^3 - 2t^2 + t - 2 mod 103
    assert factor_degree_multiset_p([(-2) % 103, 1, (-2) % 103, 1], 103) == [1, 2]
    assert factor_degree_multiset_p([1, 0, 1], 101) == [1, 1]  # t^2 + 1 splits mod 101
    print("[Self-Check] Univariate F_p Distinct-Degree Factorization verified OK\n")

    print("=== Distinct-Degree Factorization of F(Y0 + t*Y1) = det(P_perm(Y0 + t*Y1)) ===")
    rng = random.Random(202644)
    all_patterns: Dict[Tuple[int, ...], int] = Counter()
    for p in (101, 103, 107, 109, 113, 127):
        pat_counts: Dict[Tuple[int, ...], int] = Counter()
        trials_deg8 = 0
        while trials_deg8 < 25:
            y0 = [rng.randrange(p) for _ in range(8)]
            y1 = [rng.randrange(p) for _ in range(8)]
            h = eval_line_slice(det_P_perm, y0, y1, p)
            if len(h) - 1 != 8:
                continue
            degs = tuple(factor_degree_multiset_p(h, p))
            pat_counts[degs] += 1
            all_patterns[degs] += 1
            trials_deg8 += 1
        top_str = ", ".join(f"{k}:{v}" for k, v in pat_counts.most_common(6))
        print(f"  p={p:3d} (25 lines): {top_str}")

    irred_count = all_patterns.get((8,), 0)
    print(f"\nTotal degree-8 irreducible slices across 6 primes (150 lines): {irred_count}/150")
    print(f"All observed factor degree patterns: {dict(all_patterns)}")

    # Entry span rank in S^2(C^8) and Sing(det(P_perm)) probe
    p_det_entries = [P_det[i][j] for i in range(4) for j in range(4) if P_det[i][j]]
    p_perm_entries = [P_perm[i][j] for i in range(4) for j in range(4) if P_perm[i][j]]
    rk_span_det = rank_mod_numpy(p_det_entries, mod=MOD)
    rk_span_perm = rank_mod_numpy(p_perm_entries, mod=MOD)
    print(f"\nQuadric entry span in S^2(C^8): P_det={rk_span_det}/16 | P_perm={rk_span_perm}/16")

    # Test a rank-2 point of P_perm: col 2 & 3 of Y are zero -> Y = [[1,2,0,0],[3,4,0,0]]
    # Check P_perm at Y=[[1,2,0,0],[3,4,0,0]]: nonzero only at (2,3) & (3,2) -> rank 2 -> det(P_perm) vanishes to order >= 2!
    y_rk2 = [1, 2, 0, 0, 3, 4, 0, 0]
    rk_p_at_y = rank_matrix_mod(eval_mat_mod(P_perm, y_rk2), mod=MOD)
    nul_sing = hessian_nullity_at(det_P_perm, 8, y_rk2, mod=MOD)
    print(f"Sing(det(P_perm)) at col2=col3=0 (rk(P_perm)={rk_p_at_y}): Hessian nullity = {nul_sing}/8")


if __name__ == "__main__":
    main()
