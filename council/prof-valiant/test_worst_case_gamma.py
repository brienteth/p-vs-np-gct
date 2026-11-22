"""Test the absolute worst-case Gamma of dimension 11 on M6."""
import sys
sys.path.insert(0, '/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council/prof-valiant')
import itertools
import numpy as np
from test_slice_rank import M6

# Test worst-case 11-dimensional Gamma:
# A worst-case Gamma has ker(Gamma) = W of dimension 4 maximizing dim(Sym_0 cap (W x C^6)).
# Any coordinate 4-subspace W:
subsets_km1 = list(itertools.combinations(range(6), 2)) # 15

# Test all C(15, 4) = 1365 coordinate 4-subspaces as kernels:
min_r = 999
for comb in itertools.combinations(range(15), 4):
    # W is spanned by e_i for i in comb
    # Gamma has rows e_j for j not in comb (11 rows)
    Gamma = np.zeros((11, 15))
    row = 0
    for j in range(15):
        if j not in comb:
            Gamma[row, j] = 1.0
            row += 1
    
    G_kron = np.kron(Gamma, np.eye(6))
    r = np.linalg.matrix_rank(G_kron @ M6)
    if r < min_r:
        min_r = r

print(f"Minimum rank across ALL 1,365 coordinate 4-subspaces for Gamma (dim 11): {min_r}")
