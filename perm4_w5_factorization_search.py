"""Wall 1 frontier search: M_1(Y)_{4xw} M_2(Y)_{wx4} = P_perm(Y) for w=4, 5, 6 (m=13, 14, 15)."""
from __future__ import annotations

import itertools
from typing import List, Tuple

import numpy as np

from apolar_higher_betti_probe import rank_matrix_mod
from perm4_middle_factorization_probe import eval_mat_mod, extract_middle_4x4
from poly_exact import Poly, permanent_poly


def build_target_tensor(P_mat: List[List[Poly]]) -> Tuple[np.ndarray, List[Tuple[int, int]]]:
    """Return T of shape (36, 4, 4) and list of 36 unordered pairs (a, b) with 0 <= a <= b < 8."""
    pairs2 = [(a, b) for a in range(8) for b in range(a, 8)]
    pair_to_k = {p: k for k, p in enumerate(pairs2)}
    T = np.zeros((len(pairs2), 4, 4), dtype=np.float64)
    for i in range(4):
        for j in range(4):
            for m, c in P_mat[i][j].items():
                nz = [idx for idx, e in enumerate(m) if e > 0]
                assert sum(m) == 2
                a, b = (nz[0], nz[0]) if len(nz) == 1 else (nz[0], nz[1])
                T[pair_to_k[(a, b)], i, j] = float(c)
    return T, pairs2


def grenet_w6_factors() -> Tuple[np.ndarray, np.ndarray]:
    """Exact Grenet w=6 factors (U_grenet of shape (8,4,6), V_grenet of shape (8,6,4))."""
    U = np.zeros((8, 4, 6), dtype=np.float64)
    V = np.zeros((8, 6, 4), dtype=np.float64)
    subsets2 = list(itertools.combinations(range(4), 2))
    full = {0, 1, 2, 3}
    for s_idx, s2 in enumerate(subsets2):
        for j0 in s2:
            c1 = s2[1] if s2[0] == j0 else s2[0]
            U[c1, j0, s_idx] = 1.0
        for j3 in range(4):
            if j3 in s2:
                continue
            c2 = (full - set(s2) - {j3}).pop()
            V[4 + c2, s_idx, j3] = 1.0
    return U, V


def residual_only(
    U: np.ndarray, V: np.ndarray, T: np.ndarray, pairs2: List[Tuple[int, int]]
) -> np.ndarray:
    UV = np.einsum("aik,bkj->abij", U, V)
    pred = np.empty((len(pairs2), 4, 4), dtype=U.dtype)
    for k, (a, b) in enumerate(pairs2):
        pred[k] = UV[a, b] if a == b else UV[a, b] + UV[b, a]
    return (pred - T).reshape(-1)


def residual_and_jacobian(
    theta: np.ndarray, w: int, T: np.ndarray, pairs2: List[Tuple[int, int]]
) -> Tuple[np.ndarray, np.ndarray]:
    """Holomorphic exact residual (576,) and analytical Jacobian (576, 64*w)."""
    n_u = 8 * 4 * w
    U = theta[:n_u].reshape(8, 4, w)
    V = theta[n_u:].reshape(8, w, 4)
    r = residual_only(U, V, T, pairs2)

    dtype = theta.dtype
    J_U = np.zeros((36, 4, 4, 8, 4, w), dtype=dtype)
    J_V = np.zeros((36, 4, 4, 8, w, 4), dtype=dtype)

    for k, (a, b) in enumerate(pairs2):
        if a == b:
            VaT = V[a].T
            Ua = U[a]
            for i in range(4):
                J_U[k, i, :, a, i, :] += VaT
            for j in range(4):
                J_V[k, :, j, a, :, j] += Ua
        else:
            VaT, VbT = V[a].T, V[b].T
            Ua, Ub = U[a], U[b]
            for i in range(4):
                J_U[k, i, :, a, i, :] += VbT
                J_U[k, i, :, b, i, :] += VaT
            for j in range(4):
                J_V[k, :, j, b, :, j] += Ua
                J_V[k, :, j, a, :, j] += Ub

    J = np.concatenate([J_U.reshape(576, n_u), J_V.reshape(576, n_u)], axis=1)
    return r, J


def run_lm(
    theta0: np.ndarray,
    w: int,
    T: np.ndarray,
    pairs2: List[Tuple[int, int]],
    max_iter: int = 350,
) -> Tuple[float, np.ndarray]:
    theta = theta0.copy()
    lam = 1e-3
    r, J = residual_and_jacobian(theta, w, T, pairs2)
    norm_r = float(np.linalg.norm(r))
    eye = np.eye(len(theta), dtype=theta.dtype)

    for _ in range(max_iter):
        if norm_r < 1e-12:
            break
        JH = J.conj().T
        H = JH @ J
        g = JH @ r
        accepted = False
        for _ in range(12):
            try:
                delta = -np.linalg.solve(H + lam * eye, g)
            except np.linalg.LinAlgError:
                lam *= 10.0
                continue
            cand = theta + delta
            n_u = 8 * 4 * w
            r_cand = residual_only(cand[:n_u].reshape(8, 4, w), cand[n_u:].reshape(8, w, 4), T, pairs2)
            norm_cand = float(np.linalg.norm(r_cand))
            if norm_cand < norm_r:
                theta = cand
                rel_imp = (norm_r - norm_cand) / max(norm_r, 1e-15)
                norm_r = norm_cand
                r, J = residual_and_jacobian(theta, w, T, pairs2)
                lam = max(lam * 0.3, 1e-13)
                accepted = True
                if rel_imp < 1e-13 and float(np.linalg.norm(delta)) < 1e-13:
                    return norm_r, theta
                break
            lam *= 5.0
        if not accepted or lam > 1e10:
            break
    return norm_r, theta


def main() -> None:
    p4 = permanent_poly(4)
    P_perm = extract_middle_4x4(p4)
    T_perm, pairs2 = build_target_tensor(P_perm)

    # Self-check 1: Grenet w=6 exact residual == 0
    Ug, Vg = grenet_w6_factors()
    r_g = residual_only(Ug, Vg, T_perm, pairs2)
    assert np.max(np.abs(r_g)) == 0.0, f"Grenet w=6 residual nonzero: {np.max(np.abs(r_g))}"

    # Self-check 2: F_2 rank-2 collapse of P_perm
    rng_f2 = np.random.default_rng(7)
    max_rk_f2 = 0
    for _ in range(20):
        pt = [int(v) for v in rng_f2.integers(0, 2, size=8)]
        rk = rank_matrix_mod(eval_mat_mod(P_perm, pt, mod=2), mod=2)
        max_rk_f2 = max(max_rk_f2, rk)
    assert max_rk_f2 <= 2

    # Self-check 3: Finite-difference verification of analytical Jacobian (real & complex)
    rng = np.random.default_rng(2026)
    w_chk = 5
    theta_chk = (rng.standard_normal(64 * w_chk) + 1j * rng.standard_normal(64 * w_chk)) * 0.5
    r0, J0 = residual_and_jacobian(theta_chk, w_chk, T_perm, pairs2)
    eps = 1e-7
    max_fd_err = 0.0
    for idx in rng.choice(len(theta_chk), size=20, replace=False):
        e = np.zeros_like(theta_chk)
        e[idx] = eps
        n_u = 8 * 4 * w_chk
        rp = residual_only((theta_chk + e)[:n_u].reshape(8, 4, w_chk), (theta_chk + e)[n_u:].reshape(8, w_chk, 4), T_perm, pairs2)
        rm = residual_only((theta_chk - e)[:n_u].reshape(8, 4, w_chk), (theta_chk - e)[n_u:].reshape(8, w_chk, 4), T_perm, pairs2)
        fd = (rp - rm) / (2 * eps)
        err = float(np.max(np.abs(fd - J0[:, idx])))
        max_fd_err = max(max_fd_err, err)
    assert max_fd_err < 1e-7, f"Jacobian FD check failed: {max_fd_err}"
    print(
        f"[Self-Checks] Grenet w=6 exact residual=0.0 | F_2 max_rk={max_rk_f2}<=2 | "
        f"Jacobian max FD err={max_fd_err:.2e} (OK)\n"
    )

    # Generic Jacobian ranks
    print("=== Generic Jacobian Rank of Factorization Map M_1(Y)_{4xw} M_2(Y)_{wx4} ===")
    print("w | params (64w) | gauge (w^2) | eff_dof (64w-w^2) | rank(J) | codim in C^{576}")
    print("-" * 80)
    for w in (4, 5, 6, 7, 8):
        th = rng.standard_normal(64 * w) + 1j * rng.standard_normal(64 * w)
        _, J = residual_and_jacobian(th, w, T_perm, pairs2)
        rk_j = int(np.linalg.matrix_rank(J, tol=1e-9))
        eff = 64 * w - w * w
        print(f"{w} | {64*w:12d} | {w*w:11d} | {eff:17d} | {rk_j:7d} | {576 - rk_j:16d}")

    print("\n=== Multi-Start Damped Levenberg-Marquardt Search (target: ||r||_2 < 1e-10) ===")
    best_w5_res = float("inf")
    best_w5_theta = None

    for w, n_c, n_r, n_warm in [(6, 5, 0, 0), (4, 8, 0, 0), (5, 15, 5, 5)]:
        residuals: List[float] = []
        scale = 1.0 / np.sqrt(w)
        # Complex starts
        for _ in range(n_c):
            th0 = (rng.standard_normal(64 * w) + 1j * rng.standard_normal(64 * w)) * (scale / np.sqrt(2.0))
            res, th_sol = run_lm(th0, w, T_perm, pairs2)
            residuals.append(res)
            if w == 5 and res < best_w5_res:
                best_w5_res, best_w5_theta = res, th_sol
        # Real starts
        for _ in range(n_r):
            th0 = rng.standard_normal(64 * w) * scale
            res, th_sol = run_lm(th0, w, T_perm, pairs2)
            residuals.append(res)
            if w == 5 and res < best_w5_res:
                best_w5_res, best_w5_theta = res, th_sol
        # Warm starts from truncated Grenet (drop 1 of 6 middle vertices + perturbation)
        for drop_idx in range(n_warm):
            keep = [k for k in range(6) if k != drop_idx]
            u0 = Ug[:, :, keep].astype(np.complex128)
            v0 = Vg[:, keep, :].astype(np.complex128)
            th0 = np.concatenate([u0.reshape(-1), v0.reshape(-1)])
            th0 += (rng.standard_normal(64 * w) + 1j * rng.standard_normal(64 * w)) * 0.15
            res, th_sol = run_lm(th0, w, T_perm, pairs2)
            residuals.append(res)
            if w == 5 and res < best_w5_res:
                best_w5_res, best_w5_theta = res, th_sol

        arr = np.sort(np.array(residuals))
        n_ok = int(np.sum(arr < 1e-10))
        print(
            f"w={w} (starts={len(arr):2d}): min={arr[0]:.3e} | median={np.median(arr):.3e} | "
            f"max={arr[-1]:.3e} | solved(<1e-10)={n_ok}/{len(arr)}"
        )

    if best_w5_res < 1e-8 and best_w5_theta is not None:
        n_u = 8 * 4 * 5
        U5 = best_w5_theta[:n_u].reshape(8, 4, 5)
        V5 = best_w5_theta[n_u:].reshape(8, 5, 4)
        a1 = np.linalg.matrix_rank(U5[:4].reshape(16, 5), tol=1e-7)
        a2 = np.linalg.matrix_rank(U5[4:].reshape(16, 5), tol=1e-7)
        b1 = np.linalg.matrix_rank(V5[:4].reshape(4, 20), tol=1e-7)
        b2 = np.linalg.matrix_rank(V5[4:].reshape(4, 20), tol=1e-7)
        np.savez("w5_candidate.npz", U=U5, V=V5, residual=best_w5_res)
        print(
            f"\n[DISCOVERY!] Found w=5 candidate with ||r||_2={best_w5_res:.3e}! "
            f"Bidegree ranks: U_r1={a1}, U_r2={a2}, V_r1={b1}, V_r2={b2}; saved w5_candidate.npz"
        )


if __name__ == "__main__":
    main()
