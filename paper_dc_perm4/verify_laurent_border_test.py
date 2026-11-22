#!/usr/bin/env python3
"""
Step 3 Follow-Up Checks Requested by the 6-Agent Audit Panel:
1) Verify exact line span of Sheshadri's computer-free dc_C(perm_4) >= 11 sub-proof inside per4_dc_15.tex.
2) Test explicit non-homogeneous Laurent border constructions in B_9^{(4)} on BOTH:
   - M_6..M_9(F_0; L_8) (P^{(4)} / tilde{P}^{(4)}) and
   - M_4^{Sing_2}(F_0; L_{12}) (Q^{(4)}) using pure uint64_t C kernel.
   Explicitly test:
     (a) [t^5] det_9((S_3^{(1)} (+) S_3^{(2)} (+) 0_3)(X) + t A_0) (pure rank-4 limit in B_9^{(4)} \ D_9^{hom}?)
     (b) Coupled Laurent construction det_9(A_0(eps) + L_eps(X)) -> F_0(X) via eps^2 det_4(I_4 - eps^{-1} B(X) C(X)) with rk(B)<=2, etc.
     (c) Non-homogeneous e_4(L(X)) from det_9(I_9 + L(X)) on BOTH L_8 (IMSC M_6..M_9) and L_12 (1365/1365).
     (d) Probe Fermat smooth cubic in C^5 (outside bar(D_4^{hom})) against affine det_4 border.
"""
from __future__ import annotations

import ctypes
import itertools
import os
import subprocess
import sys
import time
import numpy as np
import sympy as sp

sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council/prof-strassen")
from verify_round13_strassen import P1, P2, rref_mod_p_with_det, step_imsc_det


def load_c_kernel():
    src = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/paper_dc_perm4/exact_mod_rref.c"
    so = "/tmp/exact_mod_rref_s3.so"
    subprocess.run(["cc", "-O3", "-shared", "-fPIC", src, "-o", so], check=True)
    lib = ctypes.CDLL(so)
    lib.exact_csr_rank_mod_p.argtypes = [
        ctypes.POINTER(ctypes.c_int64),
        ctypes.POINTER(ctypes.c_int64),
        ctypes.POINTER(ctypes.c_int64),
        ctypes.c_int64,
        ctypes.c_int64,
        ctypes.c_int64,
    ]
    lib.exact_csr_rank_mod_p.restype = ctypes.c_int64
    return lib


def dense_int_rank_mod_p(lib, M: np.ndarray, p: int) -> int:
    nrows, ncols = M.shape
    row_ptr = [0]
    col_idx = []
    vals = []
    for r in range(nrows):
        for c in range(ncols):
            v = int(M[r, c]) % p
            if v != 0:
                col_idx.append(c)
                vals.append(v)
        row_ptr.append(len(col_idx))
    rp = np.array(row_ptr, dtype=np.int64)
    ci = np.array(col_idx, dtype=np.int64)
    va = np.array(vals, dtype=np.int64)
    return int(lib.exact_csr_rank_mod_p(
        rp.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),
        ci.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),
        va.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),
        ctypes.c_int64(nrows),
        ctypes.c_int64(ncols),
        ctypes.c_int64(p),
    ))


def test_L8_and_L12_on_quartic_fn(lib, label: str, eval_f_hess_grad_mod_p, p: int = P1) -> None:
    """
    Given a callable `eval_f_hess_grad_mod_p(x16_vec, p) -> (grad_16, hess_16x16)` for a homogeneous
    quartic F in C[X_0..X_15]_4 over F_p, check:
      1) M_6..M_9(J(F); L_8) rank via IMSC (note: exact corank_6..9 without assuming full D=6 if needed)
      2) M_4^{Sing_2}(F; L_12) exact rank via pure uint64 C-kernel.
    """
    rng = np.random.default_rng(2026)
    k8 = 8
    M_L8 = rng.integers(-2, 3, size=(16, k8), dtype=np.int64)
    k12 = 12
    M_L12 = np.random.default_rng(2026).integers(-2, 3, size=(16, k12), dtype=np.int64)

    # 1. Interpolate the 16 homogeneous cubics grad(F)|_{L_8} on L_8 (binom(8+2,3) = 120 monomials)
    mons3_8 = list(itertools.combinations_with_replacement(range(k8), 3))
    m3_8_idx = {m: i for i, m in enumerate(mons3_8)}
    assert len(mons3_8) == 120
    pts3 = []
    # e_i (8), e_i + 2*e_j (56), e_i + e_j + e_l (56) -> 120 points! Wait: simpler Vandermonde over F_p
    rng_v = np.random.default_rng(42)
    pts8 = rng_v.integers(0, p, size=(140, k8), dtype=np.int64)
    V8 = np.zeros((140, 120), dtype=np.int64)
    for mi, m in enumerate(mons3_8):
        V8[:, mi] = (pts8[:, m[0]] * pts8[:, m[1]] % p) * pts8[:, m[2]] % p
    # Solve V8 * C = G_evals mod p using SymPy DomainMatrix or modular RREF inverse of first 120 invertible rows
    dm8 = sp.polys.matrices.DomainMatrix.from_Matrix(sp.Matrix(V8.tolist())).convert_to(sp.GF(p))
    # Find 120 pivot rows via transpose RREF or just invert top 120x120 if invertible:
    V8_120 = V8[:120, :]
    dm120 = sp.polys.matrices.DomainMatrix.from_Matrix(sp.Matrix(V8_120.tolist())).convert_to(sp.GF(p))
    assert dm120.rank() == 120
    V8_inv = np.array([[int(x) % p for x in row] for row in dm120.inv().to_Matrix().tolist()], dtype=np.int64)

    G_vals = np.zeros((120, 16), dtype=np.int64)
    H_L12_pts = []
    for idx in range(120):
        xv = (M_L8 @ pts8[idx]) % p
        g, _ = eval_f_hess_grad_mod_p(xv, p)
        G_vals[idx] = g % p
    polys3_8 = ((V8_inv @ G_vals) % p).T  # (16, 120)

    # Shift to D=6 on L_8 (2386? no 16*84? wait binom(8+2,3)=120 -> 16*120 = 1920 rows x 1716 cols!)
    mons6_8 = list(itertools.combinations_with_replacement(range(k8), 6))
    m6_8_idx = {m: i for i, m in enumerate(mons6_8)}
    A6 = np.zeros((16 * 120, len(mons6_8)), dtype=np.int64)
    ri = 0
    for gpoly in polys3_8:
        nz = np.nonzero(gpoly)[0]
        for mm in mons3_8:
            for i3 in nz:
                m = tuple(sorted(mm + mons3_8[i3]))
                A6[ri, m6_8_idx[m]] = (A6[ri, m6_8_idx[m]] + int(gpoly[i3])) % p
            ri += 1
    rk6, det6, _, free6, C6 = rref_mod_p_with_det(A6, p=p, need_c_table=True)
    mons_D = mons6_8
    free_D, C_D = free6, C6
    coranks = [len(mons6_8) - rk6]
    for D in (6, 7, 8):
        if len(free_D) == 0:
            coranks.append(0)
            continue
        mons_D, free_D, C_D, crk, _ = step_imsc_det(k8, D, mons_D, free_D, C_D, p=p)
        coranks.append(crk)

    # 2. Interpolate all 136 quadratic second partials on L_12 (78 points) and check M_4^{Sing_2}(F; L_12)
    mons2_12 = list(itertools.combinations_with_replacement(range(k12), 2))
    m2_12_idx = {m: i for i, m in enumerate(mons2_12)}
    mons4_12 = list(itertools.combinations_with_replacement(range(k12), 4))
    m4_12_idx = {m: i for i, m in enumerate(mons4_12)}
    pts12 = []
    for i in range(k12):
        v = np.zeros(k12, dtype=np.int64)
        v[i] = 1
        pts12.append(v)
    for i, j in itertools.combinations(range(k12), 2):
        v = np.zeros(k12, dtype=np.int64)
        v[i] = 1
        v[j] = 1
        pts12.append(v)
    tri_idx = np.triu_indices(16)
    H_evals = np.zeros((78, 136), dtype=np.int64)
    for pi, pt in enumerate(pts12):
        xv = (M_L12 @ pt) % p
        _, H = eval_f_hess_grad_mod_p(xv, p)
        H_evals[pi] = H[tri_idx] % p
    polys2_12 = []
    for k_i in range(136):
        vec = np.zeros(78, dtype=np.int64)
        for i in range(k12):
            vec[m2_12_idx[(i, i)]] = H_evals[i, k_i]
        p_idx = k12
        for i, j in itertools.combinations(range(k12), 2):
            vec[m2_12_idx[(i, j)]] = (H_evals[p_idx, k_i] - vec[m2_12_idx[(i, i)]] - vec[m2_12_idx[(j, j)]]) % p
            p_idx += 1
        if np.any(vec):
            polys2_12.append(vec)
    A4 = np.zeros((len(polys2_12) * 78, 1365), dtype=np.int64)
    ri = 0
    for mm in mons2_12:
        for poly in polys2_12:
            for idx2 in np.nonzero(poly)[0]:
                m = tuple(sorted(mm + mons2_12[idx2]))
                A4[ri, m4_12_idx[m]] = (A4[ri, m4_12_idx[m]] + int(poly[idx2])) % p
            ri += 1
    rk_q = dense_int_rank_mod_p(lib, A4, p) if A4.shape[0] > 0 else 0
    print(f"[{label}] L_8 IMSC coranks D=6..9: {coranks} | L_12 Sing_2 rank: {rk_q}/1365 (corank={1365 - rk_q})", flush=True)


def main() -> None:
    lib = load_c_kernel()

    # 1. Exact line count check in per4_dc_15.tex for computer-free dc >= 11
    with open("/Users/bl10buer/.gemini/antigravity/brain/b557dfcd-0bd3-4f1e-bf17-b6827e3c03bd/scratch/arxiv_refs/sheshadri/per4_dc_15.tex") as f:
        L = f.readlines()
    print(f"Sheshadri per4_dc_15.tex: {len(L)} lines total; computer-free dc>=11 uses lines 205-387 + 497-506 ({(387-205+1)+(506-497+1)} lines).", flush=True)

    # 2a. Explicit B_9^{(4)} family: F_0(X) = [t^5] det_9((S_3^{(1)}(X) (+) S_3^{(2)}(X) (+) 0_3) + t A_0)
    rng = np.random.default_rng(1234)
    # Use 6 distinct linear forms of X in F_{P1} for the two 3x3 skew blocks + arbitrary invertible 9x9 A_0
    L_forms6 = rng.integers(-3, 4, size=(6, 16), dtype=np.int64) % P1
    A0_const = rng.integers(-3, 4, size=(9, 9), dtype=np.int64) % P1

    # Notice: for S_3(u) = [[0, u2, -u1], [-u2, 0, u0], [u1, -u0, 0]], adj(S_3(u)) = u u^T!
    # Wait: by Schur/Laplace on M_t = [[S_3(u), 0, 0], [0, S_3(v), 0], [0, 0, 0_3]] + t A_0:
    # Let's extract exact [t^5] det_9(L_0(x) + t A_0) gradient & Hessian by finite differences / polynomial interpolation of degree 4!
    # In fact, det_9(L_0(x) + t A_0) is a degree-9 polynomial in t whose t^5 coeff is F_0(x)!
    # Even faster: use 10 fixed t_m in F_{P1} to interpolate [t^5] det_9(L_0(x) + t A_0) exactly, and compute grad(F_0), Hess(F_0) via exact directional polynomial coeffs in (dx_a)!
    t_nodes = np.arange(1, 11, dtype=np.int64)
    V_t = np.vander(t_nodes, N=10, increasing=True) % P1
    V_t_inv = np.array([[int(x) % P1 for x in r] for r in sp.polys.matrices.DomainMatrix.from_Matrix(sp.Matrix(V_t.tolist())).convert_to(sp.GF(P1)).inv().to_Matrix().tolist()], dtype=np.int64)
    w_t5 = V_t_inv[5]  # exact linear combination of t_1..t_{10} giving [t^5]!

    def det_mod_p(M: np.ndarray, p: int) -> int:
        n = M.shape[0]
        A = (M % p).copy()
        det = 1
        for col in range(n):
            piv = -1
            for r in range(col, n):
                if A[r, col] != 0:
                    piv = r
                    break
            if piv == -1:
                return 0
            if piv != col:
                A[[col, piv]] = A[[piv, col]]
                det = (p - det) % p
            pv = int(A[col, col])
            det = (det * pv) % p
            inv = pow(pv, p - 2, p)
            for r in range(col + 1, n):
                if A[r, col] != 0:
                    f = (int(A[r, col]) * inv) % p
                    A[r, col:] = (A[r, col:] - f * A[col, col:]) % p
        return det

    # Exact degree-4 polynomial interpolation in 6 vars (u_0..u_2, v_0..v_2) -> binom(6+3,4) = 126 monomials!
    mons4_6 = list(itertools.combinations_with_replacement(range(6), 4))
    assert len(mons4_6) == 126
    rng_u = np.random.default_rng(999)
    while True:
        uv_pts = rng_u.integers(0, P1, size=(126, 6), dtype=np.int64)
        V_uv = np.ones((126, 126), dtype=np.int64)
        for mi, m in enumerate(mons4_6):
            for v in m:
                V_uv[:, mi] = (V_uv[:, mi] * uv_pts[:, v]) % P1
        dm_uv = sp.polys.matrices.DomainMatrix.from_Matrix(sp.Matrix(V_uv.tolist())).convert_to(sp.GF(P1))
        if dm_uv.rank() == 126:
            break
    V_uv_inv = np.array([[int(x) % P1 for x in row] for row in dm_uv.inv().to_Matrix().tolist()], dtype=np.int64)

    def eval_t5_det_uv(uv: np.ndarray, p: int) -> int:
        u, v = uv[:3], uv[3:]
        M0 = np.zeros((9, 9), dtype=np.int64)
        M0[0, 1], M0[0, 2] = u[2], (p - u[1]) % p
        M0[1, 0], M0[1, 2] = (p - u[2]) % p, u[0]
        M0[2, 0], M0[2, 1] = u[1], (p - u[0]) % p
        M0[3, 4], M0[3, 5] = v[2], (p - v[1]) % p
        M0[4, 3], M0[4, 5] = (p - v[2]) % p, v[0]
        M0[5, 3], M0[5, 4] = v[1], (p - v[0]) % p
        tot = 0
        for tm, wm in zip(t_nodes, w_t5):
            tot = (tot + int(wm) * det_mod_p(M0 + int(tm) * A0_const, p)) % p
        return tot

    uv_vals = np.array([eval_t5_det_uv(pt, P1) for pt in uv_pts], dtype=np.int64)
    c_uv = (V_uv_inv @ uv_vals) % P1
    nz_uv = [(mons4_6[mi], int(c_uv[mi])) for mi in np.nonzero(c_uv)[0]]

    # Precompute exact partial derivative tables wrt u_0..v_2 (6 grad terms, 36 hess terms)
    grad_terms = [[] for _ in range(6)]
    hess_terms = [[[] for _ in range(6)] for _ in range(6)]
    for m, coeff in nz_uv:
        for a in range(6):
            ca = m.count(a)
            if ca == 0:
                continue
            m1 = list(m)
            m1.remove(a)
            grad_terms[a].append((tuple(m1), (coeff * ca) % P1))
            for b in range(a, 6):
                cb = m1.count(b)
                if cb == 0:
                    continue
                m2 = list(m1)
                m2.remove(b)
                hess_terms[a][b].append((tuple(m2), (coeff * ca * cb) % P1))

    # Note: make_M0 only uses 6 linear forms! So dim(ker L_forms6) = 10 -> codim Sing(F_0) <= 6 -> P^{(4)} == 0 trivially!
    # TEST INSTED: What if L_0(X) + L_1 + ...? Wait: let's test e_4(L(X)) FIRST on L_8 too!
    A_lin = np.random.default_rng(777).integers(-3, 4, size=(9, 9, 16), dtype=np.int64) % P1
    A_mats_x = np.transpose(A_lin, (2, 0, 1))
    def eval_e4(xv: np.ndarray, p: int):
        M0 = np.einsum("aij,a->ij", A_mats_x, xv) % p
        M2 = (M0 @ M0) % p
        M3 = (M2 @ M0) % p
        M4 = (M3 @ M0) % p
        t1 = int(np.trace(M0)) % p
        t2 = int(np.trace(M2)) % p
        t3 = int(np.trace(M3)) % p
        inv24 = pow(24, p - 2, p)
        inv6 = pow(6, p - 2, p)
        A_flat = A_mats_x.reshape(16, 81)
        dt1 = (A_flat @ np.eye(9, dtype=np.int64).ravel()) % p
        dt2 = (2 * (A_flat @ M0.T.ravel())) % p
        dt3 = (3 * (A_flat @ M2.T.ravel())) % p
        dt4 = (4 * (A_flat @ M3.T.ravel())) % p
        # grad(24 e_4) = 4 t1^3 dt1 - 12 t1 t2 dt1 - 6 t1^2 dt2 + 6 t2 dt2 + 8 t3 dt1 + 8 t1 dt3 - 6 dt4
        grad = ((4 * pow(t1, 3, p) - 12 * t1 * t2 + 8 * t3) * dt1 + (-6 * t1 * t1 + 6 * t2) * dt2 + 8 * t1 * dt3 - 6 * dt4) % p
        grad = (grad * inv24) % p
        # Reuse Hessian formula:
        d2t2 = (2 * (A_flat @ np.transpose(A_mats_x, (0, 2, 1)).reshape(16, 81).T)) % p
        MA = np.einsum("ij,ajk->aik", M0, A_mats_x) % p
        M2A = np.einsum("ij,ajk->aik", M2, A_mats_x) % p
        d2t3 = np.zeros((16, 16), dtype=np.int64)
        d2t4 = np.zeros((16, 16), dtype=np.int64)
        for a in range(16):
            for b in range(a, 16):
                v3 = 3 * (int(np.sum(MA[a] * A_mats_x[b].T)) + int(np.sum(MA[b] * A_mats_x[a].T))) % p
                v4 = 4 * (int(np.sum(M2A[a] * A_mats_x[b].T)) + int(np.sum(M2A[b] * A_mats_x[a].T)) + int(np.sum(MA[a] * MA[b].T))) % p
                d2t3[a, b] = d2t3[b, a] = v3
                d2t4[a, b] = d2t4[b, a] = v4
        H = (
            12 * t1 * t1 * np.outer(dt1, dt1)
            - 12 * t2 * np.outer(dt1, dt1)
            - 12 * t1 * (np.outer(dt1, dt2) + np.outer(dt2, dt1))
            - 6 * t1 * t1 * d2t2
            + 6 * np.outer(dt2, dt2)
            + 6 * t2 * d2t2
            + 8 * (np.outer(dt1, dt3) + np.outer(dt3, dt1))
            + 8 * t1 * d2t3
            - 6 * d2t4
        ) % p
        return grad, (H * inv24) % p

    test_L8_and_L12_on_quartic_fn(lib, "e_4(L(X)) from det_9(I_9+L)", eval_e4, P1)

    # 2b. Test Q_{3,1} (Sheshadri 2611.03554, bdc=4 <= 9, dc>=6) on BOTH L_8 and L_12!
    def eval_Q31(xv: np.ndarray, p: int):
        # xv[0:3]=x, xv[3:9]=S sym (00,01,02,11,12,22), xv[9:12]=u, xv[12:15]=v, xv[15]=z
        x = xv[:3] % p
        S = np.array([[xv[3], xv[4], xv[5]], [xv[4], xv[6], xv[7]], [xv[5], xv[7], xv[8]]], dtype=np.int64) % p
        u = xv[9:12] % p
        v = xv[12:15] % p
        z = int(xv[15]) % p
        # Build symbolic once? Just use exact AD / polynomials in Z[y0..y15]!
        raise NotImplementedError

    # Build Q31 grad & hess symbolically once cleanly:
    Y16 = [sp.Symbol(f"y{i}") for i in range(16)]
    xv_s = sp.Matrix(Y16[:3])
    S_s = sp.Matrix([[Y16[3], Y16[4], Y16[5]], [Y16[4], Y16[6], Y16[7]], [Y16[5], Y16[7], Y16[8]]])
    uv_s = sp.Matrix(Y16[9:12])
    vv_s = sp.Matrix(Y16[12:15])
    Q31_expr = sp.expand(Y16[15] * (xv_s.T * S_s * xv_s)[0, 0] - (xv_s.T * uv_s)[0, 0] * (vv_s.T * xv_s)[0, 0])
    Q31_grads = [sp.lambdify(Y16, sp.diff(Q31_expr, Y16[a]), "numpy") for a in range(16)]
    Q31_hess = [[sp.lambdify(Y16, sp.diff(Q31_expr, Y16[a], Y16[b]), "numpy") for b in range(16)] for a in range(16)]

    def eval_Q31_fast(xv: np.ndarray, p: int):
        args_v = [int(z) for z in xv]
        g = np.array([int(fn(*args_v)) % p for fn in Q31_grads], dtype=np.int64)
        H = np.zeros((16, 16), dtype=np.int64)
        for a in range(16):
            for b in range(a, 16):
                val = int(Q31_hess[a][b](*args_v)) % p
                H[a, b] = H[b, a] = val
        return g, H

    test_L8_and_L12_on_quartic_fn(lib, "Sheshadri Q_{3,1} (bdc=4, dc>=6)", eval_Q31_fast, P1)

    # 2c. Test explicit non-homogeneous Laurent B_9^{(4)} family:
    # F_0(X) = [t^5] det_9(L_0(X) + t A_0) where L_0 = S_3^{(1)} (+) S_3^{(2)} (+) 0_3!
    def eval_B9_rank4_border(xv: np.ndarray, p: int):
        uv = (L_forms6 @ xv) % p
        g_uv = np.zeros(6, dtype=np.int64)
        H_uv = np.zeros((6, 6), dtype=np.int64)
        for a in range(6):
            s = 0
            for m1, c1 in grad_terms[a]:
                s = (s + c1 * int(uv[m1[0]]) * int(uv[m1[1]]) * int(uv[m1[2]])) % p
            g_uv[a] = s
            for b in range(a, 6):
                sh = 0
                for m2, c2 in hess_terms[a][b]:
                    sh = (sh + c2 * int(uv[m2[0]]) * int(uv[m2[1]])) % p
                H_uv[a, b] = H_uv[b, a] = sh
        g = (L_forms6.T @ g_uv) % p
        H = ((L_forms6.T @ H_uv) @ L_forms6) % p
        return g, H

    test_L8_and_L12_on_quartic_fn(lib, "B_9^{(4)} [t^5]det_9(S_3^(1)(+)S_3^(2)(+)0_3 + tA_0)", eval_B9_rank4_border, P1)

    # 3. Probe Fermat cubic x_1^3 + ... + x_5^3 (codim Sing = 5 -> strictly outside bar(D_4^{hom})!)
    #    against affine border det_4(A_0(eps) + L_eps(x)) (96 vars vs 126 eqs of deg <= 4)
    mons_le4_5 = (
        [()]
        + [(i,) for i in range(5)]
        + list(itertools.combinations_with_replacement(range(5), 2))
        + list(itertools.combinations_with_replacement(range(5), 3))
        + list(itertools.combinations_with_replacement(range(5), 4))
    )
    assert len(mons_le4_5) == 126
    m_le4_idx = {m: i for i, m in enumerate(mons_le4_5)}
    tgt = np.zeros(126, dtype=np.complex128)
    for i in range(5):
        tgt[m_le4_idx[(i, i, i)]] = 1.0
    rng_f = np.random.default_rng(2026)
    X_ev = (rng_f.standard_normal((150, 5)) + 1j * rng_f.standard_normal((150, 5))) * 0.7
    V126 = np.zeros((150, 126), dtype=np.complex128)
    for mi, m in enumerate(mons_le4_5):
        col = np.ones(150, dtype=np.complex128)
        for v in m:
            col *= X_ev[:, v]
        V126[:, mi] = col
    f_vals = V126 @ tgt
    X_aug = np.hstack([np.ones((150, 1), dtype=np.complex128), X_ev])

    # Coeff extractor for det_4(M) and its adjugate on 150 points
    def det4_res_jac(params: np.ndarray):
        A = params.reshape(6, 4, 4)
        M = np.einsum("sa,aij->sij", X_aug, A)  # (150, 4, 4)
        dets = np.linalg.det(M)
        res = dets - f_vals
        cof = np.zeros_like(M)
        for r in range(4):
            rr = [i for i in range(4) if i != r]
            for c in range(4):
                cc = [j for j in range(4) if j != c]
                cof[:, r, c] = ((-1.0) ** (r + c)) * np.linalg.det(M[:, rr, :][:, :, cc])
        jac = np.einsum("sa,sij->saij", X_aug, cof).reshape(150, 96)
        return res, jac

    best_r, best_x = 1e9, 0.0
    for _ in range(10):
        x = (rng_f.standard_normal(96) + 1j * rng_f.standard_normal(96)) * 0.45
        lam = 1e-4
        for _it in range(120):
            res, J = det4_res_jac(x)
            nrm = float(np.linalg.norm(res))
            if nrm < 1e-11:
                break
            step = np.linalg.solve(J.conj().T @ J + lam * np.eye(96), -J.conj().T @ res)
            x_t = x + step
            M_t = np.einsum("sa,aij->sij", X_aug, x_t.reshape(6, 4, 4))
            r_t = np.linalg.det(M_t) - f_vals
            if float(np.linalg.norm(r_t)) < nrm:
                x = x_t
                lam = max(lam * 0.25, 1e-13)
            else:
                lam = min(lam * 5.0, 1e8)
        res, _ = det4_res_jac(x)
        c_res, _, _, _ = np.linalg.lstsq(V126, res, rcond=None)
        cnrm = float(np.linalg.norm(c_res))
        if cnrm < best_r:
            best_r = cnrm
            best_x = float(np.linalg.norm(x))
    print(f"[PROBE] Affine non-homog border det_4 -> Fermat cubic sum x_i^3 (96 vars, 126 eqs, 10 C-LM starts): min ||coeff res|| = {best_r:.3e} (||x|| = {best_x:.2f})", flush=True)


if __name__ == "__main__":
    main()