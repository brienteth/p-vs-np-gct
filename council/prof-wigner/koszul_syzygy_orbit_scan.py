"""Prof. Wigner Round 6: Exact S_6 decomposition, codimension-k restricted syzygies of B_{2,full}|_H,
and S_6-orbit / Koszul classification of im(E_in) cap im(E_out) for t_B in {2, 3, 4}.
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
    return B2_full, V_basis, sub_2, sub_3

def s6_irrep_decomp_exact():
    print("=" * 74)
    print("1. EXACT S_6 IRREP DECOMPOSITION (IDENTITY CLASS FIXED)")
    print("=" * 74)
    Mn, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    sub2_idx = {s: i for i, s in enumerate(sub_2)}
    perms = list(itertools.permutations(range(6)))
    def cyc_type(p):
        vis = [False]*6; cs = []
        for i in range(6):
            if not vis[i]:
                c = 0; cur = i
                while not vis[cur]:
                    vis[cur] = True; cur = p[cur]; c += 1
                cs.append(c)
        return tuple(sorted(cs, reverse=True))
    cls_rep = {}; cls_size = {}
    for p in perms:
        ct = cyc_type(p)
        cls_size[ct] = cls_size.get(ct, 0) + 1
        if ct not in cls_rep:
            cls_rep[ct] = p
    cls_list = sorted(cls_rep.keys()) # (1,1,1,1,1,1) is first!
    id_idx = cls_list.index((1,1,1,1,1,1))
    assert id_idx == 0

    def count_fixed_ordered(p, parts):
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

    parts_6 = [
        (6,), (5,1), (4,2), (4,1,1), (3,3), (3,2,1),
        (3,1,1,1), (2,2,2), (2,2,1,1), (2,1,1,1,1), (1,1,1,1,1,1)
    ]
    M_chars = np.zeros((11, 11), dtype=int)
    for i, mu in enumerate(parts_6):
        for j, ct in enumerate(cls_list):
            M_chars[i, j] = count_fixed_ordered(cls_rep[ct], mu)

    weights = np.array([cls_size[ct] for ct in cls_list], dtype=float) / 720.0
    V_chars = np.zeros((11, 11), dtype=int)
    for i in range(11):
        v = M_chars[i].astype(float).copy()
        for k in range(i):
            inner = np.sum(v * V_chars[k] * weights)
            v -= round(inner) * V_chars[k]
        norm2 = np.sum(v * v * weights)
        assert abs(norm2 - 1.0) < 1e-9
        V_chars[i] = np.round(v).astype(int)

    P_S = V_basis.astype(float) @ V_basis.astype(float).T / 3.0
    O_in_mask = np.array([1.0 if c in J else 0.0 for J in sub_2 for c in range(6)])
    O_out_mask = 1.0 - O_in_mask
    P_Oin = np.diag(O_in_mask)
    P_Oout = np.diag(O_out_mask)

    def perm_mat_90(p):
        M = np.zeros((90, 90), dtype=float)
        for j_idx, J in enumerate(sub_2):
            jp_idx = sub2_idx[tuple(sorted((p[J[0]], p[J[1]])))]
            for c in range(6):
                M[jp_idx * 6 + p[c], j_idx * 6 + c] = 1.0
        return M

    def decompose(char_vec, name):
        mults = []
        total_dim = 0
        for i, lam in enumerate(parts_6):
            m = int(round(np.sum(char_vec * V_chars[i] * weights)))
            if m != 0:
                mults.append(f"{m}*{lam}[{V_chars[i,0]}]")
                total_dim += m * V_chars[i, 0]
        print(f"  {name:26s} (dim {total_dim:3d}) = " + " + ".join(mults))

    for name, P in [
        ("F[b]_1^{15} (total)", np.eye(90)),
        ("O_in (c in J)", P_Oin),
        ("O_out (c not in J)", P_Oout),
        ("S_{6,3}", P_S),
        ("O_out / S_{6,3}", P_Oout - P_S),
        ("Quotient F[b]_1^15/S_{6,3}", np.eye(90) - P_S),
    ]:
        ch = np.array([np.trace(perm_mat_90(cls_rep[ct]) @ P) for ct in cls_list])
        decompose(ch, name)

    # Also im(E_full) in F[b]_2^{15}
    B2_full, _, _, _ = build_B2_full_int()
    mons_2 = [(a, b) for a in range(6) for b in range(a, 6)]
    mon_idx = {m: i for i, m in enumerate(mons_2)}
    E_full = np.zeros((315, 120), dtype=float)
    for ell in range(20):
        for c_u in range(6):
            col = c_u * 20 + ell
            for J in range(15):
                for c_b in range(6):
                    val = float(B2_full[c_b, ell, J])
                    if val != 0:
                        m = (min(c_u, c_b), max(c_u, c_b))
                        E_full[J * 21 + mon_idx[m], col] += val
    Q_E, _ = np.linalg.qr(E_full)
    P_imE = Q_E @ Q_E.T
    def perm_mat_315(p):
        M = np.zeros((315, 315), dtype=float)
        for j_idx, J in enumerate(sub_2):
            jp_idx = sub2_idx[tuple(sorted((p[J[0]], p[J[1]])))]
            for m_i, (a, b) in enumerate(mons_2):
                pa, pb = p[a], p[b]
                M[jp_idx * 21 + mon_idx[(min(pa, pb), max(pa, pb))], j_idx * 21 + m_i] = 1.0
        return M
    ch_315 = np.array([np.trace(perm_mat_315(cls_rep[ct])) for ct in cls_list])
    ch_imE = np.array([np.trace(perm_mat_315(cls_rep[ct]) @ P_imE) for ct in cls_list])
    decompose(ch_315, "F[b]_2^{15} (total)")
    decompose(ch_imE, "im(E_full)")
    decompose(ch_315 - ch_imE, "F[b]_2^{15} / im(E_full)")

def restricted_syzygies_on_subspaces():
    """For B_{2,full}(b) restricted to a subspace H = span(P_{6 x d}) of F^6 (dim d = 6-k),
    compute the degree-1 syzygies u(t) B_{2,full}(P t) = 0 in F[t_0..t_{d-1}]!
    Notice: ANY degree-1 left syzygy of [B_{2,in}; B_{2,out}] with t_B protruding rows
    whose u_out coefficients vanish on H induces a degree-1 syzygy of B_{2,in}|_H!
    Wait: even better, compute for B_{2,full}|_H across coordinate and structured H of codim k=1..4!
    """
    print("\n" + "=" * 74)
    print("2. DEGREE-1 SYZYGIES OF B_{2,full}(b)|_H ON CODIMENSION-k SUBSPACES H")
    print("=" * 74)
    B2_full, _, sub_2, sub_3 = build_B2_full_int()
    rng = np.random.default_rng(2026)

    def syz_dim_on_H(P_mat):
        # P_mat is 6 x d (parameterizes b = P_mat @ t, t in F^d)
        d = P_mat.shape[1]
        # B2_H[t_idx, ell, J] = sum_c P_mat[c, t_idx] * B2_full[c, ell, J] mod MOD
        B2_H = np.einsum("ct,clJ->tlJ", P_mat, B2_full) % MOD
        mons_d = [(a, b) for a in range(d) for b in range(a, d)]
        mon_idx = {m: i for i, m in enumerate(mons_d)}
        n_mons = len(mons_d)
        # Unknowns: d * 20; Equations: 15 * n_mons
        E = np.zeros((15 * n_mons, d * 20), dtype=np.int64)
        for J in range(15):
            for a in range(d):
                for b in range(a, d):
                    r = J * n_mons + mon_idx[(a, b)]
                    for ell in range(20):
                        E[r, a * 20 + ell] = (E[r, a * 20 + ell] + B2_H[b, ell, J]) % MOD
                        if a != b:
                            E[r, b * 20 + ell] = (E[r, b * 20 + ell] + B2_H[a, ell, J]) % MOD
        rk = rank_matrix_mod(E, MOD)
        return d * 20 - rk

    for k in [1, 2, 3, 4]:
        d = 6 - k
        # 1) Coordinate subspaces (zero out k variables)
        P_coord = np.eye(6, dtype=np.int64)[:, :d]
        dim_coord = syz_dim_on_H(P_coord)
        # 2) Equal-variable / sum-zero subspaces (e.g. b_0 = b_1, etc.)
        # Build P where first k pairs/variables are set equal or sum=0
        P_eq = np.zeros((6, d), dtype=np.int64)
        for i in range(d):
            P_eq[i, i] = 1
        # set remaining k vars equal to var 0
        for i in range(d, 6):
            P_eq[i, 0] = 1
        dim_eq = syz_dim_on_H(P_eq)
        # 3) Sum-zero subspace of codim k (k=1: sum b_i=0; k=2: b0+b1+b2=0, b3+b4+b5=0, etc.)
        # 4) Generic random H of dim d (10 trials)
        gen_dims = []
        for _ in range(10):
            P_rand = rng.integers(0, MOD, size=(6, d), dtype=np.int64)
            gen_dims.append(syz_dim_on_H(P_rand))
        print(f"  codim k={k} (dim H={d}): coord_zero_k syz_dim={dim_coord}, equal_vars syz_dim={dim_eq}, generic_H max={max(gen_dims)} (vals={set(gen_dims)})")

def analyze_hilbert_and_noether_witnesses():
    """Analyze the exact F(b)-rank s_1 and constant wire support c of syzygy spaces
    generated by t_B = 2, 3, 4 protruding rows constructed from Koszul cancellations."""
    print("\n" + "=" * 74)
    print("3. SYZYGY DIMENSION & FUNCTION-FIELD RANK s_1 FOR t_B = 2, 3, 4 KOSZUL WITNESSES")
    print("=" * 74)
    B2_full, _, sub_2, sub_3 = build_B2_full_int()
    sub2_idx = {s: i for i, s in enumerate(sub_2)}
    sub3_idx = {s: i for i, s in enumerate(sub_3)}
    rng = np.random.default_rng(77)

    def inspect_witness(name, drop_s3_indices, r_out_tensor):
        """drop_s3_indices: list of t_B+1 indices dropped from B2_full (keeping 19-t_B wires in S_{6,3}),
        r_out_tensor: shape (6, t_B, 15) mod MOD."""
        t_B = r_out_tensor.shape[1]
        keep = [i for i in range(20) if i not in drop_s3_indices]
        assert len(keep) == 19 - t_B
        B2_in = B2_full[:, keep, :] # (6, 19-t_B, 15)
        B2 = np.concatenate([B2_in, r_out_tensor], axis=1) # (6, 19, 15)
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
        # Compute exact nullspace of E mod MOD via RREF!
        # Let's compute RREF over F_MOD
        M = E.copy()
        rows, cols = M.shape
        piv_cols = []
        r_ptr = 0
        for c in range(cols):
            piv = None
            for r in range(r_ptr, rows):
                if M[r, c] != 0:
                    piv = r; break
            if piv is None:
                continue
            M[[r_ptr, piv]] = M[[piv, r_ptr]]
            inv = pow(int(M[r_ptr, c]), MOD - 2, MOD)
            M[r_ptr] = (M[r_ptr] * inv) % MOD
            nz = np.where(M[:, c] != 0)[0]
            for r in nz:
                if r != r_ptr:
                    M[r] = (M[r] - M[r, c] * M[r_ptr]) % MOD
            piv_cols.append(c)
            r_ptr += 1
        free_cols = [c for c in range(cols) if c not in piv_cols]
        basis = []
        for fc in free_cols:
            vec = np.zeros(cols, dtype=np.int64)
            vec[fc] = 1
            for idx_p, pc in enumerate(piv_cols):
                vec[pc] = (-M[idx_p, fc]) % MOD
            basis.append(vec)
        syz_dim = len(basis)
        if syz_dim == 0:
            print(f"  [{name}] t_B={t_B}: syz_dim = 0")
            return
        # Form B1_max(b) with all syz_dim syzygies as rows: shape (6, syz_dim, 19)
        B1_max = np.zeros((6, syz_dim, 19), dtype=np.int64)
        for s_i, vec in enumerate(basis):
            B1_max[:, s_i, :] = vec.reshape(6, 19)
        # Check F(b)-rank s_1 at a generic point
        b_pt = rng.integers(1, MOD, size=6, dtype=np.int64)
        B1_val = sum(int(b_pt[c]) * B1_max[c] for c in range(6)) % MOD
        s1_max = rank_matrix_mod(B1_val, MOD)
        # Check constant middle-wire support c = dim_F R(B1_max) = rank of (6*syz_dim) x 19 matrix!
        c_wires = rank_matrix_mod(B1_max.reshape(6 * syz_dim, 19), MOD)
        # Also check rank of u_in alone and u_out alone
        c_in = rank_matrix_mod(B1_max[:, :, :19-t_B].reshape(6 * syz_dim, 19-t_B), MOD)
        rk_B2 = rank_matrix_mod(sum(int(b_pt[c]) * B2[c] for c in range(6)) % MOD, MOD)
        print(f"  [{name}] t_B={t_B}: F-syz_dim={syz_dim}, F(b)-rank s1_max={s1_max}, const wire support c={c_wires} (c_in={c_in}), rank(B2)={rk_B2}")

    # Witness 1: Hilbert #55 (t_B = 2)
    # Keep all 17 wires except {0,4,5}, {1,4,5}, plus 1 extra? Wait: 19 - 2 = 17 wires in S_{6,3}, so drop 3 from 20!
    # In Hilbert #55, only {0,4,5} and {1,4,5} are needed in B2_in, so drop e.g. {2,3,4}, {2,3,5}, {3,4,5} (3 wires), keeping {0,4,5} and {1,4,5}!
    r_hilb = np.zeros((6, 2, 15), dtype=np.int64)
    # r1(b) = b0 e_{1,5} - b1 e_{0,5}
    r_hilb[0, 0, sub2_idx[(1, 5)]] = 1; r_hilb[1, 0, sub2_idx[(0, 5)]] = MOD - 1
    # r2(b) = b0 e_{1,4} - b1 e_{0,4}
    r_hilb[0, 1, sub2_idx[(1, 4)]] = 1; r_hilb[1, 1, sub2_idx[(0, 4)]] = MOD - 1
    inspect_witness("Hilbert #55 (t_B=2)", [sub3_idx[(2,3,4)], sub3_idx[(2,3,5)], sub3_idx[(3,4,5)]], r_hilb)

    # Witness 2: Shared-edge t_B = 3 (3 vertices {0,1,2} sharing edge {4,5})
    # r_i(b) = b_4 e_{i,5} + b_5 e_{i,4} for i=0,1,2 (3 rows!) -> v_{i,4,5} - r_i = b_i e_{4,5}
    # Drop 4 wires from 20 (NOT {0,4,5}, {1,4,5}, {2,4,5}!)
    r_edge3 = np.zeros((6, 3, 15), dtype=np.int64)
    for i in range(3):
        r_edge3[4, i, sub2_idx[(i, 5)]] = 1
        r_edge3[5, i, sub2_idx[(i, 4)]] = 1
    inspect_witness("Shared-edge t_B=3 (3 syz)", [sub3_idx[(0,1,2)], sub3_idx[(0,1,3)], sub3_idx[(0,2,3)], sub3_idx[(1,2,3)]], r_edge3)

    # Witness 3: Hilbert-style 3-edge protruding around (0,1,2) on {4,5}:
    # r1 = b0 e_{1,5} - b1 e_{0,5}, r2 = b0 e_{1,4} - b1 e_{0,4}, plus r3 = b0 e_{2,5} - b2 e_{0,5}? Wait:
    # For {0,4,5}, {1,4,5}, {2,4,5}: v_{i,4,5} = b_i e_{4,5} + b_4 e_{i,5} + b_5 e_{i,4}.
    # Wait: how does Hilbert's t_B=2 work? b0 v_{1,4,5} - b1 v_{0,4,5} = b4 r1 + b5 r2.
    # For 3 indices {0,1,2} with 2 shared variables {4,5}, there are 3 pairs {0,1}, {0,2}, {1,2},
    # needing r_{01,4}, r_{01,5}, r_{02,4}, r_{02,5}, r_{12,4}, r_{12,5} = 4 independent rows:
    # Actually span({b_i e_{j,5} - b_j e_{i,5} : i,j in {0,1,2}}) has dim 2 (since b2 r_{01} + b0 r_{12} + b1 r_{20} = 0)!
    # Wait! Does span({b_i e_{j,c} - b_j e_{i,c} : i,j in {0,1,2}, c in {4,5}}) have dim 4 or dim 2*2=4?
    # Let's test t_B = 4 with r_{01,5}, r_{02,5}, r_{01,4}, r_{02,4}!
    r_h4 = np.zeros((6, 4, 15), dtype=np.int64)
    r_h4[0, 0, sub2_idx[(1, 5)]] = 1; r_h4[1, 0, sub2_idx[(0, 5)]] = MOD - 1
    r_h4[0, 1, sub2_idx[(1, 4)]] = 1; r_h4[1, 1, sub2_idx[(0, 4)]] = MOD - 1
    r_h4[0, 2, sub2_idx[(2, 5)]] = 1; r_h4[2, 2, sub2_idx[(0, 5)]] = MOD - 1
    r_h4[0, 3, sub2_idx[(2, 4)]] = 1; r_h4[2, 3, sub2_idx[(0, 4)]] = MOD - 1
    inspect_witness("Koszul-3-cycle t_B=4 (b_c e_{4,5} elim)", [sub3_idx[(0,1,3)], sub3_idx[(0,2,3)], sub3_idx[(1,2,3)], sub3_idx[(3,4,5)], sub3_idx[(1,3,4)]], r_h4)

    # Witness 4: Noether #58 (t_B = 4)
    r_noether = np.zeros((6, 4, 15), dtype=np.int64)
    for i in range(4):
        r_noether[4, i, sub2_idx[(i, 5)]] = 1
        r_noether[5, i, sub2_idx[(i, 4)]] = 1
    inspect_witness("Noether #58 (t_B=4)", [sub3_idx[(0,1,2)], sub3_idx[(0,1,3)], sub3_idx[(0,2,3)], sub3_idx[(1,2,3)], sub3_idx[(0,1,4)]], r_noether)

    # Witness 5: What about TWO disjoint Hilbert #55 pairs at t_B = 4?
    # Pair 1: {0,4,5}, {1,4,5} with r1, r2
    # Pair 2: {2,0,1}, {3,0,1} with r3 = b2 e_{3,1} - b3 e_{2,1}, r4 = b2 e_{3,0} - b3 e_{2,0}
    r_2disj = np.zeros((6, 4, 15), dtype=np.int64)
    r_2disj[0, 0, sub2_idx[(1, 5)]] = 1; r_2disj[1, 0, sub2_idx[(0, 5)]] = MOD - 1
    r_2disj[0, 1, sub2_idx[(1, 4)]] = 1; r_2disj[1, 1, sub2_idx[(0, 4)]] = MOD - 1
    r_2disj[2, 2, sub2_idx[(1, 3)]] = 1; r_2disj[3, 2, sub2_idx[(1, 2)]] = MOD - 1
    r_2disj[2, 3, sub2_idx[(0, 3)]] = 1; r_2disj[3, 3, sub2_idx[(0, 2)]] = MOD - 1
    inspect_witness("2-Disjoint-Pairs t_B=4", [sub3_idx[(2,4,5)], sub3_idx[(3,4,5)], sub3_idx[(2,3,4)], sub3_idx[(2,3,5)], sub3_idx[(0,2,4)]], r_2disj)

    # Witness 6: What about PURE O_in protruding rows? E.g., r_i = b_i e_{4,5}? Wait: 4 in {4,5}, so b_4 e_{4,5} is in O_in!
    # Actually in Noether #58, v_{i,4,5} - r_i = b_i e_{4,5} IS in O_out! Because i not in {4,5}!
    # What if we take t_B = 3 or 4 rows in O_in (c in J)?
    # e.g. e_{0,1} * b_0, e_{0,1} * b_1, ... Can O_in couple to im(E_full)?
    # Let's check: does ANY vector in O_in lie in im(E_full)? Wait: im(E_full) is quadratic!
    # Take r_1 = b_4 e_{4,5}, r_2 = b_5 e_{4,5}: can b_4*r_1 + b_5*r_2 lie in im(E_full)?
    r_Oin = np.zeros((6, 4, 15), dtype=np.int64)
    r_Oin[4, 0, sub2_idx[(4, 5)]] = 1
    r_Oin[5, 1, sub2_idx[(4, 5)]] = 1
    r_Oin[0, 2, sub2_idx[(0, 1)]] = 1
    r_Oin[1, 3, sub2_idx[(0, 1)]] = 1
    inspect_witness("Pure O_in t_B=4", [0, 1, 2, 3, 4], r_Oin)

if __name__ == "__main__":
    s6_irrep_decomp_exact()
    restricted_syzygies_on_subspaces()
    analyze_hilbert_and_noether_witnesses()
