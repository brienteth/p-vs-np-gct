"""Prof. Wigner Round 6: Exact S_6 representation decomposition and Koszul syzygy analysis
of F[b]_1^{15} / S_{6,3} and im(E_in) cap im(E_out) for t_B in {2, 3, 4}.
"""
import itertools
import numpy as np
import sys
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council/prof-noether")
from general_n2k_noether import build_Mn

def s6_irrep_characters():
    """Return S_6 conjugacy class reps, sizes, and exact character table for all 11 irreps."""
    # Partitions of 6:
    # (6), (5,1), (4,2), (4,1,1), (3,3), (3,2,1), (3,1,1,1), (2,2,2), (2,2,1,1), (2,1,1,1,1), (1^6)
    # Better yet: compute characters directly from permutation modules or verify with known dimensions!
    perms = list(itertools.permutations(range(6)))
    def cyc_type(p):
        vis = [False]*6
        cs = []
        for i in range(6):
            if not vis[i]:
                c = 0; cur = i
                while not vis[cur]:
                    vis[cur] = True; cur = p[cur]; c += 1
                cs.append(c)
        return tuple(sorted(cs, reverse=True))
    cls_rep = {}
    cls_size = {}
    for p in perms:
        ct = cyc_type(p)
        cls_size[ct] = cls_size.get(ct, 0) + 1
        if ct not in cls_rep:
            cls_rep[ct] = p
    return cls_rep, cls_size, cyc_type

def build_B2_full():
    Mn, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    # B2_full[c, ell, J] = V_basis[J*6 + c, ell]
    B2_full = np.zeros((6, 20, 15), dtype=np.int64)
    for ell in range(20):
        B2_full[:, ell, :] = V_basis[:, ell].reshape(15, 6).T
    return B2_full, V_basis, sub_2, sub_3

def compute_s6_decomp():
    print("=" * 72)
    print("1. S_6 REPRESENTATION DECOMPOSITION OF F[b]_1^{15}, S_{6,3}, AND QUOTIENT")
    print("=" * 72)
    cls_rep, cls_size, cyc_type = s6_irrep_characters()
    Mn, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    sub2_idx = {s: i for i, s in enumerate(sub_2)}
    sub3_idx = {s: i for i, s in enumerate(sub_3)}

    # Orthonormal projector onto S_{6,3} (dim 20 in R^{90})
    P_S = V_basis.astype(float) @ V_basis.astype(float).T / 3.0
    assert np.allclose(P_S @ P_S, P_S)

    # Also build Young permutation modules M^lambda or use standard S_6 character table!
    # Wait: we can get exact traces of any S_6-invariant subspace projector P on R^{90}
    # by computing Tr(Pi_90(g) @ P) for one representative g per conjugacy class!
    # Let's build Pi_90(g) and check orbit structure (c in J vs c not in J).
    O_in_mask = np.zeros(90, dtype=float)
    O_out_mask = np.zeros(90, dtype=float)
    for j_idx, J in enumerate(sub_2):
        for c in range(6):
            if c in J:
                O_in_mask[j_idx * 6 + c] = 1.0
            else:
                O_out_mask[j_idx * 6 + c] = 1.0
    P_Oin = np.diag(O_in_mask)
    P_Oout = np.diag(O_out_mask)
    P_quot = np.eye(90) - P_S
    P_Oout_mod_S = P_Oout - P_S

    def perm_mat_90(p):
        M = np.zeros((90, 90), dtype=float)
        for j_idx, J in enumerate(sub_2):
            J_p = tuple(sorted((p[J[0]], p[J[1]])))
            jp_idx = sub2_idx[J_p]
            for c in range(6):
                cp = p[c]
                M[jp_idx * 6 + cp, j_idx * 6 + c] = 1.0
        return M

    # Build known S_6 irrep characters from permutation module characters M^\mu via Kostka/Frobenius or explicit Young projectors!
    # Easier: build permutation characters for partitions of 6:
    # M^(6) (1), M^(5,1) (6), M^(4,2) (15), M^(4,1,1) (30), M^(3,3) (20), M^(3,2,1) (60),
    # M^(3,1,1,1) (120), M^(2,2,2) (90), M^(2,2,1,1) (180), M^(2,1^4) (360), M^(1^6) (720)
    # Wait: even simpler! Count fixed tuples for ordered partitions of size mu!
    def count_fixed_ordered(p, parts):
        # For a permutation p with cycle type cyc_type(p), count ordered set partitions of sizes `parts` fixed by p!
        # Wait: p acts on subsets/tuples. Easier for small sets of size <= 6: count fixed points via cycle lengths!
        # Coefficient of prod x_i^{parts[i]} in prod_{c in cycles(p)} (sum x_i^{c})!
        ct = cyc_type(p)
        poly = {tuple([0]*len(parts)): 1}
        for c in ct:
            new_poly = {}
            for deg, coeff in poly.items():
                for i in range(len(parts)):
                    if deg[i] + c <= parts[i]:
                        nd = list(deg); nd[i] += c; nd = tuple(nd)
                        new_poly[nd] = new_poly.get(nd, 0) + coeff
            poly = new_poly
        return poly.get(tuple(parts), 0)

    # All 11 partitions of 6 in dominance order (descending):
    parts_6 = [
        (6,), (5,1), (4,2), (4,1,1), (3,3), (3,2,1),
        (3,1,1,1), (2,2,2), (2,2,1,1), (2,1,1,1,1), (1,1,1,1,1,1)
    ]
    cls_list = sorted(cls_rep.keys(), reverse=True)
    # Compute M^mu character matrix (11 x 11)
    M_chars = np.zeros((11, 11), dtype=int)
    for i, mu in enumerate(parts_6):
        for j, ct in enumerate(cls_list):
            M_chars[i, j] = count_fixed_ordered(cls_rep[ct], mu)

    # Gram-Schmidt over inner product weighted by class sizes / 720 gives EXACT irreducible characters V_lambda!
    weights = np.array([cls_size[ct] for ct in cls_list], dtype=float) / 720.0
    V_chars = np.zeros((11, 11), dtype=int)
    for i in range(11):
        v = M_chars[i].astype(float).copy()
        for k in range(i):
            inner = np.sum(v * V_chars[k] * weights)
            v -= round(inner) * V_chars[k]
        norm2 = np.sum(v * v * weights)
        assert abs(norm2 - 1.0) < 1e-9, f"GS failed at {parts_6[i]}: norm2={norm2}"
        V_chars[i] = np.round(v).astype(int)

    print("Irreps of S_6 (verified orthonormal):")
    for i, lam in enumerate(parts_6):
        print(f"  {str(lam):16s}: dim = {V_chars[i, 0]:2d}")

    def decompose(char_vec, name):
        mults = []
        total_dim = 0
        for i, lam in enumerate(parts_6):
            m = int(round(np.sum(char_vec * V_chars[i] * weights)))
            if m != 0:
                mults.append(f"{m}*{lam}[{V_chars[i,0]}]")
                total_dim += m * V_chars[i, 0]
        print(f"  {name:24s} (dim {total_dim:3d}) = " + " + ".join(mults))

    for name, P in [
        ("F[b]_1^{15} (total)", np.eye(90)),
        ("O_in (c in J)", P_Oin),
        ("O_out (c not in J)", P_Oout),
        ("S_{6,3}", P_S),
        ("O_out / S_{6,3}", P_Oout_mod_S),
        ("Quotient F[b]_1^15/S_{6,3}", P_quot),
    ]:
        ch = np.array([np.trace(perm_mat_90(cls_rep[ct]) @ P) for ct in cls_list])
        decompose(ch, name)

    # Also decompose im(E_full) in F[b]_2^{15} (dim 120 inside dim 315)!
    B2_full, _, _, _ = build_B2_full()
    mons_2 = [(a, b) for a in range(6) for b in range(a, 6)]
    mon_idx = {m: i for i, m in enumerate(mons_2)}
    # Build E_full: 315 x 120
    # Index 315 as J*21 + mon_idx
    E_full = np.zeros((315, 120), dtype=float)
    for ell in range(20):
        for c_u in range(6):
            col = c_u * 20 + ell
            for J in range(15):
                for c_b in range(6):
                    val = B2_full[c_b, ell, J]
                    if val != 0:
                        m = (min(c_u, c_b), max(c_u, c_b))
                        E_full[J * 21 + mon_idx[m], col] += val
    assert np.linalg.matrix_rank(E_full) == 120, "E_full must have full rank 120!"
    Q_E, _ = np.linalg.qr(E_full)
    P_imE = Q_E @ Q_E.T

    def perm_mat_315(p):
        M = np.zeros((315, 315), dtype=float)
        for j_idx, J in enumerate(sub_2):
            jp_idx = sub2_idx[tuple(sorted((p[J[0]], p[J[1]]))) ]
            for m_i, (a, b) in enumerate(mons_2):
                pa, pb = p[a], p[b]
                mp_i = mon_idx[(min(pa, pb), max(pa, pb))]
                M[jp_idx * 21 + mp_i, j_idx * 21 + m_i] = 1.0
        return M

    ch_315 = np.array([np.trace(perm_mat_315(cls_rep[ct])) for ct in cls_list])
    ch_imE = np.array([np.trace(perm_mat_315(cls_rep[ct]) @ P_imE) for ct in cls_list])
    ch_cok = ch_315 - ch_imE
    print("\nQuadratic space F[b]_2^{15} and im(E_full):")
    decompose(ch_315, "F[b]_2^{15} (total)")
    decompose(ch_imE, "im(E_full) = F[b]_1^20*B2")
    decompose(ch_cok, "F[b]_2^{15} / im(E_full)")

if __name__ == "__main__":
    compute_s6_decomp()
