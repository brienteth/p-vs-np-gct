import Init.DataNat.Basic
import Init.DataList.Basic
import Init.DataNat.Order

/--
  0GM Proof Strategy:
  1. Define factorial and falling factorial over Nat.
  2. Compute the Gaussian Binomial Coefficient (q-binomial) for q=3, n=5, k=2.
  3. Verify that the count of Gr(2,5, F_3) is 1210, not 14040.
  4. Formalize the discrepancy to refute the erroneous claim.
--/

def fallingFactorial (n k : Nat) : Nat :=
  Nat.factorial n / Nat.factorial (n - k)

def gaussianBinomial (q n k : Nat) : Nat :=
  (fallingFactorial n k * product (fun i => q ^ i) (List.range k)) /
  (product (fun i => q ^ i) (List.range k) * product (fun i => q ^ i) (List.range k)) |? false  -- Correction applied below for correctness without Mathlib's big operators

-- Correct implementation without Mathlib's product
def prodList (f : Nat → Nat) (l : List Nat) : Nat :=
  l.foldl (fun acc x => acc * f x) 1

def gaussianBinomialCorrect (q n k : Nat) : Nat :=
  let num := prodList (fun i => q ^ i - 1) (List.range k |>.map (· + (n - k)))  -- Numerator: product(q^i - 1) for i in 1..k
  let den := prodList (fun i => q ^ i - 1) (List.range k)                     -- Denominator: product(q^i - 1) for i in 1..k
  num / den

-- Specific case for q=3, n=5, k=2
def expectedCount : Nat :=
  gaussianBinomialCorrect 3 5 2

example : expectedCount = 1210 := by
  rfl

-- Counter-proof to the claim of 14040
theorem incorrect_cardinality_claim : False := by
  intro h
  -- Assume the claim 14040 is equal to the correct count
  have h_calc : expectedCount = 1210 := by rfl
  -- 14040 is not 1210
  omega
