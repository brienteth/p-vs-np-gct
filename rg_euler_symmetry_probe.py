"""RG / MPS entanglement cut-rank spectrum and Euler characteristic conservation probe."""
from __future__ import annotations

import random
from typing import Dict, List, Set, Tuple

import numpy as np

from ancilla_immanant_probe import grenet_perm4_subset_mask, immanant_poly_4
from apolar_higher_betti_probe import apolar_betti_deg4_torus, rank_matrix_mod
from corank_schur_n4_probe import torus_s2a_det2_dc_m10
from multilinear_torus_probe import random_set_multilinear_abp4
from padding_betti_probe import apolar_betti_deg4_torus_padded
from perm4_abp_frontier import MOD, random_abp4_det
from perm_n_betti_scaling import apolar_betti_deg4_orbit
from poly_exact import Poly, determinant_poly, permanent_poly


def bipartition_cut_rank(f: Poly, subset_a: Set[int], num_vars: int = 16, mod: int = MOD) -> int:
    """
    Exact RG / MPS entanglement cut-rank on the degree (2, 2) bipartition across subset_a | complement.
    Lower semicontinuous one-way monotone under degeneration.
    """
    a_idx = sorted(subset_a)
    b_idx = [i for i in range(num_vars) if i not in subset_a]

    row_to_i: Dict[Tuple[int, ...], int] = {}
    col_to_j: Dict[Tuple[int, ...], int] = {}
    entries: List[Tuple[int, int, int]] = []

    for m, coeff in f.items():
        if sum(m) != 4:
            continue
        deg_a = sum(m[i] for i in a_idx)
        if deg_a != 2:
            continue
        c = coeff % mod
        if c == 0:
            continue
        ma = tuple(m[i] for i in a_idx)
        mb = tuple(m[j] for j in b_idx)
        ri = row_to_i.get(ma)
        if ri is None:
            ri = len(row_to_i)
            row_to_i[ma] = ri
        cj = col_to_j.get(mb)
        if cj is None:
            cj = len(col_to_j)
            col_to_j[mb] = cj
        entries.append((ri, cj, c))

    if not entries:
        return 0
    mat = np.zeros((len(row_to_i), len(col_to_j)), dtype=np.int64)
    for ri, cj, c in entries:
        mat[ri, cj] = (mat[ri, cj] + c) % mod
    return rank_matrix_mod(mat, mod=mod)


def run_euler_conservation() -> None:
    print("=== Part A: Alternating-Sum / Euler Characteristic Conservation chi_4 = b34 - b24 + b14 ===")
    print("Model              | b_{1,4} | b_{2,4} | b_{3,4} | chi_4 = b34 - b24 + b14")
    print("-" * 74)

    p3, d3 = permanent_poly(3), determinant_poly(3)
    p4, d4 = permanent_poly(4), determinant_poly(4)
    p5, d5 = permanent_poly(5), determinant_poly(5)

    entries: List[Tuple[str, Tuple[int, int, int, int, int, int]]] = [
        ("det_3", apolar_betti_deg4_orbit(d3, 3)[0]),
        ("perm_3", apolar_betti_deg4_orbit(p3, 3)[0]),
        ("det_4", apolar_betti_deg4_orbit(d4, 4)[0]),
        ("perm_4", apolar_betti_deg4_orbit(p4, 4)[0]),
        ("torus s=2a m=10", apolar_betti_deg4_torus(torus_s2a_det2_dc_m10(), 4)[0]),
        ("Grenet_14", apolar_betti_deg4_torus(grenet_perm4_subset_mask({(0, 1)}), 4)[0]),
        ("imm_(2,2)", apolar_betti_deg4_torus(immanant_poly_4("(2,2)"), 4)[0]),
        ("z^1 * det_4", apolar_betti_deg4_torus_padded(d4, 4, 1)[0]),
        ("z^1 * perm_4", apolar_betti_deg4_torus_padded(p4, 4, 1)[0]),
        ("z^2 * det_4", apolar_betti_deg4_torus_padded(d4, 4, 2)[0]),
        ("z^2 * perm_4", apolar_betti_deg4_torus_padded(p4, 4, 2)[0]),
        ("det_5", apolar_betti_deg4_orbit(d5, 5)[0]),
        ("perm_5", apolar_betti_deg4_orbit(p5, 5)[0]),
    ]
    chi_map: Dict[str, int] = {}
    for name, (_, _, _, b14, b24, b34) in entries:
        chi4 = b34 - b24 + b14
        chi_map[name] = chi4
        print(f"{name:18s} | {b14:7d} | {b24:7d} | {b34:7d} | {chi4:23d}")

    assert chi_map["det_3"] == chi_map["perm_3"] == 315
    assert chi_map["det_4"] == chi_map["perm_4"] == chi_map["torus s=2a m=10"] == 3075
    assert chi_map["z^1 * det_4"] == chi_map["z^1 * perm_4"] == 2975
    assert chi_map["z^2 * det_4"] == chi_map["z^2 * perm_4"] == 3092
    assert chi_map["det_5"] == chi_map["perm_5"] == 17325
    print("[Verified] chi_4 is strictly conserved across identical deg 2..3 Hilbert profiles.\n")


def run_rg_cut_spectrum() -> None:
    print("=== Part B (n=4): RG / MPS Entanglement Cut-Rank Spectrum (One-Way Monotone) ===")
    row_splits = [
        {r * 4 + c for r in (0, 1) for c in range(4)},
        {r * 4 + c for r in (0, 2) for c in range(4)},
        {r * 4 + c for r in (0, 3) for c in range(4)},
    ]
    col_splits = [
        {r * 4 + c for r in range(4) for c in (0, 1)},
        {r * 4 + c for r in range(4) for c in (0, 2)},
        {r * 4 + c for r in range(4) for c in (0, 3)},
    ]
    block_diag_split = {
        r * 4 + c for r in range(4) for c in range(4) if (r < 2 and c < 2) or (r >= 2 and c >= 2)
    }
    checker_split = {r * 4 + c for r in range(4) for c in range(4) if (r + c) % 2 == 0}

    rng = random.Random(202612)
    models: List[Tuple[str, Poly, int]] = [
        ("det_4", determinant_poly(4), 0),
        ("perm_4", permanent_poly(4), 0),
        ("Grenet_12 (drop 3)", grenet_perm4_subset_mask({(0, 1), (1, 2), (2, 3)}), 0),
        ("Grenet_13 (drop 2)", grenet_perm4_subset_mask({(0, 1), (2, 3)}), 0),
        ("Grenet_14 (drop 1)", grenet_perm4_subset_mask({(0, 1)}), 0),
        ("Set-ML m=8  (2,3,2)", random_set_multilinear_abp4(2, 3, 2, rng), 3),
        ("Set-ML m=10 (3,3,3)", random_set_multilinear_abp4(3, 3, 3, rng), 3),
        ("Set-ML m=12 (3,5,3)", random_set_multilinear_abp4(3, 5, 3, rng), 5),
        ("Set-ML m=14 (4,5,4)", random_set_multilinear_abp4(4, 5, 4, rng), 5),
        ("Set-ML m=15 (4,6,4)", random_set_multilinear_abp4(4, 6, 4, rng), 6),
        ("Gen ABP m=7  (2,2,2)", random_abp4_det(2, 2, 2, 16, rng), 0),
        ("Gen ABP m=10 (3,3,3)", random_abp4_det(3, 3, 3, 16, rng), 0),
        ("Gen ABP m=12 (4,3,4)", random_abp4_det(4, 3, 4, 16, rng), 0),
        ("Gen ABP m=13 (4,4,4)", random_abp4_det(4, 4, 4, 16, rng), 0),
        ("Gen ABP m=15 (4,6,4)", random_abp4_det(4, 6, 4, 16, rng), 0),
    ]

    print(
        "Model                | row_cuts (01|02|03) | col_cuts (01|02|03) | blk_diag | checker"
    )
    print("-" * 86)
    for name, poly, w2_setml in models:
        rc = [bipartition_cut_rank(poly, s) for s in row_splits]
        cc = [bipartition_cut_rank(poly, s) for s in col_splits]
        bd = bipartition_cut_rank(poly, block_diag_split)
        ch = bipartition_cut_rank(poly, checker_split)
        if w2_setml > 0:
            assert rc[0] <= w2_setml, f"Nisan cut-rank violated: {rc[0]} > {w2_setml}"
        rc_str = f"{rc[0]:2d}, {rc[1]:2d}, {rc[2]:2d}"
        cc_str = f"{cc[0]:2d}, {cc[1]:2d}, {cc[2]:2d}"
        print(f"{name:20s} | {rc_str:19s} | {cc_str:19s} | {bd:8d} | {ch:7d}")


def main() -> None:
    run_euler_conservation()
    run_rg_cut_spectrum()


if __name__ == "__main__":
    main()
