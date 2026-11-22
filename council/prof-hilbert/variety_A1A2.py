"""Prof. Hilbert: Study the algebraic variety Z = {(A1, A2) : A1(a) A2(a) = 0 for all a}.
Dimension, irreducible components, and rank stratification.
"""
import numpy as np

def test_variety():
    # A1 is 4x5 linear in a in C^4 (80 parameters)
    # A2 is 5x4 linear in a in C^4 (80 parameters)
    # Total space dimension = 160.
    # The condition A1(a) A2(a) = 0 gives 10 4x4 matrix equations:
    # A1_i A2_i = 0  (4 equations of 16 entries each = 64)
    # A1_i A2_j + A1_j A2_i = 0  (6 equations of 16 entries each = 96)
    # Total = 160 scalar quadratic equations in 160 variables.
    print("Z is cut out by 160 quadratic equations in 160 variables.")

if __name__ == "__main__":
    test_variety()
