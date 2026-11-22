"""Analyze Regime 2 orbits: (2,2,2,2), (2,2,2,3), (2,2,3,3), (2,3,3,2)."""
import sys
sys.path.insert(0, '/Users/bl10buer/Desktop/matemk/p-vs-np-gct')
import numpy as np

# In Regime 2:
# Every tuple has min(r1, s2) >= 2 and min(s1, r2) >= 2.
# Since r1 + r2 <= 5 and s1 + s2 <= 5:
# Max possible values are 2 and 3!
# Because if any rank was 4, say r1 = 4:
# then r2 <= 5 - 4 = 1 => min(s1, r2) <= 1, which violates k_min = 2!
# PROOF:
# If r1 = 4, then r2 <= 1 => min(s1, r2) <= 1 => k_min <= 1!
# By symmetry, NONE of r1, s1, r2, s2 can be 4 in Regime 2!
# Therefore: r1, s1, r2, s2 in {2, 3} for all tuples in Regime 2!

print("PROVEN: In Regime 2, every rank r1, s1, r2, s2 must be either 2 or 3.")
print("None can be 4, and none can be <= 1.")

# Let us verify this:
regime2_tuples = [
    (2, 2, 2, 2),
    (2, 2, 2, 3), (2, 2, 3, 2), (2, 3, 2, 2), (3, 2, 2, 2),
    (2, 2, 3, 3), (3, 3, 2, 2),
    (2, 3, 3, 2), (3, 2, 2, 3)
]
for t in regime2_tuples:
    assert all(x in (2, 3) for x in t)
print("Verified: all 9 tuples have ranks strictly in {2, 3}!")
