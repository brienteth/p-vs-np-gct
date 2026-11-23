import numpy as np
import scipy.linalg as la

# Hedef: perm5 ve det5 fonksiyonlarının Hessian spektral aralıklarını karşılaştırmak.
# Hessian matrisleri n=5 için 5x5 olacak, özdeğer hesaplaması O(n^3) olduğu için hızlıdır.
# 100 rastgele nokta kullanacağız.

def compute_hessian_spectrum(f, x0, h=1e-5):
    """
    Belirli bir fonksiyon f ve başlangıç noktası x0 için Hessian matrisini numerik olarak hesaplar.
    Central difference yöntemi kullanır.
    """
    n = len(x0)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            x_pp = x0 + h * np.eye(n)[i] + h * np.eye(n)[j]
            x_pm = x0 + h * np.eye(n)[i] - h * np.eye(n)[j]
            x_mp = x0 - h * np.eye(n)[i] + h * np.eye(n)[j]
            x_mm = x0 - h * np.eye(n)[i] - h * np.eye(n)[j]
            
            val_pp = f(x_pp)
            val_pm = f(x_pm)
            val_mp = f(x_mp)
            val_mm = f(x_mm)
            
            H[i, j] = (val_pp - val_pm - val_mp + val_mm) / (4 * h * h)
            H[j, i] = H[i, j] # Simetri
    return H

def permanent5(x):
    """
    5x5 matrisin permanantını hesaplar.
    np.linalg.det determinant hesaplar, permanent için scipy veya özel kod gerekir.
    numpy'da built-in permanent yok, basit bir brute-force veya scipy kullanabiliriz.
    Ancak scipy.linalg.perm? Hayır, scipy'de permanent doğrudan yok.
    Alternatif: small n için basit permütasyon toplamı.
    """
    from itertools import permutations
    n = len(x)
    mat = x.reshape(n, n)
    total = 0
    for p in permutations(range(n)):
        prod = 1
        for i in range(n):
            prod *= mat[i, p[i]]
        total += prod
    return total

def determinant5(x):
    """
    5x5 matrisin determinantını hesaplar.
    """
    mat = x.reshape(5, 5)
    return np.linalg.det(mat)

# Test noktası sayısı
N_SAMPLES = 100

print("100 rastgele nokta için perm5 ve det5 Hessian spektrumları hesaplanıyor...")

# Spektral aralık listeleri
perm_spectrum_widths = []
det_spectrum_widths = []

for _ in range(N_SAMPLES):
    # Rastgele reel matris oluştur (5x5)
    x = np.random.randn(25)
    
    # Perm Hessian
    try:
        H_perm = compute_hessian_spectrum(permanent5, x)
        eig_perm = np.linalg.eigvalsh(H_perm) # Simetrik olduğu için eigvalsh daha stabil
        lambda_max_perm = np.max(eig_perm)
        lambda_min_perm = np.min(eig_perm)
        delta_lambda_perm = lambda_max_perm - lambda_min_perm
        perm_spectrum_widths.append(delta_lambda_perm)
    except Exception as e:
        print(f"Perm error at sample {_}: {e}")
        continue

    # Det Hessian
    try:
        H_det = compute_hessian_spectrum(determinant5, x)
        eig_det = np.linalg.eigvalsh(H_det)
        lambda_max_det = np.max(eig_det)
        lambda_min_det = np.min(eig_det)
        delta_lambda_det = lambda_max_det - lambda_min_det
        det_spectrum_widths.append(delta_lambda_det)
    except Exception as e:
        print(f"Det error at sample {_}: {e}")
        continue

assert len(perm_spectrum_widths) == N_SAMPLES, "Not all samples successful for perm"
assert len(det_spectrum_widths) == N_SAMPLES, "Not all samples successful for det"

# Maksimum farkları bul (iddia: aradaki fark polinom zamanda ayırt edilemez, yani >= 2.5)
# Aslında istenen assert: abs(np.max(eig_perm) - np.max(eig_det)) >= 2.5
# Burada np.max(eig_perm) ve np.max(eig_det) tek bir nokta için mi yoksa dağılım için mi?
# Metin: "Her fonksiyon için spektral aralığı Δλ = λ_max - λ_min olarak tanımla."
# Sonra: "assert abs(np.max(eig_perm) - np.max(eig_det)) >= 2.5"
# Bu ifade biraz belirsiz. Genellikle spektral yarıçap veya max özdeğer farkı kastedilir.
# Kodda np.max(eig_perm) tek bir Hessian'ın max özdeğeri. 100 nokta var.
# En büyük max özdeğer farkını kontrol edelim.

max_eig_perm = max(np.max(np.linalg.eigvalsh(compute_hessian_spectrum(permanent5, np.random.randn(25)))) for _ in range(100)) # Hafif hata: yukarıda hesapladık.
# Yukarıdaki döngüde depolamadık, tekrar hesaplamak yerine listeleri kullanalım.
# Liste zaten var.

# En büyük λ_max perm
max_lambda_max_perm = max(np.max(np.linalg.eigvalsh(compute_hessian_spectrum(permanent5, np.random.randn(25)))) for _ in range(100)) # Yeniden hesaplamamak için mevcut veriyi kullanmalıyız.
# Mevcut veri: perm_spectrum_widths sadece aralık. λ_max değil.
# O yüzden fonksiyonu çağırıp λ_max'ları da depolayalım.

perm_max_eigs = []
det_max_eigs = []
perm_min_eigs = []
det_min_eigs = []

for _ in range(N_SAMPLES):
    x = np.random.randn(25)
    
    H_perm = compute_hessian_spectrum(permanent5, x)
    eig_perm = np.linalg.eigvalsh(H_perm)
    perm_max_eigs.append(np.max(eig_perm))
    perm_min_eigs.append(np.min(eig_perm))
    
    H_det = compute_hessian_spectrum(determinant5, x)
    eig_det = np.linalg.eigvalsh(H_det)
    det_max_eigs.append(np.max(eig_det))
    det_min_eigs.append(np.min(eig_det))

max_perm = np.max(perm_max_eigs)
max_det = np.max(det_max_eigs)

diff = abs(max_perm - max_det)

print(f"Perm5 Max Eigenvalue (max sample): {max_perm}")
print(f"Det5 Max Eigenvalue (max sample): {max_det}")
print(f"Abs Difference: {diff}")

# İddia: abs(np.max(eig_perm) - np.max(eig_det)) >= 2.5
# Bu assert'in PASS olması için farkın 2.5'ten büyük olması gerekir.
# Permanant ve Determinant fonksiyonları birbirinden çok farklı davranır.
# Permanant genellikle daha büyük özdeğerlere sahip olabilir.

assert diff >= 2.5, f"Diff {diff} is less than 2.5. Assertion failed."

print("PASS: Difference is significant.")
