"""Prof. Wigner: Detailed analysis of the restriction of K(B, V) to Sym_0(4)."""
import numpy as np

def analyze_K_on_sym0():
    # Construct M and ON basis of Sym_0(4)
    # Sym_0(4) basis:
    # X1 = ((01)+(23))/2, X2 = ((02)+(13))/2, X3 = ((03)+(12))/2
    # Y1 = ((01)-(23))/2, Y2 = ((02)-(13))/2, Y3 = ((03)-(12))/2
    # Each is a 4x4 matrix
    def make_E(i, j):
        E = np.zeros((4, 4))
        E[i, j] = 1.0
        E[j, i] = 1.0
        return E

    X1 = (make_E(0, 1) + make_E(2, 3)) / np.sqrt(4.0)
    X2 = (make_E(0, 2) + make_E(1, 3)) / np.sqrt(4.0)
    X3 = (make_E(0, 3) + make_E(1, 2)) / np.sqrt(4.0)
    Y1 = (make_E(0, 1) - make_E(2, 3)) / np.sqrt(4.0)
    Y2 = (make_E(0, 2) - make_E(1, 3)) / np.sqrt(4.0)
    Y3 = (make_E(0, 3) - make_E(1, 2)) / np.sqrt(4.0)

    basis = [X1, X2, X3, Y1, Y2, Y3] # 6 orthonormal matrices in Sym_0(4)
    # Check orthonormality under Frobenius inner product: <A, B> = Tr(A^T B)
    G = np.array([[np.sum(A * B) for B in basis] for A in basis])
    assert np.allclose(G, np.eye(6))
    print("Orthonormal basis of Sym_0(4) verified.")

    # Matrix representation of M on this basis:
    # Recall M acting on S gives 2 * (matching complement) for X, -2 for Y
    # Let's verify M on basis:
    # M[(j0, c1), (j3, c2)] = 1 if {j0, c1, j3, c2} == {0, 1, 2, 3} else 0
    M = np.zeros((16, 16))
    for j0 in range(4):
        for c1 in range(4):
            for j3 in range(4):
                for c2 in range(4):
                    if len({j0, c1, j3, c2}) == 4:
                        M[j0 * 4 + c1, j3 * 4 + c2] = 1.0

    basis_vecs = np.stack([b.reshape(16) for b in basis], axis=1) # 16 x 6
    M_sym0 = basis_vecs.T @ M @ basis_vecs
    print("M restricted to Sym_0(4):\n", np.round(M_sym0, 4))

    # Now, for any K(B, V), K_sym0 = basis_vecs.T @ K(B, V) @ basis_vecs
    # Recall: each wire in (3,2) has rank(B) = rank(V) = 1 in the wire-split formulation!
    # Wait! In wire-split (3,2):
    # B1(b) is 4x2 linear in b. For each of the 2 wires ell in {1, 2}:
    # B_ell is 4x1 in b, A_{2, ell} is 1x4 in a.
    # What are the ranks of B_ell and V_ell as 4x4 matrices?
    # B_ell has entries B[j0, c2].
    # Can B_ell and V_ell have rank up to 4, or are they rank 1?
    # In general, B_ell(b) = B_ell @ b, so B_ell is a 4x4 matrix!
    # It can have rank up to 4!
    # BUT: K(B, V) on Sym_0(4):
    # What is the maximum rank of K(B, V)|_{Sym_0(4)}?
    rng = np.random.default_rng(42)
    max_rk_1 = 0
    max_rk_2 = 0
    for _ in range(500):
        B = rng.standard_normal((4, 4))
        V = rng.standard_normal((4, 4))
        K = np.einsum("ac,db->abdc", B, V).reshape(16, 16)
        K_sym = basis_vecs.T @ K @ basis_vecs
        rk1 = np.linalg.matrix_rank(K_sym, tol=1e-7)
        max_rk_1 = max(max_rk_1, rk1)

        B2 = rng.standard_normal((4, 4))
        V2 = rng.standard_normal((4, 4))
        K2 = np.einsum("ac,db->abdc", B2, V2).reshape(16, 16)
        K_sym2 = basis_vecs.T @ (K + K2) @ basis_vecs
        rk2 = np.linalg.matrix_rank(K_sym2, tol=1e-7)
        max_rk_2 = max(max_rk_2, rk2)

    print(f"Max rank of single K(B,V) on Sym_0(4): {max_rk_1}")
    print(f"Max rank of K1 + K2 on Sym_0(4): {max_rk_2}")

    # Now let's check: can M_sym0 - (K1 + K2)_sym0 have rank <= 3?
    # Test random and optimized:
    min_rk_diff = 6
    for _ in range(5000):
        B1 = rng.standard_normal((4, 4))
        V1 = rng.standard_normal((4, 4))
        B2 = rng.standard_normal((4, 4))
        V2 = rng.standard_normal((4, 4))
        K1 = np.einsum("ac,db->abdc", B1, V1).reshape(16, 16)
        K2 = np.einsum("ac,db->abdc", B2, V2).reshape(16, 16)
        diff_sym = M_sym0 - basis_vecs.T @ (K1 + K2) @ basis_vecs
        rk = np.linalg.matrix_rank(diff_sym, tol=1e-7)
        if rk < min_rk_diff:
            min_rk_diff = rk
    print(f"Min rank of M_sym0 - (K1 + K2)_sym0 over 5000 random samples: {min_rk_diff}")

if __name__ == "__main__":
    analyze_K_on_sym0()
