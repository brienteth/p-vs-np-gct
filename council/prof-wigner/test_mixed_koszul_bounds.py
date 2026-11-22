"""Prof. Wigner Round 6: Test mixed Koszul constructions (Edge-Koszul + Star-Koszul + Orbit-B)
at t_B = 4 to check whether ANY combination achieves rk_B2 = 15, s_1 in {3, 4}, d_syz >= 6, AND c >= 5.
"""
import itertools
import numpy as np
import sys
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council/prof-noether")
from general_n2k_noether import build_Mn
from apolar_higher_betti_probe import rank_matrix_mod
from perm4_abp_frontier import MOD

def analyze_B2(name, B2_in, B2_out):
    B2 = np.concatenate([B2_in, B2_out], axis=1) # (6, 19, 15)
    rng = np.random.default_rng(42)
    b_pt = rng.integers(1, MOD, size=6, dtype=np.int64)
    rk_B2 = rank_matrix_mod(sum(int(b_pt[c]) * B2[c] for c in range(6)) % MOD, MOD)
    mons_2 = [(a, b) for a in range(6) for b in range(a, 6)]
    mon_idx = {m: i for i, m in enumerate(mons_2)}
    E = np.zeros((315, 114), dtype=np.int64)
    for J in range(15):
        for a in range(6):
            for b in range(a, 6):
                r = J * 21 + mon_idx[(a, b)]
                for ell in range(19):
                    E[r, a * 19 + ell] = (E[r, a * 19 + ell] + B2[b, ell, J]) % MOD
                    if a != b:
                        E[r, b * 19 + ell] = (E[r, b * 19 + ell] + B2[a, ell, J]) % MOD
    M = E.copy()
    piv_cols = []; r_ptr = 0
    for c in range(114):
        piv = next((r for r in range(r_ptr, 315) if M[r, c] != 0), None)
        if piv is None: continue
        M[[r_ptr, piv]] = M[[piv, r_ptr]]
        inv = pow(int(M[r_ptr, c]), MOD - 2, MOD)
        M[r_ptr] = (M[r_ptr] * inv) % MOD
        for r in np.where(M[:, c] != 0)[0]:
            if r != r_ptr: M[r] = (M[r] - M[r, c] * M[r_ptr]) % MOD
        piv_cols.append(c); r_ptr += 1
    free_cols = [c for c in range(114) if c not in piv_cols]
    d_syz = len(free_cols)
    if d_syz == 0:
        print(f"  [{name}] rk_B2={rk_B2}, d_syz=0")
        return
    B1 = np.zeros((6, d_syz, 19), dtype=np.int64)
    for s_i, fc in enumerate(free_cols):
        vec = np.zeros(114, dtype=np.int64)
        vec[fc] = 1
        for ip, pc in enumerate(piv_cols):
            vec[pc] = (-M[ip, fc]) % MOD
        B1[:, s_i, :] = vec.reshape(6, 19)
    s1 = rank_matrix_mod(sum(int(b_pt[c]) * B1[c] for c in range(6)) % MOD, MOD)
    c_supp = rank_matrix_mod(B1.reshape(6 * d_syz, 19), MOD)
    print(f"  [{name}] rk_B2={rk_B2}, d_syz={d_syz}, s1={s1}, c={c_supp}")

def main():
    print("=" * 74)
    print("MIXED KOSZUL CONSTRUCTIONS AT t_B = 4 (SEARCHING FOR c >= 5 AND d_syz >= 6)")
    print("=" * 74)
    Mn, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    sub2_idx = {s: i for i, s in enumerate(sub_2)}
    sub3_idx = {s: i for i, s in enumerate(sub_3)}
    B2_full = np.zeros((6, 20, 15), dtype=np.int64)
    for ell in range(20):
        B2_full[:, ell, :] = V_basis[:, ell].reshape(15, 6).T

    # 1. Pure Edge-Koszul on {4,5}: r_i = b_4 e_{i,5} + b_5 e_{i,4} (i=0..3)
    # Keep {0,4,5},{1,4,5},{2,4,5},{3,4,5} + 11 others
    keep_edge = [sub3_idx[(i,4,5)] for i in range(4)] + [i for i in range(20) if i not in [sub3_idx[(i,4,5)] for i in range(4)]][:11]
    r_edge = np.zeros((6, 4, 15), dtype=np.int64)
    for i in range(4):
        r_edge[4, i, sub2_idx[(i,5)]] = 1; r_edge[5, i, sub2_idx[(i,4)]] = 1
    analyze_B2("Pure Edge-Koszul (Noether #58)", B2_full[:, keep_edge, :], r_edge)

    # 2. 3 Edge-Koszul (i=0,1,2 on {4,5}) + 1 Star-Koszul (r_3 = b_0 e_{1,3} - b_1 e_{0,3} or b_4 e_{3,5}):
    r_mix1 = r_edge.copy()
    r_mix1[:, 3, :] = 0
    r_mix1[0, 3, sub2_idx[(1, 3)]] = 1; r_mix1[1, 3, sub2_idx[(0, 3)]] = MOD - 1
    # Keep {0,4,5},{1,4,5},{2,4,5}, {0,2,3},{1,2,3}, {0,3,4},{1,3,4}, ...
    must = [sub3_idx[s] for s in [(0,4,5),(1,4,5),(2,4,5),(0,2,3),(1,2,3),(0,3,4),(1,3,4),(0,3,5),(1,3,5)]]
    keep_m1 = must + [i for i in range(20) if i not in must][:6]
    analyze_B2("3 Edge + 1 Star", B2_full[:, keep_m1, :], r_mix1)

    # 3. 2-wire Edge-Koszul on {4,5} + 2-wire Edge-Koszul on {0,1}?
    # e.g. i=0,1 on {4,5} (1 syz) and j=2,3 on {0,1} (1 syz):
    r_mix2 = np.zeros((6, 4, 15), dtype=np.int64)
    r_mix2[4, 0, sub2_idx[(0,5)]] = 1; r_mix2[5, 0, sub2_idx[(0,4)]] = 1
    r_mix2[4, 1, sub2_idx[(1,5)]] = 1; r_mix2[5, 1, sub2_idx[(1,4)]] = 1
    r_mix2[0, 2, sub2_idx[(1,2)]] = 1; r_mix2[1, 2, sub2_idx[(0,2)]] = 1
    r_mix2[0, 3, sub2_idx[(1,3)]] = 1; r_mix2[1, 3, sub2_idx[(0,3)]] = 1
    must2 = [sub3_idx[s] for s in [(0,4,5),(1,4,5),(0,1,2),(0,1,3)]]
    keep_m2 = must2 + [i for i in range(20) if i not in must2][:11]
    analyze_B2("2 Edge({4,5}) + 2 Edge({0,1})", B2_full[:, keep_m2, :], r_mix2)

    # 4. Orbit-B witness (b4=0, b0=b1): v_{0,4,j} - v_{1,4,j} = b_j(e_{0,4} - e_{1,4}) + b4(...)
    # To kill b4 terms for j in {2,3,5}, we need 3 protruding rows: r_j = b_0 e_{4,j} - b_1 e_{4,j} = (b_0 - b_1) e_{4,j}?
    # Wait: v_{0,4,j} - v_{1,4,j} = b_j(e_{0,4}-e_{1,4}) + b_4(e_{0,j}-e_{1,j}) + (b_0 - b_1) e_{4,j}!
    # So to leave ONLY b_j(e_{0,4}-e_{1,4}), we need r_j = b_4(e_{0,j}-e_{1,j}) + (b_0 - b_1) e_{4,j} (3 rows for j=2,3,5)!
    # Plus what if we add j=4? No, 4 not in {2,3,5}. Add 1 more edge:
    r_orbB = np.zeros((6, 4, 15), dtype=np.int64)
    for idx_j, j in enumerate([2, 3, 5]):
        r_orbB[4, idx_j, sub2_idx[(0, j)]] = 1
        r_orbB[4, idx_j, sub2_idx[(1, j)]] = MOD - 1
        ej4 = tuple(sorted((4, j)))
        r_orbB[0, idx_j, sub2_idx[ej4]] = 1
        r_orbB[1, idx_j, sub2_idx[ej4]] = MOD - 1
    # 4th row: random/zero or another pair
    r_orbB[4, 3, sub2_idx[(2, 3)]] = 1
    mustB = [sub3_idx[s] for s in [(0,2,4),(1,2,4),(0,3,4),(1,3,4),(0,4,5),(1,4,5)]]
    keep_B = mustB + [i for i in range(20) if i not in mustB][:9]
    analyze_B2("Orbit-B 3-pair (t_B=4)", B2_full[:, keep_B, :], r_orbB)

    # 5. What if we take TWO overlapping Orbit-B pairs? Say {0,4,j} - {1,4,j} (j=2,3,5) -> 3 pairs (6 wires),
    # Wait: that only uses 3 protruding rows r_j! Why did it give c=6 instead of 3? Wait:
    # Let's see what analyze_B2 prints for Orbit-B!

if __name__ == "__main__":
    main()
