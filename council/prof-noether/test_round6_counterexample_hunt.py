"""Round 6 (Phase 6A) Prof. Noether — Systematic Hunt for (t_B <= 4, s_1 in {3, 4}, c >= 5)
AND Algebraic Obstruction Verification for s_1 = 4 & Rank-2 Protrusion Theorem."""
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

def analyze_B2(B2_tensor, name=""):
    """Compute deg-1 left syzygy space, function-field rank s_1, constant wire support c = dim_F R(B_1),
    and B_2 K-rank."""
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
    rng = np.random.default_rng(12345)
    b_pt = rng.standard_normal(6)
    rk_B2 = np.linalg.matrix_rank(np.tensordot(b_pt, B2_tensor, axes=([0], [0])))
    if num_syz == 0:
        print(f"  [{name:45s}] rk(B2)={rk_B2}, #syz=0, s1=0, c=0")
        return rk_B2, 0, 0, 0
    B1_eval = np.zeros((num_syz, w))
    all_rows = []
    for k in range(num_syz):
        U_k = syz_basis[k].reshape(6, w)
        B1_eval[k] = b_pt @ U_k
        all_rows.append(U_k)
    s1 = np.linalg.matrix_rank(B1_eval)
    c_dim = np.linalg.matrix_rank(np.vstack(all_rows))
    print(f"  [{name:45s}] rk(B2)={rk_B2}, #syz={num_syz:2d}, s1={s1}, c=dim R(B1)={c_dim}")
    return rk_B2, num_syz, s1, c_dim

print("=== SYSTEMATIC ADVERSARIAL CONSTRUCTIONS AT t_B = 2, 3, 4 ===")

# Construction A: Hilbert #55 (t_B = 2) -> s1 = 1, c = 4
B2 = np.zeros((6, 19, 15))
in_S = [sub3_to_idx[(0,4,5)], sub3_to_idx[(1,4,5)]] + [i for i in range(20) if i not in (sub3_to_idx[(0,4,5)], sub3_to_idx[(1,4,5)])][:15]
for ell, s_idx in enumerate(in_S):
    B2[:, ell, :] = B2_full[:, s_idx, :]
# r1 = b0 e_{1,5} - b1 e_{0,5}, r2 = b0 e_{1,4} - b1 e_{0,4}
B2[0, 17, sub2_to_idx[(1,5)]] = 1; B2[1, 17, sub2_to_idx[(0,5)]] = -1
B2[0, 18, sub2_to_idx[(1,4)]] = 1; B2[1, 18, sub2_to_idx[(0,4)]] = -1
analyze_B2(B2, "A: Hilbert #55 (t_B=2)")

# Construction B: Double Hilbert #55 on {0,1} and {2,3} (t_B = 4) -> s1 = 2, c = 8
B2 = np.zeros((6, 19, 15))
special4 = [sub3_to_idx[(i,4,5)] for i in range(4)]
in_S = special4 + [i for i in range(20) if i not in special4][:11]
for ell, s_idx in enumerate(in_S):
    B2[:, ell, :] = B2_full[:, s_idx, :]
B2[0, 15, sub2_to_idx[(1,5)]] = 1; B2[1, 15, sub2_to_idx[(0,5)]] = -1
B2[0, 16, sub2_to_idx[(1,4)]] = 1; B2[1, 16, sub2_to_idx[(0,4)]] = -1
B2[2, 17, sub2_to_idx[(3,5)]] = 1; B2[3, 17, sub2_to_idx[(2,5)]] = -1
B2[2, 18, sub2_to_idx[(3,4)]] = 1; B2[3, 18, sub2_to_idx[(2,4)]] = -1
analyze_B2(B2, "B: Double Hilbert #55 (t_B=4)")

# Construction C: Overlapping Hilbert #55 on {0,1} and {0,2} (t_B = 4) -> s1 = 2, c = 7
B2 = np.zeros((6, 19, 15))
for ell, s_idx in enumerate(in_S):
    B2[:, ell, :] = B2_full[:, s_idx, :]
B2[0, 15, sub2_to_idx[(1,5)]] = 1; B2[1, 15, sub2_to_idx[(0,5)]] = -1
B2[0, 16, sub2_to_idx[(1,4)]] = 1; B2[1, 16, sub2_to_idx[(0,4)]] = -1
B2[0, 17, sub2_to_idx[(2,5)]] = 1; B2[2, 17, sub2_to_idx[(0,5)]] = -1
B2[0, 18, sub2_to_idx[(2,4)]] = 1; B2[2, 18, sub2_to_idx[(0,4)]] = -1
analyze_B2(B2, "C: Overlapping Hilbert #55 {0,1},{0,2} (t=4)")

# Construction D: Noether #58 Mixed Koszul (t_B = 4, r_i = b4 e_{i,5} + b5 e_{i,4}) -> s1 = 3, c = 4
B2 = np.zeros((6, 19, 15))
for ell, s_idx in enumerate(in_S):
    B2[:, ell, :] = B2_full[:, s_idx, :]
for i in range(4):
    B2[4, 15 + i, sub2_to_idx[(i,5)]] = 1
    B2[5, 15 + i, sub2_to_idx[(i,4)]] = 1
analyze_B2(B2, "D: Noether #58 Mixed Koszul (t_B=4)")

# Construction E: Hybrid — 2 Noether rows (w0, w1 on {4,5}) + 2 Hilbert-style rows for v_{2,4,5} (t_B = 4)
B2 = np.zeros((6, 19, 15))
for ell, s_idx in enumerate(in_S):
    B2[:, ell, :] = B2_full[:, s_idx, :]
B2[4, 15, sub2_to_idx[(0,5)]] = 1; B2[5, 15, sub2_to_idx[(0,4)]] = 1
B2[4, 16, sub2_to_idx[(1,5)]] = 1; B2[5, 16, sub2_to_idx[(1,4)]] = 1
B2[0, 17, sub2_to_idx[(2,5)]] = 1
B2[0, 18, sub2_to_idx[(2,4)]] = 1
analyze_B2(B2, "E: Hybrid 2-Noether + 2-Hilbert (t_B=4)")

# Construction F: TRY TO BREAK c <= 4 AT s_1 = 3!!
# WAIT A SECOND! Look at Construction D vs Construction E:
# In Construction E, w0 = b0 e_{4,5}, w1 = b1 e_{4,5} (on column {4,5}), and r3 = b0 e_{2,5}, r4 = b0 e_{2,4}.
# What if we ALSO make r3, r4 have a syzygy WITH EACH OTHER? No, r3 and r4 are on different columns {2,5} and {2,4}!
# What if we use a 2-VARIABLE codim-2 block on TWO columns {4,5} and {3,5}?
# Try: r1 = b4 e_{0,5} + b5 e_{0,4}, r2 = b4 e_{1,5} + b5 e_{1,4}, r3 = b4 e_{2,5} + b5 e_{2,4}, r4 = b_0 e_{3,5}?
B2 = np.zeros((6, 19, 15))
for ell, s_idx in enumerate(in_S):
    B2[:, ell, :] = B2_full[:, s_idx, :]
for i in range(3):
    B2[4, 15 + i, sub2_to_idx[(i,5)]] = 1
    B2[5, 15 + i, sub2_to_idx[(i,4)]] = 1
B2[0, 18, sub2_to_idx[(3,5)]] = 1
analyze_B2(B2, "F: 3-Noether + 1 extra (t_B=4)")

# Construction G: WHAT ABOUT USING A DEGREE-1 LINEAR COMBINATION OF B2_full ROWS THAT HAS ONLY 2 COLUMNS?
# Recall: by Diagonal alpha_S I_3 Submatrix Lemma, NO nonzero linear combination of B2_full rows has <= 2 columns (rank >= 3)!
# What about a canonical row v_{3,4,5} = b3 e_{4,5} + b4 e_{3,5} + b5 e_{3,4} + 3 protruding rows on {4,5},{3,5},{3,4}?
# Try: r1 = b0 e_{4,5}, r2 = b0 e_{3,5}, r3 = b0 e_{3,4}, r4 = b1 e_{4,5} (t_B = 4)
B2 = np.zeros((6, 19, 15))
in_S_g = [sub3_to_idx[(3,4,5)]] + [i for i in range(20) if i != sub3_to_idx[(3,4,5)]][:14]
for ell, s_idx in enumerate(in_S_g):
    B2[:, ell, :] = B2_full[:, s_idx, :]
B2[0, 15, sub2_to_idx[(4,5)]] = 1
B2[0, 16, sub2_to_idx[(3,5)]] = 1
B2[0, 17, sub2_to_idx[(3,4)]] = 1
B2[1, 18, sub2_to_idx[(4,5)]] = 1
analyze_B2(B2, "G: v_{345} + b0*(e45,e35,e34) + b1*e45 (t=4)")

# Construction H: WAIT A SECOND!! WHAT ABOUT ADDING b1 e_{4,5}, b2 e_{4,5}, b3 e_{4,5} AND ONE ROW THAT LINKS TO v_{3,4,5}?!
# Look at G: we had syz 1: b0 v_{345} - b3 r1 - b4 r2 - b5 r3 = 0, AND syz 2: b1 r1 - b0 r4 = 0!
# Now what if we add TWO rows on {4,5}: r1 = b0 e_{4,5}, r2 = b1 e_{4,5}, PLUS r3 = b0 e_{3,5}, r4 = b0 e_{3,4}? (That's G!)
# Wait: in G, #syz = 2, s1 = 2, c = 5!
# WHAT IF WE REPLACE r1 = b0 e_{4,5} BY A VECTOR THAT COUPLES WITH TWO DIFFERENT v_T's?!
# Try: r1 = b4 e_{0,5} + b5 e_{0,4}, r2 = b4 e_{1,5} + b5 e_{1,4}, r3 = b3 e_{0,5} + b5 e_{0,3}, r4 = b3 e_{1,5} + b5 e_{1,3}
# Wait: then:
#   w_{0,45} = v_{0,4,5} - r1 = b0 e_{4,5}
#   w_{1,45} = v_{1,4,5} - r2 = b1 e_{4,5}  --> syzygy 1 (on {4,5})
#   w_{0,35} = v_{0,3,5} - r3 = b0 e_{3,5}
#   w_{1,35} = v_{1,3,5} - r4 = b1 e_{3,5}  --> syzygy 2 (on {3,5})
# Still s1 = 2, c = 4!

# Construction I: TRY EAGON-NORTHCOTT / 3x2 RANK-2 MATRIX ON 2 COLUMNS!
# Suppose 4 protruding rows span:
#   r1 = b0 e_{4,5}, r2 = b1 e_{4,5}, r3 = b2 e_{4,5}, r4 = b0 e_{3,5} + b1 e_{4,5}? No, b1 e_{4,5} is already r2!
# Wait: WHAT ABOUT **ONE** SYZYGY INVOLVING r1..r4 AND **THREE** PURE KOSZUL SYZYGIES AMONG r1..r4?!
# HOLD EVERYTHING!! STOP!! TEST THIS RIGHT NOW!!
# Take r1 = b0 e_{4,5}, r2 = b1 e_{4,5}, r3 = b2 e_{4,5} (3 pure Koszul rows on {4,5} -> 3 syzygies, s = 2, c = 3)
# AND take r4 = b3 e_{4,5} + b4 e_{3,5} + b5 e_{3,4}?? No, that's v_{3,4,5} itself!
# Wait: what if we take:
#   r1 = b0 e_{4,5}
#   r2 = b1 e_{4,5}
#   r3 = b2 e_{4,5}
#   r4 = b3 e_{4,5}  (4 pure Koszul rows on {4,5}: s1 = 3, c = 4)
# AND ask: is there ANY 5th canonical row v_T that can couple to r1, r2, r3, r4 via a degree-1 syzygy?!
# Check:
B2 = np.zeros((6, 19, 15))
in_S_i = list(range(15))
for ell, s_idx in enumerate(in_S_i):
    B2[:, ell, :] = B2_full[:, s_idx, :]
for i in range(4):
    B2[i, 15 + i, sub2_to_idx[(4,5)]] = 1
analyze_B2(B2, "I: 4 pure Koszul on {4,5} (t_B=4)")

# Construction J: WHAT IF WE PUT THE 4 PURE KOSZUL ROWS ON {4,5} WITH VARIABLES b0, b1, b4, b5 (OVERLAPPING WITH v_{0,4,5} = b0 e_{4,5} + b4 e_{0,5} + b5 e_{0,4})?!
# Wait: v_{0,4,5} has e_{0,5} and e_{0,4}, not {4,5}!
# What if we put 4 protruding rows on {4,5} with b0, b1, b2, b3 AND include v_{0,4,5}..v_{3,4,5} in B2_in?
B2 = np.zeros((6, 19, 15))
for ell, s_idx in enumerate(in_S):
    B2[:, ell, :] = B2_full[:, s_idx, :]
for i in range(4):
    B2[i, 15 + i, sub2_to_idx[(4,5)]] = 1
analyze_B2(B2, "J: 4 pure Koszul + v_{0..3,4,5} in B2_in")

# Construction K: WAIT A SECOND!! WHAT ABOUT A **DEGREE-1 SYZYGY WITH s_1 = 3 AND c = 5** USING **ONE** CANONICAL ROW v_{0,1,2}?!
# Look at v_{0,1,2} = b0 e_{1,2} + b1 e_{0,2} + b2 e_{0,1} (3 entries on {1,2}, {0,2}, {0,1}!).
# Set the 4 protruding rows to:
#   r1 = b0 e_{1,2} + b1 e_{0,2}  (so v_{0,1,2} - r1 = b2 e_{0,1}!)
#   r2 = b3 e_{0,1}
#   r3 = b4 e_{0,1}
#   r4 = b5 e_{0,1}
# Still c = 4 (wires v_{0,1,2}-r1, r2, r3, r4)!
# WHAT IF WE INSTEAD SET:
#   r1 = b0 e_{1,2}
#   r2 = b1 e_{0,2}
#   r3 = b3 e_{0,1}
#   r4 = b4 e_{0,1}
# Look at w_0 := v_{0,1,2} - r1 - r2 = b2 e_{0,1}!
# Then w_0, r3, r4 are 3 rows on {0,1} -> s1 = 2, c = 3!
# AND WHAT ABOUT r1 = b0 e_{1,2} and r2 = b1 e_{0,2}? No extra syzygies!

# Construction L: WAIT A SECOND!! WHAT ABOUT **FIVE** LINEARLY INDEPENDENT ROWS IN B_2 THAT SHARE A **2-COLUMN** PROJECTION (i.e., K-rank 2)?
# Look at 4 protruding rows:
#   r1 = b0 e_{0,1} + b1 e_{0,2}
#   r2 = b1 e_{0,1} + b2 e_{0,2}
#   r3 = b2 e_{0,1} + b3 e_{0,2}
#   r4 = b3 e_{0,1} + b4 e_{0,2}
# Wait: that's a 4 x 2 Hankel/scroll matrix of linear forms!
# What is the degree-1 syzygy dim of a 4 x 2 scroll matrix?
# A 4 x 2 matrix of linear forms has K-rank 2, so its K-kernel has dim 4 - 2 = 2 (NOT 3)!
# Wait: what about a 3 x 2 matrix? K-kernel dim 3 - 2 = 1 (degree 2, not degree 1!).
# Wait: what about a **5 x 2** matrix? That needs 5 rows supported on 2 columns — IMPOSSIBLE because dim(rowsp(B2) cap M_2) <= t_B = 4!!
B2 = np.zeros((6, 19, 15))
for ell, s_idx in enumerate(in_S):
    B2[:, ell, :] = B2_full[:, s_idx, :]
B2[0, 15, 0] = 1; B2[1, 15, 1] = 1
B2[1, 16, 0] = 1; B2[2, 16, 1] = 1
B2[2, 17, 0] = 1; B2[3, 17, 1] = 1
B2[3, 18, 0] = 1; B2[4, 18, 1] = 1
analyze_B2(B2, "L: 4x2 Hankel scroll (t_B=4)")

# Construction M: WAIT A SECOND!! TRY A **2-VARIABLE** (b0, b1 ONLY!) 4-ROW BLOCK OF PROTRUDING ROWS!
# If all 4 protruding rows depend ONLY on (b0, b1) AND span a 2D column space (e.g. col 0 and col 1):
#   r1 = b0 e_0, r2 = b1 e_0, r3 = b0 e_1, r4 = b1 e_1 -> s1 = 2, c = 4.
# What if 4 protruding rows depend ONLY on (b0, b1) and lie on ONE column? Wait: only 2 independent linear forms in (b0, b1)!
# What if 4 protruding rows are b0 e_0, b1 e_0, b2 e_0, b3 e_0 -> s1 = 3, c = 4!
# NOW TRY: Can ANY 4 protruding rows + 1 canonical row have s1 = 3 AND c = 5?!
# WAIT A SECOND!! TEST THIS!!
# Take:
#   r1 = b0 e_{0,1}
#   r2 = b1 e_{0,1}
#   r3 = b2 e_{0,1}  (gives 3 syzygies on {r1, r2, r3}, s = 2, c = 3)
#   AND NOW try to get a 3rd syzygy with r4 AND a canonical row!
#   Remember: by Hyperplane Syzygy Rigidity, a single row r4 CANNOT create a deg-1 syzygy with B2_in alone!
#   Could a syzygy use r1, r2, r3, r4 AND B2_in?
#   YES!! TRY:
#     v_{0,1,2} = b0 e_{1,2} + b1 e_{0,2} + b2 e_{0,1}!
#     Suppose we have r1 = b0 e_{0,1}, r2 = b1 e_{0,1} (only 1 syzygy: b1 r1 - b0 r2 = 0),
#     and r3 = b0 e_{1,2} + b1 e_{0,2} (so v_{0,1,2} - r3 = b2 e_{0,1} -> now {r1, r2, v-r3} gives s = 2, c = 3!),
#     and r4 = ... still only 1 row left!
#   WHAT IF WE HAVE **2** CANONICAL ROWS v_{0,1,2} AND v_{0,1,3}?!
#   Look:
#     v_{0,1,2} = b2 e_{0,1} + b0 e_{1,2} + b1 e_{0,2}
#     v_{0,1,3} = b3 e_{0,1} + b0 e_{1,3} + b1 e_{0,3}
#     v_{0,1,4} = b4 e_{0,1} + b0 e_{1,4} + b1 e_{0,4}
#     v_{0,1,5} = b5 e_{0,1} + b0 e_{1,5} + b1 e_{0,5}
#   WAIT A SECOND!! LOOK AT WHAT HAPPENS IF WE TAKE:
#     r1 = b0 e_{1,2} + b1 e_{0,2}   (kills {1,2},{0,2} of v_{0,1,2} => w2 = v_{0,1,2} - r1 = b2 e_{0,1})
#     r2 = b0 e_{1,3} + b1 e_{0,3}   (kills {1,3},{0,3} of v_{0,1,3} => w3 = v_{0,1,3} - r2 = b3 e_{0,1})
#     r3 = b0 e_{1,4} + b1 e_{0,4}   (kills {1,4},{0,4} of v_{0,1,4} => w4 = v_{0,1,4} - r3 = b4 e_{0,1})
#     r4 = b0 e_{1,5} + b1 e_{0,5}   (kills {1,5},{0,5} of v_{0,1,5} => w5 = v_{0,1,5} - r4 = b5 e_{0,1})
#   That's Construction D (s1 = 3, c = 4)!
#   WAIT A SECOND!! WHAT IF WE KEEP r1, r2, r3, r4 AS **UNCOUPLED** COMPONENTS?!
#     r1 = b0 e_{1,2} + b1 e_{0,2}
#     r2 = b0 e_{1,3} + b1 e_{0,3}
#     r3 = b0 e_{1,4} + b1 e_{0,4}
#     r4 = b0 e_{1,5} + b1 e_{0,5}
#   Wait: in Construction D, the syzygies are ONLY among {w2, w3, w4, w5}, which is a 4D subspace!
#   Notice why c = 4 even though 8 original wires {v_{012}..v_{015}, r1..r4} were non-zero:
#   Because in the basis {w2, w3, w4, w5, r1, r2, r3, r4}, ALL syzygies vanish on r1..r4!
print("\n[DONE] Constructions A-L tested.")
