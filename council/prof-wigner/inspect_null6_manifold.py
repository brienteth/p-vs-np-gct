"""Prof. Wigner Round 7 (GAP 2):
Map out the ENTIRE manifold of t_B = 4 protruding matrices B_{2,out} achieving nullity(M(B2_out)) >= 6!
For every zero found from 20 random starts:
  - Lift U_out back to full U = (U_in | U_out) in E_full (20 + 4 = 24 wires)
  - Measure:
    1) true_null = dim_F ker M(B2_out)
    2) s1(U_out) and s1(U_full)
    3) constant wire support c_out = dim_F R(U_out) and c_full = dim_F R(U)
    4) whether there exists ANY rank-15 15D subspace B2_in of S_{6,3} carrying all 6 syzygies
       (or only a smaller subset, as in Star-Koszul!).
"""
import numpy as np
from scipy.optimize import minimize
import sys
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council/prof-noether")
from general_n2k_noether import build_Mn
from test_gap2_cokernel_bound import build_cokernel_proj

def map_null6_manifold():
    print("=" * 74)
    print("MAPPING THE ENTIRE {null(M(B2_out)) >= 6} MANIFOLD AT t_B = 4 (20 STARTS)")
    print("=" * 74)
    B2_full, Q_perp_tensor, Q_perpE, T_M, sub_2, sub_3 = build_cokernel_proj()

    # Also build E_full (315 x 120) and exact solver for u_in given u_out * B2_out in im(E_full)
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
    # Pseudoinverse of E_full (exact since E_full has full column rank 120!)
    E_pinv = np.linalg.pinv(E_full) # 120 x 315

    # Build E_basis (70, 315, 6)
    E_basis = np.zeros((70, 315, 6), dtype=float)
    for q in range(70):
        rq = Q_perp_tensor[q]
        for J in range(15):
            for a in range(6):
                for b in range(6):
                    val = rq[b, J]
                    if val != 0:
                        m = (min(a, b), max(a, b))
                        E_basis[q, J * 21 + mon_idx[m], a] += val

    rng = np.random.default_rng(2026)
    b_chk = rng.standard_normal(6)
    t_B = 4
    k_null = 6
    n_c = t_B * 70
    n_v = (6 * t_B) * k_null

    stats = []
    for start in range(20):
        p0 = rng.standard_normal(n_c + n_v) * 0.3
        def loss_and_grad(p):
            C = p[:n_c].reshape(t_B, 70)
            V = p[n_c:].reshape(t_B, 6, k_null)
            M_C = np.einsum("tq,mqa->mta", C, T_M)
            R = np.einsum("mta,tak->mk", M_C, V)
            G_C = C @ C.T - np.eye(t_B)
            V_flat = V.reshape(6 * t_B, k_null)
            G_V = V_flat.T @ V_flat - np.eye(k_null)
            loss = 0.5 * (np.sum(R**2) + np.sum(G_C**2) + np.sum(G_V**2))
            g_MC = np.einsum("mk,tak->mta", R, V)
            g_C = np.einsum("mta,mqa->tq", g_MC, T_M) + 2.0 * (G_C @ C)
            g_V = np.einsum("mta,mk->tak", M_C, R) + 2.0 * (V_flat @ G_V).reshape(t_B, 6, k_null)
            return loss, np.concatenate([g_C.reshape(-1), g_V.reshape(-1)])

        res = minimize(loss_and_grad, p0, jac=True, method='L-BFGS-B', options={'maxiter': 500, 'ftol': 1e-15, 'gtol': 1e-12})
        if res.fun < 1e-9:
            C = res.x[:n_c].reshape(t_B, 70)
            M_C = np.einsum("tq,mqa->mta", C, T_M).reshape(195, 24)
            svals = np.linalg.svd(M_C, compute_uv=False)
            true_null = int(np.sum(svals < 1e-6))
            _, _, Vt = np.linalg.svd(M_C, full_matrices=True)
            U_out_flat = Vt[-true_null:, :] # (true_null, 24), where 24 = t_B * 6
            U_out = U_out_flat.reshape(true_null, t_B, 6).transpose(2, 0, 1) # (6, true_null, t_B)

            # Compute E_out @ U_out_flat^T in R^{315} -> lift to u_in in R^{120}!
            # E_out_C has shape (315, t_B, 6) -> (315, 24)
            E_out_C = np.einsum("tq,qra->rta", C, E_basis).reshape(315, 24)
            quad_vecs = E_out_C @ U_out_flat.T # (315, true_null)
            # Check projection error onto im(E_full)
            U_in_cols = - E_pinv @ quad_vecs # (120, true_null)
            rec_err = np.linalg.norm(E_full @ U_in_cols + quad_vecs)
            assert rec_err < 1e-6, f"Lift failed: {rec_err}"

            # U_in has shape (6, true_null, 20)
            U_in = U_in_cols.T.reshape(true_null, 6, 20).transpose(1, 0, 2)
            # Full U on 24 wires (20 canonical + 4 protruding): (6, true_null, 24)
            U_full = np.concatenate([U_in, U_out], axis=2)

            s1_out = np.linalg.matrix_rank(np.tensordot(b_chk, U_out, axes=([0],[0])), tol=1e-6)
            s1_full = np.linalg.matrix_rank(np.tensordot(b_chk, U_full, axes=([0],[0])), tol=1e-6)
            c_out = np.linalg.matrix_rank(U_out.reshape(6 * true_null, 4), tol=1e-6)
            c_in = np.linalg.matrix_rank(U_in.reshape(6 * true_null, 20), tol=1e-6)
            c_full = np.linalg.matrix_rank(U_full.reshape(6 * true_null, 24), tol=1e-6)

            # Check rank of B2_out(b_chk) and how many canonical wires U_in actually uses (20 - nullity of U_in)
            B2_out = np.einsum("tq,qcJ->ctJ", C, Q_perp_tensor)
            rk_B2out = np.linalg.matrix_rank(np.tensordot(b_chk, B2_out, axes=([0],[0])), tol=1e-6)
            # Also check rank of B2_out as a 15x6-flattened (4 x 90) or column-space dimension in R^{15}:
            col_B2out = np.linalg.matrix_rank(B2_out.transpose(2, 0, 1).reshape(15, 24), tol=1e-6)

            stats.append((true_null, s1_out, s1_full, c_out, c_in, c_full, rk_B2out, col_B2out))
            print(f"  Start {start+1:2d}: null={true_null}, s1_out={s1_out}, s1_full={s1_full}, c_out={c_out}, c_in={c_in}, c_full={c_full}, rk_B2out={rk_B2out}, col_B2out={col_B2out}")
        else:
            print(f"  Start {start+1:2d}: stalled at loss={res.fun:.3e}")

    print("\nSummary of all converged {null >= 6} solutions:")
    print(f"  Converged: {len(stats)}/20")
    if stats:
        print(f"  Distinct (null, s1_out, s1_full, c_out, c_in, c_full, rk_B2out, col_B2out):")
        for row in sorted(set(stats)):
            print(f"    {row} (count={stats.count(row)})")

if __name__ == "__main__":
    map_null6_manifold()
