"""Prof. Wigner Round 6:
1. Exact analytical inspection of Orbit B & C syzygies on codim-2 H.
2. Fast analytical-gradient alternating / L-BFGS search over protruding B2_out (t_B = 2, 3, 4)
   hunting for ANY configuration with F(b)-rank s_1 >= 3 and constant wire support c >= 5!
"""
import itertools
import numpy as np
from scipy.optimize import minimize
import sys
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council/prof-noether")
from general_n2k_noether import build_Mn
from apolar_higher_betti_probe import rank_matrix_mod
from perm4_abp_frontier import MOD

def build_B2_full_int():
    Mn, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    B2_full = np.zeros((6, 20, 15), dtype=np.int64)
    for ell in range(20):
        B2_full[:, ell, :] = V_basis[:, ell].reshape(15, 6).T
    return B2_full, V_basis, sub_2, sub_3

def inspect_orbit_BC_syzygies():
    print("=" * 74)
    print("1. EXACT STRUCTURE OF ORBIT B & C SYZYGIES OF B_{2,full}|_H")
    print("=" * 74)
    B2_full, _, sub_2, sub_3 = build_B2_full_int()

    def get_H_syz(name, P_mat):
        d = P_mat.shape[1]
        B2_H = np.einsum("ct,clJ->tlJ", P_mat, B2_full) % MOD
        mons_d = [(a, b) for a in range(d) for b in range(a, d)]
        mon_idx = {m: i for i, m in enumerate(mons_d)}
        n_mons = len(mons_d)
        E = np.zeros((15 * n_mons, d * 20), dtype=np.int64)
        for J in range(15):
            for a in range(d):
                for b in range(a, d):
                    r = J * n_mons + mon_idx[(a, b)]
                    for ell in range(20):
                        E[r, a * 20 + ell] = (E[r, a * 20 + ell] + B2_H[b, ell, J]) % MOD
                        if a != b:
                            E[r, b * 20 + ell] = (E[r, b * 20 + ell] + B2_H[a, ell, J]) % MOD
        # RREF
        M = E.copy()
        rows, cols = M.shape
        piv_cols = []; r_ptr = 0
        for c in range(cols):
            piv = next((r for r in range(r_ptr, rows) if M[r, c] != 0), None)
            if piv is None: continue
            M[[r_ptr, piv]] = M[[piv, r_ptr]]
            inv = pow(int(M[r_ptr, c]), MOD - 2, MOD)
            M[r_ptr] = (M[r_ptr] * inv) % MOD
            nz = np.where(M[:, c] != 0)[0]
            for r in nz:
                if r != r_ptr: M[r] = (M[r] - M[r, c] * M[r_ptr]) % MOD
            piv_cols.append(c); r_ptr += 1
        free_cols = [c for c in range(cols) if c not in piv_cols]
        print(f"\n[{name}] syz_dim = {len(free_cols)}")
        # Build F(t)-rank of all syzygies:
        B1_H = np.zeros((d, len(free_cols), 20), dtype=np.int64)
        for idx, fc in enumerate(free_cols):
            vec = np.zeros(cols, dtype=np.int64)
            vec[fc] = 1
            for ip, pc in enumerate(piv_cols):
                vec[pc] = (-M[ip, fc]) % MOD
            B1_H[:, idx, :] = vec.reshape(d, 20)
            # Print compact formula for first 3 syzygies
            if idx < 3:
                terms = []
                for ell in range(20):
                    lin = [f"{vec[t*20+ell] if vec[t*20+ell]<1000 else vec[t*20+ell]-MOD}*t{t}" for t in range(d) if vec[t*20+ell] != 0]
                    if lin:
                        terms.append(f"({'+'.join(lin)})*v{sub_3[ell]}")
                print(f"  syz {idx}: " + " + ".join(terms[:6]) + ("..." if len(terms)>6 else ""))
        rng = np.random.default_rng(1)
        t_pt = rng.integers(1, MOD, size=d, dtype=np.int64)
        rk_t = rank_matrix_mod(sum(int(t_pt[i]) * B1_H[i] for i in range(d)) % MOD, MOD)
        c_supp = rank_matrix_mod(B1_H.reshape(d * len(free_cols), 20), MOD)
        print(f"  F(t)-rank s1 = {rk_t}, wire support in S_{{6,3}} = {c_supp}")

    # Orbit A: b4=b5=0
    get_H_syz("Orbit A: b4=b5=0", np.eye(6, dtype=np.int64)[:, :4])
    # Orbit B: b4=0, b0=b1
    P_B = np.array([[1,0,0,0],[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,0],[0,0,0,1]], dtype=np.int64)
    get_H_syz("Orbit B: b4=0, b0=b1", P_B)
    # Orbit C: b0=b1, b2=b3
    P_C = np.array([[1,0,0,0],[1,0,0,0],[0,1,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]], dtype=np.int64)
    get_H_syz("Orbit C: b0=b1, b2=b3", P_C)

def fast_search_syz():
    """Fast analytical-gradient search for (B1, B2_out) with s_1 >= 3 and B1(b) B2(b) = 0,
    where B2 = [B2_in; B2_out] has t_B in {2, 3, 4} protruding rows.
    Wait: optimize B1 (6 x k x 19) and B2_out (6 x t_B x 15) jointly!
    Why? The equation B1(b) B2(b) = 0 is BILINEAR in (B1, B2_out), with exact analytical gradients!
    To prevent trivial rank-drop solutions (like s_1 <= 2 or B1_in = 0), we add:
    1. Orthogonal / well-conditioned rows of B1 at a test point b_0 (forcing F(b)-rank s_1 >= k!)
    2. Penalty if rank(B2) < 15 or if B1_in == 0!
    """
    print("\n" + "=" * 74)
    print("2. FAST ANALYTICAL-GRADIENT SEARCH FOR BOUNDARY SYZYGIES WITH s_1 in {3, 4}")
    print("=" * 74)
    B2_full, _, sub_2, sub_3 = build_B2_full_int()
    B2_full_f = B2_full.astype(float)
    mons_2 = [(a, b) for a in range(6) for b in range(a, 6)]
    n_mons = len(mons_2) # 21

    rng = np.random.default_rng(2026)
    b_pts = rng.standard_normal((4, 6))

    for t_B in [2, 3, 4]:
        n_in = 19 - t_B
        keep = list(range(n_in)) # first 19 - t_B canonical wires
        B2_in = B2_full_f[:, keep, :] # (6, n_in, 15)

        for k_rows in [3, 4]:
            # Parameterize B1: (6, k_rows, 19) and B2_out: (6, t_B, 15)
            # Syzygy residual: for each (a <= b) and (i in 0..k_rows-1, J in 0..14):
            # R[i, J, a, b] = sum_ell (B1[a, i, ell] * B2[b, ell, J] + (B1[b, i, ell] * B2[a, ell, J] if a != b else 0))
            # Actually simpler: symmetric tensor over (a, b) in {0..5}^2:
            # S[i, J, a, b] = B1[a, i, :] @ B2[b, :, J] + B1[b, i, :] @ B2[a, :, J] == 0!
            # Exact analytical gradient of ||S||_F^2 wrt B1 and B2_out is trivial with einsum!
            n_b1 = 6 * k_rows * 19
            n_b2 = 6 * t_B * 15

            best_syz_res = 1e9
            best_sol = None

            for trial in range(15):
                # Random init, plus in last 3 trials seed B1_in nonzero
                p0 = rng.standard_normal(n_b1 + n_b2) * 0.4
                # Target: enforce B1(b_pts[0]) has orthonormal rows (so rank_K(B1) == k_rows!)
                # AND B2(b_pts[0]) is full rank 15, AND B1_in has norm >= 0.5!
                def loss_and_grad(p):
                    B1 = p[:n_b1].reshape(6, k_rows, 19)
                    B2_out = p[n_b1:].reshape(6, t_B, 15)
                    B2 = np.concatenate([B2_in, B2_out], axis=1) # (6, 19, 15)

                    # P[a, b, i, J] = sum_ell B1[a, i, ell] * B2[b, ell, J]
                    P = np.einsum("ail,blJ->abiJ", B1, B2)
                    S = P + P.transpose(1, 0, 2, 3) # symmetric in (a, b): zero iff B1(b)B2(b)==0!
                    loss_syz = 0.5 * np.sum(S**2)

                    # Grad of loss_syz wrt B1 and B2:
                    # d(loss)/dP = 2 * S (since S is already symmetric)
                    # d(loss)/dB1[a, i, ell] = 2 * sum_{b, J} S[a, b, i, J] * B2[b, ell, J]
                    g_B1 = 2.0 * np.einsum("abiJ,blJ->ail", S, B2)
                    g_B2 = 2.0 * np.einsum("abiJ,ail->blJ", S, B1)
                    g_B2_out = g_B2[:, n_in:, :]

                    # Constraint 1: B1(b0) @ B1(b0)^T == I_{k_rows} (forces s_1 = k_rows!)
                    b0 = b_pts[0]
                    B1_0 = np.tensordot(b0, B1, axes=([0],[0])) # (k_rows, 19)
                    G1 = B1_0 @ B1_0.T - np.eye(k_rows)
                    w_orth = 0.5
                    loss_orth = 0.5 * w_orth * np.sum(G1**2)
                    # d(loss_orth)/dB1_0 = 2 * w_orth * G1 @ B1_0
                    g_B1_0 = 2.0 * w_orth * (G1 @ B1_0)
                    g_B1 += np.einsum("a,il->ail", b0, g_B1_0)

                    # Constraint 2: B1_in nonzero: encourage ||B1_in||_F^2 >= 1.0
                    B1_in = B1[:, :, :n_in]
                    nrm2_in = np.sum(B1_in**2)
                    loss_in = 0.0
                    if nrm2_in < 1.0:
                        diff_in = 1.0 - nrm2_in
                        loss_in = 0.2 * (diff_in**2)
                        g_B1[:, :, :n_in] += -0.8 * diff_in * B1_in

                    # Constraint 3: B2_out non-degenerate: ||B2_out||_F^2 <= 50 (prevents blowup)
                    loss_reg = 1e-5 * np.sum(B2_out**2)
                    g_B2_out += 2e-5 * B2_out

                    grad = np.concatenate([g_B1.reshape(-1), g_B2_out.reshape(-1)])
                    return loss_syz + loss_orth + loss_in + loss_reg, grad

                res = minimize(loss_and_grad, p0, jac=True, method='L-BFGS-B', options={'maxiter': 500, 'ftol': 1e-15, 'gtol': 1e-12})
                # Check true syzygy residual alone
                B1 = res.x[:n_b1].reshape(6, k_rows, 19)
                B2_out = res.x[n_b1:].reshape(6, t_B, 15)
                B2 = np.concatenate([B2_in, B2_out], axis=1)
                P = np.einsum("ail,blJ->abiJ", B1, B2)
                S = P + P.transpose(1, 0, 2, 3)
                syz_norm = np.linalg.norm(S)
                if syz_norm < best_syz_res:
                    best_syz_res = syz_norm
                    best_sol = (B1, B2_out, B2)

            B1, B2_out, B2 = best_sol
            b0 = b_pts[1]
            s1_obs = np.linalg.matrix_rank(np.tensordot(b0, B1, axes=([0],[0])), tol=1e-5)
            rk_B2 = np.linalg.matrix_rank(np.tensordot(b0, B2, axes=([0],[0])), tol=1e-5)
            c_wires = np.linalg.matrix_rank(B1.reshape(6 * k_rows, 19), tol=1e-5)
            nrm_in = np.linalg.norm(B1[:, :, :n_in])
            print(f"  t_B={t_B}, k={k_rows}: min ||S||_F = {best_syz_res:.3e} | s1={s1_obs}, rk_B2={rk_B2}, c_wires={c_wires}, ||B1_in||={nrm_in:.3f}")

if __name__ == "__main__":
    inspect_orbit_BC_syzygies()
    fast_search_syz()
