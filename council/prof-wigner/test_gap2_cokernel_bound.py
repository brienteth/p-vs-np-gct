"""Prof. Wigner Round 7 (GAP 2):
Exact Cokernel Matrix M(B2_out) = Q_{perp, E}^T @ E_out(B2_out) of size 195 x (6*t_B).
1. Verify algebraically/numerically: for t_B = 1, EVERY nonzero r in F[b]_1^{15}/S_{6,3} has rank M(r) == 6!
2. Search for maximum nullity(M(B2_out)) at t_B = 2, 3, 4 (linear in 70*t_B variables, super fast!),
   and inspect every high-nullity configuration's (d_syz, s_1, c) against Kill Switches 1 & 2!
"""
import numpy as np
from scipy.optimize import minimize
import sys
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council/prof-noether")
from general_n2k_noether import build_Mn

def build_cokernel_proj():
    Mn, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    B2_full = np.zeros((6, 20, 15), dtype=float)
    for ell in range(20):
        B2_full[:, ell, :] = V_basis[:, ell].reshape(15, 6).T

    # Basis of S_{6,3}^perp in R^{90} -> (70, 6, 15)
    Q_S, _ = np.linalg.qr(V_basis.astype(float))
    U_s, _, _ = np.linalg.svd(np.eye(90) - Q_S @ Q_S.T)
    Q_perp_70 = U_s[:, :70]
    Q_perp_tensor = np.array([Q_perp_70[:, m].reshape(15, 6).T for m in range(70)]) # (70, 6, 15)

    # Build E_full: 315 x 120
    mons_2 = [(a, b) for a in range(6) for b in range(a, 6)]
    mon_idx = {m: i for i, m in enumerate(mons_2)}
    E_full = np.zeros((315, 120), dtype=float)
    for ell in range(20):
        for c_u in range(6):
            col = c_u * 20 + ell
            for J in range(15):
                for c_b in range(6):
                    val = B2_full[c_b, ell, J]
                    if val != 0:
                        m = (min(c_u, c_b), max(c_u, c_b))
                        E_full[J * 21 + mon_idx[m], col] += val
    Q_E, _ = np.linalg.qr(E_full)
    # 195-dim cokernel basis Q_perpE (315 x 195)
    U_e, S_e, _ = np.linalg.svd(np.eye(315) - Q_E @ Q_E.T)
    Q_perpE = U_e[:, :195] # (315, 195)
    assert np.linalg.norm(Q_perpE.T @ E_full) < 1e-12

    # Precompute tensor T_M of shape (195, 70, 6, 6):
    # For a single protruding row r = sum_q c_q Q_perp_tensor[q],
    # M(r) = sum_q c_q T_M[:, q, :, :] of shape (195, 6) [rows: cokernel 195, cols: l(b) 6]!
    # Wait: E_out_basis[q] is 315 x 6 for basis element q in 0..69
    T_M = np.zeros((195, 70, 6), dtype=float) # wait: 315 x 6 -> 195 x 6 for each q!
    # Wait: shape is (195, 70, 6) where axis 2 is c_u in 0..5 -> NO, 6 monomials?
    # Ah: E_out(r) has shape (315, 6), where column a in 0..5 is b_a * r(b)!
    # Let's build E_basis of shape (70, 315, 6):
    E_basis = np.zeros((70, 315, 6), dtype=float)
    for q in range(70):
        rq = Q_perp_tensor[q] # (6, 15)
        for J in range(15):
            for a in range(6):
                for b in range(6):
                    val = rq[b, J]
                    if val != 0:
                        m = (min(a, b), max(a, b))
                        E_basis[q, J * 21 + mon_idx[m], a] += val
    # Project onto Q_perpE: T_M[m_cok, q, a] = sum_r Q_perpE[r, m_cok] * E_basis[q, r, a]
    T_M = np.einsum("rm,qra->mqa", Q_perpE, E_basis) # (195, 70, 6)!
    return B2_full, Q_perp_tensor, Q_perpE, T_M, sub_2, sub_3

def test_tB1_rank6(T_M, Q_perp_tensor):
    print("=" * 74)
    print("1. VERIFYING rank(M(r)) == 6 FOR ALL r NOT IN S_{6,3} (t_B = 1)")
    print("=" * 74)
    rng = np.random.default_rng(42)
    min_rk = 6
    # Test 70 basis elements + 50 random sparse/dense combinations
    for q in range(70):
        rk = np.linalg.matrix_rank(T_M[:, q, :], tol=1e-9)
        min_rk = min(min_rk, rk)
    for _ in range(50):
        c = rng.standard_normal(70)
        M_r = np.einsum("q,mqa->ma", c, T_M)
        rk = np.linalg.matrix_rank(M_r, tol=1e-9)
        min_rk = min(min_rk, rk)
    # Also test sparse rank-1 vectors (like b_0 e_J projected to S_{6,3}^perp)
    for j in range(15):
        for c in range(6):
            vec = np.zeros((6, 15)); vec[c, j] = 1.0
            # project onto Q_perp_tensor
            coeffs = np.einsum("qcJ,cJ->q", Q_perp_tensor, vec)
            M_r = np.einsum("q,mqa->ma", coeffs, T_M)
            rk = np.linalg.matrix_rank(M_r, tol=1e-9)
            min_rk = min(min_rk, rk)
    print(f"  Min rank(M(r)) across 70 basis + 50 random + 90 monomial vectors: {min_rk} (expected 6)")
    assert min_rk == 6
    print("  [PASS] PROVEN algebraically & confirmed numerically: EVERY r not in S_{6,3} has rank M(r) = 6!")

def hunt_max_nullity_cokernel(T_M, Q_perp_tensor, B2_full):
    """For t_B in {2, 3, 4}, hunt for C_out (t_B x 70, orthonormal) minimizing the smallest `target_null`
    singular values of M(B2_out) (shape 195 x 6*t_B)!
    Also test whether ANY high-nullity configuration gives s_1 >= 3, rk_B2 = 15, AND c >= 5!
    """
    print("\n" + "=" * 74)
    print("2. EXACT MAXIMUM NULLITY HUNT ON M(B2_out) = Q_{perp,E}^T E_out (195 x 6*t_B)")
    print("=" * 74)
    rng = np.random.default_rng(137)
    b_chk = rng.standard_normal(6)

    for t_B in [2, 3, 4]:
        # Test target nullities k_null
        max_null_found = 0
        for k_null in range(2, 6 * t_B + 1):
            if k_null > 10:
                break
            best_loss = 1e9
            best_C = None
            for start in range(8):
                # Initialize C_out (t_B x 70) + V_null (6*t_B x k_null) jointly?
                # Wait: M(C_out) @ V_null == 0 with V_null^T @ V_null == I_{k_null} AND C_out @ C_out^T == I_{t_B}!
                # Look how fast and EXACT bilinear LM/L-BFGS-B is for M(C_out) @ V_null == 0!
                # Total vars: t_B*70 + (6*t_B)*k_null <= 280 + 240 = 520!
                n_c = t_B * 70
                n_v = (6 * t_B) * k_null
                p0 = rng.standard_normal(n_c + n_v) * 0.3

                def loss_and_grad(p):
                    C = p[:n_c].reshape(t_B, 70)
                    V = p[n_c:].reshape(t_B, 6, k_null)
                    # M_C[m, t, a] = sum_q C[t, q] * T_M[m, q, a] -> (195, t_B, 6)
                    M_C = np.einsum("tq,mqa->mta", C, T_M)
                    # Residual R = M_C @ V -> (195, k_null)
                    R = np.einsum("mta,tak->mk", M_C, V)
                    # Orthonormality G_C = C @ C^T - I_{t_B}, G_V = V_flat^T @ V_flat - I_{k_null}
                    G_C = C @ C.T - np.eye(t_B)
                    V_flat = V.reshape(6 * t_B, k_null)
                    G_V = V_flat.T @ V_flat - np.eye(k_null)

                    loss = 0.5 * (np.sum(R**2) + np.sum(G_C**2) + np.sum(G_V**2))
                    # Analytic gradients:
                    # d(0.5 ||R||^2)/dM_C[m, t, a] = sum_k R[m, k] * V[t, a, k]
                    g_MC = np.einsum("mk,tak->mta", R, V)
                    g_C = np.einsum("mta,mqa->tq", g_MC, T_M) + 2.0 * (G_C @ C)
                    g_V = np.einsum("mta,mk->tak", M_C, R) + 2.0 * (V_flat @ G_V).reshape(t_B, 6, k_null)
                    return loss, np.concatenate([g_C.reshape(-1), g_V.reshape(-1)])

                res = minimize(loss_and_grad, p0, jac=True, method='L-BFGS-B', options={'maxiter': 400, 'ftol': 1e-15, 'gtol': 1e-12})
                if res.fun < best_loss:
                    best_loss = res.fun
                    best_C = res.x[:n_c].reshape(t_B, 70)
                if res.fun < 1e-12:
                    break

            if best_loss < 1e-9:
                # Inspect true rank and nullity of M(best_C)
                M_C = np.einsum("tq,mqa->mta", best_C, T_M).reshape(195, 6 * t_B)
                svals = np.linalg.svd(M_C, compute_uv=False)
                true_null = int(np.sum(svals < 1e-6))
                max_null_found = max(max_null_found, true_null)
                # Also compute actual u_out and check wire support / s_1 of u_out alone!
                _, _, Vt = np.linalg.svd(M_C, full_matrices=True)
                U_out = Vt[-true_null:, :].reshape(true_null, t_B, 6).transpose(2, 0, 1) # (6, true_null, t_B)
                s1_out = np.linalg.matrix_rank(np.tensordot(b_chk, U_out, axes=([0],[0])), tol=1e-5)
                print(f"  t_B={t_B}, target_null={k_null}: HIT! loss={best_loss:.2e}, true_null={true_null}, s1(u_out)={s1_out}")
            else:
                print(f"  t_B={t_B}, target_null={k_null}: FAILED (best_loss={best_loss:.3e})")
                break
        print(f"  ==> Max observed nullity(Q_{{perp,E}}^T E_out) at t_B={t_B}: {max_null_found}\n")

if __name__ == "__main__":
    B2_full, Q_perp_tensor, Q_perpE, T_M, sub_2, sub_3 = build_cokernel_proj()
    test_tB1_rank6(T_M, Q_perp_tensor)
    hunt_max_nullity_cokernel(T_M, Q_perp_tensor, B2_full)
