"""Prof. Wigner: Analysis of Gauge Freedom, Physical DOF, and LM Landscaping."""
import numpy as np
import itertools
from typing import Tuple, List

# Define target P_perm(a, b)
# P(a,b)_{j0, j3} = 0 if j0 == j3 else a_{c1} b_{c2} + a_{c2} b_{c1} where {j0, c1, j3, c2} = {0, 1, 2, 3}
def build_target_P() -> np.ndarray:
    # Target tensor of shape (4, 4, 4, 4): P[j0, j3, c1, c2] = coeff of a_{c1} b_{c2} in P_{j0, j3}
    P = np.zeros((4, 4, 4, 4), dtype=np.float64)
    for j0 in range(4):
        for j3 in range(4):
            if j0 == j3:
                continue
            rem = [c for c in range(4) if c != j0 and c != j3]
            c1, c2 = rem[0], rem[1]
            P[j0, j3, c1, c2] += 1.0
            P[j0, j3, c2, c1] += 1.0
    return P

def test_split_jacobian():
    # Parameters for Case (3,2):
    # A1: (4, 3, 4) -> j0, wire_a, c1
    # B2: (3, 4, 4) -> wire_a, j3, c2
    # B1: (4, 2, 4) -> j0, wire_b, c2
    # A2: (2, 4, 4) -> wire_b, j3, c1
    # Residual:
    # Term 1: A1[j0, w, c1] * B2[w, j3, c2] -> sum over w in 0..2
    # Term 2: B1[j0, w, c2] * A2[w, j3, c1] -> sum over w in 0..1
    # Model: P_pred[j0, j3, c1, c2] = sum_w A1[j0, w, c1]*B2[w, j3, c2] + sum_w B1[j0, w, c2]*A2[w, j3, c1]
    
    rng = np.random.default_rng(42)
    # Generic random point
    A1 = rng.standard_normal((4, 3, 4))
    B2 = rng.standard_normal((3, 4, 4))
    B1 = rng.standard_normal((4, 2, 4))
    A2 = rng.standard_normal((2, 4, 4))
    
    # Let's vectorize theta:
    # theta has size 4*3*4 + 3*4*4 + 4*2*4 + 2*4*4 = 48 + 48 + 32 + 32 = 160
    # Let's compute Jacobian of map: R^160 -> R^256
    
    def forward(A1, B2, B1, A2):
        term1 = np.einsum("jwc,wkf->jkcf", A1, B2) # (4, 4, 4, 4)
        term2 = np.einsum("jwf,wkc->jkcf", B1, A2) # (4, 4, 4, 4)
        return term1 + term2

    P_pred = forward(A1, B2, B1, A2)
    
    # Jacobian analytically:
    # d(term1)/dA1: delta_{j, j0} * delta_{w, wa} * delta_{c, c1} * B2[wa, j3, c2]
    # shape: (4, 4, 4, 4, 4, 3, 4) -> (256, 48)
    J_A1 = np.zeros((4, 4, 4, 4, 4, 3, 4))
    for j0 in range(4):
        for c1 in range(4):
            for wa in range(3):
                J_A1[j0, :, c1, :, j0, wa, c1] += B2[wa, :, :]
                
    # d(term1)/dB2: A1[j0, wa, c1] * delta_{w, wa} * delta_{k, j3} * delta_{f, c2}
    # shape: (4, 4, 4, 4, 3, 4, 4) -> (256, 48)
    J_B2 = np.zeros((4, 4, 4, 4, 3, 4, 4))
    for j3 in range(4):
        for c2 in range(4):
            for wa in range(3):
                J_B2[:, j3, :, c2, wa, j3, c2] += A1[:, wa, :]
                
    # d(term2)/dB1: delta_{j, j0} * delta_{w, wb} * delta_{f, c2} * A2[wb, j3, c1]
    # shape: (4, 4, 4, 4, 4, 2, 4) -> (256, 32)
    J_B1 = np.zeros((4, 4, 4, 4, 4, 2, 4))
    for j0 in range(4):
        for c2 in range(4):
            for wb in range(2):
                J_B1[j0, :, :, c2, j0, wb, c2] += A2[wb, :, :]
                
    # d(term2)/dA2: B1[j0, wb, c2] * delta_{w, wb} * delta_{k, j3} * delta_{c, c1}
    # shape: (4, 4, 4, 4, 2, 4, 4) -> (256, 32)
    J_A2 = np.zeros((4, 4, 4, 4, 2, 4, 4))
    for j3 in range(4):
        for c1 in range(4):
            for wb in range(2):
                J_A2[:, j3, c1, :, wb, j3, c1] += B1[:, wb, :]
                
    J = np.concatenate([
        J_A1.reshape(256, 48),
        J_B2.reshape(256, 48),
        J_B1.reshape(256, 32),
        J_A2.reshape(256, 32)
    ], axis=1)
    
    rk = np.linalg.matrix_rank(J, tol=1e-8)
    print(f"Case (3,2): Total vars = 160, Equations = 256")
    print(f"Jacobian rank at generic point = {rk}")
    print(f"Dimension of gauge orbit (160 - {rk}) = {160 - rk}")
    
    # Check gauge generators explicitly
    # GL(3) acts on wire_a: A1 -> A1 @ G_A, B2 -> G_A^{-1} @ B2
    # infinitesimal generator: X in gl(3): delta A1 = A1 @ X, delta B2 = - X @ B2
    # There are 9 generators.
    # GL(2) acts on wire_b: B1 -> B1 @ G_B, A2 -> G_B^{-1} @ A2
    # infinitesimal generator: Y in gl(2): delta B1 = B1 @ Y, delta A2 = - Y @ A2
    # There are 4 generators.
    # Total gauge dimension = 9 + 4 = 13.
    # Let's test if all 13 gauge variations are in ker(J):
    gauge_vectors = []
    # gl(3):
    for u in range(3):
        for v in range(3):
            # X_uv: (X)_{ij} = delta_{i,u} delta_{j,v}
            # dA1 = A1 @ X_uv => (dA1)_{j, v, c} = A1_{j, u, c}
            dA1 = np.zeros_like(A1)
            dA1[:, v, :] = A1[:, u, :]
            # dB2 = - X_uv @ B2 => (dB2)_{u, k, f} = - B2_{v, k, f}
            dB2 = np.zeros_like(B2)
            dB2[u, :, :] = - B2[v, :, :]
            v_vec = np.concatenate([dA1.reshape(48), dB2.reshape(48), np.zeros(32), np.zeros(32)])
            gauge_vectors.append(v_vec)
    # gl(2):
    for u in range(2):
        for v in range(2):
            dB1 = np.zeros_like(B1)
            dB1[:, v, :] = B1[:, u, :]
            dA2 = np.zeros_like(A2)
            dA2[u, :, :] = - A2[v, :, :]
            v_vec = np.concatenate([np.zeros(48), np.zeros(48), dB1.reshape(32), dA2.reshape(32)])
            gauge_vectors.append(v_vec)
            
    gauge_mat = np.stack(gauge_vectors, axis=1) # (160, 13)
    rk_gauge = np.linalg.matrix_rank(gauge_mat)
    j_gauge = J @ gauge_mat
    max_gauge_err = np.max(np.abs(j_gauge))
    print(f"Gauge group gl(3) x gl(2) rank = {rk_gauge} (expected 13)")
    print(f"Max residual of J * gauge_vectors = {max_gauge_err:.2e}")
    assert max_gauge_err < 1e-10
    assert rk == 160 - 13, f"Unexpected rank: {rk} != 147"
    print("CONFIRMED: The gauge group is EXACTLY GL_3 x GL_2 of dimension 13.")
    print("The physical tangent space has dimension exactly 147.")
    print("The codim in equation space R^256 is 256 - 147 = 109.")

if __name__ == "__main__":
    test_split_jacobian()
