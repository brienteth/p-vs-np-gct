"""Test Grassmannian maximum of dim_ker(W) and balanced survivors."""
import sys
sys.path.insert(0, '/Users/bl10buer/Desktop/matemk/p-vs-np-gct')
import itertools
import math
import numpy as np
from apolar_higher_betti_probe import rank_matrix_mod

def cascade_kk_formula(k_out, d):
    if d <= 0:
        return 0
    k_in = k_out - 1
    rem = d
    out = 0
    for a in range(20, -1, -1):
        c = math.comb(a, k_in)
        if c <= rem and c > 0:
            out += math.comb(a, k_out)
            rem -= c
            k_in -= 1
            if rem == 0 or k_in <= 0:
                break
    return out

KK = [cascade_kk_formula(3, d) for d in range(16)]
print(f"Unconditional Hilbert-Katona KK_{{2->3}}(d): {KK}")

# Under KK, what pairs (r1, r2) survive r1 + r2 <= 19 and KK(r1) + r2 >= 15 and KK(r2) + r1 >= 15?
balanced_survivors = []
for r1 in range(1, 15):
    for r2 in range(1, 15):
        if r1 + r2 <= 19:
            if KK[r1] + r2 >= 15 and KK[r2] + r1 >= 15:
                balanced_survivors.append((r1, r2))

print(f"Balanced pairs (r1, r2 < 15) surviving UNCONDITIONAL Hilbert-Katona KK: {len(balanced_survivors)}")
print(f"List of surviving balanced pairs under KK alone: {balanced_survivors}")
