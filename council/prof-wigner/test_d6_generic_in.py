"""Prof. Wigner Round 6: Test d_syz >= 6 LM hunt when B2_in is:
  (A) a 15-wire coordinate subset WITHOUT any full 4-tuple {i,u,v},
  (B) a random 15D subspace of S_{6,3} (testing if c >= 5 or Noether (3,4) occurs!).
"""
import itertools
import numpy as np
import sys
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council/prof-noether")
from general_n2k_noether import build_Mn
from test_d6_syzygy_hunt import build_B2_full_and_perp, run_lm_d6

def main():
    print("=" * 74)
    print("D6 SYZYGY HUNT ON NON-EDGE-STAR AND GENERIC 15D B2_in SUBSPACES (t_B=4)")
    print("=" * 74)
    B2_full, Q_perp_tensor, sub_2, sub_3 = build_B2_full_and_perp()
    sub3_idx = {s: i for i, s in enumerate(sub_3)}
    rng = np.random.default_rng(999)
    b0 = rng.standard_normal(6)
    b_chk = rng.standard_normal(6)

    # Find a 5-wire drop leaving NO pair {u, v} with all 4 triples {i, u, v}:
    # Drop 5 disjoint/covering triples so every edge {u, v} loses >= 1 triple!
    # A Steiner-like 5-drop: (0,1,2), (0,3,4), (1,3,5), (2,4,5), (0,1,5) -> wait let's check max triples per edge:
    drops_no4 = [sub3_idx[s] for s in [(0,1,2), (0,3,4), (1,3,5), (2,4,5), (0,4,5)]]
    # Check max triples remaining per 2-edge:
    keep_no4 = [i for i in range(20) if i not in drops_no4]
    max_per_edge = max(sum(1 for i in keep_no4 if set(e).issubset(sub_3[i])) for e in sub_2)
    print(f"Non-edge-star 15-wire B2_in: max triples sharing any edge = {max_per_edge}")
    B2_in_no4 = B2_full[:, keep_no4, :]

    # Random 15D subspace of S_{6,3}:
    W_rand, _ = np.linalg.qr(rng.standard_normal((20, 15))) # 20 x 15 orthonormal
    B2_in_gen = np.einsum("kl,ckJ->clJ", W_rand, B2_full) # (6, 15, 15)

    for label, B2_in in [("Coord 15-set (max 3/edge)", B2_in_no4), ("Generic 15D subspace of S_{6,3}", B2_in_gen)]:
        n_b1 = 6 * 6 * 19
        n_cout = 4 * 70
        n_m = 15 * 19
        solved_info = []
        best_nr = 1e9
        for s in range(5):
            p0 = rng.standard_normal(n_b1 + n_cout + n_m) * 0.25
            nr, p = run_lm_d6(B2_in, Q_perp_tensor, 4, b0, p0, max_iter=60)
            if nr < best_nr:
                best_nr = nr
            if nr < 1e-8:
                B1 = p[:n_b1].reshape(6, 6, 19)
                s1 = np.linalg.matrix_rank(np.tensordot(b_chk, B1, axes=([0],[0])), tol=1e-6)
                c_w = np.linalg.matrix_rank(B1.reshape(36, 19), tol=1e-6)
                solved_info.append((int(s1), int(c_w)))
        print(f"  [{label}] min ||r||={best_nr:.3e} | solved={len(solved_info)}/5 | (s1, c)={solved_info}")

if __name__ == "__main__":
    main()
