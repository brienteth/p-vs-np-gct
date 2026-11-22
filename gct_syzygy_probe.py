"""Probe GCT syzygy dimensions and padding survival for perm_n vs padded det_m."""
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
)


def pad_poly(p: Poly, orig_vars: int, extra_power: int) -> Poly:
    """Multiply p(x_1..x_N) by z^{extra_power} where z is a new variable at index orig_vars."""
    res: Poly = {}
    for m, c in p.items():
        res[m + (extra_power,)] = c
    return res


def monomials_le(num_vars: int, max_deg: int) -> List[Poly]:
    res: List[Poly] = [{(0,) * num_vars: 1}]
    for d in range(1, max_deg + 1):
        for comb in itertools.combinations_with_replacement(range(num_vars), d):
            exp = [0] * num_vars
            for idx in comb:
                exp[idx] += 1
            res.append({tuple(exp): 1})
    return res


def syzygy_probe(p: Poly, num_vars: int, k: int, shift_deg: int) -> tuple[int, int, int]:
    """Return (total_generators, span_dim, syzygy_dim) for x^{<=shift} * d^{=k} p."""
    partials = kth_partial_space(p, num_vars, k)
    shifts = monomials_le(num_vars, shift_deg)
    gens = [mul_poly(s, d) for s in shifts for d in partials]
    dim = rank_mod_p(gens)
    return len(gens), dim, len(gens) - dim


def main() -> None:
    print("=== 1) Unpadded perm_n vs det_n syzygies (k=1, shift=1) ===")
    print("Poly   | vars | generators | span_dim | syzygy_dim")
    print("-" * 55)
    for n in (2, 3):
        nv = n * n
        for name, poly in [(f"perm_{n}", permanent_poly(n)), (f"det_{n}", determinant_poly(n))]:
            g, d, syz = syzygy_probe(poly, nv, k=1, shift_deg=1)
            print(f"{name:6s} | {nv:4d} | {g:10d} | {d:8d} | {syz:10d}")

    print("\n=== 2) Padding test: z^{m-3} * perm_3 vs z^{m-3} * det_3 (n=3, k=1, shift=1) ===")
    p3 = permanent_poly(3)
    d3 = determinant_poly(3)
    for m in (3, 4, 5):
        extra = m - 3
        nv = 9 if extra == 0 else 10
        pp = p3 if extra == 0 else pad_poly(p3, 9, extra)
        dd = d3 if extra == 0 else pad_poly(d3, 9, extra)
        gp, dp, sp = syzygy_probe(pp, nv, k=1, shift_deg=1)
        gd, dd_dim, sd = syzygy_probe(dd, nv, k=1, shift_deg=1)
        print(
            f"m={m} (pad z^{extra}): "
            f"perm span={dp}/{gp} (syz={sp}) | "
            f"det span={dd_dim}/{gd} (syz={sd}) | "
            f"gap={dp - dd_dim:+d}"
        )


if __name__ == "__main__":
    main()
