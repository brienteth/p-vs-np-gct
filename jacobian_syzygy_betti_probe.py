"""Exact GL_N-invariant Jacobian ideal J(f) syzygy Betti invariants at linear and quadratic order."""
from __future__ import annotations

import itertools
import random
from collections import defaultdict
from typing import Dict, List, Tuple

import numpy as np

from apolar_betti_probe import right_nullspace_mod
from apolar_higher_betti_probe import (
    Multideg,
    add_mdeg,
    monom_multideg,
    polys_to_dense_mod,
    rank_matrix_mod,
)
from general_det6_probe import layered_abp_det_split, sum_of_two_det3
from koszul_flattening_probe import recenter_poly_from_mod, substitute_shear_x0_plus_2x1
from perm4_abp_frontier import MOD
from poly_exact import (
    Poly,
    determinant_poly,
    mul_poly,
    partial_deriv,
    permanent_poly,
    var_poly,
)


def jacobian_syzygy_ungraded(
    f: Poly, num_vars: int, mod: int = MOD
) -> Tuple[int, int, int, int, int]:
    """
    Compute ungraded Jacobian ideal J(f) = <d_0 f, ..., d_{N-1} f> syzygies for deg(f)=3:
      (dim_g, dim_syz2, beta_2_4_J, beta_2_4_extra, beta_3_4_J).
    """
    partials = [
        {m: c % mod for m, c in partial_deriv(f, i).items() if c % mod != 0}
        for i in range(num_vars)
    ]
    x_vars = [var_poly(j, num_vars) for j in range(num_vars)]

    # 1) psi_1: V \otimes V^* -> S^d V (j * N + i -> x_j * d_i f)
    psi1_polys = [mul_poly(x_vars[j], partials[i]) for j in range(num_vars) for i in range(num_vars)]
    psi1_mat = polys_to_dense_mod(psi1_polys, mod=mod)
    syz1_basis = right_nullspace_mod(psi1_mat.T, mod=mod)
    dim_g = syz1_basis.shape[0]
    if dim_g > 0:
        assert not np.any((syz1_basis @ psi1_mat) % mod), "Lie annihilator kernel check failed"

    # 2) psi_2: S^2 V \otimes V^* -> S^{d+1} V
    pairs2 = [(a, b) for a in range(num_vars) for b in range(a, num_vars)]
    pair2_to_idx = {pair: idx for idx, pair in enumerate(pairs2)}
    m2 = len(pairs2)

    x_quads = []
    for a, b in pairs2:
        exp = [0] * num_vars
        exp[a] += 1
        exp[b] += 1
        x_quads.append({tuple(exp): 1})

    psi2_polys = [mul_poly(x_quads[p2_i], partials[i]) for p2_i in range(m2) for i in range(num_vars)]
    psi2_mat = polys_to_dense_mod(psi2_polys, mod=mod)
    dim_j2 = rank_matrix_mod(psi2_mat, mod=mod)
    dim_syz2 = m2 * num_vars - dim_j2

    # 3) Shifted Lie annihilators V * g_f inside S^2 V \otimes V^*
    shifted_g = np.zeros((num_vars * dim_g, m2 * num_vars), dtype=np.int64)
    for s_idx in range(dim_g):
        nz_cols = np.nonzero(syz1_basis[s_idx])[0]
        for l in range(num_vars):
            row_idx = l * dim_g + s_idx
            for c_idx in nz_cols:
                j, i = divmod(int(c_idx), num_vars)
                a, b = (l, j) if l <= j else (j, l)
                t_col = pair2_to_idx[(a, b)] * num_vars + i
                shifted_g[row_idx, t_col] = (
                    shifted_g[row_idx, t_col] + int(syz1_basis[s_idx, c_idx])
                ) % mod

    if shifted_g.shape[0] > 0:
        assert not np.any((shifted_g @ psi2_mat) % mod), "Shifted g_f not in ker(psi_2)"
    dim_v_g = rank_matrix_mod(shifted_g, mod=mod)
    beta_2_4_J = dim_syz2 - dim_v_g
    beta_3_4_J = num_vars * dim_g - dim_v_g

    # 4) Universal quadratic Koszul syzygies (d_j f) e_i - (d_i f) e_j (only when deg(f) == 3)
    koszul_rows: List[np.ndarray] = []
    for i in range(num_vars):
        for j in range(i + 1, num_vars):
            row = np.zeros(m2 * num_vars, dtype=np.int64)
            for m, c in partials[j].items():
                assert sum(m) == 2, "Koszul degree-2 syzygy requires deg(d_j f) == 2"
                nz = [idx for idx, e in enumerate(m) if e > 0]
                a, b = (nz[0], nz[0]) if len(nz) == 1 else (nz[0], nz[1])
                t_col = pair2_to_idx[(a, b)] * num_vars + i
                row[t_col] = (row[t_col] + c) % mod
            for m, c in partials[i].items():
                assert sum(m) == 2, "Koszul degree-2 syzygy requires deg(d_i f) == 2"
                nz = [idx for idx, e in enumerate(m) if e > 0]
                a, b = (nz[0], nz[0]) if len(nz) == 1 else (nz[0], nz[1])
                t_col = pair2_to_idx[(a, b)] * num_vars + j
                row[t_col] = (row[t_col] - c) % mod
            koszul_rows.append(row)

    koszul_mat = np.stack(koszul_rows, axis=0)
    assert not np.any((koszul_mat @ psi2_mat) % mod), "Koszul syzygy not in ker(psi_2)"
    stacked = np.vstack([shifted_g, koszul_mat]) if shifted_g.shape[0] > 0 else koszul_mat
    dim_expected = rank_matrix_mod(stacked, mod=mod)
    beta_2_4_extra = dim_syz2 - dim_expected
    assert beta_2_4_extra >= 0

    return dim_g, dim_syz2, beta_2_4_J, beta_2_4_extra, beta_3_4_J


def jacobian_syzygy_torus(
    f: Poly, n: int, mod: int = MOD
) -> Tuple[Tuple[int, int, int, int, int], Dict[Multideg, Tuple[int, int, int]]]:
    """
    Exact torus-multigraded Jacobian ideal syzygy invariants at linear & quadratic order
    for bihomogeneous polynomials (perm_n, det_n).
    Returns:
      totals = (dim_g, dim_syz2, dim_v_g, beta_2_4_J, beta_3_4_J)
      block_stats[mdeg2] = (dim_syz2_blk, beta_2_4_J_blk, beta_3_4_J_blk)
    """
    num_vars = n * n
    full_mdeg = ((1,) * n, (1,) * n)

    var_mdeg: List[Multideg] = []
    for k in range(num_vars):
        exp = [0] * num_vars
        exp[k] = 1
        var_mdeg.append(monom_multideg(tuple(exp), n))

    partials: List[Poly] = []
    partial_mdeg: List[Multideg] = []
    for i in range(num_vars):
        dp = {m: c % mod for m, c in partial_deriv(f, i).items() if c % mod != 0}
        partials.append(dp)
        vm = var_mdeg[i]
        partial_mdeg.append((
            tuple(x - y for x, y in zip(full_mdeg[0], vm[0])),
            tuple(x - y for x, y in zip(full_mdeg[1], vm[1])),
        ))

    x_vars = [var_poly(j, num_vars) for j in range(num_vars)]

    # 1) Blockwise psi_1 and g_f
    gens1_by_mdeg: Dict[Multideg, List[Tuple[int, int]]] = defaultdict(list)
    for j in range(num_vars):
        for i in range(num_vars):
            md1 = add_mdeg(var_mdeg[j], partial_mdeg[i])
            gens1_by_mdeg[md1].append((j, i))

    syz1_by_mdeg: Dict[Multideg, Tuple[List[Tuple[int, int]], np.ndarray]] = {}
    dim_g_total = 0
    for md1, gens1 in gens1_by_mdeg.items():
        psi1_polys = [mul_poly(x_vars[j], partials[i]) for j, i in gens1]
        psi1_blk = polys_to_dense_mod(psi1_polys, mod=mod)
        syz_blk = right_nullspace_mod(psi1_blk.T, mod=mod)
        if syz_blk.shape[0] > 0:
            assert not np.any((syz_blk @ psi1_blk) % mod)
            syz1_by_mdeg[md1] = (gens1, syz_blk)
            dim_g_total += syz_blk.shape[0]

    # 2) Blockwise psi_2 and V * g_f
    pairs2 = [(a, b) for a in range(num_vars) for b in range(a, num_vars)]
    pair2_to_idx = {pair: idx for idx, pair in enumerate(pairs2)}
    pair2_mdeg: List[Multideg] = []
    pair2_poly: List[Poly] = []
    for a, b in pairs2:
        exp = [0] * num_vars
        exp[a] += 1
        exp[b] += 1
        t = tuple(exp)
        pair2_mdeg.append(monom_multideg(t, n))
        pair2_poly.append({t: 1})

    gens2_by_mdeg: Dict[Multideg, List[Tuple[int, int]]] = defaultdict(list)
    for p2_idx in range(len(pairs2)):
        for i in range(num_vars):
            md2 = add_mdeg(pair2_mdeg[p2_idx], partial_mdeg[i])
            gens2_by_mdeg[md2].append((p2_idx, i))

    shifted1_by_mdeg: Dict[Multideg, List[Tuple[int, Multideg, int]]] = defaultdict(list)
    for md1, (_, syz_blk) in syz1_by_mdeg.items():
        for s_loc in range(syz_blk.shape[0]):
            for l in range(num_vars):
                md2 = add_mdeg(var_mdeg[l], md1)
                shifted1_by_mdeg[md2].append((l, md1, s_loc))

    dim_syz2_total = 0
    dim_v_g_total = 0
    beta_2_4_J_total = 0
    beta_3_4_J_total = 0
    block_stats: Dict[Multideg, Tuple[int, int, int]] = {}

    for md2, gens2 in gens2_by_mdeg.items():
        psi2_polys = [mul_poly(pair2_poly[p2_idx], partials[i]) for p2_idx, i in gens2]
        psi2_blk = polys_to_dense_mod(psi2_polys, mod=mod)
        dim_j2_blk = rank_matrix_mod(psi2_blk, mod=mod)
        dim_syz2_blk = len(gens2) - dim_j2_blk

        shifts2 = shifted1_by_mdeg.get(md2, [])
        if shifts2:
            gen2_to_col = {g: idx for idx, g in enumerate(gens2)}
            shift_mat = np.zeros((len(shifts2), len(gens2)), dtype=np.int64)
            for row_i, (l, md1, s_loc) in enumerate(shifts2):
                gens1, syz_blk = syz1_by_mdeg[md1]
                vec = syz_blk[s_loc]
                for c_idx in np.nonzero(vec)[0]:
                    j, i = gens1[int(c_idx)]
                    a, b = (l, j) if l <= j else (j, l)
                    t_col = gen2_to_col[(pair2_to_idx[(a, b)], i)]
                    shift_mat[row_i, t_col] = (shift_mat[row_i, t_col] + int(vec[c_idx])) % mod
            assert not np.any((shift_mat @ psi2_blk) % mod), f"Shifted g_f failed ker check at {md2}"
            dim_v_g_blk = rank_matrix_mod(shift_mat, mod=mod)
        else:
            dim_v_g_blk = 0

        b24_blk = dim_syz2_blk - dim_v_g_blk
        b34_blk = len(shifts2) - dim_v_g_blk
        assert b24_blk >= 0 and b34_blk >= 0

        dim_syz2_total += dim_syz2_blk
        dim_v_g_total += dim_v_g_blk
        beta_2_4_J_total += b24_blk
        beta_3_4_J_total += b34_blk
        block_stats[md2] = (dim_syz2_blk, b24_blk, b34_blk)

    totals = (dim_g_total, dim_syz2_total, dim_v_g_total, beta_2_4_J_total, beta_3_4_J_total)
    return totals, block_stats


def main() -> None:
    p3 = permanent_poly(3)
    d3 = determinant_poly(3)

    # Self-check 1: GL_9 shear invariance
    j_orig = jacobian_syzygy_ungraded(p3, 9)
    j_shear = jacobian_syzygy_ungraded(substitute_shear_x0_plus_2x1(p3, 9), 9)
    assert j_orig == j_shear, f"GL_9 shear invariance failed: {j_orig} != {j_shear}"

    # Self-check 2: n=3 ungraded vs torus cross-check
    j_d3 = jacobian_syzygy_ungraded(d3, 9)
    t_p3, _ = jacobian_syzygy_torus(p3, 3)
    t_d3, _ = jacobian_syzygy_torus(d3, 3)
    # Match (dim_g, dim_syz2, beta_2_4_J, beta_3_4_J)
    assert (j_orig[0], j_orig[1], j_orig[2], j_orig[4]) == (t_p3[0], t_p3[1], t_p3[3], t_p3[4])
    assert (j_d3[0], j_d3[1], j_d3[2], j_d3[4]) == (t_d3[0], t_d3[1], t_d3[3], t_d3[4])
    print(f"[Self-Checks] GL_9 shear invariance={j_orig}; torus cross-check perm_3 & det_3 OK\n")

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

    print("=== n=3 (N=9, d=3) Jacobian Ideal J(f) Syzygy Invariants (deg 1..2) ===")
    print("Model           | dim(g_f) | dim(Syz2) | b_{2,4}^J | b_{2,4}^extra | b_{3,4}^J")
    print("-" * 77)
    for name, poly in n3_models:
        dg, s2, b24, b24x, b34 = jacobian_syzygy_ungraded(poly, 9)
        print(f"{name:15s} | {dg:8d} | {s2:9d} | {b24:9d} | {b24x:13d} | {b34:9d}")

    p4 = permanent_poly(4)
    d4 = determinant_poly(4)
    tot_p4, blk_p4 = jacobian_syzygy_torus(p4, 4)
    tot_d4, blk_d4 = jacobian_syzygy_torus(d4, 4)

    print("\n=== n=4 (N=16, d=4) Jacobian Ideal J(f) Syzygy Invariants (deg 1..2) ===")
    print("Model   | dim(g_f) | dim(Syz2) | dim(V*g_f) | b_{2,5}^J | b_{3,5}^J")
    print("-" * 71)
    for name, tot in [("det_4", tot_d4), ("perm_4", tot_p4)]:
        dg, s2, dvg, b25, b35 = tot
        print(f"{name:7s} | {dg:8d} | {s2:9d} | {dvg:10d} | {b25:9d} | {b35:9d}")

    diffs = []
    for md2 in sorted(set(blk_p4.keys()) | set(blk_d4.keys())):
        vp = blk_p4.get(md2, (0, 0, 0))
        vd = blk_d4.get(md2, (0, 0, 0))
        if vp != vd:
            diffs.append((abs(vp[1] - vd[1]) + abs(vp[2] - vd[2]), md2, vp, vd))
    diffs.sort(reverse=True)
    print(f"\nMultidegree blocks where perm_4 != det_4 in (Syz2, b25_J, b35_J): {len(diffs)}")
    for _, md2, vp, vd in diffs[:15]:
        print(f"  mdeg={md2}: perm_4={vp} vs det_4={vd}")


if __name__ == "__main__":
    main()
