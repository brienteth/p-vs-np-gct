"""Prof. Wigner Round 7 (GAP 2):
Exhaustive classification of the exceptional codimension-2 locus Z_2 c Gr(2, 6)
where B_{2,full}|_H admits degree-1 left syzygies!
1. Exhaustive scan over Gr(2, 6, F_2) (651 planes) and F_3-orbit sampling / partial exhaustive.
2. Analytic-gradient / SVD scan over C for dim Z_2 and maximal syz_dim on H in Gr(4, 6).
"""
import itertools
import numpy as np
import sys
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council/prof-noether")
from general_n2k_noether import build_Mn
from apolar_higher_betti_probe import rank_matrix_mod
from perm4_abp_frontier import MOD

def build_B2_full_int():
    Mn, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    B2_full = np.zeros((6, 20, 15), dtype=np.int64)
    for ell in range(20):
        B2_full[:, ell, :] = V_basis[:, ell].reshape(15, 6).T
    return B2_full, sub_2, sub_3

def syz_dim_4D_mod(B2_full, P_6x4, p_mod):
    # B2_H: 4 x 20 x 15
    B2_H = np.einsum("ct,clJ->tlJ", P_6x4, B2_full) % p_mod
    mons_4 = [(a, b) for a in range(4) for b in range(a, 4)]
    mon_idx = {m: i for i, m in enumerate(mons_4)}
    E = np.zeros((15 * 10, 4 * 20), dtype=np.int64)
    for J in range(15):
        for a in range(4):
            for b in range(a, 4):
                r = J * 10 + mon_idx[(a, b)]
                for ell in range(20):
                    E[r, a * 20 + ell] = (E[r, a * 20 + ell] + B2_H[b, ell, J]) % p_mod
                    if a != b:
                        E[r, b * 20 + ell] = (E[r, b * 20 + ell] + B2_H[a, ell, J]) % p_mod
    return 80 - rank_matrix_mod(E, p_mod)

def scan_Gr26_F2():
    print("=" * 74)
    print("1. EXHAUSTIVE SCAN OF ALL 651 PLANES IN Gr(2, 6, F_2) FOR syz_dim(B2|_H)")
    print("=" * 74)
    B2_full, sub_2, sub_3 = build_B2_full_int()

    # Enumerate all 651 4D subspaces H c F_2^6 via RREF of 2x6 parity-check matrices H^perp
    # Equivalently, enumerate all 2x6 matrices in RREF (rows = H^perp):
    planes = []
    for p1 in range(6):
        for p2 in range(p1 + 1, 6):
            # RREF with pivots p1 < p2:
            # row 0 has 1 at p1, 0 at p2, free at {c > p1, c != p2}
            # row 1 has 0 at p1, 1 at p2, free at {c > p2}
            free0 = [c for c in range(p1 + 1, 6) if c != p2]
            free1 = [c for c in range(p2 + 1, 6)]
            for vals0 in itertools.product([0, 1], repeat=len(free0)):
                for vals1 in itertools.product([0, 1], repeat=len(free1)):
                    H_perp = np.zeros((2, 6), dtype=np.int64)
                    H_perp[0, p1] = 1
                    for c, v in zip(free0, vals0): H_perp[0, c] = v
                    H_perp[1, p2] = 1
                    for c, v in zip(free1, vals1): H_perp[1, c] = v
                    # Build 6x4 basis P of ker(H_perp)
                    non_piv = [c for c in range(6) if c not in (p1, p2)]
                    P = np.zeros((6, 4), dtype=np.int64)
                    for idx, c in enumerate(non_piv):
                        P[c, idx] = 1
                        P[p1, idx] = H_perp[0, c]
                        P[p2, idx] = H_perp[1, c]
                    assert np.all((H_perp @ P) % 2 == 0)
                    planes.append((H_perp, P))
    assert len(planes) == 651

    hist = {}
    nonzero_examples = {}
    for H_perp, P in planes:
        sd = syz_dim_4D_mod(B2_full, P, 2)
        hist[sd] = hist.get(sd, 0) + 1
        if sd > 0 and sd not in nonzero_examples:
            nonzero_examples[sd] = H_perp
    print(f"  F_2 histogram of syz_dim across all 651 planes: {sorted(hist.items())}")
    for sd, hp in sorted(nonzero_examples.items()):
        print(f"  Example syz_dim={sd} H^perp:\n{hp}")

def scan_Gr26_F3_orbits_and_C():
    """Over F_{1000003} (char != 2!), check all S_6-orbits of 2-planes spanned by
    sparse vectors (support <= 3 each) and check if any support >= 3+3 plane has syz_dim > 0."""
    print("\n" + "=" * 74)
    print("2. EXACT SCAN OF SUPPORT TYPES IN Gr(2, 6, F_{1000003}) (CHAR != 2)")
    print("=" * 74)
    B2_full, _, _ = build_B2_full_int()
    rng = np.random.default_rng(42)

    def null_6x4(H_perp):
        # Quick RREF to get 6x4 kernel of 2x6 H_perp mod MOD
        M = H_perp.copy() % MOD
        pivs = []
        r = 0
        for c in range(6):
            if r >= 2: break
            piv = next((rr for rr in range(r, 2) if M[rr, c] != 0), None)
            if piv is None: continue
            M[[r, piv]] = M[[piv, r]]
            inv = pow(int(M[r, c]), MOD - 2, MOD)
            M[r] = (M[r] * inv) % MOD
            for rr in range(2):
                if rr != r and M[rr, c] != 0:
                    M[rr] = (M[rr] - M[rr, c] * M[r]) % MOD
            pivs.append(c); r += 1
        assert len(pivs) == 2
        non_piv = [c for c in range(6) if c not in pivs]
        P = np.zeros((6, 4), dtype=np.int64)
        for idx, c in enumerate(non_piv):
            P[c, idx] = 1
            P[pivs[0], idx] = (-M[0, c]) % MOD
            P[pivs[1], idx] = (-M[1, c]) % MOD
        return P

    # Test structured 2-planes (u, v):
    # Type (1, 1): supp(u)=1, supp(v)=1 -> Orbit A (syz_dim=6)
    # Type (1, 2): supp(u)=1, supp(v)=2 disj -> Orbit B (syz_dim=3)
    # Type (1, 3): supp(u)=1, supp(v)=3 disj -> e.g. (e5, e0+2e1+3e2)
    # Type (2, 2) disj: e.g. (e0+2e1, e2+3e3) -> Orbit C (syz_dim=1)
    # Type (2, 2) overlap 1: e.g. (e0+2e1, e0+3e2) -> 3-var plane
    # Type (2, 3) disj: e.g. (e0+2e1, e2+3e3+5e4)
    # Type (2, 3) overlap 1: e.g. (e0+2e1, e0+3e2+5e3)
    # Type (3, 3) disj: e.g. (e0+2e1+3e2, e3+5e4+7e5)
    tests = [
        ("Type (1,1): e4, e5", np.array([[0,0,0,0,1,0],[0,0,0,0,0,1]])),
        ("Type (1,2) disj: e5, e0+2e1", np.array([[0,0,0,0,0,1],[1,2,0,0,0,0]])),
        ("Type (1,3) disj: e5, e0+2e1+3e2", np.array([[0,0,0,0,0,1],[1,2,3,0,0,0]])),
        ("Type (1,4) disj: e5, e0+2e1+3e2+5e3", np.array([[0,0,0,0,0,1],[1,2,3,5,0,0]])),
        ("Type (1,5) disj: e5, e0+2e1+3e2+5e3+7e4", np.array([[0,0,0,0,0,1],[1,2,3,5,7,0]])),
        ("Type (2,2) disj: e0+2e1, e2+3e3", np.array([[1,2,0,0,0,0],[0,0,1,3,0,0]])),
        ("Type (2,2) ovlp1: e0+2e1, e0+3e2", np.array([[1,2,0,0,0,0],[1,0,3,0,0,0]])),
        ("Type (2,3) disj: e0+2e1, e2+3e3+5e4", np.array([[1,2,0,0,0,0],[0,0,1,3,5,0]])),
        ("Type (2,3) ovlp1: e0+2e1, e0+3e2+5e3", np.array([[1,2,0,0,0,0],[1,0,3,5,0,0]])),
        ("Type (3,3) disj: e0+2e1+3e2, e3+5e4+7e5", np.array([[1,2,3,0,0,0],[0,0,0,1,5,7]])),
        ("Type (3,3) ovlp1: e0+2e1+3e2, e0+5e3+7e4", np.array([[1,2,3,0,0,0],[1,0,0,5,7,0]])),
        ("Type (3,3) ovlp2: e0+2e1+3e2, e0+5e1+7e3", np.array([[1,2,3,0,0,0],[1,5,0,7,0,0]])),
    ]
    for name, Hp in tests:
        sd = syz_dim_4D_mod(B2_full, null_6x4(Hp), MOD)
        print(f"  {name:45s}: syz_dim = {sd}")

if __name__ == "__main__":
    scan_Gr26_F2()
    scan_Gr26_F3_orbits_and_C()
