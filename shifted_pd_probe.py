"""Probe partial derivative & shifted partial derivative dimensions for perm_n vs det_n."""
from __future__ import annotations

import itertools
from typing import List

from poly_exact import (
    Poly,
    determinant_poly,
    kth_partial_space,
    mul_poly,
    permanent_poly,
    rank_mod_p,
    var_poly,
)


def monomials_of_degree_le(num_vars: int, max_deg: int) -> List[Poly]:
    """Generate all monomials of degree <= max_deg in num_vars variables."""
    res: List[Poly] = [{(0,) * num_vars: 1}]
    for d in range(1, max_deg + 1):
        for comb in itertools.combinations_with_replacement(range(num_vars), d):
            exp = [0] * num_vars
            for idx in comb:
                exp[idx] += 1
            res.append({tuple(exp): 1})
    return res


def shifted_pd_dim(p: Poly, num_vars: int, k: int, shift_deg: int) -> int:
    """Compute dim(< x^{<= shift_deg} * d^{=k} p >) over F_p."""
    partials = kth_partial_space(p, num_vars, k)
    if shift_deg == 0:
        return rank_mod_p(partials)
    shifts = monomials_of_degree_le(num_vars, shift_deg)
    shifted = [mul_poly(s, d) for s in shifts for d in partials]
    return rank_mod_p(shifted)


def main() -> None:
    print("n | k | shift | dim(perm_n) | dim(det_n) | gap (perm - det)")
    print("-" * 64)
    for n in (2, 3, 4):
        num_vars = n * n
        p_n = permanent_poly(n)
        d_n = determinant_poly(n)
        for k in range(1, n):
            max_shift = 1 if n <= 3 else (1 if k == n - 1 else 0)
            for s in range(0, max_shift + 1):
                dim_p = shifted_pd_dim(p_n, num_vars, k, s)
                dim_d = shifted_pd_dim(d_n, num_vars, k, s)
                print(f"{n} | {k} | {s:5d} | {dim_p:11d} | {dim_d:10d} | {dim_p - dim_d:+d}")


if __name__ == "__main__":
    main()
