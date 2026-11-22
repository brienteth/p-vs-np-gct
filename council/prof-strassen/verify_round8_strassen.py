"""
Prof. Strassen Round 8 (Quantum Tensor Networks, MPS/PEPS, & Global Mixing Stress Tests) Verification Suite:
1. [QUANTITATIVE EXPERIMENT] Bipartite Entanglement Spectra & Variable-Cut MPS Bond Dimensions:
   - Symmetric cuts F_{1,2} (n=3) and F_{2,2} (n=4) give IDENTICAL flat spectra for det_n and perm_n
     (n=3: rank 9, sv=1/3, S_vN=S_2=log2(9); n=4: rank 36, sv=1/6, S_vN=S_2=log2(36), nuc=6.0).
   - Variable-bipartition MPS cuts at n=4 (row, 2x2, checkerboard, upper-tri) give IDENTICAL Schmidt ranks
     (6, 4, 18, 6, 14) and entropies; under GL_9 global mixing at n=3, both inflate 5 -> 11.
2. [QUANTITATIVE EXPERIMENT] Global Mixing Invariance Test of Algebraic/Quantum Candidates:
   - Shifted Partial Derivatives SPD(k, l), Koszul-Young YF_{1,1}(d^3 F), and Mignon-Ressayre Hessian rank
     on det_n, perm_n, and globally-mixed width-w ABPs (det_{3w+1}):
     At n=4, ABP w=3 (m=10) ALREADY achieves SPD(1,1)=256/256 > 250 (perm_4), SPD(2,1)=672/816 > 512 (perm_4),
     and YF_{1,1}=255/256; ABP w=4 (m=13) saturates 816/816 and Hess_rk=16/16.
3. [PROVEN / QUANTITATIVE EXPERIMENT] Fermionic Gaussian Bath / Schur Complement Decomposition:
   - Grenet m=7 exact realization of perm_3 (rank A_0 = 6, nilpotent L_{11} bath max|eig|=0, rank=6 at singular zeros)
     and explicit non-nilpotent-bath homogeneous example M = [[x1, x1], [x2, 1+x2]].
"""
from __future__ import annotations

import itertools
import math

import numpy as np


def verify_symmetric_and_variable_cut_mps() -> None:
    """Verify identical bipartite entanglement spectra and variable-cut MPS bond dims for det_n and perm_n."""
    # 1. n=3 symmetric F_{1,2} (9 x 45)
    N3 = 9
    M2_3 = list(itertools.combinations_with_replacement(range(N3), 2))
    M3_3 = list(itertools.combinations_with_replacement(range(N3), 3))
    idx2_3 = {m: i for i, m in enumerate(M2_3)}
    idx3_3 = {m: i for i, m in enumerate(M3_3)}

    def flat_1_2(sign_mode: int) -> np.ndarray:
        pv = np.zeros(len(M3_3), dtype=float)
        for p in itertools.permutations(range(3)):
            inv = sum(1 for i in range(3) for j in range(i + 1, 3) if p[i] > p[j])
            sgn = -1.0 if (inv % 2 and sign_mode == -1) else 1.0
            m = tuple(sorted([0 * 3 + p[0], 1 * 3 + p[1], 2 * 3 + p[2]]))
            pv[idx3_3[m]] += sgn
        mat = np.zeros((N3, len(M2_3)), dtype=float)
        for m_idx, m in enumerate(M3_3):
            c = pv[m_idx]
            if c == 0:
                continue
            mult_3 = 6 // math.prod(math.factorial(m.count(u)) for u in set(m))
            for pos in set(m):
                rem = list(m)
                rem.remove(pos)
                rem_t = tuple(rem)
                mult_2 = 2 // math.prod(math.factorial(rem_t.count(u)) for u in set(rem_t))
                mat[pos, idx2_3[rem_t]] = (c / mult_3) * math.sqrt(mult_2)
        return mat

    for sm in (-1, 1):
        sv = np.linalg.svd(flat_1_2(sm), compute_uv=False)
        sv = sv[sv > 1e-12]
        assert len(sv) == 9 and np.allclose(sv, 1.0 / 3.0)

    # 2. n=4 symmetric F_{2,2} (136 x 136)
    N4 = 16
    M2_4 = list(itertools.combinations_with_replacement(range(N4), 2))
    idx2_4 = {m: i for i, m in enumerate(M2_4)}

    def flat_2_2(sign_mode: int) -> np.ndarray:
        mat = np.zeros((len(M2_4), len(M2_4)), dtype=float)
        for p in itertools.permutations(range(4)):
            inv = sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j])
            sgn = -1.0 if (inv % 2 and sign_mode == -1) else 1.0
            vars4 = [0 * 4 + p[0], 1 * 4 + p[1], 2 * 4 + p[2], 3 * 4 + p[3]]
            for a1, a2 in itertools.combinations(vars4, 2):
                A = tuple(sorted((a1, a2)))
                B = tuple(sorted(v for v in vars4 if v not in A))
                mat[idx2_4[A], idx2_4[B]] += sgn / 12.0
        return mat

    for sm in (-1, 1):
        sv = np.linalg.svd(flat_2_2(sm), compute_uv=False)
        sv = sv[sv > 1e-12]
        assert len(sv) == 36 and np.allclose(sv, 1.0 / 6.0)

    # 3. n=4 variable-bipartition MPS cuts
    cuts_n4 = [
        ("Rows {0,1}|{2,3}", list(range(8)), 6),
        ("Row {0}|{1,2,3}", list(range(4)), 4),
        ("Checkerboard 8|8", [0, 2, 5, 7, 8, 10, 13, 15], 18),
        ("2x2 Subblock 4|12", [0, 1, 4, 5], 6),
        ("Upper-Tri 10|6", [0, 1, 2, 3, 5, 6, 7, 10, 11, 15], 14),
    ]
    for _, L_vars, exp_rk in cuts_n4:
        L_set = set(L_vars)
        spectra = []
        for sm in (-1, 1):
            rmap, cmap, ents = {}, {}, []
            for p in itertools.permutations(range(4)):
                inv = sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j])
                sgn = -1.0 if (inv % 2 and sm == -1) else 1.0
                v = [0 * 4 + p[0], 1 * 4 + p[1], 2 * 4 + p[2], 3 * 4 + p[3]]
                mL = tuple(sorted(x for x in v if x in L_set))
                mR = tuple(sorted(x for x in v if x not in L_set))
                if mL not in rmap:
                    rmap[mL] = len(rmap)
                if mR not in cmap:
                    cmap[mR] = len(cmap)
                ents.append((rmap[mL], cmap[mR], sgn))
            mat = np.zeros((len(rmap), len(cmap)), dtype=float)
            for r, c, s in ents:
                mat[r, c] += s
            sv = np.linalg.svd(mat, compute_uv=False)
            sv = sv[sv > 1e-10]
            assert len(sv) == exp_rk
            spectra.append(sv)
        assert np.allclose(spectra[0], spectra[1])

    # 4. GL_9 global mixing inflates n=3 variable-cut rank 5 -> 11 for both det_3 and perm_3
    rng = np.random.default_rng(7)
    G3 = rng.standard_normal((9, 9))
    M_L = [(d, m) for d in range(4) for m in itertools.combinations_with_replacement(range(4), d)]
    M_R = [(d, m) for d in range(4) for m in itertools.combinations_with_replacement(range(4, 9), d)]
    iL = {m[1]: i for i, m in enumerate(M_L)}
    iR = {m[1]: i for i, m in enumerate(M_R)}
    for sm in (-1, 1):
        for G_mat, exp_rk in [(np.eye(9), 5), (G3, 11)]:
            mat = np.zeros((len(M_L), len(M_R)), dtype=float)
            for p in itertools.permutations(range(3)):
                inv = sum(1 for i in range(3) for j in range(i + 1, 3) if p[i] > p[j])
                sgn = -1.0 if (inv % 2 and sm == -1) else 1.0
                g0, g1, g2 = G_mat[p[0]], G_mat[3 + p[1]], G_mat[6 + p[2]]
                for a in range(9):
                    for b in range(9):
                        for c in range(9):
                            coef = sgn * g0[a] * g1[b] * g2[c]
                            if abs(coef) < 1e-14:
                                continue
                            mL = tuple(sorted(v for v in (a, b, c) if v < 4))
                            mR = tuple(sorted(v for v in (a, b, c) if v >= 4))
                            mat[iL[mL], iR[mR]] += coef
            rk = int(np.sum(np.linalg.svd(mat, compute_uv=False) > 1e-10))
            assert rk == exp_rk

    print("[PASS] 1. Symmetric F_{1,2}/F_{2,2} entanglement spectra & variable-cut MPS bond dims identical for det_n & perm_n.")


def verify_global_mixing_stress_test_n4() -> None:
    """
    Verify n=4 (N=16) Global Mixing Stress Test of SPD(1,1), SPD(2,1), Koszul-Young YF_{1,1}(d^3 F),
    and Mignon-Ressayre Hessian rank across det_4, perm_4, and globally-mixed ABPs (det_{3w+1}).
    """
    N4 = 16
    M2_4 = list(itertools.combinations_with_replacement(range(N4), 2))
    M3_4 = list(itertools.combinations_with_replacement(range(N4), 3))
    M4_4 = list(itertools.combinations_with_replacement(range(N4), 4))
    idx2_4 = {m: i for i, m in enumerate(M2_4)}
    idx3_4 = {m: i for i, m in enumerate(M3_4)}
    idx4_4 = {m: i for i, m in enumerate(M4_4)}
    rng = np.random.default_rng(42)

    def tens4_perm_det(sign_mode: int) -> np.ndarray:
        C = np.zeros((16, 16, 16, 16), dtype=float)
        for p in itertools.permutations(range(4)):
            inv = sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j])
            sgn = -1.0 if (inv % 2 and sign_mode == -1) else 1.0
            v = [0 * 4 + p[0], 1 * 4 + p[1], 2 * 4 + p[2], 3 * 4 + p[3]]
            for perm in itertools.permutations(v):
                C[perm[0], perm[1], perm[2], perm[3]] += sgn
        return C

    def tens4_abp(w: int) -> np.ndarray:
        W1 = rng.standard_normal((1, w, N4))
        W2 = rng.standard_normal((w, w, N4))
        W3 = rng.standard_normal((w, w, N4))
        W4 = rng.standard_normal((w, 1, N4))
        C0 = np.einsum("ia,ijb,jkc,kd->abcd", W1[0], W2, W3, W4[:, 0, :])
        C = np.zeros_like(C0)
        for perm in itertools.permutations(range(4)):
            C += np.transpose(C0, perm)
        return C

    def tens_to_poly_dict(C: np.ndarray) -> dict[tuple[int, ...], float]:
        # C is fully symmetric 16^4 tensor; poly coeff of x_m is C[m] / prod(k_i!) * 24?
        # Wait: sum_{a,b,c,d} C[a,b,c,d] x_a x_b x_c x_d -> coeff of m is C[m] * (24 / prod(cnt!)) / 24?
        # Actually C[m] summed over ordered tuples is C[m] * (24 / prod(cnt!))? Let's divide by 24:
        # In tens4_perm_det, we summed over 24 perms, so C[m] == 24 * poly_coeff(m) for multilinear, and in general:
        # Wait: F(x) = (1/24) sum C[a,b,c,d] x_a x_b x_c x_d = sum_m C[m] / prod(cnt!) x_m!
        d = {}
        for m in M4_4:
            val = C[m[0], m[1], m[2], m[3]]
            if abs(val) > 1e-12:
                denom = math.prod(math.factorial(m.count(u)) for u in set(m))
                d[m] = val / float(denom)
        return d

    def koszul_young_1_1_rank(T: np.ndarray) -> int:
        pairs = [(i, j) for i in range(N4) for j in range(i + 1, N4)]
        p_idx = {p: idx for idx, p in enumerate(pairs)}
        mat = np.zeros((len(pairs) * N4, N4 * N4), dtype=float)
        for a in range(N4):
            for b in range(N4):
                col = a * N4 + b
                for u in range(N4):
                    if u == a:
                        continue
                    row_p, s = (p_idx[(u, a)], 1.0) if u < a else (p_idx[(a, u)], -1.0)
                    mat[row_p * N4 : (row_p + 1) * N4, col] += s * T[u, b, :]
        return int(np.linalg.matrix_rank(mat, tol=1e-7))

    def metrics(C: np.ndarray) -> tuple[int, int, int, int]:
        d_poly = tens_to_poly_dict(C)
        rows_11 = np.zeros((256, len(M4_4)), dtype=float)
        rows_21 = np.zeros((N4 * len(M2_4), len(M3_4)), dtype=float)
        for m4, coef in d_poly.items():
            for s in set(m4):
                cnt = m4.count(s)
                rem = list(m4)
                rem.remove(s)
                for r in range(N4):
                    rows_11[r * N4 + s, idx4_4[tuple(sorted(rem + [r]))]] += coef * cnt
            for a in set(m4):
                c1 = m4.count(a)
                rem1 = list(m4)
                rem1.remove(a)
                for b in set(rem1):
                    if b < a:
                        continue
                    c2 = rem1.count(b)
                    rem2 = list(rem1)
                    rem2.remove(b)
                    ab_idx = idx2_4[(a, b)]
                    val = coef * c1 * c2
                    for r in range(N4):
                        rows_21[r * len(M2_4) + ab_idx, idx3_4[tuple(sorted(rem2 + [r]))]] += val
        rk_11 = int(np.linalg.matrix_rank(rows_11, tol=1e-7))
        rk_21 = int(np.linalg.matrix_rank(rows_21, tol=1e-7))

        # Smooth zero xz -> Hessian rank & YF_{1,1}(d^3 F(xz))
        ts = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
        xz = None
        for _ in range(30):
            x0 = rng.standard_normal(N4)
            dx = rng.standard_normal(N4)
            ys = np.array([sum(c * (x0 + t * dx)[m[0]] * (x0 + t * dx)[m[1]] * (x0 + t * dx)[m[2]] * (x0 + t * dx)[m[3]] for m, c in d_poly.items()) for t in ts])
            roots = [r.real for r in np.roots(np.polyfit(ts, ys, 4)) if abs(r.imag) < 1e-8]
            if roots:
                xz = x0 + roots[0] * dx
                break
        assert xz is not None
        H = np.einsum("abcd,c,d->ab", C, xz, xz) / 2.0
        rk_H = int(np.linalg.matrix_rank(H, tol=1e-6))
        rk_yf = koszul_young_1_1_rank(np.einsum("abcd,d->abc", C, xz))
        return rk_11, rk_21, rk_H, rk_yf

    C_det4 = tens4_perm_det(-1)
    C_perm4 = tens4_perm_det(1)
    C_abp2 = tens4_abp(2)
    C_abp3 = tens4_abp(3)
    C_abp4 = tens4_abp(4)

    res_det4 = metrics(C_det4)
    res_perm4 = metrics(C_perm4)
    res_abp2 = metrics(C_abp2)
    res_abp3 = metrics(C_abp3)
    res_abp4 = metrics(C_abp4)

    assert res_det4 == (226, 416, 8, 255), f"det_4 mismatch: {res_det4}"
    assert res_perm4 == (250, 512, 16, 255), f"perm_4 mismatch: {res_perm4}"
    assert res_abp2 == (176, 340, 8, 191), f"abp2 mismatch: {res_abp2}"
    assert res_abp3 == (256, 672, 14, 255), f"abp3 mismatch: {res_abp3}"
    assert res_abp4 == (256, 816, 16, 255), f"abp4 mismatch: {res_abp4}"
    print("[PASS] 2. n=4 Global Mixing Stress Test: ABP w=3 (m=10) exceeds perm_4 on SPD(1,1) & SPD(2,1) and saturates YF_{1,1}=255.")


def verify_fermionic_bath_schur_complement() -> None:
    """Verify Grenet m=7 nilpotent bath L_{11} and non-nilpotent bath homogeneous counterexample."""
    def grenet_perm3_mat(x: np.ndarray) -> np.ndarray:
        X = x.reshape(3, 3)
        subs = [tuple(s) for k in range(4) for s in itertools.combinations(range(3), k)]
        s_idx = {s: i for i, s in enumerate(subs)}
        M = np.eye(8, dtype=float)
        for k in range(3):
            for s in itertools.combinations(range(3), k):
                for j in range(3):
                    if j not in s:
                        ns = tuple(sorted(s + (j,)))
                        M[s_idx[s], s_idx[ns]] -= X[k, j]
        return M[:7, 1:]

    rng = np.random.default_rng(1)
    x = rng.standard_normal(9)
    p3 = sum(x[p[0]] * x[3 + p[1]] * x[6 + p[2]] for p in itertools.permutations(range(3)))
    assert abs(np.linalg.det(grenet_perm3_mat(x)) + p3) < 1e-10 or abs(np.linalg.det(grenet_perm3_mat(x)) - p3) < 1e-10
    A0 = grenet_perm3_mat(np.zeros(9))
    assert np.linalg.matrix_rank(A0) == 6
    perm_cols = [6, 0, 1, 2, 3, 4, 5]
    L11 = grenet_perm3_mat(x)[:, perm_cols][1:, 1:] - np.eye(6)
    assert np.max(np.abs(np.linalg.eigvals(L11))) < 1e-12
    assert np.linalg.matrix_rank(grenet_perm3_mat(np.array([0, 0, 0, 0, 0, 0, 1, 2, 3], dtype=float))) == 6

    # Non-nilpotent bath with exact degree cancellation: det([[x1, x1], [x2, 1+x2]]) == x1
    for _ in range(10):
        x1, x2 = rng.standard_normal(2)
        assert abs(np.linalg.det(np.array([[x1, x1], [x2, 1.0 + x2]])) - x1) < 1e-12

    print("[PASS] 3. Grenet m=7 nilpotent bath & non-nilpotent cancellation example verified.")


if __name__ == "__main__":
    verify_symmetric_and_variable_cut_mps()
    verify_global_mixing_stress_test_n4()
    verify_fermionic_bath_schur_complement()
    print("\nALL ROUND 8 STRASSEN VERIFICATIONS PASS (EXIT CODE 0).")
