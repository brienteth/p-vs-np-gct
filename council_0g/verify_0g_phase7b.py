"""Phase 7B: Exact Algebraic Lower Bounds for Non-Row-Separated 4-Layer ABPs (Front 2).

Two critical checks:
  1. REFEREE AUDIT on Phase 5B's `Pi_RowML` alone: test w2 = 1 and w2 = 2 (in Phase 5B we only tested
     w2 in {6,5,4,3}, assuming Archimedes' 2*w2 >= 6 applied to globally mixed Pi_RowML!).
  2. KRULL SINGULAR-LOCUS LOWER BOUND (UNCONDITIONAL FOR ALL GLOBALLY MIXED Q(X)*R(X) = perm_4(X)):
     If perm_n(X) = sum_{s=1}^{w_2} q_s(X) r_s(X) with deg(q_s) = deg(r_s) = k (n = 2k, ANY w1, w3,
     NO row-separation assumption!), then the common zero locus
       Z(q_1, ..., q_{w_2}, r_1, ..., r_{w_2}) subseteq Sing(V(perm_n))
     forces by Krull's Principal Ideal Theorem (over algebraically closed field):
       2 * w_2 >= codim_{P^{n^2 - 1}}(Sing(V(perm_n)))!
     We compute the exact local codimension of Sing(V(perm_n)) (for n = 3, 4, 5) by:
       (a) Exact Jacobian rank of grad(perm_n) = 0 on all combinatorial boundary strata (zero rows/cols,
           k x (n-k+1) zero blocks, rank-1 matrices, etc.), AND
       (b) Complex LM hunt for arbitrary smooth points of Sing(V(perm_4)) to detect any hidden
           higher-dimensional (lower-codimension!) irreducible component of Sing(V(perm_4))!
"""
from __future__ import annotations

import itertools
import time
from typing import List, Tuple

import numpy as np

from verify_0g_phase5b import build_perm4_rowml_target, run_rowml_lm


def perm_exact(mat: np.ndarray) -> complex:
    """Exact permanent of an n x n matrix via Ryser/permutation sum (n <= 5)."""
    n = mat.shape[0]
    total = 0.0 + 0.0j
    for pi in itertools.permutations(range(n)):
        prod = 1.0 + 0.0j
        for i in range(n):
            prod *= mat[i, pi[i]]
        total += prod
    return total


def grad_and_hess_perm(mat: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Exact gradient G[i,j] = d perm_n / d x_{ij} = perm_{n-1}(M^{i,j})
    and exact Hessian H[(i,j), (k,l)] = d^2 perm_n / (d x_{ij} d x_{kl}) = perm_{n-2}(M^{ik, jl}) (if i!=k, j!=l else 0).
    Note: The Jacobian of the n^2 equations {G[i,j](X) = 0} at X is EXACTLY the n^2 x n^2 Hessian H(X)!
    """
    n = mat.shape[0]
    grad = np.zeros((n, n), dtype=np.complex128)
    for i in range(n):
        rows = [r for r in range(n) if r != i]
        for j in range(n):
            cols = [c for c in range(n) if c != j]
            grad[i, j] = perm_exact(mat[np.ix_(rows, cols)])

    hess = np.zeros((n * n, n * n), dtype=np.complex128)
    for i in range(n):
        for j in range(n):
            idx1 = i * n + j
            for k in range(n):
                if k == i:
                    continue
                rows = [r for r in range(n) if r != i and r != k]
                for l in range(n):
                    if l == j:
                        continue
                    cols = [c for c in range(n) if c != j and c != l]
                    idx2 = k * n + l
                    if len(rows) == 0:
                        hess[idx1, idx2] = 1.0 + 0.0j
                    else:
                        hess[idx1, idx2] = perm_exact(mat[np.ix_(rows, cols)])
    return grad, hess


def find_singular_points_lm(n: int, rng: np.random.Generator, n_starts: int = 40) -> List[Tuple[int, float, np.ndarray]]:
    """Find arbitrary projective points on Sing(V(perm_n)) via damped LM on [grad(perm_n)(X) = 0, a^T X - 1 = 0].
    A generic linear hyperplane a^T X = 1 intersects EVERY positive-dimensional component of Sing(V(perm_n)) transversely!
    """
    found: List[Tuple[int, float, np.ndarray]] = []
    n2 = n * n

    for _ in range(n_starts):
        a = rng.standard_normal(n2) + 1j * rng.standard_normal(n2)
        a /= np.linalg.norm(a)
        x = rng.standard_normal(n2) + 1j * rng.standard_normal(n2)
        x /= np.dot(a, x)
        lam = 1e-3

        def eval_sys(xv: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
            g, h = grad_and_hess_perm(xv.reshape(n, n))
            fc = np.concatenate([g.reshape(n2), np.array([np.dot(a, xv) - 1.0])])
            jc = np.vstack([h, a.reshape(1, n2)])
            r_real = np.concatenate([fc.real, fc.imag])
            j_real = np.vstack([np.hstack([jc.real, -jc.imag]), np.hstack([jc.imag, jc.real])])
            return r_real, j_real

        r_real, j_real = eval_sys(x)
        cur = float(np.linalg.norm(r_real))
        for _it in range(120):
            if cur < 1e-12:
                break
            jtj = j_real.T @ j_real
            rhs = j_real.T @ r_real
            diag = np.maximum(np.diag(jtj), 1e-8)
            accepted = False
            for _try in range(6):
                lhs = jtj + lam * np.diag(diag)
                try:
                    step = -np.linalg.solve(lhs, rhs)
                except np.linalg.LinAlgError:
                    step, _, _, _ = np.linalg.lstsq(lhs, -rhs, rcond=None)
                xn = x + step[:n2] + 1j * step[n2:]
                rn, jn = eval_sys(xn)
                nn = float(np.linalg.norm(rn))
                if nn < cur:
                    x, r_real, j_real, cur = xn, rn, jn, nn
                    lam = max(lam * 0.3, 1e-12)
                    accepted = True
                    break
                lam = min(lam * 5.0, 1e8)
            if not accepted and lam >= 1e7:
                break

        g, h = grad_and_hess_perm(x.reshape(n, n))
        err = float(np.linalg.norm(g))
        if err < 1e-9 and np.linalg.norm(x) > 1e-3:
            # Verify rank of Hessian (exact local codimension of Sing(perm_n) at smooth point X!)
            svals = np.linalg.svd(h, compute_uv=False)
            rk = int(np.sum(svals > 1e-7 * svals[0])) if svals[0] > 1e-12 else 0
            found.append((rk, err, x.reshape(n, n)))
    return found


def check_known_strata_perm4(rng: np.random.Generator) -> None:
    print("=== 2A. Exact Local Codimension (Hessian Rank) on Known Strata of Sing(V(perm_4)) ===")

    # Stratum 1: Two zero rows (e.g. rows 0, 1 = 0) -> linear space of dim 8 in C^16 (codim 8)
    m1 = rng.standard_normal((4, 4)) + 1j * rng.standard_normal((4, 4))
    m1[0:2, :] = 0
    g1, h1 = grad_and_hess_perm(m1)
    assert np.linalg.norm(g1) < 1e-13
    print(f"  Stratum 1 (2 zero rows): ||grad||={np.linalg.norm(g1):.2e}, rank(Hess)={np.linalg.matrix_rank(h1, tol=1e-9)} (exact codim = 8)")

    # Stratum 2: One zero row (row 0) + one zero col (col 0) + perm_3(submatrix) = 0 -> codim 4 + 3 + 1 = 8
    m2 = rng.standard_normal((4, 4)) + 1j * rng.standard_normal((4, 4))
    m2[0, :] = 0
    m2[:, 0] = 0
    # Adjust m2[1,1] so perm_3(m2[1:, 1:]) == 0
    sub = m2[1:, 1:].copy()
    sub[0, 0] = 0
    c00 = perm_exact(sub[1:, 1:])
    rem = perm_exact(sub)
    m2[1, 1] = -rem / c00
    g2, h2 = grad_and_hess_perm(m2)
    assert np.linalg.norm(g2) < 1e-12
    print(f"  Stratum 2 (1 zero row + 1 zero col + perm_3=0): ||grad||={np.linalg.norm(g2):.2e}, rank(Hess)={np.linalg.matrix_rank(h2, tol=1e-9)} (exact codim = 8)")

    # Stratum 3: 2x3 zero block + 1x1 zero? Check 2x3 zero block alone:
    m3 = rng.standard_normal((4, 4)) + 1j * rng.standard_normal((4, 4))
    m3[0:2, 0:3] = 0
    g3, _ = grad_and_hess_perm(m3)
    print(f"  Check 2x3 zero block alone: ||grad||={np.linalg.norm(g3):.2e} (NOT singular unless extra eqs hold!)")
    # Wait: if m3[0:2, 0:3] = 0, which 3x3 sub-permanents are nonzero?
    # Omitting row 0 or row 1 and omitting col 0, 1, or 2 leaves a 1x2 zero block and a 2x1 column!
    # Wait: if we ALSO set m3[2:4, 3] = 0? Then col 3 is nonzero ONLY in rows 0,1, and cols 0,1,2 are nonzero ONLY in rows 2,3 -> block diagonal 2x1 and 2x3, ALL 3x3 sub-permanents vanish!!
    m3b = m3.copy()
    m3b[2:4, 3] = 0  # Total zeros: 6 + 2 = 8 zeros!
    g3b, _ = grad_and_hess_perm(m3b)
    print(f"  Check (2x3 zero + 2x1 zero): ||grad||={np.linalg.norm(g3b):.2e} (STILL NOT singular! Omitting row 0 & col 0 retains perm_2*x_{{1,3}}!)")

    # Stratum 4: What about det_4 for comparison? Rank-2 matrix has codim 4 in P^15!
    # What about rank-1 matrix for perm_4? Wait: perm_3(u v^T) = 6 * prod(u_i) * prod(v_j) != 0!
    # Unless u has >= 2 zeros (2 zero rows -> codim 8) or v has >= 2 zeros (2 zero cols -> codim 8)!
    # WAIT: What about a matrix with perm_4 = 0 and ALL 16 sub-permanents = 0 with NO zeros at all (dense singular point)?!
    # Let's check with LM!


def main() -> None:
    t0 = time.time()
    rng = np.random.default_rng(202611217)

    # 1. Referee audit on Phase 5B Pi_RowML at w2 = 2 and w2 = 1!
    print("=== 1. REFEREE AUDIT: Exact Pi_RowML ONLY (256 eqs) at w2 = 2 and w2 = 1 ===")
    target = build_perm4_rowml_target()
    for w2 in (2, 1):
        tw = time.time()
        solved, min_r, med_r = run_rowml_lm(w2, target, rng, n_starts=6, max_iters=120)
        print(
            f"  [Pi_RowML] w2={w2} [vars={16*(8+8*w2)}, eqs=256]: "
            f"solved={solved}/6, min={min_r:.3e}, med={med_r:.3e} ({time.time()-tw:.2f}s)"
        )

    # 2. Singular locus codimension of perm_3 and perm_4!
    print("\n=== 2. KRULL SINGULAR-LOCUS CODIMENSION AUDIT ===")
    check_known_strata_perm4(rng)

    print("\n=== 2B. Unconstrained Complex LM Hunt for Lowest-Codimension Component of Sing(V(perm_3)) ===")
    pts3 = find_singular_points_lm(3, rng, n_starts=25)
    rks3 = sorted([p[0] for p in pts3])
    print(f"  perm_3: found {len(pts3)}/25 singular points; Hessian ranks (local codims) = {set(rks3)}, min={min(rks3) if rks3 else None}")
    if pts3:
        min_rk3 = min(rks3)
        ex3 = [p[2] for p in pts3 if p[0] == min_rk3][0]
        print(f"  Example min-codim ({min_rk3}) singular point of perm_3 (abs entries):\n{np.round(np.abs(ex3), 3)}")

    print("\n=== 2C. Unconstrained Complex LM Hunt for Lowest-Codimension Component of Sing(V(perm_4)) ===")
    pts4 = find_singular_points_lm(4, rng, n_starts=40)
    rks4 = sorted([p[0] for p in pts4])
    from collections import Counter
    print(f"  perm_4: found {len(pts4)}/40 singular points; Hessian rank histogram = {dict(Counter(rks4))}")
    if pts4:
        min_rk4 = min(rks4)
        ex4 = [p[2] for p in pts4 if p[0] == min_rk4][0]
        print(f"  Example min-codim ({min_rk4}) singular point of perm_4 (abs entries):\n{np.round(np.abs(ex4), 3)}")
        print(f"  Number of near-zero entries (<1e-4): {int(np.sum(np.abs(ex4) < 1e-4))}/16")
        print(f"  Matrix rank of example point: {int(np.linalg.matrix_rank(ex4, tol=1e-6))}")

    print(f"\n[DONE] Phase 7B Audit finished in {time.time()-t0:.2f}s.")


if __name__ == "__main__":
    main()
