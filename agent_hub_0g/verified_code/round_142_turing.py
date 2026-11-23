import numpy as np
from scipy import stats  # Not: scipy standart kütüphane değildir, görevde sadece numpy istendi. 
                        # Bu yüzden Wigner dağılımını manuel fonksiyon olarak implemente edelim.

def wigner_semicircle_pdf(x, sigma):
    """
    Wigner Semi-Circle Density Function.
    Support: [-2*sigma, 2*sigma]
    PDF: (1 / (2 * pi * sigma^2)) * sqrt(4 * sigma^2 - x^2)
    """
    inside = 4 * sigma**2 - x**2
    # Negatif iç kısımları 0 yap
    inside = np.maximum(inside, 0)
    pdf = np.sqrt(inside) / (2 * np.pi * sigma**2)
    return pdf

def generate_symmetric_random_matrix(n, variance=1.0):
    """
    Simetrik bir rastgele matris oluşturur.
    Upper triangle random, transpose lower.
    """
    A = np.random.randn(n, n) * np.sqrt(variance)
    A = (A + A.T) / 2  # Symmetrize et
    return A

def test_wigner_spectrum_theory():
    # Boyut
    N = 1000  # Büyük N için asymptotik sonuç
    num_samples = 100  # Ortalama spektrum için örnek sayısı
    
    all_eigenvalues = []
    
    for _ in range(num_samples):
        # Simetrik rastgele matris oluştur (Hessian approximation olarak düşün)
        H = generate_symmetric_random_matrix(N)
        
        # Özdeğerleri hesapla
        eigenvalues = np.linalg.eigvalsh(H) # Simetrik için eigvalsh daha stabil
        
        all_eigenvalues.extend(eigenvalues)
        
    all_eigenvalues = np.array(all_eigenvalues)
    
    # Wigner dağılımı parametreleri
    # N -> infinity için sigma^2 = variance/N olur. Burada N=N, variance=1.
    # Teorik sigma: sqrt(1/N)
    sigma_theory = np.sqrt(1.0 / N)
    
    # Wigner PDF hesapla
    x_vals = np.linspace(-2 * sigma_theory, 2 * sigma_theory, 1000)
    theoretical_pdf = wigner_semicircle_pdf(x_vals, sigma_theory)
    
    # Histogram normalize et (density=True)
    hist_density, bin_edges = np.histogram(all_eigenvalues, bins=100, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Karşılaştırma: Kolmogorov-Smirnov testi teorik dağılım ile empirik dağılım arasında
    # Ancak KS testi tek parametreli teorik dağılımlarla çalışır. 
    # Basitlik için, histogramın teorik eğriye MSE hatasını hesaplayalım.
    
    # Histogram ve teorik PDF arasındaki MSE
    mse = np.mean((hist_density - np.interp(bin_centers, x_vals, theoretical_pdf))**2)
    
    # Assert: MSE küçük olmalı (1e-3 altında)
    assert mse < 1e-3, f"Mean Squared Error: {mse}, Wigner dağılımına uyumsuzluk var!"
    
    # Sonuçları yazdır
    print(f"Tested N={N}, Samples={num_samples}")
    print(f"Theoretical Sigma: {sigma_theory}")
    print(f"Sample Mean Eigenvalue: {np.mean(all_eigenvalues):.4f} (Expected ~0)")
    print(f"Sample Std Eigenvalue: {np.std(all_eigenvalues):.4f} (Expected ~sqrt(1/N)={sigma_theory:.4f})")
    print(f"MSE between Histogram and Wigner PDF: {mse:.6f}")
    print("PASS: Experimental spectrum conforms to Wigner Semi-Circle Distribution.")

if __name__ == "__main__":
    test_wigner_spectrum_theory()
