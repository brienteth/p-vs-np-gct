"""
Prof. Euler - Round 6 Phase 6A Test Harness: test_round6_phase6a.py
Attacking Obligations A and B:
1. Obligation B: Exhaustive scan of rank(Phi(w)) on P^14 over F_2 and orbit search over F_3.
2. Obligation A2: Strassen lower bound min rank(M_6 - sum_{j=1}^c K_j) for c = 1..6.
3. Obligation A1: Gauge-collapse and constant wire support dim_F R(B_1) for Koszul syzygies at t_B in {2, 3, 4}.
"""
import itertools
import numpy as np
import sys
sys.path.append('council/prof-noether')
from general_n2k_noether import build_Mn

def build_phi_basis_f2():
    subsets2 = sorted(itertools.combinations(range(6), 2), key=lambda s: (s[1], s[0]))
    idx2 = {s: i for i, s in enumerate(subsets2)}
    subsets3 = list(itertools.combinations(range(6), 3))
    G6 = np.zeros((20, 15), dtype=np.uint8)
    for s_idx, S in enumerate(subsets3):
        Sc = set(range(6)) - set(S)
        for J in itertools.combinations(sorted(Sc), 2):
            G6[s_idx, idx2[J]] = 1
    E_S = np.zeros((20, 15, 6), dtype=np.uint8)
    for s_idx, S in enumerate(subsets3):
        for c in S:
            I = tuple(sorted(set(S) - {c}))
            E_S[s_idx, idx2[I], c] = 1
    Phi_basis = np.einsum("sj,sic->jic", G6, E_S) % 2
    return subsets2, idx2, Phi_basis

def rank_mod2(mat):
    A = mat.copy() % 2
    m, n = A.shape
    r = 0
    for c in range(n):
        piv = None
        for i in range(r, m):
            if A[i, c] != 0:
                piv = i
                break
        if piv is None:
            continue
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        for i in range(m):
            if i != r and A[i, c] != 0:
                A[i] ^= A[r]
        r += 1
    return r

def test_obligation_b_f2():
    print("=" * 70)
    print("OBLIGATION B: EXHAUSTIVE SCAN OF rank(Phi(w)) ON P^14 OVER F_2")
    print("=" * 70)
    subsets2, idx2, Phi_basis = build_phi_basis_f2()
    # Phi_basis has shape (15, 15, 6)
    # For each w in F_2^15 \ {0}, Phi_w is 15 x 6
    
    # 32767 vectors
    rank_counts = {}
    min_rank = 10
    min_rank_vectors = []
    
    # Vectorized computation in chunks
    chunk_size = 4096
    all_w = np.zeros((32767, 15), dtype=np.uint8)
    for i in range(1, 32768):
        for bit in range(15):
            if (i >> bit) & 1:
                all_w[i - 1, bit] = 1
                
    for i in range(32767):
        w = all_w[i]
        Phi_w = np.tensordot(w, Phi_basis, axes=(0, 0)) % 2 # 15 x 6
        rk = rank_mod2(Phi_w)
        rank_counts[rk] = rank_counts.get(rk, 0) + 1
        if rk < min_rank:
            min_rank = rk
            min_rank_vectors = [w]
        elif rk == min_rank:
            if len(min_rank_vectors) < 30:
                min_rank_vectors.append(w)
                
    print(f"Exhaustive F_2 results (total 32,767 projective points):")
    for rk in sorted(rank_counts.keys()):
        print(f"  rank {rk}: {rank_counts[rk]} points ({rank_counts[rk]/32767*100:.2f}%)")
        
    print(f"\nMinimum rank observed over F_2: {min_rank}")
    print(f"Number of minimum rank points: {rank_counts[min_rank]}")
    
    # Check if the 15 w^*_{a, b} (mod 2) match the min rank vectors:
    w_star_f2 = []
    for a, b in itertools.combinations(range(6), 2):
        ab = {a, b}
        w = np.zeros(15, dtype=np.uint8)
        for j, p in enumerate(subsets2):
            if len(set(p) & ab) == 1:
                w[j] = 1
        w_star_f2.append(w)
        
    match_count = 0
    for w_s in w_star_f2:
        Phi_ws = np.tensordot(w_s, Phi_basis, axes=(0, 0)) % 2
        rk = rank_mod2(Phi_ws)
        if rk == min_rank:
            match_count += 1
    print(f"Number of the 15 w^*_{{a,b}} vectors that achieve minimum rank {min_rank}: {match_count} / 15")

def test_obligation_a2_strassen_floor():
    print("\n" + "=" * 70)
    print("OBLIGATION A2: STRASSEN RANK FLOOR min rank(M_6 - sum_{j=1}^c K_j)")
    print("=" * 70)
    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    # M6 is 90 x 90, rank 20.
    
    rng = np.random.default_rng(2026)
    
    # Test for c = 1, 2, 3, 4, 5, 6
    # For each c, test:
    # (1) Random swapped-Kronecker wires K(B_j, V_j)
    # (2) Adversarial wires K_j in colsp(M_6) (rank-1 projections of M_6)
    
    print("Testing rank(M_6 - sum_{j=1}^c K_j) across 100 trials per c:")
    for c in range(1, 7):
        min_rk_rand = 90
        min_rk_adv = 90
        
        for trial in range(100):
            # Type 1: random K(B, V) where B is 15 x 6, V is 15 x 6
            # In N_01 flattening, K(B, V)[(i, c1), (j, c2)] = B[i, c2] V[j, c1]
            K_sum = np.zeros((90, 90), dtype=float)
            for _ in range(c):
                B = rng.standard_normal((15, 6))
                V = rng.standard_normal((15, 6))
                K_w = np.einsum('ic,jd->idjc', B, V).reshape(90, 90)
                K_sum += K_w
            rk_rand = np.linalg.matrix_rank(M6 - K_sum)
            min_rk_rand = min(min_rk_rand, rk_rand)
            
            # Type 2: Adversarial wires in S_{6,3} (spanned by canonical wires)
            # Pick c random combinations of canonical wires
            K_adv = np.zeros((90, 90), dtype=float)
            for _ in range(c):
                u = V_basis @ rng.standard_normal(20) # 90
                v = V_basis @ rng.standard_normal(20) # 90
                K_adv += np.outer(u, v)
            rk_adv = np.linalg.matrix_rank(M6 - K_adv)
            min_rk_adv = min(min_rk_adv, rk_adv)
            
        print(f"  c = {c}: min rank (random K) = {min_rk_rand}, min rank (adversarial in S_{{6,3}}) = {min_rk_adv} (Floor >= {20 - c})")
        
    print("\nStrassen Bilinear Annihilation / Lemma B_6 Theorem:")
    print("  For any c wires: rank(M_6 - sum_{j=1}^c K_j) >= rank(M_6) - c = 20 - c.")
    print("  At c = 4: rank >= 16.")
    print("  HOWEVER: what if A_1(a) B_2(b) has rank <= 19?")
    print("  Then rank(M_6 - sum_{j=1}^c K_j) <= 19 is TRIVIALLY SATISFIED since 16 <= 19!")
    print("  Therefore, wire counting ALONE (M_6 - sum K_j) CANNOT rule out c = 1..4 wires")
    print("  UNLESS one proves that A_1(a) B_2(b) has rank <= 19 - (15 - c) OR invokes syzygies!")

if __name__ == '__main__':
    test_obligation_b_f2()
    test_obligation_a2_strassen_floor()
