import numpy as np
import json

def build_laurent_matrix(n, w1, w2):
    """
    n=5 için Laurent matrisini oluşturur.
    Basitleştirilmiş model: Ağırlıklar kullanılarak belirlenen simetrik yapı.
    """
    M = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            # Basit bir simetrik Laurent yapılandırması: w1 + w2 * abs(i-j)
            M[i, j] = w1 + w2 * abs(i - j)
    return M

def analyze_matrix(M, rank_assertion=True, svd_thresh=0.12):
    singular_values = np.linalg.svd(M, compute_uv=False)
    min_sigma = np.min(singular_values)
    rank = np.sum(singular_values > 1e-10)
    
    return {
        "singular_values": singular_values.tolist(),
        "min_sigma": float(min_sigma),
        "rank": int(rank),
        "svd_pass": min_sigma >= svd_thresh,
        "rank_pass": rank >= 5
    }

results = {}
configs = [
    {"w1": 6, "w2": 8, "m": 29},
    {"w1": 6, "w2": 9, "m": 30}
]

for cfg in configs:
    M = build_laurent_matrix(5, cfg["w1"], cfg["w2"])
    stats = analyze_matrix(M)
    key = f"w2={cfg['w2']}_m={cfg['m']}"
    results[key] = stats
    
    # Assertions
    assert stats["svd_pass"], f"σ_min < 0.12: {stats['min_sigma']}"
    assert stats["rank_pass"], f"Rank < 5: {stats['rank']}"

print(json.dumps(results, indent=2))
print("PASS: Tüm assertions başarılı.")
