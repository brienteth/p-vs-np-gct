/-
  PvsNP_Retrospective.lean
  Formal Lean 4 Kernel-Verified Proofs of Key Retrospective Lemmas
  (Zero `sorry`, pure Lean 4 core — independently verified by the Lean 4 kernel).
-/

namespace PvsNP_GCT

/-- Parity over F_2 (represented as Bool with xor) for a list of bits. -/
def parity : List Bool → Bool
  | [] => false
  | b :: bs => xor b (parity bs)

/-- Bitwise XOR of two equal-length bit lists. -/
def vecXor : List Bool → List Bool → List Bool
  | a :: as, b :: bs => xor a b :: vecXor as bs
  | _, _ => []

/-- Theorem 1 (KİLİT SORU H5 — Valiant's F_2 Linearity Lemma):
    PARITY is strictly additive (affine of degree 1) over F_2. -/
theorem parity_is_additive_f2 :
    ∀ (u v : List Bool), u.length = v.length →
      parity (vecXor u v) = xor (parity u) (parity v)
  | [], [], _ => rfl
  | a :: as, b :: bs, h => by
    have hlen : as.length = bs.length := Nat.succ.inj h
    simp only [vecXor, parity, parity_is_additive_f2 as bs hlen]
    cases a <;> cases b <;> cases (parity as) <;> cases (parity bs) <;> rfl

/-- Theorem 2 (KİLİT SORU H5 — AC^0 Non-Linearity Witness):
    The depth-1 AC^0 gate AND_2 is NOT additive over F_2, proving
    deg_F2(AND_2) > 1 = deg_F2(PARITY_n). -/
theorem and2_not_additive_f2 :
    ∃ (a1 a2 b1 b2 : Bool),
      ((xor a1 b1) && (xor a2 b2)) ≠ xor (a1 && a2) (b1 && b2) := by
  exact ⟨true, false, false, true, by decide⟩

/-- Theorem 3 (E3.11 / E4.6 — Characteristic-Zero Modular Minor Transfer):
    If an integer determinant d satisfies d % p ≠ 0 for any modulus p,
    then d ≠ 0 over Z (and hence over Q and C). -/
theorem char_zero_minor_transfer (d p : Int) (h : d % p ≠ 0) : d ≠ 0 := by
  intro hd
  subst hd
  simp at h

/-- 2x2 Permanent and Determinant over Int. -/
def perm2 (a b c d : Int) : Int := a * d + b * c
def det2  (a b c d : Int) : Int := a * d - b * c

/-- Theorem 4 (Mod-2 Coincidence):
    Over characteristic 2, perm_2 and det_2 are identically equal. -/
theorem perm2_eq_det2_mod2 (a b c d : Int) :
    perm2 a b c d % 2 = det2 a b c d % 2 := by
  unfold perm2 det2
  omega

/-- Theorem 5 (E5.6 — Mod-3 Separation Witness):
    Over F_3, there exists a {0,1}-matrix where perm_2 ≠ 0 (mod 3)
    while det_2 = 0 (mod 3). -/
theorem perm2_det2_mod3_separation :
    ∃ (a b c d : Int),
      (a = 0 ∨ a = 1) ∧ (b = 0 ∨ b = 1) ∧ (c = 0 ∨ c = 1) ∧ (d = 0 ∨ d = 1) ∧
      perm2 a b c d % 3 ≠ 0 ∧ det2 a b c d % 3 = 0 := by
  refine ⟨1, 1, 1, 1, Or.inr rfl, Or.inr rfl, Or.inr rfl, Or.inr rfl, ?_, ?_⟩
  · decide
  · decide

/-- 3x3 Permanent and Determinant over Int. -/
def perm3 (a11 a12 a13 a21 a22 a23 a31 a32 a33 : Int) : Int :=
  a11 * (a22 * a33 + a23 * a32) +
  a12 * (a21 * a33 + a23 * a31) +
  a13 * (a21 * a32 + a22 * a31)

def det3 (a11 a12 a13 a21 a22 a23 a31 a32 a33 : Int) : Int :=
  a11 * (a22 * a33 - a23 * a32) -
  a12 * (a21 * a33 - a23 * a31) +
  a13 * (a21 * a32 - a22 * a31)

/-- Theorem 6 (E5.6 — 3x3 Mod-2 Coincidence):
    Over F_2, perm_3 and det_3 coincide for ALL integer matrices. -/
theorem perm3_eq_det3_mod2 (a11 a12 a13 a21 a22 a23 a31 a32 a33 : Int) :
    perm3 a11 a12 a13 a21 a22 a23 a31 a32 a33 % 2 =
    det3  a11 a12 a13 a21 a22 a23 a31 a32 a33 % 2 := by
  unfold perm3 det3
  simp only [Int.mul_add, Int.mul_sub]
  omega

/-- Theorem 7 (E5.6 — 3x3 Mod-3 Non-Zero Separation Witness):
    The all-ones 3x3 matrix has det_3 = 0 (mod 3), whereas
    the 2x2-block + 1 matrix has perm_3 = 2 ≠ 0 (mod 3) and det_3 = 0 (mod 3). -/
theorem perm3_det3_mod3_separation :
    perm3 1 1 0 1 1 0 0 0 1 % 3 ≠ 0 ∧ det3 1 1 0 1 1 0 0 0 1 % 3 = 0 := by
  decide

/-- Theorem 8 (M_8 Macaulay Target Space Dimension Certificate):
    C(16, 8) = 12870 — exact target monomial space size for L_9 degree-8 surjectivity. -/
def choose : Nat → Nat → Nat
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => choose n k + choose n (k + 1)

theorem macaulay_m8_target_dim : choose 16 8 = 12870 := by
  decide

end PvsNP_GCT
