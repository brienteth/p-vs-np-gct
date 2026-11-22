"""Analyze the bilinear map (gamma, v) -> P_perm(gamma, delta) v
and the 8x4 matrix [P_perm(gamma_1, delta); P_perm(gamma_2, delta)]."""
import itertools
import numpy as np

def P_perm_mat(gamma, delta):
    P = np.zeros((4, 4), dtype=float)
    for i in range(4):
        for j in range(4):
            if i == j:
                continue
            c1, c2 = [k for k in range(4) if k != i and k != j]
            P[i, j] = gamma[c1]*delta[c2] + gamma[c2]*delta[c1]
    return P

# Notice P_perm(gamma, delta) is BILINEAR in gamma and delta,
# and P_perm(gamma, delta) v is linear in gamma!
# Therefore, P_perm(gamma, delta) v = Q(v, delta) gamma
# for a 4x4 matrix Q(v, delta)!
# WAIT A SECOND!
# Since T_{j0, c1, j3, c2} is TOTALLY SYMMETRIC in (j0, c1, j3, c2):
# (P_perm(gamma, delta) v)_{j0} = sum_{j3, c1, c2} T_{j0, c1, j3, c2} gamma_{c1} delta_{c2} v_{j3}
# = (P_perm(v, delta) gamma)_{j0} !!
# WAIT A SECOND! IS P_perm(gamma, delta) v == P_perm(v, delta) gamma ?!

rng = np.random.default_rng(42)
gamma = rng.standard_normal(4)
delta = rng.standard_normal(4)
v = rng.standard_normal(4)

lhs = P_perm_mat(gamma, delta) @ v
rhs = P_perm_mat(v, delta) @ gamma
print("||P_perm(gamma, delta) v - P_perm(v, delta) gamma|| =", np.linalg.norm(lhs - rhs))
