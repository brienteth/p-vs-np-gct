"""Phase 6B Deep Stress-Test: Is the w2=5 Obstruction in S2_4000_2200 Real (vs LM Convergence)?

Tests two targeted questions on globally mixed (1, 4, w2, 4, 1) ABPs:
  1. Pure (2,2,0,0) WITHOUT (4,0,0,0): Pi_RowML (256) + (2,2,0,0) (270) = 526 eqs for w2 in {6, 5, 4, 3}.
  2. Deep S2_4000_2200: Pi_RowML (256) + (4,0,0,0) (140) + (2,2,0,0) (270) = 666 eqs at w2 = 5 with
     10 starts x 220 LM iterations (comparing against w2 = 6 with 5 starts x 220 iterations).
  3. Also tests EXACT full (2,2,0,0) monomial span (100 pts/pair = 600 eqs vs 270 eqs) to see if
     the w2 = 5 residual jumps sharply when (2,2,0,0) is fully spanned!
"""
from __future__ import annotations

import itertools
import time
from typing import List, Tuple

import numpy as np

from verify_0g_phase6b import (
    abp_point_res_jac,
    build_perm4_rowml_target,
    eval_22_only_batch,
    eval_rowml_res_jac,
    make_single_row_points,
)


def run_probe(
    name: str,
    w2: int,
    include_4000: bool,
    pts_per_pair_22: int,
    n_starts: int,
    max_iters: int,
    rng: np.random.Generator,
) -> Tuple[int, float, float]:
    w1, w3 = 4, 4
    s1, s2, s3, s4 = 16 * w1, 16 * w1 * w2, 16 * w2 * w3, 16 * w3
    n_vars = s1 + s2 + s3 + s4
    target_flat = build_perm4_rowml_target().reshape(256)
    perms = list(itertools.permutations(range(4)))
    inv_perms = []
    for pi in perms:
        inv = [0] * 4
        for pos, r in enumerate(pi):
            inv[r] = pos
        inv_perms.append(tuple(inv))

    xs_single = make_single_row_points(rng, pts_per_row=35)
    pairs = list(itertools.combinations(range(4), 2))
    xs_two_by_pair = []
    for r1, r2 in pairs:
        xp = np.zeros((pts_per_pair_22, 4, 4), dtype=np.complex128)
        v1 = rng.standard_normal((pts_per_pair_22, 4)) + 1j * rng.standard_normal((pts_per_pair_22, 4))
        v2 = rng.standard_normal((pts_per_pair_22, 4)) + 1j * rng.standard_normal((pts_per_pair_22, 4))
        xp[:, r1, :] = v1 / np.linalg.norm(v1, axis=1, keepdims=True)
        xp[:, r2, :] = v2 / np.linalg.norm(v2, axis=1, keepdims=True)
        xs_two_by_pair.append((r1, r2, xp))

    def res_and_jac(z: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        l1 = z[0:s1].reshape(4, 4, 1, w1)
        l2 = z[s1 : s1 + s2].reshape(4, 4, w1, w2)
        l3 = z[s1 + s2 : s1 + s2 + s3].reshape(4, 4, w2, w3)
        l4 = z[s1 + s2 + s3 :].reshape(4, 4, w3, 1)

        f_list = []
        j_list = []
        f0, j0 = eval_rowml_res_jac(l1, l2, l3, l4, target_flat, perms, inv_perms)
        f_list.append(f0)
        j_list.append(j0)

        if include_4000:
            f1, j1 = abp_point_res_jac(l1, l2, l3, l4, xs_single)
            f_list.append(f1)
            j_list.append(j1)

        for r1, r2, xp in xs_two_by_pair:
            f22, j22 = eval_22_only_batch(l1, l2, l3, l4, xp, r1, r2)
            f_list.append(f22)
            j_list.append(j22)

        fc = np.concatenate(f_list)
        jc = np.vstack(j_list)
        r_real = np.concatenate([fc.real, fc.imag])
        j_real = np.vstack([np.hstack([jc.real, -jc.imag]), np.hstack([jc.imag, jc.real])])
        return r_real, j_real

    finals: List[float] = []
    for _ in range(n_starts):
        z = 0.4 * (rng.standard_normal(n_vars) + 1j * rng.standard_normal(n_vars))
        r, jac = res_and_jac(z)
        cur = float(np.linalg.norm(r))
        lam = 1e-2
        for _it in range(max_iters):
            if cur < 1e-11:
                break
            jtj = jac.T @ jac
            g = jac.T @ r
            diag = np.maximum(np.diag(jtj), 1e-6)
            accepted = False
            for _try in range(6):
                lhs = jtj + lam * np.diag(diag)
                try:
                    step = -np.linalg.solve(lhs, g)
                except np.linalg.LinAlgError:
                    step, _, _, _ = np.linalg.lstsq(lhs, -g, rcond=None)
                z_new = z + step[:n_vars] + 1j * step[n_vars:]
                r_new, j_new = res_and_jac(z_new)
                new_norm = float(np.linalg.norm(r_new))
                if new_norm < cur:
                    z, r, jac, cur = z_new, r_new, j_new, new_norm
                    lam = max(lam * 0.3, 1e-11)
                    accepted = True
                    break
                lam = min(lam * 5.0, 1e7)
            if not accepted and lam >= 1e6:
                break
        finals.append(cur)

    solved = sum(1 for v in finals if v < 1e-7)
    n_eqs = 256 + (140 if include_4000 else 0) + 6 * pts_per_pair_22
    print(
        f"[{name}] w2={w2} [vars={n_vars}, eqs={n_eqs}, starts={n_starts}, iters={max_iters}]: "
        f"solved={solved}/{n_starts}, min={min(finals):.3e}, med={float(np.median(finals)):.3e}"
    )
    return solved, min(finals), float(np.median(finals))


def main() -> None:
    t0 = time.time()
    rng = np.random.default_rng(202611219)

    print("=== TEST A: Pure (2,2,0,0) ONLY (NO (4,0,0,0)) [256 + 270 = 526 eqs] ===")
    for w2 in (6, 5, 4, 3):
        run_probe("2200_ONLY", w2, include_4000=False, pts_per_pair_22=45, n_starts=5, max_iters=140, rng=rng)

    print("\n=== TEST B: Deep S2_4000_2200 (220 iters) at w2 = 6 vs w2 = 5 [666 eqs] ===")
    run_probe("S2_DEEP", 6, include_4000=True, pts_per_pair_22=45, n_starts=4, max_iters=220, rng=rng)
    run_probe("S2_DEEP", 5, include_4000=True, pts_per_pair_22=45, n_starts=8, max_iters=220, rng=rng)

    print("\n=== TEST C: Full-Span (2,2,0,0) [100 pts/pair = 600 exact spanning eqs + 256 + 140 = 996 eqs] ===")
    run_probe("S2_FULL100", 6, include_4000=True, pts_per_pair_22=100, n_starts=3, max_iters=150, rng=rng)
    run_probe("S2_FULL100", 5, include_4000=True, pts_per_pair_22=100, n_starts=4, max_iters=150, rng=rng)

    print(f"\n[DONE] Phase 6B Deep Stress-Test finished in {time.time()-t0:.2f}s.")


if __name__ == "__main__":
    main()
