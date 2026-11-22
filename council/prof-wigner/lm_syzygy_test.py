"""Prof. Wigner Round 6: Exact Levenberg-Marquardt Test on Degree-1 Boundary Syzygies
for t_B in {2, 3, 4} and k in {3, 4} (forcing s_1 = k and rank(B2) = 15).
Can LM drive ||B1(b) B2(b)||_F to < 1e-10 (exact zero), or is there a hard floor?
"""
import numpy as np
import sys
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council/prof-noether")
from general_n2k_noether import build_Mn

def build_B2_full_f():
    Mn, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    B2_full = np.zeros((6, 20, 15), dtype=float)
    for ell in range(20):
        B2_full[:, ell, :] = V_basis[:, ell].reshape(15, 6).T
    return B2_full, sub_2, sub_3

def run_lm_syz(B2_in, t_B, k_rows, b0, p0, max_iter=80):
    n_in = 19 - t_B
    n_b1 = 6 * k_rows * 19
    n_b2 = 6 * t_B * 15
    n_vars = n_b1 + n_b2
    # Equations:
    # 1) S[a<=b, i, J] = 0: 21 * k_rows * 15 equations
    # 2) B1(b0) @ B1(b0)^T == I_k: k_rows * k_rows equations (actually k*(k+1)//2, use full k*k or upper)
    # 3) To prevent B1_in == 0 trivial solution (already known to exist for Noether #58? Wait: in Noether #58, B1_in != 0!),
    #    don't force ||B1_in|| >= 1 at first; let's see BOTH unconstrained (just s1 = k) AND with ||B1_in|| = 1!
    pairs_le = [(a, b) for a in range(6) for b in range(a, 6)]
    tri_k = [(i, j) for i in range(k_rows) for j in range(i, k_rows)]

    def res_and_jac(p):
        B1 = p[:n_b1].reshape(6, k_rows, 19)
        B2_out = p[n_b1:].reshape(6, t_B, 15)
        B2 = np.concatenate([B2_in, B2_out], axis=1)

        # Syzygy residuals for a <= b:
        r_syz = np.empty((21, k_rows, 15), dtype=float)
        J_syz_b1 = np.zeros((21, k_rows, 15, 6, k_rows, 19), dtype=float)
        J_syz_b2 = np.zeros((21, k_rows, 15, 6, t_B, 15), dtype=float)
        for m_idx, (a, b) in enumerate(pairs_le):
            if a == b:
                r_syz[m_idx] = B1[a] @ B2[a]
                for i in range(k_rows):
                    J_syz_b1[m_idx, i, :, a, i, :] += B2[a].T
                for J in range(15):
                    J_syz_b2[m_idx, :, J, a, :, J] += B1[a, :, n_in:]
            else:
                r_syz[m_idx] = B1[a] @ B2[b] + B1[b] @ B2[a]
                for i in range(k_rows):
                    J_syz_b1[m_idx, i, :, a, i, :] += B2[b].T
                    J_syz_b1[m_idx, i, :, b, i, :] += B2[a].T
                for J in range(15):
                    J_syz_b2[m_idx, :, J, b, :, J] += B1[a, :, n_in:]
                    J_syz_b2[m_idx, :, J, a, :, J] += B1[b, :, n_in:]

        # Orthogonality at b0: B1(b0) @ B1(b0)^T - I == 0 (weighted by 2.0)
        B1_0 = np.tensordot(b0, B1, axes=([0],[0])) # (k_rows, 19)
        G = B1_0 @ B1_0.T - np.eye(k_rows)
        w_g = 2.0
        r_orth = w_g * np.array([G[i, j] for (i, j) in tri_k])
        J_orth_b1 = np.zeros((len(tri_k), 6, k_rows, 19), dtype=float)
        for idx, (i, j) in enumerate(tri_k):
            for c in range(6):
                J_orth_b1[idx, c, i, :] += w_g * b0[c] * B1_0[j, :]
                J_orth_b1[idx, c, j, :] += w_g * b0[c] * B1_0[i, :]

        r = np.concatenate([r_syz.reshape(-1), r_orth])
        J1 = np.hstack([J_syz_b1.reshape(-1, n_b1), J_syz_b2.reshape(-1, n_b2)])
        J2 = np.hstack([J_orth_b1.reshape(len(tri_k), n_b1), np.zeros((len(tri_k), n_b2))])
        J = np.vstack([J1, J2])
        return r, J

    p = p0.copy()
    lam = 1e-2
    r, J = res_and_jac(p)
    nr = np.linalg.norm(r)
    eye = np.eye(n_vars)
    for it in range(max_iter):
        if nr < 1e-11:
            break
        H = J.T @ J
        g = J.T @ r
        accepted = False
        for _ in range(10):
            try:
                dp = -np.linalg.solve(H + lam * eye, g)
            except np.linalg.LinAlgError:
                lam *= 10.0; continue
            cand = p + dp
            # fast residual eval
            B1 = cand[:n_b1].reshape(6, k_rows, 19)
            B2_out = cand[n_b1:].reshape(6, t_B, 15)
            B2 = np.concatenate([B2_in, B2_out], axis=1)
            rc = []
            for a, b in pairs_le:
                rc.append((B1[a] @ B2[a] if a == b else B1[a] @ B2[b] + B1[b] @ B2[a]).reshape(-1))
            B1_0 = np.tensordot(b0, B1, axes=([0],[0]))
            G = B1_0 @ B1_0.T - np.eye(k_rows)
            rc.append(2.0 * np.array([G[i, j] for (i, j) in tri_k]))
            r_cand = np.concatenate(rc)
            nrc = np.linalg.norm(r_cand)
            if nrc < nr:
                p = cand
                rel = (nr - nrc) / max(nr, 1e-15)
                nr = nrc
                r, J = res_and_jac(p)
                lam = max(lam * 0.3, 1e-13)
                accepted = True
                if rel < 1e-12 and np.linalg.norm(dp) < 1e-12:
                    return nr, p
                break
            lam *= 5.0
        if not accepted or lam > 1e10:
            break
    return nr, p

def main():
    print("=" * 74)
    print("EXACT DAMPED LM TEST: CAN t_B in {2,3,4} PRODUCE s_1 in {3,4} SYZYGIES?")
    print("=" * 74)
    B2_full, sub_2, sub_3 = build_B2_full_f()
    sub3_idx = {s: i for i, s in enumerate(sub_3)}
    rng = np.random.default_rng(137)
    b0 = rng.standard_normal(6)
    b_chk = rng.standard_normal(6)

    # Compare two drops: lex drop vs Noether drop (preserving {0,4,5},{1,4,5},{2,4,5},{3,4,5})
    noether_drops = [sub3_idx[(0,1,2)], sub3_idx[(0,1,3)], sub3_idx[(0,2,3)], sub3_idx[(1,2,3)], sub3_idx[(0,1,4)]]

    for t_B in [2, 3, 4]:
        n_in = 19 - t_B
        drops = noether_drops[:t_B + 1]
        keep = [i for i in range(20) if i not in drops]
        B2_in = B2_full[:, keep, :]
        for k_rows in [3, 4]:
            best_nr = 1e9
            best_p = None
            n_b1 = 6 * k_rows * 19
            n_b2 = 6 * t_B * 15
            for s in range(5):
                p0 = rng.standard_normal(n_b1 + n_b2) * 0.3
                nr, p = run_lm_syz(B2_in, t_B, k_rows, b0, p0, max_iter=60)
                if nr < best_nr:
                    best_nr, best_p = nr, p
            B1 = best_p[:n_b1].reshape(6, k_rows, 19)
            B2_out = best_p[n_b1:].reshape(6, t_B, 15)
            B2 = np.concatenate([B2_in, B2_out], axis=1)
            s1 = np.linalg.matrix_rank(np.tensordot(b_chk, B1, axes=([0],[0])), tol=1e-6)
            rk_B2 = np.linalg.matrix_rank(np.tensordot(b_chk, B2, axes=([0],[0])), tol=1e-6)
            c_wires = np.linalg.matrix_rank(B1.reshape(6 * k_rows, 19), tol=1e-6)
            nrm_in = np.linalg.norm(B1[:, :, :n_in])
            print(f"  t_B={t_B}, k={k_rows}: min ||r||_2 = {best_nr:.3e} | s1={s1}, rk_B2={rk_B2}, c_wires={c_wires}, ||B1_in||={nrm_in:.3f}")

if __name__ == "__main__":
    main()
