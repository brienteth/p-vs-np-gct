"""Prof. Wigner: Round 4 Phase 4A - Analysis of the 32 Boundary Tuples for n=6, w=19."""
import numpy as np
import itertools

def enumerate_32_tuples():
    print("=" * 70)
    print("PROF. WIGNER: ROUND 4 BOUNDARY TUPLE CLASSIFICATION (n=6, w=19)")
    print("=" * 70)

    # All tuples (r1, s1, r2, s2) with 0 <= r_i, s_i <= 15
    # Conditions:
    # 1. r1 + r2 <= 19
    # 2. s1 + s2 <= 19
    # 3. min(r1, s2) + min(s1, r2) >= 15
    # 4. max(r1, r2) == 15 and max(s1, s2) == 15 (Hilbert-Kruskal-Katona eliminates balanced)
    
    candidates = []
    for r1 in range(16):
        for s1 in range(16):
            for r2 in range(16):
                for s2 in range(16):
                    if r1 + r2 <= 19 and s1 + s2 <= 19:
                        if min(r1, s2) + min(s1, r2) >= 15:
                            if max(r1, r2) == 15 and max(s1, s2) == 15:
                                candidates.append((r1, s1, r2, s2))

    print(f"Total candidates satisfying Hilbert-Katona boundary conditions: {len(candidates)}")
    
    # Check if s1 == 0 or r2 == 0 is possible:
    # If s1 == 0 or r2 == 0, then B1(b) A2(a) = 0.
    # Then P(a, b) = A1(a) B2(b) has rank <= 19 in N_01, contradicting rank(M_6) = 20.
    surviving = []
    for (r1, s1, r2, s2) in candidates:
        if r1 == 15 and s2 == 15:
            # Case A:
            if s1 > 0 and r2 > 0:
                surviving.append((r1, s1, r2, s2))
        elif r2 == 15 and s1 == 15:
            # Case B:
            if r1 > 0 and s2 > 0:
                surviving.append((r1, s1, r2, s2))
                
    print(f"Surviving boundary tuples after excluding B1 A2 == 0: {len(surviving)}")
    assert len(surviving) == 32
    print("CONFIRMED: Exactly 32 extreme boundary tuples survive!")
    
    # Print the 32 tuples
    case_A = [t for t in surviving if t[0] == 15]
    case_B = [t for t in surviving if t[2] == 15]
    print(f"\nCase A (Aligned Forward Asymmetric, r1=15, s2=15): {len(case_A)} tuples:")
    print("  s1 \\ r2 |  1   2   3   4")
    print("  " + "-" * 25)
    for s1 in range(1, 5):
        row = [f"({15},{s1},{r2},{15})" for r2 in range(1, 5)]
        print(f"    {s1}     | " + " ".join(f"{r2}" for r2 in range(1, 5)))

    print(f"\nCase B (Transpose Asymmetric, r2=15, s1=15): {len(case_B)} tuples.")
    return surviving

if __name__ == "__main__":
    enumerate_32_tuples()
