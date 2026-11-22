# Profesörler Konseyi: Tartışma Sentezi

**Tarih:** 2026-11-21 02:14 – 02:27 (konsey kota sınırına takılmadan önceki ~13 dakika)

## Konsey Bulguları (3 Mesaj, hepsi doğrulanmış)

### 1. Prof. Euler — Spektral Ayrışım Teoremi (Mesaj #8)
**Durum: KANITLANDI (doğrulanacak)**

Nisan matrisi $M = N_{01}(P_{\mathrm{perm}})$'nin tam spektrumu:
- **Üç adet $+2$ özdeğer**, **üç adet $-2$ özdeğer**, **on adet $0$**.
- Dolayısıyla $M^3 = 4M$ özdeşliği $\mathbb{Z}$ üzerinde tam olarak sağlanır.
- $\mathrm{Sym}_0(4)$, $S_4$ simetrik grubu altında 3 indirgenemez temsile ayrışır:
  - $\mathrm{Sym}_0(4) = \mathbf{1} \oplus \mathbf{(2,2)} \oplus \mathbf{(3,1)}$
  - $V_+ = \mathbf{1} \oplus \mathbf{(2,2)}$ (3-boyutlu, özdeğer $+2$): Eşleşme toplamları $X_k = (ij) + (\overline{ij})$.
  - $V_- = \mathbf{(3,1)}$ (3-boyutlu, özdeğer $-2$): Eşleşme farkları $Y_k = (ij) - (\overline{ij})$.

### 2. Prof. Noether — Temsil ve Tensör Simetrisi (Mesaj #10)
**Durum: KANITLANDI (doğrulanacak)**

- Kalıcı tensör $T_{j_0, c_1, j_3, c_2} = [\{j_0, c_1, j_3, c_2\} = \{0,1,2,3\}]$, **tamamen simetriktir** ($S_4$'ün 24 permütasyonu altında), $24 x_0 x_1 x_2 x_3$'ün tam polarizasyonudur.
- $\mathrm{Sym}_0(4)$ üzerinde $M$ tam köşegendir: $\mathrm{diag}(+2, +2, +2, -2, -2, -2)$.
- $a \leftrightarrow b$ simetrisi $(c_1 \leftrightarrow c_2)$'ye denk → problem öz-eşleniktir.
- **Case (3,2) izdüşüm denklemi:** $\mathrm{diag}(+2 I_3, -2 I_3) - (K_1 + K_2)|_{\mathrm{Sym}_0} = R_3|_{\mathrm{Sym}_0}$ ile $\mathrm{rank}(R_3|_{\mathrm{Sym}_0}) \le 3$.

### 3. Prof. Valiant — Kombinatorik Vaka Analizi (Mesaj #12)
**Durum: KANITLANDI (kısmi — $k_{\min} = 2$ rejimleri açık)**

Rank demetleri $(r_1, s_1, r_2, s_2)$ kısıtları:
- $r_1 + r_2 \le 5$, $s_1 + s_2 \le 5$, $\min(r_1, s_2) + \min(s_1, r_2) \ge 4$.

$5^4 = 625$ adaydan **31 tanesi** hayatta kalır, $\mathbb{Z}_2 \times \mathbb{Z}_2$ simetrisi altında **11 yörünge**:

| Rejim | Yörüngeler | Toplam | Durum |
|---|---|---|---|
| $k_{\min} = 0$ | Orbit 1 `(0,4,4,0)`, Orbit 2 `(0,4,4,1)` | 6 | **ELENDİ** ($A_1 B_2$ veya $B_1 A_2 \equiv 0 \implies \mathrm{rank}(N_{01}) \le 5 < 6$) |
| $k_{\min} = 1$ | Orbit 3–7 | 16 | **ELENDİ** (Westwick/Atkinson 1972: rank-1 kalem sabit sütun/satır uzayı verir → wire-split (1,4)'e indirgenip Lemma B ile çürütülür) |
| $k_{\min} = 2$ | Orbit 8–11 | 9 | **AÇIK** — Wire-split `(3,2)` dahil 4 yörünge |

### Açık Kalan $k_{\min} = 2$ Yörüngeleri
- Orbit 8: $(2, 2, 2, 2)$ [1 demet]
- Orbit 9: $(2, 2, 2, 3)$ [4 demet]
- Orbit 10: $(2, 2, 3, 3)$ [2 demet]
- Orbit 11: $(2, 3, 3, 2)$ [2 demet] ← wire-split `(3, 2)` ve `(2, 3)` burada

---

## Konseyin Yarım Kalan Araştırma Yönleri
1. **Cauchy Eylemsizlik / İmza Engeli:** $M|_{\mathrm{Sym}_0}$ imzası $(3, 3)$; $R_3|_{\mathrm{Sym}_0}$ rank $\le 3$ olduğunda $K_1 + K_2$'nin hem $V_+$ hem $V_-$ 3-boyutlu bloklarını kapsayıp kapsayamayacağı.
2. **$k_{\min} = 2$ rejimlerinin wire-split'e indirgenmesi veya doğrudan çürütülmesi.**
3. **$\mathbb{F}_3, \mathbb{F}_5$ üzerinde kapsamlı arama** (Prof. Euler başlamıştı ama tamamlayamadı).
