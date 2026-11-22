"""Prof. Wigner Round 12 — Node E5.2:
(A) TC^0 Depth-2 Forster Sign-Rank, Spectral Discrepancy, and Nuclear/Margin Norm
    across THREE balanced 256x256 variable cuts of {0,1}^{4x4}:
    1. Row-Cut (rows {0,1} vs {2,3})
    2. Checkerboard Cut ((i+j)%2 == 0 vs 1 — completely non-row-separated!)
    3. Block-Diagonal vs Off-Diagonal 2x2 Cut (non-row-separated!)
(B) Exact Scaling to n = 5 (ALL 2^{25} = 33,554,432 matrices in {0,1}^{5x5} with ZERO sampling error!)
    via exact S_5 x S_5 Orbit Compression (K_5 = 5,624 orbits):
    - Exact value distribution of |det_5| and perm_5 across all 33,554,432 matrices
    - Exact degree-n `det_n mod 2` (`= perm_n mod 2`) Hamming approximation error
      for [det_n != 0 mod 3] (P) vs [perm_n != 0 mod 3] (Mod_3 P) across n = 2, 3, 4, 5
    - Exact Total Influence I(f), sensitivity distribution (min, mean, max, s0, s1),
      and Walsh correlations across all 33,554,432 matrices at n = 5!
"""
import itertools
import math
import time
import numpy as np
from round9_wall2_boolean_probe import (
    build_all_4x4_matrices, eval_det4_perm4_exact, build_s4xs4_permutations
)
from round9_wall2_matrix_rank_and_bs import gf_rank


def forster_and_nuclear_stats(f01: np.ndarray, cut_axes_A: list, cut_axes_B: list):
    """Reshape 65536 truth table according to cut_axes_A (8 bits -> 256 rows)
    and cut_axes_B (8 bits -> 256 cols). Compute exact:
      - rk_R(M_pm), rk_F2(M_01), rk_F3(M_01)
      - sigma_max(M_pm) (spectral norm)
      - Forster_LB = 256.0 / sigma_max(M_pm) (lower bound on sign-rank!)
      - Nuclear norm ||M_pm||_* / 4096.0 (normalized trace norm = lower bound on TC^0_2 margin^-1)
      - Effective spectral rank ||M_pm||_* / sigma_max(M_pm)
    """
    f_tensor = f01.reshape((2,) * 16)
    M01 = np.transpose(f_tensor, cut_axes_A + cut_axes_B).reshape(256, 256)
    Mpm = 1.0 - 2.0 * M01.astype(np.float64)
    svals = np.linalg.svd(Mpm, compute_uv=False)
    s_max = float(svals[0])
    nuc = float(np.sum(svals))
    rk_pm = int(np.sum(svals > 1e-9))
    rk_f2 = gf_rank(M01, 2)
    rk_f3 = gf_rank(M01, 3)
    forster_lb = 256.0 / s_max
    s2 = float(svals[1]) if len(svals) > 1 else 1e-9
    forster_defl1 = 256.0 / s2
    norm_nuc = nuc / 4096.0  # in [1/16, 1] since sum(s_i^2) = 65536 -> max sum(s_i) = 16*256 = 4096
    eff_rk = nuc / s_max
    eff_rk_defl1 = (nuc - s_max) / s2
    return {
        "rk_pm": rk_pm, "rk_f2": rk_f2, "rk_f3": rk_f3,
        "s_max": s_max, "forster_lb": forster_lb, "forster_defl1": forster_defl1,
        "norm_nuc": norm_nuc, "eff_rk": eff_rk, "eff_rk_defl1": eff_rk_defl1,
    }


def exact_deg_n_approx_table_n234():
    """Compute exact deg-n `det_n mod 2` approximation error for n = 2, 3, 4."""
    out = {}
    for n in (2, 3, 4):
        N = n * n
        idx = np.arange(1 << N, dtype=np.uint32)
        X = np.array([((idx >> b) & 1) for b in range(N)], dtype=np.int64).T.reshape(1 << N, n, n)
        det = np.zeros(1 << N, dtype=np.int64)
        perm = np.zeros(1 << N, dtype=np.int64)
        for pi in itertools.permutations(range(n)):
            inv = sum(1 for i in range(n) for j in range(i + 1, n) if pi[i] > pi[j])
            sgn = -1 if (inv % 2) else 1
            term = np.ones(1 << N, dtype=np.int64)
            for i in range(n):
                term *= X[:, i, pi[i]]
            perm += term
            det += sgn * term
        f_d2 = (np.abs(det) % 2).astype(np.uint8)
        f_d3 = ((det % 3) != 0).astype(np.uint8)
        f_p3 = ((perm % 3) != 0).astype(np.uint8)
        f_pp = (perm > 0).astype(np.uint8)
        err_det = min(float(np.mean(f_d3 != f_d2)), float(np.mean(f_d3 != (1 ^ f_d2))))
        err_perm = min(float(np.mean(f_p3 != f_d2)), float(np.mean(f_p3 != (1 ^ f_d2))))
        err_pos = min(float(np.mean(f_pp != f_d2)), float(np.mean(f_pp != (1 ^ f_d2))))
        frac_le1 = float(np.mean(np.abs(det) <= 1))
        out[n] = (err_det, err_perm, err_pos, frac_le1, int(np.max(np.abs(det))))
    return out


def build_exact_n5_orbits():
    """Enumerate all C(36, 5) = 376,992 row-sorted 5x5 binary matrices, group them into the
    exact K_5 = 5,624 S_5 x S_5 orbits with exact orbit weights summing to 2^{25} = 33,554,432,
    evaluate exact det_5 and perm_5 on all 5,624 orbits, and compute exact 25-bit sensitivity / I(f)!"""
    # 1. Precompute column-permutation lookup table on 5-bit row integers 0..31:
    col_perms = list(itertools.permutations(range(5)))  # 120 perms
    col_lut = np.zeros((120, 32), dtype=np.int32)
    for p_idx, pi in enumerate(col_perms):
        for r in range(32):
            nr = 0
            for c in range(5):
                if (r >> pi[c]) & 1:
                    nr |= (1 << c)
            col_lut[p_idx, r] = nr

    # 2. Generate all C(36, 5) = 376,992 multisets of 5 rows 0 <= r0 <= r1 <= r2 <= r3 <= r4 <= 31:
    tuples = np.array(list(itertools.combinations_with_replacement(range(32), 5)), dtype=np.int32)
    M = tuples.shape[0]  # 376,992
    assert M == 376992

    # Multinomial row-permutation weight for each sorted 5-tuple: 120 / prod(count!)
    # Compute quickly by checking adjacent equalities in sorted 5-tuple!
    row_weights = np.zeros(M, dtype=np.int64)
    fact = [1, 1, 2, 6, 24, 120]
    for i in range(M):
        t = tuples[i]
        # run lengths
        denom = 1
        run = 1
        for k in range(1, 5):
            if t[k] == t[k - 1]:
                run += 1
            else:
                denom *= fact[run]
                run = 1
        denom *= fact[run]
        row_weights[i] = 120 // denom
    assert int(np.sum(row_weights)) == (1 << 25), f"Sum {np.sum(row_weights)} != 2^25"

    # Pack a sorted 5-tuple (r0..r4) in 0..31 into a single int32 key: sum_{k=0}^4 r_k * 32^(4-k)
    powers = np.array([32**4, 32**3, 32**2, 32, 1], dtype=np.int32)
    keys = tuples @ powers  # strictly increasing array of length 376,992!

    # Find canonical minimum key under all 120 column permutations:
    min_keys = keys.copy()
    for p_idx in range(1, 120):
        mapped = col_lut[p_idx, tuples]  # (M, 5)
        mapped.sort(axis=1)
        m_keys = mapped @ powers
        min_keys = np.minimum(min_keys, m_keys)

    uniq_keys, tuple_to_orb = np.unique(min_keys, return_inverse=True)
    n_orbits = len(uniq_keys)
    assert n_orbits == 5624, f"Expected K_5 = 5624 orbits, got {n_orbits}"

    orb_weights = np.bincount(tuple_to_orb, weights=row_weights, minlength=n_orbits).astype(np.int64)
    assert int(np.sum(orb_weights)) == (1 << 25)

    # Pick representative 5-tuple for each orbit (where keys == uniq_keys)
    rep_tuple_idx = np.searchsorted(keys, uniq_keys)
    rep_tuples = tuples[rep_tuple_idx]  # (5624, 5)

    # Build (5624, 5, 5) binary matrices
    X_orb = np.zeros((n_orbits, 5, 5), dtype=np.int64)
    for k in range(5):
        for c in range(5):
            X_orb[:, k, c] = (rep_tuples[:, k] >> c) & 1

    # Evaluate exact det_5 and perm_5 on all 5,624 orbit representatives!
    det5 = np.zeros(n_orbits, dtype=np.int64)
    perm5 = np.zeros(n_orbits, dtype=np.int64)
    for pi in itertools.permutations(range(5)):
        inv = sum(1 for i in range(5) for j in range(i + 1, 5) if pi[i] > pi[j])
        sgn = -1 if (inv % 2) else 1
        term = (X_orb[:, 0, pi[0]] * X_orb[:, 1, pi[1]] *
                X_orb[:, 2, pi[2]] * X_orb[:, 3, pi[3]] * X_orb[:, 4, pi[4]])
        perm5 += term
        det5 += sgn * term

    # Also build 25-neighbor orbit transitions for exact Total Influence / Sensitivity on {0,1}^{25}!
    # For each orbit rep (r0, r1, r2, r3, r4) and each bit flip (row k in 0..4, col c in 0..4),
    # new row k is r_k ^ (1 << c); sort the 5 rows, compute key, searchsorted in `keys`, map via `tuple_to_orb`!
    nbr_orbits = np.zeros((n_orbits, 25), dtype=np.int32)
    for k in range(5):
        for c in range(5):
            flipped = rep_tuples.copy()
            flipped[:, k] ^= (1 << c)
            flipped.sort(axis=1)
            f_keys = flipped @ powers
            t_idx = np.searchsorted(keys, f_keys)
            nbr_orbits[:, k * 5 + c] = tuple_to_orb[t_idx]

    return n_orbits, orb_weights, X_orb, det5, perm5, nbr_orbits


def main():
    t0 = time.time()
    print("=" * 100)
    print("PROF. WIGNER ROUND 12 (NODE E5.2): TC^0_2 FORSTER SIGN-RANK & EXACT n=5 (33,554,432 MATRICES) SCALING")
    print("=" * 100)

    X4 = build_all_4x4_matrices()
    det4, perm4 = eval_det4_perm4_exact(X4)
    _, _, n_orb4, orb_inv4 = build_s4xs4_permutations()
    rng = np.random.default_rng(20261121)

    f_d2 = (np.abs(det4) % 2).astype(np.uint8)
    f_d3 = ((det4 % 3) != 0).astype(np.uint8)
    f_pp = (perm4 > 0).astype(np.uint8)
    f_p3 = ((perm4 % 3) != 0).astype(np.uint8)
    f_rn = rng.integers(0, 2, size=1 << 16, dtype=np.uint8)
    f_rs = rng.integers(0, 2, size=n_orb4, dtype=np.uint8)[orb_inv4]

    funcs4 = [
        ("det_4 mod 2 (P)", f_d2),
        ("[det_4 != 0 mod 3] (P)", f_d3),
        ("[perm_4 > 0] (P)", f_pp),
        ("[perm_4 != 0 mod 3] (Mod3P)", f_p3),
        ("Random Boolean (RR Ctrl)", f_rn),
        ("Random S4xS4-Sym (SymCtrl)", f_rs),
    ]

    # Three balanced 8-vs-8 cuts of the 4x4 grid (indices 0..15 where b = 4*i + j):
    cut_row_A = list(range(0, 8))
    cut_row_B = list(range(8, 16))
    cut_chk_A = [4*i + j for i in range(4) for j in range(4) if (i + j) % 2 == 0]
    cut_chk_B = [4*i + j for i in range(4) for j in range(4) if (i + j) % 2 == 1]
    cut_blk_A = [4*i + j for i in range(4) for j in range(4) if (i < 2 and j < 2) or (i >= 2 and j >= 2)]
    cut_blk_B = [4*i + j for i in range(4) for j in range(4) if not ((i < 2 and j < 2) or (i >= 2 and j >= 2))]

    for cut_name, cA, cB in [
        ("CUT 1: Row-Cut (Rows {0,1} vs {2,3})", cut_row_A, cut_row_B),
        ("CUT 2: Checkerboard Cut ((i+j)%2 == 0 vs 1, Non-Row-Separated!)", cut_chk_A, cut_chk_B),
        ("CUT 3: Block-Diagonal vs Off-Diagonal 2x2 Cut (Non-Row-Separated!)", cut_blk_A, cut_blk_B),
    ]:
        print(f"\n--- {cut_name} ---")
        print(f"{'Function':27s} | {'rk_R(+-1)':9s} | {'rk_F2':5s} | {'rk_F3':5s} | {'Forster_LB':10s} | {'Forst_d1':8s} | {'||M||*/4096':11s} | {'EffRk(d1)':11s}")
        print("-" * 104)
        for name, f01 in funcs4:
            st = forster_and_nuclear_stats(f01, cA, cB)
            er_str = f"{st['eff_rk']:.1f}({st['eff_rk_defl1']:.1f})"
            print(f"{name:27s} | {st['rk_pm']:9d} | {st['rk_f2']:5d} | {st['rk_f3']:5d} | {st['forster_lb']:10.3f} | {st['forster_defl1']:8.3f} | {st['norm_nuc']:11.4f} | {er_str:11s}")

    print("\n" + "=" * 100)
    print("PART B: EXACT SCALING TO n = 5 (ALL 2^{25} = 33,554,432 MATRICES VIA K_5 = 5,624 ORBITS!)")
    print("=" * 100)
    n_orb5, w5, X5, det5, perm5, nbr5 = build_exact_n5_orbits()
    total5 = float(1 << 25)

    # Value distribution of |det_5| at n=5:
    abs_d5 = np.abs(det5)
    vals_d5 = {}
    for v in np.unique(abs_d5):
        vals_d5[int(v)] = int(np.sum(w5[abs_d5 == v]))
    print(f"Exact |det_5| distribution across all 33,554,432 {0,1}^{{5x5}} matrices:\n  {vals_d5}")
    frac5_le1 = (vals_d5.get(0, 0) + vals_d5.get(1, 0)) / total5

    # Exact degree-n `det_n mod 2` approximation table across n = 2, 3, 4, 5:
    t234 = exact_deg_n_approx_table_n234()
    f5_d2 = (abs_d5 % 2).astype(np.uint8)
    f5_d3 = ((det5 % 3) != 0).astype(np.uint8)
    f5_p3 = ((perm5 % 3) != 0).astype(np.uint8)
    f5_pp = (perm5 > 0).astype(np.uint8)

    def w_err(f_a, f_b):
        e0 = float(np.sum(w5[f_a != f_b])) / total5
        e1 = float(np.sum(w5[f_a != (1 ^ f_b)])) / total5
        return min(e0, e1)

    t234[5] = (w_err(f5_d3, f5_d2), w_err(f5_p3, f5_d2), w_err(f5_pp, f5_d2), frac5_le1, max(vals_d5.keys()))

    print("\n--- Exact Degree-n `det_n mod 2` (`= perm_n mod 2`) Hamming Error Scaling (n = 2, 3, 4, 5) ---")
    print(f"{'n (2^{n^2} matrices)':22s} | {'max|det_n|':10s} | {'P(|det_n|<=1)':13s} | {'err([det_n!=0 mod 3])':21s} | {'err([perm_n!=0 mod 3])':22s} | {'Gap Ratio':9s}")
    print("-" * 108)
    for n in (2, 3, 4, 5):
        ed, ep, epos, fle1, md = t234[n]
        ratio = (ep / ed) if ed > 0 else float("inf")
        n_str = f"n={n} ({1<<(n*n):,d})"
        print(f"{n_str:22s} | {md:10d} | {fle1:13.5f} | {ed:21.5f} | {ep:22.5f} | {ratio:8.2f}x")

    print("\n--- Exact n = 5 (25-Variable) Boolean Invariants Across All 33,554,432 Matrices ---")
    print(f"{'Function (n=5, N=25)':27s} | {'E[f]':8s} | {'I(f) [Exact]':12s} | {'s(min,max,s0,s1)':16s} | {'|f_hat(0)|':10s} | {'|f_hat(1)|':10s} | {'W_0+W_1':8s} | {'|f_hat(25)|':11s}")
    print("-" * 116)
    wt_orb = np.sum(X5.reshape(n_orb5, 25), axis=1).astype(np.float64)
    parity_all = (wt_orb.astype(np.int64) & 1).astype(np.uint8)
    char_deg1 = 1.0 - 2.0 * (wt_orb / 25.0)
    for name, f_orb in [
        ("det_5 mod 2 (P)", f5_d2),
        ("[det_5 != 0 mod 3] (P)", f5_d3),
        ("[perm_5 > 0] (P)", f5_pp),
        ("[perm_5 != 0 mod 3] (Mod3P)", f5_p3),
    ]:
        bal = float(np.sum(w5 * f_orb)) / total5
        f_nbr = f_orb[nbr5]  # (5624, 25)
        sens_orb = np.sum(f_nbr != f_orb[:, None], axis=1)
        inf_exact = float(np.sum(w5 * sens_orb)) / total5
        s_min, s_max = int(np.min(sens_orb)), int(np.max(sens_orb))
        s0_max = int(np.max(sens_orb[f_orb == 0]))
        s1_max = int(np.max(sens_orb[f_orb == 1]))
        fpm = 1.0 - 2.0 * f_orb.astype(np.float64)
        fhat_0 = abs(float(np.sum(w5 * fpm)) / total5)
        fhat_1 = abs(float(np.sum(w5 * fpm * char_deg1)) / total5)
        w01 = (fhat_0 ** 2) + 25.0 * (fhat_1 ** 2)
        fhat_all = abs(float(np.sum(w5 * fpm * (1.0 - 2.0 * parity_all))) / total5)
        s_str = f"{s_min},{s_max},{s0_max},{s1_max}"
        print(f"{name:27s} | {bal:8.5f} | {inf_exact:12.4f} | {s_str:16s} | {fhat_0:10.5f} | {fhat_1:10.5f} | {w01:8.5f} | {fhat_all:11.5f}")

    print(f"\n[DONE] Completed in {time.time()-t0:.2f}s.")


if __name__ == "__main__":
    main()
