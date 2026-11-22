"""Prof. Wigner: Dimension of Sym_0(4) cap im(K1 + K2)."""
import numpy as np
import itertools

def test_intersection_dim():
    # Basis of Sym_0(4)
    cols = []
    for i in range(4):
        for j in range(i + 1, 4):
            e = np.zeros((4, 4))
            e[i, j] = 1.0
            e[j, i] = 1.0
            cols.append(e.reshape(16))
    S0 = np.stack(cols, axis=1) # 16 x 6

    rng = np.random.default_rng(2026)
    
    # Test random full-rank B1, V1, B2, V2
    max_inter_dim = 0
    for trial in range(500):
        B1 = rng.standard_normal((4, 4))
        V1 = rng.standard_normal((4, 4))
        B2 = rng.standard_normal((4, 4))
        V2 = rng.standard_normal((4, 4))
        
        # Basis of im(K1 + K2)
        # im(K(B,V)) is spanned by B[:, c2] otimes V[j3, :] for all c2, j3
        # That's B @ E_{c2, j3} @ V
        im1 = np.stack([ (B1[:, [c]] @ V1[[j], :]).reshape(16) for c in range(4) for j in range(4) ], axis=1)
        im2 = np.stack([ (B2[:, [c]] @ V2[[j], :]).reshape(16) for c in range(4) for j in range(4) ], axis=1)
        
        # Wait, if B and V are invertible 4x4, then im(K(B, V)) is the ENTIRE space C^16!
        # Because invertible B and V span all of C^4 otimes C^4!
        # Wait! If B and V are invertible, then im(K) = C^16, so Sym_0(4) cap im(K) = Sym_0(4) (dim 6)!
        pass

    # Wait! Can B and V be invertible in Case (3,2)?
    # Let's check!
    # In Case (3,2):
    # A1 is 4x3 (in a), B2 is 3x4 (in b)
    # B1 is 4x2 (in b), A2 is 2x4 (in a)
    # The 2 wires are:
    # wire 1: B_{1, :, 0}(b) * A_{2, 0, :}(a)
    # wire 2: B_{1, :, 1}(b) * A_{2, 1, :}(a)
    # Here, for each wire ell in {0, 1}:
    # B_{1, :, ell}(b) is a 4-vector linear in b!
    # So B_ell is a 4x4 matrix: B_ell[j0, c2]
    # A_{2, ell, :}(a) is a 4-vector linear in a!
    # So V_ell is a 4x4 matrix: V_ell[j3, c1]
    # YES! B_ell and V_ell CAN be 4x4 matrices of rank up to 4!
    print("Checked.")

if __name__ == "__main__":
    test_intersection_dim()
