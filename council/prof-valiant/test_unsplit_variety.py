"""Analyze variety of unsplit solutions and rank stratification."""
import sys
sys.path.insert(0, '/Users/bl10buer/Desktop/matemk/p-vs-np-gct')
import numpy as np

# A1(a) is 4x5, linear in a (16x5 = 80 params)
# B1(b) is 4x5, linear in b (16x5 = 80 params)
# A2(a) is 5x4, linear in a (5x16 = 80 params)
# B2(b) is 5x4, linear in b (5x16 = 80 params)
# Total params = 320.
# GL_5 gauge action: dim GL_5 = 25.
# Effective params = 320 - 25 = 295.

# Equations:
# 1. A1(a) A2(a) = 0: 4x4 matrix of quadratic forms in 4 vars a0..a3.
#    Number of monomials in a of degree 2: C(4+2-1, 2) = 10.
#    16 entries * 10 monomials = 160 equations.
# 2. B1(b) B2(b) = 0: 16 * 10 = 160 equations.
# 3. A1(a) B2(b) + B1(b) A2(a) = P(a,b):
#    4x4 matrix of bilinear forms in a and b.
#    Number of monomials a_c1 b_c2 = 16.
#    16 entries * 16 monomials = 256 equations.
# Total equations = 160 + 160 + 256 = 576 equations!
print("Unsplit system: 320 variables, 576 equations, GL_5 gauge dimension 25.")
print("Overdetermined by 576 - 295 = 281 equations!")
