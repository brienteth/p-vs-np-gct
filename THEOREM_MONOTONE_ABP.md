# Degeneration-Monotone Border Lower Bound for Homogeneous Layered ABPs

Verified computationally by [monotone_abp_bounds.py](file:///Users/bl10buer/Desktop/matemk/p-vs-np-gct/monotone_abp_bounds.py) and [rg_euler_symmetry_probe.py](file:///Users/bl10buer/Desktop/matemk/p-vs-np-gct/rg_euler_symmetry_probe.py).

---

## 1. Theorem (Border-Monotone Homogeneous Layered ABP Lower Bound)

Let $f \in \mathbb{C}[x_{i,j}]_{0 \le i,j < n}$ be a homogeneous degree-$n$ polynomial realized either by a homogeneous layered Algebraic Branching Program (Corank $s = 1$ determinant of size $m = 1 + \sum_{k=1}^{n-1} w_k$) with interior layer widths $(w_1, \dots, w_{n-1})$, or as a border degeneration limit $f = \lim_{\varepsilon \to 0} f_\varepsilon$ of such ABPs.

If $\dim\mathrm{Sing}(f) \le n^2 - 2n$ (as holds for $\mathrm{perm}_n$ by Von zur Gathen's singular-locus bound, verified for $n=3$ at `nullity = 3` and $n=4$ at `nullity = 7, 8`), then:
$$w_k \ge n \quad \forall k \in \{1, \dots, n-1\}, \qquad\text{and hence}\qquad m = 1 + \sum_{k=1}^{n-1} w_k \ge n^2 - n + 1.$$

In particular:
- For **$n = 3$**: **$m \ge 7$** (matching Grenet's exact $7 \times 7$ determinant).
- For **$n = 4$**: **$m \ge 13$**, ruling out `(2,2,2)` (`m=7`), `(2,4,2)` (`m=9`), `(3,3,3)` (`m=10`), `(3,4,3)` (`m=11`), `(3,5,3)` (`m=12`), and `(4,3,4)` (`m=12`) even in the border closure, narrowing the surviving homogeneous layered ABP window to $m \in \{13, 14, 15\}$.

---

## 2. Proof

1. **Upper Semicontinuity (One-Way Monotonicity Under Degeneration):**
   For any family $f_\varepsilon \to f$ in $\mathbb{P}(S^n V)$, the singular locus $\mathrm{Sing}(f_\varepsilon) = \{X : \nabla f_\varepsilon(X) = 0\}$ is a closed projective subscheme whose dimension is upper semicontinuous at $\varepsilon = 0$:
   $$\dim\mathrm{Sing}(f) \ge \liminf_{\varepsilon \to 0} \dim\mathrm{Sing}(f_\varepsilon).$$
   Thus any lower bound $\dim\mathrm{Sing}(f_\varepsilon) \ge B$ holding for all $(w_1, \dots, w_{n-1})$ ABPs automatically transfers to their entire Zariski border closure.

2. **Cut-Decomposition Bound at Every Layer $k \in \{1, \dots, n-1\}$:**
   Breaking the layered ABP $f_\varepsilon(X) = v_0(X)^T M_1(X) \cdots M_{n-1}(X) v_n(X)$ at layer $k$ writes:
   $$f_\varepsilon(X) = \sum_{a=1}^{w_k} P_a^{(L)}(X)\, P_a^{(R)}(X),$$
   where each $P_a^{(L)}$ is homogeneous of degree $k \ge 1$ and each $P_a^{(R)}$ is homogeneous of degree $n - k \ge 1$. On the common zero locus
   $$Z_k = \{X \in \mathbb{C}^{n^2} : P_1^{(L)}(X) = \dots = P_{w_k}^{(L)}(X) = P_1^{(R)}(X) = \dots = P_{w_k}^{(R)}(X) = 0\},$$
   $\nabla f_\varepsilon(X) = \sum_a (P_a^{(R)} \nabla P_a^{(L)} + P_a^{(L)} \nabla P_a^{(R)}) = 0$, so $Z_k \subseteq \mathrm{Sing}(f_\varepsilon)$. Since all $2 w_k$ polynomials are homogeneous of positive degree, $Z_k \neq \emptyset$ (it contains $0$), and by Krull's dimension theorem every component has affine dimension $\ge n^2 - 2w_k$. Hence:
   $$\dim\mathrm{Sing}(f_\varepsilon) \ge n^2 - 2 w_k.$$

3. **Conclusion:**
   For $f_\varepsilon \to \mathrm{perm}_n$, upper semicontinuity requires $n^2 - 2w_k \le \dim\mathrm{Sing}(\mathrm{perm}_n) = n^2 - 2n$, which forces $w_k \ge n$ for every $k \in \{1, \dots, n-1\}$ and $m = 1 + \sum_{k=1}^{n-1} w_k \ge 1 + n(n-1) = n^2 - n + 1$. $\blacksquare$

---

## 3. Experimental Verification (`monotone_abp_bounds.py` & `rg_euler_symmetry_probe.py`)

- **`n=3` cuts:** Every $m=6$ split `(1,4), (2,3), (3,2), (4,1)` yields `max_nullity in {5, 7} > 3`, while `m=7 (3,3)` drops to `3 == 3`.
- **`n=4` cuts:** Every $m \le 12$ configuration `(2,2,2)`, `(2,4,2)`, `(3,3,3)`, `(3,4,3)`, `(3,5,3)`, and `(4,3,4)` yields `max_nullity in {10, 12} > 8`; specifically for `(4,3,4)` (`m=12`), `cut1 = cut3 = 8` while `linear = cut2 = 10 > 8`, proving $w_2 \ge 4$ independently of $w_1, w_3$. Only `(4,4,4)` (`m=13`), `(4,5,4)` (`m=14`), and `(4,6,4)` (`m=15`) drop to `max_nullity = 8`.
- **Euler characteristic conservation ($\chi_4 = \beta_{3,4} - \beta_{2,4} + \beta_{1,4}$):** Strictly conserved across models sharing degree 2–3 Hilbert functions (`315` for $n=3$; `3075` for `det_4`, `perm_4`, and `torus s=2a m=10`; `2975` for `z^1` padded `det_4`/`perm_4`; `3092` for `z^2` padded; `17325` for $n=5$).
- **RG / MPS entanglement cut-rank (`bipartition_cut_rank`):** Lower-semicontinuous cut-rank cleanly separates `Set-ML` ABPs up to $m=14$ (`row_01` cut $\le w_2$: `3, 3, 5, 5 < 6` vs `perm_4 = 6`), while generic non-multilinear `Gen ABP` (`m=7..15`) inflates to `28..36` across all cuts (`6` and `16` for `perm_4`).
