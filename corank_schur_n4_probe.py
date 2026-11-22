"""Schur-complement classification of affine det_m(A_0 + L(X)) for n=4 (Corank s=2a, 2b, 3)."""
from __future__ import annotations

import random
from typing import List, Tuple

from affine_det_projection_probe import poly_det_mod
from apolar_betti_probe import apolar_quadric_betti, lie_annihilator_dim
from apolar_higher_betti_probe import apolar_betti_deg4_torus, monom_multideg
from corank_schur_n3_probe import homog_part, mat_mul_poly, rand_lin_mod
from jacobian_syzygy_betti_probe import jacobian_syzygy_torus
from koszul_flattening_probe import koszul_rank
from perm4_abp_frontier import MOD
from poly_exact import (
    Poly,
    add_poly,
    const_poly,
    determinant_poly,
    mul_poly,
    partial_deriv,
    permanent_poly,
    var_poly,
    zero_poly,
)


def det2_poly(M: List[List[Poly]], mod: int = MOD) -> Poly:
    res = add_poly(mul_poly(M[0][0], M[1][1]), mul_poly(M[0][1], M[1][0]), sign=-1)
    return {m: c % mod for m, c in res.items() if c % mod != 0}


def trace_mat_poly(B: List[List[Poly]], mod: int = MOD) -> Poly:
    acc = zero_poly()
    for i in range(len(B)):
        acc = add_poly(acc, B[i][i])
    return {m: c % mod for m, c in acc.items() if c % mod != 0}


def build_corank_s2a_n4(r: int, num_vars: int, rng: random.Random, mod: int = MOD) -> Poly:
    """Corank s=2, Branch 2a (E=0): f_4 = det_{2x2}(D_{2xr} C_{rx2}), m = r + 2."""
    D = [[rand_lin_mod(num_vars, rng, mod) for _ in range(r)] for _ in range(2)]
    C = [[rand_lin_mod(num_vars, rng, mod) for _ in range(2)] for _ in range(r)]
    DC = mat_mul_poly(D, C, mod=mod)
    return det2_poly(DC, mod=mod)


def build_corank_s2b_n4(r: int, num_vars: int, rng: random.Random, mod: int = MOD) -> Poly:
    """
    Corank s=2, Branch 2b (rank(E)=1, E=[[l1,l2],[0,0]]):
      f_4 = det_2(DC) + l1*(DBC)_{1,1} - l2*(DBC)_{1,0} + tr(B)*(l2*(DC)_{1,0} - l1*(DC)_{1,1}).
    """
    B = [[rand_lin_mod(num_vars, rng, mod) for _ in range(r)] for _ in range(r)]
    C = [[rand_lin_mod(num_vars, rng, mod) for _ in range(2)] for _ in range(r)]
    D = [[rand_lin_mod(num_vars, rng, mod) for _ in range(r)] for _ in range(2)]
    l1 = rand_lin_mod(num_vars, rng, mod)
    l2 = rand_lin_mod(num_vars, rng, mod)
    DC = mat_mul_poly(D, C, mod=mod)
    DB = mat_mul_poly(D, B, mod=mod)
    DBC = mat_mul_poly(DB, C, mod=mod)
    trB = trace_mat_poly(B, mod=mod)

    term1 = det2_poly(DC, mod=mod)
    term2 = add_poly(mul_poly(l1, DBC[1][1]), mul_poly(l2, DBC[1][0]), sign=-1)
    deg3_inner = add_poly(mul_poly(l2, DC[1][0]), mul_poly(l1, DC[1][1]), sign=-1)
    term3 = mul_poly(trB, deg3_inner)
    f4 = add_poly(add_poly(term1, term2), term3)
    return {m: c % mod for m, c in f4.items() if c % mod != 0}


def build_corank_s3_n4(r: int, num_vars: int, rng: random.Random, mod: int = MOD) -> Poly:
    """
    Corank s=3 (rank(E)=2, last row of E zero):
      f_4 = -(M_0 (DC)_{2,0} + M_1 (DC)_{2,1} + M_2 (DC)_{2,2}), m = r + 3.
    """
    C = [[rand_lin_mod(num_vars, rng, mod) for _ in range(3)] for _ in range(r)]
    D = [[rand_lin_mod(num_vars, rng, mod) for _ in range(r)] for _ in range(3)]
    E = [[rand_lin_mod(num_vars, rng, mod) for _ in range(3)] for _ in range(2)]
    DC = mat_mul_poly(D, C, mod=mod)

    M0 = add_poly(mul_poly(E[0][1], E[1][2]), mul_poly(E[0][2], E[1][1]), sign=-1)
    M1 = add_poly(mul_poly(E[0][0], E[1][2]), mul_poly(E[0][2], E[1][0]), sign=-1)
    M1 = {m: (-c) % mod for m, c in M1.items() if c % mod != 0}
    M2 = add_poly(mul_poly(E[0][0], E[1][1]), mul_poly(E[0][1], E[1][0]), sign=-1)

    s = add_poly(mul_poly(M0, DC[2][0]), mul_poly(M1, DC[2][1]))
    s = add_poly(s, mul_poly(M2, DC[2][2]))
    return {m: (-c) % mod for m, c in s.items() if c % mod != 0}


def verify_schur_identities_n4() -> None:
    rng = random.Random(2025)
    nv = 16

    # Use sparse 3-variable linear forms for blazing-fast 4x4 poly_det_mod verification
    def sparse_lin() -> Poly:
        p = zero_poly()
        for v in rng.sample(range(nv), 4):
            p = add_poly(p, var_poly(v, nv, rng.randint(-3, 3)))
        return {m: c % MOD for m, c in p.items() if c % MOD != 0}

    # 1) Corank s=2a (r=2, m=4)
    B = [[sparse_lin() for _ in range(2)] for _ in range(2)]
    C = [[sparse_lin() for _ in range(2)] for _ in range(2)]
    D = [[sparse_lin() for _ in range(2)] for _ in range(2)]
    M4a: List[List[Poly]] = [[zero_poly() for _ in range(4)] for _ in range(4)]
    for i in range(2):
        for j in range(2):
            M4a[i][j] = add_poly(const_poly(1, nv), B[i][j]) if i == j else B[i][j]
            M4a[i][2 + j] = C[i][j]
            M4a[2 + i][j] = D[i][j]
    det_4a = homog_part(poly_det_mod(M4a, mod=MOD), 4)
    schur_4a = det2_poly(mat_mul_poly(D, C, mod=MOD), mod=MOD)
    assert det_4a == schur_4a, "Corank s=2a Schur formula check failed!"

    # 2) Corank s=2b (r=2, m=4)
    l1, l2 = sparse_lin(), sparse_lin()
    M4b = [row[:] for row in M4a]
    M4b[2][2] = l1
    M4b[2][3] = l2
    det_4b = homog_part(poly_det_mod(M4b, mod=MOD), 4)
    DC = mat_mul_poly(D, C, mod=MOD)
    DBC = mat_mul_poly(mat_mul_poly(D, B, mod=MOD), C, mod=MOD)
    trB = trace_mat_poly(B, mod=MOD)
    t1 = det2_poly(DC, mod=MOD)
    t2 = add_poly(mul_poly(l1, DBC[1][1]), mul_poly(l2, DBC[1][0]), sign=-1)
    t3 = mul_poly(trB, add_poly(mul_poly(l2, DC[1][0]), mul_poly(l1, DC[1][1]), sign=-1))
    schur_4b = {m: c % MOD for m, c in add_poly(add_poly(t1, t2), t3).items() if c % MOD != 0}
    assert det_4b == schur_4b, "Corank s=2b Schur formula check failed!"

    # 3) Corank s=3 (r=1, m=4)
    b00 = sparse_lin()
    C3 = [[sparse_lin() for _ in range(3)]]
    D3 = [[sparse_lin()] for _ in range(3)]
    E3 = [[sparse_lin() for _ in range(3)] for _ in range(2)]
    M4c: List[List[Poly]] = [[zero_poly() for _ in range(4)] for _ in range(4)]
    M4c[0][0] = add_poly(const_poly(1, nv), b00)
    for j in range(3):
        M4c[0][1 + j] = C3[0][j]
        M4c[1 + j][0] = D3[j][0]
    for i in range(2):
        for j in range(3):
            M4c[1 + i][1 + j] = E3[i][j]
    det_4c = homog_part(poly_det_mod(M4c, mod=MOD), 4)
    DC3 = mat_mul_poly(D3, C3, mod=MOD)
    m0 = add_poly(mul_poly(E3[0][1], E3[1][2]), mul_poly(E3[0][2], E3[1][1]), sign=-1)
    m1 = add_poly(mul_poly(E3[0][0], E3[1][2]), mul_poly(E3[0][2], E3[1][0]), sign=-1)
    m1 = {m: (-c) % MOD for m, c in m1.items() if c % MOD != 0}
    m2 = add_poly(mul_poly(E3[0][0], E3[1][1]), mul_poly(E3[0][1], E3[1][0]), sign=-1)
    schur_4c = add_poly(add_poly(mul_poly(m0, DC3[2][0]), mul_poly(m1, DC3[2][1])), mul_poly(m2, DC3[2][2]))
    schur_4c = {m: (-c) % MOD for m, c in schur_4c.items() if c % MOD != 0}
    assert det_4c == schur_4c, "Corank s=3 Schur formula check failed!"

    print("[Self-Checks] Direct poly_det_mod Schur checks passed for s=2a, s=2b, and s=3 (n=4)\n")


def torus_s2a_det2_dc_m10() -> Poly:
    """
    Construct a torus-bihomogeneous (multidegree ((1,1,1,1),(1,1,1,1))) Corank s=2a
    polynomial f = det_{2x2}(D_{2x8} C_{8x2}) using all 16 variables essentially (m=10).
    """
    x = [var_poly(k, 16) for k in range(16)]
    D = [
        [x[0], x[1], x[2], x[3], zero_poly(), zero_poly(), zero_poly(), zero_poly()],
        [zero_poly(), zero_poly(), zero_poly(), zero_poly(), x[4], x[5], x[6], x[7]],
    ]
    C = [
        [x[9], zero_poly()],
        [x[8], zero_poly()],
        [zero_poly(), x[11]],
        [zero_poly(), x[10]],
        [x[13], zero_poly()],
        [x[12], zero_poly()],
        [zero_poly(), x[15]],
        [zero_poly(), x[14]],
    ]
    poly = det2_poly(mat_mul_poly(D, C, mod=MOD), mod=MOD)
    for m in poly:
        assert monom_multideg(m, 4) == ((1, 1, 1, 1), (1, 1, 1, 1)), f"Bad multideg: {m}"
    for i in range(16):
        assert partial_deriv(poly, i), f"Torus s=2a dropped variable x_{i}"
    return poly


def main() -> None:
    verify_schur_identities_n4()

    p4 = permanent_poly(4)
    d4 = determinant_poly(4)
    rng = random.Random(27182)

    models: List[Tuple[str, Poly]] = [
        ("det_4 (s=4)", d4),
        ("perm_4", p4),
    ]
    for r in (2, 3, 4, 5, 6, 8):
        models.append((f"s=2a r={r} (m={r+2})", build_corank_s2a_n4(r, 16, rng)))
    for r in (2, 4, 6):
        models.append((f"s=2b r={r} (m={r+2})", build_corank_s2b_n4(r, 16, rng)))
    for r in (1, 2, 3, 4, 5, 7):
        models.append((f"s=3  r={r} (m={r+3})", build_corank_s3_n4(r, 16, rng)))

    print("=== Global GL_16-Invariant Scan of All Non-ABP Coranks (n=4) ===")
    print("Model               | dim(g_f) | dim(f^p_2) | b_{1,3} | b_{2,3} | koszul(1,1)")
    print("-" * 77)
    for name, poly in models:
        dg = lie_annihilator_dim(poly, 16)
        df2, _, b13, b23 = apolar_quadric_betti(poly, 16)
        kr = koszul_rank(poly, 16, k=1, p=1)
        print(f"{name:19s} | {dg:8d} | {df2:10d} | {b13:7d} | {b23:7d} | {kr:11d}")

    # Torus-structured Corank s=2a test (m=10)
    t_s2a = torus_s2a_det2_dc_m10()
    print("\n=== Torus-Structured Corank s=2a (m=10, all 16 vars) vs perm_4 & det_4 ===")
    for name, poly in [("det_4", d4), ("torus s=2a m=10", t_s2a), ("perm_4", p4)]:
        ap = apolar_betti_deg4_torus(poly, 4)[0]
        jc = jacobian_syzygy_torus(poly, 4)[0]
        print(f"{name:16s} | apolar={ap} | jacobian={jc}")


if __name__ == "__main__":
    main()
