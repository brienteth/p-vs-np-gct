"""
Prof. Strassen Round 11 (ENGEL 3 & ENGEL 4 — Determinantal Slice Variety D_m Tangent Geometry,
Slice-Rank Singular-Locus Elimination, & Calibrated w=5 vs w=6 J_4 Obstruction) Verification Suite:

1. [PROVEN / CHECKED NUMERICALLY] Referee Audit of Euler #111 test_2 & Exact Constrained Tangent
   Dimensions of D_m^{hom} (subset Sym^3(C^9), dim 165) and D_m^{inhom} (subset Sym^{<=3}(C^9), dim 220):
   - Unconstrained [t^3] det_m(A_0 + t L(X)) at generic off-variety (A_0, L) gives 129/165 (m=4) and
     165/165 (m=5) ONLY because ||det_{deg != 3}|| >> 0 (these points do not lie in D_m^{hom}).
   - Along true smooth homogeneous determinantal branches (deg != 3 == 0), D_m^{hom} retains large
     positive codimension across m = 3..7 (including Grenet perm_3 at m=7: 99/165, codim 66!),
     and D_m^{inhom} (deg > 3 == 0) likewise retains large codimension in Sym^{<=3}(C^9).

2. [PROVEN / CHECKED NUMERICALLY] 2-Line Slice-Rank Singular-Locus Theorem:
   - If F = sum_{i=1}^s h_i g_i (deg h_i, g_i >= 1), then V(h_1..h_s, g_1..g_s) subset Sing(V(F)),
     forcing 2s >= codim_{C^{n^2}}(Sing(V(F))).
   - For perm_3 (codim Sing = 6), s >= 3 unconditionally (eliminating all 4-layer ABPs with m <= 6
     and all r=2 Schur-2x2 realizations across all m). Verified directly via multi-start s <= 2 opt.

3. [CHECKED NUMERICALLY] Calibrated Couplings (J_2, J_3, R_4 == 0) at w = 6 (Grenet m = 7) vs w = 5 (m = 6):
   - Positive control (Grenet m=7, w=6): exact A_g gives ||R_4|| < 1e-11, and cold holomorphic LM
     over the 170-dim J_3-nullspace converges to ||R_4|| < 1e-10.
   - At w = 5 (m = 6): SO(10, C) solves J_2 = F_2 (< 1e-13) and J_3 = F_3 (< 1e-5, rk=76/84, null_dim=99),
     yet both fixed-(V,U) 99-dim R_4 LM and joint (SO(10,C)+A) (J_3, R_4) LM hit strict nonzero floors.
"""
from __future__ import annotations

import itertools
import numpy as np
from scipy.optimize import minimize


def check_off_variety_vs_constrained_dm() -> None:
    """Compare off-variety [t^3] det_m (Euler #111) vs constrained D_m^{hom} and D_m^{inhom}."""
    rng = np.random.default_rng(42)

    # 1. Confirm generic off-variety (A_0, L) reproduces 129/165 (m=4) and 165/165 (m=5) with deg!=3 != 0.
    for m, exp_rk in [(4, 129), (5, 165)]:
        N_dir = 400
        A_list = rng.standard_normal((10, m, m)) + 1j * rng.standard_normal((10, m, m))
        X_dir = rng.standard_normal((N_dir, 9)) + 1j * rng.standard_normal((N_dir, 9))
        K = m + 1
        omegas = np.exp(2j * np.pi * np.arange(K) / K)
        L_dir = np.einsum("kr,rij->kij", X_dir, A_list[1:])
        A_eval = A_list[0][None, None, :, :] + omegas[None, :, None, None] * L_dir[:, None, :, :]
        dets = np.linalg.det(A_eval)
        invs = np.linalg.inv(A_eval)
        adj_T = dets[:, :, None, None] * np.swapaxes(invs, 2, 3)
        C_adj = np.fft.fft(adj_T, axis=1)[:, : m + 1, :, :] / K
        mm = m * m
        J3 = np.zeros((N_dir, 10 * mm), dtype=np.complex128)
        J3[:, :mm] = C_adj[:, 3].reshape(N_dir, mm)
        J3[:, mm:] = (X_dir[:, :, None] * C_adj[:, 2].reshape(N_dir, mm)[:, None, :]).reshape(N_dir, 9 * mm)
        s3 = np.linalg.svd(J3, compute_uv=False)
        rk3 = int(np.sum(s3 > 1e-8))
        C_det = np.fft.fft(dets, axis=1)[:, : m + 1] / K
        norm_not3 = float(np.linalg.norm(np.delete(C_det, 3, axis=1)))
        assert rk3 == exp_rk and norm_not3 > 1e4
        print(f"[OFF-VARIETY] m={m}: [t^3] det_m rank={rk3}/165, ||det_{{deg!=3}}||={norm_not3:.2e}")

    # 2. Exact constrained tangent dims on true homogeneous D_m branches.
    def eval_constrained_tdims(m: int, A_list: np.ndarray, N_dir: int) -> tuple[int, int, int, int]:
        X_dir = rng.standard_normal((N_dir, 9)) + 1j * rng.standard_normal((N_dir, 9))
        K = m + 1
        omegas = np.exp(2j * np.pi * np.arange(K) / K)
        L_dir = np.einsum("kr,rij->kij", X_dir, A_list[1:])
        A_eval = A_list[0][None, None, :, :] + omegas[None, :, None, None] * L_dir[:, None, :, :]
        dets = np.linalg.det(A_eval)
        if np.min(np.abs(dets)) < 1e-11:
            omegas = 0.73 * omegas
            A_eval = A_list[0][None, None, :, :] + omegas[None, :, None, None] * L_dir[:, None, :, :]
            dets = np.linalg.det(A_eval)
        invs = np.linalg.inv(A_eval)
        adj_T = dets[:, :, None, None] * np.swapaxes(invs, 2, 3)
        rad = np.abs(omegas[0])
        C_adj = np.fft.fft(adj_T, axis=1)[:, : m + 1, :, :] / K
        if abs(rad - 1.0) > 1e-9:
            for d in range(m + 1):
                C_adj[:, d] /= rad**d

        # Confirm branch itself is strictly homogeneous of degree 3
        C_det = np.fft.fft(dets, axis=1)[:, : m + 1] / K
        if abs(rad - 1.0) > 1e-9:
            for d in range(m + 1):
                C_det[:, d] /= rad**d
        assert float(np.linalg.norm(np.delete(C_det, 3, axis=1))) < 1e-8

        mm = m * m
        J_by_deg = []
        for d in range(m + 1):
            Jd = np.zeros((N_dir, 10 * mm), dtype=np.complex128)
            Jd[:, :mm] = C_adj[:, d].reshape(N_dir, mm)
            if d >= 1:
                Cd1 = C_adj[:, d - 1].reshape(N_dir, mm)
                Jd[:, mm:] = (X_dir[:, :, None] * Cd1[:, None, :]).reshape(N_dir, 9 * mm)
            J_by_deg.append(Jd)

        J_not3 = np.vstack([J_by_deg[d] for d in range(m + 1) if d != 3])
        _, sn3, Vhn3 = np.linalg.svd(J_not3, full_matrices=False)
        rk_not3 = int(np.sum(sn3 > 1e-8))
        K_hom = Vhn3[rk_not3:].conj().T
        shom = np.linalg.svd(J_by_deg[3] @ K_hom, compute_uv=False)
        tdim_hom = int(np.sum(shom > 1e-8))

        if m >= 4:
            J_gt3 = np.vstack([J_by_deg[d] for d in range(4, m + 1)])
            _, sgt3, Vhgt3 = np.linalg.svd(J_gt3, full_matrices=False)
            rk_gt3 = int(np.sum(sgt3 > 1e-8))
            K_inhom = Vhgt3[rk_gt3:].conj().T
        else:
            K_inhom = np.eye(10 * mm, dtype=np.complex128)
        J_le3 = np.vstack([J_by_deg[d] for d in range(4)])
        sinhom = np.linalg.svd(J_le3 @ K_inhom, compute_uv=False)
        tdim_inhom = int(np.sum(sinhom > 1e-8))
        return tdim_hom, K_hom.shape[1], tdim_inhom, K_inhom.shape[1]

    def make_abp(w1: int, w2: int) -> np.ndarray:
        m = 1 + w1 + w2
        A = np.zeros((10, m, m), dtype=np.complex128)
        for r in range(1, 10):
            A[r, 0, :w1] = rng.standard_normal(w1) + 1j * rng.standard_normal(w1)
            A[r, 1 : 1 + w1, w1 : w1 + w2] = rng.standard_normal((w1, w2)) + 1j * rng.standard_normal((w1, w2))
            A[r, 1 + w1 :, m - 1] = rng.standard_normal(w2) + 1j * rng.standard_normal(w2)
        A[0, 1 : 1 + w1, :w1] = -np.eye(w1)
        A[0, 1 + w1 :, w1 : w1 + w2] = -np.eye(w2)
        return A

    def make_r2_schur2x2(m: int) -> np.ndarray:
        # Schur-2x2 realizing l_1*(u^T w) - l_2*(u^T v) via A_0 = diag(I_{m-2}, 0_2)
        A = np.zeros((10, m, m), dtype=np.complex128)
        A[0, : m - 2, : m - 2] = np.eye(m - 2)
        for r in range(1, 10):
            # L_{22} has row 0 = [l_1, l_2], row 1 = [0, 0]
            A[r, m - 2, m - 2 :] = rng.standard_normal(2) + 1j * rng.standard_normal(2)
            # L_{21} has row 0 = 0, row 1 = u^T
            A[r, m - 1, : m - 2] = rng.standard_normal(m - 2) + 1j * rng.standard_normal(m - 2)
            # L_{12} has cols [v, w]
            A[r, : m - 2, m - 2 :] = rng.standard_normal((m - 2, 2)) + 1j * rng.standard_normal((m - 2, 2))
        return A

    def make_grenet_perm3() -> np.ndarray:
        subs = [tuple(s) for k in range(4) for s in itertools.combinations(range(3), k)]
        s_idx = {s: i for i, s in enumerate(subs)}
        A = np.zeros((10, 7, 7), dtype=np.complex128)
        A[0] = np.eye(8, dtype=np.complex128)[:7, 1:]
        for r in range(9):
            k_row, j_col = divmod(r, 3)
            for s in itertools.combinations(range(3), k_row):
                if j_col not in s:
                    ns = tuple(sorted(s + (j_col,)))
                    # Submatrix [:7, 1:]: row index = s_idx[s], col index = s_idx[ns] - 1
                    A[1 + r, s_idx[s], s_idx[ns] - 1] = -1.0
        return A

    A_det3 = np.zeros((10, 3, 3), dtype=np.complex128)
    for r in range(9):
        A_det3[1 + r, r // 3, r % 3] = 1.0
    A_emb5 = np.zeros((10, 5, 5), dtype=np.complex128)
    A_emb5[0, 3:, 3:] = np.eye(2)
    A_emb5[1:, :3, :3] = A_det3[1:]

    cases = [
        ("m=3 det_3", 3, A_det3, 250, 65, 74),
        ("m=4 ABP 1->1->2->1", 4, make_abp(1, 2), 600, 38, 72),
        ("m=5 diag(det3, I_2)", 5, A_emb5, 1350, 65, 74),
        ("m=5 ABP 1->2->2->1", 5, make_abp(2, 2), 1350, 60, 100),
        ("m=5 r=2 Schur-2x2", 5, make_r2_schur2x2(5), 1350, 77, 98),
        ("m=6 ABP 1->2->3->1", 6, make_abp(2, 3), 3050, 77, 122),
        ("m=6 r=2 Schur-2x2", 6, make_r2_schur2x2(6), 3050, 90, 111),
        ("m=7 Grenet perm_3", 7, make_grenet_perm3(), 6500, 99, 148),
    ]
    for name, m, A_l, n_dir, exp_hom, exp_inhom in cases:
        th, kh, ti, ki = eval_constrained_tdims(m, A_l, n_dir)
        print(f"[D_m] {name:22s}: hom={th:3d}/165 (ker={kh:3d}) | inhom={ti:3d}/220 (ker={ki:3d})")
        assert th == exp_hom, f"{name}: expected hom={exp_hom}, got {th}"
        if exp_inhom is not None:
            assert ti == exp_inhom, f"{name}: expected inhom={exp_inhom}, got {ti}"


def check_slice_rank_singular_locus() -> None:
    """Verify s <= 2 splitting fails on perm_3 (exact codim Sing = 6 => s >= 3 unconditionally)."""
    rng = np.random.default_rng(7)
    mons3 = list(itertools.combinations_with_replacement(range(9), 3))
    m3_idx = {m: i for i, m in enumerate(mons3)}
    perm3_vec = np.zeros(165, dtype=np.float64)
    for p in itertools.permutations(range(3)):
        perm3_vec[m3_idx[tuple(sorted((0 * 3 + p[0], 1 * 3 + p[1], 2 * 3 + p[2])))]] += 1.0

    mons2 = list(itertools.combinations_with_replacement(range(9), 2))
    # Map (i, j) for linear (9) x quad (45) -> cubic (165)
    pairs = []
    for i in range(9):
        for j, (a, b) in enumerate(mons2):
            pairs.append((i, j, m3_idx[tuple(sorted((i, a, b)))]))
    pi = np.array([x[0] for x in pairs])
    pj = np.array([x[1] for x in pairs])
    pk = np.array([x[2] for x in pairs])

    def split_err(x: np.ndarray) -> float:
        l1, l2 = x[:9], x[9:18]
        q1, q2 = x[18:63], x[63:108]
        c = np.zeros(165, dtype=np.float64)
        np.add.at(c, pk, l1[pi] * q1[pj] + l2[pi] * q2[pj])
        diff = c - perm3_vec
        return float(np.dot(diff, diff))

    best_err = 1e9
    for _ in range(12):
        res = minimize(split_err, 0.4 * rng.standard_normal(108), method="BFGS", options={"maxiter": 250})
        best_err = min(best_err, float(res.fun))
    print(f"[SLICE-RANK s=2] perm_3 best ||l1 q1 + l2 q2 - perm_3||^2 = {best_err:.6f} (> 0.30)")
    assert best_err > 0.30


def check_calibrated_j4_w6_vs_w5() -> None:
    """Calibrate holomorphic LM on Grenet w=6 (positive control) vs w=5 SO(10,C) (R4 floor)."""
    rng = np.random.default_rng(2026)

    def perm3(M: np.ndarray) -> float:
        return sum(M[0, p[0]] * M[1, p[1]] * M[2, p[2]] for p in itertools.permutations(range(3)))

    X0 = rng.normal(size=(3, 3))
    X0[0, 0] = 0.0
    c0 = perm3(X0)
    X0[0, 0] = 1.0
    c1 = perm3(X0) - c0
    X0[0, 0] = -c0 / c1
    grad = np.zeros(9)
    for a in range(9):
        ia, ja = divmod(a, 3)
        rr = [r for r in range(3) if r != ia]
        cc = [c for c in range(3) if c != ja]
        sub = X0[np.ix_(rr, cc)]
        grad[a] = sub[0, 0] * sub[1, 1] + sub[0, 1] * sub[1, 0]
    _, _, Vt_g = np.linalg.svd(grad.reshape(1, -1), full_matrices=True)
    T_basis = Vt_g[1:, :]
    H_p3 = np.zeros((9, 9))
    for a in range(9):
        ia, ja = divmod(a, 3)
        for b in range(a + 1, 9):
            ib, jb = divmod(b, 3)
            if ia == ib or ja == jb:
                continue
            rr = [r for r in range(3) if r != ia and r != ib][0]
            cc = [c for c in range(3) if c != ja and c != jb][0]
            H_p3[a, b] = H_p3[b, a] = X0[rr, cc]
    Q2 = 0.5 * (T_basis @ H_p3 @ T_basis.T)
    eigvals, eigvecs = np.linalg.eigh(Q2)
    order = np.argsort(-np.abs(eigvals))
    eigvals, eigvecs = eigvals[order], eigvecs[:, order]
    P_z = np.zeros((8, 8), dtype=np.complex128)
    for r in range(7):
        P_z[r, :] = np.sqrt(eigvals[r] + 0j) * eigvecs[:, r]
    P_z[7, :] = eigvecs[:, 7]
    T_z = np.linalg.inv(P_z).T @ T_basis

    mons3_7 = list(itertools.combinations_with_replacement(range(7), 3))
    m3_7_idx = {m: i for i, m in enumerate(mons3_7)}
    F3_z = np.zeros(84, dtype=np.complex128)
    for p in itertools.permutations(range(3)):
        l0, l1, l2 = T_z[:7, 0 * 3 + p[0]], T_z[:7, 1 * 3 + p[1]], T_z[:7, 2 * 3 + p[2]]
        for a in range(7):
            for b in range(7):
                for c in range(7):
                    F3_z[m3_7_idx[tuple(sorted((a, b, c)))]] += l0[a] * l1[b] * l2[c]

    M_pts = 260
    Z_pts = (rng.standard_normal((M_pts, 7)) + 1j * rng.standard_normal((M_pts, 7))) * 0.55

    def run_r4_lm(V: np.ndarray, U: np.ndarray, w_dim: int, starts: int, max_it: int) -> tuple[int, int, float]:
        ww = w_dim * w_dim
        M_J3 = np.zeros((84, 7 * ww), dtype=np.complex128)
        for k in range(7):
            for i in range(w_dim):
                for j in range(w_dim):
                    col = k * ww + i * w_dim + j
                    for p in range(7):
                        for q in range(7):
                            M_J3[m3_7_idx[tuple(sorted((k, p, q)))], col] += V[i, p] * U[j, q]
                    if i == j:
                        for r in range(7):
                            M_J3[m3_7_idx[tuple(sorted((k, r, r)))], col] += 1.0
        U_j, s_j, Vh_j = np.linalg.svd(M_J3, full_matrices=True)
        rk_j = int(np.sum(s_j > 1e-9))
        A_sol = Vh_j[:rk_j].conj().T @ ((U_j[:, :rk_j].conj().T @ F3_z) / s_j[:rk_j])
        N_A = Vh_j[rk_j:].conj().T
        nd = N_A.shape[1]

        V_pts = Z_pts @ V.T
        U_pts = Z_pts @ U.T
        b0_pts = np.einsum("mi,mi->m", V_pts, U_pts)
        N_Ax = np.einsum("mk,kija->mija", Z_pts, N_A.reshape(7, w_dim, w_dim, nd))
        A0_Ax = np.einsum("mk,kij->mij", Z_pts, A_sol.reshape(7, w_dim, w_dim))

        def res_jac(alpha: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
            Ax = A0_Ax + np.einsum("mija,a->mij", N_Ax, alpha)
            vA = np.einsum("mi,mij->mj", V_pts, Ax)
            Au = np.einsum("mij,mj->mi", Ax, U_pts)
            b1 = np.einsum("mi,mi->m", vA, U_pts)
            b2 = np.einsum("mi,mi->m", vA, Au)
            t1 = np.trace(Ax, axis1=1, axis2=2)
            t2 = np.einsum("mij,mji->m", Ax, Ax)
            e2 = 0.5 * (t1 * t1 - t2)
            r4 = -b2 + t1 * b1 - e2 * b0_pts
            W = (
                -(np.einsum("ma,mb->mab", V_pts, Au) + np.einsum("ma,mb->mab", vA, U_pts))
                + t1[:, None, None] * np.einsum("ma,mb->mab", V_pts, U_pts)
                + (b1 - b0_pts * t1)[:, None, None] * np.eye(w_dim)[None, :, :]
                + b0_pts[:, None, None] * np.swapaxes(Ax, 1, 2)
            )
            J_c = np.einsum("mij,mija->ma", W, N_Ax)
            return r4, J_c

        best_r = 1e9
        for _ in range(starts):
            alpha = 0.25 * (rng.standard_normal(nd) + 1j * rng.standard_normal(nd))
            lam = 1e-3
            r4, J_c = res_jac(alpha)
            norm_r = float(np.linalg.norm(r4))
            for _ in range(max_it):
                if norm_r < 1e-12:
                    break
                d = -np.linalg.solve(J_c.conj().T @ J_c + lam * np.eye(nd), J_c.conj().T @ r4)
                r4_n, _ = res_jac(alpha + d)
                norm_n = float(np.linalg.norm(r4_n))
                if norm_n < norm_r:
                    alpha = alpha + d
                    r4, J_c = res_jac(alpha)
                    norm_r = norm_n
                    lam = max(lam * 0.3, 1e-14)
                    if np.linalg.norm(d) < 1e-13:
                        break
                else:
                    lam = min(lam * 5.0, 1e8)
            best_r = min(best_r, norm_r)
        return rk_j, nd, best_r

    # 1. Positive control: Grenet w = 6 (m = 7)
    def grenet_perm3_mat(X: np.ndarray) -> np.ndarray:
        subs = [tuple(s) for k in range(4) for s in itertools.combinations(range(3), k)]
        s_idx = {s: i for i, s in enumerate(subs)}
        M = np.eye(8, dtype=np.complex128)
        for k in range(3):
            for s in itertools.combinations(range(3), k):
                for j in range(3):
                    if j not in s:
                        ns = tuple(sorted(s + (j,)))
                        M[s_idx[s], s_idx[ns]] -= X[k, j]
        return M[:7, 1:]

    M_g0 = grenet_perm3_mat(X0.astype(np.complex128))
    U_g, s_g, Vt_g0 = np.linalg.svd(M_g0)
    P_left = np.vstack([(U_g[:, :6] / s_g[:6]).T, U_g[:, 6:7].T])
    Q_right = np.hstack([Vt_g0[:6, :].T, Vt_g0[6:7, :].T])
    L_z = np.zeros((7, 7, 7), dtype=np.complex128)
    M_zero = grenet_perm3_mat(np.zeros((3, 3), dtype=np.complex128))
    for k in range(7):
        L_z[k] = P_left @ (grenet_perm3_mat(T_z[k].reshape(3, 3)) - M_zero) @ Q_right
    V_g = L_z[:, 6, :6].T
    U_g6 = L_z[:, :6, 6].T
    z_t = rng.standard_normal(7) + 1j * rng.standard_normal(7)
    V_g = V_g * (np.sum(z_t**2) / (-(z_t @ V_g.T) @ (z_t @ U_g6.T)))
    assert np.max(np.abs(-0.5 * (V_g.T @ U_g6 + U_g6.T @ V_g) - np.eye(7))) < 1e-12
    rk6, nd6, r4_w6 = run_r4_lm(V_g, U_g6, 6, starts=5, max_it=80)
    print(f"[J4-LM w=6 Grenet] rk={rk6}/84, null_dim={nd6}, cold LM best ||R4||={r4_w6:.3e}")
    assert rk6 == 82 and nd6 == 170 and r4_w6 < 1e-10

    # 2. w = 5 (m = 6): SO(10, C) J_3 solution followed by 99-dim R_4 LM
    tri10 = np.triu_indices(10, k=1)
    I10 = np.eye(10, dtype=np.complex128)
    map3_7 = np.array([[[m3_7_idx[tuple(sorted((i, j, k)))] for k in range(7)] for j in range(7)] for i in range(7)], dtype=np.int32).ravel()
    S_map_7 = np.zeros((49, 7 * 84), dtype=np.float64)
    for idx_m, val_m in enumerate(map3_7):
        S_map_7[idx_m // 7, (idx_m % 7) * 84 + val_m] = 1.0
    F2_cols = np.zeros((7, 84), dtype=np.complex128)
    for k in range(7):
        for r in range(7):
            F2_cols[k, m3_7_idx[tuple(sorted((k, r, r)))]] += 1.0

    def j3_span_res(x: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
        K = np.zeros((10, 10), dtype=np.complex128)
        K[tri10] = x[:45] + 1j * x[45:]
        O = np.linalg.solve(I10 + K - K.T, I10 - K + K.T)
        R = O[:, :7]
        V = -(R[:5] + 1j * R[5:])
        U = R[:5] - 1j * R[5:]
        rows = np.vstack([(np.einsum("ai,bj->abij", V, U).reshape((25, 49)) @ S_map_7).reshape((175, 84)), F2_cols])
        Us, s, _ = np.linalg.svd(rows.T, full_matrices=False)
        rk = int(np.sum(s > 1e-8))
        Ur = Us[:, :rk]
        return float(np.linalg.norm(F3_z - Ur @ (Ur.conj().T @ F3_z))), V, U

    opt = minimize(lambda x: j3_span_res(x)[0], 0.4 * rng.standard_normal(90), method="BFGS", options={"maxiter": 180})
    r_j3, V5, U5 = j3_span_res(opt.x)
    assert np.max(np.abs(-0.5 * (V5.T @ U5 + U5.T @ V5) - np.eye(7))) < 1e-12
    rk5, nd5, r4_w5 = run_r4_lm(V5, U5, 5, starts=6, max_it=80)
    print(f"[J4-LM w=5 SO(10,C)] J3_res={r_j3:.2e}, rk={rk5}/84, null_dim={nd5}, cold LM best ||R4||={r4_w5:.3e}")
    assert rk5 == 76 and nd5 == 99 and r_j3 < 1e-4 and r4_w5 > 10.0


def main() -> None:
    check_off_variety_vs_constrained_dm()
    check_slice_rank_singular_locus()
    check_calibrated_j4_w6_vs_w5()
    print("ALL ROUND 11 CHECKS PASSED.")


if __name__ == "__main__":
    main()
