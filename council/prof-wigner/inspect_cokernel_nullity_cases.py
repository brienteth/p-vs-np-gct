"""Prof. Wigner Round 7: Inspect exact nullities of M(C_out) = Q_{perp,E}^T E_out(C_out)
across Star-Koszul, Edge-Koszul, Pure-Protruding, and LM solutions at t_B = 2, 3, 4.
Also check what happens when Star-Koszul (m=6 pairs, null=6 in M) is intersected with ANY 15D B2_in!
"""
import itertools
import numpy as np
import sys
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council/prof-noether")
from general_n2k_noether import build_Mn
from test_gap2_cokernel_bound import build_cokernel_proj

def proj_to_perp(mat_6x15, Q_perp_tensor):
    return np.einsum("qcJ,cJ->q", Q_perp_tensor, mat_6x15)

def check_known_families(T_M, Q_perp_tensor, sub_2, sub_3):
    print("=" * 74)
    print("1. EXACT NULLITIES OF M(C_out) FOR ALL KNOWN KOSZUL FAMILIES")
    print("=" * 74)
    sub2_idx = {s: i for i, s in enumerate(sub_2)}
    rng = np.random.default_rng(42)
    b_chk = rng.standard_normal(6)

    def eval_M(name, r_list):
        t_B = len(r_list)
        C = np.stack([proj_to_perp(r, Q_perp_tensor) for r in r_list], axis=0) # t_B x 70
        rk_C = np.linalg.matrix_rank(C, tol=1e-9)
        M_C = np.einsum("tq,mqa->mta", C, T_M).reshape(195, 6 * t_B)
        svals = np.linalg.svd(M_C, compute_uv=False)
        null = int(np.sum(svals < 1e-8))
        s1_out = 0
        c_out = 0
        if null > 0:
            _, _, Vt = np.linalg.svd(M_C, full_matrices=True)
            U_out = Vt[-null:, :].reshape(null, t_B, 6).transpose(2, 0, 1)
            s1_out = np.linalg.matrix_rank(np.tensordot(b_chk, U_out, axes=([0],[0])), tol=1e-7)
            c_out = np.linalg.matrix_rank(U_out.reshape(6 * null, t_B), tol=1e-7)
        print(f"  [{name:32s}] t_B={t_B}, rk_mod_S={rk_C}: null(M)={null}, s1(u_out)={s1_out}, c(u_out)={c_out}")

    # 1. Hilbert #55 (t_B=2)
    r1 = np.zeros((6, 15)); r1[0, sub2_idx[(1,5)]] = 1; r1[1, sub2_idx[(0,5)]] = -1
    r2 = np.zeros((6, 15)); r2[0, sub2_idx[(1,4)]] = 1; r2[1, sub2_idx[(0,4)]] = -1
    eval_M("Hilbert #55", [r1, r2])

    # 2. Pure protruding on single J=(4,5): b_0 e_{4,5}..b_3 e_{4,5}
    p_rows = []
    for i in range(4):
        r = np.zeros((6, 15)); r[i, sub2_idx[(4, 5)]] = 1
        p_rows.append(r)
    for t in [2, 3, 4]:
        eval_M(f"Pure protruding b_i e_45 (t={t})", p_rows[:t])

    # 3. Pure O_in protruding on single J=(0,1): b_0 e_{0,1}, b_1 e_{0,1}
    oi_rows = []
    for i in [0, 1]:
        r = np.zeros((6, 15)); r[i, sub2_idx[(0, 1)]] = 1
        oi_rows.append(r)
    eval_M("Pure O_in b_0,b_1 e_01 (t=2)", oi_rows)

    # 4. Edge-Koszul (Noether #58): b_4 e_{i,5} + b_5 e_{i,4} for i=0..3
    ek_rows = []
    for i in range(4):
        r = np.zeros((6, 15)); r[4, sub2_idx[(i, 5)]] = 1; r[5, sub2_idx[(i, 4)]] = 1
        ek_rows.append(r)
    for t in [2, 3, 4]:
        eval_M(f"Edge-Koszul Noether (t={t})", ek_rows[:t])

    # 5. Star-Koszul (Noether #65): b_0 e_{1,c} - b_1 e_{0,c} for c=2..5
    sk_rows = []
    for c in [2, 3, 4, 5]:
        r = np.zeros((6, 15)); r[0, sub2_idx[(1, c)]] = 1; r[1, sub2_idx[(0, c)]] = -1
        sk_rows.append(r)
    for t in [2, 3, 4]:
        eval_M(f"Star-Koszul Noether (t={t})", sk_rows[:t])

    # 6. Orbit-B protruding: b_4(e_{0,j}-e_{1,j}) + (b_0-b_1)e_{4,j} for j=2,3,5
    ob_rows = []
    for j in [2, 3, 5]:
        r = np.zeros((6, 15))
        r[4, sub2_idx[(0, j)]] = 1; r[4, sub2_idx[(1, j)]] = -1
        ej4 = tuple(sorted((4, j)))
        r[0, sub2_idx[ej4]] = 1; r[1, sub2_idx[ej4]] = -1
        ob_rows.append(r)
    eval_M("Orbit-B 3-pair (t=3)", ob_rows)

    # 7. Can we mix Pure Protruding (2 rows: b_0 e_01, b_1 e_01) + Hilbert #55 (2 rows)?
    eval_M("Mix: b_0,b_1 e_01 + Hilbert #55", oi_rows + [r1, r2])

    # 8. Wait: what about 2 different columns with 2 rows each? e.g. b_0,b_1 e_01 AND b_2,b_3 e_23?
    p2_rows = []
    for j_pair, vs in [((0,1), [0,1]), ((2,3), [2,3])]:
        for v in vs:
            r = np.zeros((6, 15)); r[v, sub2_idx[j_pair]] = 1
            p2_rows.append(r)
    eval_M("2 disjoint pure pairs (t=4)", p2_rows)

if __name__ == "__main__":
    B2_full, Q_perp_tensor, Q_perpE, T_M, sub_2, sub_3 = build_cokernel_proj()
    check_known_families(T_M, Q_perp_tensor, sub_2, sub_3)
