"""Test bilinear annihilation on extreme boundary tuples for n=6, w=19."""
import itertools
import numpy as np

# In n=6, m6=15, w=19.
# Target: P(a,b)_{15x15}.
# Nisan matrix M6 has rank 20.
# Suppose M6 = N_01(A1 B2) + N_01(B1 A2).
# Here A1(a) has rank 15, B2(b) has rank 15,
# while B1(b) has rank s1 <= 4, and A2(a) has rank r2 <= 4.

# What is the maximum possible rank of N_01(B1 A2)?
# B1(b)_{15x19} has rank <= 4.
# A2(a)_{19x15} has rank <= 4.
# In N_01, N_01(B1 A2) = sum_{k=1}^19 K(B_k, A_k).
# Notice that B1(b) has rank s1 <= 4 over K(b).
# What is the rank of the tensor flattening N_01(B1 A2)?
# Let us test random B1 of rank s1 <= 4 and A2 of rank r2 <= 4!
print("Testing rank of N_01(B1 A2) when s1 <= 4 and r2 <= 4...")
