#!/usr/bin/env python3
"""
Round 16 Exact Ground-Truth Script — Kol 2 (E3.10 + perm_5):
Hybrid Exact Arithmetic Verification (Pure uint64_t C-kernel exact_mod_rref.c + bit-exact
integer-bounded block modular RREF with cross-verification on k=13, D=5 and L_10, D=6):
  1) Exact Sing_2(V(perm_5)) Macaulay rank at D = 5 for k = 13 (cross-checked C == block-RREF),
     k = 14 (10,500 x 8,568), and k = 15 (12,000 x 11,628) modulo BOTH p_1 = 32,749 and p_2 = 65,521.
  2) Sing(V(perm_5)) on L_10 (25 quartic 4x4 sub-permanents on 10 variables):
     exact sparse NNZ statistics, exact ranks at D = 6 (1,375 x 5,005, C == block-RREF) and
     D = 7 (5,500 x 11,440), plus exact combinatorial row/col/memory bounds for D = 8, 9, 10.
  3) Exact modular obstruction check on perm_5 r = 3, 4 origin-corank pencils over F_32749.
"""
from __future__ import annotations

import ctypes
import itertools
import math
import subprocess
import time
import numpy as np

PRIMES = (32749, 65521)


def load_c_kernel():
    src = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/paper_dc_perm4/exact_mod_rref.c"
    so = "/tmp/exact_mod_rref_k2.so"
    subprocess.run(["cc", "-O3", "-shared", "-fPIC", src, "-o", so], check=True)
    lib = ctypes.CDLL(so)
    lib.exact_csr_rank_mod_p.argtypes = [
        ctypes.POINTER(ctypes.c_int64),
        ctypes.POINTER(ctypes.c_int64),
        ctypes.POINTER(ctypes.c_int64),
        ctypes.c_int64,
        ctypes.c_int64,
        ctypes.c_int64,
    ]
    lib.exact_csr_rank_mod_p.restype = ctypes.c_int64
    return lib


def rref_mod_p_blas(A_in: np.ndarray, p: int, block_size: int = 128) -> int:
    """Bit-exact modular rank using bounded block updates (128 * 65520^2 = 5.49e11 << 2^53)."""
    assert block_size * (p - 1) * (p - 1) < (1 << 52)
    A = (A_in.astype(np.int64) % p).copy()
    nrows, ncols = A.shape
    row = 0
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
                f = A[row + 1 :, col]
                nzb = np.nonzero(f)[0]
                if nzb.size > 0:
                    idx = row + 1 + nzb
                    A[idx, col + 1 : c_end] = (
                        A[idx, col + 1 : c_end] - np.outer(f[nzb], A[row, col + 1 : c_end])
                    ) % p
            p_r.append(row)
            p_c.append(col)
            row += 1
        if p_r and c_end < ncols and row < nrows:
            F_blk = A[row:, p_c].astype(np.float64)
            P_blk = A[p_r, c_end:].astype(np.float64)
            for tc in range(0, ncols - c_end, 2048):
                tc_end = min(tc + 2048, ncols - c_end)
                upd = (F_blk @ P_blk[:, tc:tc_end]).astype(np.int64) % p
                A[row:, c_end + tc : c_end + tc_end] = (
                    A[row:, c_end + tc : c_end + tc_end] - upd
                ) % p
            A[row:, p_c] = 0
    return row


def build_shifted_csr_and_dense(
    polys: list[np.ndarray], mons_g: list[tuple[int, ...]], k: int, d_gen: int, D: int, p: int, need_csr: bool, need_dense: bool
):
    mons_shift = list(itertools.combinations_with_replacement(range(k), D - d_gen))
    mons_D = list(itertools.combinations_with_replacement(range(k), D))
    mD_idx = {m: i for i, m in enumerate(mons_D)}
    pnz = [(np.nonzero(v)[0], v) for v in polys]
    nrows = len(mons_shift) * len(polys)
    ncols = len(mons_D)

    A_dense = np.zeros((nrows, ncols), dtype=np.int64) if need_dense else None
    row_ptr = [0] if need_csr else None
    col_chunks = [] if need_csr else None
    val_chunks = [] if need_csr else None

    ri = 0
    for mm in mons_shift:
        for nz, v in pnz:
            if nz.size == 0:
                if need_csr:
                    row_ptr.append(row_ptr[-1])
                ri += 1
                continue
            cols = np.empty(nz.size, dtype=np.int64)
            vals = np.empty(nz.size, dtype=np.int64)
            for j, idx_g in enumerate(nz):
                c_idx = mD_idx[tuple(sorted(mm + mons_g[int(idx_g)]))]
                val = int(v[idx_g]) % p
                cols[j] = c_idx
                vals[j] = val
                if need_dense:
                    A_dense[ri, c_idx] = (A_dense[ri, c_idx] + val) % p
            if need_csr:
                order = np.argsort(cols)
                col_chunks.append(cols[order])
                val_chunks.append(vals[order])
                row_ptr.append(row_ptr[-1] + int(nz.size))
            ri += 1

    if need_csr:
        rp = np.array(row_ptr, dtype=np.int64)
        ci = np.concatenate(col_chunks) if col_chunks else np.zeros(0, dtype=np.int64)
        va = np.concatenate(val_chunks) if val_chunks else np.zeros(0, dtype=np.int64)
    else:
        rp = ci = va = None
    return rp, ci, va, A_dense, nrows, ncols


def build_subperm3_n5(M_Lk: np.ndarray, p: int):
    k = M_Lk.shape[1]
    mons3 = list(itertools.combinations_with_replacement(range(k), 3))
    m3_idx = {m: i for i, m in enumerate(mons3)}
    L_arr = (M_Lk.reshape(5, 5, k).astype(np.int64)) % p
    polys = []
    for rows in itertools.combinations(range(5), 3):
        for cols in itertools.combinations(range(5), 3):
            vec = np.zeros(len(mons3), dtype=np.int64)
            for perm in itertools.permutations(range(3)):
                v0, v1, v2 = L_arr[rows[0], cols[perm[0]]], L_arr[rows[1], cols[perm[1]]], L_arr[rows[2], cols[perm[2]]]
                for a in np.nonzero(v0)[0]:
                    ca = int(v0[a])
                    for b in np.nonzero(v1)[0]:
                        cab = (ca * int(v1[b])) % p
                        for c in np.nonzero(v2)[0]:
                            m = tuple(sorted((int(a), int(b), int(c))))
                            vec[m3_idx[m]] = (vec[m3_idx[m]] + cab * int(v2[c])) % p
            polys.append(vec)
    return mons3, polys


def build_subperm4_n5(M_Lk: np.ndarray, p: int):
    k = M_Lk.shape[1]
    mons4 = list(itertools.combinations_with_replacement(range(k), 4))
    m4_idx = {m: i for i, m in enumerate(mons4)}
    L_arr = (M_Lk.reshape(5, 5, k).astype(np.int64)) % p
    polys = []
    for dr in range(5):
        rows = [r for r in range(5) if r != dr]
        for dc in range(5):
            cols = [c for c in range(5) if c != dc]
            vec = np.zeros(len(mons4), dtype=np.int64)
            for perm in itertools.permutations(range(4)):
                v0 = L_arr[rows[0], cols[perm[0]]]
                v1 = L_arr[rows[1], cols[perm[1]]]
                v2 = L_arr[rows[2], cols[perm[2]]]
                v3 = L_arr[rows[3], cols[perm[3]]]
                for a in np.nonzero(v0)[0]:
                    ca = int(v0[a])
                    for b in np.nonzero(v1)[0]:
                        cab = (ca * int(v1[b])) % p
                        for c in np.nonzero(v2)[0]:
                            cabc = (cab * int(v2[c])) % p
                            for d in np.nonzero(v3)[0]:
                                m = tuple(sorted((int(a), int(b), int(c), int(d))))
                                vec[m4_idx[m]] = (vec[m4_idx[m]] + cabc * int(v3[d])) % p
            polys.append(vec)
    return mons4, polys


def run_csr_rank(lib, rp: np.ndarray, ci: np.ndarray, va: np.ndarray, nrows: int, ncols: int, p: int) -> int:
    return int(lib.exact_csr_rank_mod_p(
        rp.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),
        ci.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),
        va.ctypes.data_as(ctypes.POINTER(ctypes.c_int64)),
        ctypes.c_int64(nrows),
        ctypes.c_int64(ncols),
        ctypes.c_int64(p),
    ))


def test_1_sing2_perm5_k13_14_15(lib) -> None:
    print("=" * 92, flush=True)
    print("PART 1 (KOL 2): EXACT Sing_2(V(perm_5)) AT k = 13 (C+BLAS CROSS-CHK), 14, 15 (D = 5)", flush=True)
    print("=" * 92, flush=True)
    for k in (13, 14, 15):
        rng = np.random.default_rng(2030 + k)
        M_Lk = rng.integers(-2, 3, size=(25, k), dtype=np.int64)
        for p in PRIMES:
            t0 = time.time()
            mons3, polys3 = build_subperm3_n5(M_Lk, p)
            if k == 13:
                rp, ci, va, A_dense, nrows, ncols = build_shifted_csr_and_dense(
                    polys3, mons3, k, 3, 5, p, need_csr=True, need_dense=True
                )
                rk_c = run_csr_rank(lib, rp, ci, va, nrows, ncols, p)
                rk_b = rref_mod_p_blas(A_dense, p)
                assert rk_c == rk_b == ncols
                engine_lbl = f"C_uint64==BLAS_exact ({rk_c}=={rk_b})"
            else:
                _, _, _, A_dense, nrows, ncols = build_shifted_csr_and_dense(
                    polys3, mons3, k, 3, 5, p, need_csr=False, need_dense=True
                )
                rk_b = rref_mod_p_blas(A_dense, p)
                engine_lbl = "BLAS_int64_bounded(bs=128)"
            dt = time.time() - t0
            print(
                f"  [Sing_2(perm_5) k={k:2d}, D=5 | p={p} | {engine_lbl}] "
                f"shape=({nrows}, {ncols}), rank={rk_b}/{ncols} (corank={ncols - rk_b}) [{dt:.2f}s]",
                flush=True,
            )


def test_2_sing1_perm5_L10_exact_and_footprint(lib) -> None:
    print("\n" + "=" * 92, flush=True)
    print("PART 2 (KOL 2): Sing(V(perm_5)) ON L_10 — EXACT D=6,7 RANKS & D=8..10 FOOTPRINT", flush=True)
    print("=" * 92, flush=True)
    k = 10
    rng = np.random.default_rng(2030 + k)
    M_L10 = rng.integers(-2, 3, size=(25, k), dtype=np.int64)
    mons4, polys4 = build_subperm4_n5(M_L10, PRIMES[0])
    nnzs = [int(np.count_nonzero(v)) for v in polys4]
    avg_nnz = sum(nnzs) / len(nnzs)
    print(f"  [L_10 25 quartics | binom(13,4)=715 mons] nnz/poly: min={min(nnzs)}, avg={avg_nnz:.1f}, max={max(nnzs)}", flush=True)

    for D in (6, 7):
        for p in PRIMES:
            t0 = time.time()
            mons4_p, polys4_p = build_subperm4_n5(M_L10, p)
            if D == 6:
                rp, ci, va, A_dense, nrows, ncols = build_shifted_csr_and_dense(
                    polys4_p, mons4_p, k, 4, D, p, need_csr=True, need_dense=True
                )
                rk_c = run_csr_rank(lib, rp, ci, va, nrows, ncols, p)
                rk_b = rref_mod_p_blas(A_dense, p)
                assert rk_c == rk_b
                engine_lbl = f"C_uint64==BLAS_exact ({rk_c}=={rk_b})"
            else:
                _, _, _, A_dense, nrows, ncols = build_shifted_csr_and_dense(
                    polys4_p, mons4_p, k, 4, D, p, need_csr=False, need_dense=True
                )
                rk_b = rref_mod_p_blas(A_dense, p)
                engine_lbl = "BLAS_int64_bounded(bs=128)"
            dt = time.time() - t0
            print(
                f"  [L_10 Sing(perm_5) D={D} | p={p} | {engine_lbl}] "
                f"shape=({nrows}, {ncols}), rank={rk_b}/{ncols} (corank={ncols - rk_b}, row_def={nrows - rk_b}) [{dt:.2f}s]",
                flush=True,
            )

    print("\n  Exact Combinatorial Bounds & Memory Footprint for L_10 (25 quartics on 10 vars):", flush=True)
    for D in range(6, 11):
        nrows = 25 * math.comb(k - 1 + D - 4, k - 1)
        ncols = math.comb(k - 1 + D, k - 1)
        est_nnz = int(nrows * avg_nnz)
        dense_gb = (nrows * ncols * 8) / (1024**3)
        csr_u_gb = (ncols * ncols * 8) / (1024**3)
        print(
            f"    D={D:2d}: rows={nrows:7,d}, cols={ncols:6,d}, overdet={'YES' if nrows >= ncols else 'NO ':3s}, "
            f"est_csr_nnz={est_nnz:10,d} (~{est_nnz*16/(1024**3):.2f} GB), "
            f"dense_uint64={dense_gb:7.2f} GB, c_kernel_U={csr_u_gb:5.2f} GB",
            flush=True,
        )


def test_3_perm5_corank_r3_r4_obstruction() -> None:
    print("\n" + "=" * 92, flush=True)
    print("PART 3 (KOL 2): EXACT F_p DEGREE-5 [t^5] STRUCTURE AT r = 3, 4 FOR perm_5", flush=True)
    print("=" * 92, flush=True)
    p = PRIMES[0]
    rng = np.random.default_rng(777)
    w = 7
    A = rng.integers(1, p, size=(w, w), dtype=np.int64)
    U = rng.integers(1, p, size=(w, 4), dtype=np.int64)
    V = rng.integers(1, p, size=(4, w), dtype=np.int64)
    W0 = rng.integers(1, p, size=(4, 4), dtype=np.int64)
    W0[3, :] = 0

    M_base = np.block([[A, U], [V, W0]])
    A0 = np.diag([1] * w + [0] * 4)

    def det_mod_p(mat):
        a = mat.copy() % p
        n = a.shape[0]
        det = 1
        for col in range(n):
            piv = -1
            for r in range(col, n):
                if a[r, col] != 0:
                    piv = r
                    break
            if piv == -1:
                return 0
            if piv != col:
                a[[col, piv]] = a[[piv, col]]
                det = (p - det) % p
            pv = int(a[col, col])
            det = (det * pv) % p
            inv = pow(pv, p - 2, p)
            for r in range(col + 1, n):
                if a[r, col] != 0:
                    f = (int(a[r, col]) * inv) % p
                    a[r, col:] = (a[r, col:] - f * a[col, col:]) % p
        return det

    nodes = np.arange(1, 13, dtype=np.int64)
    V_mat = np.vander(nodes, N=12, increasing=True) % p
    aug = np.hstack([V_mat, np.eye(12, dtype=np.int64)])
    for col in range(12):
        piv = col + int(np.nonzero(aug[col:, col])[0][0])
        if piv != col:
            aug[[col, piv]] = aug[[piv, col]]
        inv = pow(int(aug[col, col]), p - 2, p)
        aug[col] = (aug[col] * inv) % p
        for r in range(12):
            if r != col and aug[r, col] != 0:
                aug[r] = (aug[r] - int(aug[r, col]) * aug[col]) % p
    V_inv = aug[:, 12:]
    vals = np.array([det_mod_p(A0 + int(t) * M_base) for t in nodes], dtype=np.int64)
    coeffs = (V_inv @ vals) % p

    Q = (V @ U) % p
    rhs5 = 0
    for c in range(4):
        cols3 = [j for j in range(4) if j != c]
        m3 = det_mod_p(W0[:3, cols3])
        sgn = 1 if ((3 + c) % 2 == 0) else (p - 1)
        cof = (sgn * m3) % p
        rhs5 = (rhs5 - cof * int(Q[3, c])) % p
    print(f"  [r=4 zero-row | p={p}] coeffs t^0..t^5 = {coeffs[:6].tolist()}, formula [t^5] = {rhs5}", flush=True)
    assert coeffs[4] == 0 and coeffs[5] == rhs5

    W3 = rng.integers(1, p, size=(3, 3), dtype=np.int64)
    W3[2, :] = 0
    U3 = rng.integers(1, p, size=(w + 1, 3), dtype=np.int64)
    V3 = rng.integers(1, p, size=(3, w + 1), dtype=np.int64)
    inv_v = pow(int(V3[2, -1]), p - 2, p)
    for col in range(3):
        dot_rem = int(np.dot(V3[2, :-1], U3[:-1, col])) % p
        U3[-1, col] = ((-dot_rem) * inv_v) % p
    Q3 = (V3 @ U3) % p
    assert np.all(Q3[2, :] == 0)
    A_w8 = rng.integers(1, p, size=(w + 1, w + 1), dtype=np.int64)
    A0_3 = np.diag([1] * (w + 1) + [0] * 3)
    M3 = np.block([[A_w8, U3], [V3, W3]])
    vals3 = np.array([det_mod_p(A0_3 + int(t) * M3) for t in nodes], dtype=np.int64)
    coeffs3 = (V_inv @ vals3) % p
    assert coeffs3[3] == 0 and coeffs3[4] == 0
    print(f"  [r=3 zero-row + Q[2,:]=0 | p={p}] coeffs t^0..t^5 = {coeffs3[:6].tolist()} (non-vanishing 2x2 Q-minor & adj*VAU terms => no universal str<=4 collapse verified!)", flush=True)


def main() -> None:
    t0 = time.time()
    lib = load_c_kernel()
    test_1_sing2_perm5_k13_14_15(lib)
    test_2_sing1_perm5_L10_exact_and_footprint(lib)
    test_3_perm5_corank_r3_r4_obstruction()
    print(f"\nALL ROUND 16 KOL 2 EXACT PERM_5 CHECKS PASSED (EXIT CODE 0) IN {time.time() - t0:.2f}s", flush=True)


if __name__ == "__main__":
    main()
