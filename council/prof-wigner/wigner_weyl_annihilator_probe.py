"""Prof. Wigner Round 8: Weyl-Algebra / Second-Order Differential Annihilators,
k=2 Shifted Partials, and Hessian Rank on Smooth Locus V(F) for n=3 and n=4!
"""
import random
import numpy as np
import sys
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
from poly_exact import (
    Poly, add_poly, const_poly, determinant_poly, kth_partial_space,
    mul_poly, permanent_poly, poly_det, rank_mod_p, var_poly, zero_poly
)
from affine_det_projection_probe import syzygy_span, MOD
from shifted_pd_probe import monomials_of_degree_le
from quantum_cumulant_and_gct_probe import (
    non_layered_nilpotent_det_Z, poly_to_dense_sym_tensor_general, eval_poly_and_derivs_R
)

def random_homogeneous_poly_Z(num_vars: int, deg: int, rng: random.Random) -> Poly:
    mons = [next(iter(pm.keys())) for pm in monomials_of_degree_le(num_vars, deg)]
    mons = [m for m in mons if sum(m) == deg]
    p: Poly = {}
    for m in mons:
        c = rng.randint(-3, 3)
        if c != 0:
            p[m] = c
    return p

def hessian_rank_on_VF(T_sym: np.ndarray, rng_np: np.random.Generator, trials: int = 10) -> int:
    """Find a generic smooth zero x0 of F(x) = 0 by fixing all-but-one coordinates on a line
    and solving the degree-n univariate equation for the root! Then compute rank(Hess F(x0))."""
    deg = T_sym.ndim
    N = T_sym.shape[0]
    max_rk = 0
    for _ in range(trials):
        u = rng_np.standard_normal(N)
        v = rng_np.standard_normal(N)
        # F(u + t v) = sum_{k=0}^deg c_k t^k = 0
        # Compute coefficients via evaluating at deg+1 points or Vandermonde
        ts = np.linspace(-2.0, 2.0, deg + 1)
        vals = [eval_poly_and_derivs_R(T_sym, u + t * v)[0] for t in ts]
        coeffs = np.polyfit(ts, vals, deg) # highest power first
        roots = np.roots(coeffs)
        # pick a real root if available, else complex? Use complex Hessian too!
        real_roots = [r.real for r in roots if abs(r.imag) < 1e-7]
        if not real_roots:
            r = roots[0]
            x0 = u + r * v
            # complex eval
            if deg == 3:
                H = 6.0 * np.einsum("ijk,k->ij", T_sym, x0)
                F0 = float(np.abs(np.einsum("ijk,i,j,k->", T_sym, x0, x0, x0)))
            else:
                H = 12.0 * np.einsum("ijkl,l->ijk", T_sym, x0)
                H = np.einsum("ijk,k->ij", H, x0)
                F0 = float(np.abs(np.einsum("ijkl,i,j,k,l->", T_sym, x0, x0, x0, x0)))
        else:
            x0 = u + real_roots[0] * v
            F0, _, H, _ = eval_poly_and_derivs_R(T_sym, x0)
        assert abs(F0) < 1e-6, f"Root accuracy {F0}"
        rk = int(np.linalg.matrix_rank(H, tol=1e-7))
        max_rk = max(max_rk, rk)
    return max_rk

def main():
    print("=" * 78)
    print("PROF. WIGNER ROUND 8: SHIFTED PD (k=1,2), GENERIC BASELINE & HESSIAN ON V(F)")
    print("=" * 78)
    p3 = permanent_poly(3)
    d3 = determinant_poly(3)
    rng_py = random.Random(42)
    rng_np = np.random.default_rng(137)

    gen3 = random_homogeneous_poly_Z(9, 3, rng_py)
    abp4 = non_layered_nilpotent_det_Z(4, 3, rng_py)
    abp5 = non_layered_nilpotent_det_Z(5, 3, rng_py)
    # Test best of 5 random ABP det_6
    abp6_list = [non_layered_nilpotent_det_Z(6, 3, rng_py) for _ in range(5)]

    models = [
        ("det_3", d3),
        ("perm_3 (== Grenet_7)", p3),
        ("generic_deg3 (9 vars)", gen3),
        ("rand_ABP_det_4", abp4),
        ("rand_ABP_det_5", abp5),
    ] + [(f"rand_ABP_det_6 #{i+1}", p) for i, p in enumerate(abp6_list)]

    print("\n--- n=3 GL_9-Invariant Shifted PD Dimensions & Hessian Rank on V(F) ---")
    print(f"{'Model':23s} | {'k=1,s=1':10s} | {'k=1,s=2':10s} | {'k=2,s=1':10s} | {'k=2,s=2':10s} | {'rk Hess|V(F)'}")
    print("-" * 82)
    for name, poly in models:
        s11, g11 = syzygy_span(poly, 9, k=1, shift_deg=1)
        s12, g12 = syzygy_span(poly, 9, k=1, shift_deg=2)
        s21, g21 = syzygy_span(poly, 9, k=2, shift_deg=1)
        s22, g22 = syzygy_span(poly, 9, k=2, shift_deg=2)
        T = poly_to_dense_sym_tensor_general(poly, 9, 3)
        rk_v = hessian_rank_on_VF(T, rng_np, trials=8)
        print(f"{name:23s} | {s11:3d}/{g11:<6d} | {s12:3d}/{g12:<6d} | {s21:3d}/{g21:<6d} | {s22:3d}/{g22:<6d} | {rk_v:2d}/9")

    print("\n--- n=4 (16 vars) Baseline Comparison ---")
    p4 = permanent_poly(4)
    d4 = determinant_poly(4)
    for name, poly in [("det_4", d4), ("perm_4", p4)]:
        s11, g11 = syzygy_span(poly, 16, k=1, shift_deg=1)
        s21, g21 = syzygy_span(poly, 16, k=2, shift_deg=1)
        T4 = poly_to_dense_sym_tensor_general(poly, 16, 4)
        rk_v = hessian_rank_on_VF(T4, rng_np, trials=8)
        print(f"  {name:8s}: (k=1,s=1)={s11}/{g11}, (k=2,s=1)={s21}/{g21}, max rk(Hess|_V(F))={rk_v}/16")

if __name__ == "__main__":
    main()
