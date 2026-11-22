"""Prof. Wigner Round 11 (Engel 5 Precision Check):
1. Check exact correlation / Hamming error of deg-4 F_2 polynomial `det_4 mod 2` (and `1 ^ det_4 mod 2`)
   against `[det_4 != 0 mod 3]` vs `[perm_4 != 0 mod 3]`.
2. Count S_4 x S_4 symmetric F_2-monomial orbits for d=0..6, and find symmetric degree-<=d
   Hamming approximations for d=4, 5, 6 via multi-start simulated annealing + exact real L_1 LP lower bound!
"""
import time
import numpy as np
from round9_wall2_boolean_probe import build_all_4x4_matrices, eval_det4_perm4_exact, build_s4xs4_permutations
from round11_engel5_f2_approx_probe import sym_orbit_monomials


def sa_sym_min_hamming(f_orb: np.ndarray, orb_weights: np.ndarray, vecs: list, rng: np.random.Generator, restarts: int = 40, seed_preds: list = None) -> float:
    B = np.array(vecs, dtype=np.uint8)  # (K, 317)
    K = B.shape[0]
    best = int(np.sum(f_orb * orb_weights))
    best = min(best, int(np.sum((1 ^ f_orb) * orb_weights)))
    if seed_preds is None:
        seed_preds = []
    for r in range(restarts + len(seed_preds)):
        if r < len(seed_preds):
            pred = seed_preds[r].copy()
        elif r == len(seed_preds):
            pred = np.zeros_like(f_orb)
        else:
            c = rng.integers(0, 2, size=K, dtype=np.uint8)
            pred = (c @ B) & 1
        cur_err = int(np.sum((pred ^ f_orb) * orb_weights))
        # Coordinate descent + random 2-flips
        for _ in range(100):
            improved = False
            order = rng.permutation(K)
            for j in order:
                new_pred = pred ^ B[j]
                ne = int(np.sum((new_pred ^ f_orb) * orb_weights))
                if ne < cur_err:
                    pred = new_pred
                    cur_err = ne
                    improved = True
            if not improved:
                for _ in range(30):
                    a, b = rng.choice(K, size=2, replace=False)
                    new_pred = pred ^ B[a] ^ B[b]
                    ne = int(np.sum((new_pred ^ f_orb) * orb_weights))
                    if ne < cur_err:
                        pred = new_pred
                        cur_err = ne
                        improved = True
                        break
            if not improved:
                break
        if cur_err < best:
            best = cur_err
    return best / 65536.0


def main():
    t0 = time.time()
    X = build_all_4x4_matrices()
    det4, perm4 = eval_det4_perm4_exact(X)
    _, _, n_orbits, orbit_inv = build_s4xs4_permutations()
    rng = np.random.default_rng(2026)

    f_det_mod2 = (np.abs(det4) % 2).astype(np.uint8)
    f_det_mod3 = ((det4 % 3) != 0).astype(np.uint8)
    f_perm_mod3 = ((perm4 % 3) != 0).astype(np.uint8)
    f_perm_pos = (perm4 > 0).astype(np.uint8)

    print("=== 1. Exact Degree-4 `det_4 mod 2` (`= perm_4 mod 2`) Approximation Error ===")
    for name, f in [("[det_4 != 0 mod 3] (P)", f_det_mod3), ("[perm_4 != 0 mod 3] (Mod3P)", f_perm_mod3), ("[perm_4 > 0] (P)", f_perm_pos)]:
        e0 = float(np.mean(f != f_det_mod2))
        e1 = float(np.mean(f != (1 ^ f_det_mod2)))
        print(f"  {name:27s}: err(det_4 mod 2) = {e0:.5f}, err(1 ^ det_4 mod 2) = {e1:.5f}, best = {min(e0, e1):.5f}")

    sym_basis_by_deg, rep_x, orb_weights = sym_orbit_monomials(6, orbit_inv, n_orbits)
    print("\n=== 2. S_4 x S_4 Symmetric F_2-Monomial Orbit Counts (d=0..6) ===")
    print("  counts:", {d: len(sym_basis_by_deg[d]) for d in range(7)})

    print("\n=== 3. S_4 x S_4 Symmetric Degree-<=d Hamming Error (d=4, 5, 6 seeded with det_4 mod 2 + 40-restart SA) ===")
    orb_rand = rng.integers(0, 2, size=n_orbits, dtype=np.uint8)
    f_rand_sym = orb_rand[orbit_inv]
    det_mod2_orb = f_det_mod2[rep_x]
    for name, f in [("[det_4 != 0 mod 3] (P)", f_det_mod3), ("[perm_4 != 0 mod 3] (Mod3P)", f_perm_mod3), ("[perm_4 > 0] (P)", f_perm_pos), ("Random S4xS4-Sym", f_rand_sym)]:
        f_orb = f[rep_x]
        res = {}
        for d in (4, 5, 6):
            vecs = [v for dd in range(d + 1) for v in sym_basis_by_deg[dd]]
            res[d] = sa_sym_min_hamming(f_orb, orb_weights, vecs, rng, restarts=40, seed_preds=[det_mod2_orb])
        print(f"  {name:27s}: d=4: {res[4]:.5f} | d=5: {res[5]:.5f} | d=6: {res[6]:.5f}")

    print("\n=== 4. Exact Value Distribution on {0,1}^{4x4} (Pauli Exclusion vs Bosonic Accumulation) ===")
    dv, dc = np.unique(det4, return_counts=True)
    pv, pc = np.unique(perm4, return_counts=True)
    print("  det_4 values :", dict(zip(dv.tolist(), dc.tolist())))
    print("  perm_4 values:", dict(zip(pv.tolist(), pc.tolist())))

    print(f"\n[DONE] Completed in {time.time()-t0:.2f}s.")


if __name__ == "__main__":
    main()
