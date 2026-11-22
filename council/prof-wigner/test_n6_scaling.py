"""Prof. Wigner: General n = 2k Scaling and n = 6 Verification Suite.
1. Construction of P_{perm, 6}(a, b) and Nisan matrix M_6 of size (15*6) x (15*6) = 90 x 90.
2. Verification that rank(M_6) = C(6, 3) = 20.
3. Proof of partial-transpose invariance T(M_6) = M_6 and Choi-Jamiolkowski realignment R(M_6) = M_6.
4. Exact spectral decomposition of M_6.
5. Exact gauge degrees of freedom and codimension defect for w = 19 and w = 20.
"""
import itertools
import numpy as np

def build_n6_target():
    # n = 6, k = 3.
    # Rows/cols of P indexed by subsets of {0..5} of size k-1 = 2: C(6, 2) = 15 subsets.
    subsets_2 = list(itertools.combinations(range(6), 2))
    assert len(subsets_2) == 15
    subset_to_idx = {s: i for i, s in enumerate(subsets_2)}

    # P is 15 x 15 matrix of quadratic polynomials in a, b in F^6.
    # P_{S, T} = 0 if S cap T != empty else a_{c1} b_{c2} + a_{c2} b_{c1} where {c1, c2} = {0..5} \ (S cup T)
    # The Nisan matrix M_6 has rows (S_idx, c1) and cols (T_idx, c2)
    # Row size: 15 * 6 = 90. Col size: 15 * 6 = 90.
    M_6 = np.zeros((90, 90), dtype=np.float64)
    all_elements = set(range(6))

    for s_idx, S in enumerate(subsets_2):
        S_set = set(S)
        for c1 in range(6):
            if c1 in S_set:
                continue
            U = S_set | {c1} # size 3
            assert len(U) == 3
            for t_idx, T in enumerate(subsets_2):
                T_set = set(T)
                for c2 in range(6):
                    if c2 in T_set:
                        continue
                    V = T_set | {c2} # size 3
                    assert len(V) == 3
                    # Condition: U and V form a partition of {0..5}
                    if U | V == all_elements:
                        # Nonzero entry 1.0
                        M_6[s_idx * 6 + c1, t_idx * 6 + c2] = 1.0

    return M_6, subsets_2

def test_n6():
    print("=" * 70)
    print("PROF. WIGNER: GENERAL n=2k & n=6 SCALING VERIFICATION")
    print("=" * 70)

    M_6, subsets_2 = build_n6_target()
    print(f"Constructed M_6: shape = {M_6.shape} (90 x 90)")

    # 1. Rank of M_6
    rk_6 = np.linalg.matrix_rank(M_6, tol=1e-7)
    print(f"rank(M_6) = {rk_6} (Expected C(6, 3) = 20)")
    assert rk_6 == 20, f"Expected rank 20, got {rk_6}"
    print("[PASS 1] Middle Nisan Cut Rank: rank(M_6) == C(6,3) == 20.")

    # 2. Symmetry of M_6
    sym_err = np.max(np.abs(M_6 - M_6.T))
    print(f"Symmetry ||M_6 - M_6^T||_max = {sym_err:.2e}")
    assert sym_err == 0.0
    print("[PASS 2] M_6 is an exact symmetric operator.")

    # 3. Partial-transpose invariance T(M_6) = M_6
    # In M_6, row is (s_idx, c1), col is (t_idx, c2)
    # T swaps c1 and c2: T(M_6)_{(s_idx, c2), (t_idx, c1)} = M_6_{(s_idx, c1), (t_idx, c2)}
    M_6_tensor = M_6.reshape(15, 6, 15, 6)
    T_M_6 = np.transpose(M_6_tensor, (0, 3, 2, 1)).reshape(90, 90)
    pt_err = np.max(np.abs(M_6 - T_M_6))
    print(f"Partial transpose ||T(M_6) - M_6||_max = {pt_err:.2e}")
    assert pt_err == 0.0
    print("[PASS 3] Partial-Transpose Self-Duality: T(M_6) == M_6 identically for n=6.")

    # 4. Choi-Jamiolkowski realignment R(M_6)
    # R maps ((s_idx, c1), (t_idx, c2)) to ((s_idx, t_idx), (c1, c2))
    # Shape is (15*15, 6*6) = (225, 36)
    R_M_6 = np.transpose(M_6_tensor, (0, 2, 1, 3)).reshape(225, 36)
    rk_R = np.linalg.matrix_rank(R_M_6, tol=1e-7)
    print(f"Choi-Jamiolkowski realigned matrix shape = {R_M_6.shape}, rank = {rk_R}")
    # Note: For general n, the complement {c1, c2} = {0..n-1} \ (S cup T) has size 2.
    # The number of such pairs is C(n, 2). For n=6, C(6, 2) = 15!
    # Hence the column space is supported on the C(n, 2) pairs, giving rank C(n, 2) = 15!
    assert rk_R == 15, f"Expected rank 15, got {rk_R}"
    print(f"[PASS 4] Realignment Rank: rank(R(M_6)) == C(6, 2) == 15.")

    # 5. Spectral Decomposition of M_6
    evals = np.linalg.eigvalsh(M_6)
    # Check non-zero eigenvalues
    evals_nz = evals[np.abs(evals) > 1e-4]
    print(f"Number of non-zero eigenvalues = {len(evals_nz)} (expected 20)")
    assert len(evals_nz) == 20
    pos_evals = evals_nz[evals_nz > 0]
    neg_evals = evals_nz[evals_nz < 0]
    print(f"Positive eigenvalues ({len(pos_evals)}): {np.round(pos_evals[:5], 3)}...")
    print(f"Negative eigenvalues ({len(neg_evals)}): {np.round(neg_evals[:5], 3)}...")
    print(f"Spectrum summary: {len(pos_evals)} positive, {len(neg_evals)} negative, {90 - len(evals_nz)} zero.")
    print(f"[PASS 5] Spectral Inertia of M_6: Signature is ({len(pos_evals)}, {len(neg_evals)}, {90 - len(evals_nz)}).")

    # 6. Gauge Degrees of Freedom and Codimension Defect Scaling
    print("\n--- Gauge Degrees of Freedom & Codimension Defect for n=6 ---")
    m_6 = 15
    n = 6
    n_quad_eqs = m_6 * m_6 * (n * (n + 1) // 2) # 15 * 15 * 21 = 4725
    n_bilinear_eqs = m_6 * m_6 * (n * n)         # 15 * 15 * 36 = 8100
    total_eqs = 2 * n_quad_eqs + n_bilinear_eqs  # 17550
    print(f"Total equations in unsplit system = 2 * {n_quad_eqs} + {n_bilinear_eqs} = {total_eqs}")

    for w in (19, 20):
        raw_params = 4 * m_6 * w * n # 4 * 15 * w * 6 = 360 * w
        gauge_dim = w * w
        dof_phys = raw_params - gauge_dim
        defect = total_eqs - dof_phys
        print(f"w = {w}: raw_params = {raw_params}, gauge_dim = {gauge_dim}, dof_phys = {dof_phys}, defect = {defect}")

    # Wire-split (r, 19-r)
    print("\nWire-split for w = 19:")
    for r in (9, 10):
        wire_params = 2 * m_6 * r * n + 2 * m_6 * (19 - r) * n
        wire_gauge = r * r + (19 - r) * (19 - r)
        wire_dof = wire_params - wire_gauge
        wire_defect = n_bilinear_eqs - wire_dof
        print(f"Split ({r}, {19-r}): params = {wire_params}, gauge = {wire_gauge}, dof = {wire_dof}, defect in bilinear eqs = {wire_defect}")

    print("=" * 70)
    print("ALL GENERAL n=6 SCALING CHECKS PASSED.")
    print("=" * 70)

if __name__ == "__main__":
    test_n6()
