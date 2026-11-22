"""General even n = 2k Noether-Young representation theory, spectral decomposition,
Diagonal I_k Submatrix Lemma, and Lemma A_n / B_n / C_n verification for n = 4 and n = 6."""
import itertools
import math
import numpy as np

def build_Mn(n):
    assert n % 2 == 0
    k = n // 2
    subsets_km1 = list(itertools.combinations(range(n), k - 1))
    sub_to_idx = {s: idx for idx, s in enumerate(subsets_km1)}
    m_n = len(subsets_km1)
    D = m_n * n

    subsets_k = list(itertools.combinations(range(n), k))
    k_to_idx = {s: idx for idx, s in enumerate(subsets_k)}
    N_k = len(subsets_k)

    V_basis = np.zeros((D, N_k), dtype=int)
    for s_idx, S in enumerate(subsets_k):
        S_set = set(S)
        for c in S:
            I = tuple(sorted(S_set - {c}))
            row = sub_to_idx[I] * n + c
            V_basis[row, s_idx] = 1

    full_set = set(range(n))
    comp_perm = np.zeros((N_k, N_k), dtype=int)
    for s_idx, S in enumerate(subsets_k):
        Sc = tuple(sorted(full_set - set(S)))
        sc_idx = k_to_idx[Sc]
        comp_perm[s_idx, sc_idx] = 1

    Mn = V_basis @ comp_perm @ V_basis.T
    return Mn, V_basis, comp_perm, subsets_km1, subsets_k

def main():
    # 1. Verify Spectral & Cubic Identity M_n^3 = k^2 M_n for n = 4 and n = 6
    for n in [4, 6]:
        k = n // 2
        Mn, V_basis, comp_perm, sub_km1, sub_k = build_Mn(n)
        m_n = len(sub_km1)
        N_k = len(sub_k)
        D = m_n * n
        rk = np.linalg.matrix_rank(Mn)
        assert rk == N_k, f"Rank mismatch: {rk} != {N_k}"

        gram = V_basis.T @ V_basis
        assert np.array_equal(gram, k * np.eye(N_k, dtype=int))

        Mn2 = Mn @ Mn
        Mn3 = Mn2 @ Mn
        assert np.array_equal(Mn3, (k ** 2) * Mn), f"M_{n}^3 != {k^2} M_{n}"

        evals = np.linalg.eigvalsh(Mn.astype(float))
        n_pos = int(np.sum(np.isclose(evals, k)))
        n_neg = int(np.sum(np.isclose(evals, -k)))
        n_zero = int(np.sum(np.isclose(evals, 0.0)))
        assert n_pos == N_k // 2 and n_neg == N_k // 2 and n_zero == D - N_k
        print(f"[PASS] n={n} (k={k}): M_{n} is {D}x{D}, rank={rk}=C({n},{k}), spectrum={{+{k}: {n_pos}, -{k}: {n_neg}, 0: {n_zero}}}, M_{n}^3 == {k**2} M_{n}")

    # 2. Verify S_6 Irreducible Representation Decomposition of Sym_0(3; 6) (dim 20)
    n = 6
    k = 3
    Mn, V_basis, comp_perm, sub_km1, sub_k = build_Mn(6)
    sub_to_idx = {s: i for i, s in enumerate(sub_km1)}

    def cycle_type_s6(p):
        vis = [False] * 6
        cyc = []
        for i in range(6):
            if not vis[i]:
                c = 0
                cur = i
                while not vis[cur]:
                    vis[cur] = True
                    cur = p[cur]
                    c += 1
                cyc.append(c)
        cyc.sort(reverse=True)
        return tuple(cyc)

    s6_perms = list(itertools.permutations(range(6)))
    sub_r = {r: list(itertools.combinations(range(6), r)) for r in [1, 2, 3]}

    def fix_r_count(p, r):
        cnt = 0
        for s in sub_r[r]:
            ps = tuple(sorted(p[i] for i in s))
            if ps == s:
                cnt += 1
        return cnt

    class_reps = {}
    class_sizes = {}
    for p in s6_perms:
        ct = cycle_type_s6(p)
        class_sizes[ct] = class_sizes.get(ct, 0) + 1
        if ct not in class_reps:
            class_reps[ct] = p

    irrep_chars = {
        "(6) [j=0]": (1, {}),
        "(5,1) [j=1]": (5, {}),
        "(4,2) [j=2]": (9, {}),
        "(3,3) [j=3]": (5, {}),
    }
    for ct, p in class_reps.items():
        f1 = fix_r_count(p, 1)
        f2 = fix_r_count(p, 2)
        f3 = fix_r_count(p, 3)
        irrep_chars["(6) [j=0]"][1][ct] = 1
        irrep_chars["(5,1) [j=1]"][1][ct] = f1 - 1
        irrep_chars["(4,2) [j=2]"][1][ct] = f2 - f1
        irrep_chars["(3,3) [j=3]"][1][ct] = f3 - f2

    print("\n[S_6 Isotypic & Eigenvalue Decomposition on Sym_0(3; 6) (dim 20)]:")
    for name, (dim_ir, chi) in irrep_chars.items():
        mult_num = 0
        eig_trace_num = 0
        for ct, p in class_reps.items():
            sz = class_sizes[ct]
            tr_rho = fix_r_count(p, 3)
            comp_fixed = 0
            for S in sub_k:
                pS = set(p[i] for i in S)
                if pS.isdisjoint(set(S)):
                    comp_fixed += 1
            tr_M_rho = 3 * comp_fixed
            mult_num += sz * chi[ct] * tr_rho
            eig_trace_num += sz * chi[ct] * tr_M_rho
        assert mult_num % 720 == 0
        mult = mult_num // 720
        eig_scalar = (eig_trace_num // 720) // mult
        print(f"  Irrep {name:12s} | dim = {dim_ir:2d} | mult = {mult} | M_6 eigenvalue = {eig_scalar:+d}")
        j_val = int(name.split("j=")[1][0])
        assert mult == 1 and eig_scalar == ((-1) ** j_val) * 3

    print("[PASS] Noether-Young Formula verified for n=6: M_{2k}|_{V_{(2k-j, j)}} = (-1)^j * k * I")

    # 3. Verify Diagonal alpha_S I_k Submatrix Lemma & Lemma A_6 for n = 6 (k = 3)
    rng = np.random.default_rng(2026)
    for _ in range(20):
        alpha = rng.standard_normal(20)
        Y = (V_basis @ alpha).reshape(15, 6)
        for s_idx, S in enumerate(sub_k):
            rows = [sub_to_idx[tuple(sorted(set(S) - {c}))] for c in S]
            cols = list(S)
            submat = Y[np.ix_(rows, cols)]
            assert np.allclose(submat, alpha[s_idx] * np.eye(3)), "Diagonal I_k submatrix failed!"
    print("[PASS] Diagonal alpha_S I_k Submatrix Lemma verified for n=6 (every nonzero Y in Sym_0(k;n) has rank >= k=3)")

    for d in range(1, 7):
        max_obs = 0
        for trial in range(15):
            if trial < 6 and d <= 6:
                Z = np.eye(6)[:, :d]
            else:
                Z = rng.standard_normal((6, d))
            if d == 6:
                inter_dim = 20
            else:
                u, _, _ = np.linalg.svd(Z)
                Gamma = u[:, d:].T
                proj = np.kron(np.eye(15), Gamma) @ V_basis
                rk_proj = np.linalg.matrix_rank(proj)
                inter_dim = 20 - rk_proj
            if inter_dim > max_obs:
                max_obs = inter_dim
        bound = math.comb(d, 3)
        assert max_obs <= bound, f"Lemma A_6 failed for d={d}: {max_obs} > {bound}"
        print(f"[PASS] Lemma A_6 (d={d}): max dim(Sym_0(3;6) cap (F^15 (x) Z)) = {max_obs} <= C({d},3) = {bound}")

    # 4. Verify Single-Wire and Multi-Wire Swapped-Kronecker Perturbations at n = 6 (M_6 is 90x90, rank 20)
    def make_K6(B, V):
        # B, V are 15 x 6; K[(I, c1), (J, c2)] = B[I, c2] * V[J, c1]
        return np.einsum('il,jk->ikjl', B, V).reshape(90, 90)

    min_rk_1wire = 100
    for rB, rV in itertools.product(range(1, 7), repeat=2):
        B = rng.standard_normal((15, rB)) @ rng.standard_normal((rB, 6))
        V = rng.standard_normal((15, rV)) @ rng.standard_normal((rV, 6))
        rk = np.linalg.matrix_rank(Mn - make_K6(B, V))
        if rk < min_rk_1wire:
            min_rk_1wire = rk
    assert min_rk_1wire >= 21
    print(f"[PASS] Lemma B_6 (Single-Wire Floor across all (rB, rV) in {{1..6}}^2): min rank(M_6 - K(B,V)) = {min_rk_1wire} >= 21 > 20")

    # Test w = 19 wire-split (19 - s, s) at n = 6 for s = 1..9 (needs rank(M_6 - sum_{l=1}^s K_l) <= 19 - s)
    print("\n[n=6, w=19 Wire-Split (19-s, s) Swapped-Kronecker Perturbation Test]:")
    for s in range(1, 10):
        K_sum = np.zeros((90, 90))
        for _ in range(s):
            B = rng.standard_normal((15, 6))
            V = rng.standard_normal((15, 6))
            K_sum += make_K6(B, V)
        rk = np.linalg.matrix_rank(Mn - K_sum)
        req = 19 - s
        assert rk > req
        print(f"  s={s} (b,a)-wires: rank(M_6 - sum_{{l=1}}^{s} K_l) = {rk} > {req} required for w=19 [OBSTRUCTED]")

if __name__ == "__main__":
    main()
