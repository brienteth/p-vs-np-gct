"""Study projections of K(B, V) onto V_+ and V_-."""
import numpy as np

# Basis of Sym_0(4):
# V_+ basis:
# X1 = (01) + (23) -> normalized
# X2 = (02) + (13) -> normalized
# X3 = (03) + (12) -> normalized
# Note: X1, X2, X3 are orthogonal in R^16!
# Each has 4 entries equal to 1, rest 0. Norm = 2.
X1 = np.zeros(16)
for i, j in [(0, 1), (1, 0), (2, 3), (3, 2)]:
    X1[i*4 + j] = 0.5
X2 = np.zeros(16)
for i, j in [(0, 2), (2, 0), (1, 3), (3, 1)]:
    X2[i*4 + j] = 0.5
X3 = np.zeros(16)
for i, j in [(0, 3), (3, 0), (1, 2), (2, 1)]:
    X3[i*4 + j] = 0.5

# V_- basis:
# Y1 = (01) - (23) -> normalized
# Y2 = (02) - (13) -> normalized
# Y3 = (03) - (12) -> normalized
Y1 = np.zeros(16)
for (i, j), s in [((0, 1), 0.5), ((1, 0), 0.5), ((2, 3), -0.5), ((3, 2), -0.5)]:
    Y1[i*4 + j] = s
Y2 = np.zeros(16)
for (i, j), s in [((0, 2), 0.5), ((2, 0), 0.5), ((1, 3), -0.5), ((3, 1), -0.5)]:
    Y2[i*4 + j] = s
Y3 = np.zeros(16)
for (i, j), s in [((0, 3), 0.5), ((3, 0), 0.5), ((1, 2), -0.5), ((2, 1), -0.5)]:
    Y3[i*4 + j] = s

U_plus = np.column_stack([X1, X2, X3])   # 16 x 3, orthonormal
U_minus = np.column_stack([Y1, Y2, Y3])  # 16 x 3, orthonormal

print("U_plus orthogonal:", np.allclose(U_plus.T @ U_plus, np.eye(3)))
print("U_minus orthogonal:", np.allclose(U_minus.T @ U_minus, np.eye(3)))
print("Plus and minus orthogonal:", np.allclose(U_plus.T @ U_minus, np.zeros((3, 3))))

# Check M on this basis:
def make_M():
    M = np.zeros((16, 16))
    for j0 in range(4):
        for c1 in range(4):
            for j3 in range(4):
                for c2 in range(4):
                    if len({j0, c1, j3, c2}) == 4:
                        M[j0*4 + c1, j3*4 + c2] = 1.0
    return M

M = make_M()
print("M restricted to V_+:\n", np.round(U_plus.T @ M @ U_plus, 2))
print("M restricted to V_-:\n", np.round(U_minus.T @ M @ U_minus, 2))

# Now test K(B, V) restricted to V_+ and V_-:
def make_K(B, V):
    K = np.zeros((16, 16))
    for j0 in range(4):
        for c1 in range(4):
            for j3 in range(4):
                for c2 in range(4):
                    K[j0*4 + c1, j3*4 + c2] = B[j0, c2] * V[j3, c1]
    return K

rng = np.random.default_rng(777)
print("\nTesting K(B, V) projections for 5 random pairs:")
for t in range(5):
    B = rng.standard_normal((4, 4))
    V = rng.standard_normal((4, 4))
    K = make_K(B, V)
    K_pp = U_plus.T @ K @ U_plus
    K_mm = U_minus.T @ K @ U_minus
    K_pm = U_plus.T @ K @ U_minus
    print(f"Trial {t}: rank(K_pp)={np.linalg.matrix_rank(K_pp)}, rank(K_mm)={np.linalg.matrix_rank(K_mm)}, rank(K_pm)={np.linalg.matrix_rank(K_pm)}")
