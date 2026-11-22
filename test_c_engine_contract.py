#!/usr/bin/env python3
"""
Unit tests for exact_csr_rank_mod_p C contract hardening.
Verifies all contract preconditions, error return codes, and exact rank calculations.
"""

import ctypes
import numpy as np
import os
import subprocess

def test_c_contract():
    so_path = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/paper_dc_perm4/exact_mod_rref.so"
    c_path = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/paper_dc_perm4/exact_mod_rref.c"
    
    # Recompile
    subprocess.run(["gcc", "-O3", "-shared", "-fPIC", "-o", so_path, c_path], check=True)
    lib = ctypes.CDLL(so_path)
    
    lib.exact_csr_rank_mod_p.argtypes = [
        ctypes.POINTER(ctypes.c_int64),
        ctypes.POINTER(ctypes.c_int64),
        ctypes.POINTER(ctypes.c_int64),
        ctypes.c_int64,
        ctypes.c_int64,
        ctypes.c_int64,
        ctypes.c_int64
    ]
    lib.exact_csr_rank_mod_p.restype = ctypes.c_int64

    def run_rank(row_ptr, col_idx, vals, nrows, ncols, nnz, p):
        rp_c = (ctypes.c_int64 * len(row_ptr))(*row_ptr)
        ci_c = (ctypes.c_int64 * len(col_idx))(*col_idx) if len(col_idx) > 0 else None
        v_c = (ctypes.c_int64 * len(vals))(*vals) if len(vals) > 0 else None
        return lib.exact_csr_rank_mod_p(rp_c, ci_c, v_c, nrows, ncols, nnz, p)

    print("Running contract checks...")

    # 1. Composite modulus check (p=10) -> expected -2
    res = run_rank([0, 1], [0], [1], 1, 1, 1, 10)
    assert res == -2, f"Expected -2 for composite modulus, got {res}"
    print("  [PASS] Composite modulus correctly rejected (code -2).")

    # 2. Prime modulus p=32749 -> expected rank 1
    res = run_rank([0, 1], [0], [5], 1, 1, 1, 32749)
    assert res == 1, f"Expected rank 1, got {res}"
    print("  [PASS] Valid 1x1 rank computed correctly (rank 1).")

    # 3. nnz mismatch: row_ptr reports nnz=2 but nnz parameter is 1 -> expected -5
    res = run_rank([0, 2], [0, 1], [1, 1], 1, 2, 1, 32749)
    assert res == -5, f"Expected -5 for nnz mismatch, got {res}"
    print("  [PASS] nnz mismatch correctly rejected (code -5).")

    # 4. Non-monotonic row_ptr [0, 2, 1] -> expected -5
    res = run_rank([0, 2, 1], [0, 1], [1, 1], 2, 2, 2, 32749)
    assert res == -5, f"Expected -5 for non-monotonic row_ptr, got {res}"
    print("  [PASS] Non-monotonic row_ptr correctly rejected (code -5).")

    # 5. Out of bounds column index (c=5 when ncols=3) -> expected -8
    res = run_rank([0, 1], [5], [1], 1, 3, 1, 32749)
    assert res == -8, f"Expected -8 for column out of bounds, got {res}"
    print("  [PASS] Column index out-of-bounds correctly caught (code -8).")

    # 6. Empty matrix 0x0 -> expected rank 0
    res = run_rank([0], [], [], 0, 0, 0, 32749)
    assert res == 0, f"Expected 0 for 0x0 matrix, got {res}"
    print("  [PASS] Empty matrix contract verified (rank 0).")

    # 7. Known 3x3 identity matrix mod 65521 -> rank 3
    res = run_rank([0, 1, 2, 3], [0, 1, 2], [1, 1, 1], 3, 3, 3, 65521)
    assert res == 3, f"Expected rank 3, got {res}"
    print("  [PASS] Identity 3x3 rank 3 over p=65521 verified.")

    # 8. Dependent rows: [1, 2], [2, 4] -> rank 1
    res = run_rank([0, 2, 4], [0, 1, 0, 1], [1, 2, 2, 4], 2, 2, 4, 32749)
    assert res == 1, f"Expected rank 1, got {res}"
    print("  [PASS] Linearly dependent 2x2 rank 1 verified.")

    print("\nALL 8 C CONTRACT CHECKS PASSED WITH FULL INTEGRITY!")

if __name__ == "__main__":
    test_c_contract()
