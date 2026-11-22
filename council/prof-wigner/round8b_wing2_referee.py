"""Prof. Wigner Round 8B: Referee Suite for Wing 2 (0G Council) Proposals:
- 0g-pisagor (SFSS / U(1) phase symmetry vs GL_9 mixing & rand_ABP_det_7)
- 0g-oklid (Genus g vs Grenet m=2^n-1 & Galluccio-Loebl 4^g bound)
- 0g-arsimet (Morse / Gradient-Flow Trapping on S^8 under GL_9 mixing & rand_ABP_det_7,
  PLUS exact GL_9-invariant Milnor Algebra / Sing(V(F)) Hilbert Function dim(R/Jac(F))_d for d=2..5!)
"""
import random
import numpy as np
from scipy.optimize import minimize
import sys
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
from poly_exact import Poly, determinant_poly, permanent_poly, rank_mod_p
from affine_det_projection_probe import MOD
from shifted_pd_probe import monomials_of_degree_le
from quantum_boson_fermion_probe import (
    poly_to_dense_sym_tensor_n3, apply_gl_mixing_poly, linear_stabilizer_dim_mod
)
from quantum_cumulant_and_gct_probe import (
    non_layered_nilpotent_det_Z, poly_to_dense_sym_tensor_general, eval_poly_and_derivs_R
)
from wigner_weyl_annihilator_probe import random_homogeneous_poly_Z
from round8_dmodule_and_m7_probe import partial_poly, mul_poly_mod


def milnor_algebra_hilbert_dims(p: Poly, num_vars: int = 9, max_d: int = 5) -> list:
    """Compute exact GL_N-invariant Hilbert function dim (R / Jac(F))_d mod MOD
    for degrees d = 2, ..., max_d, where Jac(F) = <d_1 F, ..., d_N F>."""
    partials = [partial_poly(p, i) for i in range(num_vars)]
    dims = []
    for d in range(2, max_d + 1):
        shift_deg = d - 2
        mons_all = [next(iter(pm.keys())) for pm in monomials_of_degree_le(num_vars, shift_deg)]
        mons_s = [m for m in mons_all if sum(m) == shift_deg]
        polys = []
        for i in range(num_vars):
            for ms in mons_s:
                polys.append(mul_poly_mod({ms: 1}, partials[i]))
        rk = rank_mod_p(polys, MOD)
        # Total monomials of degree d in num_vars vars: C(num_vars + d - 1, d)
        from math import comb
        total_d = comb(num_vars + d - 1, d)
        dims.append((d, total_d - rk, total_d))
    return dims


def gradient_flow_sphere_traps(T_sym: np.ndarray, rng_np: np.random.Generator, n_trials: int = 25):
    """Minimize E_F(x) = |F(x)|^2 on S^{N-1} via spherical L-BFGS-B from random unit vectors.
    Reports (fraction reaching V(F) with E < 1e-8, median E_final, min E_final)."""
    N = T_sym.shape[0]
    finals = []
    for _ in range(n_trials):
        x_init = rng_np.standard_normal(N)
        x_init /= np.linalg.norm(x_init)

        def obj_and_grad(z):
            nrm = np.linalg.norm(z)
            x = z / nrm
            F, g, _, _ = eval_poly_and_derivs_R(T_sym, x)
            E = F * F
            # grad_x E = 2 F g; pullback through x = z / ||z||:
            gE_x = 2.0 * F * g
            gE_z = (gE_x - np.dot(gE_x, x) * x) / nrm
            return E, gE_z

        res = minimize(obj_and_grad, x_init, jac=True, method="L-BFGS-B",
                       options={"maxiter": 400, "ftol": 1e-14, "gtol": 1e-10})
        finals.append(float(res.fun))
    arr = np.array(finals)
    reached = int(np.sum(arr < 1e-8))
    return reached, float(np.median(arr)), float(np.min(arr)), float(np.max(arr))


def gradient_flow_sing_traps(T_sym: np.ndarray, rng_np: np.random.Generator, n_trials: int = 25):
    """Minimize E_sing(x) = ||grad F(x)||^2 on S^{N-1} via spherical L-BFGS-B (matching
    verify_quantum_vs_nature_bridge.py Part B1). Reports (reached Sing with E < 1e-8, median, min)."""
    N = T_sym.shape[0]
    finals = []
    for _ in range(n_trials):
        x_init = rng_np.standard_normal(N)
        x_init /= np.linalg.norm(x_init)

        def obj(z):
            x = z / np.linalg.norm(z)
            _, g, _, _ = eval_poly_and_derivs_R(T_sym, x)
            return float(np.dot(g, g))

        res = minimize(obj, x_init, method="BFGS", options={"maxiter": 200})
        finals.append(float(res.fun))
    arr = np.array(finals)
    return int(np.sum(arr < 1e-8)), float(np.median(arr)), float(np.min(arr))


def main():
    print("=" * 88)
    print("PROF. WIGNER ROUND 8B: REFEREEING WING 2 (PISAGOR, OKLID, ARSIMET)")
    print("=" * 88)
    p3 = permanent_poly(3)
    d3 = determinant_poly(3)
    rng_py = random.Random(42)
    rng_np = np.random.default_rng(2026)

    gen3 = random_homogeneous_poly_Z(9, 3, rng_py)
    abp6 = non_layered_nilpotent_det_Z(6, 3, rng_py)
    abp7 = non_layered_nilpotent_det_Z(7, 3, rng_py)

    # GL_9 integer mixing matrix (small entries, invertible mod MOD)
    while True:
        G_int = np.array([[rng_py.randint(-1, 1) for _ in range(9)] for _ in range(9)], dtype=np.int64)
        if abs(round(np.linalg.det(G_int))) == 1:
            break
    d3_mix = apply_gl_mixing_poly(d3, G_int % MOD, mod=MOD)
    p3_mix = apply_gl_mixing_poly(p3, G_int % MOD, mod=MOD)

    models = [
        ("det_3", d3),
        ("det_3_GL9_mixed", d3_mix),
        ("perm_3 (== Grenet_7)", p3),
        ("perm_3_GL9_mixed", p3_mix),
        ("rand_ABP_det_6", abp6),
        ("rand_ABP_det_7", abp7),
        ("generic_deg3 (9 vars)", gen3),
    ]

    print("\n--- PART 1 & 3: GL_9-Invariant Milnor Algebra dim(R / Jac(F))_d (Sing(V(F)) Topology!) ---")
    print("Note: For smooth V(F) in P^8 (isolated 0), (1+t)^9 gives d=2..4: 36, 84, 126.")
    print(f"{'Model':22s} | {'dim g_lin':9s} | {'d=2 (45)':9s} | {'d=3 (165)':9s} | {'d=4 (495)'}")
    print("-" * 70)
    for name, poly in models:
        gdim = linear_stabilizer_dim_mod(poly, 9)
        hdims = milnor_algebra_hilbert_dims(poly, 9, max_d=4)
        vals = [hd[1] for hd in hdims]
        print(f"{name:22s} | {gdim:9d} | {vals[0]:9d} | {vals[1]:9d} | {vals[2]:9d}")

    print("\n--- PART 2: Arsimet Energy Landscape E_F = |F|^2 on S^8 (25 spherical L-BFGS-B starts) ---")
    print("Testing BOTH GL_9 invariance AND whether rand_ABP_det_7 mimics frustrated glass traps!")
    G_real = rng_np.standard_normal((9, 9))
    T_d3 = poly_to_dense_sym_tensor_general(d3, 9, 3)
    T_p3 = poly_to_dense_sym_tensor_general(p3, 9, 3)
    T_d3_mix = np.einsum("ijk,ia,jb,kc->abc", T_d3, G_real, G_real, G_real)
    T_p3_mix = np.einsum("ijk,ia,jb,kc->abc", T_p3, G_real, G_real, G_real)

    landscapes = [
        ("det_3", T_d3),
        ("det_3_GL9_real", T_d3_mix),
        ("perm_3", T_p3),
        ("perm_3_GL9_real", T_p3_mix),
        ("rand_ABP_det_6", poly_to_dense_sym_tensor_general(abp6, 9, 3)),
        ("rand_ABP_det_7", poly_to_dense_sym_tensor_general(abp7, 9, 3)),
        ("generic_deg3", poly_to_dense_sym_tensor_general(gen3, 9, 3)),
    ]
    print(f"{'Model':22s} | {'Reached V(F)':12s} | {'Median E':10s} | {'Min E':10s} | {'Max E':10s}")
    print("-" * 74)
    for name, T in landscapes:
        reached, med_e, min_e, max_e = gradient_flow_sphere_traps(T, rng_np, n_trials=25)
        print(f"{name:22s} | {reached:2d}/25        | {med_e:10.3e} | {min_e:10.3e} | {max_e:10.3e}")

    print("\n--- PART 2B: Arsimet E_sing = ||grad F||^2 on S^8 (matching Wing 2 B1!) ---")
    print(f"{'Model':22s} | {'Reached Sing':12s} | {'Median ||g||^2':14s} | {'Min ||g||^2':12s}")
    print("-" * 70)
    for name, T in landscapes:
        r_s, med_s, min_s = gradient_flow_sing_traps(T, rng_np, n_trials=25)
        print(f"{name:22s} | {r_s:2d}/25        | {med_s:14.3e} | {min_s:12.3e}")


if __name__ == "__main__":
    main()
