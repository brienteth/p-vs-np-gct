"""Prof. Wigner Round 8 (Wing 1 — Quantum Modeling):
Test GL_{n^2}-invariant quantum/physics diagnostics:
1. Connected k-point logarithmic cumulants (Feynman loop correlators of -log F(X)):
   - kappa_2 = -d^2 log F (Hessian of free energy, n^2 x n^2)
   - kappa_3 = -d^3 log F (3-point connected vertex, n^2 x n^4 flattening!)
   Wait: check invariance of rank(kappa_2) and rank(kappa_3_flat) under GL_{n^2} global mixing!
2. Non-layered globally-mixed degree-3 affine determinants det_m(A_0 + L(X)) (via similarity conjugation
   P (A_0 + N(X)) P^{-1} + compensating Schur complements) vs perm_3 and det_3!
3. Compare n=3 and n=4 (det_4 vs perm_4)!
"""
import itertools
import random
import numpy as np
import sys
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
from poly_exact import (
    Poly, add_poly, const_poly, determinant_poly, mul_poly, permanent_poly,
    poly_det, rank_mod_p, var_poly, zero_poly
)
from grenet_verify import grenet_matrix_perm3
from affine_det_projection_probe import syzygy_span, MOD
from quantum_boson_fermion_probe import (
    linear_stabilizer_dim_mod, poly_to_dense_sym_tensor_n3, apply_gl_mixing_poly
)

def eval_poly_and_derivs_R(T_sym: np.ndarray, x: np.ndarray):
    """Given symmetric tensor T_sym of degree n (shape (N,)*n where F(x) = T_sym[x,...,x]),
    compute exact F(x), grad F (N,), Hess F (N,N), and 3rd derivative D3 F (N,N,N)!
    Wait: for general degree n, T_sym[i1,...,in] * x[i1]...x[in] gives F(x)!
    """
    deg = T_sym.ndim
    N = T_sym.shape[0]
    if deg == 3:
        # F = T[x, x, x]
        Tx = np.einsum("ijk,k->ij", T_sym, x)
        Txx = np.einsum("ij,j->i", Tx, x)
        F = float(np.dot(Txx, x))
        grad = 3.0 * Txx
        hess = 6.0 * Tx
        d3 = 6.0 * T_sym
        return F, grad, hess, d3
    elif deg == 4:
        Tx = np.einsum("ijkl,l->ijk", T_sym, x)
        Txx = np.einsum("ijk,k->ij", Tx, x)
        Txxx = np.einsum("ij,j->i", Txx, x)
        F = float(np.dot(Txxx, x))
        grad = 4.0 * Txxx
        hess = 12.0 * Txx
        d3 = 24.0 * Tx
        return F, grad, hess, d3
    else:
        raise ValueError("Only deg 3, 4")

def log_cumulants(T_sym: np.ndarray, x: np.ndarray):
    """Compute 2-point and 3-point connected logarithmic cumulants of -log F(x):
    kappa_1 = d_i log F = g_i / F
    kappa_2 = d_i d_j log F = (H_ij F - g_i g_j) / F^2
    kappa_3 = d_i d_j d_k log F = (D3_ijk F^2 - F(H_ij g_k + H_ik g_j + H_jk g_i) + 2 g_i g_j g_k) / F^3
    """
    F, g, H, D3 = eval_poly_and_derivs_R(T_sym, x)
    assert abs(F) > 1e-8
    k1 = g / F
    k2 = (H * F - np.outer(g, g)) / (F**2)
    term2 = np.einsum("ij,k->ijk", H, g) + np.einsum("ik,j->ijk", H, g) + np.einsum("jk,i->ijk", H, g)
    term3 = 2.0 * np.einsum("i,j,k->ijk", g, g, g)
    k3 = (D3 * (F**2) - F * term2 + term3) / (F**3)
    return k1, k2, k3

def poly_to_dense_sym_tensor_general(p: Poly, N: int, deg: int):
    T = np.zeros((N,) * deg, dtype=np.float64)
    for mon, coeff in p.items():
        assert sum(mon) == deg
        idx = []
        for v, e in enumerate(mon):
            idx.extend([v] * e)
        perms = set(itertools.permutations(idx))
        val = float(coeff) / len(perms)
        for pt in perms:
            T[pt] = val
    return T

def non_layered_nilpotent_det_Z(m: int, deg: int, rng: random.Random):
    """Construct a NON-layered globally-mixed degree-`deg` affine determinant of size m x m
    satisfying det(A_0 + t L(X)) == t^deg F(X) identically!
    Method: Start from a block-nilpotent DAG with max path length `deg` (so det(I + t N) == 1
    or root-sink det(A_0 + t M) = t^deg F), THEN conjugate by random invertible integer P, Q in GL_m(Z)
    with det(P) = det(Q) = 1! That globally mixes rows/cols of M(X) AND A_0!
    Wait: conjugating by P, Q in GL_m(Z) leaves det(A_0 + L(X)) identical, wait — it changes the
    matrix entries, NOT the polynomial! To get a NON-layered *polynomial* det_m(A_0 + L(X)),
    use a NON-layered (arbitrary upper-triangular with MULTIPLE sources/sinks or rank-3 A_0 = diag(0_3, I_{m-3})
    with general dense nilpotent subblocks!).
    Actually: if A_0 = diag(0_3, I_{m-3}), and M(X) = A_0 + L(X) where ALL blocks interact,
    how do we ensure det(A_0 + t L(X)) has ONLY degree 3?
    Put an arbitrary dense strictly-upper-triangular matrix U(X) of size m x m (with A_0 = diag(0_3, I_{m-3})?
    Wait: for A_0 = diag(0_3, I_{m-3}) + strictly upper triangular U(X) + rank-1 lower feedback?
    Even better: a block-3 cycle-cover determinant where ALL 9 variables enter EVERY edge, AND
    conjugate by P, Q in SL_m(Z)!)
    Wait: conjugating M(X) -> P M(X) Q changes M(X), NOT the polynomial det(M(X))!
    Wait: random_abp_det_Z ALREADY had all 9 variables entering every edge (global mixing in X!),
    AND had layers l1 -> l2. To also allow skip-edges (0 -> 0 directly, 0 -> l2, l1 -> 0 directly = non-layered!),
    we just keep A_0 = diag(0, 1, ..., 1) and add a random strictly upper-triangular nilpotent DAG of
    longest path <= 3 from 0 back to 0! Wait: with skip-edges, deg can be 1 or 2 unless 0->0, 0->l2, l1->0 are 0!
    In fact, ANY degree-3 homogeneous polynomial with A_0 = diag(0, 1..1) and nilpotent M_0 + L(X)
    has longest cycle through 0 of length 3 -> which IS a 3-layer DAG (possibly with edge from l1 directly to sink? No, length 2 cycle creates degree 2)!
    WHAT IF A_0 = diag(0, 0, 1..1) (corank 2!) or A_0 = diag(0, 0, 0, 1..1) (corank 3!)?!
    YES!! If A_0 = diag(0, 0, 0, I_{m-3}) (corank 3!), then the 3 zeros on the diagonal FORCE deg >= 3,
    AND if the bottom-right (m-3)x(m-3) block is I + N(X) (nilpotent) while the top-left 3x3 block is linear L_3(X)
    plus cross-couplings to the nilpotent block, Wait — then N(X) can still have non-zero entries, creating deg 4, 5...!
    To make det == pure deg 3 with corank 3: the 3x3 Schur complement must be degree 3, so N(X) cannot feed into it unless its contribution cancels!
    Wait: a simple non-layered rank-(m-2) or rank-(m-3) pure degree-3 polynomial is:
    det([ [L_11(X), L_12(X)], [0, L_22(X)] ]) where L_11 is 2x2 linear, L_22 is (m-2)x(m-2) Grenet-style degree 1!
    Better: let's test BOTH `rand_ABP_det_m` (which ALREADY mixes all 9 vars X globally!) AND `rank-2 + rank-1` block sums / products!
    """
    l1_size = max(1, (m - 1) // 2)
    l1 = list(range(1, 1 + l1_size))
    l2 = list(range(1 + l1_size, m)) or l1
    mat = [[zero_poly() for _ in range(m)] for _ in range(m)]
    for i in range(1, m): mat[i][i] = const_poly(1, 9)
    def rl():
        p = {}
        for v in range(9):
            c = rng.randint(-2, 2)
            if c != 0: p = add_poly(p, var_poly(v, 9, c))
        return p
    for u in l1: mat[0][u] = rl()
    for u in l1:
        for v in l2:
            if u != v: mat[u][v] = rl()
    for v in l2: mat[v][0] = rl()
    return poly_det(mat, 9)

def main():
    print("=" * 78)
    print("PROF. WIGNER ROUND 8: LOGARITHMIC FEYNMAN CUMULANTS (k2, k3) & n=3 vs n=4")
    print("=" * 78)
    p3 = permanent_poly(3)
    d3 = determinant_poly(3)
    rng_py = random.Random(42)
    rng_np = np.random.default_rng(137)

    # Test n=3 models
    T_d3 = poly_to_dense_sym_tensor_general(d3, 9, 3)
    T_p3 = poly_to_dense_sym_tensor_general(p3, 9, 3)

    # Apply random GL_9 global mixing over R
    G = rng_np.standard_normal((9, 9))
    T_d3_mix = np.einsum("ijk,ia,jb,kc->abc", T_d3, G, G, G)
    T_p3_mix = np.einsum("ijk,ia,jb,kc->abc", T_p3, G, G, G)

    x0 = rng_np.standard_normal(9)
    # Transform point consistently for covariance check: if F'(x) = F(G x), then x0 -> G^{-1} x0 gives same invariants!
    # Also test at an INDEPENDENT random point x1!
    x1 = rng_np.standard_normal(9)

    print("\n--- TABLE A: n=3 Connected Logarithmic Cumulants kappa_2 (9x9) & kappa_3 (9x81) ---")
    print(f"{'Model':24s} | {'rk(k2)':6s} | {'rk(k3_9x81)':11s} | {'top svals of k3 (9x81)'}")
    print("-" * 78)
    n3_list = [
        ("det_3 (at x1)", T_d3, x1),
        ("det_3_GL9_mixed (at x1)", T_d3_mix, x1),
        ("perm_3 (at x1)", T_p3, x1),
        ("perm_3_GL9_mixed (at x1)", T_p3_mix, x1),
        ("rand_ABP_det_4", poly_to_dense_sym_tensor_general(non_layered_nilpotent_det_Z(4, 3, rng_py), 9, 3), x1),
        ("rand_ABP_det_5", poly_to_dense_sym_tensor_general(non_layered_nilpotent_det_Z(5, 3, rng_py), 9, 3), x1),
        ("rand_ABP_det_6", poly_to_dense_sym_tensor_general(non_layered_nilpotent_det_Z(6, 3, rng_py), 9, 3), x1),
    ]
    for name, T, pt in n3_list:
        k1, k2, k3 = log_cumulants(T, pt)
        rk2 = np.linalg.matrix_rank(k2, tol=1e-8)
        svals3 = np.linalg.svd(k3.reshape(9, 81), compute_uv=False)
        rk3 = int(np.sum(svals3 > 1e-8))
        print(f"{name:24s} | {rk2:6d} | {rk3:11d} | {np.round(svals3[:5], 4).tolist()}")

    # NOW TEST n = 4: det_4 vs perm_4!
    print("\n--- TABLE B: n=4 (16 variables) Lie Stabilizer, syz_1, & Log Cumulants ---")
    p4 = permanent_poly(4)
    d4 = determinant_poly(4)
    g_d4 = linear_stabilizer_dim_mod(d4, 16)
    g_p4 = linear_stabilizer_dim_mod(p4, 16)
    s1_d4_span, s1_d4_gens = syzygy_span(d4, 16, k=1, shift_deg=1)
    s1_p4_span, s1_p4_gens = syzygy_span(p4, 16, k=1, shift_deg=1)
    print(f"  det_4 : dim g_lin = {g_d4:3d}, syz_1 = {s1_d4_gens - s1_d4_span:3d} (span {s1_d4_span}/{s1_d4_gens})")
    print(f"  perm_4: dim g_lin = {g_p4:3d}, syz_1 = {s1_p4_gens - s1_p4_span:3d} (span {s1_p4_span}/{s1_p4_gens})")

    T_d4 = poly_to_dense_sym_tensor_general(d4, 16, 4)
    T_p4 = poly_to_dense_sym_tensor_general(p4, 16, 4)
    x4 = rng_np.standard_normal(16)
    for name, T in [("det_4", T_d4), ("perm_4", T_p4)]:
        k1, k2, k3 = log_cumulants(T, x4)
        rk2 = np.linalg.matrix_rank(k2, tol=1e-8)
        svals3 = np.linalg.svd(k3.reshape(16, 256), compute_uv=False)
        rk3 = int(np.sum(svals3 > 1e-8))
        print(f"  {name:6s} log cumulants: rk(k2) = {rk2}/16, rk(k3_16x256) = {rk3}/16, top svals(k3) = {np.round(svals3[:5], 4).tolist()}")

if __name__ == "__main__":
    main()
