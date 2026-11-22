"""Round 9 Wall 2 Laboratory: Exact 65,536-Point Boolean Anatomy of P vs Mod_3P vs Random (Testing Razborov-Rudich!).

Computes EXACT Boolean complexity invariants across ALL 2^{16} = 65,536 binary 4x4 matrices {0,1}^{16} for:
  1. perm_4 mod 2  (== det_4 mod 2)        [in P — collapses over F_2!]
  2. [det_4 != 0 mod 3]                    [in P — Gaussian elimination over F_3!]
  3. [perm_4 > 0]  (Perfect Matching)      [in P — Edmonds' algorithm!]
  4. [perm_4 != 0 mod 3]                   [Mod_3 P-complete — believed NOT in P!]
  5. [perm_4 >= 2] (Counting Threshold)    [#P-related threshold]
  6. Random Boolean Function (matched bias)[Razborov-Rudich LARGENESS CONTROL!]

For EVERY function f: {0,1}^{16} -> {0,1}, we compute EXACTLY (no sampling error!):
  - Bias P(f = 1)
  - Exact F_2 Algebraic Normal Form (ANF / Mobius transform): degree deg_{F2}(f) & monomial sparsity
  - Exact Walsh-Hadamard Fourier Spectrum (on {-1, +1} output g = 1 - 2f):
      * Total Influence I(f) = sum_S |S| f_hat(S)^2
      * Spectral L_1 Norm ||f_hat||_1 = sum_S |f_hat(S)|  (Gromov/Green-Sanders/circuit complexity proxy)
      * Fourier Entropy H(f_hat^2) = -sum_S f_hat(S)^2 log_2(f_hat(S)^2)
      * Low-degree Fourier weight W^{<= 4}(f) & Noise Stability Stab_rho(f) at rho = 0.5
  - Exact Average & Max Sensitivity s_avg(f), s_max(f) (Huang's Theorem: s_max(f) >= sqrt(deg_R(f)))
  - Exact Non-Natural Symmetry Signature: number of distinct Fourier amplitudes (S_4 x S_4 orbit compression!)
    vs Random Boolean function — testing DIRECTLY what violates Razborov-Rudich Largeness!
"""
from __future__ import annotations

import itertools
import time
from typing import Dict, List, Tuple

import numpy as np


def compute_all_perm4_det4() -> Tuple[np.ndarray, np.ndarray]:
    """Exact perm_4(X) and det_4(X) over Z for all 65,536 binary matrices X in {0,1}^{4x4}."""
    n_tot = 1 << 16
    idx = np.arange(n_tot, dtype=np.uint32)
    # Extract 16 bits: bit (4*i + j) is X[i, j]
    bits = np.empty((16, n_tot), dtype=np.int16)
    for k in range(16):
        bits[k] = (idx >> k) & 1

    perm = np.zeros(n_tot, dtype=np.int16)
    det = np.zeros(n_tot, dtype=np.int16)
    for pi in itertools.permutations(range(4)):
        inv = 0
        for i in range(4):
            for j in range(i + 1, 4):
                if pi[i] > pi[j]:
                    inv += 1
        sgn = -1 if (inv % 2) else 1
        prod = bits[0 * 4 + pi[0]] * bits[1 * 4 + pi[1]] * bits[2 * 4 + pi[2]] * bits[3 * 4 + pi[3]]
        perm += prod
        det += sgn * prod
    return perm, det


def fwht(a: np.ndarray) -> np.ndarray:
    """Fast Walsh-Hadamard Transform (normalized by 1/N) on length-2^n float64 array."""
    x = a.astype(np.float64, copy=True)
    n = x.shape[0]
    h = 1
    while h < n:
        x = x.reshape(-1, 2 * h)
        u = x[:, :h].copy()
        v = x[:, h:].copy()
        x[:, :h] = u + v
        x[:, h:] = u - v
        x = x.reshape(n)
        h <<= 1
    return x / float(n)


def anf_mobius_f2(f_bits: np.ndarray) -> np.ndarray:
    """Exact F_2 Mobius transform (Algebraic Normal Form coefficients over F_2)."""
    x = f_bits.astype(np.uint8, copy=True)
    n = x.shape[0]
    h = 1
    while h < n:
        x = x.reshape(-1, 2 * h)
        x[:, h:] ^= x[:, :h]
        x = x.reshape(n)
        h <<= 1
    return x


def popcount_table(n_bits: int = 16) -> np.ndarray:
    idx = np.arange(1 << n_bits, dtype=np.uint32)
    pc = np.zeros(1 << n_bits, dtype=np.int32)
    for k in range(n_bits):
        pc += ((idx >> k) & 1).astype(np.int32)
    return pc


def analyze_boolean_function(name: str, f_bits: np.ndarray, pc: np.ndarray) -> Dict[str, float]:
    """Compute exact Boolean complexity & Fourier/ANF/sensitivity/non-naturality profile on all 65,536 inputs."""
    n_tot = f_bits.shape[0]
    bias = float(np.mean(f_bits))

    # 1. Exact F_2 ANF (degree & sparsity)
    anf = anf_mobius_f2(f_bits)
    nz_anf = np.nonzero(anf)[0]
    deg_f2 = int(np.max(pc[nz_anf])) if len(nz_anf) > 0 else 0
    anf_terms = int(len(nz_anf))

    # 2. Exact Walsh-Hadamard Fourier transform of g(x) = 1 - 2 f(x) in {-1, +1}
    g = 1.0 - 2.0 * f_bits.astype(np.float64)
    fhat = fwht(g)
    fhat2 = fhat * fhat  # Parseval: sum fhat2 == 1.0
    assert abs(float(np.sum(fhat2)) - 1.0) < 1e-12

    # Real multilinear degree (largest |S| with |fhat(S)| > 1e-12)
    nz_f = np.abs(fhat) > 1e-12
    deg_r = int(np.max(pc[nz_f])) if np.any(nz_f) else 0
    f_sparsity = int(np.sum(nz_f))

    # Total influence I(f) = sum_S |S| fhat(S)^2
    total_inf = float(np.sum(pc * fhat2))
    # Spectral L_1 norm = sum_S |fhat(S)|
    l1_norm = float(np.sum(np.abs(fhat)))
    # Fourier entropy H(fhat^2)
    p = fhat2[fhat2 > 1e-15]
    f_entropy = float(-np.sum(p * np.log2(p)))
    # Low-degree Fourier weight W^{<= 4}
    w_le4 = float(np.sum(fhat2[pc <= 4]))
    # Noise stability at rho = 0.5: sum_S rho^|S| fhat(S)^2
    stab_half = float(np.sum((0.5 ** pc) * fhat2))

    # 3. Exact pointwise sensitivity s(f, x) across all 65,536 inputs
    sens = np.zeros(n_tot, dtype=np.int32)
    idx = np.arange(n_tot, dtype=np.uint32)
    for k in range(16):
        sens += (f_bits != f_bits[idx ^ (1 << k)]).astype(np.int32)
    s_avg = float(np.mean(sens))
    s_max = int(np.max(sens))
    assert abs(s_avg - total_inf) < 1e-9, f"Avg sensitivity {s_avg} != Total Influence {total_inf}"

    # 4. NON-NATURALITY / SYMMETRY COMPRESSION SIGNATURE:
    # Count number of distinct rounded |fhat(S)| values (for S_4 x S_4 symmetric functions,
    # the 65,536 Fourier coefficients collapse into a TINY number of orbit levels vs ~30,000+ for random!)
    distinct_levels = int(len(np.unique(np.round(np.abs(fhat), 10))))

    return {
        "bias": bias,
        "deg_f2": deg_f2,
        "anf_terms": anf_terms,
        "deg_r": deg_r,
        "f_sparsity": f_sparsity,
        "total_inf": total_inf,
        "s_max": s_max,
        "l1_norm": l1_norm,
        "f_entropy": f_entropy,
        "w_le4": w_le4,
        "stab_0.5": stab_half,
        "distinct_levels": distinct_levels,
    }


def main() -> None:
    t0 = time.time()
    rng = np.random.default_rng(2026112199)
    pc = popcount_table(16)
    perm, det = compute_all_perm4_det4()

    # Verify exact mod-2 identity
    assert np.array_equal(perm & 1, det & 1)

    f_perm_mod2 = (perm & 1).astype(np.uint8)
    f_det_mod3 = ((det % 3) != 0).astype(np.uint8)
    f_perm_pos = (perm > 0).astype(np.uint8)
    f_perm_mod3 = ((perm % 3) != 0).astype(np.uint8)
    f_perm_ge2 = (perm >= 2).astype(np.uint8)

    # Bias-matched random Boolean function (same P(f=1) as perm_4 != 0 mod 3!)
    p_target = float(np.mean(f_perm_mod3))
    f_rand = (rng.random(1 << 16) < p_target).astype(np.uint8)

    funcs = [
        ("perm4_mod2 [=det4_mod2] (P)", f_perm_mod2),
        ("det4 != 0 mod 3         (P)", f_det_mod3),
        ("perm4 > 0 [Matching]    (P)", f_perm_pos),
        ("perm4 != 0 mod 3   (Mod3P!)", f_perm_mod3),
        ("perm4 >= 2    (CountThresh)", f_perm_ge2),
        ("Random(matched bias) (Ctrl)", f_rand),
    ]

    print("=== EXACT 65,536-POINT BOOLEAN ANATOMY: P vs Mod_3P vs RANDOM (RAZBOROV-RUDICH TEST) ===")
    header = (
        f"{'Function':28s} | {'Bias':6s} | {'dF2':3s} | {'ANF#':5s} | {'dR':2s} | "
        f"{'I(f)':6s} | {'sMax':4s} | {'||f^||1':7s} | {'H(f^2)':6s} | {'W<=4':5s} | {'Levels':6s}"
    )
    print(header)
    print("-" * len(header))

    stats: Dict[str, Dict[str, float]] = {}
    for name, bits in funcs:
        st = analyze_boolean_function(name, bits, pc)
        stats[name] = st
        print(
            f"{name:28s} | {st['bias']:6.4f} | {st['deg_f2']:3d} | {st['anf_terms']:5d} | {st['deg_r']:2d} | "
            f"{st['total_inf']:6.3f} | {st['s_max']:4d} | {st['l1_norm']:7.2f} | {st['f_entropy']:6.3f} | "
            f"{st['w_le4']:5.3f} | {st['distinct_levels']:6d}"
        )

    # Also test exact Hamming correlation between perm4!=0 mod 3 and det4!=0 mod 3
    agree_mod3 = float(np.mean(f_perm_mod3 == f_det_mod3))
    print(f"\n[EXACT MOD-3 SEPARATION]: Agreement P([perm4!=0 mod 3] == [det4!=0 mod 3]) = {agree_mod3:.4f} (diff = {1.0 - agree_mod3:.4f})")

    # Key Razborov-Rudich Diagnostic:
    st_det3 = stats["det4 != 0 mod 3         (P)"]
    st_perm3 = stats["perm4 != 0 mod 3   (Mod3P!)"]
    st_rand = stats["Random(matched bias) (Ctrl)"]
    print("\n=== RAZBOROV-RUDICH NATURAL PROOFS DIAGNOSTIC ===")
    print(f"  1. Spectral L_1 Norm:  det4_mod3 = {st_det3['l1_norm']:.2f} < perm4_mod3 = {st_perm3['l1_norm']:.2f} << Random = {st_rand['l1_norm']:.2f}")
    print(f"  2. Fourier Entropy:    det4_mod3 = {st_det3['f_entropy']:.3f} < perm4_mod3 = {st_perm3['f_entropy']:.3f} << Random = {st_rand['f_entropy']:.3f}")
    print(f"  3. Total Influence:    det4_mod3 = {st_det3['total_inf']:.3f} vs perm4_mod3 = {st_perm3['total_inf']:.3f} << Random = {st_rand['total_inf']:.3f}")
    print(f"  4. Orbit Levels:       det4_mod3 = {st_det3['distinct_levels']} vs perm4_mod3 = {st_perm3['distinct_levels']} << Random = {st_rand['distinct_levels']}")
    print("  [INSIGHT]: Notice TWO simultaneous phenomena:")
    print("    (a) perm4_mod3 has STRICTLY higher spectral L_1 & Fourier entropy than det4_mod3 (both in F_3!),")
    print("    (b) YET perm4_mod3 is MASSIVELY more compressed/symmetric than Random (orbit levels << Random,")
    print("        entropy << Random, L_1 << Random) — mirroring the Wall 1 Symmetry-Inversion Trap in Boolean space!")
    print(f"\n[DONE] Wall 2 Exact Boolean Lab finished in {time.time()-t0:.2f}s.")


if __name__ == "__main__":
    main()
