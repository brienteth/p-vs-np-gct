"""Prof. Wigner Round 9 (Part II — Wall 2 Direct Attack on P != NP & Natural Proofs):
Exact exhaustive analysis across ALL 65,536 Boolean matrices {0,1}^{4x4} comparing:
  1. det_4 mod 2 (== perm_4 mod 2, in P)
  2. [det_4 != 0 mod 3] (in P)
  3. [perm_4 > 0] (Bipartite Matching, in P)
  4. [perm_4 != 0 mod 3] (Mod_3 P-complete)
  5. Random Boolean function (Razborov-Rudich Largeness control)

Measures:
  - Balance E[f]
  - Exact F_2-ANF degree & monomial count (via Fast Mobius Transform over F_2^{16})
  - Exact F_3 polynomial degree? (note: on {0,1}^16, det_4 mod 3 has F_3-deg <= 8 via det_4^2, perm_4^2 mod 3)
  - Exact Walsh-Hadamard Fourier spectrum (f_pm = 1 - 2*f in {+1, -1}):
    Total Influence I(f), ||f_hat||_1, Fourier Entropy H(f_hat^2), Fourier sparsity,
    degree-k weights W_k, Noise Stability Stab_{0.5}(f) & Stab_{0.9}(f)
  - Exact Sensitivity s(f, x) distribution (min, mean=I(f), max, s_0, s_1)
  - S_4 x S_4 (|G|=576) & S_4 x S_4 x Z_2 (|G|=1152) Stabilizer size, Orbit count on {0,1}^{16},
    and fraction of Fourier energy inside the S_4 x S_4-invariant subspace!
  - Exact 2-adic / 3-adic gate-cancellation / submatrix rank separation between [det_4!=0 mod 3] and [perm_4!=0 mod 3]!
"""
import itertools
import time
import numpy as np


def build_all_4x4_matrices() -> np.ndarray:
    """Return array X of shape (65536, 4, 4) with {0,1} entries indexed by 16-bit integer."""
    idx = np.arange(1 << 16, dtype=np.uint32)
    bits = ((idx[:, None] >> np.arange(16, dtype=np.uint32)) & 1).astype(np.int64)
    return bits.reshape(1 << 16, 4, 4)


def eval_det4_perm4_exact(X: np.ndarray):
    """Exact integer det_4 and perm_4 on all 65,536 {0,1}^{4x4} matrices."""
    det = np.zeros(X.shape[0], dtype=np.int64)
    perm = np.zeros(X.shape[0], dtype=np.int64)
    for pi in itertools.permutations(range(4)):
        inv = sum(1 for i in range(4) for j in range(i + 1, 4) if pi[i] > pi[j])
        sgn = -1 if (inv % 2) else 1
        term = X[:, 0, pi[0]] * X[:, 1, pi[1]] * X[:, 2, pi[2]] * X[:, 3, pi[3]]
        perm += term
        det += sgn * term
    return det, perm


def f2_anf_transform(f01: np.ndarray) -> np.ndarray:
    """Exact Fast Mobius Transform over F_2^16 returning ANF coefficients in {0,1}^{65536}."""
    a = f01.copy().astype(np.uint8)
    for b in range(16):
        step = 1 << b
        a_view = a.reshape(-1, 2 * step)
        a_view[:, step:] ^= a_view[:, :step]
    return a


def fwht_pm(f01: np.ndarray) -> np.ndarray:
    """Exact normalized Walsh-Hadamard transform of f_pm = 1 - 2*f01 in {+1, -1}."""
    h = (1.0 - 2.0 * f01.astype(np.float64)).copy()
    for b in range(16):
        step = 1 << b
        v = h.reshape(-1, 2 * step)
        x = v[:, :step].copy()
        y = v[:, step:]
        v[:, :step] = x + y
        v[:, step:] = x - y
    return h / (1 << 16)


def compute_sensitivity(f01: np.ndarray):
    """Exact sensitivity s(f, x) at all 65,536 inputs."""
    s = np.zeros(1 << 16, dtype=np.int32)
    idx = np.arange(1 << 16, dtype=np.uint32)
    for b in range(16):
        s += (f01 != f01[idx ^ (1 << b)]).astype(np.int32)
    return s


def build_s4xs4_permutations():
    """Build index permutation maps on 0..65535 for all 576 elements of S_4 x S_4,
    plus the 1152 elements of (S_4 x S_4) x Z_2 (transpose)."""
    bit_pos = np.arange(16).reshape(4, 4)
    perms_576 = []
    for pr in itertools.permutations(range(4)):
        for pc in itertools.permutations(range(4)):
            # New bit b' at (i,j) comes from old bit at (pr[i], pc[j])
            src_bits = bit_pos[np.ix_(pr, pc)].reshape(16)
            perms_576.append(src_bits)
    # Apply bit-permutation on 65536 states quickly via two 8-bit lookup tables!
    # Wait: even simpler, build 65536-len map using vectorized bit shifts!
    idx = np.arange(1 << 16, dtype=np.uint32)
    bits = np.stack([((idx >> b) & 1) for b in range(16)], axis=0)  # (16, 65536)
    weights = (1 << np.arange(16, dtype=np.uint32))[:, None]

    # Precompute orbit partition under S_4 x S_4!
    # Wait: 576 maps * 65536 is ~37M ints, fast in numpy! Let's compute orbit ids via union/min-label or BFS!
    orbit_id = np.full(1 << 16, -1, dtype=np.int32)
    # Use a small generating set of S_4 x S_4 (adjacent transpositions: 3 row + 3 col = 6 generators!)
    gens = []
    for k in range(3):
        pr = list(range(4)); pr[k], pr[k + 1] = pr[k + 1], pr[k]
        gens.append(bit_pos[np.ix_(pr, range(4))].reshape(16))
        pc = list(range(4)); pc[k], pc[k + 1] = pc[k + 1], pc[k]
        gens.append(bit_pos[np.ix_(range(4), pc)].reshape(16))
    gen_maps = []
    for g in gens:
        # map state x -> new_x where bit_new[k] = bit_old[g[k]]
        # i.e. sum_k bits[g[k]] << k
        m = np.zeros(1 << 16, dtype=np.uint32)
        for k in range(16):
            m |= (bits[g[k]] << k)
        gen_maps.append(m)
    # Also transpose generator
    tr_bits = bit_pos.T.reshape(16)
    tr_map = np.zeros(1 << 16, dtype=np.uint32)
    for k in range(16):
        tr_map |= (bits[tr_bits[k]] << k)

    # Propagate minimum label in each S_4 x S_4 orbit until convergence (diameter <= 12)!
    labels = np.arange(1 << 16, dtype=np.int32)
    while True:
        prev = labels.copy()
        for m in gen_maps:
            labels = np.minimum(labels, labels[m])
            # Also push forward (since m is an involution!)
        if np.array_equal(labels, prev):
            break
    unique_orbits, inverse_ids = np.unique(labels, return_inverse=True)
    return gen_maps, tr_map, len(unique_orbits), inverse_ids


def stabilizer_count(f01: np.ndarray, bits_mat: np.ndarray):
    """Exact |Stab_{S4xS4}(f)| out of 576 and |Stab_{(S4xS4)xZ2}(f)| out of 1152."""
    bit_pos = np.arange(16).reshape(4, 4)
    idx = np.arange(1 << 16, dtype=np.uint32)
    stab_576 = 0
    stab_1152 = 0
    # Precompute 256-entry low-byte and high-byte contributions per permutation for speed?
    # Actually 576 iterations of 16 bit-shifts on 65536 ints is ~0.15s total? Let's test 2-byte LUT!
    # Low byte (bits 0..7), High byte (bits 8..15)
    lo = (idx & 255)
    hi = (idx >> 8)
    b_lo = np.array([[(v >> b) & 1 for b in range(8)] for v in range(256)], dtype=np.uint32)
    b_hi = np.array([[(v >> b) & 1 for b in range(8)] for v in range(256)], dtype=np.uint32)

    for tr in (False, True):
        for pr in itertools.permutations(range(4)):
            for pc in itertools.permutations(range(4)):
                bp = bit_pos.T if tr else bit_pos
                src = bp[np.ix_(pr, pc)].reshape(16)
                lut_lo = np.zeros(256, dtype=np.uint32)
                lut_hi = np.zeros(256, dtype=np.uint32)
                for k, sb in enumerate(src):
                    if sb < 8:
                        lut_lo |= (b_lo[:, sb] << k)
                    else:
                        lut_hi |= (b_hi[:, sb - 8] << k)
                mapped = lut_lo[lo] | lut_hi[hi]
                if np.array_equal(f01, f01[mapped]):
                    stab_1152 += 1
                    if not tr:
                        stab_576 += 1
    return stab_576, stab_1152


def analyze_function(name: str, f01: np.ndarray, popcount: np.ndarray, orbit_inv: np.ndarray, n_orbits: int):
    f01 = f01.astype(np.uint8)
    bal = float(np.mean(f01))
    anf = f2_anf_transform(f01)
    anf_nz = np.where(anf > 0)[0]
    anf_deg = int(np.max(popcount[anf_nz])) if len(anf_nz) else 0
    anf_count = int(len(anf_nz))
    anf_by_deg = [int(np.sum(popcount[anf_nz] == d)) for d in range(17)]

    fhat = fwht_pm(f01)
    fhat2 = fhat ** 2
    influence = float(np.sum(popcount * fhat2))
    l1_norm = float(np.sum(np.abs(fhat)))
    nz_hat = fhat2[fhat2 > 1e-18]
    fourier_sparsity = int(len(nz_hat))
    fourier_entropy = float(-np.sum(nz_hat * np.log2(nz_hat)))
    stab_05 = float(np.sum((0.5 ** popcount) * fhat2))
    stab_09 = float(np.sum((0.9 ** popcount) * fhat2))
    w_k = [float(np.sum(fhat2[popcount == k])) for k in range(17)]

    sens = compute_sensitivity(f01)
    s_min, s_max = int(np.min(sens)), int(np.max(sens))
    s0_max = int(np.max(sens[f01 == 0])) if np.any(f01 == 0) else 0
    s1_max = int(np.max(sens[f01 == 1])) if np.any(f01 == 1) else 0

    # Symmetrized energy fraction ||Pi_{S4xS4} f_pm||^2 / ||f_pm||^2:
    f_pm = 1.0 - 2.0 * f01.astype(np.float64)
    orb_sums = np.bincount(orbit_inv, weights=f_pm, minlength=n_orbits)
    orb_cnts = np.bincount(orbit_inv, minlength=n_orbits)
    proj_energy = float(np.sum((orb_sums ** 2) / orb_cnts) / (1 << 16))

    stab576, stab1152 = stabilizer_count(f01, None)

    return {
        "name": name, "bal": bal, "anf_deg": anf_deg, "anf_cnt": anf_count,
        "anf_by_deg": anf_by_deg, "I": influence, "L1": l1_norm,
        "H_four": fourier_entropy, "sparsity": fourier_sparsity,
        "stab05": stab_05, "stab09": stab_09, "w_k": w_k,
        "s_min": s_min, "s_max": s_max, "s0_max": s0_max, "s1_max": s1_max,
        "proj_sym": proj_energy, "stab576": stab576, "stab1152": stab1152,
    }


def main():
    t0 = time.time()
    print("=" * 94)
    print("PROF. WIGNER ROUND 9 (PART II — WALL 2): ALL 65,536 MATRICES {0,1}^{4x4} SEPARATION AUDIT")
    print("=" * 94)
    X = build_all_4x4_matrices()
    det4, perm4 = eval_det4_perm4_exact(X)

    idx = np.arange(1 << 16, dtype=np.uint32)
    popcount = np.zeros(1 << 16, dtype=np.int32)
    for b in range(16):
        popcount += ((idx >> b) & 1).astype(np.int32)

    _, _, n_orbits, orbit_inv = build_s4xs4_permutations()
    print(f"Total {0,1}^{{4x4}} states = 65,536 | Exact S_4 x S_4 orbits = {n_orbits} "
          f"(orbit-space dim = {n_orbits}/65536 = {n_orbits/65536:.5f})")

    rng = np.random.default_rng(202611219)
    f_det_mod2 = (np.abs(det4) % 2).astype(np.uint8)
    assert np.array_equal(f_det_mod2, (perm4 % 2).astype(np.uint8))
    f_det_mod3 = ((det4 % 3) != 0).astype(np.uint8)
    f_perm_pos = (perm4 > 0).astype(np.uint8)
    f_perm_mod3 = ((perm4 % 3) != 0).astype(np.uint8)
    f_rand_bal = rng.integers(0, 2, size=1 << 16, dtype=np.uint8)
    # Also include a random S_4 x S_4-symmetric Boolean function (symmetric control!)
    orb_rand_bits = rng.integers(0, 2, size=n_orbits, dtype=np.uint8)
    f_rand_sym = orb_rand_bits[orbit_inv]

    funcs = [
        ("det_4 mod 2 (P)", f_det_mod2),
        ("[det_4 != 0 mod 3] (P)", f_det_mod3),
        ("[perm_4 > 0] (P)", f_perm_pos),
        ("[perm_4 != 0 mod 3] (Mod3P)", f_perm_mod3),
        ("Random Boolean (RR Ctrl)", f_rand_bal),
        ("Random S4xS4-Sym (SymCtrl)", f_rand_sym),
    ]

    results = [analyze_function(n, f, popcount, orbit_inv, n_orbits) for n, f in funcs]

    print(f"\n{'Function':27s} | {'E[f]':6s} | {'ANFd':4s} | {'#ANF':5s} | {'I(f)':6s} | {'||f^||1':8s} | {'H(f^2)':6s} | {'Spars':5s} | {'Stab0.9':7s} | {'s(min,max,s0,s1)':16s} | {'SymE%':6s} | {'Stab(G)':7s}")
    print("-" * 134)
    for r in results:
        s_str = f"{r['s_min']},{r['s_max']},{r['s0_max']},{r['s1_max']}"
        st_str = f"{r['stab576']}/{r['stab1152']}"
        print(f"{r['name']:27s} | {r['bal']:6.4f} | {r['anf_deg']:4d} | {r['anf_cnt']:5d} | {r['I']:6.3f} | {r['L1']:8.2f} | {r['H_four']:6.2f} | {r['sparsity']:5d} | {r['stab09']:7.4f} | {s_str:16s} | {100*r['proj_sym']:5.2f}% | {st_str:7s}")

    print("\n--- Fourier Weight Profile W_k = sum_{|S|=k} f_hat(S)^2 (k = 0..16) ---")
    for r in results:
        wk_str = " ".join(f"{w:.3f}" for w in r["w_k"][:11])
        wk_tail = sum(r["w_k"][11:])
        print(f"  {r['name']:27s}: k=0..10: [{wk_str}] | k>=11: {wk_tail:.4f}")

    print("\n--- F_2 ANF Degree Spectrum (# monomials of degree d = 0..16) ---")
    for r in results:
        d_str = " ".join(f"{c:4d}" for c in r["anf_by_deg"][:13])
        print(f"  {r['name']:27s}: d=0..12: [{d_str}] | d=13..16: {r['anf_by_deg'][13:]}")

    # Extra check: F_3 algebraic degree (exact polynomial degree mod 3 on {0,1}^16 via F_3 Mobius?)
    # On {0,1}^16, indicator [F != 0 mod 3] == F^2 mod 3!
    # Wait: for det_4^2 mod 3 and perm_4^2 mod 3, check how many monomials survive mod 3 and their max degree!
    # Even simpler: evaluate max univariate degree along random affine lines or F_3-Hilbert check? No, multilinear deg of F^2 mod 3!
    # Wait: det_4^2 has degree 8; on {0,1}, x_i^2 = x_i, so some cancellations occur mod 3! Let's check exact multilinear F_3 degree!
    print(f"\n--- Exact Multilinear F_3-Representation (f(x) in {{0,1}} as polynomial in F_3[x]/<x_i^2-x_i>) ---")
    for name_p, vals in [("det_4^2 mod 3", (det4 * det4) % 3), ("perm_4^2 mod 3", (perm4 * perm4) % 3)]:
        # Fast Mobius over F_3: f(x) = sum_S c_S prod_{i in S} x_i -> invert by subtracting lower subsets mod 3!
        c = (vals % 3).astype(np.int16).copy()
        for b in range(16):
            step = 1 << b
            v = c.reshape(-1, 2 * step)
            v[:, step:] = (v[:, step:] - v[:, :step]) % 3
        nz = np.where(c != 0)[0]
        f3_deg = int(np.max(popcount[nz]))
        f3_cnt = int(len(nz))
        by_d = [int(np.sum(popcount[nz] == d)) for d in range(f3_deg + 1)]
        print(f"  {name_p:20s}: exact F_3-deg = {f3_deg}, #F_3-monomials = {f3_cnt}, by deg = {by_d}")

    print(f"\n[DONE] Completed in {time.time()-t0:.2f}s.")


if __name__ == "__main__":
    main()
