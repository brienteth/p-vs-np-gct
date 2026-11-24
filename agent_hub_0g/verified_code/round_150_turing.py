import numpy as np

def mod_rank(A, p):
    """Matrix rank modulo p, numpy-based simple Gaussian elimination."""
    A = A % p
    m, n = A.shape
    rank = 0
    pivot_row = 0
    for col in range(n):
        if pivot_row >= m:
            break
        # Find pivot
        found = False
        for row in range(pivot_row, m):
            if A[row, col] % p != 0:
                # Swap
                A[[pivot_row, row]] = A[[row, pivot_row]]
                found = True
                break
        if not found:
            continue
        # Eliminate
        inv = pow(int(A[pivot_row, col]), p - 2, p)  # Fermat's little theorem for inverse mod p
        for row in range(m):
            if row != pivot_row and A[row, col] % p != 0:
                factor = (A[row, col] * inv) % p
                A[row] = (A[row] - factor * A[pivot_row]) % p
        pivot_row += 1
        rank += 1
    return rank

# Test Case: 3x3 Matrix modulo 3
# Matrix designed to have determinant 0 mod 3 -> rank should be < 3
test_matrix = np.array([[1, 2, 1],
                        [2, 1, 1],
                        [1, 1, 2]])

print("Matrix modulo 3:")
print(test_matrix % 3)

det_mod3 = np.linalg.det(test_matrix) % 3
print(f"Determinant mod 3: {det_mod3}")

rank_mod3 = mod_rank(test_matrix, 3)
print(f"Rank modulo 3: {rank_mod3}")

# Assert: If det is 0 mod 3, rank must be < 3
assert det_mod3 == 0, "Determinant mod 3 should be 0"
assert rank_mod3 < 3, "Rank modulo 3 should be less than 3 if determinant is 0"

# Contrast: Identity matrix rank should be 3
identity = np.eye(3, dtype=int)
rank_id = mod_rank(identity, 3)
assert rank_id == 3, "Identity matrix rank mod 3 should be 3"

print("PASS: Modular rank consistency verified.")
