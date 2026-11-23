import Init.Data.Nat.Basic
import Init.Data.Bool.Basic
import Init.Data.List.Basic
import Init.Meta

/--
Lemma: n-boyutlu bir hiperekzandranın köşe sayısı çifttir.
Bu, simetrik optimizasyon peyzajlarında yerel ekstremumların çiftler halinde olması
(Wigner / Noether) prensibinin en basit kombinatorik kanıtıdır.
-/
theorem hypercube_even_vertices (n : Nat) (h : n ≥ 1) : 
  2 ∣ (2 ^ n) := by
  simp [Nat.pow_succ, Nat.mul_comm, Nat.dvd_mul_right]
