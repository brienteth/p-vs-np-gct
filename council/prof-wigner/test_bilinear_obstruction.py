"""Prof. Wigner: Testing the (u, W) bilinear obstruction for Case (3,2).
Can there exist a nonzero u in C^4 and a 2-dimensional subspace W in C^4 such that
for all v in W, and all c2 in {0,1,2,3}:
sum_{j0, c1, j3} u_{j0} a_{c1} v_{j3} M_{(j0, c1), (j3, c2)} = 0 ?
"""
import numpy as np

def test_bilinear_obstruction():
    # Build M: 16x16 matrix M[(j0, c1), (j3, c2)] = 1 if {j0, c1, j3, c2} == {0, 1, 2, 3} else 0
    M = np.zeros((4, 4, 4, 4), dtype=np.float64) # (j0, c1, j3, c2)
    for j0 in range(4):
        for c1 in range(4):
            for j3 in range(4):
                for c2 in range(4):
                    if len({j0, c1, j3, c2}) == 4:
                        M[j0, c1, j3, c2] = 1.0

    # Fix a generic a in R^4
    rng = np.random.default_rng(2026)
    a = rng.standard_normal(4)
    print(f"Testing for generic a = {a}")

    # For a fixed u in C^4, define the bilinear form on v and c2:
    # T(u)_{j3, c2} = sum_{j0, c1} u_{j0} a_{c1} M[j0, c1, j3, c2]
    # Then the condition is: for all v in W, T(u)^T v = 0 in C^4 (for all c2).
    # That means: W must be contained in ker(T(u))!
    # Where T(u) is the 4x4 matrix: T(u)[j3, c2] = sum_{j0, c1} u_{j0} a_{c1} M[j0, c1, j3, c2].
    # But W is a 2-dimensional subspace!
    # So ker(T(u)) must have dimension >= 2!
    # Which means rank(T(u)) <= 4 - 2 = 2!
    # That is: rank(T(u)) <= 2 for this u!

    # Let's inspect T(u) as a function of u!
    # T(u) is a 4x4 matrix linear in u!
    # Let's compute rank(T(u)) for random u:
    for trial in range(5):
        u = rng.standard_normal(4)
        T_u = np.einsum("j,c,jckf->kf", u, a, M) # shape (4, 4) in (j3, c2)
        rk = np.linalg.matrix_rank(T_u, tol=1e-8)
        svals = np.linalg.svd(T_u, compute_uv=False)
        print(f"Random u: rank(T(u)) = {rk}, svals = {svals}")

    # What is the minimum rank of T(u) over all nonzero u in C^4?
    # T(u) is a 4x4 matrix. Can rank(T(u)) <= 2 for some nonzero u?
    # Let's check the determinant det(T(u)) and 3x3 minors of T(u)!
    # T(u) entries are linear in u.
    # T(u)[j3, c2] = sum_{j0, c1} u_{j0} a_{c1} M[j0, c1, j3, c2]
    # Notice: if j3 == c2, M is 0!
    # So T(u) ALSO HAS ZERO DIAGONAL!
    print("\nCheck diagonal of T(u):")
    u_test = rng.standard_normal(4)
    T_test = np.einsum("j,c,jckf->kf", u_test, a, M)
    print(f"Diagonal of T(u): {np.diag(T_test)}")

if __name__ == "__main__":
    test_bilinear_obstruction()
