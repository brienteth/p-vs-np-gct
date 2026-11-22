"""Prof. Wigner: The Skeptic's Test.
Does LM from random starts find solutions for w=6 where a solution is PROVEN to exist (Grenet)?
If LM fails to find w=6 from random starts, then an LM floor of 2.26 for w=5 cannot be trusted
as evidence of non-existence!
"""
import numpy as np
from perm4_w5_factorization_search import (
    build_target_tensor, extract_middle_4x4, permanent_poly,
    run_lm, grenet_w6_factors, residual_only
)

def test_w6_random_starts():
    p4 = permanent_poly(4)
    P_perm = extract_middle_4x4(p4)
    T_perm, pairs2 = build_target_tensor(P_perm)

    Ug, Vg = grenet_w6_factors()
    res_grenet = np.max(np.abs(residual_only(Ug, Vg, T_perm, pairs2)))
    print(f"Verified: Grenet w=6 exact solution exists with residual = {res_grenet:.2e}")

    rng = np.random.default_rng(137) # Wigner's fine structure constant
    n_starts = 15
    w = 6
    scale = 1.0 / np.sqrt(w)
    residuals = []
    print(f"\nRunning LM on w=6 from {n_starts} random complex starts...")
    for s in range(n_starts):
        th0 = (rng.standard_normal(64 * w) + 1j * rng.standard_normal(64 * w)) * (scale / np.sqrt(2.0))
        res, _ = run_lm(th0, w, T_perm, pairs2, max_iter=300)
        residuals.append(res)
        print(f"  Start {s+1:2d}: final ||r||_2 = {res:.4f}")

    arr = np.array(residuals)
    n_solved = np.sum(arr < 1e-8)
    print(f"\nw=6 Results: min={np.min(arr):.4f}, median={np.median(arr):.4f}, max={np.max(arr):.4f}")
    print(f"Solved w=6 from random starts: {n_solved}/{n_starts}")

if __name__ == "__main__":
    test_w6_random_starts()
