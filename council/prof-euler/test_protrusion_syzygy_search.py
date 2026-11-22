"""
Prof. Euler: test_protrusion_syzygy_search.py
Systematic analysis of degenerate Kruskal-Katona loci for n = 6, w = 19.
Examine all subgraphs of K_6 that achieve delta(U) >= 3, construct their canonical wires,
add t_B in {2, 3, 4} protruding rows, and test for non-trivial left syzygies with B_{1,in} != 0.
"""
import itertools
import numpy as np
import sys
sys.path.append('council/prof-noether')
from general_n2k_noether import build_Mn

def find_all_delta_ge_3_subspaces():
    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    sub2_to_idx = {s: i for i, s in enumerate(sub_2)}
    sub3_to_idx = {s: i for i, s in enumerate(sub_3)}
    
    print("=" * 70)
    print("STEP 1: IDENTIFYING ALL DEGENERATE SUBGRAPHS U OF K_6 WITH DELTA(U) >= 3")
    print("=" * 70)
    
    # Subgraphs on 6 vertices with d <= 8 edges that achieve delta >= 3:
    # A subgraph G has delta(G) = number of triangles K_3 contained in G!
    # Because for coordinate edge sets U, each triangle T in G has all 3 edges in U,
    # so v_T in S_{6,3} cap (U x F^6).
    # Can delta(G) exceed the number of triangles for coordinate edge sets?
    # Let's verify for ALL edge sets of size d in {6, 7, 8}!
    
    high_delta_sets = []
    
    for d in [6, 7, 8]:
        for edges in itertools.combinations(range(15), d):
            drop = [i for i in range(15) if i not in edges]
            Gamma = np.zeros((15 - d, 15))
            for r, row_idx in enumerate(drop):
                Gamma[r, row_idx] = 1.0
            H = np.kron(Gamma, np.eye(6)) @ V_basis
            rk = np.linalg.matrix_rank(H, tol=1e-7)
            delta = 20 - rk
            if delta >= 3:
                # Count triangles
                tri_count = 0
                for T in sub_3:
                    e1 = sub2_to_idx[(T[0], T[1])]
                    e2 = sub2_to_idx[(T[0], T[2])]
                    e3 = sub2_to_idx[(T[1], T[2])]
                    if e1 in edges and e2 in edges and e3 in edges:
                        tri_count += 1
                assert delta == tri_count, f"delta {delta} != tri_count {tri_count}"
                high_delta_sets.append((d, delta, edges, tri_count))
                
    print(f"Found {len(high_delta_sets)} edge sets with delta >= 3 (out of C(15,6)+C(15,7)+C(15,8) = 17875):")
    # Group by (d, delta)
    counts = {}
    for d, delta, _, _ in high_delta_sets:
        counts[(d, delta)] = counts.get((d, delta), 0) + 1
    for k in sorted(counts.keys()):
        print(f"  d = {k[0]}, delta = {k[1]}: {counts[k]} isomorphic subgraphs")
        
    return high_delta_sets

def test_syzygy_on_degenerate_loci(high_delta_sets):
    M6, V_basis, comp_perm, sub_2, sub_3 = build_Mn(6)
    sub2_to_idx = {s: i for i, s in enumerate(sub_2)}
    
    print("\n" + "=" * 70)
    print("STEP 2: TESTING SYZYGY RIGIDITY ON ALL NON-ISOMORPHIC DEGENERATE LOCI")
    print("=" * 70)
    
    # Pick one representative for each (d, delta)
    representatives = {}
    for d, delta, edges, tri in high_delta_sets:
        if (d, delta) not in representatives:
            representatives[(d, delta)] = edges
            
    rng = np.random.default_rng(2026)
    
    # S_{6,3}^perp basis
    u_V, s_V, _ = np.linalg.svd(V_basis)
    V_orth = u_V[:, 20:] # 90 x 70
    
    for (d, delta), edges in representatives.items():
        print(f"\n--- Testing representative for d={d}, delta={delta} ({delta} triangles) ---")
        
        # What are the triangles in this subgraph?
        subgraph_triangles = []
        for s_idx, T in enumerate(sub_3):
            e1 = sub2_to_idx[(T[0], T[1])]
            e2 = sub2_to_idx[(T[0], T[2])]
            e3 = sub2_to_idx[(T[1], T[2])]
            if e1 in edges and e2 in edges and e3 in edges:
                subgraph_triangles.append(s_idx)
        print(f"  Triangles in subgraph: {subgraph_triangles}")
        
        # Test for t_B in {2, 3, 4} protruding wires:
        # B2_in has 19 - t_B wires from S_{6,3}.
        # What if B2_in contains the delta triangles of U?
        for t_B in [2, 3, 4]:
            n_in = 19 - t_B
            # Pick 19 - t_B wires in S_{6,3} containing the delta triangles
            remaining_wires = [w for w in range(20) if w not in subgraph_triangles]
            wires_to_pick = subgraph_triangles + remaining_wires[:(n_in - len(subgraph_triangles))]
            assert len(wires_to_pick) == n_in
            
            B2_in = np.zeros((6, n_in, 15))
            for ell, w_idx in enumerate(wires_to_pick):
                B2_in[:, ell, :] = V_basis[:, w_idx].reshape(15, 6).T
                
            # Now add t_B protruding wires:
            # 1. Random in S_{6,3}^perp
            # 2. Koszul relations of the delta triangles (e.g. b_i e_J^T)
            # Test 10 random choices of B2_out in S_{6,3}^perp
            min_syz_dim = 100
            for trial in range(5):
                W_out = rng.standard_normal((t_B, 70))
                B2_out_rows = W_out @ V_orth.T # t_B x 90
                B2_out = np.zeros((6, t_B, 15))
                for ell in range(t_B):
                    B2_out[:, ell, :] = B2_out_rows[ell].reshape(15, 6).T
                    
                B2_tensor = np.concatenate([B2_in, B2_out], axis=1) # (6, 19, 15)
                
                # Compute syzygy matrix
                eqs = []
                for J in range(15):
                    for c1 in range(6):
                        for c2 in range(c1, 6):
                            row = np.zeros(6 * 19, dtype=float)
                            for ell in range(19):
                                row[c1 * 19 + ell] += B2_tensor[c2, ell, J]
                                if c1 != c2:
                                    row[c2 * 19 + ell] += B2_tensor[c1, ell, J]
                            eqs.append(row)
                E_mat = np.array(eqs)
                rk = np.linalg.matrix_rank(E_mat, tol=1e-7)
                syz_dim = 114 - rk
                min_syz_dim = min(min_syz_dim, syz_dim)
                
            print(f"  t_B = {t_B} protruding: dim(deg-1 left syzygies) = {min_syz_dim}")

if __name__ == '__main__':
    high_delta = find_all_delta_ge_3_subspaces()
    test_syzygy_on_degenerate_loci(high_delta)
