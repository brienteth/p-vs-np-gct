theorem qh1_orbit_combinatorial_identity :
  ∀ (n : Nat), n > 0 →
  Nat.choose (2 * n) n = 2 * Nat.choose (2 * n - 1) (n - 1) :=
by
  intro n hn
  rw [Nat.choose_symm2]
  ring
  <;> omega
