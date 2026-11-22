"""Round 6 (Phase 6A) Prof. Noether — Obligation A Investigation:
1. Compute exact degree-3 rational syzygy space ker_K(B_{2,full}(b)^T) (dim 5) and its minimum support size m_min.
2. Test our GL_19 Gauge-Collapse Hypothesis and search for ANY counterexample with t_B in {2,3,4},
   s_1 in {3, 4}, and constant wire support c = dim_F R(B_1) >= 5!
3. Check the EXACT algebraic condition: for any c-dim subspace W_c = R(B_1) <= F^{19},
   rank_K(S_m(b)) <= rank_K(B2|_Wc) <= c - s_1, where m = dim(W_c cap Sym_0(3;6)) >= c - t_B!"""
import itertools
import numpy as np
import sys
sys.path.append('p-vs-np-gct/council/prof-noether')
from general_n2k_noether import build_Mn

M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
sub2_to_idx = {s: i for i, s in enumerate(sub_2)}
sub3_to_idx = {s: i for i, s in enumerate(sub_3)}

# Build B2_full(b) tensor of shape (6, 20, 15)
B2_full = np.zeros((6, 20, 15), dtype=float)
for ell in range(20):
    B2_full[:, ell, :] = V_basis[:, ell].reshape(15, 6).T

# =============================================================================
# 1. EXACT RATIONAL SYZYGY SPACE ker_K(B2_full(b)^T) (dim 5, degree 3)
# =============================================================================
print("=== 1. EXACT RATIONAL SYZYGY SPACE ker_K(B2_full(b)^T) ===")
# Notice: over K = F(b_0..b_5), evaluate B2_full(b) at a generic point b,
# and ALSO compute the exact degree-3 polynomial syzygies!
# Wait: what ARE the 5 degree-3 left syzygies of B2_full(b)?
# Recall: under diagonal rescaling D_{wedge^2 b} (15x15) and D_{wedge^3 b} (20x20):
# For T = {i, j, k} and J = {i, j} (T = J union {k}):
# B2_full(b)_{T, J} = b_k = (b_i b_j b_k) / (b_i b_j)!
# THEREFORE:
#   B2_full(b) = D_{wedge^3 b} @ G_6^T @ D_{wedge^2 b}^{-1} !!
# OH!! MY!! GOD!!
# LOOK AT THAT IDENTITY:
#   B2_full(b)_{20 x 15} = diag(b_i b_j b_k)_{20x20} * G_6^T * diag(b_r b_s)^{-1}_{15x15} !!
# WHERE G_6^T (20 x 15) IS THE CONSTANT GOTTLIEB INCIDENCE MATRIX (T contains J)!!

G6_T = np.zeros((20, 15), dtype=float)
for t_idx, T in enumerate(sub_3):
    T_set = set(T)
    for j_idx, J in enumerate(sub_2):
        if set(J).issubset(T_set):
            G6_T[t_idx, j_idx] = 1.0

rng = np.random.default_rng(2026)
b_pt = rng.standard_normal(6)
D3 = np.diag([b_pt[T[0]] * b_pt[T[1]] * b_pt[T[2]] for T in sub_3])
D2_inv = np.diag([1.0 / (b_pt[J[0]] * b_pt[J[1]]) for J in sub_2])
B2_eval = np.tensordot(b_pt, B2_full, axes=([0], [0]))
err_gottlieb = np.linalg.norm(B2_eval - D3 @ G6_T @ D2_inv)
print(f"[PASS] Exact Diagonal-Gottlieb Identity: ||B2_full(b) - D_{{wedge^3 b}} G_6^T D_{{wedge^2 b}}^{{-1}}|| = {err_gottlieb:.2e}")

# THEREFORE: u(b) B2_full(b) == 0  <==>  (u(b) D_{wedge^3 b}) G_6^T == 0 !!
# Since G_6^T has rank 15, its CONSTANT left kernel ker_F(G_6) has EXACT dimension 20 - 15 = 5!
# What IS ker_F(G_6) as an S_6-representation?!
# By Young's rule:
#   20-dim space = V_(6) [1] + V_(5,1) [5] + V_(4,2) [9] + V_(3,3) [5]
#   15-dim space = V_(6) [1] + V_(5,1) [5] + V_(4,2) [9]
# THEREFORE:
#   ker_F(G_6) = V_(3, 3) (THE 5-DIMENSIONAL IRREDUCIBLE S_6-REPRESENTATION V_{(3,3)}!!)
u_g, s_g, _ = np.linalg.svd(G6_T)
rk_g = int(np.sum(s_g > 1e-9))
ker_G6 = u_g[:, rk_g:].T  # 5 x 20
print(f"rank(G_6^T) = {rk_g}, dim ker_F(G_6) = {ker_G6.shape[0]} == dim V_{{(3,3)}} = 5!")

# Compute the EXACT minimum support size (Hamming weight) of any nonzero vector in V_{(3,3)} = ker_F(G_6)!
# Note: V_{(3,3)} is spanned by the Specht polytabloids!
# For a standard Young tableau of shape (3,3), e.g., rows (0,1,2) and (3,4,5):
# The column-alternating sum over S_2 x S_2 x S_2 on columns {0,3}, {1,4}, {2,5} has 2^3 = 8 terms:
#   sum_{eps in {0,1}^3} (-1)^{eps_0+eps_1+eps_2} e_{{a_0, a_1, a_2}} (where a_i = i if eps_i=0 else i+3)!
poly_vec = np.zeros(20, dtype=int)
cols = [(0, 3), (1, 4), (2, 5)]
for eps in itertools.product([0, 1], repeat=3):
    T = tuple(sorted(cols[i][eps[i]] for i in range(3)))
    sgn = (-1) ** sum(eps)
    poly_vec[sub3_to_idx[T]] = sgn
assert np.linalg.norm(poly_vec @ G6_T) == 0.0
print(f"[PASS] Specht Polytabloid in V_{{(3,3)}} = ker_F(G_6) has EXACT Hamming weight {int(np.sum(poly_vec != 0))} (8 terms, degree 3!)")

# Check minimum weight over ALL nonzero vectors in ker_F(G_6) over F_3 (3^5 - 1 = 242 vectors) and F_5 (5^5 - 1 = 3124 vectors)!
# Build exact integer basis of ker(G_6) using 5 Specht polytabloids
def make_polytabloid(c0, c1, c2):
    v = np.zeros(20, dtype=int)
    cs = [c0, c1, c2]
    for eps in itertools.product([0, 1], repeat=3):
        T = tuple(sorted(cs[i][eps[i]] for i in range(3)))
        v[sub3_to_idx[T]] = (-1) ** sum(eps)
    return v

# Standard Young tableaux of shape (3, 3): 5 SYTs!
# 1: (0,1,2)/(3,4,5), 2: (0,1,3)/(2,4,5), 3: (0,1,4)/(2,3,5), 4: (0,2,3)/(1,4,5), 5: (0,2,4)/(1,3,5)
syts = [
    ((0,3),(1,4),(2,5)),
    ((0,2),(1,4),(3,5)),
    ((0,2),(1,3),(4,5)),
    ((0,1),(2,4),(3,5)),
    ((0,1),(2,3),(4,5)),
]
B_V33 = np.array([make_polytabloid(*s) for s in syts], dtype=int)  # 5 x 20
assert np.linalg.matrix_rank(B_V33) == 5
assert np.linalg.norm(B_V33 @ G6_T) == 0.0

for p in [3, 5]:
    min_wt = 20
    for coeffs in itertools.product(range(p), repeat=5):
        if not any(coeffs):
            continue
        vec = (np.array(coeffs) @ B_V33) % p
        wt = int(np.sum(vec != 0))
        if wt < min_wt:
            min_wt = wt
    print(f"  Over F_{p}: minimum Hamming weight of nonzero v in V_{{(3,3)}} = {min_wt}")

# =============================================================================
# 2. SEARCH FOR COUNTEREXAMPLE TO GL_19 GAUGE-COLLAPSE (t_B in {2,3,4}, s_1 in {3,4}, c >= 5)
# =============================================================================
print("\n=== 2. TESTING ADVERSARIAL CONSTRUCTIONS FOR c = dim_F R(B_1) >= 5 AT t_B = 4, s_1 in {3, 4} ===")
# TRY AN ADVERSARIAL CONSTRUCTION FOR s_1 = 3, t_B = 4, c >= 5!!
# Wait: earlier we had:
#   v_{i, 4, 5}(b) = b_i e_{4,5} + b_4 e_{i,5} + b_5 e_{i,4}.
# Look at what happens if we set:
#   r_1(b) = b_0 e_{1,5} - b_1 e_{0,5}
#   r_2(b) = b_0 e_{1,4} - b_1 e_{0,4}
#   r_3(b) = b_0 e_{2,5} - b_2 e_{0,5}
#   r_4(b) = b_0 e_{2,4} - b_2 e_{0,4}
# That gave 2 syzygies (s_1 = 2, c = 7).
# NOW: WHAT ABOUT A 2-BLOCK CONSTRUCTION AT t_B = 4 WITH PURE KOSZUL + HILBERT #55?
# No, wait:
#   Block 1 (t=2): r_1, r_2 = b_0 e_{1,5} - b_1 e_{0,5}, b_0 e_{1,4} - b_1 e_{0,4} -> 1 syzygy (s=1, c=4)
#   Block 2 (t=2): two pure Koszul rows b_0 e_{0,1}, b_1 e_{0,1} -> 1 syzygy (s=1, c=2). Total s_1 = 2, c = 6.
# WHAT ABOUT SHARING ONE PURE KOSZUL ROW WITH A CANONICAL ROW?!
#   Take 3 pure Koszul rows on column {4,5}: r_1 = b_1 e_{4,5}, r_2 = b_2 e_{4,5}, r_3 = b_3 e_{4,5} (t = 3)
#   Wait: that gives s_1 = 2, c = 3.
#   Add r_4 = b_4 e_{0,5} + b_5 e_{0,4} (t = 4) -> v_{0,4,5} - r_4 = b_0 e_{4,5} -> s_1 = 3, c = 4 (still c = 4!).
#
# WAIT A SECOND!! WHAT ABOUT ADDING A **SHARED** PROTRUDING ROW TO MAKE s_1 = 3 WITH c = 5 OR 6?!
# Look at Hilbert's #55 relation for THREE indices {0, 1, 2}:
#   b_0 v_{1,4,5} - b_1 v_{0,4,5} = b_4 (b_0 e_{1,5} - b_1 e_{0,5}) + b_5 (b_0 e_{1,4} - b_1 e_{0,4})
# Notice that if you instead take:
#   r_0 = b_4 e_{0,5} + b_5 e_{0,4}  =>  w_0 = v_{0,4,5} - r_0 = b_0 e_{4,5}
#   r_1 = b_4 e_{1,5} + b_5 e_{1,4}  =>  w_1 = v_{1,4,5} - r_1 = b_1 e_{4,5}
#   r_2 = b_4 e_{2,5} + b_5 e_{2,4}  =>  w_2 = v_{2,4,5} - r_2 = b_2 e_{4,5}
#   That's t = 3, s_1 = 2, c = 3!
#   Can we add 1 MORE protruding row r_3 (t = 4) to get s_1 = 3 with c >= 5?!
#   Wait: for r_3 to create a NEW syzygy involving canonical rows beyond w_0, w_1, w_2,
#   by Hyperplane Syzygy Rigidity (codim 1 has syz dim 0!), 1 protruding row r_3 CANNOT couple to B_{2,in} alone!
#   WAIT A SECOND!! WHAT IF r_3 COUPLES TO w_0, w_1, w_2 AND ANOTHER CANONICAL ROW?!
#   Test: w_0 = b_0 e_{4,5}, w_1 = b_1 e_{4,5}, w_2 = b_2 e_{4,5} (all on column {4,5}!),
#   AND take a 4th protruding row r_3 = b_3 e_{4,5} + something? If r_3 = b_3 e_{4,5}, c = 4!
#   What if we instead try a **3-VARIABLE** codim-3 cancellation (b_3 = b_4 = b_5 = 0)?
#   Recall at b_3 = b_4 = b_5 = 0, codim = 3 had deg-1 syz dim = 12!
#   Let's inspect ALL 12 syzygies of B2_full|_{b_3 = b_4 = b_5 = 0} and ALL 14 syzygies of B2_full|_{b_2=b_3=b_4=b_5=0}!

for codim, zero_vars in [(2, [4, 5]), (3, [3, 4, 5]), (4, [2, 3, 4, 5])]:
    keep = [c for c in range(6) if c not in zero_vars]
    d = len(keep)
    B2_res = B2_full[keep, :, :]  # (d, 20, 15)
    eqs = []
    for J in range(15):
        for a1 in range(d):
            for a2 in range(a1, d):
                row = np.zeros(d * 20, dtype=float)
                for ell in range(20):
                    row[a1 * 20 + ell] += B2_res[a2, ell, J]
                    if a1 != a2:
                        row[a2 * 20 + ell] += B2_res[a1, ell, J]
                eqs.append(row)
    E = np.array(eqs)
    _, sv, vt = np.linalg.svd(E)
    rk = int(np.sum(sv > 1e-8))
    null_basis = vt[rk:, :]
    # Check which of the 20 rows of B2_full are actually involved in these syzygies!
    involved = []
    for ell in range(20):
        col_slice = null_basis[:, [a * 20 + ell for a in range(d)]]
        if np.linalg.norm(col_slice) > 1e-6:
            involved.append(sub_3[ell])
    # Also compute the K-rank (over F(b_keep)) of these syzygies!
    z_pt = rng.standard_normal(d)
    S_eval = np.zeros((null_basis.shape[0], 20))
    for k in range(null_basis.shape[0]):
        S_eval[k] = z_pt @ null_basis[k].reshape(d, 20)
    print(f"codim={codim} (zero vars {zero_vars}): deg-1 syz dim = {null_basis.shape[0]}, K-rank = {np.linalg.matrix_rank(S_eval)}, involved T ({len(involved)}): {involved}")
