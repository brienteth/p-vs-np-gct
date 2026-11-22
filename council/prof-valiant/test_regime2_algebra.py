"""Analyze exactness and syzygies of the (2,3) and (3,2) complexes."""
import sys
sys.path.insert(0, '/Users/bl10buer/Desktop/matemk/p-vs-np-gct')
import numpy as np

# In Orbit 11: (r1, s1, r2, s2) = (3, 2, 2, 3).
# Here:
# C(a)^4 -> C(a)^5 -> C(a)^4 has ranks 2 and 3, sum = 5.
# Exact at the middle: im(A2(a)) = ker(A1(a)).
# Similarly, for B: C(b)^4 -> C(b)^5 -> C(b)^4 has ranks 3 and 2, sum = 5.
# Exact at the middle: im(B2(b)) = ker(B1(b)).

print("Orbit 11 exhibits exact complexes over the function fields C(a) and C(b).")
print("What about Orbit 8: (2, 2, 2, 2)?")
print("Here r1 + r2 = 4 < 5. The middle homology has dimension 5 - 4 = 1.")
print("im(A2(a)) is a proper 2D subspace of the 3D subspace ker(A1(a)).")
print("What about Orbit 9: (2, 2, 2, 3)?")
print("r1 + r2 = 4 < 5, but s1 + s2 = 5.")
print("What about Orbit 10: (2, 2, 3, 3)?")
print("r1 + r2 = 5, s1 + s2 = 5.")
