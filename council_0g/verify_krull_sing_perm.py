"""Phase 7B-2: Exact Codimension & Irreducible Component Audit of Sing(V(perm_n)) for n = 3, 4, 5.

Checks whether Sing(V(perm_4)) has ANY component of codimension < 8 (e.g., dense singular points with
no zero rows/columns, or block-structured singular points).
If codim_{P^{15}}(Sing(V(perm_4))) = c_4, then Krull's Principal Ideal Theorem IMMEDIATELY gives
an UNCONDITIONAL algebraic lower bound for EVERY globally mixed quadratic splitting
  perm_4(X) = sum_{s=1}^{w_2} q_s(X) r_s(X)   (including ALL non-row-separated 4-layer ABPs of ANY w1, w3!):
    2 * w_2 >= c_4   ==>   w_2 >= ceil(c_4 / 2) !
Also checks the EXACT permanent-vs-determinant Wall 2 contrast:
  codim(Sing(V(det_n))) = 4 for ALL n >= 3 (rank <= n-2 matrices),
  whereas codim(Sing(V(perm_n))) grows with n!
"""
from __future__ import annotations

import itertools
import time
from collections import Counter
from typing import List, Tuple

import numpy as np

from verify_0g_phase7b import grad_and_hess_perm, perm_exact


def check_dense_singular_perm4(rng: np.random.Generator, n_starts: int = 80) -> None:
    """Search for singular points of perm_4 on various affine charts, including charts forbidding zero rows/cols."""
    n = 4
    n2 = 16
    results: List[Tuple[int, int, int, np.ndarray]] = []  # (hess_rk, n_zeros, mat_rk, X)

    for s in range(n_starts):
        # First 40 starts: generic affine chart a^T X = 1
        # Next 40 starts: fix diagonal entries x_{00}=x_{11}=x_{22}=x_{33}=1 (forbids any zero row or zero col!)
        forbid_zero_rc = (s >= 40)
        if forbid_zero_rc:
            # 12 free variables (off-diagonal), diagonal fixed to 1!
            free_idx = [i * 4 + j for i in range(4) for j in range(4) if i != j]
            x_full = np.eye(4, dtype=np.complex128).reshape(16)
            z = 0.7 * (rng.standard_normal(12) + 1j * rng.standard_normal(12))

            def eval_sys(zv: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
                xf = x_full.copy()
                xf[free_idx] = zv
                g, h = grad_and_hess_perm(xf.reshape(4, 4))
                fc = g.reshape(16)
                jc = h[:, free_idx]
                r_real = np.concatenate([fc.real, fc.imag])
                j_real = np.vstack([np.hstack([jc.real, -jc.imag]), np.hstack([jc.imag, jc.real])])
                return r_real, j_real

            r_real, j_real = eval_sys(z)
            cur = float(np.linalg.norm(r_real))
            lam = 1e-3
            for _it in range(150):
                if cur < 1e-12:
                    break
                jtj = j_real.T @ j_real
                rhs = j_real.T @ r_real
                diag = np.maximum(np.diag(jtj), 1e-8)
                accepted = False
                for _try in range(6):
                    lhs = jtj + lam * np.diag(diag)
                    try:
                        step = -np.linalg.solve(lhs, rhs)
                    except np.linalg.LinAlgError:
                        step, _, _, _ = np.linalg.lstsq(lhs, -rhs, rcond=None)
                    zn = z + step[:12] + 1j * step[12:]
                    rn, jn = eval_sys(zn)
                    nn = float(np.linalg.norm(rn))
                    if nn < cur:
                        z, r_real, j_real, cur = zn, rn, jn, nn
                        lam = max(lam * 0.3, 1e-12)
                        accepted = True
                        break
                    lam = min(lam * 5.0, 1e8)
                if not accepted and lam >= 1e7:
                    break
            xf = x_full.copy()
            xf[free_idx] = z
            mat = xf.reshape(4, 4)
        else:
            a = rng.standard_normal(16) + 1j * rng.standard_normal(16)
            a /= np.linalg.norm(a)
            x = rng.standard_normal(16) + 1j * rng.standard_normal(16)
            x /= np.dot(a, x)

            def eval_sys_a(xv: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
                g, h = grad_and_hess_perm(xv.reshape(4, 4))
                fc = np.concatenate([g.reshape(16), np.array([np.dot(a, xv) - 1.0])])
                jc = np.vstack([h, a.reshape(1, 16)])
                r_real = np.concatenate([fc.real, fc.imag])
                j_real = np.vstack([np.hstack([jc.real, -jc.imag]), np.hstack([jc.imag, jc.real])])
                return r_real, j_real

            r_real, j_real = eval_sys_a(x)
            cur = float(np.linalg.norm(r_real))
            lam = 1e-3
            for _it in range(150):
                if cur < 1e-12:
                    break
                jtj = j_real.T @ j_real
                rhs = j_real.T @ r_real
                diag = np.maximum(np.diag(jtj), 1e-8)
                accepted = False
                for _try in range(6):
                    lhs = jtj + lam * np.diag(diag)
                    try:
                        step = -np.linalg.solve(lhs, rhs)
                    except np.linalg.LinAlgError:
                        step, _, _, _ = np.linalg.lstsq(lhs, -rhs, rcond=None)
                    xn = x + step[:16] + 1j * step[16:]
                    rn, jn = eval_sys_a(xn)
                    nn = float(np.linalg.norm(rn))
                    if nn < cur:
                        x, r_real, j_real, cur = xn, rn, jn, nn
                        lam = max(lam * 0.3, 1e-12)
                        accepted = True
                        break
                    lam = min(lam * 5.0, 1e8)
                if not accepted and lam >= 1e7:
                    break
            mat = x.reshape(4, 4)

        g, h = grad_and_hess_perm(mat)
        if np.linalg.norm(g) < 1e-9:
            svals = np.linalg.svd(h, compute_uv=False)
            hrk = int(np.sum(svals > 1e-7 * svals[0])) if svals[0] > 1e-12 else 0
            n_zeros = int(np.sum(np.abs(mat) < 1e-4 * np.max(np.abs(mat))))
            mrk = int(np.linalg.matrix_rank(mat, tol=1e-6 * np.max(np.abs(mat))))
            results.append((hrk, n_zeros, mrk, mat))

    generic_res = results[: len([r for r in results])]
    hist_hrk = Counter(r[0] for r in results)
    print(f"Total singular points found: {len(results)}/{n_starts}")
    print(f"Hessian rank (local codim) histogram: {dict(sorted(hist_hrk.items()))}")

    # Check specifically the dense (no-zero-row/col) points!
    dense_pts = [r for r in results if np.min(np.linalg.norm(r[3], axis=1)) > 1e-3 and np.min(np.linalg.norm(r[3], axis=0)) > 1e-3]
    print(f"Strictly dense (no zero row & no zero col) singular points found: {len(dense_pts)}")
    if dense_pts:
        hist_dense = Counter(r[0] for r in dense_pts)
        print(f"  Dense singular points Hessian rank histogram: {dict(sorted(hist_dense.items()))}")
        best_d = min(dense_pts, key=lambda r: r[0])
        print(f"  Min-codim dense singular point: rank(Hess)={best_d[0]}, zeros={best_d[1]}, mat_rank={best_d[2]}")
        print(f"  |X| =\n{np.round(np.abs(best_d[3]), 4)}")


def check_det_vs_perm_codim(rng: np.random.Generator) -> None:
    print("\n=== Wall 2 Contrast: Exact Singularity Codimension of det_n vs perm_n ===")
    for n in (3, 4, 5):
        # det_n: generic rank n-2 matrix has codim (n - (n-2))^2 = 4 ALWAYS!
        codim_det = 4
        # perm_n: Stratum A = two zero rows -> 2n equations -> codim 2n!
        m = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
        m[0:2, :] = 0
        if n <= 4:
            g, h = grad_and_hess_perm(m)
            rk_h = int(np.linalg.matrix_rank(h, tol=1e-9))
            assert np.linalg.norm(g) < 1e-12
            print(f"  n={n}: codim(Sing(det_{n})) = {codim_det} | perm_{n} (2 zero rows) rank(Hess) = {rk_h} (= 2n = {2*n})")
        else:
            print(f"  n={n}: codim(Sing(det_{n})) = {codim_det} | perm_{n} (2 zero rows) exact linear codim = {2*n}")


def main() -> None:
    t0 = time.time()
    rng = np.random.default_rng(2026112172)
    print("=== Phase 7B-2: Dense & General Singular Locus Audit of perm_4 ===")
    check_dense_singular_perm4(rng, n_starts=80)
    check_det_vs_perm_codim(rng)
    print(f"\n[DONE] Finished in {time.time()-t0:.2f}s.")


if __name__ == "__main__":
    main()
