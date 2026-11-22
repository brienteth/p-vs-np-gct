"""Prof. Wigner Round 8: Test globally mixed m=7 ABP (same size as Grenet_7!)
and test GL_9-invariant D-module / logarithmic derivation filtrations:
1. Shifted PD (k=1,2; s=1,2) + Hessian rank on V(F) for rand_ABP_det_7.
2. Quadratic logarithmic derivations Der_2(-log F) = {v in Vect_2 : v(F) in <F>},
   which are vector fields tangent to V(F) with quadratic coefficients (GL_9-invariant!).
3. Constant-coeff apolarity (F^perp)_2 = {P in C[d_1..d_9]_2 : P(F) = 0} (GL_9-invariant!).
"""
import random
import numpy as np
import sys
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
from poly_exact import (
    Poly, add_poly, determinant_poly, mul_poly, permanent_poly, rank_mod_p, var_poly
)
from affine_det_projection_probe import syzygy_span, MOD
from shifted_pd_probe import monomials_of_degree_le
from quantum_cumulant_and_gct_probe import (
    non_layered_nilpotent_det_Z, poly_to_dense_sym_tensor_general
)
from wigner_weyl_annihilator_probe import random_homogeneous_poly_Z, hessian_rank_on_VF


def partial_poly(p: Poly, var_idx: int) -> Poly:
    out: Poly = {}
    for mon, coeff in p.items():
        e = mon[var_idx]
        if e > 0:
            nm = list(mon)
            nm[var_idx] = e - 1
            t = tuple(nm)
            out[t] = (out.get(t, 0) + coeff * e) % MOD
            if out[t] == 0:
                del out[t]
    return out


def mul_poly_mod(a: Poly, b: Poly) -> Poly:
    out: Poly = {}
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            t = tuple(x + y for x, y in zip(m1, m2))
            out[t] = (out.get(t, 0) + c1 * c2) % MOD
            if out[t] == 0:
                del out[t]
    return out


def der_k_log_dim_mod(p: Poly, num_vars: int, coeff_deg: int) -> tuple:
    """Compute dim of {v = sum_i a_i(x) d_i : deg(a_i) == coeff_deg, v(p) == q(x)*p}
    mod MOD, plus the quotient dimension (vector fields tangent modulo trivial Koszul syzygies)!
    For coeff_deg=1: outputs (dim Der_1(-log F), total ops = N*N).
    For coeff_deg=2: outputs (dim Der_2(-log F), trivial_koszul_dim, total_ops).
    Wait: trivial syzygies where v(p) == 0 include Koszul pairs (d_j p) d_i - (d_i p) d_j (for coeff_deg=deg-1=2!).
    """
    mons_all = [next(iter(pm.keys())) for pm in monomials_of_degree_le(num_vars, coeff_deg)]
    mons_a = [m for m in mons_all if sum(m) == coeff_deg]
    mons_q_all = [next(iter(pm.keys())) for pm in monomials_of_degree_le(num_vars, coeff_deg - 1)]
    mons_q = [m for m in mons_q_all if sum(m) == coeff_deg - 1]

    partials = [partial_poly(p, i) for i in range(num_vars)]
    polys = []
    # Unknowns: for each (i, m_a) -> m_a * d_i p; for each m_q -> - m_q * p
    for i in range(num_vars):
        for m_a in mons_a:
            mp = {m_a: 1}
            polys.append(mul_poly_mod(mp, partials[i]))
    for m_q in mons_q:
        mp = {m_q: MOD - 1}
        polys.append(mul_poly_mod(mp, p))

    rk = rank_mod_p(polys, MOD)
    total_unknowns = len(polys)
    nullity = total_unknowns - rk
    return nullity, total_unknowns


def apolar_deg2_dim_mod(p: Poly, num_vars: int) -> tuple:
    """Compute dim (F^perp)_2 = {P in C[d_1..d_N]_2 : P(F) = 0} mod MOD."""
    mons_all = [next(iter(pm.keys())) for pm in monomials_of_degree_le(num_vars, 2)]
    mons_2 = [m for m in mons_all if sum(m) == 2]
    partials = [partial_poly(p, i) for i in range(num_vars)]
    polys = []
    for m in mons_2:
        nz = [i for i, e in enumerate(m) if e > 0]
        if len(nz) == 1:
            i = nz[0]
            q = partial_poly(partials[i], i)
        else:
            i, j = nz[0], nz[1]
            q = partial_poly(partials[i], j)
        polys.append(q)
    rk = rank_mod_p(polys, MOD)
    return len(mons_2) - rk, len(mons_2)


def main():
    print("=" * 84)
    print("PROF. WIGNER ROUND 8: m=7 ABP STRESS TEST, Der_2(-log F), AND APOLAR (F^perp)_2")
    print("=" * 84)
    p3 = permanent_poly(3)
    d3 = determinant_poly(3)
    rng_py = random.Random(42)
    rng_np = np.random.default_rng(137)
    gen3 = random_homogeneous_poly_Z(9, 3, rng_py)
    abp6 = non_layered_nilpotent_det_Z(6, 3, rng_py)
    abp7_list = [non_layered_nilpotent_det_Z(7, 3, rng_py) for _ in range(3)]

    models = [
        ("det_3", d3),
        ("perm_3 (== Grenet_7)", p3),
        ("generic_deg3 (9 vars)", gen3),
        ("rand_ABP_det_6", abp6),
    ] + [(f"rand_ABP_det_7 #{i+1}", p) for i, p in enumerate(abp7_list)]

    print(f"\n{'Model':22s} | {'k=1,s=1':8s} | {'k=1,s=2':8s} | {'k=2,s=2':9s} | {'Hess|VF':7s} | {'Der1':6s} | {'Der2':10s} | {'(F^perp)_2'}")
    print("-" * 96)
    for name, poly in models:
        s11, g11 = syzygy_span(poly, 9, k=1, shift_deg=1)
        s12, g12 = syzygy_span(poly, 9, k=1, shift_deg=2)
        s22, g22 = syzygy_span(poly, 9, k=2, shift_deg=2)
        T = poly_to_dense_sym_tensor_general(poly, 9, 3)
        rk_v = hessian_rank_on_VF(T, rng_np, trials=8)
        d1, t1 = der_k_log_dim_mod(poly, 9, 1)
        d2, t2 = der_k_log_dim_mod(poly, 9, 2)
        ap2, tap2 = apolar_deg2_dim_mod(poly, 9)
        print(f"{name:22s} | {s11:3d}/{g11:<4d} | {s12:3d}/{g12:<4d} | {s22:3d}/{g22:<5d} | {rk_v:2d}/9    | {d1:2d}/{t1:<3d} | {d2:3d}/{t2:<6d} | {ap2:2d}/{tap2:<2d}")


if __name__ == "__main__":
    main()
