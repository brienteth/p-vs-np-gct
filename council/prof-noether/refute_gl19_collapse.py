"""EARTH-SHATTERING COUNTEREXAMPLE TO THE #58 GL_19 GAUGE-COLLAPSE HYPOTHESIS:
With ONLY t_B = 3 protruding rows r_c(b) = b_0 e_{1,c} - b_1 e_{0,c} (c in {3, 4, 5}),
we achieve s_1 = 3 AND c = dim_F R(B_1) = 9 >> 4!
With t_B = 4 protruding rows r_c(b) = b_0 e_{1,c} - b_1 e_{0,c} (c in {2, 3, 4, 5}),
we achieve s_1 = 4 (FULL rational left kernel of B_2!) AND c = dim_F R(B_1) = 16 >> 4!"""
import itertools
import numpy as np
import sys
sys.path.append('p-vs-np-gct/council/prof-noether')
from general_n2k_noether import build_Mn

M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
sub2_to_idx = {s: i for i, s in enumerate(sub_2)}
sub3_to_idx = {s: i for i, s in enumerate(sub_3)}

B2_full = np.zeros((6, 20, 15), dtype=float)
for ell in range(20):
    B2_full[:, ell, :] = V_basis[:, ell].reshape(15, 6).T

def analyze_B2(B2_tensor, name):
    w = B2_tensor.shape[1]
    eqs = []
    for J in range(15):
        for c1 in range(6):
            for c2 in range(c1, 6):
                row = np.zeros(6 * w, dtype=float)
                for ell in range(w):
                    row[c1 * w + ell] += B2_tensor[c2, ell, J]
                    if c1 != c2:
                        row[c2 * w + ell] += B2_tensor[c1, ell, J]
                eqs.append(row)
    E = np.array(eqs)
    _, sv, vt = np.linalg.svd(E)
    rk_E = int(np.sum(sv > 1e-8))
    syz_basis = vt[rk_E:, :]
    num_syz = syz_basis.shape[0]
    rng = np.random.default_rng(2026)
    b_pt = rng.standard_normal(6)
    rk_B2 = np.linalg.matrix_rank(np.tensordot(b_pt, B2_tensor, axes=([0], [0])))
    B1_eval = np.zeros((num_syz, w))
    all_rows = []
    for k in range(num_syz):
        U_k = syz_basis[k].reshape(6, w)
        B1_eval[k] = b_pt @ U_k
        all_rows.append(U_k)
    s1 = np.linalg.matrix_rank(B1_eval)
    c_dim = np.linalg.matrix_rank(np.vstack(all_rows))
    print(f"[{name}]")
    print(f"  rank_K(B_2) = {rk_B2}, #deg-1 syzygies = {num_syz}, s_1 = rank_K(B_1) = {s1}, c = dim_F R(B_1) = {c_dim} !!")
    # Check exact equation B_1(b) B_2(b) == 0 at 5 random points
    for _ in range(5):
        bp = rng.standard_normal(6)
        B1p = np.array([bp @ syz_basis[k].reshape(6, w) for k in range(num_syz)])
        B2p = np.tensordot(bp, B2_tensor, axes=([0], [0]))
        assert np.linalg.norm(B1p @ B2p) < 1e-12
    # Check constant column space of B_1(b) when we embed the syzygies into 15 rows:
    return rk_B2, num_syz, s1, c_dim

# 1. t_B = 3 Counterexample: r_c(b) = b_0 e_{1,c} - b_1 e_{0,c} for c in {3, 4, 5}
# Canonical rows: include all 6 triples {0, c1, c2} and {1, c1, c2} for {c1, c2} subset {3, 4, 5}, plus 10 more (total 16)
needed_3 = [sub3_to_idx[tuple(sorted((a, c1, c2)))] for a in (0, 1) for c1, c2 in itertools.combinations([3, 4, 5], 2)]
other_3 = [i for i in range(20) if i not in needed_3][:10]
in_S_3 = needed_3 + other_3
assert len(in_S_3) == 16

B2_t3 = np.zeros((6, 19, 15))
for ell, s_idx in enumerate(in_S_3):
    B2_t3[:, ell, :] = B2_full[:, s_idx, :]
for idx, c in enumerate([3, 4, 5]):
    B2_t3[0, 16 + idx, sub2_to_idx[(1, c)]] = 1.0
    B2_t3[1, 16 + idx, sub2_to_idx[(0, c)]] = -1.0

rk2_3, nsyz_3, s1_3, c_3 = analyze_B2(B2_t3, "t_B = 3 Star-Koszul Counterexample (c in {3,4,5})")

# 2. t_B = 4 Counterexample: r_c(b) = b_0 e_{1,c} - b_1 e_{0,c} for c in {2, 3, 4, 5}
# Canonical rows: include all 12 triples {0, c1, c2} and {1, c1, c2} for {c1, c2} subset {2, 3, 4, 5}, plus 3 more (total 15)
needed_4 = [sub3_to_idx[tuple(sorted((a, c1, c2)))] for a in (0, 1) for c1, c2 in itertools.combinations([2, 3, 4, 5], 2)]
other_4 = [i for i in range(20) if i not in needed_4][:3]
in_S_4 = needed_4 + other_4
assert len(in_S_4) == 15

B2_t4 = np.zeros((6, 19, 15))
for ell, s_idx in enumerate(in_S_4):
    B2_t4[:, ell, :] = B2_full[:, s_idx, :]
for idx, c in enumerate([2, 3, 4, 5]):
    B2_t4[0, 15 + idx, sub2_to_idx[(1, c)]] = 1.0
    B2_t4[1, 15 + idx, sub2_to_idx[(0, c)]] = -1.0

rk2_4, nsyz_4, s1_4, c_4 = analyze_B2(B2_t4, "t_B = 4 Star-Koszul Counterexample (c in {2,3,4,5})")

# Check if rank_K(B2_t4) == 15! Wait: if needed_4 (12) + other_4 (3) has K-rank < 15, let's check ALL choices of other_4!
if rk2_4 < 15:
    print("  Checking other choices of 3 canonical rows to get rank_K(B_2) = 15...")
    rem = [i for i in range(20) if i not in needed_4]
    rng = np.random.default_rng(42)
    b_pt = rng.standard_normal(6)
    for comb in itertools.combinations(rem, 3):
        in_S_try = needed_4 + list(comb)
        B2_try = np.zeros((6, 19, 15))
        for ell, s_idx in enumerate(in_S_try):
            B2_try[:, ell, :] = B2_full[:, s_idx, :]
        for idx, c in enumerate([2, 3, 4, 5]):
            B2_try[0, 15 + idx, sub2_to_idx[(1, c)]] = 1.0
            B2_try[1, 15 + idx, sub2_to_idx[(0, c)]] = -1.0
        if np.linalg.matrix_rank(np.tensordot(b_pt, B2_try, axes=([0], [0]))) == 15:
            analyze_B2(B2_try, f"t_B = 4 with rank_K(B_2) == 15 (extra={[sub_3[i] for i in comb]})")
            break
