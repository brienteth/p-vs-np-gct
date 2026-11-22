"""Wall 2 probe: exact vectorized Boolean, F_2-ANF, F_3-multilinear, and Fourier/Influence bridge."""
from __future__ import annotations

import itertools
from typing import Dict, List, Tuple

import numpy as np


def all_binary_matrices(n: int) -> np.ndarray:
    """Return array of shape (2^(n^2), n, n) containing all binary n x n matrices."""
    nv = n * n
    count = 1 << nv
    idx = np.arange(count, dtype=np.int32)
    bits = ((idx[:, None] >> np.arange(nv, dtype=np.int32)[None, :]) & 1).astype(np.int32)
    return bits.reshape(count, n, n)


def eval_perm_and_det(mats: np.ndarray, n: int) -> Tuple[np.ndarray, np.ndarray]:
    """Compute exact integer perm_n and det_n across all binary matrices."""
    count = mats.shape[0]
    perm_vals = np.zeros(count, dtype=np.int32)
    det_vals = np.zeros(count, dtype=np.int32)
    rows = np.arange(n, dtype=np.int32)

    for p in itertools.permutations(range(n)):
        # Parity of permutation p
        inv = 0
        for i in range(n):
            for j in range(i + 1, n):
                if p[i] > p[j]:
                    inv += 1
        sgn = 1 if (inv % 2 == 0) else -1
        prod = np.ones(count, dtype=np.int32)
        for r, c in zip(rows, p):
            prod *= mats[:, r, c]
        perm_vals += prod
        det_vals += sgn * prod
    return perm_vals, det_vals


def mobius_f2(f_bool: np.ndarray, nv: int) -> np.ndarray:
    """Fast Mobius transform over F_2 returning exact ANF coefficients."""
    a = f_bool.astype(np.uint8).copy()
    for b in range(nv):
        view = a.reshape(-1, 2, 1 << b)
        view[:, 1, :] ^= view[:, 0, :]
    return a


def mobius_f3(f_bool: np.ndarray, nv: int) -> np.ndarray:
    """Fast Mobius transform over F_3 returning exact multilinear coeffs mod 3 on {0,1}^nv."""
    a = (f_bool.astype(np.int16) % 3).copy()
    for b in range(nv):
        view = a.reshape(-1, 2, 1 << b)
        view[:, 1, :] = (view[:, 1, :] - view[:, 0, :]) % 3
    return a


def inv_mobius_f3(coeffs: np.ndarray, nv: int) -> np.ndarray:
    a = coeffs.copy()
    for b in range(nv):
        view = a.reshape(-1, 2, 1 << b)
        view[:, 1, :] = (view[:, 1, :] + view[:, 0, :]) % 3
    return a


def fwht_int(f_bool: np.ndarray, nv: int) -> np.ndarray:
    """Exact unnormalized Walsh-Hadamard transform of g(x) = 1 - 2*F(x) in {-1, +1}."""
    g = (1 - 2 * f_bool.astype(np.int64)).copy()
    for b in range(nv):
        view = g.reshape(-1, 2, 1 << b)
        u0 = view[:, 0, :].copy()
        u1 = view[:, 1, :]
        view[:, 0, :] = u0 + u1
        view[:, 1, :] = u0 - u1
    return g


def avg_sensitivity(f_bool: np.ndarray, nv: int) -> float:
    total = 0.0
    for b in range(nv):
        view = f_bool.reshape(-1, 2, 1 << b)
        diff = (view[:, 0, :] != view[:, 1, :]).mean()
        total += 2.0 * float(diff) * 0.5  # mean over both halves equals exact flip prob
    return total


def analyze_n(n: int) -> None:
    nv = n * n
    count = 1 << nv
    idx = np.arange(count, dtype=np.int32)
    popcounts = np.zeros(count, dtype=np.int32)
    for b in range(nv):
        popcounts += (idx >> b) & 1

    mats = all_binary_matrices(n)
    perm_vals, det_vals = eval_perm_and_det(mats, n)
    assert np.array_equal(perm_vals & 1, det_vals & 1), "perm != det mod 2!"

    funcs: List[Tuple[str, np.ndarray]] = [
        ("det_mod2", ((det_vals % 2) != 0)),
        ("det_nz_mod3", ((det_vals % 3) != 0)),
        ("perm_nz_mod3", ((perm_vals % 3) != 0)),
        ("det_nz_Z", (det_vals != 0)),
        ("perm_pos_Z", (perm_vals > 0)),
        ("perm_ge2_Z", (perm_vals >= 2)),
    ]

    print(f"=== n={n} (N={nv} vars, {count} binary matrices) Boolean-Algebraic Bridge ===")
    print(
        "Function     | P(F=1) | F2(d,nnz)    | F3(d,nnz)    | R(d,nnz)     | Inf(F) | L1_spec | tail(>2, >3, >4)"
    )
    print("-" * 108)

    for name, f_bool in funcs:
        anf = mobius_f2(f_bool, nv)
        assert np.array_equal(mobius_f2(anf, nv), f_bool.astype(np.uint8)), "F2 Mobius round-trip failed"
        deg_f2 = int(popcounts[anf != 0].max()) if np.any(anf) else 0
        nnz_f2 = int(np.count_nonzero(anf))

        c_f3 = mobius_f3(f_bool, nv)
        assert np.array_equal(inv_mobius_f3(c_f3, nv), f_bool.astype(np.int16) % 3), "F3 round-trip failed"
        deg_f3 = int(popcounts[c_f3 != 0].max()) if np.any(c_f3) else 0
        nnz_f3 = int(np.count_nonzero(c_f3))

        g_int = fwht_int(f_bool, nv)
        ghat = g_int.astype(np.float64) / float(count)
        assert abs(float(np.sum(ghat * ghat)) - 1.0) < 1e-10, "Parseval failed"
        deg_r = int(popcounts[g_int != 0].max()) if np.any(g_int) else 0
        nnz_r = int(np.count_nonzero(g_int))

        inf_f = float(np.sum(popcounts * (ghat * ghat)))
        sens_f = avg_sensitivity(f_bool, nv)
        assert abs(inf_f - sens_f) < 1e-10, f"Influence != Sensitivity: {inf_f} != {sens_f}"
        l1_spec = float(np.sum(np.abs(ghat)))

        tail2 = float(np.sum(ghat[popcounts > 2] ** 2))
        tail3 = float(np.sum(ghat[popcounts > 3] ** 2))
        tail4 = float(np.sum(ghat[popcounts > 4] ** 2))

        p1 = float(np.mean(f_bool))
        f2_str = f"({deg_f2:2d},{nnz_f2:5d})"
        f3_str = f"({deg_f3:2d},{nnz_f3:5d})"
        r_str = f"({deg_r:2d},{nnz_r:5d})"
        tail_str = f"({tail2:.3f}, {tail3:.3f}, {tail4:.3f})"
        print(
            f"{name:12s} | {p1:6.4f} | {f2_str:12s} | {f3_str:12s} | {r_str:12s} | "
            f"{inf_f:6.3f} | {l1_spec:7.2f} | {tail_str}"
        )
    print()


def main() -> None:
    analyze_n(3)
    analyze_n(4)


if __name__ == "__main__":
    main()
