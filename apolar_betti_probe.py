"""GL_N-invariant Lie algebra annihilator dim(g_f) and Macaulay apolar ideal f^perp Betti numbers."""
from __future__ import annotations

import math
import random
from typing import Dict, List, Tuple

import numpy as np

from general_det6_probe import layered_abp_det_split, sum_of_two_det3
from koszul_flattening_probe import recenter_poly_from_mod, substitute_shear_x0_plus_2x1
from multilinear_torus_probe import random_set_multilinear_abp4
from perm4_abp_frontier import MOD, random_abp4_det, rank_mod_numpy
from poly_exact import (
    Poly,
    determinant_poly,
    kth_partial_space,
    mul_poly,
    partial_deriv,
    permanent_poly,
    var_poly,
)


def lie_annihilator_dim(f: Poly, num_vars: int, mod: int = MOD) -> int:
    """Compute dim(g_f) = N^2 - dim(< x_j * d_i f >) over F_mod."""
    partials = [partial_deriv(f, i) for i in range(num_vars)]
    gens: List[Poly] = []
    for j in range(num_vars):
        xj = var_poly(j, num_vars)
        for dp in partials:
            if dp:
                gens.append(mul_poly(xj, dp))
    return num_vars * num_vars - rank_mod_numpy(gens, mod=mod)


def right_nullspace_mod(mat_in: np.ndarray, mod: int = MOD) -> np.ndarray:
    """Return basis rows (nullity x ncols) of the right nullspace of mat_in over F_mod."""
    mat = mat_in.copy() % mod
    n_rows, n_cols = mat.shape
    piv_cols: List[int] = []
    r = 0
    for c in range(n_cols):
        if r >= n_rows:
            break
        nz = np.nonzero(mat[r:, c])[0]
        if len(nz) == 0:
            continue
        piv = r + int(nz[0])
        if piv != r:
            mat[[r, piv]] = mat[[piv, r]]
        inv = pow(int(mat[r, c]), mod - 2, mod)
        mat[r] = (mat[r] * inv) % mod
        all_nz = np.nonzero(mat[:, c])[0]
        all_nz = all_nz[all_nz != r]
        if len(all_nz) > 0:
            factors = mat[all_nz, c][:, None]
            mat[all_nz] = (mat[all_nz] - factors * mat[r][None, :]) % mod
        piv_cols.append(c)
        r += 1

    piv_set = set(piv_cols)
    free_cols = [c for c in range(n_cols) if c not in piv_set]
    basis = np.zeros((len(free_cols), n_cols), dtype=np.int64)
    for idx, fc in enumerate(free_cols):
        basis[idx, fc] = 1
        for row_idx, pc in enumerate(piv_cols):
            val = mat[row_idx, fc]
            if val != 0:
                basis[idx, pc] = (mod - val) % mod
    return basis


def apolar_quadric_betti(f: Poly, num_vars: int, mod: int = MOD) -> Tuple[int, int, int, int]:
    """
    Compute GL_N-invariant Macaulay apolar ideal f^perp invariants at degrees 2 and 3:
      - dim_f2: dim(f^perp_2) = C(N+1, 2) - dim(d^{=2} f)
      - dim_v_f2: dim(V^* . f^perp_2) inside S^3 V^*
      - beta_1_3: dim(f^perp_3) - dim(V^* . f^perp_2)  (minimal cubic generators)
      - beta_2_3: N * dim_f2 - dim(V^* . f^perp_2)    (linear syzygies among quadric annihilators)
    """
    pairs = [(i, j) for i in range(num_vars) for j in range(i, num_vars)]
    m2 = len(pairs)

    # Compute d_i d_j f for each (i, j)
    partials_2: List[Poly] = []
    monom_to_col: Dict[Tuple[int, ...], int] = {}
    for i, j in pairs:
        dij = partial_deriv(partial_deriv(f, i), j)
        dij_mod = {m: c % mod for m, c in dij.items() if c % mod != 0} if dij else {}
        partials_2.append(dij_mod)
        for m in dij_mod:
            if m not in monom_to_col:
                monom_to_col[m] = len(monom_to_col)

    # A has shape (m2, num_monoms); right nullspace of A^T equals left nullspace of A
    n_cols = max(1, len(monom_to_col))
    A = np.zeros((m2, n_cols), dtype=np.int64)
    for r_idx, p2 in enumerate(partials_2):
        for m, c in p2.items():
            A[r_idx, monom_to_col[m]] = c

    null_basis = right_nullspace_mod(A.T, mod=mod)
    dim_f2 = null_basis.shape[0]
    # Verify c^T A == 0 (mod MOD) for all basis vectors
    if dim_f2 > 0:
        check = (null_basis @ A) % mod
        assert not np.any(check), "Nullspace verification c^T A == 0 failed!"

    # Sanity check against dim(d^{=2} f)
    d2_dim = rank_mod_numpy(partials_2, mod=mod)
    assert dim_f2 == m2 - d2_dim, f"dim_f2 mismatch: {dim_f2} != {m2 - d2_dim}"

    # Convert f^perp_2 basis vectors to dual quadrics in y_0..y_{N-1} and shift by y_k
    dual_quadrics: List[Poly] = []
    for row in null_basis:
        q: Poly = {}
        for idx in np.nonzero(row)[0]:
            i, j = pairs[int(idx)]
            exp = [0] * num_vars
            exp[i] += 1
            exp[j] += 1
            q[tuple(exp)] = int(row[idx])
        dual_quadrics.append(q)

    y_vars = [var_poly(k, num_vars) for k in range(num_vars)]
    shifted = [mul_poly(yk, q) for yk in y_vars for q in dual_quadrics]
    dim_v_f2 = rank_mod_numpy(shifted, mod=mod)

    d3_dim = rank_mod_numpy(kth_partial_space(f, num_vars, 3), mod=mod)
    dim_f3 = math.comb(num_vars + 2, 3) - d3_dim
    assert dim_v_f2 <= dim_f3, f"Subspace check failed: {dim_v_f2} > {dim_f3}"

    beta_1_3 = dim_f3 - dim_v_f2
    beta_2_3 = num_vars * dim_f2 - dim_v_f2
    return dim_f2, dim_v_f2, beta_1_3, beta_2_3


def summarize(name: str, poly: Poly, num_vars: int) -> Tuple[int, int, int, int, int]:
    lg = lie_annihilator_dim(poly, num_vars)
    df2, dvf2, b13, b23 = apolar_quadric_betti(poly, num_vars)
    return lg, df2, dvf2, b13, b23


def main() -> None:
    p3 = permanent_poly(3)
    d3 = determinant_poly(3)

    # Built-in checks: exact Lie annihilator dims & GL_N shear invariance
    lg_p3 = lie_annihilator_dim(p3, 9)
    lg_d3 = lie_annihilator_dim(d3, 9)
    assert lg_p3 == 4, f"Expected dim(g_perm3)=4, got {lg_p3}"
    assert lg_d3 == 16, f"Expected dim(g_det3)=16, got {lg_d3}"

    orig_stats = summarize("perm_3", p3, 9)
    shear_stats = summarize("perm_3_sheared", substitute_shear_x0_plus_2x1(p3, 9), 9)
    assert orig_stats == shear_stats, f"GL_N shear invariance failed: {orig_stats} != {shear_stats}"
    print(f"[Self-Checks] dim(g_perm3)={lg_p3}, dim(g_det3)={lg_d3}, GL_N shear invariance={orig_stats} (OK)\n")

    rng = random.Random(123)
    n3_models = [
        ("det_3", d3),
        ("m=4 (1,2)", recenter_poly_from_mod(layered_abp_det_split(1, 2, 9, rng))),
        ("m=5 (2,2)", recenter_poly_from_mod(layered_abp_det_split(2, 2, 9, rng))),
        ("m=6 (1,4)", recenter_poly_from_mod(layered_abp_det_split(1, 4, 9, rng))),
        ("m=6 (2,3)", recenter_poly_from_mod(layered_abp_det_split(2, 3, 9, rng))),
        ("perm_3", p3),
        ("m=7 (3,3)", recenter_poly_from_mod(layered_abp_det_split(3, 3, 9, rng))),
        ("det_3 + det_3", recenter_poly_from_mod(sum_of_two_det3(9, rng))),
    ]

    print("=== n=3 (N=9, d=3) Lie Annihilator & Macaulay Apolar Ideal f^perp ===")
    print("Model           | dim(g_f) | dim(f^perp_2) | dim(V*f^p_2) | beta_{1,3} | beta_{2,3}")
    print("-" * 82)
    for name, poly in n3_models:
        lg, df2, dvf2, b13, b23 = summarize(name, poly, 9)
        print(f"{name:15s} | {lg:8d} | {df2:13d} | {dvf2:12d} | {b13:10d} | {b23:10d}")

    p4 = permanent_poly(4)
    d4 = determinant_poly(4)
    rng4 = random.Random(2026)
    n4_models = [
        ("det_4", d4),
        ("Set-ML m=8 (2,3,2)", random_set_multilinear_abp4(2, 3, 2, rng4)),
        ("Set-ML m=10 (3,3,3)", random_set_multilinear_abp4(3, 3, 3, rng4)),
        ("Set-ML m=12 (3,5,3)", random_set_multilinear_abp4(3, 5, 3, rng4)),
        ("Set-ML m=15 (4,6,4)", random_set_multilinear_abp4(4, 6, 4, rng4)),
        ("Gen ABP m=9 (2,4,2)", random_abp4_det(2, 4, 2, 16, rng4)),
        ("Gen ABP m=10 (3,3,3)", random_abp4_det(3, 3, 3, 16, rng4)),
        ("perm_4", p4),
    ]

    print("\n=== n=4 (N=16, d=4) Lie Annihilator & Macaulay Apolar Ideal f^perp ===")
    print("Model                 | dim(g_f) | dim(f^perp_2) | dim(V*f^p_2) | beta_{1,3} | beta_{2,3}")
    print("-" * 88)
    for name, poly in n4_models:
        lg, df2, dvf2, b13, b23 = summarize(name, poly, 16)
        print(f"{name:21s} | {lg:8d} | {df2:13d} | {dvf2:12d} | {b13:10d} | {b23:10d}")


if __name__ == "__main__":
    main()
