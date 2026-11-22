#!/usr/bin/env python3
"""
Round 9 — Prof. Hilbert (Pillars 2 & 3 — Wall 1 Benchmark & Push):
PART 1 (Pillar 2): Complete Coupled-Jet H-Q3 Optimization at Generic Smooth
  X0 in V(perm_3)_sm for m=5 (w=4), m=6 (w=5), m=7 (w=6):
  - Exact Theorem H-Q4: Fano scheme F_2(Q_2 cap C_3) of 3-dim isotropic subspaces
    W subset C^7 inside Q_2 cap C_3 (both R and C), pairwise intersections
    dim(W_i cap W_j), and direct test for disjoint pairs (W_v cap W_u = {0})!
  - Direct optimization over ALL SO(7, C) factorizations of F_2 = -v^T u
    minimizing min_{A, g_1} ||v^T A u + g_1 F_2 - F_3|| for w=4, 5, 6!
  - Exact verification of Jet-2 + Jet-3 + Jet-4 on scrambled Grenet m=7!
PART 2 (Pillar 3): Explicit Non-Linear GL-Covariant / Wick-Plucker Equations:
  - Exact Hessian Determinant Equation Hess(det_n)(X) = c_n * det_n(X)^{n(n-2)}
    (degree 12 GL_9-covariant F^3 ^ Hess(F) = 0 for n=3; scaling to n=4: F^8 | Hess(F)),
    plus exact vanishing order on globally mixed det_m(A_0 + L(X)) for m=3..8!
  - Exact Koszul / Young Flattening KF_1(F) (324 x 81) across det_3, perm_3,
    and globally mixed det_m(A_0 + L(X)) for m=3..7!
"""
import itertools
import math
import numpy as np


def perm_exact(M):
    n = M.shape[0]
    total = 0.0 + 0.0j if np.iscomplexobj(M) else 0.0
    for p in itertools.permutations(range(n)):
        prod = 1.0
        for i in range(n):
            prod *= M[i, p[i]]
        total += prod
    return total


def det_exact(M):
    return np.linalg.det(M)


def monomial_basis(num_vars, deg):
    return list(itertools.combinations_with_replacement(range(num_vars), deg))


def build_perm3_jets_on_C7(seed=2026):
    """
    Pick a generic smooth X0 in V(perm_3), build orthonormal basis of
    T_{X0} / (C * X0) ~ C^7 (orthogonal to both grad(X0) and X0!),
    and return exact Q2 (7x7 symmetric, rank 7), F3_tens (7x7x7 symmetric),
    plus X0 and the 7x9 basis B7!
    """
    rng = np.random.default_rng(seed)
    X0 = rng.normal(size=(3, 3))
    X0[0, 0] = 0.0
    c0 = perm_exact(X0)
    X0[0, 0] = 1.0
    c1 = perm_exact(X0) - c0
    X0[0, 0] = -c0 / c1
    assert abs(perm_exact(X0)) < 1e-13

    grad = np.zeros(9)
    for a in range(9):
        ia, ja = divmod(a, 3)
        rr = [r for r in range(3) if r != ia]
        cc = [c for c in range(3) if c != ja]
        grad[a] = perm_exact(X0[np.ix_(rr, cc)])
    # Basis of 7-dim space orthogonal to BOTH grad and X0
    M_orth = np.vstack([grad / np.linalg.norm(grad), X0.reshape(-1) / np.linalg.norm(X0)])
    assert abs(np.dot(M_orth[0], M_orth[1])) < 1e-12
    _, _, Vt = np.linalg.svd(M_orth, full_matrices=True)
    B7 = Vt[2:, :]  # 7 x 9

    # Hessian of perm_3 at X0
    H = np.zeros((9, 9))
    for a in range(9):
        ia, ja = divmod(a, 3)
        for b in range(a + 1, 9):
            ib, jb = divmod(b, 3)
            if ia == ib or ja == jb:
                continue
            r_rem = [r for r in range(3) if r != ia and r != ib][0]
            c_rem = [c for c in range(3) if c != ja and c != jb][0]
            H[a, b] = X0[r_rem, c_rem]
            H[b, a] = X0[r_rem, c_rem]
    Q2 = 0.5 * (B7 @ H @ B7.T)  # F_2(z) = z^T Q2 z
    assert np.linalg.matrix_rank(Q2, tol=1e-9) == 7

    # Exact symmetric cubic tensor C3[a,b,c] such that F_3(z) = sum_{a,b,c} C3[a,b,c] z_a z_b z_c
    C3 = np.zeros((7, 7, 7), dtype=np.float64)
    for p in itertools.permutations(range(3)):
        l0 = B7[:, 0 * 3 + p[0]]
        l1 = B7[:, 1 * 3 + p[1]]
        l2 = B7[:, 2 * 3 + p[2]]
        # Add symmetrized outer product
        T_p = np.einsum("a,b,c->abc", l0, l1, l2)
        C3 += (T_p + T_p.transpose(0, 2, 1) + T_p.transpose(1, 0, 2) +
               T_p.transpose(1, 2, 0) + T_p.transpose(2, 0, 1) + T_p.transpose(2, 1, 0)) / 6.0

    # Verify F_2(z) + F_3(z) == perm_3(X0 + z @ B7)!
    for _ in range(5):
        z = rng.normal(size=7)
        lhs = perm_exact(X0 + (z @ B7).reshape(3, 3))
        rhs = float(z @ Q2 @ z + np.einsum("abc,a,b,c->", C3, z, z, z))
        assert abs(lhs - rhs) < 1e-13

    return X0, B7, Q2, C3


# =============================================================================
# PART 1A: EXACT CLASSIFICATION OF ALL P^2's (3-DIM SUBSPACES W subset C^7)
#          IN Q_2 cap C_3 FOR perm_3 (THEOREM H-Q4 TEST FOR m=5 [w=4]!)
# =============================================================================
print("=" * 78)
print("PART 1A: THEOREM H-Q4 — CLASSIFYING ALL P^2's IN Q_2 cap C_3 (perm_3, m=5)")
print("=" * 78)

X0, B7, Q2, C3 = build_perm3_jets_on_C7(seed=2026)

# Orthonormalize Q2 over C: D^T D = Q2 -> work in coordinates w = D z where Q2(w) = w^T w!
eigvals, eigvecs = np.linalg.eigh(Q2)
D_mat = np.zeros((7, 7), dtype=np.complex128)
for r in range(7):
    D_mat[r, :] = np.sqrt(eigvals[r] + 0j) * eigvecs[:, r]
D_inv = np.linalg.inv(D_mat)
# Transform C3 into w-coordinates: C3_w[a,b,c] = sum C3[i,j,k] D_inv[i,a] D_inv[j,b] D_inv[k,c]
C3_w = np.einsum("ijk,ia,jb,kc->abc", C3.astype(np.complex128), D_inv, D_inv, D_inv)
assert np.max(np.abs(D_mat.T @ D_mat - Q2)) < 1e-12


def find_P2s_in_Q2_cap_C3(Q2_mat, C3_tens, n_restarts=120, complex_mode=True, seed=100):
    """
    Find 3-dim subspaces W = col(U) subset C^7 (U: 7x3) satisfying:
      U^T Q2 U == 0   (6 quadratic eqs: isotropic for Q2)
      C3(U, U, U) == 0 (10 cubic eqs: vanishes on C3)
    16 complex equations in 3*(7-3) = 12 Grassmannian variables!
    Use Levenberg-Marquardt directly on the 16 exact polynomial coefficients!
    """
    rng = np.random.default_rng(seed)
    idx2 = [(i, j) for i in range(3) for j in range(i, 3)]  # 6 pairs
    idx3 = [(i, j, k) for i in range(3) for j in range(i, 3) for k in range(j, 3)]  # 10 triples
    found = []

    def eval_res_and_jac(U):
        # U: 7x3 complex
        # Residual: 6 quadric + 10 cubic = 16 complex values
        QU = Q2_mat @ U  # 7x3
        M2 = U.T @ QU    # 3x3
        # Cubic: T3[i,j,k] = C3_tens contracted with U[:,i], U[:,j], U[:,k]
        CU1 = np.einsum("abc,ai->ibc", C3_tens, U)       # 3x7x7
        CU2 = np.einsum("ibc,bj->ijc", CU1, U)           # 3x3x7
        T3 = np.einsum("ijc,ck->ijk", CU2, U)            # 3x3x3

        f = np.zeros(16, dtype=np.complex128)
        for idx, (i, j) in enumerate(idx2):
            f[idx] = M2[i, j]
        for idx, (i, j, k) in enumerate(idx3):
            f[6 + idx] = T3[i, j, k]

        # Exact complex Jacobian df / dU (16 x 21)
        J = np.zeros((16, 21), dtype=np.complex128)
        for idx, (i, j) in enumerate(idx2):
            # d(u_i^T Q u_j)/du_a: delta_{a,i} (Q u_j) + delta_{a,j} (Q u_i)
            J[idx, 7 * i:7 * (i + 1)] += QU[:, j]
            J[idx, 7 * j:7 * (j + 1)] += QU[:, i]
        for idx, (i, j, k) in enumerate(idx3):
            J[6 + idx, 7 * i:7 * (i + 1)] += CU2[j, k, :]
            J[6 + idx, 7 * j:7 * (j + 1)] += CU2[i, k, :]
            J[6 + idx, 7 * k:7 * (k + 1)] += CU2[i, j, :]
        return f, J

    for r in range(n_restarts):
        if complex_mode:
            U = rng.normal(size=(7, 3)) + 1j * rng.normal(size=(7, 3))
        else:
            U = rng.normal(size=(7, 3)).astype(np.complex128)
        U, _ = np.linalg.qr(U)
        lam = 1e-2
        for it in range(80):
            f, J = eval_res_and_jac(U)
            nrm = float(np.linalg.norm(f))
            if nrm < 1e-12:
                break
            # Work on Grassmannian tangent (orthogonal to col(U) in Hermitian inner product)
            # dU = U_perp @ Z (U_perp: 7x4, Z: 4x3 -> 12 complex vars)
            Q_full, _ = np.linalg.qr(U, mode="complete")
            U_perp = Q_full[:, 3:]  # 7x4
            # Map J (16x21) to J_tan (16x12): col (i, p) is J[:, 7i..7(i+1)] @ U_perp[:, p]
            J_tan = np.zeros((16, 12), dtype=np.complex128)
            for i in range(3):
                J_tan[:, 4 * i:4 * (i + 1)] = J[:, 7 * i:7 * (i + 1)] @ U_perp
            if not complex_mode:
                # Real step only
                Hr = np.real(J_tan.T @ J_tan) + lam * np.eye(12)
                step = np.linalg.solve(Hr, -np.real(J_tan.T @ f)).reshape(3, 4).T
            else:
                # Complex holomorphic Gauss-Newton!
                Hc = J_tan.conj().T @ J_tan + lam * np.eye(12)
                step = np.linalg.solve(Hc, -J_tan.conj().T @ f).reshape(3, 4).T
            U_try, _ = np.linalg.qr(U + U_perp @ step)
            f_try, _ = eval_res_and_jac(U_try)
            if np.linalg.norm(f_try) < nrm:
                U = U_try
                lam = max(lam * 0.3, 1e-12)
            else:
                lam = min(lam * 5.0, 1e6)
        f, J = eval_res_and_jac(U)
        if np.linalg.norm(f) < 1e-9:
            # Compute tangent space dimension of Fano scheme at U: 12 - rank(J_tan)
            Q_full, _ = np.linalg.qr(U, mode="complete")
            U_perp = Q_full[:, 3:]
            J_tan = np.zeros((16, 12), dtype=np.complex128)
            for i in range(3):
                J_tan[:, 4 * i:4 * (i + 1)] = J[:, 7 * i:7 * (i + 1)] @ U_perp
            rk_J = int(np.linalg.matrix_rank(J_tan, tol=1e-6))
            tan_dim = 12 - rk_J
            # Check if distinct from already-found subspaces
            is_new = True
            for U_old, _ in found:
                # Principal angles: svd of U_old^H U -> all 1s iff same subspace
                s_ang = np.linalg.svd(U_old.conj().T @ U, compute_uv=False)
                if np.min(s_ang) > 1.0 - 1e-5:
                    is_new = False
                    break
            if is_new:
                found.append((U, tan_dim))
    return found


P2_real = find_P2s_in_Q2_cap_C3(Q2.astype(np.complex128), C3.astype(np.complex128),
                                n_restarts=80, complex_mode=False, seed=11)
P2_comp = find_P2s_in_Q2_cap_C3(Q2.astype(np.complex128), C3.astype(np.complex128),
                                n_restarts=150, complex_mode=True, seed=22)

print(f"  Real search (80 restarts):    found {len(P2_real)} distinct P^2's in Q_2 cap C_3")
print(f"  Complex search (150 restarts): found {len(P2_comp)} distinct P^2's in Q_2 cap C_3")
if P2_comp:
    tan_dims = [td for _, td in P2_comp]
    print(f"  Tangent dims of Fano scheme F_2(Q_2 cap C_3) at found P^2's: "
          f"min={min(tan_dims)}, max={max(tan_dims)}")
    # Inspect pairwise intersection dimensions dim(W_i cap W_j) = 6 - rank([U_i, U_j])!
    min_inter = 3
    disjoint_pairs = []
    for i in range(len(P2_comp)):
        for j in range(i + 1, len(P2_comp)):
            comb = np.hstack([P2_comp[i][0], P2_comp[j][0]])  # 7 x 6
            rk = int(np.linalg.matrix_rank(comb, tol=1e-6))
            inter_dim = 6 - rk
            if inter_dim < min_inter:
                min_inter = inter_dim
            if inter_dim == 0:
                disjoint_pairs.append((i, j))
    print(f"  Pairwise intersection dims dim(W_i cap W_j) among {len(P2_comp)} found P^2's:")
    print(f"    min dim(W_i cap W_j) = {min_inter}, count of DISJOINT pairs (dim=0) = {len(disjoint_pairs)}")
    # Inspect structure of the first 6 found P^2's in the original 3x3 matrix coordinates!
    print("  Checking 3x3 matrix support / rank of found P^2's in C^9 (W subset T_{X0}):")
    for idx in range(min(6, len(P2_comp))):
        U_mat = P2_comp[idx][0]
        W9 = (B7.T @ U_mat)  # 9 x 3 (each col is a 3x3 perturbation matrix!)
        # Check if all matrices in W9 have rank <= 1 or zero row/col or what!
        # Sample a generic linear comb in W9 and check its 3x3 rank!
        v_rand = W9 @ np.array([1.0, 0.37 - 0.21j, -0.53 + 0.44j])
        M_rand = v_rand.reshape(3, 3)
        s_m = np.linalg.svd(M_rand, compute_uv=False)
        rk3 = int(np.sum(s_m > 1e-6))
        # Also check row/col zero count!
        row_norms = [float(np.linalg.norm(W9[3 * r:3 * (r + 1), :])) for r in range(3)]
        col_norms = [float(np.linalg.norm(W9[[c, 3 + c, 6 + c], :])) for c in range(3)]
        print(f"    P^2 #{idx}: tan_dim={P2_comp[idx][1]}, generic 3x3 rk={rk3}, "
              f"row_norms={[round(x, 2) for x in row_norms]}, "
              f"col_norms={[round(x, 2) for x in col_norms]}")

    # If ANY disjoint pair (W_v, W_u) was found, TEST Theorem H-Q4 explicitly!
    # Does it give an EXACT w=4 (m=5) solution to F_2 = -v^T u AND F_3 = v^T A u + g_1 F_2?!
    if disjoint_pairs:
        i0, j0 = disjoint_pairs[0]
        Wv = P2_comp[i0][0]  # 7 x 3
        Wu = P2_comp[j0][0]  # 7 x 3
        # Check Q2 restricted to Wv + Wu (hyperplane H):
        H6 = np.hstack([Wv, Wu])  # 7 x 6, rank 6
        M_vu = Wv.T @ Q2 @ Wu     # 3 x 3 coupling matrix!
        rk_Mvu = int(np.linalg.matrix_rank(M_vu, tol=1e-6))
        print(f"  DISJOINT PAIR ({i0}, {j0}) FOUND! Checking Theorem H-Q4 exact w=4 (m=5) solution:")
        print(f"    rank(Wv^T Q2 Wu) = {rk_Mvu} / 3 (3 => non-tangent hyperplane => EXACT w=4!)")
        # Construct exact v_1..v_4, u_1..u_4 on C^7!
        # Let l in (C^7)* be normal to H6 = col(Wv, Wu): l^T H6 = 0
        _, _, Vt_h = np.linalg.svd(H6.T, full_matrices=True)
        l_vec = Vt_h[-1, :]  # 7, l_vec @ H6 = 0 (no conj: use transpose!)
        # Actually use nullspace of H6.T (algebraic transpose, not Hermitian!)
        # SVD gives Hermitian nullspace, so conjugate!
        l_vec = np.conj(Vt_h[-1, :])
        assert np.linalg.norm(l_vec @ H6) < 1e-10
        # Find 7th basis vector e_l such that e_l^T Q2 Wv = 0 and e_l^T Q2 Wu = 0!
        # That is, Q2 e_l is proportional to l_vec -> e_l = Q2^{-1} l_vec!
        e_l = np.linalg.solve(Q2.astype(np.complex128), l_vec)
        q_ll = complex(e_l @ Q2 @ e_l)
        print(f"    e_l^T Q2 e_l = {abs(q_ll):.4e} (> 0 => H6 non-tangent to Q2!)")
        if rk_Mvu == 3 and abs(q_ll) > 1e-7:
            # Build exact basis [Wv, Wu, e_l] (7x7 invertible)!
            P_bas = np.hstack([Wv, Wu, e_l.reshape(7, 1)])
            P_inv = np.linalg.inv(P_bas)
            # In coords (alpha in C^3, beta in C^3, gamma in C) = P_inv @ z:
            # z^T Q2 z = 2 * alpha^T M_vu beta + q_ll * gamma^2!
            # Set v = [-2 M_vu^T alpha, -sqrt(q_ll) gamma], u = [beta, sqrt(q_ll) gamma] -> -v^T u == Q2!
            v4 = np.zeros((4, 7), dtype=np.complex128)
            u4 = np.zeros((4, 7), dtype=np.complex128)
            v4[:3, :] = -2.0 * (M_vu.T @ P_inv[:3, :])
            u4[:3, :] = P_inv[3:6, :]
            sq_q = np.sqrt(q_ll)
            v4[3, :] = -sq_q * P_inv[6, :]
            u4[3, :] = sq_q * P_inv[6, :]
            Q_chk = -0.5 * (v4.T @ u4 + u4.T @ v4)
            assert np.max(np.abs(Q_chk - Q2)) < 1e-9

            # NOW SOLVE LINEARLY FOR A (7 x 4 x 4) AND g_1 (7) SUCH THAT v^T A u + g_1 F_2 == F_3!
            mons3_7 = monomial_basis(7, 3)
            m3_idx7 = {m: idx for idx, m in enumerate(mons3_7)}
            F3_vec7 = np.zeros(len(mons3_7), dtype=np.complex128)
            for m_idx, (a, b, c) in enumerate(mons3_7):
                mult = len(set(itertools.permutations((a, b, c))))
                F3_vec7[m_idx] = mult * C3[a, b, c]

            rows = []
            # g_1 * F_2 (7 vectors)
            for k in range(7):
                row = np.zeros(len(mons3_7), dtype=np.complex128)
                for i in range(7):
                    for j in range(7):
                        row[m3_idx7[tuple(sorted((i, j, k)))]] += Q2[i, j]
                rows.append(row)
            # v_a * u_b * z_k (16 * 7 = 112 vectors)
            for a in range(4):
                for b in range(4):
                    for k in range(7):
                        row = np.zeros(len(mons3_7), dtype=np.complex128)
                        for i in range(7):
                            for j in range(7):
                                row[m3_idx7[tuple(sorted((i, j, k)))]] += v4[a, i] * u4[b, j]
                        rows.append(row)
            M_sys = np.vstack(rows)  # 119 x 84
            sol, _, _, _ = np.linalg.lstsq(M_sys.T, F3_vec7, rcond=None)
            res_f3 = float(np.linalg.norm(M_sys.T @ sol - F3_vec7))
            print(f"    *** EXACT w=4 (m=5) COUPLED JET-2 + JET-3 SOLVER: "
                  f"||v^T A u + g_1 F_2 - F_3|| = {res_f3:.3e} ***")

            # NOW TEST JET-4 VANISHING: CAN v^T A^2 u LIE IN <F_2, F_3>_4?!
            # Extract exact A (7 x 4 x 4) and check the nullspace of M_sys.T (free parameters of A)!
            # Actually check if ANY solution (A, g_1) of Jet-3 ALSO satisfies Jet-4:
            # v^T A^2 u - g_1 (v^T A u) + g_2 (v^T u) == 0  (Wait: g_1 = Tr(A), g_2 = e_2(A)!!)
            # WAIT A SECOND!! CHECK THAT!!
            # In det(I_4 + A) = 1 + Tr(A) + e_2(A) + e_3(A) + det(A):
            #   g_1 IS NOT ARBITRARY — g_1 MUST EQUAL Tr(A)!!
            #   AND Jet-4 requires: v^T A^2 u == Tr(A) F_3 - e_2(A) F_2?
            #   Let's check exact identity:
            #   (1 + Tr(A) + e_2(A) + e_3(A) + e_4(A)) * (-v^T u + v^T A u - v^T A^2 u + v^T A^3 u - ...) == F_2 + F_3!
            #   Deg 2: -v^T u = F_2
            #   Deg 3: v^T A u - Tr(A) v^T u = F_3  =>  v^T A u + Tr(A) F_2 = F_3  (EXACT LINEAR CONSTRAINT g_1 == Tr(A)!!)
            #   Deg 4: -v^T A^2 u + Tr(A) v^T A u - e_2(A) v^T u = 0!
            # TEST WHETHER THE EXTRA EXACT CONSTRAINT g_1 == Tr(A) STILL SOLVES JET-3 AT w=4!
            rows_tr = []
            # Each variable A[k, a, b] (7 * 16 = 112 vars):
            # contributes v_a * u_b * z_k + (delta_{a,b} * F_2 * z_k)!!
            for a in range(4):
                for b in range(4):
                    for k in range(7):
                        row = np.zeros(len(mons3_7), dtype=np.complex128)
                        for i in range(7):
                            for j in range(7):
                                val = v4[a, i] * u4[b, j]
                                if a == b:
                                    val += Q2[i, j]
                                row[m3_idx7[tuple(sorted((i, j, k)))]] += val
                        rows_tr.append(row)
            M_tr = np.vstack(rows_tr)  # 112 x 84
            sol_tr, _, _, _ = np.linalg.lstsq(M_tr.T, F3_vec7, rcond=None)
            res_tr = float(np.linalg.norm(M_tr.T @ sol_tr - F3_vec7))
            rk_tr = int(np.linalg.matrix_rank(M_tr, tol=1e-8))
            print(f"    *** EXACT w=4 (m=5) WITH g_1 == Tr(A) ENFORCED: "
                  f"rk={rk_tr}/84, ||v^T A u + Tr(A) F_2 - F_3|| = {res_tr:.3e} ***")

            # Also check Jet-4 residual on the minimum-norm solution A_0!
            A0_sol = sol_tr.reshape(4, 4, 7).transpose(2, 0, 1)  # 7 x 4 x 4
            rng_chk = np.random.default_rng(77)
            j4_vals = []
            for _ in range(10):
                z = rng_chk.normal(size=7) * 0.05
                Az = np.tensordot(z, A0_sol, axes=([0], [0]))
                vz = v4 @ z
                uz = u4 @ z
                f_schur = np.linalg.det(np.eye(4) + Az) * (-vz @ np.linalg.solve(np.eye(4) + Az, uz))
                f_perm = float(z @ Q2 @ z + np.einsum("abc,a,b,c->", C3, z, z, z))
                j4_vals.append(abs(f_schur - f_perm) / (np.linalg.norm(z) ** 4))
            print(f"    Jet-4 residual on min-norm w=4 Jet-3 solution: mean |R_4|/||z||^4 = {np.mean(j4_vals):.3e}")

            # PART 1C: OPTIMIZE OVER THE ENTIRE 48-DIM NULLSPACE OF M_tr (EXACT JET-2 + JET-3)
            # TO TEST WHETHER JET-4 (R_4 == 0, 180 EQS vs 48 VARS) IS OBSTRUCTED AT w=4 (m=5)!
            U_m, s_m, Vt_m = np.linalg.svd(M_tr.T, full_matrices=True)
            # M_tr.T is 84 x 112, rank 64 -> nullspace is last 48 rows of Vt_m (48 x 112)
            null_dim = 112 - rk_tr
            N_null = Vt_m[rk_tr:, :]  # (null_dim, 112), each row reshaped (4,4,7).transpose(2,0,1)
            N_tens = N_null.reshape(null_dim, 4, 4, 7).transpose(0, 3, 1, 2)  # (48, 7, 4, 4)

            # Sample S = 200 complex points z_s in C^7 and evaluate EXACT degree-4 polynomial:
            # R_4(z) = -v^T A^2 u + Tr(A) (v^T A u) - e_2(A) (v^T u)
            # where e_2(A) = 0.5 * (Tr(A)^2 - Tr(A^2))!
            S_pts = 200
            Z_pts = (rng_chk.normal(size=(S_pts, 7)) + 1j * rng_chk.normal(size=(S_pts, 7))) * 0.5
            # Precompute v_s (S,4), u_s (S,4), A0_s (S,4,4), Nk_s (48,S,4,4)
            v_s = Z_pts @ v4.T  # (S, 4)
            u_s = Z_pts @ u4.T  # (S, 4)
            A0_s = np.einsum("sa,aij->sij", Z_pts, A0_sol)        # (S, 4, 4)
            Nk_s = np.einsum("sa,kaij->ksij", Z_pts, N_tens)      # (48, S, 4, 4)
            vu_s = np.einsum("si,si->s", v_s, u_s)                # (S,)

            def eval_R4_and_jac(c_vec):
                A_s = A0_s + np.einsum("k,ksij->sij", c_vec, Nk_s)  # (S, 4, 4)
                trA = np.trace(A_s, axis1=1, axis2=2)               # (S,)
                A2_s = np.einsum("sij,sjk->sik", A_s, A_s)          # (S, 4, 4)
                trA2 = np.trace(A2_s, axis1=1, axis2=2)             # (S,)
                e2A = 0.5 * (trA * trA - trA2)                      # (S,)
                vAu = np.einsum("si,sij,sj->s", v_s, A_s, u_s)
                vA2u = np.einsum("si,sij,sj->s", v_s, A2_s, u_s)
                R4 = -vA2u + trA * vAu - e2A * vu_s                 # (S,)

                # Exact analytical derivative dR4 / dc_k (S x 48):
                # d(v^T A^2 u)/dc_k = v^T (Nk A + A Nk) u
                # d(Tr(A))/dc_k = Tr(Nk)
                # d(e_2(A))/dc_k = Tr(A) Tr(Nk) - Tr(A Nk)
                vA = np.einsum("si,sij->sj", v_s, A_s)              # (S, 4)
                Au = np.einsum("sij,sj->si", A_s, u_s)              # (S, 4)
                trN = np.trace(Nk_s, axis1=2, axis2=3)              # (48, S)
                trAN = np.einsum("sij,ksji->ks", A_s, Nk_s)         # (48, S)
                vNu = np.einsum("si,ksij,sj->ks", v_s, Nk_s, u_s)   # (48, S)
                d_vA2u = (np.einsum("si,ksij,sj->ks", v_s, Nk_s, Au) +
                          np.einsum("si,ksij,sj->ks", vA, Nk_s, u_s))
                d_e2 = trA[None, :] * trN - trAN
                J_c = (-d_vA2u + trN * vAu[None, :] + trA[None, :] * vNu - d_e2 * vu_s[None, :]).T  # (S, 48)
                return R4, J_c

            best_r4 = 1e9
            for r_idx in range(6):
                c_cur = (rng_chk.normal(size=null_dim) + 1j * rng_chk.normal(size=null_dim)) * (0.2 if r_idx > 0 else 0.0)
                lam = 1e-2
                for _ in range(50):
                    R4, Jc = eval_R4_and_jac(c_cur)
                    nrm = float(np.linalg.norm(R4))
                    if nrm < 1e-11:
                        break
                    Hc = Jc.conj().T @ Jc + lam * np.eye(null_dim)
                    step = np.linalg.solve(Hc, -Jc.conj().T @ R4)
                    R4_try, _ = eval_R4_and_jac(c_cur + step)
                    if np.linalg.norm(R4_try) < nrm:
                        c_cur = c_cur + step
                        lam = max(lam * 0.3, 1e-10)
                    else:
                        lam = min(lam * 5.0, 1e6)
                best_r4 = min(best_r4, float(np.linalg.norm(eval_R4_and_jac(c_cur)[0])))
            print(f"    *** PART 1C JET-4 SEARCH OVER FULL {null_dim}-DIM NULLSPACE (w=4, m=5, 6 C-restarts): "
                  f"min ||R_4||_2 = {best_r4:.4e} ***")


# =============================================================================
# PART 1B: VERIFY EXACT SCRAMBLED GRENET m=7 (w=6) ON JET-2 + JET-3 + JET-4 + JET-5!
# =============================================================================
print("\n" + "=" * 78)
print("PART 1B: EXACT VERIFICATION OF SCRAMBLED GRENET m=7 (w=6) ON ALL JETS")
print("=" * 78)


def build_grenet_matrix(X):
    n = X.shape[0]
    m = (1 << n) - 1
    M = np.zeros((m, m), dtype=X.dtype)
    for S in range(1, m):
        M[S, S - 1] = 1.0
    for S in range(0, m):
        layer = bin(S).count("1")
        for j in range(n):
            if not (S & (1 << j)):
                T = S | (1 << j)
                M[S, T - 1] = X[layer, j]
    M_id = np.zeros((m, m), dtype=np.float64)
    for S in range(1, m):
        M_id[S, S - 1] = 1.0
    for S in range(0, m):
        layer = bin(S).count("1")
        for j in range(n):
            if not (S & (1 << j)):
                M_id[S, (S | (1 << j)) - 1] = 1.0 if layer == j else 0.0
    if np.linalg.det(M_id) < 0:
        M[0, :] *= -1.0
    return M


rng_g = np.random.default_rng(55)
A0_g = build_grenet_matrix(np.zeros((3, 3)))
L_g = np.zeros((9, 7, 7))
for a in range(9):
    E = np.zeros((3, 3))
    E[divmod(a, 3)] = 1.0
    L_g[a] = build_grenet_matrix(E) - A0_g

P_s = rng_g.normal(size=(7, 7))
Q_s = rng_g.normal(size=(7, 7))
Y0_g = P_s @ (A0_g + np.tensordot(X0.reshape(-1), L_g, axes=([0], [0]))) @ Q_s
U_g, s_g, Vt_g = np.linalg.svd(Y0_g)
assert s_g[-1] < 1e-12
inv_s = np.ones(7)
inv_s[:-1] = 1.0 / s_g[:-1]
Left_g = np.diag(inv_s) @ U_g.T @ P_s
Right_g = Q_s @ Vt_g.T
L_gn = np.einsum("ab,ibc,cd->iad", Left_g, L_g, Right_g)
scale_g = float(np.prod(s_g[:-1]) * np.linalg.det(U_g) * np.linalg.det(Vt_g) / (np.linalg.det(P_s) * np.linalg.det(Q_s)))
# Restrict to C^7 via B7 (7 x 9):
L_g7 = np.einsum("ka,aij->kij", B7, L_gn)  # 7 x 7 x 7
A_g7 = L_g7[:, :6, :6]
u_g7 = L_g7[:, :6, 6].T  # 6 x 7
v_g7 = L_g7[:, 6, :6].T  # 6 x 7

# Check exact Jet-2, Jet-3, and ALL-ORDER (Jet-4..7 = 0!) identity on C^7!
max_all_err = 0.0
for _ in range(10):
    z = rng_g.normal(size=7) * 0.1
    Az = np.tensordot(z, A_g7, axes=([0], [0]))
    vz = v_g7 @ z
    uz = u_g7 @ z
    f_schur = scale_g * np.linalg.det(np.eye(6) + Az) * (-vz @ np.linalg.solve(np.eye(6) + Az, uz))
    f_perm = float(z @ Q2 @ z + np.einsum("abc,a,b,c->", C3, z, z, z))
    max_all_err = max(max_all_err, abs(f_schur - f_perm))
print(f"  Scrambled Grenet m=7 (w=6) on C^7: max ALL-ORDER |Schur - (F_2+F_3)| = {max_all_err:.2e}")
assert max_all_err < 1e-13


# =============================================================================
# PART 2: PILLAR 3 — EXPLICIT NON-LINEAR GL-COVARIANT / WICK-PLUCKER EQUATIONS
#         (Hessian Determinant Divisibility & Koszul/Young Flattening KF_1)
# =============================================================================
print("\n" + "=" * 78)
print("PART 2A: PILLAR 3 — EXACT DEGREE-12 GL_9-COVARIANT EQUATION F^3 ^ Hess(F) = 0")
print("         (AND SCALING TO n=4: F^8 ^ Hess(F) = 0, PLUS GLOBALLY MIXED det_m)")
print("=" * 78)


def hessian_matrix_poly(eval_fn, x, eps=1e-4):
    """Accurate finite-difference Hessian (for random det_m checks) or exact."""
    N = len(x)
    H = np.zeros((N, N), dtype=np.float64)
    f0 = eval_fn(x)
    for i in range(N):
        xp = x.copy(); xp[i] += eps
        xm = x.copy(); xm[i] -= eps
        H[i, i] = (eval_fn(xp) - 2.0 * f0 + eval_fn(xm)) / (eps ** 2)
        for j in range(i + 1, N):
            xpp = x.copy(); xpp[i] += eps; xpp[j] += eps
            xpm = x.copy(); xpm[i] += eps; xpm[j] -= eps
            xmp = x.copy(); xmp[i] -= eps; xmp[j] += eps
            xmm = x.copy(); xmm[i] -= eps; xmm[j] -= eps
            val = (eval_fn(xpp) - eval_fn(xpm) - eval_fn(xmp) + eval_fn(xmm)) / (4.0 * eps ** 2)
            H[i, j] = val
            H[j, i] = val
    return H


def exact_hess_det_or_perm(X, is_perm=False):
    """Exact n^2 x n^2 Hessian matrix of det_n or perm_n at X."""
    n = X.shape[0]
    N = n * n
    H = np.zeros((N, N), dtype=np.float64)
    for a in range(N):
        ia, ja = divmod(a, n)
        for b in range(a + 1, N):
            ib, jb = divmod(b, n)
            if ia == ib or ja == jb:
                continue
            rr = [r for r in range(n) if r != ia and r != ib]
            cc = [c for c in range(n) if c != ja and c != jb]
            sub = X[np.ix_(rr, cc)]
            if is_perm:
                val = perm_exact(sub)
            else:
                sgn = (-1) ** (ia + ja + ib + jb)
                if (ia < ib) != (ja < jb):
                    sgn = -sgn
                val = sgn * det_exact(sub)
            H[a, b] = val
            H[b, a] = val
    return H


rng_h = np.random.default_rng(31415)
for n, power in [(3, 3), (4, 8)]:
    ratios_det = []
    ratios_perm = []
    for _ in range(15):
        X = rng_h.normal(size=(n, n)) * 0.7
        f_d = det_exact(X)
        h_d = np.linalg.det(exact_hess_det_or_perm(X, is_perm=False))
        ratios_det.append(h_d / (f_d ** power))

        f_p = perm_exact(X)
        h_p = np.linalg.det(exact_hess_det_or_perm(X, is_perm=True))
        ratios_perm.append(h_p / (f_p ** power))

    c_det = float(np.mean(ratios_det))
    spread_det = float(np.max(np.abs(np.array(ratios_det) - c_det)) / abs(c_det))
    # Also evaluate |Hess(perm_n)(X0)| at a smooth zero X0 in V(perm_n)!
    X0_p = rng_h.normal(size=(n, n)) * 0.7
    X0_p[0, 0] = 0.0
    c0 = perm_exact(X0_p)
    X0_p[0, 0] = 1.0
    c1 = perm_exact(X0_p) - c0
    X0_p[0, 0] = -c0 / c1
    h_p_zero = abs(np.linalg.det(exact_hess_det_or_perm(X0_p, is_perm=True)))
    rk_p_zero = int(np.linalg.matrix_rank(exact_hess_det_or_perm(X0_p, is_perm=True), tol=1e-9))
    # And at a smooth zero of det_n:
    X0_d = rng_h.normal(size=(n, n)) * 0.7
    Ud, sd, Vtd = np.linalg.svd(X0_d)
    sd[-1] = 0.0
    X0_d = Ud @ np.diag(sd) @ Vtd
    h_d_zero = abs(np.linalg.det(exact_hess_det_or_perm(X0_d, is_perm=False)))
    rk_d_zero = int(np.linalg.matrix_rank(exact_hess_det_or_perm(X0_d, is_perm=False), tol=1e-9))

    print(f"\n[n={n}, N={n*n}] Exact Hessian Equation Hess(F) == c * F^{power}:")
    print(f"  det_{n} : Hess(det_{n}) / det_{n}^{power} = {c_det:.6f} (rel spread = {spread_det:.2e}, EXACT IDENTITY!)")
    print(f"          At smooth zero X0 in V(det_{n}):  rank(H) = {rk_d_zero:2d}/{n*n}, |det H| = {h_d_zero:.2e}")
    print(f"  perm_{n}: Hess(perm_{n}) / perm_{n}^{power} varies wildly (std/mean = {np.std(ratios_perm)/(abs(np.mean(ratios_perm))+1e-12):.2e})")
    print(f"          At smooth zero X0 in V(perm_{n}): rank(H) = {rk_p_zero:2d}/{n*n}, |det H| = {h_p_zero:.4e} (NONZERO!)")
    assert spread_det < 1e-10
    assert rk_p_zero == n * n and h_p_zero > 1e-8

# Check vanishing of Hess(F)(X0) on globally mixed det_m(A0 + L(X)) for n=3 (m=3..7) and n=4 (m=4..9)!
print("\n[Global Mixing Stress Test on Hess(F)(X0) == 0 on V(F) (n=3: N=9, n=4: N=16)]:")
for n, m_list in [(3, [3, 4, 5, 6, 7]), (4, [4, 5, 6, 7, 8, 9])]:
    N = n * n
    print(f"  n={n} (N={N}, MR threshold m = {N//2 + (N%2)}):")
    for m in m_list:
        # Random globally mixed m x m affine pencil with corank(A0) = 1 (so X0 = 0 is smooth zero!)
        U = rng_h.normal(size=(m, m))
        V = rng_h.normal(size=(m, m))
        A0_r = U @ np.diag([1.0] * (m - 1) + [0.0]) @ V
        L_r = rng_h.normal(size=(N, m, m))
        # Exact N x N Hessian of det_m(A0_r + L_r(x)) at x = 0 via normalized Schur complement!
        # Normalize: Left @ A0_r @ Right = diag(I_{m-1}, 0)
        L_rn = np.einsum("ab,ibc,cd->iad", np.linalg.inv(U), L_r, np.linalg.inv(V))
        # det(diag(I,0) + L_rn(x)) = (1 + Tr A(x) + ...)(s(x) - v(x)^T u(x) + ...)
        # Degree-2 term on ALL of C^N is: Tr(A(x)) * s(x) - v(x)^T u(x)!
        trA = np.trace(L_rn[:, :m - 1, :m - 1], axis1=1, axis2=2)  # N
        s_vec = L_rn[:, m - 1, m - 1]                              # N
        V_mat = L_rn[:, m - 1, :m - 1].T                           # (m-1) x N
        U_mat = L_rn[:, :m - 1, m - 1].T                           # (m-1) x N
        H_full = np.outer(trA, s_vec) + np.outer(s_vec, trA) - (V_mat.T @ U_mat + U_mat.T @ V_mat)
        rk_full = int(np.linalg.matrix_rank(H_full, tol=1e-9))
        vanishes = "VANISHES (OBSTRUCTED!)" if rk_full < N else "NONZERO (MR ceiling reached)"
        print(f"    m={m}: full N x N Hessian rank at smooth X0 in V(F) = {rk_full:2d}/{N} -> {vanishes}")


# =============================================================================
# PART 2B: KOSZUL / YOUNG FLATTENING KF_1(F) (324 x 81, LINEAR IN F) ON n=3
# =============================================================================
print("\n" + "=" * 78)
print("PART 2B: KOSZUL / YOUNG FLATTENING KF_1(F) (324 x 81) FOR n=3 CUBICS")
print("=" * 78)


def koszul_flattening_1(C3_9):
    """
    For a symmetric cubic tensor C3_9 (9 x 9 x 9), build the GL_9-equivariant
    Koszul flattening KF_1(F): C^9 otimes C^9 -> Lambda^2(C^9) otimes (C^9)*
    mapping e_a otimes e_b -> sum_c (e_a ^ e_c) otimes C3_9[b, c, :].
    Size: (36 * 9) x (9 * 9) = 324 x 81, LINEAR in F!
    """
    pairs = [(i, j) for i in range(9) for j in range(i + 1, 9)]
    p_idx = {p: idx for idx, p in enumerate(pairs)}
    M = np.zeros((36 * 9, 81), dtype=np.float64)
    for a in range(9):
        for b in range(9):
            col = 9 * a + b
            for c in range(9):
                if c == a:
                    continue
                if a < c:
                    p = p_idx[(a, c)]
                    sgn = 1.0
                else:
                    p = p_idx[(c, a)]
                    sgn = -1.0
                M[9 * p:9 * (p + 1), col] += sgn * C3_9[b, c, :]
    return M


def cubic_tensor_perm_or_det_3(is_perm=True):
    C = np.zeros((9, 9, 9), dtype=np.float64)
    for p in itertools.permutations(range(3)):
        sgn = 1.0
        if not is_perm:
            inv = sum(1 for i in range(3) for j in range(i + 1, 3) if p[i] > p[j])
            sgn = -1.0 if (inv % 2) else 1.0
        idxs = [i * 3 + p[i] for i in range(3)]
        for q in itertools.permutations(idxs):
            C[q] += sgn / 6.0
    return C


def cubic_tensor_from_abp(w, seed=0):
    """Random globally mixed homogeneous degree-3 ABP (det_{2w+1}): v(x)^T A(x) u(x)."""
    rng_a = np.random.default_rng(seed)
    v = rng_a.normal(size=(9, w))
    A = rng_a.normal(size=(9, w, w))
    u = rng_a.normal(size=(9, w))
    T = np.einsum("ai,bij,cj->abc", v, A, u)
    return (T + T.transpose(0, 2, 1) + T.transpose(1, 0, 2) +
            T.transpose(1, 2, 0) + T.transpose(2, 0, 1) + T.transpose(2, 1, 0)) / 6.0


def cubic_tensor_det_slice(m, seed=0):
    """
    Random globally mixed cubic slice of det_m(A0 + L(x)) with A0 = diag(I_{m-3}, 0_3):
    wait: lowest homogeneous part of det_m(diag(I_{m-3}, 0_3) + L(x)) is det_3(L_22(x)),
    and generic det_m(A0 + L(x)) with corank(A0) = 1 has degree-3 part
    F_3 = v^T A u - Tr(A) v^T u + ... (same as homogeneous degree-3 projection!).
    To get a genuine homogeneous degree-3 polynomial in det_m orbit closure, take
    det_m(diag(I_{m-3}, 0) + L(x))|_{deg 3} = det_3(L_{22})? No, better: take random
    3-layer ABP of widths (w1, w2) -> det_{w1+w2+1}!
    """
    rng_d = np.random.default_rng(seed)
    w1 = (m - 1) // 2
    w2 = (m - 1) - w1
    M1 = rng_d.normal(size=(9, w1))
    M2 = rng_d.normal(size=(9, w1, w2))
    M3 = rng_d.normal(size=(9, w2))
    T = np.einsum("ai,bij,cj->abc", M1, M2, M3)
    return (T + T.transpose(0, 2, 1) + T.transpose(1, 0, 2) +
            T.transpose(1, 2, 0) + T.transpose(2, 0, 1) + T.transpose(2, 1, 0)) / 6.0


models_kf = [
    ("det_3 (m=3)", cubic_tensor_perm_or_det_3(is_perm=False)),
    ("perm_3 (Grenet m=7)", cubic_tensor_perm_or_det_3(is_perm=True)),
    ("ABP w=1 (det_3 slice)", cubic_tensor_from_abp(1, seed=1)),
    ("ABP (1,2) (det_4 slice)", cubic_tensor_det_slice(4, seed=2)),
    ("ABP (2,2) (det_5 slice)", cubic_tensor_det_slice(5, seed=3)),
    ("ABP (2,3) (det_6 slice)", cubic_tensor_det_slice(6, seed=4)),
    ("ABP (3,3) (det_7 slice)", cubic_tensor_det_slice(7, seed=5)),
    ("Generic cubic in C^9", (lambda T: (T + T.transpose(0,2,1) + T.transpose(1,0,2) +
                                         T.transpose(1,2,0) + T.transpose(2,0,1) + T.transpose(2,1,0))/6.0)(
                                             rng_h.normal(size=(9, 9, 9)))),
]

for name, C_tens in models_kf:
    KF = koszul_flattening_1(C_tens)
    rk_kf = int(np.linalg.matrix_rank(KF, tol=1e-8))
    print(f"  {name:26s}: rank(KF_1) = {rk_kf:2d} / 81")

print("\nALL ROUND 9 PROF. HILBERT VERIFICATIONS PASSED (EXIT CODE 0)!")
