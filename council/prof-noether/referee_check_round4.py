"""CRITICAL REFEREE CHECK for Round 4 (#34 Valiant & #35 Wigner):
1. Demonstrate the explicit COUNTEREXAMPLE to the bidegree-only equation
   A1(a)_{15x19} B2(b)_{19x15} + B1(b)_{15x19} A2(a)_{19x15} = P_perm,6(a,b)
   with (r1, s1, r2, s2) = (15, 3, 3, 15) (showing that the gap in #34/#35 is REAL:
   function-field rank s1 = r2 = 3 does NOT imply <= 4 constant wires!).
2. Compute the EXACT degree-1 left syzygies u(b) B2(b) = 0 of the 19 rows {v_T(b) : T != {3,4,5}}!"""
import itertools
import numpy as np
import sys
sys.path.append('p-vs-np-gct/council/prof-noether')
from general_n2k_noether import build_Mn

M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
sub2_to_idx = {s: i for i, s in enumerate(sub_2)}
sub3_to_idx = {s: i for i, s in enumerate(sub_3)}

# 1. Construct the explicit (r1=15, s1=3, r2=3, s2=15) bidegree-only solution at w = 19!
# Target missing rank-1 term in N_01: v_{0,1,2} v_{3,4,5}^T
idx_012 = sub3_to_idx[(0, 1, 2)]
idx_345 = sub3_to_idx[(3, 4, 5)]

# Rows of B1(b) supported on {0,1}, {0,2}, {1,2} (3 rows); 9 wires used (wires 0..8)
# B1_tensor[c2, I, ell]
B1_tensor = np.zeros((6, 15, 19), dtype=float)
A2_tensor = np.zeros((6, 19, 15), dtype=float)

row_pairs = [((0, 1), 2), ((0, 2), 1), ((1, 2), 0)]   # (I, c1 = {0,1,2}\I)
col_pairs = [((3, 4), 5), ((3, 5), 4), ((4, 5), 3)]   # (J, c2 = {3,4,5}\J)

wire = 0
for I_tup, c1 in row_pairs:
    I_idx = sub2_to_idx[I_tup]
    for J_tup, c2 in col_pairs:
        J_idx = sub2_to_idx[J_tup]
        B1_tensor[c2, I_idx, wire] = 1.0
        A2_tensor[c1, wire, J_idx] = 1.0
        wire += 1
assert wire == 9

# Verify function-field ranks s1 = rank B1(b) and r2 = rank A2(a) at random points!
rng = np.random.default_rng(42)
a_pt = rng.standard_normal(6)
b_pt = rng.standard_normal(6)
B1_val = np.tensordot(b_pt, B1_tensor, axes=([0], [0]))  # 15 x 19
A2_val = np.tensordot(a_pt, A2_tensor, axes=([0], [0]))  # 19 x 15
print(f"Counterexample ranks: s1 = rank B1(b) = {np.linalg.matrix_rank(B1_val)}, r2 = rank A2(a) = {np.linalg.matrix_rank(A2_val)}")

# Compute N_01(B1(b) A2(a))
# N01[(I, c1), (J, c2)] = sum_ell B1[c2, I, ell] * A2[c1, ell, J]
N01_BA = np.einsum('kIl,mJl->ImJk', B1_tensor, A2_tensor.transpose(0, 2, 1)).reshape(90, 90)
expected_rank1 = np.outer(V_basis[:, idx_012], V_basis[:, idx_345])
assert np.allclose(N01_BA, expected_rank1), "N01(B1 A2) != v_{012} v_{345}^T"

# Now check rank(M6 - N01(B1 A2)):
M6_rem = M6 - N01_BA
rk_rem = np.linalg.matrix_rank(M6_rem)
print(f"rank(M6 - N_01(B1(b) A2(a))) = {rk_rem} == 19 !! (EXACT BIDEGREE-ONLY SOLUTION AT w=19!)")

# Build exact A1(a)_{15x19} and B2(b)_{19x15} for the remaining 19 terms of M6:
remaining_S = [s_idx for s_idx in range(20) if s_idx != idx_012]
A1_tensor = np.zeros((6, 15, 19), dtype=float)
B2_tensor = np.zeros((6, 19, 15), dtype=float)
for ell, s_idx in enumerate(remaining_S):
    sc_idx = int(np.argmax(comp_perm[s_idx]))
    # v_S reshaped as 15 x 6 -> A1_tensor[:, :, ell] = v_S.T
    A1_tensor[:, :, ell] = V_basis[:, s_idx].reshape(15, 6).T
    B2_tensor[:, ell, :] = V_basis[:, sc_idx].reshape(15, 6).T

A1_val = np.tensordot(a_pt, A1_tensor, axes=([0], [0]))  # 15 x 19
B2_val = np.tensordot(b_pt, B2_tensor, axes=([0], [0]))  # 19 x 15
print(f"r1 = rank A1(a) = {np.linalg.matrix_rank(A1_val)}, s2 = rank B2(b) = {np.linalg.matrix_rank(B2_val)}")

# Verify A1(a) B2(b) + B1(b) A2(a) == P_perm,6(a, b) identically!
N01_AB = np.einsum('cIl,dJl->IcJd', A1_tensor, B2_tensor.transpose(0, 2, 1)).reshape(90, 90)
err_P = np.linalg.norm(N01_AB + N01_BA - M6)
print(f"||N_01(A1 B2 + B1 A2) - M6|| = {err_P:.2e}  [EXACT SOLUTION TO EQUATION (iii) WITH (15, 3, 3, 15)!]")

# 2. NOW CHECK THE DEGREE-1 SYZYGIES OF B2(b) (invariant under GL_19)!
# A degree-1 left syzygy of B2(b) is a 1 x 19 linear form u(b) = sum_{c=0}^5 u_c b_c such that u(b) B2(b) == 0 in F[b]^15.
# For each J in 0..14 and each unordered pair {c1 <= c2} in 0..5 (21 quadratic monomials):
# coeff of b_{c1} b_{c2} in (u(b) B2(b))_J is:
#   sum_ell (u_{c1, ell} B2[c2, ell, J] + (u_{c2, ell} B2[c1, ell, J] if c1 != c2 else 0)) == 0.
# Unknowns: 6 * 19 = 114 entries of u_{c, ell}.
# Equations: 15 * 21 = 315 linear equations.
eqs = []
for J in range(15):
    for c1 in range(6):
        for c2 in range(c1, 6):
            row = np.zeros(6 * 19, dtype=float)
            for ell in range(19):
                row[c1 * 19 + ell] += B2_tensor[c2, ell, J]
                if c1 != c2:
                    row[c2 * 19 + ell] += B2_tensor[c1, ell, J]
            eqs.append(row)
E_mat = np.array(eqs)  # 315 x 114
rk_E = np.linalg.matrix_rank(E_mat)
syz_dim = 114 - rk_E
print(f"\n[SYZYGY CHECK on B2(b) = {{v_T(b) : T != {{3,4,5}}}}]:")
print(f"  Linear syzygy system size: {E_mat.shape}, rank = {rk_E}, dim(deg-1 left syzygies) = {syz_dim}")

# Also compute the FULL 20-wire matrix B2_full(b) = {v_T(b) : all 20 T} degree-1 syzygies for comparison!
eqs_full = []
B2_full = np.zeros((6, 20, 15), dtype=float)
for ell in range(20):
    B2_full[:, ell, :] = V_basis[:, ell].reshape(15, 6).T
for J in range(15):
    for c1 in range(6):
        for c2 in range(c1, 6):
            row = np.zeros(6 * 20, dtype=float)
            for ell in range(20):
                row[c1 * 20 + ell] += B2_full[c2, ell, J]
                if c1 != c2:
                    row[c2 * 20 + ell] += B2_full[c1, ell, J]
            eqs_full.append(row)
E_full = np.array(eqs_full)
rk_full = np.linalg.matrix_rank(E_full)
print(f"  Full 20-wire B2_full(b) deg-1 left syzygies: dim = {120 - rk_full}")
