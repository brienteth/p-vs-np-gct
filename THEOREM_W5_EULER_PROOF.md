# Euler $\mathrm{Sym}_0(4)$ Linear-Algebraic Obstruction Proof for $w = 5$ ($m = 14$) Middle Factorization

**Script:** [euler_w5_obstruction_proof.py](file:///Users/bl10buer/Desktop/matemk/p-vs-np-gct/euler_w5_obstruction_proof.py)

## 1. Setup & Euler's $b = a$ Determinant Identity

Inside a row-separated $4$-layer homogeneous ABP for $\mathrm{perm}_4(X)$ (`layer sizes (4, 4, w, 4)` corresponding to $m = 9 + w$), contracting rows $1$ (`a = (y_0..y_3)`) and $2$ (`b = (y_4..y_7)`) gives a quadratic $4 \times 4$ matrix factorization problem over $\mathbb{C}$ (or any field $\mathbb{F}$ of $\mathrm{char} \neq 2$):
$$M_1(a, b)_{4 \times 5} \, M_2(a, b)_{5 \times 4} = P_{\mathrm{perm}}(a, b),$$
where $P_{\mathrm{perm}}(a, b)_{j_0, j_3} = (1 - \delta_{j_0, j_3})(a_{c_1} b_{c_2} + a_{c_2} b_{c_1})$ ($\{j_0, c_1, j_3, c_2\} = \{0, 1, 2, 3\}$). Writing $M_1 = A_1(a) + B_1(b)$ and $M_2 = A_2(a) + B_2(b)$ splits the polynomial identity by bidegree into:
1. $A_1(a) A_2(a) \equiv 0$,
2. $B_1(b) B_2(b) \equiv 0$,
3. $A_1(a) B_2(b) + B_1(b) A_2(a) \equiv P_{\mathrm{perm}}(a, b)$.

**Theorem 1 (Euler $b = a$ Determinant Identity).**
Setting $b_k = a_k$ ($0 \le k \le 3$) yields $P_{\mathrm{perm}}(a, a)_{j_0, j_3} = 2 (a_0 a_1 a_2 a_3) (1 - \delta_{j_0, j_3}) / (a_{j_0} a_{j_3})$, so:
$$\det(P_{\mathrm{perm}}(a, a)) = (2 a_0 a_1 a_2 a_3)^4 (a_0 a_1 a_2 a_3)^{-2} \det(J_4 - I_4) = 16 (-3) a_0^2 a_1^2 a_2^2 a_3^2 = -48 a_0^2 a_1^2 a_2^2 a_3^2.$$
*Symbolic check:* Verified exactly over $\mathbb{Z}$ (`{(2, 2, 2, 2): -48}`). Hence $\mathrm{rank}_{\mathbb{F}(a)}(P_{\mathrm{perm}}(a, a)) = 4$, forcing $\mathrm{rank}_{\mathbb{F}(a)}(M_1(a, a)) = \mathrm{rank}_{\mathbb{F}(a)}(M_2(a, a)) = 4$ and $\min(r_1, s_2) + \min(s_1, r_2) \ge 4$ alongside $r_1 + r_2 \le 5$, $s_1 + s_2 \le 5$.

---

## 2. Nisan Matrix & $\mathrm{Sym}_0(4)$ Structure

Define the $16 \times 16$ bilinear tensor (Nisan matrix) $M = N_{01}(P_{\mathrm{perm}})$ indexed by $(j_0, c_1) \in \{0..3\}^2$ (rows) and $(j_3, c_2) \in \{0..3\}^2$ (columns):
$$M_{(j_0, c_1), (j_3, c_2)} = [a_{c_1} b_{c_2}] \, P_{\mathrm{perm}}(a, b)_{j_0, j_3} = \begin{cases} 1 & \text{if } \{j_0, c_1, j_3, c_2\} = \{0, 1, 2, 3\}, \\ 0 & \text{otherwise.} \end{cases}$$
Reshaping each column (or row) as a $4 \times 4$ matrix makes $M$ invariant under $j_0 \leftrightarrow c_1$ with zero diagonal:
$$\mathrm{colsp}(M) = \mathrm{rowsp}(M) = \mathrm{Sym}_0(4) := \{S \in \mathbb{F}^{4 \times 4} : S^T = S,\; S_{ii} = 0\}, \qquad \dim \mathrm{Sym}_0(4) = \binom{4}{2} = 6.$$

---

## 3. Core Linear-Algebraic Lemmas (Over Any Field $\mathbb{F}$ of $\mathrm{char} \neq 2$)

**Lemma A (Symmetric Zero-Diagonal Subspace Bound).**
For every $d$-dimensional subspace $W \subseteq \mathbb{F}^4$,
$$\dim\big(\mathrm{Sym}_0(4) \cap (W \otimes W)\big) \le \binom{d}{2}.$$
*Proof.* Let $U \in \mathbb{F}^{4 \times d}$ have columns forming a basis of $W$. Any symmetric matrix in $W \otimes W$ has the form $U C U^T$ for a unique symmetric $C \in \mathrm{Sym}(d)$. Since $\mathrm{rank}(U) = d$, choose $d$ linearly independent rows $I \subseteq \{0..3\}$ of $U$ so $U_I \in \mathrm{GL}_d(\mathbb{F})$. The congruence $C \mapsto C' = U_I C U_I^T$ is a linear bijection $\mathrm{Sym}(d) \xrightarrow{\sim} \mathrm{Sym}(d)$, and the zero-diagonal condition on $U C U^T$ at rows $I$ forces $C'_{rr} = (U C U^T)_{I_r, I_r} = 0$ for all $1 \le r \le d$. Thus $C' \in \mathrm{Sym}_0(d)$, which has dimension $\binom{d}{2}$. $\square$

**Lemma C (Kernel-Complement Survival).**
For every nonzero vector $\beta \in \mathbb{F}^4$ and every $3 \times 4$ matrix $\Gamma$ whose rows span $\ker(\beta^T)$,
$$\mathrm{rank}\big((\Gamma \otimes I_4) M\big) = \mathrm{rank}\big((I_4 \otimes \Gamma) M\big) = 6.$$
*Proof.* Suppose $S \in \mathrm{Sym}_0(4)$ satisfies $(\Gamma \otimes I_4) \mathrm{vec}(S) = \mathrm{vec}(\Gamma S) = 0$. Then every column of $S$ lies in $\ker(\Gamma) = \mathrm{span}(\beta)$, and by symmetry of $S$, every row also lies in $\mathrm{span}(\beta)$, so $S \in \mathrm{Sym}_0(4) \cap (\mathrm{span}(\beta) \otimes \mathrm{span}(\beta))$. By Lemma A ($d = 1$), $\binom{1}{2} = 0$, so $S = 0$. Hence $(\Gamma \otimes I_4)$ is injective on $\mathrm{colsp}(M) = \mathrm{Sym}_0(4)$. Symmetry under $S \mapsto S^T$ yields the identical rank $6$ for $(I_4 \otimes \Gamma) M$. $\square$

**Lemma B (Swapped-Kronecker Rank Floor).**
For nonzero $B, V \in \mathbb{F}^{4 \times 4}$, define the rank-$(\mathrm{rank}(B)\mathrm{rank}(V))$ operator $K(B, V) \in \mathbb{F}^{16 \times 16}$ by $K(B, V)_{(j_0, c_1), (j_3, c_2)} = B_{j_0, c_2} V_{j_3, c_1}$ (arising from a single $B_1(b)_{4 \times 1} A_2(a)_{1 \times 4}$ wire). Then:
$$\mathrm{rank}\big(M - K(B, V)\big) \ge 5 \qquad \text{for all nonzero } B, V \in \mathbb{F}^{4 \times 4}.$$
*Proof.* Let $r_B = \mathrm{rank}(B) \ge 1$, $r_V = \mathrm{rank}(V) \ge 1$, $r_K = \mathrm{rank}(K) = r_B r_V$, and $U = \mathrm{im}(K) = \mathrm{im}(B) \otimes \mathrm{rowsp}(V)$. Any $S \in \mathrm{Sym}_0(4) \cap U$ satisfies $S = S^T \in W \otimes W$ where $W = \mathrm{im}(B) \cap \mathrm{rowsp}(V)$ has $\dim W \le \min(r_B, r_V)$. By Lemma A, $d_0 := \dim(\mathrm{im}(M) \cap U) \le \binom{\min(r_B, r_V)}{2}$. Next, for any matrices $M, K$ of the same size:
1. Projecting modulo $U$ gives $\mathrm{rank}(M - K) \ge \mathrm{rank}(M) - d_0 = 6 - d_0$.
2. For any $x \in \ker(M - K)$, $Kx = Mx \in \mathrm{im}(M) \cap U$, so $K(\ker(M - K))$ has dimension $\le d_0$ while $\ker(K|_{\ker(M-K)}) \subseteq \ker(K)$, giving $\dim\ker(M - K) \le \dim\ker(K) + d_0$, hence $\mathrm{rank}(M - K) \ge r_K - d_0$.

Combining both bounds across all $(r_B, r_V) \in \{1..4\}^2$:
- $\min(r_B, r_V) = 1$: $d_0 \le \binom{1}{2} = 0 \implies \mathrm{rank}(M - K) \ge 6 - 0 = 6$ (also directly from Lemma C).
- $\min(r_B, r_V) = 2$: $d_0 \le \binom{2}{2} = 1 \implies \mathrm{rank}(M - K) \ge 6 - 1 = 5$.
- $\min(r_B, r_V) = 3$: $d_0 \le \binom{3}{2} = 3$ and $r_K \ge 9 \implies \mathrm{rank}(M - K) \ge 9 - 3 = 6$.
- $(r_B, r_V) = (4, 4)$: $d_0 \le 6$ and $r_K = 16 \implies \mathrm{rank}(M - K) \ge 16 - 6 = 10$. $\square$

---

## 4. Elimination of Wire-Split $(5,0), (0,5), (4,1), (1,4)$ & Status of $(3,2)$

Consider any **constant-basis wire-split** factorization of width $w = 5$, meaning $r$ wires have bidegree $(a, b)$ (`A_1(a)_{4 x r} B_2(b)_{r x 4}`) and $5 - r$ wires have bidegree $(b, a)$ (`B_1(b)_{4 x (5-r)} A_2(a)_{(5-r) x 4}`):
$$P_{\mathrm{perm}}(a, b) = A_1(a)_{4 \times r} B_2(b)_{r \times 4} + B_1(b)_{4 \times (5-r)} A_2(a)_{(5-r) \times 4}.$$
Taking the Nisan matrix $N_{01}$ turns the $r$ wires of $A_1(a) B_2(b)$ into a matrix of rank $\le r$, and each of the $5 - r$ wires of $B_1(b) A_2(a)$ into $K(B_\ell, V_\ell)$. By $P_{\mathrm{perm}}(a, b) = P_{\mathrm{perm}}(b, a)$, swapping $a \leftrightarrow b$ exchanges $(r, 5-r) \leftrightarrow (5-r, r)$.

1. **Case $(5, 0)$ & $(0, 5)$ (Eliminated Formal Proof):** For $(5, 0)$, $\mathrm{rank}(M) \le 5$, contradicting $\mathrm{rank}(M) = 6$. By $a \leftrightarrow b$ swap, $(0, 5)$ is likewise impossible.
2. **Case $(4, 1)$ & $(1, 4)$ (Eliminated Formal Proof):** For $(4, 1)$, $M - K(B_1, V_1) = N_{01}(A_1(a)_{4 \times 4} B_2(b)_{4 \times 4})$ must have rank $\le 4$. This directly contradicts **Lemma B** ($\mathrm{rank}(M - K) \ge 5$). By $a \leftrightarrow b$ swap, $(1, 4)$ is likewise impossible.
3. **Case $(3, 2)$ & $(2, 3)$ (Surviving Regime — Probed Numerically):** Here $M - K_1 - K_2$ must have rank $\le 3$ (equivalently $A_1(a)_{4 \times 3} B_2(b)_{3 \times 4} + B_1(b)_{4 \times 2} A_2(a)_{2 \times 4} = P_{\mathrm{perm}}(a, b)$). While not eliminated algebraically by Lemma B alone, both algebraic discrete probes over $\mathbb{F}_{1000003}$ and $10$-start complex Levenberg–Marquardt optimization hit a hard residual floor $> 2.26$ (`0/10` solved).

---

## 5. Exact Observed Verification Results (`euler_w5_obstruction_proof.py`)

Run over $\mathbb{Z}$, $\mathbb{F}_{1000003}$, and $\mathbb{C}$ (exited with code `0` in `10.98s`):
- **Euler $b = a$ identity:** `det(P_perm(a, a)) == -48 * a_0^2 a_1^2 a_2^2 a_3^2` (`[PASS]` exact over $\mathbb{Z}$).
- **Nisan characterization:** `rank(M) == 6`, `colsp(M) == Sym_0(4)` (`[PASS]`).
- **Lemma A (`135` coordinate + random subspaces over $\mathbb{F}_{1000003}$):**
  - `d=1: max=0<=0`, `d=2: max=1<=1`, `d=3: max=3<=3`, `d=4: max=6<=6` (`[PASS]`).
- **Lemma C (`34` nonzero $\beta$ vectors, both tensor factors):** `min rank == 6` (`[PASS]`).
- **Lemma B (`1,545` random + adversarial structured pairs over $\mathbb{F}_{1000003}$):** ALL pairs satisfied `rank(M - K) >= 5`; empirical minimum ranks observed:
  - `r_B = 1`: `7, 8, 9, 10` (`r_V = 1..4`)
  - `r_B = 2`: `8, 9, 10, 12`
  - `r_B = 3`: `9, 10, 11, 13`
  - `r_B = 4`: `10, 12, 13, 16`
- **Test 4a (`(3, 2)` 2-Kronecker perturbation):**
  - Aligned rank-`(1+1)` pairs over $\mathbb{F}_{1000003}$: `min rank(M - K1 - K2) = 6` (`> 3`).
  - `500` random mixed-rank `(K1, K2)` pairs over $\mathbb{F}_{1000003}$: `min rank(M - K1 - K2) = 8` (`> 3`).
  - Complex LM (`10` starts, `256` eqs / `160` vars for $K_1 + K_2 + U_{16\times 3} W_{3\times 16} = M$): `min = 2.313171`, `median = 2.358023`, `best tail_svals[3:] = 2.313144`, `sigma_3 = 1.213865`.
- **Test 4b (Exact bidegree `(3, 2)` holomorphic LM, `10` starts, `256` eqs / `160` vars):**
  - `solved = 0/10`, `min = 2.262810`, `median = 2.313340`, `max = 2.390180`.

*Honest Scope Note:* Lemmas A, B, C rigorously eliminate all constant-basis wire-split `(5,0), (0,5), (4,1), (1,4)` regimes over any field of $\mathrm{char} \neq 2$. Two pieces remain mathematically open for a complete $\mathbb{C}$-proof excluding $w = 5$: (i) ruling out Case `(3, 2)` algebraically (currently backed by $0/10$ LM convergence and $\mathrm{rank} \ge 6$ on $\mathbb{F}_{1000003}$ samples), and (ii) proving whether arbitrary mixed-variable $(A_1(a)+B_1(b))(A_2(a)+B_2(b)) = P_{\mathrm{perm}}(a, b)$ must fall into `(3, 2)` or admits an unsplit cancellation (probed numerically by [perm4_w5_factorization_search.py](file:///Users/bl10buer/Desktop/matemk/p-vs-np-gct/perm4_w5_factorization_search.py) with `0/25` solved and floor `min = 1.983`).
