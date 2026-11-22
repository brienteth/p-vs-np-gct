"""Prof. Wigner Round 6: Test the 6-pair Star-Koszul (and mixed Koszul) construction at t_B = 4
to see why d_syz >= 6 and c >= 5 collides with rank_K(B_2) = 15 (or whether it can survive)!
Also inspect exact algebraic syzygy identities across ALL S_6 orbits for t_B = 2, 3, 4.
"""
import itertools
import numpy as np
import sys
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council/prof-noether")
from general_n2k_noether import build_Mn
from apolar_higher_betti_probe import rank_matrix_mod
from perm4_abp_frontier import MOD

def test_star_koszul_6_pairs():
    print("=" * 74)
    print("TESTING FULL 6-PAIR STAR-KOSZUL & MIXED CONSTRUCTIONS AT t_B = 4")
    print("=" * 74)
    Mn, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    sub2_idx = {s: i for i, s in enumerate(sub_2)}
    sub3_idx = {s: i for i, s in enumerate(sub_3)}
    B2_full = np.zeros((6, 20, 15), dtype=np.int64)
    for ell in range(20):
        B2_full[:, ell, :] = V_basis[:, ell].reshape(15, 6).T

    # Star-Koszul protruding rows around {0, 1}: r_c(b) = b_0 e_{1,c} - b_1 e_{0,c} for c in {2,3,4,5}
    r_star = np.zeros((6, 4, 15), dtype=np.int64)
    for idx_c, c in enumerate([2, 3, 4, 5]):
        r_star[0, idx_c, sub2_idx[(1, c)]] = 1
        r_star[1, idx_c, sub2_idx[(0, c)]] = MOD - 1

    # All 6 pairs in {2,3,4,5}:
    pairs_2345 = list(itertools.combinations([2, 3, 4, 5], 2))
    # For m pairs (m = 4, 5, 6), take {0, c1, c2} and {1, c1, c2} plus remaining canonical wires to reach 15 in B2_in
    other_s3 = [i for i in range(20) if not (0 in sub_3[i] and 1 not in sub_3[i] and set(sub_3[i]-set() if False else sub_3[i]).issubset({0,2,3,4,5})) ]
    # Cleaner:
    pair_wires = {}
    for p in pairs_2345:
        pair_wires[p] = (sub3_idx[(0, p[0], p[1])], sub3_idx[(1, p[0], p[1])])
    all_pair_wire_set = set(w for ws in pair_wires.values() for w in ws)
    rem_wires = [i for i in range(20) if i not in all_pair_wire_set] # 20 - 12 = 8 wires!

    rng = np.random.default_rng(42)
    b_pt = rng.integers(1, MOD, size=6, dtype=np.int64)
    mons_2 = [(a, b) for a in range(6) for b in range(a, 6)]
    mon_idx = {m: i for i, m in enumerate(mons_2)}

    for m_pairs in [3, 4, 5, 6]:
        chosen = pairs_2345[:m_pairs]
        keep_in = [w for p in chosen for w in pair_wires[p]]
        # fill up to 15 canonical wires from rem_wires (or unused pair_wires)
        pool = rem_wires + [w for p in pairs_2345[m_pairs:] for w in pair_wires[p]]
        keep_in = keep_in + pool[:15 - len(keep_in)]
        assert len(keep_in) == 15
        B2 = np.concatenate([B2_full[:, keep_in, :], r_star], axis=1) # (6, 19, 15)
        rk_B2 = rank_matrix_mod(sum(int(b_pt[c]) * B2[c] for c in range(6)) % MOD, MOD)

        # Compute exact degree-1 left syzygies of B2
        E = np.zeros((315, 114), dtype=np.int64)
        for J in range(15):
            for a in range(6):
                for b in range(a, 6):
                    r = J * 21 + mon_idx[(a, b)]
                    for ell in range(19):
                        E[r, a * 19 + ell] = (E[r, a * 19 + ell] + B2[b, ell, J]) % MOD
                        if a != b:
                            E[r, b * 19 + ell] = (E[r, b * 19 + ell] + B2[a, ell, J]) % MOD
        # RREF
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
        B1 = np.zeros((6, d_syz, 19), dtype=np.int64)
        for s_i, fc in enumerate(free_cols):
            vec = np.zeros(114, dtype=np.int64)
            vec[fc] = 1
            for ip, pc in enumerate(piv_cols):
                vec[pc] = (-M[ip, fc]) % MOD
            B1[:, s_i, :] = vec.reshape(6, 19)
        s1 = rank_matrix_mod(sum(int(b_pt[c]) * B1[c] for c in range(6)) % MOD, MOD)
        c_supp = rank_matrix_mod(B1.reshape(6 * d_syz, 19), MOD)
        print(f"  m_pairs={m_pairs}: rk_B2={rk_B2}, d_syz={d_syz}, F(b)-rank s1={s1}, const wire support c={c_supp}")

if __name__ == "__main__":
    test_star_koszul_6_pairs()
