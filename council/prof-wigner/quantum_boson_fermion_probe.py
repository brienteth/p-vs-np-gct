"""Prof. Wigner Round 8 (Wing 1 — Quantum Modeling):
Boson vs Fermion Representation, Non-Gaussianity / Plücker Violation,
Stabilizer Lie Algebra / Orbit Codimension, & Global Mixing Invariance Test
for perm_3, det_3, Grenet_7, and general affine det_m(A_0 + L(X)) projections.
"""
import itertools
import random
import numpy as np
import sys
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
from poly_exact import (
    Poly, add_poly, const_poly, determinant_poly, kth_partial_space,
    mul_poly, permanent_poly, rank_mod_p, var_poly, zero_poly
)
from grenet_verify import grenet_matrix_perm3
from affine_det_projection_probe import poly_det_mod, random_abp_det, syzygy_span, MOD
from shifted_pd_probe import monomials_of_degree_le

def poly_to_dense_sym_tensor_n3(p: Poly):
    """Convert homogeneous degree-3 poly in 9 vars to symmetric 9x9x9 tensor (Fock state in Sym^3(C^9))."""
    T = np.zeros((9, 9, 9), dtype=np.float64)
    for mon, coeff in p.items():
        assert sum(mon) == 3, f"Non-homogeneous term {mon}: {coeff}"
        idx = []
        for v, e in enumerate(mon):
            idx.extend([v] * e)
        perms = set(itertools.permutations(idx))
        val = float(coeff) / len(perms)
        for p_tup in perms:
            T[p_tup] = val
    return T

def poly_to_multilinear_n3(p: Poly):
    """Extract row-multilinear tensor Psi_{j0, j1, j2} = [x_{0,j0} x_{1,j1} x_{2,j2}] p in (C^3)^{otimes 3}."""
    Psi = np.zeros((3, 3, 3), dtype=np.float64)
    for j0 in range(3):
        for j1 in range(3):
            for j2 in range(3):
                m = [0] * 9
                m[0*3 + j0] += 1
                m[1*3 + j1] += 1
                m[2*3 + j2] += 1
                Psi[j0, j1, j2] = float(p.get(tuple(m), 0))
    return Psi

def plucker_and_wick_measures_n3(Psi: np.ndarray):
    """Given Psi in (C^3)^{otimes 3}, measure:
    1) Antisymmetric projection norm ||P_wedge(Psi)|| / ||Psi|| vs symmetric ||P_sym(Psi)|| / ||Psi||
    2) 1-body reduced density matrix rho_1 (3x3) purity Tr(rho_1^2) and von Neumann / Renyi-2 entropy
    3) Fermionic 3-body Plucker / Grassmannian relation violation (only nonzero if non-Slater in C^3 otimes C^3 otimes C^3!)
       Wait: in C^3, Lambda^3(C^3) is 1D, so ANY antisymmetric tensor is Slater!
       To test non-trivial Plucker violation, embed into 6-mode Fermionic Fock space (or use 9-mode Sym^3(C^9) / 27-dim)!
       Wait: let's compute the 1-body RDM across mode cuts of the full 9x9x9 tensor T (Fock representation in Sym^3(C^9))!
    """
    nrm = np.linalg.norm(Psi)
    if nrm < 1e-12:
        return {}
    Psi_n = Psi / nrm
    # 1-body RDM on site 0:
    rho1 = np.einsum("ijk,ljk->il", Psi_n, Psi_n)
    pur1 = float(np.trace(rho1 @ rho1))
    evals1 = np.maximum(np.linalg.eigvalsh(rho1), 0.0)
    s_vn1 = float(-np.sum(evals1[evals1 > 1e-12] * np.log2(evals1[evals1 > 1e-12])))
    s_renyi2_1 = float(-np.log2(max(pur1, 1e-15)))

    # Antisymmetric vs symmetric content under S_3 acting on (j0, j1, j2):
    P_asym = np.zeros_like(Psi_n)
    P_sym = np.zeros_like(Psi_n)
    for perm in itertools.permutations(range(3)):
        # sign of perm
        inv = sum(1 for a in range(3) for b in range(a+1, 3) if perm[a] > perm[b])
        sgn = -1.0 if (inv % 2) else 1.0
        Tp = np.transpose(Psi_n, perm)
        P_asym += sgn * Tp / 6.0
        P_sym += Tp / 6.0

    return {
        "asym_frac": float(np.sum(P_asym**2)),
        "sym_frac": float(np.sum(P_sym**2)),
        "rho1_purity": pur1,
        "S_vN_1": s_vn1,
        "S_Renyi2_1": s_renyi2_1,
    }

def full_9mode_quantum_measures(T: np.ndarray):
    """Treat T in Sym^3(C^9) as a 3-boson symmetric state on 9 modes (9x9x9 tensor, dim=729).
    Compute:
    1) 1-particle RDM rho_1 (9x9) spectrum, purity, Renyi-2 entropy
    2) Schmidt rank of T flattened as 9 x 81 (mode 1 vs modes 2,3)! Note: this IS GL_9 invariant!
    3) 2-particle RDM rho_2 (81x81) spectrum, purity, Renyi-2 entropy
    4) Flattenings / singular-value spectrum of T (9 x 81)!
    """
    nrm = np.linalg.norm(T)
    if nrm < 1e-12:
        return {}
    Tn = T / nrm
    # 1-body RDM: 9 x 9
    rho1 = np.einsum("ijk,ljk->il", Tn, Tn)
    svals_flat = np.linalg.svd(Tn.reshape(9, 81), compute_uv=False)
    schmidt_rk = int(np.sum(svals_flat > 1e-9))
    pur1 = float(np.trace(rho1 @ rho1))
    s_renyi2 = float(-np.log2(max(pur1, 1e-15)))
    evals1 = np.maximum(np.linalg.eigvalsh(rho1), 0.0)
    s_vn = float(-np.sum(evals1[evals1 > 1e-12] * np.log2(evals1[evals1 > 1e-12])))
    # 2-body RDM: 81 x 81
    rho2 = np.einsum("ijk,abk->ijab", Tn, Tn).reshape(81, 81)
    pur2 = float(np.trace(rho2 @ rho2))
    # Geometric entanglement proxy: max_u |<u,u,u|Tn>| (symmetric injective norm over 50 random restarts)
    rng = np.random.default_rng(42)
    best_ov = 0.0
    for _ in range(30):
        u = rng.standard_normal(9)
        u /= np.linalg.norm(u)
        for _ in range(15):
            # power iteration for symmetric best rank-1 approx: u_new = T(., u, u)
            v = np.einsum("ijk,j,k->i", Tn, u, u)
            vn = np.linalg.norm(v)
            if vn < 1e-12: break
            u = v / vn
        ov = abs(float(np.einsum("ijk,i,j,k->", Tn, u, u, u)))
        best_ov = max(best_ov, ov)
    geom_ent = float(-2.0 * np.log2(max(best_ov, 1e-15)))
    return {
        "schmidt_9x81": schmidt_rk,
        "pur1": pur1,
        "S_vN_9": s_vn,
        "S_R2_9": s_renyi2,
        "pur2": pur2,
        "geom_ent_approx": geom_ent,
        "top_svals": np.round(svals_flat[:5], 4).tolist(),
    }

def linear_stabilizer_dim_mod(p: Poly, num_vars: int = 9) -> int:
    """Exact dimension of {A in gl_{num_vars} : sum_{i,j} A_{i,j} x_j (dF/dx_i) == c * F} over F_MOD!
    This is 100% invariant under GL_{num_vars} global mixing X -> G X!
    """
    # Build partials df_i = dF / dx_i
    partials = kth_partial_space(p, num_vars, 1)
    # Wait: kth_partial_space returns NON-ZERO partials in order? Let's compute dF/dx_i explicitly!
    df = []
    for i in range(num_vars):
        d: Poly = {}
        for m, c in p.items():
            if m[i] > 0:
                nm = list(m); nm[i] -= 1
                val = (c * m[i]) % MOD
                if val != 0:
                    d[tuple(nm)] = val
        df.append(d)

    # Generators: x_j * df_i for all i, j in 0..num_vars-1 (81 generators), PLUS (-F) for scalar lambda (1 gen)
    gens = []
    for i in range(num_vars):
        for j in range(num_vars):
            gens.append(mul_poly(var_poly(j, num_vars), df[i]))
    neg_p = {m: (-c) % MOD for m, c in p.items() if c % MOD != 0}
    gens.append(neg_p)
    rk = rank_mod_p(gens, mod=MOD)
    return len(gens) - rk # includes (A, lambda); dim g_lin = (82 - rk) (1D for scaling I, rest nontrivial!)

def apply_gl_mixing_poly(p: Poly, G: np.ndarray, mod: int = MOD) -> Poly:
    """Substitute x_i -> sum_j G_{i,j} x_j mod `mod` into homogeneous degree-3 poly in 9 vars."""
    # Convert to symmetric tensor mod `mod`, transform, convert back!
    T = np.zeros((9, 9, 9), dtype=np.int64)
    for m, c in p.items():
        idx = []
        for v, e in enumerate(m): idx.extend([v] * e)
        # Put all coeff on one canonical ordered tuple (avoid /6!), then contract G!
        # Wait: sum_{p} G[i0, p0] G[i1, p1] G[i2, p2] T[i0, i1, i2] works directly on ANY tensor with sum(perms)=coeff!
        T[idx[0], idx[1], idx[2]] = (T[idx[0], idx[1], idx[2]] + c) % mod
    # Contract T with G on all 3 axes: T'[j0, j1, j2] = sum_{i0,i1,i2} T[i0,i1,i2] G[i0,j0] G[i1,j1] G[i2,j2]
    T1 = np.tensordot(T, G, axes=([0], [0])) % mod # (i1, i2, j0)
    T2 = np.tensordot(T1, G, axes=([0], [0])) % mod # (i2, j0, j1)
    T3 = np.tensordot(T2, G, axes=([0], [0])) % mod # (j0, j1, j2)
    out: Poly = {}
    for j0 in range(9):
        for j1 in range(9):
            for j2 in range(9):
                val = int(T3[j0, j1, j2]) % mod
                if val != 0:
                    m = [0]*9; m[j0]+=1; m[j1]+=1; m[j2]+=1
                    mt = tuple(m)
                    nv = (out.get(mt, 0) + val) % mod
                    if nv == 0: out.pop(mt, None)
                    else: out[mt] = nv
    return out

def main():
    print("=" * 78)
    print("PROF. WIGNER ROUND 8: BOSON VS FERMION QUANTUM INVARIANTS & GLOBAL MIXING TEST")
    print("=" * 78)
    p3 = permanent_poly(3)
    d3 = determinant_poly(3)
    g3 = poly_det_mod(grenet_matrix_perm3(), mod=MOD)
    # Note: poly_det of grenet_matrix_perm3 over Z is exact perm_3!
    from poly_exact import poly_det
    g3_exact = poly_det(grenet_matrix_perm3(), 9)
    assert g3_exact == p3, "Grenet 7x7 must equal perm_3 identically!"

    # Random invertible GL_9 mixing matrix over Z / F_MOD (small entries for float stability too!)
    rng_np = np.random.default_rng(137)
    G_small = rng_np.integers(-2, 3, size=(9, 9))
    while abs(np.linalg.det(G_small)) < 0.5:
        G_small = rng_np.integers(-2, 3, size=(9, 9))

    d3_mixed = apply_gl_mixing_poly(d3, G_small % MOD, mod=MOD)
    p3_mixed = apply_gl_mixing_poly(p3, G_small % MOD, mod=MOD)

    # Also construct random homogeneous degree-3 ABP det_m projections (m=4, 5, 6, 7)
    rng_py = random.Random(42)
    # Wait: random_abp_det uses mod=1_000_000_007 by default! Let's build over Z using poly_det!
    def random_abp_det_Z(m: int):
        l1_size = max(1, (m - 1) // 2)
        l1 = list(range(1, 1 + l1_size))
        l2 = list(range(1 + l1_size, m)) or l1
        mat = [[zero_poly() for _ in range(m)] for _ in range(m)]
        for i in range(1, m): mat[i][i] = const_poly(1, 9)
        def rl():
            p = {}
            for v in range(9):
                c = rng_py.randint(-2, 2)
                if c != 0: p = add_poly(p, var_poly(v, 9, c))
            return p
        for u in l1: mat[0][u] = rl()
        for u in l1:
            for v in l2:
                if u != v: mat[u][v] = rl()
        for v in l2: mat[v][0] = rl()
        return poly_det(mat, 9)

    models = [
        ("det_3 (Fermionic Gaussian)", d3),
        ("det_3_GL9_mixed", d3_mixed),
        ("perm_3 == Grenet_7 (Bosonic)", p3),
        ("perm_3_GL9_mixed", p3_mixed),
        ("rand_ABP_det_4", random_abp_det_Z(4)),
        ("rand_ABP_det_5", random_abp_det_Z(5)),
        ("rand_ABP_det_6", random_abp_det_Z(6)),
    ]

    print("\n--- TABLE 1: Algebraic / Lie Symmetry Invariants (Exact mod 1,000,003) ---")
    print(f"{'Model':30s} | {'dim g_lin':9s} | {'syz_1(F)':8s} | {'syz_2(F)':8s} | {'span(x<=1 d=1)':14s}")
    print("-" * 78)
    for name, poly in models:
        g_dim = linear_stabilizer_dim_mod(poly, 9)
        s1_span, s1_gens = syzygy_span(poly, 9, k=1, shift_deg=1)
        s2_span, s2_gens = syzygy_span(poly, 9, k=1, shift_deg=2)
        print(f"{name:30s} | {g_dim:9d} | {s1_gens - s1_span:8d} | {s2_gens - s2_span:8d} | {s1_span:4d}/{s1_gens:<9d}")

    print("\n--- TABLE 2: Quantum 9-Mode Boson State Sym^3(C^9) Entanglement & Schmidt Rank ---")
    # Note: for float tensor, apply G_small over R to det_3 and perm_3!
    def transform_tensor_R(T, G):
        # x_i -> (G x)_i corresponds to contracting G on each mode!
        return np.einsum("ijk,ia,jb,kc->abc", T, G, G, G)

    T_d3 = poly_to_dense_sym_tensor_n3(d3)
    T_p3 = poly_to_dense_sym_tensor_n3(p3)
    T_models = [
        ("det_3", T_d3),
        ("det_3_GL9_mixed", transform_tensor_R(T_d3, G_small.astype(float))),
        ("perm_3 (== Grenet_7)", T_p3),
        ("perm_3_GL9_mixed", transform_tensor_R(T_p3, G_small.astype(float))),
        ("rand_ABP_det_4", poly_to_dense_sym_tensor_n3(models[4][1])),
        ("rand_ABP_det_5", poly_to_dense_sym_tensor_n3(models[5][1])),
        ("rand_ABP_det_6", poly_to_dense_sym_tensor_n3(models[6][1])),
    ]
    print(f"{'Model':24s} | {'rk_9x81':7s} | {'pur1':6s} | {'S_vN':6s} | {'S_R2':6s} | {'geom_E':6s} | {'top svals (9x81)'}")
    print("-" * 78)
    for name, T in T_models:
        q = full_9mode_quantum_measures(T)
        print(f"{name:24s} | {q['schmidt_9x81']:7d} | {q['pur1']:.4f} | {q['S_vN_9']:.4f} | {q['S_R2_9']:.4f} | {q['geom_ent_approx']:.4f} | {q['top_svals']}")

    print("\n--- TABLE 3: 3-Qudit Multilinear Sector (C^3)^{otimes 3} (Fails Global Mixing Test!) ---")
    for name, poly in [("det_3", d3), ("det_3_GL9_mixed (non-multilinear!)", d3_mixed), ("perm_3", p3)]:
        # Note: d3_mixed mod MOD has large positive entries; use R tensor for d3_mixed!
        if "mixed" in name:
            Tm = transform_tensor_R(T_d3, G_small.astype(float))
            # Extract [x_{0,j0} x_{1,j1} x_{2,j2}] = 6 * Tm[j0, 3+j1, 6+j2]
            Psi = 6.0 * Tm[:3, 3:6, 6:9]
        else:
            Psi = poly_to_multilinear_n3(poly)
        m_res = plucker_and_wick_measures_n3(Psi)
        print(f"  {name:34s}: asym_frac={m_res.get('asym_frac',0):.4f}, sym_frac={m_res.get('sym_frac',0):.4f}, pur1={m_res.get('rho1_purity',0):.4f}")

if __name__ == "__main__":
    main()
