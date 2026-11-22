"""Prof. Wigner Round 6:
1. Classify syzygy loci of B_{2,full}|_H across H in Gr(6-k, 6) for k=2,3,4.
2. Check Witness 3 & Witness 5 with full rank(B2)=15.
3. Adversarial search over F_p and R for t_B in {2,3,4} protruding rows yielding s_1 >= 3,
   testing Noether's GL_19 gauge-collapse hypothesis (c = dim_F R(B1) <= 4 vs >= 5).
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

def build_syz_mat_float(B2_tensor):
    # B2_tensor: (6, 19, 15) -> returns (315, 114)
    mons_2 = [(a, b) for a in range(6) for b in range(a, 6)]
    mon_idx = {m: i for i, m in enumerate(mons_2)}
    E = np.zeros((315, 114), dtype=float)
    for J in range(15):
        for a in range(6):
            for b in range(a, 6):
                r = J * 21 + mon_idx[(a, b)]
                for ell in range(19):
                    E[r, a * 19 + ell] += B2_tensor[b, ell, J]
                    if a != b:
                        E[r, b * 19 + ell] += B2_tensor[a, ell, J]
    return E

def test_codim2_orbits():
    print("=" * 74)
    print("1. EXACT CLASSIFICATION OF CODIMENSION-2 SUBSPACES H c F^6 (S_6 ORBITS)")
    print("=" * 74)
    B2_full, _, sub_2, sub_3 = build_B2_full_int()

    def syz_dim_on_H(P_mat):
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
        return d * 20 - rank_matrix_mod(E, MOD)

    # Test all natural S_6-orbit representatives of 2-planes H^perp in F^6:
    # A) 2-planes H^perp spanned by two coordinate vectors: e_4, e_5 (b_4 = b_5 = 0)
    # B) H^perp = span(e_4, e_0 - e_1) (b_4 = 0, b_0 = b_1)
    # C) H^perp = span(e_0 - e_1, e_2 - e_3) (b_0 = b_1, b_2 = b_3)
    # D) H^perp = span(e_0 - e_1, e_1 - e_2) (b_0 = b_1 = b_2)
    # E) H^perp = span(e_0 + e_1 + e_2 + e_3 + e_4 + e_5, e_0 - e_1)
    # F) H^perp = span(e_0 + alpha e_1, e_2 + beta e_3) (two disjoint support-2 forms!)
    cases = []
    # A: b4=0, b5=0
    P_A = np.eye(6, dtype=np.int64)[:, :4]
    cases.append(("H^perp = span(e4, e5) [support 2]", P_A))
    # B: b4=0, b0=b1
    P_B = np.array([[1,0,0,0],[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,0],[0,0,0,1]], dtype=np.int64)
    cases.append(("H^perp = span(e4, e0-e1) [support 3]", P_B))
    # C: b0=b1, b2=b3
    P_C = np.array([[1,0,0,0],[1,0,0,0],[0,1,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]], dtype=np.int64)
    cases.append(("H^perp = span(e0-e1, e2-e3) [disj pairs]", P_C))
    # D: b0=b1=b2
    P_D = np.array([[1,0,0,0],[1,0,0,0],[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]], dtype=np.int64)
    cases.append(("H^perp = span(e0-e1, e1-e2) [3 equal]", P_D))
    # E: b0+2 b1=0, b2+3 b3=0 (generic coeff support-2 pairs)
    P_F = np.array([[2,0,0,0],[MOD-1,0,0,0],[0,3,0,0],[0,MOD-1,0,0],[0,0,1,0],[0,0,0,1]], dtype=np.int64)
    cases.append(("H^perp = span(e0+2e1, e2+3e3) [gen disj 2]", P_F))
    # G: H^perp = span(e0 + e1 + e2, e3 + e4 + e5)
    P_G = np.array([[1,1,0,0],[MOD-1,0,0,0],[0,MOD-1,0,0],[0,0,1,1],[0,0,MOD-1,0],[0,0,0,MOD-1]], dtype=np.int64)
    cases.append(("H^perp = span(e0+e1+e2, e3+e4+e5)", P_G))
    # H: What about e4 + c*e5? Wait, span(e4 + c*e5, anything): NO! span(e4, e5) ONLY depends on the 2-plane!
    # Wait: what about span(e0 + e1, e0 - e2)?
    # Let's check span(e4, e5) with arbitrary non-zero diagonal scaling D = diag(1,2,3,4,5,6):
    # Wait: D changes b_i -> d_i b_i, which preserves b_4=b_5=0!
    for name, P in cases:
        print(f"  {name:44s}: syz_dim = {syz_dim_on_H(P)}")

def test_adversarial_search_tB(t_B_list=(2, 3, 4)):
    """Actively hunt for protruding rows B2_out (shape 6 x t_B x 15) that produce
    degree-1 syzygies of high F(b)-rank s_1 >= 3, WITHOUT restricting B2_out to coordinate forms!
    Measure F-syz_dim, F(b)-rank s_1, rank(B2), and constant wire support c = dim_F R(B1)."""
    print("\n" + "=" * 74)
    print("2. ADVERSARIAL OPTIMIZATION HUNT FOR HIGH-RANK SYZYGIES AT t_B = 2, 3, 4")
    print("=" * 74)
    B2_full, _, sub_2, sub_3 = build_B2_full_int()
    B2_full_f = B2_full.astype(float)
    rng = np.random.default_rng(137)

    # Precompute index map for fast E matrix construction from B2 (6, 19, 15)
    mons_2 = [(a, b) for a in range(6) for b in range(a, 6)]
    mon_idx = {m: i for i, m in enumerate(mons_2)}
    # Linear operator mapping B2 (6, 19, 15) to E (315, 114):
    # E[J*21 + mon_idx[(a,b)], a*19 + ell] += B2[b, ell, J]
    # Better: build E_in (315, 6*(19-t_B)) once, and map B2_out (6, t_B, 15) to E_out (315, 6*t_B) fast!

    for t_B in t_B_list:
        n_in = 19 - t_B
        # Try several choices of which (t_B + 1) canonical wires to drop from B2_full
        # e.g. drop wires that still leave rank_K(B2_in) = 15 (actually B2_full has 20 rows, rank 15, so dropping 5 still usually leaves rank 15? Wait: 19 - t_B >= 15 for t_B <= 4!)
        # For t_B = 4, n_in = 15!
        drop_sets = [
            list(range(t_B + 1)),
            [0, 1, 2, 18, 19][:t_B + 1],
        ]
        # Make sure B2_in has rank 15:
        for d_idx, drops in enumerate(drop_sets):
            keep = [i for i in range(20) if i not in drops]
            B2_in = B2_full_f[:, keep, :] # (6, n_in, 15)
            b_test = rng.standard_normal(6)
            rk_in = np.linalg.matrix_rank(np.tensordot(b_test, B2_in, axes=([0],[0])))
            # Build E_in (315, 6 * n_in)
            E_in = np.zeros((315, 6 * n_in), dtype=float)
            for J in range(15):
                for a in range(6):
                    for b in range(a, 6):
                        r = J * 21 + mon_idx[(a, b)]
                        for ell in range(n_in):
                            E_in[r, a * n_in + ell] += B2_in[b, ell, J]
                            if a != b:
                                E_in[r, b * n_in + ell] += B2_in[a, ell, J]
            # QR of E_in (since E_in has full column rank 6*n_in!):
            Q_in, _ = np.linalg.qr(E_in)
            # Note: im(E_in) cap im(E_out) != {0} iff P_in_perp @ E_out drops rank!
            # Wait: more directly, for E = [E_in_reordered | E_out_reordered] (columns ordered as c*19 + ell),
            # singular values of [Q_in, E_out] are small iff E_out hits im(E_in) or drops rank!
            # Even better: minimize sum of smallest `target_syz` singular values of (I - Q_in Q_in^T) @ E_out!
            # Why? Because E_in has full column rank, nullity([E_in, E_out]) == nullity((I - P_in) E_out)!
            # AND notice: E_out has only 6 * t_B columns (12, 18, or 24 columns!!), whereas E had 114!
            # THAT'S A HUGE REDUCTION: minimizing smallest singular values of a 315 x (6*t_B) matrix!!
            P_in_perp = np.eye(315) - Q_in @ Q_in.T

            for target_syz in [3, 4, 5, 6]:
                if target_syz > 6 * t_B:
                    continue
                found = False
                best_loss = 1e9
                for start in range(4):
                    p0 = rng.standard_normal(6 * t_B * 15)
                    def loss_fn(p):
                        B2_out = p.reshape(6, t_B, 15)
                        E_out = np.zeros((315, 6 * t_B), dtype=float)
                        for J in range(15):
                            for a in range(6):
                                for b in range(a, 6):
                                    r = J * 21 + mon_idx[(a, b)]
                                    for ell in range(t_B):
                                        E_out[r, a * t_B + ell] += B2_out[b, ell, J]
                                        if a != b:
                                            E_out[r, b * t_B + ell] += B2_out[a, ell, J]
                        # Normalize columns/frobenius to avoid trivial B2_out -> 0 collapse:
                        nrm = np.linalg.norm(B2_out)
                        M_proj = P_in_perp @ (E_out / (nrm + 1e-12))
                        svals = np.linalg.svd(M_proj, compute_uv=False)
                        # Minimize smallest `target_syz` singular values PLUS penalty if B2_out has near-zero row
                        row_norms = np.sum(B2_out**2, axis=(0, 2)) / (nrm**2 + 1e-12)
                        min_row_pen = np.sum(np.maximum(0.0, 0.05 - row_norms)**2) * 100.0
                        return np.sum(svals[-target_syz:]**2) + min_row_pen

                    res = minimize(loss_fn, p0, method='BFGS', options={'maxiter': 250})
                    if res.fun < best_loss:
                        best_loss = res.fun
                        best_p = res.x
                    if res.fun < 1e-10:
                        found = True
                        break

                if best_loss < 1e-8:
                    B2_out = best_p.reshape(6, t_B, 15)
                    E_out = np.zeros((315, 6 * t_B), dtype=float)
                    for J in range(15):
                        for a in range(6):
                            for b in range(a, 6):
                                r = J * 21 + mon_idx[(a, b)]
                                for ell in range(t_B):
                                    E_out[r, a * t_B + ell] += B2_out[b, ell, J]
                                    if a != b:
                                        E_out[r, b * t_B + ell] += B2_out[a, ell, J]
                    # Compute nullspace of [E_in | E_out]
                    E_joint = np.hstack([E_in, E_out]) # 315 x (6*19)
                    U, S, Vt = np.linalg.svd(E_joint, full_matrices=True)
                    null_dim = int(np.sum(S < 1e-6))
                    # Actually Vt has shape (114, 114); last null_dim rows are nullspace!
                    if null_dim > 0:
                        N_vecs = Vt[-null_dim:, :] # (null_dim, 114)
                        # First 6*n_in coords are u_in (order c*n_in + ell), last 6*t_B are u_out (order c*t_B + ell)
                        B1_in_part = N_vecs[:, :6*n_in].reshape(null_dim, 6, n_in).transpose(1, 0, 2)
                        B1_out_part = N_vecs[:, 6*n_in:].reshape(null_dim, 6, t_B).transpose(1, 0, 2)
                        B1_max = np.concatenate([B1_in_part, B1_out_part], axis=2) # (6, null_dim, 19)
                        B1_val = np.tensordot(b_test, B1_max, axes=([0],[0]))
                        s1_max = np.linalg.matrix_rank(B1_val, tol=1e-6)
                        c_wires = np.linalg.matrix_rank(B1_max.reshape(6 * null_dim, 19), tol=1e-6)
                        c_in = np.linalg.matrix_rank(B1_in_part.reshape(6 * null_dim, n_in), tol=1e-6)
                        B2_comb = np.concatenate([B2_in, B2_out], axis=1)
                        rk_B2 = np.linalg.matrix_rank(np.tensordot(b_test, B2_comb, axes=([0],[0])), tol=1e-6)
                        print(f"  t_B={t_B} drop#{d_idx} (rk_in={rk_in}) target={target_syz}: HIT! null={null_dim}, s1_max={s1_max}, c={c_wires} (c_in={c_in}), rk_B2={rk_B2}")
                    else:
                        print(f"  t_B={t_B} drop#{d_idx} target={target_syz}: loss={best_loss:.2e} but null=0")
                else:
                    print(f"  t_B={t_B} drop#{d_idx} (rk_in={rk_in}) target={target_syz}: NO HIT (best_loss={best_loss:.3e})")

if __name__ == "__main__":
    test_codim2_orbits()
    test_adversarial_search_tB()
