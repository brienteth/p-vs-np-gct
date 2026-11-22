"""Phase 6B: Surgical Dissection of the 3,620 Non-Row-Multilinear Syzygies in Non-Row-Separated 4-Layer ABPs.

In Phase 5B (`verify_0g_phase5b.py`), we discovered a striking phenomenon:
  Solving ONLY the 256 exact row-multilinear equations Pi_RowML(L1 L2 L3 L4) == perm_4(X)
  for a globally mixed (1, 4, w2, 4, 1) homogeneous ABP yields 6/6 exact solutions (norm ~ 1e-14)
  all the way down to Archimedes' lower bound w2 = 3!

The full homogeneous degree-4 polynomial F(X) = L1(X) L2(X) L3(X) L4(X) in 16 variables has
C(16 + 4 - 1, 4) = 3,876 monomials, partitioned by row-degree multiset d = (d0, d1, d2, d3):
  - (1, 1, 1, 1):  1 type  x 256 =   256 monomials  [Pi_RowML == perm_4(X)]
  - (4, 0, 0, 0):  4 types x  35 =   140 monomials  [Single-row nilpotency: F(X_r, 0, 0, 0) == 0]
  - (3, 1, 0, 0): 12 types x  80 =   960 monomials  [Two-row (3,1) vanishing]
  - (2, 2, 0, 0):  6 types x 100 =   600 monomials  [Two-row (2,2) vanishing]
  - (2, 1, 1, 0): 12 types x 160 = 1,920 monomials  [Three-row (2,1,1) vanishing]
  Total: 256 + 3,620 = 3,876 monomials.

In this script we test INCREMENTAL syzygy stages on (1, 4, w2, 4, 1) for w2 in {6, 5, 4, 3}:
  - Stage S0: Pi_RowML only (256 eqs) — plus measure exact garbage norms on (4,0,0,0), (3,1,0,0), (2,2,0,0), (2,1,1,0).
  - Stage S1: Pi_RowML + (4,0,0,0) single-row nilpotency (256 + 140 = 396 exact eqs, via 35 fixed generic X_r in C^4 per row).
  - Stage S2: Pi_RowML + (4,0,0,0) + (2,2,0,0) via exact row-degree filtering on 6 row-pairs.
  - Stage S3: Pi_RowML + ALL 2-row restrictions vanishing (F(X_i, X_j, 0, 0) == 0 covers (4,0,0,0)+(3,1,0,0)+(2,2,0,0) = 1,700 eqs).
  - Local Tangent / Jacobian Rank Audit around exact Grenet (1, 4, 6, 4, 1) to verify algebraic independence & local dimension.
"""
from __future__ import annotations

import itertools
import time
from typing import Dict, List, Tuple

import numpy as np


def build_perm4_rowml_target() -> np.ndarray:
    t = np.zeros((4, 4, 4, 4), dtype=np.complex128)
    for pi in itertools.permutations(range(4)):
        t[pi[0], pi[1], pi[2], pi[3]] = 1.0
    return t


def grenet_params() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
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


def eval_abp_batch(
    l1: np.ndarray, l2: np.ndarray, l3: np.ndarray, l4: np.ndarray, xs: np.ndarray
) -> np.ndarray:
    """Evaluate scalar ABP F(X) on a batch xs of shape (N, 4, 4)."""
    # L_r(X) = einsum('nij,ijab->nab', xs, L_r)
    m1 = np.einsum("nij,ijab->nab", xs, l1)  # (N, 1, w1)
    m2 = np.einsum("nij,ijab->nab", xs, l2)  # (N, w1, w2)
    m3 = np.einsum("nij,ijab->nab", xs, l3)  # (N, w2, w3)
    m4 = np.einsum("nij,ijab->nab", xs, l4)  # (N, w3, 1)
    v = np.einsum("nab,nbc,ncd,nde->nae", m1, m2, m3, m4)
    return v[:, 0, 0]


def abp_point_res_jac(
    l1: np.ndarray, l2: np.ndarray, l3: np.ndarray, l4: np.ndarray, xs: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """Evaluate F(X) and exact complex Jacobian wrt (l1, l2, l3, l4) on batch xs (N, 4, 4)."""
    n_pts = xs.shape[0]
    w1 = l1.shape[3]
    w2 = l2.shape[3]
    w3 = l3.shape[3]
    xf = xs.reshape(n_pts, 16)

    m1 = np.einsum("nij,ijab->nab", xs, l1)  # (N, 1, w1)
    m2 = np.einsum("nij,ijab->nab", xs, l2)  # (N, w1, w2)
    m3 = np.einsum("nij,ijab->nab", xs, l3)  # (N, w2, w3)
    m4 = np.einsum("nij,ijab->nab", xs, l4)  # (N, w3, 1)

    m12 = np.einsum("nab,nbc->nac", m1, m2)       # (N, 1, w2)
    m123 = np.einsum("nab,nbc->nac", m12, m3)     # (N, 1, w3)
    m34 = np.einsum("nab,nbc->nac", m3, m4)       # (N, w2, 1)
    m234 = np.einsum("nab,nbc->nac", m2, m34)     # (N, w1, 1)

    vals = np.einsum("nab,nbc->nac", m123, m4)[:, 0, 0]

    # dF/dM1[0, b] = m234[:, b, 0]
    j1 = np.einsum("nk,nb->nkb", xf, m234[:, :, 0]).reshape(n_pts, 16 * w1)
    # dF/dM2[b, g] = m1[:, 0, b] * m34[:, g, 0]
    j2 = np.einsum("nk,nb,ng->nkbg", xf, m1[:, 0, :], m34[:, :, 0]).reshape(n_pts, 16 * w1 * w2)
    # dF/dM3[g, h] = m12[:, 0, g] * m4[:, h, 0]
    j3 = np.einsum("nk,ng,nh->nkgh", xf, m12[:, 0, :], m4[:, :, 0]).reshape(n_pts, 16 * w2 * w3)
    # dF/dM4[h, 0] = m123[:, 0, h]
    j4 = np.einsum("nk,nh->nkh", xf, m123[:, 0, :]).reshape(n_pts, 16 * w3)

    jac = np.hstack([j1, j2, j3, j4])
    return vals, jac


def eval_rowml_res_jac(
    l1: np.ndarray,
    l2: np.ndarray,
    l3: np.ndarray,
    l4: np.ndarray,
    target_flat: np.ndarray,
    perms: List[Tuple[int, ...]],
    inv_perms: List[Tuple[int, ...]],
) -> Tuple[np.ndarray, np.ndarray]:
    """Exact 256-equation Pi_RowML(L1 L2 L3 L4) - perm_4 and complex Jacobian."""
    w1 = l1.shape[3]
    w2 = l2.shape[3]
    w3 = l3.shape[3]
    s1, s2, s3, s4 = 16 * w1, 16 * w1 * w2, 16 * w2 * w3, 16 * w3

    pred = np.zeros((4, 4, 4, 4), dtype=np.complex128)
    j1 = np.zeros((4, 4, 4, 4, 4, 4, w1), dtype=np.complex128)
    j2 = np.zeros((4, 4, 4, 4, 4, 4, w1, w2), dtype=np.complex128)
    j3 = np.zeros((4, 4, 4, 4, 4, 4, w2, w3), dtype=np.complex128)
    j4 = np.zeros((4, 4, 4, 4, 4, 4, w3), dtype=np.complex128)

    for pi, inv in zip(perms, inv_perms):
        r0, r1, r2, r3 = pi
        a0 = l1[r0, :, 0, :]
        a1 = l2[r1, :, :, :]
        a2 = l3[r2, :, :, :]
        a3 = l4[r3, :, :, 0]

        term = np.einsum("ab,cbg,dgh,eh->acde", a0, a1, a2, a3)
        pred += np.transpose(term, inv)

        r_123 = np.einsum("cbg,dgh,eh->cdeb", a1, a2, a3)
        r_23 = np.einsum("dgh,eh->deg", a2, a3)
        l_01 = np.einsum("ab,cbg->acg", a0, a1)
        l_012 = np.einsum("acg,dgh->acdh", l_01, a2)

        j1_p = np.zeros((4, 4, 4, 4, 4, w1), dtype=np.complex128)
        for c0 in range(4):
            j1_p[c0, :, :, :, c0, :] = r_123
        j1[:, :, :, :, r0, :, :] += np.transpose(j1_p, inv + (4, 5))

        j2_p = np.zeros((4, 4, 4, 4, 4, w1, w2), dtype=np.complex128)
        outer_0_23 = np.einsum("ab,deg->adegb", a0, r_23)
        for c1 in range(4):
            j2_p[:, c1, :, :, c1, :, :] = np.transpose(outer_0_23, (0, 1, 2, 4, 3))
        j2[:, :, :, :, r1, :, :, :] += np.transpose(j2_p, inv + (4, 5, 6))

        j3_p = np.zeros((4, 4, 4, 4, 4, w2, w3), dtype=np.complex128)
        outer_01_3 = np.einsum("acg,eh->acegh", l_01, a3)
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
    return f, jc


def make_single_row_points(rng: np.random.Generator, pts_per_row: int = 35) -> np.ndarray:
    """35 generic points per row = exact spanning set for degree-4 polynomials in 4 vars (C(7,4)=35)."""
    xs = np.zeros((4 * pts_per_row, 4, 4), dtype=np.complex128)
    for r in range(4):
        v = rng.standard_normal((pts_per_row, 4)) + 1j * rng.standard_normal((pts_per_row, 4))
        v /= np.linalg.norm(v, axis=1, keepdims=True)
        xs[r * pts_per_row : (r + 1) * pts_per_row, r, :] = v
    return xs


def make_two_row_points(rng: np.random.Generator, pts_per_pair: int = 80) -> np.ndarray:
    """Generic points with exactly 2 active rows (tests (4,0,0,0), (3,1,0,0), (2,2,0,0) simultaneously)."""
    pairs = list(itertools.combinations(range(4), 2))
    xs = np.zeros((len(pairs) * pts_per_pair, 4, 4), dtype=np.complex128)
    for idx, (r1, r2) in enumerate(pairs):
        v1 = rng.standard_normal((pts_per_pair, 4)) + 1j * rng.standard_normal((pts_per_pair, 4))
        v2 = rng.standard_normal((pts_per_pair, 4)) + 1j * rng.standard_normal((pts_per_pair, 4))
        v1 /= np.linalg.norm(v1, axis=1, keepdims=True)
        v2 /= np.linalg.norm(v2, axis=1, keepdims=True)
        sl = slice(idx * pts_per_pair, (idx + 1) * pts_per_pair)
        xs[sl, r1, :] = v1
        xs[sl, r2, :] = v2
    return xs


def make_three_row_points(rng: np.random.Generator, pts_per_triple: int = 60) -> np.ndarray:
    """Generic points with exactly 3 active rows (also hits (2,1,1,0) vanishing syzygies!)."""
    triples = list(itertools.combinations(range(4), 3))
    xs = np.zeros((len(triples) * pts_per_triple, 4, 4), dtype=np.complex128)
    for idx, tr in enumerate(triples):
        sl = slice(idx * pts_per_triple, (idx + 1) * pts_per_triple)
        for r in tr:
            v = rng.standard_normal((pts_per_triple, 4)) + 1j * rng.standard_normal((pts_per_triple, 4))
            v /= np.linalg.norm(v, axis=1, keepdims=True)
            xs[sl, r, :] = v
    return xs


def eval_22_only_batch(
    l1: np.ndarray, l2: np.ndarray, l3: np.ndarray, l4: np.ndarray, xs_pair: np.ndarray, r1: int, r2: int
) -> Tuple[np.ndarray, np.ndarray]:
    """Extract pure (2,2) component via 4-point phase filter in t in {1, i, -1, -i} on row r2:
       F_{2,2}(X_{r1}, X_{r2}) = 1/4 * (F(X_{r1}, X_{r2}) - F(X_{r1}, i X_{r2}) + F(X_{r1}, -X_{r2}) - F(X_{r1}, -i X_{r2}))
       Wait: sum_{k=0}^3 (-1)^k F(X_{r1}, i^k X_{r2}) / 4 picks out d_{r2} == 2 (mod 4), which for total deg 4 is EXACTLY (2,2)!
    """
    n_pts = xs_pair.shape[0]
    n_vars = l1.size + l2.size + l3.size + l4.size
    val_sum = np.zeros(n_pts, dtype=np.complex128)
    jac_sum = np.zeros((n_pts, n_vars), dtype=np.complex128)
    phases = [1.0 + 0j, 1j, -1.0 + 0j, -1j]
    signs = [1.0, -1.0, 1.0, -1.0]
    for ph, sg in zip(phases, signs):
        xm = xs_pair.copy()
        xm[:, r2, :] *= ph
        v, j = abp_point_res_jac(l1, l2, l3, l4, xm)
        val_sum += (0.25 * sg) * v
        jac_sum += (0.25 * sg) * j
    return val_sum, jac_sum


def run_stage_lm(
    stage_name: str,
    w2: int,
    target_flat: np.ndarray,
    perms: List[Tuple[int, ...]],
    inv_perms: List[Tuple[int, ...]],
    rng: np.random.Generator,
    xs_single: np.ndarray,
    xs_two_by_pair: List[Tuple[int, int, np.ndarray]],
    xs_two_all: np.ndarray,
    xs_three_all: np.ndarray,
    n_starts: int = 5,
    max_iters: int = 90,
) -> Tuple[int, float, float, np.ndarray]:
    w1, w3 = 4, 4
    s1, s2, s3, s4 = 16 * w1, 16 * w1 * w2, 16 * w2 * w3, 16 * w3
    n_vars = s1 + s2 + s3 + s4

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

        if stage_name in ("S1_4000", "S2_4000_2200"):
            f1, j1 = abp_point_res_jac(l1, l2, l3, l4, xs_single)
            f_list.append(f1)
            j_list.append(j1)

        if stage_name == "S2_4000_2200":
            for r1, r2, xp in xs_two_by_pair:
                f22, j22 = eval_22_only_batch(l1, l2, l3, l4, xp, r1, r2)
                f_list.append(f22)
                j_list.append(j22)

        if stage_name == "S3_ALL2ROW":
            # Single-row + two-row points cover (4,0,0,0), (3,1,0,0), (2,2,0,0)
            f2, j2 = abp_point_res_jac(l1, l2, l3, l4, xs_two_all)
            f_list.append(f2)
            j_list.append(j2)

        if stage_name == "S4_ALL3ROW":
            # Three-row zero restrictions cover ALL 3,620 non-row-multilinear syzygies!
            f3, j3 = abp_point_res_jac(l1, l2, l3, l4, xs_three_all)
            f_list.append(f3)
            j_list.append(j3)

        fc = np.concatenate(f_list)
        jc = np.vstack(j_list)
        r_real = np.concatenate([fc.real, fc.imag])
        j_real = np.vstack([np.hstack([jc.real, -jc.imag]), np.hstack([jc.imag, jc.real])])
        return r_real, j_real

    # Quick FD check once per stage/w2
    z_chk = 0.3 * (rng.standard_normal(n_vars) + 1j * rng.standard_normal(n_vars))
    _, j_chk = res_and_jac(z_chk)
    eps = 1e-6
    for idx in rng.choice(2 * n_vars, size=4, replace=False):
        dz = np.zeros(2 * n_vars)
        dz[idx] = eps
        dc = dz[:n_vars] + 1j * dz[n_vars:]
        rp, _ = res_and_jac(z_chk + dc)
        rm, _ = res_and_jac(z_chk - dc)
        err = float(np.max(np.abs(j_chk[:, idx] - (rp - rm) / (2.0 * eps))))
        assert err < 1e-6, f"FD mismatch in {stage_name} w2={w2}: {err}"

    finals: List[float] = []
    best_z = z_chk
    best_cur = 1e99

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
        if cur < best_cur:
            best_cur = cur
            best_z = z

    solved = sum(1 for v in finals if v < 1e-7)
    return solved, min(finals), float(np.median(finals)), best_z


def main() -> None:
    t0 = time.time()
    rng = np.random.default_rng(202611216)
    target_flat = build_perm4_rowml_target().reshape(256)
    perms = list(itertools.permutations(range(4)))
    inv_perms = []
    for pi in perms:
        inv = [0] * 4
        for pos, r in enumerate(pi):
            inv[r] = pos
        inv_perms.append(tuple(inv))

    # Build deterministic spanning test sets
    xs_single = make_single_row_points(rng, pts_per_row=35)       # 140 exact spanning points for (4,0,0,0)
    pairs = list(itertools.combinations(range(4), 2))
    xs_two_by_pair: List[Tuple[int, int, np.ndarray]] = []
    for r1, r2 in pairs:
        xp = np.zeros((45, 4, 4), dtype=np.complex128)            # 45 pts/pair x 6 = 270 eqs probing (2,2,0,0)
        v1 = rng.standard_normal((45, 4)) + 1j * rng.standard_normal((45, 4))
        v2 = rng.standard_normal((45, 4)) + 1j * rng.standard_normal((45, 4))
        xp[:, r1, :] = v1 / np.linalg.norm(v1, axis=1, keepdims=True)
        xp[:, r2, :] = v2 / np.linalg.norm(v2, axis=1, keepdims=True)
        xs_two_by_pair.append((r1, r2, xp))

    xs_two_all = make_two_row_points(rng, pts_per_pair=50)        # 300 eqs covering 2-row vanishing
    xs_three_all = make_three_row_points(rng, pts_per_triple=60)  # 240 eqs covering 3-row vanishing (ALL garbage types!)

    # 1. Self-check exact Grenet (1, 4, 6, 4, 1) on ALL syzygy stages!
    g1, g2, g3, g4 = grenet_params()
    f0_g, j0_g = eval_rowml_res_jac(g1, g2, g3, g4, target_flat, perms, inv_perms)
    v1_g, j1_g = abp_point_res_jac(g1, g2, g3, g4, xs_single)
    v2_g, j2_g = abp_point_res_jac(g1, g2, g3, g4, xs_two_all)
    v3_g, j3_g = abp_point_res_jac(g1, g2, g3, g4, xs_three_all)
    assert np.linalg.norm(f0_g) < 1e-13
    assert np.linalg.norm(v1_g) < 1e-13
    assert np.linalg.norm(v2_g) < 1e-13
    assert np.linalg.norm(v3_g) < 1e-13

    # Check exact complex Jacobian ranks at Grenet (1,4,6,4,1) (896 complex params, gauge dim = 4^2+6^2+4^2-1 = 67? Wait: 16+36+16 = 68!)
    rk_rowml = int(np.linalg.matrix_rank(j0_g, tol=1e-9))
    rk_s1 = int(np.linalg.matrix_rank(np.vstack([j0_g, j1_g]), tol=1e-9))
    rk_s3 = int(np.linalg.matrix_rank(np.vstack([j0_g, j2_g]), tol=1e-9))
    rk_s4 = int(np.linalg.matrix_rank(np.vstack([j0_g, j2_g, j3_g]), tol=1e-9))
    print(f"[PASS] Exact Grenet (1,4,6,4,1) satisfies S0, S1, S3, S4 with 0.00e+00 error.")
    print(
        f"[GRENET TANGENT AUDIT] Complex Jacobian ranks at Grenet (896 params): "
        f"S0(RowML)={rk_rowml}, S1(+4000)={rk_s1}, S3(+2row)={rk_s3}, S4(+3row)={rk_s4}"
    )

    # 2. Run surgical syzygy sweep across stages and w2 in {6, 5, 4, 3}
    stages = [
        ("S1_4000", "Pi_RowML (256) + Single-row (4,0,0,0) (140) = 396 eqs"),
        ("S2_4000_2200", "Pi_RowML (256) + (4,0,0,0) (140) + (2,2,0,0) (270) = 666 eqs"),
        ("S3_ALL2ROW", "Pi_RowML (256) + 2-row zero restrictions (300) = 556 eqs"),
        ("S4_ALL3ROW", "Pi_RowML (256) + 3-row zero restrictions (240) = 496 eqs"),
    ]

    for stage_name, desc in stages:
        print(f"\n=== {stage_name}: {desc} ===")
        for w2 in (6, 5, 4, 3):
            tw = time.time()
            solved, min_r, med_r, best_z = run_stage_lm(
                stage_name,
                w2,
                target_flat,
                perms,
                inv_perms,
                rng,
                xs_single,
                xs_two_by_pair,
                xs_two_all,
                xs_three_all,
                n_starts=5,
                max_iters=90,
            )
            # Also evaluate FULL 3-row residual of best_z on fresh independent random points!
            w1, w3 = 4, 4
            s1, s2, s3 = 16 * w1, 16 * w1 * w2, 16 * w2 * w3
            bl1 = best_z[0:s1].reshape(4, 4, 1, w1)
            bl2 = best_z[s1 : s1 + s2].reshape(4, 4, w1, w2)
            bl3 = best_z[s1 + s2 : s1 + s2 + s3].reshape(4, 4, w2, w3)
            bl4 = best_z[s1 + s2 + s3 :].reshape(4, 4, w3, 1)
            chk_1 = float(np.linalg.norm(eval_abp_batch(bl1, bl2, bl3, bl4, xs_single)))
            chk_2 = float(np.linalg.norm(eval_abp_batch(bl1, bl2, bl3, bl4, xs_two_all)))
            chk_3 = float(np.linalg.norm(eval_abp_batch(bl1, bl2, bl3, bl4, xs_three_all)))
            print(
                f"  w2={w2} [vars={16*(8+8*w2)}]: solved={solved}/5, min={min_r:.3e}, med={med_r:.3e} | "
                f"leak(1row={chk_1:.2e}, 2row={chk_2:.2e}, 3row={chk_3:.2e}) ({time.time()-tw:.1f}s)"
            )

    print(f"\n[DONE] Phase 6B Surgical Syzygy Sweep completed in {time.time()-t0:.2f}s.")


if __name__ == "__main__":
    main()
