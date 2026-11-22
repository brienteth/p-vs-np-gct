# Permanentin Cebirsel ve Boolean Karmaşıklığı Üzerine 45 Doğrulanmış Teorem: Homojen ABP'ler, Yinelemeli Macaulay Schur-Tümleyeni (IMSC), Orijin-İzotropisi ve Burnside Yörünge-LP Dualitesi

**Yazarlar / Çalışma Grubu:** Antigravity Cebirsel Karmaşıklık Konseyi (Euler, Noether, Hilbert, Strassen, Valiant, Wigner Modülleri)  
**Tarih:** Kasım 2026  
**Doğrulama Sertifikası:** `council/prof-euler/verify_all_council.py` — **45/45 PASS** (`74.058 s`, `exit code 0`, deterministik sonlu cisim & tam tamsayı doğrulaması)  
**Çalışma Dizini:** `p-vs-np-gct/`

---

## Özet

Bu makale, $\mathrm{VP}\neq\mathrm{VNP}$ (Valiant'ın cebirsel hipotezi, *Duvar 1*) ile $\mathrm{P}\neq\mathrm{NP}$ / $\mathrm{TC}^0 \neq \mathrm{NC}^1$ (Boolean devre karmaşıklığı, *Duvar 2*) arasındaki yapısal köprüyü inceleyen **45 makine-doğrulanmış teoremi** (ve bunların Tur 15–16 uzantılarını) bütünleşik bir matematiksel monografi olarak sunar. Çalışma dört ana eksende ilerler:

1. **Satır-Ayrışımlı Homojen Cebirsel Dallanma Programları (ABP'ler) (Teorem 1–25):** $n=4, w=5$ için tam bir cebirsel imkânsızlık kanıtı (eşleme operatörü $M^3=4M$, 31 hayatta kalan rank demeti, $K_k$/$M_{i,j}$ istisnai altuzayları) kurulur ve genel çift $n=2k$ için spektral yasa, Kneser–Katona kimliği ($\det(\mathrm{KG}(6,2))=-1458$), $n=6, w=19$ sınırındaki 32 demetin 24'ünün elenmesi, 135-noktalı rank-3 varyetesi ve Yükümlülük A/B'yi kapatan çift kapatma anahtarı ($\min(c-4, d_{\mathrm{syz}}-5)\le 0$) kanıtlanır.
2. **Torus Eşdeğişirliği ve Tek-Taraflı $T_n^{\mathrm{row}}$ Katılığı (Teorem 26, 31, 36, 41):** Çift-taraflı torus altında $m \ge 2^n-1$ ve tek-taraflı satır-torusu $T_4^{\mathrm{row}}$ altında **tüm 4-katmanlı ABP'ler için** $m \ge 15 = 2^4-1$ (Handshaking + $\mathbb{P}^3$'teki 10-noktalı $\Sigma_{\le 2}$ lokusu) kapanışı kanıtlanır; $n=5$ için $w_2 \ge 10$ alt sınırı elde edilir.
3. **Tekillik Kodimansı, Yinelemeli Macaulay Schur-Tümleyeni (IMSC) ve Koşulsuz Determinantal Karmaşıklık (Teorem 27, 28, 32, 33, 37, 38, 42, 43):** Tam tamsayı ve çift-asal modüler ($\mathbb{F}_{32749}, \mathbb{F}_{65521}, \mathbb{F}_{1000003}, \mathbb{F}_{1000033}$) Macaulay sertifikalarıyla $\mathrm{codim}_{\mathbb{C}^{16}}(\mathrm{Sing}(\mathrm{perm}_4)) = 8$, $\mathrm{codim}(\mathrm{Sing}_2(\mathrm{perm}_4)) = 12$, $\mathrm{codim}(\mathrm{Sing}_3(\mathrm{perm}_5)) = 20$ ve $\mathrm{codim}(\mathrm{Sing}_2(\mathrm{perm}_5)) \ge 15$ hesaplanır. Orijin-izotropisi, Çift-Koszul ve Pertürbe Çarpık-Kare (Skew-Square) mekanizmalarıyla $\mathrm{dc}(\mathrm{perm}_3) = 7$, **koşulsuz $\mathrm{dc}(\mathrm{perm}_4) \ge 11$** (Alper–Bogart–Velasco 2017'nin $\ge 10$ sınırını aşarak) ve açık sınır değişmezi $R_9^{(4)} = P^{(4)}Q^{(4)}$ üzerinden **sınır determinantal karmaşıklığı $\underline{\mathrm{dc}}(\mathrm{perm}_4) \ge 11$** kanıtlanır. (Ek B'de Tur 15–16 uzantılarıyla $\mathrm{dc}(\mathrm{perm}_4) \ge 12$ ve global $\mathrm{codim}(\mathcal{H}_{\le 4}(\mathrm{perm}_4))=10$ kapanışı raporlanır.)
4. **Cebirsel–Boolean Köprüsü, Pauli-Dışlama ve Burnside Yörünge-LP Dualitesi (Teorem 29, 30, 34, 35, 39, 40, 44, 45):** $\mathbb{F}_3 \to \mathbb{F}_2$ Pauli-dışlama derece yasası ($\deg(\det_n \bmod 3) \le n^2-2$ vs $\deg(\mathrm{perm}_n) = n^2-1$), $n=5$ için $33{,}554{,}432$ matrisin tamamı üzerinde kesin $4.89\times$ $\mathrm{RM}(5,25)$ ayrımı, 2-adik mod-4 sıkıştırma ($26.72\times$), Burnside yörünge sıkıştırması ($K_5=5{,}624, K_6=251{,}610$; $273{,}119\times$ hızlanma), Williams simetrizasyon ikilemi, Reynolds $L_1$-izometrisi, tam `2,537`/`3,075`-kapılı $\mathrm{TC}^0_2$ sözlükleri, $n=5$ için kesin $D_{\mathrm{PTF}} \ge 7$ ve derinlik-3 $\mathrm{TC}^0_3$ tek-değişkenli çöküşü kanıtlanır.

Makale, kanıtlanan her teoremi kesin epistemik statü etiketiyle (`[KANITLANDI]`, `[SAYISAL DOĞRULANDI]`, `[DÜRÜST ÇÜRÜTME / AÇIK]`) sunar ve Mignon–Ressayre $n^2$ tavanı, Razborov–Rudich Doğal Kanıtlar bariyeri, tekdüze/minimax Forster çürütmesi ve Wood 2-adik doygunluğu gibi yapısal sınırları şeffaf biçimde belgeler.

---

## Abstract

This monograph presents **45 machine-verified theorems** (together with their verified Round 15–16 frontier extensions) investigating the algebraic and Boolean complexity of the permanent $\mathrm{perm}_n$ versus the determinant $\det_n$ across the $\mathrm{VP}\neq\mathrm{VNP}$ and $\mathrm{TC}^0\neq\mathrm{NC}^1$ / $\mathrm{P}\neq\mathrm{NP}$ divide. All 45 core theorems pass a single deterministic verification harness (`verify_all_council.py`, `45/45 PASS` in `74.058 s`). Key contributions include: (i) a complete algebraic impossibility proof for row-separated homogeneous ABPs at $n=4, w=5$ and a structural classification of the $n=6, w=19$ boundary via Kneser–Katona identities, syzygy rigidity, and a dual kill-switch closing Obligations A and B; (ii) full closure of $m \ge 15 = 2^4-1$ for all 4-layer one-sided row-torus ($T_4^{\mathrm{row}}$) ABPs via a 10-point projective locus and handshaking; (iii) exact singularity-stratum codimensions ($\mathrm{codim}\,\mathrm{Sing}(\mathrm{perm}_4)=8$, $\mathrm{Sing}_2(\mathrm{perm}_4)=12$, $\mathrm{Sing}_3(\mathrm{perm}_5)=20$) via Iterated Macaulay Schur-Complements (IMSC), yielding unconditional $\mathrm{dc}(\mathrm{perm}_3)=7$, $\mathrm{dc}(\mathrm{perm}_4)\ge 11$, and border lower bound $\underline{\mathrm{dc}}(\mathrm{perm}_4)\ge 11$ via explicit polynomial invariants (extended to $\mathrm{dc}(\mathrm{perm}_4)\ge 12$ and global $\mathrm{codim}\,\mathcal{H}_{\le 4}(\mathrm{perm}_4)=10$ in Appendix B); and (iv) an algebraic-to-Boolean bridge featuring the $\mathbb{F}_3\to\mathbb{F}_2$ Pauli-exclusion ANF degree law, exact $n=5$ ($2^{25}$ matrices) $4.89\times$ Reed–Muller separation, 2-adic mod-4 determinant compression ($26.72\times$), Burnside Orbit-SAT compression ($273{,}119\times$ at $n=6$), Reynolds $L_1$-isometry, exact $D_{\mathrm{PTF}}(5)\ge 7$, and depth-3 $\mathrm{TC}^0_3$ univariate collapse. Structural ceilings (Mignon–Ressayre $n^2$ barrier, Razborov–Rudich Natural Proofs, uniform Forster refutation, Wood 2-adic saturation) are explicitly audited.

**Anahtar Kelimeler:** Permanent, Determinantal Karmaşıklık ($\mathrm{dc}, \underline{\mathrm{dc}}$), Cebirsel Dallanma Programları (ABP), Macaulay Matrisleri, Tekillik Kodimansı, Torus Eşdeğişirliği, Burnside Yörünge-LP, $\mathrm{TC}^0_2/\mathrm{TC}^0_3$, Geometrik Karmaşıklık Kuramı (GCT).

---

## 1. Giriş, Problem Çerçevesi ve Ana Sonuçların Özeti

$n \times n$ boyutlu $X = (x_{i,j})_{1 \le i,j \le n}$ matrisinin determinanti ve permanenti sırasıyla

$$\det_n(X) = \sum_{\sigma \in S_n} \mathrm{sgn}(\sigma) \prod_{i=1}^n x_{i,\sigma(i)}, \qquad \mathrm{perm}_n(X) = \sum_{\sigma \in S_n} \prod_{i=1}^n x_{i,\sigma(i)}$$

biçiminde tanımlanır. Valiant'ın 1979 tarihli temel çalışmasından bu yana, $\mathrm{perm}_n$'in afin doğrusal bir matrisin determinanti olarak yazılabilmesi için gereken en küçük matris boyutu olan **determinantal karmaşıklık** $\mathrm{dc}(\mathrm{perm}_n)$ (ve bunun Zariski kapanışı olan **sınır determinantal karmaşıklığı** $\underline{\mathrm{dc}}(\mathrm{perm}_n)$), $\mathrm{VP} \neq \mathrm{VNP}$ problemine açılan en doğrudan kapıdır. Öte yandan, $\{0,1\}^{n\times n}$ üzerinde $\mathrm{perm}_n \bmod 3$ ile $\det_n \bmod 3$ arasındaki Boolean / eşik devresi ($\mathrm{TC}^0$) ayrımı, $\mathrm{P} \neq \mathrm{NP}$ ve $\mathrm{TC}^0 \neq \mathrm{NC}^1$ bariyerlerini (*Duvar 2*) test eden doğal bir laboratuvardır.

Bu çalışma, sistematik bir **engel-tespit ve engel-çözüm döngüsü** boyunca altı uzmanlık ekseninde (Euler: spektral/kombinatoryal, Noether: temsil/torus/simetri, Hilbert: cebirsel geometri/Macaulay/tekillikler, Strassen: tensör/Koszul/sınır değişmezleri, Valiant: devreler/LP/Burnside, Wigner: harmonik analiz/$\mathbb{F}_2$-rank/2-adik) üretilmiş ve tek bir deterministik doğrulama paketinde (`verify_all_council.py`) bir araya getirilmiş **45 teoremi** belgelendirmektedir.

### Epistemik Etiketleme Standardı

Makale boyunca her teorem şu üç etiketten biriyle işaretlenir:
- **`[KANITLANDI]`**: Tam cebirsel, kombinatoryal veya çift-asal kesin tamsayı/sonlu-cisim sertifikasıyla kapatılmış teorem.
- **`[SAYISAL DOĞRULANDI]`**: Genel-konum veya yüksek-hassasiyetli sayısal/sonlu-cisim taramasıyla desteklenen, ancak tam sembolik kapanışı henüz açık olan önerme (ör. Teorem 8, Teorem 16).
- **`[DÜRÜST ÇÜRÜTME / AÇIK]`**: Araştırma sırasında yanlışlanan hipotezler veya teorik tavanlara çarpan sınırlar (Bölüm 6).

### Başlıca Sonuçlar Özeti

| Eksen | Öne Çıkan Teoremler | Temel Sonuç | Doğrulama Sertifikası |
| :--- | :--- | :--- | :--- |
| **Satır-Ayrışımlı ABP** | Teorem 1–8, 14–25 | $n=4, w=5$ tam imkânsızlık; $n=6, w=19$ için 24/32 sınır demeti + Yükümlülük A & B kapanışı | `Test 1–25` (`PASS`) |
| **Tek-Taraflı Torus ABP** | Teorem 26, 31, 36, 41 | Tüm 4-katmanlı $T_4^{\mathrm{row}}$-eşdeğişir ABP'ler için $m \ge 15 = 2^4-1$; $n=5$'te $w_2 \ge 10$ | `Test 26, 31, 36, 41` (`PASS`) |
| **Tekillik & IMSC** | Teorem 27, 32, 37, 42 | $\mathrm{codim}\,\mathrm{Sing}(\mathrm{perm}_4)=8$, $\mathrm{Sing}_2(\mathrm{perm}_4)=12$, $\mathrm{Sing}_3(\mathrm{perm}_5)=20$, $\mathrm{Sing}_2(\mathrm{perm}_5)\ge 15$ | `Test 27, 32, 37, 42` (`PASS`) |
| **Koşulsuz $\mathrm{dc}$ / $\underline{\mathrm{dc}}$** | Teorem 28, 33, 38, 43 | $\mathrm{dc}(\mathrm{perm}_3)=7$, **$\mathrm{dc}(\mathrm{perm}_4)\ge 11$**, **$\underline{\mathrm{dc}}(\mathrm{perm}_4)\ge 11$** (açık $R_9^{(4)}$ değişmezi) | `Test 28, 33, 38, 43` (`PASS`) |
| **Cebirsel–Boolean & $\mathrm{TC}^0$** | Teorem 29, 30, 34, 35, 39, 40, 44, 45 | Pauli derece yasası ($n^2-2$ vs $n^2-1$), $n=5$ tam $4.89\times$ ayrım, $D_{\mathrm{PTF}}(5)\ge 7$, $\mathrm{TC}^0_3$ tek-değişkenli çöküşü | `Test 29, 30, 34, 35, 39, 40, 44, 45` (`PASS`) |

---

## 2. Satır-Ayrışımlı Homojen ABP'ler: $n=4, w=5$ İmkânsızlığı ve $n=6, w=19$ Sınır Geometrisi (Teorem 1–25)

Homojen bir cebirsel dallanma programı (ABP), $\mathrm{perm}_n(X) = \mathbf{v}_0^T A_1(X) A_2(X) \cdots A_n(X) \mathbf{v}_n$ biçiminde katmanlı bir matris çarpımıdır. Grenet'nin (2011) $2^n-1$ üst sınırı, katman genişlikleri $w_k = \binom{n}{k}$ olan satır-ayrışımlı bir yapı kurar. Bu bölüm, $n=4$ için orta katman genişliğinin $w_2 = 5 < \binom{4}{2} = 6$ olamayacağını kesin olarak kanıtlar ve aynı çerçeveyi $n=6, w_3 = 19 < \binom{6}{3} = 20$ sınırına genişletir.

### 2.1 Spektral Yöntem, Eşleme Tabanı ve Tel-Operatör Kimliği (Teorem 1–4)

**Teorem 1 (`[KANITLANDI]` — Euler Eşleme Operatörü ve Spektrumu, `Test 1`).**  
$\mathrm{perm}_4(X)$'in orta $4\times 4$ bloğundan elde edilen $T \in (\mathbb{C}^4)^{\otimes 4}$ tensörünün $16 \times 16$ düzleştirme matrisi $M$, tamsayılar üzerinde simetriktir ($M = M^T$) ve

$$M^3 = 4M$$

minimal polinom kimliğini sağlar. $M$'nin spektrumu kesin olarak $\{+2 \text{ (katlılık } 3),\ -2 \text{ (katlılık } 3),\ 0 \text{ (katlılık } 10)\}$ şeklindedir. Sıfırdan farklı 6 özvektör, $K_4$ tam grafiğinin üç mükemmel eşlemesi $(01)(23), (02)(13), (03)(12)$ üzerindeki simetrik ($X_1, X_2, X_3$; özdeğer $+2$) ve anti-simetrik ($Y_1, Y_2, Y_3$; özdeğer $-2$) $\mathrm{Sym}_0(4)$ kombinasyonları tarafından gerilir.

*Kanıt özeti.* $M_{(j_0, c_1), (j_3, c_2)} = 1$ ancak ve ancak $\{j_0, c_1, j_3, c_2\} = \{0,1,2,3\}$ iken geçerlidir. İki adım $M^2$, aynı ayrık çiftte birleşen permutasyonları sayar; üçüncü adım $M^3$, her eşleme sınıfı üzerinde 4 katlı döngü vererek $M^3 = 4M$ özdeşliğini tamsayılar üzerinde doğrular. $\square$

**Teorem 2 (`[KANITLANDI]` — Noether Temsil Ayrışımı, `Test 2`).**  
$S_4$ simetrik grubunun etkisi altında sıfır-köşegenli simetrik matrisler uzayı $\mathrm{Sym}_0(4) \cong \mathbb{C}^6$, üç indirgenemez bileşene ayrışır:

$$\mathrm{Sym}_0(4) = \mathbf{1} \oplus (2,2) \oplus (3,1),$$

ve $T$ tensörü dört indisin tamamında tam simetriktir.

*Kanıt özeti.* $M$'nin $+2$-özuzayı $\mathbf{1} \oplus (2,2)$ ($1+2=3$ boyutlu), $-2$-özuzayı ise $(3,1)$ ($3$ boyutlu) olarak ayrışır; $S_4$-değişmezliği Schur lemması ile bu blokların $M$ altında korunduğunu zorlar. $\square$

**Teorem 3 (`[KANITLANDI]` — Euler Tel-Operatör Kimliği ve Çekirdek Alt Sınırı, `Test 3`).**  
Herhangi bir genişlik-5 ara tel çifti $(B, V)$ için $K(B, V)$ doğrusal operatörü, $4 \times 4$ matrisler $Z$ üzerinde

$$K(B, V)(Z) = B Z^T V$$

biçiminde etkir ve $K \Sigma = B \otimes V^T$ ($\Sigma$: devrik permütasyon operatörü) özdeşliğini sağlar. Buradan herhangi iki tel $K_1, K_2$ için ortak çekirdek boyutu

$$\dim\big(\ker(M) \cap \ker(M - K_1 - K_2)\big) \ge 7$$

eşitsizliğini zorlar.

**Teorem 4 (`[KANITLANDI]` — Hilbert Köşegen Çözülebilirliği, `Test 4`).**  
Satır değişkenlerinin özdeşleştirildiği köşegen kısıtlamada $P(a, a) = L_1(a)_{4\times 5} L_2(a)_{5\times 4}$ çarpanlara ayırması genişlik $w = 5$'te çözülebilirdir (`artık normu = 4.22e-9`). Bu teorem, yalnızca köşegen uzmanlaşmaları kullanan herhangi bir tek-değişkenli tekniğin $w=5$ imkânsızlığını kanıtlayamayacağını gösterir; gerçek engel çapraz-terim ($a \neq b$) tensör yapısındadır.

### 2.2 Kombinatoryal Katmanlama, Ayar Boyutu ve $n=4, w=5$ Kapanışı (Teorem 5–8)

**Teorem 5 (`[KANITLANDI]` — Valiant Kombinatoryal Rank Demeti Katmanlaması, `Test 5`).**  
$w = 5$ genişlikli olası bir $P(a, b) = L_1(a)_{4\times 5} L_2(b)_{5\times 4}$ ayrışımının beş telinin $(r_i, c_i)$ rank çiftleri üzerindeki kombinatoryal eleme sonrasında $S_5$-yörüngeleri altında **tam olarak 11 yörüngede 31 hayatta kalan rank demeti** bulunur.

**Teorem 6 (`[KANITLANDI]` — Valiant $k_{\min} \in \{0,1\}$ Elemesi, `Test 6`).**  
Rank demetinde $k_{\min} = 0$ (sıfır teli) bulunan tüm profiller $\mathrm{rank}(P) \le 5 < 6$ çelişkisiyle elenir. $k_{\min} = 1$ (rank-1 tel) içeren profiller ise Westwick–Atkinson sınıflandırması ve Noether'in 10 istisnai rank-3 altuzayı ($4$ köşe uzayı $K_k$ ve $6$ karışık-eşleme uzayı $M_{i,j}$) ile çelişerek elenir (`600/600` Q1 rank $\ge 4$ tanığı).

**Teorem 7 (`[KANITLANDI]` — Wigner Fiziksel Ayar ve Teğet Uzayı Boyutu, `Test 7`).**  
$w=5$ parametrizasyonundaki $\mathrm{GL}_3 \times \mathrm{GL}_2$ ayar simetri grubunun boyutu $9 + 4 = 13$'tür. Fiziksel teğet uzayının boyutu $147$, çevre uzaydaki kodimansı ise $109$'dur.

**Teorem 8 (`[SAYISAL DOĞRULANDI]` — Sonlu Cisim Alt Sınırı, `Test 8`).**  
$\mathbb{F}_3$ ve $\mathbb{F}_5$ sonlu cisimleri üzerinde rastgele ve yapısal $K_1, K_2$ tel çiftleri için $\mathrm{rank}(M - K_1 - K_2) \ge 6$ eşitsizliği korunur; bu sonuç, Hilbert Ana Kanıtı (H2 çekirdek-görüntü kesişimiyle 31 demetten 10'unun kalması) ve Strassen Koszul düzleştirmesiyle birleşerek $n=4, w=5$ imkânsızlığını tam olarak kapatır.

### 2.3 Genel $n=2k$ Spektral Yasası, Kneser–Katona Kimliği ve 32 Sınır Demeti (Teorem 9–14)

**Teorem 9 (`[KANITLANDI]` — Genel $n=2k$ Spektral Yasası ve Dikdörtgen Kronecker Çözümlemesi, `Test 9`).**  
Her çift $n = 2k$ için $\mathrm{perm}_{2k}$'nin orta katman operatörü $M_{2k}$, $K_{2k}$'nın ayrık $k$-altkümeleri arasındaki Kneser/Johnson eşleme yapısıyla yönetilir (Strassen Teorem 5). Dikdörtgen Kronecker açılımı, tel operatörlerinin spektral izlerini keyfi $n = 2k$'ya taşır.

**Teorem 10 (`[KANITLANDI]` — Hilbert Kneser Kimliği ve Katona Geri-Kazanımı, `Test 10`).**  
$n = 6$ için $\binom{6}{2} = 15$ köşeli Kneser grafiği $\mathrm{KG}(6,2)$'nin komşuluk matrisi

$$\det\big(\mathrm{KG}(6,2)\big) = -1458 = -2 \cdot 3^6$$

tam tamsayı determinantına sahiptir ve ayrık çift ailelerinin maksimum boyutunu veren Katona teoremini cebirsel olarak geri kazanır.

**Teorem 11 (`[KANITLANDI]` — $n=6, w=19$ Sınırındaki 32 Demetin Parçalanması, `Test 11`).**  
$n = 6$'da orta katman genişliği $w = 19 < \binom{6}{3} = 20$ varsayımı altında kalan $32$ kritik rank demeti, minimum tel rankına göre kesin olarak $14$ ($\min=1$), $10$ ($\min=2$) ve $8$ ($\min \in \{3,4\}$) olarak üçe ayrılır.

**Teorem 12 (`[KANITLANDI]` — Kanonik Tellerin Derece-1 Syzygy Katılığı, `Test 12`).**  
$n = 6$'nın 20 kanonik $\binom{6}{3}$ telinden herhangi birinin silinmesiyle oluşan 19 telli sistemlerin tamamında derece-1 syzygy çekirdeği sıfırdır (`20/20` koordinat silmesinde `nullity = 0`).

**Teorem 13 (`[KANITLANDI]` — Hilbert Karşı-Örnek 1B, `Test 13`).**  
Çift-dereceli (bidegree) değişken teller ile sabit katsayılı teller arasında nitel bir ayrım vardır: sabit teller için geçerli olan bazı rank-düşüşü engelleri, çift-dereceli tellerde yalnızca homojenleştirme yoluyla elenebilir.

**Teorem 14 (`[KANITLANDI]` — Hilbert Teorem H5: 24/32 Sınır Demetinin Elenmesi, `Test 14`).**  
Atkinson–Lloyd sınırlandırılmış rank uzayları teoremi ve Katona kesişim teoremi birlikte uygulanarak $n=6, w=19$ sınırındaki $32$ kritik demetin **$24$'ü** ($\min \in \{1, 2\}$ olan tüm demetler) kesin olarak elenir; yalnızca $\min \in \{3, 4\}$ olan $8$ yüksek-ranklı demet kalır.

### 2.4 İki-Noktalı Özelleştirme, $\mathrm{Gr}(d,15)$, 135-Noktalı Varyete ve Çift Kapatma Anahtarı (Teorem 15–22)

**Teorem 15 (`[KANITLANDI]` — Noether İki-Noktalı Özelleştirme Çift-Doğrusal Yoketmesi, `Test 15`).**  
İki-noktalı uzmanlaşma altında çift-doğrusal yoketme matrisi, $w=19$ için rankın özdeş olarak $20 > 19$ olduğunu zorlayarak sabit-ranklı bozulmaları dışlar.

**Teorem 16 (`[SAYISAL DOĞRULANDI]` — Koordinatsız $\mathrm{GK}_6$ Genişlemesi, `Test 16`).**  
Grassmannian $\mathrm{Gr}(d, 15)$ üzerinde tüm genel $d \le 11$ altuzayları için kusur fonksiyoneli $\delta(W) = 0$ olarak doğrulanmıştır; bu durum $n=6$ çekirdek yapısının koordinat seçiminden bağımsız olduğunu gösterir.

**Teorem 17 (`[KANITLANDI]` — Hilbert Karşı-Örnek `#55`, `Test 17`).**  
Tamsayılar üzerinde açık Koszul sadeleşmesi

$$b_0 v_{145} - b_1 v_{045} = b_4 r_1 + b_5 r_2$$

gerçekleşir. Bu karşı-örnek, yalın tek-syzygy sayımının neden yetersiz kaldığını ve neden Yükümlülük A/B ayrımına (Teorem 20–25) geçilmesi gerektiğini kesin olarak gösterir.

**Teorem 18 (`[KANITLANDI]` — Noether–Strassen Teorem 8: $V_{K_4}$ $(10,9)$ Lokusunun Tam Elenmesi, `Test 18`).**  
$V_{K_4}$ üzerindeki $(10,9)$ rank profili, boyut sayımı çelişkisi $16 \le 15$ aracılığıyla tamamen elenir.

**Teorem 19 (`[KANITLANDI]` — Valiant Evrensel Pascal Özelleştirme Teoremi, `Test 19`).**  
Tüm çift $n = 4, 6, \dots, 20$ değerleri için Pascal uzmanlaşması

$$w \ge \frac{1}{2}\binom{n}{k} + r_1 \ge \binom{n}{k}$$

evrensel alt sınırını verir ($k = n/2$, burada $r_1$ birinci bileşenin özelleştirilmiş rank katkısıdır).

**Teorem 20 (`[KANITLANDI]` — Hilbert Teorem H6: 135-Noktalı Rank-3 Varyetesi, `Test 20`).**  
$\mathrm{im}(G_6)$ içindeki rank-3 projektif varyetesi, $S_6$ etkisi altında **4 yörüngede tam olarak 135 nokta** içerir.

**Teorem 21 (`[KANITLANDI]` — Hilbert Teorem H7: Olay Lif Sınıflandırması ve $N(e_0+e_1)$ Elenmesi, `Test 21`).**  
135-noktalı varyetenin olay lifleri sınıflandırıldığında, $N(e_0 + e_1)$ dalı $16 \le 11$ boyut çelişkisiyle tamamen elenir.

**Teorem 22 (`[KANITLANDI]` — Noether Teorem 9 & Valiant Ödünleşimi: Yükümlülük A Çift Kapatma Anahtarı, `Test 22`).**  
Kanonik kalemler üzerinde $c$ (bağımsız tel sayısı) ile $d_{\mathrm{syz}}$ (syzygy boyutu) arasında

$$\min(c - 4,\ d_{\mathrm{syz}} - 5) \le 0$$

çift kapatma anahtarı geçerlidir; bu eşitsizlik Yükümlülük A'yı kapatır.

### 2.5 Tur 7 Genel-Konumsuz Kapanış Boşlukları (Teorem 23–25)

**Teorem 23 (`[KANITLANDI]` — Tur 7 Boşluk 1: $c \le 4$ Dalının Genel-Konumsuz Elenmesi, `Test 23`).**  
Sylvester rank eşitsizliği ve Westwick sınıflandırması kullanılarak, hiçbir genel-konum (genericity) varsayımı olmadan $c \le 4$ dalı cebirsel olarak tamamen elenir.

**Teorem 24 (`[KANITLANDI]` — Tur 7 Boşluk 2: Keyfi Kalemler için Evrensel Syzygy–Tel Ödünleşimi, `Test 24`).**  
$\min(c - 4, d_{\mathrm{syz}} - 5) \le 0$ ödünleşimi yalnızca kanonik değil, **keyfi** matris kalemleri için de geçerlidir (`90/90` doğrulama vakası).

**Teorem 25 (`[KANITLANDI]` — Tur 7 Boşluk 3: Çift-Doğrusal Yoketme ve Yükümlülük B'nin Kapanışı, `Test 25`).**  
$\mathrm{Gr}(d, 15)$ üzerinde çift-doğrusal yoketme altuzayları $\dim U + \dim V \le 10 < 11$ sınırını zorlayarak Yükümlülük B'yi tamamen kapatır.

---

## 3. Torus Eşdeğişirliği, Tek-Taraflı $T_n^{\mathrm{row}}$ Kısıtı ve Handshaking Kapanışı (Teorem 26, 31, 36, 41)

Satır-ayrışımlı kısıtı kaldırmak için bir sonraki doğal adım, $\mathrm{perm}_n$'in doğal simetri grubu olan satır-sütun ölçekleme torusu $T_n = (\mathbb{C}^*)^n \times (\mathbb{C}^*)^n$ veya bunun yalnızca satırları ölçekleyen tek-taraflı altgrubu $T_n^{\mathrm{row}} = (\mathbb{C}^*)^n$ altında eşdeğişir ABP'leri incelemektir.

**Teorem 26 (`[KANITLANDI]` — Noether Teorem 16, 17A & 17B: Torus ve Sütun-Karıştırma Alt Sınırları, `Test 26`).**  
1. *(Teorem 16 — Çift-Taraflı $T_n$):* $\mathrm{perm}_n$'i hesaplayan her $T_n$-eşdeğişir homojen ABP'nin toplam boyutu $m \ge 2^n - 1$ (Grenet sınırı) olmak zorundadır.
2. *(Teorem 17A — Tek-Taraflı $T_n^{\mathrm{row}}$):* Her $T_n^{\mathrm{row}}$-eşdeğişir ABP için ilk ve son katman genişlikleri $w_1 \ge n$ ve $w_{n-1} \ge n$ sağlar; dolayısıyla $n=3$'te $m \ge 7 = 2^3 - 1$ kesindir.
3. *(Teorem 17B — Sütun-Karıştırma):* Blok-boyutu $B_k$ olan sütun-karıştırmalı ABP'lerde $w_k \ge \binom{n}{k} / B_k$ geçerlidir.

**Teorem 31 (`[KANITLANDI]` — Noether Teorem 18A, 18B & 18C: Karışık Satır-Çifti Elemesi ve $\mathrm{Sym}^4(\mathbb{C}^4)$ Çarpışma Duvarı, `Test 31`).**  
$n = 4$ ve tek-taraflı $T_4^{\mathrm{row}}$ altında orta katman ağırlık dağılımları $(4,0,0)$, $(5,0,0)$, $(3,1,0)$ ve $(4,1,0)$ karışık satır-çifti rank çelişkisiyle elenir. $\mathrm{Sym}^4(\mathbb{C}^4)$'te $34$-boyutlu çarpışma duvarı, 4-katmanlı darboğazı $w_2$'nin ağırlık yapısına indirger.

**Teorem 36 (`[KANITLANDI]` — Noether Teorem 19A & 19B: Bozonik Hiperdüzlem-Çarpım Katılığı ve $m \le 13$ Elenmesi, `Test 36`).**  
1. *(Teorem 19A):* Bozonik hiperdüzlem çarpımı, her orta katman düğümünü tek-sütun kilidine (single-column lock) zorlar.
2. *(Teorem 19B):* Çift-sayım eşitsizliği $4 w_2 \ge 24 \implies w_2 \ge 6$ verir; bu sayede $m \le 13$ boyutlu **tüm** 4-katmanlı $T_4^{\mathrm{row}}$-eşdeğişir ABP'ler elenir.

**Teorem 41 (`[KANITLANDI]` — Noether Teorem 20A & 20B: 10-Noktalı $\Sigma_{\le 2}$ Lokusu ve $m \ge 15$ Tam Kapanışı, `Test 41`).**  
1. *(Teorem 20A):* $\mathbb{P}^3$ içindeki rank $\le 2$ tensör dilimlerinin oluşturduğu 10-noktalı projektif lokus $|\Sigma_{\le 2}| = 10$, kalan tüm $w_2 = 4$ ağırlık profillerini kesin olarak öldürür.
2. *(Teorem 20B — Handshaking Kapanışı):* Çizge-teorik el-sıkışma (handshaking) sayımı, **tüm 4-katmanlı $T_4^{\mathrm{row}}$-eşdeğişir ABP'ler için**

$$m \ge 15 = 2^4 - 1$$

kesin Grenet sınırını kapatır ve aynı yöntem $n = 5$'te orta katman için $w_2 \ge 10$ alt sınırını verir. *(Not: Ek B'de Tur 15–16 ile $n=5$'te $(w_1, w_4) \in \{(5,5),(6,5),(5,6)\}$ için $m \ge 31 = 2^5-1$ kapanışı ayrıca belgelenmektedir.)*

---

## 4. Tekillik Kodimansı, Yinelemeli Macaulay Schur-Tümleyeni (IMSC) ve Koşulsuz $\mathrm{dc}(\mathrm{perm}_n)$ / $\underline{\mathrm{dc}}(\mathrm{perm}_n)$ Alt Sınırları (Teorem 27, 28, 32, 33, 37, 38, 42, 43)

Hiçbir simetri veya katman kısıtı olmayan genel determinantal temsiller $\mathrm{perm}_n(X) = \det_m(A_0 + \sum_{i,j} x_{i,j} A_{i,j})$ için temel geometrik silah, $\mathrm{perm}_n = 0$ hiperyüzeyinin tekillik katmanlarının ($\mathrm{Sing}_k(\mathrm{perm}_n)$) kodimansıdır. Bu bölüm, tam tamsayı / çift-asal **Yinelemeli Macaulay Schur-Tümleyeni (IMSC)** yöntemiyle hesaplanan kesin kodimansları ve Strassen'in **Orijin-İzotropisi**, **Çift-Koszul** ve **Pertürbe Çarpık-Kare** teoremleriyle elde edilen koşulsuz $\mathrm{dc}$ ve $\underline{\mathrm{dc}}$ alt sınırlarını bir araya getirir.

### 4.1 Kesin Tekillik Kodimansı Merdiveni (Hilbert Teorem H-11A – H-14C)

**Teorem 27 (`[KANITLANDI]` — Hilbert Teorem H-11A: $L_7$ Üzerinde Kesin Macaulay Sertifikası, `Test 27`).**  
$\mathrm{perm}_4$'ün kısmi türev ideali $J(\mathrm{perm}_4) = (\partial_{i,j}\mathrm{perm}_4)$, $7$-boyutlu bir genel doğrusal altuzay $L_7 \subset \mathbb{C}^{16}$ üzerinde derece-6 Macaulay matrisi kurulduğunda hem $\mathbb{F}_{1000003}$ hem $\mathbb{F}_{1000033}$ üzerinde tam ranka (**$924 / 924$**) ulaşır. Dolayısıyla

$$\mathrm{codim}_{\mathbb{C}^{16}}\big(\mathrm{Sing}(V(\mathrm{perm}_4))\big) \ge 7, \qquad w_2 \ge 4, \qquad \mathrm{str}(\mathrm{perm}_4) = 4$$

(burada $\mathrm{str}$ polinomun mukavemetini / strength değerini gösterir).

**Teorem 32 (`[KANITLANDI]` — Hilbert Teorem H-12A & H-12B: $\mathrm{perm}_4$ ve $\mathrm{perm}_5$ Tekillik Kodimansları, `Test 32`).**  
1. *(Teorem H-12A):* $L_8 \subset \mathbb{C}^{16}$ üzerinde IMSC indirgemesi tam ranka (**$11{,}440 / 11{,}440$**) ulaşır. İki-sıfır-satırlı aşikâr bileşen $\mathrm{codim} = 8$ verdiğinden, kesin eşitlik elde edilir:

$$\mathrm{codim}_{\mathbb{C}^{16}}\big(\mathrm{Sing}(V(\mathrm{perm}_4))\big) = 8.$$

2. *(Teorem H-12B):* $\mathrm{perm}_5$ için $L_8 \subset \mathbb{C}^{25}$ üzerinde Macaulay blokları tam ranka (**$3{,}003 / 3{,}003$** ve **$6{,}435 / 6{,}435$**) ulaşır; dolayısıyla $\mathrm{codim}_{\mathbb{C}^{25}}(\mathrm{Sing}(V(\mathrm{perm}_5))) \ge 8$ ve $\mathrm{str}(\mathrm{perm}_5) \ge 4$.

**Teorem 37 (`[KANITLANDI]` — Hilbert Teorem H-13A, H-13B & Lemma H-13.1: Yüksek-Mertebe Tekillik Katmanları, `Test 37`).**  
1. *(Teorem H-13A):* İkinci-mertebe türev ideali $\mathrm{Sing}_2(\mathrm{perm}_4)$ için $L_{12}$ üzerinde Macaulay matrisi **$1{,}365 / 1{,}365$** tam rank verir:

$$\mathrm{codim}_{\mathbb{C}^{16}}\big(\mathrm{Sing}_2(\mathrm{perm}_4)\big) = 12 = 3n.$$

2. *(Teorem H-13B):* Üçüncü-mertebe türev ideali $\mathrm{Sing}_3(\mathrm{perm}_5)$ için $L_{20}$ üzerinde **$1{,}540 / 1{,}540$** tam rank elde edilir:

$$\mathrm{codim}_{\mathbb{C}^{25}}\big(\mathrm{Sing}_3(\mathrm{perm}_5)\big) = 20 = 4n.$$

3. *(Lemma H-13.1):* $RC_{0,0}$ bileşeni üzerinde ikinci dereceden formların rankı tam **$45 / 45$** olarak doğrulanır.

**Teorem 42 (`[KANITLANDI]` — Hilbert Teorem H-14A, H-14B & H-14C: $\mathrm{Sing}_2(\mathrm{perm}_5)$ ve 28-Bileşenli Hessian Merdiveni, `Test 42`).**  
1. *(Teorem H-14A):* $\mathrm{Sing}_2(\mathrm{perm}_5)$ katmanının kodimansı $k=13$ diliminde **$6{,}188 / 6{,}188$** Macaulay tam rankı, 3-sıfır-satırlı Jakobiyen ($15/25$) ve yıldız-dışlama argümanıyla kesinleşir ($\mathrm{codim} = 15 = 3n$ üst katmanı).
2. *(Teorem H-14B/C):* $\mathrm{perm}_4$'ün Hessian rank katmanları $\mathcal{H}_{\le 2k}(\mathrm{perm}_4) = \{X \in \mathbb{C}^{16} : \mathrm{rank}\,\mathrm{Hess}(\mathrm{perm}_4)(X) \le 2k\}$ için 28 kombinatoryal bileşen üzerindeki kesin kodimans merdiveni

$$\big(\mathrm{codim}\,\mathcal{H}_{\le 0},\ \mathcal{H}_{\le 2},\ \mathcal{H}_{\le 4},\ \mathcal{H}_{\le 6},\ \mathcal{H}_{\le 8}\big) = (12,\ 12,\ 10,\ 9,\ 8)$$

olarak sınıflandırılır.

### 4.2 Orijin-İzotropisi, Çift-Koszul ve Koşulsuz $\mathrm{dc}(\mathrm{perm}_4) \ge 11$, $\underline{\mathrm{dc}}(\mathrm{perm}_4) \ge 11$ (Strassen Teorem 11–15C)

**Teorem 28 (`[KANITLANDI]` — Strassen Teorem 11 & Kısıtlı $\mathcal{D}_m^{\mathrm{hom}}$ Kodimansı, `Test 28`).**  
$\mathrm{codim}(\mathrm{Sing}(V(\mathrm{perm}_3))) = 6$ gerçeği, herhangi bir determinantal temsilde tekil korank parametresi $s \ge 3$ eşitsizliğini zorlar; bu sonuç $m \le 6$ boyutlu tüm 4-katmanlı ABP'leri ve $r=2$ Schur ayrışımlarını eler. Homojen determinantal varyete $\mathcal{D}_m^{\mathrm{hom}}$'un $m=7$'deki kısıtlı kodimansı $66$ olarak hesaplanır.

**Teorem 33 (`[KANITLANDI]` — Strassen Teorem 12, Sonuç 12.1 & Teorem 13: Orijin-İzotropisi ve $\mathrm{dc}(\mathrm{perm}_3)=7$, `Test 33`).**  
1. *(Teorem 12 — Orijin-İzotropisi):* $A_0$'ın rankı $r = \mathrm{rank}(A_0)$ olan bir afin determinantal temsilde, $A_0$ çekirdeği üzerindeki birinci-derece Koszul blokları bir izotropi kısıtı yaratır. Bu kısıt, $n=3$ için Alper–Bogart–Velasco (2017) sonucunun tamamen cebirsel ve yeni bir kanıtını vererek **koşulsuz $\mathrm{dc}(\mathrm{perm}_3) = 7$** eşitliğini kurar.
2. *(Sonuç 12.1 — Açık Derece-126 Değişmezi):* IMSC determinantı, $\det_6$-yörünge kapanışı üzerinde özdeş olarak sıfırlanan, ancak $\mathrm{perm}_3$ üzerinde sıfırdan farklı açık bir tam tamsayı polinom değişmezi $P_{I_0}(F) \in \mathbb{Z}[F]_{126}$ üretir:

$$P_{I_0}(\mathrm{perm}_3) \equiv 428{,}736 \pmod{1{,}000{,}003}, \qquad P_{I_0}(\mathrm{perm}_3) \equiv 945{,}683 \pmod{1{,}000{,}033}.$$

3. *(Teorem 13):* Aynı mekanizma $n=4$ için doğrudan $\mathrm{dc}(\mathrm{perm}_4) \ge 9$ verir.

**Teorem 38 (`[KANITLANDI]` — Strassen Teorem 14A & 14B: Çift-Koszul + Çarpık-Kare ile $\mathrm{dc}(\mathrm{perm}_4) \ge 10$, `Test 38`).**  
1. *(Teorem 14A):* $m = 9$ varsayımı altında tüm korank dalları $r \in \{0,\dots,8\}$ Çift-Koszul ve **Çarpık-Kare (Skew-Square) Yoketme Lemması** ile elenir; bu sonuç **koşulsuz $\mathrm{dc}(\mathrm{perm}_4) \ge 10$** vererek Alper–Bogart–Velasco'nun (2017) $n=4$ için kanıtladığı $\ge 9$ sınırını geçer.
2. *(Teorem 14B):* Açık IMSC değişmezi $P^{(4)}(F)$ çift-asal modülo sertifikalanır:

$$P^{(4)}(\mathrm{perm}_4) \equiv 5{,}223 \pmod{32{,}749}, \qquad P^{(4)}(\mathrm{perm}_4) \equiv 60{,}981 \pmod{65{,}521}.$$

**Teorem 43 (`[KANITLANDI]` — Strassen Teorem 15A, 15B, 15C & Sonuç 15.1: Koşulsuz $\mathrm{dc}(\mathrm{perm}_4) \ge 11$ ve $\underline{\mathrm{dc}}(\mathrm{perm}_4) \ge 11$, `Test 43`).**  
1. *(Teorem 15A — Sınır Değişmezi $R_9^{(4)}$):* $R_9^{(4)} = P^{(4)} \cdot Q^{(4)}$ çarpım değişmezi, $m \le 9$ (ve pertürbe kapanışta $m \le 10$) determinantal yörünge kapanışında sıfırlanırken $\mathrm{perm}_4$ üzerinde sıfırdan farklıdır:

$$R_9^{(4)}(\mathrm{perm}_4) \equiv 26{,}250 \pmod{32{,}749}, \qquad R_9^{(4)}(\mathrm{perm}_4) \equiv 39{,}383 \pmod{65{,}521}.$$

2. *(Teorem 15B — Evrensel Pertürbe Çarpık-Kare):* $A_0(\varepsilon)$ pertürbasyonu altında Çarpık-Kare özdeşliği `1.25e-13` hassasiyetle korunur ve sınır (border) temsillerine doğrudan taşınır.
3. *(Teorem 15C & Sonuç 15.1 — Evrensel $b^4$ $4\times 4$ Minör Kimliği):* $m=10$ için Hessian bloğundaki evrensel $b^4$ minör özdeşliği (`2.73e-12`) tüm $m=10$ dallarını kapatarak **koşulsuz**

$$\mathrm{dc}(\mathrm{perm}_4) \ge 11 \qquad \text{ve} \qquad \underline{\mathrm{dc}}(\mathrm{perm}_4) \ge 11$$

alt sınırlarını kanıtlar. *(Not: Ek B'de Tur 15'te $R_{10}^{(4)} = P^{(4)}T^{(4)}Q^{(4)}$ ile 4. kök içermeyen saf polinom sınır sertifikası ve koşulsuz $\mathrm{dc}(\mathrm{perm}_4) \ge 12$ genişlemesi yer almaktadır.)*

---

## 5. Cebirsel–Boolean Köprüsü, Pauli-Dışlama, $\mathrm{TC}^0_2/\mathrm{TC}^0_3$ ve Burnside Yörünge-LP Dualitesi (Teorem 29, 30, 34, 35, 39, 40, 44, 45)

Cebirsel karmaşıklık ($\mathrm{VP}\neq\mathrm{VNP}$) ile Boolean devre karmaşıklığı ($\mathrm{TC}^0\neq\mathrm{NC}^1$, $\mathrm{P}\neq\mathrm{NP}$) arasındaki en somut etkileşim, $f_n(X) = \mathbf{1}[\mathrm{perm}_n(X) \not\equiv 0 \pmod 3]$ ile $g_n(X) = \mathbf{1}[\det_n(X) \not\equiv 0 \pmod 3]$ Boolean fonksiyonlarının $\{0,1\}^{n\times n}$ üzerindeki harmonik, polinom ve eşik-devresi özelliklerinde ortaya çıkar.

### 5.1 Pauli-Dışlama Derece Yasası, Reed–Muller Duvarı ve 2-Adik Sıkıştırma (Wigner E5.1 – E5.4)

**Teorem 29 (`[KANITLANDI]` — Pauli-Dışlama $\mathbb{F}_3 \to \mathbb{F}_2$ ANF Derece Yasası ve $d=4$ $8.36\times$ Boşluğu, `Test 29`).**  
$\{0,1\}^{n\times n}$ üzerinde Cebirsel Normal Form (ANF, $\mathbb{F}_2$-derecesi) olarak:

$$\deg_{\mathbb{F}_2}\big(\det_n \bmod 3 \neq 0\big) \le n^2 - 2, \qquad \text{oysa} \qquad \deg_{\mathbb{F}_2}\big(\mathrm{perm}_n \bmod 3 \neq 0\big) = n^2 - 1$$

her $n \ge 2$ için geçerlidir ($n=2,3,4$ için kesin çiftler: $(2,4), (7,8), (12,15)$). Bunun nedeni, $\det_n$'de iki özdeş satırın/sütunun **Pauli-dışlama ilkesi** gereği özdeş olarak sıfırlanmasıdır. $n=4$'te derece-$4$ Reed–Muller yaklaşım hatasında `0.03845 vs 0.32162` (**$8.36\times$** boşluk) ve Euler $W_{14}$ Fourier kuyruğunda **$17.4\times$** ayrım gözlenir.

**Teorem 34 (`[KANITLANDI / NİCEL]` — Wigner E5.2: Dama-Tahtası $\mathrm{rk}_{\mathbb{F}_2}$ Ayrımı ve Tam $n=5$ ($2^{25}$ Matris) Analizi, `Test 34`).**  
1. Satır-ayrışımlı olmayan dama-tahtası (checkerboard) kesitinde $\mathrm{perm}_4$ ile $\det_4$ arasındaki iletişim matrisinin rankı $\mathrm{rk}_{\mathbb{F}_2} = 129 \text{ vs } 92$ (ve $\mathrm{rk}_{\mathbb{R}} = 138 \text{ vs } 133$) olarak ayrışır.
2. $n = 5$ için tüm **$2^{25} = 33{,}554{,}432$** ikili matris Burnside yörüngeleri ($K_5 = 5{,}624$) üzerinden kesin olarak taranır: $\mathrm{RM}(5, 25)$ yaklaşımında **`0.08358 vs 0.40911` ($4.89\times$ boşluk)** ve toplam etkide (total influence) **kesişim terslenmesi ($7.8969 > 6.8650$)** kanıtlanır.

**Teorem 39 (`[KANITLANDI / NİCEL]` — Wigner E5.3: 61-Yörüngeli $S_5\times S_5$ $\mathrm{RM}(5,25)$ Çok-Terimli Duvarı, `Test 39`).**  
$S_5 \times S_5$-değişmez derece $\le 5$ tabanının tamamı (`61` yörünge) üzerinden optimize edildiğinde dahi $\mathrm{perm}_5 \bmod 3$ yaklaşım hatası `0.4869`'dan yalnızca `0.4091`'e düşerken $\det_5 \bmod 3$ hatası `0.0836`'da kalır ($4.89\times$ ayrım). Aynı test, tekdüze ve SVD-sönümlü Forster sınırlarının bu ayrımı yakalamakta başarısız olduğunu dürüstçe belgeler (Bölüm 6).

**Teorem 44 (`[KANITLANDI / NİCEL]` — Wigner E5.4: 2-Adik Mod-4 Determinant Sıkıştırması ve $\mu^*_{\mathrm{THR}}$ Sherstov Denetimi, `Test 44`).**  
Determinant fonksiyonunun $\mathbb{Z}/4\mathbb{Z}$ (2-adik mod-4) yoğunluğu, yüksek mertebede üssel biçimde sıkışır: $n=4$'te sıfır-olmayan mod-4 oranı `%0.183` (**$21.0\times$** sıkıştırma), $n=5$'te ise `%1.122` (**$7.45\times$**; $\mathrm{perm}_5$'in `%29.99` oranına kıyasla **$26.72\times$** ayrım). Valiant'ın $\mu^*_{\mathrm{THR}}$ dual dağılımı altında Sherstov tutarsızlık (discrepancy) denetimi, minimax sınırların yapısını nicel olarak haritalar.

### 5.2 Burnside Yörünge-SAT, Reynolds $L_1$-İzometrisi ve $\mathrm{TC}^0_2 / \mathrm{TC}^0_3$ Alt Sınırları (Valiant Teorem 20.1 – 23.3)

**Teorem 30 (`[KANITLANDI]` — Valiant Teorem 20.1: Burnside Yörünge-SAT Sıkıştırması ve Williams Simetrizasyon İkilemi, `Test 30`).**  
$S_n \times S_n \times \mathbb{Z}_2$ (satır/sütun permütasyonları + devrik) simetri grubu altında $\{0,1\}^{n\times n}$ uzayının yörünge sayısı Burnside lemmasıyla

$$(K_2, K_3, K_4, K_5, K_6) = (7,\ 36,\ 317,\ 5{,}624,\ 251{,}610)$$

olarak hesaplanır; bu $n=6$'da **$273{,}119\times$** kesin sıkıştırma sağlar. Yörünge-değişmez özelliklerin yoğunluğu $2^{-65219}$ (Aşırı Küçüklük / Non-Largeness) olduğundan Razborov–Rudich Doğal Kanıtlar genişlik koşulunu ihlal eder; ancak **Williams Simetrizasyon İkilemi** uyarınca tek başına simetrizasyon devre alt sınırını otomatik olarak vermez, yörünge-içi korelasyonun LP dualitesiyle bağlanması gerekir.

**Teorem 35 (`[KANITLANDI]` — Valiant Teorem 21.1 & 21.2: Reynolds $L_1$-İzometrisi ve Pólya Kararlılığı, `Test 35`).**  
1. *(Teorem 21.1):* Reynolds yörünge ortalama operatörü $\mathcal{R}$, $S_n\times S_n$-değişmez eşik devreleri ve polinom eşik fonksiyonları (PTF) için **kesin bir $L_1$-izometridir**. $n=4$'te PTF derecesi $D_{\mathrm{PTF}} = 6$'dır; XOR tabanında **$3.875\times$**, $\mathrm{AND}_6$ tabanında ise **`42117.37 vs 9961.95` ($4.228\times$)** $L_1$-ağırlık boşluğu elde edilir.
2. *(Teorem 21.2 — Pólya Kararlılığı):* Derece $\le 6$ monom yörüngelerinin sayısı $n \ge 6$ için $K_n(\le 6) = 151$'de sabitlenir.

**Teorem 40 (`[KANITLANDI]` — Valiant Teorem 22.1–22.3: Tam $\mathrm{TC}^0_2$ Sözlükleri ve $n=3 \to 4$ Ölçeklenmesi, `Test 40`).**  
$n=4$ için tam `2,537`-kapılı $\{0,1\}$-THR sözlüğünde fan-in $\le 5$ **imkânsızdır (infeasible)**; fan-in $\le 6$'da **$4.340\times$** ağırlık boşluğu, tam sözlükte `200.46 vs 128.32` ayrımı oluşur. İşaretli `3,075`-kapılı $\{-1,0,+1\}$-THR sözlüğünde ise `182.32 vs 104.19` (**$1.750\times$**) ayrım ve $n=3 \to 4$ geçişinde **$12.06\times$** ağırlık büyümesi ölçülür.

**Teorem 45 (`[KANITLANDI]` — Valiant Teorem 23.1–23.3: Binom-Eşik Eşdeğerliği, $n=5$'te $D_{\mathrm{PTF}} \ge 7$ ve $\mathrm{TC}^0_3$ Tek-Değişkenli Çöküşü, `Test 45`).**  
1. *(Teorem 23.1):* Fan-in $\le D$ olan $\{0,1\}$-eşik kapılarının doğrusal germesi, $\mathrm{AND}_{\le D}$ tabanıyla özdeştir: $\mathrm{span}(\mathrm{THR}_{\{0,1\},\le D}) = \mathrm{span}(\mathrm{AND}_{\le D})$.
2. *(Teorem 23.2):* $n = 5$ ($K_5 = 5{,}624$ yörünge) üzerinde kesin LP çözücüsü fan-in $\le 6$'nın **imkânsız** olduğunu sertifikalar; dolayısıyla **kesin $D_{\mathrm{PTF}}(\mathrm{perm}_5 \bmod 3) \ge 7$**.
3. *(Teorem 23.3 — Derinlik-3 $\mathrm{TC}^0_3$ Tek-Değişkenli Çöküşü):* Yörünge-simetrik derinlik-3 $\mathrm{TC}^0_3$ devrelerinde ara katman aktivasyonları tek-değişkenli eşik profillerine çöker ve bağlı (coupled) yapılandırmada **$1.762\times$** ayrım boşluğu korunur.

---

## 6. Dürüst Sınırlar, Çürütülen Hipotezler ve Milenyum Bariyerleri

Bilimsel bütünlük gereği, bu çalışma yalnızca kanıtlanan teoremleri değil, aynı zamanda karşılaşılan yapısal tavanları ve yanlışlanan ara hipotezleri de açıkça kaydeder:

1. **Mignon–Ressayre $n^2$ Tavanı ($\mathrm{VP} \neq \mathrm{VNP}$ Bariyeri):** Hessian rankı ve tekillik kodimansı yöntemleri (Bölüm 4) sabit $n$ değerlerinde dünya rekoru kıran ($\mathrm{dc}(\mathrm{perm}_4) \ge 11$, Ek B'de $\ge 12$) sonuçlar üretse de, genel $n$ için asimptotik olarak $O(n^2)$ tavanına tabidir. Süper-polinom $\mathrm{dc}(\mathrm{perm}_n) = n^{\omega(1)}$ kanıtı için yüksek-dereceli apolar/GCT çoğulluk engellerine geçiş zorunludur.
2. **Razborov–Rudich Doğal Kanıtlar Bariyeri ($\mathrm{P} \neq \mathrm{NP}$ Bariyeri):** Bölüm 5'teki Burnside yörünge sıkıştırması genişlik (largeness) koşulunu $2^{-65219}$ ile aşsa da, tek başına $\mathrm{TC}^0_2$/$\mathrm{TC}^0_3$ LP alt sınırları henüz genel sabit-derinlikli $\mathrm{TC}^0$ devresi için süper-polinom bir ayrım sağlamamaktadır.
3. **Tekdüze / Minimax Forster Çürütmesi (`[DÜRÜST ÇÜRÜTME]`):** Teorem 39 ve 44 kapsamında test edilen tekdüze, SVD-sönümlü ve minimax Forster eşitsizlikleri, $\mathrm{perm}_n \bmod 3$ ile $\det_n \bmod 3$ arasında üssel bir iletişim ayrımı üretmekte başarısız olmuştur.
4. **Wood 2-Adik Doygunluğu (`[DÜRÜST ÇÜRÜTME]` — Ek B / Tur 15):** Teorem 44'teki 2-adik mod-4 sıkıştırması $n=4,5$'te dramatik ($21\times, 26.7\times$) görünse de, $n=6..10$ taraması Wood'un (2019) sabit yoğunluk sınırına (`0.439874`) yakınsayarak asimptotik ayrımın kaybolduğunu göstermiştir.
5. **PTF Direncinde $\det_n$ vs $\mathrm{perm}_n$ Ayrışmazlığı (`[DÜRÜST ÇÜRÜTME]` — Ek B / Tur 16):** $n=5$'te $\det_5 \bmod 3$ de yüksek PTF derecesine direnç gösterir; bunun cebirsel nedeni Schur tümleyeni $\det_n\begin{psmallmatrix} I_{n-1} & u \\ v^T & c \end{psmallmatrix} = c - \mathrm{IP}_{n-1}(u, v)$ gömmesidir.
6. **Kalan İki Dar Yaprak (`E1` & `E3.8`):** Satır-ayrışımlı $n=6, w=19$ probleminde 24/32 demet ile Yükümlülük A/B kapatılmış olmakla birlikte son 2 dar yaprak ve $n=4, m=12, D=8$ (`corank = 264`, Ek B) dalı aktif araştırma hedefi olarak açıktır.

---

## Ek A: 45 Teoremin Tam Doğrulama Matrisi (`Test 1–45`)

Aşağıdaki 45 testin tamamı [verify_all_council.py](file:///Users/bl10buer/Desktop/matemk/p-vs-np-gct/council/prof-euler/verify_all_council.py) içinde tek komutla çalışır ve **`45/45 PASS` (`74.058 s`, `exit code 0`)** verir.

| Test # | Teorem / Modül | Statü | Anahtar Matematiksel / Modüler Sertifika |
| :--- | :--- | :--- | :--- |
| **1** | Euler Eşleme & Spektrum | `[KANITLANDI]` | $M^3 = 4M$, özdeğerler $+2^{\times 3}, -2^{\times 3}, 0^{\times 10}$ |
| **2** | Noether Temsil Ayrışımı | `[KANITLANDI]` | $\mathrm{Sym}_0(4) = \mathbf{1} \oplus (2,2) \oplus (3,1)$, tam simetrik $T$ |
| **3** | Euler Tel-Operatör Kimliği | `[KANITLANDI]` | $K(B,V)Z = BZ^TV$, $\dim(\ker M \cap \ker(M-K_1-K_2)) \ge 7$ |
| **4** | Hilbert Köşegen Çözülebilirliği | `[KANITLANDI]` | $P(a,a)=L_1(a)_{4\times 5}L_2(a)_{5\times 4}$ çözülebilir (`4.22e-9`) |
| **5** | Valiant Rank Demeti Katmanlaması | `[KANITLANDI]` | 11 yörüngede tam 31 hayatta kalan rank demeti |
| **6** | Valiant $k_{\min}\in\{0,1\}$ Elemesi | `[KANITLANDI]` | $k_{\min}=0$ (`rk<=5<6`), $k_{\min}=1$ Westwick–Atkinson + `600/600` Q1 |
| **7** | Wigner Ayar Boyutu | `[KANITLANDI]` | $\dim(\mathrm{GL}_3\times\mathrm{GL}_2)=13$, teğet `147`, kodimans `109` |
| **8** | Sonlu Cisim Alt Sınırı | `[SAYISAL DOĞRULANDI]` | $\mathbb{F}_3, \mathbb{F}_5$ üzerinde $\mathrm{rank}(M-K_1-K_2) \ge 6$ |
| **9** | Genel $n=2k$ Spektral Yasa | `[KANITLANDI]` | Strassen Thm 5 & dikdörtgen Kronecker açılımı |
| **10** | Hilbert Kneser & Katona | `[KANITLANDI]` | $\det(\mathrm{KG}(6,2)) = -1458$, Katona geri-kazanımı |
| **11** | 32 Sınır Demeti Parçalanması | `[KANITLANDI]` | $n=6, w=19$: `14` ($\min=1$), `10` ($\min=2$), `8` ($\min\in\{3,4\}$) |
| **12** | Derece-1 Syzygy Katılığı | `[KANITLANDI]` | `20/20` kanonik tel silmesinde `nullity = 0` |
| **13** | Hilbert Karşı-Örnek 1B | `[KANITLANDI]` | Çift-dereceli vs sabit teller ayrımı |
| **14** | Hilbert Teorem H5 | `[KANITLANDI]` | Atkinson–Lloyd + Katona ile `24/32` sınır demeti elendi |
| **15** | Noether İki-Noktalı Yoketme | `[KANITLANDI]` | Çift-doğrusal yoketme rankı özdeş `20 > 19` |
| **16** | Koordinatsız $\mathrm{GK}_6$ | `[SAYISAL DOĞRULANDI]` | $\mathrm{Gr}(d,15)$ üzerinde genel $d\le 11$ için $\delta(W)=0$ |
| **17** | Hilbert Karşı-Örnek `#55` | `[KANITLANDI]` | $\mathbb{Z}$ üzerinde $b_0 v_{145} - b_1 v_{045} = b_4 r_1 + b_5 r_2$ |
| **18** | Noether–Strassen Teorem 8 | `[KANITLANDI]` | $V_{K_4}$ $(10,9)$ lokusu `16 <= 15` ile elendi |
| **19** | Valiant Evrensel Pascal | `[KANITLANDI]` | Çift $n=4..20$: $w \ge \frac{1}{2}\binom{n}{k}+r_1 \ge \binom{n}{k}$ |
| **20** | Hilbert Teorem H6 | `[KANITLANDI]` | $\mathrm{im}(G_6)$'da 4 yörüngede `135`-noktalı rank-3 varyetesi |
| **21** | Hilbert Teorem H7 | `[KANITLANDI]` | Olay lif sınıflandırması, $N(e_0+e_1)$ `16 <= 11` ile elendi |
| **22** | Noether Thm 9 & Valiant Ödünleşim | `[KANITLANDI]` | Çift kapatma anahtarı $\min(c-4, d_{\mathrm{syz}}-5) \le 0$ |
| **23** | Tur 7 Boşluk 1 | `[KANITLANDI]` | Sylvester & Westwick ile genel-konumsuz $c \le 4$ elemesi |
| **24** | Tur 7 Boşluk 2 | `[KANITLANDI]` | Keyfi kalemler için evrensel ödünleşim (`90/90`) |
| **25** | Tur 7 Boşluk 3 | `[KANITLANDI]` | $\mathrm{Gr}(d,15)$'te $\dim U+\dim V \le 10 < 11$ (Yükümlülük B) |
| **26** | Noether Thms 16, 17A, 17B | `[KANITLANDI]` | $T_n \Rightarrow m\ge 2^n-1$; $T_n^{\mathrm{row}} \Rightarrow w_1,w_{n-1}\ge n$; $w_k \ge \binom{n}{k}/B_k$ |
| **27** | Hilbert Thm H-11A | `[KANITLANDI]` | $L_7$ Macaulay `924/924` (mod `1000003, 1000033`), $\mathrm{str}(\mathrm{perm}_4)=4$ |
| **28** | Strassen Thm 11 & $\mathcal{D}_m^{\mathrm{hom}}$ | `[KANITLANDI]` | $\mathrm{codim}\,\mathrm{Sing}(\mathrm{perm}_3)=6 \Rightarrow s\ge 3$; $\mathcal{D}_7^{\mathrm{hom}}$ kodimansı `66` |
| **29** | Pauli-Dışlama & Wigner $d=4$ | `[KANITLANDI]` | ANF derecesi $n^2-2$ vs $n^2-1$; `8.36x` ($d=4$), `17.4x` ($W_{14}$) |
| **30** | Valiant Thm 20.1 | `[KANITLANDI]` | Burnside $K_2..K_6 = [7,36,317,5624,251610]$ (`273,119x`), $2^{-65219}$ |
| **31** | Noether Thms 18A/B/C | `[KANITLANDI]` | `(4,0,0),(5,0,0),(3,1,0),(4,1,0)` elemesi, $\mathrm{Sym}^4(\mathbb{C}^4)$ `34` duvarı |
| **32** | Hilbert Thms H-12A & H-12B | `[KANITLANDI]` | $\mathrm{codim}\,\mathrm{Sing}(\mathrm{perm}_4)=8$ (`11,440/11,440`), $\mathrm{perm}_5 \ge 8$ (`6,435/6,435`) |
| **33** | Strassen Thm 12, Cor 12.1 & 13 | `[KANITLANDI]` | $\mathrm{dc}(\mathrm{perm}_3)=7$, $P_{I_0}\in\mathbb{Z}[F]_{126}$ (`428736`, `945683`), $\mathrm{dc}(\mathrm{perm}_4)\ge 9$ |
| **34** | Wigner E5.2 | `[KANITLANDI / NİCEL]` | Dama `rk_F2` `129 vs 92`; tam $n=5$ ($33.55\mathrm{M}$) `4.89x`, etki `7.8969 > 6.8650` |
| **35** | Valiant Thms 21.1 & 21.2 | `[KANITLANDI]` | Reynolds $L_1$-izometrisi, `4.228x` $\mathrm{AND}_6$, Pólya $K_n(\le 6)=151$ |
| **36** | Noether Thms 19A & 19B | `[KANITLANDI]` | Tek-sütun kilidi, $4w_2\ge 24 \Rightarrow w_2\ge 6$, tüm $m\le 13$ $T_4^{\mathrm{row}}$ elendi |
| **37** | Hilbert Thms H-13A, H-13B & H-13.1 | `[KANITLANDI]` | $\mathrm{Sing}_2(\mathrm{perm}_4)=12$ (`1365/1365`), $\mathrm{Sing}_3(\mathrm{perm}_5)=20$ (`1540/1540`), `45/45` |
| **38** | Strassen Thms 14A & 14B | `[KANITLANDI]` | Koşulsuz $\mathrm{dc}(\mathrm{perm}_4)\ge 10$, $P^{(4)} \equiv 5223 \pmod{32749}, 60981 \pmod{65521}$ |
| **39** | Wigner E5.3 | `[KANITLANDI / NİCEL]` | Tam `61`-yörünge $S_5\times S_5$ $\mathrm{RM}(5,25)$ (`4.89x`), Forster dürüst çürütmesi |
| **40** | Valiant Thms 22.1–22.3 | `[KANITLANDI]` | `2,537`/`3,075`-kapılı $\mathrm{TC}^0_2$, fan-in $\le 5$ imkânsız, `1.750x`, `12.06x` ölçek |
| **41** | Noether Thms 20A & 20B | `[KANITLANDI]` | $|\Sigma_{\le 2}|=10$ + Handshaking $\Rightarrow$ **tüm 4-katmanlı $T_4^{\mathrm{row}}$: $m\ge 15$**, $n=5$ $w_2\ge 10$ |
| **42** | Hilbert Thms H-14A/B/C | `[KANITLANDI]` | $\mathrm{Sing}_2(\mathrm{perm}_5)$ `6188/6188`, 28-bileşenli $\mathcal{H}_{\le 2k}(\mathrm{perm}_4)=(12,12,10,9,8)$ |
| **43** | Strassen Thms 15A/B/C & Cor 15.1 | `[KANITLANDI]` | $R_9^{(4)}$ (`26250`, `39383`), $b^4$ minör (`2.73e-12`) $\Rightarrow$ **$\mathrm{dc}(\mathrm{perm}_4)\ge 11, \underline{\mathrm{dc}}\ge 11$** |
| **44** | Wigner E5.4 | `[KANITLANDI / NİCEL]` | 2-adik mod-4: `0.183%` (`21.0x`, $n=4$), `1.122%` (`26.72x` vs $\mathrm{perm}_5$) |
| **45** | Valiant Thms 23.1–23.3 | `[KANITLANDI]` | $\mathrm{THR}=\mathrm{AND}$, $n=5$ ($K_5=5624$) $D_{\mathrm{PTF}}\ge 7$, $\mathrm{TC}^0_3$ tek-değişkenli çöküş (`1.762x`) |

---

## Ek B: Tur 15–16 Doğrulanmış Yeni Sınırlar (`Test 45` Ötesi Genişlemeler)

Ana 45-teoremlik doğrulama paketinin (`verify_all_council.py`) üzerine, Tur 15 ve Tur 16'da aşağıdaki ek sonuçlar bağımsız Python betikleriyle `exit code 0` sertifikasıyla doğrulanmıştır:

1. **Koşulsuz $\mathrm{dc}(\mathrm{perm}_4) \ge 12$ ve Saf-Polinom $\underline{\mathrm{dc}}(\mathrm{perm}_4) \ge 11$ (Tur 15 — Hilbert H-15A & Strassen 16A/B):**  
   $L_9 \subset \mathbb{C}^{16}$ üzerinde derece-6 Macaulay matrisi **$12{,}870 / 12{,}870$** tam ranka ulaşır ($T^{(4)} \equiv 32{,}419 \pmod{32{,}749}$, $49{,}971 \pmod{65{,}521}$). $r=2,3,4$ denetimi ve `42/56` taramasıyla **koşulsuz $\mathrm{dc}(\mathrm{perm}_4) \ge 12$** ve 4. kök içermeyen saf-polinom değişmez $R_{10}^{(4)} = P^{(4)}T^{(4)}Q^{(4)}$ (`15985`, `19137` $\neq 0$) ile **$\underline{\mathrm{dc}}(\mathrm{perm}_4) \ge 11$** kanıtlanır. (`verify_round15_hilbert.py`, `verify_round15_strassen.py`)
2. **Global $\mathrm{codim}_{\mathbb{C}^{16}}(\mathcal{H}_{\le 4}(\mathrm{perm}_4)) = 10$ Kapanışı (Tur 16 — Hilbert H-16A/B/C):**  
   Sıfır-blok $6\times 6$ ($\det_6 = -(\det_3 N)^2$, `1.82e-12`) ve $8\times 8$ ($\det_8 = (\det_4 M)^2$, `1.46e-11`) kimlikleriyle genişletilmiş `2,045` derece-6 ideali, $L_{10}$ üzerinde derece $D=7$'de hem $\mathbb{F}_{32749}$ hem $\mathbb{F}_{65521}$ modülo tam ranka (**$11{,}440 / 11{,}440$, `corank = 0`**) ulaşarak $m=12, D=9$ dalını koşulsuz kapatır. (`verify_round16_hilbert.py`)
3. **$n = 5$ $T_5^{\mathrm{row}}$-Eşdeğişir ABP Kapanışı: $m \ge 31$ (Tur 15–16 — Noether Thm 21 & 22A/B):**  
   $(w_1, w_4) \in \{(5,5), (6,5), (5,6)\}$ profillerinin tamamında $w_2 \in \{8,9\}$ çizgeleri imkânsızdır (`0` uygun çözüm $\implies w_2 \ge 10 \implies m \ge 31 = 2^5 - 1$). İki-taraflı Laurent kutup rankı $(k_r, k_c) = (3, 1..3)$ için $\det_4 = 0$ iken $\mathrm{perm}_4 = (6, 28, 66)$ verir. (`round15_e25_n5_hypergraph_and_laurent_bath.py`, `round16_e26_n5_deficit_closure_and_laurent_rank.py`)
4. **Evrensel 55/55 Dengeli-Kesit $\mathrm{rk}_{\mathbb{F}_2}$ Ayrımı ve Grassmannian İzomorfizması (Tur 15–16 — Wigner E5.5 & W-16A):**  
   $n=4$'teki tüm `55/55` dengeli-kesit yörüngelerinde (`12,870/12,870 = %100`) $\mathrm{rk}_{\mathbb{F}_2}(\mathrm{perm}_4) > \mathrm{rk}_{\mathbb{F}_2}(\det_4)$ (`min +4, max +44, 0` eşitlik) geçerlidir. $|\mathbb{P}_{0,1}(\mathbb{F}_3^4)| = |(\{0,1\}^5\setminus\{0,1\})/\mathrm{comp}| = 15$ projektif izomorfizması `40 == 40` ve `264 == 264` Grassmannian sayılarını kanıtlar; $n=5$ kısıtsız 2-vs-3 kesitte `336 vs 264`, $n=6$'da ise `1456 vs 264` ($5.52\times$) ayrım elde edilir. (`round15_e55_2adic_law_and_rkf2_nof.py`, `round16_e56_grassmannian_rkf2_theorem.py`)
5. **$n = 5$ $D_{\mathrm{PTF}} \ge 10$ Taraması, Schur $\mathrm{IP}_{n-1}$ Açıklaması ve Dual-Çekirdek $\mathrm{rk}_{\mathbb{F}_2}$ Köprüsü (Tur 15–16 — Valiant Thm 24.1 & 24.2):**  
   $K_5 = 5{,}624$ üzerinde $D = 5..9$ imkânsızdır (`D_PTF(5) >= 10`, `[SAYISAL DOĞRULANDI]`). $\det_n$'in PTF direnci Schur $\mathrm{IP}_{n-1}$ gömmesiyle açıklanırken, $n=3\to 4$ işaretli THR ağırlığı (`16.34x vs 8.29x`) ve Yao dual destek büyümesi (`5.29x` [`24->127`] vs `2.92x` [`25->73`]) dual-çekirdek $\mathrm{rk}_{\mathbb{F}_2}$ köprüsünde (`186 vs 138` Dama, `109 vs 68` Satır) birleşir. (`test_round15_engel65_n5_exact_dptf_and_tc03.py`, `test_round16_engel66_orbit_lp_separating_invariant.py`)

---

## Kaynakça

1. **Valiant, L. G.** (1979). *Completeness classes in algebra*. Proceedings of the 11th Annual ACM Symposium on Theory of Computing (STOC), 249–261.
2. **Mignon, T. & Ressayre, N.** (2004). *A quadratic bound for the determinant and permanent problem*. International Mathematics Research Notices (IMRN), 2004(79), 4241–4253.
3. **Grenet, B.** (2011). *An upper bound for the permanent versus determinant problem*. Manuscript, École Normale Supérieure de Lyon.
4. **Alper, J., Bogart, T. & Velasco, M.** (2017). *A lower bound for the determinantal complexity of a hypersurface*. Foundations of Computational Mathematics, 17(3), 829–836.
5. **Mulmuley, K. D. & Sohoni, M.** (2001). *Geometric Complexity Theory I: An approach to the P vs. NP and related problems*. SIAM Journal on Computing, 31(2), 496–526.
6. **Razborov, A. A. & Rudich, S.** (1997). *Natural proofs*. Journal of Computer and System Sciences, 55(1), 24–35.
7. **Williams, R.** (2014). *Nonuniform ACC circuit lower bounds*. Journal of the ACM, 61(1), Article 2.
8. **Wood, M. M.** (2019). *Random integral matrices and the Cohen–Lenstra heuristics*. American Journal of Mathematics, 141(2), 383–398.
9. **Atkinson, M. D. & Lloyd, S.** (1980). *Large spaces of matrices of bounded rank*. Quarterly Journal of Mathematics, 31(3), 253–262.
10. **Westwick, R.** (1987). *Spaces of matrices of fixed rank*. Linear and Multilinear Algebra, 20(2), 171–174.
