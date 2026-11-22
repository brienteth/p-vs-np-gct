"""Decomposition of Sym_0(4) and Nisan matrix M under S_4."""
import itertools
import numpy as np

# Basis of Sym_0(4)
pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
pair_to_idx = {p: i for i, p in enumerate(pairs)}

def pair_norm(i, j):
    return (min(i, j), max(i, j))

# Build S_4 representation on Sym_0(4)
perms = list(itertools.permutations(range(4)))
rep = []
for p in perms:
    mat = np.zeros((6, 6), dtype=float)
    for idx, (i, j) in enumerate(pairs):
        pi, pj = pair_norm(p[i], p[j])
        mat[pair_to_idx[(pi, pj)], idx] = 1.0
    rep.append((p, mat))

# Character table of S_4
# Classes:
# id (1), (0 1) (6), (0 1)(2 3) (3), (0 1 2) (8), (0 1 2 3) (6)
def cycle_type(p):
    visited = [False]*4
    cycles = []
    for i in range(4):
        if not visited[i]:
            c = 0
            curr = i
            while not visited[curr]:
                visited[curr] = True
                curr = p[curr]
                c += 1
            cycles.append(c)
    cycles.sort(reverse=True)
    return tuple(cycles)

# Projection operators: P_chi = (dim_chi / |G|) sum_{g} chi(g) rho(g)
chars = {
    'triv (4)': {
        'dim': 1,
        'chi': {(1,1,1,1): 1, (2,1,1): 1, (2,2): 1, (3,1): 1, (4,): 1}
    },
    'std (3,1)': {
        'dim': 3,
        'chi': {(1,1,1,1): 3, (2,1,1): 1, (2,2): -1, (3,1): 0, (4,): -1}
    },
    '(2,2)': {
        'dim': 2,
        'chi': {(1,1,1,1): 2, (2,1,1): 0, (2,2): 2, (3,1): -1, (4,): 0}
    },
    '(2,1,1)': {
        'dim': 3,
        'chi': {(1,1,1,1): 3, (2,1,1): -1, (2,2): -1, (3,1): 0, (4,): 1}
    },
    'sgn (1,1,1,1)': {
        'dim': 1,
        'chi': {(1,1,1,1): 1, (2,1,1): -1, (2,2): 1, (3,1): 1, (4,): -1}
    }
}

projections = {}
for name, data in chars.items():
    P = np.zeros((6, 6), dtype=float)
    dim_chi = data['dim']
    chi_dict = data['chi']
    for p, mat in rep:
        ct = cycle_type(p)
        P += chi_dict[ct] * mat
    P = (dim_chi / 24.0) * P
    tr = np.trace(P)
    projections[name] = P
    if abs(tr) > 1e-5:
        print(f"Irrep {name:15s}: dim = {tr:.1f}")

# Action of M on Sym_0(4):
# M swaps complementary pairs and multiplies by 2
# Pairs:
# 0: (0,1) <-> 5: (2,3)
# 1: (0,2) <-> 4: (1,3)
# 2: (0,3) <-> 3: (1,2)
M_sym0 = np.zeros((6, 6), dtype=float)
M_sym0[0, 5] = 2.0
M_sym0[5, 0] = 2.0
M_sym0[1, 4] = 2.0
M_sym0[4, 1] = 2.0
M_sym0[2, 3] = 2.0
M_sym0[3, 2] = 2.0

print("\nChecking commutativity of M_sym0 with S_4 representation:")
max_comm_err = max(np.linalg.norm(M_sym0 @ mat - mat @ M_sym0) for p, mat in rep)
print(f"Max ||M rho - rho M||: {max_comm_err:.2e}")

# Check action on each irrep subspace
print("\nEigenvalues of M on each irrep subspace:")
for name in ['triv (4)', 'std (3,1)', '(2,2)']:
    P = projections[name]
    # M @ P should equal lambda * P
    # Find scalar
    # Since P is non-zero, let's take tr(M @ P) / tr(P)
    lam = np.trace(M_sym0 @ P) / np.trace(P)
    err = np.linalg.norm(M_sym0 @ P - lam * P)
    print(f"  {name:15s}: eigenvalue = {lam:+.2f}, error = {err:.2e}")
