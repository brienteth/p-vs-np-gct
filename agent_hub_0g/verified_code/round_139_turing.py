import numpy as np
from itertools import combinations

def koszul_matrix(n, k):
    """
    n değişkenli polinom halkası R = k[x_1, ..., x_n] üzerindeki Koszul kompleksinin
    k. basamağındaki matrisini oluşturur.
    
    Koszul kompleksinin basamakları Λ^k(k^n) şeklindedir. Boyut: C(n, k).
    Matris boyutu: C(n, k) x C(n, k-1).
    Elemanlar ±1 şeklindedir (standart Koszul diferencialine göre).
    """
    dim_in = np.math.comb(n, k - 1)
    dim_out = np.math.comb(n, k)
    
    basis_in = list(combinations(range(n), k - 1))
    basis_out = list(combinations(range(n), k))
    
    mat = np.zeros((dim_out, dim_in), dtype=np.int8)
    
    for j, beta in enumerate(basis_in):
        for i, alpha in enumerate(basis_out):
            # d(e_beta) = sum_{x in beta} (-1)^{pos(x)} e_{beta \ {x}}
            # Burada alpha == beta \ {x} olmalı.
            # alpha seti beta setinden tek bir eleman çıkarılarak elde edildi mi?
            
            try:
                missing = tuple(sorted(set(beta) - set(alpha)))[0]
                pos = list(beta).index(missing)
                sign = (-1) ** pos
                mat[i, j] = sign
            except IndexError:
                pass
                
    return mat

def compute_homology_ranks(n):
    """
    n için Koszul kompleksinin homoloji rank'larını hesaplar.
    H^k = ker(d_k) / im(d_{k+1})
    rank(H^k) = nullity(d_k) - rank(d_{k+1})
    = (dim(domain) - rank(d_k)) - rank(d_{k+1})
    """
    ranks = []
    for k in range(n + 1):
        d_k = koszul_matrix(n, k)
        rk_dk = np.linalg.matrix_rank(d_k)
        
        dim_domain = np.math.comb(n, k)
        nullity_dk = dim_domain - rk_dk
        
        rank_Hk = nullity_dk - rk_dk_prev if k > 0 else nullity_dk # İlk basamak için im yok (0)
        # Düzeltme: H^0 = ker(d_0). d_0: R -> R. Genellikle d_0=0 alınır, H^0=R.
        # Standart Koszul kompleksinde d_0: Λ^0 -> Λ^{-1} tanımsızdır, genelde kompleks 0 basamağında biter.
        # H^0 = ker(d_1). rank(H^0) = dim(Λ^0) - rank(d_1) = 1 - rank(d_1).
        # Hesaplama şeması:
        # rk_k = rank(d_k)
        # rank(H^k) = nullity(d_k) - rk_{k+1}
        
        ranks.append(nullity_dk)
        rk_dk_prev = rk_dk
        
    # rank(H^k) hesaplamasını düzeltelim
    homology_ranks = []
    for k in range(n + 1):
        d_k = koszul_matrix(n, k)
        rk_dk = np.linalg.matrix_rank(d_k)
        dim_in = np.math.comb(n, k)
        nullity_dk = dim_in - rk_dk
        
        if k < n:
            d_next = koszul_matrix(n, k + 1)
            rk_next = np.linalg.matrix_rank(d_next)
            hk = nullity_dk - rk_next
        else:
            hk = nullity_dk
            
        homology_ranks.append(hk)
        
    return homology_ranks

# Veri toplama
data_n = [4, 5, 6, 7]
diffs = []

print("n \t rank(H^1) \t rank(H^0) \t diff \t log(n)")
for n in data_n:
    ranks = compute_homology_ranks(n)
    rk_h1 = ranks[1]
    rk_h0 = ranks[0]
    diff = rk_h1 - rk_h0
    diffs.append(diff)
    print(f"{n} \t {rk_h1} \t\t {rk_h0} \t\t {diff} \t {np.log(n)}")

diffs = np.array(diffs)
X = np.array([np.log(n) for n in data_n]).reshape(-1, 1)

# Polyfit: log(diff) ~ alpha * log(n) + C
# log(diff) = alpha * log(n) + C => diff = C * n^alpha
Y = np.log(diffs).reshape(-1, 1)

coeffs = np.polyfit(X.flatten(), Y.flatten(), 1)
alpha = coeffs[0]

print(f"\nFit sonucu: log(diff) = {alpha:.4f} * log(n) + {coeffs[1]:.4f}")
print(f"Tahmini α (üst): {alpha:.4f}")

# Assertions
# α > 1.5
assert alpha > 1.5, f"α = {alpha} <= 1.5. Hipotez çürütüldü."

# rank_diff(7) > 100
assert diffs[-1] > 100, f"rank_diff(7) = {diffs[-1]} <= 100. Hipotez çürütüldü."

print("\nPASS: Hipotezler başarılı.")
