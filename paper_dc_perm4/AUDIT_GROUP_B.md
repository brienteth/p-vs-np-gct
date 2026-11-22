# GRUP B ('Doğrulama ve Yayın Hazırlığı' — 12 Ajan, 4 Tur) Denetim Dosyası

## Tur 1 — Bağımsız Okuma (10 Uzman)

### B-hesaplamalı-cebir
- **M2 `permanent` belirsizliği ve açık toplam gerekliliği:** `README.md` içindeki Macaulay2 örneğinde `permanent X` fonksiyonunun çekirdekte varlığı doğrulanmamıştır [LİTERATÜR-DOĞRULANMADI]. M2, Singular ve Sage betiklerinde `perm_4` açık permütasyon toplamıyla tanımlanıp `L_8` üzerinde derece $D=9$ Hilbert fonksiyonunun sıfırlandığı ayrıca doğrulanmalıdır [SANI].

- **`perm_3` pozitif kontrolü eksik:** `verify_codim_sing_perm4.py` yalnız `L_8` (pozitif) ve `L_9` (negatif) testlerini içerir; $\codim_{\mathbb{C}^9}(\Sing(V(\perm_3))) = 6$ pozitif kontrolü eksiktir [KESİN HESAP]. Hem Python IMSC betiğine hem harici CAS doğrulama planına $6$-boyutlu altuzayda `perm_3` tam rank testi eklenmelidir [SANI].

- **Tek altuzay ve tek motor bağımlılığı:** Teorem 3.1 tek bir sabit tohumlu (`2026`) $L_8$ altuzayına ve yalnız Python IMSC uygulamasına dayanmaktadır [KESİN HESAP]. Singular (`std`, `dim`), Macaulay2 (`gb`, `codim`) ve SageMath ile hem `L_8` hem çoklu rastgele $L_8^{(k)}$ altuzayları bağımsız test edilmelidir [SANI].

- **Sonlu cisimden $\mathbb{C}$'ye aktarım farkı:** `L_8` üzerinde `corank = 0` mod $p$ sonucu, sıfır olmayan bir tam sayı minörü üzerinden $\mathbb{C}$'de $\codim \ge 8$ sınırını kanıtlar [İSPAT]. Buna karşın `README.md`'deki `ZZ/32749` üzerinde doğrudan `codim J` çıktısı tek başına `L_8` sertifikasının yerini tutmaz [İSPAT].

- **Aktarım çerçevesinin yeri:** `QUANTITATIVE_TRANSFER_THEOREM_SYNTHESIS.md` içindeki `H1–H4` çerçevesi sabit $n=4$ hesaplamalı cebir sertifikasından bağımsızdır [İSPAT]. Makalede ayrı bir sonuç yerine `H1` ve `H4` açıklarını vurgulayan kısa bir motivasyon/tartışma bölümüne konmalıdır [SANI].

### B-sayılar-kuramı
1. **Tek Asal Yeterliliği ve İki Asalın Rolü:** Tamsayı $M_9(I)$ matrisinde tek bir asalda bile $\mathbb{F}_p$-tam sütun rankı $\mathbb{Q}$-tam sütun rankını zorunlu kılar; kötü indirgeme yalnızca rank düşürür, yapay tam rank üretmez `[İSPAT]`. Dolayısıyla $p_1=32749$ ve $p_2=65521$ seçimi kötü indirgeme olasılığını azaltmak için değil, yalnızca aritmetik/kod hatasına karşı çapraz kontrol sağlar; Teorem 3.1 metni bunu netleştirmelidir `[İSPAT]`.

2. **IMSC Çarpımında Eksik Taşma ve Asallık Denetimi:** `rref_mod_p_exact` yalnızca `block_size * (p - 1)^2 < 2^53` koşulunu denetlerken, `step_imsc` içindeki `R_canon @ C_s` matris çarpımının iç boyutu `n_S` için sınır kontrolü yapmaz `[KESİN HESAP]`. $D=6\to 7$ adımında $|S_7| \le 8 \times 132 = 1056$ olup $1056 \cdot 65520^2 \approx 4{,}53 \times 10^{12} < 2^{53}$ sağlanır; yine de `n_S` taşma sınırı ve `pow(..., p - 2, p)` öncesi $p$ asallık denetimi koda eklenmelidir `[KESİN HESAP]`.

3. **$L_8$'de Sıfıra Bölme ve Rank Koşulu:** `rref_mod_p_exact` yalnızca mod $p$ sıfır olmayan pivotları seçtiğinden asallık altında sıfıra bölme oluşmaz `[İSPAT]`. $I_9 \otimes \mathbb{F}_p = R_9 \otimes \mathbb{F}_p$ sağlanması $\ker(M_{L_8}) = \{0\}$ olmasını zorunlu kılar; ancak tekrarlanabilirlik için $M_{L_8}$, `default_rng(2026)` yerine makalede açık tamsayı matrisi olarak verilmelidir `[İSPAT]`.

4. **Doğrulama Kontrol Eksikleri:** $\perm_3$ için $\codim \Sing = 6$ pozitif kontrolü betikte eksiktir; $L_9$ negatif kontrolü de yalnızca `P1` ve $D \le 7$ için çalıştırılmıştır `[KESİN HESAP]`.

5. **Aktarım Özeti:** Özet belgedeki H1–H4 koşulları asimptotik $2^{n^\varepsilon}$ alt sınırlarına yöneliktir ve sabit $n=4$ $\perm_4$ kanıtıyla doğrudan mantıksal bağ kurmaz; aktarım ve literatür iddiaları birincil kaynaklardan teyit edilmelidir `[LİTERATÜR-DOĞRULANMADI]`.

### B-cebirsel-karmaşıklık
- **Literatür konumlandırması doğrulanmamış:** Makaledeki MR04 ($n^2/2=8$), ABV17 ($\mathrm{codim}\,\mathrm{Sing}+1$), Yabe 2015 ($\mathbb{R}$ üzerinde $(n-1)^2+1=10$), Grenet 2011 ($\le 15$) ve Landsberg–Ressayre 2017 ifadeleri birincil kaynaklardan kontrol edilmemiştir; ayrıca Sheshadri 2026 gibi $\mathrm{dc}_{\mathbb{C}}(\mathrm{perm}_4)$ üzerine olası güncel yayınların varlığı bilinmemekte olup birincil kaynaktan kontrol edilmelidir [LİTERATÜR-DOĞRULANMADI].
- **$r=3$ sınıflandırmasında eksik tip:** Prop. 4.1'de rank $\le 2$'lik $3\times 3$ uzaylar için yalnızca sıfır satır ve çarpık-simetrik tipleri verilmiş, $\mathrm{GL}_3\times\mathrm{GL}_3$ ve devrik altında eşlenemeyen $2\times 2$ sıfır alt bloklu sıkıştırma tipi atlanmıştır; ancak bu tipte $\adj(B) = (0,-c,b)^T(0,e,-d)$ biçiminde çarpanlara ayrıldığından $\str(\mathrm{perm}_4) \le 1 < 4$ çelişkisiyle elenir [İSPAT].
- **Sınır karmaşıklığı ($\underline{\mathrm{dc}}$) ve GCT ayrımı:** İspat sabit $A_0$ matrisli $\det(A_0+L(X))$ temsillerine, dolayısıyla $\mathrm{dc}_{\mathbb{C}}(\mathrm{perm}_4)$'e uygulanır; oysa GCT bağlamındaki sınır determinantal karmaşıklığı $\underline{\mathrm{dc}}_{\mathbb{C}}(\mathrm{perm}_4)$ için $A_0$ normunun sınırsız büyüdüğü dejenerasyonlar bu sınıflandırmayla elenmez [İSPAT].
- **$m \ge 10$ bariyeri:** Remark 5.2'de belirtildiği üzere $m \ge 10$ durumunda $w_{\mathrm{mid}} \ge 1$ bloğu ortaya çıktığından mevcut argüman $\mathrm{codim}(\Sing_2)=12$ yerine Hessian rank $\le 2w_{\mathrm{mid}}$ katmanlarına ihtiyaç duyar ve $O(n^2)$ MR engelini aşmaz [İSPAT].
- **Boolean/SAT aktarım metni kapsam dışı:** Özetlenen koşullu aktarım çerçevesi asimptotik $2^{n^\varepsilon}$ ölçeğinde ve $I_B$ modülo fonksiyonel alt sınır (H1) talep ederken, makale sabit $n=4$ boyutunda biçimsel $\mathrm{dc}_{\mathbb{C}}(\mathrm{perm}_4)\ge 10$ kanıtlamaktadır [İSPAT]. Bu nedenle aktarım tartışması makalede en fazla kısa bir motivasyon notuyla sınırlandırılmalıdır [SANI].

### B-lineer-cebir
- **$r=3$ vaka analizi eksik ama onarılabilir:** `prop:corank1` içindeki $r=3$ vakası $3\times 3$ sınırlı ranklı uzayları yalnız "sıfır satır" ve "çarpık-simetrik" olarak ikiye ayırıyor; oysa $2\times 2$ sıfır bloklu $(1,1)$-sıkıştırma tipi $\mathrm{GL}_3 \times \mathrm{GL}_3$ ve devrik altında bunlara eşdeğer değildir [İSPAT]. Bu blok için $\operatorname{adj}(B) = (0, b_2, -b_1)^T(0, -c_2, c_1)$ olup $\perm_4 = -\operatorname{tr}(\operatorname{adj}(B)UV)$ ifadesi $\str(\perm_4) \le 2 < 4$ verir ve çelişki korunur [İSPAT].
- **Diğer $r$ vakaları, `prop:sing2` ve Theorem 1.1 sağlam:** Yeniden türetmede $r=0,2,4,\ge 5$ elemeleri, $\codim \Sing_2 = 12$ hesabı, $\Omega$-izotropi ($\dim W = 8$), $2$-blok normal form ($u_1 = Ky$), $[t^3]=0$'dan $\xi$-lineer ayrıştırma, Skew-Square Lemması ($(M^2K)^T = -M^2K$) ve $\perm_4 \in I_W^3$ çıkarımı tutarlıdır [İSPAT].
- **Sınır durumu ($d_v \ge 1$) açık yazılmalı:** Step 2'de $d_v = 0$ hâlinin $v \equiv 0 \implies \perm_4 \equiv 0$ ile elendiği kısaca not edilmelidir [İSPAT].
- **Hesapsal doğrulama eksikleri:** `verify_codim_sing_perm4.py` yalnız $L_8$ ve $L_9$ üzerinde IMSC çalıştırıyor; `perm_3` için $\codim \Sing = 6$ pozitif kontrolü eksiktir [SANI]. `README.md` içindeki M2 `permanent` komutu doğrulanmamıştır [LİTERATÜR-DOĞRULANMADI].
- **Literatür ve aktarım bölümü:** Yabe (2015), ABV (2017), MR (2004), LR (2017) ayrıntıları ile Sheshadri (2026) benzeri olası yayınların varlığını bilmiyorum, birincil kaynaktan kontrol edilmeli [LİTERATÜR-DOĞRULANMADI]. Aktarım teoremi ayrı sonuç değil, H1 ve H4 açık vurgulu kısa Tartışma notu olmalıdır [SANI].

### B-mantık-ispat
1. **$r=3$ vaka eksikliği (Prop. 4.1):** Makale $\rank \le 2$ olan $3\times 3$ lineer uzayları yalnızca sıfır satır ve $\mathfrak{so}_3$ ile sınırlar; $2\times 2$ sıfır bloklu sıkıştırma tipi eksiktir (`Atkinson1983`/`EH1988` sınıflandırması birincil kaynaktan kontrol edilmelidir [LİTERATÜR-DOĞRULANMADI]). Ancak $B$’de $2\times 2$ sıfır blok varken $\adj(B) = (0,-e,d)^T(0,c,-b)$ bulunur; böylece $\perm_4 = -\tr(\adj(B)UV) = -c(UV)_{2,\cdot}(0,-e,d)^T + b(UV)_{3,\cdot}(0,-e,d)^T$ olup $\str(\perm_4) \le 2 < 4$ çelişkisiyle kapanır (sıfır sütun ise devrikle sıfır satıra iner) [İSPAT].

2. **Koni varsayımı ve jeneriklik (Teorem 3.1, Remark 3.2):** Açık tam sayılı $L_8$’de $\Sing(V(\perm_4)) \cap L_8 = \{0\}$ elde edilmesi, her iki küme orijinden geçen koni olduğundan kesişimin boş kalmamasını garantiler ve afin boyut teoremini jeneriklik gerekmeden geçerli kılar; bu koni adımı metne açıkça yazılmalıdır [İSPAT]. Remark 3.2’de "generic $L_9$" denip belirli bir tam sayılı $L_9$ kullanılması terminolojik tutarsızlıktır (koni kesişimi zaten her $9$-boyutlu altuzayda $\ge 1$ boyutludur) [İSPAT].

3. **IMSC $\to$ Nullstellensatz köprüsü (Teorem 3.1):** $M_{\mathrm{syz}}$ tam rankının $S_9 \subseteq I_9 \otimes \mathbb{F}_p$, dolayısıyla $M_9(I) \bmod p$ tam sütun rankı ve $\mathbb{Z} \to \mathbb{C}$ Nullstellensatz kapanışını verdiği mantıksal olarak doğrudur, ancak $I_{D+1}=\sum t_i I_D$ eşitliğinin $D=6$ indirgemesiyle nasıl tam $M_9(I)$ rankına bağlandığı tek cümlede netleştirilmelidir [İSPAT].

4. **Sınır vakaları ve döngüsellik:** $m<9$ için birim blok ekleme (`padding`) $\corank(A_0)$ değerini değiştirmez [İSPAT]. Adım 2’de $d_v=0$’ın $\perm_4 \equiv 0$ ile elendiği ve $d_z=0$’da boş blokların sıfır kabul edildiği belirtilmelidir; teoremler arası akışta döngüsellik yoktur [İSPAT].

5. **Aktarım teoremi:** Sabit $n=4$ alt sınırı ile asimptotik $2^{n^\varepsilon}$ ve açık H1/H4 gerektiren aktarım teoremi mantıksal olarak birleştirilemez; en fazla tartışma bağlamında anılabilir [İSPAT].

### B-yazım-editörü
- **LaTeX ve notasyon tutarsızlıkları [İSPAT]:** Özette geçen $A_{11}(X_0)K$ ifadesindeki $X_0$ metinde tanımsızdır (Step 3–4'te $A_{11}^{(\xi)}(\xi)$ kullanılır). Step 2'de $2$-bloklu matris $A_{11}, A_{13}, A_{31}, A_{33}$ diye numaralanmıştır ($2$ indisi atlanmaktadır). Ayrıca $\adj(B)$ (özellikle $r=3$ vakasındaki $e_3^T$ uyumu için kofaktör devriği konvansiyonu), $\tr$ ve $\mathfrak{so}_d(\mathbb{C})$ tanımlanmamış; alt matris için $X_{\{...\}}$ (`prop:sing2`) ve $X_{\hat{1},\hat{j}}$ (`thm:sing1`) karışık yazılmıştır.
- **Yayın yer tutucuları ve doğrulama eksikleri [KESİN HESAP]:** Makalede `\author{[Author Name(s) --- Draft Manuscript]}` yer tutucusu durmaktadır. `README.md`'deki Macaulay2 `permanent X` komutunun geçerliliği doğrulanmamıştır ve betikte $\perm_3$ için $\codim \Sing = 6$ pozitif kontrolü yoktur.
- **Kaynakça ve öncelik doğrulaması [LİTERATÜR-DOĞRULANMADI]:** Yabe (2015), ABV (2017), MR (2004), LR (2017), Atkinson (1983) ve Eisenbud–Harris (1988) iddiaları ile 2026 öncesi olası $\dc_{\mathbb{C}}(\perm_4)$ çalışmaları (ör. Sheshadri 2026) hakkında birincil kaynak kontrolü yapılmamıştır; bilmiyorum, birincil kaynaktan kontrol edilmelidir.
- **“Ne İddia Ediyoruz / Etmiyoruz” bölümü ihtiyacı [SANI]:** Yalnız `Remark 5.2` yetersizdir; girişe eklenecek ayrı bir alt bölümle bu sonucun $n=4$ sabit boyutu için $10 \le \dc_{\mathbb{C}}(\perm_4) \le 15$ aralığını kapatmadığı, $O(n^2)$ Mignon–Ressayre bariyerini aşmadığı ve $\mathrm{VP} \neq \mathrm{VNP}$ ya da Boolean alt sınırı vermediği netleştirilmelidir.
- **Aktarım teoreminin makaledeki konumu [SANI]:** Aktarım özeti asimptotik ($2^{n^\varepsilon}$) devre alt sınırlarına yöneliktir ve sabit boyutlu $\dc_{\mathbb{C}}(\perm_4) \ge 10$ teoremine doğrudan bağlanmaz; ayrı sonuç olarak sunulmamalı, en fazla Tartışma bölümünde H1 ve H4'ün `[AÇIK]` olduğu belirtilerek motivasyon çerçevesinde anılmalıdır.

### B-istatistiksel-fizik
- **$L_8$'in genelliği gerekmez:** $J \subset \mathbb{Z}[X]$ homojen olduğundan, $\mathbb{P}^{15}$'te projektif boyut teoremi gereği *herhangi* bir 8-boyutlu $L_8$'de $V_{\mathbb{C}}(J|_{L_8})=\{0\}$ çıkması $\codim \Sing(V(\perm_4)) \ge 8$ için yeterlidir; dahası $D=9$'da tam rank çıkması $\ker(M_{L_8})=\{0\}$ ve $\rank(M_{L_8})=8$ olmasını zorunlu kılar. `[İSPAT]`
- **$L_9$ kıyaslaması ve ortak tohum pürüzü:** Benzer biçimde $\dim \Sing(V(\perm_4)) \ge 8$ olduğu için $\rank(M_{L_9})=9$ sağlayan *her* 9-uzay $\Sing$ ile en az $1$ boyutta kesişir, dolayısıyla $L_9$'un da genel olması gerekmez. `[İSPAT]` Ancak betikte `M_L8` ve `M_L9` aynı `default_rng(2026)` tohumunu kullanmakta, $\rank(M_{L_9})=9$ doğrulanmamakta ve $D=6,7$'de korank $>0$ çıkması $L_8$'de de ($132, 32$) gözlendiğinden ayrımı tek başına kanıtlamamaktadır. `[KESİN HESAP]`
- **`[-2, 2]` katsayıları ve tekrarlanabilirlik:** Küçük tamsayı matrisi seçimi `block_size * (p-1)^2 < 2^53` bit-kesin aritmetik sınırını sağladığından meşrudur. `[KESİN HESAP]` Yine de `M_L8`'in `np.random.default_rng(2026)` çağrısına bırakılması yerine açık tamsayı matrisi olarak makaleye ve betiğe sabitlenmesi önerilir. `[SANI]`
- **Pozitif kontrol eksiği:** `verify_codim_sing_perm4.py` betiğine $\perm_3$ için $\codim(\Sing)=6$ pozitif kontrolünün eklenmesi, algoritmanın bilinen tam değerde kapandığını doğrulayacaktır. `[SANI]`
- **Aktarım teoreminin yeri:** Tekillik/Hessian yöntemi $n\to\infty$'da $O(n^2)$ bariyerine takıldığından, Boolean/SAT aktarım çerçevesi (`H1`, `H4` `[AÇIK]`) makalede ayrı sonuç olarak değil, yalnızca Tartışma bölümünde kısa motivasyon olarak verilmelidir. `[SANI]`

### B-matematiksel-fizik
1. **Fizik jargonu denetimi:** `dc_perm4_ge_10.tex`, `verify_codim_sing_perm4.py` ve `README.md` metinlerinde bozonik/fermiyonik benzetme veya fizik jargonu sızıntısı yoktur; $\Omega$-izotropi ve $K \in \mathfrak{so}_{d_v}(\mathbb{C})$ tamamen standart çiftdoğrusal cebir ve Lie cebiri dilindedir [İSPAT].

2. **Blok indis kirliliği ($A_{13}, A_{31}, A_{33}$):** İspatın 2. adımında orta blok bulunmayan $m=9$ ($w=D=8$) durumunda $A(X)$ matrisi, `Scope and limitations` notundaki $3$-blok şemasından kalma $A_{13}, A_{31}, A_{33}$ indisleriyle yazılmıştır; tam blok indirgemeyi temiz tutmak için gövdede $(11,12,21,22)$ indislerine geçilmelidir [İSPAT].

3. **$d_v \in \{0,8\}$ uç durumları ve $P$ dönüşümü:** $\Omega$'nın dejenere olmaması $\dim W = \dim S \le 8$'i ve $(v^T P^{-1}, P A P^{-1}, P u)$ eşlemesi $u_1 = Ky$ ($K^T = -K$) normal formunu verir; ancak $d_v=0$ ($\perm_4 \equiv 0$) ve $d_v=8$ ($z$ boş) sınırları metinde açıkça kapatılmalı ve sütun vektörü olarak $v \mapsto P^{-T}v$ yazımı belirtilmelidir [İSPAT].

4. **Skew-Square ve $I_W^3$ indirgemesi:** $K^T = -K$ ve $(MK)^T = -MK$ koşullarından $(M^2K)^T = -M^2K$ özdeşliği $K$ tekil olsa dahi geçerlidir; $A_{13} \in I_W$ ile birleşince $\perm_4 \in I_W^3$ çıkarımı tamdır [İSPAT].

5. **$m \ge 10$ orta-blok uyarısı:** Son nottaki $w_{\mathrm{mid}} = w - D$ için $\rank(\mathrm{Hess}(\perm_4)(X_0)) \le 2w_{\mathrm{mid}}$ sınırı makalede türetilmemiştir; kanıt eklenmeyecekse sezgisel gözlem olarak daraltılmalıdır [SANI].

### B-kuantum-hesaplama
1. **Kapsam Uyumsuzluğu:** `dc_perm4_ge_10.tex` sabit $n=4$ için biçimsel $\dc_{\mathbb{C}}(\perm_4) \ge 10$ sınırını incelerken, Nicel Aktarım Teoremi asimptotik $2^{n^\varepsilon}$ ölçeğinde ve $I_B$ modülo fonksiyonel devre alt sınırı (H1) gerektirir; mevcut sonuç Boolean/SAT alt sınırı üretmez `[İSPAT]`.
2. **H1 ve H4 Tamamen Açık:** Verilen aktarım özeti H3 ortasında kesilmiş olup H4 metnini içermemektedir `[İSPAT]`. H1 ($I_B$ modülo üstel fonksiyonel alt sınır) ve H4 tamamen açık durumdadır; ilgili literatür çerçevesi birincil kaynaklardan doğrulanmalıdır `[LİTERATÜR-DOĞRULANMADI]`.
3. **Yayın Riski (Q3):** Aktarım teoremini makalede ayrı bir sonuç veya bölüm olarak sunmak, hem $n=4$ sabit boyutuyla ölçek uyumsuzluğu hem de H1 ve H4'ün tamamen açık olması nedeniyle ciddi hakem riski doğurur `[SANI]`.
4. **Önerilen 'Motivasyon / Tartışma' Bölümü (Q3):** Makale sonundaki *Remark* kısa bir *Motivation and Discussion* bölümüne dönüştürülmelidir: tekillik/Hessian yöntemi $O(n^2)$ Mignon–Ressayre bariyerinde kalır `[İSPAT]`; $\mathrm{VP} \neq \mathrm{VNP}$ ve Boolean/SAT alt sınırlarına aktarım için H1 ve H4'ün tamamen açık engeller olarak kaldığı açıkça belirtilmelidir `[SANI]`.
5. **Doğrulama ve Literatür Eksikleri:** Yabe (2015), ABV (2017), Mignon–Ressayre (2004), Landsberg–Ressayre (2017) ve olası güncel $\dc(\perm_4)$ yayınları birincil kaynaktan denetlenmeli `[LİTERATÜR-DOĞRULANMADI]`; ayrıca $r=3$ vakasındaki olası $2\times 2$ sıfır blok eksikliği ve `perm_3` ($\codim=6$) pozitif kontrolü tamamlanmalıdır `[SANI]`.

### B-deneysel-doğrulama
* **BLAS `float64` taşma marjı:** `rref_mod_p_exact` içinde `block_size = 96` ve `P2 = 65521` için $96 \times 65520^2 \approx 4.12 \times 10^{11} < 2^{53}$ sınırı korunur [KESİN HESAP]. Ancak `step_imsc` içindeki `R_canon @ C_s` çarpımının iç boyutu `n_S` ($L_8$'de $n_S \le 1056$, $1056 \times 65520^2 \approx 4.53 \times 10^{12} < 2^{53}$) için `assert` yoktur [KESİN HESAP]. Büyük `corank` veya daha büyük asalda taşmayı önlemek için bu çarpıma bloklama ve `assert` eklenmelidir [SANI].
* **`build_subperm3_on_L` ve IMSC doğruluğu:** $3\times 3$ alt-kalıcılar $6$ permütasyonla eksiksiz toplanır; `A6` kurulumunda sabit `m_mul` için `sorted(m_mul + m_p)` birebir olduğundan katsayı ezilmez ve `C_table` sağ sıfır-uzayı $I_D$ indirgemesini tam verir [İSPAT].
* **Tekrarlanabilirlik riski:** `M_L8` ve `M_L9` matrislerinin `np.random.default_rng(2026)` ile üretilmesi NumPy sürüm değişimlerinde farklı altuzay üretme riski taşır; `M_L8` açık tam sayı matrisi olarak sabitlenmelidir [SANI].
* **Kontrol eksiği:** `L_9` negatif kontrolü yalnızca kodun her şeyi sıfırlamadığını gösterir [İSPAT]. Bilinen $\codim(\Sing(V(\perm_3))) = 6$ [LİTERATÜR-DOĞRULANMADI] için `perm_3` pozitif kontrolü eklenmelidir [SANI].
* **Bağımsız doğrulama protokolü:** `README.md`'deki Macaulay2 `permanent X` sözdizimi doğrulanmamıştır [LİTERATÜR-DOĞRULANMADI]. Bağımsız teyit için açık toplam formüllü M2/Singular betiği ile kayan noktasız saf Python `int` referans çapraz kontrolü çalıştırılmalıdır [SANI].

---

## Tur 2 — crit-B Saldırıları ve Yanıtlar

### crit-B Soruları
Öncelik açısından, bu sonucun daha önce (ör. Sheshadri 2026 veya Yabe 2015/ABV 2017 çizgisinde) bulunup bulunmadığını bilmiyorum, birincil kaynaktan kontrol edilmeli [LİTERATÜR-DOĞRULANMADI].

### B-hesaplamalı-cebir
- `r=3` vakasındaki eksik $2\times 2$ sıfır bloğunu ve `Remark 3.2`'deki "generic $L_9$" ile açık $L_8$ arasındaki tutarsızlığı hiç sorgulamadın [KESİN HESAP].
- `Atkinson1983`, `EH1988` ve diğer literatür iddialarının öncelik/doğruluk durumunu kontrolsüz bıraktın [LİTERATÜR-DOĞRULANMADI].
- *Hakem reddi:* Tek tohumlu (`2026`) IMSC dışında bağımsız CAS teyidi, doğrulanmış `M2` komutu ve `perm_3` pozitif kontrolü olmadan Teorem 3.1 güvenilmez sayılır [SANI].

### B-sayılar-kuramı
- Tek asal yeterliğini savunurken `step_imsc` indirgemesinin tüm $I_9$ idealini temsil ettiğini ve $r=3$ sınıflandırmasının tam olduğunu sessizce varsaydın [İSPAT].
- `M_L9`'un tam ranklı ($9$) olup olmadığının kodda denetlenmediğini, `M2` `permanent` belirsizliğini ve literatür önceliğini atladın [KESİN HESAP].
- *Hakem reddi:* `L_9`'un $D=6,7$ koranklarının pozitif çıkması $L_8$'de de ($132, 32$) gözlendiğinden kontrol yetersiz bulunur [SANI].

### B-cebirsel-karmaşıklık
- $2\times 2$ sıfır blokta $\adj(B)=(0,-c,b)^T(0,e,-d)$ ile $\str\le 1$ türettin; ancak tek motorlu IMSC sertifikası riskini ve `M2` `permanent` hatasını sorgulamadın [KESİN HESAP].
- `Remark 3.2`'deki "generic $L_9$" çelişkisini ve `perm_3` ($\codim=6$) pozitif kontrol eksikliğini dışarıda bıraktın [KESİN HESAP].
- *Hakem reddi:* Ana alt-sonuç bağımsız CAS ile doğrulanmadıkça ve öncelik literatürü birincil kaynaklardan teyit edilmedikçe makale reddedilir [SANI].

### B-lineer-cebir
- $2\times 2$ sıfır blokta $\adj(B)$ çarpanlamasıyla $\str\le 2$ dedin; oysa tek sıra-1 çarpım $\str\le 1$ verir ve sıfır sütunun devrikle elendiğini göstermedin [İSPAT].
- `Remark 3.2`'deki "generic $L_9$" hatasını, `M_L8`/`M_L9` ortak tohumunu ve `Atkinson1983`/`EH1988` kaynak kontrolünü atladın [KESİN HESAP].
- *Hakem reddi:* $r=3$ ispatındaki eksiklik, bağımsız CAS eksikliği ve doğrulanmamış literatür konumu reddedilme sebebidir [SANI].

### B-mantık-ispat
- $2\times 2$ sıfır bloklu $B = \begin{pmatrix} a & b & c \\ d & 0 & 0 \\ e & 0 & 0 \end{pmatrix}$ için $\adj(B)=(0,-e,d)^T(0,c,-b)$ yazdın; bu $\adj(B)$'nin kendisi değil devriğidir ($(2,3)$ bileşeni $cd$ olmalıdır) [İSPAT].
- Betikteki `perm_3` kontrolsüzlüğünü, `M2` `permanent` riskini ve birincil literatür önceliğini denetlemedin [KESİN HESAP].
- *Hakem reddi:* Hatalı kofaktör devriği, tek motorlu sertifika ve öncelik kontrolsüzlüğü hakemin makaleyi reddetmesine yeter [SANI].

### B-yazım-editörü
- `X_0` ve $A_{13}$ hatalarını yakaladın ama `r=3` $2\times 2$ sıfır blok deliğini ve "generic $L_9$" vs açık $L_8$ çelişkisini tamamen atladın [KESİN HESAP].
- `verify_codim_sing_perm4.py` içindeki `step_imsc` taşma kontrolsüzlüğünü ve `M_L9` rank denetimsizliğini sessizce geçtin [KESİN HESAP].
- *Hakem reddi:* Düzenli yazım, $r=3$ ispat boşluğunu, doğrulanmamış `M2` betiğini ve öncelik taraması eksikliğini kurtaramaz [SANI].

### B-istatistiksel-fizik
- `L_8`/`L_9` genelliğinin gerekmediğini kanıtladın ama `r=3` $2\times 2$ sıfır bloğunu, `M2` `permanent` belirsizliğini ve tüm literatür/öncelik kontrolünü es geçtin [KESİN HESAP].
- `R_canon @ C_s` çarpımının `n_S` taşma sınırını denetlemeden `[-2,2]` tamsayı seçimini sorunsuz saydın [KESİN HESAP].
- *Hakem reddi:* `L_8/L_9` boyut argümanı doğru olsa da $r=3$ açığı ve öncelik teyidi yokluğu nedeniyle makale reddedilir [SANI].

### B-matematiksel-fizik
- Yalnız blok indisleri ve jargon denetimi yapıp `r=3` $2\times 2$ sıfır blok eksikliğini, `L_8`/`L_9` betik açıklarını ve `M2` `permanent` sorununu tamamen atladın [KESİN HESAP].
- Literatürdeki sonuçların daha önce bulunup bulunmadığını ve `Atkinson1983`/`EH1988` referanslarını hiç sorgulamadın [LİTERATÜR-DOĞRULANMADI].
- *Hakem reddi:* İndis temizliği yeterli değildir; $r=3$ boşluğu, doğrulanmamış sertifika araçları ve öncelik belirsizliği redde yol açar [SANI].

### B-kuantum-hesaplama
- Aktarım teoremini eledin ama `M2` `permanent` hatasını, `Remark 3.2` "generic $L_9$" tutarsızlığını ve `step_imsc` taşma marjını incelemedin [KESİN HESAP].
- `r=3` $2\times 2$ sıfır blok eksikliğini kendin türetmeden başkasının şüphesi olarak yineledin [SANI].
- *Hakem reddi:* Öncelik taraması, bağımsız CAS doğrulaması ve onarılmış $r=3$ ispatı olmadan makale dergiden döner [SANI].

### B-deneysel-doğrulama
- Sayısal taşmayı inceledin ama `r=3` $2\times 2$ sıfır blok açığını, `M_L9` rank denetimsizliğini ve `Remark 3.2` genellik hatasını atladın [KESİN HESAP].
- Makale iddialarının literatürdeki öncelik ve tutarlılık denetimini tamamen dışarıda bıraktın [LİTERATÜR-DOĞRULANMADI].
- *Hakem reddi:* Betik bit-kesin olsa bile `perm_3` pozitif kontrolü, bağımsız CAS çıktısı ve $r=3$ düzeltmesi olmadan makale kabul edilmez [SANI].

### B-hesaplamalı-cebir (Tur 2 Yanıtı)
- **`r=3` $2\times 2$ sıfır bloğu (kabul):** Tur 1'de bunu atladım; eleştiri haklıdır [SANI]. $B=\begin{pmatrix} a&b&c\\ d&0&0\\ e&0&0 \end{pmatrix}$ için doğrudan kofaktör hesabıyla $\adj(B)=(0,c,-b)^T(0,-e,d)$ sıra-$1$ çıkar, böylece $\perm_4=-\tr(\adj(B)UV)=-(0,-e,d)UV(0,c,-b)^T$ olup $\str(\perm_4)\le 1<4$ çelişkisini verir [İSPAT]. Sıfır sütun vakası $(B,U,V,A)\mapsto(B^T,V^T,U^T,A^T)$ devriğiyle sıfır satıra indirgenir [İSPAT].

- **`Remark 3.2` ve $L_9$ tutarsızlığı (kabul):** `Remark 3.2`'de "generic $L_9$" denmesine karşın betikte tek sabit tohum (`2026`) kullanılmasını ve `M_L8`/`M_L9` matrislerinin tam ranklı ($8$, $9$) olduğunun kodda denetlenmemesini Tur 1'de atladım [KESİN HESAP]. Ayrıca `L_9`'da $D=6,7$ pozitif korankları $L_8$'de de görüldüğünden, sonlu derece pozitif korankı tek başına `L_9` kontrolü için zayıftır [KESİN HESAP].

- **Literatür ve öncelik (kabul):** `Atkinson1983`, `EH1988`, `Yabe 2015`, `ABV 2017`, `MR2004`, `LR2017` ile daha önce `dc(perm_4)>=10` veya `Sheshadri 2026` gibi yayınların olup olmadığını bilmiyorum, birincil kaynaktan kontrol edilmeli [LİTERATÜR-DOĞRULANMADI].

- **CAS doğrulama eşiği (mutabıkım):** Tur 1'de de vurguladığım gibi tek tohumlu IMSC yerine Singular, M2 ve Sage üzerinde açık permütasyon toplamıyla `perm_3` ($\codim=6$), `L_8` ($D=9$ tam rank) ve çoklu rastgele altuzaylar çalıştırılmadan Teorem 3.1 güvenilir sayılmaz [SANI].

### B-sayılar-kuramı (Tur 2 Yanıtı)
- **IMSC Kapsamı (Savunma):** `step_imsc` kanıtında $M_{\mathrm{syz}}$'nin tüm $I_{D+1}$'i tüketmesi gerekmez; $D=6$'da $m-C_6(m)\in I_6\otimes\mathbb{F}_p$ geçerlidir ve her adımda $\Span(M_{\mathrm{syz}})\subseteq I_{D+1}\otimes\mathbb{F}_p$ kapsanır `[İSPAT]`. Tümevarımla $D=9$'da korank $0$ çıkması $I_9\otimes\mathbb{F}_p=R_9\otimes\mathbb{F}_p$ eşitliğini ve tek asalla dahi $M_9(I)$'nın $\mathbb{Q}$-tam rankını kanıtlar `[İSPAT]`.
- **$r=3$ Eksikliği (Kabul):** Tur 1'de $r=3$ sınıflandırmasını denetlemedim; birinci satır ve sütun dışındaki $2\times 2$ sıfır bloklu $B$ tipi eksiktir `[İSPAT]`. Bu tipte $\adj(B)=(0,c,-b)^T(0,-e,d)$ sıra-1 olduğundan $\str(\perm_4)\le 1 < 4$ çelişkisi çıkar `[İSPAT]`.
- **`M_L9`, `M2` ve Öncelik (Kabul):** `M_L9`'un tam ranklı ($9$) olduğu kodda doğrulanmadığından çekirdek yapay pozitif korank üretebilir; `rank(M_L9)==9` kontrolü eklenmelidir `[KESİN HESAP]`. Ayrıca `M2`'deki `permanent` komutu ve birincil literatür önceliği doğrulanmamıştır `[LİTERATÜR-DOĞRULANMADI]`.
- **`L_9` Kontrol Yetersizliği (Kabul):** $D=6,7$'deki pozitif koranklar $L_8$'de de ($132,32$) gözlendiğinden `L_9` testi en az $D=9$'a uzatılmalı ve `perm_3` ($\codim=6$) pozitif kontrolü eklenmelidir `[KESİN HESAP]`.

### B-cebirsel-karmaşıklık (Tur 2 Yanıtı)
- **Sıfır blok türetimi korunuyor:** $B=\begin{pmatrix} a&b&c\\ d&0&0\\ e&0&0 \end{pmatrix}$ için $\mathrm{adj}(B)=(0,-c,b)^T(0,e,-d)$ olduğundan $-\mathrm{tr}(\mathrm{adj}(B)UV)=-(0,e,-d)UV(0,-c,b)^T$ tek çarpıma indirgenir ve $\mathrm{str}(\mathrm{perm}_4)\le 1<4$ çelişkisini verir [İSPAT]. Bu tip, sıfır sütun/devrik simetrisiyle birlikte Prop. 4.1'e açıkça eklenmelidir [SANI].
- **Sertifika ve `M2` açığını kabul ediyorum:** Tur 1'de tek motorlu IMSC riskini ve `README.md`'deki `permanent` komutunun Macaulay2'de doğrulanmamış olmasını sorgulamadım [KESİN HESAP]. Teorem 3.1 bağımsız bir CAS'ta doğrulanmalı ve `M2` betiğinde `permanent` yerine açık polinom tanımı veya doğrulanmış sözdizimi kullanılmalıdır [SANI].
- **`Remark 3.2` ve `perm_3` eksiklerini kabul ediyorum:** $0\in L_9$ iken $\dim(L_9\cap\mathrm{Sing})\ge 1$ için "generic $L_9$" değil yalnızca $\mathrm{rank}(M_{L_9})=9$ gerekir [İSPAT]; ayrıca betikte $\mathrm{rank}(M_{L_9})=9$ denetimi ile `perm_3` ($\mathrm{codim}=6$) pozitif kontrolü eksiktir [KESİN HESAP].
- **Hakem reddi değerlendirmesi:** Öncelik ve literatür konumu (MR04, Yabe 2015, ABV17, LR17, olası yeni sonuçlar) birincil kaynaklardan doğrulanmamıştır [LİTERATÜR-DOĞRULANMADI]. Bağımsız CAS teyidi ve bu literatür kontrolü eklenmeden makale hakemden ret alabilir [SANI].

### B-lineer-cebir (Tur 2 Yanıtı)
- **`str <= 2` savunması (`str <= 1` yanlış):** $2\times 2$ sıfır bloklu $B$ için $\adj(B) = \tilde{b}\tilde{c}^T$ ($\tilde{b}=(0,b_2,-b_1)^T$, $\tilde{c}=(0,-c_2,c_1)^T$) biçimindedir; ancak $U \in \mathbb{C}[X]_1^{3\times w}$ ve $V \in \mathbb{C}[X]_1^{w\times 3}$ ($w = m-3 \ge 2$) olduğundan $\perm_4 = -\tilde{c}^T U V \tilde{b}$ ifadesi $(\tilde{c}^T U)\cdot(V\tilde{b})$ biçiminde $w$ adet kuadratik çarpımın toplamıdır, tek başına $\str \le 1$ vermez [İSPAT]. Buna karşılık $\tilde{c}^T$'nin iki sıfırsız bileşeniyle açılım $\perm_4 = c_2(UV\tilde{b})_2 - c_1(UV\tilde{b})_3$ olarak $\str(\perm_4) \le 2 < 4$ verir ve çelişkiyi kapatır [İSPAT].
- **Sıfır sütun devrik eşleniği:** Tur 1'de yazılmayan sıfır sütun durumu için $M(tX)^T$ almak $(B,U,V,A) \mapsto (B^T,V^T,U^T,A^T)$ dönüşümüyle sıfır satıra indirger ve $\tr(\adj(B)UV) = \tr(\adj(B^T)V^TU^T)$ özdeşliğiyle elenir [İSPAT].
- **Kabul edilen eksikler:** `Remark 3.2`'de "generic $L_9$" ifadesi gereksizdir (afın boyut teoremi her $9$-boyutlu $L_9$ için geçerlidir) ve betikte `M_L8`/`M_L9` aynı `2026` tohumunu paylaşıp $\rank(M_{L_9})=9$ denetimi yapmamaktadır [KESİN HESAP]. `Atkinson1983`/`EH1988` ayrıntıları ve olası öncelik yayınları birincil kaynaktan doğrulanmalıdır [LİTERATÜR-DOĞRULANMADI].

### B-mantık-ispat (Tur 2 Yanıtı)
1. **Kofaktör devriği (Geri çekme ve düzeltme):** `crit-B` haklıdır; Tur 1’de $\adj(B)$ yerine devriği $\adj(B)^T=(0,-e,d)^T(0,c,-b)$ yazılmıştır, oysa $(2,3)$ bileşeni $+cd$ olmalıdır [İSPAT]. Doğru çarpanlama $\adj(B)=(0,-c,b)^T(0,e,-d)$ olup $B\adj(B)=\adj(B)B=0$ koşulunu sağlar [İSPAT]. Ancak $\perm_4=-(0,e,-d)UV(0,-c,b)^T$ ifadesi $U$ ($3\times w$) ve $V$ ($w\times 3$) üzerinden $w$ terimli kuadratik çarpım verdiği için $\str\le 1$ değil, $(0,e,-d)$ üzerinden açılarak $e,d$ lineer çarpanlarıyla $\str(\perm_4)\le 2<4$ verir [İSPAT].

2. **Atlanan doğrulama ve literatür denetimleri (Kabul):** Tur 1’de betikteki `perm_3` ($\codim=6$) pozitif kontrolü eksikliğini, `README.md`’deki `M2` `permanent` belirsizliğini ve `M_L9` tam-rank denetimsizliğini kapsam dışı bıraktığımı kabul ediyorum [KESİN HESAP]. Yabe 2015, ABV 2017, Mignon–Ressayre, Landsberg–Ressayre ve olası Sheshadri 2026 önceliğini bilmiyorum, birincil kaynaktan kontrol edilmelidir [LİTERATÜR-DOĞRULANMADI]. Bağımsız CAS doğrulaması ve `perm_3` kontrolü eklenmeden Teorem 3.1 hakem onayından geçmeyebilir [SANI].

### B-yazım-editörü (Tur 2 Yanıtı)
- **Geri çekme — $r=3$ sıfır blok açığı [İSPAT]:** Tur 1'de yalnızca yazım/notasyona odaklanıp $r=3$'teki $2\times 2$ sıfır bloklu sıkıştırma tipini atladım; haklısın. Kendim türettiğimde $B = \begin{pmatrix} a & b & c \\ d & 0 & 0 \\ e & 0 & 0 \end{pmatrix}$ için kofaktör devriği $\adj(B) = (0,-c,b)^T (0,e,-d)$ olup $-\tr(\adj(B)UV)$ tek çarpım verir ($\str \le 1 < 4$); bu vaka makaleye açıkça eklenmelidir.
- **Geri çekme — `Remark 3.2` ve betik denetimi [KESİN HESAP]:** `Remark 3.2`'de "generic $L_9$" yazılırken kodda sabit tohumlu (`2026`) açık $L_9$ kullanılması yazım çelişkisidir (üstelik boyut sayımı tüm $9$-boyutlu altuzaylarda geçerlidir). Kodda `rank(M_L9) == 9` `assert`'i ve `step_imsc`'deki `R_canon @ C_s` çarpımı için `n_S * (p-1)^2 < 2^53` taşma denetimi eksikliği de atladığım somut kusurlardır.
- **Savunma — `M2`, `perm_3` ve öncelik [LİTERATÜR-DOĞRULANMADI]:** Tur 1'in 2. ve 3. maddelerinde `M2` `permanent` komutu belirsizliğini, `perm_3` ($\codim=6$) pozitif kontrol eksikliğini ve birincil literatür/öncelik (ör. Sheshadri 2026) kontrolsüzlüğünü zaten doğrudan raporlamıştım.
- **Hakem riski [SANI]:** Bu boşluklar giderilmeden yalnızca editoryal düzeltmeyle makale kabul edilmez.

### B-istatistiksel-fizik (Tur 2 Yanıtı)
- **Geri çekme (`R_canon @ C_s` taşması):** `step_imsc` içindeki `R_canon @ C_s` çarpımında `rref_mod_p_exact`'taki gibi açık bir `2^53` taşma `assert`'i olmadığını kabul ediyorum. `[KESİN HESAP]` Yine de `R_canon`'un her satırında en fazla $\mathrm{corank}_D$ sıfır dışı terim vardır ($L_8$'de $\le 132$, $132\cdot 65520^2 \approx 5.67\times 10^{11} \ll 2^{53}$; $L_9$'da $D=6$'da $\le 753$, $753\cdot 32748^2 \approx 8.08\times 10^{11} \ll 2^{53}$), fakat koda açık `assert` eklenmelidir. `[KESİN HESAP]`
- **`r=3` $2\times 2$ sıfır bloğu (kendi türetimim):** Tur 1'de dışarıda bıraktığım $B=\begin{pmatrix}a&b&c\\d&0&0\\e&0&0\end{pmatrix}$ vakasında $\adj(B)=u w^T$ ($u=(0,-e,d)^T$, $w^T=(0,c,-b)$) çıkar; $u_1=0$ olduğundan $\perm_4=-(w^T UV)u$ yalnızca iki terim içerir ve $\str(\perm_4)\le 2<4$ verir (sıfır sütun da devrikle sıfır satıra iner). `[İSPAT]`
- **M2 ve literatür/öncelik:** `README.md`'deki M2 `permanent` komutunu ve `Atkinson1983`, `EH1988`, `Yabe 2015`, `ABV 2017`, `Sheshadri 2026` gibi kaynakların öncelik/doğruluğunu bilmiyorum, birincil kaynaktan kontrol edilmeli. `[LİTERATÜR-DOĞRULANMADI]`
- **Yayın yargısı:** `L_8/L_9` boyut argümanı doğru kalsa da $r=3$ düzeltmesi, bağımsız CAS doğrulaması, `perm_3` pozitif kontrolü ve öncelik taraması yapılmadan makale reddedilir. `[SANI]`

### B-matematiksel-fizik (Tur 2 Yanıtı)
Eleştirileri kabul ediyorum; Tur 1'de yalnız blok indirgeme/jargon odağında kalıp şu eksikleri atlamıştım:

1. **$r=3$ sınıflandırma açığı:** `Prop. 4.1`'de sıfır sütun devrikle ($\adj(B^T)=\adj(B)^T$) kapanır [İSPAT]. Eksik olan $2\times 2$ sıfır bloklu sıkıştırma tipi $B=\begin{pmatrix}a&b&c\\d&0&0\\e&0&0\end{pmatrix}$ için $\adj(B)=p\,q^T$ ($p=(0,c,-b)^T$, $q=(0,-e,d)^T$) olur ve $\perm_4=-(q^T U)(Vp)$ ile $\str(\perm_4)\le 1 < 4$ çelişkisi doğrudan çıkar [İSPAT].
2. **Sertifika ve `M2` açıkları:** `verify_codim_sing_perm4.py`'de `M_L9` rank-$9$ denetimi ve `perm_3` ($\codim=6$) pozitif kontrolü eksiktir; `README.md`'deki `M2` `permanent` komutu da doğrulanmamıştır [KESİN HESAP].
3. **Literatür ve öncelik:** `Atkinson1983`, `EH1988`, `Yabe2015`, `ABV2017`, `MR2004`, `LR2017` detayları ile `dc_C(perm_4)` üzerine daha önce (ör. Sheshadri 2026) yayın olup olmadığını bilmiyorum, birincil kaynaktan kontrol edilmeli [LİTERATÜR-DOĞRULANMADI].
4. **Korunan Tur 1 bulguları:** Gövdedeki $A_{13},A_{31},A_{33}$ indis kirliliği ve $d_v\in\{0,8\}$ sınır eksikleri düzelmeli [İSPAT]; bu açıklar ve bağımsız CAS eksikliği giderilmezse makale reddedilebilir [SANI].

### B-kuantum-hesaplama (Tur 2 Yanıtı)
- **Kabul edilen eksikler:** İlk turda aktarım teoremine odaklandığım için `step_imsc` içindeki `R_canon @ C_s` çarpımında açık taşma `assert`inin bulunmadığını `[KESİN HESAP]`, `Remark 3.2`deki "generic $L_9$" ifadesi ile kodda $\rank(M_{L_9})=9$ denetimsizliğini `[KESİN HESAP]` ve `README`deki M2 `permanent` belirsizliğini `[LİTERATÜR-DOĞRULANMADI]` atladım; bu eleştirileri kabul ediyorum.
- **$r=3$ kendi türetimim:** $2\times 2$ sıfır bloklu $B=\begin{pmatrix}a&b&c\\d&0&0\\e&0&0\end{pmatrix}$ için kofaktör devriğini doğrudan hesaplayınca $\adj(B)=(0,-c,b)^T(0,e,-d)$ çıkar; böylece $\perm_4 = -\tr(\adj(B)UV) = -e(UV)_{2,\bullet}(0,-c,b)^T + d(UV)_{3,\bullet}(0,-c,b)^T$ iki $(1,3)$-dereceli çarpıma indirgenip $\str(\perm_4)\le 2 < 4$ çelişkisi verir; sıfır sütun ise $M\mapsto M^T$ devriğiyle sıfır satıra indirgenir `[İSPAT]`.
- **`step_imsc` taşma sınırı:** `R_canon` satırlarında en fazla $\mathrm{corank}_D$ (ör. $132$) sıfırdan farklı terim olduğundan iç çarpım üst sınırı $132(p_2-1)^2 \approx 5{,}67\times 10^{11} \ll 2^{53}$ kalır; ancak açık `assert` eklenmelidir `[KESİN HESAP]`.
- **Aktarım teoremi ve yayın kararı:** H1 ve H4'ün tamamen açık kalması sebebiyle aktarım teoremini makaleden dışlayıp kısa bir *Tartışma* paragrafı önermem geçerlidir `[SANI]`; `crit-B`'nin onarılmış $r=3$, bağımsız CAS ve öncelik taraması olmadan makalenin dergiden döneceği hükmüne katılıyorum `[SANI]`.

### B-deneysel-doğrulama (Tur 2 Yanıtı)
* **Kabul edilen eksikler:** İlk turda yalnız sayısal/kod alanına odaklanıp `M_L9` rank denetimsizliğini, `Remark 3.2` genellik hatasını, `r=3` $2\times 2$ sıfır blok açığını ve literatür öncelik kontrolünü atladım [SANI].
* **`M_L9` rankı ve `Remark 3.2`:** Afin boyut teoremine göre $8$-boyutlu bir koniyi $\ge 1$ boyutta kesmek için $L_9$'un "genel" olması gerekmez, $\dim L_9 = 9$ yeterlidir [İSPAT]. Mevcut betikte `M_L9`'un tam ranklı ($9$) olduğu doğrulanmamaktadır [KESİN HESAP].
* **`r=3` $2\times 2$ sıfır blok düzeltmesi:** $B = \begin{pmatrix} a & b & c \\ d & 0 & 0 \\ e & 0 & 0 \end{pmatrix}$ için $\adj(B) = (0,-c,b)^T (0,e,-d)$ olduğundan $-\tr(\adj(B)UV)$ ifadesi $c$ ve $b$ üzerinden iki terimli ayrışım verip $\str(\perm_4)\le 2 < 4$ çelişkisini üretir; sıfır sütun durumu devrikle aynıdır [İSPAT].
* **Literatür ve öncelik:** Sheshadri 2026 olasılığı dahil tüm öncelik iddiaları (Yabe 2015, ABV 2017, Atkinson 1983, EH 1988) ve M2 `permanent` sözdizimi birincil kaynaklardan kontrol edilmelidir [LİTERATÜR-DOĞRULANMADI].
* **Korunan doğrulama protokolü:** `perm_3` pozitif kontrolünde beklenen $\codim(\Sing(V(\perm_3)))=6$ değeri birincil kaynaktan teyit edilmelidir [LİTERATÜR-DOĞRULANMADI]. Hakem reddi riskine karşı `step_imsc` içindeki `n_S` taşma kontrolü, `M_L9` rank-9 `assert`'i, `perm_3` pozitif kontrolü, sabit `M_L8` ve bağımsız CAS/tam-`int` çapraz doğrulaması eklenmelidir [SANI].

---

## Tur 3 — Üretilen Düzeltme ve Doğrulama Çıktıları

### (a) Düzeltilmiş r = 3 LaTeX Paragrafı (B-lineer-cebir)
Aşağıdaki `Case r = 3` LaTeX metni, Tur 1–2'deki satır satır yeniden türetim temelinde $1\times 3$ sıfır satır, $3\times 1$ sıfır sütun (devrik eşleniği), $2\times 2$ sıfır bloğu ($\adj(B) = \tilde{b}\tilde{c}^T \implies \str(\perm_4) \le 2 < 4$) ve $\mathfrak{so}_3(\mathbb{C})$ primitif tipini eksiksiz kapsayacak biçimde hazırlanmıştır [İSPAT]. `Atkinson1983` ve `EH1988` içindeki tam teorem numaraları ve ifade biçimleri birincil kaynaklardan henüz kontrol edilmediğinden hakem öncesi doğrulanmalıdır [LİTERATÜR-DOĞRULANMADI].

```latex
\emph{Case $r = 3$.} Comparing $[t^3]$ and $[t^4]$ in~\eqref{eq:schur} gives $\det_3(B(X)) \equiv 0$ and
\[
  \perm_4(X) = \tr(A)\underbrace{\det_3(B)}_{=\,0} - \tr\!\big(\adj(B(X))\, U(X) V(X)\big)
  = -\tr\!\big(\adj(B(X))\, U(X) V(X)\big).
\]
Thus $B(X)$ spans a linear subspace of $\mathbb{C}^{3\times 3}$ consisting of matrices of rank $\le 2$. Left and right multiplication $B \mapsto P_1 B Q_1$ ($P_1, Q_1 \in \mathrm{GL}_3(\mathbb{C})$) corresponds to multiplying~\eqref{eq:blockM} by $\mathrm{diag}(P_1, I_w)$ and $\mathrm{diag}(Q_1, I_w)$, which only scales $\perm_4$ by $\det(P_1 Q_1) \neq 0$ and preserves $\str(\perm_4)$; likewise, matrix transposition $M(tX) \mapsto M(tX)^T$ preserves $\det(M(tX))$ and maps $(B, U, V, A) \mapsto (B^T, V^T, U^T, A^T)$, with $\tr(\adj(B)UV) = \tr(\adj(B^T)V^T U^T)$.

By the classification of $3 \times 3$ spaces of matrices of rank $\le 2$ over an algebraically closed field of characteristic $\neq 2$ (Atkinson~\cite{Atkinson1983}, Eisenbud--Harris~\cite{EH1988}), up to $\mathrm{GL}_3(\mathbb{C}) \times \mathrm{GL}_3(\mathbb{C})$, $B(X)$ is either of compression type—having a $(3-a)\times(3-b)$ zero submatrix with $a+b = 2$, i.e., $(a,b) \in \{(2,0),(0,2),(1,1)\}$—or of primitive skew-symmetric type:
\begin{enumerate}
  \item \emph{$1\times 3$ zero row or $3\times 1$ zero column ($(a,b)=(2,0)$ or $(0,2)$):} By transposition $M(tX) \mapsto M(tX)^T$, a $3\times 1$ zero column reduces to a $1\times 3$ zero row (say row $3$). Then $\adj(B(X)) = c(X) e_3^T$, where $c(X) = (c_1,c_2,c_3)^T \in \mathbb{C}[X]_2^3$ consists of the signed $2\times 2$ minors of the top $2\times 3$ block of $B(X)$. Hence
  \[
    \perm_4(X) = -\big(e_3^T U(X) V(X)\big) c(X) = -\sum_{j=1}^3 \big(e_3^T U(X) V(X)\big)_j\, c_j(X),
  \]
  giving $\str(\perm_4) \le 3 < 4$, a contradiction.
  \item \emph{$2\times 2$ zero block ($(a,b)=(1,1)$):} $B(X)$ takes the block form
  \[
    B(X) = \begin{pmatrix} a(X) & b_1(X) & b_2(X) \\ c_1(X) & 0 & 0 \\ c_2(X) & 0 & 0 \end{pmatrix}
  \]
  for linear forms $a, b_1, b_2, c_1, c_2 \in \mathbb{C}[X]_1$. Direct computation of the $2\times 2$ cofactors shows that the first row and first column of $\adj(B(X))$ vanish, and
  \[
    \adj(B(X)) = \tilde{b}(X)\,\tilde{c}(X)^T, \qquad
    \tilde{b}(X) := \begin{pmatrix} 0 \\ b_2(X) \\ -b_1(X) \end{pmatrix}, \quad
    \tilde{c}(X) := \begin{pmatrix} 0 \\ -c_2(X) \\ c_1(X) \end{pmatrix},
  \]
  which is either identically zero or a rank-$1$ outer product of linear vectors. Therefore,
  \[
    \perm_4(X) = -\tilde{c}(X)^T \big(U(X) V(X) \tilde{b}(X)\big)
    = c_2(X)\big(U(X) V(X) \tilde{b}(X)\big)_2 - c_1(X)\big(U(X) V(X) \tilde{b}(X)\big)_3,
  \]
  giving $\str(\perm_4) \le 2 < 4$, a contradiction.
  \item \emph{Primitive skew-symmetric type:} $B(X) \in \mathfrak{so}_3(\mathbb{C})$, i.e.,
  \[
    B(X) = \begin{pmatrix} 0 & \ell_3 & -\ell_2 \\ -\ell_3 & 0 & \ell_1 \\ \ell_2 & -\ell_1 & 0 \end{pmatrix}
  \]
  for $\ell(X) = (\ell_1,\ell_2,\ell_3)^T \in \mathbb{C}[X]_1^3$. Then $\adj(B(X)) = \ell(X)\ell(X)^T$, so
  \[
    \perm_4(X) = -\ell(X)^T U(X) V(X) \ell(X) = -\sum_{i=1}^3 \ell_i(X)\, \big(U(X) V(X) \ell(X)\big)_i,
  \]
  again giving $\str(\perm_4) \le 3 < 4$, a contradiction.
\end{enumerate}
```

Bu düzeltme eklendiğinde `Proposition 4.1` (`Case r = 3`) ile birlikte `dc_perm4_ge_10.tex` içindeki lineer cebir vaka analizi mantıksal olarak kapanmaktadır [İSPAT].

### (b) Bağımsız Macaulay2 & Singular Betikleri (B-hesaplamalı-cebir)
Aşağıdaki betikler yerleşik hiçbir `permanent` fonksiyonu çağırmadan açık $S_3$/$S_4$ permütasyon toplamını kullanır ve makinede M2/Singular/Sage kurulu olmadığı için sonuç beklentileri **[KESİN HESAP — HENÜZ ÇALIŞTIRILMADI]** olarak işaretlenmiştir.

---

### 1. Macaulay2 Betiği (`verify_sing_perm.m2`) — [KESİN HESAP — HENÜZ ÇALIŞTIRILMADI]

```m2
-- Çalıştırma: M2 --script verify_sing_perm.m2
explicitPerm = (X, n) -> sum(permutations toList(0..n-1), s -> product(0..n-1, i -> X_(i, s#i)));

-- (i) perm_3 pozitif kontrolü: codim(Sing(V(perm_3))) == 6
R3 = (ZZ/32749)[x_0..x_8];
X3 = genericMatrix(R3, 3, 3);
f3 = explicitPerm(X3, 3);
J3 = ideal diff(vars R3, f3);
assert(codim J3 == 6);
print "PASS perm_3: codim J3 == 6";

checkSubspace = (J4, R4, M, p, expectZero) -> (
  k := numColumns M;
  S := (ZZ/p)[t_0..t_(k-1)];
  Ms := sub(M, S);
  lin := transpose(Ms * transpose vars S);
  assert(codim ideal lin == k); -- rank_Fp(M) == k kontrolü
  phi := map(S, R4, lin);
  I := phi J4;
  if expectZero then (
    assert(codim I == 8);
    assert(hilbertFunction(9, S/I) == 0);
  ) else (
    assert(dim(S/I) >= 1);
  );
);

-- (ii) perm_4 Jakobiyen ideali, L_8 kesiti ve (iii) L_9 + 5 rastgele F_p kesiti
for p in {32749, 65521} do (
  R4 := (ZZ/p)[x_0..x_15];
  X4 := genericMatrix(R4, 4, 4);
  f4 := explicitPerm(X4, 4);
  J4 := ideal diff(vars R4, f4);
  assert(codim J4 == 8);

  -- Python betiğindeki M_L8 ve M_L9 matrisleri dışa aktarılıp yüklenir (aşağıda protokolde)
  load "L8_L9_matrices.m2"; -- M_L8 (16x8) ve M_L9 (16x9) tanımlar
  checkSubspace(J4, R4, M_L8, p, true);
  checkSubspace(J4, R4, M_L9, p, false);

  for trial from 1 to 5 do (
    Mrand := matrix table(16, 8, (i, j) -> random p);
    checkSubspace(J4, R4, Mrand, p, true);
  );
  print("PASS perm_4 mod " | toString p);
);
```

---

### 2. Singular Betiği (`verify_sing_perm.sing`) — [KESİN HESAP — HENÜZ ÇALIŞTIRILMADI]

```singular
// Çalıştırma: Singular -q verify_sing_perm.sing
proc perm3(matrix X) {
  poly s = 0; int a, b, c;
  for (a = 1; a <= 3; a++) {
    for (b = 1; b <= 3; b++) { if (b != a) {
      c = 6 - a - b;
      s = s + X[1,a]*X[2,b]*X[3,c];
    }}
  }
  return(s);
}

proc perm4(matrix X) {
  poly s = 0; int a, b, c, d;
  for (a = 1; a <= 4; a++) {
    for (b = 1; b <= 4; b++) { if (b != a) {
      for (c = 1; c <= 4; c++) { if (c != a && c != b) {
        d = 10 - a - b - c;
        s = s + X[1,a]*X[2,b]*X[3,c]*X[4,d];
      }}
    }}
  }
  return(s);
}

// (i) perm_3 pozitif kontrolü
ring R3 = 32749, (x(1..9)), dp;
matrix X3[3][3];
int idx = 1; int i; int j;
for (i = 1; i <= 3; i++) { for (j = 1; j <= 3; j++) { X3[i,j] = var(idx); idx++; } }
ideal G3 = std(jacob(perm3(X3)));
if (9 - dim(G3) != 6) { ERROR("FAIL: perm_3 codim != 6"); }
"PASS perm_3: codim == 6";

proc test_perm4_for_prime(int p) {
  ring R4 = p, (x(1..16)), dp;
  matrix X4[4][4];
  int idx = 1; int i; int j;
  for (i = 1; i <= 4; i++) { for (j = 1; j <= 4; j++) { X4[i,j] = var(idx); idx++; } }
  ideal J4 = jacob(perm4(X4));
  if (16 - dim(std(J4)) != 8) { ERROR("FAIL: perm_4 codim != 8"); }

  // Python'dan üretilen L8_L9_matrices.sing dosyası M8[16][8] ve M9[16][9] yükler
  < "L8_L9_matrices.sing";

  // L_8 pozitif sertifika (dim == 0 ve derece 9 tam rank)
  ring S8 = p, (t(1..8)), dp;
  ideal lin8;
  for (i = 1; i <= 16; i++) {
    poly lf = 0;
    for (j = 1; j <= 8; j++) { lf = lf + M8[i,j]*t(j); }
    lin8[i] = lf;
  }
  if (dim(std(lin8)) != 0) { ERROR("FAIL: rank(M8) < 8"); }
  map phi8 = R4, lin8;
  ideal G8 = std(phi8(J4));
  if (dim(G8) != 0) { ERROR("FAIL: L_8 dim != 0"); }
  if (size(reduce(maxideal(9), G8)) != 0) { ERROR("FAIL: L_8 corank(D=9) != 0"); }

  // L_9 negatif kontrol (dim >= 1)
  ring S9 = p, (t(1..9)), dp;
  ideal lin9;
  for (i = 1; i <= 16; i++) {
    poly lf = 0;
    for (j = 1; j <= 9; j++) { lf = lf + M9[i,j]*t(j); }
    lin9[i] = lf;
  }
  if (dim(std(lin9)) != 0) { ERROR("FAIL: rank(M9) < 9"); }
  map phi9 = R4, lin9;
  ideal G9 = std(phi9(J4));
  if (dim(G9) < 1) { ERROR("FAIL: L_9 dim < 1"); }

  // 5 rastgele F_p altuzay (k = 8)
  setring S8;
  int tr;
  for (tr = 1; tr <= 5; tr++) {
    ideal linr;
    for (i = 1; i <= 16; i++) {
      poly lf = 0;
      for (j = 1; j <= 8; j++) { lf = lf + random(0, p - 1)*t(j); }
      linr[i] = lf;
    }
    if (dim(std(linr)) == 0) {
      map phir = R4, linr;
      ideal Gr = std(phir(J4));
      if (dim(Gr) != 0) { ERROR("FAIL: random L_8 dim != 0"); }
    }
  }
  "PASS perm_4 mod " + string(p);
}

test_perm4_for_prime(32749);
test_perm4_for_prime(65521);
quit;
```

---

### 3. SageMath Betiği (`verify_sing_perm.sage`) — [KESİN HESAP — HENÜZ ÇALIŞTIRILMADI]

```python
# Çalıştırma: sage verify_sing_perm.sage
import numpy as np

def explicit_perm(X, n):
    return sum(prod(X[i, p[i]] for i in range(n)) for p in Permutations(range(n)))

# (i) perm_3 pozitif kontrolü
R3 = PolynomialRing(GF(32749), 9, 'x')
X3 = matrix(R3, 3, 3, R3.gens())
f3 = explicit_perm(X3, 3)
J3 = R3.ideal([f3.derivative(v) for v in R3.gens()])
assert 9 - J3.dimension() == 6

M_L8_py = np.random.default_rng(2026).integers(-2, 3, size=(16, 8))
M_L9_py = np.random.default_rng(2026).integers(-2, 3, size=(16, 9))

for p in (32749, 65521):
    Fp = GF(p)
    R4 = PolynomialRing(Fp, 16, 'x')
    X4 = matrix(R4, 4, 4, R4.gens())
    f4 = explicit_perm(X4, 4)
    J4 = R4.ideal([f4.derivative(v) for v in R4.gens()])
    assert 16 - J4.dimension() == 8

    # L_8 + 5 rastgele F_p kesiti
    S8 = PolynomialRing(Fp, 8, 't')
    t8 = vector(S8.gens())
    mats8 = [matrix(Fp, M_L8_py.tolist())] + [random_matrix(Fp, 16, 8) for _ in range(5)]
    for idx, M in enumerate(mats8):
        assert M.rank() == 8
        I8 = S8.ideal([g.subs(dict(zip(R4.gens(), M * t8))) for g in J4.gens()])
        assert I8.dimension() == 0
        if idx == 0:
            assert max(m.degree() for m in I8.normal_basis()) < 9  # D=9 corank == 0

    # L_9 negatif kontrol
    S9 = PolynomialRing(Fp, 9, 't')
    t9 = vector(S9.gens())
    M9 = matrix(Fp, M_L9_py.tolist())
    assert M9.rank() == 9
    I9 = S9.ideal([g.subs(dict(zip(R4.gens(), M9 * t9))) for g in J4.gens()])
    assert I9.dimension() >= 1
print("PASS SageMath")
```

---

### 4. Çalıştırma ve Matris Dışa Aktarım Protokolü — [KESİN HESAP — HENÜZ ÇALIŞTIRILMADI]
1. **Aynı `L_8`/`L_9` matrislerini dışa aktarma:** Python'da `np.random.default_rng(2026).integers(-2, 3, size=(16, k))` çıktısı `L8_L9_matrices.m2` (`M_L8 = matrix {{...}}; M_L9 = matrix {{...}};`) ve `L8_L9_matrices.sing` (`intmat M8[16][8] = ...; intmat M9[16][9] = ...;`) olarak yazılır; böylece M2, Singular ve Sage Python'daki aynı altuzayları denetler.
2. **Sıralı çalıştırma:**
   - `M2 --script verify_sing_perm.m2`
   - `Singular -q verify_sing_perm.sing`
   - `sage verify_sing_perm.sage`
3. **Kabul ölçütü:** Üç bağımsız CAS motorunun tamamında `perm_3` için `codim == 6`, `perm_4` Jakobiyeni için `codim == 8`, `L_8` için hem $p_1=32749$ hem $p_2=65521$'de `dim == 0` ve $D=9$ korank sıfırlanması, `L_9` için `dim >= 1` ve 5 rastgele $\mathbb{F}_p$-altuzayı için `dim == 0` elde edilmesi Teorem 3.1'i bağımsız olarak doğrular [İSPAT].

### (b-ek) Bağımsız Yeniden Üretim Protokolü Denetimi (B-deneysel-doğrulama)
* **Yanlış-pozitif ve kapsam riski (Singular):** `verify_sing_perm.sing` içindeki `if (dim(std(linr)) == 0)` bloğu, rastgele `linr` rankı $<8$ çıktığında hata vermek yerine deneyi sessizce atlayarak yanlış-pozitif riski doğurur [KESİN HESAP]. Ayrıca `test_perm4_for_prime` iki asal için çağrıldığında prosedür içinde `< "L8_L9_matrices.sing"` çalıştırmak `intmat` yeniden bildirim hatasına yol açabileceğinden matrisler prosedür dışında bir kez yüklenmelidir [LİTERATÜR-DOĞRULANMADI].
* **Matris kaynağı tutarsızlığı (SageMath):** `verify_sing_perm.sage`, M2 ve Singular gibi dışa aktarılan dosyayı okumak yerine doğrudan `np.random.default_rng(2026)` çağırır ve farklı NumPy sürümlerinde farklı altuzay üretme riski taşır [KESİN HESAP]. `M_L8` ve `M_L9` RNG yerine sabit tamsayı dizisi olarak tanımlanıp tüm CAS betiklerine tek kaynaktan verilmelidir [SANI].
* **16-değişkenli darboğaz ve $\mathbb{F}_p \to \mathbb{C}$ aktarımı:** Üç betik de $L_8$ kesitinden önce 16 değişkenli `J4` için tam Gröbner tabanı (`codim == 8`) hesaplar; bu gereksiz darboğazdır çünkü Teorem 3.1 alt sınırı için yalnız $L_8$ üzerinde $\dim(S/I)=0$ yeterlidir [İSPAT]. Sonlu cisimde $(S/I)_9 = 0$ çıkması, her derecede $\dim_{\mathbb{Q}}(M \otimes \mathbb{Q}) \le \dim_{\mathbb{F}_p}(M \otimes \mathbb{F}_p)$ nedeniyle $\codim_{\mathbb{C}}(\Sing(V(\perm_4))) \ge 8$ sonucunu koşulsuz sağlar [İSPAT].
* **Rastgele altuzaylarda yanlış-negatif riski:** 5 rastgele $\mathbb{F}_p$-altuzayının tamamında `assert(dim == 0)` zorlamak, şans eseri $\Sing(V(\perm_4))$ ile kesişen bir örnek seçildiğinde teorem doğru olsa bile betiği düşürür [İSPAT]. Rastgele denemeler kabul kapısı yapılmamalı, sertifika sabit $L_8$'e bağlanmalıdır [SANI].
* **Hilbert profili ve doğrulanmamış CAS sözdizimi:** Betikler yalnız $D=9$'u sınar; Python'daki $D=6..9$ ($[132,32,8,0]$) ve $L_9$ $D=6,7$ ($[753,580]$) korank dizilerini de karşılaştırmak `step_imsc` hatalarını yakalar [SANI]. Yerel kurulum olmadığından M2 `hilbertFunction(9, S/I)`, Singular `size(reduce(maxideal(9), G8))` ve Sage `normal_basis()` davranışları çalıştırılıp doğrulanmamıştır [LİTERATÜR-DOĞRULANMADI].

### (c) Makale Değişiklik Listesi & 'Ne İddia Ediyoruz / Etmiyoruz' (B-yazım-editörü)
### Makale Değişiklik Listesi (Baştan Kaynakçaya)

- **Başlık & Yazar (`Title/Author`) [KESİN HESAP]:** `\author{[Author Name(s) --- Draft Manuscript]}` yer tutucusu gerçek yazar ve kurum bilgisiyle değiştirilmelidir.
- **Özet (`Abstract`) [İSPAT]:** `A_{11}(X_0)K` ve `A_{11}(X_0)^2 K` ifadelerindeki tanımsız $X_0$ kaldırılıp Step 3–4'teki $A_{11}^{(\xi)}(\xi)$ notasyonuna eşitlenmelidir.
- **Giriş (`Section 1`) [LİTERATÜR-DOĞRULANMADI]:** Yabe (2015), ABV (2017), MR (2004) ve LR (2017) iddiaları ile 2026 öncesi olası $\dc_{\mathbb{C}}(\perm_4)$ öncelik yayınları (ör. Sheshadri 2026) birincil kaynaklardan teyit edilmelidir; ayrıca `\codim` alt indisleri (`\codim_{\mathbb{C}^N}` / `\codim_{\mathbb{C}^{16}}`) standardize edilmelidir `[İSPAT]`.
- **Ön Bilgiler (`Section 2`) [İSPAT]:** `\adj(B)` (kofaktör devriği konvansiyonu), `\tr` ve `\mathfrak{so}_d(\mathbb{C})` tanımlanmalı; alt matris gösterimi (`X_{\{...\}}` vs `X_{\hat{1},\hat{j}}`) tek tipe indirilmelidir.
- **Sertifika & Betik (`Section 3`, `README.md`, `.py`) [KESİN HESAP]:**
  - `Remark 3.2`'deki "generic $L_9$" ifadesi "explicit $9$-dimensional integer subspace $L_9$" yapılmalıdır `[İSPAT]`.
  - Betiğe `rank(M_L8)==8`, `rank(M_L9)==9` kontrolleri, `step_imsc`'deki `R_canon @ C_s` çarpımı için `n_S * (p-1)^2 < 2^53` taşma `assert`'i ve $\perm_3$ ($\codim = 6$) pozitif kontrolü eklenmelidir; bağımsız CAS (M2/Singular) teyidi alınmalıdır `[KESİN HESAP]`.
  - `README.md`'deki `permanent X` komutu doğrulanmalı veya açık permütasyon toplamıyla değiştirilmelidir `[KESİN HESAP]`.
- **$r=3$ Sınıflandırması (`Section 4`, `Prop. 4.1`) [İSPAT]:** $\mathrm{GL}_3 \times \mathrm{GL}_3$ ve devrik altında "two types" ifadesi üç tipe düzeltilmeli (sıfır satır/sütun devrikle eşlenir; $2\times 2$ sıfır bloklu $B = \begin{pmatrix} a & b & c \\ d & 0 & 0 \\ e & 0 & 0 \end{pmatrix}$ eklenmelidir); bu 3. tip için $\adj(B) = (0,-c,b)^T(0,e,-d)$ üzerinden $\str(\perm_4) \le 1 < 4$ çelişkisi yazılmalı, `Atkinson1983`/`EH1988` tam teorem atfı kontrol edilmelidir `[LİTERATÜR-DOĞRULANMADI]`.
- **Ana İspat & Tartışma (`Section 5`) [İSPAT]:** Step 2'deki $A_{11}, A_{13}, A_{31}, A_{33}$ indisleri $A_{11}, A_{12}, A_{21}, A_{22}$ yapılmalıdır. Boolean/SAT aktarım teoremi ayrı sonuç olarak konmamalı; `Remark 5.2` içinde yalnızca H1 ve H4'ün `[AÇIK]` olduğu vurgulanarak kısa motivasyon notu olarak anılmalıdır `[SANI]`.
- **Kaynakça (`Bibliography`) [LİTERATÜR-DOĞRULANMADI]:** Tüm 8 künyenin (özellikle `Grenet2011`, `Atkinson1983`, `EH1988`) dergi/arXiv bilgileri birincil kaynaktan doğrulanmalıdır.

---

### Önerilen 'What This Paper Does and Does Not Claim' Paragrafı (Giriş Sonuna Eklenecek) [SANI]

> **What This Paper Does and Does Not Claim.** This paper establishes $\dc_{\mathbb{C}}(\perm_4) \ge 10$ for the fixed $4\times 4$ permanent over $\mathbb{C}$ by combining hand-proved algebraic reductions with one exact finite-field IMSC rank certificate for $\codim_{\mathbb{C}^{16}}(\Sing(V(\perm_4))) = 8$ (checked modulo $32{,}749$ and $65{,}521$, pending independent CAS and $\perm_3$ positive-control checks). It does \emph{not} resolve the remaining interval $10 \le \dc_{\mathbb{C}}(\perm_4) \le 15$, does not yield asymptotic lower bounds beyond the quadratic Mignon--Ressayre barrier $O(n^2)$, and establishes neither $\mathrm{VP} \neq \mathrm{VNP}$ nor Boolean circuit lower bounds (such as for $\mathrm{SAT}$), where any quantitative transfer remains conditional on open functional ideal-modulo and structural hypotheses.

### (c-ek) Motivasyon / Tartışma — Boolean/SAT Aktarım Taslağı (B-kuantum-hesaplama)
### Önerilen Konum ve Tasarım İlkeleri (Q3)
- Bu metin ayrı bir teorem veya bağımsız aktarım sonucu olarak değil, `dc_perm4_ge_10.tex` sonundaki `Scope and limitations` notunun yerine/devamına tek alt-bölüm olarak yerleştirilmelidir `[SANI]`.
- $\dc_{\mathbb{C}}(\perm_4) \ge 10$ sonucu sabit $n=4$ ve biçimsel determinantal model için olup $O(n^2)$ bariyeri içinde kalır; dolayısıyla Boolean/SAT alt sınırı üretmez `[İSPAT]`.
- Taslaktaki **H1** (genel derinlikte $I_B$ modülo fonksiyonel alt sınır) ve **H4** (SAT-indirgenebilirlik / Ters-Toda köprüsü) tamamen açık problemler olarak sunulmuştur; ilgili dış literatür (ör. Forbes–Kumar–Saptharishi veya Toda çizgisi) birincil kaynaklardan ayrıca doğrulanmalıdır `[LİTERATÜR-DOĞRULANMADI]`.

---

### LaTeX Taslağı (`dc_perm4_ge_10.tex` sonu için)

```latex
\subsection*{Motivation and Discussion: Barriers Toward Boolean Complexity}

Our proof establishes $\dc_{\mathbb{C}}(\perm_4) \ge 10$ for the fixed size $n=4$ by combining first- and second-order singularity codimensions ($\codim \Sing(V(\perm_4)) = 8$, $\codim \Sing_2(V(\perm_4)) = 12$) with origin-isotropy. Extending this approach to $m \ge 10$ requires controlling higher Hessian rank strata $\mathcal{H}_{\le 2k}(\perm_4)$; more fundamentally, as with all singularity- and Hessian-based techniques, the method faces the quadratic Mignon--Ressayre barrier $O(n^2)$ as $n \to \infty$~\cite{MR2004} and therefore does not yield super-polynomial lower bounds for $\mathrm{VP} \neq \mathrm{VNP}$~\cite{Valiant1979}.

From a broader complexity-theoretic perspective, bridging algebraic circuit lower bounds to Boolean circuit lower bounds for $\mathrm{SAT}$ is subject to substantially stronger, currently unresolved requirements. Even if an asymptotic super-polynomial algebraic bound $\operatorname{AC}_{\mathbb{F}}(f_n) \ge 2^{n^\varepsilon}$ were known, transferring it to $\mathrm{SAT}$ would still require at least the following two hypotheses, both of which remain \textbf{completely open}:
\begin{enumerate}
  \item \textbf{H1 (General-Depth Functional Lower Bound modulo $I_B$ --- [OPEN]):} The exponential lower bound must hold not merely for $f_n$ as a formal polynomial, but for \emph{every} division-free $\mathbb{F}$-circuit computing a polynomial $g \equiv f_n \pmod{\langle x_1^2-x_1,\dots,x_n^2-x_n\rangle}$ that agrees with $f_n$ on the Boolean cube $\{0,1\}^n$. Establishing such functional lower bounds without severe depth restrictions is completely open.
  \item \textbf{H4 ($\mathrm{SAT}$-Reducibility / Reverse-Toda Bridge --- [OPEN]):} A constructive, low-depth/low-overhead reduction is required to translate non-uniform Boolean hardness of $f_n$ (or its bit-level evaluation) back into Boolean circuit lower bounds for $\mathrm{SAT}$ without unproved complexity collapses. No unconditional bridge of this form is known.
\end{enumerate}
Accordingly, Theorem~\ref{thm:main} should be viewed strictly as a sharp fixed-$n$ determinantal separation over $\mathbb{C}$, rather than a step toward unconditional Boolean or $\mathrm{SAT}$ lower bounds.
```

### Türkçe Özet Notu
- Taslak mevcut kaynakça dışına taşmadan yalnızca `MR2004` ve `Valiant1979` atıflarını kullanır; H1 ve H4'ün tamamen açık olduğunu açıkça vurgular ve makalenin bilimsel kapsamını abartısız biçimde sınırlar `[SANI]`.

### (d) Uzman Gönderim Planı & Öncelik Denetimi (B-cebirsel-karmaşıklık)
- **Öncelik sorusu (daha önce bulundu mu?):** $\mathrm{dc}_{\mathbb{C}}(\mathrm{perm}_4) \ge 10$ (veya daha güçlü bir sınırın) 2017–2026 arasında yayımlanıp yayımlanmadığını (ör. Sheshadri 2026 gibi olası çalışmalar dahil) bilmiyorum, birincil kaynaktan kontrol edilmeli [LİTERATÜR-DOĞRULANMADI]. Makaledeki MR04 ($8$), Yabe 2015 ($\mathbb{R}$ üzerinde $10$), ABV 2017 ($\mathbb{C}$ üzerinde $9$), Grenet 2011 ($15$) ve Landsberg–Ressayre 2017 ($15$, simetri altında) atıflarının kesin teorem koşulları da birincil kaynaklardan henüz doğrulanmamıştır [LİTERATÜR-DOĞRULANMADI].
- **Adım 1 — Literatür ve kapsam konumlandırması:** Gönderim öncesi arXiv, ECCC, zbMATH ve Google Scholar üzerinde $\mathrm{perm}_4$ determinantal karmaşıklığı ve ilgili tüm yazarlar için sistematik öncelik taraması yapılmalıdır [LİTERATÜR-DOĞRULANMADI]. Ayrıca makale sabit $A_0$'lı $\mathrm{dc}_{\mathbb{C}}(\mathrm{perm}_4)$ alt sınırını kanıtladığından, GCT açısından kritik olan sınır karmaşıklığı $\underline{\mathrm{dc}}_{\mathbb{C}}(\mathrm{perm}_4)$'ü kapsamadığı açıkça belirtilmelidir [İSPAT].
- **Adım 2 — İspat ve metin onarımları (Q1, Q3):** Prop. 4.1 ($r=3$) içine $2\times 2$ sıfır bloklu sıkıştırma tipi eklenmeli ve $\mathrm{adj}(B)=(0,-c,b)^T(0,e,-d)$ üzerinden $\mathrm{str}(\mathrm{perm}_4)\le 1<4$ elemesi verilerek $r=3$ vakası kapatılmalıdır [İSPAT]. `Remark 3.2` ("generic $L_9$" yerine $0\in L_9$ ve $\mathrm{rank}(M_{L_9})=9$ koşulu) ile metin içindeki $X_0$/$\xi$ tutarsızlıkları düzeltilmelidir [KESİN HESAP]. Boolean/SAT aktarım özeti ayrı teorem yapılmamalı, yalnızca H1–H4 açık koşulları vurgulanarak kısa bir "Motivasyon / Tartışma" notuyla sınırlandırılmalıdır [SANI].
- **Adım 3 — Bağımsız CAS ve betik doğrulaması (Q2):** Teorem 3.1 dış bir ortamda Macaulay2, Singular veya SageMath ile bağımsız olarak yeniden doğrulanmalı ve `README.md`'deki `M2` betiğindeki `permanent` çağrısı test edilmiş açık tanımla değiştirilmelidir [KESİN HESAP]. `verify_codim_sing_perm4.py`'ye $\mathrm{rank}(M_{L_9})=9$ kontrolü, `R_canon @ C_s` taşma sınırı denetimi ve $\mathrm{perm}_3$ ($\mathrm{codim}=6$) pozitif kontrolü eklenmelidir [SANI].
- **Adım 4 — Uzman hakem paketi:** Uzmana onarılmış LaTeX metni, bağımsız CAS günlüğü, güncellenmiş Python betiği ve öncelik tarama listesi birlikte sunulmalı; uzman görüşü özellikle $r=3$ üç-tipli sınıflandırma tamlığı ve $m\ge 10$ Hessian engeli üzerine istenmelidir [SANI].

---

## Tur 4 — mod-B Son Hükmü

## BÖLÜM I — "BUGÜN NEYİ KESİN OLARAK KAPATABİLDİK?" TABLOSU & AÇIK KRİTİK SORULAR

| Adım / İddia | Bugünkü Durum | Eksik Kalan İş |
| :--- | :--- | :--- |
| `Prop. 2.2`: $\codim \Sing_2(V(\perm_4)) = 12$ | El ile türetme eksiksiz doğrulandı `[İSPAT]` | Yok `[İSPAT]` |
| `Lem. 2.1`: $\codim \Sing(V(F)) \le 2\,\str(F)$ | Krull asal ideal teoremiyle doğrulandı `[İSPAT]` | Yok `[İSPAT]` |
| `Prop. 4.1`: $r \in \{0, 2, 4, \ge 5\}$ elemeleri | Tamamı adım adım doğrulandı `[İSPAT]` | Yok `[İSPAT]` |
| `Prop. 4.1`: $r=3$ vakası ($3\times 3$, $\rank \le 2$) | $2\times 2$ sıfır bloğu ve devrik simetrisi eksikti; $2\times 2$ sıfır blokta $\adj(B)=\tilde{b}\tilde{c}^T$ ile $\str \le 2 < 4$ türetildi `[İSPAT]` | Düzeltilmiş 3-tipli metnin `.tex`'e işlenmesi `[KESİN HESAP]`; `Atkinson1983`/`EH1988` birincil kontrolü `[LİTERATÜR-DOĞRULANMADI]` |
| `Sec. 5`: $m=9$ izotropi, 2-blok normal form, Skew-Square, $\perm_4 \in I_W^3$ | Matematiksel ispat zinciri sağlam `[İSPAT]` | `X_0`/`\xi`, `A_{13}\to A_{12}`, $d_v\in\{0,8\}$ temizliği `[KESİN HESAP]` |
| `Thm. 3.1`: $\codim \Sing(V(\perm_4)) = 8$ (`IMSC` argümanı) | `IMSC -> M_9(I)` tam rankı $\mathbb{F}_p \to \mathbb{C}$ aktarımını sağlar `[İSPAT]`; `rref` taşma marjı ($4.12\times 10^{11} < 2^{53}$) korunuyor `[KESİN HESAP]` | Bağımsız CAS (M2/Singular/Sage) çalıştırması, `perm_3` pozitif kontrolü, `M_L9` rank-9 ve `R_canon @ C_s` taşma `assert`'leri `[KESİN HESAP]` |
| `README.md` M2 `permanent X` komutu | Yerel M2 olmadığı için doğrulanamadı `[LİTERATÜR-DOĞRULANMADI]` | Açık permütasyon toplamlı M2/Singular betiğiyle değiştirme `[KESİN HESAP]` |
| Literatür & öncelik (`Yabe15`, `ABV17`, `MR04`, `LR17`, olası `Sheshadri26`) | Birincil kaynaklardan teyit edilmedi `[LİTERATÜR-DOĞRULANMADI]` | arXiv / ECCC / birincil makale taraması `[LİTERATÜR-DOĞRULANMADI]` |
| Boolean/SAT aktarım çerçevesi (`H1–H4`) | Sabit $n=4$ sınırıyla kapsam dışı ve `H1`, `H4` açık `[İSPAT]` | Ayrı teorem yapılmayıp Tartışma bölümüne alınması `[SANI]` |

### `crit-B`'nin Henüz Cevaplanmayan Kritik Soruları
1. **Birincil literatür ve öncelik:** $\dc_{\mathbb{C}}(\perm_4) \ge 10$ (veya `Sheshadri 2026` benzeri) bir sonucun önceden yayımlanıp yayımlanmadığı ile `Yabe 2015`, `ABV 2017`, `MR 2004`, `LR 2017`, `Atkinson 1983`, `EH 1988` detayları henüz birincil kaynaklardan doğrulanmadı `[LİTERATÜR-DOĞRULANMADI]`.
2. **Bağımsız CAS çıktısı:** Yerel makinede M2, Singular ve Sage bulunmadığından Teorem 3.1 tek bir Python IMSC betiği dışında henüz çalıştırılıp teyit edilmedi `[KESİN HESAP]`.
3. **M2 `permanent` sözdizimi:** `README.md` içindeki `permanent X` komutunun Macaulay2'de yerleşik olup olmadığı doğrulanmadı `[LİTERATÜR-DOĞRULANMADI]`.
4. **`perm_3` pozitif kontrolü ve `L_9` eksikliği:** `verify_codim_sing_perm4.py` içinde $\perm_3$ ($\codim = 6$) pozitif kontrolü, `rank(M_L9) == 9` kontrolü, `R_canon @ C_s` taşma `assert`'i ve $L_9$'un $D=9$'a uzatılması henüz uygulanmadı `[KESİN HESAP]`; beklenen $\codim(\Sing(V(\perm_3)))=6$ değeri de birincil kaynaktan teyit edilmelidir `[LİTERATÜR-DOĞRULANMADI]`.
5. **Yazım ve notasyon onarımı:** `X_0` tanımsızlığı, `A_{13}` blok indisleri, `Remark 3.2`'deki "generic $L_9$" çelişkisi ve koni kesişimi adımı `.tex` dosyasında henüz güncellenmedi `[KESİN HESAP]`.

---

## BÖLÜM II — ZORUNLU SON ÇIKTI BİÇİMİ

### 1. Q1 / Q2 / Q3 Karar Cevapları

**Q1 (r = 3 Düzeltmesi ve Mantıksal Kapanış):**
1. Evet; `Prop. 4.1`'deki $r=3$ boşluğu kapatıldığında makalenin cebirsel ispat zinciri mantıksal olarak tamamen kapanır `[İSPAT]`.
2. `GL_3 x GL_3` ve devrik ($M \mapsto M^T$) altında $\rank \le 2$ olan $3\times 3$ uzaylar üç tiptir: (i) sıfır satır/sütun, (ii) $2\times 2$ sıfır bloklu sıkıştırma, (iii) $\mathfrak{so}_3(\mathbb{C})$ `[İSPAT]`.
3. Eksik olan 2. tipte $B = \begin{pmatrix} a & b_1 & b_2 \\ c_1 & 0 & 0 \\ c_2 & 0 & 0 \end{pmatrix}$ için $\adj(B) = (0,b_2,-b_1)^T (0,-c_2,c_1)$ bulunur `[İSPAT]`.
4. Böylece $\perm_4 = -\tr(\adj(B)UV) = c_2(UV\tilde{b})_2 - c_1(UV\tilde{b})_3$ olup $\str(\perm_4) \le 2 < 4$ çelişkisini verir `[İSPAT]`.
5. Düzeltilmiş paragrafta devrik simetrisinin ($3\times 1$ sıfır sütun $\to$ $1\times 3$ sıfır satır) ve üç tipin açıkça yazılması gerekir `[İSPAT]`.
6. İspatın geri kalan tüm adımları ($\codim \Sing_2=12$, $r\neq 1$ elemeleri, $m=9$ izotropisi, Skew-Square, $I_W^3$) sağlamdır `[İSPAT]`.

**Q2 (codim Sing(V(perm_4)) = 8 Bağımsız Doğrulaması ve Kabul Ölçütü):**
1. Tek başına Python IMSC yerine Macaulay2, Singular ve SageMath ile açık permütasyon toplamı (`explicitPerm`) kullanılarak doğrulama yapılmalıdır `[SANI]`.
2. `verify_codim_sing_perm4.py` içine sabit tamsayı `M_L8`/`M_L9` matrisleri, `rank == 8`/`9` `assert`'leri ve `R_canon @ C_s` taşma kontrolü eklenmelidir `[KESİN HESAP]`.
3. Betiğe `perm_3` pozitif kontrolü ($\codim = 6$) eklenmeli ve `L_9` negatif kontrolü $D=9$'a kadar çalıştırılmalıdır `[KESİN HESAP]`.
4. Teoremin tutarlı sayılması için bağımsız CAS motorları aynı `M_L8` üzerinde $p_1=32749$ ve $p_2=65521$ modülo $\dim(S/I)=0$ ve $D=9$'da korank $0$ vermelidir `[İSPAT]`.
5. Ek olarak aynı CAS'larda `perm_3` için $\codim = 6$ ve `M_L9` için $\dim(S/I) \ge 1$ çıkmalıdır `[KESİN HESAP]`.
6. Rastgele $\mathbb{F}_p$-altuzayları olası yanlış-negatif riskinden ötürü kabul kapısı yapılmamalı, sertifika sabit `M_L8`'e bağlanmalıdır `[İSPAT]`.

**Q3 (Yayın Öncesi Değişiklikler ve Boolean/SAT Aktarımının Yeri):**
1. Makalede `\author` yer tutucusu doldurulmalı, özetteki tanımsız $X_0$ yerine $A_{11}^{(\xi)}(\xi)$ yazılmalı ve `A_{13}, A_{31}, A_{33}` indisleri `A_{12}, A_{21}, A_{22}` yapılmalıdır `[KESİN HESAP]`.
2. `Prop. 4.1` ($r=3$) 3-tipli düzeltilmeli, Step 2'de $d_v \in \{0,8\}$ sınırları ve Thm. 3.1'de koni kesişimi ile `Remark 3.2` ("explicit $L_9$") netleştirilmelidir `[İSPAT]`.
3. Giriş sonuna sınırları çizen *"What This Paper Does and Does Not Claim"* paragrafı eklenmelidir `[SANI]`.
4. `README.md`'deki doğrulanmamış `permanent X` komutu açık toplamla değiştirilmeli ve tüm literatür/öncelik iddiaları birincil kaynaktan denetlenmelidir `[LİTERATÜR-DOĞRULANMADI]`.
5. Boolean/SAT aktarım çerçevesi sabit $n=4$ sonucuyla ölçek ve model uyumsuzluğu taşıdığından ayrı teorem olarak konmamalıdır `[İSPAT]`.
6. Aktarım çerçevesi yalnızca makale sonundaki *"Motivation and Discussion"* bölümünde `H1` ve `H4` açık problemleri vurgulanarak kısa bağlam notu yapılmalıdır `[SANI]`.

---

### 2. "Kesin Olarak Doğru Bulunanlar" ve "Hâlâ Doğrulanmamış Olanlar"

**Kesin Olarak Doğru Bulunanlar:**
- `Prop. 2.2` ($\codim \Sing_2(V(\perm_4)) = 12$) ve `Lem. 2.1` ($\codim \Sing \le 2\,\str$) ispatları doğrudur `[İSPAT]`.
- `Prop. 4.1` içindeki $r=0, 2, 4, \ge 5$ elemeleri ve $2\times 2$ sıfır bloklu $r=3$ düzeltmesiyle $\corank(A_0)=1$ çıkarımı doğrudur `[İSPAT]`.
- `Sec. 5`'teki $\Omega$-izotropi ($\dim W = 8$), 2-blok normal form ($u_1 = Ky$), $[t^3]=0$ $\xi$-ayrıştırması, Skew-Square Lemması ve $\perm_4 \in I_W^3 \implies W^\perp \subseteq \Sing_2$ zinciri doğrudur `[İSPAT]`.
- Tek asalda $\mathbb{F}_p$-tam sütun rankı $\mathbb{Q}$ ve $\mathbb{C}$'de tam rankı zorunlu kılar; $L_8$ üzerinde `IMSC` kapanışı koni varsayımıyla $\codim \Sing \ge 8$ sonucunu verir `[İSPAT]`.
- `rref_mod_p_exact` içindeki `block_size * (p-1)^2 < 2^53` taşma sınırı (`96 * 65520^2 = 4.12e11 < 2^53`) sağlanmaktadır `[KESİN HESAP]`.

**Hâlâ Doğrulanmamış Olanlar:**
- Teorem 3.1'in (`L_8` tam rank ve `L_9` pozitif korank) Macaulay2, Singular veya SageMath gibi bağımsız bir CAS'ta çalıştırılıp teyit edilmesi `[KESİN HESAP]`.
- `perm_3` ($\codim = 6$) pozitif kontrolünün kodlanması/çalıştırılması `[KESİN HESAP]` ve beklenen `6` değerinin birincil kaynaktan teyidi `[LİTERATÜR-DOĞRULANMADI]`.
- `README.md` içindeki M2 `permanent X` komutunun geçerliliği `[LİTERATÜR-DOĞRULANMADI]`.
- `Yabe 2015`, `ABV 2017`, `MR 2004`, `LR 2017`, `Grenet 2011`, `Atkinson 1983`, `EH 1988` künyeleri ile olası daha yeni $\dc_{\mathbb{C}}(\perm_4)$ öncelik yayınları (ör. `Sheshadri 2026`) `[LİTERATÜR-DOĞRULANMADI]`.
- `H1–H4` aktarım çerçevesindeki dış literatür ve kesik kalan `H3–H4` tam koşulları `[LİTERATÜR-DOĞRULANMADI]`.

---

### 3. Gruptaki En Güçlü İtiraz ve Nasıl Karşılandığı
- **En güçlü itiraz (`crit-B` + İç Denetim):** (i) `Prop. 4.1` $r=3$ vakasında $2\times 2$ sıfır bloklu sıkıştırma tipinin ve sıfır sütun devrik eşleniğinin eksik olması, (ii) Teorem 3.1'in tek tohumlu (`2026`) bir Python betiğine dayanıp bağımsız CAS, `perm_3` pozitif kontrolü ve `M_L9` rank-9 denetimi içermemesi ve (iii) literatür önceliğinin kontrolsüz kalması makalenin hakemden doğrudan ret almasına yol açar `[SANI]`.
- **Nasıl karşılandı:** $r=3$ eksikliği doğrudan kofaktör hesabıyla onarılarak $\adj(B)=\tilde{b}\tilde{c}^T$ üzerinden $\str(\perm_4)\le 2<4$ olarak kapatıldı `[İSPAT]`. Doğrulama açığı için açık permütasyon toplamlı M2/Singular/Sage betikleri ve sabit matrisli `assert` protokolü üretildi `[KESİN HESAP]`. Literatür ve CAS çalıştırması ise dış kaynak/araç gerektirdiğinden açık kapanış kapısı olarak raporlandı `[LİTERATÜR-DOĞRULANMADI]`.

---

### 4. Güven Düzeyi ve Nedeni
- **Makale içi cebirsel argüman (düzeltilmiş $r=3$ ile): Yüksek** — $\Sing_2$, `Prop. 4.1`, Skew-Square ve $I_W^3$ adımlarının tamamı kapalı formda adım adım yeniden türetildi `[İSPAT]`.
- **Teorem 3.1 ve Yayın Hazırlığı (mevcut haliyle): Orta–Düşük** — İspatın tek sayısal/cebirsel girdisi olan `codim Sing = 8` sonucu bağımsız CAS'ta henüz çalıştırılmamıştır `[KESİN HESAP]` ve literatür öncelik taraması tamamlanmamıştır `[LİTERATÜR-DOĞRULANMADI]`.

---

### 5. Bir Sonraki Somut Tek Adım
- `verify_codim_sing_perm4.py` betiğine sabit `M_L8`/`M_L9` matrislerini, `rank == 8/9` ve `R_canon @ C_s` taşma `assert`'lerini, $L_9$ için $D=9$ çalıştırmasını ve `perm_3` pozitif kontrolünü ekleyip M2/Singular kurulu bir ortamda `verify_sing_perm.m2` / `verify_sing_perm.sing` betiklerini çalıştırarak çıktıları `dc_perm4_ge_10.tex`'in düzeltilmiş sürümüne paralel biçimde doğrulamak `[SANI]`.

---

### 6. Azınlık Görüşleri ve Çatışma Çözümü
- **$\str \le 1$ vs. $\str \le 2$ çatışması (Tur 2–3):** `B-hesaplamalı-cebir`, `B-cebirsel-karmaşıklık`, `B-yazım-editörü` ve `B-matematiksel-fizik`, $2\times 2$ sıfır blokta $\adj(B) = \tilde{b}\tilde{c}^T$ olduğu için $\perm_4 = -\tilde{c}^T U V \tilde{b}$ ifadesinin $\str(\perm_4) \le 1$ verdiğini öne sürmüştür `[SANI]`. Ancak $U \in \mathbb{C}[X]_1^{3\times w}$ ve $V \in \mathbb{C}[X]_1^{w\times 3}$ ($w = m-3 \ge 2$) olduğundan $(\tilde{c}^T U)(V \tilde{b})$ çarpımı $w$ adet kuadratik terimin toplamıdır ve $\str \le 1$ vermez; doğru sınır $\tilde{c}^T = (0, -c_2, c_1)$ açılımıyla $\str(\perm_4) \le 2 < 4$ olmalıdır (`B-lineer-cebir`, `B-mantık-ispat`, `B-istatistiksel-fizik`, `B-kuantum-hesaplama`, `B-deneysel-doğrulama`) `[İSPAT]`.
- **Rastgele altuzay kapısı (Tur 3):** `B-hesaplamalı-cebir` 5 rastgele $\mathbb{F}_p$-altuzayının tamamında `dim == 0` şartını kabul ölçütüne eklemeyi önermiştir `[SANI]`. `B-deneysel-doğrulama`, şans eseri tekillik konisiyle kesişen altuzay seçilmesinin sahte redde yol açacağını belirterek kabul kapısının sabit `M_L8`'e bağlanmasını savunmuştur; bu itiraz haklıdır `[İSPAT]`.

---

### `mod-B` Son Değerlendirmesi
Grup B dört tur sonunda makalenin el ile yapılan tüm cebirsel zincirini (`Prop. 2.2`, onarılmış `Prop. 4.1`, `Sec. 5`) kendi içinde tutarlı biçimde doğrulamış ve $r=3$ vakasındaki $\str \le 1$ / $\str \le 2$ alt sınır hatasını temizlemiştir `[İSPAT]`. Buna karşılık çalışma mevcut haliyle uzmana veya dergiye gönderilmeye hazır değildir: bağımsız CAS doğrulaması, `perm_3` pozitif kontrolü, LaTeX notasyon düzeltmeleri ve birincil literatür/öncelik taraması tamamlanmadan gönderim yapılmamalıdır `[SANI]`.
