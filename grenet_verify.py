"""Verify explicit determinantal complexity constructions for perm_2 and perm_3 (Grenet 2011)."""
from __future__ import annotations

from typing import Dict, List, Tuple

from poly_exact import (
    Poly,
    const_poly,
    permanent_poly,
    poly_det,
    var_poly,
    zero_poly,
)


def grenet_matrix_perm3() -> List[List[Poly]]:
    """
    Grenet's 7x7 affine-linear matrix M(X) such that det(M(X)) = perm_3(X).
    Vertices correspond to subsets S of {0, 1, 2} with |S| < 3 (7 vertices total):
      0: ()
      1: (0,), 2: (1,), 3: (2,)
      4: (0, 1), 5: (0, 2), 6: (1, 2)
    """
    num_vars = 9
    subsets: List[Tuple[int, ...]] = [
        (),
        (0,),
        (1,),
        (2,),
        (0, 1),
        (0, 2),
        (1, 2),
    ]
    idx_of: Dict[Tuple[int, ...], int] = {s: i for i, s in enumerate(subsets)}
    m = len(subsets)  # 7
    mat: List[List[Poly]] = [[zero_poly() for _ in range(m)] for _ in range(m)]

    # Self-loops of weight 1 on all vertices except the root ()
    for i in range(1, m):
        mat[i][i] = const_poly(1, num_vars)

    # Transitions: from S of size r, add element j not in S with weight x_{r, j}
    for s in subsets:
        r = len(s)
        u = idx_of[s]
        for j in range(3):
            if j in s:
                continue
            nxt = tuple(sorted(s + (j,)))
            v = 0 if len(nxt) == 3 else idx_of[nxt]
            mat[u][v] = var_poly(r * 3 + j, num_vars)

    return mat


def main() -> None:
    # Check perm_2 as 2x2 determinant: [[x00, x01], [-x10, x11]]
    mat2 = [
        [var_poly(0, 4), var_poly(1, 4)],
        [var_poly(2, 4, coeff=-1), var_poly(3, 4)],
    ]
    det2 = poly_det(mat2, 4)
    p2 = permanent_poly(2)
    print(f"perm_2 == det(M_2): {det2 == p2} (terms={len(p2)})")

    # Check perm_3 as 7x7 Grenet determinant
    mat3 = grenet_matrix_perm3()
    det3 = poly_det(mat3, 9)
    p3 = permanent_poly(3)
    print(f"perm_3 == det(Grenet_7x7): {det3 == p3} (terms={len(p3)})")


if __name__ == "__main__":
    main()
