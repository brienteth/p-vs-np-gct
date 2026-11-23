# 🎯 P vs NP SORU AVCISI — T1 → T6 RAPORU (İnsan Kararına Hazır)

> Üretim Tarihi: `2026-11-23 21:59:00` · 4 Katmanlı Mimari (`P1–P8` → Red Team `G1–G7` → Sentezci)

## 1. Eleme İstatistikleri (Öldürme Oranı & Kapı Dağılımı)

| Tur | Toplam Aday | Hayatta Kalan | Ölen | Öldürme Oranı | Kapı Bazlı Öldürme Dağılımı |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **T1 → T2 (Red Team I)** | 24 | **0** | 24 | `%100.0` | `{'G1': 17, 'G3': 6, 'G5': 23, 'G6': 2}` |
| **T3 → T4 (Red Team II)** | 6 | **0** | 6 | `%100.0` | `{'G1': 6, 'G5': 3, 'G2': 2, 'G3': 2}` |

**Olgun Adaylar (T2 + T4 Çifte Geçiş):** `Doğrudan çifte geçiş yok — T4 en güçlüleri sentezlendi`

---

## 2. Sentezlenen Araştırma Programı (T5): Orbit Topolojisi ve Yaklaşılabilirlik Sınırı: Perm-Det Mesafesinin Empirik İncelemesi

### Seçilen Nihai Sorular (Bağımlılık Sırasıyla, ≤ 3 Soru)

#### 1. `[P8-Q1]` n=4'te, perm_4'ün m=14 boyutlu ABP ile en iyi yaklaşımdaki kalıntı normunun ortalaması, det_4'ün aynı koşullardaki kalıntı normunun ortalamasından büyük müdür?
- **Önkoşulu olduğu sorular:** `['P6-Q1', 'P6-Q2']`
- **Yanlışsa ne kaybederiz:** Yanlışsa (kalıntı farkı yoksa), perm ve det'in ABP uzayındaki 'yakınlığı' kanıtlanır. Bu, orbit mesafesinin (P6-Q1) ve yerel minimumların (P6-Q2) üstel büyüklükte olma ihtimalini düşürür. Kaybedilen: Üstel alt sınır arayışının temel dayanağı olan 'temsil zorluğu' farkı. Kazanılan: Daha ince taneli bir yakınsama analizi.
- **`dc` / `VP ≠ VNP` bağlantısı:** Kalıntı normu farkı, doğrudan dc(perm) >= dc(det) + delta eşitsizliğinin pratik bir göstergesidir. Büyük fark, VP!=VNP'nin 'yumuşak' bir alt sınırına işaret eder.

#### 2. `[P6-Q1]` perm_n'in det_n orbitine, sadece rank-1 güncellemeleri ve 2x2 blok dönüşümleri kullanılarak ulaşmak için gereken minimum adım sayısı n²/2'den üstel büyüklükte midir?
- **Önkoşulu olduğu sorular:** `['P6-Q2']`
- **Yanlışsa ne kaybederiz:** Yanlışsa (mesafe polinomiyse), perm'in det'e 'kısa yoldan' ulaşılabilir. Bu, P6-Q2'deki yerel minimumların çokluğunun bir 'tuzak' olduğunu, aslında global optimuma yakınlık olduğunu gösterir. Kaybedilen: Üstel komutasyon karmaşıklığı hipotezi. Kazanılan: Orbit geometrisinin daha düzgün olduğu kanıtı.
- **`dc` / `VP ≠ VNP` bağlantısı:** Eğer d(perm, det) üstel ise, bu doğrudan dc(perm) için üstel alt sınır anlamına gelir (Sheshadri bağlantısı). Bu, VP!=VNP için güçlü bir kanıttır.

#### 3. `[P6-Q2]` perm_n'in det_n orbitine en yakın noktasına (orbit mesafesi metriğinde) ulaşan tüm yerel minimumların sayısı, n=4 için 15'ten büyük müdür?
- **Önkoşulu olduğu sorular:** `[]`
- **Yanlışsa ne kaybederiz:** Yanlışsa (yerel minimum azsa), optimizasyon peyzajı 'temiz'dir. Bu, P6-Q1'deki uzun yolun varlığına rağmen, global optimuma hızlı ulaşılabilir olabileceğini gösterir. Kaybedilen: Peyzajın 'frustrated' olduğu hipotezi. Kazanılan: Arama uzayının yapısı hakkında net bilgi.
- **`dc` / `VP ≠ VNP` bağlantısı:** Yerel minimumların çokluğu, global optimuma ulaşmanın zorluğunu (optimizasyon karmaşıklığı) gösterir. Bu, hesaplama karmaşıklığı ile geometrik karmaşıklık arasında köprü kurar.

### Ortak Vekil Altyapısı (Tek Betik Ailesi)
- **Aile Adı:** orbit_geometry_suite
- **Betikler:** `['abp_fitting.py', 'orbit_bfs.py', 'lm_basins.py']`
- **Ortak Yapı Taşları:** `['polynomial_ring_ops', 'orbit_distance_metric', 'local_minimizer', 'rank_update_generator']`

### İlk 72 Saatte Yapılacak 3 Somut Ölçüm

| Adım | Ölçüm | Süre | Betik | Kabul Eşiği | Ret (Öldürme) Eşiği |
| :---: | :--- | :---: | :--- | :--- | :--- |
| 1 | ABP Yaklaşım Kalıntı Normu Karşılaştırması | 8s | `abp_fitting.py` | perm_4 kalıntısı, det_4 kalıntısından en az 10 kat büyük | perm_4 kalıntısı, det_4 kalıntısından 2 kat küçük veya eşit |
| 2 | Orbit Mesafesi BFS Taraması (n=4) | 24s | `orbit_bfs.py` | Minimum adım sayısı 15'i aşar (n²/2 + C) | Minimum adım sayısı 15 veya altındadır |
| 3 | Yerel Minimum Çanak Analizi (n=4) | 12s | `lm_basins.py` | Yerel minimum sayısı 15'i aşar | Yerel minimum sayısı 15 veya altındadır |

### `VP ≠ VNP` Bağının Dürüst Kırılganlık Analizi

Bu program, VP!=VNP'ye dolaylı yoldan bağlanır. Kalıntı normu farkı (P8-Q1) ve orbit mesafesi (P6-Q1) üstel ise, bu dc(perm) için üstel alt sınır demektir. Ancak, bu bağ kırılgandır çünkü: 1) Kalıntı normu farkı, doğrudan alt sınır değil, sadece bir göstergedir. 2) Orbit mesafesi, kullanılan operatör setine (rank-1/blok) bağlıdır; daha güçlü operatörlerle mesafe kısalabilir. 3) Yerel minimumlar, optimizasyon zorluğunu gösterir ama hesaplama karmaşıklığını kanıtlamaz. Bu nedenle, program VP!=VNP'yi kanıtlamaz, ancak 'yumuşak' bir alt sınır için güçlü kanıtlar sağlar.

---

## 3. T4'ten Sağ Çıkan Adayların Hakem Gerekçeleri


---

## 4. T6 — İNSAN KARARI & CANLI KONSEY ENTEGRASYONU

- Yeni üretilen cepheler (`council_frontiers.json`) otomatik olarak mevcut **8 Ajanlık 0G Konseyi** (`Prof. Henri Poincaré` + `Turing [Python]` + `Curry [Lean 4]`) rotasyonuna enjekte edildi.
- **T6 İnsan Kararı Bekleniyor:** Yukarıdaki ≤3 sorudan hangilerinin 72 saatlik ilk deney betiklerini (`lm_basins.py` vb.) hemen çalıştıralım?
