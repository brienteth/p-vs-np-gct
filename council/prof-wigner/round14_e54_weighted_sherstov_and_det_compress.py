"""Prof. Wigner Round 14 — Node E5.4:
  Part 1 (E5.4a): Extract Valiant's 127/317-orbit adversarial dual distribution mu*_THR
    from `test_round13_engel63_tc0_thr_dictionary_lp.py` and compute weighted Sherstov discrepancy
    disc_mu(M) = ||M o mu||_2 / ||mu||_F (plus ||M o P||_2, weighted Forster ||P||_F / ||M o P||_2,
    effective weighted rank, and best-rectangle discrepancy) across Row-Cut and Checkerboard Cut
    (256 x 256) at n = 4!
  Part 2 (E5.4b): Explicit 2-term / mod-4 (`det_n mod 4 != 0`, exact deg <= 2n F_2-polynomial!)
    and AC^0[2]/NC^2-friendly corrections targeting |det_n| = 2 on n = 4 (65,536 matrices) and
    n = 5 (33,554,432 matrices via K_5 = 5,624 orbits!), plus comparison vs [perm_n != 0 mod 3]!
"""
import itertools
import sys
import time
import numpy as np

sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council/prof-valiant")
from test_round13_engel63_tc0_thr_dictionary_lp import (
    build_fast_s4_orbits, build_complete_01_thr_dictionary,
    build_signed_ternary_thr_dictionary, solve_dict_lp
)
from round9_wall2_boolean_probe import (
    build_all_4x4_matrices, eval_det4_perm4_exact, f2_anf_transform
)
from round12_e52_forster_and_n5_probe import build_exact_n5_orbits


def weighted_sherstov_metrics(M01: np.ndarray, P_mat: np.ndarray, rng: np.random.Generator):
    """Given M01 in {0,1}^{256x256} and probability matrix P_mat in R_{>=0}^{256x256} (sum P = 1):
    Compute exact weighted Sherstov metrics on M_pm = 1 - 2*M01:
      - ||M_pm o P||_2 (spectral norm of weighted matrix)
      - disc_mu = ||M_pm o P||_2 / ||P||_F
      - weighted_Forster = ||P||_F / ||M_pm o P||_2
      - weighted_eff_rk = ||M_pm o P||_* / ||M_pm o P||_2
      - rect_disc = max_{u,v in {+-1}^256} |u^T (M_pm o P) v| (via 30 restarts alternating sign maximization)
    """
    Mpm = 1.0 - 2.0 * M01.astype(np.float64)
    W = Mpm * P_mat
    s = np.linalg.svd(W, compute_uv=False)
    s_max = float(s[0])
    p_frob = float(np.linalg.norm(P_mat, "fro"))
    disc_mu = s_max / p_frob
    w_forster = p_frob / s_max
    eff_rk = float(np.sum(s)) / s_max

    # Alternating maximization of |u^T W v| over u, v in {+-1}^256
    U, _, Vt = np.linalg.svd(W, full_matrices=False)
    best_rect = 0.0
    for r in range(30):
        if r == 0:
            v = np.where(Vt[0] >= 0, 1.0, -1.0)
        else:
            v = rng.choice([-1.0, 1.0], size=256)
        for _ in range(12):
            u = np.where(W @ v >= 0, 1.0, -1.0)
            v_new = np.where(W.T @ u >= 0, 1.0, -1.0)
            if np.array_equal(v_new, v):
                break
            v = v_new
        val = abs(float(u @ (W @ v)))
        if val > best_rect:
            best_rect = val

    return {
        "s_max_W": s_max, "p_frob": p_frob, "disc_mu": disc_mu,
        "w_forster": w_forster, "eff_rk": eff_rk, "rect_disc": best_rect,
    }


def main():
    t0 = time.time()
    print("=" * 100)
    print("PROF. WIGNER ROUND 14 — NODE E5.4: LP-WEIGHTED SHERSTOV DISCREPANCY & MOD-4 DET COMPRESSION")
    print("=" * 100)

    # --- PART 1 (E5.4a): Extract Valiant's 127/317-orbit mu*_THR ---
    perms, unique_reps, orbit_id, orbit_sizes, orbit_degs, X_reps, X_reps_orb = build_fast_s4_orbits()
    T_01, _ = build_complete_01_thr_dictionary(X_reps, X_reps_orb, orbit_degs)
    T_full, _ = build_signed_ternary_thr_dictionary(perms, X_reps, X_reps_orb, orbit_degs, T_01)

    X4 = build_all_4x4_matrices()
    det4, perm4 = eval_det4_perm4_exact(X4)

    f4_d2 = (np.abs(det4) % 2).astype(np.uint8)
    f4_d3 = ((det4 % 3) != 0).astype(np.uint8)
    f4_pp = (perm4 > 0).astype(np.uint8)
    f4_p3 = ((perm4 % 3) != 0).astype(np.uint8)

    F4_p3_orb = 1.0 - 2.0 * f4_p3[unique_reps].astype(float)
    F4_d3_orb = 1.0 - 2.0 * f4_d3[unique_reps].astype(float)

    g_p3, res_p3 = solve_dict_lp(F4_p3_orb, T_full)
    g_d3, res_d3 = solve_dict_lp(F4_d3_orb, T_full)
    mu_p3_orb = np.maximum(-res_p3.ineqlin.marginals[:317], 0.0)
    mu_p3_orb /= np.sum(mu_p3_orb)
    mu_d3_orb = np.maximum(-res_d3.ineqlin.marginals[:317], 0.0)
    mu_d3_orb /= np.sum(mu_d3_orb)
    supp_p3 = int(np.sum(mu_p3_orb > 1e-9))
    supp_d3 = int(np.sum(mu_d3_orb > 1e-9))
    print(f"[E5.4a] Extracted Valiant 3,075-gate THR duals: gamma*(perm4)=1/{1/g_p3:.2f} (supp {supp_p3}/317), "
          f"gamma*(det4)=1/{1/g_d3:.2f} (supp {supp_d3}/317)")

    # Lift mu_p3_orb and mu_d3_orb to full 65,536-point probability distributions: P(X) = mu[orb(X)] / |orb(X)|
    P_mu_p3 = mu_p3_orb[orbit_id] / orbit_sizes[orbit_id].astype(np.float64)
    P_mu_d3 = mu_d3_orb[orbit_id] / orbit_sizes[orbit_id].astype(np.float64)
    assert abs(np.sum(P_mu_p3) - 1.0) < 1e-12 and abs(np.sum(P_mu_d3) - 1.0) < 1e-12
    P_unif = np.full(1 << 16, 1.0 / 65536.0)

    rng = np.random.default_rng(20261122)
    f4_rn = rng.integers(0, 2, size=1 << 16, dtype=np.uint8)
    funcs4 = [
        ("det_4 mod 2 (P)", f4_d2),
        ("[det_4 != 0 mod 3] (P)", f4_d3),
        ("[perm_4 > 0] (P)", f4_pp),
        ("[perm_4 != 0 mod 3] (Mod3P)", f4_p3),
        ("Random Boolean (RR Ctrl)", f4_rn),
    ]

    chk_A = [4*i + j for i in range(4) for j in range(4) if (i + j) % 2 == 0]
    chk_B = [4*i + j for i in range(4) for j in range(4) if (i + j) % 2 == 1]

    for cut_label, is_chk in [("ROW-CUT (256x256)", False), ("CHECKERBOARD CUT (256x256)", True)]:
        for dist_label, P_vec in [
            ("Uniform Distribution", P_unif),
            ("Valiant mu*_THR(det_4) [73/317 orbits — Fairness Control]", P_mu_d3),
            ("Valiant mu*_THR(perm_4) [127/317 orbits]", P_mu_p3),
        ]:
            if is_chk:
                P_mat = np.transpose(P_vec.reshape((2,)*16), chk_A + chk_B).reshape(256, 256)
            else:
                P_mat = P_vec.reshape(256, 256)
            print(f"\n--- {cut_label} | {dist_label} ---")
            print(f"{'Function':27s} | {'||MoP||_2':10s} | {'disc_mu':9s} | {'w_Forster':9s} | {'w_EffRk':8s} | {'rect_disc':9s}")
            print("-" * 86)
            for name, f01 in funcs4:
                if is_chk:
                    M01 = np.transpose(f01.reshape((2,)*16), chk_A + chk_B).reshape(256, 256)
                else:
                    M01 = f01.reshape(256, 256)
                st = weighted_sherstov_metrics(M01, P_mat, rng)
                print(f"{name:27s} | {st['s_max_W']:10.6f} | {st['disc_mu']:9.5f} | {st['w_forster']:9.3f} | {st['eff_rk']:8.2f} | {st['rect_disc']:9.5f}")

    # Also test: what if we use a symmetric-projected optimal distribution P_opt (maximizing 1 / disc_mu(perm4))?
    # Note: Let's check exact margin of mu*_THR(perm4) against all 256x256 rank-1 matrices vs P_unif!

    # --- PART 2 (E5.4b): Explicit 2-Term / Mod-4 (`det_n mod 4 != 0`) Asymptotic Compression at n=4 and n=5 ---
    print("\n" + "=" * 100)
    print("PART 2 (E5.4b): MOD-4 DETERMINANT CORRECTION `[det_n mod 4 != 0]` & AC^0[2]/NC^2 COMPRESSION")
    print("=" * 100)

    # Check exact F_2-ANF degree and #monomials of [det_4 mod 4 != 0], [det_4 mod 4 == 2], [perm_4 mod 4 != 0] at n=4:
    idx16 = np.arange(1 << 16, dtype=np.uint32)
    pop16 = np.zeros(1 << 16, dtype=np.int32)
    for b in range(16):
        pop16 += ((idx16 >> b) & 1).astype(np.int32)

    g4_mod4_eq2 = ((np.abs(det4) % 4) == 2).astype(np.uint8)
    g4_det_mod4_nz = ((det4 % 4) != 0).astype(np.uint8)
    g4_perm_mod4_nz = ((perm4 % 4) != 0).astype(np.uint8)
    # Also check: [det_4 != 0 mod 4] AND NOT [det_4 == +-3]? Wait, let's check exact ANF of g4_det_mod4_nz!
    print("\n--- n = 4 (65,536 Matrices) F_2-ANF & Compression of Mod-4 Determinant Correction ---")
    for name, g, target, tname in [
        ("det_4 mod 2", f4_d2, f4_d3, "[det_4!=0 mod 3]"),
        ("[det_4 mod 4 == 2]", g4_mod4_eq2, f4_d3, "[det_4!=0 mod 3]"),
        ("[det_4 mod 4 != 0] (2-term OR)", g4_det_mod4_nz, f4_d3, "[det_4!=0 mod 3]"),
        ("[perm_4 mod 4 != 0] vs perm", g4_perm_mod4_nz, f4_p3, "[perm_4!=0 mod 3]"),
    ]:
        anf = f2_anf_transform(g)
        nz = np.where(anf > 0)[0]
        deg = int(np.max(pop16[nz])) if len(nz) else 0
        err = float(np.mean(g != target))
        print(f"  {name:32s} -> F_2-deg = {deg:2d}, #ANF = {len(nz):5d}, err vs {tname:17s} = {err:.5f} ({100*err:.3f}%)")

    # Now n = 5 (ALL 33,554,432 matrices via K_5 = 5,624 orbits!):
    n_orb5, w5, X5, det5, perm5, _ = build_exact_n5_orbits()
    total5 = float(1 << 25)
    f5_d2 = (np.abs(det5) % 2).astype(np.uint8)
    f5_d3 = ((det5 % 3) != 0).astype(np.uint8)
    f5_p3 = ((perm5 % 3) != 0).astype(np.uint8)
    g5_det_mod4_nz = ((det5 % 4) != 0).astype(np.uint8)
    g5_perm_mod4_nz = ((perm5 % 4) != 0).astype(np.uint8)
    # Also mod 8 / mod 12 / exact [det_5 mod 4 != 0] AND [det_5 != +-3]? Wait: what about 2-bit / 3-bit modulus?
    # What is error of [det_5 mod 6 != 0]? No, mod 6 contains mod 3! What about mod 8 or [det_5 mod 4 != 0] XOR [|det_5| == 3]?
    # Test [det_5 mod 4 != 0] (pure 2-adic NC^2 / F_2-deg <= 2n = 10!) AND [det_5 mod 8 != 0] vs mod 3!
    g5_det_mod8_nz = ((det5 % 8) != 0).astype(np.uint8)  # cures |det_5|=4 too! Leaves ONLY +-3!

    print("\n--- n = 5 (ALL 33,554,432 Matrices via K_5 = 5,624 Orbits) Mod-4 & Mod-8 Compression ---")
    for name, g, target, tname in [
        ("det_5 mod 2 (deg 5)", f5_d2, f5_d3, "[det_5!=0 mod 3]"),
        ("[det_5 mod 4 != 0] (deg <= 10)", g5_det_mod4_nz, f5_d3, "[det_5!=0 mod 3]"),
        ("[det_5 mod 8 != 0] (deg <= 20)", g5_det_mod8_nz, f5_d3, "[det_5!=0 mod 3]"),
        ("perm_5 mod 2 (deg 5)", f5_d2, f5_p3, "[perm_5!=0 mod 3]"),
        ("[perm_5 mod 4 != 0]", g5_perm_mod4_nz, f5_p3, "[perm_5!=0 mod 3]"),
    ]:
        e0 = float(np.sum(w5[g != target])) / total5
        e1 = float(np.sum(w5[g != (1 ^ target)])) / total5
        err = min(e0, e1)
        print(f"  {name:32s} vs {tname:18s}: exact err = {err:.5f} ({100*err:.3f}%)")

    # Quick scaling ratio summary:
    err_d5_mod2 = float(np.sum(w5[f5_d2 != f5_d3])) / total5
    err_d5_mod4 = float(np.sum(w5[g5_det_mod4_nz != f5_d3])) / total5
    err_p5_mod4 = min(float(np.sum(w5[g5_perm_mod4_nz != f5_p3])) / total5,
                      float(np.sum(w5[g5_perm_mod4_nz != (1 ^ f5_p3)])) / total5)
    print(f"\n  [SUMMARY n=5]: [det_5!=0 mod 3] error drops {err_d5_mod2:.5f} -> {err_d5_mod4:.5f} "
          f"({err_d5_mod2/err_d5_mod4:.2f}x reduction via mod-4!) vs [perm_5!=0 mod 3] mod-4 error = {err_p5_mod4:.5f} "
          f"({err_p5_mod4/err_d5_mod4:.2f}x gap!)")

    print(f"\n[DONE] Completed in {time.time()-t0:.2f}s.")


if __name__ == "__main__":
    main()
