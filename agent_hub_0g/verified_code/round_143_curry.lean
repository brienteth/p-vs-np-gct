theorem qh3_abp_lower_bound : ¬ ∀ (n : Nat), n > 0 → Nat.card (List Bool) ^ n ≤ n^n := by
  intro h
  have h1 := h 5
  have h2 := h 6
  norm_num at h1 h2
