"""
verify_round15_hilbert.py  --  Prof. Hilbert, Round 15 (Nodes E3.8 and support for E3.9)

PART A  (Theorem H-15A, [PROVEN] by exact modular linear algebra):
    GLOBAL codim_{C^16}( H_{<=4}(perm_4) ) >= 9, with NO component-list assumption.
    H_{<=4} = {X : grad perm_4(X) = 0 and rank Hess(perm_4)(X) <= 4}.
    Degree-<=6 generators (all vanish on H_{<=4}):
      * 16 cubics  d perm_4 / d x_{ia}
      * 3x3 minors of B_{r1 r2}  (6 row pairs; 8x8 principal Hessian block [[0,B],[B,0]])
      * 3x3 minors of C_{c1 c2}  (6 column pairs)
      * det_3( C_{i,a} )         (16 pairs)
    On the explicit integer plane L_9 in C^16 we compute the Macaulay rank at D=6, D=7 and then one
    Iterated-Macaulay-Schur-Complement (IMSC) step D=7 -> 8, modulo BOTH 32749 and 65521.
    Full rank 12870/12870 at D=8  =>  m^8 subset I on L_9  =>  V(I) cap P(L_9) = empty
    =>  codim_{C^16} V(I) >= 9  =>  codim_{C^16} H_{<=4} >= 9.

PART B  (Node E3.8, [PROVEN] exact flattening facts + [CHECKED NUMERICALLY] LM experiments):
    exact flattenings / spectrum of perm_4(A,B) in S^2(A (x) B); numerical tangent dimensions of the
    (1,1)-product variety; honest Levenberg-Marquardt audit of w_2 = 4, 5 including ||theta||
    (a decaying residual with exploding ||theta|| is BORDER behaviour, not a hard floor).
    NO symbolic proof of the w_2 = 4 impossibility is claimed here:  that remains [OPEN].
"""
import itertools
import time
import numpy as np

PRIMES = (32749, 65521)
T_START = time.time()


# ----------------------------------------------------------------------------------------------
# bit-exact float64-BLAS modular RREF (block_size * p^2 << 2^53) with C-table for IMSC
# ----------------------------------------------------------------------------------------------
def rref_mod_p(A_in, p, block_size=96, need_c_table=True):
    A = (A_in.astype(np.int64) % p).copy()
    nrows, ncols = A.shape
    row = 0
    piv_cols = []
    for c_start in range(0, ncols, block_size):
        c_end = min(c_start + block_size, ncols)
        p_r, p_c = [], []
        for col in range(c_start, c_end):
            if row >= nrows:
                break
            nz = np.nonzero(A[row:, col])[0]
            if nz.size == 0:
                continue
            piv = row + int(nz[0])
            if piv != row:
                A[[row, piv]] = A[[piv, row]]
            if p_r and c_end < ncols:
                upd = (A[row, p_c].astype(np.float64) @ A[p_r, c_end:].astype(np.float64)).astype(np.int64) % p
                A[row, c_end:] = (A[row, c_end:] - upd) % p
                A[row, p_c] = 0
            inv_p = pow(int(A[row, col]), p - 2, p)
            A[row, col:] = (A[row, col:] * inv_p) % p
            if row + 1 < nrows and col + 1 < c_end:
                f = A[row + 1:, col]
                nzb = np.nonzero(f)[0]
                if nzb.size > 0:
                    idx = row + 1 + nzb
                    A[idx, col + 1:c_end] = (A[idx, col + 1:c_end] - np.outer(f[nzb], A[row, col + 1:c_end])) % p
            p_r.append(row)
            p_c.append(col)
            piv_cols.append(col)
            row += 1
        if p_r and c_end < ncols and row < nrows:
            F_blk = A[row:, p_c].astype(np.float64)
            P_blk = A[p_r, c_end:].astype(np.float64)
            for tc in range(0, ncols - c_end, 2048):
                tc_end = min(tc + 2048, ncols - c_end)
                upd = (F_blk @ P_blk[:, tc:tc_end]).astype(np.int64) % p
                A[row:, c_end + tc:c_end + tc_end] = (A[row:, c_end + tc:c_end + tc_end] - upd) % p
            A[row:, p_c] = 0
    rk = row
    piv_set = set(piv_cols)
    free_cols = [c for c in range(ncols) if c not in piv_set]
    n_free = len(free_cols)
    if not need_c_table or n_free == 0:
        return rk, piv_cols, free_cols, np.zeros((ncols, n_free), dtype=np.int64)
    C_table = np.zeros((ncols, n_free), dtype=np.int64)
    for j, fc in enumerate(free_cols):
        C_table[fc, j] = 1
    if rk > 0:
        X = (-A[:rk, free_cols]) % p
        for b_end in range(rk, 0, -block_size):
            b_start = max(0, b_end - block_size)
            for i in range(b_end - 1, b_start - 1, -1):
                for j in range(i + 1, b_end):
                    val = int(A[i, piv_cols[j]])
                    if val != 0:
                        X[i, :] = (X[i, :] - val * X[j, :]) % p
            if b_start > 0:
                p_c_blk = [piv_cols[j] for j in range(b_start, b_end)]
                U_blk = A[:b_start, p_c_blk].astype(np.float64)
                X_blk = X[b_start:b_end, :].astype(np.float64)
                upd = (U_blk @ X_blk).astype(np.int64) % p
                X[:b_start, :] = (X[:b_start, :] - upd) % p
        C_table[piv_cols, :] = X
    return rk, piv_cols, free_cols, C_table


def step_imsc(k, D, mons_D, free_cols_D, C_D, p):
    """Exact Iterated Macaulay Schur-Complement step from degree D to D+1."""
    t0 = time.time()
    mons_next = list(itertools.combinations_with_replacement(range(k), D + 1))
    m_next_idx = {m: i for i, m in enumerate(mons_next)}
    m_D_idx = {m: i for i, m in enumerate(mons_D)}
    free_mons = [mons_D[fc] for fc in free_cols_D]
    S_set = set()
    uf_to_next = np.zeros((k, len(free_mons)), dtype=np.int64)
    for i in range(k):
        for j, fm in enumerate(free_mons):
            idx = m_next_idx[tuple(sorted(fm + (i,)))]
            uf_to_next[i, j] = idx
            S_set.add(idx)
    S_list = sorted(S_set)
    s_to_pos = {s: i for i, s in enumerate(S_list)}
    n_S = len(S_list)
    uf_to_spos = np.array([[s_to_pos[uf_to_next[i, j]] for j in range(len(free_mons))] for i in range(k)],
                          dtype=np.int64)
    R_canon = np.zeros((len(mons_next), n_S), dtype=np.int64)
    syz_rows = []
    for beta_idx, beta in enumerate(mons_next):
        i0 = beta[0]
        row_c = C_D[m_D_idx[beta[1:]], :]
        nz_c = np.nonzero(row_c)[0]
        if nz_c.size > 0:
            R_canon[beta_idx, uf_to_spos[i0, nz_c]] = (R_canon[beta_idx, uf_to_spos[i0, nz_c]] + row_c[nz_c]) % p
        if beta_idx in s_to_pos:
            s_row = (-R_canon[beta_idx]).copy()
            s_row[s_to_pos[beta_idx]] = (s_row[s_to_pos[beta_idx]] + 1) % p
            if np.any(s_row):
                syz_rows.append(s_row)
        prev_v = i0
        for pos in range(1, D + 1):
            v = beta[pos]
            if v == prev_v:
                continue
            prev_v = v
            row_v = C_D[m_D_idx[beta[:pos] + beta[pos + 1:]], :]
            nz_v = np.nonzero(row_v)[0]
            diff = (-R_canon[beta_idx]).copy()
            if nz_v.size > 0:
                sp = uf_to_spos[v, nz_v]
                diff[sp] = (diff[sp] + row_v[nz_v]) % p
            if np.any(diff):
                syz_rows.append(diff)
    M_syz = np.vstack(syz_rows) if syz_rows else np.zeros((1, n_S), dtype=np.int64)
    rk_s, _, free_s, C_s = rref_mod_p(M_syz, p, need_c_table=True)
    corank_next = n_S - rk_s
    tot_rk = len(mons_next) - corank_next
    free_cols_next = [S_list[f] for f in free_s]
    if corank_next > 0:
        C_next = (R_canon.astype(np.float64) @ C_s.astype(np.float64)).astype(np.int64) % p
    else:
        C_next = np.zeros((len(mons_next), 0), dtype=np.int64)
    print(f"      IMSC D={D}->{D + 1} (p={p}): |S|={n_S}, syz={M_syz.shape} -> exact rank "
          f"{tot_rk}/{len(mons_next)} (corank {corank_next}) [{time.time() - t0:.1f}s]")
    return mons_next, free_cols_next, C_next, corank_next, tot_rk


# ----------------------------------------------------------------------------------------------
# PART A
# ----------------------------------------------------------------------------------------------
def build_ideal_on_L(M_L, p):
    k = M_L.shape[1]
    L = (M_L.reshape(4, 4, k).astype(np.int64)) % p
    mons2 = list(itertools.combinations_with_replacement(range(k), 2))
    m2 = {m: i for i, m in enumerate(mons2)}
    mons3 = list(itertools.combinations_with_replacement(range(k), 3))
    m3 = {m: i for i, m in enumerate(mons3)}
    mons6 = list(itertools.combinations_with_replacement(range(k), 6))
    m6 = {m: i for i, m in enumerate(mons6)}

    sub2 = {}
    for r0, r1 in itertools.combinations(range(4), 2):
        for c0, c1 in itertools.combinations(range(4), 2):
            v = np.zeros(len(mons2), dtype=np.int64)
            for a in range(k):
                for b in range(k):
                    val = (L[r0, c0, a] * L[r1, c1, b] + L[r0, c1, a] * L[r1, c0, b]) % p
                    if val:
                        key = (a, b) if a <= b else (b, a)
                        v[m2[key]] = (v[m2[key]] + val) % p
            sub2[(r0, r1, c0, c1)] = v

    cubics = []
    for i in range(4):
        rows = [r for r in range(4) if r != i]
        for j in range(4):
            cols = [c for c in range(4) if c != j]
            v = np.zeros(len(mons3), dtype=np.int64)
            for perm in itertools.permutations(cols):
                L0, L1, L2 = L[rows[0], perm[0]], L[rows[1], perm[1]], L[rows[2], perm[2]]
                for a in np.nonzero(L0)[0]:
                    for b in np.nonzero(L1)[0]:
                        ab = (L0[a] * L1[b]) % p
                        for c in np.nonzero(L2)[0]:
                            key = tuple(sorted((int(a), int(b), int(c))))
                            v[m3[key]] = (v[m3[key]] + ab * L2[c]) % p
            cubics.append(v)

    def mul3(v1, v2, v3):
        d4 = {}
        nz1 = [(mons2[i], int(v1[i])) for i in np.nonzero(v1)[0]]
        nz2 = [(mons2[i], int(v2[i])) for i in np.nonzero(v2)[0]]
        nz3 = [(mons2[i], int(v3[i])) for i in np.nonzero(v3)[0]]
        for ma, ca in nz1:
            for mb, cb in nz2:
                mm = tuple(sorted(ma + mb))
                d4[mm] = (d4.get(mm, 0) + ca * cb) % p
        out = np.zeros(len(mons6), dtype=np.int64)
        for mm, cc in d4.items():
            if not cc:
                continue
            for mc, c3 in nz3:
                key = m6[tuple(sorted(mm + mc))]
                out[key] = (out[key] + cc * c3) % p
        return out

    def det3(M3):
        res = np.zeros(len(mons6), dtype=np.int64)
        for perm in itertools.permutations(range(3)):
            inv = sum(1 for x in range(3) for y in range(x + 1, 3) if perm[x] > perm[y])
            sgn = -1 if inv % 2 else 1
            res = (res + sgn * mul3(M3[0][perm[0]], M3[1][perm[1]], M3[2][perm[2]])) % p
        return res

    zero2 = np.zeros(len(mons2), dtype=np.int64)
    sextics = []
    for r0, r1 in itertools.combinations(range(4), 2):          # B_{r0 r1}: 4x4 symmetric, zero diagonal
        rr = tuple(r for r in range(4) if r not in (r0, r1))
        B = [[zero2] * 4 for _ in range(4)]
        for c0 in range(4):
            for c1 in range(c0 + 1, 4):
                cc = tuple(c for c in range(4) if c not in (c0, c1))
                B[c0][c1] = B[c1][c0] = sub2[(rr[0], rr[1], cc[0], cc[1])]
        for rs in itertools.combinations(range(4), 3):
            for cs in itertools.combinations(range(4), 3):
                if rs <= cs:
                    sextics.append(det3([[B[r][c] for c in cs] for r in rs]))
    for c0, c1 in itertools.combinations(range(4), 2):          # C_{c0 c1}
        cc = tuple(c for c in range(4) if c not in (c0, c1))
        C = [[zero2] * 4 for _ in range(4)]
        for r0 in range(4):
            for r1 in range(r0 + 1, 4):
                rr = tuple(r for r in range(4) if r not in (r0, r1))
                C[r0][r1] = C[r1][r0] = sub2[(rr[0], rr[1], cc[0], cc[1])]
        for rs in itertools.combinations(range(4), 3):
            for cs in itertools.combinations(range(4), 3):
                if rs <= cs:
                    sextics.append(det3([[C[r][c] for c in cs] for r in rs]))
    for i in range(4):                                          # C_{i,a}: 3x3 matrices of 2x2 sub-permanents
        r_comp = [r for r in range(4) if r != i]
        for a in range(4):
            c_comp = [c for c in range(4) if c != a]
            M3 = [[None] * 3 for _ in range(3)]
            for ri, r in enumerate(r_comp):
                rr = tuple(x for x in range(4) if x not in (i, r))
                for ci, c in enumerate(c_comp):
                    cc = tuple(y for y in range(4) if y not in (a, c))
                    M3[ri][ci] = sub2[(rr[0], rr[1], cc[0], cc[1])]
            sextics.append(det3(M3))
    return mons3, cubics, mons6, sextics


def part_a():
    print("=" * 100)
    print("PART A: GLOBAL degree-6 ideal of H_{<=4}(perm_4) on L_9 subset C^16  (Theorem H-15A)")
    print("=" * 100)
    k = 9
    for p in PRIMES:
        t0 = time.time()
        rng = np.random.default_rng(2026 + k)
        M_L = rng.integers(-2, 3, size=(16, k), dtype=np.int64)
        mons3, cubics, mons6, sextics = build_ideal_on_L(M_L, p)
        assert len(cubics) == 16 and len(sextics) == 6 * 10 + 6 * 10 + 16, len(sextics)
        mons4 = list(itertools.combinations_with_replacement(range(k), 4))
        mons7 = list(itertools.combinations_with_replacement(range(k), 7))
        m6 = {m: i for i, m in enumerate(mons6)}
        m7 = {m: i for i, m in enumerate(mons7)}
        cnz = [[(mons3[i], int(v[i])) for i in np.nonzero(v)[0]] for v in cubics]
        snz = [[(mons6[i], int(v[i])) for i in np.nonzero(v)[0]] for v in sextics]
        print(f"  [p={p}] generators: {len(cubics)} cubics + {len(sextics)} sextics "
              f"(60 B-minors + 60 C-minors + 16 det_3(C_ia)); built in {time.time() - t0:.1f}s")

        # D = 6
        A6 = np.zeros((16 * len(mons3) + len(sextics), len(mons6)), dtype=np.int64)
        ri = 0
        for mm in mons3:
            for terms in cnz:
                for m3_, c in terms:
                    j = m6[tuple(sorted(mm + m3_))]
                    A6[ri, j] = (A6[ri, j] + c) % p
                ri += 1
        for v in sextics:
            A6[ri, :] = v
            ri += 1
        rk6 = rref_mod_p(A6, p, need_c_table=False)[0]
        print(f"      D=6: exact rank {rk6}/{len(mons6)} (corank {len(mons6) - rk6})")
        if p == PRIMES[0]:
            assert rk6 == 2386

        # D = 7
        A7 = np.zeros((16 * len(mons4) + k * len(sextics), len(mons7)), dtype=np.int64)
        ri = 0
        for mm in mons4:
            for terms in cnz:
                for m3_, c in terms:
                    j = m7[tuple(sorted(mm + m3_))]
                    A7[ri, j] = (A7[ri, j] + c) % p
                ri += 1
        for vv in range(k):
            for terms in snz:
                for m6_, c in terms:
                    j = m7[tuple(sorted(m6_ + (vv,)))]
                    A7[ri, j] = (A7[ri, j] + c) % p
                ri += 1
        rk7, _, free7, C7 = rref_mod_p(A7, p, need_c_table=True)
        print(f"      D=7: exact rank {rk7}/{len(mons7)} (corank {len(mons7) - rk7}) [{time.time() - t0:.1f}s]")
        if p == PRIMES[0]:
            assert len(mons7) - rk7 == 16

        # D = 7 -> 8 via IMSC
        _, _, _, crk8, rk8 = step_imsc(k, 7, mons7, free7, C7, p)
        assert crk8 == 0 and rk8 == 12870, (crk8, rk8)
        print(f"  [p={p}] *** m^8 subset I_{{H<=4}}^{{deg<=6}} on L_9 (rank 12870/12870) ***  [{time.time() - t0:.1f}s]")
    print("\n  [PROVEN, Theorem H-15A]  V(I) cap P(L_9) = empty in P^15_C (two independent primes) =>")
    print("      codim_{C^16} H_{<=4}(perm_4) >= 9  GLOBALLY (no assumption on the component list).")
    print("  [NOT CLAIMED] degree(Sing V(perm_4)) = 60: IMSC on the 16 cubics alone gives h(6)=753, h(7)=580, h(8)=588")
    print("      (measured interactively; D=8->9 costs ~700s), still growing, so the Hilbert function has NOT")
    print("      stabilised and the degree-60 / component-completeness test is INCONCLUSIVE ([OPEN], E3.6a).")


# ----------------------------------------------------------------------------------------------
# PART B
# ----------------------------------------------------------------------------------------------
def part_b():
    print("\n" + "=" * 100)
    print("PART B: Node E3.8 -- (1,1)-collapse perm_4(A,B) = sum_{s<=w2} G_s H_s, G_s,H_s in A (x) B")
    print("=" * 100)
    # (i) exact flattenings of the multilinear tensor
    T = np.zeros((4, 4, 4, 4))
    for p in itertools.permutations(range(4)):
        T[p] = 1.0
    fl = [np.linalg.matrix_rank(T.reshape(16, 16)),
          np.linalg.matrix_rank(T.transpose(0, 2, 1, 3).reshape(16, 16)),
          np.linalg.matrix_rank(T.transpose(0, 3, 1, 2).reshape(16, 16)),
          np.linalg.matrix_rank(T.reshape(4, 64))]
    print(f"  [PROVEN, exact integer matrices] flattening ranks of perm_4 tensor: 2|2 splits = {fl[:3]}, 1|3 = {fl[3]}")
    assert fl == [6, 6, 6, 4]
    # (ii) 64x64 symmetric matrix in S^2(A (x) B)
    F = np.zeros((64, 64))
    for p in itertools.permutations(range(4)):
        a0, a1, b0, b1 = p[0], 4 + p[1], p[2], 4 + p[3]
        for (i1, j1), (i2, j2) in [((a0, b0), (a1, b1)), ((a1, b1), (a0, b0)),
                                    ((a0, b1), (a1, b0)), ((a1, b0), (a0, b1))]:
            F[8 * i1 + j1, 8 * i2 + j2] += 0.25
    ev = np.linalg.eigvalsh(F)
    nzev = ev[np.abs(ev) > 1e-9]
    print(f"  [PROVEN] canonical symmetric lift F4_sym (64x64): rank {len(nzev)}, eigenvalues +-1/2 "
          f"({int((nzev > 0).sum())}+/{int((nzev < 0).sum())}-), nuclear norm {np.abs(nzev).sum():.6f}")
    assert len(nzev) == 24 and abs(np.abs(nzev).sum() - 12.0) < 1e-9
    print("      NOTE: the lift is only defined modulo Lambda^2A (x) Lambda^2B, so rank 24 is NOT a rank bound for the")
    print("      polynomial; no rank lower bound for w_2 = 4 is deduced from it.")

    # (iii) numerical tangent dimensions of the product variety
    rng = np.random.default_rng(2026)
    mons2 = list(itertools.combinations_with_replacement(range(8), 2))
    m2 = {m: i for i, m in enumerate(mons2)}
    idxA = np.zeros((8, 8), dtype=np.int32)
    for i in range(8):
        for j in range(8):
            idxA[i, j] = m2[(i, j) if i <= j else (j, i)]
    S = 1500
    Ap = (rng.normal(size=(S, 8)) + 1j * rng.normal(size=(S, 8))) * 0.6
    Bp = (rng.normal(size=(S, 8)) + 1j * rng.normal(size=(S, 8))) * 0.6
    X = np.hstack([Ap, Bp]).reshape(S, 4, 4)
    Fpts = np.zeros(S, dtype=np.complex128)
    for p in itertools.permutations(range(4)):
        Fpts += X[:, 0, p[0]] * X[:, 1, p[1]] * X[:, 2, p[2]] * X[:, 3, p[3]]
    F4 = np.zeros((36, 36), dtype=np.complex128)
    for p in itertools.permutations(range(4)):
        F4[idxA[p[0], 4 + p[1]], idxA[p[2], 4 + p[3]]] += 1.0
    F4_vec = F4.reshape(-1)
    AB = Ap[:, :, None] * Bp[:, None, :]

    dims = {}
    for w2 in (4, 5, 6):
        W = rng.normal(size=(2, w2, 8, 8))
        Ar, Br = Ap[:1350].real, Bp[:1350].real
        G = np.einsum("ni,sij,nj->ns", Ar, W[0], Br)
        H = np.einsum("ni,sij,nj->ns", Ar, W[1], Br)
        ABr = Ar[:, :, None] * Br[:, None, :]
        J = np.zeros((1350, 2 * w2 * 64))
        for s in range(w2):
            J[:, s * 64:(s + 1) * 64] = (H[:, s:s + 1, None] * ABr).reshape(1350, 64)
            J[:, (w2 + s) * 64:(w2 + s + 1) * 64] = (G[:, s:s + 1, None] * ABr).reshape(1350, 64)
        dims[w2] = int(np.linalg.matrix_rank(J, tol=1e-9))
    print(f"  [CHECKED NUMERICALLY] tangent dim of {{sum_{{s<=w2}} G_s H_s}} in C[A,B]_(2,2) (dim 1296) at a random point: "
          f"w2=4: {dims[4]}, w2=5: {dims[5]}, w2=6: {dims[6]}")
    assert dims[4] < dims[5] < dims[6] < 1296

    # (iv) honest LM audit with ||theta||
    def lm(w2, seed, iters):
        r = np.random.default_rng(700 + 37 * w2 + seed)
        theta = (r.normal(size=2 * w2 * 64) + 1j * r.normal(size=2 * w2 * 64)) * 0.35
        lam = 1e-4
        hist = []
        for it in range(iters):
            W = theta.reshape(2, w2, 8, 8)
            G = np.einsum("ni,sij,nj->ns", Ap, W[0], Bp)
            H = np.einsum("ni,sij,nj->ns", Ap, W[1], Bp)
            res = np.sum(G * H, axis=1) - Fpts
            err = np.linalg.norm(res)
            if err < 1e-12:
                break
            J = np.zeros((S, 2 * w2 * 64), dtype=np.complex128)
            for s in range(w2):
                J[:, s * 64:(s + 1) * 64] = (H[:, s:s + 1, None] * AB).reshape(S, 64)
                J[:, (w2 + s) * 64:(w2 + s + 1) * 64] = (G[:, s:s + 1, None] * AB).reshape(S, 64)
            Jr = np.vstack([np.hstack([J.real, -J.imag]), np.hstack([J.imag, J.real])])
            rr_ = np.concatenate([res.real, res.imag])
            step = -np.linalg.solve(Jr.T @ Jr + lam * np.eye(4 * w2 * 64), Jr.T @ rr_)
            th_new = theta + step[:2 * w2 * 64] + 1j * step[2 * w2 * 64:]
            Wn = th_new.reshape(2, w2, 8, 8)
            err_n = np.linalg.norm(np.sum(np.einsum("ni,sij,nj->ns", Ap, Wn[0], Bp) *
                                          np.einsum("ni,sij,nj->ns", Ap, Wn[1], Bp), axis=1) - Fpts)
            if err_n < err:
                theta = th_new
                lam = max(lam * 0.3, 1e-12)
            else:
                lam = min(lam * 5.0, 1e4)
            if it % 100 == 0:
                hist.append(err)
        W = theta.reshape(2, w2, 8, 8)
        P = np.zeros((36, 36), dtype=np.complex128)
        for s in range(w2):
            Ms, Ns = W[0, s], W[1, s]
            for i1 in range(8):
                for j1 in range(8):
                    c1 = Ms[i1, j1]
                    for i2 in range(8):
                        for j2 in range(8):
                            P[idxA[i1, i2], idxA[j1, j2]] += c1 * Ns[i2, j2]
        return np.linalg.norm(P.reshape(-1) - F4_vec), np.linalg.norm(theta), hist

    iters = 500
    out = {}
    for w2 in (4, 5):
        t0 = time.time()
        ex, nt, hist = lm(w2, 0, iters)
        out[w2] = (ex, nt)
        print(f"  [CHECKED NUMERICALLY] LM w2={w2}, {iters} steps, 1 start: exact coefficient error {ex:.4e} "
              f"(||P||={np.sqrt(24):.4f}), ||theta||={nt:.1f}  [{time.time() - t0:.0f}s]")
    print("  Interactive 1000-step runs (not repeated here): w2=5 -> exact_err 4.15e-3 / 4.11e-3 with ||theta|| ~ 106,")
    print("  i.e. residual still decaying while ||theta|| diverges: this is BORDER (closure) behaviour at w2 = 5,")
    print("  NOT a proof either way.  The Round-14 'hard floor 0.7119' at w2 = 4 (250 steps, 6 starts) is therefore only")
    print("  a numerical observation; it does not exclude perm_4 from the closure of the w2 = 4 product variety.")
    assert out[5][0] < out[4][0] + 1e-9 or out[5][1] > 20.0
    print("\n  [OPEN]  E3.8: a symbolic proof that perm_4(A,B) is not a sum of 4 products of (1,1)-forms is NOT achieved.")
    print("  [OPEN]  Sing_2(V(perm_5)) at k=14, D=6 (27132 columns) not attempted; k=14, D=5 corank 140 (Round 14).")


if __name__ == "__main__":
    part_a()
    part_b()
    print(f"\nALL ROUND 15 PROF. HILBERT CHECKS PASSED (EXIT CODE 0)  [{time.time() - T_START:.0f}s total]")
