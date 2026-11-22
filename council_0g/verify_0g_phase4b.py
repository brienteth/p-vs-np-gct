"""Phase 4B Verification: Non-Row-Separated (Globally Mixed) 4-Layer Homogeneous ABP for perm_4.

Tests:
1. Exact perm_4 evaluation on random complex points X in C^{4x4}.
2. Damped Levenberg-Marquardt search for a completely general NON-ROW-SEPARATED 4-layer
   homogeneous ABP F(X) = L_1(X)_{1 x w1} L_2(X)_{w1 x w2} L_3(X)_{w2 x w3} L_4(X)_{w3 x 1}
   matching perm_4(X) identically at 1,500 generic complex points (Schwartz-Zippel),
   with w1 = 4, w3 = 4, and middle cut width w2 in {4, 5, 6}:
   - Does w2 = 6 solve to 0.0 (recovering Grenet as a special case)?
   - Can global 16-variable mixing break w2 = 5 or w2 = 4, or does it hit a hard residual floor?
"""
from __future__ import annotations

import itertools
import time
from typing import List, Tuple

import numpy as np


def eval_perm4_batch(x_batch: np.ndarray) -> np.ndarray:
    """Evaluate perm_4(X) on a batch of shape (N, 4, 4)."""
    out = np.zeros(x_batch.shape[0], dtype=x_batch.dtype)
    for pi in itertools.permutations(range(4)):
        out += (
            x_batch[:, 0, pi[0]]
            * x_batch[:, 1, pi[1]]
            * x_batch[:, 2, pi[2]]
            * x_batch[:, 3, pi[3]]
        )
    return out


def grenet_w6_params() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Construct exact Grenet 4-layer homogeneous ABP for perm_4 with widths (1, 4, 6, 4, 1)
    where each layer is a tensor of shape (16, rows, cols) over X_flat (0..15).
    """
    # Layer 1 (1 x 4): X_{0, j0} -> node j0 in {0..3}
    l1 = np.zeros((16, 1, 4), dtype=np.complex128)
    for j0 in range(4):
        l1[j0, 0, j0] = 1.0

    # Layer 2 (4 x 6): subsets S of size 2 indexed 0..5: (0,1),(0,2),(0,3),(1,2),(1,3),(2,3)
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    l2 = np.zeros((16, 4, 6), dtype=np.complex128)
    for p_idx, (a, b) in enumerate(pairs):
        # from j0=a, pick X_{1, b}; from j0=b, pick X_{1, a}
        l2[4 + b, a, p_idx] = 1.0
        l2[4 + a, b, p_idx] = 1.0

    # Layer 3 (6 x 4): subsets T of size 3 indexed by missing element j3 in {0..3}
    l3 = np.zeros((16, 6, 4), dtype=np.complex128)
    for p_idx, (a, b) in enumerate(pairs):
        rem = [c for c in range(4) if c not in (a, b)]
        c1, c2 = rem[0], rem[1]
        # add c1 -> T = {a,b,c1}, missing is c2
        l3[8 + c1, p_idx, c2] = 1.0
        # add c2 -> T = {a,b,c2}, missing is c1
        l3[8 + c2, p_idx, c1] = 1.0

    # Layer 4 (4 x 1): missing element j3 -> pick X_{3, j3}
    l4 = np.zeros((16, 4, 1), dtype=np.complex128)
    for j3 in range(4):
        l4[12 + j3, j3, 0] = 1.0

    return l1, l2, l3, l4


def forward_abp_batch(
    x_flat: np.ndarray,
    l1: np.ndarray,
    l2: np.ndarray,
    l3: np.ndarray,
    l4: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Evaluate L1(X) L2(X) L3(X) L4(X) on batch (N, 16) and return intermediates."""
    m1 = np.einsum("nx,xij->nij", x_flat, l1)  # (N, 1, w1)
    m2 = np.einsum("nx,xij->nij", x_flat, l2)  # (N, w1, w2)
    m3 = np.einsum("nx,xij->nij", x_flat, l3)  # (N, w2, w3)
    m4 = np.einsum("nx,xij->nij", x_flat, l4)  # (N, w3, 1)
    m12 = np.einsum("nij,njk->nik", m1, m2)
    m34 = np.einsum("nij,njk->nik", m3, m4)
    val = np.einsum("nij,nji->n", m12, m34)
    return val, m1, m2, m3, m4


def run_global_abp_lm(
    w2: int,
    x_flat: np.ndarray,
    y_target: np.ndarray,
    rng: np.random.Generator,
    w1: int = 4,
    w3: int = 4,
    n_starts: int = 6,
    max_iters: int = 120,
) -> Tuple[int, float, float]:
    """Run complex damped LM for completely non-row-separated 4-layer ABP (1, w1, w2, w3, 1)."""
    n_pts = x_flat.shape[0]
    s1 = 16 * 1 * w1
    s2 = 16 * w1 * w2
    s3 = 16 * w2 * w3
    s4 = 16 * w3 * 1
    n_vars = s1 + s2 + s3 + s4

    def res_and_jac(z: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        l1 = z[0:s1].reshape(16, 1, w1)
        l2 = z[s1 : s1 + s2].reshape(16, w1, w2)
        l3 = z[s1 + s2 : s1 + s2 + s3].reshape(16, w2, w3)
        l4 = z[s1 + s2 + s3 :].reshape(16, w3, 1)

        m1 = np.einsum("nx,xab->nab", x_flat, l1)  # (N, 1, w1)
        m2 = np.einsum("nx,xbc->nbc", x_flat, l2)  # (N, w1, w2)
        m3 = np.einsum("nx,xcd->ncd", x_flat, l3)  # (N, w2, w3)
        m4 = np.einsum("nx,xde->nde", x_flat, l4)  # (N, w3, 1)

        p12 = m1[:, 0, :]  # (N, w1)
        p123 = np.einsum("nb,nbc->nc", p12, m2)  # (N, w2)
        p1234 = np.einsum("nc,ncd->nd", p123, m3)  # (N, w3)
        pred = np.einsum("nd,nd->n", p1234, m4[:, :, 0])

        q34 = m4[:, :, 0]  # (N, w3)
        q234 = np.einsum("ncd,nd->nc", m3, q34)  # (N, w2)
        q1234 = np.einsum("nbc,nc->nb", m2, q234)  # (N, w1)

        f = pred - y_target
        j1 = np.einsum("nx,nb->nxb", x_flat, q1234).reshape(n_pts, s1)
        j2 = np.einsum("nx,nb,nc->nxbc", x_flat, p12, q234).reshape(n_pts, s2)
        j3 = np.einsum("nx,nc,nd->nxcd", x_flat, p123, q34).reshape(n_pts, s3)
        j4 = np.einsum("nx,nd->nxd", x_flat, p1234).reshape(n_pts, s4)

        jc = np.hstack([j1, j2, j3, j4])
        r_real = np.concatenate([f.real, f.imag])
        j_real = np.vstack([np.hstack([jc.real, -jc.imag]), np.hstack([jc.imag, jc.real])])
        return r_real, j_real

    # Analytical Jacobian FD check
    z_chk = 0.4 * (rng.standard_normal(n_vars) + 1j * rng.standard_normal(n_vars))
    r0, j0 = res_and_jac(z_chk)
    eps = 1e-6
    for idx in rng.choice(2 * n_vars, size=8, replace=False):
        dz = np.zeros(2 * n_vars)
        dz[idx] = eps
        dc = dz[:n_vars] + 1j * dz[n_vars:]
        rp, _ = res_and_jac(z_chk + dc)
        rm, _ = res_and_jac(z_chk - dc)
        fd_col = (rp - rm) / (2.0 * eps)
        err = float(np.max(np.abs(j0[:, idx] - fd_col)))
        assert err < 1e-7, f"Jacobian FD mismatch at {idx}: {err}"

    finals: List[float] = []
    for _ in range(n_starts):
        z = 0.45 * (rng.standard_normal(n_vars) + 1j * rng.standard_normal(n_vars))
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
    return solved, min(finals), float(np.median(finals))


def main() -> None:
    t0 = time.time()
    rng = np.random.default_rng(20261121)

    # 1. Self-check Grenet w=6 exactness
    n_pts = 1200
    x_pts = 0.5 * (rng.standard_normal((n_pts, 4, 4)) + 1j * rng.standard_normal((n_pts, 4, 4)))
    x_flat = x_pts.reshape(n_pts, 16)
    y_target = eval_perm4_batch(x_pts)

    g1, g2, g3, g4 = grenet_w6_params()
    g_pred, _, _, _, _ = forward_abp_batch(x_flat, g1, g2, g3, g4)
    g_err = float(np.max(np.abs(g_pred - y_target)))
    assert g_err < 1e-12, f"Grenet exact check failed: {g_err}"
    print(f"[PASS] Grenet (1,4,6,4,1) exactness on {n_pts} complex points: max err = {g_err:.2e}")

    # 2. Non-row-separated global mixing LM search for w2 = 4, 5, 6
    for w2 in (6, 5, 4):
        t_w = time.time()
        solved, min_res, med_res = run_global_abp_lm(w2, x_flat, y_target, rng, n_starts=6, max_iters=100)
        print(
            f"[RESULT] Non-row-separated ABP (1, 4, {w2}, 4, 1) "
            f"[vars={16*(8+8*w2)}, pts={n_pts}]: solved={solved}/6, min={min_res:.6e}, median={med_res:.6e} "
            f"({time.time()-t_w:.2f}s)"
        )

    print(f"\n[DONE] Phase 4B Non-Row-Separated probe completed in {time.time() - t0:.2f}s.")


if __name__ == "__main__":
    main()
