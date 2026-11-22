"""Mignon-Ressayre Hessian rank probe for perm_n, det_n, and Grenet_7x7."""
from __future__ import annotations

from typing import List, Sequence, Tuple

from grenet_verify import grenet_matrix_perm3
from poly_exact import (
    Poly,
    determinant_poly,
    partial_deriv,
    permanent_poly,
    poly_det,
)

MOD = 1_000_000_007


def eval_poly_mod(p: Poly, point: Sequence[int], mod: int = MOD) -> int:
    total = 0
    for monom, coeff in p.items():
        term = coeff % mod
        for var_i, exp in enumerate(monom):
            if exp:
                term = (term * pow(point[var_i], exp, mod)) % mod
        total = (total + term) % mod
    return total


def matrix_rank_mod(rows: List[List[int]], mod: int = MOD) -> int:
    if not rows:
        return 0
    m = len(rows)
    n = len(rows[0])
    mat = [[v % mod for v in r] for r in rows]
    rank = 0
    for col in range(n):
        pivot = None
        for r in range(rank, m):
            if mat[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col], mod - 2, mod)
        for r in range(rank + 1, m):
            if mat[r][col] != 0:
                factor = (mat[r][col] * inv) % mod
                for c in range(col, n):
                    mat[r][c] = (mat[r][c] - factor * mat[rank][c]) % mod
        rank += 1
    return rank


def nullspace_basis_mod(vec: List[int], mod: int = MOD) -> List[List[int]]:
    """Basis of ker(vec^T) in F_mod^N."""
    n = len(vec)
    piv = next((i for i, v in enumerate(vec) if v % mod != 0), None)
    if piv is None:
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    inv_piv = pow(vec[piv], mod - 2, mod)
    basis: List[List[int]] = []
    for j in range(n):
        if j == piv:
            continue
        b = [0] * n
        b[j] = 1
        b[piv] = (-vec[j] * inv_piv) % mod
        basis.append(b)
    return basis


def hessian_and_tangent_rank(p: Poly, num_vars: int, point: Sequence[int]) -> Tuple[int, int, int]:
    """Return (f(pt), rank(H_f(pt)), rank(H_f(pt)|_{ker grad f}))."""
    val = eval_poly_mod(p, point)
    partials = [partial_deriv(p, i) for i in range(num_vars)]
    grad = [eval_poly_mod(dp, point) for dp in partials]
    hess = [
        [eval_poly_mod(partial_deriv(partials[i], j), point) for j in range(num_vars)]
        for i in range(num_vars)
    ]
    h_rank = matrix_rank_mod(hess)

    basis = nullspace_basis_mod(grad)
    # Compute B * H * B^T where rows of B form basis of ker(grad)
    bh = []
    for b in basis:
        row = [sum(b[k] * hess[k][j] for k in range(num_vars)) % MOD for j in range(num_vars)]
        bh.append(row)
    bhbt = []
    for row in bh:
        bhbt.append([sum(row[k] * b2[k] for k in range(num_vars)) % MOD for b2 in basis])
    tangent_rank = matrix_rank_mod(bhbt)
    return val, h_rank, tangent_rank


def main() -> None:
    print("Model | Point type | f(X0) | rank(H) | rank(H|_ker(grad))")
    print("-" * 62)

    # n = 3: compare perm_3, det_3, and Grenet_7x7 at a zero point
    p3 = permanent_poly(3)
    d3 = determinant_poly(3)
    g3 = poly_det(grenet_matrix_perm3(), 9)

    # Zero of perm_3: [[1, 1, 1], [1, -1, 0], [0, 1, -1]] -> perm = 1*1 + 1*(-1) + ... let's check:
    # Actually let's use [[1, 0, 0], [0, 1, 1], [0, 1, -1]] -> perm = 1*(1*(-1)+1*1) = 0, det = 1*(-1-1) = -2
    pt_perm_zero = [1, 0, 0, 0, 1, 1, 0, 1, -1]
    # Zero of det_3: [[1, 0, 0], [0, 1, 1], [0, 1, 1]] -> det = 0, perm = 2
    pt_det_zero = [1, 0, 0, 0, 1, 1, 0, 1, 1]
    # Generic point
    pt_gen = [1, 2, 3, 4, 5, 6, 7, 8, 10]

    for name, poly, pt_label, pt in [
        ("perm_3", p3, "perm=0", pt_perm_zero),
        ("Grenet_7x7", g3, "perm=0", pt_perm_zero),
        ("det_3", d3, "det=0", pt_det_zero),
        ("perm_3", p3, "generic", pt_gen),
        ("det_3", d3, "generic", pt_gen),
    ]:
        val, hr, tr = hessian_and_tangent_rank(poly, 9, pt)
        print(f"{name:10s} | {pt_label:10s} | {val:5d} | {hr:7d} | {tr:18d}")

    # n = 4: compare perm_4 and det_4 at a zero point vs generic point
    p4 = permanent_poly(4)
    d4 = determinant_poly(4)
    # Zero of perm_4: block diag [[1,1],[1,-1]] x [[1,0],[0,1]] -> perm = 0
    pt4_p0 = [1, 1, 0, 0, 1, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    # Zero of det_4: block diag [[1,1],[1,1]] x [[1,0],[0,1]] -> det = 0
    pt4_d0 = [1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    for name, poly, pt_label, pt in [
        ("perm_4", p4, "perm=0", pt4_p0),
        ("det_4", d4, "det=0", pt4_d0),
    ]:
        val, hr, tr = hessian_and_tangent_rank(poly, 16, pt)
        print(f"{name:10s} | {pt_label:10s} | {val:5d} | {hr:7d} | {tr:18d}")


if __name__ == "__main__":
    main()
