"""Prof. Valiant: Combinatorial Case Analysis of Q2 Rank Tuples (r1, s1, r2, s2)."""
import itertools
from collections import defaultdict
import numpy as np

def analyze_rank_tuples():
    survivors = []
    for r1 in range(5):
        for s1 in range(5):
            for r2 in range(5):
                for s2 in range(5):
                    # Necessary conditions:
                    # 1. A1 A2 = 0 => rank(A1) + rank(A2) <= 5
                    # 2. B1 B2 = 0 => rank(B1) + rank(B2) <= 5
                    # 3. P(a,a) = A1(a)B2(a) + B1(a)A2(a) has rank 4 => min(r1,s2) + min(s1,r2) >= 4
                    # 4. M1(a,a) has rank >= 4 => r1 + s1 >= 4
                    # 5. M2(a,a) has rank >= 4 => r2 + s2 >= 4
                    if r1 + r2 <= 5 and s1 + s2 <= 5:
                        if min(r1, s2) + min(s1, r2) >= 4:
                            if r1 + s1 >= 4 and r2 + s2 >= 4:
                                survivors.append((r1, s1, r2, s2))

    def get_orbit(t):
        r1, s1, r2, s2 = t
        return frozenset({
            (r1, s1, r2, s2),
            (s1, r1, s2, r2), # a <-> b
            (r2, s2, r1, s1), # transpose
            (s2, r2, s1, r1), # both
        })

    orbits = sorted(list(set(get_orbit(t) for t in survivors)), key=lambda x: min(x))
    
    print(f"Total surviving tuples: {len(survivors)}")
    print(f"Total symmetry orbits: {len(orbits)}\n")
    
    # Categorize into Regimes
    regimes = defaultdict(list)
    for orb in orbits:
        rep = min(orb)
        r1, s1, r2, s2 = rep
        m1 = min(r1, s2)
        m2 = min(s1, r2)
        min_rank = min(m1, m2)
        regimes[min_rank].append(orb)
        
    for k in sorted(regimes.keys()):
        print(f"==================================================")
        print(f"REGIME min(min(r1,s2), min(s1,r2)) = {k}")
        print(f"==================================================")
        for orb in regimes[k]:
            rep = min(orb)
            r1, s1, r2, s2 = rep
            m1 = min(r1, s2)
            m2 = min(s1, r2)
            print(f"Orbit representative: {rep} (orbit size: {len(orb)})")
            print(f"  All members: {sorted(list(orb))}")
            print(f"  Ranks: min(r1,s2)={m1}, min(s1,r2)={m2}, sum={m1+m2}")
            print(f"  Sylvester: r1+r2={r1+r2}<=5, s1+s2={s1+s2}<=5")
            print()

if __name__ == "__main__":
    analyze_rank_tuples()
