"""Prof. Wigner Round 11 (ENGEL 5 — Razborov-Smolensky Low-Degree F_2 Approximation
& Boolean S_4 x S_4 Isotypic Gap across ALL 65,536 matrices {0,1}^{4x4}):
Computes for d = 1..6:
1. Exact L_2 projection error W_{>d}(f) = sum_{|S|>d} f_hat(S)^2.
2. Exact d=1 global minimum Hamming error over all 2^{17} affine F_2 functions.
3. Exact exhaustive S_4 x S_4-symmetric minimum Hamming error for d = 1, 2, 3 (over all sym F_2 polys!).
4. Unconstrained (asymmetric) degree-<=d F_2 polynomial minimum Hamming error upper bound
   via multi-start greedy + steepest coordinate descent over all C(16, <=d) monomials (d=2..6),
   PLUS exact Reed-Muller RM(d, 16) dual-coset packing LOWER BOUND!
"""
import itertools
import time
import numpy as np
from round9_wall2_boolean_probe import (
    build_all_4x4_matrices, eval_det4_perm4_exact, build_s4xs4_permutations, fwht_pm
)


def build_monomial_basis_packed(max_deg: int):
    """For each degree <= max_deg, build uint64 bit-packed evaluation vectors of every F_2 monomial
    on all 65,536 inputs (1024 uint64 words per monomial -> bitwise XOR in microseconds!)."""
    idx = np.arange(1 << 16, dtype=np.uint32)
    popcount = np.zeros(1 << 16, dtype=np.int32)
    vars_bool = np.zeros((16, 1 << 16), dtype=np.uint8)
    for b in range(16):
        vb = ((idx >> b) & 1).astype(np.uint8)
        vars_bool[b] = vb
        popcount += vb

    mons_by_deg = [[] for _ in range(max_deg + 1)]
    for m_idx in range(1 << 16):
        d = int(popcount[m_idx])
        if d <= max_deg:
            mons_by_deg[d].append(m_idx)

    # Evaluate each monomial on 65536 inputs and pack into 1024 uint64 words
    def pack(arr01):
        # arr01 shape (65536,) uint8 -> reshape (1024, 64)
        bits = arr01.reshape(1024, 64).astype(np.uint64)
        shifts = np.arange(64, dtype=np.uint64)
        return np.sum(bits << shifts, axis=1)

    packed_mons = {}
    for d in range(max_deg + 1):
        vecs = []
        for m_idx in mons_by_deg[d]:
            v = np.ones(1 << 16, dtype=np.uint8)
            for b in range(16):
                if (m_idx >> b) & 1:
                    v &= vars_bool[b]
            vecs.append(pack(v))
        packed_mons[d] = np.array(vecs, dtype=np.uint64)  # shape (num_d, 1024)
    return mons_by_deg, packed_mons, popcount


POPCOUNT_16 = np.array([bin(i).count("1") for i in range(65536)], dtype=np.int32)


def fast_hamming_weight_packed(arr_u64: np.ndarray) -> int:
    """Exact popcount of 1024 uint64 words using 16-bit lookup table."""
    u16 = arr_u64.view(np.uint16)
    return int(np.sum(POPCOUNT_16[u16]))


def sym_orbit_monomials(max_deg: int, orbit_inv: np.ndarray, n_orbits: int):
    """Find a representative for each S_4 x S_4-invariant sum of F_2 monomials of degree <= max_deg,
    evaluated on the 317 orbits!"""
    # An S_4 x S_4-invariant polynomial is a linear combination of orbit sums of monomials!
    # Notice: monomials m_idx are indexed by 16-bit subsets of the 4x4 grid, so S_4 x S_4 acts on monomials
    # by the EXACT SAME orbit_inv mapping!
    idx = np.arange(1 << 16, dtype=np.uint32)
    vars_bool = np.array([((idx >> b) & 1).astype(np.uint8) for b in range(16)])
    popcount = np.sum(vars_bool, axis=0)

    # Pick one representative input x_rep per orbit
    rep_x = np.zeros(n_orbits, dtype=np.int32)
    for oid in range(n_orbits):
        rep_x[oid] = int(np.where(orbit_inv == oid)[0][0])
    orb_weights = np.bincount(orbit_inv, minlength=n_orbits)

    sym_basis_by_deg = {}
    for d in range(max_deg + 1):
        m_list = np.where(popcount == d)[0]
        orbit_groups = {}
        for m in m_list:
            oid = int(orbit_inv[m])
            orbit_groups.setdefault(oid, []).append(int(m))
        vecs = []
        for oid, ms in sorted(orbit_groups.items()):
            # Evaluate sum_{m in ms} prod_{b in m} x_b mod 2 on the 317 orbit representatives
            val = np.zeros(n_orbits, dtype=np.uint8)
            for m in ms:
                v = np.ones(n_orbits, dtype=np.uint8)
                for b in range(16):
                    if (m >> b) & 1:
                        v &= vars_bool[b, rep_x]
                val ^= v
            vecs.append(val)
        sym_basis_by_deg[d] = vecs
    return sym_basis_by_deg, rep_x, orb_weights


def exact_sym_min_hamming(f_orb: np.ndarray, orb_weights: np.ndarray, sym_vecs: list) -> float:
    """Exhaustively find exact minimum Hamming error across ALL 2^K S_4 x S_4-symmetric F_2 polynomials
    formed by the K basis vectors in sym_vecs (feasible up to K <= 18)."""
    K = len(sym_vecs)
    assert K <= 18, f"Too many sym basis vectors: {K}"
    B = np.array(sym_vecs, dtype=np.uint8)  # (K, 317)
    # Gray-code or vectorized batch evaluation in chunks of 4096
    best = 65536
    total = 1 << K
    for start in range(0, total, 4096):
        end = min(total, start + 4096)
        c_idx = np.arange(start, end, dtype=np.uint32)
        coeffs = ((c_idx[:, None] >> np.arange(K, dtype=np.uint32)) & 1).astype(np.uint8)  # (B, K)
        preds = (coeffs @ B) & 1  # (batch, 317)
        errs = (preds ^ f_orb[None, :]) @ orb_weights  # (batch,)
        m = int(np.min(errs))
        if m < best:
            best = m
    return best / 65536.0


def greedy_unconstrained_hamming(f_packed: np.ndarray, basis_packed: np.ndarray, rng: np.random.Generator, restarts: int = 8) -> float:
    """Multi-start greedy + coordinate-descent over ALL unconstrained F_2 monomials of degree <= d."""
    M, W = basis_packed.shape
    best_w = fast_hamming_weight_packed(f_packed)
    for r in range(restarts):
        if r == 0:
            cur = f_packed.copy()
        else:
            # Random low-weight start from basis
            sel = rng.integers(0, 2, size=M)
            cur = f_packed.copy()
            for idx in np.where(sel == 1)[0]:
                cur ^= basis_packed[idx]
        cur_w = fast_hamming_weight_packed(cur)
        # Coordinate descent passes
        for _ in range(15):
            # Vectorized XOR of all M basis vectors with cur -> shape (M, 1024)
            cands = cur[None, :] ^ basis_packed
            u16 = cands.view(np.uint16)
            weights = np.sum(POPCOUNT_16[u16], axis=1)
            j = int(np.argmin(weights))
            nw = int(weights[j])
            if nw < cur_w:
                cur = cands[j]
                cur_w = nw
            else:
                break
        if cur_w < best_w:
            best_w = cur_w
    return best_w / 65536.0


def rm_dual_coset_lower_bound(f01: np.ndarray, d: int, rng: np.random.Generator, trials: int = 400) -> float:
    """Exact Reed-Muller RM(d, 16) dual-coset packing LOWER bound:
    For any (d+1)-subset S of the 16 coordinates, every deg-<=d poly g sums to 0 mod 2
    on every (d+1)-subcube coset. Thus err(f, g) >= (# odd-parity cosets) / 65536."""
    import math
    k = d + 1
    best_odd = 0
    # If C(16, k) <= 2000, check all coordinate k-subsets! Else sample `trials` + structured!
    all_subs = list(itertools.combinations(range(16), k))
    if len(all_subs) > trials:
        picks = [all_subs[i] for i in rng.choice(len(all_subs), size=trials, replace=False)]
    else:
        picks = all_subs
    for sub in picks:
        other = [b for b in range(16) if b not in sub]
        # Reshape f01 into (2^(16-k), 2^k) by transposing axes!
        f_tensor = f01.reshape((2,) * 16)
        f_perm = np.transpose(f_tensor, other + list(sub)).reshape(1 << (16 - k), 1 << k)
        parities = np.sum(f_perm, axis=1) & 1
        odd_cnt = int(np.sum(parities))
        if odd_cnt > best_odd:
            best_odd = odd_cnt
    return best_odd / 65536.0


def main():
    t0 = time.time()
    print("=" * 96)
    print("PROF. WIGNER ROUND 11 (ENGEL 5): RAZBOROV-SMOLENSKY F_2-APPROXIMATION AUDIT (65,536 INPUTS)")
    print("=" * 96)

    X = build_all_4x4_matrices()
    det4, perm4 = eval_det4_perm4_exact(X)
    _, _, n_orbits, orbit_inv = build_s4xs4_permutations()
    rng = np.random.default_rng(20261121)

    f_det_mod3 = ((det4 % 3) != 0).astype(np.uint8)
    f_perm_mod3 = ((perm4 % 3) != 0).astype(np.uint8)
    f_perm_pos = (perm4 > 0).astype(np.uint8)
    f_rand = rng.integers(0, 2, size=1 << 16, dtype=np.uint8)
    orb_rand = rng.integers(0, 2, size=n_orbits, dtype=np.uint8)
    f_rand_sym = orb_rand[orbit_inv]

    funcs = [
        ("[det_4 != 0 mod 3] (P)", f_det_mod3, True),
        ("[perm_4 != 0 mod 3] (Mod3P)", f_perm_mod3, True),
        ("[perm_4 > 0] (P)", f_perm_pos, True),
        ("Random Boolean (RR Ctrl)", f_rand, False),
        ("Random S4xS4-Sym (SymCtrl)", f_rand_sym, True),
    ]

    max_deg = 6
    mons_by_deg, packed_mons, popcount = build_monomial_basis_packed(max_deg)
    sym_basis_by_deg, rep_x, orb_weights = sym_orbit_monomials(3, orbit_inv, n_orbits)
    sym_counts = {d: len(sym_basis_by_deg[d]) for d in range(4)}
    print(f"S_4 x S_4 symmetric F_2-monomial orbit counts (d=0..3): {sym_counts} (total <= 3: {sum(sym_counts.values())})")

    def pack(arr01):
        bits = arr01.reshape(1024, 64).astype(np.uint64)
        shifts = np.arange(64, dtype=np.uint64)
        return np.sum(bits << shifts, axis=1)

    print("\n--- TABLE A: Exact Real L_2 Tail Error W_{>d}(f) = sum_{|S|>d} f_hat(S)^2 (d=1..6) ---")
    print(f"{'Function':27s} | {'d=1':7s} | {'d=2':7s} | {'d=3':7s} | {'d=4':7s} | {'d=5':7s} | {'d=6':7s}")
    print("-" * 86)
    for name, f01, _ in funcs:
        fhat2 = fwht_pm(f01) ** 2
        errs = [float(np.sum(fhat2[popcount > d])) for d in range(1, 7)]
        print(f"{name:27s} | " + " | ".join(f"{e:7.5f}" for e in errs))

    print("\n--- TABLE B: Exact Symmetric Min Hamming Error (d=1..3) & Unconstrained Min/RM-LB (d=1..6) ---")
    print(f"{'Function':27s} | {'d=1 ex':7s} | {'d=2 sym/unc (LB)':18s} | {'d=3 sym/unc (LB)':18s} | {'d=4 unc (LB)':14s} | {'d=5 unc (LB)':14s} | {'d=6 unc (LB)':14s}")
    print("-" * 124)

    for name, f01, is_sym in funcs:
        f_pk = pack(f01)
        fhat = fwht_pm(f01)
        d1_ex = 0.5 * (1.0 - float(np.max(np.abs(fhat))))
        f_orb = f01[rep_x] if is_sym else None

        sym_res = {}
        for d in (2, 3):
            if is_sym:
                vecs = [v for dd in range(d + 1) for v in sym_basis_by_deg[dd]]
                sym_res[d] = exact_sym_min_hamming(f_orb, orb_weights, vecs)
            else:
                sym_res[d] = float("nan")

        unc_res = {}
        lb_res = {}
        for d in range(2, 7):
            basis_d = np.vstack([packed_mons[dd] for dd in range(d + 1)])
            unc_res[d] = greedy_unconstrained_hamming(f_pk, basis_d, rng, restarts=6)
            lb_res[d] = rm_dual_coset_lower_bound(f01, d, rng, trials=300)

        c2 = f"{sym_res[2]:.4f}/{unc_res[2]:.4f}({lb_res[2]:.4f})" if is_sym else f"  --  /{unc_res[2]:.4f}({lb_res[2]:.4f})"
        c3 = f"{sym_res[3]:.4f}/{unc_res[3]:.4f}({lb_res[3]:.4f})" if is_sym else f"  --  /{unc_res[3]:.4f}({lb_res[3]:.4f})"
        c4 = f"{unc_res[4]:.4f}({lb_res[4]:.4f})"
        c5 = f"{unc_res[5]:.4f}({lb_res[5]:.4f})"
        c6 = f"{unc_res[6]:.4f}({lb_res[6]:.4f})"
        print(f"{name:27s} | {d1_ex:7.5f} | {c2:18s} | {c3:18s} | {c4:14s} | {c5:14s} | {c6:14s}")

    print(f"\n[DONE] Completed in {time.time()-t0:.2f}s.")


if __name__ == "__main__":
    main()
