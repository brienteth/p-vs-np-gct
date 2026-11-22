"""Exact S_3 x S_3 irreducible representation decomposition of shifted PD spaces for perm_3 vs det_3."""
from __future__ import annotations

import itertools
from typing import Dict, List, Tuple

import numpy as np

from poly_exact import (
    Poly,
    determinant_poly,
    kth_partial_space,
    mul_poly,
    permanent_poly,
)
from shifted_pd_probe import monomials_of_degree_le

MOD = 1_000_003


def perm_cycle_type(p: Tuple[int, ...]) -> Tuple[int, ...]:
    n = len(p)
    seen = [False] * n
    cycles = []
    for i in range(n):
        if not seen[i]:
            cur = i
            length = 0
            while not seen[cur]:
                seen[cur] = True
                cur = p[cur]
                length += 1
            cycles.append(length)
    return tuple(sorted(cycles, reverse=True))


# Irreducible characters of S_3 indexed by cycle type: (1,1,1), (2,1), (3,)
S3_CHARS: Dict[str, Tuple[int, Dict[Tuple[int, ...], int]]] = {
    "(3) triv": (1, {(1, 1, 1): 1, (2, 1): 1, (3,): 1}),
    "(2,1) std": (2, {(1, 1, 1): 2, (2, 1): 0, (3,): -1}),
    "(1,1,1) sgn": (1, {(1, 1, 1): 1, (2, 1): -1, (3,): 1}),
}


def act_poly_s3xs3(p: Poly, row_perm: Tuple[int, ...], col_perm: Tuple[int, ...]) -> Poly:
    """Apply (row_perm, col_perm) in S_3 x S_3 to variables x_{i,j} -> x_{row_perm[i], col_perm[j]}."""
    res: Poly = {}
    for m, c in p.items():
        new_m = [0] * 9
        for i in range(3):
            ri = row_perm[i]
            for j in range(3):
                e = m[i * 3 + j]
                if e:
                    new_m[ri * 3 + col_perm[j]] = e
        res[tuple(new_m)] = c
    return res


def basis_mod_p(polys: List[Poly], mod: int = MOD) -> Tuple[np.ndarray, Dict[Tuple[int, ...], int]]:
    """Return an RREF basis matrix (rank x num_monoms) over F_mod and monomial->col map."""
    monom_to_col: Dict[Tuple[int, ...], int] = {}
    for p in polys:
        for m in p:
            if m not in monom_to_col:
                monom_to_col[m] = len(monom_to_col)
    n_cols = len(monom_to_col)
    mat = np.zeros((len(polys), n_cols), dtype=np.int64)
    for i, p in enumerate(polys):
        for m, c in p.items():
            mat[i, monom_to_col[m]] = c % mod

    rank = 0
    piv_cols: List[int] = []
    for col in range(n_cols):
        if rank >= mat.shape[0]:
            break
        nz = np.nonzero(mat[rank:, col])[0]
        if len(nz) == 0:
            continue
        piv = rank + int(nz[0])
        if piv != rank:
            mat[[rank, piv]] = mat[[piv, rank]]
        inv = pow(int(mat[rank, col]), mod - 2, mod)
        mat[rank] = (mat[rank] * inv) % mod
        # Eliminate both above and below for clean RREF
        all_nz = np.nonzero(mat[:, col])[0]
        all_nz = all_nz[all_nz != rank]
        if len(all_nz) > 0:
            factors = mat[all_nz, col][:, None]
            mat[all_nz] = (mat[all_nz] - factors * mat[rank][None, :]) % mod
        piv_cols.append(col)
        rank += 1
    return mat[:rank], monom_to_col


def compute_s3xs3_multiplicities(p: Poly, k: int, shift_deg: int) -> Tuple[int, Dict[Tuple[str, str], int]]:
    """
    Compute exact character chi_V(g) = Tr(g|_V) for representatives of all 9 conjugacy classes
    of S_3 x S_3, then extract exact irreducible multiplicities by inner product!
    """
    partials = kth_partial_space(p, 9, k)
    shifts = monomials_of_degree_le(9, shift_deg)
    gens = [mul_poly(s, d) for s in shifts for d in partials]

    basis, monom_to_col = basis_mod_p(gens)
    dim_v = basis.shape[0]
    col_to_monom = [None] * len(monom_to_col)
    for m, c in monom_to_col.items():
        col_to_monom[c] = m

    # Find pivot column of each RREF basis row so extracting coordinates in basis is O(1) per row!
    piv_cols = [int(np.nonzero(basis[r])[0][0]) for r in range(dim_v)]

    # Representatives and sizes of the 3 conjugacy classes of S_3
    s3_classes = [
        ((0, 1, 2), (1, 1, 1), 1),
        ((1, 0, 2), (2, 1), 3),
        ((1, 2, 0), (3,), 2),
    ]

    # Preconvert each basis vector back to Poly for fast group action
    basis_polys: List[Poly] = []
    for r in range(dim_v):
        poly_r: Poly = {}
        nz = np.nonzero(basis[r])[0]
        for c in nz:
            poly_r[col_to_monom[int(c)]] = int(basis[r, c])
        basis_polys.append(poly_r)

    # Trace of (g1, g2) on V: Tr(g|_V) = sum_r (g(b_r) evaluated at piv_cols[r])!
    # Wait: since basis is in RREF, for any vector v in V, its coordinate along b_r is simply v[piv_cols[r]]!
    traces: Dict[Tuple[Tuple[int, ...], Tuple[int, ...]], int] = {}
    for g1, ct1, _ in s3_classes:
        for g2, ct2, _ in s3_classes:
            tr = 0
            for r in range(dim_v):
                acted = act_poly_s3xs3(basis_polys[r], g1, g2)
                piv_m = col_to_monom[piv_cols[r]]
                tr = (tr + acted.get(piv_m, 0)) % MOD
            # Convert from mod p to signed small integer (since |Tr| <= dim_v << MOD/2)
            if tr > MOD // 2:
                tr -= MOD
            traces[(ct1, ct2)] = tr

    # Compute multiplicities: m_{lam, mu} = (1/36) * sum |C1|*|C2| * chi_lam(C1) * chi_mu(C2) * Tr(C1, C2)
    mults: Dict[Tuple[str, str], int] = {}
    for name1, (_, ch1) in S3_CHARS.items():
        for name2, (_, ch2) in S3_CHARS.items():
            total = 0
            for _, ct1, sz1 in s3_classes:
                for _, ct2, sz2 in s3_classes:
                    total += sz1 * sz2 * ch1[ct1] * ch2[ct2] * traces[(ct1, ct2)]
            assert total % 36 == 0, f"Non-integer multiplicity: {total}/36"
            mults[(name1, name2)] = total // 36

    return dim_v, mults


def main() -> None:
    p3 = permanent_poly(3)
    d3 = determinant_poly(3)

    for k, s in [(1, 1), (1, 2)]:
        dp, mp = compute_s3xs3_multiplicities(p3, k, s)
        dd, md = compute_s3xs3_multiplicities(d3, k, s)
        print(f"=== S_3 x S_3 Irreducible Decomposition: k={k}, shift={s} (perm={dp}, det={dd}) ===")
        print(f"{'Irrep (row x col)':26s} | dim | perm_3 | det_3 | gap (perm - det)")
        print("-" * 68)
        for name1, (dim1, _) in S3_CHARS.items():
            for name2, (dim2, _) in S3_CHARS.items():
                vp = mp[(name1, name2)]
                vd = md[(name1, name2)]
                label = f"{name1} x {name2}"
                print(f"{label:26s} | {dim1*dim2:3d} | {vp:6d} | {vd:5d} | {vp - vd:+d}")
        print()


if __name__ == "__main__":
    main()
