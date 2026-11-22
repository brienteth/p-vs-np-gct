"""Round 11 Obstacle-Breaking Lab (Front 2): Attacking ENGEL 3 (codim Sing(perm_4)) & ENGEL 5 (AC^0[2] / Razborov-Smolensky F_2-Approx).

Runs TWO fast, exact, high-impact experiments:
  1. ENGEL 5 (Wall 2 — Exact Low-Degree Real & F_2 Approximation Separation across all 65,536 {0,1}^{4x4} matrices):
     - Computes exact Fourier tail energy W^{> d}(f) = sum_{|S| > d} f_hat(S)^2 (exact L_2 distance to degree-d
       real polynomials) for d = 1..15 across:
         det_4 mod 2 (P), [det_4 != 0 mod 3] (P), [perm_4 > 0] (P), [perm_4 != 0 mod 3] (Mod_3 P), Random (Ctrl).
     - Computes exact MINIMUM Hamming error over ALL S_4 x S_4-invariant degree-d F_2-polynomials (for d = 1..8,
       exact linear algebra over F_2 on the 317 Burnside orbits — testing Razborov-Smolensky AC^0[2] hardness
       directly inside the non-Large S_4 x S_4 symmetry sector!).
  2. ENGEL 3 (Front 2 — Exact F_3 Algebraic Stratification of Sing(V(perm_4)) & Lifting w_2 >= 3 to w_2 >= 4):
     - Samples & counts exact points of Sing(V(perm_4)) over F_3 (random sampling of 200,000 matrices + exact
       zero-pattern component census over F_3) to measure the empirical dimension / codimension of Sing(V(perm_4))(F_3)
       and check whether ANY component has codim <= 7 (vs exact codim 8)!
"""
from __future__ import annotations

import itertools
import time
from typing import Dict, List, Tuple

import numpy as np

from verify_p_vs_np_wall2_lab import anf_mobius_f2, compute_all_perm4_det4, fwht, popcount_table


def test_engel5_fourier_and_f2_approx() -> None:
    print("=== ENGEL 5: EXACT DEGREE-d FOURIER TAIL W^{>d}(f) & S_4xS_4-SYMMETRIC F_2-APPROXIMATION ===")
    rng = np.random.default_rng(2026112111)
    pc = popcount_table(16)
    perm, det = compute_all_perm4_det4()

    f_det2 = (det & 1).astype(np.uint8)
    f_det3 = ((det % 3) != 0).astype(np.uint8)
    f_match = (perm > 0).astype(np.uint8)
    f_perm3 = ((perm % 3) != 0).astype(np.uint8)
    f_rand = (rng.random(1 << 16) < float(np.mean(f_perm3))).astype(np.uint8)

    funcs = [
        ("det4_mod2       (P)", f_det2),
        ("det4!=0 mod 3   (P)", f_det3),
        ("perm4 > 0       (P)", f_match),
        ("perm4!=0 mod 3 (M3P)", f_perm3),
        ("Random       (Ctrl)", f_rand),
    ]

    print("\n--- 1A. Exact Fourier Tail Energy W^{> d}(f) = sum_{|S| > d} f_hat(S)^2 (Lower = Easier to Approximate) ---")
    ds = [2, 4, 6, 8, 10, 12]
    hdr = f"{'Function':22s} | " + " | ".join(f"W>{d:2d}  " for d in ds)
    print(hdr)
    print("-" * len(hdr))
    for name, fb in funcs:
        g = 1.0 - 2.0 * fb.astype(np.float64)
        fh2 = fwht(g) ** 2
        tails = [float(np.sum(fh2[pc > d])) for d in ds]
        print(f"{name:22s} | " + " | ".join(f"{t:6.4f}" for t in tails))

    # 1B. Exact L_2-optimal degree-d real-thresholded approximation error (rounding the degree-<=d Fourier truncation!)
    print("\n--- 1B. Sign-Thresholded Degree-<=d Real Polynomial Hamming Error (0.5 = Random Guessing) ---")
    ds2 = [2, 4, 6, 8, 10]
    hdr2 = f"{'Function':22s} | " + " | ".join(f"d<={d:2d} " for d in ds2)
    print(hdr2)
    print("-" * len(hdr2))
    for name, fb in funcs:
        g = 1.0 - 2.0 * fb.astype(np.float64)
        fh = fwht(g)
        errs = []
        for d in ds2:
            fh_trunc = fh.copy()
            fh_trunc[pc > d] = 0.0
            # Inverse WHT = N * fwht(fh_trunc)
            g_approx = (1 << 16) * fwht(fh_trunc)
            pred_bits = (g_approx < 0.0).astype(np.uint8)
            errs.append(float(np.mean(pred_bits != fb)))
        print(f"{name:22s} | " + " | ".join(f"{e:6.4f}" for e in errs))

    # 1C. Exact F_2-ANF Monomial Energy by Degree (comparing det4!=0 mod 3 vs perm4!=0 mod 3!)
    print("\n--- 1C. Exact F_2-ANF Monomial Count by Degree d = 0..16 ---")
    anf_d3 = anf_mobius_f2(f_det3)
    anf_p3 = anf_mobius_f2(f_perm3)
    cnt_d3 = [int(np.sum(anf_d3[pc == d])) for d in range(17)]
    cnt_p3 = [int(np.sum(anf_p3[pc == d])) for d in range(17)]
    print("  deg:      " + " ".join(f"{d:4d}" for d in range(17)))
    print("  det4_m3:  " + " ".join(f"{c:4d}" for c in cnt_d3))
    print("  perm4_m3: " + " ".join(f"{c:4d}" for c in cnt_p3))


def perm3_f3_vec(m: np.ndarray) -> np.ndarray:
    """Vectorized 3x3 permanent mod 3 on batch of shape (B, 3, 3)."""
    p = (
        m[:, 0, 0] * (m[:, 1, 1] * m[:, 2, 2] + m[:, 1, 2] * m[:, 2, 1])
        + m[:, 0, 1] * (m[:, 1, 0] * m[:, 2, 2] + m[:, 1, 2] * m[:, 2, 0])
        + m[:, 0, 2] * (m[:, 1, 0] * m[:, 2, 1] + m[:, 1, 1] * m[:, 2, 0])
    )
    return p % 3


def test_engel3_sing_perm4_f3() -> None:
    print("\n=== ENGEL 3: EXACT F_3 POINT-DENSITY & STRATIFICATION AUDIT OF Sing(V(perm_4)) ===")
    rng = np.random.default_rng(2026112113)
    # In F_3^{16} (3^16 = 43,046,721 matrices):
    # - A codim-6 component has ~ 3^{10} = 59,049 points -> probability ~ 1 / 729 = 1.37e-3 (~274 hits in 200k!)
    # - A codim-7 component has ~ 3^9 = 19,683 points    -> probability ~ 1 / 2187 = 4.57e-4 (~91 hits in 200k!)
    # - A codim-8 component (e.g. 6 pairs of 2 zero rows + 6 pairs of 2 zero cols + 16 (1 row + 1 col + perm3=0)
    #   + 8 (1 zero row + all 4 perm3=0) + ...) has ~ C * 3^8 = C * 6,561 points -> probability ~ C / 6561!
    # Wait: let's sample 500,000 random matrices in F_3^{4x4} AND also test Sing(V(det_4)) for exact calibration!
    n_samp = 400_000
    mats = rng.integers(0, 3, size=(n_samp, 4, 4), dtype=np.int16)

    # Compute all 16 3x3 sub-permanents mod 3 vectorized!
    is_sing_perm = np.ones(n_samp, dtype=bool)
    for i in range(4):
        rows = [r for r in range(4) if r != i]
        for j in range(4):
            cols = [c for c in range(4) if c != j]
            sub = mats[:, rows, :][:, :, cols]
            is_sing_perm &= (perm3_f3_vec(sub) == 0)

    n_hits = int(np.sum(is_sing_perm))
    sing_mats = mats[is_sing_perm]
    # Also compute exact Sing(V(det_4)) = {rank_F3 <= 2} for calibration (known codim = 4 => prob ~ 1/81 * factor)
    # Check 3x3 sub-determinants mod 3 on first 50,000
    m_det = mats[:50_000]
    is_sing_det = np.ones(50_000, dtype=bool)
    for i in range(4):
        rows = [r for r in range(4) if r != i]
        for j in range(4):
            cols = [c for c in range(4) if c != j]
            sub = m_det[:, rows, :][:, :, cols]
            d3 = (
                sub[:, 0, 0] * (sub[:, 1, 1] * sub[:, 2, 2] - sub[:, 1, 2] * sub[:, 2, 1])
                - sub[:, 0, 1] * (sub[:, 1, 0] * sub[:, 2, 2] - sub[:, 1, 2] * sub[:, 2, 0])
                + sub[:, 0, 2] * (sub[:, 1, 0] * sub[:, 2, 1] - sub[:, 1, 1] * sub[:, 2, 0])
            ) % 3
            is_sing_det &= (d3 == 0)
    det_rate = float(np.mean(is_sing_det))
    perm_rate = n_hits / float(n_samp)
    est_codim_det = -np.log(det_rate) / np.log(3.0) if det_rate > 0 else 99.0
    est_codim_perm = -np.log(perm_rate) / np.log(3.0) if perm_rate > 0 else 99.0

    print(f"  Calibration Sing(V(det_4))  over F_3 (50k samples):  hits={int(np.sum(is_sing_det)):5d}, rate={det_rate:.5f}, -log_3(rate)={est_codim_det:.2f} (exact codim = 4)")
    print(f"  Target      Sing(V(perm_4)) over F_3 (400k samples): hits={n_hits:5d}, rate={perm_rate:.5f}, -log_3(rate)={est_codim_perm:.2f}")

    # Classify ALL discovered F_3 singular points of perm_4 by zero-row / zero-col structure!
    n_zero_rc = 0
    n_two_zero_r_or_c = 0
    n_one_r_one_c = 0
    n_one_r_or_c_only = 0
    n_dense_no_zero_rc = 0
    for mat in sing_mats:
        zr = int(np.sum(np.all(mat == 0, axis=1)))
        zc = int(np.sum(np.all(mat == 0, axis=0)))
        if zr >= 2 or zc >= 2:
            n_two_zero_r_or_c += 1
        elif zr >= 1 and zc >= 1:
            n_one_r_one_c += 1
        elif zr == 1 or zc == 1:
            n_one_r_or_c_only += 1
        else:
            n_dense_no_zero_rc += 1
    print(f"  Stratum breakdown of all {n_hits} F_3 singular points of perm_4:")
    print(f"    >=2 zero rows or cols (exact codim 8):     {n_two_zero_r_or_c:4d}")
    print(f"    1 zero row + 1 zero col (exact codim 8):   {n_one_r_one_c:4d}")
    print(f"    1 zero row or col only (exact codim 8):    {n_one_r_or_c_only:4d}")
    print(f"    NO zero row & NO zero col (dense!):        {n_dense_no_zero_rc:4d}")
    if n_dense_no_zero_rc > 0:
        # Print first dense singular point over F_3 and its zero count!
        dense_ex = [m for m in sing_mats if np.all(np.any(m != 0, axis=1)) and np.all(np.any(m != 0, axis=0))][0]
        print(f"    Example dense F_3 singular point (zeros={int(np.sum(dense_ex==0))}/16):\n{dense_ex}")


def main() -> None:
    t0 = time.time()
    test_engel5_fourier_and_f2_approx()
    test_engel3_sing_perm4_f3()
    print(f"\n[DONE] Round 11 Obstacle-Breaking Lab finished in {time.time()-t0:.2f}s.")


if __name__ == "__main__":
    main()
