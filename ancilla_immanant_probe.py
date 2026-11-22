"""Fermion-to-Boson spectrum probe: S_4 immanants, signed det_4 superpositions, and truncated Grenet ABPs."""
from __future__ import annotations

import itertools
import random
from typing import Dict, List, Set, Tuple

from apolar_higher_betti_probe import apolar_betti_deg4_torus
from gct_symmetry_invariants import perm_cycle_type
from jacobian_syzygy_betti_probe import jacobian_syzygy_torus
from poly_exact import (
    Poly,
    add_poly,
    determinant_poly,
    mul_poly,
    partial_deriv,
    permanent_poly,
    poly_det,
    scale_poly,
    var_poly,
    zero_poly,
)
from s4xs4_irrep_probe import S4_CHARS


def immanant_poly_4(irrep_name: str) -> Poly:
    """Exact S_4 immanant sum_{pi in S_4} chi(pi) prod_i x_{i, pi(i)}."""
    num_vars = 16
    _, char_map = S4_CHARS[irrep_name]
    total: Poly = {}
    for perm in itertools.permutations(range(4)):
        ct = perm_cycle_type(perm)
        chi = char_map[ct]
        if chi == 0:
            continue
        exp = [0] * num_vars
        for i, j in enumerate(perm):
            exp[i * 4 + j] = 1
        t = tuple(exp)
        val = total.get(t, 0) + chi
        if val == 0:
            total.pop(t, None)
        else:
            total[t] = val
    return total


def signed_det4(sign_mat: List[List[int]]) -> Poly:
    """Determinant of 4x4 matrix with signed entries sign_mat[i][j] * x_{i,j}."""
    mat = [[var_poly(i * 4 + j, 16, coeff=sign_mat[i][j]) for j in range(4)] for i in range(4)]
    return poly_det(mat, 16)


def grenet_perm4_subset_mask(dropped_s2: Set[Tuple[int, int]]) -> Poly:
    """
    Truncated Grenet (1 + 4 + 6 + 4) ABP for perm_4 removing layer-2 vertices in `dropped_s2`.
    Computes an exact (15 - len(dropped_s2)) x (15 - len(dropped_s2)) determinantal polynomial.
    """
    num_vars = 16
    s1 = [(j,) for j in range(4)]
    s2 = [t for t in itertools.combinations(range(4), 2) if t not in dropped_s2]
    s3 = list(itertools.combinations(range(4), 3))

    v1 = [var_poly(0 * 4 + j, num_vars) for j in range(4)]
    v2 = []
    for t2 in s2:
        acc = zero_poly()
        for idx1, t1 in enumerate(s1):
            if t1[0] in t2:
                j = t2[1] if t2[0] == t1[0] else t2[0]
                acc = add_poly(acc, mul_poly(v1[idx1], var_poly(1 * 4 + j, num_vars)))
        v2.append(acc)

    v3 = []
    for t3 in s3:
        acc = zero_poly()
        for idx2, t2 in enumerate(s2):
            if set(t2).issubset(t3):
                j = (set(t3) - set(t2)).pop()
                acc = add_poly(acc, mul_poly(v2[idx2], var_poly(2 * 4 + j, num_vars)))
        v3.append(acc)

    total = zero_poly()
    full = {0, 1, 2, 3}
    for idx3, t3 in enumerate(s3):
        j = (full - set(t3)).pop()
        total = add_poly(total, mul_poly(v3[idx3], var_poly(3 * 4 + j, num_vars)))
    return total


def main() -> None:
    d4 = determinant_poly(4)
    p4 = permanent_poly(4)

    assert immanant_poly_4("(1,1,1,1) sgn") == d4
    assert immanant_poly_4("(4) triv") == p4
    assert grenet_perm4_subset_mask(set()) == p4

    def ones_sign() -> List[List[int]]:
        return [[1] * 4 for _ in range(4)]

    # 1) det4 + 2 * det4(flip x00)
    s_flip1 = ones_sign()
    s_flip1[0][0] = -1
    sup_flip1 = add_poly(d4, scale_poly(signed_det4(s_flip1), 2))

    # 2) det4 + det4(flip x00, x11, x22)
    s_flip3 = ones_sign()
    s_flip3[0][0] = -1
    s_flip3[1][1] = -1
    s_flip3[2][2] = -1
    sup_flip3 = add_poly(d4, signed_det4(s_flip3))

    # 3) Random signed det_4 superpositions (3 and 4 terms)
    rng = random.Random(42)
    def rand_signed_det4() -> Poly:
        sm = [[rng.choice([-1, 1]) for _ in range(4)] for _ in range(4)]
        return signed_det4(sm)

    sup3 = zero_poly()
    for w in (1, 2, 3):
        sup3 = add_poly(sup3, scale_poly(rand_signed_det4(), w))

    sup4 = zero_poly()
    for w in (1, 2, 3, 5):
        sup4 = add_poly(sup4, scale_poly(rand_signed_det4(), w))

    models: List[Tuple[str, Poly]] = [
        ("det_4 (sgn)", d4),
        ("imm_(2,1,1)", immanant_poly_4("(2,1,1)")),
        ("imm_(2,2)", immanant_poly_4("(2,2)")),
        ("imm_(3,1) std", immanant_poly_4("(3,1) std")),
        ("det4 + 2*det4(f00)", sup_flip1),
        ("det4 + det4(f00,11,22)", sup_flip3),
        ("sum 3 signed det_4", sup3),
        ("sum 4 signed det_4", sup4),
        ("Grenet_12 (drop 3)", grenet_perm4_subset_mask({(0, 1), (1, 2), (2, 3)})),
        ("Grenet_13 (drop 2)", grenet_perm4_subset_mask({(0, 1), (2, 3)})),
        ("Grenet_14 (drop 1)", grenet_perm4_subset_mask({(0, 1)})),
        ("perm_4 (Grenet_15)", p4),
    ]

    # Verify every model is nonzero and uses all 16 variables essentially
    for name, poly in models:
        assert len(poly) > 0, f"{name} is zero polynomial!"
        for i in range(16):
            assert partial_deriv(poly, i), f"{name} dropped variable x_{i}!"

    print("=== Table 1: Fermion-to-Boson Spectrum — Apolar Ideal f^perp Betti (n=4) ===")
    print("Model                   | terms | dim(f^p_2) | b_{1,3} | b_{2,3} | b_{1,4} | b_{2,4} | b_{3,4}")
    print("-" * 92)
    jac_rows = []
    for name, poly in models:
        ap_tot, _ = apolar_betti_deg4_torus(poly, 4)
        df2, b13, b23, b14, b24, b34 = ap_tot
        print(
            f"{name:23s} | {len(poly):5d} | {df2:10d} | {b13:7d} | {b23:7d} | {b14:7d} | {b24:7d} | {b34:7d}"
        )
        j_tot, _ = jacobian_syzygy_torus(poly, 4)
        jac_rows.append((name, j_tot))

    print("\n=== Table 2: Fermion-to-Boson Spectrum — Jacobian Ideal J(f) Syzygies (n=4) ===")
    print("Model                   | dim(g_f) | dim(Syz2) | dim(V*g_f) | b_{2,5}^J | b_{3,5}^J")
    print("-" * 86)
    for name, (dg, s2, dvg, b25, b35) in jac_rows:
        print(f"{name:23s} | {dg:8d} | {s2:9d} | {dvg:10d} | {b25:9d} | {b35:9d}")


if __name__ == "__main__":
    main()
