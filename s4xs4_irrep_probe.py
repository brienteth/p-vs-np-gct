"""Exact S_4 x S_4 irreducible representation decomposition of shifted PD spaces for perm_4 vs det_4."""
from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

from gct_symmetry_invariants import basis_mod_p
from perm4_abp_frontier import MOD
from poly_exact import (
    Poly,
    determinant_poly,
    kth_partial_space,
    mul_poly,
    permanent_poly,
)
from shifted_pd_probe import monomials_of_degree_le

# 5 conjugacy classes of S_4: (representative, cycle_type, class_size)
S4_CLASSES: List[Tuple[Tuple[int, ...], Tuple[int, ...], int]] = [
    ((0, 1, 2, 3), (1, 1, 1, 1), 1),
    ((1, 0, 2, 3), (2, 1, 1), 6),
    ((1, 0, 3, 2), (2, 2), 3),
    ((1, 2, 0, 3), (3, 1), 8),
    ((1, 2, 3, 0), (4,), 6),
]

# Irreducible characters of S_4: name -> (dim, {cycle_type: chi})
S4_CHARS: Dict[str, Tuple[int, Dict[Tuple[int, ...], int]]] = {
    "(4) triv": (1, {(1, 1, 1, 1): 1, (2, 1, 1): 1, (2, 2): 1, (3, 1): 1, (4,): 1}),
    "(3,1) std": (3, {(1, 1, 1, 1): 3, (2, 1, 1): 1, (2, 2): -1, (3, 1): 0, (4,): -1}),
    "(2,2)": (2, {(1, 1, 1, 1): 2, (2, 1, 1): 0, (2, 2): 2, (3, 1): -1, (4,): 0}),
    "(2,1,1)": (3, {(1, 1, 1, 1): 3, (2, 1, 1): -1, (2, 2): -1, (3, 1): 0, (4,): 1}),
    "(1,1,1,1) sgn": (1, {(1, 1, 1, 1): 1, (2, 1, 1): -1, (2, 2): 1, (3, 1): 1, (4,): -1}),
}


def invert_perm(p: Tuple[int, ...]) -> Tuple[int, ...]:
    inv = [0] * len(p)
    for i, pi in enumerate(p):
        inv[pi] = i
    return tuple(inv)


def act_monom_s4xs4(m: Tuple[int, ...], row_perm: Tuple[int, ...], col_perm: Tuple[int, ...]) -> Tuple[int, ...]:
    """Map monomial m under x_{i,j} -> x_{row_perm[i], col_perm[j]}."""
    new_m = [0] * 16
    for i in range(4):
        ri = row_perm[i]
        base = i * 4
        rbase = ri * 4
        for j in range(4):
            e = m[base + j]
            if e:
                new_m[rbase + col_perm[j]] = e
    return tuple(new_m)


def compute_s4xs4_multiplicities(p: Poly, k: int, shift_deg: int) -> Tuple[int, Dict[Tuple[str, str], int]]:
    """
    Exact S_4 x S_4 irrep decomposition of <x^{<=shift} d^{=k} p> via RREF pivot lookup:
    since basis is in RREF, (g(b_r))[piv_m] == b_r[g^{-1}(piv_m)].
    """
    partials = kth_partial_space(p, 16, k)
    shifts = monomials_of_degree_le(16, shift_deg)
    gens = [mul_poly(s, d) for s in shifts for d in partials]

    basis, monom_to_col = basis_mod_p(gens, mod=MOD)
    dim_v = basis.shape[0]
    col_to_monom = [None] * len(monom_to_col)
    for m, c in monom_to_col.items():
        col_to_monom[c] = m

    piv_monoms = [col_to_monom[int(np.nonzero(basis[r])[0][0])] for r in range(dim_v)]

    traces: Dict[Tuple[Tuple[int, ...], Tuple[int, ...]], int] = {}
    for g1, ct1, _ in S4_CLASSES:
        inv1 = invert_perm(g1)
        for g2, ct2, _ in S4_CLASSES:
            inv2 = invert_perm(g2)
            tr = 0
            for r in range(dim_v):
                pre_m = act_monom_s4xs4(piv_monoms[r], inv1, inv2)
                c_idx = monom_to_col.get(pre_m)
                if c_idx is not None:
                    tr = (tr + int(basis[r, c_idx])) % MOD
            if tr > MOD // 2:
                tr -= MOD
            traces[(ct1, ct2)] = tr

    mults: Dict[Tuple[str, str], int] = {}
    dim_check = 0
    for name1, (d1, ch1) in S4_CHARS.items():
        for name2, (d2, ch2) in S4_CHARS.items():
            total = 0
            for _, ct1, sz1 in S4_CLASSES:
                for _, ct2, sz2 in S4_CLASSES:
                    total += sz1 * sz2 * ch1[ct1] * ch2[ct2] * traces[(ct1, ct2)]
            assert total % 576 == 0, f"Non-integer multiplicity: {total}/576 for {name1} x {name2}"
            m_val = total // 576
            assert m_val >= 0, f"Negative multiplicity {m_val} for {name1} x {name2}"
            mults[(name1, name2)] = m_val
            dim_check += d1 * d2 * m_val

    assert dim_check == dim_v, f"Dimension sum mismatch: {dim_check} != {dim_v}"
    return dim_v, mults


def report(k: int, shift_deg: int, p4: Poly, d4: Poly) -> None:
    dp, mp = compute_s4xs4_multiplicities(p4, k, shift_deg)
    dd, md = compute_s4xs4_multiplicities(d4, k, shift_deg)
    print(f"=== S_4 x S_4 Irrep Decomposition: k={k}, shift={shift_deg} (perm_4={dp}, det_4={dd}, net={dp - dd:+d}) ===")
    print(f"{'Irrep (row x col)':31s} | dim | perm_4 | det_4 | mult_gap | dim_gap")
    print("-" * 78)

    rows = []
    pos_dim_gap = 0
    neg_dim_gap = 0
    for name1, (d1, _) in S4_CHARS.items():
        for name2, (d2, _) in S4_CHARS.items():
            vp = mp[(name1, name2)]
            vd = md[(name1, name2)]
            mg = vp - vd
            dg = d1 * d2 * mg
            if dg > 0:
                pos_dim_gap += dg
            elif dg < 0:
                neg_dim_gap += dg
            if mg != 0:
                rows.append((dg, f"{name1} x {name2}", d1 * d2, vp, vd, mg))

    rows.sort(key=lambda x: x[0], reverse=True)
    for dg, label, ir_dim, vp, vd, mg in rows:
        print(f"{label:31s} | {ir_dim:3d} | {vp:6d} | {vd:5d} | {mg:+8d} | {dg:+7d}")
    print(
        f"Summary: positive-sector gap = {pos_dim_gap:+d}, "
        f"negative-sector cancellation = {neg_dim_gap:+d}, net = {pos_dim_gap + neg_dim_gap:+d}\n"
    )


def main() -> None:
    p4 = permanent_poly(4)
    d4 = determinant_poly(4)
    report(1, 1, p4, d4)
    report(2, 1, p4, d4)


if __name__ == "__main__":
    main()
