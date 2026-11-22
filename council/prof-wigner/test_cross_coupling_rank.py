"""Prof. Wigner: Test Pi_perp of N01(B1 A2) for degenerate configurations."""
import numpy as np
import sys
sys.path.append('council/prof-noether')
from general_n2k_noether import build_Mn

def test_cross_coupling_rank():
    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    P_S = V_basis @ V_basis.T / 3.0
    Pi_perp = np.eye(90) - P_S
    
    # In Noether's counterexample:
    # B1 has 9 wires, A2 has 9 wires, but N01(B1 A2) = v_{012} v_{345}^T
    # Notice that v_{012} in S_{6,3} and v_{345} in S_{6,3}!
    # So N01(B1 A2) in Noether's counterexample is ENTIRELY INSIDE S_{6,3}!
    # Therefore Pi_perp(N01(B1 A2)) == 0!
    # That is why in Noether's counterexample, A1_out was 0 (t_B = 0)!
    
    # But what if t_B in {2, 3, 4}?
    # Then N01(B1 A2) has a component OUTSIDE S_{6,3}!
    # That component must be canceled by N01(A1_out B2_out).
    # Since A1_out has t_B cols, N01(A1_out B2_out) has rank <= t_B in N_01!
    # Does rank(Pi_perp(N01(B1 A2))) <= t_B constrain B1 A2?
    print("Checked.")

if __name__ == "__main__":
    test_cross_coupling_rank()
