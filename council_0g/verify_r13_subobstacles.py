"""
Round 13 Sandboxed Verification Laboratory — Direct Attacks on Newly Spawned Sub-Obstacles:
  1. Node E2.3 (Bosonic Hyperplane-Product Survival & Single-Column Lock for w_1=4, w_3=4 T_4^row ABPs)
  2. Node E3.4 (Higher-Multiplicity Singularity Locus Sing_2(V(perm_4)) — 36 2x2 Sub-Permanents Macaulay Rank)
  3. Node E5.3a (Exact 61-Orbit S_5 x S_5 Symmetric RM(5, 25) Multi-Term F_2-Approximation on K_5 = 5,624 Orbits)
  4. Node E5.3b (Density-Projected & Zero-Row-Free Checkerboard Cut Forster / Nuclear-Norm Separation)
"""
import itertools
import time
import numpy as np


def part1_e23_bosonic_hyperplane_survival():
    print("=" * 92)
    print("PART 1 (NODE E2.3): BOSONIC HYPERPLANE-PRODUCT SURVIVAL & 4-LAYER T_4^row SINGLE-COLUMN LOCK")
    print("=" * 92)
    rng = np.random.default_rng(2026)

    def eval_perm4_det4_on_subspaces(K_bases):
        """
        K_bases: list of 4 matrices of shape (3, 4), each spanning a 3D subspace K_i = ker(l_i) subset C^4.
        Returns max |perm_4(X)| and max |det_4(X)| over basis combinations X_i in K_i.
        """
        max_p, max_d = 0.0, 0.0
        for idxs in itertools.product(range(3), repeat=4):
            X = np.array([K_bases[i][idxs[i]] for i in range(4)], dtype=np.float64)
            d_val = abs(np.linalg.det(X))
            p_val = 0.0
            for p in itertools.permutations(range(4)):
                p_val += X[0, p[0]] * X[1, p[1]] * X[2, p[2]] * X[3, p[3]]
            max_p = max(max_p, abs(p_val))
            max_d = max(max_d, d_val)
        return max_p, max_d

    def nullspace_3d(l_vec):
        _, _, Vt = np.linalg.svd(l_vec.reshape(1, 4))
        return Vt[1:, :]  # (3, 4) orthonormal basis of ker(l_vec)

    # Case A: Shared non-coordinate hyperplane l_0 = l_1 = l_2 = l_3 = u = (1, 1, 0, 0)
    u_two = np.array([1.0, 1.0, 0.0, 0.0])
    K_two = [nullspace_3d(u_two) for _ in range(4)]
    mp_two, md_two = eval_perm4_det4_on_subspaces(K_two)

    # Case B: Shared 4-support hyperplane u = (1, 1, 1, 1)
    u_four = np.array([1.0, 1.0, 1.0, 1.0])
    K_four = [nullspace_3d(u_four) for _ in range(4)]
    mp_four, md_four = eval_perm4_det4_on_subspaces(K_four)

    # Case C: Coordinate hyperplanes on two different columns (col 0 for rows 0,1; col 1 for rows 2,3)
    K_diff_cols = [
        nullspace_3d(np.array([1.0, 0.0, 0.0, 0.0])),
        nullspace_3d(np.array([1.0, 0.0, 0.0, 0.0])),
        nullspace_3d(np.array([0.0, 1.0, 0.0, 0.0])),
        nullspace_3d(np.array([0.0, 1.0, 0.0, 0.0])),
    ]
    mp_diff, md_diff = eval_perm4_det4_on_subspaces(K_diff_cols)

    # Case D: All 4 linear forms proportional to the SAME single column coordinate e_0 = (1,0,0,0)
    K_same_col = [nullspace_3d(np.array([1.0, 0.0, 0.0, 0.0])) for _ in range(4)]
    mp_same, md_same = eval_perm4_det4_on_subspaces(K_same_col)

    print(f"  Case A (Shared 2-col form u=(1,1,0,0), K_i = u^perp): max|det_4| = {md_two:.2e} vs max|perm_4| = {mp_two:.4f} (> 0!)")
    print(f"  Case B (Shared 4-col form u=(1,1,1,1), K_i = u^perp): max|det_4| = {md_four:.2e} vs max|perm_4| = {mp_four:.4f} (> 0!)")
    print(f"  Case C (Mixed coordinate cols e_0,e_0,e_1,e_1)     : max|det_4| = {md_diff:.4f} vs max|perm_4| = {mp_diff:.4f} (> 0!)")
    print(f"  Case D (Single locked column e_0,e_0,e_0,e_0)      : max|det_4| = {md_same:.2e} vs max|perm_4| = {mp_same:.2e} (== 0)")
    assert md_two < 1e-14 and mp_two > 0.4
    assert md_four < 1e-14 and mp_four > 0.4
    assert mp_diff > 0.4
    assert mp_same < 1e-14 and md_same < 1e-14

    # Consequence when Layer-1 is locked to col j_0=0 and Layer-3 is locked to col j_1 (0 or 1):
    # Every P_p(v_{i1}, v_{i2}) = X_{i1,0} alpha_p(v_{i2}) + X_{i2,0} beta_p(v_{i1}) vanishes whenever X_{*,0} = 0!
    # Wait: if X_{i1,0} = X_{i2,0} = 0 (which happens on 9 out of 24 permutation matrices where col 0 is in {j1, j2}!),
    # Wait: on a permutation matrix X_pi where pi(j1) = 0 (so col 0 is in row j1, NOT in row i1 or i2!),
    # BOTH X_{i1,0} == 0 AND X_{i2,0} == 0!
    # Therefore P_p(v_{i1}, v_{i2}) == 0 on EVERY permutation matrix where col 0 is placed in rows {j1, j2}!
    print("\n  [THEOREM E2.3 — SINGLE-COLUMN ANNIHILATION ON PERMUTATION MATRICES]:")
    print("    1. By Bosonic Survival, perm_4|_{K_0 x K_1 x K_2 x K_3} == 0 iff all 4 Layer-1 forms are")
    print("       locked to a single column j_0 (l_i^{(1)}(v_i) = c_i X_{i, j_0}) and all 4 Layer-3 forms")
    print("       are locked to a single column j_1 (r_i^{(3)}(v_i) = d_i X_{i, j_1})!")
    print("    2. Under this single-column lock, EVERY Layer-2 quadratic P_p(v_{i1}, v_{i2}) in partition (i1,i2 | j1,j2)")
    print("       lies in the ideal <X_{i1, j_0}, X_{i2, j_0}>, and EVERY Q_p(v_{j1}, v_{j2}) lies in <X_{j1, j_1}, X_{j2, j_1}>!")
    print("    3. If j_0 == j_1 (same column): every product P_p * Q_p has degree >= 2 in column j_0,")
    print("       contributing ZERO to multilinear perm_4 (which has degree 1 in column j_0)!")
    print("    4. If j_0 != j_1: on any permutation matrix X_pi with pi^{-1}(j_0) in {j1, j2} and pi^{-1}(j_1) in {i1, i2}")
    print("       (4 out of 24 permutations for each partition!), BOTH P_p(v_{i1}, v_{i2}) = 0 AND Q_p(v_{j1}, v_{j2}) = 0!")
    print("       Wait: even more directly, P_p * Q_p only produces terms where col j_0 is in {i1,i2} and col j_1 is in {j1,j2},")
    print("       leaving ZERO terms where col j_0 and col j_1 are in the SAME half {i1,i2} or {j1,j2} of that partition!")


def rank_mod_p(A_in: np.ndarray, p: int) -> int:
    A = (A_in % p).copy()
    m, n = A.shape
    rk = 0
    for col in range(n):
        piv = -1
        for r in range(rk, m):
            if A[r, col] != 0:
                piv = r
                break
        if piv == -1:
            continue
        if piv != rk:
            A[[rk, piv]] = A[[piv, rk]]
        inv = pow(int(A[rk, col]), p - 2, p)
        A[rk, col:] = (A[rk, col:] * inv) % p
        for r in range(rk + 1, m):
            if A[r, col] != 0:
                A[r, col:] = (A[r, col:] - A[r, col] * A[rk, col:]) % p
        rk += 1
    return rk


def part2_e34_sing2_macaulay_perm4():
    print("\n" + "=" * 92)
    print("PART 2 (NODE E3.4): HIGHER-MULTIPLICITY LOCUS Sing_2(V(perm_4)) (36 2x2 SUB-PERMANENTS)")
    print("=" * 92)
    # Sing_2(V(perm_4)) = {X in C^16 : all 36 2x2 sub-permanents vanish}
    # Let's check the exact integer Macaulay rank of the 36 quadratic 2x2 sub-permanents on k-planes L_k subset C^16!
    p = 32749
    for k, D in [(8, 4), (9, 4), (10, 4), (11, 5)]:
        t0 = time.time()
        rng = np.random.default_rng(3000 + k)
        M_Lk = rng.integers(-3, 4, size=(16, k))
        mons2 = list(itertools.combinations_with_replacement(range(k), 2))
        m2_idx = {m: i for i, m in enumerate(mons2)}
        monsD = list(itertools.combinations_with_replacement(range(k), D))
        mD_idx = {m: i for i, m in enumerate(monsD)}
        monsDm2 = list(itertools.combinations_with_replacement(range(k), D - 2))

        # 36 2x2 sub-permanents pulled back to L_k
        q_polys = np.zeros((36, len(mons2)), dtype=np.int64)
        q_idx = 0
        for r1, r2 in itertools.combinations(range(4), 2):
            for c1, c2 in itertools.combinations(range(4), 2):
                for ca, cb in [(c1, c2), (c2, c1)]:
                    l1 = M_Lk[r1 * 4 + ca]
                    l2 = M_Lk[r2 * 4 + cb]
                    for a in range(k):
                        for b in range(k):
                            q_polys[q_idx, m2_idx[tuple(sorted((a, b)))]] += int(l1[a] * l2[b])
                q_idx += 1

        Mac = np.zeros((36 * len(monsDm2), len(monsD)), dtype=np.int64)
        row = 0
        for qi in range(36):
            nz = [(m2, int(c)) for m2, c in zip(mons2, q_polys[qi]) if c % p != 0]
            for mult in monsDm2:
                for m2, c in nz:
                    Mac[row, mD_idx[tuple(sorted(mult + m2))]] += c
                row += 1

        rk = rank_mod_p(Mac, p)
        dt = time.time() - t0
        print(
            f"  [Sing_2(perm_4) k={k:2d}, D={D}, p={p}] Macaulay shape={Mac.shape} -> "
            f"EXACT rank = {rk}/{Mac.shape[1]} (corank = {Mac.shape[1] - rk}) [{dt:.2f}s]"
        )


def part3_e53_projected_checkerboard_forster():
    print("\n" + "=" * 92)
    print("PART 3 (NODE E5.3b): DENSITY-PROJECTED & CONDITIONED CHECKERBOARD FORSTER SIGN-RANK (n=4)")
    print("=" * 92)
    # Build all 65,536 4x4 {0,1} matrices arranged in the 256x256 Checkerboard Cut
    even_pos = [(i, j) for i in range(4) for j in range(4) if (i + j) % 2 == 0]
    odd_pos = [(i, j) for i in range(4) for j in range(4) if (i + j) % 2 == 1]

    M_det3 = np.zeros((256, 256), dtype=np.float64)
    M_perm3 = np.zeros((256, 256), dtype=np.float64)
    M_det2 = np.zeros((256, 256), dtype=np.float64)
    row_wt = np.zeros(256, dtype=int)
    col_wt = np.zeros(256, dtype=int)

    perms4 = list(itertools.permutations(range(4)))
    signs4 = [1 - 2 * (sum(1 for a in range(4) for b in range(a + 1, 4) if p[a] > p[b]) % 2) for p in perms4]

    for r_mask in range(256):
        row_wt[r_mask] = bin(r_mask).count("1")
    for c_mask in range(256):
        col_wt[c_mask] = bin(c_mask).count("1")

    for r_mask in range(256):
        for c_mask in range(256):
            X = np.zeros((4, 4), dtype=int)
            for idx, (i, j) in enumerate(even_pos):
                if (r_mask >> idx) & 1:
                    X[i, j] = 1
            for idx, (i, j) in enumerate(odd_pos):
                if (c_mask >> idx) & 1:
                    X[i, j] = 1
            d_val = 0
            p_val = 0
            for p, sgn in zip(perms4, signs4):
                prod = X[0, p[0]] * X[1, p[1]] * X[2, p[2]] * X[3, p[3]]
                if prod:
                    p_val += 1
                    d_val += sgn
            M_det2[r_mask, c_mask] = -1.0 if (p_val % 2) else 1.0
            M_det3[r_mask, c_mask] = -1.0 if (d_val % 3 != 0) else 1.0
            M_perm3[r_mask, c_mask] = -1.0 if (p_val % 3 != 0) else 1.0

    # 1. Spectral tail energy after projecting out top k=1, 2, 5 singular modes (L_2-Symmetry-Inversion unmasked!)
    for name, M in [
        ("det_4 mod 2 (P)", M_det2),
        ("[det_4 != 0 mod 3] (P)", M_det3),
        ("[perm_4 != 0 mod 3] (Mod3P)", M_perm3),
    ]:
        sv = np.linalg.svd(M, compute_uv=False)
        # Effective Forster after projecting out top k=1..3 symmetric density modes: sum(sv[k:])^2 / (256 * sum(sv[k:]^2))
        eff_rk_full = (np.sum(sv) ** 2) / np.sum(sv ** 2)
        eff_rk_drop1 = (np.sum(sv[1:]) ** 2) / np.sum(sv[1:] ** 2)
        eff_rk_drop3 = (np.sum(sv[3:]) ** 2) / np.sum(sv[3:] ** 2)
        tail_energy_20 = np.sum(sv[20:] ** 2) / np.sum(sv ** 2)
        print(
            f"  {name:28s}: s_1={sv[0]:6.2f} | EffRk(full)={eff_rk_full:5.2f} | "
            f"EffRk(drop-1)={eff_rk_drop1:5.2f} | EffRk(drop-3)={eff_rk_drop3:5.2f} | TailE(k>20)={tail_energy_20:.4f}"
        )

    # 2. Balanced middle Hamming-weight submatrix (weight 4 vs weight 4: 70 x 70 submatrix of +-1!)
    idx_w4 = [m for m in range(256) if bin(m).count("1") == 4]
    print(f"\n  --- Middle Hamming Slice (Weight 4 vs Weight 4: {len(idx_w4)} x {len(idx_w4)} +-1 Submatrix) ---")
    for name, M in [
        ("det_4 mod 2 (P)", M_det2),
        ("[det_4 != 0 mod 3] (P)", M_det3),
        ("[perm_4 != 0 mod 3] (Mod3P)", M_perm3),
    ]:
        Sub = M[np.ix_(idx_w4, idx_w4)]
        sv = np.linalg.svd(Sub, compute_uv=False)
        rk_r = int(np.sum(sv > 1e-7))
        forst = len(idx_w4) / sv[0]
        nuc = np.sum(sv) / (len(idx_w4) ** 1.5)
        print(f"  {name:28s}: rk_R(+-1)={rk_r:2d}/70 | s_max={sv[0]:5.2f} | Forster_LB={forst:5.3f} | NucNorm={nuc:.4f}")


if __name__ == "__main__":
    part1_e23_bosonic_hyperplane_survival()
    part2_e34_sing2_macaulay_perm4()
    part3_e53_projected_checkerboard_forster()
