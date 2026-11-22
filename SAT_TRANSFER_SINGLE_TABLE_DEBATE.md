# Tek Masa Tartışması: SAT ∉ P/poly İçin Süperpolinom Devre Alt Sınırları ve Cebirsel → Boolean Aktarım İlkesi

**Tarih:** 22 Kasım 2026  
**Katılımcılar (2 Kol, Tek Masa):**
- **0G Kolu (`0gm-1.0-35b-a3b`):** `0g-pisagor`, `0g-oklid`, `0g-arsimet`, `0g-gauss`, `0g-harezmi`, `0g-ramanujan`  
- **Swarm Konseyi (`gemini-4-hydrogen-high`):** `prof-euler`, `prof-strassen`, `prof-wigner`, `prof-hilbert`, `prof-noether`, `prof-valiant`

**Kaynak Kayıtlar:**
- Faz 1 (0G Açılış Tezleri): `council_0g/0G_SAT_TRANSFER_R1.md`
- Faz 2 (Swarm Konseyi Yanıtları & Karşı Soruları): Swarm Board `#146–#152`
- Faz 3 (0G Karşı Sorgulama & Final Yanıtları): `council_0g/0G_SAT_TRANSFER_R2.md`

---

## 1. Masanın Kurulumu ve Eşleşme Haritası

Kullanıcının beş temel sorusu şu şekilde birebir eşleştirilmiştir:

| Mesele | Odak Alanı | 0G Temsilcisi | Swarm Temsilcisi |
| :--- | :--- | :--- | :--- |
| **Mesele 1** | $\mathrm{SAT}\notin\mathrm{P}/\mathrm{poly}$ devre alt sınırı, Li–Yang ($3.1n-o(n)$) ve iç hat kodlaması | `0g-pisagor` | `prof-euler` |
| **Mesele 2** | Cebirsel $\to$ Boolean aktarım boşluğu, Bürgisser (GRH), Toda ($\mathrm{PH}\subseteq\mathrm{P}^{\#\mathrm{P}}$) ve PIT | `0g-oklid` | `prof-strassen` |
| **Mesele 3** | Temsil karmaşıklığı, $\mathrm{perm}_n\equiv\det_n \pmod 2$ çöküşü ve $I=\langle x_i^2-x_i\rangle$ ideal sınıfı | `0g-arsimet` | `prof-wigner` (+ `prof-noether`) |
| **Mesele 4** | Sabit-$n$'den ($\mathrm{dc}_{\mathbb{C}}(\mathrm{perm}_4)\ge 10$) asimptotik $|C_n|>n^k$'ya geçiş & Mignon–Ressayre $O(n^2)$ | `0g-gauss` | `prof-hilbert` |
| **Mesele 5** | Relativization, Algebrization ve Natural Proofs (GCT *largeness* vs Williams *constructivity*) | `0g-harezmi` | `prof-noether` & `prof-valiant` |
| **Sentez** | Genel bir aktarım ilkesi var mı; en gerçekçi ara hedef hangisi? | `0g-ramanujan` | Tüm Swarm Konseyi (sözcü `prof-valiant`) |

---

## 2. Konu Konu Tek Masa Diyaloğu (Faz 1 → Faz 2 → Faz 3)

### Mesele 1: Devre Alt Sınırı ($\mathrm{SAT} \notin \mathrm{P}/\mathrm{poly}$) — `0g-pisagor` $\times$ `prof-euler`

- **0G Açılışı (`0g-pisagor`, R1):** Genel Boolean devrelerde alt sınırın $\Omega(n)$ kaldığını öne sürdü (Li–Yang 2022 kaynağının literatürde yer almadığını iddia ederek) ve RR94 / AW08 bariyerleri nedeniyle ara kapıların kombinatoryal kodlamasını kırmak için *devre derinliği ile etkileşim grafiği kesme genişliği* arasında doğal-olmayan bir bağ önerdi.
  - *Soru:* Devre ailesinin simetri kırılımını ölçen, kriptografik varsayımlara bağımlı olmayan yeni bir yapısal invaryant tanımlanabilir mi?
- **Swarm Yanıtı (`prof-euler`, `#148`):**
  1. *Literatür düzeltmesi:* Li–Yang (STOC 2022) tam ikili tabanda $3.1n - o(n)$ kapı alt sınırını gerçekten kanıtlamıştır ($O(n)$ içinde, Blum $3n$'nin hafif üzerinde).
  2. *Kesme genişliği eleştirisi:* Valiant süper-yoğunlaştırıcıları ve sabit dereceli genişletici DAG'ları $O(n)$–$O(n\log n)$ kapıyla zaten $\Omega(n)$ kesme genişliğine ulaşır; sınırsız *fan-out* paylaşımı kapı sayısını kesitten koparır.
  3. *Simetri kırılımı eleştirisi:* *Largeness*'ı kıran invaryant tanımlanabilse bile ($S_n\times S_n$ altuzayı gibi), doğruluk tablosu üzerinde tanımlanırsa tek-yönlü fonksiyonlar altında sahte-rastgele asimetrik devrelerce atlatılır (RR97); devre içinde tanımlanırsa serbest DAG topolojisi yapay asimetriye kapı maliyeti ödetmez.
  - *Karşı Soru:* Sınırsız fan-out paylaşımını hangi ek topolojik veya cebirsel kısıt olmadan $\omega(n)$ kapı alt sınırına dönüştürebilirsiniz?
- **0G Final Yanıtı (`0g-pisagor`, R2):** Li–Yang (STOC 2022) düzeltmesini **kabul etti**. Euler'in eleştirisini haklı bularak kesme genişliğinin serbest $\mathrm{P}/\mathrm{poly}$'de yüksek fan-out nedeniyle bilgi akışını gizlediğini kabul etti; dönüşümün yalnızca **sabit fan-out + $O(\log n)$ derinlik + yerel cebirsel bağımsızlık** altında çalışacağını ve serbest $\mathrm{P}/\mathrm{poly}$'de topolojik olarak engellendiğini teslim etti.

---

### Mesele 2: Cebirsel $\to$ Boolean Aktarım Boşluğu — `0g-oklid` $\times$ `prof-strassen`

- **0G Açılışı (`0g-oklid`, R1):** Bürgisser (2000, GRH) $\mathrm{VP}_{\mathbb{C}}\neq\mathrm{VNP}_{\mathbb{C}}\implies\mathrm{P}^{\#\mathrm{P}}\not\subseteq\mathrm{P}/\mathrm{poly}$ ile Toda (1991) teoremi arasındaki uçurumda temel köprünün deterministik PIT / vuruş kümeleri (Kabanets–Impagliazzo / Nisan–Wigderson çerçevesi) olduğunu savundu; ancak metinde `NP ⊆ #P` ifadesi yer aldı.
  - *Soru:* Deterministik PIT derandomizasyonu olmadan permanent'ın cebirsel zorluğunu $\mathrm{SAT}\notin\mathrm{P}/\mathrm{poly}$'ye aktaran tek geçerli yapısal köprü nedir?
- **Swarm Yanıtı (`prof-strassen`, `#152`):**
  1. *Tip hatası düzeltmesi:* `#P` fonksiyon sınıfı, `NP` karar sınıfıdır; doğru kapsama Toda Teoremi $\mathrm{PH}\subseteq\mathrm{P}^{\#\mathrm{P}}$'dir. Tam da kapsamanın bu yönü yüzünden $\mathrm{VP}_{\mathbb{C}}\neq\mathrm{VNP}_{\mathbb{C}}$ bile $\mathrm{SAT}\notin\mathrm{P}/\mathrm{poly}$ vermez.
  2. *PIT-siz köprü yokluğu:* Literatürde deterministik PIT derandomizasyonu olmadan $\mathrm{VP}_{\mathbb{C}}\neq\mathrm{VNP}_{\mathbb{C}}$'den $\mathrm{SAT}\notin\mathrm{P}/\mathrm{poly}$ çıkaran **geçerli ve kanıtlanmış tek bir yapısal köprü yoktur**. Kabanets–Impagliazzo (2004) dahi $\mathrm{PIT}\in\mathrm{P}$'den yalnızca $(\mathrm{NEXP}\not\subseteq\mathrm{P}/\mathrm{poly} \lor \mathrm{perm}\notin\mathrm{VP})$ ikilemi verir.
  - *Karşı Soru:* Kesin sayma $\mathrm{NP}$'ye indirgenemediğine göre ($\mathrm{BPP}^{\mathrm{NP}}$ yalnızca Stockmeyer ile yaklaşık sayar), PIT derandomizasyonu olmadan bağ kurmak için hangi kanıtlanmamış *sayma-karar ters indirgemesini* varsaymak zorunda kalırsınız?
- **0G Final Yanıtı (`0g-oklid`, R2):** Her iki düzeltmeyi de **tamamen kabul etti**. PIT derandomizasyonu olmadan $\mathrm{VP}_{\mathbb{C}}\neq\mathrm{VNP}_{\mathbb{C}}\implies\mathrm{SAT}\notin\mathrm{P}/\mathrm{poly}$ bağlantısı için kanıtlanmamış bir `permanent mod p ∉ NP` tarzı tek-adımlı, uniform *sayma-karar ters indirgemesi* varsaymanın zorunlu olduğunu ve literatürde böyle bir köprünün bulunmadığını onayladı. *(Not: Çıktının son özet satırı token kesiminden ziyade son cümlede kısa kaldı, ancak tüm argüman eksiksiz verildi.)*

---

### Mesele 3: Temsil Karmaşıklığı & İdeal Belirsizliği — `0g-arsimet` $\times$ `prof-wigner` & `prof-noether`

- **0G Açılışı (`0g-arsimet`, R1):** $\mathrm{perm}_n \bmod 2 = \det_n \bmod 2 \in \mathrm{NC}^2$ çöküşünü ve $I=\langle x_i^2-x_i\rangle$ ideal sınıfında cebirsel boyutun Boolean zorluğu taşımadığını belirtti.
  - *Soru:* $I=\langle x_i^2-x_i\rangle$ sınıfında her $s$-boyutlu polinomun Boolean devre karmaşıklığını $\Omega(s^c)$ ile alt sınırlandıran, modüler indirgeme altında invaryant kalan tek ölçü nedir?
- **Swarm Yanıtları (`prof-wigner` `#151`, `prof-noether` `#149`):**
  1. *Böyle bir evrensel ölçünün yokluğu:* Modüler indirgeme ($\bmod\,2$) $\mathrm{perm}_n$'i doğrudan $\mathrm{NC}^2$'ye düşürdüğünden, tüm modüllerde invaryant kalan ve $s\to\Omega(s^c)$ aktaran tek bir ölçü **var olamaz**. Ayrıca her $s_B$-boyutlu Boolean devre zaten $O(s_B)$ cebirsel $f+g$ temsilcisi üretir; tersi ise geçerli değildir (*Simetri-Tersine Çevirme Tuzağı* ve Wood `0.439874` doygunluğu).
  2. *$\mathbb{F}_3$ ve $\mathbb{F}_2$ ayrımı:* $\det_4^2\bmod 3$ ve $\mathrm{perm}_4^2\bmod 3$, $\mathbb{F}_3[X]/I$'da özdeş derecede (`8`, `282` terim) olmasına karşın $\mathbb{F}_2$-ANF (`12` vs `15`) ve dengeli kesit $\mathrm{rk}_{\mathbb{F}_2}$'de (`55/55` yörünge) ayrışır; bunun kökü $\mathrm{GL}_n(\mathbb{F}_p)$ ayar simetrisidir ($p\neq 2$), ancak Boolean devre alt sınırına aktarımı `[AÇIK]`tır.
  - *Karşı Soru:* $p\neq 2$'de $\mathrm{GL}_n(\mathbb{F}_p)$ ayar kırılımı tek başına Boolean devre alt sınırı verebilir mi, yoksa Toda/algoritmik ikilik zorunlu mudur?
- **0G Final Yanıtı (`0g-arsimet`, R2):** Wigner'in $\bmod\,2$ ve $\mathbb{F}_2$-ANF/rank teşhisini **kabul etti**. Simetri kırılımının ($\mathrm{GL}_n(\mathbb{F}_p)$) tek başına Boolean devre alt sınırı veremeyeceğini, simetri temsilleri ile Boolean duyarlılığı bağlamak için Nisan–Wigderson veya Toda tipi yapısal/algoritmik ikiliğin **zorunlu** olduğunu savundu.

---

### Mesele 4: Asimptotik Genelleme & Mignon–Ressayre Tavanı — `0g-gauss` $\times$ `prof-hilbert`

- **0G Açılışı (`0g-gauss`, R1):** $\mathrm{dc}_{\mathbb{C}}(\mathrm{perm}_4)\ge 10$'dan $O(n^2)$ MR04 tavanını aşıp $|C_n|>n^k$'ya geçmek için tensör rank'ın asimptotik çarpım özelliği ile GCT yörünge kapanışı engellerinin birleşmesi gerektiğini öne sürdü.
  - *Soru:* Bu birleşimde henüz kanıtlanmamış temel cebirsel geometri koşulu nedir?
- **Swarm Yanıtı (`prof-hilbert`, `#147`):**
  1. *Çift Düzeltme:* (a) $\mathrm{dc}_{\mathbb{C}}(\mathrm{perm}_n)>n^k$ dahi doğrudan SAT devre boyutu vermez; (b) $\mathrm{perm}_n$ yörünge kapanışı Kronecker–plethysm simetrisi taşır, asimptotik tensör rank çarpımına indirgenmez. Üstelik **Bürgisser–Ikenmeyer–Panova (2019, BIP19)**, GCT'de **olay (occurrence) engellerinin** süper-polinom alt sınır veremeyeceğini kanıtlamıştır; yalnızca **çokluk (multiplicity) engelleri** açıktadır.
  2. *Gerekli koşul:* $\mathrm{Sing}_r$/Hessian yöntemleri $O(n^2)$'de durur. Bunu aşmak için $\mathbb{C}[\overline{\mathrm{GL}_{m^2}\cdot \det_m}]$ içinde **dolgu ($\ell^{m-n}\mathrm{perm}_n$) altında yok olmayan** çokluk engellerinin (veya düzleştirmeye indirgenmeyen yüksek syzygy/regülarite invaryantlarının) süper-polinom $m$'de varlığı gerekir — ve bu tamamen `[AÇIK]`tır.
  - *Karşı Soru:* Dolgu etkisinden ($\ell^{m-n}\mathrm{perm}_n$) kurtulmayı garanti eden tek bir cebirsel-geometrik mekanizma gösterebilir misiniz?
- **0G Final Yanıtı (`0g-gauss`, R2):** BIP19'un occurrence engellerini çökerttiğini ve yalnızca multiplicity engellerinin açık kaldığını **kabul etti**. Ikenmeyer–Panova (2018) ve BIP19 ışığında, **dolgu etkisini aşmayı garanti eden tek bir cebirsel-geometrik mekanizmanın bugün literatürde bulunmadığını** ("yanıt: yok") net biçimde teslim etti.

---

### Mesele 5: Üç Büyük Bariyer (Relativization, Algebrization, Natural Proofs) — `0g-harezmi` $\times$ `prof-noether` & `prof-valiant`

- **0G Açılışı (`0g-harezmi`, R1):** Asıl engelin RR97 olduğunu, GCT'nin *largeness*'ı, Williams meta-teoreminin ise *constructivity*'yi kırdığını belirterek pratikte Williams yolunun daha gerçekçi olduğunu savundu; kesişimde ortak bir "cebirsel-Boolean eşleme fonksiyonunun zorunlu karmaşıklık sınıfını" sordu.
- **Swarm Yanıtları (`prof-noether` `#149`, `prof-valiant` `#150`):**
  1. Her iki Swarm üyesi de **böyle bir "cebirsel-Boolean eşleme sınıfının" ne var olduğu ne de gerektiği** konusunda 0G ile ayrıştı: Williams yolu $\mathcal{C}$-SAT'ı $2^N/N^{\omega(1)}$'de çözmekten doğrudan $\mathrm{NEXP}\not\subseteq\mathcal{C}$ köşegenleştirmesine geçer; GCT ise $\mathbb{C}[X]$-yörünge kapanışında kalır.
  2. `prof-valiant`, kendi `E6.1–E6.2` yörünge-sıkıştırma sonuçlarının yalnızca simetrik/tek-katmanlı modelleri bağladığını; genel asimetrik $\mathrm{P}/\mathrm{poly}$-SAT hızlanmasının ve $\mathrm{NEXP}\to\mathrm{NP}$ inişinin hâlâ `[AÇIK]` olduğunu dürüstçe kaydetti.
  - *Karşı Sorular:* (`prof-noether`) Mod-2 çöküşü varken simetri kırılımını $\mathbb{F}_2$ Boolean devrelere taşıyacak karakteristik-bağımsız invaryant hangi nesne üzerinde kurulabilir? (`prof-valiant`) $\mathrm{NP}\not\subseteq\mathrm{TC}^0$ dahi kanıtlanmadan Boolean analizinden $\mathrm{VP}\neq\mathrm{VNP}$'ye hangi somut kısıt aktarılabilir?
- **0G Final Yanıtı (`0g-harezmi`, R2):** Ortak bir eşleme sınıfının **bulunmadığını kabul etti**. Motivik ölçüler veya Grothendieck halkası elemanlarının $\mathbb{F}_2$ Boolean devre simetri kırılımını taşımadığını, ayrıca $\mathrm{NP}\not\subseteq\mathrm{TC}^0$ kanıtlanmadan Boolean analizinden $\mathrm{VP}\neq\mathrm{VNP}$'ye somut kısıt aktarımının imkânsız göründüğünü belirtti.

---

### Final Sentezi: Aktarım İlkesi Var mı? — `0g-ramanujan` $\times$ `prof-valiant` (ve Tüm Konsey)

- **Ortak Zemin (R1 + `#150` + R2):** Tüm 12 temsilci (6 0G + 6 Swarm) şu ana yargıda birleşti:
  > **Bugünkü matematikte, cebirsel karmaşıklıktaki ($\mathrm{VP}/\mathrm{VNP}, \mathrm{dc}, \mathrm{ABP}$) alt sınırları doğrudan ve genel olarak $\mathrm{SAT}\notin\mathrm{P}/\mathrm{poly}$ sonucuna dönüştüren bir aktarım ilkesi MEVCUT DEĞİLDİR.**
- **Fay Hattı / Öncelik Farkı:**
  - `0g-ramanujan` (R2), önümüzdeki 10 yılda ilk kırılması daha olası cephe olarak **$\mathrm{TC}^0$ alt sınırlarını** *(not: R2 metninde notasyonu ters olarak `TC^0 ⊄ NP` yazsa da kastettiği açık problem $\mathrm{NP}\not\subseteq\mathrm{TC}^0$ / Williams sonrası öğrenme–PRG köprüleridir)* öne çıkarırken; Mignon–Ressayre $O(n^2)$ cebirsel tavanının mod-2 çöküşü ve karakteristik bağımlılığı nedeniyle daha dirençli kalacağını savundu.
  - `prof-valiant` ve Swarm Konseyi ise iki hedefin **birbirine indirgenemeyen bağımsız duvarlar** olduğunu vurguladı: $\mathrm{TC}^0$ cephesinde Williams + yörünge-LP, cebirsel cephede ise $O(n^2)$ Mignon–Ressayre üstü syzygy/GCT çokluk engelleri kendi başlarına somut basamaklardır; biri diğerini otomatik çözmez.

---

## 3. Fikir Birliği Matrisi (Konsensüs)

| Konu | Ortak Hüküm |
| :--- | :--- |
| **$\mathrm{SAT} \notin \mathrm{P}/\mathrm{poly}$ durumu** | Genel Boolean devrelerde bilinen en iyi açık alt sınır lineerdir ($3.1n-o(n)$, Li–Yang STOC 2022); $\mathrm{P}\neq\mathrm{NP}$ / $\mathrm{SAT}\notin\mathrm{P}/\mathrm{poly}$ tamamen `[AÇIK]`. |
| **Genel Cebirsel $\to$ Boolean Aktarım** | Bugün böyle bir aktarım teoremi **yoktur**. Bürgisser (GRH) $\mathrm{P}^{\#\mathrm{P}}$ verir; Toda ($\mathrm{PH}\subseteq\mathrm{P}^{\#\mathrm{P}}$) yönü nedeniyle $\#\mathrm{P}$'den $\mathrm{NP}$'ye iniş kapalıdır; Kabanets–Impagliazzo yalnızca PIT derandomizasyonu ile $\mathrm{NEXP}$'e bağlanır. |
| **İdeal $\langle x_i^2-x_i\rangle$ ve $\bmod\,2$ Çöküşü** | $\mathrm{perm}_n\equiv\det_n\pmod 2 \in \mathrm{NC}^2$ nedeniyle her modülde invaryant kalıp $s\to\Omega(s^c)$ Boolean alt sınır zorlayan tek bir evrensel ölçü **yoktur**. |
| **GCT & Asimptotik Genelleme** | BIP19 ile *occurrence* engelleri elenmiştir; açık kalan *multiplicity* engellerinde $\ell^{m-n}\mathrm{perm}_n$ dolgusunu aşmayı garanti eden tek bir mekanizma henüz bilinmemektedir. Sabit-$n$ tekillik/Hessian yöntemleri MR04 $O(n^2)$ tavanında durur. |
| **Ortak Bariyer Stratejisi** | Ya Williams tarzı algoritma $\Rightarrow$ alt sınır (*constructivity* kırılımı) ya da sıfır-olmayan yörünge-dışı simetri kırılımı (*largeness* kırılımı) şarttır; birleşik "eşleme karmaşıklık sınıfı" kanıtsızdır ve gerekmez. |

---

## 4. Aktif Fay Hatları (Kalan Uyuşmazlıklar)

1. **10 Yıllık Kırılma Önceliği:** `0g-ramanujan`, öğrenme teorisi / PRG entegrasyonu nedeniyle sabit-derinlikli Boolean cephenin ($\mathrm{NP}\not\subseteq\mathrm{TC}^0$ / $\mathrm{NEXP}\not\subseteq\mathrm{TC}^0$) cebirsel $O(n^2)$ tavanından daha önce kırılacağını öngörürken; Swarm Konseyi ($\mathrm{dc}_{\mathbb{C}}(\mathrm{perm}_4)$ ve IMSC/yörünge-LP bulgularına dayanarak) her iki duvarın kendi iç dinamiklerine sahip olduğunu ve birbirine tercüme edilmeden bağımsız ilerleyebileceğini savundu.
2. **Simetrinin Rolü:** `0g-arsimet` ve `0g-pisagor` simetri kırılımı / kesme genişliğinin yalnızca sıkı topolojik-derinlik kısıtları (sabit fan-out, $O(\log n)$ derinlik) ve Toda/NW çerçevesiyle anlamlı kaldığını kabul etmekle birlikte bu yönde arayışı sürdürmekte; `prof-noether` ve `prof-euler` ise serbest DAG paylaşımının ("yapay asimetri bedelsizliği") ve Simetri-Tersine Çevirme Tuzağı'nın bu yolu yapısal olarak kilitlediğini vurgulamaktadır.

---

## 5. Yanlışlanabilir ve Somut Sonraki Alt-Problemler

Doğrudan "$\mathrm{P}\neq\mathrm{NP}$" veya "genel aktarım teoremi" peşinde koşmak yerine, bu tartışmadan çıkan üç temiz, matematiksel olarak test edilebilir ara hedef şunlardır:

1. **Boolean / $\mathrm{TC}^0$ Cephesi:** Williams algoritma-alt sınır köprüsünü ve yörünge-LP / iletişim-rankı araçlarını birleştirerek $\mathrm{NEXP}\not\subseteq\mathrm{TC}^0$ (veya kısıtlı genişlikteki $\mathrm{TC}^0_3$ devreleri için $\mathrm{perm}_n \bmod 3$ alt sınırı) üzerine ilerlemek — $\mathrm{GL}_n(\mathbb{F}_3)$ vs $S_n\times S_n$ ayrışmasının çok-katmanlı dağılım altuzaylarında nasıl eridiğini veya korunduğunu kanıtlamak.
2. **Cebirsel Cephe (Mignon–Ressayre Üstü):** $\mathbb{C}^{n^2}$ ortamında $\mathrm{Sing}_k$ ve Hessian düzleştirme tavanı olan $O(n^2)$'yi aşmak için, kaydırılmış kısmi türevler / yüksek syzygy veya dolgu-dirençli GCT çokluk engelleri üzerinden süper-kuadratik ($\mathrm{dc}(\mathrm{perm}_n) \ge n^{2+\varepsilon}$ veya $\underline{\mathrm{dc}}$ üzerinde) yeni bir aile inşası aramak; sabit-$n$'de ise $m=12, D=8$ ($\mathcal{H}_{\le 6}$) ve $\underline{\mathrm{dc}}(\mathrm{perm}_4)$ sınırını netleştirmek.
3. **Sayısal / İşaretli Aktarım Denetimi (`#P` vs `NP` Köprüsü Yerine Mod-$p$ Kriteri):** $\mathrm{VP}\neq\mathrm{VNP}\Rightarrow\mathrm{SAT}\notin\mathrm{P}/\mathrm{poly}$ aramak yerine, PIT derandomizasyonu olmadan hangi özel Boolean devre ailelerinin (ör. sabit derinlik + mod kapıları) yüksek cebirsel temsil sınıfını zorlayabildiğini — özellikle $\bmod\,3$ altında $I=\langle x_i^2-x_i\rangle$ denklik sınıfı minimumunun alt sınırlarını — bağımsız incelemek.
