"""
Prof. Euler: test_swapped_tensor_projection.py
Investigate the projection of N_01(B_1 A_2) onto S_{6,3}^perp and its interaction with B_2 syzygies.
"""
import itertools
import numpy as np
import sys
sys.path.append('council/prof-noether')
from general_n2k_noether import build_Mn

def test_swapped_tensor():
    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    # V_basis is 90 x 20
    u_V, s_V, _ = np.linalg.svd(V_basis)
    V_orth = u_V[:, 20:] # 90 x 70
    
    rng = np.random.default_rng(2026)
    
    print("=== Testing Projection of N_01(B_1 A_2) onto S_{6,3}^perp ===")
    
    # Let B1(b) be 15 x 19 of rank s1 in {3, 4}
    # Let A2(a) be 19 x 15 of rank r2 in {3, 4}
    # What is the projection of N_01(B_1 A_2) on the right onto S_{6,3}^perp?
    # N_01 has size 90 x 90. The columns correspond to b in R^90.
    # The right projection onto S_{6,3}^perp is N_01 @ V_orth (size 90 x 70).
    
    for s1 in [3, 4]:
        for r2 in [3, 4]:
            ranks_proj = []
            for trial in range(20):
                # Random rank-s1 pencil B1(b) = U(b)_{15 x s1} C_{s1 x 19}
                U_B = rng.standard_normal((6, 15, s1))
                C_B = rng.standard_normal((s1, 19))
                # B1_tensor: shape (6, 15, 19)
                B1_tensor = np.einsum('cik,kl->cil', U_B, C_B)
                
                # Random rank-r2 pencil A2(a) = D_{19 x r2} V(a)_{r2 x 15}
                D_A = rng.standard_normal((19, r2))
                V_A = rng.standard_normal((6, r2, 15))
                # A2_tensor: shape (6, 19, 15)
                A2_tensor = np.einsum('lk,ckj->clj', D_A, V_A)
                
                # Compute N_01(B_1 A_2): shape (90, 90)
                # B1_tensor is (c2, I, ell) = (d, I, l)
                # A2_tensor is (c1, ell, J) = (c, l, J)
                # Target in N_01: row (I, c1), col (J, c2) -> (I, c, J, d)
                N01_BA = np.einsum('dIl,clJ->IcJd', B1_tensor, A2_tensor).reshape(90, 90)
                
                # Project onto S_{6,3}^perp on the right:
                proj_right = N01_BA @ V_orth # 90 x 70
                rk_proj = np.linalg.matrix_rank(proj_right, tol=1e-7)
                ranks_proj.append(rk_proj)
                
            print(f"s1={s1}, r2={r2}: rank(N_01(B1 A2) @ V_orth) in {set(ranks_proj)}")
            
    print("\nKey Observation:")
    print("For random pencils B1, A2, the right projection onto S_{6,3}^perp has rank min(s1*r2, 70) >> 4!")
    print("However, A_{1,out} B_{2,out} can have rank at most t_B <= 4!")
    print("Therefore, in order for A_{1,out} B_{2,out} to cancel N_01(B_1 A_2) outside S_{6,3},")
    print("B_1 and A_2 MUST be highly constrained so that rank(N_01(B1 A2) @ V_orth) <= t_B <= 4!")

if __name__ == '__main__':
    test_swapped_tensor()
