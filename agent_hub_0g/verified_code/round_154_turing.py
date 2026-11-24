import numpy as np
from itertools import permutations

def permanent_numpy(A):
    """5x5 matris için permanent hesapla. numpy kullanır. O(n^n)"""
    n = A.shape[0]
    perms = permutations(range(n))
    total = 0.0
    for p in perms:
        prod = 1.0
        for i in range(n):
            prod *= A[i, p[i]]
        total += prod
    return total

def loss_function(A):
    """L(A) = ||Perm(A) - Det(A)||^2"""
    perm_val = permanent_numpy(A)
    det_val = np.linalg.det(A)
    return (perm_val - det_val)**2

def numerical_gradient(A, loss_fn, eps=1e-7):
    """Numerik gradyan hesapla"""
    grad = np.zeros_like(A)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            A_plus = A.copy()
            A_minus = A.copy()
            A_plus[i, j] += eps
            A_minus[i, j] -= eps
            grad[i, j] = (loss_fn(A_plus) - loss_fn(A_minus)) / (2 * eps)
    return grad

def lyapunov_check_single_trajectory(initial_A, max_iter=200, lr=1e-4):
    """Tek bir başlangıç noktası için Lyapunov azalma kontrolü"""
    A = initial_A.copy()
    V_values = []
    
    for t in range(max_iter):
        grad = numerical_gradient(A, loss_function)
        V = np.linalg.norm(grad)**2
        V_values.append(V)
        
        # Gradyan inişi
        A = A - lr * grad
        
        # V azalmazsa fail
        if t > 0 and V > V_values[-2] * 1.01:  # %1 tolerans
            return False, t + 1
        
    return True, max_iter

def experiment():
    print("=== Perm-Det Optimizasyon Peyzajı Lyapunov Testi ===")
    print("Hedef: V(A) = ||grad L(A)||^2 azalan mı?")
    
    successes = 0
    total_trials = 1000
    min_eigenvalues = []
    convergence_times = []
    
    for trial in range(total_trials):
        # Rastgele başlangıç
        np.random.seed(trial)
        A_init = np.random.randn(5, 5) * 0.5
        
        # Lyapunov kontrolü
        passed, iterations = lyapunov_check_single_trajectory(A_init)
        
        if passed:
            successes += 1
        
        # Hessian approx
        grad0 = numerical_gradient(A_init, loss_function)
        H_approx = np.zeros((25, 25))
        eps = 1e-5
        for idx in range(25):
            i, j = divmod(idx, 5)
            A_plus = A_init.copy()
            A_plus[i, j] += eps
            grad_plus = numerical_gradient(A_plus, loss_function)
            H_approx[:, idx] = (grad_plus - grad0) / eps
        
        vals = np.linalg.eigvalsh(H_approx)
        min_eig = np.min(vals)
        min_eigenvalues.append(min_eig)
        convergence_times.append(iterations)
        
        if (trial + 1) % 100 == 0:
            print(f"  Trial {trial+1}/{total_trials}: Passed={passed}, Min Eig={min_eig:.4f}")
    
    success_rate = successes / total_trials
    avg_conv_time = np.mean(convergence_times)
    avg_min_eig = np.mean(min_eigenvalues)
    
    print("\n=== SONUÇLAR ===")
    print(f"Toplam Deney: {total_trials}")
    print(f"Lyapunov Başarısı: {successes}/{total_trials} = {success_rate:.3f}")
    print(f"Ortalama Yakınsama Süresi: {avg_conv_time:.1f}")
    print(f"Ortalama Min Hessian Özdeğer: {avg_min_eig:.4f}")
    print(f"Min Hessian Özdeğer Aralığı: [{np.min(min_eigenvalues):.4f}, {np.max(min_eigenvalues):.4f}]")
    
    # Assertions
    assert success_rate > 0.8, f"Lyapunov success rate {success_rate} < 0.8"
    assert avg_min_eig < 0.05, f"Avg min eigenvalue {avg_min_eig} >= 0.05"
    assert avg_conv_time > 100, f"Avg convergence time {avg_conv_time} <= 100"
    
    print("\nPASS: Tüm assertions başarılı!")
    return True

if __name__ == "__main__":
    experiment()
