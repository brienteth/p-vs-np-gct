"""Prof. Wigner Round 7 (GAP 2):
Exact exhaustive classification of ALL 11,011 planes in Gr(2, 6, F_3) (char = 3 != 2)
via S_6 x F_3^* orbit reduction (~0.5s runtime!).
Determines the EXACT dimension and orbit structure of Z_2 = {H^perp in Gr(2, 6) : syz_dim(B_{2,full}|_H) > 0}.
"""
import itertools
import numpy as np
import sys
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council/prof-noether")
from general_n2k_noether import build_Mn
from apolar_higher_betti_probe import rank_matrix_mod

def rref_2x6_mod3(M):
    M = M.copy() % 3
    r = 0
    for c in range(6):
        if r >= 2: break
        piv = next((rr for rr in range(r, 2) if M[rr, c] != 0), None)
        if piv is None: continue
        M[[r, piv]] = M[[piv, r]]
        if M[r, c] == 2:
            M[r] = (2 * M[r]) % 3
        for rr in range(2):
            if rr != r and M[rr, c] != 0:
                M[rr] = (M[rr] - M[rr, c] * M[r]) % 3
        r += 1
    return tuple(int(x) for x in M.reshape(12))

def main():
    print("=" * 74)
    print("EXHAUSTIVE S_6-ORBIT CLASSIFICATION OF ALL 11,011 PLANES IN Gr(2, 6, F_3)")
    print("=" * 74)
    Mn, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    B2_full = np.zeros((6, 20, 15), dtype=np.int64)
    for ell in range(20):
        B2_full[:, ell, :] = V_basis[:, ell].reshape(15, 6).T

    # Enumerate all 11,011 2x6 RREF matrices over F_3
    planes = {}
    for p1 in range(6):
        for p2 in range(p1 + 1, 6):
            free0 = [c for c in range(p1 + 1, 6) if c != p2]
            free1 = [c for c in range(p2 + 1, 6)]
            for vals0 in itertools.product([0, 1, 2], repeat=len(free0)):
                for vals1 in itertools.product([0, 1, 2], repeat=len(free1)):
                    H_perp = np.zeros((2, 6), dtype=np.int64)
                    H_perp[0, p1] = 1
                    for c, v in zip(free0, vals0): H_perp[0, c] = v
                    H_perp[1, p2] = 1
                    for c, v in zip(free1, vals1): H_perp[1, c] = v
                    key = tuple(int(x) for x in H_perp.reshape(12))
                    planes[key] = H_perp
    assert len(planes) == 11011, f"Expected 11011, got {len(planes)}"

    # Partition into S_6 orbits! (Wait: also sign flips of coordinates b_i -> -b_i if needed, S_6 alone is fast!)
    # Actually S_6 has 720 elements; let's just pick unvisited key and generate its S_6 orbit!
    perms = list(itertools.permutations(range(6)))
    visited = set()
    orbits = []
    for key, H_perp in planes.items():
        if key in visited:
            continue
        orb = set()
        for p in perms:
            H_p = H_perp[:, p]
            k_p = rref_2x6_mod3(H_p)
            orb.add(k_p)
        visited.update(orb)
        orbits.append((H_perp, len(orb)))

    print(f"Partitioned all 11,011 planes into {len(orbits)} S_6-orbits!")

    def syz_dim_mod3(H_perp):
        # Compute 6x4 kernel P
        pivs = []
        for r in range(2):
            pivs.append(next(c for c in range(6) if H_perp[r, c] != 0))
        non_piv = [c for c in range(6) if c not in pivs]
        P = np.zeros((6, 4), dtype=np.int64)
        for idx, c in enumerate(non_piv):
            P[c, idx] = 1
            P[pivs[0], idx] = (-H_perp[0, c]) % 3
            P[pivs[1], idx] = (-H_perp[1, c]) % 3
        B2_H = np.einsum("ct,clJ->tlJ", P, B2_full) % 3
        mons_4 = [(a, b) for a in range(4) for b in range(a, 4)]
        mon_idx = {m: i for i, m in enumerate(mons_4)}
        E = np.zeros((150, 80), dtype=np.int64)
        for J in range(15):
            for a in range(4):
                for b in range(a, 4):
                    r = J * 10 + mon_idx[(a, b)]
                    for ell in range(20):
                        E[r, a * 20 + ell] = (E[r, a * 20 + ell] + B2_H[b, ell, J]) % 3
                        if a != b:
                            E[r, b * 20 + ell] = (E[r, b * 20 + ell] + B2_H[a, ell, J]) % 3
        return 80 - rank_matrix_mod(E, 3)

    hist_planes = {}
    nonzero_orbits = []
    for H_perp, sz in orbits:
        sd = syz_dim_mod3(H_perp)
        hist_planes[sd] = hist_planes.get(sd, 0) + sz
        if sd > 0:
            nonzero_orbits.append((sd, sz, H_perp))

    print(f"F_3 syz_dim histogram across ALL 11,011 planes: {sorted(hist_planes.items())}")
    print(f"Nonzero syz_dim orbits ({len(nonzero_orbits)} orbits, total {11011 - hist_planes[0]} planes):")
    for sd, sz, hp in sorted(nonzero_orbits, key=lambda x: (-x[0], x[1])):
        supp_cols = int(np.sum(np.any(hp != 0, axis=0)))
        print(f"  syz_dim={sd}, orbit_size={sz:4d}, col_support={supp_cols}: H^perp={hp.tolist()}")

if __name__ == "__main__":
    main()
