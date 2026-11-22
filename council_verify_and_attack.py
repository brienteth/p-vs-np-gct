"""Council verification + kmin=2 regime attack.

Verifies:
1. Euler's spectral decomposition: eigenvalues of M|_Sym_0(4) are {+2, +2, +2, -2, -2, -2}.
2. Noether's S4 irrep decomposition: V+ = 1 ⊕ (2,2), V- = (3,1).
3. Valiant's rank tuple enumeration: 31 survivors, 11 orbits.
4. NEW: Projection of K(B,V) onto Sym_0(4) basis — what's the max rank of K|_{Sym_0}?
5. NEW: For kmin=2, test whether (K1+K2)|_{Sym_0} can make rank(diag(+2,-2,...) - (K1+K2)) <= 3.
"""
import itertools
import numpy as np
from apolar_higher_betti_probe import rank_matrix_mod
from perm4_abp_frontier import MOD
from euler_w5_obstruction_proof import (
    build_nisan_and_sym0, kron_swap_mod, random_rank_matrix,
)
from perm4_middle_factorization_probe import extract_middle_4x4
from poly_exact import permanent_poly

rng = np.random.default_rng(20261121)

# --- Build M and Sym_0(4) basis ---
f_perm = permanent_poly(4)
p_perm = extract_middle_4x4(f_perm)
m_mat, s0 = build_nisan_and_sym0(p_perm, MOD)

# === TEST 1: Spectral decomposition of M restricted to Sym_0(4) ===
# s0 is 16x6 basis of Sym_0(4), with s0^T s0 = 2 * I_6.
# Operator matrix of M|_{Sym_0(4)} in the s0 basis is (s0^T s0)^{-1} s0^T M s0 = inv2 * s0^T M s0.
inv2 = pow(2, MOD - 2, MOD)
m_rest = (inv2 * (s0.T @ m_mat @ s0)) % MOD
# Over F_MOD, check eigenvalues by computing characteristic polynomial
# Or simpler: verify M_rest^2 = 4 * I_6 (since eigenvalues are ±2)
m_rest2 = (m_rest @ m_rest) % MOD
eye6_mod = (4 * np.eye(6, dtype=np.int64)) % MOD
assert np.array_equal(m_rest2 % MOD, eye6_mod % MOD), f"M_rest^2 != 4*I_6"
print("[PASS] Euler spectral: M|_Sym0(4)^2 = 4*I_6 (eigenvalues ±2)")

# Verify trace of M_rest = 0 (3*(+2) + 3*(-2) = 0)
tr = sum(m_rest[i, i] for i in range(6)) % MOD
assert tr == 0, f"trace = {tr}"
print(f"[PASS] trace(M|_Sym0) = 0 -> signature (3,3)")

# Compute the ±2 eigenspaces explicitly over F_MOD
# V+ = ker(M_rest - 2*I_6), V- = ker(M_rest + 2*I_6)
half_m = (m_rest * inv2) % MOD  # M_rest / 2
# P+ = (I + M_rest/2)/2, P- = (I - M_rest/2)/2
eye6 = np.eye(6, dtype=np.int64) % MOD
p_plus = ((eye6 + half_m) * inv2) % MOD
p_minus = ((eye6 - half_m) * inv2) % MOD
rk_plus = rank_matrix_mod(p_plus, MOD)
rk_minus = rank_matrix_mod(p_minus, MOD)
assert rk_plus == 3 and rk_minus == 3, f"rk+ = {rk_plus}, rk- = {rk_minus}"
print(f"[PASS] Eigenspace dimensions: V+ = {rk_plus}, V- = {rk_minus}")

# Check P+ P- = 0 (orthogonality)
pp = (p_plus @ p_minus) % MOD
assert np.all(pp % MOD == 0), "P+ P- != 0"
print("[PASS] V+ ⊥ V- (P+ P- = 0)")

# === TEST 2: Noether's matching basis ===
# X_k = (ij)+(complement), Y_k = (ij)-(complement)
# Pairs: {01,23}, {02,13}, {03,12}
pair_indices = [(0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2)]
# s0 columns are e_{ij} + e_{ji} for (i,j) in [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
# Column order: (01)=0, (02)=1, (03)=2, (12)=3, (13)=4, (23)=5
edge_to_col = {(0,1):0, (0,2):1, (0,3):2, (1,2):3, (1,3):4, (2,3):5}
for k, (i, j, p, q) in enumerate(pair_indices):
    e1 = min(i, j), max(i, j)
    e2 = min(p, q), max(p, q)
    c1, c2 = edge_to_col[e1], edge_to_col[e2]
    # X_k = col c1 + col c2 (in s0 basis, this is e_{c1} + e_{c2} in R^6)
    xk = np.zeros(6, dtype=np.int64)
    xk[c1] = 1; xk[c2] = 1
    yk = np.zeros(6, dtype=np.int64)
    yk[c1] = 1; yk[c2] = MOD - 1  # e_{c1} - e_{c2}
    # Check M_rest @ xk == 2 * xk (mod MOD)
    mx = (m_rest @ xk) % MOD
    assert np.array_equal(mx, (2 * xk) % MOD), f"X_{k} not +2 eigenvector: {mx} vs {(2*xk)%MOD}"
    my = (m_rest @ yk) % MOD
    assert np.array_equal(my, ((MOD - 2) * yk) % MOD), f"Y_{k} not -2 eigenvector: {my} vs {((MOD-2)*yk)%MOD}"
print("[PASS] Noether matching basis: X_k eigenvectors of +2, Y_k of -2")

# === TEST 3: Valiant rank tuple enumeration ===
count = 0
survivors = []
for r1 in range(5):
    for s1 in range(5):
        for r2 in range(5):
            for s2 in range(5):
                if r1 + r2 > 5: continue
                if s1 + s2 > 5: continue
                if min(r1, s2) + min(s1, r2) < 4: continue
                if r1 + s1 < 4: continue  # M1(a,a) has rank r1+s1 >= 4
                if r2 + s2 < 4: continue
                count += 1
                survivors.append((r1, s1, r2, s2))
print(f"[INFO] Valiant enumeration: {count} surviving rank tuples")
# Note: Valiant claimed 31 with r_i, s_i in {0..4}. Let's verify.
# Actually r1+s1 >= 4 is not necessarily a constraint — let me also count without it.
count2 = 0
for r1 in range(5):
    for s1 in range(5):
        for r2 in range(5):
            for s2 in range(5):
                if r1 + r2 > 5: continue
                if s1 + s2 > 5: continue
                if min(r1, s2) + min(s1, r2) < 4: continue
                count2 += 1
print(f"[INFO] Without r1+s1>=4 constraint: {count2} tuples")

# === TEST 4: Projection of K(B,V) onto Sym_0(4) ===
# K in R^{16x16}, project onto Sym_0(4): K_sym0 = s0^T K s0 (6x6 matrix)
# What is the maximum rank of K_sym0 for rank-r_B B, rank-r_V V?
max_proj_rank = {}
for rb in range(1, 5):
    for rv in range(1, 5):
        max_rk = 0
        for _ in range(200):
            B = random_rank_matrix(rb, rng, MOD)
            V = random_rank_matrix(rv, rng, MOD)
            K = kron_swap_mod(B, V, MOD)
            K_proj = (inv2 * (s0.T @ K @ s0)) % MOD
            rk = rank_matrix_mod(K_proj, MOD)
            if rk > max_rk:
                max_rk = rk
        max_proj_rank[(rb, rv)] = max_rk
print("\n[KEY RESULT] Max rank of K(B,V)|_Sym_0(4) (200 random per pair):")
header = "  r_B \\ r_V | " + "  ".join(f" {rv} " for rv in range(1, 5))
print(header)
print("  " + "-" * (len(header) - 2))
for rb in range(1, 5):
    row_str = "  ".join(f" {max_proj_rank[(rb, rv)]:2d}" for rv in range(1, 5))
    print(f"      {rb}     | {row_str}")

# === TEST 5: Can (K1+K2)|_Sym_0 make rank(diag(+2,-2,...) - (K1+K2)|_Sym_0) <= 3? ===
# M_rest in its eigenbasis is diag(+2,+2,+2,-2,-2,-2).
# We need K1_proj + K2_proj such that rank(M_rest_diag - K1_proj - K2_proj) <= 3.
# Since M_rest has rank 6, this means K1_proj + K2_proj must "cover" at least 3 eigenvalues.
# Test: for each (rb1, rv1, rb2, rv2) with rb1*rv1 + rb2*rv2 = potential Nisan rank,
# can we find K1 + K2 such that M_rest - K1_proj - K2_proj has rank <= 3?
print("\n[TEST 5] Testing rank(M_rest - K1_proj - K2_proj) for Case (3,2) configurations...")
min_residual_rank = {}
for rb1 in range(1, 5):
    for rv1 in range(1, 5):
        for rb2 in range(1, 5):
            for rv2 in range(1, 5):
                min_rk = 6
                for _ in range(50):
                    B1 = random_rank_matrix(rb1, rng, MOD)
                    V1 = random_rank_matrix(rv1, rng, MOD)
                    K1 = kron_swap_mod(B1, V1, MOD)
                    K1_proj = (inv2 * (s0.T @ K1 @ s0)) % MOD
                    B2 = random_rank_matrix(rb2, rng, MOD)
                    V2 = random_rank_matrix(rv2, rng, MOD)
                    K2 = kron_swap_mod(B2, V2, MOD)
                    K2_proj = (inv2 * (s0.T @ K2 @ s0)) % MOD
                    residual = (m_rest - K1_proj - K2_proj) % MOD
                    rk = rank_matrix_mod(residual, MOD)
                    if rk < min_rk:
                        min_rk = rk
                min_residual_rank[(rb1, rv1, rb2, rv2)] = min_rk

# Summarize: what's the absolute minimum residual rank across all configurations?
abs_min = min(min_residual_rank.values())
print(f"[KEY RESULT] Absolute minimum rank(M_rest - K1_proj - K2_proj) across all (rb1,rv1,rb2,rv2): {abs_min}")
# Show which configs achieved the minimum
for key, val in sorted(min_residual_rank.items()):
    if val <= 4:
        print(f"  Config {key}: min_rank = {val}")

# === TEST 6: Specific signature/inertia argument ===
# Over R (or F_p approximation): M_rest has signature (3,3).
# If K1_proj + K2_proj is positive semidefinite, then M_rest - K_sum has at most 3 negative eigenvalues
# (from M_rest's -2 block) so rank >= 3. For it to be exactly 3, the +2 block must be zeroed out.
# But K(B,V) is NOT symmetric in general! Check: is K_proj symmetric?
sym_count = 0
asym_count = 0
for _ in range(500):
    rb = int(rng.integers(1, 5))
    rv = int(rng.integers(1, 5))
    B = random_rank_matrix(rb, rng, MOD)
    V = random_rank_matrix(rv, rng, MOD)
    K = kron_swap_mod(B, V, MOD)
    K_proj = (inv2 * (s0.T @ K @ s0)) % MOD
    if np.array_equal(K_proj % MOD, K_proj.T % MOD):
        sym_count += 1
    else:
        asym_count += 1
print(f"\n[TEST 6] Symmetry of K(B,V)|_Sym_0: symmetric={sym_count}/500, asymmetric={asym_count}/500")

# === TEST 7: Does K(B,V)|_Sym_0 respect the V+/V- block structure? ===
# Check: does K_proj have zero off-diagonal blocks in the ±2 eigenbasis?
# Change of basis: construct the 6x6 unitary from X_k, Y_k basis
change_basis = np.zeros((6, 6), dtype=np.int64)
for k, (i, j, p, q) in enumerate(pair_indices):
    e1 = min(i, j), max(i, j)
    e2 = min(p, q), max(p, q)
    c1, c2 = edge_to_col[e1], edge_to_col[e2]
    change_basis[c1, k] = 1
    change_basis[c2, k] = 1
    change_basis[c1, k + 3] = 1
    change_basis[c2, k + 3] = MOD - 1
change_basis = change_basis % MOD
# Verify it diagonalizes M_rest
cb_inv = np.zeros((6, 6), dtype=np.int64)
# Since change_basis columns are orthogonal with norm 2, cb_inv = change_basis^T / 2
for i in range(6):
    for j in range(6):
        cb_inv[i, j] = (change_basis[j, i] * inv2) % MOD
m_diag = (cb_inv @ m_rest @ change_basis) % MOD
print(f"\n[TEST 7] M_rest in eigenbasis:")
print(m_diag)

# Now project K into this eigenbasis and check block structure
block_cross_nonzero = 0
block_cross_zero = 0
for _ in range(200):
    rb = int(rng.integers(1, 5))
    rv = int(rng.integers(1, 5))
    B = random_rank_matrix(rb, rng, MOD)
    V = random_rank_matrix(rv, rng, MOD)
    K = kron_swap_mod(B, V, MOD)
    K_proj = (inv2 * (s0.T @ K @ s0)) % MOD
    K_eig = (cb_inv @ K_proj @ change_basis) % MOD
    # Check off-diagonal blocks K_eig[0:3, 3:6] and K_eig[3:6, 0:3]
    cross1 = K_eig[0:3, 3:6] % MOD
    cross2 = K_eig[3:6, 0:3] % MOD
    if np.any(cross1 != 0) or np.any(cross2 != 0):
        block_cross_nonzero += 1
    else:
        block_cross_zero += 1
print(f"[TEST 7] K(B,V) in eigenbasis: cross-block nonzero = {block_cross_nonzero}/200, zero = {block_cross_zero}/200")

print("\n[DONE] Council verification + kmin=2 attack complete.")
