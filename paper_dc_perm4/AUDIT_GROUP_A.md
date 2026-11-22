# GRUP A ('Kanıt Denetimi' — 12 Ajan, 4 Tur) Denetim Dosyası

## Tur 1 — Bağımsız Okuma (10 Uzman)

### A-cebirsel-geometri
- **Prop 4.1 ($r=3$) eksik tip hatası:** Rank $\le 2$ olan $3\times 3$ matris uzaylarının yalnızca "sıfır satır" ve "çarpık-simetrik" olduğu iddiası eksiktir; $2\times 2$ sıfır bloklu sıkıştırma tipi ($B=\left(\begin{smallmatrix}a&b&c\\d&0&0\\e&0&0\end{smallmatrix}\right)$) $\det_3(B)\equiv 0$ sağlar ve diğer iki tipe indirgenemez `[İSPAT]`. Bu tipte $\adj(B)=(0,-e,d)^T(0,c,-b)$ olup $\str(\perm_4)\le 2<4$ çelişkisini verir; sıfır sütun ise devrik ile kapanır `[KESİN HESAP]`.
- **Prop 2.3 ($\Sing_2$) satır satır denetimi:** $36$ adet $2\times 2$ alt-permanent denklemi, Claim 1 (tek bileşen $K_{a,b}$), Claim 2 ($a\ge 2, b\ge 3$ elenmesi, $\mathrm{char}\neq 2$) ile $\dim=4$ ($K_{1,4}, K_{4,1}$) ve $\dim=3$ ($\perm_2=0$) katman sayımı doğrudur; $\codim(\Sing_2)=12$ geçerlidir `[İSPAT]`.
- **Teorem 3.1 ($L_8$ konik boyut indirgemesi):** $I_9\otimes\mathbb{C}=R_9\otimes\mathbb{C}$ ile $V_{\mathbb{C}}(I)=\{0\}$ elde edilir; ancak "affine dimension theorem" doğrudan $\Sing$ yerine, $0\in Z_i\cap L_8$ sağlayan *her indirgenemez bileşen* $Z_i$ üzerine (veya $\mathbb{P}^{15}$'te $\mathbb{P}(\Sing)\cap\mathbb{P}(L_8)=\emptyset$ üzerinden) uygulanacak şekilde netleştirilmelidir `[İSPAT]`.
- **IMSC sertifikası ve betik kontrolü:** Her syzygy satırı $I_{D+1}$ içinde kaldığından $\mathrm{corank}=0$ geçerli bir tam-sıra alt sınırıdır `[İSPAT]`. Ancak `verify_codim_sing_perm4.py` satır 139'daki `R_canon @ C_s` çarpımında `n_S*(p-1)^2 < 2^53` `assert` koruması yoktur ($L_8/L_9$ verisinde aşılmaz) ve $\perm_3$ ($\codim\Sing=6$) pozitif kontrolü eksiktir `[KESİN HESAP]`.
- **Literatür ve Macaulay2 komutu:** Atkinson (1983), Eisenbud–Harris (1988), ABV (2017), Mignon–Ressayre (2004), Yabe (2015) ifadeleri ile README'deki M2 `permanent` komutu birincil kaynaklardan veya çalışan CAS'tan doğrulanmamıştır `[LİTERATÜR-DOĞRULANMADI]`.

### A-sınırlı-rank-uzayları
- **Eksik $2\times 2$ sıkıştırma tipi (`r = 3` vakası):** Makale $\rank \le 2$ olan $3\times 3$ lineer uzayları yalnızca sıfır satır ($1\times 3$) ve $\mathfrak{so}_3$ ile sınırlıyor; oysa $2\times 2$ sıfır bloklu sıkıştırma uzayı ($b_{22}=b_{23}=b_{32}=b_{33}=0$) $\mathrm{GL}_3(\mathbb{C})\times\mathrm{GL}_3(\mathbb{C})$ ve devrik altında sıfır satır/sütuna eşlenemez, çünkü genel matrislerinin sabit sol veya sağ çekirdeği yoktur [İSPAT].
- **Eksik tipin elenmesi (düzeltme önerisi):** $b_{22}=b_{23}=b_{32}=b_{33}=0$ biçimindeki $B(X)$ için $\adj(B(X)) = p(X)q(X)^T$ çarpanlarına ayrılır; burada $p=(0,-b_{13},b_{12})^T$ ve $q=(0,b_{31},-b_{21})^T$ olup $\perm_4(X) = -q^T U V p = -b_{31}(UVp)_2 + b_{21}(UVp)_3$ elde edilir ve $\str(\perm_4) \le 2 < 4$ çelişkisiyle `r = 3` vakası kapanır [İSPAT].
- **$\mathrm{GL}_3\times\mathrm{GL}_3$ ve devriğin $M(tX)$ üzerindeki etkisi:** $\mathrm{diag}(P_1,I_w)M(tX)\mathrm{diag}(Q_1,I_w)$ çarpımı $\det M(tX)$'i $\det(P_1 Q_1)\neq 0$ sabitiyle ölçekleyerek $\str$'yi korur, tüm blok matrise uygulanan $M(tX)^T$ devriği ise $B\mapsto B^T$ ile birlikte $(U,V)\mapsto(V^T,U^T)$ dönüşümü yaparak determinantı korur; metinde devriğin tüm $M(tX)$'e uygulandığı açıkça belirtilmelidir [İSPAT].
- **$\mathfrak{so}_3$ alt vakası:** $B(X)\in\mathfrak{so}_3(\mathbb{C})$ için $\adj(B(X))=\ell(X)\ell(X)^T$ ve $\str(\perm_4)\le 3$ hesabı doğrudur [KESİN HESAP].
- **Literatür sınıflandırması:** Atkinson (1983), Eisenbud–Harris (1988) ve Beasley'de $3\times 3$ $\rank\le 2$ uzayların tam listesinin ($1\times 3$, $3\times 1$, $2\times 2$ sıfır blok ve $\mathfrak{so}_3$) tam önerme/teorem numaraları birincil kaynaklardan kontrol edilmelidir [LİTERATÜR-DOĞRULANMADI].

### A-determinantal-karmaşıklık
- **Literatür denetimi:** ABV 2017 ($\dc_{\mathbb{C}}(f)\ge \codim(\Sing(V(f)))+1$ için $d>2$, $\codim\ge 5$ koşulları ve $\perm_4\ge 9$), Mignon–Ressayre 2004 ($n^2/2$), Yabe 2015 ($\dc_{\mathbb{R}}\ge (n-1)^2+1$ ve reel imza gerekçesi) ile Landsberg–Ressayre 2017 (simetri altgrubu koşulu) iddiaları birincil kaynaklardan kontrol edilmelidir [LİTERATÜR-DOĞRULANMADI].
- **$r=3$ sınıflandırma boşluğu (Önerme 4.1):** Atkinson 1983 ve Eisenbud–Harris 1988 kapsamındaki $3\times 3$ rank $\le 2$ tipleri birincil kaynaktan doğrulanmalıdır [LİTERATÜR-DOĞRULANMADI]. Makale $2\times 2$ sıfır bloklu $B=\begin{pmatrix}b_{11}&b_{12}&b_{13}\\ b_{21}&0&0\\ b_{31}&0&0\end{pmatrix}$ sıkıştırma tipini atlamıştır; bu tipte $\adj(B)=p\,q^T$ ($p=(0,b_{13},-b_{12})^T$, $q=(0,-b_{31},b_{21})^T$) olduğundan $\perm_4=b_{31}(UVp)_2-b_{21}(UVp)_3$ yazılır ve $\str(\perm_4)\le 2<4$ elde edilir [İSPAT]. Sıfır sütun durumu da $\adj(B)=e_3 c(X)^T$ ile $\str(\perm_4)\le 3$ vererek ayrıca yazılmalıdır [İSPAT].
- **Sınır karmaşıklığı ($\underline{\dc}_{\mathbb{C}}$) kapsamı:** İspat yalnızca kesin $\dc_{\mathbb{C}}(\perm_4)\ge 10$ sonucunu verir; $\varepsilon$-degenerasyonlara izin veren sınır determinantal karmaşıklığı ($\underline{\dc}_{\mathbb{C}}(\perm_4)$) bu Schur açılımıyla kapsanmadığından kapsam sınırı açıkça belirtilmelidir [İSPAT].
- **Uç blok durumları (Ana İspat):** Adım 2–4'te $d_v=0$ ($v\equiv 0$) veya $d_z=0$ ($u=Ky$) uç durumlarında alt blokların boş kaldığı ve $\perm_4\in I_W^3$ sonucunun yine sağlandığı açıkça not edilmelidir [İSPAT].
- **Sertifika bağımlılığı:** Ana Teorem'deki $\dc_{\mathbb{C}}(\perm_4)\ge 10$ sınırı, $\codim(\Sing(V(\perm_4)))=8$ değerini veren tekil Teorem 3.1 sertifikasına mantıksal olarak bağlıdır [İSPAT].

### A-lineer-cebir
- **Prop 4.1 ($r=3$) sınıflandırma boşluğu ve düzeltmesi [İSPAT]:** Rank $\le 2$ olan $3\times 3$ lineer matris uzaylarının $\mathrm{GL}_3(\mathbb{C})\times\mathrm{GL}_3(\mathbb{C})$ ve devrik altındaki sınıflandırmasında $2\times 2$ sıfır blok tipi atlanmıştır (sıfır sütun ise devrikle sıfır satıra eşlenir). Düzeltme: Alt-sol $2\times 2$ bloğu sıfır olan $B(X)$ için $\adj(B) = (-b_{12}, b_{11}, 0)^T (0, b_{33}, -b_{23})$ biçiminde rank $\le 1$ çarpanlarına ayrılır; böylece $\perm_4 = -\tr(\adj(B)UV) = -b_{33}(UV\alpha)_2 + b_{23}(UV\alpha)_3$ ($\alpha=(-b_{12},b_{11},0)^T$) olup $\str(\perm_4)\le 2 < 4$ çelişkisini verir.

- **Prop 4.1 ($r=0,2,4,\ge 5$) ve Schur açılımı [İSPAT]:** Denklem (2) Schur açılımı, $r=0$ ($0=1$), $r\ge 5$ ($[t^4]=0$), $r=4$ ($\codim B^{-1}(\Sigma_2)\le 4 < 8$) ve $r=2$ ($d_2=0, d_3=0, d_4=\perm_4$ katsayıları ile $\mathbb{C}[X]$ UFD ayrımı) adımlarının tamamı satır satır tutarlıdır.

- **Skew-Square Lemması ($K$ tekilken) [İSPAT]:** $K^T=-K$ ve $(MK)^T=-MK \implies KM^T=MK$ çıkarımı ile $(M^2K)^T = K^T(M^T)^2 = (-KM^T)M^T = (-MK)M^T = -M(KM^T) = -M^2K$ türetimi tersinirlik gerektirmez; $K$ tekilken (ve $K=0$ iken) tamamen geçerlidir.

- **Teorem 1.1 Adım 1–4 satır denetimi [İSPAT]:** $b(X)\equiv 0$, $[t^2],[t^3],[t^4]$ açılımları, $\Omega$-izotropisinden $\dim W=8$, $\xi$-derecesi $1$ olan terimlerin $(y,z)$-biderece ayrımından $A_{13}^{(\xi)}=0$ ve $(A_{11}^{(\xi)}K)^T=-A_{11}^{(\xi)}K$, ardından $\perm_4\in I_W^3 \implies W^\perp\subseteq\Sing_2$ zinciri doğrudur; yalnızca Adım 2'de $d_v=0$ ($v\equiv 0 \implies \perm_4\equiv 0$) ve $d_v=8$ ($z, A_{13}$ boş) sınır halleri bir cümleyle belirtilmelidir.

- **Atkinson (1983) ve Eisenbud–Harris (1988) kapsamı [LİTERATÜR-DOĞRULANMADI]:** $3\times 3$ rank $\le 2$ uzayların üçlü sınıflandırmasının bu iki kaynaktaki kesin teorem referansları ve cisim/karakteristik koşulları birincil kaynaklardan doğrulanmalıdır.

### A-değişmeli-cebir
- **IMSC–Hilbert denkliği ve metin boşluğu:** $I$ derece $3$'te üretildiğinden $I_{D+1}=\sum_{i=1}^k t_i I_D$ geçerlidir; `step_imsc` içinde üretilen $\beta - R_{\mathrm{canon}}(\beta)$ ($\beta \in S_{D+1}$) ve $t_v C_D(\alpha_v) - R_{\mathrm{canon}}(\beta)$ satırları $W_0 = \mathrm{span}(S_{D+1})$ içinde tam olarak $W_0 \cap I_{D+1}$ uzayını gerer, dolayısıyla $n_S - \mathrm{rank}(M_{\mathrm{syz}}) = \dim_{\mathbb{F}_p}(R_{D+1}/I_{D+1})$ olup Macaulay eş-rankıyla birebir denktir [İSPAT]. Teorem 3.1 kanıtı $\beta \in S_{D+1}$ durumunu açıkça formüle etmeden yalnızca çarpan çiftlerini yazmaktadır; $S_{D+1}$ indirgeme bağıntısı metne açıkça eklenmelidir [İSPAT].
- **`C_next` çarpımında taşma koruması eksikliği:** `rref_mod_p_exact` içinde `block_size*(p-1)^2 < 2^53` kontrolü bulunmasına karşın `step_imsc` içindeki `R_canon @ C_s` çarpımında koruma `assert`i yoktur; $L_8$ ($n_S \le 1056$) ve $p_2 = 65{,}521$ için $n_S(p_2-1)^2 \approx 4.53\times 10^{12} < 2^{53}$ olduğundan mevcut koşuda taşma oluşmaz ancak genel güvenlik için `assert` eklenmelidir [KESİN HESAP].
- **$r=2$ UFD ve sütun işlemi adımı:** $\mathbb{C}[X]$ UFD'sinde lineer bağımsız $b_1, b_2 \in \mathbb{C}[X]_1$ için $\gcd(b_1,b_2)=1$ ve $b_1 Q_{22}=b_2 Q_{21} \implies Q_{21}=b_1\ell, Q_{22}=b_2\ell$ adımı geçerlidir [İSPAT]. Doğrusal bağımlı durumda $b_2=0$ yapan sütun işleminin blok yapısında $V \mapsto Q_r^{-1} V$ dönüşümünü de içerdiği belirtilmelidir [İSPAT].
- **$I_W = \langle y, z \rangle$ ve $\Sing_2$ içerimi:** $I_W$ bağımsız lineer formlarla üretildiğinden $\perm_4 \in I_W^3$ tüm $\le 2$. mertebeden kısmi türevleri $I_W$'ye düşürür ve $W^\perp \subseteq \Sing_2(V(\perm_4))$ sağlar [İSPAT]. Adım 2'de $\perm_4 \not\equiv 0$ nedeniyle $d_v \ge 1$ olduğu not edilmelidir [İSPAT].
- **Macaulay2 doğrulaması:** `README.md` içindeki M2 betiğinde `permanent` fonksiyonunun varlığı ve `verify_codim_sing_perm4.py` çıktısının bağımsız CAS ile uyumu doğrulanmamıştır [LİTERATÜR-DOĞRULANMADI].

### A-kombinatorik
1. **Prop 2.3 — $G(X)$ ve $K_{a,b}$ indirgemesi `[İSPAT]`:** $\perm_4$'ün sıfır olmayan ikinci türevleri tam olarak $\binom{4}{2}^2 = 36$ adet $2\times 2$ alt-permanenttir. Sav 1 uyarınca herhangi iki kenar ya köşe paylaşır ya da $C_4$'e tamamlanır; dolayısıyla en fazla bir kenarlı bileşen bulunur ve bu bileşen $K_{a,b}$ tam ikipartili grafiğidir. Yalnızca *"every induced 2-edge matching completes to a 4-cycle"* ifadesi terminolojik olarak yanlıştır (*induced* eşleşme $C_4$'e tamamlanamaz; *"every 2-edge matching..."* yazılmalıdır).

2. **Prop 2.3 — $\mathrm{char}\neq 2$ altında $(a\ge 2, b\ge 3)$ çelişkisi `[İSPAT]`:** $K_{2,3}$ alt-bloğunda $\{1,2\}$, $\{2,3\}$, $\{1,3\}$ sütun çiftlerinden türetilen oran eşitlikleri $x_{2,1}/x_{1,1} = -x_{2,1}/x_{1,1}$ sonucunu verir; tüm girişler sıfır dışı ve $\mathrm{char}\neq 2$ olduğundan çelişki kesindir.

3. **Prop 2.3 — Bileşen sayımı ($4+4+36$) ve ters yön `[İSPAT]`:** $4$ satır ($K_{1,4}$, $\dim=4$), $4$ sütun ($K_{4,1}$, $\dim=4$) ve $36$ adet $2\times 2$ blokta $\perm_2(X_{I,J})=0$ ($\dim=3$) sayımı tamdır. Ancak *"Conversely..."* cümlesi yalnızca satır/sütun uzaylarını anmakta; 36 kuadrik bileşenin de diğer $2\times 2$ bloklarda en az bir sıfır satır/sütun bırakacağı için denklem (1)'i sağladığını açıkça belirtmelidir.

4. **`subperm3` indekslemesi (`verify_codim_sing_perm4.py`) `[KESİN HESAP]`:** `build_subperm3_on_L` fonksiyonundaki `reshape(4,4,k)`, `dr, dc` atlaması ($16$ alt-permanent), `permutations(range(3))` ($6$ terim) ve `tuple(sorted((a,b,c)))` monom eşlemesi doğrudur. `run_macaulay_cascade` içindeki `A6[row_idx, ...] = coeff` ataması sabit `m_mul` için birebir olduğundan çakışma üretmez.

5. **Alt-uzay rankı doğrulaması `[İSPAT]`:** Betikte $M_{L_8}$ ve $M_{L_9}$ matrislerinin $\mathbb{F}_p$ üzerinde tam sütun rankına ($8$ ve $9$) ulaştığı doğrulanmamaktadır; $\dim L_8 = 8$ varsayımı için mod $p$ rank `assert`'i eklenmelidir.

### A-hakem
- **$r=3$ sınıflandırma boşluğu (`Prop. 4.1`):** $\rank \le 2$ olan $3\times 3$ matris uzaylarında "sıfır satır/sütun" ve "çarpık-simetrik" tiplerine ek olarak $2\times 2$ sıfır bloklu sıkıştırma tipi ($b_{21}=b_{22}=b_{31}=b_{32}=0$) eksiktir [İSPAT]. Bu tipte $\adj(B)=(-a_2,a_1,0)^T(0,b_3,-b_2)$ rank-$1$ matristir; $-\tr(\adj(B)UV)$ biçimi $\str(\perm_4)\le 2 < 4$ çelişkisini verir [KESİN HESAP].
- **$r=2$ açılımında atlanan gerekçe (`Prop. 4.1`):** $(1+t\tr(A)+\cdots)\det(B+tC_1+t^2C_2+\cdots)$ çarpımında $\det(I_w+tA)$ kaynaklı $[t^3],[t^4]$ çapraz terimlerinin $\det(B)=d_3=0$ yüzünden sıfırlandığı açıkça yazılmamıştır; bir cümleyle eklenmelidir [İSPAT].
- **Sertifika ve pozitif kontrol eksikliği (`Teorem 3.1`):** Makale yalnızca Python IMSC betiğine dayanmakta, `M_L8` matrisini açıkça vermek yerine `default_rng(2026)` çıktısına bağlamaktadır [SAYISAL]. $L_9$ negatif kontrolü doğru ideal kurulumunu kanıtlamaz; bağımsız CAS (M2/Singular) kontrolü ve $\perm_3$ ($\codim\Sing=6$) pozitif kontrolü eklenmelidir [SANI].
- **`README.md` Macaulay2 komutu:** `perm4 = permanent X;` ifadesinin geçerli Macaulay2 sözdizimi olup olmadığı doğrulanmamıştır; bağımsız CAS'ta test edilip düzeltilmelidir [LİTERATÜR-DOĞRULANMADI].
- **Literatür ve notasyon boşlukları:** Yabe (2015), ABV (2017), Mignon–Ressayre (2004), Atkinson (1983) ve Eisenbud–Harris (1988) teoremlerinin tam hipotezleri birincil kaynaklardan doğrulanmamıştır [LİTERATÜR-DOĞRULANMADI]. Ayrıca Bölüm 5 Adım 1'de $I_W$ ön-tanımsız kullanılmış ve Adım 4'te $f\in I_W^3 \Rightarrow W^\perp\subseteq\Sing_2(V(f))$ türev kuralı adımı atlanmıştır [İSPAT].

### A-mat-fizikçi-simetri
- **$A_0$ normal formu ve $r=0$ sırası [İSPAT]:** Denklem `(2)` öncesinde $P,Q \in \mathrm{GL}_m(\mathbb{C})$ için $\det(PQ)=1$ şartı konduğunda, $r=0$ ($A_0 \in \mathrm{GL}_m(\mathbb{C})$) durumunda $PA_0Q = I_m$ yalnızca $\det(A_0)=1$ iken mümkündür; oysa $\perm_4(0)=\det(A_0)=0$ doğrudan $\corank(A_0) \ge 1$ zorlar. Düzeltme: Önce $t=0$ değerlendirmesiyle $r \ge 1$ gösterilmeli; $r \ge 1$ iken $P_0$'ın ilk satırını $\det(P_0 Q_0)^{-1}$ ile ölçeklemek $0_r$ bloğunu bozmadan $\det(PQ)=1$ sağlar.
- **Schur tümleyeni ve küresel devrik simetrisi [İSPAT]:** Denklem `(3)`'teki Schur açılımı $t^r \det(I_w+tA)\det(B - \sum_{k\ge 0}(-1)^k t^{k+1}UA^kV)$ tamdır. Ancak $r=3$ ve $r=2$ vakalarında $B(X)$ üzerine uygulanan "devrik alma" işleminin, $A_0^T=A_0$ korunduğu için tüm blok matris $M(X)^T$ üzerinden ($B \mapsto B^T$, $U \leftrightarrow V^T$, $A \mapsto A^T$) yapıldığı açıkça belirtilmelidir; bu işlem $\det(M)$ ve $[t^k]$ katsayılarını değişmez bırakır.
- **$r=3$ sınıflandırmasında eksik tip [İSPAT]:** $\mathrm{GL}_3(\mathbb{C}) \times \mathrm{GL}_3(\mathbb{C})$ ve devrik altında sıfır sütun ile sıfır satır eşleniktir; fakat $2\times 2$ sıfır bloklu sıkıştırma tipi $B(X)=\begin{pmatrix} a & b & c \\ d & 0 & 0 \\ e & 0 & 0 \end{pmatrix}$ eksiktir. Bu tipte $\adj(B)=(0,-c,b)^T(0,e,-d)$ olduğundan $\perm_4 = -(0,e,-d)UV(0,-c,b)^T$ en fazla $2$ terimli bir $c(\cdot) - b(\cdot)$ ayrışımı vererek $\str(\perm_4) \le 2 < 4$ çelişkisiyle elenir.
- **$\mathrm{GL}_8(\mathbb{C})$ eşlenikliği ve $d_v$ uç durumları [İSPAT]:** Adım 2'de $\mathrm{diag}(1,P) M \mathrm{diag}(1,P^{-1})$ eşlenikliği $A_0$, $\det$ ve `(5)–(7)`'yi korur; kontragredient $(v,u) \mapsto ((P^{-1})^T v, Pu)$ etkisi $\Omega$ formunu korur. Ayrıca $d_v=0$ doğrudan `(7)`'den $\perm_4 \equiv 0$ vererek elenir; $d_v=8$ ($d_z=0$) iken $z, A_{13}$ boştur ve Adım 3–4 geçerliliğini korur.

### A-kuantum-bilgi
- **$\Omega$ izotropi adımı (Adım 1):** $\Omega((v,u)^T,(v',u')^T)=v^T u'+(v')^T u$ formunun Gram matrisi $\begin{pmatrix}0&I_8\\I_8&0\end{pmatrix}$ tersinirdir ($\det=1$). $v(X)^T u(X)\equiv 0$ kutuplanınca $S\subseteq S^\perp$ ve $\dim S+\dim S^\perp=16$ üzerinden $\dim W=\dim S\le 8$ bağımsızca türetildi **[İSPAT]**.
- **Normal form ve Skew-Square (Adım 2–4):** $v^T P^{-1}=(y^T,0)$ seçimi $u_1=Ky$ ($K^T=-K$) ve $\dim W=8$ verir; $(A_{11}^{(\xi)}K)^T=-A_{11}^{(\xi)}K$ ile $K^T=-K$'dan $(A_{11}^{(\xi)2}K)^T=-A_{11}^{(\xi)2}K$ ve $\perm_4\in I_W^3$ çıkarımı sağlamdır **[İSPAT]**.
- **$r=3$ boşluğu ($2\times 2$ sıfır blok):** Sadece sıfır satır ve $\mathfrak{so}_3$ sayılması eksiktir; $B(X)=\begin{pmatrix}\ell_{11}&\ell_{12}&\ell_{13}\\\ell_{21}&0&0\\\ell_{31}&0&0\end{pmatrix}$ tipi sıfır satır/sütun (devrikle eş) ve $\mathfrak{so}_3$'e $\mathrm{GL}_3\times\mathrm{GL}_3$ + devrikle eşlenmez **[İSPAT]**. Ancak bu tipte $\adj(B)=-(0,\ell_{13},-\ell_{12})^T(0,\ell_{31},-\ell_{21})$ rank-1 olduğundan $\str(\perm_4)\le 2<4$ ile yine elenir; 3. alt-vaka eklenmelidir **[KESİN HESAP]**.
- **$r=4$, $r=2$ ve kaynak kontrolü:** $r=4$'te $\codim(\Sigma_2)=4$ ve $r=2$'de UFD indirgemesi ($\str\le 2$) tutarlıdır **[İSPAT]**. Atkinson (1983) ve Eisenbud–Harris (1988) tam ifadesi birincil kaynaktan doğrulanmalıdır **[LİTERATÜR-DOĞRULANMADI]**.
- **SAT aktarım notu (H1/H4):** Özet metinde H1 küp ideali $I_B$ modülo üstel alt sınır gerektirir; H4 metni kesildiği için içeriği doğrulanamadı **[LİTERATÜR-DOĞRULANMADI]**. Sabit $n=4$ ve $O(n^2)$ bariyeri nedeniyle bu not teorem olarak değil, H1/H4'ün açık kaldığını belirten kısa bir Motivasyon/Tartışma paragrafı olarak yer almalıdır **[SANI]**.

### A-hesaplamalı-fizikçi
- **BLAS `float64` taşma denetimi:** `rref_mod_p_exact` içinde `block_size * (p - 1)^2 = 96 * 65520^2 ≈ 4.12×10^11 < 2^53` taşma sınırı sağlanır [KESİN HESAP]. Ancak `step_imsc` fonksiyonundaki `R_canon @ C_s` çarpımında iç çarpım boyutu `96` değil `n_S` (`L_9` için `D=6->7` adımında `n_S ≤ 6777`) olup `assert n_S * (p - 1)^2 < (1 << 53)` kontrolü eksiktir [KESİN HESAP].
- **Modüler rank -> $\mathbb{Q}$ aktarımı:** `M_{L_8}` tamsayı matris olduğundan `D=9`'da tek bir asal modülo `corank = 0` elde edilmesi $\mathbb{Q}$ ve $\mathbb{C}$ üzerinde tam sütun rankını garantiler [İSPAT]. İki asal (`32749, 65521`) ara derecelerdeki mod-`p` rank düşüşlerini elemek için yeterlidir; fakat `M_{L_8}`'in rankının tam `8` olduğu betikte açıkça doğrulanmamıştır [İSPAT].
- **Kontrol seti boşluğu (`L_9` vs `perm_3`):** `L_9` üzerinde `D=6, 7` için sırasıyla `753` ve `580` pozitif corank çıkması algoritmanın her girişi sıfırlamadığını gösterir [SAYISAL], ancak `build_subperm3_on_L` fonksiyonunun doğru `3×3` alt-permanentleri kurduğunu kanıtlamaz [İSPAT]. Bilinen `perm_3` (`codim Sing = 6`: `L_6`'da `corank = 0`, `L_7`'de `corank > 0`) pozitif kontrolü betiğe eklenmelidir [İSPAT].
- **Bağımsız doğrulama ve `README.md`:** Yerel makinede M2, Singular, Sage ve SymPy bulunmadığından, `float64` BLAS kullanmayan saf tamsayı (`int64`) tabanlı bağımsız bir doğrudan `M_9` rank/IMSC betiği yazılmalıdır [SANI]. Ayrıca `README.md` içindeki Macaulay2 `permanent X` komutunun varlığı ve sözdizimi birincil kaynaktan doğrulanmamıştır [LİTERATÜR-DOĞRULANMADI].

---

## Tur 2 — crit-A Saldırıları ve Yanıtlar

### crit-A Soruları
### A-cebirsel-geometri
- $2\times 2$ sıfır bloklu $B=\left(\begin{smallmatrix}a&b&c\\d&0&0\\e&0&0\end{smallmatrix}\right)$ için yazdığınız $\adj(B)=(0,-e,d)^T(0,c,-b)$ ifadesi gerçek ek matrisin devriğidir; $(2,3)$ bileşeni $cd$ olmalıdır `[KESİN HESAP]`.
- Vaka listesi gerçekten tam mı: Atkinson (1983) ve Eisenbud–Harris (1988) doğrulanmamışken 4. bir tip olmadığını savunup bunu `[İSPAT]` diye etiketlemeniz doğru mudur `[SANI]`?
- M2 `permanent` fonksiyonu belirsizken, önerdiğiniz $\perm_3$ pozitif kontrolünün hangi indeksleme hatalarını eleyeceğini belirtmediniz `[LİTERATÜR-DOĞRULANMADI]`.

### A-sınırlı-rank-uzayları
- Vaka listesi tam mı: Atkinson/EH sınıflandırmasını dış kaynak olarak doğrulamadan `r=3` kapanışına `[İSPAT]` etiketi vermeniz etiket tutarsızlığıdır `[SANI]`.
- $\adj(B)=pq^T$ hesabınız doğru olsa da, betikteki $\perm_3$ pozitif kontrolü eksikliği ve M2 `permanent` fonksiyonu belirsizliği tamamen denetimsiz bırakılmıştır `[LİTERATÜR-DOĞRULANMADI]`.

### A-determinantal-karmaşıklık
- $p=(0,b_{13},-b_{12})^T$, $q=(0,-b_{31},b_{21})^T$ için $pq^T=-\adj(B)$ çıkar; bu işaret hatası $\perm_4$ eşitliğinizde karşı-örnek üretir `[KESİN HESAP]`.
- Atkinson/EH doğrulanmamışken vaka listesinin tamlığını `[İSPAT]` saydınız; ayrıca $\perm_3$ pozitif kontrolü ile M2 `permanent` sözdizimi eksikliğine hiç değinmediniz `[LİTERATÜR-DOĞRULANMADI]`.

### A-lineer-cebir
- Alt-sol $2\times 2$ sıfır blok seçiminizde $\adj(B)$ doğru, ancak tüm $2\times 2$ sıfır blok yerleşimlerinin $\mathrm{GL}_3\times\mathrm{GL}_3$ ile eşlendiğini göstermediniz `[İSPAT]`.
- Vaka listesi tam mı: Atkinson/EH doğrulanmamışken `Prop 4.1` kapanışını `[İSPAT]` etiketlemek doğru mu; ayrıca $\perm_3$ kontrolü ve M2 `permanent` doğrulaması tamamen eksiktir `[LİTERATÜR-DOĞRULANMADI]`.

### A-değişmeli-cebir
- `n_S - rank(M_syz)` denkliğinde $M_{L_8}$ matrisinin mod-$p$ tam rank $8$ olduğu betikte denetlenmemiştir; rank $<8$ olan bir $M_{L_8}$ karşı-örneğinde `corank=0` çıktısı $\codim\Sing\ge 8$ vermez `[İSPAT]`.
- Hipotez nerede kullanıldı: $L_9$ yerine $\perm_3$ pozitif kontrolünün neden zorunlu olduğunu ve M2 `permanent` fonksiyonunun varlığını incelemediniz `[LİTERATÜR-DOĞRULANMADI]`.

### A-kombinatorik
- `build_subperm3_on_L` için `[KESİN HESAP]` etiketi kullandınız, ancak $\perm_3$ pozitif kontrolü olmadan doğru ideali kurduğunu ve `R_canon @ C_s` çarpımında taşma olmadığını nereden doğruluyorsunuz `[SANI]`?
- Prop 2.3'te `36` kuadriğin `4+4` düzlem içinde erimediği gösterilmeli; ayrıca `r=3` vaka listesinin tam olmadığı ($2\times 2$ sıfır blok eksikliği) tamamen gözden kaçırılmıştır `[İSPAT]`.

### A-hakem
- `2x2` sıfır blokta $a_1,a_2,b_2,b_3$ sembollerini $B$ matrisinde tanımlamadan $\adj(B)$ yazmanız tanımsızdır; $\perm_3$ kontrolü için de $\det_3$ ($\codim\Sing=4$) gibi hatalı kübiklerden ayrım kriteri vermediniz `[SANI]`.
- Atkinson/EH vaka listesinin tamlığı ve `README.md` içindeki M2 `permanent` sözdizimi hâlâ birincil kaynakta doğrulanmamıştır `[LİTERATÜR-DOĞRULANMADI]`.

### A-mat-fizikçi-simetri
- $\det(PQ)=1$ düzeltmesi sağlamdır, ancak `r=3` sınıflandırmasında vaka listesinin gerçekten tam olduğu Atkinson/EH doğrulanmadan savunulamaz `[İSPAT]`.
- $\perm_3$ pozitif kontrolünü, `M_{L_8}` rank denetimini ve M2 `permanent` fonksiyonunun geçerliliğini tamamen atladınız `[LİTERATÜR-DOĞRULANMADI]`.

### A-kuantum-bilgi
- Verdiğiniz $\adj(B)=-(0,\ell_{13},-\ell_{12})^T(0,\ell_{31},-\ell_{21})$ formülü fazladan eksi işareti taşır ve $-\adj(B)$ verir `[KESİN HESAP]`.
- H1–H4 aktarım notunda $n=4$ için hipotezin nerede kullanıldığı açık değil; ayrıca `2x2` blok dışındaki vaka listesi tamlığı, $\perm_3$ kontrolü ve M2 `permanent` denetimi eksiktir `[LİTERATÜR-DOĞRULANMADI]`.

### A-hesaplamalı-fizikçi
- `L_9` için `n_S <= 6777` sınırı `753*9` ile doğru olsa da `M_{L_8}` matrisinin mod-$p$ rankının $8$ olduğu betikte doğrulanmamıştır `[KESİN HESAP]`.
- Saf `int64` ile doğrudan $M_9$ ($27{,}456\times 11{,}440$) rankı için süre/bellek analizi vermediniz; ayrıca $\perm_3$ pozitif kontrolünün $4\times 4$ döngü hatalarını yakalayıp yakalamadığı ve M2 `permanent` varlığı belirsizdir `[LİTERATÜR-DOĞRULANMADI]`.

### A-cebirsel-geometri (Tur 2 Yanıtı)
- **$\adj(B)$ düzeltmesi (haklısınız):** Tur 1'deki ifadem gerçek ek matrisin devriğiydi; doğru hesap $\adj(B)=(0,c,-b)^T(0,-e,d)=\left(\begin{smallmatrix}0&0&0\\0&-ce&cd\\0&be&-bd\end{smallmatrix}\right)$ olup $(2,3)$ bileşeni $cd$'dir `[KESİN HESAP]`. Bu düzeltmeyle $-\tr(\adj(B)UV)=e(UVp)_2-d(UVp)_3$ ($p=(0,c,-b)^T$) elde edilir ve $\str(\perm_4)\le 2<4$ çelişkisi korunur `[İSPAT]`.
- **Vaka listesi tamlığı:** Tur 1'deki `[İSPAT]` etiketim "4. tip yoktur" iddiasına değil, makaledeki 2 tipli listenin $2\times 2$ sıfır bloklu karşı-örnekle *eksik* olduğuna ilişkindi `[İSPAT]`. Üç tipli listenin tamlığı ise Atkinson (1983) ve Eisenbud–Harris (1988) birincil kaynaklardan doğrulanana veya makaleye öz-yeterli bir ispat eklenene kadar belirsizdir `[LİTERATÜR-DOĞRULANMADI]`.
- **$\perm_3$ pozitif kontrolü ve M2:** Prop 2.3 yöntemiyle $\codim_{\mathbb{C}^9}(\Sing(V(\perm_3)))=6$ iken $\codim_{\mathbb{C}^9}(\Sing(V(\det_3)))=4$'tür `[İSPAT]`. $L_6\subset\mathbb{C}^9$ kontrolü IMSC indirgemesi ile permanent–determinant ayrımını sınar, ancak `3x3` alt-permanent döngüsünü doğrudan test etmez; $3\times 3$ indeksleme hatalarını elemek için ek olarak $\det_4$ ($\codim\Sing=4$, $L_4$) kontrolü gerekir `[İSPAT]`. M2 `permanent` fonksiyonunun varlığı hâlâ doğrulanmamıştır `[LİTERATÜR-DOĞRULANMADI]`.

### A-sınırlı-rank-uzayları (Tur 2 Yanıtı)
- **Etiket düzeltmesi ve öz-yeterli tamlık kanıtı:** Crit-A haklıdır; Tur 1'de Atkinson/EH listesini dış kaynaktan doğrulamadan `[İSPAT]` etiketi kullanmak tutarsızdı ve bu literatür atfı hâlâ doğrulanmamıştır `[LİTERATÜR-DOĞRULANMADI]`. Ancak $3\times 3$ $\rank\le 2$ tiplerinin tamlığı dış kaynak olmadan türetilir: $\max\rank\le 1$ ortak satır/sütun ($1\times 3$ veya $3\times 1$ sıfır blok) verir; $\max\rank=2$ ise $\mathrm{GL}_3\times\mathrm{GL}_3$ ile $A_0=\mathrm{diag}(1,1,0)$ alınıp $\det(tA_0+M)\equiv 0$'dan $M_{33}=0$ ve $r^Tq=0$ çıkar: (i) $q\equiv 0$ veya $r\equiv 0$ sıfır sütun/satır, (ii) $\dim Q=\dim R=1$ ise $q_2\equiv r_1\equiv 0$ ve $[t^0]=q_1 r_2 p_{21}\equiv 0$ ile $2\times 2$ sıfır blok, (iii) $\dim Q=2$ (veya $\dim R=2$) ise $r=Kq$ ($K^T=-K\neq 0$), $\ker(q)$ üzerinde $P=\lambda I_2$ ve $[t^0]=p_{21}q_1^2+(p_{22}-p_{11})q_1 q_2-p_{12}q_2^2\equiv 0$ ile $\mathfrak{so}_3$ elde edilir; başka tip yoktur ve `r=3` kapanışı öz-yeterlidir `[İSPAT]`.
- **$\perm_3$ kontrolü ve M2 belirsizliği:** Crit-A haklıdır; `build_subperm3_on_L`'deki olası işaret/indeksleme hatalarını (örn. $\det_3$'e kayıp $\codim\Sing=4$ vermesini) elemek için $\perm_3$'te $\codim\Sing(V(\perm_3))=6$ pozitif kontrolü eklenmelidir `[İSPAT]`. Ayrıca README'deki Macaulay2 `permanent` fonksiyonunun varlığı birincil M2 belgelerinden doğrulanmamıştır `[LİTERATÜR-DOĞRULANMADI]`.

### A-determinantal-karmaşıklık (Tur 2 Yanıtı)
- **$\adj(B)=pq^T$ savunması:** `crit-A`'nın $pq^T=-\adj(B)$ eleştirisi hatalıdır. $B=\begin{pmatrix}b_{11}&b_{12}&b_{13}\\ b_{21}&0&0\\ b_{31}&0&0\end{pmatrix}$ için $\adj(B)_{i,j}=(-1)^{i+j}\det(B_{\hat{j},\hat{i}})$ formülü $\adj(B)_{2,2}=-b_{13}b_{31}$, $\adj(B)_{2,3}=+b_{13}b_{21}$, $\adj(B)_{3,2}=+b_{12}b_{31}$ ve $\adj(B)_{3,3}=-b_{12}b_{21}$ verir; bu da $p=(0,b_{13},-b_{12})^T$, $q=(0,-b_{31},b_{21})^T$ ile tam olarak $+pq^T$ olur ve $\perm_4=-\tr(\adj(B)UV)=b_{31}(UVp)_2-b_{21}(UVp)_3$ özdeşliği geçerlidir [KESİN HESAP].
- **Atkinson/EH tamlığı ve etiket ayrımı:** Tur 1'de vaka listesi tamlığını `[İSPAT]` saymadım, Atkinson 1983 ve Eisenbud–Harris 1988 sınıflandırmasını `[LİTERATÜR-DOĞRULANMADI]` etiketledim; `[İSPAT]` yalnızca $2\times 2$ sıfır blok ve sıfır sütun tiplerinin elenmesine aittir [İSPAT]. Dördüncü tip bulunmadığı birincil kaynaklardan teyit edilmeden $r=3$ kapanışı bu referanslara koşulludur [LİTERATÜR-DOĞRULANMADI].
- **Atlanan kontrollerin kabulü:** Tur 1'de $\perm_3$ pozitif kontrolü eksikliğini ve `README.md`'deki Macaulay2 `permanent` sözdizimini atladım. $L_9$ negatif kontrolü `build_subperm3_on_L` ideal kuruluşunu doğrulamadığından betiğe $\perm_3$ ($\codim\Sing=6$) pozitif kontrolü eklenmelidir [İSPAT]. Ayrıca M2 `permanent` fonksiyonunun varlığı doğrulanmalıdır [LİTERATÜR-DOĞRULANMADI].

### A-lineer-cebir (Tur 2 Yanıtı)
- **2×2 sıfır blok yerleşimlerinin eşliği [İSPAT]:** Eleştiri haklıdır; Tur 1'de eksik kalan adım şudur: Herhangi bir $I=\{i_1,i_2\}$ satır ve $J=\{j_1,j_2\}$ sütun kesişimindeki $2\times 2$ sıfır blok, $I\to\{2,3\}$ ve $J\to\{1,2\}$ gönderen permütasyon matrisleri $P_\sigma, Q_\tau\in\mathrm{GL}_3(\mathbb{C})$ ile alt-sol $\{2,3\}\times\{1,2\}$ konumuna taşınır ($\det(P_\sigma Q_\tau)=-1$ ise bir satır $-1$ ile ölçeklenerek $\det(PQ)=1$ sağlanır). Blok dönüşümü $(B,U,V)\mapsto(PBQ,PU,VQ)$ olup $\tr(\adj(PBQ)PUVQ)=\det(PQ)\tr(Q^{-1}\adj(B)UVQ)=\tr(\adj(B)UV)$ eşitliğini korur.

- **Atkinson/EH sınıflandırmasının tamlığı [LİTERATÜR-DOĞRULANMADI]:** Eleştiri haklıdır; Atkinson (1983) ve Eisenbud–Harris (1988) birincil kaynaklardan doğrulanmadan `Prop 4.1` ($r=3$) kapanışının tamlığını `[İSPAT]` etiketlemem hatalıydı, bu etiketi geri çekiyorum.

- **Üç tipin elenmesi (sınıflandırma veriliyken) [İSPAT]:** Rank $\le 2$ olan $3\times 3$ uzayların sıfır satır (devrikle eşlenen sıfır sütun), $2\times 2$ sıfır blok ve $\mathfrak{so}_3$ tiplerinden ibaret olduğu kabulü altında her üç tipin $\str(\perm_4)\le 3 < 4$ çelişkisiyle elenmesi geçerlidir.

- **$\perm_3$ kontrolü ve M2 `permanent` [LİTERATÜR-DOĞRULANMADI]:** Betikte $\perm_3$ ($\codim\Sing=6$) pozitif kontrolü eksiktir ve `README.md` içindeki Macaulay2 `permanent X` sözdiziminin geçerliliği doğrulanmamıştır.

### A-değişmeli-cebir (Tur 2 Yanıtı)
- **$M_{L_8}$ rank denetimi ve `n_S - rank(M_syz)`:** Betikte $\rank_{\mathbb{F}_p}(M_{L_8})=8$ açıkça kontrol edilmemiştir; savunma amaçlı `assert` eklenmelidir [KESİN HESAP]. Ancak `crit-A`'nın öne sürdüğü rank $<8$ karşı-örneği mümkün değildir: eğer $\rank_{\mathbb{F}_p}(M_{L_8})<8$ olsaydı $M_{L_8} t_0 = 0$ sağlayan bir $t_0 \in \mathbb{F}_p^8 \setminus \{0\}$ bulunurdu; $I = J|_{L_8}$ üreteçleri $M_{L_8} t$'nin homojen kübikleri olduğundan tüm $I_9$ elemanları $t_0$'da sıfırlanır, oysa bir $t_i^9(t_0) \neq 0$ olduğundan $I_9 \subsetneq R_9$ ve $\mathrm{corank} \ge 1$ zorlanırdı [İSPAT]. Dolayısıyla `corank = 0` çıktısı $\rank_{\mathbb{F}_p}(M_{L_8}) = 8$'i ve Hilbert denkliğini zorunlu kılar [İSPAT].
- **$\perm_3$ pozitif kontrolü ve M2 `permanent`:** İlk turda atlanan $\perm_3$ kontrolü zorunludur; $L_9$ yalnızca `corank > 0` gösterir, `build_subperm3_on_L` içindeki işaret/permütasyon hatalarını eleyemez [İSPAT]. Prop 2.3 argümanıyla $2\times 2$ alt-permanentlerden oluşan $\Sing(V(\perm_3))\subset\mathbb{C}^9$ eş-boyutu $6$, oysa $\det_3$ için eş-boyut $(3-1)^2=4$'tür; bu nedenle $L_6 \subset \mathbb{C}^9$ üzerinde `corank = 0` pozitif testi işaret hatalarını yakalar [İSPAT]. `README.md`'deki M2 `permanent` fonksiyonunun varlığı doğrulanmamıştır; M2 betiği birincil kaynaktan denetlenmeli veya açık toplamla yazılmalıdır [LİTERATÜR-DOĞRULANMADI].

### A-kombinatorik (Tur 2 Yanıtı)
- **`build_subperm3_on_L` ve $\perm_3$ kontrolü:** İndeksleme kodu statik olarak tutarlı olsa da betik çalıştırılmadığından ve $\perm_3$ ($\codim=6$, örn. $\det_3$'ün $\codim=4$'ünden ayırır) pozitif kontrolü bulunmadığından ideal doğruluğu iddiasını geri çekiyorum; $\perm_3$ pozitif kontrolü eklenmelidir `[SANI]`.
- **`R_canon @ C_s` taşma denetimi:** `R_canon` satırında en fazla $\mathrm{corank}_D$ sıfır-dışı girdi vardır. $L_8$'de ($p\le 65521$, $\mathrm{corank}_6=132$) iç çarpım $\le 132\cdot 65520^2 \approx 5{,}67\times 10^{11} \ll 2^{53}$; $L_9$'da ($p=32749$, $\mathrm{corank}_6=753$) $\le 753\cdot 32748^2 \approx 8{,}08\times 10^{11} \ll 2^{53}$ olup taşma oluşmaz. Yine de `step_imsc` içine `assert` eklenmelidir `[KESİN HESAP]`.
- **Prop 2.3 kuadriklerinin $4+4$ içinde erimemesi:** Her $2\times 2$ blok $I\times J=\{i_1,i_2\}\times\{j_1,j_2\}$ için $x_{i_1,j_1}=x_{i_1,j_2}=x_{i_2,j_1}=1$, $x_{i_2,j_2}=-1$ (diğerleri $0$) noktası $\perm_2(X_{I,J})=0$ sağlar; iki satır ve iki sütunu sıfır-dışı olduğundan hiçbir $K_{1,4}$ veya $K_{4,1}$ düzlemine düşmez (`4+4+36` bileşen ayrıktır) `[İSPAT]`.
- **`r=3` vaka listesi:** İlk turda $2\times 2$ sıfır blok eksikliğini incelemedim; eleştiri haklıdır, eksik vaka eklenmeli ve Atkinson (1983)/EH (1988) sınıflandırmasının tamlığı birincil kaynaktan doğrulanmalıdır `[LİTERATÜR-DOĞRULANMADI]`.

### A-hakem (Tur 2 Yanıtı)
- **Tanımsız sembol düzeltmesi:** Eleştiri haklıdır; $2\times 2$ sıfır bloklu tip için matrisi açıkça $B=\begin{pmatrix}a_1&a_2&a_3\\0&0&b_2\\0&0&b_3\end{pmatrix}$ olarak tanımlıyorum [İSPAT]. Bu matrisin $2\times 2$ kofaktörleri $\adj(B)_{j,i}=(-1)^{i+j}\det B_{\hat{i},\hat{j}}$ formülünden yalnızca $(1,2)\mapsto -a_2 b_3$, $(1,3)\mapsto a_2 b_2$, $(2,2)\mapsto a_1 b_3$, $(2,3)\mapsto -a_1 b_2$ bileşenlerinde sıfırdan farklıdır; dolayısıyla $\adj(B)=(-a_2,a_1,0)^T(0,b_3,-b_2)$ olup $\str(\perm_4)\le 2<4$ verir [KESİN HESAP].
- **$\perm_3$ ve $\det_3$ ayrım kriteri:** Eleştiri yerindedir; $\Sing(V(\det_3))$, $\rank\le 1$ matrislerden oluştuğundan boyutu $3+3-1=5$ ve $\codim_{\mathbb{C}^9}(\Sing(V(\det_3)))=4$'tür [KESİN HESAP]. Buna karşılık $\perm_3$'ün tüm $2\times 2$ alt-permanentleri sıfırlandığında $\dim\Sing(V(\perm_3))=3$ ve $\codim_{\mathbb{C}^9}(\Sing(V(\perm_3)))=6$ çıkar [İSPAT]. Dolayısıyla $\codim\Sing=6$ testi işaret hatası kaynaklı $\det_3$'e kaymayı yakalar, ancak $4\times 4$ döngü/indeks hatalarını garanti etmez [SANI].
- **Vaka listesi tamlığı ve M2 sözdizimi:** $2\times 2$ sıfır bloklu uzayın sıfır satır/sütuna ve $\mathfrak{so}_3$'e denk olmadığı gösterilse de, dördüncü bir tipin bulunmadığı iddiası Atkinson (1983) ve Eisenbud–Harris (1988) birincil kaynaklarında henüz doğrulanmamıştır [LİTERATÜR-DOĞRULANMADI]. Aynı şekilde `README.md` içindeki `permanent` komutu da Macaulay2 belgelerinden doğrulanmamıştır [LİTERATÜR-DOĞRULANMADI].

### A-mat-fizikçi-simetri (Tur 2 Yanıtı)
- **`r=3` vaka listesinin tamlığı [LİTERATÜR-DOĞRULANMADI]:** Eleştiri haklıdır. $2\times 2$ sıfır bloklu tipin $\adj(B)=(0,-c,b)^T(0,e,-d)$ ile $\str(\perm_4)\le 2$ verip elendiği ve sıfır satır/sütunun devrikle eşlendiği kesin ispatımızdır; ancak dördüncü bir tip olmadığı iddiası Atkinson (1983) ve Eisenbud–Harris (1988) birincil kaynaklarından doğrulanmadığı için bu kapsayıcılık üzerindeki önceki ispat etiketini geri çekiyorum (kaynak doğrulanmalı veya makaleye öz-yeterli bir kanıt eklenmelidir).
- **`M_{L_8}` mod-$p$ rank denetimi [İSPAT]:** Eleştiri haklıdır. Betikte `M_L8` matrisinin $\mathbb{F}_p$ üzerinde rank $8$ olduğu denetlenmemiştir; $\rank_{\mathbb{F}_p}(M_{L_8})<8$ ise `corank=0` çıktısı $\codim \ge 8$ vermez. Her iki asal ($p_1, p_2$) için $\rank_{\mathbb{F}_p}(M_{L_8})=8$ doğrulaması eklenmelidir.
- **$\perm_3$ pozitif kontrolü [İSPAT]:** Betikte eksiktir. Prop 2.3 argümanıyla $3\times 3$ matrislerde tüm $2\times 2$ alt-permanentlerin sıfırlanması yalnızca tek satır/sütun ($3$B) veya $\perm_2=0$ olan $2\times 2$ bloklar ($3$B) verdiğinden $\codim_{\mathbb{C}^9}(\Sing(V(\perm_3)))=6$ iken, $\det_3$ için rank-$\le 1$ yerinin kodboyutu $4$'tür; bu kontrol kübik kurulumdaki işaret/indeksleme hatalarını ayırır.
- **M2 `permanent` sözdizimi [LİTERATÜR-DOĞRULANMADI]:** `README.md`'deki `permanent X` komutunun Macaulay2'de yerleşik varlığını bilmiyorum, birincil kaynaktan kontrol edilmeli.

### A-kuantum-bilgi (Tur 2 Yanıtı)
- **$\adj(B)$ işareti korunuyor:** $B=\begin{pmatrix}\ell_{11}&\ell_{12}&\ell_{13}\\\ell_{21}&0&0\\\ell_{31}&0&0\end{pmatrix}$ için $\det(B+\varepsilon E_{ij})=\varepsilon\,(\adj B)_{ji}$ üzerinden $(\adj B)_{22}=-\ell_{13}\ell_{31}$, $(\adj B)_{23}=+\ell_{13}\ell_{21}$, $(\adj B)_{32}=+\ell_{12}\ell_{31}$, $(\adj B)_{33}=-\ell_{12}\ell_{21}$ elde edilir. Önerdiğimiz $-(0,\ell_{13},-\ell_{12})^T(0,\ell_{31},-\ell_{21})$ formülü birebir doğrudur (`+` işareti $-\adj B$ verir) **[KESİN HESAP]**.
- **H1–H4 ve $n=4$ ilişkisi:** `dc_perm4_ge_10.tex` ispatında H1–H4 kullanılmaz; $\dc_{\mathbb{C}}(\perm_4)\ge 10$ sabit $n=4$ sınırıdır, H1 ise asimptotik $2^{n^\varepsilon}$ ($I_B$-modülo) sınır gerektirir. Aktarım notu yalnızca Motivasyon/Tartışma bölümünde, H1/H4'ün açık kaldığını belirterek yer almalıdır **[SANI]**. (H4 tam metni özet dışında kaldığından doğrulanamadı **[LİTERATÜR-DOĞRULANMADI]**.)
- **$r=3$ tamlığı ve konum:** Her $2\times 2$ sıfır blok permütasyonlarla ($\mathrm{GL}_3\times\mathrm{GL}_3$) sağ-alta taşınır **[İSPAT]**; ancak bu 3 tipin tüm rank $\le 2$ uzaylarını tükettiği Atkinson (1983)/EH (1988) birincil kaynağından doğrulanmamıştır **[LİTERATÜR-DOĞRULANMADI]**.
- **$\perm_3$ ve M2 eksiği:** `L_9` yalnızca idealin tam çökmediğini gösterir, kübiklerin işaret/indeks doğruluğunu kanıtlamaz; betikte $\perm_3$ pozitif kontrolü eksiktir **[İSPAT]** ve `README.md`'deki M2 `permanent X` sözdizimi doğrulanmamıştır **[LİTERATÜR-DOĞRULANMADI]**.

### A-hesaplamalı-fizikçi (Tur 2 Yanıtı)
- **`M_{L_8}` rank-8 denetimi:** Eleştiriyi kısmen düzeltiyorum: $\rank_{\mathbb{F}_p}(M_{L_8}) < 8$ olsaydı, sıfır olmayan bir $v \in \ker_{\mathbb{F}_p}(M_{L_8})$ için $g(v) = \perm_3^{\mathrm{sub}}(M_{L_8}v) \equiv 0 \pmod p$ olacağından $I_D \otimes \mathbb{F}_p$ tüm $D$'lerde $v$'de sıfırlanır ve `corank = 0` çıkamazdı; dolayısıyla `D = 9`'da `corank = 0` çıktısı $\rank_{\mathbb{F}_p}(M_{L_8}) = \rank_{\mathbb{Q}}(M_{L_8}) = 8$'i zaten zorlar [İSPAT]. Yine de açık bir rank kontrolü betiğe eklenmelidir [SANI].
- **`M_9` `int64` maliyet analizi:** Eleştiri haklıdır; yoğun `int64` $M_9$ ($27{,}456 \times 11{,}440$) $2.51\text{ GB}$ bellek ve tam elemede $\approx 1.55 \times 10^{12}$ çarpma-toplama işlemi gerektirir [KESİN HESAP]. Bunun yerine satır başına en fazla $\binom{10}{3} = 120$ sıfır-olmayan terim içeren seyrek mod-`p` RREF veya `float64`'sız küçük bloklu `int64` doğrulama kullanılmalıdır [SANI].
- **`perm_3` kapsamı ve M2:** `build_subperm3_on_L` kodu $n=4$'e sabitlendiğinden ayrı bir `perm_3` fonksiyonu $4\times 4$ döngü hatasını yakalayamaz; işlev `n` parametreli yazılıp `perm_3` ($\codim=6$), `det_3` ($\codim=4$) ve noktasal $\nabla\perm_4$ çapraz kontrolüyle sınanmalıdır [İSPAT]. `README.md`'deki M2 `permanent` varlığı doğrulanamamıştır [LİTERATÜR-DOĞRULANMADI].

---

## Tur 3 — Üretilen Düzeltme ve Doğrulama Çıktıları

### (a) Düzeltilmiş r = 3 LaTeX Paragrafı (A-sınırlı-rank-uzayları)
```latex
\emph{Case $r = 3$.} Comparing $[t^3]$ and $[t^4]$ in~\eqref{eq:schur} gives $\det_3(B(X)) \equiv 0$ and
\[
  \perm_4(X) = \tr(A)\underbrace{\det_3(B)}_{=\,0} - \tr\!\big(\adj(B(X))\, U(X) V(X)\big)
  = -\tr\!\big(\adj(B(X))\, U(X) V(X)\big).
\]
Thus $B(X)$ spans a linear subspace of $\mathbb{C}^{3\times 3}$ consisting of matrices of rank $\le 2$. Left and right multiplication of $M(tX)$ in~\eqref{eq:blockM} by $\mathrm{diag}(P_1, I_w)$ and $\mathrm{diag}(Q_1, I_w)$ ($P_1, Q_1 \in \mathrm{GL}_3(\mathbb{C})$) replaces $(B, U, V)$ by $(P_1 B Q_1, P_1 U, V Q_1)$ while scaling $\det M(tX)$ by $c := \det(P_1 Q_1) \in \mathbb{C}^\times$; transposition $M(tX) \mapsto M(tX)^T$ preserves $\det M(tX)$ and replaces $(B, U, V, A)$ by $(B^T, V^T, U^T, A^T)$. Denoting the resulting blocks again by $(B, U, V, A)$, we still have $c\,\perm_4(X) = -\tr(\adj(B(X)) U(X) V(X))$. Up to these operations, every linear space of $3 \times 3$ matrices of rank $\le 2$ over $\mathbb{C}$ falls into one of three types (cf.\ Atkinson~\cite{Atkinson1983}, Eisenbud--Harris~\cite{EH1988}; a self-contained verification is given immediately below):
\begin{enumerate}
  \item \emph{Compression type I ($1\times 3$ zero row, or $3\times 1$ zero column via transpose):} $B(X)$ has a zero third row. Then $\adj(B(X)) = c(X) e_3^T$, where $c(X) = (c_1,c_2,c_3)^T \in \mathbb{C}[X]_2^3$ consists of the signed $2\times 2$ minors of the top $2\times 3$ block of $B(X)$. Hence
  \[
    c\,\perm_4(X) = -\big(e_3^T U(X) V(X)\big) c(X) = -\sum_{j=1}^3 \big(e_3^T U(X) V(X)\big)_j\, c_j(X),
  \]
  giving $\str(\perm_4) = \str(c\,\perm_4) \le 3 < 4$, a contradiction.
  \item \emph{Compression type II ($2\times 2$ zero block):} Permuting rows and columns puts the zero block in rows $\{2,3\}$ and columns $\{2,3\}$, so
  \[
    B(X) = \begin{pmatrix} b_{11}(X) & b_{12}(X) & b_{13}(X) \\ b_{21}(X) & 0 & 0 \\ b_{31}(X) & 0 & 0 \end{pmatrix}.
  \]
  All $2\times 2$ minors involving two rows from $\{2,3\}$ or two columns from $\{2,3\}$ vanish, so the first row and first column of $\adj(B(X))$ are zero, and computing the remaining four cofactors gives the rank-$\le 1$ outer product
  \[
    \adj(B(X)) = p(X)\, q(X)^T, \qquad
    p(X) := \begin{pmatrix} 0 \\ -b_{13}(X) \\ b_{12}(X) \end{pmatrix}, \quad
    q(X) := \begin{pmatrix} 0 \\ b_{31}(X) \\ -b_{21}(X) \end{pmatrix}.
  \]
  Consequently,
  \[
    c\,\perm_4(X) = -q(X)^T U(X) V(X) p(X)
    = -b_{31}(X)\big(U(X)V(X)p(X)\big)_2 + b_{21}(X)\big(U(X)V(X)p(X)\big)_3,
  \]
  which gives $\str(\perm_4) = \str(c\,\perm_4) \le 2 < 4$, a contradiction.
  \item \emph{Skew-symmetric primitive type:} $B(X) \in \mathfrak{so}_3(\mathbb{C})$, i.e.,
  \[
    B(X) = \begin{pmatrix} 0 & \ell_3 & -\ell_2 \\ -\ell_3 & 0 & \ell_1 \\ \ell_2 & -\ell_1 & 0 \end{pmatrix}
  \]
  for linear forms $\ell_1,\ell_2,\ell_3 \in \mathbb{C}[X]_1$. Then $\adj(B(X)) = \ell(X)\ell(X)^T$, so
  \[
    c\,\perm_4(X) = -\ell(X)^T U(X) V(X) \ell(X) = -\sum_{i=1}^3 \ell_i(X)\, \big(U(X) V(X) \ell(X)\big)_i,
  \]
  again giving $\str(\perm_4) = \str(c\,\perm_4) \le 3 < 4$, a contradiction.
\end{enumerate}

\emph{Self-contained verification of the $3\times 3$ classification:} Since $c\,\perm_4 \neq 0$, we have $B \not\equiv 0$. If $\max_{X \in \mathbb{C}^{16}} \rank B(X) = 1$, choose $X_0$ with $B(X_0) = E_{11}$ up to $\mathrm{GL}_3(\mathbb{C})\times\mathrm{GL}_3(\mathbb{C})$; vanishing of all $2\times 2$ minors of $t E_{11} + B(X)$ forces $b_{ij} \equiv 0$ ($i,j\in\{2,3\}$) and $b_{1j} b_{i1} \equiv 0$, so in the integral domain $\mathbb{C}[X]$ either rows $\{2,3\}$ or columns $\{2,3\}$ vanish (Type~I). Otherwise $\max_X \rank B(X) = 2$; choose $X_0$ with $B(X_0) = \mathrm{diag}(1,1,0)$ and write $B(X) = \left(\begin{smallmatrix} P(X) & q(X) \\ r(X)^T & s(X) \end{smallmatrix}\right)$ with $P \in \mathbb{C}[X]_1^{2\times 2}$ and $q,r \in \mathbb{C}[X]_1^2$. From $\det_3(t B(X_0) + B(X)) \equiv 0$, $[t^2] = 0$ gives $s \equiv 0$ and $[t^1] = 0$ gives $r^T q \equiv 0$, which polarizes to $r(X)^T q(Y) + r(Y)^T q(X) \equiv 0$. Let $Q := \Span_{\mathbb{C}}\{q(X)\} \subseteq \mathbb{C}^2$ and $R := \Span_{\mathbb{C}}\{r(X)\} \subseteq \mathbb{C}^2$. If $\dim R = 0$ or $\dim Q = 0$, $B$ is of Type~I. If $\dim Q = \dim R = 1$, conjugating by $\mathrm{diag}(g,1)$ and $\mathrm{diag}(g^{-1},1)$ ($g \in \mathrm{GL}_2(\mathbb{C})$) preserves $B(X_0)$ and sets $q_2 \equiv 0$ with $q_1 \not\equiv 0$; polarity forces $r_1 \equiv 0$ with $r_2 \not\equiv 0$, and then $0 \equiv \det_3(B(X)) = q_1 r_2 p_{21}$ forces $p_{21} \equiv 0$, placing $B$ in Type~II (rows $\{2,3\}$ and columns $\{1,3\}$ zero). Finally, if $\dim Q = 2$ (or $\dim R = 2$, reduced by transpose), polarity implies $q(X) = 0 \implies r(X) = 0$, so $r(X) = K_2 q(X)$ with $K_2^T = -K_2 \neq 0$; rescaling row and column~$3$ gives $r = (-q_2, q_1)^T$, and $0 \equiv \det_3(B(X)) = p_{21} q_1^2 + (p_{22} - p_{11}) q_1 q_2 - p_{12} q_2^2$. Decomposing $X = Y + Z$ with $Y \in \ker(q)$ and independent coordinates $(q_1, q_2)$ on a complement shows $p_{21} = \alpha q_2$, $p_{12} = \gamma q_1$, and $p_{22} - p_{11} = -\alpha q_1 + \gamma q_2$ for constants $\alpha,\gamma \in \mathbb{C}$. Left multiplication by $\left(\begin{smallmatrix} 1 & 0 & \alpha \\ 0 & 1 & \gamma \\ 0 & 0 & 1 \end{smallmatrix}\right)\left(\begin{smallmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & -1 \end{smallmatrix}\right) \in \mathrm{GL}_3(\mathbb{C})$ then maps $B(X)$ into $\mathfrak{so}_3(\mathbb{C})$ (Type~III).
```

**Kısa Gerekçe:**
- **Mevcut boşluğun kapatılması:** $\mathrm{GL}_3(\mathbb{C})\times\mathrm{GL}_3(\mathbb{C})$ ve devrik dönüşümlerinin $M(tX)$ üzerindeki etkisi açıkça yazılarak $3\times 1$ sıfır sütun tipinin $1\times 3$ sıfır satır tipine indirgenmesi meşrulaştırıldı ve eksik $2\times 2$ sıfır bloklu sıkıştırma tipi eklendi `[İSPAT]`.
- **$2\times 2$ sıfır blok hesabı:** Sağ-alt $2\times 2$ sıfır bloklu $B(X)$ için $\adj(B(X)) = p(X)q(X)^T$ (rank $\le 1$) doğrudan kofaktörlerle hesaplandı ve $c\,\perm_4(X) = -b_{31}(UVp)_2 + b_{21}(UVp)_3$ üzerinden $\str(\perm_4) \le 2 < 4$ çelişkisi elde edildi `[İSPAT]`.
- **Öz-yeterli tamlık ve literatür bağımsızlığı:** $\max\rank\in\{1,2\}$ ayrımıyla 4. bir tip bulunmadığı makale içinde sıfırdan kanıtlandığından `r = 3` kapanışı dış literatüre bağımlı değildir `[İSPAT]`; bununla birlikte Atkinson~\cite{Atkinson1983} ve Eisenbud--Harris~\cite{EH1988} makalelerindeki kesin teorem numaraları birincil kaynaklardan henüz teyit edilmemiştir `[LİTERATÜR-DOĞRULANMADI]`.

### (a-ek) Bağımsız Lineer Cebir Yeniden Türetimi (A-lineer-cebir)
`A-sınırlı-rank-uzayları`'nın önerdiği düzeltilmiş $r=3$ LaTeX paragrafı satır satır yeniden türetilerek denetlenmiştir; matematiksel bir boşluk kalmamıştır:

1. **$\mathrm{GL}_3(\mathbb{C})\times\mathrm{GL}_3(\mathbb{C})$ ve devrik dönüşümü [İSPAT]:** $\mathrm{diag}(P_1,I_w)M(tX)\mathrm{diag}(Q_1,I_w)$ işlemi $(B,U,V)\mapsto(P_1 B Q_1, P_1 U, V Q_1)$ dönüşümünü verir ve $\det M(tX)$'i $c=\det(P_1 Q_1)\in\mathbb{C}^\times$ ile ölçekler; devrik $M(tX)^T$ ise $(B,U,V,A)\mapsto(B^T,V^T,U^T,A^T)$ ile determinantı korur. Her iki halde $c\,\perm_4 = -\tr(\adj(B)UV)$ ve $\str(c\,\perm_4)=\str(\perm_4)$ geçerlidir.

2. **$2\times 2$ sıfır blokta $\adj(B)$ hesabı (Tip II) [İSPAT]:** Sağ-alt $\{2,3\}\times\{2,3\}$ sıfır bloğu için $\adj(B)_{j,i}=(-1)^{i+j}\det(B_{\hat{i},\hat{j}})$ kofaktörleri tek tek hesaplandığında: $i=1$ ve $j=1$ için tüm $2\times 2$ minörler sıfırdır; kalan dört giriş ise $\adj(B)_{2,2}=-b_{13}b_{31}$, $\adj(B)_{2,3}=b_{13}b_{21}$, $\adj(B)_{3,2}=b_{12}b_{31}$, $\adj(B)_{3,3}=-b_{12}b_{21}$ olur. Bu matris $p=(0,-b_{13},b_{12})^T$, $q=(0,b_{31},-b_{21})^T$ için $p q^T$ ile işaret ve bileşen olarak birebir örtüşür; dolayısıyla $c\,\perm_4 = -b_{31}(UVp)_2 + b_{21}(UVp)_3$ ayrışımı $(1,3)$ dereceli $2$ terimle $\str(\perm_4)\le 2 < 4$ çelişkisini verir.

3. **Tip I ve Tip III elemesi [İSPAT]:** Tip I'de $\deg((e_3^T UV)_j)=\deg(c_j)=2$ olduğundan $\str(\perm_4)\le 3 < 4$, Tip III'te $\adj(B)=\ell\ell^T$ ve $\deg(\ell_i)=1$, $\deg((UV\ell)_i)=3$ olduğundan $\str(\perm_4)\le 3 < 4$ elde edilir.

4. **Öz-yeterli $3\times 3$ sınıflandırma kanıtı [İSPAT]:**
   - $\max\rank(B)=1$ halinde $tE_{11}+B(X)$'in $2\times 2$ minörlerinden $b_{ij}\equiv 0$ ve $b_{1j}b_{i1}\equiv 0$ ($i,j\in\{2,3\}$) çıkar; $\mathbb{C}[X]$ tamlık bölgesinde $\{2,3\}$ satırları veya $\{2,3\}$ sütunları sıfırlanır (Tip I).
   - $\max\rank(B)=2$ halinde $B(X_0)=\mathrm{diag}(1,1,0)$ ile $[t^2]=0\implies s\equiv 0$ ve $[t^1]=0\implies r^T q\equiv 0$ polarize olur. $(\dim Q,\dim R)$ durumlarından $(0,*), (*,0)$ Tip I; $(1,1)$ durumda $q_2\equiv 0, r_1\equiv 0$ ve $\det_3(B)=q_1 r_2 p_{21}\equiv 0\implies p_{21}\equiv 0$ Tip II; $\dim Q=2$ (ve devrikle $(1,2)$ dahil $\dim R=2$) durumunda $K_2=0$ halinde $\dim R=0$ zaten elenmiş olduğundan $r=(-q_2,q_1)^T$ elde edilir. $X=Y+Z$ ayrımından $p_{21}=\alpha q_2$, $p_{12}=\gamma q_1$, $p_{22}-p_{11}=-\alpha q_1+\gamma q_2$ çıkar ve doğrudan matris çarpımıyla
   \[
     \begin{pmatrix}1&0&\alpha\\0&1&\gamma\\0&0&1\end{pmatrix}\begin{pmatrix}0&-1&0\\1&0&0\\0&0&-1\end{pmatrix}B(X)
     = \begin{pmatrix}0&-(p_{11}+\gamma q_2)&-q_2\\ p_{11}+\gamma q_2&0&q_1\\ q_2&-q_1&0\end{pmatrix}\in\mathfrak{so}_3(\mathbb{C})
   \]
   elde edilerek Tip III kapanır.

5. **Sonuç [İSPAT]:** Düzeltilmiş $r=3$ paragrafı dış literatür atfı (Atkinson/Eisenbud–Harris) olmadan kendi içinde tamamen kapalı ve hatasızdır; yalnız ilk satırda $\mathrm{GL}_3\times\mathrm{GL}_3$ ve devrik adımlarının ardışık uygulanmasında $c\in\mathbb{C}^\times$ sabitinin güncellenebileceği sözel olarak açıktır ve bir boşluk yaratmaz.

### (b) Bağımsız Singular & Macaulay2 Betikleri (A-hesaplamalı-fizikçi)
Yerel makinede Macaulay2 (M2) ve Singular kurulu değildir; bu nedenle aşağıdaki iki bağımsız doğrulama betiği **[KESİN HESAP — HENÜZ ÇALIŞTIRILMADI]** statüsündedir [KESİN HESAP — HENÜZ ÇALIŞTIRILMADI]. Her iki betik de yerleşik `permanent` işlevini kullanmaz ve açık $S_3$/$S_4$ permütasyon toplamı üzerinden çalışır [İSPAT].

---

### 1. Bağımsız Macaulay2 Betiği (`verify_perm4.m2`) — `[KESİN HESAP — HENÜZ ÇALIŞTIRILMADI]`

```m2
-- Bagimsiz M2 Dogrulamasi (yerlesik 'permanent' kullanmaz)
permSum = (M) -> (
    n := numRows M;
    sum(permutations toList(0..n-1), s -> product(n, i -> M_(i, s#i)))
);

-- (i) Pozitif kontrol: perm_3 icin codim Sing(V(perm_3)) == 6
R3 = (ZZ/32749)[x_0..x_8];
X3 = matrix table(3, 3, (i,j) -> x_(3*i+j));
J3 = ideal diff(vars R3, permSum X3);
c3 = codim J3;
print("perm_3 codim Sing = " | toString c3);
assert(c3 == 6);

-- (ii) Tam Jakobiyen ideali ve L_8 kesiti (p1 = 32749, p2 = 65521)
setRandomSeed 2026;
M8 = matrix table(16, 8, (i,j) -> random(5) - 2);
M9 = matrix table(16, 9, (i,j) -> random(5) - 2);

scan({32749, 65521}, p -> (
    R4 = (ZZ/p)[x_0..x_15];
    X4 = matrix table(4, 4, (i,j) -> x_(4*i+j));
    J4 = ideal diff(vars R4, permSum X4);
    if p == 32749 then (
        c4 = codim J4;
        print("perm_4 tam codim Sing (p=32749) = " | toString c4);
        assert(c4 == 8);
    );
    assert(rank sub(M8, ZZ/p) == 8);
    S8 = (ZZ/p)[t_0..t_7];
    f8 = map(S8, R4, flatten entries (sub(M8, S8) * transpose vars S8));
    I8 = f8 J4;
    c8 = codim I8;
    hf9 = hilbertFunction(9, S8/I8);
    print("L_8 (p=" | toString p | "): codim = " | toString c8 | ", corank(D=9) = " | toString hf9);
    assert(c8 == 8 and hf9 == 0);
));

-- (iii) Negatif kontrol: L_9 kesiti (dim >= 1)
R4p = (ZZ/32749)[x_0..x_15];
X4p = matrix table(4, 4, (i,j) -> x_(4*i+j));
J4p = ideal diff(vars R4p, permSum X4p);
S9 = (ZZ/32749)[t_0..t_8];
f9 = map(S9, R4p, flatten entries (sub(M9, S9) * transpose vars S9));
I9 = f9 J4p;
d9 = dim I9;
print("L_9 negatif kontrol dim = " | toString d9);
assert(d9 >= 1);
print("TUM M2 KONTROLLERI BASARILI.");
```

---

### 2. Bağımsız Singular Betiği (`verify_perm4.sing`) — `[KESİN HESAP — HENÜZ ÇALIŞTIRILMADI]`

```singular
// Bagimsiz Singular Dogrulamasi (yerlesik 'permanent' kullanmaz)
system("random", 2026);
int i, j, a, b, c, d;

// (i) Pozitif kontrol: perm_3 icin codim Sing(V(perm_3)) == 6
ring r3 = 32749, (x(1..9)), dp;
matrix X3[3][3] = x(1),x(2),x(3), x(4),x(5),x(6), x(7),x(8),x(9);
poly p3 = 0;
for (a = 1; a <= 3; a++) {
  for (b = 1; b <= 3; b++) {
    if (b != a) {
      c = 6 - a - b;
      p3 = p3 + X3[1,a] * X3[2,b] * X3[3,c];
    }
  }
}
ideal J3;
for (i = 1; i <= 9; i++) { J3[i] = diff(p3, var(i)); }
ideal S3 = std(J3);
int codim3 = nvars(r3) - dim(S3);
printf("perm_3 codim Sing = %s", codim3);
if (codim3 != 6) { ERROR("perm_3 pozitif kontrol basarisiz"); }

// (ii) perm_4 tam Jakobiyen ideali ve L_8 kesiti (p = 32749; Singular 4+ icin 65521 de calisir)
ring r4 = 32749, (x(1..16)), dp;
matrix X4[4][4] =
  x(1),x(2),x(3),x(4),     x(5),x(6),x(7),x(8),
  x(9),x(10),x(11),x(12),  x(13),x(14),x(15),x(16);
poly p4 = 0;
for (a = 1; a <= 4; a++) {
  for (b = 1; b <= 4; b++) {
    if (b != a) {
      for (c = 1; c <= 4; c++) {
        if (c != a && c != b) {
          d = 10 - a - b - c;
          p4 = p4 + X4[1,a] * X4[2,b] * X4[3,c] * X4[4,d];
        }
      }
    }
  }
}
ideal J4;
for (i = 1; i <= 16; i++) { J4[i] = diff(p4, var(i)); }
ideal S4 = std(J4);
int codim4 = nvars(r4) - dim(S4);
printf("perm_4 tam codim Sing = %s", codim4);
if (codim4 != 8) { ERROR("perm_4 tam codim basarisiz"); }

ring s8 = 32749, (t(1..8)), dp;
ideal L8;
poly lf;
for (i = 1; i <= 16; i++) {
  lf = 0;
  for (j = 1; j <= 8; j++) { lf = lf + random(-2, 2) * t(j); }
  L8[i] = lf;
}
map phi8 = r4, L8;
ideal S8 = std(phi8(J4));
int codim8 = nvars(s8) - dim(S8);
int cor9 = size(kbase(S8, 9));
printf("L_8: codim = %s, corank(D=9) = %s", codim8, cor9);
if (codim8 != 8 || cor9 != 0) { ERROR("L_8 kesit kontrolu basarisiz"); }

// (iii) Negatif kontrol: L_9 kesiti (dim >= 1)
ring s9 = 32749, (t(1..9)), dp;
ideal L9;
for (i = 1; i <= 16; i++) {
  lf = 0;
  for (j = 1; j <= 9; j++) { lf = lf + random(-2, 2) * t(j); }
  L9[i] = lf;
}
map phi9 = r4, L9;
ideal S9 = std(phi9(J4));
int dim9 = dim(S9);
printf("L_9 negatif kontrol dim = %s", dim9);
if (dim9 < 1) { ERROR("L_9 negatif kontrol basarisiz"); }
"TUM SINGULAR KONTROLLERI BASARILI.";
```

---

### Kısa Denetim Notları
- **Tutarlılık kriteri:** Her iki betikte `perm_3` için `codim = 6`, `perm_4` tam ideal ve `L_8` için `codim = 8` (`corank(D=9) = 0`), `L_9` için `dim >= 1` çıkması Teorem 3.1'in doğruluğunu destekler [İSPAT].
- **Çalıştırma durumu:** Makinede M2 ve Singular kurulu olmadığı için sözdizimi ve çıktı yalnızca statik incelemeye dayanır; `README.md`'deki `permanent` komutu da hâlâ doğrulanmamıştır [LİTERATÜR-DOĞRULANMADI].

### (c) Makale Değişiklik Listesi (A-hakem)
### `dc_perm4_ge_10.tex` Değişiklik Listesi

1. **Özet & Bölüm 1 (`Abstract`, `Introduction`) — Literatür Doğrulaması:** Yabe (2015), ABV (2017), Mignon–Ressayre (2004), Grenet (2011) ve Landsberg–Ressayre (2017) için verilen kesin sınır/hipotez iddiaları (özellikle ABV'nin $d>2$, $\codim \ge 5$ koşulları) birincil kaynaklardan teyit edildikten sonra kesinleştirilmelidir `[LİTERATÜR-DOĞRULANMADI]`.
2. **Bölüm 3 (`Theorem 3.1` ve `Remark: Negative Control`) — Matris Tanımı, Rank Denetimi ve Pozitif Kontrol:**
   - `Proof of Theorem 3.1`: `M_{L_8}` matrisi yalnızca `default_rng(2026)` tohumuna atıfla bırakılmamalı, açık $16\times 8$ tamsayı girdileri ekte/metinde verilmeli ve $\rank_{\mathbb{F}_p}(M_{L_8})=8$ koşulu sertifika adımı olarak belirtilmelidir `[İSPAT]`.
   - `Theorem 3.1` sonrasına bağımsız CAS (Macaulay2/Singular) doğrulaması ile $\perm_3$ pozitif kontrolü ($\codim_{\mathbb{C}^9}(\Sing(V(\perm_3)))=6$; işaret hatasıyla $\det_3$'e kaymada $4$'ten ayrılır) eklenmelidir `[İSPAT]`; tek başına Python IMSC çıktısı bağımsız CAS doğrulaması yerine geçmez `[SANI]`.
3. **Bölüm 4 (`Proposition 4.1`, `Case r = 3`) — Eksik $2\times 2$ Sıfır Bloklu Tip:**
   - "one of two types" ifadesi "one of three types (up to $\mathrm{GL}_3(\mathbb{C})\times \mathrm{GL}_3(\mathbb{C})$ and transposition)" olarak düzeltilmeli, Atkinson (1983) ve Eisenbud–Harris (1988) sınıflandırmasının karakteristik/boyut hipotezleri birincil kaynaktan doğrulanmalıdır `[LİTERATÜR-DOĞRULANMADI]`.
   - Ek alt-vaka olarak satır/sütun permütasyonlarıyla $B(X)=\begin{pmatrix}a_1&a_2&a_3\\0&0&b_2\\0&0&b_3\end{pmatrix}$ formuna getirilen $2\times 2$ sıfır bloklu uzay eklenmelidir `[İSPAT]`. Bu tipte $\adj(B)=(-a_2,a_1,0)^T(0,b_3,-b_2)$ rank-$1$ olduğundan $\perm_4=-(0,b_3,-b_2)UV(-a_2,a_1,0)^T$ eşitliği $\str(\perm_4)\le 2<4$ çelişkisini verir `[KESİN HESAP]`.
4. **Bölüm 4 (`Proposition 4.1`, `Case r = 2`) — $\det(I_w+tA)$ Çapraz Terimleri:** `Expanding det(B + t C_1 + t^2 C_2)` cümlesinin başına, $(1+t\tr(A)+O(t^2))\det(B+tC_1+t^2C_2+O(t^3))$ açılımında $\det(I_w+tA)$ kaynaklı $[t^3]$ ve $[t^4]$ çapraz terimlerinin $[t^2]=\det(B)=0$ ve $[t^3]=d_3=0$ nedeniyle sıfırlandığı açıkça eklenmelidir `[İSPAT]`.
5. **Bölüm 5 (`Step 1`, `Step 4` ve `Remark: Scope and limitations`) — Notasyon & Boolean/SAT Notu (Q3):**
   - `Step 1`: $I_W$ ideali Adım 3'ten önce burada ($I_W=\langle v_1,\dots,v_8,u_1,\dots,u_8\rangle$) tanımlanmalıdır `[İSPAT]`.
   - `Step 4`: $\perm_4\in I_W^3 \Rightarrow W^\perp\subseteq\Sing_2(V(\perm_4))$ çıkarımına $\partial_a\partial_b(I_W^3)\subseteq I_W$ gerekçesi bir cümleyle eklenmelidir `[İSPAT]`.
   - `Remark: Scope and limitations` (kısa `Motivation / Open Limitations` alt-notu olarak): Boolean/SAT aktarım bağı **ayrı bir teorem/sonuç olarak değil**, yalnızca açık sınırlılıklar notu olarak yer almalıdır; $n=4$ için elde edilen sabit alt sınırın asimptotik Boolean devre alt sınırına aktarılabilmesi için ideal-modülo bölmesiz fonksiyonel alt sınır (**H1** [AÇIK]) ve derinlik/derece aktarım koşulu (**H4** [AÇIK]) gereksinimlerinin açık kaldığı vurgulanmalıdır `[SANI]`.

### `README.md` Değişiklik Listesi

6. **Macaulay2 Doğrulama Bloğu:** `perm4 = permanent X;` satırı gerçek bir Macaulay2 oturumunda doğrulanana dek kaldırılmalı veya doğrulanmış sözdizimiyle değiştirilmelidir `[LİTERATÜR-DOĞRULANMADI]`.
7. **Tekrarlanabilirlik ve Kontrol Listesi:** `README.md` içine betiğin `rank(M_L8)==8` kontrolü, $\perm_3$ ($\codim\Sing=6$) pozitif kontrol komutu ve bağımsız Singular/M2 doğrulama yönergesi eklenmelidir `[SANI]`.

### (d) Uzman Gönderim Planı (A-determinantal-karmaşıklık)
### 1. Birincil Kaynak Literatür Kontrol Listesi
- **ABV 2017 (`FoCM 2017`, Teorem 1.2):** $\dc_{\mathbb{C}}(f)\ge \codim(\Sing(V(f)))+1$ sınırının $\codim > 4$ ($\ge 5$), $d>2$ ve indirgenemezlik/afin-projektif kodboyut hipotezleri ile $\perm_4\ge 9$ çıkarımının ABV'de mi yoksa bu makalede mi kurulduğu birincil kaynaktan doğrulanmalıdır [LİTERATÜR-DOĞRULANMADI].
- **Mignon–Ressayre 2004 (`IMRN 2004`):** $\dc_{\mathbb{C}}(\perm_n)\ge n^2/2$ alt sınırının kesin tanım koşulları (afin/homojen ayrımı ve Hessian rank argümanı) birincil kaynaktan doğrulanmalıdır [LİTERATÜR-DOĞRULANMADI].
- **Yabe 2015 (`arXiv:1504.00151`):** $\mathbb{R}$ üzerinde $\dc_{\mathbb{R}}(\perm_n)\ge (n-1)^2+1$ sınırı ($n=4$ için $10$) ve "reel imza/pozitiflik kısıtları" açıklamasının kesin ispat mekanizması birincil kaynaktan doğrulanmalıdır [LİTERATÜR-DOĞRULANMADI].
- **Landsberg–Ressayre 2017 (`Abh. Math. Semin. Univ. Hambg.`):** Eşit-simetrik determinantal karmaşıklıkta $\mathrm{edc}_{\mathbb{C}}(\perm_4)=15$ alt sınırının tam simetri altgrubu koşulu ve sınır karmaşıklığı ($\underline{\dc}$) ilişkisi birincil kaynaktan doğrulanmalıdır [LİTERATÜR-DOĞRULANMADI].
- **Atkinson 1983 & Eisenbud–Harris 1988:** Karakteristik $\neq 2$ üzerinde $\rank\le 2$ olan $3\times 3$ lineer matris uzaylarının sıfır satır, sıfır sütun, $2\times 2$ sıfır blok ve $\mathfrak{so}_3$ tipleri dışında başka bir tip bırakmadığı birincil kaynaklardan doğrulanmalıdır [LİTERATÜR-DOĞRULANMADI].

### 2. Gönderim Öncesi Zorunlu Son Kapılar
- **Kapı 1 — Cebirsel Boşlukların Kapatılması:** Önerme 4.1 ($r=3$) içine $2\times 2$ sıfır bloklu sıkıştırma tipi ($\adj(B)=pq^T \implies \str(\perm_4)\le 2$) ile sıfır sütun durumu açıkça eklenmelidir [İSPAT]. Ana ispatta $d_v=0$ ($v\equiv 0$) ve $d_z=0$ ($u=Ky$) uç blok durumları not edilmeli, sonucun yalnızca kesin $\dc_{\mathbb{C}}(\perm_4)$ için geçerli olup $\underline{\dc}_{\mathbb{C}}(\perm_4)$'ü kapsamadığı açıkça belirtilmelidir [İSPAT].
- **Kapı 2 — Sertifika ve Bağımsız CAS Kapısı:** `verify_codim_sing_perm4.py` içine $M_{L_8}$'in mod-$p_1,p_2$ tam rank $8$ denetimi ve ideal kuruluşunu sınayan $\perm_3$ ($\codim\Sing=6$) pozitif kontrolü eklenmelidir [İSPAT]. Teorem 3.1 ($\codim=8$) Macaulay2 veya Singular'da bağımsız çalıştırılmalı ve `README.md`'deki `permanent` komutunun M2 sözdiziminde geçerliliği doğrulanmalıdır [LİTERATÜR-DOĞRULANMADI].
- **Kapı 3 — Boolean/SAT Aktarım Notu:** Nicel aktarım tartışması ayrı bir sonuç/teorem gibi değil, yalnızca H1 ve H4'ün açık olduğunu vurgulayan kısa bir "Motivasyon / Tartışma" notu olarak yerleştirilmelidir [SANI].

### 3. Uzman ve Dergi Gönderim Planı
- **Ön Hakem / Uzman Listesi:** Kapı 1–3 tamamlandıktan sonra taslak, doğrudan ilgili yazarlara (J. Alper, T. Bogart, M. Velasco, J. M. Landsberg, N. Ressayre, A. Yabe) teknik ön-inceleme için iletilmelidir [SANI].
- **Dergi Hedefleri:** Kesin sertifika ve determinantal karmaşıklık profili nedeniyle *Foundations of Computational Mathematics*, *Computational Complexity* veya *Journal of Symbolic Computation* öncelikli gönderim hedefleridir [SANI].

---

## Tur 4 — mod-A Son Hükmü

### BÖLÜM I — KANIT ADIMI OY SAYIMI VE AÇIK SORULAR

**1. Ana Kanıt Adımları Oy Özeti (10 Grup A üyesi + mod-A denetimi):**
- **Prop 2.3 ($\codim(\Sing_2(V(\perm_4))) = 12$):** Kabul (çoğunlukla doğrudan onaylandı; `A-cebirsel-geometri` ve `A-kombinatorik` satır satır doğruladı, red oyu yok) — $\mathrm{char}\neq 2$ altında $36$ alt-permanent, $K_{a,b}$ tek bileşeni ve $(4+4+36)$ ayrık katman sayımı geçerlidir (`"induced 2-edge matching"` yerine `"2-edge matching"` yazılmalı ve `36` kuadrik bileşen ters yönde açıkça anılmalıdır) `[İSPAT]`.
- **Thm 3.1 ($\codim(\Sing(V(\perm_4))) = 8$, IMSC):** Belirsiz / Koşullu Kabul (`10/10` cebirsel IMSC mantığını kabul etti, ancak betiğin bu oturumda çalıştırılmaması, bağımsız CAS yokluğu ve $\perm_3$ pozitif kontrolünün eksikliği nedeniyle sertifika deneysel olarak doğrulanmamış sayıldı) — IMSC–Hilbert denkliği ve `corank=0 \implies \rank_{\mathbb{F}_p}(M_{L_8})=8` çıkarımı sağlamdır; fakat `R_canon @ C_s` için taşma `assert`'i ve $M_{L_8}$ matrisinin metinde açık verilmesi gerekir `[İSPAT]`.
- **Lemma 2.2 & $\str(\perm_4) = 4$:** Koşullu Kabul (`Thm 3.1`'e bağlı olarak itirazsız) — Krull'un esas ideal teoremiyle $\codim(\Sing)\le 2\str$ ve Laplace açılımıyla $\str\le 4$ geçerlidir `[İSPAT]`.
- **Prop 4.1 ($r = 0$ ve $r \ge 5$):** Kabul (itirazsız; `A-mat-fizikçi-simetri` küçük bir sıra düzeltmesi önerdi) — $\det(PQ)=1$ ölçeklemesinden önce $t=0 \implies \det(A_0)=0 \implies r \ge 1$ yazılmalı; $r\ge 5$ için $t^r$ çarpanı $[t^4]=0$ verir `[İSPAT]`.
- **Prop 4.1 ($r = 4$):** Koşullu Kabul (`Thm 3.1`'e bağlı olarak itirazsız) — $\perm_4=\det_4(B)$ halinde $\codim B^{-1}(\Sigma_2)\le 4 < 8$ çelişki verir `[İSPAT]`.
- **Prop 4.1 ($r = 3$, makaledeki mevcut metin):** Red (`10/10` red) — $\rank\le 2$ olan $3\times 3$ matris uzaylarında $2\times 2$ sıfır bloklu sıkıştırma tipi eksiktir ve devrik işleminin tüm $M(tX)$ bloğuna uygulanıp sıfır sütunu kapattığı yazılmamıştır `[İSPAT]`.
- **Prop 4.1 ($r = 3$, Tur 3'teki düzeltilmiş metin):** Kabul (`A-sınırlı-rank-uzayları` üretti, `A-lineer-cebir` ve `mod-A` satır satır yeniden türetti, red yok) — Tip II ($2\times 2$ sıfır blok) için $\adj(B)=pq^T$ rank-$1$ olup $\str(\perm_4)\le 2<4$ verir ve öz-yeterli $\max\rank\in\{1,2\}$ sınıflandırması 4. bir tip olmadığını dış literatüre dayanmadan kanıtlar `[İSPAT]`.
- **Prop 4.1 ($r = 2$):** Koşullu Kabul (`str=4`'e bağlı; `A-hakem` ve `A-değişmeli-cebir` netleştirme istedi) — $\mathbb{C}[X]$ UFD indirgemesi geçerlidir; $\det(I_w+tA)$ çapraz terimlerinin $\det(B)=d_3=0$ ile sıfırlandığı ve sütun işleminin $V$'yi de dönüştürdüğü eklenmelidir `[İSPAT]`.
- **Lemma 5.1 (Skew-Square Lemması):** Kabul (`A-lineer-cebir`, `A-kuantum-bilgi` ve `mod-A` yeniden türetti, red yok) — $K$ tekil veya sıfırken bile $(M^2K)^T = -M^2K$ özdeşliği geçerlidir `[İSPAT]`.
- **Thm 1.1 Ana İspat ($m=9 \implies I_W^3 \implies$ çelişki):** Koşullu Kabul (`Thm 3.1` ve `Prop 2.3`'e bağlı, red yok) — $\Omega$-izotropisi, $2$-blok normal form, $[t^3]=0$ $\xi$-lineer ayrımı ve $\perm_4\in I_W^3 \implies W^\perp\subseteq\Sing_2$ zinciri doğrudur; $d_v\ge 1$ ($d_v=0\implies\perm_4\equiv 0$), $d_z=0$ uç durumu, $I_W$ ön-tanımı ve $\underline{\dc}_{\mathbb{C}}$'nin kapsanmadığı not edilmelidir `[İSPAT]`.
- **README.md Macaulay2 Kodu:** Red / Belirsiz (`10/10` doğrulanamadı) — Yerleşik `permanent` fonksiyonunun varlığı doğrulanmamıştır ve yerel makinede M2 yoktur `[LİTERATÜR-DOĞRULANMADI]`.
- **Literatür İddiaları (Yabe 2015, ABV 2017, Mignon–Ressayre 2004, Atkinson 1983, Eisenbud–Harris 1988, Grenet 2011, Landsberg–Ressayre 2017):** Belirsiz — Hiçbiri birincil kaynaklardan teyit edilmemiştir `[LİTERATÜR-DOĞRULANMADI]`.

**2. `crit-A`'nın Cevapsız Kalan Açık Soruları:**
- Yerel makinede M2, Singular, Sage ve SymPy bulunmadığından `verify_codim_sing_perm4.py`, `verify_perm4.m2` ve `verify_perm4.sing` betiklerinin hiçbiri çalıştırılamamıştır `[SANI]`.
- `build_subperm3_on_L` fonksiyonunun $4\times 4$ döngü/indeks hatalarını yakalamak için yalnızca ayrı bir $\perm_3$ fonksiyonu yetmez; $n$-parametreli alt-permanent kurucu + $\det_4$ ($\codim=4$) + noktasal $\nabla\perm_4$ çapraz kontrolü henüz betiğe eklenmemiştir `[İSPAT]`.
- `verify_codim_sing_perm4.py` içindeki `step_imsc` taşma `assert`'i ve açık $\rank_{\mathbb{F}_p}(M_{L_8})=8$ kontrolü henüz koda işlenmemiştir `[KESİN HESAP]`.
- `README.md`'deki `permanent X` komutunun M2 sözdiziminde geçerliliği ve Atkinson/EH/ABV/Yabe/MR/LR hipotezleri birincil kaynakta doğrulanmamıştır `[LİTERATÜR-DOĞRULANMADI]`.
- `QUANTITATIVE_TRANSFER_THEOREM_SYNTHESIS.md` özetinde `H4` koşulunun tam metni kesik olduğundan içeriği hâlâ belirsizdir `[LİTERATÜR-DOĞRULANMADI]`.

---

### BÖLÜM II — ZORUNLU SON ÇIKTI BİÇİMİ

#### 1. Karar Soruları (Q1 / Q2 / Q3)

**Q1:**
1. Evet, Tur 3'te üretilen düzeltilmiş $r=3$ paragrafı eklendiğinde makalenin cebirsel zinciri mantıksal olarak tamamen kapanmaktadır (yalnızca `Thm 3.1`'deki $\codim\Sing=8$ sertifikasına koşulludur) `[İSPAT]`.
2. Düzeltilmiş paragrafta önce $\mathrm{diag}(P_1,I_w)/\mathrm{diag}(Q_1,I_w)$ ölçeklemesi ve tüm $M(tX)^T$ devriği tanımlanmalı, böylece sıfır sütun sıfır satıra indirgenmelidir `[İSPAT]`.
3. Ardından 3. tip olarak $2\times 2$ sıfır bloklu sıkıştırma uzayı eklenmeli; $\adj(B)=pq^T$ ($p=(0,-b_{13},b_{12})^T$, $q=(0,b_{31},-b_{21})^T$) üzerinden $c\,\perm_4 = -b_{31}(UVp)_2 + b_{21}(UVp)_3$ ve $\str(\perm_4)\le 2 < 4$ türetilmelidir `[İSPAT]`.
4. Sonuna Tur 3'teki $\max\rank\in\{1,2\}$ ayrımına dayalı öz-yeterli tamlık kanıtı konarak 4. bir tip bulunmadığı gösterilmeli ve Atkinson/EH atfına olan zorunlu bağımlılık kaldırılmalıdır `[İSPAT]`.

**Q2:**
1. Yerleşik `permanent` kullanmayan, açık $S_3$/$S_4$ permütasyon toplamlı bağımsız Macaulay2 (`verify_perm4.m2`) ve Singular (`verify_perm4.sing`) betikleri çalıştırılmalıdır `[SANI]`.
2. Python tarafında `build_subperm_k` $n$-parametreli yapılıp `perm_3` ($\codim=6$, `det_3`'ün `4`'ünden ayırır) ve `det_4` ($\codim=4$) kontrolleri ile noktasal $\nabla\perm_4$ testi eklenmeli; `float64` BLAS'tan bağımsız küçük-bloklu `int64` veya seyrek RREF doğrulaması yapılmalıdır `[İSPAT]`.
3. Tutarlılık ölçütü: `perm_3` için `codim = 6`, `det_4` için `codim = 4`, tam $J(\perm_4)$ ve $L_8$ kesiti için `codim = 8` (`D=9`'da `hilbertFunction = 0` / `corank = 0`, `rank(M_L8)=8`), `L_9` için `dim >= 1` çıkmalıdır `[İSPAT]`.

**Q3:**
1. **Makale düzeltmeleri:** Düzeltilmiş öz-yeterli $r=3$ vakasını koy; $M_{L_8}$ girdilerini metne/eke yaz; Prop 2.3 (`2-edge matching`, `36` kuadrik), Prop 4.1 ($r=0$ sırası, $r=2$ çapraz terim/sütun işlemi) ve Bölüm 5 ($d_v\ge 1$, $d_z=0$, $I_W$ ön-tanımı, $\partial^2(I_W^3)\subseteq I_W$, $\underline{\dc}_{\mathbb{C}}$ kapsam sınırı) netleştirmelerini yap `[İSPAT]`.
2. **Altyapı ve literatür:** `README.md`'deki doğrulanmamış `permanent X` M2 kodunu açık permütasyon toplamlı çalışan M2/Singular betikleriyle değiştir; tüm literatür teorem/hipotezlerini birincil kaynaklardan teyit et `[LİTERATÜR-DOĞRULANMADI]`.
3. **Boolean/SAT aktarım notu:** Ayrı teorem/sonuç olarak değil, yalnızca Bölüm 5 sonundaki "Motivasyon / Tartışma" (`Remark: Scope and limitations`) içine konulmalı; $n=4$'teki sabit alt sınırın ve $O(n^2)$ bariyerinin ötesinde Boolean devre alt sınırına geçiş için ideal-modülo bölmesiz fonksiyonel alt sınır (H1 açık) ile derece/derinlik aktarım koşulunun (H4 açık) sağlanmadığı açıkça vurgulanmalıdır `[SANI]`.

---

#### 2. Kesin Olarak Doğru Bulunanlar ve Hâlâ Doğrulanmamış Olanlar

**Kesin olarak doğru bulunanlar:**
- Prop 2.3 ($\codim(\Sing_2(V(\perm_4))) = 12$) ve `4 + 4 + 36` ayrık bileşen sayımı `[İSPAT]`.
- Lemma 2.2 ($\codim\Sing \le 2\str$) ve $\codim\Sing=8$ altında $\str(\perm_4)=4$ sonucu `[İSPAT]`.
- Prop 4.1 ($r=0, r\ge 5, r=4, r=2$) elemeleri ve Tur 3'teki düzeltilmiş, öz-yeterli $r=3$ kanıtı ($2\times 2$ sıfır blokta $\adj(B)=pq^T \implies \str\le 2$) `[İSPAT]`.
- Skew-Square Lemması ($K$ tekilken dahil) ve $m=9 \implies \dim W=8 \implies \perm_4\in I_W^3 \implies W^\perp\subseteq\Sing_2 \implies 12\le 8$ çelişkisi `[İSPAT]`.
- IMSC syzygy kurulumunun $\dim_{\mathbb{F}_p}(R_{D+1}/I_{D+1})$ ile denkliği ve `D=9` `corank=0` çıktısının $\rank_{\mathbb{F}_p}(M_{L_8})=8$'i zorlaması `[İSPAT]`.
- `rref_mod_p_exact` ($96\cdot 65520^2 \approx 4.12\times 10^{11} < 2^{53}$) ile $L_8/L_9$ için `R_canon @ C_s` ($\le 8.08\times 10^{11} < 2^{53}$) çarpımlarında tam tamsayı taşma sınırının korunması `[KESİN HESAP]`.

**Hâlâ doğrulanmamış olanlar:**
- `verify_codim_sing_perm4.py` çıktısı (`[132, 32, 8, 0]` ve `[753, 580]`) bu oturumda yürütülmemiştir ve bağımsız CAS kontrolü yoktur `[SAYISAL]`.
- Bağımsız Macaulay2 (`verify_perm4.m2`) ve Singular (`verify_perm4.sing`) betikleri makinede kurulu CAS olmadığı için çalıştırılmamıştır `[SANI]`.
- `README.md`'deki M2 `permanent X` komutunun geçerliliği bilinmemektedir `[LİTERATÜR-DOĞRULANMADI]`.
- Atkinson (1983), Eisenbud–Harris (1988), ABV (2017), Mignon–Ressayre (2004), Yabe (2015), Grenet (2011) ve Landsberg–Ressayre (2017) kaynaklarındaki kesin hipotez ve teorem ifadeleri birincil kaynaklardan teyit edilmemiştir `[LİTERATÜR-DOĞRULANMADI]`.
- `QUANTITATIVE_TRANSFER_THEOREM_SYNTHESIS.md` özetindeki `H4` koşulunun tam içeriği metinde kesik kaldığı için belirsizdir `[LİTERATÜR-DOĞRULANMADI]`.

---

#### 3. Gruptaki En Güçlü İtiraz ve Nasıl Karşılandığı
- **En güçlü itiraz:** Makaledeki `r=3` vakasının $2\times 2$ sıfır bloklu sıkıştırma tipini atlaması ve kalan tiplerin tamlığı için birincil kaynakta doğrulanmamış Atkinson/EH atfına dayanması (ek olarak `Thm 3.1`'in tek başına çalıştırılmamış Python betiğine bağlı kalması) `[İSPAT]`.
- **Nasıl karşılandı:** `A-sınırlı-rank-uzayları` tarafından $2\times 2$ sıfır blok tipi ($\adj(B)=pq^T \implies \str\le 2$) ile birlikte $\max\rank\in\{1,2\}$ ayrımına dayalı sıfırdan, dış kaynağa ihtiyaç duymayan tam $3\times 3$ sınıflandırma kanıtı yazıldı ve `A-lineer-cebir` ile `mod-A` tarafından doğrulandı `[İSPAT]`. Sertifika açığı ise açık $S_3$/$S_4$ toplamlı M2/Singular betikleri ve $\perm_3$/$\det_4$ pozitif kontrol protokolü tanımlanarak çerçevelendi (çalıştırılması bir sonraki adıma bırakıldı) `[SANI]`.

---

#### 4. Güven Düzeyi ve Nedeni
- **Cebirsel ispat iskeleti (`Thm 3.1` ve literatür atıfları koşullu):** **Yüksek** — Eksik $r=3$ tipi ve tüm uç/editörlük boşlukları satır satır yeniden türetilerek kapatılmıştır `[İSPAT]`.
- **Bütün olarak makalenin mevcut gönderime hazır olma düzeyi:** **Orta** — $\codim(\Sing(V(\perm_4)))=8$ sertifikası bağımsız bir CAS'ta (M2/Singular) çalıştırılmadığı, $\perm_3$/$\det_4$ pozitif kontrolleri betiğe eklenip koşulmadığı ve birincil literatür kontrolleri tamamlanmadığı için makale henüz uzman gönderimine hazır değildir `[SANI]`.

---

#### 5. Bir Sonraki Somut Tek Adım
- `verify_perm4.m2` veya `verify_perm4.sing` betiğini Macaulay2/Singular kurulu bir ortamda çalıştırarak `perm_3` ($\codim=6$), tam $J(\perm_4)$ ($\codim=8$), $L_8$ (`D=9` `corank=0`) ve $L_9$ (`dim>=1`) çıktılarını doğrulamak; eşzamanlı olarak düzeltilmiş $r=3$ metnini `dc_perm4_ge_10.tex` içine işlemek `[SANI]`.

---

#### 6. Azınlık Görüşleri
- `A-hesaplamalı-fizikçi` ve `A-değişmeli-cebir`, `corank=0` çıktısının zaten $\rank_{\mathbb{F}_p}(M_{L_8})=8$'i cebirsel olarak zorladığını kanıtlasa da, `A-kombinatorik` ve `A-hakem` savunmacı mühendislik açısından açık bir rank `assert`'i ve $M_{L_8}$ matrisinin metinde basılmasını zorunlu görmüştür (uzlaşı olarak ikincisi benimsendi) `[İSPAT]`.
- `A-cebirsel-geometri`, $3\times 3$ indeksleme hatalarını yakalamak için $\perm_3$ pozitif kontrolünün tek başına yetmeyeceğini, ek olarak $4\times 4$ $\det_4$ ($\codim=4$) veya `n`-parametreli fonksiyon testinin gerektiğini vurgulamıştır `[İSPAT]`.

---

### mod-A (Grup Moderatörü) Kendi Görüşüm
- Düzeltilmiş $r=3$ kanıtının tüm kofaktör işaretlerini ve $\mathfrak{so}_3$ matris çarpımını bizzat yeniden hesapladım; el ile yapılan cebirsel kanıt (`Thm 3.1`'deki $\codim\Sing=8$ girdisi sağlandığı sürece) tamamen tutarlı ve öz-yeterlidir `[İSPAT]`.
- Makalenin en kritik zayıf noktası artık $r=3$ değil, `Thm 3.1`'in tek başına bir `rng(2026)` Python betiğine dayanması ile birincil literatürün (özellikle ABV 2017 ve Yabe 2015 hipotezlerinin) henüz çapraz okunmamış olmasıdır `[LİTERATÜR-DOĞRULANMADI]`.
- Bu iki kapı kapatılıp Q1–Q3 düzeltmeleri uygulandığında taslak dış hakeme sunulabilir olgunluğa ulaşacaktır `[SANI]`.
