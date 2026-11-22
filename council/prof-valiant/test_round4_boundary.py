"""Analyze the surviving 32 boundary tuples for n=6, w=19."""
import itertools
import numpy as np

# We have n = 6, k = 3, m6 = 15, w = 19, N_3 = 20.
# Boundary tuples: r1 = 15, s2 = 15, r2 <= 4, s1 <= 4.
# (and transpose: r2 = 15, s1 = 15, r1 <= 4, s2 <= 4).
# In this regime:
# A1(a) is 15x19 of rank 15.
# A2(a) is 19x15 of rank r2 <= 4.
# B1(b) is 15x19 of rank s1 <= 4.
# B2(b) is 19x15 of rank 15.

# Condition (i): A1(a) A2(a) = 0 for all a.
# Over K = F(a0..a5), im(A2(a)) is a subspace of ker(A1(a)).
# Since r1 = 15 and A1 has 19 columns, dim ker(A1(a)) = 19 - 15 = 4.
# im(A2(a)) has dimension r2 <= 4.

# What can we say about the kernel ker(A1(a))?
# A1(a) is 15x19 linear in a0..a5.
# Does ker(A1(a)) have a constant subspace?
print("Analyzing kernel and image structure for r1=15, r2<=4...")
