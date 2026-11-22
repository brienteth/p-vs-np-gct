"""Prof. Wigner: Test whether Pi_perp(N_01(B1 A2)) can be canceled by t_B <= 4 wires."""
import numpy as np
import itertools
import sys
sys.path.append('council/prof-noether')
from general_n2k_noether import build_Mn

def test_cross_coupling_cancellation():
    print("=" * 70)
    print("PROF. WIGNER: CROSS-COUPLING PROJECTION RANK FOR DEGENERATE U")
    print("=" * 70)

    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    P_S = V_basis @ V_basis.T / 3.0
    Pi_perp = np.eye(90) - P_S
    
    # Let U be a coordinate subspace of dimension 6 where delta(U) = 4 >= 3.
    # U is spanned by 6 subsets of size 2.
    # For example, all 6 subsets of a 4-element set {0, 1, 2, 3}: C(4, 2) = 6 subsets!
    sub_4 = [s for s in sub_2 if set(s).issubset({0, 1, 2, 3})]
    assert len(sub_4) == 6
    sub2_to_idx = {s: i for i, s in enumerate(sub_2)}
    U_indices = [sub2_to_idx[s] for s in sub_4]
    
    # Basis of U in C^15:
    U_basis = np.zeros((15, 6))
    for r, idx in enumerate(U_indices):
        U_basis[idx, r] = 1.0
        
    U_kron = np.kron(U_basis, np.eye(6))
    rk_joint = np.linalg.matrix_rank(np.hstack([V_basis, U_kron]), tol=1e-7)
    delta_U = 20 + 36 - rk_joint
    print(f"Verified degenerate U (all subsets of {0,1,2,3}): dim U = 6, delta(U) = {delta_U}")
    assert delta_U == 4
    
    # In this degenerate U, B1(b) has rows supported on U_indices (dim s1 <= 4).
    # A2(a) has cols supported on some V_indices (dim r2 <= 4).
    # For random choices of B1 supported on U and A2:
    rng = np.random.default_rng(42)
    min_perp_rank = 90
    for trial in range(50):
        # B1_tensor: (6, 15, 9) supported on U_indices
        B1_tensor = np.zeros((6, 15, 9))
        for c in range(6):
            B1_tensor[c, U_indices, :] = rng.standard_normal((6, 9))
            
        # A2_tensor: (6, 9, 15)
        A2_tensor = np.zeros((6, 9, 15))
        for c in range(6):
            A2_tensor[c, :, :] = rng.standard_normal((9, 15))
            
        N01_BA = np.einsum('kIl,mJl->ImJk', B1_tensor, A2_tensor.transpose(0, 2, 1)).reshape(90, 90)
        
        # Project outside S_{6,3}:
        perp_BA = Pi_perp @ N01_BA
        rk_perp = np.linalg.matrix_rank(perp_BA, tol=1e-7)
        if rk_perp < min_perp_rank:
            min_perp_rank = rk_perp
            
    print(f"Minimum rank of Pi_perp(N_01(B1 A2)) = {min_perp_rank}")
    print(f"Can it be canceled by A1_out B2_out of rank t_B <= 4? {min_perp_rank <= 4}")
    
    print("=" * 70)

if __name__ == "__main__":
    test_cross_coupling_cancellation()
