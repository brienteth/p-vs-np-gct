"""Prof. Wigner Round 6: Direct LM Hunt for {d_syz >= 6, rk_B2 = 15, dim_F(I_B) = 19}
at t_B in {2, 3, 4}, WITHOUT restricting B1 to s1=6 (only requiring 6 F-linearly independent
degree-1 syzygies!). Measures s_1 and constant wire support c of every found solution.
"""
import numpy as np
import sys
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council/prof-noether")
from general_n2k_noether import build_Mn

def build_B2_full_and_perp():
    Mn, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    B2_full = np.zeros((6, 20, 15), dtype=float)
    for ell in range(20):
        B2_full[:, ell, :] = V_basis[:, ell].reshape(15, 6).T
    Q_S, _ = np.linalg.qr(V_basis.astype(float))
    U, S, _ = np.linalg.svd(np.eye(90) - Q_S @ Q_S.T)
    Q_perp = U[:, :70]
    Q_perp_tensor = np.array([Q_perp[:, m].reshape(15, 6).T for m in range(70)])
    return B2_full, Q_perp_tensor, sub_2, sub_3

def run_lm_d6(B2_in, Q_perp_tensor, t_B, b0, p0, max_iter=60):
    d_target = 6
    n_in = 19 - t_B
    n_b1 = 6 * d_target * 19
    n_cout = t_B * 70
    n_m = 15 * 19
    n_vars = n_b1 + n_cout + n_m

    pairs_le = [(a, b) for a in range(6) for b in range(a, 6)]
    tri_d = [(i, j) for i in range(d_target) for j in range(i, d_target)]
    tri_t = [(i, j) for i in range(t_B) for j in range(i, t_B)]
    Q_b0 = np.einsum("c,mcJ->mJ", b0, Q_perp_tensor)

    def eval_res(p):
        B1 = p[:n_b1].reshape(6, d_target, 19)
        C_out = p[n_b1:n_b1+n_cout].reshape(t_B, 70)
        M_left = p[n_b1+n_cout:].reshape(15, 19)
        B2_out = np.einsum("tm,mcJ->ctJ", C_out, Q_perp_tensor)
        B2 = np.concatenate([B2_in, B2_out], axis=1)

        parts = []
        for a, b in pairs_le:
            parts.append((B1[a] @ B2[a] if a == b else B1[a] @ B2[b] + B1[b] @ B2[a]).reshape(-1))
        # F-orthonormality of the 6 syzygies: B1_flat (6 x 114) @ B1_flat^T == I_6
        B1_flat = B1.transpose(1, 0, 2).reshape(d_target, 114)
        G1 = B1_flat @ B1_flat.T - np.eye(d_target)
        parts.append(2.0 * np.array([G1[i, j] for (i, j) in tri_d]))
        G2 = C_out @ C_out.T - np.eye(t_B)
        parts.append(2.0 * np.array([G2[i, j] for (i, j) in tri_t]))
        B2_0 = np.tensordot(b0, B2, axes=([0],[0]))
        parts.append((M_left @ B2_0 - np.eye(15)).reshape(-1))
        return np.concatenate(parts)

    def res_and_jac(p):
        B1 = p[:n_b1].reshape(6, d_target, 19)
        C_out = p[n_b1:n_b1+n_cout].reshape(t_B, 70)
        M_left = p[n_b1+n_cout:].reshape(15, 19)
        B2_out = np.einsum("tm,mcJ->ctJ", C_out, Q_perp_tensor)
        B2 = np.concatenate([B2_in, B2_out], axis=1)

        n_syz = 21 * d_target * 15
        r_syz = np.empty((21, d_target, 15))
        J1_b1 = np.zeros((21, d_target, 15, 6, d_target, 19))
        J1_b2_diag = np.zeros((21, d_target, 15, 6, t_B))
        for m_idx, (a, b) in enumerate(pairs_le):
            if a == b:
                r_syz[m_idx] = B1[a] @ B2[a]
                for i in range(d_target):
                    J1_b1[m_idx, i, :, a, i, :] += B2[a].T
                for c_J in range(15):
                    J1_b2_diag[m_idx, :, c_J, a, :] += B1[a, :, n_in:]
            else:
                r_syz[m_idx] = B1[a] @ B2[b] + B1[b] @ B2[a]
                for i in range(d_target):
                    J1_b1[m_idx, i, :, a, i, :] += B2[b].T
                    J1_b1[m_idx, i, :, b, i, :] += B2[a].T
                for c_J in range(15):
                    J1_b2_diag[m_idx, :, c_J, b, :] += B1[a, :, n_in:]
                    J1_b2_diag[m_idx, :, c_J, a, :] += B1[b, :, n_in:]
        J1_cout = np.einsum("aiJct,qcJ->aiJtq", J1_b2_diag, Q_perp_tensor)

        B1_flat = B1.transpose(1, 0, 2).reshape(d_target, 114)
        G1 = B1_flat @ B1_flat.T - np.eye(d_target)
        r_g1 = 2.0 * np.array([G1[i, j] for (i, j) in tri_d])
        J2_b1 = np.zeros((len(tri_d), 6, d_target, 19))
        for idx, (i, j) in enumerate(tri_d):
            J2_b1[idx, :, i, :] += 2.0 * B1[:, j, :]
            J2_b1[idx, :, j, :] += 2.0 * B1[:, i, :]

        G2 = C_out @ C_out.T - np.eye(t_B)
        r_g2 = 2.0 * np.array([G2[i, j] for (i, j) in tri_t])
        J3_cout = np.zeros((len(tri_t), t_B, 70))
        for idx, (i, j) in enumerate(tri_t):
            J3_cout[idx, i, :] += 2.0 * C_out[j, :]
            J3_cout[idx, j, :] += 2.0 * C_out[i, :]

        B2_0 = np.tensordot(b0, B2, axes=([0],[0]))
        r_rk = (M_left @ B2_0 - np.eye(15)).reshape(-1)
        J4_cout = np.zeros((15, 15, t_B, 70))
        for u in range(15):
            for t in range(t_B):
                J4_cout[u, :, t, :] += M_left[u, n_in + t] * Q_b0.T
        J4_m = np.zeros((15, 15, 15, 19))
        for u in range(15):
            J4_m[u, :, u, :] += B2_0.T

        r = np.concatenate([r_syz.reshape(-1), r_g1, r_g2, r_rk])
        row1 = np.hstack([J1_b1.reshape(n_syz, n_b1), J1_cout.reshape(n_syz, n_cout), np.zeros((n_syz, n_m))])
        row2 = np.hstack([J2_b1.reshape(len(tri_d), n_b1), np.zeros((len(tri_d), n_cout + n_m))])
        row3 = np.hstack([np.zeros((len(tri_t), n_b1)), J3_cout.reshape(len(tri_t), n_cout), np.zeros((len(tri_t), n_m))])
        row4 = np.hstack([np.zeros((225, n_b1)), J4_cout.reshape(225, n_cout), J4_m.reshape(225, n_m)])
        J = np.vstack([row1, row2, row3, row4])
        return r, J

    p = p0.copy()
    lam = 1e-2
    r, J = res_and_jac(p)
    nr = np.linalg.norm(r)
    eye = np.eye(n_vars)
    for _ in range(max_iter):
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
            nrc = np.linalg.norm(eval_res(cand))
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
    print("DIRECT LM HUNT FOR d_syz >= 6 WITH rk_B2 = 15 AND B2_out in S_{6,3}^perp")
    print("=" * 74)
    B2_full, Q_perp_tensor, sub_2, sub_3 = build_B2_full_and_perp()
    sub3_idx = {s: i for i, s in enumerate(sub_3)}
    rng = np.random.default_rng(777)
    b0 = rng.standard_normal(6)
    b_chk = rng.standard_normal(6)
    noether_drops = [sub3_idx[(0,1,2)], sub3_idx[(0,1,3)], sub3_idx[(0,2,3)], sub3_idx[(1,2,3)], sub3_idx[(0,1,4)]]

    for t_B in [2, 3, 4]:
        n_in = 19 - t_B
        drops = noether_drops[:t_B + 1]
        keep = [i for i in range(20) if i not in drops]
        B2_in = B2_full[:, keep, :]
        n_b1 = 6 * 6 * 19
        n_cout = t_B * 70
        n_m = 15 * 19
        solved_info = []
        best_nr = 1e9
        for s in range(4):
            p0 = rng.standard_normal(n_b1 + n_cout + n_m) * 0.25
            nr, p = run_lm_d6(B2_in, Q_perp_tensor, t_B, b0, p0, max_iter=55)
            if nr < best_nr:
                best_nr = nr
            if nr < 1e-8:
                B1 = p[:n_b1].reshape(6, 6, 19)
                s1 = np.linalg.matrix_rank(np.tensordot(b_chk, B1, axes=([0],[0])), tol=1e-6)
                c_w = np.linalg.matrix_rank(B1.reshape(36, 19), tol=1e-6)
                solved_info.append((int(s1), int(c_w)))
        print(f"  t_B={t_B}: min ||r||={best_nr:.3e} | solved={len(solved_info)}/4 | (s1, c)={solved_info}")

if __name__ == "__main__":
    main()
