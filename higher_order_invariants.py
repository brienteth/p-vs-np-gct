"""Higher-order shifted partial derivative probe for perm_n vs det_n (n=3, 4)."""
from __future__ import annotations

from poly_exact import (
    determinant_poly,
    kth_partial_space,
    mul_poly,
    permanent_poly,
    rank_mod_p,
)
from shifted_pd_probe import monomials_of_degree_le


def measure(p, num_vars: int, k: int, shift_deg: int) -> tuple[int, int]:
    partials = kth_partial_space(p, num_vars, k)
    shifts = monomials_of_degree_le(num_vars, shift_deg)
    gens = [mul_poly(s, d) for s in shifts for d in partials]
    return rank_mod_p(gens), len(gens)


def main() -> None:
    print("n | k | shift | perm_dim / gens | det_dim / gens | gap (perm - det)")
    print("-" * 72)

    p3 = permanent_poly(3)
    d3 = determinant_poly(3)
    for k, s in [(1, 1), (1, 2), (2, 1), (2, 2)]:
        dp, gp = measure(p3, 9, k, s)
        dd, gd = measure(d3, 9, k, s)
        print(f"3 | {k} | {s:5d} | {dp:6d} / {gp:<6d} | {dd:6d} / {gd:<6d} | {dp - dd:+d}")

    p4 = permanent_poly(4)
    d4 = determinant_poly(4)
    for k, s in [(1, 1), (2, 1)]:
        dp, gp = measure(p4, 16, k, s)
        dd, gd = measure(d4, 16, k, s)
        print(f"4 | {k} | {s:5d} | {dp:6d} / {gp:<6d} | {dd:6d} / {gd:<6d} | {dp - dd:+d}")


if __name__ == "__main__":
    main()
