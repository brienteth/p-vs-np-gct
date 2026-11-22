# Synthesis of Wall 1 ($m \in \{13, 14, 15\}$) & Wall 2 (Boolean–Algebraic Bridge)

Synthesizes experimental and proof findings from [perm4_middle_factorization_probe.py](file:///Users/bl10buer/Desktop/matemk/p-vs-np-gct/perm4_middle_factorization_probe.py) and [boolean_algebraic_bridge.py](file:///Users/bl10buer/Desktop/matemk/p-vs-np-gct/boolean_algebraic_bridge.py).

---

## 1. Wall 1: Closing $m = 13$ (`4,4,4`) for Row-Separated Homogeneous ABPs

From [THEOREM_MONOTONE_ABP.md](file:///Users/bl10buer/Desktop/matemk/p-vs-np-gct/THEOREM_MONOTONE_ABP.md), every homogeneous layered ABP computing $\mathrm{perm}_4$ (even as a border limit) must have $w_1, w_2, w_3 \ge 4$, leaving $m \in \{13, 14, 15\}$.

At the minimal candidate $m = 13$ (`(4, 4, 4)`), if the outer $4$-dimensional linear layers isolate two rows (e.g. row $0$ and row $3$), extracting the $(x_{0, j_0}, x_{3, j_3})$ bilinear coefficients reduces computing $\mathrm{perm}_4$ to factoring the $4 \times 4$ quadratic matrix $P_{\mathrm{perm}}(Y)$ (in $Y = X_{\{1,2\}}$, $8$ variables) as:
$$M_1(Y)_{4\times 4} \cdot M_2(Y)_{4\times 4} = P_{\mathrm{perm}}(Y)_{4\times 4}, \qquad M_1, M_2 \in M_4(\mathbb{C}[Y]_1).$$

### Observed Results (`perm4_middle_factorization_probe.py`)
- **Determinant & Rank:**
  - $\det(P_{\det}(Y)) \equiv 0$ identically (generic rank $2$ at $Y = [[1,1,1,1],[1,2,3,4]]$).
  - $\det(P_{\mathrm{perm}}(Y))$ is a nonzero degree-$8$ polynomial with $12$ terms, generic rank $4$, evaluating to $-1616$ at $[[1,1,1,1],[1,2,3,4]]$.
  - Both $P_{\det}$ and $P_{\mathrm{perm}}$ span $6$-dimensional subspaces of quadrics in $S^2(\mathbb{C}^8)$. At `col2 = col3 = 0` (`rk(P_perm) = 2`), $\det(P_{\mathrm{perm}})$ has Hessian nullity `8/8`.
- **Irreducibility & Galois Obstruction against $4 \times 4$ Factorization:**
  - Any factorization $P_{\mathrm{perm}}(Y) = M_1(Y) M_2(Y)$ with linear $4\times 4$ matrices forces $\det(P_{\mathrm{perm}}(Y)) = \det(M_1(Y)) \cdot \det(M_2(Y))$ to split as a **degree-$4 \times$ degree-$4$** product over $\mathbb{C}$.
  - Across $150$ random univariate line slices $h(t) = \det(P_{\mathrm{perm}}(Y_0 + t Y_1))$ over $p \in \{101, 103, 107, 109, 113, 127\}$:
    - **`(8,)` (irreducible degree 8)** appeared **`17 / 150`** times across primes `101, 103, 109, 113, 127`, certifying **irreducibility over $\mathbb{Q}$**.
    - **`(1, 7)`** appeared **`29 / 150`** times and **`(3, 5)`** appeared **`11 / 150`** times. In a $\mathbb{Q}$-irreducible degree-8 polynomial, any decomposition into $k \in \{2, 4\}$ geometric factors of degrees $(4,4)$ or $(2,2,2,2)$ over $\mathbb{C}$ forces Frobenius cycle lengths on a line slice to either stay $\le 4$ or be even (when swapping conjugate blocks) — **ruling out $4\times 4$ and $2\times 2\times 2\times 2$ geometric factorizations** (`k = 2` and `k = 4`), hence ruling out $P_{\mathrm{perm}}(Y) = M_1(Y) M_2(Y)$ over $\mathbb{C}$!
- **Remaining Wall 1 Frontier (`m = 14` vs `m = 15`):**
  - Follow-up test [perm4_w5_factorization_search.py](file:///Users/bl10buer/Desktop/matemk/p-vs-np-gct/perm4_w5_factorization_search.py) probed $M_1(Y)_{4\times w} M_2(Y)_{w\times 4} = P_{\mathrm{perm}}(Y)$ ($576$ bilinear equations) via exact holomorphic Levenberg–Marquardt (verified: Grenet $w=6$ exact residual `0.0`, $\mathbb{F}_2$ rank $\le 2$, analytical Jacobian FD error `4.12e-09`, generic Jacobian rank `64w - w^2` for `w=4..8`):
    - **`w = 6` (`m = 15`):** `3/5` random complex starts solved to `min ||r||_2 = 1.539e-15` (median `1.230e-13`).
    - **`w = 4` (`m = 13`):** `0/8` starts (`min = 2.668`, median `2.669`), consistent with the Galois irreducibility obstruction.
    - **`w = 5` (`m = 14`):** `0/25` starts (`15` complex, `5` real, `5` truncated-Grenet warm starts) solved; all hit a hard residual floor `min = 1.983`, median `2.001`.
  - Thus `w = 5` (`m = 14` row-separated) shows strong numerical resistance at `||r||_2 ~ 2.0`, while an exact algebraic proof ruling out `m = 14` over $\mathbb{C}$ (and non-homogeneous ABPs) remains open.

---

## 2. Wall 2: Exact Boolean–Algebraic Bridge ($n = 3$ and $n = 4$)

[boolean_algebraic_bridge.py](file:///Users/bl10buer/Desktop/matemk/p-vs-np-gct/boolean_algebraic_bridge.py) computed exact Möbius transforms over $\mathbb{F}_2$ and $\mathbb{F}_3$ plus integer Fast Walsh–Hadamard spectra across all $2^9 = 512$ ($n=3$) and $2^{16} = 65,536$ ($n=4$) binary matrices:

### Key Observations for $n = 4$ (`65,536` matrices)

| Function | Complexity | $\mathbb{F}_2$ `(deg, nnz)` | $\mathbb{F}_3$ `(deg, nnz)` | $\mathrm{Inf}(F)$ | $L_1$-spec | $\mathrm{tail}(>4)$ |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| `det_mod2` | $\mathrm{P}$ ($\equiv \mathrm{perm}\bmod 2$) | `(4, 24)` | `(14, 6498)` | `5.250` | `165.88` | `0.565` |
| `det_nz_mod3` | $\mathrm{P}$ | `(12, 2832)` | **`(8, 282)`** | `4.699` | `150.25` | `0.482` |
| `perm_nz_mod3` | $\mathrm{Mod}_3\mathrm{P}$-hard | **`(15, 5002)`** | **`(8, 282)`** | `4.708` | `144.11` | `0.469` |
| `det_nz_Z` | $\mathrm{P}$ | `(9, 1080)` | `(13, 4194)` | `4.641` | `150.36` | `0.471` |
| `perm_pos_Z` | $\mathrm{P}$ (Matching) | `(16, 7443)` | `(16, 7443)` | **`2.407`** | **`75.84`** | **`0.120`** |
| `perm_ge2_Z` | $\mathrm{P}$ | `(16, 4323)` | `(16, 4857)` | `2.635` | `102.15` | `0.195` |

### Structural Lessons for the $\mathrm{VP} \neq \mathrm{VNP} \implies \mathrm{P} \neq \mathrm{NP}$ Bridge
1. **Field-translation blowup (`det_nz_mod3` vs `perm_nz_mod3`):** Over $\mathbb{F}_3$, squaring `(det_4)^2` and `(perm_4)^2` preserves identical polynomial complexity (`deg = 8, nnz = 282` for both; `deg = 6, nnz = 21` at `n = 3`). Translating into the Boolean $\mathbb{F}_2$-ANF basis breaks this symmetry: `det_nz_mod3` compresses to `(12, 2832)`, whereas `perm_nz_mod3` blows up to `(15, 5002)` (`n = 3`: `deg 7` vs `8`).
2. **Why raw Boolean degree fails against monotone $\mathrm{P}$ functions:** Bipartite Perfect Matching (`perm_pos_Z`, in $\mathrm{P}$) hits full Boolean degree `(16, 7443)` in both $\mathbb{F}_2$ and $\mathbb{F}_3$, exceeding `perm_nz_mod3` (`(15, 5002)`, `(8, 282)`), yet `perm_pos_Z` is **monotone** and concentrates `88%` of its Fourier $L_2$ energy at degree $\le 4$ (`Inf = 2.407`, `tail(>4) = 0.120`), whereas `perm_nz_mod3` retains `46.9%` of its $L_2$ energy above degree `4` (`Inf = 4.708`).
3. **Where the true gap remains:** Any bridge lifting $\mathrm{VP} \neq \mathrm{VNP}$ to general Boolean $\mathrm{P} \neq \mathrm{NP}$ must overcome the Razborov–Rudich natural proofs barrier on general $\mathrm{P}/\mathrm{poly}$ circuits; simple spectral tails or algebraic degrees over $\mathbb{F}_2$/$\mathbb{F}_3$ separate restricted classes ($\mathrm{AC}^0[2]$, $\mathrm{AC}^0[3]$) rather than unrestricted polynomial-size Boolean circuits.
