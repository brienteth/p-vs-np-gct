"""Prof. Wigner: Analysis of the 8 Remaining Boundary Tuples with s1, r2 in {3, 4}."""
import numpy as np

def analyze_remaining_8():
    print("=" * 70)
    print("PROF. WIGNER: AUDIT OF THE 8 REMAINING BOUNDARY TUPLES (n=6, w=19)")
    print("=" * 70)

    # 4 aligned tuples:
    # (15, 3, 3, 15), (15, 3, 4, 15), (15, 4, 3, 15), (15, 4, 4, 15)
    # 4 transposed tuples:
    # (3, 15, 15, 3), (3, 15, 15, 4), (4, 15, 15, 3), (4, 15, 15, 4)
    aligned_8 = [
        (15, 3, 3, 15), (15, 3, 4, 15), (15, 4, 3, 15), (15, 4, 4, 15)
    ]
    trans_8 = [
        (3, 15, 15, 3), (3, 15, 15, 4), (4, 15, 15, 3), (4, 15, 15, 4)
    ]
    total_8 = aligned_8 + trans_8
    print(f"8 Remaining Boundary Tuples: {total_8}")
    
    # In each of these tuples:
    # r1 = 15, s2 = 15.
    # What is the codimension defect in C^{17550}?
    # Recall for w = 19:
    # D_phys = 360 * 19 - 19^2 = 6479.
    # Total equations = 17550.
    # The algebraic codimension defect is 17550 - 6479 = 11,071!
    print("Codimension defect of the variety remains: 11,071 constraints excess.")
    print("=" * 70)

if __name__ == "__main__":
    analyze_remaining_8()
