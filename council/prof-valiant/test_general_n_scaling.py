"""Verify the General n = 2k Kernel Expansion and Rank Confinement Theorem."""
import math

def analyze_scaling():
    print(f"{'n':<4}{'k':<4}{'m_n':<8}{'w_n':<8}{'d*':<6}{'2(m_n - d* + 1)':<18}{'w_n':<8}{'Gap':<6}")
    print("-" * 65)
    for n in range(4, 16, 2):
        k = n // 2
        m_n = math.comb(n, k - 1)
        w_n = math.comb(n, k) - 1
        d_star = math.ceil(m_n / n)
        min_sum = 2 * (m_n - d_star + 1)
        gap = min_sum - w_n
        print(f"{n:<4}{k:<4}{m_n:<8}{w_n:<8}{d_star:<6}{min_sum:<18}{w_n:<8}{gap:<6}")

if __name__ == "__main__":
    analyze_scaling()
