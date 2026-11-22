"""Exact sparse multivariate polynomial arithmetic over Z and F_p."""
from __future__ import annotations

import itertools
from typing import Dict, Iterable, List, Tuple

Monomial = Tuple[int, ...]
Poly = Dict[Monomial, int]


def zero_poly() -> Poly:
    return {}


def const_poly(c: int, num_vars: int) -> Poly:
    if c == 0:
        return {}
    return {(0,) * num_vars: c}


def var_poly(idx: int, num_vars: int, coeff: int = 1) -> Poly:
    if coeff == 0:
        return {}
    exp = [0] * num_vars
    exp[idx] = 1
    return {tuple(exp): coeff}


def add_poly(a: Poly, b: Poly, sign: int = 1) -> Poly:
    res = dict(a)
    for m, c in b.items():
        val = res.get(m, 0) + sign * c
        if val == 0:
            res.pop(m, None)
        else:
            res[m] = val
    return res


def scale_poly(a: Poly, k: int) -> Poly:
    if k == 0:
        return {}
    return {m: c * k for m, c in a.items() if c * k != 0}


def mul_poly(a: Poly, b: Poly) -> Poly:
    if not a or not b:
        return {}
    res: Poly = {}
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            m = tuple(e1 + e2 for e1, e2 in zip(m1, m2))
            val = res.get(m, 0) + c1 * c2
            if val == 0:
                res.pop(m, None)
            else:
                res[m] = val
    return res


def poly_det(mat: List[List[Poly]], num_vars: int) -> Poly:
    """Exact determinant of a matrix of polynomials using Bareiss/Laplace expansion."""
    m = len(mat)
    if m == 1:
        return mat[0][0]
    if m == 2:
        return add_poly(mul_poly(mat[0][0], mat[1][1]), mul_poly(mat[0][1], mat[1][0]), sign=-1)

    # Laplace expansion along first row, skipping zero entries (fast for sparse matrices).
    total = zero_poly()
    for col in range(m):
        entry = mat[0][col]
        if not entry:
            continue
        sub = [row[:col] + row[col + 1 :] for row in mat[1:]]
        cofactor = poly_det(sub, num_vars)
        term = mul_poly(entry, cofactor)
        total = add_poly(total, term, sign=1 if col % 2 == 0 else -1)
    return total


def permanent_poly(n: int) -> Poly:
    """Exact permanent of an n x n symbolic matrix X_{i,j}."""
    num_vars = n * n
    total = zero_poly()
    for perm in itertools.permutations(range(n)):
        exp = [0] * num_vars
        for i, j in enumerate(perm):
            exp[i * n + j] = 1
        m = tuple(exp)
        total[m] = total.get(m, 0) + 1
    return total


def determinant_poly(n: int) -> Poly:
    """Exact determinant of an n x n symbolic matrix X_{i,j}."""
    num_vars = n * n
    mat = [[var_poly(i * n + j, num_vars) for j in range(n)] for i in range(n)]
    return poly_det(mat, num_vars)


def partial_deriv(p: Poly, var_idx: int) -> Poly:
    """Partial derivative of p with respect to x_{var_idx}."""
    res: Poly = {}
    for m, c in p.items():
        e = m[var_idx]
        if e > 0:
            new_m = list(m)
            new_m[var_idx] = e - 1
            t = tuple(new_m)
            val = res.get(t, 0) + c * e
            if val == 0:
                res.pop(t, None)
            else:
                res[t] = val
    return res


def kth_partial_space(p: Poly, num_vars: int, k: int) -> List[Poly]:
    """All distinct k-th order partial derivatives of p (up to non-zero)."""
    current: List[Poly] = [p]
    for _ in range(k):
        nxt: List[Poly] = []
        seen = set()
        for q in current:
            for v in range(num_vars):
                dq = partial_deriv(q, v)
                if dq:
                    key = tuple(sorted(dq.items()))
                    if key not in seen:
                        seen.add(key)
                        nxt.append(dq)
        current = nxt
    return current


def rank_mod_p(polys: Iterable[Poly], mod: int = 1_000_000_007) -> int:
    """Exact linear rank of a list of sparse polynomials over F_mod via Gaussian elimination."""
    pivots: Dict[int, Dict[int, int]] = {}
    monomial_to_col: Dict[Monomial, int] = {}

    for p in polys:
        if not p:
            continue
        row: Dict[int, int] = {}
        for m, c in p.items():
            val = c % mod
            if val == 0:
                continue
            col = monomial_to_col.get(m)
            if col is None:
                col = len(monomial_to_col)
                monomial_to_col[m] = col
            row[col] = val

        while row:
            lead_col = min(row.keys())
            if lead_col in pivots:
                piv_row = pivots[lead_col]
                factor = row[lead_col]
                for c_idx, p_val in piv_row.items():
                    new_v = (row.get(c_idx, 0) - factor * p_val) % mod
                    if new_v == 0:
                        row.pop(c_idx, None)
                    else:
                        row[c_idx] = new_v
            else:
                inv = pow(row[lead_col], mod - 2, mod)
                norm_row = {c_idx: (v * inv) % mod for c_idx, v in row.items()}
                pivots[lead_col] = norm_row
                break

    return len(pivots)
