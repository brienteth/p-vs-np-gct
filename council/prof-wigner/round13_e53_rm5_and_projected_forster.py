"""Prof. Wigner Round 13 — Node E5.3:
  (A) E5.3a: Exact multi-term S_5 x S_5-symmetric RM(5, 25) F_2-approximation across ALL
      2^{25} = 33,554,432 matrices in {0,1}^{5x5} (using all K_5(<=5) = 61 invariant basis
      polynomials on the K_5 = 5,624 weighted orbits!).
  (B) E5.3b: Density-projected & conditional TC^0_2 Forster Sign-Rank / Discrepancy at n = 4:
      1. Active Non-Zero-Row Submatrix (225 x 225 on Row-Cut) -> rigorous Forster LB!
      2. Fixed-Hamming-Weight Slice (70 x 70 on Checkerboard Cut, wt_A=4, wt_B=4) -> rigorous Forster LB!
      3. Constant-Row-Sum / Weight-Balanced Checkerboard & Low-Rank SVD Deflation M^{(k)} (k=1,2,3,5).
"""
import itertools
import time
import numpy as np
from round9_wall2_boolean_probe import (
    build_all_4x4_matrices, eval_det4_perm4_exact, build_s4xs4_permutations
)
from round9_wall2_matrix_rank_and_bs import gf_rank
from round12_e52_forster_and_n5_probe import build_exact_n5_orbits


def build_n5_sym_rm_basis(n_orb5: int, X5: np.ndarray, max_deg: int = 5):
    """Build exact K_5(<=5) = 61 S_5 x S_5-symmetric F_2 basis vectors of degree <= 5
    evaluated on all 5,624 orbit representatives!"""
    col_perms = list(itertools.permutations(range(5)))
    col_lut = np.zeros((120, 32), dtype=np.int32)
    for p_idx, pi in enumerate(col_perms):
        for r in range(32):
            nr = 0
            for c in range(5):
                if (r >> pi[c]) & 1:
                    nr |= (1 << c)
            col_lut[p_idx, r] = nr

    # Represent each 5x5 matrix X5[o] as a 25-bit uint32 integer:
    X_flat = X5.reshape(n_orb5, 25).astype(np.uint32)
    X_u32 = np.sum(X_flat << np.arange(25, dtype=np.uint32), axis=1)  # (5624,)

    powers = np.array([32**4, 32**3, 32**2, 32, 1], dtype=np.int32)

    basis_by_deg = {}
    counts = {}
    for d in range(max_deg + 1):
        # Enumerate all C(25, d) monomials as sorted 5-row tuples
        combos = list(itertools.combinations(range(25), d))
        M_cnt = len(combos)
        m_u32 = np.zeros(M_cnt, dtype=np.uint32)
        m_rows = np.zeros((M_cnt, 5), dtype=np.int32)
        for idx, bits in enumerate(combos):
            mask = 0
            rows = [0, 0, 0, 0, 0]
            for b in bits:
                mask |= (1 << b)
                rows[b // 5] |= (1 << (b % 5))
            rows.sort()
            m_u32[idx] = mask
            m_rows[idx] = rows

        keys = m_rows @ powers
        min_keys = keys.copy()
        for p_idx in range(1, 120):
            mapped = col_lut[p_idx, m_rows]
            mapped.sort(axis=1)
            m_keys = mapped @ powers
            min_keys = np.minimum(min_keys, m_keys)

        uniq_k, inv = np.unique(min_keys, return_inverse=True)
        counts[d] = len(uniq_k)

        vecs = []
        for oid in range(len(uniq_k)):
            sub_masks = m_u32[inv == oid]  # (L,)
            # Evaluate parity of #{m in sub_masks : (X_u32 & m) == m} in chunks of 512!
            par = np.zeros(n_orb5, dtype=np.uint8)
            for start in range(0, len(sub_masks), 512):
                chunk = sub_masks[start:start + 512]
                hits = (X_u32[:, None] & chunk[None, :]) == chunk[None, :]
                par ^= (np.sum(hits, axis=1) & 1).astype(np.uint8)
            vecs.append(par)
        basis_by_deg[d] = vecs

    return basis_by_deg, counts


def exact_weighted_sym_min(f_orb: np.ndarray, w5: np.ndarray, vecs: list) -> float:
    """Exhaustive optimum over all 2^K polynomials (feasible for K <= 14)."""
    K = len(vecs)
    B = np.array(vecs, dtype=np.uint8)
    total = 1 << K
    best = int(np.sum(w5))
    for start in range(0, total, 1024):
        end = min(total, start + 1024)
        c_idx = np.arange(start, end, dtype=np.uint32)
        coeffs = ((c_idx[:, None] >> np.arange(K, dtype=np.uint32)) & 1).astype(np.uint8)
        preds = (coeffs @ B) & 1  # (batch, 5624)
        errs = (preds ^ f_orb[None, :]) @ w5
        m = int(np.min(errs))
        if m < best:
            best = m
    return best / float(1 << 25)


def sa_weighted_sym_min(f_orb: np.ndarray, w5: np.ndarray, vecs: list, rng: np.random.Generator,
                        restarts: int = 50, seed_preds: list = None) -> float:
    """Multi-start coordinate descent + 2-flip search over K symmetric basis vectors on weighted orbits."""
    B = np.array(vecs, dtype=np.uint8)  # (K, 5624)
    K = B.shape[0]
    best = int(np.sum(f_orb * w5))
    best = min(best, int(np.sum((1 ^ f_orb) * w5)))
    if seed_preds is None:
        seed_preds = []
    for r in range(restarts + len(seed_preds)):
        if r < len(seed_preds):
            pred = seed_preds[r].copy()
        elif r == len(seed_preds):
            pred = np.zeros_like(f_orb)
        else:
            c = rng.integers(0, 2, size=K, dtype=np.uint8)
            pred = (c @ B) & 1
        cur_err = int(np.sum((pred ^ f_orb) * w5))
        for _ in range(80):
            # Vectorized evaluation of ALL K single-bit flips at once!
            cands = pred[None, :] ^ B  # (K, 5624)
            errs = (cands ^ f_orb[None, :]) @ w5
            j = int(np.argmin(errs))
            ne = int(errs[j])
            if ne < cur_err:
                pred = cands[j]
                cur_err = ne
            else:
                # Try random 2-flips (batch of 64)
                pairs = rng.integers(0, K, size=(64, 2))
                c2 = pred[None, :] ^ B[pairs[:, 0]] ^ B[pairs[:, 1]]
                e2 = (c2 ^ f_orb[None, :]) @ w5
                j2 = int(np.argmin(e2))
                if int(e2[j2]) < cur_err:
                    pred = c2[j2]
                    cur_err = int(e2[j2])
                else:
                    break
        if cur_err < best:
            best = cur_err
    return best / float(1 << 25)


def submatrix_forster_stats(M01_sub: np.ndarray):
    """Exact Forster lower bound & trace/rank metrics on any rectangular {0,1} submatrix!
    For M_pm in {+-1}^{m x n}, Forster LB = sqrt(m * n) / sigma_max(M_pm).
    (Wait: strictly, Forster's theorem gives sign_rank(M_pm) >= sqrt(m*n)/||M_pm||_2 for any +-1 matrix!)"""
    m, n = M01_sub.shape
    Mpm = 1.0 - 2.0 * M01_sub.astype(np.float64)
    s = np.linalg.svd(Mpm, compute_uv=False)
    s_max = float(s[0])
    nuc = float(np.sum(s))
    rk_pm = int(np.sum(s > 1e-9))
    rk_f2 = gf_rank(M01_sub, 2)
    rk_f3 = gf_rank(M01_sub, 3)
    forster_lb = np.sqrt(m * n) / s_max
    # Normalized nuclear norm relative to Frobenius norm sqrt(m*n)*min(m,n)^{1/2} -> trace norm / (m*n) or / (sqrt(rk)*||M||_F)
    # Better: effective rank ||M||_* / ||M||_2 and normalized ||M||_* / (m*sqrt(n))!
    norm_nuc = nuc / (m * np.sqrt(n))  # max is 1.0 if all s equal sqrt(m) for m=n
    eff_rk = nuc / s_max
    # Also SVD deflation M - sum_{i<=k} s_i u_i v_i^T residual Forster proxy = ||M^(k)||_F / s_{k+1}
    frob2 = float(m * n)
    res_defl1 = np.sqrt(max(frob2 - s[0]**2, 0.0)) / float(s[1])
    res_defl2 = np.sqrt(max(frob2 - s[0]**2 - s[1]**2, 0.0)) / float(s[2])
    return {
        "shape": (m, n), "rk_pm": rk_pm, "rk_f2": rk_f2, "rk_f3": rk_f3,
        "forster_lb": forster_lb, "norm_nuc": norm_nuc, "eff_rk": eff_rk,
        "defl1": res_defl1, "defl2": res_defl2,
    }


def main():
    t0 = time.time()
    print("=" * 100)
    print("PROF. WIGNER ROUND 13 (NODE E5.3): n=5 RM(5,25) SYM APPROXIMATION & PROJECTED FORSTER TC^0_2")
    print("=" * 100)

    # --- PART A: E5.3a (n=5, 33,554,432 matrices, 61 symmetric RM basis polynomials) ---
    n_orb5, w5, X5, det5, perm5, _ = build_exact_n5_orbits()
    basis_by_deg, counts = build_n5_sym_rm_basis(n_orb5, X5, max_deg=5)
    print(f"\n[E5.3a] Verified S_5 x S_5 F_2-monomial orbit counts d=0..5: {counts} (total <=5: {sum(counts.values())})")
    assert sum(counts.values()) == 61

    f5_d2 = (np.abs(det5) % 2).astype(np.uint8)
    f5_d3 = ((det5 % 3) != 0).astype(np.uint8)
    f5_p3 = ((perm5 % 3) != 0).astype(np.uint8)
    f5_pp = (perm5 > 0).astype(np.uint8)

    # Verify det_5 mod 2 is inside span of degree-5 basis (in fact, exactly one of the 34 orbits!)
    assert any(np.array_equal(v, f5_d2) for v in basis_by_deg[5]), "det_5 mod 2 must be an exact deg-5 orbit!"
    print("[E5.3a] Verified: det_5 mod 2 (= perm_5 mod 2) is an exact single degree-5 orbit polynomial.")

    rng = np.random.default_rng(20261121)
    orb_rand5 = rng.integers(0, 2, size=n_orb5, dtype=np.uint8)

    print(f"\n--- E5.3a: Multi-Term S_5 x S_5-Symmetric RM(d, 25) Hamming Error (All 33,554,432 Matrices) ---")
    print("  (d=1..3: EXHAUSTIVE global min over all 2^1..2^11 sym polys; d=4..5: 60-restart seeded SA)")
    print(f"{'Function (n=5, 33.55M)':27s} | {'d=1 ex':7s} | {'d=2 ex':7s} | {'d=3 ex':7s} | {'d=4 SA':8s} | {'d=5 SA':8s}")
    print("-" * 80)

    for name, f_orb in [
        ("[det_5 != 0 mod 3] (P)", f5_d3),
        ("[perm_5 != 0 mod 3] (Mod3P)", f5_p3),
        ("[perm_5 > 0] (P)", f5_pp),
        ("Random S5xS5-Sym (SymCtrl)", orb_rand5),
    ]:
        e1 = exact_weighted_sym_min(f_orb, w5, [v for dd in range(2) for v in basis_by_deg[dd]])
        e2 = exact_weighted_sym_min(f_orb, w5, [v for dd in range(3) for v in basis_by_deg[dd]])
        e3 = exact_weighted_sym_min(f_orb, w5, [v for dd in range(4) for v in basis_by_deg[dd]])
        e4 = sa_weighted_sym_min(f_orb, w5, [v for dd in range(5) for v in basis_by_deg[dd]], rng, restarts=60)
        # At d=5, seed with det_5 mod 2 and (1 ^ det_5 mod 2)!
        e5 = sa_weighted_sym_min(
            f_orb, w5, [v for dd in range(6) for v in basis_by_deg[dd]],
            rng, restarts=60, seed_preds=[f5_d2, 1 ^ f5_d2]
        )
        print(f"{name:27s} | {e1:7.5f} | {e2:7.5f} | {e3:7.5f} | {e4:8.5f} | {e5:8.5f}")

    # --- PART B: E5.3b (Projected & Conditional TC^0_2 Forster Sign-Rank at n = 4) ---
    print("\n" + "=" * 100)
    print("PART B (E5.3b): CONDITIONAL SUBMATRICES & SVD-DEFLATED FORSTER BOUND (n = 4)")
    print("=" * 100)
    X4 = build_all_4x4_matrices()
    det4, perm4 = eval_det4_perm4_exact(X4)
    _, _, n_orb4, orb_inv4 = build_s4xs4_permutations()

    f4_d2 = (np.abs(det4) % 2).astype(np.uint8)
    f4_d3 = ((det4 % 3) != 0).astype(np.uint8)
    f4_pp = (perm4 > 0).astype(np.uint8)
    f4_p3 = ((perm4 % 3) != 0).astype(np.uint8)
    f4_rn = rng.integers(0, 2, size=1 << 16, dtype=np.uint8)
    f4_rs = rng.integers(0, 2, size=n_orb4, dtype=np.uint8)[orb_inv4]

    funcs4 = [
        ("det_4 mod 2 (P)", f4_d2),
        ("[det_4 != 0 mod 3] (P)", f4_d3),
        ("[perm_4 > 0] (P)", f4_pp),
        ("[perm_4 != 0 mod 3] (Mod3P)", f4_p3),
        ("Random Boolean (RR Ctrl)", f4_rn),
        ("Random S4xS4-Sym (SymCtrl)", f4_rs),
    ]

    # Mask 1: Row-Cut Active Core (no all-zero row in rows {0,1} or {2,3} -> 15^2 = 225 x 225)
    # In bit order: row 0 = bits 0..3, row 1 = bits 4..7, row 2 = bits 8..11, row 3 = bits 12..15.
    idx8 = np.arange(256, dtype=np.uint32)
    row_active = ((idx8 & 0x0F) != 0) & ((idx8 & 0xF0) != 0)
    act_idx = np.where(row_active)[0]  # 225 indices!

    # Mask 2: Checkerboard Cut Fixed-Weight Balanced Slice (wt(A)=4, wt(B)=4 -> 70 x 70)
    chk_A = [4*i + j for i in range(4) for j in range(4) if (i + j) % 2 == 0]
    chk_B = [4*i + j for i in range(4) for j in range(4) if (i + j) % 2 == 1]
    wt8 = np.array([bin(v).count("1") for v in range(256)])
    bal_idx = np.where(wt8 == 4)[0]  # C(8,4) = 70 indices!

    # Mask 3: Checkerboard Cut Active (no all-zero 4-tuple on either even or odd side? Even better:
    # Restrict to matrices where ALL 4 rows and ALL 4 cols of the full 4x4 matrix are non-zero? That's not a product set!
    # A submatrix MUST be a Cartesian product A_sub x B_sub so Forster LB is a genuine sign-rank LB!
    # Also test Checkerboard wt in {3, 4, 5}: C(8,3)+C(8,4)+C(8,5) = 56+70+56 = 182 x 182!)
    mid_idx = np.where((wt8 >= 3) & (wt8 <= 5))[0]  # 182 x 182!

    for label, mode in [
        ("1. Row-Cut No-Zero-Row Active Submatrix (225 x 225)", "row_active"),
        ("2. Checkerboard Balanced Weight-4 Submatrix (70 x 70)", "chk_bal4"),
        ("3. Checkerboard Mid-Weight {3,4,5} Submatrix (182 x 182)", "chk_mid"),
        ("4. Full Checkerboard (256 x 256) w/ SVD Deflation (d1, d2)", "chk_full"),
    ]:
        print(f"\n--- {label} ---")
        print(f"{'Function':27s} | {'rk_R(+-1)':9s} | {'rk_F2':5s} | {'rk_F3':5s} | {'Forster_LB':10s} | {'Defl_1':8s} | {'Defl_2':8s} | {'Eff_Rk':8s}")
        print("-" * 100)
        for name, f01 in funcs4:
            if mode == "row_active":
                Msub = f01.reshape(256, 256)[np.ix_(act_idx, act_idx)]
            else:
                Mchk = np.transpose(f01.reshape((2,)*16), chk_A + chk_B).reshape(256, 256)
                if mode == "chk_bal4":
                    Msub = Mchk[np.ix_(bal_idx, bal_idx)]
                elif mode == "chk_mid":
                    Msub = Mchk[np.ix_(mid_idx, mid_idx)]
                else:
                    Msub = Mchk
            st = submatrix_forster_stats(Msub)
            print(f"{name:27s} | {st['rk_pm']:9d} | {st['rk_f2']:5d} | {st['rk_f3']:5d} | {st['forster_lb']:10.3f} | {st['defl1']:8.3f} | {st['defl2']:8.3f} | {st['eff_rk']:8.2f}")

    print(f"\n[DONE] Completed in {time.time()-t0:.2f}s.")


if __name__ == "__main__":
    main()
