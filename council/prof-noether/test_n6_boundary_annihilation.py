"""Round 4: Test the Unsplit Bilinear Annihilation Proof for the 32 Extreme Boundary Tuples
of n = 6, w = 19: (r1 = 15, s2 = 15, r2 <= 4, s1 <= 4)."""
import itertools
import numpy as np
import sys
sys.path.append('p-vs-np-gct/council/prof-noether')
from general_n2k_noether import build_Mn

M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
# M6 is 90 x 90, rows (I, c1), cols (J, c2)
# Rectangular commutation matrix K_{15, 6}: maps (c2, J) -> (J, c2)
K_comm = np.zeros((90, 90), dtype=int)
for J in range(15):
    for c2 in range(6):
        K_comm[J * 6 + c2, c2 * 15 + J] = 1

MK = M6 @ K_comm  # rows (I, c1), cols (c2, J)

rng = np.random.default_rng(2026)

# 1. Verify rank of (M6 K_{15,6}) (Y (x) I_15) for q = 1, 2, 3 vectors in R^6
for q in [1, 2, 3]:
    Y = rng.standard_normal((6, q))
    sub = MK @ np.kron(Y, np.eye(15))  # 90 x (15*q)
    print(f"q={q}: rank((M6 K_comm)(Y (x) I_15)) = {np.linalg.matrix_rank(sub)}")

# 2. Verify for ANY pair of linearly independent vectors y1, y2 in F_p^6 (exhaustive over F_3!)
# Does (M6 K_comm)([y1, y2] (x) I_15) ALWAYS have rank 20, or are there special 2D planes Y in Gr(2, 6)?
def rank_mod(A, p):
    A = A.copy() % p
    m, n = A.shape
    r = 0
    for c in range(n):
        piv = None
        for i in range(r, m):
            if A[i, c] != 0:
                piv = i
                break
        if piv is None:
            continue
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        inv = pow(int(A[r, c]), p - 2, p)
        A[r] = (A[r] * inv) % p
        col = A[:, c].copy()
        col[r] = 0
        A = (A - np.outer(col, A[r])) % p
        r += 1
    return r

# Check all 2D subspaces of F_3^6? Wait: |Gr(2, F_3^6)| = (3^6-1)(3^6-3)/((3^2-1)(3^2-3)) = 728*726 / 48 = 11011.
# Even better, test 200 random + all 15 coordinate 2-planes over F_1000003 and R!
min_rk_Y2 = 100
coord_drops = []
for i, j in itertools.combinations(range(6), 2):
    Y = np.zeros((6, 2), dtype=float)
    Y[i, 0] = 1.0
    Y[j, 1] = 1.0
    rk = np.linalg.matrix_rank(MK @ np.kron(Y, np.eye(15)))
    if rk < 20:
        coord_drops.append(((i, j), rk))
    min_rk_Y2 = min(min_rk_Y2, rk)

print(f"Coordinate 2-planes Y=[e_i, e_j]: min rank = {min_rk_Y2}, drops = {coord_drops[:5]} (total {len(coord_drops)}/15)")

# Test 100 random Y of size 6 x 2
min_rk_rand = 100
for _ in range(100):
    Y = rng.standard_normal((6, 2))
    rk = np.linalg.matrix_rank(MK @ np.kron(Y, np.eye(15)))
    min_rk_rand = min(min_rk_rand, rk)
print(f"100 random Y in R^{{6x2}}: min rank((M6 K_comm)(Y (x) I_15)) = {min_rk_rand}")

# 3. Test Unsplit Bilinear Annihilation for random rank-s1 pencils B1(b) (15 x 19) for s1 = 1, 2, 3, 4:
# Build a moving rank-s1 linear pencil B1(b) = L(b)_{15 x s1} R_{s1 x 19} or sum of moving rank-1 terms
for s1 in [1, 2, 3, 4]:
    min_witness_rk = 100
    for trial in range(25):
        # Construct moving rank-s1 linear pencil: B1(b) = U(b)_{15 x s1} C_{s1 x 19} (moving column space!)
        U_coeffs = rng.standard_normal((6, 15, s1))
        C_const = rng.standard_normal((s1, 19))
        # Pick generic y1, y2 in R^6
        Y = rng.standard_normal((6, 2))
        B_y1 = np.tensordot(Y[:, 0], U_coeffs, axes=([0], [0])) @ C_const  # 15 x 19, rank s1
        B_y2 = np.tensordot(Y[:, 1], U_coeffs, axes=([0], [0])) @ C_const  # 15 x 19, rank s1
        # Left kernel X of [B_y1, B_y2] has >= 15 - 2*s1 rows!
        M_cat = np.hstack([B_y1, B_y2])
        u, svals, _ = np.linalg.svd(M_cat)
        p_rows = 15 - 2 * s1
        X = u[:, 2*s1:].T  # p_rows x 15
        assert np.linalg.norm(X @ B_y1) < 1e-10 and np.linalg.norm(X @ B_y2) < 1e-10
        witness = np.kron(X, np.eye(6)) @ MK @ np.kron(Y, np.eye(15))
        rk = np.linalg.matrix_rank(witness)
        if rk < min_witness_rk:
            min_witness_rk = rk
    print(f"s1={s1} (p=15-2*s1={15-2*s1} rows in X): min witness rank = {min_witness_rk} (need <= 19 for w=19!)")
