"""Phase 5B: Exact 256-Equation Row-Multilinear (Pi_RowML) Probe for Non-Row-Separated 4-Layer ABPs.

Tests the exact Al-Khwarizmi-Euclid 24-permutation identity:
  Pi_RowML(L1(X) L2(X) L3(X) L4(X)) == perm_4(X)
where each layer L_r(X) = sum_{i=0}^3 L_r^{(i)}(X_i) mixes all 4 rows of X in C^{4x4},
with layer widths (1, w1=4, w2, w3=4, 1) for w2 in {6, 5, 4, 3}.
This eliminates ALL non-row-multilinear garbage monomials (only 256 exact equations!).
"""
from __future__ import annotations

import itertools
import time
from typing import List, Tuple

import numpy as np


def build_perm4_rowml_target() -> np.ndarray:
    """Return target tensor of shape (4, 4, 4, 4) indexed by (c0, c1, c2, c3) for perm_4."""
    t = np.zeros((4, 4, 4, 4), dtype=np.complex128)
    for pi in itertools.permutations(range(4)):
        t[pi[0], pi[1], pi[2], pi[3]] = 1.0
    return t


def eval_rowml_abp(
    l1: np.ndarray, l2: np.ndarray, l3: np.ndarray, l4: np.ndarray
) -> np.ndarray:
    """
    Compute exact Pi_RowML(L1 L2 L3 L4) of shape (4, 4, 4, 4) indexed by (c0, c1, c2, c3).
    Each L_r has shape (4_rows, 4_cols, in_dim, out_dim).
    """
    out = np.zeros((4, 4, 4, 4), dtype=np.complex128)
    for pi in itertools.permutations(range(4)):
        # pi[0] in layer 0, pi[1] in layer 1, pi[2] in layer 2, pi[3] in layer 3
        a0 = l1[pi[0], :, 0, :]  # (4, w1)
        a1 = l2[pi[1], :, :, :]  # (4, w1, w2)
        a2 = l3[pi[2], :, :, :]  # (4, w2, w3)
        a3 = l4[pi[3], :, :, 0]  # (4, w3)
        # Contract inner ABP wires (w1, w2, w3), keeping column indices (c_{pi[0]}, c_{pi[1]}, c_{pi[2]}, c_{pi[3]})
        t = np.einsum("ab,cbg,dgh,eh->acde", a0, a1, a2, a3)
        # Map axes (0,1,2,3) corresponding to rows (pi[0],pi[1],pi[2],pi[3]) back to (row0, row1, row2, row3)
        inv_perm = [0] * 4
        for pos, r in enumerate(pi):
            inv_perm[r] = pos
        out += np.transpose(t, inv_perm)
    return out


def grenet_rowml_params() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Grenet (1,4,6,4,1) in (row, col, in, out) format."""
    l1 = np.zeros((4, 4, 1, 4), dtype=np.complex128)
    for j0 in range(4):
        l1[0, j0, 0, j0] = 1.0

    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    l2 = np.zeros((4, 4, 4, 6), dtype=np.complex128)
    for p_idx, (a, b) in enumerate(pairs):
        l2[1, b, a, p_idx] = 1.0
        l2[1, a, b, p_idx] = 1.0

    l3 = np.zeros((4, 4, 6, 4), dtype=np.complex128)
    for p_idx, (a, b) in enumerate(pairs):
        rem = [c for c in range(4) if c not in (a, b)]
        c1, c2 = rem[0], rem[1]
        l3[2, c1, p_idx, c2] = 1.0
        l3[2, c2, p_idx, c1] = 1.0

    l4 = np.zeros((4, 4, 4, 1), dtype=np.complex128)
    for j3 in range(4):
        l4[3, j3, j3, 0] = 1.0
    return l1, l2, l3, l4


def run_rowml_lm(
    w2: int,
    target: np.ndarray,
    rng: np.random.Generator,
    w1: int = 4,
    w3: int = 4,
    n_starts: int = 8,
    max_iters: int = 120,
) -> Tuple[int, float, float]:
    """Damped complex LM on exact 256-equation Pi_RowML(L1 L2 L3 L4) = perm_4."""
    s1 = 16 * 1 * w1
    s2 = 16 * w1 * w2
    s3 = 16 * w2 * w3
    s4 = 16 * w3 * 1
    n_vars = s1 + s2 + s3 + s4
    target_flat = target.reshape(256)

    # Precompute inverse permutations for all 24 pi in S_4
    perms = list(itertools.permutations(range(4)))
    inv_perms = []
    for pi in perms:
        inv = [0] * 4
        for pos, r in enumerate(pi):
            inv[r] = pos
        inv_perms.append(tuple(inv))

    def res_and_jac(z: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        l1 = z[0:s1].reshape(4, 4, 1, w1)
        l2 = z[s1 : s1 + s2].reshape(4, 4, w1, w2)
        l3 = z[s1 + s2 : s1 + s2 + s3].reshape(4, 4, w2, w3)
        l4 = z[s1 + s2 + s3 :].reshape(4, 4, w3, 1)

        pred = np.zeros((4, 4, 4, 4), dtype=np.complex128)
        j1 = np.zeros((4, 4, 4, 4, 4, 4, w1), dtype=np.complex128)
        j2 = np.zeros((4, 4, 4, 4, 4, 4, w1, w2), dtype=np.complex128)
        j3 = np.zeros((4, 4, 4, 4, 4, 4, w2, w3), dtype=np.complex128)
        j4 = np.zeros((4, 4, 4, 4, 4, 4, w3), dtype=np.complex128)

        for pi, inv in zip(perms, inv_perms):
            r0, r1, r2, r3 = pi
            a0 = l1[r0, :, 0, :]  # (4, w1)
            a1 = l2[r1, :, :, :]  # (4, w1, w2)
            a2 = l3[r2, :, :, :]  # (4, w2, w3)
            a3 = l4[r3, :, :, 0]  # (4, w3)

            # Term in (pos0, pos1, pos2, pos3) coordinates
            term = np.einsum("ab,cbg,dgh,eh->acde", a0, a1, a2, a3)
            pred += np.transpose(term, inv)

            # Analytical derivatives in (pos0, pos1, pos2, pos3) then transpose first 4 axes
            # d/da0[a, b]: a1[c,b,g] a2[d,g,h] a3[e,h] -> (c,d,e,b)
            r_123 = np.einsum("cbg,dgh,eh->cdeb", a1, a2, a3)
            # d/da1[c, b, g]: a0[a, b] * (a2[d,g,h] a3[e,h]) -> a0[a,b], r_23[d,e,g]
            r_23 = np.einsum("dgh,eh->deg", a2, a3)
            # d/da2[d, g, h]: (a0[a,b] a1[c,b,g]) * a3[e,h] -> l_01[a,c,g], a3[e,h]
            l_01 = np.einsum("ab,cbg->acg", a0, a1)
            # d/da3[e, h]: l_012[a,c,d,h]
            l_012 = np.einsum("acg,dgh->acdh", l_01, a2)

            # Map into j1..j4 carefully
            # j1_perm[a, c, d, e, c_in=a, b] = r_123[c, d, e, b]
            j1_p = np.zeros((4, 4, 4, 4, 4, w1), dtype=np.complex128)
            for c0 in range(4):
                j1_p[c0, :, :, :, c0, :] = r_123
            j1[:, :, :, :, r0, :, :] += np.transpose(j1_p, inv + (4, 5))

            j2_p = np.zeros((4, 4, 4, 4, 4, w1, w2), dtype=np.complex128)
            outer_0_23 = np.einsum("ab,deg->adegb", a0, r_23)  # (a, d, e, g, b)
            for c1 in range(4):
                j2_p[:, c1, :, :, c1, :, :] = np.transpose(outer_0_23, (0, 1, 2, 4, 3))
            j2[:, :, :, :, r1, :, :, :] += np.transpose(j2_p, inv + (4, 5, 6))

            j3_p = np.zeros((4, 4, 4, 4, 4, w2, w3), dtype=np.complex128)
            outer_01_3 = np.einsum("acg,eh->acegh", l_01, a3)  # (a, c, e, g, h)
            for c2 in range(4):
                j3_p[:, :, c2, :, c2, :, :] = outer_01_3
            j3[:, :, :, :, r2, :, :, :] += np.transpose(j3_p, inv + (4, 5, 6))

            j4_p = np.zeros((4, 4, 4, 4, 4, w3), dtype=np.complex128)
            for c3 in range(4):
                j4_p[:, :, :, c3, c3, :] = l_012
            j4[:, :, :, :, r3, :, :] += np.transpose(j4_p, inv + (4, 5))

        f = pred.reshape(256) - target_flat
        jc = np.hstack([
            j1.reshape(256, s1),
            j2.reshape(256, s2),
            j3.reshape(256, s3),
            j4.reshape(256, s4),
        ])
        r_real = np.concatenate([f.real, f.imag])
        j_real = np.vstack([np.hstack([jc.real, -jc.imag]), np.hstack([jc.imag, jc.real])])
        return r_real, j_real

    # Analytical Jacobian FD check
    z_chk = 0.35 * (rng.standard_normal(n_vars) + 1j * rng.standard_normal(n_vars))
    _, j0 = res_and_jac(z_chk)
    eps = 1e-6
    for idx in rng.choice(2 * n_vars, size=8, replace=False):
        dz = np.zeros(2 * n_vars)
        dz[idx] = eps
        dc = dz[:n_vars] + 1j * dz[n_vars:]
        rp, _ = res_and_jac(z_chk + dc)
        rm, _ = res_and_jac(z_chk - dc)
        err = float(np.max(np.abs(j0[:, idx] - (rp - rm) / (2.0 * eps))))
        assert err < 1e-7, f"Jacobian FD mismatch at {idx}: {err}"

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
    return solved, min(finals), float(np.median(finals))


def main() -> None:
    t0 = time.time()
    rng = np.random.default_rng(20261121)
    target = build_perm4_rowml_target()

    g1, g2, g3, g4 = grenet_rowml_params()
    g_out = eval_rowml_abp(g1, g2, g3, g4)
    assert np.allclose(g_out, target)
    print("[PASS] Grenet (1,4,6,4,1) exactness under Pi_RowML verified (24 terms).")

    for w2 in (6, 5, 4, 3):
        tw = time.time()
        solved, min_r, med_r = run_rowml_lm(w2, target, rng, n_starts=6, max_iters=100)
        print(
            f"[RESULT] Exact Pi_RowML ABP (1, 4, {w2}, 4, 1) [vars={16*(8+8*w2)}, eqs=256]: "
            f"solved={solved}/6, min={min_r:.6e}, median={med_r:.6e} ({time.time()-tw:.2f}s)"
        )

    print(f"\n[DONE] Phase 5B Exact Pi_RowML probe finished in {time.time()-t0:.2f}s.")


if __name__ == "__main__":
    main()
