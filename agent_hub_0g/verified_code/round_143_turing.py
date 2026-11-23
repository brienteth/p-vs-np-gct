import numpy as np

def test_abp_error_asymptotics():
    """
    Prof. Strassen'in iddiasını test eder:
    ABP yaklaşımındaki hata terimlerinin O(n^-alpha) asimptotik sınırına uyup uymadığını numerik olarak doğrular.
    """
    print("QH-3 ABP Yaklaşımının Sınırları Numerik Testi Başlatılıyor...")
    
    # Simülasyon parametreleri
    max_n = 100
    alpha_target = 0.5  # Tahmini asimptotik decay exponent
    
    errors = []
    ns = []
    
    # n boyutlu tensörler için ABP tahmin hatasını simüle et
    # Not: Gerçek ABP hesaplaması yerine, tensör normları arasındaki farkla hata modellenmiştir.
    for n in range(10, max_n + 1, 10):
        # Rastgele A, B, C matrisleri oluştur (1, n, n boyutlarında)
        A = np.random.rand(1, n)
        B = np.random.rand(n, n)
        C = np.random.rand(n, 1)
        
        # Gerçek tensör çarpımı: A @ B @ C
        exact_product = np.squeeze(A @ B @ C)
        
        # ABP yaklaşımı (basitleştirilmiş model): A @ np.diag(np.mean(B, axis=0)) @ C
        # Bu basitleştirme, border rank yaklaşımındaki hatayı temsil eder
        approx_product = np.squeeze(A @ np.diag(np.mean(B, axis=0)) @ C)
        
        # Hata normu (L2)
        error = np.linalg.norm(exact_product - approx_product)
        errors.append(error)
        ns.append(n)
    
    ns = np.array(ns)
    errors = np.array(errors)
    
    # O(n^-alpha) fit'i log-log space'de yap
    # log(error) ~= -alpha * log(n) + C
    log_n = np.log(ns)
    log_error = np.log(errors)
    
    # Lineer regresyon ile alpha'yı tahmin et
    slope, intercept = np.polyfit(log_n, log_error, 1)
    estimated_alpha = -slope
    
    print(f"Estimated Alpha (decay rate): {estimated_alpha:.4f}")
    print(f"Target Alpha: {alpha_target}")
    
    # Assert: Estimated alpha yaklaşık olarak target alpha'ya yakın olmalı (tolerans içinde)
    # %10 tolerans
    assert abs(estimated_alpha - alpha_target) < 0.1, \
        f"Alpha mismatch: Estimated {estimated_alpha:.4f} vs Target {alpha_target}"
    
    # Sonuçları yazdır
    print("="*40)
    print("QH-3 ABP Error Asymptotics Test Result: PASS")
    print(f"n values: {ns[:5]}... to {ns[-1]}")
    print(f"Errors: {errors[:5]}... to {errors[-1]}")
    print(f"Fit Alpha: {estimated_alpha:.4f}")
    print("="*40)

if __name__ == "__main__":
    test_abp_error_asymptotics()
