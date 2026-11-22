# 0G Konseyi — Nicel Aktarım Teoremi Tur 1 (AC(f_n) ≥ 2^{n^ε} → SAT)

## 0g-pisagor (Alt Soru 1: İndirgemenin Koruması Gereken Bilgiler)

$f_n \to \text{SAT}$ indirgemesi, cebirsel zorluğu Boolean yapıya aktarmak için şu korumaları sağlamalıdır:
1. **Sayma/Parsimony:** İndirgeme, $\phi_n$'nin tatmin edici atamalarının sayısını $f_n$'ye doğrudan eşlemeli veya mod $p$'de korumalıdır ($|\text{Sat}(\phi_n)| \equiv f_n \pmod p$). Karar (NP) indirgemeleri sayma yapısını kaybeder; #P zorluğu aktarılamaz.
2. **Mod-p/Algebraic Koruma:** Valiant'ın VNP/VP ayrımı gereği, indirgeme derecesi ve çarpan yapısını korumalıdır. Parsimonyen indirgemeler, cebirsel polinomun katsayılarını Boolean değişkenlere doğrusal eşler.
3. **Promise/İzolasyon:** Valiant-Vazirani, benzersiz çözüm garantisi verir ancak cebirsel zorluğu (derece/altyapı) korumaz; sadece karar sorusunu daraltır.
4. **Turing/Cook Yetersizliği:** Adaptif sorgular, cebirsel yapıyı parçalayır. Toda'nın $PH \subseteq P^{\#P}$ sonucu, saymayı karar üstüne kurar ancak alt sınır kanıtı için gerekli olan tek-seferlik, yapıyı koruyan (non-adaptive, parsimony) eşlemeyi sağlamaz.
Gerekli koşul: İndirgeme, $f_n$'nin derecesini ve mod $p$ sayısını koruyan, adaptif olmayan, parsimonyen bir CNF dönüşümü olmalıdır.
TEOREM KOŞULU: $f_n \to \text{SAT}$ indirgemesi, $|\text{Sat}(\phi_n)| \equiv f_n \pmod p$ eşitliğini ve $\deg(\phi_n) = \deg(f_n)$ yapısını koruyan tek-seferlik, adaptif olmayan bir parsimonyen eşleme değilse, $AC(f_n) \ge 2^{n^\epsilon}$ alt sınırı SAT devre alt sınırına aktarılamaz.

---

## 0g-oklid (Alt Soru 2: Alan Değişimi — C → Qbar → Z → F_p → F_2)

$AC_{\mathbb{C}}(f_n) \ge 2^{n^\epsilon}$ alt sınırı, $\mathbb{C} \to \overline{\mathbb{Q}} \to \mathbb{Z} \to \mathbb{F}_p \to \mathbb{F}_2 zincirinde doğrusal aktarım göstermez. Transandantal katsayıların sabit eleme (specialization) işlemi, $f_n$'in $\mathbb{F}_p$'de indirgenmiş formunun katsayı yüksekliği $H$'ye bağlı olarak $AC_{\mathbb{F}_p}(f_n \bmod p) \ge AC_{\mathbb{C}}(f_n) - O(\log H)$ eşitsizliğini sağlar; $H$ üstel ise alt sınır çöker. GRH altında $p \le O(\log^2 n)$ seçimi, CRT yeniden inşasında $O(n \log n)$ bit maliyeti ekler; bu, $\mathbb{C}$ alt sınırını $\mathbb{F}_p$'de korumak için yeterlidir ancak $f_n$'in indirgenmiş kök yapısını bozmaz. Char=2 çöküşü ($\text{perm}_n \equiv \det_n \pmod 2$), $\text{perm}_n$'in $\mathbb{F}_2$'de $\text{NC}^2$'ye düşmesine neden olur; bu, $\mathbb{C}$'deki $\#P$-tamamlılık ile uyumsuzdur ve nicel kayıp değil, yapısal çöküştür. Asimetri: $\mathbb{C} \to \mathbb{F}_p$ indirgeme, $AC_{\mathbb{F}_p}(f \bmod p) \le AC_{\mathbb{C}}(f) + O(1)$ ile sadece alt sınır düşürür; $\mathbb{F}_p \to \mathbb{C}$ yükseltme, $AC_{\mathbb{C}}(f) \ge AC_{\mathbb{F}_p}(f) - O(\log p)$ ile alt sınırı korur ancak $f$'in $\mathbb{F}_p$'de indirgenmemiş olması gerekir.

TEOREM KOŞULU: $AC_{\mathbb{C}}(f_n) \ge 2^{n^\epsilon}$ alt sınırı, $f_n$'in $\mathbb{F}_p$'de indirgenmiş formunun katsayı yüksekliği $H \le 2^{n^{o(1)}}$ ve $p \nmid \text{disc}(f_n)$ koşulları altında $AC_{\mathbb{F}_p}(f_n \bmod p) \ge 2^{n^\epsilon - o(1)}$ eşitsizliğini sağlar; aksi halde çöküş kaçınılmazdır.

---

## 0g-arsimet (Alt Soru 3: Booleanlaştırma Sırasında Derece ve Boyut Dinamiği)

Boolean→aritmetik dönüşümde AND $\mapsto xy$, NOT $\mapsto 1-x$, OR $\mapsto x+y-xy$ uygulanır. Her AND/OR katmanı derecesini 2 ile çarpar; $D_B$ derinlikte formal derece $d_{\text{formal}} \le 2^{D_B}$ olur. $I=\langle x_i^2-x_i\rangle$ idealine göre modüler çokdoğrusallaştırma, her değişkenin derecesini 1’e indirger; böylece fonksiyonel derece $d_{\text{func}} \le n$ (değişken sayısı) kalır. Formal vs fonksiyonel alt sınır farkı, idealin $x_i^2-x_i$ ile bölümünün semantik davranışı koruyup sentaktik yapıyı değiştirmesinden kaynaklanır. Forbes–Kumar–Saptharishi (2016) örneği, fonksiyonel alt sınırların $d_{\text{func}}$ üzerinden kurulmasını gerektirdiğini, ancak aritmetik devre modellerinin formal dereceye dayandığını gösterir. Nicel ilişki: $d_{\text{formal}} \le 2^{D_B}$, $d_{\text{func}} \le \min(n, d_{\text{formal}})$, gap $\ge 2^{D_B}/n$. Çokdoğrusallaştırma, her kapı sonrası $I$ ile indirgeme yapıldığında dereceyi $\le n$’de tutar; aksi halde formal patlama devam eder.

TEOREM KOŞULU: $\deg_{\text{formal}}(\mathcal{C}) \le 2^{D_B}$ ve $\deg_{\text{func}}(\mathcal{C}) \le n$ eşzamanlı sağlanır iff her kapı çıktısı $I=\langle x_i^2-x_i\rangle$ idealine göre tam çokdoğrusal indirgeyici ile normalize edilir; aksi halde $\deg_{\text{formal}}(\mathcal{C}) \ge 2^{D_B}$ üstel patlar.

---

## 0g-gauss (Alt Soru 4a: Nicel Eşikler — AC(f_n) >= 2^{n^eps} Ne Zaman Hayatta Kalır?)

$AC_F$ veya sabit derinlik aritmetik alt sınırı $S_{\text{arith}} \ge 2^{n^\epsilon}$, Booleanizasyon sonrası $|C_n| \ge 2^{n^{\epsilon'}}$ kalıcılığı için gerekli: $p = 2^{O(n^\delta)}$ ile $\delta < \epsilon$ ve $D_{\text{arith}} = O(1)$. Yeterli: $\epsilon' = \epsilon - \delta > 0$. Boolean boyut $|C_n| \le S_{\text{arith}} \cdot \text{poly}(\log p)$, derinlik $D_B \le D_{\text{arith}} \cdot \log p + O(1)$. Süperpolinom $n^{\omega(1)}$ için $\delta < \epsilon$ yeterlidir. Çökme rejimi: $\log p \ge n^\epsilon$ veya $D_B = \omega(\log n)$ olduğunda, Boolean devre sabit derinlik sınıfından çıkar ve alt sınır anlamsızlaşır. $p$ üstel ise $|C_n|$ üstel patlar, indirgeme triviyalize olur.

TEOREM KOŞULU: $\log p = o(n^\epsilon) \land D_{\text{arith}} = O(1) \implies |C_n| \ge 2^{n^{\epsilon-\delta}}$; aksi halde $D_B = \omega(\log n)$ ile alt sınır çöker.

---

## 0g-harezmi (Alt Soru 4b: Bilinen İspat Bariyerleriyle Uyum)

Bariyerler, belirli kanıt tekniklerinin sınırlarını gösterir; teoremin çelişmemesi için bu teknikler kullanılmamalıdır. Koşullu aktarım, derandomizasyon hipotezleri veya cebirsel zorluktan rastgeleliğe dönüşüm şemaları üzerinden kurulur; bu şemalar oracle bağımlı değildir. AC(f_n) ≥ 2^{n^ε} alt sınırının doğal olmaması, verimli hesaplanabilen doğal özelliklerle yakalanamayacağı anlamına gelir; bu durum, teoremin relativize/algebrize olup olmamasından bağımsızdır. Relativize/algebrize durumu kanıt metodunun oracle sabitliğini, doğal olmama ise alt sınırın yapısal direncini ifade eder. Aktarım için gerek koşul: ∃ oracle-free indirgeme R s.t. H(f) → L(f). Yeterli koşul: R’nin doğruluğu NEXP ⊄ P/poly varsayımına dayanır.

TEOREM KOŞULU: Aktarım, oracle bağımlı kanıt teknikleri kullanılmadıkça ve alt sınır doğal özelliklerle tanımlanmadıkça geçerlidir.

---

## 0g-ramanujan (Sentez: Koşullu Nicel Aktarım Teoremi & En Keskin Karşı-Örnek)

H1: f_n ∉ AC^0 (derinlik/kapasite sınırı kırık). H2: f_n, ε-özlü dağılımdan ayrışır. H3: f_n, polinom zamanlı öğrenilemez (PAC/VC boyutu sınırlı değil). H4: f_n, formel polinom derecesi Ω(n^δ) ile alt sınırlandırılır.

AC(f_n) ≥ 2^{n^ε} ⇒ SAT için Ω(2^{cn}) alt sınırı, H1–H4 birlikte sağlandığında geçerlidir. H1 düşerse: perm_n mod 2 (AC^0'da düşük devre, SAT'ta üst sınır yok). H2 düşerse: düşük fonksiyonel karmaşıklıklı yüksek dereceli formel polinom (özlülük ihlali, transfer kopar). H3 düşerse: P^#P ⊇ NP varsayımı altında sahte alt sınır üretimi. H4 düşerse: düşük formel dereceli fonksiyonlar (örn. iç çarpım) AC üst sınırını aşsa da SAT transferi imkânsızdır.

TEOREM KOŞULU: AC(f_n) ≥ 2^{n^ε} ∧ H1∧H2∧H3∧H4 ⇒ SAT için Ω(2^{cn}) alt sınırı, aksi halde transfer imkânsızdır.

---
