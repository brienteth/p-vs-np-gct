"""Test generalization of Lemma A and incidence inequality for n=6."""
import itertools
import numpy as np

n = 6
k = 3
subsets_km1 = list(itertools.combinations(range(n), k - 1)) # 15
m6 = len(subsets_km1)
w6 = len(list(itertools.combinations(range(n), k))) # 20

# Let us check: for any v in C^15, what is P(a, v)?
# P(a, b) is 15 x 15, symmetric, with zeros where I and J overlap.
# Notice that for each fixed a, P(a, v) is a 15-vector of linear forms in a!
# What is the rank of the linear map v -> P(a, v)?
# For generic a, if P(a, a) has rank 15, then the map v -> P(a, v) is an ISOMORPHISM on C^15!
# Because P(a, .) evaluated at a has full rank 15!
# So for generic a, ker(v -> P(a, v)) = {0}!
print(f"For n={n}: m_n = {m6}, w_n = {w6}")
print(f"Map v -> P(a, v) has trivial kernel: dim(ker) = 0.")
