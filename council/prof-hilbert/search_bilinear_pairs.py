"""Prof. Hilbert Round 7 (Gap 3): Alternating-SVD & Grassmannian Discovery of ALL Maximal Orthogonal Pairs (U, V)
with B(U, V) = 0 and dim U + dim V >= 11 over R and C!
"""
import itertools
from collections import Counter
import numpy as np


def build_G_slices():
    subsets2 = sorted(itertools.combinations(range(6), 2), key=lambda s: (s[1], s[0]))
    idx2 = {s: i for i, s in enumerate(subsets2)}
    subsets3 = list(itertools.combinations(range(6), 3))
    G6 = np.zeros((20, 15), dtype=float)
    for s_idx, S in enumerate(subsets3):
        Sc = set(range(6)) - set(S)
        for J in itertools.combinations(sorted(Sc), 2):
            G6[s_idx, idx2[J]] = 1.0
    E_S = np.zeros((20, 15, 6), dtype=float)
    for s_idx, S in enumerate(subsets3):
        for c in S:
            I = tuple(sorted(set(S) - {c}))
            E_S[s_idx, idx2[I], c] = 1.0
    return np.einsum("sj,sic->cij", G6, E_S)  # (6, 15, 15)


def alt_svd_search(G_slices, p, q, n_starts=60, max_iter=250, complex_mode=False):
    rng = np.random.default_rng(1000 + p * 100 + q + (1 if complex_mode else 0))
    solutions = []
    non_fiber_examples = []
    min_loss = float("inf")
    for st in range(n_starts):
        if complex_mode:
            U = rng.standard_normal((15, p)) + 1j * rng.standard_normal((15, p))
        else:
            U = rng.standard_normal((15, p))
        U, _ = np.linalg.qr(U)
        for it in range(max_iter):
            M_U = np.vstack([U.conj().T @ G_slices[c] for c in range(6)])
            _, s_U, Vh = np.linalg.svd(M_U, full_matrices=True)
            V = Vh[-q:, :].conj().T
            M_V = np.vstack([V.conj().T @ G_slices[c] for c in range(6)])
            _, s_V, Uh = np.linalg.svd(M_V, full_matrices=True)
            U = Uh[-p:, :].conj().T
            loss = float(np.sum(s_V[-p:] ** 2))
            if loss < 1e-22:
                break
        if loss < min_loss:
            min_loss = loss
        if loss < 1e-12:
            M_U = np.vstack([U.conj().T @ G_slices[c] for c in range(6)])
            _, s1, Vh1 = np.linalg.svd(M_U, full_matrices=True)
            rk1 = int(np.sum(s1 > 1e-7))
            dV_max = 15 - rk1
            V_max = Vh1[rk1:, :].conj().T
            M_V = np.vstack([V_max.conj().T @ G_slices[c] for c in range(6)])
            _, s2, Uh2 = np.linalg.svd(M_V, full_matrices=True)
            rk2 = int(np.sum(s2 > 1e-7))
            dU_max = 15 - rk2
            U_max = Uh2[rk2:, :].conj().T

            # Check if U_max or V_max is contained in N(lambda) (i.e. rk_lam <= 5)
            Phi_U = np.vstack([np.einsum("cij,j->ic", G_slices, U_max[:, k]) for k in range(dU_max)])
            rk_lam_U = int(np.sum(np.linalg.svd(Phi_U, compute_uv=False) > 1e-7))
            Phi_V = np.vstack([np.einsum("cij,j->ic", G_slices, V_max[:, k]) for k in range(dV_max)])
            rk_lam_V = int(np.sum(np.linalg.svd(Phi_V, compute_uv=False) > 1e-7))
            # Keep ordering by (dU_max <= dV_max)
            if dU_max <= dV_max:
                sig = (dU_max, dV_max, rk_lam_U, rk_lam_V)
            else:
                sig = (dV_max, dU_max, rk_lam_V, rk_lam_U)
            solutions.append(sig)
            if rk_lam_U == 6 and rk_lam_V == 6:
                non_fiber_examples.append((dU_max, dV_max, U_max, V_max))

    mode_str = "C" if complex_mode else "R"
    print(f"({p:2d}, {q:2d}) [{mode_str}]: {len(solutions):2d}/{n_starts} solved, min_loss={min_loss:.3e}, "
          f"maximal (dU, dV, rk_lam_U, rk_lam_V) = {dict(Counter(solutions))}")
    return non_fiber_examples


if __name__ == "__main__":
    G_slices = build_G_slices()
    all_non_fiber = []
    for p, q in [(2, 9), (3, 8), (4, 7), (5, 6)]:
        all_non_fiber.extend(alt_svd_search(G_slices, p, q, n_starts=60, max_iter=300, complex_mode=False))
        all_non_fiber.extend(alt_svd_search(G_slices, p, q, n_starts=40, max_iter=300, complex_mode=True))
    print(f"\nTotal NON-FIBER (rk_lam_U == 6 AND rk_lam_V == 6) solutions found across 400 starts: {len(all_non_fiber)}")
