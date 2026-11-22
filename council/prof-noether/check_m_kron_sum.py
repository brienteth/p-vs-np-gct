"""Test minimum possible rank of M - B1 (x) C1 - B2 (x) C2 over structured and adversarial choices."""
import itertools
import numpy as np

M = np.zeros((16, 16), dtype=int)
for j0 in range(4):
    for c1 in range(4):
        for j3 in range(4):
            for c2 in range(4):
                if len({j0, c1, j3, c2}) == 4:
                    M[j0*4 + c1, j3*4 + c2] = 1

# Basis of Sym_0(4): 6 matrices E_{ij} = E_{i,j} + E_{j,i}
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
E_pairs = {}
for i, j in pairs:
    E = np.zeros((4, 4), dtype=int)
    E[i, j] = 1
    E[j, i] = 1
    E_pairs[(i, j)] = E

# Note: M itself is a sum of 6 Kronecker products!
# Namely:
# M = sum_{(i,j) in pairs} E_{ij} (x) E_{comp(i,j)}
M_decomp = np.zeros((16, 16), dtype=int)
comp = {
    (0, 1): (2, 3),
    (2, 3): (0, 1),
    (0, 2): (1, 3),
    (1, 3): (0, 2),
    (0, 3): (1, 2),
    (1, 2): (0, 3),
}
# Wait: M[(j0, c1), (j3, c2)] = 1 iff {j0, c1, j3, c2} = {0,1,2,3}
# Notice that in (j0, j3) x (c1, c2), M = sum_{p in pairs} E_p (x) E_{comp(p)}!
# Wait: what is E_p (x) E_{comp(p)} in (j0, c1) x (j3, c2) (i.e. standard np.kron)?
# In standard np.kron(B, C), entry [(j0, c1), (j3, c2)] is B[j0, j3] * C[c1, c2]!
for p, cp in comp.items():
    M_decomp += np.kron(E_pairs[p], E_pairs[cp])

print("Does M equal sum_{p in pairs} kron(E_p, E_{comp(p)})?:", np.array_equal(M, M_decomp))
