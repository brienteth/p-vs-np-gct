"""Prof. Wigner Round 10 (Representation-Theoretic Gluing & Symmetry-Locked Obstruction):
1. Check whether Grenet_7(X) lifts S_3^{col} and S_3^{row} to internal GL_7 x GL_7 gauge (P M(X) = M(g.X) R).
2. Compute exact S_3 x S_3 irrep energy spectrum (all 9 irreps lambda_L x lambda_R) in Sym^3(C^9)
   for det_3, perm_3, rand_ABP_det_4..7!
3. Compute exact GL_3 x GL_3 Young-diagram decomposition (lambda = (3), (2,1), (1,1,1) in Cauchy's
   Sym^3(C^3 otimes C^3) = sum S_lambda x S_lambda) for det_3, perm_3, rand_ABP_det_6, rand_ABP_det_7!
"""
import itertools
import random
import numpy as np
import sys
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
from poly_exact import Poly, determinant_poly, permanent_poly, rank_mod_p
from grenet_verify import grenet_matrix_perm3
from affine_det_projection_probe import MOD
from quantum_cumulant_and_gct_probe import (
    non_layered_nilpotent_det_Z, poly_to_dense_sym_tensor_general
)


def grenet_matrix_slices_R():
    """Extract constant A_0 and 9 coefficient matrices L_v (v=0..8) of Grenet's 7x7 matrix M(X)."""
    gm = grenet_matrix_perm3()  # 7x7 of Poly in 9 vars
    A0 = np.zeros((7, 7), dtype=np.float64)
    Ls = [np.zeros((7, 7), dtype=np.float64) for _ in range(9)]
    for i in range(7):
        for j in range(7):
            p = gm[i][j]
            for mon, coeff in p.items():
                if sum(mon) == 0:
                    A0[i, j] += float(coeff)
                else:
                    v = mon.index(1)
                    Ls[v][i, j] += float(coeff)
    return A0, Ls


def check_pencil_equivalence(A0, Ls, perm_var_fn, label: str):
    """Solve linear system P A0 - A0 R = 0, P L_v - L_{perm(v)} R = 0 for (P, R) in M_7 x M_7.
    Check nullspace dimension and max determinant/rank of solutions (P, R)!"""
    # Unknowns: vec(P) (49) + vec(R) (49) = 98 unknowns.
    # For each slice k in {const, 0..8} (10 slices of 7x7 = 490 equations):
    # (P M1_k - M2_k R)_{ij} = sum_a P_{ia} M1_k[a,j] - sum_b M2_k[i,b] R_{bj} = 0
    M1 = [A0] + Ls
    M2 = [A0] + [Ls[perm_var_fn(v)] for v in range(9)]
    eqs = []
    for k in range(10):
        A = M1[k]
        B = M2[k]
        for i in range(7):
            for j in range(7):
                row = np.zeros(98, dtype=np.float64)
                for a in range(7):
                    row[i * 7 + a] += A[a, j]
                for b in range(7):
                    row[49 + b * 7 + j] -= B[i, b]
                eqs.append(row)
    Mat = np.array(eqs)
    _, svals, Vt = np.linalg.svd(Mat)
    null_vecs = Vt[svals < 1e-9] if len(svals) == 98 else Vt[np.sum(svals > 1e-9):]
    # Better: compute exact rank with tol=1e-9
    rk = int(np.sum(svals > 1e-9))
    null_dim = 98 - rk
    max_det_P = 0.0
    if null_dim > 0:
        basis = Vt[rk:]
        rng = np.random.default_rng(7)
        for _ in range(20):
            c = rng.standard_normal(null_dim)
            vec = c @ basis
            P = vec[:49].reshape(7, 7)
            R = vec[49:].reshape(7, 7)
            if abs(np.linalg.det(P)) > 1e-8 and abs(np.linalg.det(R)) > 1e-8:
                max_det_P = max(max_det_P, abs(np.linalg.det(P)))
    print(f"  {label:32s}: null_dim(P,R) = {null_dim:2d}, invertible lift exists? {max_det_P > 1e-8} (max |det P|={max_det_P:.3e})")


def s3_irrep_characters():
    """Irreps of S_3: (3) triv, (2,1) std, (1,1,1) sign. Class reps by cycle type."""
    def cycle_type(perm):
        seen = [False]*3
        lens = []
        for i in range(3):
            if not seen[i]:
                c = 0; j = i
                while not seen[j]:
                    seen[j] = True; j = perm[j]; c += 1
                lens.append(c)
        return tuple(sorted(lens, reverse=True))
    chars = {
        "(3)": {(1,1,1): 1.0, (2,1): 1.0, (3,): 1.0},
        "(2,1)": {(1,1,1): 2.0, (2,1): 0.0, (3,): -1.0},
        "(1,1,1)": {(1,1,1): 1.0, (2,1): -1.0, (3,): 1.0},
    }
    dims = {"(3)": 1, "(2,1)": 2, "(1,1,1)": 1}
    return cycle_type, chars, dims


def s3xs3_spectrum_in_sym3(T_sym: np.ndarray):
    """Compute exact L2 energy fraction of T_sym (shape 9,9,9) in each of the 9 S_3 x S_3 irreps!"""
    cycle_type, chars, dims = s3_irrep_characters()
    nrm2 = float(np.sum(T_sym ** 2))
    # Map each of 36 group elements (pr, pc) to variable permutation on 0..8
    var_pos = np.arange(9).reshape(3, 3)
    orbit_T = {}
    for pr in itertools.permutations(range(3)):
        for pc in itertools.permutations(range(3)):
            vp = var_pos[np.ix_(pr, pc)].reshape(9)
            # T'(i,j,k) = T(vp[i], vp[j], vp[k])
            Tp = T_sym[np.ix_(vp, vp, vp)]
            orbit_T[(pr, pc)] = Tp
    # Compute <T, g.T> for all g in S_3 x S_3
    ips = {g: float(np.sum(T_sym * Tp)) / nrm2 for g, Tp in orbit_T.items()}
    spec = {}
    for l1 in ["(3)", "(2,1)", "(1,1,1)"]:
        for l2 in ["(3)", "(2,1)", "(1,1,1)"]:
            d = dims[l1] * dims[l2]
            proj = 0.0
            for (pr, pc), val in ips.items():
                chi = chars[l1][cycle_type(pr)] * chars[l2][cycle_type(pc)]
                proj += d * chi * val
            spec[f"{l1}x{l2}"] = proj / 36.0
    return spec


def gl3xgl3_cauchy_proj(T_sym: np.ndarray):
    """In Sym^3(C^3 otimes C^3) = S_(3)xS_(3) + S_(2,1)xS_(2,1) + S_(1,1,1)xS_(1,1,1),
    Wait: S_lambda(C^3) x S_lambda(C^3) is an irrep of GL_3 x GL_3!
    How do we project a tensor T[(i0,j0), (i1,j1), (i2,j2)] (symmetric in the 3 pairs) onto lambda in {(3), (2,1), (1,1,1)}?
    By Schur-Weyl duality, the Young projector c_lambda acting on the 3 ROW indices (i0, i1, i2) ONLY
    automatically projects onto S_lambda(C^3) x S_lambda(C^3)!! (Because T is symmetric under joint swap of (i_k, j_k),
    symmetrizing/antisymmetrizing rows automatically forces matching Young symmetry on cols!)"""
    T6 = T_sym.reshape(3, 3, 3, 3, 3, 3)  # (i0, j0, i1, j1, i2, j2)
    # Apply S_3 central Young idempotent P_lambda = (d_lambda / 6) sum_{s in S_3} chi_lambda(s) s_rows
    _, chars, dims = s3_irrep_characters()
    nrm2 = float(np.sum(T6 ** 2))
    # Permute ONLY row axes (0, 2, 4) while keeping col axes (1, 3, 5) fixed!
    projs = {}
    for lam in ["(3)", "(2,1)", "(1,1,1)"]:
        P_T = np.zeros_like(T6)
        for s in itertools.permutations(range(3)):
            # cycle type
            seen = [False]*3; lens = []
            for a in range(3):
                if not seen[a]:
                    c = 0; b = a
                    while not seen[b]: seen[b]=True; b=s[b]; c+=1
                    lens.append(c)
            ct = tuple(sorted(lens, reverse=True))
            w = chars[lam][ct]
            # permute row axes (0, 2, 4) -> (2*s[0], 2*s[1], 2*s[2])
            axes = [2*s[0], 1, 2*s[1], 3, 2*s[2], 5]
            P_T += w * np.transpose(T6, axes)
        P_T *= dims[lam] / 6.0
        projs[lam] = float(np.sum(P_T ** 2)) / nrm2
    return projs


def main():
    print("=" * 88)
    print("PROF. WIGNER ROUND 10: REPRESENTATION-THEORETIC GLUING & SYMMETRY OBSTRUCTIONS")
    print("=" * 88)

    print("\n--- PART 1: Can Grenet_7(X) Lift S_3^{row} & S_3^{col} to Internal GL_7 x GL_7 Gauge? ---")
    A0, Ls = grenet_matrix_slices_R()
    check_pencil_equivalence(A0, Ls, lambda v: v, "Identity (Endomorphism P,R)")
    # Col swap (0 <-> 1): v = 3*r + c -> 3*r + (1 if c==0 else (0 if c==1 else 2))
    check_pencil_equivalence(A0, Ls, lambda v: 3 * (v // 3) + ({0: 1, 1: 0, 2: 2}[v % 3]), "S_3^col swap (0 <-> 1)")
    check_pencil_equivalence(A0, Ls, lambda v: 3 * (v // 3) + ((v % 3 + 1) % 3), "S_3^col 3-cycle (0->1->2)")
    # Row swap (0 <-> 1):
    check_pencil_equivalence(A0, Ls, lambda v: 3 * ({0: 1, 1: 0, 2: 2}[v // 3]) + (v % 3), "S_3^row swap (0 <-> 1)")
    check_pencil_equivalence(A0, Ls, lambda v: 3 * ((v // 3 + 1) % 3) + (v % 3), "S_3^row 3-cycle (0->1->2)")
    # Transpose (r <-> c):
    check_pencil_equivalence(A0, Ls, lambda v: 3 * (v % 3) + (v // 3), "Matrix Transpose X -> X^T")

    p3 = permanent_poly(3)
    d3 = determinant_poly(3)
    rng = random.Random(42)
    abp4 = non_layered_nilpotent_det_Z(4, 3, rng)
    abp5 = non_layered_nilpotent_det_Z(5, 3, rng)
    abp6 = non_layered_nilpotent_det_Z(6, 3, rng)
    abp7 = non_layered_nilpotent_det_Z(7, 3, rng)

    models = [
        ("det_3", d3),
        ("perm_3 (== Grenet_7)", p3),
        ("rand_ABP_det_4", abp4),
        ("rand_ABP_det_5", abp5),
        ("rand_ABP_det_6", abp6),
        ("rand_ABP_det_7", abp7),
    ]

    print("\n--- PART 2: GL_3 x GL_3 Cauchy Young-Diagram Decomposition Sym^3(C^3 x C^3) ---")
    print("  Sym^3(C^9) = [S_(3)xS_(3) (dim 100)] + [S_(2,1)xS_(2,1) (dim 64)] + [S_(1,1,1)xS_(1,1,1) (dim 1)]")
    print(f"  {'Model':22s} | {'lam=(3)':8s} | {'lam=(2,1)':9s} | {'lam=(1,1,1)':11s}")
    print("  " + "-" * 58)
    for name, poly in models:
        T = poly_to_dense_sym_tensor_general(poly, 9, 3)
        pr = gl3xgl3_cauchy_proj(T)
        print(f"  {name:22s} | {pr['(3)']:8.4f} | {pr['(2,1)']:9.4f} | {pr['(1,1,1)']:11.4f}")

    print("\n--- PART 3: Discrete S_3 x S_3 Irrep Energy Spectrum inside Sym^3(C^9) ---")
    keys = ["(3)x(3)", "(3)x(2,1)", "(2,1)x(3)", "(2,1)x(2,1)", "(1,1,1)x(1,1,1)", "other_sgn"]
    print(f"  {'Model':22s} | {'(3)x(3)':7s} | {'(3)x(2,1)':9s} | {'(2,1)x(3)':9s} | {'(2,1)^2':7s} | {'(1^3)^2':7s} | {'other':7s}")
    print("  " + "-" * 78)
    for name, poly in models:
        T = poly_to_dense_sym_tensor_general(poly, 9, 3)
        sp = s3xs3_spectrum_in_sym3(T)
        other = 1.0 - (sp["(3)x(3)"] + sp["(3)x(2,1)"] + sp["(2,1)x(3)"] + sp["(2,1)x(2,1)"] + sp["(1,1,1)x(1,1,1)"])
        print(f"  {name:22s} | {sp['(3)x(3)']:7.4f} | {sp['(3)x(2,1)']:9.4f} | {sp['(2,1)x(3)']:9.4f} | {sp['(2,1)x(2,1)']:7.4f} | {sp['(1,1,1)x(1,1,1)']:7.4f} | {other:7.4f}")


if __name__ == "__main__":
    main()
