"""Euler-style pure linear algebra obstruction proof for w=5 (m=14) P_perm factorization."""
from __future__ import annotations

import itertools
import time
from typing import Dict, List, Tuple

import numpy as np

from apolar_higher_betti_probe import rank_matrix_mod
from perm4_abp_frontier import MOD
from perm4_middle_factorization_probe import extract_middle_4x4
from poly_exact import Poly, permanent_poly, poly_det


def substitute_b_eq_a(p_mat: List[List[Poly]]) -> List[List[Poly]]:
    """Substitute b_k = a_k (y_{4+k} = y_k) into 4x4 matrix of degree-2 polys in 8 vars."""
    out: List[List[Poly]] = [[{} for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            d: Poly = {}
            for mon, coeff in p_mat[i][j].items():
                m4 = tuple(mon[k] + mon[4 + k] for k in range(4))
                nv = d.get(m4, 0) + coeff
                if nv == 0:
                    d.pop(m4, None)
                else:
                    d[m4] = nv
            out[i][j] = d
    return out


def verify_euler_b_eq_a_identity(p_perm: List[List[Poly]]) -> None:
    """Verify det(P_perm(a, a)) == -48 * a_0^2 * a_1^2 * a_2^2 * a_3^2 over Z."""
    p_diag = substitute_b_eq_a(p_perm)
    det_diag = poly_det(p_diag, 4)
    expected: Poly = {(2, 2, 2, 2): -48}
    assert det_diag == expected, f"Expected {expected}, got {det_diag}"
    # Also verify double symmetry P_perm(a, b) == P_perm(b, a) == P_perm(a, b)^T
    for i in range(4):
        for j in range(4):
            assert p_perm[i][j] == p_perm[j][i], f"Entry symmetry failed at ({i},{j})"
            swapped = {mon[4:8] + mon[0:4]: c for mon, c in p_perm[i][j].items()}
            assert swapped == p_perm[i][j], f"a<->b symmetry failed at ({i},{j})"
    print("[PASS] Euler b=a identity: det(P_perm(a, a)) == -48 * a_0^2 a_1^2 a_2^2 a_3^2 (exact over Z)")


def build_nisan_and_sym0(p_perm: List[List[Poly]], mod: int = MOD) -> Tuple[np.ndarray, np.ndarray]:
    """Build 16x16 Nisan matrix M = N_{01}(P_perm) and 16x6 basis S0 of Sym_0(4)."""
    m_mat = np.zeros((16, 16), dtype=np.int64)
    for j0 in range(4):
        for j3 in range(4):
            comp = p_perm[j0][j3]
            for mon, c in comp.items():
                a_idx = [k for k in range(4) if mon[k] == 1]
                b_idx = [k for k in range(4) if mon[4 + k] == 1]
                assert len(a_idx) == 1 and len(b_idx) == 1 and sum(mon) == 2
                c1, c2 = a_idx[0], b_idx[0]
                m_mat[j0 * 4 + c1, j3 * 4 + c2] = (m_mat[j0 * 4 + c1, j3 * 4 + c2] + c) % mod

    # Check combinatorial complement definition
    for j0 in range(4):
        for c1 in range(4):
            for j3 in range(4):
                for c2 in range(4):
                    expected = 1 if len({j0, c1, j3, c2}) == 4 else 0
                    assert m_mat[j0 * 4 + c1, j3 * 4 + c2] == expected

    # Build explicit 16x6 basis of Sym_0(4)
    cols: List[np.ndarray] = []
    for i in range(4):
        for j in range(i + 1, 4):
            e = np.zeros((4, 4), dtype=np.int64)
            e[i, j] = 1
            e[j, i] = 1
            cols.append(e.reshape(16))
    s0 = np.stack(cols, axis=1) % mod

    assert rank_matrix_mod(m_mat, mod) == 6
    assert rank_matrix_mod(s0, mod) == 6
    assert rank_matrix_mod(np.hstack([s0, m_mat]) % mod, mod) == 6
    # On Sym_0(4), M^2 == I_6 (involution permuting complementary unordered pairs)
    ms0 = (m_mat @ s0) % mod
    assert rank_matrix_mod(ms0, mod) == 6
    print("[PASS] Nisan matrix M = N_{01}(P_perm): rank(M) == 6, colsp(M) == Sym_0(4)")
    return m_mat, s0


def subspace_intersect_dim(u_cols: np.ndarray, v_cols: np.ndarray, mod: int = MOD) -> int:
    """Compute dim(colsp(U) cap colsp(V)) over F_mod via Zassenhaus rank identity."""
    ru = rank_matrix_mod(u_cols, mod)
    rv = rank_matrix_mod(v_cols, mod)
    ruv = rank_matrix_mod(np.hstack([u_cols, v_cols]) % mod, mod)
    return ru + rv - ruv


def random_subspace_basis(d: int, rng: np.random.Generator, mod: int = MOD) -> np.ndarray:
    """Generate a full-rank (d, 4) matrix over F_mod."""
    while True:
        w = rng.integers(0, mod, size=(d, 4), dtype=np.int64)
        if rank_matrix_mod(w, mod) == d:
            return w


def verify_lemma_a(s0: np.ndarray, rng: np.random.Generator, mod: int = MOD) -> None:
    """Verify dim(Sym_0(4) cap (W otimes W)) <= binom(d, 2) over F_mod."""
    max_by_d: Dict[int, int] = {1: 0, 2: 0, 3: 0, 4: 0}
    total_checked = 0

    def test_w(w_rows: np.ndarray, d: int) -> None:
        nonlocal total_checked
        assert rank_matrix_mod(w_rows, mod) == d
        # W otimes W spanned by all w_i otimes w_j
        ww_cols = np.stack(
            [np.kron(w_rows[i], w_rows[j]) % mod for i in range(d) for j in range(d)],
            axis=1,
        )
        dim_inter = subspace_intersect_dim(s0, ww_cols, mod)
        bound = d * (d - 1) // 2
        assert dim_inter <= bound, f"Lemma A failed for d={d}: got {dim_inter} > {bound}"
        if dim_inter > max_by_d[d]:
            max_by_d[d] = dim_inter
        total_checked += 1

    # All 15 coordinate subspaces
    for d in (1, 2, 3, 4):
        for subset in itertools.combinations(range(4), d):
            w_coord = np.zeros((d, 4), dtype=np.int64)
            for r, idx in enumerate(subset):
                w_coord[r, idx] = 1
            test_w(w_coord, d)

    # 30 random d-dimensional subspaces per d
    for d in (1, 2, 3, 4):
        for _ in range(30):
            w_rand = random_subspace_basis(d, rng, mod)
            test_w(w_rand, d)

    summary = ", ".join(f"d={d}: max={max_by_d[d]}<={d*(d-1)//2}" for d in (1, 2, 3, 4))
    print(f"[PASS] Lemma A ({total_checked} subspaces): {summary}")


def kernel_left_basis(beta: np.ndarray, mod: int = MOD) -> np.ndarray:
    """Given nonzero 4-vector beta over F_mod, return 3x4 full-rank Gamma with Gamma @ beta == 0."""
    piv = next(i for i in range(4) if beta[i] % mod != 0)
    inv_piv = pow(int(beta[piv] % mod), mod - 2, mod)
    rows: List[np.ndarray] = []
    for j in range(4):
        if j == piv:
            continue
        row = np.zeros(4, dtype=np.int64)
        row[j] = 1
        row[piv] = (-int(beta[j]) * inv_piv) % mod
        rows.append(row)
    gamma = np.stack(rows, axis=0) % mod
    assert np.all((gamma @ beta) % mod == 0)
    assert rank_matrix_mod(gamma, mod) == 3
    return gamma


def verify_lemma_c(m_mat: np.ndarray, rng: np.random.Generator, mod: int = MOD) -> None:
    """Verify rank((Gamma otimes I_4) M) == 6 (and symmetric (I_4 otimes Gamma) M) for all beta != 0."""
    betas: List[np.ndarray] = [
        np.array([1, 0, 0, 0], dtype=np.int64),
        np.array([1, 1, 0, 0], dtype=np.int64),
        np.array([1, 1, 1, 0], dtype=np.int64),
        np.array([1, 1, 1, 1], dtype=np.int64),
    ]
    for _ in range(30):
        while True:
            b = rng.integers(0, mod, size=4, dtype=np.int64)
            if np.any(b != 0):
                betas.append(b)
                break

    eye4 = np.eye(4, dtype=np.int64)
    for beta in betas:
        gamma = kernel_left_basis(beta, mod)
        op_left = np.kron(gamma, eye4) % mod
        # Sanity check: op_left annihilates beta otimes I_4
        assert np.all((op_left @ np.kron(beta.reshape(4, 1), eye4)) % mod == 0)
        rk_left = rank_matrix_mod((op_left @ m_mat) % mod, mod)
        assert rk_left == 6, f"Lemma C left failed for beta={beta}: rank={rk_left}"

        op_fast = np.kron(eye4, gamma) % mod
        rk_fast = rank_matrix_mod((op_fast @ m_mat) % mod, mod)
        assert rk_fast == 6, f"Lemma C fast failed for beta={beta}: rank={rk_fast}"

    print(f"[PASS] Lemma C ({len(betas)} nonzero beta vectors, both tensor factors): min rank == 6")


def kron_swap_mod(b_mat: np.ndarray, v_mat: np.ndarray, mod: int = MOD) -> np.ndarray:
    """Return 16x16 K[(j0, c1), (j3, c2)] = B[j0, c2] * V[j3, c1] mod `mod`."""
    return (np.einsum("ac,db->abdc", b_mat, v_mat) % mod).reshape(16, 16)


def random_rank_matrix(r: int, rng: np.random.Generator, mod: int = MOD) -> np.ndarray:
    """Return a random 4x4 matrix over F_mod of exact rank r."""
    while True:
        u = rng.integers(0, mod, size=(4, r), dtype=np.int64)
        w = rng.integers(0, mod, size=(r, 4), dtype=np.int64)
        mat = (u @ w) % mod
        if rank_matrix_mod(mat, mod) == r:
            return mat


def verify_lemma_b(m_mat: np.ndarray, rng: np.random.Generator, mod: int = MOD) -> None:
    """Verify rank(M - K(B, V)) >= 5 across all (r_B, r_V) in {1,2,3,4}^2 over F_mod."""
    # Exact indexing self-check
    b_chk = rng.integers(0, mod, size=(4, 4), dtype=np.int64)
    v_chk = rng.integers(0, mod, size=(4, 4), dtype=np.int64)
    k_chk = kron_swap_mod(b_chk, v_chk, mod)
    for j0 in range(4):
        for c1 in range(4):
            for j3 in range(4):
                for c2 in range(4):
                    assert k_chk[j0 * 4 + c1, j3 * 4 + c2] == (b_chk[j0, c2] * v_chk[j3, c1]) % mod

    # Pre-build adversarial structured rank-r matrices (coordinate subsets + rotations)
    adversarial_by_rank: Dict[int, List[np.ndarray]] = {1: [], 2: [], 3: [], 4: []}
    # 1. All coordinate diagonal projections
    for r in (1, 2, 3, 4):
        for subset in itertools.combinations(range(4), r):
            d = np.zeros((4, 4), dtype=np.int64)
            for idx in subset:
                d[idx, idx] = 1
            adversarial_by_rank[r].append(d)
    # 2. Row/col permuted basis blocks for r=2, 3 (including the exact W_L != W_R block!)
    perms = list(itertools.permutations(range(4)))
    for r in (1, 2, 3):
        for p_idx in range(0, len(perms), 4):
            perm = perms[p_idx]
            mat = np.zeros((4, 4), dtype=np.int64)
            for k in range(r):
                mat[k, perm[k]] = 1
            adversarial_by_rank[r].append(mat)
    # 3. Specific rank-3 twisted blocks: B supported on rows {1,2,3}, cols {0,2,3}; same for V
    b_tw = np.zeros((4, 4), dtype=np.int64)
    for i, r_i in enumerate((1, 2, 3)):
        c_i = (0, 2, 3)[i]
        b_tw[r_i, c_i] = 1
    b_tw[1, 3] = 1
    b_tw[2, 2] = 1
    adversarial_by_rank[3].append(b_tw)
    b_anti = np.zeros((4, 4), dtype=np.int64)
    b_anti[1, 2] = 1
    b_anti[2, 0] = 1
    b_anti[3, 3] = 1
    b_anti[1, 3] = 1
    b_anti[2, 2] = 1
    adversarial_by_rank[3].append(b_anti % mod)

    min_rank_table: Dict[Tuple[int, int], int] = {}
    total_pairs = 0
    for rb in range(1, 5):
        for rv in range(1, 5):
            min_rk = 16
            # 20 random pairs
            for _ in range(20):
                b_mat = random_rank_matrix(rb, rng, mod)
                v_mat = random_rank_matrix(rv, rng, mod)
                k_mat = kron_swap_mod(b_mat, v_mat, mod)
                rk = rank_matrix_mod((m_mat - k_mat) % mod, mod)
                assert rk >= 5, f"Lemma B violated at random ({rb},{rv}): rk={rk}"
                if rk < min_rk:
                    min_rk = rk
                total_pairs += 1
            # Adversarial structured pairs (product of coordinate/twisted lists)
            for b_adv in adversarial_by_rank[rb]:
                assert rank_matrix_mod(b_adv, mod) == rb
                for v_adv in adversarial_by_rank[rv]:
                    assert rank_matrix_mod(v_adv, mod) == rv
                    k_mat = kron_swap_mod(b_adv, v_adv, mod)
                    rk = rank_matrix_mod((m_mat - k_mat) % mod, mod)
                    assert rk >= 5, (
                        f"Lemma B violated at adversarial ({rb},{rv}): rk={rk}\nB=\n{b_adv}\nV=\n{v_adv}"
                    )
                    if rk < min_rk:
                        min_rk = rk
                    total_pairs += 1
            min_rank_table[(rb, rv)] = min_rk

    print(f"[PASS] Lemma B ({total_pairs} random + adversarial pairs): ALL rank(M - K) >= 5")
    header = "  r_B \\ r_V | " + "  ".join(f" {rv} " for rv in range(1, 5))
    print(header)
    print("  " + "-" * (len(header) - 2))
    for rb in range(1, 5):
        row_str = "  ".join(f" {min_rank_table[(rb, rv)]:2d}" for rv in range(1, 5))
        print(f"      {rb}     | {row_str}")


# ---- Complex Levenberg-Marquardt infrastructure for Case (3, 2) ----

def run_complex_lm(
    residual_and_jac,
    n_complex_vars: int,
    n_complex_eqs: int,
    rng: np.random.Generator,
    n_starts: int = 10,
    max_iters: int = 250,
    scale: float = 0.6,
) -> Tuple[List[float], np.ndarray]:
    """Damped LM minimizing ||r(z)||_2 over C^{n_complex_vars} via real isomorphism."""
    best_x: np.ndarray | None = None
    best_norm = float("inf")
    finals: List[float] = []

    # Verify analytical Jacobian on start 0
    z_chk = scale * (rng.standard_normal(n_complex_vars) + 1j * rng.standard_normal(n_complex_vars))
    r0, j0 = residual_and_jac(z_chk)
    eps = 1e-6
    j_fd = np.zeros_like(j0)
    idx_chk = rng.choice(2 * n_complex_vars, size=min(12, 2 * n_complex_vars), replace=False)
    for idx in idx_chk:
        dz = np.zeros(2 * n_complex_vars)
        dz[idx] = eps
        dc = dz[:n_complex_vars] + 1j * dz[n_complex_vars:]
        rp, _ = residual_and_jac(z_chk + dc)
        rm, _ = residual_and_jac(z_chk - dc)
        j_fd[:, idx] = (rp - rm) / (2.0 * eps)
    fd_err = float(np.max(np.abs(j0[:, idx_chk] - j_fd[:, idx_chk])))
    assert fd_err < 1e-7, f"Analytical Jacobian mismatch: max err={fd_err:.3e}"

    for _ in range(n_starts):
        z = scale * (rng.standard_normal(n_complex_vars) + 1j * rng.standard_normal(n_complex_vars))
        r, jac = residual_and_jac(z)
        cur_norm = float(np.linalg.norm(r))
        lam = 1e-3
        for _it in range(max_iters):
            if cur_norm < 1e-13:
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
                    step_rel = cur_norm - new_norm
                    z, r, jac, cur_norm = z_new, r_new, j_new, new_norm
                    lam = max(lam * 0.3, 1e-12)
                    accepted = True
                    if step_rel < 1e-14 and cur_norm > 1e-8:
                        # plateau detected early after sufficient drop? Let LM keep squeezing unless stalled
                        pass
                    break
                lam = min(lam * 5.0, 1e8)
            if not accepted and lam >= 1e7:
                break
        finals.append(cur_norm)
        if cur_norm < best_norm:
            best_norm = cur_norm
            best_x = z
    assert best_x is not None
    return finals, best_x


def unpack_real_jac(jc: np.ndarray) -> np.ndarray:
    """Convert complex Jacobian dF/dz (plus linear wrt Re/Im, where F is holomorphic) to real 2m x 2n."""
    # For holomorphic F(z) where z = x + i y: dF/dx = J_c, dF/dy = i * J_c.
    jr = jc.real
    ji = jc.imag
    top = np.hstack([jr, -ji])
    bot = np.hstack([ji, jr])
    return np.vstack([top, bot])


def probe_two_kronecker_w32(m_mat: np.ndarray, rng: np.random.Generator, mod: int = MOD) -> float:
    """
    Test 4a:
      (i) Aligned coordinate 2-Kronecker pairs K_1 + K_2 over F_mod: verify min rank(M - K_1 - K_2).
      (ii) 10 random complex LM starts minimizing ||K_1 + K_2 + U_{16x3} W_{3x16} - M||_F.
    """
    # Part (i): exhaustive structured 2-Kronecker rank-1/2 coordinate pairs over F_mod
    coord_r1 = []
    for i in range(4):
        for j in range(4):
            e = np.zeros((4, 4), dtype=np.int64)
            e[i, j] = 1
            coord_r1.append(e)
    # Try removing two coordinate rank-1 Kronecker terms trying to cancel 2 entries of M
    min_rk_r1_pair = 16
    for i1, b1 in enumerate(coord_r1):
        for v1 in coord_r1:
            k1 = kron_swap_mod(b1, v1, mod)
            for b2 in coord_r1[i1:]:
                for v2 in coord_r1:
                    k2 = kron_swap_mod(b2, v2, mod)
                    rk = rank_matrix_mod((m_mat - k1 - k2) % mod, mod)
                    if rk < min_rk_r1_pair:
                        min_rk_r1_pair = rk
                        if min_rk_r1_pair <= 3:
                            break
                if min_rk_r1_pair <= 3:
                    break
            if min_rk_r1_pair <= 3:
                break
        if min_rk_r1_pair <= 3:
            break
    print(f"  Test 4a (F_mod aligned rank-1+1 pair): min rank(M - K1 - K2) = {min_rk_r1_pair}")

    # Test 500 random full-rank / mixed-rank pairs (K1, K2) over F_mod
    min_rk_rand = 16
    for _ in range(500):
        r1 = int(rng.integers(1, 5))
        r2 = int(rng.integers(1, 5))
        k1 = kron_swap_mod(random_rank_matrix(r1, rng, mod), random_rank_matrix(r2, rng, mod), mod)
        r3 = int(rng.integers(1, 5))
        r4 = int(rng.integers(1, 5))
        k2 = kron_swap_mod(random_rank_matrix(r3, rng, mod), random_rank_matrix(r4, rng, mod), mod)
        rk = rank_matrix_mod((m_mat - k1 - k2) % mod, mod)
        if rk < min_rk_rand:
            min_rk_rand = rk
    print(f"  Test 4a (F_mod 500 random K1+K2 pairs): min rank(M - K1 - K2) = {min_rk_rand}")

    # Part (ii): Complex LM on K_1(B1,V1) + K_2(B2,V2) + U_{16x3} W_{3x16} = M
    m_c = m_mat.astype(np.complex128)
    n_vars = 16 + 16 + 16 + 16 + 48 + 48  # 160

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
        # F[(j0,c1),(j3,c2)] += B[j0,c2] * V[j3,c1]
        # jc_4d has axes (j0, c1, j3, c2, var) -> jc_4d[a, :, :, c] has axes (c1, j3) == V^T
        jc_4d = jc.reshape(4, 4, 4, 4, n_vars)
        for a in range(4):
            for c in range(4):
                jc_4d[a, :, :, c, a * 4 + c] += v1.T
                jc_4d[a, :, :, c, 32 + a * 4 + c] += v2.T
        # V1: col offset 16 + d*4 + b (axes in jc_4d[:, b, d, :] are (j0, c2) == b1)
        for d in range(4):
            for b in range(4):
                jc_4d[:, b, d, :, 16 + d * 4 + b] += b1
                jc_4d[:, b, d, :, 48 + d * 4 + b] += b2

        # U3 @ W3: U3 is (16, 3) at offset 64 + row*3 + k
        jc_mat = jc.reshape(16, 16, n_vars)
        for row in range(16):
            for k in range(3):
                jc_mat[row, :, 64 + row * 3 + k] += w3[k, :]
        # W3 is (3, 16) at offset 112 + k*16 + col
        for k in range(3):
            for col in range(16):
                jc_mat[:, col, 112 + k * 16 + col] += u3[:, k]

        r_real = np.concatenate([f.real, f.imag])
        j_real = unpack_real_jac(jc)
        return r_real, j_real

    finals, best_z = run_complex_lm(res_jac, n_vars, 256, rng, n_starts=10, max_iters=250)
    b1 = best_z[0:16].reshape(4, 4)
    v1 = best_z[16:32].reshape(4, 4)
    b2 = best_z[32:48].reshape(4, 4)
    v2 = best_z[48:64].reshape(4, 4)
    rem = m_c - np.einsum("ac,db->abdc", b1, v1).reshape(16, 16) - np.einsum("ac,db->abdc", b2, v2).reshape(16, 16)
    svals = np.linalg.svd(rem, compute_uv=False)
    tail_norm = float(np.linalg.norm(svals[3:]))
    min_res = min(finals)
    med_res = float(np.median(finals))
    print(
        f"  Test 4a (Complex LM, 10 starts, 256 eqs / 160 vars): "
        f"min={min_res:.6f}, median={med_res:.6f}, best tail_svals[3:]={tail_norm:.6f}, sigma_3={svals[3]:.6f}"
    )
    return min_res


def probe_exact_bidegree_32(m_mat: np.ndarray, rng: np.random.Generator) -> float:
    """
    Test 4b: 10 random complex LM starts on
      A_1(a)_{4x3} B_2(b)_{3x4} + B_1(b)_{4x2} A_2(a)_{2x4} = P_perm(a, b)
    (256 bilinear equations in 160 complex variables).
    """
    m_c = m_mat.astype(np.complex128)
    # A1: (j0, c1, k) shape (4, 4, 3) -> 48 vars [0:48]
    # B2: (j3, c2, k) shape (4, 4, 3) -> 48 vars [48:96]
    # B1: (j0, c2, k) shape (4, 4, 2) -> 32 vars [96:128]
    # A2: (j3, c1, k) shape (4, 4, 2) -> 32 vars [128:160]
    n_vars = 160

    def res_jac(z: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        a1 = z[0:48].reshape(4, 4, 3)
        b2 = z[48:96].reshape(4, 4, 3)
        b1 = z[96:128].reshape(4, 4, 2)
        a2 = z[128:160].reshape(4, 4, 2)

        t1 = np.einsum("abk,dck->abdc", a1, b2)
        t2 = np.einsum("ack,dbk->abdc", b1, a2)
        f = ((t1 + t2).reshape(16, 16) - m_c).reshape(256)

        jc = np.zeros((256, n_vars), dtype=np.complex128)
        jc_4d = jc.reshape(4, 4, 4, 4, n_vars)
        # d/dA1[a,b,k]: contributes B2[d,c,k] at (a,b,d,c)
        for a in range(4):
            for b in range(4):
                for k in range(3):
                    jc_4d[a, b, :, :, (a * 4 + b) * 3 + k] += b2[:, :, k]
        # d/dB2[d,c,k]: contributes A1[a,b,k] at (a,b,d,c)
        for d in range(4):
            for c in range(4):
                for k in range(3):
                    jc_4d[:, :, d, c, 48 + (d * 4 + c) * 3 + k] += a1[:, :, k]
        # d/dB1[a,c,k]: contributes A2[d,b,k] at (a,b,d,c), so transpose of A2[:,:,k] over (b,d)
        for a in range(4):
            for c in range(4):
                for k in range(2):
                    jc_4d[a, :, :, c, 96 + (a * 4 + c) * 2 + k] += a2[:, :, k].T
        # d/dA2[d,b,k]: contributes B1[a,c,k] at (a,b,d,c)
        for d in range(4):
            for b in range(4):
                for k in range(2):
                    jc_4d[:, b, d, :, 128 + (d * 4 + b) * 2 + k] += b1[:, :, k]

        r_real = np.concatenate([f.real, f.imag])
        j_real = unpack_real_jac(jc)
        return r_real, j_real

    finals, _ = run_complex_lm(res_jac, n_vars, 256, rng, n_starts=10, max_iters=250)
    min_res = min(finals)
    med_res = float(np.median(finals))
    max_res = max(finals)
    solved = sum(1 for v in finals if v < 1e-8)
    print(
        f"  Test 4b (Exact bidegree (3,2) LM, 10 starts, 256 eqs / 160 vars): "
        f"solved={solved}/10, min={min_res:.6f}, median={med_res:.6f}, max={max_res:.6f}"
    )
    return min_res


def main() -> None:
    t0 = time.time()
    rng = np.random.default_rng(20261121)

    f_perm = permanent_poly(4)
    p_perm = extract_middle_4x4(f_perm)

    verify_euler_b_eq_a_identity(p_perm)
    m_mat, s0 = build_nisan_and_sym0(p_perm, MOD)
    verify_lemma_a(s0, rng, MOD)
    verify_lemma_c(m_mat, rng, MOD)
    verify_lemma_b(m_mat, rng, MOD)

    print("\n--- Case (3, 2) Obstruction Probes ---")
    min_4a = probe_two_kronecker_w32(m_mat, rng, MOD)
    min_4b = probe_exact_bidegree_32(m_mat, rng)
    assert min_4a > 1e-8 and min_4b > 1e-8, (
        f"Unexpected small residual in Case (3,2): Test4a={min_4a:.3e}, Test4b={min_4b:.3e}"
    )
    print(f"\n[DONE] All Euler w=5 checks passed in {time.time() - t0:.2f}s.")


if __name__ == "__main__":
    main()
