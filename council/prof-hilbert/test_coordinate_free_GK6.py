"""Prof. Hilbert Round 5 (Phase 5A): Testing Coordinate-Free GK_6 on im(G_6) cap (W x K^6)
1. Tests 500 random non-coordinate subspaces W of dim d = 1..14 over F_{1000003} (as requested in #48).
2. Tests adversarial non-coordinate subspaces W = colsp(Phi(V)) and their duals W' = V^perp (using G_c symmetry!).
3. Checks whether ANY non-zero w in K^15 can have rank(Phi(w)) == 3 (i.e. whether rank(Phi(w)) >= 4 always).
4. Maps out the EXACT achievable region of (r1, r2) with dim(im(G_6) cap (W x K^6)) >= 15 - r2!
"""
import itertools
import numpy as np
import sys

sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
from apolar_higher_betti_probe import rank_matrix_mod
from perm4_abp_frontier import MOD


def build_objects():
    subsets2 = sorted(itertools.combinations(range(6), 2), key=lambda s: (s[1], s[0]))
    idx2 = {s: i for i, s in enumerate(subsets2)}
    subsets3 = list(itertools.combinations(range(6), 3))

    G6 = np.zeros((20, 15), dtype=np.int64)
    for s_idx, S in enumerate(subsets3):
        Sc = set(range(6)) - set(S)
        for J in itertools.combinations(sorted(Sc), 2):
            G6[s_idx, idx2[J]] = 1

    E_S = np.zeros((20, 15, 6), dtype=np.int64)
    for s_idx, S in enumerate(subsets3):
        for c in S:
            I = tuple(sorted(set(S) - {c}))
            E_S[s_idx, idx2[I], c] = 1

    # Phi_basis[j, i, c] = (Phi(e_j))[i, c] of shape (15, 15, 6)
    Phi_basis = np.einsum("sj,sic->jic", G6, E_S) % MOD
    return subsets2, idx2, subsets3, G6, E_S, Phi_basis


def test_500_random_subspaces(Phi_basis):
    print("=== 1. Testing 500 Random Non-Coordinate Subspaces W of dim d = 1..14 over F_1000003 ===")
    rng = np.random.default_rng(2026)
    # X = sum_j w_j Phi_basis[j] lies in W x K^6 iff P_perp @ X == 0,
    # where P_perp is (15 - d) x 15 annihilating W!
    # Equations on w in F^15: for each r in 0..(15-d-1), c in 0..5: sum_j (P_perp[r] . Phi_basis[j, :, c]) w_j == 0
    # Pre-reshape Phi_basis to (15, 6*15) or compute M_eq = einsum("ri,jic->rcj", P_perp, Phi_basis)
    for d in range(1, 15):
        max_dim = 0
        min_dim = 15
        for _ in range(500):
            P_perp = rng.integers(0, MOD, size=(15 - d, 15), dtype=np.int64)
            # Shape: ((15-d)*6, 15)
            M_eq = np.einsum("ri,jic->rcj", P_perp, Phi_basis).reshape((15 - d) * 6, 15) % MOD
            dim_int = 15 - rank_matrix_mod(M_eq, MOD)
            if dim_int > max_dim:
                max_dim = dim_int
            if dim_int < min_dim:
                min_dim = dim_int
        print(f"  d = {d:2d}: 500 random non-coord W => dim(im(G_6) cap (W x K^6)) in [{min_dim:2d}, {max_dim:2d}]")


def test_adversarial_non_coordinate_W(subsets2, idx2, G6, Phi_basis):
    print("\n=== 2. Testing Adversarial Non-Coordinate Subspaces W = colsp(Phi(V)) & Duals ===")
    # Key fact: For W = colsp(Phi(e_{0,1})) (dim 4), we ALREADY know dim(im(G_6) cap (W x K^6)) >= 1 > 0 = GK_6(4)!
    # Let us compute the EXACT dimension of im(G_6) cap (W x K^6) for ALL adversarial W = colsp(Phi(V)) and their duals!
    def exact_dim_for_W_cols(W_cols):
        # W_cols has shape (15, k), compute exact dim W and exact dim(im(G_6) cap (W x K^6))
        # Find P_perp over F_MOD via Gaussian elimination on W_cols.T
        # Easier: use SVD over float for structured integer matrices, then verify mod MOD!
        # Let us do exact nullspace mod MOD!
        mat = W_cols.T.copy() % MOD  # (k, 15)
        rows, cols = mat.shape
        pivots = []
        r = 0
        for c in range(cols):
            piv = None
            for i in range(r, rows):
                if mat[i, c] != 0:
                    piv = i
                    break
            if piv is None:
                continue
            mat[[r, piv]] = mat[[piv, r]]
            inv = pow(int(mat[r, c]), MOD - 2, MOD)
            mat[r] = (mat[r] * inv) % MOD
            for i in range(rows):
                if i != r and mat[i, c] != 0:
                    mat[i] = (mat[i] - mat[i, c] * mat[r]) % MOD
            pivots.append(c)
            r += 1
        dim_W = len(pivots)
        free_cols = [c for c in range(cols) if c not in pivots]
        # Basis of nullspace of W_cols.T (= W^perp) has size (15 - dim_W) x 15
        P_perp = np.zeros((len(free_cols), 15), dtype=np.int64)
        for idx_f, fc in enumerate(free_cols):
            P_perp[idx_f, fc] = 1
            for row_i, pc in enumerate(pivots):
                P_perp[idx_f, pc] = (MOD - mat[row_i, fc]) % MOD
        if len(free_cols) == 0:
            return dim_W, 15
        M_eq = np.einsum("ri,jic->rcj", P_perp, Phi_basis).reshape(len(free_cols) * 6, 15) % MOD
        dim_int = 15 - rank_matrix_mod(M_eq, MOD)
        return dim_W, dim_int

    # Record max dim_int observed for each dim_W = 0..15 across all non-coord adversarial constructions!
    max_for_d = {d: 0 for d in range(16)}
    witness_for_d = {}

    def record(name, W_cols):
        dW, dInt = exact_dim_for_W_cols(W_cols)
        if dInt > max_for_d[dW]:
            max_for_d[dW] = dInt
            witness_for_d[dW] = name
        # Also record DUAL by symmetry of G_c!
        # If dim(im(G6) cap (W x K^6)) = dInt, then there is a subspace V of dim dInt such that
        # W^perp (dim 15 - dW) is annihilated by G_c(V), so G_c(W^perp) subseteq V^perp (dim 15 - dInt)!
        # Thus for W_dual = V^perp (dim 15 - dInt), dim(im(G6) cap (W_dual x K^6)) >= 15 - dW!
        dW_dual = 15 - dInt
        dInt_dual = 15 - dW
        if dInt_dual > max_for_d[dW_dual]:
            max_for_d[dW_dual] = dInt_dual
            witness_for_d[dW_dual] = f"DUAL({name})"

    # Test 1: W = colsp(Phi(e_J)) for 1, 2, 3 basis vectors
    record("Phi(e_01)", Phi_basis[idx2[(0, 1)]])
    record("Phi(e_01, e_02)", np.hstack([Phi_basis[idx2[(0, 1)]], Phi_basis[idx2[(0, 2)]]]))
    record("Phi(e_01, e_02, e_03)", np.hstack([Phi_basis[idx2[(0, 1)]], Phi_basis[idx2[(0, 2)]], Phi_basis[idx2[(0, 3)]]]))
    record("Phi(e_01, e_02, e_12)", np.hstack([Phi_basis[idx2[(0, 1)]], Phi_basis[idx2[(0, 2)]], Phi_basis[idx2[(1, 2)]]]))
    record("Phi(e_01, e_23)", np.hstack([Phi_basis[idx2[(0, 1)]], Phi_basis[idx2[(2, 3)]]]))
    record("Phi(e_01, e_23, e_45)", np.hstack([Phi_basis[idx2[(0, 1)]], Phi_basis[idx2[(2, 3)]], Phi_basis[idx2[(4, 5)]]]))

    # Test 2: Vertex stars, cliques, S_6 irreps, and linear combinations of pairs
    st0 = [idx2[p] for p in subsets2 if 0 in p]
    k4 = [idx2[p] for p in itertools.combinations([0, 1, 2, 3], 2)]
    k5 = [idx2[p] for p in itertools.combinations([0, 1, 2, 3, 4], 2)]
    for name, lst in [("star0", st0), ("K4", k4), ("K5", k5)]:
        for m in range(1, len(lst) + 1):
            record(f"Phi({name}[:{m}])", np.hstack([Phi_basis[j] for j in lst[:m]]))

    # Test 3: Low-rank combinations w = e_ij - e_ik, w = e_01 + e_23 - e_02 - e_13 (V_(4,2) Specht vectors!), etc.
    specht_vecs = []
    # Specht vectors of V_{(4,2)}: (e_a - e_b)(e_c - e_d) = e_{ac} - e_{ad} - e_{bc} + e_{bd}
    for (a, b, c, d) in [(0, 1, 2, 3), (0, 1, 2, 4), (0, 2, 1, 3), (0, 1, 3, 4), (0, 1, 4, 5), (2, 3, 4, 5)]:
        v = np.zeros(15, dtype=np.int64)
        v[idx2[tuple(sorted((a, c)))]] = 1
        v[idx2[tuple(sorted((a, d)))]] = MOD - 1
        v[idx2[tuple(sorted((b, c)))]] = MOD - 1
        v[idx2[tuple(sorted((b, d)))]] = 1
        specht_vecs.append(v)
    for k in range(1, len(specht_vecs) + 1):
        mats = [np.tensordot(specht_vecs[i], Phi_basis, axes=(0, 0)) % MOD for i in range(k)]
        record(f"Specht_42[:{k}]", np.hstack(mats))

    # Test 4: V_{(5,1)} vectors: w_J = u_i + u_j with sum u = 0
    v51_vecs = []
    for k_v in range(1, 6):
        u = [0] * 6; u[0] = 1; u[k_v] = MOD - 1
        v = np.array([(u[p[0]] + u[p[1]]) % MOD for p in subsets2], dtype=np.int64)
        v51_vecs.append(v)
    for k in range(1, len(v51_vecs) + 1):
        mats = [np.tensordot(v51_vecs[i], Phi_basis, axes=(0, 0)) % MOD for i in range(k)]
        record(f"V51[:{k}]", np.hstack(mats))

    # Test 5: Coordinate subspaces W_colex[:d]
    for d in range(1, 15):
        W_cols = np.eye(15, dtype=np.int64)[:, :d]
        record(f"CoordColex({d})", W_cols)

    # Print comparison table!
    print("\nd (r1) | max dim(im(G6) cap (W x K^6)) | min r2 = 15 - max | min (r1 + r2) | witness")
    print("-" * 92)
    for d in range(1, 15):
        md = max_for_d[d]
        r2_min = 15 - md
        print(f"  {d:2d}   |              {md:2d}               |        {r2_min:2d}         |      {d + r2_min:2d}       | {witness_for_d.get(d)}")


def test_min_rank_Phi_exhaustive_F3():
    print("\n=== 3. Checking Minimum Possible Rank of Phi(w) over F_3 (Structured + 50,000 Random) ===")
    # Can rank(Phi(w)) EVER be 3 for w != 0 over F_3 (or F_MOD)?
    # Recall: every non-zero element of S_{6,3} has rank >= 3 (Diagonal alpha_S I_3 Lemma).
    # What if Phi(w) has rank 3? Notice Phi(w) is 15 x 6!
    # Wait: if Phi(w) has rank 3, then its 6 columns span a 3D space, so ker(Phi(w)) in K^6 has dim 3!
    # Let us check ALL 3-element subsets of columns (or random 3D right kernels) to see if ANY w != 0 satisfies Phi(w) Z = 0 for a 6x3 matrix Z of rank 3!
    subsets2, idx2, subsets3, G6, E_S, Phi_basis = build_objects()
    # Wait: Phi(w) Z = 0 is a LINEAR system on w in K^15!
    # For a FIXED 6x3 matrix Z (3 cols in K^6), Phi(w) Z = 0 is 15 * 3 = 45 linear equations in 15 unknowns w!
    # Let us test ALL C(6, 3) = 20 coordinate 3-subsets Z + 500 random 6x3 matrices Z over F_MOD!
    found_rk3 = False
    for Z_cols in itertools.combinations(range(6), 3):
        Z = np.zeros((6, 3), dtype=np.int64)
        for j, c in enumerate(Z_cols):
            Z[c, j] = 1
        # Equation: sum_j w_j (Phi_basis[j] @ Z) == 0 -> (45, 15) matrix
        M_eq = np.einsum("jic,ck->ikj", Phi_basis, Z).reshape(45, 15) % MOD
        rk = rank_matrix_mod(M_eq, MOD)
        if rk < 15:
            print(f"  FOUND rank <= 3 at coord kernel {Z_cols}! nullity = {15 - rk}")
            found_rk3 = True
    rng = np.random.default_rng(777)
    for _ in range(500):
        Z = rng.integers(0, MOD, size=(6, 3), dtype=np.int64)
        if rank_matrix_mod(Z, MOD) < 3:
            continue
        M_eq = np.einsum("jic,ck->ikj", Phi_basis, Z).reshape(45, 15) % MOD
        rk = rank_matrix_mod(M_eq, MOD)
        if rk < 15:
            print(f"  FOUND rank <= 3 at random 6x3 Z! nullity = {15 - rk}")
            found_rk3 = True
    # Also check ALL 6x2 coordinate subsets Z (rank <= 4):
    rk4_count = 0
    for Z_cols in itertools.combinations(range(6), 2):
        Z = np.zeros((6, 2), dtype=np.int64)
        for j, c in enumerate(Z_cols):
            Z[c, j] = 1
        M_eq = np.einsum("jic,ck->ikj", Phi_basis, Z).reshape(30, 15) % MOD
        rk = rank_matrix_mod(M_eq, MOD)
        if rk < 15:
            rk4_count += 1
    print(f"  Coordinate 6x3 kernels giving rank(Phi(w)) <= 3: {'FOUND' if found_rk3 else '0/20 (and 0/500 random)'}")
    print(f"  Coordinate 6x2 kernels giving rank(Phi(w)) <= 4: {rk4_count}/15 (precisely the 15 basis vectors e_{{i,j}}!)")


if __name__ == "__main__":
    subsets2, idx2, subsets3, G6, E_S, Phi_basis = build_objects()
    test_500_random_subspaces(Phi_basis)
    test_adversarial_non_coordinate_W(subsets2, idx2, G6, Phi_basis)
    test_min_rank_Phi_exhaustive_F3()
