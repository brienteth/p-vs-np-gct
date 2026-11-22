"""
Prof. Euler - High-Precision Fast Complex Optimization Lab for Case (3,2)
Solves ||K(B1,V1) + K(B2,V2) + U_{16x3} W_{3x16} - M||_F^2 = 0 over C
using exact analytic holomorphic Jacobian and Levenberg-Marquardt with 25 random restarts.
"""
import time
from typing import List, Tuple
import numpy as np
from perm4_middle_factorization_probe import extract_middle_4x4
from poly_exact import permanent_poly

def build_nisan_matrix() -> np.ndarray:
    p_perm = extract_middle_4x4(permanent_poly(4))
    T = np.zeros((4, 4, 4, 4), dtype=float)
    for j0 in range(4):
        for j3 in range(4):
            for mon, c in p_perm[j0][j3].items():
                c1 = [k for k in range(4) if mon[k] == 1][0]
                c2 = [k for k in range(4) if mon[4+k] == 1][0]
                T[j0, c1, j3, c2] = c
    return T.reshape(16, 16)

def unpack_real_jac(jc: np.ndarray) -> np.ndarray:
    jr = jc.real
    ji = jc.imag
    top = np.hstack([jr, -ji])
    bot = np.hstack([ji, jr])
    return np.vstack([top, bot])

def run_complex_lm(
    residual_and_jac,
    n_complex_vars: int,
    n_complex_eqs: int,
    rng: np.random.Generator,
    n_starts: int = 25,
    max_iters: int = 200,
    scale: float = 0.6,
) -> Tuple[List[float], np.ndarray]:
    best_x: np.ndarray | None = None
    best_norm = float("inf")
    finals: List[float] = []

    for start in range(n_starts):
        z = scale * (rng.standard_normal(n_complex_vars) + 1j * rng.standard_normal(n_complex_vars))
        r, jac = residual_and_jac(z)
        cur_norm = float(np.linalg.norm(r))
        lam = 1e-3
        for _it in range(max_iters):
            if cur_norm < 1e-12:
                break
            jtj = jac.T @ jac
            g = jac.T @ r
            diag = np.maximum(np.diag(jtj), 1e-6)
            accepted = False
            for _try in range(8):
                lhs = jtj + lam * np.diag(diag)
                try:
                    step = -np.linalg.solve(lhs, g)
                except np.linalg.LinAlgError:
                    step, _, _, _ = np.linalg.lstsq(lhs, -g, rcond=None)
                z_new = z + step[:n_complex_vars] + 1j * step[n_complex_vars:]
                r_new, j_new = residual_and_jac(z_new)
                new_norm = float(np.linalg.norm(r_new))
                if new_norm < cur_norm:
                    z, r, jac, cur_norm = z_new, r_new, j_new, new_norm
                    lam = max(lam * 0.3, 1e-12)
                    accepted = True
                    break
                lam = min(lam * 5.0, 1e8)
            if not accepted and lam >= 1e7:
                break
        finals.append(cur_norm)
        if cur_norm < best_norm:
            best_norm = cur_norm
            best_x = z
        print(f"Start {start:2d}: final residual = {cur_norm:.6f}")
    assert best_x is not None
    return finals, best_x

def main():
    m_mat = build_nisan_matrix()
    m_c = m_mat.astype(np.complex128)
    n_vars = 16 + 16 + 16 + 16 + 48 + 48  # 160
    rng = np.random.default_rng(2026)

    def res_jac(z: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        b1 = z[0:16].reshape(4, 4)
        v1 = z[16:32].reshape(4, 4)
        b2 = z[32:48].reshape(4, 4)
        v2 = z[48:64].reshape(4, 4)
        u3 = z[64:112].reshape(16, 3)
        w3 = z[112:160].reshape(3, 16)

        k1 = np.einsum("ac,db->abdc", b1, v1).reshape(16, 16)
        k2 = np.einsum("ac,db->abdc", b2, v2).reshape(16, 16)
        f = (k1 + k2 + u3 @ w3 - m_c).reshape(256)

        jc = np.zeros((256, n_vars), dtype=np.complex128)
        jc_4d = jc.reshape(4, 4, 4, 4, n_vars)
        for a in range(4):
            for c in range(4):
                jc_4d[a, :, :, c, a * 4 + c] += v1.T
                jc_4d[a, :, :, c, 32 + a * 4 + c] += v2.T
        for d in range(4):
            for b in range(4):
                jc_4d[:, b, d, :, 16 + d * 4 + b] += b1
                jc_4d[:, b, d, :, 48 + d * 4 + b] += b2

        jc_mat = jc.reshape(16, 16, n_vars)
        for row in range(16):
            for k in range(3):
                jc_mat[row, :, 64 + row * 3 + k] += w3[k, :]
        for k in range(3):
            for col in range(16):
                jc_mat[:, col, 112 + k * 16 + col] += u3[:, k]

        r_real = np.concatenate([f.real, f.imag])
        j_real = unpack_real_jac(jc)
        return r_real, j_real

    print("=== Prof. Euler Complex LM Lab: 25 Starts on Case (3,2) ===")
    t0 = time.time()
    finals, best_z = run_complex_lm(res_jac, n_vars, 256, rng, n_starts=25, max_iters=200)
    dt = time.time() - t0
    
    b1 = best_z[0:16].reshape(4, 4)
    v1 = best_z[16:32].reshape(4, 4)
    b2 = best_z[32:48].reshape(4, 4)
    v2 = best_z[48:64].reshape(4, 4)
    rem = m_c - np.einsum("ac,db->abdc", b1, v1).reshape(16, 16) - np.einsum("ac,db->abdc", b2, v2).reshape(16, 16)
    svals = np.linalg.svd(rem, compute_uv=False)
    tail_norm = float(np.linalg.norm(svals[3:]))
    min_res = min(finals)
    med_res = float(np.median(finals))
    
    print("--------------------------------------------------")
    print(f"Completed 25 starts in {dt:.2f}s.")
    print(f"Min residual: {min_res:.6f}")
    print(f"Median residual: {med_res:.6f}")
    print(f"Best tail singular values svals[3:]: {tail_norm:.6f}")
    print(f"Singular values of best M - K1 - K2:\n{np.round(svals, 4)}")
    print(f"Solved (res < 1e-4): {sum(r < 1e-4 for r in finals)} / 25")
    print("--------------------------------------------------")

if __name__ == '__main__':
    main()
