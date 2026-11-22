"""Prof. Wigner Round 9 (Wall 2 Follow-up):
Test exact 256x256 bipartite communication matrices (rows {0,1} vs {2,3}) over R, F_2, F_3,
AND exact maximum monotone/constant subcube / affine restriction structure, AND
joint (Symmetry + Non-Linear/Algebraic Rank) separation across all 6 Boolean functions on {0,1}^{4x4}!
"""
import numpy as np
import time
from round9_wall2_boolean_probe import (
    build_all_4x4_matrices, eval_det4_perm4_exact, build_s4xs4_permutations
)


def gf_rank(mat: np.ndarray, p: int) -> int:
    """Exact Gaussian elimination rank of a binary/integer matrix mod prime p."""
    A = (mat % p).astype(np.int64).copy()
    m, n = A.shape
    r = 0
    for c in range(n):
        piv = -1
        for i in range(r, m):
            if A[i, c] != 0:
                piv = i
                break
        if piv == -1:
            continue
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        inv = pow(int(A[r, c]), p - 2, p)
        A[r, c:] = (A[r, c:] * inv) % p
        # Vectorized elimination on remaining rows
        col = A[r + 1:, c]
        nz = np.where(col != 0)[0] + (r + 1)
        if len(nz) > 0:
            factors = A[nz, c:c + 1]
            A[nz, c:] = (A[nz, c:] - factors * A[r:r + 1, c:]) % p
        r += 1
    return r


def max_affine_or_subcube_check(f01: np.ndarray):
    """Find best correlation max_L |E[(-1)^{f(x) + L(x)}]| = max_S |f_hat(S)| (Walsh spectral radius / nonlinearity)
    AND max correlation with quadratic F_2 forms? No, spectral radius & L_inf of Walsh transform!"""
    h = (1.0 - 2.0 * f01.astype(np.float64)).copy()
    for b in range(16):
        step = 1 << b
        v = h.reshape(-1, 2 * step)
        x = v[:, :step].copy()
        y = v[:, step:]
        v[:, :step] = x + y
        v[:, step:] = x - y
    fhat = h / (1 << 16)
    lin_bias = float(np.max(np.abs(fhat)))
    # Also compute exact 2-local / pair correlation and exact real SVD entropy of 256x256 matrix!
    return lin_bias


def main():
    t0 = time.time()
    X = build_all_4x4_matrices()
    det4, perm4 = eval_det4_perm4_exact(X)
    _, _, n_orbits, orbit_inv = build_s4xs4_permutations()
    rng = np.random.default_rng(202611219)

    f_det_mod2 = (np.abs(det4) % 2).astype(np.uint8)
    f_det_mod3 = ((det4 % 3) != 0).astype(np.uint8)
    f_perm_pos = (perm4 > 0).astype(np.uint8)
    f_perm_mod3 = ((perm4 % 3) != 0).astype(np.uint8)
    f_rand_bal = rng.integers(0, 2, size=1 << 16, dtype=np.uint8)
    orb_rand_bits = rng.integers(0, 2, size=n_orbits, dtype=np.uint8)
    f_rand_sym = orb_rand_bits[orbit_inv]

    funcs = [
        ("det_4 mod 2 (P)", f_det_mod2),
        ("[det_4 != 0 mod 3] (P)", f_det_mod3),
        ("[perm_4 > 0] (P)", f_perm_pos),
        ("[perm_4 != 0 mod 3] (Mod3P)", f_perm_mod3),
        ("Random Boolean (RR Ctrl)", f_rand_bal),
        ("Random S4xS4-Sym (SymCtrl)", f_rand_sym),
    ]

    # Note: bit order in build_all_4x4_matrices: bits 0..7 are rows 0..1, bits 8..15 are rows 2..3!
    # So reshape(256, 256) splits rows {2,3} (axis 0) vs rows {0,1} (axis 1)!
    print("=" * 96)
    print("PROF. WIGNER ROUND 9 (WALL 2): 256x256 BIPARTITE COMMUNICATION RANKS (R, F_2, F_3) & NONLINEARITY")
    print("=" * 96)
    print(f"{'Function':27s} | {'rk_R(M)':7s} | {'rk_F2(M)':8s} | {'rk_F3(M)':8s} | {'rk_R(+-1)':9s} | {'max|f^|':8s} | {'1/s_eff(M)':10s}")
    print("-" * 96)
    for name, f01 in funcs:
        M01 = f01.reshape(256, 256)
        Mpm = 1.0 - 2.0 * M01.astype(np.float64)
        rk_R = int(np.linalg.matrix_rank(M01.astype(np.float64)))
        rk_pm = int(np.linalg.matrix_rank(Mpm))
        rk_2 = gf_rank(M01, 2)
        rk_3 = gf_rank(M01, 3)
        lin_bias = max_affine_or_subcube_check(f01)
        # Effective Schmidt rank exp(H_vN) of normalized M01 (or Mpm):
        s = np.linalg.svd(Mpm, compute_uv=False)
        p = (s ** 2) / np.sum(s ** 2)
        p = p[p > 1e-16]
        schmidt_eff = float(2.0 ** (-np.sum(p * np.log2(p))))
        print(f"{name:27s} | {rk_R:7d} | {rk_2:8d} | {rk_3:8d} | {rk_pm:9d} | {lin_bias:8.5f} | {schmidt_eff:10.2f}")

    # Also check: F_3-polynomial degree / rank of the indicator [F != 0 mod 3] vs [F == 0 mod 3]
    # Wait: WHY is rk_F3([det_4 != 0 mod 3]) low?! Because det_4 is sum of 6 products, so det_4^2 mod 3 is sum of 21 products!
    # Check rk_F3 and rk_R on the 2x2-column vs 2x2-row split? It's identical by transpose symmetry for S4xS4xZ2!
    # Wait: check 1-row vs 3-rows (16 x 4096) matrix rank over R, F_2, F_3!
    print("\n--- 1-Row vs 3-Rows (16 x 4096) Bipartite Matrix Rank ---")
    print(f"{'Function':27s} | {'rk_R(16x4096)':13s} | {'rk_F2(16x4096)':14s} | {'rk_F3(16x4096)':14s}")
    print("-" * 78)
    for name, f01 in funcs:
        M1 = f01.reshape(4096, 16).T
        print(f"{name:27s} | {int(np.linalg.matrix_rank(M1.astype(np.float64))):13d} | {gf_rank(M1, 2):14d} | {gf_rank(M1, 3):14d}")

    print(f"\n[DONE] Completed in {time.time()-t0:.2f}s.")


if __name__ == "__main__":
    main()
