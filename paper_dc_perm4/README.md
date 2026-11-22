# Standalone Manuscript & Exact Certificate: $\mathrm{dc}_{\mathbb{C}}(\mathrm{perm}_4) \ge 10$

## Contents
- `dc_perm4_ge_10.tex`: Self-contained LaTeX manuscript proving $\mathrm{dc}_{\mathbb{C}}(\mathrm{perm}_4) \ge 10$.
  - Every algebraic step ($\mathrm{codim}(\mathrm{Sing}_2(V(\mathrm{perm}_4))) = 12$, mandatory $\mathrm{corank}(A_0) = 1$, origin-isotropy $\dim W = 8$, $2$-block normal form, $\xi$-linear extraction, Skew-Square Lemma, and order-$3$ vanishing) is proved completely by hand.
  - The single computer-assisted input is Theorem 3.1 ($\mathrm{codim}_{\mathbb{C}^{16}}(\mathrm{Sing}(V(\mathrm{perm}_4))) = 8$).
- `verify_codim_sing_perm4.py`: Standalone exact finite-field verification script (~185 lines) certifying:
  1. **Positive certificate ($L_8 \subset \mathbb{C}^{16}$):** Exact IMSC reduction modulo both $p_1 = 32{,}749$ and $p_2 = 65{,}521$ reaching full rank `11,440 / 11,440` (`corank = 0`) at degree $D = 9$.
  2. **Negative control ($L_9 \subset \mathbb{C}^{16}$):** Exact IMSC reduction modulo $p_1 = 32{,}749$ confirming strictly positive coranks (`753` at $D=6$, `580` at $D=7$).

## Reproduction
```bash
python3 verify_codim_sing_perm4.py
```

## Independent Verification in Macaulay2 (Optional)
Any algebraic geometer can independently verify $\mathrm{codim}_{\mathbb{C}^{16}}(\mathrm{Sing}(V(\mathrm{perm}_4))) = 8$ in Macaulay2 in 5 lines:
```m2
R = ZZ/32749[x_0..x_15];
X = genericMatrix(R, 4, 4);
perm4 = permanent X;
J = ideal diff(vars R, perm4);
codim J  -- returns 8
```
