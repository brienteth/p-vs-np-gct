theorem positive_square_positivity (x : ℝ) (h : x > 0) : x ^ 2 > 0 := by
  exact mul_pos h h
