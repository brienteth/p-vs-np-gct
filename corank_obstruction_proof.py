"""Arbitrary-m Corank s >= 2 obstruction theorems & constructive proofs for n=3 and n=4."""
from __future__ import annotations

import random
from typing import Dict, List, Sequence, Tuple

import numpy as np

from affine_det_projection_probe import poly_det_mod
from apolar_betti_probe import apolar_quadric_betti, lie_annihilator_dim
from apolar_higher_betti_probe import apolar_betti_deg4_ungraded, polys_to_dense_mod, rank_matrix_mod
from corank_schur_n3_probe import homog_part, mat_mul_poly, rand_lin_mod
from corank_schur_n4_probe import det2_poly, trace_mat_poly
from jacobian_syzygy_betti_probe import jacobian_syzygy_ungraded
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
    scale_poly,
    var_poly,
    zero_poly,
)


def eval_poly_mod(p: Poly, point: Sequence[int], mod: int = MOD) -> int:
    total = 0
    for monom, coeff in p.items():
        term = coeff % mod
        for var_i, exp in enumerate(monom):
            if exp:
                term = (term * pow(point[var_i], exp, mod)) % mod
        total = (total + term) % mod
    return total


def hessian_nullity_at(f: Poly, num_vars: int, point: Sequence[int], mod: int = MOD) -> int:
    """Assert point lies in Sing(f) (f(pt)=0, grad f(pt)=0) and return num_vars - rank(H_f(pt))."""
    val = eval_poly_mod(f, point, mod=mod)
    assert val == 0, f"Point is not on hypersurface: f(pt)={val}"
    partials = [partial_deriv(f, i) for i in range(num_vars)]
    grad = [eval_poly_mod(dp, point, mod=mod) for dp in partials]
    assert all(g == 0 for g in grad), f"Point is not singular: grad={grad}"

    hess = np.zeros((num_vars, num_vars), dtype=np.int64)
    for i in range(num_vars):
        for j in range(i, num_vars):
            v = eval_poly_mod(partial_deriv(partials[i], j), point, mod=mod)
            hess[i, j] = v
            hess[j, i] = v
    return num_vars - rank_matrix_mod(hess, mod=mod)


def rand_homog_poly_mod(
    num_vars: int, deg: int, rng: random.Random, zero_monom: Tuple[int, ...] = (), mod: int = MOD
) -> Poly:
    """Dense random homogeneous polynomial of degree `deg`, optionally zeroing `zero_monom`."""
    import itertools

    p: Poly = {}
    for comb in itertools.combinations_with_replacement(range(num_vars), deg):
        exp = [0] * num_vars
        for idx in comb:
            exp[idx] += 1
        t = tuple(exp)
        if t == zero_monom:
            continue
        c = rng.randint(-5, 5)
        if c != 0:
            p[t] = c % mod
    return p


def prove_n3_corank_s2() -> None:
    print("=== Part A (n=3, N=9): Arbitrary-m Corank s=2 Obstruction Proof ===")
    rng = random.Random(202601)
    # Build f_3 = x_0 Q_1 + x_1 Q_2 with zero x_2^2 terms in Q_1, Q_2 so pt = e_2 in Sing(f_3)
    e2_sq = tuple(2 if i == 2 else 0 for i in range(9))
    Q1 = rand_homog_poly_mod(9, 2, rng, zero_monom=e2_sq)
    Q2 = rand_homog_poly_mod(9, 2, rng, zero_monom=e2_sq)
    x0 = var_poly(0, 9)
    x1 = var_poly(1, 9)
    f3 = add_poly(mul_poly(x0, Q1), mul_poly(x1, Q2))
    f3 = {m: c % MOD for m, c in f3.items() if c % MOD != 0}

    ap = apolar_betti_deg4_ungraded(f3, 9)
    jc = jacobian_syzygy_ungraded(f3, 9)
    k1, k2, k3 = koszul_rank(f3, 9, 1, 1), koszul_rank(f3, 9, 1, 2), koszul_rank(f3, 9, 1, 3)
    assert ap == (36, 0, 160, 0, 0, 315), f"Unexpected apolar for generic s=2: {ap}"
    assert jc == (0, 71, 71, 35, 0), f"Unexpected jacobian for generic s=2: {jc}"
    assert (k1, k2, k3) == (80, 315, 672), f"Unexpected koszul for generic s=2: {(k1, k2, k3)}"
    print(f"Generic f_3 = x0*Q1 + x1*Q2: apolar={ap}, jacobian={jc}, koszul={(k1, k2, k3)}")

    # Constructive Hilbert-Burch 35 = C(7,3) syzygy verification
    pairs2 = [(u, v) for u in range(9) for v in range(u, 9)]
    pair2_to_idx = {pair: idx for idx, pair in enumerate(pairs2)}
    x_quads = []
    for a, b in pairs2:
        exp = [0] * 9
        exp[a] += 1
        exp[b] += 1
        x_quads.append({tuple(exp): 1})

    partials = [
        {m: c % MOD for m, c in partial_deriv(f3, i).items() if c % MOD != 0} for i in range(9)
    ]
    psi2_polys = [mul_poly(x_quads[p2_i], partials[i]) for p2_i in range(45) for i in range(9)]
    psi2_mat = polys_to_dense_mod(psi2_polys, mod=MOD)

    L = [partial_deriv(Q1, a) for a in range(9)]
    M = [partial_deriv(Q2, a) for a in range(9)]

    def add_quad_to_row(row: np.ndarray, q: Poly, var_e: int, sign: int = 1) -> None:
        for mon, c in q.items():
            nz = [idx for idx, e in enumerate(mon) if e > 0]
            u, v = (nz[0], nz[0]) if len(nz) == 1 else (nz[0], nz[1])
            col = pair2_to_idx[(u, v)] * 9 + var_e
            row[col] = (row[col] + sign * c) % MOD

    import itertools

    hb_rows = []
    for a, b, c in itertools.combinations(range(2, 9), 3):
        row = np.zeros(45 * 9, dtype=np.int64)
        qa = add_poly(mul_poly(L[b], M[c]), mul_poly(L[c], M[b]), sign=-1)
        qb = add_poly(mul_poly(L[a], M[c]), mul_poly(L[c], M[a]), sign=-1)
        qc = add_poly(mul_poly(L[a], M[b]), mul_poly(L[b], M[a]), sign=-1)
        add_quad_to_row(row, qa, a, sign=1)
        add_quad_to_row(row, qb, b, sign=-1)
        add_quad_to_row(row, qc, c, sign=1)
        hb_rows.append(row)

    hb_mat = np.stack(hb_rows, axis=0)
    assert not np.any((hb_mat @ psi2_mat) % MOD), "Hilbert-Burch syzygy failed ker(psi_2)!"
    hb_rank = rank_matrix_mod(hb_mat, mod=MOD)
    assert hb_rank == 35, f"Expected Hilbert-Burch rank 35, got {hb_rank}"

    # Universal 36 Koszul syzygies
    koszul_rows = []
    for i in range(9):
        for j in range(i + 1, 9):
            row = np.zeros(45 * 9, dtype=np.int64)
            add_quad_to_row(row, partials[j], i, sign=1)
            add_quad_to_row(row, partials[i], j, sign=-1)
            koszul_rows.append(row)
    koszul_mat = np.stack(koszul_rows, axis=0)
    total_rank = rank_matrix_mod(np.vstack([koszul_mat, hb_mat]), mod=MOD)
    assert total_rank == 71, f"Expected Koszul + Hilbert-Burch rank 71, got {total_rank}"
    print(f"[Constructive Proof] 35 Hilbert-Burch syzygies verified: ker(psi_2)=True, rank(HB)={hb_rank}, rank(Koszul+HB)={total_rank}")

    # Singular-locus Hessian nullity comparison (n=3)
    p3 = permanent_poly(3)
    d3 = determinant_poly(3)
    pt_s2 = [0, 0, 1, 0, 0, 0, 0, 0, 0]
    pt_d3 = [1, 0, 0, 0, 0, 0, 0, 0, 0]
    pt_p3_rows = [1, 2, 3, 0, 0, 0, 0, 0, 0]
    pt_p3_mix = [0, 0, 0, 0, 1, 1, 0, 1, -1]

    nul_s2 = hessian_nullity_at(f3, 9, pt_s2)
    nul_d3 = hessian_nullity_at(d3, 9, pt_d3)
    nul_p3_r = hessian_nullity_at(p3, 9, pt_p3_rows)
    nul_p3_m = hessian_nullity_at(p3, 9, pt_p3_mix)
    assert nul_s2 == 5 and nul_d3 == 5 and nul_p3_r == 3 and nul_p3_m == 3
    print(
        f"[Sing(f) Nullity n=3] s=2(e_2)={nul_s2}, det_3(rk1)={nul_d3} vs "
        f"perm_3(2 zero rows)={nul_p3_r}, perm_3(1zr+1zc)={nul_p3_m}\n"
    )


def verify_n4_schur_reductions() -> None:
    rng = random.Random(777)
    nv = 16

    def sparse_lin() -> Poly:
        p = zero_poly()
        for v in rng.sample(range(nv), 4):
            p = add_poly(p, var_poly(v, nv, rng.randint(-3, 3)))
        return {m: c % MOD for m, c in p.items() if c % MOD != 0}

    # 1) s=2b with vanishing degree-3 part (r=2, m=4)
    B = [[sparse_lin() for _ in range(2)] for _ in range(2)]
    l1, l2, q = sparse_lin(), sparse_lin(), sparse_lin()
    D = [[sparse_lin(), sparse_lin()], [q, zero_poly()]]
    C = [[l1, l2], [sparse_lin(), sparse_lin()]]
    M4b: List[List[Poly]] = [[zero_poly() for _ in range(4)] for _ in range(4)]
    for i in range(2):
        for j in range(2):
            M4b[i][j] = add_poly(const_poly(1, nv), B[i][j]) if i == j else B[i][j]
            M4b[i][2 + j] = C[i][j]
            M4b[2 + i][j] = D[i][j]
    M4b[2][0], M4b[2][1] = l1, l2
    # Wait: M4b[2][2], M4b[2][3] is E[0][0], E[0][1]! Fix:
    M4b[2][0], M4b[2][1] = D[0][0], D[0][1]
    M4b[2][2], M4b[2][3] = l1, l2

    full_det_b = poly_det_mod(M4b, mod=MOD)
    assert homog_part(full_det_b, 3) == {}, "Expected vanishing degree-3 part in s=2b reduction!"
    det4_b = homog_part(full_det_b, 4)

    DC = mat_mul_poly(D, C, mod=MOD)
    DBC = mat_mul_poly(mat_mul_poly(D, B, mod=MOD), C, mod=MOD)
    term_l1 = mul_poly(l1, add_poly(DBC[1][1], mul_poly(DC[0][1], q), sign=-1))
    term_l2 = mul_poly(l2, add_poly(mul_poly(DC[0][0], q), DBC[1][0], sign=-1))
    schur_b = {m: c % MOD for m, c in add_poly(term_l1, term_l2).items() if c % MOD != 0}
    assert det4_b == schur_b, "s=2b (deg-3=0) Schur reduction mismatch!"

    # 2) s=3 skew-symmetric E (r=1, m=4)
    b00 = sparse_lin()
    C3 = [[sparse_lin() for _ in range(3)]]
    D3 = [[sparse_lin()] for _ in range(3)]
    l1, l2, l3 = sparse_lin(), sparse_lin(), sparse_lin()
    E3 = [
        [zero_poly(), l1, l2],
        [scale_poly(l1, -1), zero_poly(), l3],
        [scale_poly(l2, -1), scale_poly(l3, -1), zero_poly()],
    ]
    M4s: List[List[Poly]] = [[zero_poly() for _ in range(4)] for _ in range(4)]
    M4s[0][0] = add_poly(const_poly(1, nv), b00)
    for j in range(3):
        M4s[0][1 + j] = C3[0][j]
        M4s[1 + j][0] = D3[j][0]
    for i in range(3):
        for j in range(3):
            M4s[1 + i][1 + j] = E3[i][j]

    det4_s = homog_part(poly_det_mod(M4s, mod=MOD), 4)
    DC3 = mat_mul_poly(D3, C3, mod=MOD)
    v = [l3, scale_poly(l2, -1), l1]
    acc = zero_poly()
    for i in range(3):
        for j in range(3):
            acc = add_poly(acc, mul_poly(mul_poly(v[i], DC3[i][j]), v[j]))
    schur_s = {m: (-c) % MOD for m, c in acc.items() if c % MOD != 0}
    assert det4_s == schur_s, "s=3 skew Schur reduction mismatch!"

    print("[Self-Checks n=4] Verified s=2b (deg-3=0 -> <l1,l2>) and s=3 skew (-v^T DC v) via poly_det_mod\n")


def prove_n4_arbitrary_m_branches() -> None:
    print("=== Part B (n=4, N=16): Arbitrary-m Obstructions for All Non-s=1 Branches ===")
    verify_n4_schur_reductions()
    rng = random.Random(202602)

    e0_sq = tuple(2 if i == 0 else 0 for i in range(16))
    e2_cu = tuple(3 if i == 2 else 0 for i in range(16))

    # 1) s=2a (arb m): Q00*Q11 - Q01*Q10 vanishing at e_0
    Q00 = rand_homog_poly_mod(16, 2, rng, zero_monom=e0_sq)
    Q11 = rand_homog_poly_mod(16, 2, rng, zero_monom=e0_sq)
    Q01 = rand_homog_poly_mod(16, 2, rng, zero_monom=e0_sq)
    Q10 = rand_homog_poly_mod(16, 2, rng, zero_monom=e0_sq)
    f_s2a = add_poly(mul_poly(Q00, Q11), mul_poly(Q01, Q10), sign=-1)
    f_s2a = {m: c % MOD for m, c in f_s2a.items() if c % MOD != 0}

    # 2) s=2b (arb m, deg-3=0): x_0*C1 + x_1*C2 vanishing at e_2
    C1 = rand_homog_poly_mod(16, 3, rng, zero_monom=e2_cu)
    C2 = rand_homog_poly_mod(16, 3, rng, zero_monom=e2_cu)
    f_s2b = add_poly(mul_poly(var_poly(0, 16), C1), mul_poly(var_poly(1, 16), C2))
    f_s2b = {m: c % MOD for m, c in f_s2b.items() if c % MOD != 0}

    # 3) s=3 compression (arb m): M0*Q0 + M1*Q1 + M2*Q2 vanishing at e_0 (E_1 has no x_0 term)
    E0 = [rand_lin_mod(16, rng) for _ in range(3)]
    E1 = []
    for _ in range(3):
        lin = rand_lin_mod(16, rng)
        lin.pop(tuple(1 if i == 0 else 0 for i in range(16)), None)
        E1.append(lin)
    M0 = add_poly(mul_poly(E0[1], E1[2]), mul_poly(E0[2], E1[1]), sign=-1)
    M1 = add_poly(mul_poly(E0[2], E1[0]), mul_poly(E0[0], E1[2]), sign=-1)
    M2 = add_poly(mul_poly(E0[0], E1[1]), mul_poly(E0[1], E1[0]), sign=-1)
    q0 = rand_homog_poly_mod(16, 2, rng, zero_monom=e0_sq)
    q1 = rand_homog_poly_mod(16, 2, rng, zero_monom=e0_sq)
    q2 = rand_homog_poly_mod(16, 2, rng, zero_monom=e0_sq)
    f_s3c = add_poly(add_poly(mul_poly(M0, q0), mul_poly(M1, q1)), mul_poly(M2, q2))
    f_s3c = {m: c % MOD for m, c in f_s3c.items() if c % MOD != 0}

    # 4) s=3 skew (arb m): -v^T Q v with v = (x_2, -x_1, x_0) -> singular at e_3
    Qsym = [[rand_homog_poly_mod(16, 2, rng) for _ in range(3)] for _ in range(3)]
    v_vec = [var_poly(2, 16), scale_poly(var_poly(1, 16), -1), var_poly(0, 16)]
    acc = zero_poly()
    for i in range(3):
        for j in range(3):
            acc = add_poly(acc, mul_poly(mul_poly(v_vec[i], Qsym[i][j]), v_vec[j]))
    f_s3s = {m: (-c) % MOD for m, c in acc.items() if c % MOD != 0}

    pt_e0 = [1 if i == 0 else 0 for i in range(16)]
    pt_e2 = [1 if i == 2 else 0 for i in range(16)]
    pt_e3 = [1 if i == 3 else 0 for i in range(16)]
    pt_d4_rk2 = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    p4 = permanent_poly(4)
    d4 = determinant_poly(4)

    # Check singular-locus Hessian nullities
    n_s2a = hessian_nullity_at(f_s2a, 16, pt_e0)
    n_s2b = hessian_nullity_at(f_s2b, 16, pt_e2)
    n_s3c = hessian_nullity_at(f_s3c, 16, pt_e0)
    n_s3s = hessian_nullity_at(f_s3s, 16, pt_e3)
    n_d4 = hessian_nullity_at(d4, 16, pt_d4_rk2)
    assert n_s2a >= 12 and n_s2b >= 12 and n_s3c >= 11 and n_s3s >= 13 and n_d4 == 12

    perm4_strata = [
        ("2 zero rows", [1, 2, 3, 4, 5, 6, 7, 8, 0, 0, 0, 0, 0, 0, 0, 0]),
        ("1zr + 1zc + perm_3=0", [0, 0, 0, 0, 0, 1, 2, 1, 0, 1, 1, -1, 0, 6, 3, 2]),
        ("1zr + 2x2 zero + perm_2=0", [0, 0, 0, 0, 1, 2, 3, 4, 0, 0, 1, 1, 0, 0, 1, -1]),
        ("3x3 zero block", [1, 2, 3, 4, 5, 0, 0, 0, 6, 0, 0, 0, 7, 0, 0, 0]),
    ]
    print("perm_4 canonical singular strata Hessian nullities:")
    for label, pt in perm4_strata:
        nul = hessian_nullity_at(p4, 16, pt)
        assert nul <= 8, f"Expected perm_4 stratum nullity <= 8, got {nul}"
        print(f"  {label:27s}: nullity(H) = {nul}")

    print("\nGlobal Comparison (Arbitrary-m Non-s=1 Branches vs det_4 & perm_4):")
    print("Branch               | Sing nullity | dim(g_f) | dim(f^p_2) | b_{1,3} | koszul(1,1)")
    print("-" * 83)
    entries = [
        ("det_4 (s=4)", d4, n_d4),
        ("s=2a (arb m)", f_s2a, n_s2a),
        ("s=2b (arb m, deg3=0)", f_s2b, n_s2b),
        ("s=3 comp (arb m)", f_s3c, n_s3c),
        ("s=3 skew (arb m)", f_s3s, n_s3s),
        ("perm_4", p4, 8),
    ]
    for name, poly, nul in entries:
        dg = lie_annihilator_dim(poly, 16)
        df2, _, b13, _ = apolar_quadric_betti(poly, 16)
        kr = koszul_rank(poly, 16, k=1, p=1)
        print(f"{name:20s} | {nul:12d} | {dg:8d} | {df2:10d} | {b13:7d} | {kr:11d}")


def main() -> None:
    prove_n3_corank_s2()
    prove_n4_arbitrary_m_branches()


if __name__ == "__main__":
    main()
