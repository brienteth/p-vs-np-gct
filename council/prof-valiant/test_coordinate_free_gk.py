"""Test coordinate-free GK_6 drop for 500 random non-coordinate subspaces W in F_MOD^15."""
import sys
sys.path.insert(0, '/Users/bl10buer/Desktop/matemk/p-vs-np-gct')
import itertools
import numpy as np
from perm4_abp_frontier import MOD
from apolar_higher_betti_probe import rank_matrix_mod

n = 6
k = 3
subsets2 = list(itertools.combinations(range(n), 2)) # 15
subsets3 = list(itertools.combinations(range(n), k)) # 20

# Gottlieb matrix G: 20 x 15
G = np.zeros((20, 15), dtype=np.int64)
for s_idx, S in enumerate(subsets3):
    for j_idx, J in enumerate(subsets2):
        if set(J).issubset(set(S)):
            G[s_idx, j_idx] = 1

assert rank_matrix_mod(G % MOD, MOD) == 15

# What is the question?
# For a subspace W in K^15 of dimension d (given by basis matrix B_W in F^{15 x d} or nullspace Gamma in F^{(15-d) x 15}):
# When v in ker(A2(a)) has dimension 15 - r2:
# What is the maximum dimension of im(G) that can lie in a d-dimensional subspace W?
# Notice: G is an injective linear map from F^15 to F^20.
# For any subspace W in F^15 of dimension d:
# G(W) is a subspace of F^20 of dimension EXACTLY d!
# But what is the intersection with what?
# Let us check: In Hilbert Theorem H2(n):
# The stack is Phi_a(v) = [P_0(a) v, ..., P_5(a) v] in S_{6,3}(K).
# For any subspace W in K^15 of dimension d:
# What is the dimension of { v in K^15 : Phi_a(v) in S_{6,3}(K) cap (W x K^6) }?
# That is, for all c in {0..5}, P_c(a) v in W!
# That means for all c in {0..5}, Gamma_{15-d x 15} P_c(a) v = 0!
# where Gamma is a basis for W^perp (size (15-d) x 15).
# So v is in the common kernel of the 6 matrices (Gamma P_c(a)) for c = 0..5!
# The dimension of this space of v is:
# dim_ker(W) = 15 - rank( [Gamma P_0; Gamma P_1; ...; Gamma P_5] )!

print("Testing dim_ker(W) across 500 random non-coordinate subspaces W for each d = 1..14...")
rng = np.random.default_rng(42)

# Build the 6 slice matrices P_c (15 x 15)
full_set = set(range(n))
P_slices = []
for c in range(n):
    Pc = np.zeros((15, 15), dtype=np.int64)
    for i, I in enumerate(subsets2):
        for j, J in enumerate(subsets2):
            if set(I).isdisjoint(set(J)):
                rem = list(full_set - set(I) - set(J))
                if rem[0] == c or rem[1] == c:
                    Pc[i, j] = 1
    P_slices.append(Pc)

# Test for each d from 1 to 14:
results = {}
for d in range(1, 15):
    p = 15 - d # dimension of Gamma
    dim_kers = []
    # Test 35 random subspaces per d (total 14 * 35 = 490 tests)
    for trial in range(35):
        # Random Gamma of size p x 15 over MOD
        Gamma = rng.integers(1, MOD, size=(p, 15), dtype=np.int64)
        while rank_matrix_mod(Gamma, MOD) < p:
            Gamma = rng.integers(1, MOD, size=(p, 15), dtype=np.int64)
            
        # Stack Gamma P_c for c = 0..5: size (6p) x 15
        stacked = np.vstack([(Gamma @ Pc) % MOD for Pc in P_slices]) % MOD
        r_stack = rank_matrix_mod(stacked, MOD)
        dim_v = 15 - r_stack
        dim_kers.append(dim_v)
        
    min_k, max_k = min(dim_kers), max(dim_kers)
    results[d] = (min_k, max_k)
    print(f"d = {d:2d} (p = {p:2d}): dim_ker range = [{min_k}, {max_k}]")
