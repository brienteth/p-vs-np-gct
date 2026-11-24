theorem E2_6_hypergraph_handshake_bound :
  ∀ (w₂ : ℕ),
    w₂ = 8 ∨ w₂ = 9 →
    ∀ (a : List ℕ),
      a = [2, 1, 1, 1, 1] →
      List.sum a = 6 →
      6 + w₂ ≥ 14
:= by
  intro w₂ h_w₂ a h_a h_sum
  simp [h_a, h_sum] at *
  rcases h_w₂ with (rfl | rfl)
  · -- Case w₂ = 8
    omega
  · -- Case w₂ = 9
    omega
