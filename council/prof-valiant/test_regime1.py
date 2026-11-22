"""Test properties of linear matrices A1(a) of generic rank 1."""
import numpy as np

# A1(a) is 4x5, linear in a0, a1, a2, a3.
# If rank(A1(a)) <= 1 for all a:
# By Westwick (1972), either:
# Type Col: A1(a) = u(a) * v^T where v in C^5 is constant, u(a) in C^4 linear.
# Type Row: A1(a) = u * v(a)^T where u in C^4 is constant, v(a) in C^5 linear.

print("Type Col: v in C^5 is constant.")
print("Then by GL_5 gauge transformation, v can be rotated to e_1 = (1, 0, 0, 0, 0)^T.")
print("Then A1(a) has ONLY column 1 non-zero, columns 2..5 are ZERO.")
print("This means wire 1 carries all of A1, and wires 2..5 have no A1 component!")
print()
print("Type Row: u in C^4 is constant.")
print("Then the row space of A1(a) is spanned by u for ALL a.")
print("Then row space of A1(a) B2(b) is contained in span(u).")
print("Then for any gamma in C^4 with gamma^T u = 0, gamma^T A1(a) B2(b) = 0.")
print("Thus gamma^T P(a,b) = gamma^T (B1(b) A2(a)).")
