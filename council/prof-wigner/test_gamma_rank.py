"""Prof. Wigner: Test rank of (Gamma otimes I_6) M_6 for 11 x 15 matrix Gamma."""
import numpy as np
import sys
sys.path.append('council/prof-noether')
from general_n2k_noether import build_Mn

def test_gamma_rank():
    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    print(f"M6 shape: {M6.shape}, rank: {np.linalg.matrix_rank(M6)}")
    
    # Gamma is 11 x 15 (corank 4)
    # (Gamma otimes I_6) has shape (11*6, 15*6) = (66, 90)
    rng = np.random.default_rng(2026)
    
    min_rk = 90
    for trial in range(50):
        # Random full-rank 11 x 15 matrix Gamma
        Gamma = rng.standard_normal((11, 15))
        op = np.kron(Gamma, np.eye(6)) # 66 x 90
        prod = op @ M6 # 66 x 90
        rk = np.linalg.matrix_rank(prod, tol=1e-7)
        if rk < min_rk:
            min_rk = rk
            
    print(f"Random 11 x 15 Gamma: min rank((Gamma otimes I_6) M6) = {min_rk} (out of 20)")
    
    # What about worst-case adversarial coordinate projections of size 11 x 15?
    # Drop 4 rows of size 15: C(15, 4) = 1365 combinations!
    import itertools
    min_adv_rk = 90
    for drop_rows in itertools.islice(itertools.combinations(range(15), 4), 200):
        keep_rows = [i for i in range(15) if i not in drop_rows]
        Gamma_coord = np.zeros((11, 15))
        for r, row_idx in enumerate(keep_rows):
            Gamma_coord[r, row_idx] = 1.0
        op = np.kron(Gamma_coord, np.eye(6))
        rk = np.linalg.matrix_rank(op @ M6, tol=1e-7)
        if rk < min_adv_rk:
            min_adv_rk = rk
            
    print(f"Adversarial 11 x 15 coordinate drops: min rank = {min_adv_rk}")

if __name__ == "__main__":
    test_gamma_rank()
