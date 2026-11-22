# Council Problem Brief (shared by all 6 professors)

Workbench: `/Users/bl10buer/Desktop/matemk/p-vs-np-gct/` (Python 3.9.6, NumPy 2.0.2, no sympy, no internet).
Key files: `THEOREM_W5_EULER_PROOF.md`, `euler_w5_obstruction_proof.py`, `perm4_middle_factorization_probe.py`,
`perm4_w5_factorization_search.py`, `poly_exact.py`, `README.md`, `BRIDGE_SYNTHESIS.md`.
Tip: `python3 -c` scripts can import `from perm4_middle_factorization_probe import extract_middle_4x4`,
`from poly_exact import permanent_poly`, `from apolar_higher_betti_probe import rank_matrix_mod`, `from perm4_abp_frontier import MOD` (MOD = 1_000_003).
Run from inside `p-vs-np-gct/`. Python 3.9: no `int.bit_count()`.

## Big picture (be honest about scale)
Valiant's VP vs VNP asks whether perm_n is a projection of det_m with m = poly(n). We study a tiny, concrete
instance: can perm_4 be computed by a row-separated layered homogeneous ABP with layer widths (4, 4, w, 4), i.e.
determinantal size m = 9 + w? Known: w = 6 (m = 15, Grenet) works; w = 4 (m = 13) is ruled out (Galois/irreducibility).
**Open: w = 5 (m = 14).** Settling it is a small but genuine finite result; it does NOT by itself resolve VP vs VNP.

## The reduced problem
Variables a = (a_0..a_3) (row 1 of X), b = (b_0..b_3) (row 2). Target 4x4 quadratic matrix:
P(a,b)_{j0,j3} = 0 if j0 = j3, else a_{c1} b_{c2} + a_{c2} b_{c1} where {j0,c1,j3,c2} = {0,1,2,3}.
Need linear matrices M1(a,b) (4x5), M2(a,b) (5x4) with M1 M2 = P identically.
Write M1 = A1(a) + B1(b), M2 = A2(a) + B2(b). Bidegree splitting gives:
  (i) A1(a)A2(a) = 0,  (ii) B1(b)B2(b) = 0,  (iii) A1(a)B2(b) + B1(b)A2(a) = P(a,b).

Nisan matrix M = N_01(P) is 16x16, M[(j0,c1),(j3,c2)] = 1 iff {j0,c1,j3,c2} = {0,1,2,3}. rank M = 6,
colspace = rowspace = Sym_0(4) (symmetric zero-diagonal 4x4).
A "(b,a) wire" ℓ (column of B1 linear in b, row of A2 linear in a) contributes K(B,V)[(j0,c1),(j3,c2)] = B[j0,c2] V[j3,c1].
An "(a,b) wire" contributes a rank-1 term to N_01.

## Proven (char != 2), see THEOREM_W5_EULER_PROOF.md
- det P(a,a) = -48 a0^2 a1^2 a2^2 a3^2 (exact).
- Lemma A: dim(Sym_0(4) ∩ W⊗W) <= C(d,2) for dim W = d.
- Lemma B: rank(M - K(B,V)) >= 5 for all nonzero B,V.  Lemma C: (Γ⊗I)M has rank 6.
- Hence wire-split regimes (5,0),(0,5),(4,1),(1,4) are impossible.

## OPEN — what the council must attack
**Q1 (Case (3,2)).** Prove or refute: there exist A1 (4x3, linear in a), B2 (3x4, linear in b),
B1 (4x2, linear in b), A2 (2x4, linear in a) with A1 B2 + B1 A2 = P(a,b) (with or without (i),(ii)).
Equivalent: M = R3 + K(B1,V1) + K(B2,V2) with rank R3 <= 3. Numerics: 0/10 complex LM, floor ≈ 2.26;
F_p samples give rank(M - K1 - K2) >= 6. Need an ALGEBRAIC proof (or an explicit solution!).
**Q2 (Unsplit case).** In general the 5 middle wires need not be pure (a,b) or (b,a): a column of M1 may mix
a and b, as may a row of M2. Constraints (i),(ii) then restrict ranks: with r1 = rank A1(a), s1 = rank B1(b),
r2 = rank A2(a), s2 = rank B2(b) over the function field, (i) gives r1 + r2 <= 5, (ii) gives s1 + s2 <= 5,
and det P(a,a) ≠ 0 gives min(r1,s2)+min(s1,r2) >= 4. Show that every solution reduces to a wire-split
case (so Q1 + Lemmas A–C finish w = 5), or find an unsplit obstruction directly. Numerics on the full
576-equation system: 0/25 solved, floor min 1.983.
**Q3.** Which conserved invariant / symmetry argument (S4×S4, transpose, a↔b swap, GL-actions on the 5-dim middle)
gives the cleanest proof? Is there an obstruction of the form "rank of a flattening of the 3-tensor"?

## Rules
- Mathematical honesty: label each claim as PROVEN (with argument), CHECKED NUMERICALLY (with exact command/output), or CONJECTURE.
- Write your own scratch scripts ONLY under `p-vs-np-gct/council/<your-name>/`. Never edit files outside your folder.
- Discuss on the message board: challenge each other's arguments, find gaps, propose lemmas. Keep posts concrete.
- Final deliverable per professor: `p-vs-np-gct/council/<your-name>/REPORT.md` with your verified contributions.
