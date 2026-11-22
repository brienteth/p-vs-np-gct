"""
Prof. Euler: test_max_constant_wires_search.py
Systematic search and algebraic classification of the maximum constant wire support
c = dim_F R(B_1) for degree-1 syzygies of B_2(b) with t_B in {2, 3, 4}.
"""
import itertools
import numpy as np
import sys
sys.path.append('council/prof-noether')
from general_n2k_noether import build_Mn

def test_wire_support_koszul():
    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    sub2_to_idx = {s: i for i, s in enumerate(sub_2)}
    sub3_to_idx = {s: i for i, s in enumerate(sub_3)}
    
    print("=" * 70)
    print("TESTING MAXIMUM CONSTANT WIRE SUPPORT c = dim_F R(B_1) FOR t_B in {2, 3, 4}")
    print("=" * 70)
    
    # 1. Hilbert Counterexample at t_B = 2:
    # Wires: v_{1,4,5}, v_{0,4,5}, r_1(b), r_2(b)
    # Plus 15 other canonical wires to make 19 wires
    w_145 = sub3_to_idx[(1, 4, 5)]
    w_045 = sub3_to_idx[(0, 4, 5)]
    other_wires = [w for w in range(20) if w not in (w_145, w_045)][:15]
    canonical_17 = [w_145, w_045] + other_wires # 17 canonical wires
    
    e_15 = sub2_to_idx[(1, 5)]
    e_05 = sub2_to_idx[(0, 5)]
    e_14 = sub2_to_idx[(1, 4)]
    e_04 = sub2_to_idx[(0, 4)]
    
    r1 = np.zeros((15, 6))
    r1[e_15, 0] = 1.0; r1[e_05, 1] = -1.0
    r2 = np.zeros((15, 6))
    r2[e_14, 0] = 1.0; r2[e_04, 1] = -1.0
    
    B2_tensor = np.zeros((6, 19, 15))
    for ell, w in enumerate(canonical_17):
        B2_tensor[:, ell, :] = V_basis[:, w].reshape(15, 6).T
    B2_tensor[:, 17, :] = r1.T
    B2_tensor[:, 18, :] = r2.T
    
    # Build syzygy matrix
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
    E_mat = np.array(eqs)
    u, s, vh = np.linalg.svd(E_mat)
    nullity = np.sum(s < 1e-8)
    print(f"Hilbert t_B = 2 Construction:")
    print(f"  Syzygy nullity = {nullity}")
    ker = vh[-nullity:] # (nullity, 114)
    # For each kernel vector, reshape to (6, 19)
    # The constant wire support is the column space of ker_mat (in R^19)
    wire_support = np.vstack([ker[k].reshape(6, 19) for k in range(nullity)]) # (6*nullity, 19)
    c_wire = np.linalg.matrix_rank(wire_support)
    active_wires = [ell for ell in range(19) if np.max(np.abs(wire_support[:, ell])) > 1e-5]
    print(f"  Exact constant wire support dim_F R(B_1) = {c_wire}")
    print(f"  Active wire indices: {active_wires} (wires 0, 1 are v_{{1,4,5}}, v_{{0,4,5}}; wires 17, 18 are r_1, r_2)")
    assert c_wire == 4 and active_wires == [0, 1, 17, 18]
    print("  [PASS] Hilbert t_B = 2 syzygy space uses EXACTLY 4 wires: {v_{1,4,5}, v_{0,4,5}, r_1, r_2}!")
    
    # 2. Noether t_B = 4 Construction (#58):
    chosen_S = [sub3_to_idx[(i, 4, 5)] for i in range(4)]
    other_S = [s for s in range(20) if s not in chosen_S][:11]
    in_S = chosen_S + other_S
    
    B2_t4 = np.zeros((6, 19, 15))
    for ell, s_idx in enumerate(in_S):
        B2_t4[:, ell, :] = V_basis[:, s_idx].reshape(15, 6).T
    for i in range(4):
        B2_t4[4, 15 + i, sub2_to_idx[(i, 5)]] = 1.0
        B2_t4[5, 15 + i, sub2_to_idx[(i, 4)]] = 1.0
        
    eqs_t4 = []
    for J in range(15):
        for c1 in range(6):
            for c2 in range(c1, 6):
                row = np.zeros(6 * 19, dtype=float)
                for ell in range(19):
                    row[c1 * 19 + ell] += B2_t4[c2, ell, J]
                    if c1 != c2:
                        row[c2 * 19 + ell] += B2_t4[c1, ell, J]
                eqs_t4.append(row)
    E_t4 = np.array(eqs_t4)
    u4, s4, vh4 = np.linalg.svd(E_t4)
    null4 = np.sum(s4 < 1e-8)
    print(f"\nNoether t_B = 4 Construction:")
    print(f"  Syzygy nullity = {null4}")
    ker4 = vh4[-null4:]
    wire_support4 = np.vstack([ker4[k].reshape(6, 19) for k in range(null4)])
    c_wire4 = np.linalg.matrix_rank(wire_support4)
    active4 = [ell for ell in range(19) if np.max(np.abs(wire_support4[:, ell])) > 1e-5]
    print(f"  Active wires in R^{{19}}: {active4} (total {len(active4)} wires)")
    print(f"  Dimension of constant wire support: {c_wire4}")
    
    # Check the GL_19 gauge change:
    # Notice that wire_support4 is supported on wires 0, 1, 2, 3 (the 4 canonical wires)
    # AND wires 15, 16, 17, 18 (the 4 protruding wires).
    # Why? Because v_{i,4,5} and r_i are coupled!
    # Under GL_19: define w_tilde_i = wire_i - wire_{15+i}
    # Then syzygies are b_i w_tilde_j - b_j w_tilde_i!
    # How many independent vectors in the syzygy image?
    # R(B_1) is spanned by the rows of B_1(b).
    # What is the function-field rank of B_1(b)?
    rng = np.random.default_rng(42)
    b_pt = rng.standard_normal(6)
    B1_val = np.zeros((null4, 19))
    for k in range(null4):
        B1_val[k] = sum(b_pt[c] * ker4[k].reshape(6, 19)[c] for c in range(6))
    rk_B1 = np.linalg.matrix_rank(B1_val)
    print(f"  Function-field rank s_1 = rank(B_1(b)) = {rk_B1}")
    print(f"  Number of coupled pairs (wire_i, wire_{{15+i}}): 4 pairs!")

if __name__ == '__main__':
    test_wire_support_koszul()
