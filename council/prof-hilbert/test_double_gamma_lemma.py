"""Test the rank of (Gamma x I_4)(M - K(B, V))(Gamma_tilde x I_4)
and analyze Koszul cores (A1_bar, A2_bar) on W_A of dimension m_A <= 5.
"""
import numpy as np
import sys

sys.path.insert(0, "/Users/bl10buer/Desktop/matemk/p-vs-np-gct")
from apolar_higher_betti_probe import rank_matrix_mod
from perm4_abp_frontier import MOD

def build_M():
    M = np.zeros((16, 16), dtype=np.int64)
    for j0 in range(4):
        for c1 in range(4):
            for j3 in range(4):
                for c2 in range(4):
                    if len({j0, c1, j3, c2}) == 4:
                        M[j0*4 + c1, j3*4 + c2] = 1
    return M

def build_K(B, V, mod=MOD):
    K = np.zeros((16, 16), dtype=np.int64)
    for j0 in range(4):
        for c1 in range(4):
            for j3 in range(4):
                for c2 in range(4):
                    K[j0*4 + c1, j3*4 + c2] = (int(B[j0, c2]) * int(V[j3, c1])) % mod
    return K

def main():
    M = build_M()
    rng = np.random.default_rng(42)
    min_rk = 16
    for trial in range(500):
        # Random rank-3 Gamma (3x4) and Gamma_tilde (4x3)
        Gamma = rng.integers(0, MOD, size=(3, 4), dtype=np.int64)
        Gamma_tilde = rng.integers(0, MOD, size=(4, 3), dtype=np.int64)
        if rank_matrix_mod(Gamma, MOD) < 3 or rank_matrix_mod(Gamma_tilde, MOD) < 3:
            continue
        G_left = np.kron(Gamma, np.eye(4, dtype=np.int64)) % MOD
        G_right = np.kron(Gamma_tilde, np.eye(4, dtype=np.int64)) % MOD
        
        for rB in [1, 2, 3, 4]:
            for rV in [1, 2, 3, 4]:
                B = (rng.integers(0, MOD, size=(4, rB)) @ rng.integers(0, MOD, size=(rB, 4))) % MOD
                V = (rng.integers(0, MOD, size=(4, rV)) @ rng.integers(0, MOD, size=(rV, 4))) % MOD
                K = build_K(B, V, MOD)
                diff = (M - K) % MOD
                proj = (G_left @ diff % MOD) @ G_right % MOD
                rk = rank_matrix_mod(proj, MOD)
                if rk < min_rk:
                    min_rk = rk
    print(f"Minimum observed rank of (Gamma x I)(M - K)(Gamma_tilde x I) across 8000 trials: {min_rk}")

    # Also test structured / coordinate Gammas and aligned B, V
    min_struct = 16
    for i in range(4):
        Gamma = np.delete(np.eye(4, dtype=np.int64), i, axis=0)
        for j in range(4):
            Gamma_tilde = np.delete(np.eye(4, dtype=np.int64), j, axis=1)
            G_left = np.kron(Gamma, np.eye(4, dtype=np.int64)) % MOD
            G_right = np.kron(Gamma_tilde, np.eye(4, dtype=np.int64)) % MOD
            # Test rank-1 B, V aligned with coordinate rows/cols
            for b_row in range(4):
                for v_row in range(4):
                    B = np.zeros((4, 4), dtype=np.int64)
                    V = np.zeros((4, 4), dtype=np.int64)
                    B[b_row, :] = rng.integers(1, MOD, size=4)
                    V[v_row, :] = rng.integers(1, MOD, size=4)
                    K = build_K(B, V, MOD)
                    proj = (G_left @ ((M - K) % MOD) % MOD) @ G_right % MOD
                    rk = rank_matrix_mod(proj, MOD)
                    if rk < min_struct:
                        min_struct = rk
    print(f"Minimum observed structured rank of (Gamma x I)(M - K)(Gamma_tilde x I): {min_struct}")

if __name__ == "__main__":
    main()
