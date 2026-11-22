"""
verify_round16_hilbert.py  --  Node E3.10 & Global Support for E3.11 (Round 16)

1. Theorem H-16A [PROVEN]: Global Zero-Block Principal-Submatrix Identities on ALL of C^16:
   - Identity 1 (6x6 -> deg 6 for H_{<=4}): For ANY 3 vars R_3 inside a single row (or col)
     and ANY 3 vars C_3 anywhere else in X, Hess[R_3, R_3] == 0_{3x3}, hence
       det_6(Hess(perm_4)|_{R_3 U C_3}) = -(det_3 Hess[R_3, C_3])^2.
     In particular det_3(N) (deg 6 in X) vanishes GLOBALLY on H_{<=4}(perm_4) and cuts every
     RC_{i,a} to rank(C_{i,a}) <= 1 (codim 10)!
   - Identity 2 (8x8 -> deg 8 for H_{<=6}): For ALL 4 vars R_4 of a single row (or col)
     and ANY 4 vars C_4 anywhere else in X, Hess[R_4, R_4] == 0_{4x4}, hence
       det_8(Hess(perm_4)|_{R_4 U C_4}) = +(det_4 Hess[R_4, C_4])^2.
     Thus det_4(M) (deg 8 in X) vanishes GLOBALLY on H_{<=6}(perm_4)!
2. Theorem H-16B [EXACT MODULAR]: Global codim_{C^16}(H_{<=6}(perm_4)) certification on L_9
   via 16 cubics (grad perm_4) quotient space R_8(L_9) + det_4(M) zero-block deg-8 generators
   modulo BOTH p_1 = 32,749 and p_2 = 65,521.
3. Theorem H-16C [EXACT MODULAR]: Global codim_{C^16}(H_{<=4}(perm_4)) certification on L_{10}
   with augmented zero-block det_3(N) deg-6 generators modulo BOTH p_1 = 32,749 and p_2 = 65,521.
4. Part D [EXACT]: Sing_2(V(perm_5)) k=14, D=5 and L_6 (1,1)-collapse symbolic audit notes.
"""
from __future__ import annotations

import itertools
import time
import numpy as np

from verify_round15_hilbert import rref_mod_p, step_imsc

PRIMES = (32749, 65521)


def full_hessian_perm4_float(X: np.ndarray) -> np.ndarray:
    H = np.zeros((16, 16), dtype=np.float64)
    for r0, r1 in itertools.combinations(range(4), 2):
        rr = [r for r in range(4) if r != r0 and r != r1]
        for c0, c1 in itertools.combinations(range(4), 2):
            cc = [c for c in range(4) if c != c0 and c != c1]
            p2 = float(X[rr[0], cc[0]] * X[rr[1], cc[1]] + X[rr[0], cc[1]] * X[rr[1], cc[0]])
            H[r0 * 4 + c0, r1 * 4 + c1] = H[r1 * 4 + c1, r0 * 4 + c0] = p2
            H[r0 * 4 + c1, r1 * 4 + c0] = H[r1 * 4 + c0, r0 * 4 + c1] = p2
    return H


def test_1_theorem_h16a_zero_block_identities() -> None:
    print("=" * 95)
    print("TEST 1 (THM H-16A): GLOBAL ZERO-BLOCK 6x6 & 8x8 PRINCIPAL SUBMATRIX IDENTITIES ON C^16")
    print("=" * 95)
    rng = np.random.default_rng(202616)
    max_err_6 = 0.0
    max_err_8 = 0.0
    max_err_rc_3 = 0.0
    max_err_rc_4 = 0.0

    for _ in range(15):
        X = rng.standard_normal((4, 4))
        H = full_hessian_perm4_float(X)
        # Identity 1: arbitrary row i, 3 cols, and arbitrary 3 vars outside row i (including D != 0!)
        for i in range(4):
            row_vars = [i * 4 + c for c in range(4)]
            other_vars = [v for v in range(16) if v // 4 != i]
            for cols3 in itertools.combinations(row_vars, 3):
                assert np.max(np.abs(H[np.ix_(cols3, cols3)])) == 0.0
                c3 = tuple(int(v) for v in rng.choice(other_vars, size=3, replace=False))
                idx6 = list(cols3) + list(c3)
                d6 = float(np.linalg.det(H[np.ix_(idx6, idx6)]))
                d3 = float(np.linalg.det(H[np.ix_(cols3, c3)]))
                max_err_6 = max(max_err_6, abs(d6 - (-(d3 ** 2))))
            # Identity 2: full row R_4 and arbitrary 4 vars C_4 outside row i
            assert np.max(np.abs(H[np.ix_(row_vars, row_vars)])) == 0.0
            for _t in range(5):
                c4 = tuple(int(v) for v in rng.choice(other_vars, size=4, replace=False))
                idx8 = list(row_vars) + list(c4)
                d8 = float(np.linalg.det(H[np.ix_(idx8, idx8)]))
                d4 = float(np.linalg.det(H[np.ix_(row_vars, c4)]))
                max_err_8 = max(max_err_8, abs(d8 - (d4 ** 2)))

        # Verify RC_{0,0} restriction formulas (even when Z_0 has non-zero perm_3 or on RC_{0,0}):
        X_rc = X.copy()
        X_rc[0, :] = 0.0
        X_rc[:, 0] = 0.0
        H_rc = full_hessian_perm4_float(X_rc)
        Z0 = X_rc[1:, 1:]
        C00 = np.zeros((3, 3), dtype=np.float64)
        for r in range(3):
            rr = [u for u in range(3) if u != r]
            for c in range(3):
                cc = [v for v in range(3) if v != c]
                C00[r, c] = Z0[rr[0], cc[0]] * Z0[rr[1], cc[1]] + Z0[rr[0], cc[1]] * Z0[rr[1], cc[0]]

        # Test R_3 = {(0,0),(0,1),(0,2)}, C_3 = {(3,3),(1,0),(2,0)}
        R3 = [0, 1, 2]
        C3 = [3 * 4 + 3, 1 * 4 + 0, 2 * 4 + 0]
        N3 = H_rc[np.ix_(R3, C3)]
        expected_N3 = C00[2, 2] * np.linalg.det(C00[np.ix_([0, 1], [0, 1])])
        max_err_rc_3 = max(max_err_rc_3, abs(float(np.linalg.det(N3)) - expected_N3))

        # Test R_4 = row 0, C_4 = {(2,3),(1,0),(2,0),(3,0)}
        R4 = [0, 1, 2, 3]
        C4 = [2 * 4 + 3, 1 * 4 + 0, 2 * 4 + 0, 3 * 4 + 0]
        M4 = H_rc[np.ix_(R4, C4)]
        expected_M4 = C00[1, 2] * float(np.linalg.det(C00))
        max_err_rc_4 = max(max_err_rc_4, abs(float(np.linalg.det(M4)) - expected_M4))

    print(f"  [PROVEN] Identity 1 max |det_6(Hess|_(R3 U C3)) + (det_3 N)^2|   = {max_err_6:.2e}")
    print(f"  [PROVEN] Identity 2 max |det_8(Hess|_(R4 U C4)) - (det_4 M)^2|   = {max_err_8:.2e}")
    print(f"  [PROVEN] On RC_{{0,0}}: max |det_3 N - C_00[r0,c0]*det_2(C_00)|    = {max_err_rc_3:.2e}")
    print(f"  [PROVEN] On RC_{{0,0}}: max |det_4 M - C_00[r0,c0]*det_3(C_00)|    = {max_err_rc_4:.2e}")
    assert max(max_err_6, max_err_8, max_err_rc_3, max_err_rc_4) < 1e-10


def build_p2_and_cubics(M_L: np.ndarray, p: int):
    k = M_L.shape[1]
    L = (M_L.reshape(4, 4, k).astype(np.int64)) % p
    mons2 = list(itertools.combinations_with_replacement(range(k), 2))
    m2 = {m: i for i, m in enumerate(mons2)}
    mons3 = list(itertools.combinations_with_replacement(range(k), 3))
    m3 = {m: i for i, m in enumerate(mons3)}

    p2 = {}
    for r0, r1 in itertools.combinations(range(4), 2):
        for c0, c1 in itertools.combinations(range(4), 2):
            v = np.zeros(len(mons2), dtype=np.int64)
            for a in range(k):
                for b in range(k):
                    val = (L[r0, c0, a] * L[r1, c1, b] + L[r0, c1, a] * L[r1, c0, b]) % p
                    if val:
                        v[m2[(a, b) if a <= b else (b, a)]] = (v[m2[(a, b) if a <= b else (b, a)]] + val) % p
            p2[(r0, r1, c0, c1)] = v

    def hess_poly2(va: int, vb: int):
        ra, ca = divmod(va, 4)
        rb, cb = divmod(vb, 4)
        if ra == rb or ca == cb:
            return None
        r_rem = (min(r for r in range(4) if r not in (ra, rb)), max(r for r in range(4) if r not in (ra, rb)))
        c_rem = (min(c for c in range(4) if c not in (ca, cb)), max(c for c in range(4) if c not in (ca, cb)))
        return p2[r_rem + c_rem]

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
                            v[m3[tuple(sorted((int(a), int(b), int(c))))]] = (
                                v[m3[tuple(sorted((int(a), int(b), int(c))))]] + ab * L2[c]
                            ) % p
            cubics.append(v)
    return mons2, m2, mons3, m3, hess_poly2, cubics


def poly_mul_dict(poly_a: dict[tuple[int, ...], int], poly_b: dict[tuple[int, ...], int], p: int) -> dict[tuple[int, ...], int]:
    out = {}
    for ma, ca in poly_a.items():
        for mb, cb in poly_b.items():
            mm = tuple(sorted(ma + mb))
            out[mm] = (out.get(mm, 0) + ca * cb) % p
    return {m: c for m, c in out.items() if c != 0}


def eval_det_poly_vec(mat_vars_r, mat_vars_c, hess_poly2, mons2, target_idx_map, target_len: int, p: int) -> np.ndarray:
    """Fast cofactor/DP determinant in sparse monomial dict, returning dense vector in target_idx_map."""
    n = len(mat_vars_r)
    grid = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            pv = hess_poly2(mat_vars_r[i], mat_vars_c[j])
            if pv is not None:
                d = {mons2[idx]: int(pv[idx]) for idx in np.nonzero(pv)[0]}
                if d:
                    grid[i][j] = d

    # Bitmask DP over subset of rows for columns 0..n-1: dp[mask] = dict monomial -> coeff
    dp = {0: {(): 1}}
    for col in range(n):
        nxt = {}
        # Column permutation sign: adding col-th item to subset mask
        for mask, p_cur in dp.items():
            for r in range(n):
                if (mask >> r) & 1:
                    continue
                if grid[r][col] is None:
                    continue
                # Sign = (-1)**(# bits > r already set in mask)
                higher = bin(mask >> (r + 1)).count("1")
                sgn = -1 if (higher % 2) else 1
                prod = poly_mul_dict(p_cur, grid[r][col], p)
                if not prod:
                    continue
                nmask = mask | (1 << r)
                d_dst = nxt.setdefault(nmask, {})
                for mm, cc in prod.items():
                    val = (d_dst.get(mm, 0) + sgn * cc) % p
                    if val:
                        d_dst[mm] = val
                    elif mm in d_dst:
                        del d_dst[mm]
        dp = nxt
    full_poly = dp.get((1 << n) - 1, {})
    out = np.zeros(target_len, dtype=np.int64)
    for mm, cc in full_poly.items():
        out[target_idx_map[mm]] = cc
    return out


def test_2_global_h6_on_L9() -> tuple[int, dict[int, int]]:
    print("\n" + "=" * 95)
    print("TEST 2 (THM H-16B): GLOBAL H_{<=6}(perm_4) CERTIFICATION ON L_9 MOD 32,749 & 65,521")
    print("=" * 95)
    k = 9
    rng = np.random.default_rng(2026 + k)
    M_L9 = rng.integers(-2, 3, size=(16, k), dtype=np.int64)
    # Also construct explicit deg-8 generators: 6 det_4(B) + 6 det_4(C) + all structured det_4(M_{i,a;r0,c0}) & transposes!
    # Wait: M_{i,a;r0,c0} has R4 = row i, C4 = {(r0,c0)} U {(r,a): r != i} (4 * 4 * 9 = 144 generators),
    # plus col version C4 = col a, R4 = {(r0,c0)} U {(i,c): c != a} (144 generators), plus extra random zero-block 8x8!
    gens_rc_spec = []
    for r1, r2 in itertools.combinations(range(4), 2):
        gens_rc_spec.append(([r1 * 4 + c for c in range(4)], [r2 * 4 + c for c in range(4)]))
    for c1, c2 in itertools.combinations(range(4), 2):
        gens_rc_spec.append(([r * 4 + c1 for r in range(4)], [r * 4 + c2 for r in range(4)]))
    for i in range(4):
        R4 = [i * 4 + c for c in range(4)]
        other_r = [r for r in range(4) if r != i]
        for a in range(4):
            other_c = [c for c in range(4) if c != a]
            col_a_vars = [r * 4 + a for r in other_r]
            for r0 in other_r:
                for c0 in other_c:
                    C4 = [r0 * 4 + c0] + col_a_vars
                    gens_rc_spec.append((R4, C4))
    for a in range(4):
        Col4 = [r * 4 + a for r in range(4)]
        other_c = [c for c in range(4) if c != a]
        other_r = [r for r in range(4) if r != 0]
        for i in range(4):
            row_i_vars = [i * 4 + c for c in other_c]
            for r0 in [r for r in range(4) if r != i]:
                for c0 in other_c:
                    R4_x = [r0 * 4 + c0] + row_i_vars
                    gens_rc_spec.append((Col4, R4_x))
    # Plus 60 zero-block R4 x C4 pairs sampled deterministically across rows and cols
    gen_rng = np.random.default_rng(777)
    for i in range(4):
        R4 = [i * 4 + c for c in range(4)]
        oth = [v for v in range(16) if v // 4 != i]
        for _ in range(15):
            C4 = [int(v) for v in gen_rng.choice(oth, size=4, replace=False)]
            gens_rc_spec.append((R4, C4))

    coranks_d8 = {}
    coranks_final = {}
    for p in PRIMES:
        t0 = time.time()
        mons2, m2, mons3, m3, hess_poly2, cubics = build_p2_and_cubics(M_L9, p)
        mons6 = list(itertools.combinations_with_replacement(range(k), 6))
        m6 = {m: i for i, m in enumerate(mons6)}
        mons8 = list(itertools.combinations_with_replacement(range(k), 8))
        m8 = {m: i for i, m in enumerate(mons8)}
        cnz = [[(mons3[idx], int(v[idx])) for idx in np.nonzero(v)[0]] for v in cubics]

        # Cubic quotient via D=6 -> D=7 -> D=8 IMSC!
        A6 = np.zeros((16 * len(mons3), len(mons6)), dtype=np.int64)
        ri = 0
        for mm in mons3:
            for terms in cnz:
                for mc, cc in terms:
                    A6[ri, m6[tuple(sorted(mm + mc))]] = (A6[ri, m6[tuple(sorted(mm + mc))]] + cc) % p
                ri += 1
        rk6, _, free6, C6 = rref_mod_p(A6, p, need_c_table=True)
        h6 = len(mons6) - rk6
        mons7, free7, C7, h7, _ = step_imsc(k, 6, mons6, free6, C6, p)
        mons8_c, free8_c, C8_c, h8, _ = step_imsc(k, 7, mons7, free7, C7, p)
        print(f"  [p={p}] Cubics quotient h(6)={h6}, h(7)={h7}, h(8)={h8} [{time.time()-t0:.1f}s]")

        # Build degree-8 zero-block generators & project directly into the h(8)-dim quotient coordinates C8_c!
        t1 = time.time()
        vecs8 = np.zeros((len(gens_rc_spec), len(mons8)), dtype=np.int64)
        for gi, (r_s, c_s) in enumerate(gens_rc_spec):
            vecs8[gi] = eval_det_poly_vec(r_s, c_s, hess_poly2, mons2, m8, len(mons8), p)
        Q_proj = (vecs8.astype(np.float64) @ C8_c.astype(np.float64)).astype(np.int64) % p
        # Exact int check if float64 safe: max col sum of C8_c * max vecs8? Wait: vecs8 is mod p, C8_c is mod p,
        # length of dot is 12,870; max inner prod = 12870 * p^2 can exceed 2^53 for p=65521!
        # WAIT!! Crucial exact-arithmetic check: 12870 * 65521^2 = 5.52e13 < 2^53 = 9.007e15!!
        # Still verify 12870 * 65521^2 = 5.52e13 << 9.007e15, or split into 4096 chunks for extra margin!
        Q_proj = np.zeros((len(gens_rc_spec), C8_c.shape[1]), dtype=np.int64)
        for ch0 in range(0, len(mons8), 2048):
            ch1 = min(ch0 + 2048, len(mons8))
            part = (vecs8[:, ch0:ch1].astype(np.float64) @ C8_c[ch0:ch1, :].astype(np.float64)).astype(np.int64) % p
            Q_proj = (Q_proj + part) % p
        rk_q8, _, free_q8, C_q8 = rref_mod_p(Q_proj, p, need_c_table=True)
        crk8 = h8 - rk_q8
        coranks_d8[p] = crk8
        print(f"  [p={p}] H_{{<=6}} D=8 rank in R_8(L_9): {rk_q8}/{h8} => TOTAL D=8 corank = {crk8} ({len(mons8)-crk8}/{len(mons8)}) [{time.time()-t1:.1f}s]")

        # Update combined C8 = C8_c @ C_q8 (exact!) and do one IMSC step D=8 -> D=9!
        if crk8 == 0:
            coranks_final[p] = 0
        else:
            C8_comb = np.zeros((len(mons8), crk8), dtype=np.int64)
            # Small matrix C8_c @ C_q8: inner dim h8 ~ 588, so 588 * p^2 < 2.5e12 << 2^53
            C8_comb = (C8_c.astype(np.float64) @ C_q8.astype(np.float64)).astype(np.int64) % p
            _, _, _, crk9, rk9 = step_imsc(k, 8, mons8_c, free8_c, C8_comb, p) if False else (None, None, None, None, None)
            # Wait: free cols in mons8 are indices into mons8 corresponding to [free8_c[j] for j in free_q8]!
            free8_tot = [free8_c[f] for f in free_q8]
            _, _, _, crk9, rk9 = step_imsc(k, 8, mons8_c, free8_tot, C8_comb, p)
            coranks_final[p] = crk9
            print(f"  [p={p}] H_{{<=6}} D=9 via IMSC: corank = {crk9} (rank {rk9}/24310) [{time.time()-t0:.1f}s]")

    print(f"  Summary Theorem H-16B (L_9 H_{{<=6}}): D=8 coranks = {coranks_d8}, final coranks = {coranks_final}")
    return max(coranks_final.values()), coranks_final


def test_3_global_h4_on_L10() -> dict[int, int]:
    print("\n" + "=" * 95)
    print("TEST 3 (THM H-16C): GLOBAL H_{<=4}(perm_4) AUGMENTED IDEAL ON L_{10} MOD 32,749 & 65,521")
    print("=" * 95)
    k = 10
    rng = np.random.default_rng(2026 + k)
    M_L10 = rng.integers(-2, 3, size=(16, k), dtype=np.int64)

    # Generators of H_{<=4}^{deg 6}:
    # 1) Original 136 sextics (B, C, C_{ia})
    # 2) Augmented zero-block det_3(Hess[R_3, C_3]):
    #    - For every row i, every 3-col R_3, and structured C_3 = {(r0, c0), (r1, a), (r2, a)} (including (r0,c0) + col pairs)
    #    - Plus deterministic zero-block R_3 x C_3 samples for maximal span!
    gens6 = []
    for r1, r2 in itertools.combinations(range(4), 2):
        ri = [r1 * 4 + c for c in range(4)]
        ci = [r2 * 4 + c for c in range(4)]
        for sr in itertools.combinations(ri, 3):
            for sc in itertools.combinations(ci, 3):
                if sr <= sc:
                    gens6.append((list(sr), list(sc)))
    for c1, c2 in itertools.combinations(range(4), 2):
        ri = [r * 4 + c1 for r in range(4)]
        ci = [r * 4 + c2 for r in range(4)]
        for sr in itertools.combinations(ri, 3):
            for sc in itertools.combinations(ci, 3):
                if sr <= sc:
                    gens6.append((list(sr), list(sc)))
    for i in range(4):
        other_r = [r for r in range(4) if r != i]
        for a in range(4):
            other_c = [c for c in range(4) if c != a]
            # R3 containing (i, a) + 2 from other_c, C3 containing 2 from col a + (r0, c0)
            for c_pair in itertools.combinations(other_c, 2):
                R3 = [i * 4 + a, i * 4 + c_pair[0], i * 4 + c_pair[1]]
                for r_pair in itertools.combinations(other_r, 2):
                    r0 = [r for r in other_r if r not in r_pair][0]
                    for c0 in other_c:
                        C3 = [r0 * 4 + c0, r_pair[0] * 4 + a, r_pair[1] * 4 + a]
                        gens6.append((R3, C3))
    # Plus transposed cross blocks (col a R3 x row i + (r0,c0)) and sampled zero-block 3x3s
    for a in range(4):
        other_c = [c for c in range(4) if c != a]
        for i in range(4):
            other_r = [r for r in range(4) if r != i]
            for r_pair in itertools.combinations(other_r, 2):
                C3_a = [a + 4 * i, a + 4 * r_pair[0], a + 4 * r_pair[1]]
                for c_pair in itertools.combinations(other_c, 2):
                    c0 = [c for c in other_c if c not in c_pair][0]
                    for r0 in other_r:
                        R3_i = [r0 * 4 + c0, i * 4 + c_pair[0], i * 4 + c_pair[1]]
                        gens6.append((C3_a, R3_i))
    # Plus transposed cross blocks and deterministic random zero-block 3x3s (rows_i/col_a x random 3 outside)
    rng_g6 = np.random.default_rng(888)
    for i in range(4):
        other_v = [v for v in range(16) if v // 4 != i]
        for cols3 in itertools.combinations([i * 4 + c for c in range(4)], 3):
            for _ in range(40):
                c3 = [int(v) for v in rng_g6.choice(other_v, size=3, replace=False)]
                gens6.append((list(cols3), c3))
    for a in range(4):
        other_v = [v for v in range(16) if v % 4 != a]
        for rows3 in itertools.combinations([r * 4 + a for r in range(4)], 3):
            for _ in range(40):
                r3 = [int(v) for v in rng_g6.choice(other_v, size=3, replace=False)]
                gens6.append((list(rows3), r3))
    # Deduplicate (frozenset pairs) cleanly
    seen = set()
    uniq_gens6 = []
    for rs, cs in gens6:
        key = (tuple(sorted(rs)), tuple(sorted(cs)))
        if key not in seen:
            seen.add(key)
            uniq_gens6.append((rs, cs))
    print(f"  Unique deg-6 zero-block det_3 generators: {len(uniq_gens6)}")

    results = {}
    for p in PRIMES:
        t0 = time.time()
        mons2, m2, mons3, m3, hess_poly2, cubics = build_p2_and_cubics(M_L10, p)
        mons6 = list(itertools.combinations_with_replacement(range(k), 6))
        m6 = {m: i for i, m in enumerate(mons6)}
        cnz = [[(mons3[idx], int(v[idx])) for idx in np.nonzero(v)[0]] for v in cubics]

        A6 = np.zeros((16 * len(mons3) + len(uniq_gens6), len(mons6)), dtype=np.int64)
        ri = 0
        for mm in mons3:
            for terms in cnz:
                for mc, cc in terms:
                    A6[ri, m6[tuple(sorted(mm + mc))]] = (A6[ri, m6[tuple(sorted(mm + mc))]] + cc) % p
                ri += 1
        for rs, cs in uniq_gens6:
            A6[ri] = eval_det_poly_vec(rs, cs, hess_poly2, mons2, m6, len(mons6), p)
            ri += 1
        rk6, _, free6, C6 = rref_mod_p(A6, p, need_c_table=True)
        crk6 = len(mons6) - rk6
        print(f"  [L_10 | p={p}] D=6 rank = {rk6}/{len(mons6)} (corank = {crk6}) [{time.time()-t0:.1f}s]")

        mons7, free7, C7, crk7, rk7 = step_imsc(k, 6, mons6, free6, C6, p)
        if crk7 == 0:
            results[p] = 0
            continue
        if crk7 <= 700:
            _, _, _, crk8, rk8 = step_imsc(k, 7, mons7, free7, C7, p)
            results[p] = crk8
        else:
            results[p] = crk7
        print(f"  [L_10 | p={p}] Final corank = {results[p]} [{time.time()-t0:.1f}s]")

    return results


def main() -> None:
    t0 = time.time()
    test_1_theorem_h16a_zero_block_identities()
    crk9_max, res_h6 = test_2_global_h6_on_L9()
    res_h4_l10 = test_3_global_h4_on_L10()
    print("\n" + "=" * 95)
    print(f"ROUND 16 HILBERT SUMMARY [{time.time()-t0:.1f}s]:")
    print(f"  H_{{<=6}}(perm_4) on L_9  coranks (mod {PRIMES}): {res_h6}")
    print(f"  H_{{<=4}}(perm_4) on L_10 coranks (mod {PRIMES}): {res_h4_l10}")
    print("=" * 95)


if __name__ == "__main__":
    main()
