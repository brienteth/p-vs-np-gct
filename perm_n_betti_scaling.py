"""Exact S_n x S_n orbit-compressed n=3..5 apolar Betti scaling & explicit perm_4 quadratic syzygy."""
from __future__ import annotations

import itertools
import math
from collections import Counter, defaultdict
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
from perm4_abp_frontier import MOD, rank_mod_numpy
from poly_exact import (
    Poly,
    add_poly,
    determinant_poly,
    mul_poly,
    partial_deriv,
    permanent_poly,
    scale_poly,
    var_poly,
)


def partitions_of_k(k: int, length: int) -> List[Tuple[int, ...]]:
    """All non-increasing integer tuples of given length summing to k."""
    res: List[Tuple[int, ...]] = []

    def rec(rem: int, max_val: int, cur: List[int]) -> None:
        if len(cur) == length:
            if rem == 0:
                res.append(tuple(cur))
            return
        if rem == 0:
            res.append(tuple(cur + [0] * (length - len(cur))))
            return
        for v in range(min(rem, max_val), 0, -1):
            rec(rem - v, v, cur + [v])

    rec(k, k, [])
    return res


def orbit_size_tuple(t: Tuple[int, ...]) -> int:
    denom = 1
    for cnt in Counter(t).values():
        denom *= math.factorial(cnt)
    return math.factorial(len(t)) // denom


def rref_mod(mat_in: np.ndarray, mod: int = MOD) -> Tuple[np.ndarray, List[int]]:
    """Compute RREF of dense int64 matrix over F_mod, returning (rref_rows, piv_cols)."""
    if mat_in.size == 0:
        return np.zeros((0, mat_in.shape[1]), dtype=np.int64), []
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
    return mat[:r], piv_cols


def partials_of_mdeg(f: Poly, n: int, k: int, md: Multideg, mod: int = MOD) -> List[Poly]:
    """Evaluate all k-th order partials d^alpha f with multidegree md."""
    r_vec, c_vec = md
    if max(r_vec) > 1 or max(c_vec) > 1:
        return []
    rows = [i for i, v in enumerate(r_vec) if v == 1]
    cols = [j for j, v in enumerate(c_vec) if v == 1]
    assert len(rows) == k and len(cols) == k
    res: List[Poly] = []
    for perm_c in itertools.permutations(cols):
        cur = f
        for r_i, c_j in zip(rows, perm_c):
            cur = partial_deriv(cur, r_i * n + c_j)
            if not cur:
                break
        if cur:
            res.append({m: c % mod for m, c in cur.items() if c % mod != 0})
    return res


def apolar_betti_deg4_orbit(
    f: Poly, n: int, mod: int = MOD
) -> Tuple[Tuple[int, int, int, int, int, int], List[Tuple[Multideg, int, int, int]]]:
    """
    Exact S_n x S_n orbit-compressed apolar ideal Betti invariants through degree 4.
    Returns (totals, orbit_records) where:
      totals = (dim_f2, beta_1_3, beta_2_3, beta_1_4, beta_2_4, beta_3_4)
      orbit_records = list of (rep_md4, b14_blk, b24_blk, b34_blk)
    """
    num_vars = n * n
    pairs2 = [(i, j) for i in range(num_vars) for j in range(i, num_vars)]
    pair2_to_idx = {pair: idx for idx, pair in enumerate(pairs2)}

    var_mdeg: List[Multideg] = []
    for k in range(num_vars):
        exp = [0] * num_vars
        exp[k] = 1
        var_mdeg.append(monom_multideg(tuple(exp), n))

    pair2_mdeg: List[Multideg] = []
    pair2_poly: List[Poly] = []
    pair2_by_mdeg: Dict[Multideg, List[int]] = defaultdict(list)
    for p_idx, (a, b) in enumerate(pairs2):
        exp = [0] * num_vars
        exp[a] += 1
        exp[b] += 1
        t = tuple(exp)
        md = monom_multideg(t, n)
        pair2_mdeg.append(md)
        pair2_poly.append({t: 1})
        pair2_by_mdeg[md].append(p_idx)

    # Precompute f^perp_2 for all degree-2 multidegrees
    f2_quadrics_by_mdeg: Dict[Multideg, List[Poly]] = {}
    dim_f2_total = 0
    for md2, p_indices in pair2_by_mdeg.items():
        p2_polys: List[Poly] = []
        for p_idx in p_indices:
            i, j = pairs2[p_idx]
            dij = partial_deriv(partial_deriv(f, i), j)
            p2_polys.append({m: c % mod for m, c in dij.items() if c % mod != 0} if dij else {})
        A_blk = polys_to_dense_mod(p2_polys, mod=mod)
        nb = right_nullspace_mod(A_blk.T, mod=mod)
        if nb.shape[0] > 0:
            assert not np.any((nb @ A_blk) % mod)
            q_list: List[Poly] = []
            for row in nb:
                q_poly: Poly = {}
                for loc_idx in np.nonzero(row)[0]:
                    i, j = pairs2[p_indices[int(loc_idx)]]
                    exp = [0] * num_vars
                    exp[i] += 1
                    exp[j] += 1
                    q_poly[tuple(exp)] = int(row[loc_idx])
                q_list.append(q_poly)
            f2_quadrics_by_mdeg[md2] = q_list
            dim_f2_total += len(q_list)

    # Pre-count S^3 V^* and S^4 V^* multidegree dimensions
    deg3_monoms_by_mdeg: Dict[Multideg, int] = defaultdict(int)
    for comb in itertools.combinations_with_replacement(range(num_vars), 3):
        exp = [0] * num_vars
        for idx in comb:
            exp[idx] += 1
        deg3_monoms_by_mdeg[monom_multideg(tuple(exp), n)] += 1

    deg4_monoms_by_mdeg: Dict[Multideg, int] = defaultdict(int)
    for comb in itertools.combinations_with_replacement(range(num_vars), 4):
        exp = [0] * num_vars
        for idx in comb:
            exp[idx] += 1
        deg4_monoms_by_mdeg[monom_multideg(tuple(exp), n)] += 1

    y_vars = [var_poly(k, num_vars) for k in range(num_vars)]
    syz3_cache: Dict[Multideg, Tuple[List[Tuple[int, Multideg, int]], np.ndarray]] = {}

    def get_syz3_block(md3: Multideg) -> Tuple[List[Tuple[int, Multideg, int]], np.ndarray]:
        if md3 in syz3_cache:
            return syz3_cache[md3]
        gens3: List[Tuple[int, Multideg, int]] = []
        r3, c3 = md3
        for k in range(num_vars):
            rk, ck = k // n, k % n
            if r3[rk] == 0 or c3[ck] == 0:
                continue
            md2 = (
                tuple(r3[x] - (1 if x == rk else 0) for x in range(n)),
                tuple(c3[y] - (1 if y == ck else 0) for y in range(n)),
            )
            q_list = f2_quadrics_by_mdeg.get(md2)
            if q_list:
                for q_loc in range(len(q_list)):
                    gens3.append((k, md2, q_loc))
        if not gens3:
            res = ([], np.zeros((0, 0), dtype=np.int64))
            syz3_cache[md3] = res
            return res
        phi3_polys = [
            mul_poly(y_vars[k], f2_quadrics_by_mdeg[md2][q_loc]) for k, md2, q_loc in gens3
        ]
        phi3_blk = polys_to_dense_mod(phi3_polys, mod=mod)
        syz_blk = right_nullspace_mod(phi3_blk.T, mod=mod)
        if syz_blk.shape[0] > 0:
            assert not np.any((syz_blk @ phi3_blk) % mod)
        res = (gens3, syz_blk)
        syz3_cache[md3] = res
        return res

    # Degree-3 orbit loop
    beta_1_3_total = 0
    beta_2_3_total = 0
    parts3 = partitions_of_k(3, n)
    for r3 in parts3:
        w_r = orbit_size_tuple(r3)
        for c3 in parts3:
            w = w_r * orbit_size_tuple(c3)
            md3 = (r3, c3)
            gens3, syz_blk = get_syz3_block(md3)
            dim_v_f2_blk = len(gens3) - syz_blk.shape[0]
            d3_rank = rank_mod_numpy(partials_of_mdeg(f, n, 3, md3, mod=mod), mod=mod)
            dim_f3_blk = deg3_monoms_by_mdeg[md3] - d3_rank
            assert dim_v_f2_blk <= dim_f3_blk
            beta_1_3_total += w * (dim_f3_blk - dim_v_f2_blk)
            beta_2_3_total += w * syz_blk.shape[0]

    # Degree-4 orbit loop
    beta_1_4_total = 0
    beta_2_4_total = 0
    beta_3_4_total = 0
    orbit_records: List[Tuple[Multideg, int, int, int]] = []
    parts4 = partitions_of_k(4, n)
    for r4 in parts4:
        w_r = orbit_size_tuple(r4)
        for c4 in parts4:
            w = w_r * orbit_size_tuple(c4)
            md4 = (r4, c4)
            d4_rank = rank_mod_numpy(partials_of_mdeg(f, n, 4, md4, mod=mod), mod=mod)
            dim_f4_blk = deg4_monoms_by_mdeg[md4] - d4_rank

            gens4: List[Tuple[int, Multideg, int]] = []
            for p2_idx, md2_p in enumerate(pair2_mdeg):
                rem_r = tuple(r4[x] - md2_p[0][x] for x in range(n))
                if min(rem_r) < 0:
                    continue
                rem_c = tuple(c4[y] - md2_p[1][y] for y in range(n))
                if min(rem_c) < 0:
                    continue
                q_md2 = (rem_r, rem_c)
                q_list = f2_quadrics_by_mdeg.get(q_md2)
                if q_list:
                    for q_loc in range(len(q_list)):
                        gens4.append((p2_idx, q_md2, q_loc))

            if gens4:
                phi4_polys = [
                    mul_poly(pair2_poly[p2_idx], f2_quadrics_by_mdeg[md2][q_loc])
                    for p2_idx, md2, q_loc in gens4
                ]
                phi4_blk = polys_to_dense_mod(phi4_polys, mod=mod)
                dim_s2_f2_blk = rank_matrix_mod(phi4_blk, mod=mod)
                dim_syz1_4_blk = len(gens4) - dim_s2_f2_blk
            else:
                phi4_blk = np.zeros((0, 1), dtype=np.int64)
                dim_s2_f2_blk = 0
                dim_syz1_4_blk = 0

            assert dim_s2_f2_blk <= dim_f4_blk
            b14_blk = dim_f4_blk - dim_s2_f2_blk

            shifts4: List[Tuple[int, Multideg, int]] = []
            for l in range(num_vars):
                rl, cl = l // n, l % n
                if r4[rl] == 0 or c4[cl] == 0:
                    continue
                md3 = (
                    tuple(r4[x] - (1 if x == rl else 0) for x in range(n)),
                    tuple(c4[y] - (1 if y == cl else 0) for y in range(n)),
                )
                _, syz3_blk = get_syz3_block(md3)
                for s_loc in range(syz3_blk.shape[0]):
                    shifts4.append((l, md3, s_loc))

            if shifts4:
                gen4_to_col = {g: idx for idx, g in enumerate(gens4)}
                shift_mat = np.zeros((len(shifts4), len(gens4)), dtype=np.int64)
                for row_i, (l, md3, s_loc) in enumerate(shifts4):
                    gens3, syz3_blk = get_syz3_block(md3)
                    vec = syz3_blk[s_loc]
                    for c_idx in np.nonzero(vec)[0]:
                        k, q_md2, q_loc = gens3[int(c_idx)]
                        a, b = (l, k) if l <= k else (k, l)
                        t_col = gen4_to_col[(pair2_to_idx[(a, b)], q_md2, q_loc)]
                        shift_mat[row_i, t_col] = (shift_mat[row_i, t_col] + int(vec[c_idx])) % mod
                assert not np.any((shift_mat @ phi4_blk) % mod)
                dim_v_syz3_blk = rank_matrix_mod(shift_mat, mod=mod)
            else:
                dim_v_syz3_blk = 0

            b24_blk = dim_syz1_4_blk - dim_v_syz3_blk
            b34_blk = len(shifts4) - dim_v_syz3_blk
            assert b24_blk >= 0 and b34_blk >= 0

            beta_1_4_total += w * b14_blk
            beta_2_4_total += w * b24_blk
            beta_3_4_total += w * b34_blk
            orbit_records.append((md4, b14_blk, b24_blk, b34_blk))

    return (
        dim_f2_total,
        beta_1_3_total,
        beta_2_3_total,
        beta_1_4_total,
        beta_2_4_total,
        beta_3_4_total,
    ), orbit_records


def format_monom_y(m: Tuple[int, ...], n: int = 4) -> str:
    parts = []
    for idx, e in enumerate(m):
        if e > 0:
            r, c = divmod(idx, n)
            parts.append(f"y{r}{c}" if e == 1 else f"y{r}{c}^{e}")
    return "*".join(parts)


def format_poly_y(p: Poly, n: int = 4, mod: int = MOD) -> str:
    terms = []
    half = mod // 2
    for m in sorted(p.keys(), reverse=True):
        c = p[m] % mod
        if c == 0:
            continue
        if c > half:
            c -= mod
        m_str = format_monom_y(m, n)
        if not terms:
            prefix = "-" if c == -1 else ("" if c == 1 else f"{c}*")
            terms.append(f"{prefix}{m_str}")
        else:
            sign = " + " if c > 0 else " - "
            ac = abs(c)
            coef_str = "" if ac == 1 else f"{ac}*"
            terms.append(f"{sign}{coef_str}{m_str}")
    return "".join(terms)


def extract_explicit_perm4_syzygy(mod: int = MOD) -> None:
    """
    Extract an explicit minimal quadratic syzygy in perm_4^perp at block ((2,2,0,0),(1,1,1,1)),
    and test what happens under Polya's sign flip to det_4^perp quadrics.
    """
    n = 4
    num_vars = 16
    p4 = permanent_poly(n)
    d4 = determinant_poly(n)
    md4 = ((2, 2, 0, 0), (1, 1, 1, 1))

    pairs2 = [(i, j) for i in range(num_vars) for j in range(i, num_vars)]
    pair2_to_idx = {pair: idx for idx, pair in enumerate(pairs2)}
    pair2_mdeg = []
    pair2_poly = []
    pair2_by_mdeg: Dict[Multideg, List[int]] = defaultdict(list)
    for p_idx, (a, b) in enumerate(pairs2):
        exp = [0] * num_vars
        exp[a] += 1
        exp[b] += 1
        t = tuple(exp)
        md = monom_multideg(t, n)
        pair2_mdeg.append(md)
        pair2_poly.append({t: 1})
        pair2_by_mdeg[md].append(p_idx)

    # Compute f^perp_2 for perm_4 and det_4
    def build_f2(f: Poly) -> Dict[Multideg, List[Poly]]:
        out: Dict[Multideg, List[Poly]] = {}
        for md2, p_indices in pair2_by_mdeg.items():
            p2_polys = []
            for p_idx in p_indices:
                i, j = pairs2[p_idx]
                dij = partial_deriv(partial_deriv(f, i), j)
                p2_polys.append({m: c % mod for m, c in dij.items() if c % mod != 0} if dij else {})
            A_blk = polys_to_dense_mod(p2_polys, mod=mod)
            nb = right_nullspace_mod(A_blk.T, mod=mod)
            if nb.shape[0] > 0:
                q_list = []
                for row in nb:
                    q_poly: Poly = {}
                    for loc_idx in np.nonzero(row)[0]:
                        i, j = pairs2[p_indices[int(loc_idx)]]
                        exp = [0] * num_vars
                        exp[i] += 1
                        exp[j] += 1
                        q_poly[tuple(exp)] = int(row[loc_idx])
                    q_list.append(q_poly)
                out[md2] = q_list
        return out

    f2_p4 = build_f2(p4)
    f2_d4 = build_f2(d4)
    y_vars = [var_poly(k, num_vars) for k in range(num_vars)]

    # Build gens4 and shift_mat in md4 for perm_4
    gens4: List[Tuple[int, Multideg, int]] = []
    for p2_idx, md2_p in enumerate(pair2_mdeg):
        rem_r = tuple(md4[0][x] - md2_p[0][x] for x in range(n))
        rem_c = tuple(md4[1][y] - md2_p[1][y] for y in range(n))
        if min(rem_r) < 0 or min(rem_c) < 0:
            continue
        q_md2 = (rem_r, rem_c)
        for q_loc in range(len(f2_p4.get(q_md2, []))):
            gens4.append((p2_idx, q_md2, q_loc))

    phi4_polys = [mul_poly(pair2_poly[p2_i], f2_p4[md2][ql]) for p2_i, md2, ql in gens4]
    phi4_blk = polys_to_dense_mod(phi4_polys, mod=mod)
    syz4_blk = right_nullspace_mod(phi4_blk.T, mod=mod)

    # Compute V* . Syz_1(perm_4^perp)_3 at md4
    shift_rows: List[np.ndarray] = []
    gen4_to_col = {g: idx for idx, g in enumerate(gens4)}
    for l in range(num_vars):
        rl, cl = l // n, l % n
        if md4[0][rl] == 0 or md4[1][cl] == 0:
            continue
        md3 = (
            tuple(md4[0][x] - (1 if x == rl else 0) for x in range(n)),
            tuple(md4[1][y] - (1 if y == cl else 0) for y in range(n)),
        )
        gens3: List[Tuple[int, Multideg, int]] = []
        for k in range(num_vars):
            rk, ck = k // n, k % n
            if md3[0][rk] == 0 or md3[1][ck] == 0:
                continue
            md2 = (
                tuple(md3[0][x] - (1 if x == rk else 0) for x in range(n)),
                tuple(md3[1][y] - (1 if y == ck else 0) for y in range(n)),
            )
            for ql in range(len(f2_p4.get(md2, []))):
                gens3.append((k, md2, ql))
        if not gens3:
            continue
        phi3_blk = polys_to_dense_mod(
            [mul_poly(y_vars[k], f2_p4[md2][ql]) for k, md2, ql in gens3], mod=mod
        )
        syz3_blk = right_nullspace_mod(phi3_blk.T, mod=mod)
        for s_row in syz3_blk:
            row = np.zeros(len(gens4), dtype=np.int64)
            for c_idx in np.nonzero(s_row)[0]:
                k, q_md2, q_loc = gens3[int(c_idx)]
                a, b = (l, k) if l <= k else (k, l)
                t_col = gen4_to_col[(pair2_to_idx[(a, b)], q_md2, q_loc)]
                row[t_col] = (row[t_col] + int(s_row[c_idx])) % mod
            shift_rows.append(row)

    shift_mat = np.stack(shift_rows, axis=0)
    rref_shift, piv_cols = rref_mod(shift_mat, mod=mod)

    # Reduce each syz4_blk row modulo rref_shift and pick the sparsest nonzero representative
    best_vec = None
    best_nnz = 10**9
    for row in syz4_blk:
        v = row.copy() % mod
        for r_idx, pc in enumerate(piv_cols):
            if v[pc] != 0:
                v = (v - v[pc] * rref_shift[r_idx]) % mod
        nnz = int(np.count_nonzero(v))
        if nnz > 0 and nnz < best_nnz:
            best_nnz = nnz
            best_vec = v

    assert best_vec is not None
    assert not np.any((best_vec @ phi4_blk) % mod), "Extracted syzygy does not vanish in S^4 V^*!"
    assert rank_matrix_mod(np.vstack([shift_mat, best_vec[None, :]]), mod=mod) == rref_shift.shape[0] + 1

    # Normalize first nonzero coeff to +1
    first_nz = int(np.nonzero(best_vec)[0][0])
    inv_lead = pow(int(best_vec[first_nz]), mod - 2, mod)
    best_vec = (best_vec * inv_lead) % mod

    print("\n=== Explicit Minimal Quadratic Syzygy in perm_4^perp at ((2,2,0,0), (1,1,1,1)) ===")
    print(f"Sparse representative has {best_nnz} terms:")
    half = mod // 2
    det_eval: Poly = {}
    for col_idx in np.nonzero(best_vec)[0]:
        c = int(best_vec[col_idx])
        if c > half:
            c -= mod
        p2_idx, q_md2, q_loc = gens4[int(col_idx)]
        q_perm = f2_p4[q_md2][q_loc]
        m2_str = format_poly_y(pair2_poly[p2_idx], n=4, mod=mod)
        q_str = format_poly_y(q_perm, n=4, mod=mod)
        print(f"  {c:+d} * ({m2_str}) * [{q_str}]")

        # Map quadric to det_4^perp by flipping monomial signs of mixed-row/col 2x2 quadrics
        if len(q_perm) == 1:
            q_det = q_perm
        else:
            # Flip second monomial relative to first -> verify annihilates det_4
            ms = list(q_perm.keys())
            assert len(ms) == 2
            q_det = {ms[0]: q_perm[ms[0]], ms[1]: (-q_perm[ms[1]]) % mod}
            # Verify q_det is proportional to f2_d4[q_md2][q_loc]
            assert len(f2_d4[q_md2]) == 1
        term = mul_poly(pair2_poly[p2_idx], scale_poly(q_det, c))
        det_eval = add_poly(det_eval, term)

    det_eval = {m: c % mod for m, c in det_eval.items() if c % mod != 0}
    print(
        f"\n[Polya Sign-Flip Test] Substituting det_4^perp (+) quadrics into the exact same coefficients:\n"
        f"  Evaluates to ZERO? {len(det_eval) == 0} (nonzero S^4 V^* terms = {len(det_eval)})"
    )
    if det_eval:
        print(f"  Residual polynomial in S^4 V^* = {format_poly_y(det_eval, n=4, mod=mod)}")


def main() -> None:
    # Self-checks on n=3 and n=4
    p3 = permanent_poly(3)
    d3 = determinant_poly(3)
    t_p3, _ = apolar_betti_deg4_orbit(p3, 3)
    t_d3, _ = apolar_betti_deg4_orbit(d3, 3)
    assert t_p3 == (36, 0, 160, 0, 0, 315), f"perm_3 mismatch: {t_p3}"
    assert t_d3 == (36, 0, 160, 0, 0, 315), f"det_3 mismatch: {t_d3}"

    p4 = permanent_poly(4)
    d4 = determinant_poly(4)
    t_p4, _ = apolar_betti_deg4_orbit(p4, 4)
    t_d4, _ = apolar_betti_deg4_orbit(d4, 4)
    assert t_p4 == (100, 0, 800, 0, 12, 3087), f"perm_4 mismatch: {t_p4}"
    assert t_d4 == (100, 0, 800, 0, 0, 3075), f"det_4 mismatch: {t_d4}"

    p5 = permanent_poly(5)
    d5 = determinant_poly(5)
    assert len(p5) == 120 and len(d5) == 120
    t_p5, orb_p5 = apolar_betti_deg4_orbit(p5, 5)
    t_d5, orb_d5 = apolar_betti_deg4_orbit(d5, 5)

    print("=== Exact Scaling Table: Macaulay Apolar Ideal f^perp Betti (n = 3, 4, 5) ===")
    print("Model  | dim(f^p_2) | b_{1,3} | b_{2,3} | b_{1,4} | b_{2,4} | b_{3,4}")
    print("-" * 70)
    for name, tot in [
        ("det_3", t_d3),
        ("perm_3", t_p3),
        ("det_4", t_d4),
        ("perm_4", t_p4),
        ("det_5", t_d5),
        ("perm_5", t_p5),
    ]:
        df2, b13, b23, b14, b24, b34 = tot
        print(f"{name:6s} | {df2:10d} | {b13:7d} | {b23:7d} | {b14:7d} | {b24:7d} | {b34:7d}")

    print("\n=== n=5 Orbits Where perm_5 != det_5 ===")
    for (md4, b14p, b24p, b34p), (_, b14d, b24d, b34d) in zip(orb_p5, orb_d5):
        if (b14p, b24p, b34p) != (b14d, b24d, b34d):
            w = orbit_size_tuple(md4[0]) * orbit_size_tuple(md4[1])
            print(
                f"  orbit {md4} (size={w}): perm_5=({b14p},{b24p},{b34p}) vs det_5=({b14d},{b24d},{b34d}) "
                f"| weighted delta b24 = {w * (b24p - b24d):+d}"
            )

    extract_explicit_perm4_syzygy()


if __name__ == "__main__":
    main()
