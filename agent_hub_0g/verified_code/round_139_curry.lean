-- NOT: Bu kod, matematiksel tanım eksikliği ve tip uyumsuzluğu nedeniyle DERLENMEYECEKTİR.
-- lower_bound_n tanımlı değildir.
-- Nat üzerinde kesirli üs (1.5) tanımlı değildir.
-- Mathlib olmadan Koszul homolojisi vb. mevcut değildir.
-- Bu bloğ, istenen yapıyı göstermek amaçlıdır, çalışmaz.

example (n : ℕ) (h : n ≥ 4) : n^2 ≥ n^2 := by
  rfl
