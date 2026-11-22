"""
Prof. Strassen Round 4 (Phase 4A) Verification Suite:
1. Explicit Counterexample 1A to Equation (iii) alone at n=6, w=19 with (r1,s1,r2,s2) = (15,3,3,15).
2. Hyperplane Degree-1 Syzygy Rigidity (364 hyperplanes) and Degree-2 Syzygy Rigidity (420/420) of B_{2,full}(b).
3. Degree-3 Syzygy onset (1115/1120, nullity 5) and generic 17D/16D/15D subspace rigidity (nullity 0).
4. Generic 2-point intersection delta = 0 for all d <= 11 in F^{15} (and d <= 8 inside W_10).
"""
from __future__ import annotations

import itertools
import sys
from pathlib import Path

import numpy as np

WORKBENCH = Path(__file__).resolve().parents[2]
if str(WORKBENCH) not in sys.path:
    sys.path.insert(0, str(WORKBENCH))

from apolar_higher_betti_probe import rank_matrix_mod
from perm4_abp_frontier import MOD


def verify_counterexample_iii_alone() -> None:
    """Verify explicit w=19 (15,3,3,15) solution to A1(a)B2(b) + B1(b)A2(a) == P_{perm,6}(a,b) identically."""
    subsets = list(itertools.combinations(range(6), 2))
    sub_idx = {s: idx for idx, s in enumerate(subsets)}
    S_list = [S for S in itertools.combinations(range(6), 3) if S != (3, 4, 5)]

    A1_base = np.zeros((15, 19, 6), dtype=np.int64)
    B2_base = np.zeros((19, 15, 6), dtype=np.int64)
    for idx, S in enumerate(S_list):
        Sc = tuple(x for x in range(6) if x not in S)
        for c in S:
            I = tuple(x for x in S if x != c)
            A1_base[sub_idx[I], idx, c] = 1
        for c in Sc:
            J = tuple(x for x in Sc if x != c)
            B2_base[idx, sub_idx[J], c] = 1

    B1_base = np.zeros((15, 19, 6), dtype=np.int64)
    A2_base = np.zeros((19, 15, 6), dtype=np.int64)
    rows_345 = [sub_idx[(3, 4)], sub_idx[(3, 5)], sub_idx[(4, 5)]]
    cols_012 = [sub_idx[(0, 1)], sub_idx[(0, 2)], sub_idx[(1, 2)]]
    b_vars = [2, 1, 0]
    a_vars = [5, 4, 3]
    for q in range(3):
        for r in range(3):
            w = 3 * q + r
            B1_base[rows_345[r], w, b_vars[q]] = 1
            A2_base[w, cols_012[q], a_vars[r]] = 1

    rng = np.random.default_rng(123)
    for _ in range(15):
        a = rng.integers(1, MOD, size=6, dtype=np.int64)
        b = rng.integers(1, MOD, size=6, dtype=np.int64)
        P6 = np.zeros((15, 15), dtype=np.int64)
        for i_idx, I in enumerate(subsets):
            for j_idx, J in enumerate(subsets):
                sI, sJ = set(I), set(J)
                if not (sI & sJ):
                    u, v = [x for x in range(6) if x not in sI and x not in sJ]
                    P6[i_idx, j_idx] = (a[u] * b[v] + a[v] * b[u]) % MOD
        A1 = np.einsum("iwc,c->iw", A1_base, a) % MOD
        B2 = np.einsum("wjc,c->wj", B2_base, b) % MOD
        B1 = np.einsum("iwc,c->iw", B1_base, b) % MOD
        A2 = np.einsum("wjc,c->wj", A2_base, a) % MOD
        assert np.array_equal((A1 @ B2 + B1 @ A2) % MOD, P6)
        assert rank_matrix_mod(A1, MOD) == 15
        assert rank_matrix_mod(B2, MOD) == 15
        assert rank_matrix_mod(B1, MOD) == 3
        assert rank_matrix_mod(A2, MOD) == 3

    print("[PASS] Counterexample to Eq (iii) alone: exact w=19 (15,3,3,15) identity verified over F_MOD")


def verify_higher_syzygy_rigidity() -> None:
    """Verify Hyperplane deg-1 rigidity (364 hyperplanes), deg-2 rigidity, and deg-3 onset of B_{2,full}(b)."""
    subsets = list(itertools.combinations(range(6), 2))
    sub_idx = {s: idx for idx, s in enumerate(subsets)}
    S_all = list(itertools.combinations(range(6), 3))

    B2_int = np.zeros((20, 15, 6), dtype=np.int64)
    for idx, S in enumerate(S_all):
        Sc = tuple(x for x in range(6) if x not in S)
        for c in Sc:
            J = tuple(x for x in Sc if x != c)
            B2_int[idx, sub_idx[J], c] = 1

    # 1. Hyperplane deg-1 rigidity across all 364 hyperplanes in {0, 1, -1}^6
    mon_m = [(i, j) for i in range(5) for j in range(i, 5)]
    mon_idx = {mo: idx for idx, mo in enumerate(mon_m)}
    tested = 0
    for c in itertools.product([0, 1, -1], repeat=6):
        if all(x == 0 for x in c):
            continue
        if next(x for x in c if x != 0) < 0:
            continue
        tested += 1
        piv = next(i for i, x in enumerate(c) if x != 0)
        other = [i for i in range(6) if i != piv]
        P = np.zeros((6, 5), dtype=np.int64)
        for col_idx, o in enumerate(other):
            P[o, col_idx] = 1
            P[piv, col_idx] = (-c[o] * pow(c[piv], MOD - 2, MOD)) % MOD
        B2_sub = np.einsum("wjc,cd->wjd", B2_int, P) % MOD
        eqs = np.zeros((15 * 15, 100), dtype=np.int64)
        for col in range(15):
            for c1 in range(5):
                for w in range(20):
                    coeff = int(B2_sub[w, col, c1])
                    if coeff == 0:
                        continue
                    for c2 in range(5):
                        mo = (min(c1, c2), max(c1, c2))
                        eqs[col * 15 + mon_idx[mo], w * 5 + c2] = (
                            eqs[col * 15 + mon_idx[mo], w * 5 + c2] + coeff
                        ) % MOD
        assert rank_matrix_mod(eqs, MOD) == 100
    assert tested == 364

    # 2. Degree-2 syzygy rigidity of B_{2,full}(b): 420 / 420 full rank (nullity = 0)
    mon2 = list(itertools.combinations_with_replacement(range(6), 2))
    mon3 = list(itertools.combinations_with_replacement(range(6), 3))
    mon4 = list(itertools.combinations_with_replacement(range(6), 4))
    mon3_idx = {m: idx for idx, m in enumerate(mon3)}
    mon4_idx = {m: idx for idx, m in enumerate(mon4)}

    eqs_d2 = np.zeros((15 * len(mon3), 20 * len(mon2)), dtype=np.int64)
    for col in range(15):
        for c1 in range(6):
            for w in range(20):
                coeff = int(B2_int[w, col, c1])
                if coeff == 0:
                    continue
                for m2_i, m2 in enumerate(mon2):
                    m3 = tuple(sorted(m2 + (c1,)))
                    eqs_d2[col * len(mon3) + mon3_idx[m3], w * len(mon2) + m2_i] = (
                        eqs_d2[col * len(mon3) + mon3_idx[m3], w * len(mon2) + m2_i] + coeff
                    ) % MOD
    assert rank_matrix_mod(eqs_d2, MOD) == 20 * len(mon2)

    # 3. Degree-3 syzygy onset of B_{2,full}(b): rank 1115 / 1120 (nullity = 5)
    eqs_d3 = np.zeros((15 * len(mon4), 20 * len(mon3)), dtype=np.int64)
    for col in range(15):
        for c1 in range(6):
            for w in range(20):
                coeff = int(B2_int[w, col, c1])
                if coeff == 0:
                    continue
                for m3_i, m3 in enumerate(mon3):
                    m4 = tuple(sorted(m3 + (c1,)))
                    eqs_d3[col * len(mon4) + mon4_idx[m4], w * len(mon3) + m3_i] = (
                        eqs_d3[col * len(mon4) + mon4_idx[m4], w * len(mon3) + m3_i] + coeff
                    ) % MOD
    assert rank_matrix_mod(eqs_d3, MOD) == 1115

    # 4. Generic 17D, 16D, 15D subspaces of S_{6,3} have full rank 15 over F(b) and 0 deg-3 syzygies
    rng = np.random.default_rng(42)
    b_pt = rng.integers(1, MOD, size=6, dtype=np.int64)
    for n_in in (17, 16, 15):
        W = rng.integers(0, MOD, size=(n_in, 20), dtype=np.int64)
        B2_in = np.einsum("aw,wjc->ajc", W, B2_int) % MOD
        assert rank_matrix_mod(np.einsum("ajc,c->aj", B2_in, b_pt) % MOD, MOD) == 15
        eqs_sub = np.zeros((15 * len(mon4), n_in * len(mon3)), dtype=np.int64)
        for col in range(15):
            for c1 in range(6):
                for w in range(n_in):
                    coeff = int(B2_in[w, col, c1])
                    if coeff == 0:
                        continue
                    for m3_i, m3 in enumerate(mon3):
                        m4 = tuple(sorted(m3 + (c1,)))
                        eqs_sub[col * len(mon4) + mon4_idx[m4], w * len(mon3) + m3_i] = (
                            eqs_sub[col * len(mon4) + mon4_idx[m4], w * len(mon3) + m3_i] + coeff
                        ) % MOD
        assert rank_matrix_mod(eqs_sub, MOD) == n_in * len(mon3)

    print("[PASS] Hyperplane deg-1 (364/364), deg-2 (420/420), deg-3 (1115/1120), and generic 15D-17D rigidity verified")


def verify_generic_two_point_delta_zero() -> None:
    """Verify dim(S_{6,3} cap (U kron F^6)) == 0 for generic U in F^{15} of dim <= 11 (and <= 8 inside W_10)."""
    subsets = list(itertools.combinations(range(6), 2))
    sub_idx = {s: idx for idx, s in enumerate(subsets)}
    S_all = list(itertools.combinations(range(6), 3))

    S_basis = np.zeros((90, 20), dtype=np.int64)
    for idx, S in enumerate(S_all):
        for c in S:
            I = tuple(x for x in S if x != c)
            S_basis[sub_idx[I] * 6 + c, idx] = 1

    rng = np.random.default_rng(42)
    for d in range(1, 12):
        U = rng.integers(0, MOD, size=(15, d), dtype=np.int64)
        U_F6 = np.kron(U, np.eye(6, dtype=np.int64)) % MOD
        r_sum = rank_matrix_mod(np.hstack([S_basis, U_F6]) % MOD, MOD)
        assert 20 + 6 * d - r_sum == 0

    rows_5 = [sub_idx[p] for p in itertools.combinations(range(5), 2)]
    W10 = np.zeros((15, 10), dtype=np.int64)
    for j, r in enumerate(rows_5):
        W10[r, j] = 1
    for d in range(1, 9):
        U = (W10 @ rng.integers(0, MOD, size=(10, d), dtype=np.int64)) % MOD
        U_F6 = np.kron(U, np.eye(6, dtype=np.int64)) % MOD
        r_sum = rank_matrix_mod(np.hstack([S_basis, U_F6]) % MOD, MOD)
        assert 20 + 6 * d - r_sum == 0

    print("[PASS] Generic U subset F^{15} (d <= 11) and U subset W_10 (d <= 8) give delta == 0")


if __name__ == "__main__":
    verify_counterexample_iii_alone()
    verify_higher_syzygy_rigidity()
    verify_generic_two_point_delta_zero()
    print("\nALL ROUND 4 STRASSEN VERIFICATIONS PASS (EXIT CODE 0).")
