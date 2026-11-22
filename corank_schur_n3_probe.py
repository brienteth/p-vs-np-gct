"""Schur-complement classification of affine det_m(A_0 + L(X)) for n=3 (Corank s=2 and s=3)."""
from __future__ import annotations

import random
from typing import List, Tuple

from affine_det_projection_probe import poly_det_mod
from apolar_higher_betti_probe import apolar_betti_deg4_ungraded
from general_det6_probe import layered_abp_det_split
from jacobian_syzygy_betti_probe import jacobian_syzygy_ungraded
from koszul_flattening_probe import koszul_rank, recenter_poly_from_mod
from perm4_abp_frontier import MOD
from poly_exact import (
    Poly,
    add_poly,
    const_poly,
    determinant_poly,
    mul_poly,
    permanent_poly,
    var_poly,
    zero_poly,
)


def rand_lin_mod(num_vars: int, rng: random.Random, mod: int = MOD) -> Poly:
    p: Poly = {}
    for v in range(num_vars):
        c = rng.randint(-5, 5)
        if c != 0:
            p[tuple(1 if k == v else 0 for k in range(num_vars))] = c % mod
    return p


def homog_part(p: Poly, deg: int, mod: int = MOD) -> Poly:
    return {m: c % mod for m, c in p.items() if sum(m) == deg and c % mod != 0}


def mat_mul_poly(A: List[List[Poly]], B: List[List[Poly]], mod: int = MOD) -> List[List[Poly]]:
    r_a = len(A)
    c_a = len(A[0])
    c_b = len(B[0])
    out = [[zero_poly() for _ in range(c_b)] for _ in range(r_a)]
    for i in range(r_a):
        for j in range(c_b):
            acc = zero_poly()
            for k in range(c_a):
                if A[i][k] and B[k][j]:
                    acc = add_poly(acc, mul_poly(A[i][k], B[k][j]))
            out[i][j] = {m: c % mod for m, c in acc.items() if c % mod != 0}
    return out


def build_corank_s2_n3(r: int, num_vars: int, rng: random.Random, mod: int = MOD) -> Poly:
    """
    Exact degree-3 component of det_{r+2}([[I_r + B(X), C(X)], [D(X), E(X)]])
    with rank(E) = 1: E = [[l1, l2], [0, 0]].
    Formula: f_3 = l2 * (D C)_{1,0} - l1 * (D C)_{1,1}.
    """
    D = [[rand_lin_mod(num_vars, rng, mod) for _ in range(r)] for _ in range(2)]
    C = [[rand_lin_mod(num_vars, rng, mod) for _ in range(2)] for _ in range(r)]
    l1 = rand_lin_mod(num_vars, rng, mod)
    l2 = rand_lin_mod(num_vars, rng, mod)
    DC = mat_mul_poly(D, C, mod=mod)
    f3 = add_poly(mul_poly(l2, DC[1][0]), mul_poly(l1, DC[1][1]), sign=-1)
    return {m: c % mod for m, c in f3.items() if c % mod != 0}


def verify_schur_identities_n3() -> None:
    rng = random.Random(999)
    nv = 9

    # 1) Corank s=3 check at m=5 (r=2, s=3)
    B = [[rand_lin_mod(nv, rng) for _ in range(2)] for _ in range(2)]
    C = [[rand_lin_mod(nv, rng) for _ in range(3)] for _ in range(2)]
    D = [[rand_lin_mod(nv, rng) for _ in range(2)] for _ in range(3)]
    E = [[rand_lin_mod(nv, rng) for _ in range(3)] for _ in range(3)]
    M5: List[List[Poly]] = [[zero_poly() for _ in range(5)] for _ in range(5)]
    for i in range(2):
        for j in range(2):
            M5[i][j] = add_poly(const_poly(1, nv), B[i][j]) if i == j else B[i][j]
        for j in range(3):
            M5[i][2 + j] = C[i][j]
    for i in range(3):
        for j in range(2):
            M5[2 + i][j] = D[i][j]
        for j in range(3):
            M5[2 + i][2 + j] = E[i][j]
    det_m5_deg3 = homog_part(poly_det_mod(M5, mod=MOD), 3)
    det_e = homog_part(poly_det_mod(E, mod=MOD), 3)
    assert det_m5_deg3 == det_e, "Corank s=3 Schur lemma verification failed!"

    # 2) Corank s=2 check at m=4 (r=2) and m=5 (r=3)
    for r in (2, 3):
        m = r + 2
        B = [[rand_lin_mod(nv, rng) for _ in range(r)] for _ in range(r)]
        C = [[rand_lin_mod(nv, rng) for _ in range(2)] for _ in range(r)]
        D = [[rand_lin_mod(nv, rng) for _ in range(r)] for _ in range(2)]
        l1 = rand_lin_mod(nv, rng)
        l2 = rand_lin_mod(nv, rng)
        M: List[List[Poly]] = [[zero_poly() for _ in range(m)] for _ in range(m)]
        for i in range(r):
            for j in range(r):
                M[i][j] = add_poly(const_poly(1, nv), B[i][j]) if i == j else B[i][j]
            for j in range(2):
                M[i][r + j] = C[i][j]
        for i in range(2):
            for j in range(r):
                M[r + i][j] = D[i][j]
        M[r][r] = l1
        M[r][r + 1] = l2
        det_deg3 = homog_part(poly_det_mod(M, mod=MOD), 3)
        DC = mat_mul_poly(D, C, mod=MOD)
        schur_f3 = add_poly(mul_poly(l2, DC[1][0]), mul_poly(l1, DC[1][1]), sign=-1)
        schur_f3 = {k: v % MOD for k, v in schur_f3.items() if v % MOD != 0}
        assert det_deg3 == schur_f3, f"Corank s=2 Schur formula failed at r={r}!"

    print("[Self-Checks] Direct poly_det_mod Schur checks passed for s=3 (m=5) and s=2 (m=4,5)\n")


def main() -> None:
    verify_schur_identities_n3()

    p3 = permanent_poly(3)
    d3 = determinant_poly(3)
    rng_abp = random.Random(123)
    m6_23 = recenter_poly_from_mod(layered_abp_det_split(2, 3, 9, rng_abp))
    m7_33 = recenter_poly_from_mod(layered_abp_det_split(3, 3, 9, rng_abp))

    rng = random.Random(31415)
    models: List[Tuple[str, Poly]] = [
        ("det_3 (s=3)", d3),
        ("s=1 m=6 (2,3)", m6_23),
        ("s=1 m=7 (3,3)", m7_33),
        ("perm_3", p3),
    ]
    for r in (2, 3, 4, 5, 6, 8):
        models.append((f"s=2 r={r} (m={r+2})", build_corank_s2_n3(r, 9, rng)))

    print("=== Table 1 (n=3): Macaulay Apolar Ideal f^perp Betti (deg 2..4) ===")
    print("Model           | dim(f^p_2) | b_{1,3} | b_{2,3} | b_{1,4} | b_{2,4} | b_{3,4}")
    print("-" * 77)
    jac_rows = []
    kos_rows = []
    for name, poly in models:
        df2, b13, b23, b14, b24, b34 = apolar_betti_deg4_ungraded(poly, 9)
        print(f"{name:15s} | {df2:10d} | {b13:7d} | {b23:7d} | {b14:7d} | {b24:7d} | {b34:7d}")
        jac_rows.append((name, jacobian_syzygy_ungraded(poly, 9)))
        kos_rows.append(
            (name, koszul_rank(poly, 9, 1, 1), koszul_rank(poly, 9, 1, 2), koszul_rank(poly, 9, 1, 3))
        )

    print("\n=== Table 2 (n=3): Jacobian Ideal J(f) Syzygy Invariants (deg 1..2) ===")
    print("Model           | dim(g_f) | dim(Syz2) | b_{2,4}^J | b_{2,4}^extra | b_{3,4}^J")
    print("-" * 77)
    for name, (dg, s2, b24, b24x, b34) in jac_rows:
        print(f"{name:15s} | {dg:8d} | {s2:9d} | {b24:9d} | {b24x:13d} | {b34:9d}")

    print("\n=== Table 3 (n=3): Koszul Flattening Ranks (k=1) ===")
    print("Model           | p=1 (<=81) | p=2 (<=324) | p=3 (<=756)")
    print("-" * 58)
    for name, r1, r2, r3 in kos_rows:
        print(f"{name:15s} | {r1:9d} | {r2:11d} | {r3:11d}")


if __name__ == "__main__":
    main()
