import Init.Data.Nat.Basic
import Init.Data.List.Basic
import Init.Data.Fin.Basic
import Init.Meta

/-- 
  Lemma: $n$ elemanlı bir kümenin permütasyonlarında,
  sabit nokta sayısı tam olarak $k$ olan permütasyon sayısı pozitif
  olur ($0 \le k \le n$)
-/
theorem fixed_point_permutation_positive (n k : Nat) (h_bounds : k ≤ n) :
  Nat.pos (count_fixed_points_permutations n k) := by
  simp [count_fixed_points_permutations]
  omega
