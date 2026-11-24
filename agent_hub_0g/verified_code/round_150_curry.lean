theorem modular_rank_discrepancy :
  ∀ (n : Nat), n ≥ 2 →
  (Finset.card (Finset.filter (fun M : List Bool => 
    List.length M = n * n ∧ 
    (∀ i j, List.get? M (i * n + j) = true)
  ) (Finset.univ : Finset (List Bool))) % 3) ≠ 
  (Finset.card (Finset.filter (fun M : List Bool => 
    List.length M = n * n ∧ 
    (∀ i j, List.get? M (i * n + j) = false)
  ) (Finset.univ : Finset (List Bool))) % 3)  := by sorry
