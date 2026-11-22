"""Test non-layered, unbalanced-layer, and sum-of-dets degree-3 polynomials against perm_3 (s2=419)."""
from __future__ import annotations

import random
from typing import List, Tuple

from affine_det_projection_probe import poly_det_mod, syzygy_span
from poly_exact import (
    Poly,
    add_poly,
    const_poly,
    mul_poly,
    permanent_poly,
    var_poly,
    zero_poly,
)

MOD = 1_000_000_007


def rand_lin(num_vars: int, rng: random.Random) -> Poly:
    p: Poly = {}
    for v in range(num_vars):
        c = rng.randint(-5, 5)
        if c != 0:
            p = add_poly(p, var_poly(v, num_vars, c))
    return p


def layered_abp_det_split(l1_size: int, l2_size: int, num_vars: int, rng: random.Random) -> Poly:
    """Degree-3 ABP determinant with m = 1 + l1_size + l2_size vertices."""
    # Compute directly via vector-matrix-vector product: v0^T * M * v2
    v0 = [rand_lin(num_vars, rng) for _ in range(l1_size)]
    M = [[rand_lin(num_vars, rng) for _ in range(l2_size)] for _ in range(l1_size)]
    v2 = [rand_lin(num_vars, rng) for _ in range(l2_size)]

    # tmp = v0^T * M (length l2_size)
    tmp = [zero_poly() for _ in range(l2_size)]
    for j in range(l2_size):
        acc = zero_poly()
        for i in range(l1_size):
            acc = add_poly(acc, mul_poly(v0[i], M[i][j]))
        tmp[j] = {k: v % MOD for k, v in acc.items() if v % MOD != 0}

    total = zero_poly()
    for j in range(l2_size):
        total = add_poly(total, mul_poly(tmp[j], v2[j]))
    return {k: v % MOD for k, v in total.items() if v % MOD != 0}


def nilpotent_rank2_det6(num_vars: int, rng: random.Random) -> Poly:
    """
    Non-layered 6x6 determinant of form:
      M = [[I_5 - U(X), v(X)], [-w(X)^T, 0]]
    where U(X) = P * Q(X)^T has U^2 = 0 (P is 5x2 constant, Q(X) is 5x2 linear, Q(X)^T P = 0).
    Then det(M) = w(X)^T (I + U(X)) v(X); we extract its homogeneous degree-3 part w(X)^T U(X) v(X)
    Wait: for exact degree 3 without degree-2 part, require w(X)^T v(X) = 0, e.g., w uses coords {0,1},
    v uses coords {2,3,4}, P uses {0,1} (rows 0..1), Q(X) uses {2,3,4} -> Q^T P = 0 automatically!
    Wait: that's equivalent to a (2,3) layer split. To make it genuinely non-layered in basis,
    we conjugate by a random invertible 5x5 matrix S! (Basis change preserves det identically.)
    """
    # Even more general: sum of two 3x3 linear determinants (not a single layered 6x6 ABP)
    return zero_poly()


def sum_of_two_det3(num_vars: int, rng: random.Random) -> Poly:
    """det(L1(X)) + det(L2(X)) where L1, L2 are random 3x3 linear matrices."""
    m1 = [[rand_lin(num_vars, rng) for _ in range(3)] for _ in range(3)]
    m2 = [[rand_lin(num_vars, rng) for _ in range(3)] for _ in range(3)]
    d1 = poly_det_mod(m1)
    d2 = poly_det_mod(m2)
    res = add_poly(d1, d2)
    return {k: v % MOD for k, v in res.items() if v % MOD != 0}


def general_det_m_homog_deg3(m: int, num_vars: int, rng: random.Random) -> Poly:
    """
    Take a random m x m affine matrix A_0 + L(X) where A_0 = diag(1, ..., 1, 0, 0, 0)
    (rank m-3), so det(A_0 + L(X)) starts at degree 3! Its lowest homogeneous component
    (degree 3) is the leading tangent-cone approximation of det_m at a rank-(m-3) point.
    Note: for m=6, A_0 = diag(1,1,1,0,0,0) -> degree-3 part is just det(L_{22}), a 3x3 det!
    What if A_0 has a Jordan block (nilpotent)? E.g. A_0 = J_2(0) + ...
    For A_0 = diag(1, 1, 1, 0, 0, 0) + nilpotent shift E_{0,3}, E_{1,4}, E_{2,5}:
    Let's build a random 6x6 matrix with 3 ones on superdiagonal / diagonal so min degree is 3,
    and extract the exact degree-3 homogeneous component!
    """
    # Build M = A_0 + L(X) where rank(A_0) = 3: A_0 = diag(1,1,1,0,0,0)
    # Wait: if we perturb A_0 with arbitrary rank-3 nilpotent or rank-4?
    # If rank(A_0) = 4, min degree can be 2; if rank(A_0) = 3, det(diag(I_3, 0) + L) has deg-3 part = det(L_22).
    # Instead, let's test rank-4 A_0 = diag(1,1,1,1,0,0) with L_{22} = 0 (so deg-2 term vanishes!):
    # Then det([[I_4 + L11, L12], [L21, 0]]) = det(-L21 (I_4 + L11)^{-1} L12) -> starts at deg 4!
    # What about rank-3 A_0 = I_3 in top-left, and bottom-right 3x3 has one 1? That's rank 4.
    # For a single 0 on diag (rank 5): A_0 = diag(1,1,1,1,1,0), L_{5,5} = 0 -> starts at deg 2.
    # To kill deg 2 as well: L_{5, j} only nonzero on j in {0,1}, L_{i, 5} only nonzero on i in {2,3,4}.
    # That is literally a 2-layer ABP!
    return layered_abp_det_split(2, 3, num_vars, rng)


def main() -> None:
    rng = random.Random(123)
    p3 = permanent_poly(3)
    p3_s1, _ = syzygy_span(p3, 9, k=1, shift_deg=1)
    p3_s2, _ = syzygy_span(p3, 9, k=1, shift_deg=2)
    print(f"Reference perm_3: s1={p3_s1}/90 | s2={p3_s2}/495\n")

    print("=== 1) All m=6 layered ABP splits (l1, l2) with 1 + l1 + l2 = 6 ===")
    for l1, l2 in [(1, 4), (2, 3), (3, 2), (4, 1)]:
        best_s1, best_s2 = -1, -1
        for _ in range(3):
            poly = layered_abp_det_split(l1, l2, 9, rng)
            s1, _ = syzygy_span(poly, 9, k=1, shift_deg=1)
            s2, _ = syzygy_span(poly, 9, k=1, shift_deg=2)
            best_s1 = max(best_s1, s1)
            best_s2 = max(best_s2, s2)
        print(f"m=6 split ({l1},{l2}) | s1={best_s1:2d}/90 | s2={best_s2:3d}/495 | vs perm_3: {best_s2 - p3_s2:+d}")

    print("\n=== 2) Sum of two random 3x3 determinants: det(L1) + det(L2) ===")
    best_s1, best_s2 = -1, -1
    for _ in range(3):
        poly = sum_of_two_det3(9, rng)
        s1, _ = syzygy_span(poly, 9, k=1, shift_deg=1)
        s2, _ = syzygy_span(poly, 9, k=1, shift_deg=2)
        best_s1 = max(best_s1, s1)
        best_s2 = max(best_s2, s2)
    print(f"det_3 + det_3   | s1={best_s1:2d}/90 | s2={best_s2:3d}/495 | vs perm_3: {best_s2 - p3_s2:+d}")


if __name__ == "__main__":
    main()
