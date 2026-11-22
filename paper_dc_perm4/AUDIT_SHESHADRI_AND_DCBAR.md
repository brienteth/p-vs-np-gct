# Birincil Metin Denetim Dosyası: Sheshadri (2611.06658), ≥ 10 İspatının Değeri / perm₅ ve Sınır Karmaşıklığı (dc-bar)

6 Kişilik Odaklanmış Panel: Moderatör, Eleştirmen, Cebirsel geometri, Sınırlı rank uzayları / temsil, Sınır karmaşıklığı uzmanı, Hesaplamalı cebir.

---

## KONU 1 — Sheshadri (`2611.06658`) Denetimi ve Karşılaştırma

### Tur 1 — Bağımsız Birincil Metin Okuması ve Yeniden Türetim

### Cebirsel geometri
# Konu 1 (Tur 1): Birincil Metin Yeniden Türetimi ve Karşılaştırma

> **Notasyon ve Bölümleme Notu:** Verilen `per4_dc_15.tex` metninde `lem:zero2`, `lem:singF`, `prop:singdim` sonuçları **Bölüm 2.3 (`\subsection{The singular locus}`)** altında, `lem:cubicirreducible`, `lem:crossdet`, `lem:tenranktwo` ise **Bölüm 2.2 (`\subsection{Polynomials attached to the permanent}`)** altında yer almaktadır; aşağıda her ikisi de eksiksiz türetilmiştir. [İSPAT]

---

## 1. Sheshadri (Bölüm 2.2–2.5 ve Bölüm 3) Adım Adım Yeniden Türetim

### Bölüm 2.2: Permanenta Bağlı Polinomlar
* **`lem:cubicirreducible` ($F_z$ ve $\per_3$ indirgenemezliği):**
  * $\C[a,b,c]$ tamlık bölgesi olduğundan her değişken grubunda en büyük ve en küçük dereceler çarpımda toplanır; dolayısıyla multiderecesi $(1,1,1)$ olan bir çarpım ancak multihomojen çarpanlara ayrılabilir ve bir çarpan tek bir satırda lineer olmalıdır (diğer satırlardan bağımsız). [İSPAT]
  * $\per_3$ için bir satıra göre kısmi türevler kalan iki satırdaki üç ayrı $2\times 2$ subpermanenttir; her biri diğerlerinde bulunmayan tekterimliler içerdiğinden lineer bağımsızdır ($\dim = 3 > 1$), bu nedenle türevler tek bir polinomun katları olamaz. [İSPAT]
  * $F_z(a,b,c)=\per_4(z,a,b,c)$ ($z\neq 0$) için $z_j\neq 0$ seçilip $a_j=b_j=c_j=0$ koyulduğunda $F_z$ kalan üç sütunda $z_j\per_3$'e indirgenir; dolayısıyla uzmanlaşmadan önce de her alt satırdaki kısmi türev uzayı en az $3$ boyutludur ve çarpanlara ayrılamaz. [İSPAT]

* **`lem:crossdet` ($\det B_1(a)$ ve $\Delta(u,v)=\det B(u,v)$):**
  * $B_1(a)$ simetrik ve $a$'da derece $1$ olduğundan $\det B_1(a)$, $a_1,a_2,a_3,a_4$'te $4$. derece simetrik homojen polinomdur; yani $e_1^4, e_1^2e_2, e_1e_3, e_2^2, e_4$'ün lineer birleşimidir. $a_3=a_4=0$ iken $B_1(a_1,a_2,0,0)$'ın ilk iki satırı $(0,0,a_2,a_2)$ ve $(0,0,a_1,a_1)$ olarak orantılıdır, dolayısıyla $e_3=e_4=0$ iken $\det B_1=0$ olur ve $e_1^4, e_1^2e_2, e_2^2$ katsayıları sıfırdır. [İSPAT]
  * $a=(1,1,1,0)$ için satır/sütun indirgemesiyle $\det B_1(1,1,1,0)=-12$ ($e_1e_3=3$), $a=(1,1,1,1)$ için $B_1(\mathbf{1})=2(J_4-I_4)$ özdeğerleri $6,-2,-2,-2$ çarpımından $\det B_1(\mathbf{1})=-48$ ($e_1e_3=16, e_4=1$) elde edilir; buradan $\det B_1(a) = -4(e_1e_3-4e_4) = -4q(a)$ bulunur. [İSPAT]
  * $q(a)=Pa_1^2+(SP-3R)a_1+SR$ ($S,P,R$: $a_2,a_3,a_4$'ün temel simetrik polinomları) ilkeldir ($\gcd(P,R)=1$) ve $a_1$'e göre diskriminantı $(SP-R)(SP-9R) = (a_2+a_3)(a_2+a_4)(a_3+a_4)(SP-9R)$ olup $a_2=-a_3$'te $SP-9R = 8a_3^2a_4 \neq 0$ olduğundan tek katlı çarpan içerir, tam kare değildir; Gauss lemması ile $q$ indirgenemezdir. [İSPAT]
  * $u_1u_2u_3u_4\neq 0$ açık kümesinde $B(u,v)=U\diag(u_i^{-1})B_1(v/u)\diag(u_i^{-1})$ ($U=\prod u_i$) ve $\Delta(u,v)=-4U^2 q(v/u)$ olur. $u_i=0$ sınırında Schur tümleyeniyle $\Delta|_{u_i=0} = -4v_i^2 \prod_{j\neq i}u_j \sum_{j\neq i}u_j\prod_{k\neq i,j}v_k \neq 0$ olduğundan hiçbir $u_i$ çarpanı $\Delta$'yı bölmez; dolayısıyla $\Delta$ hem $\C[u,v]$'de hem de $\C(u)[v]$'de indirgenemezdir. [İSPAT]

* **`lem:tenranktwo` ($\rk B_1(a)\le 2$ olan sıfırdan farklı vektörler):**
  * Sıfır köşegenli simetrik matrisin rankı $1$ olamaz ($\lambda vv^T$ köşegeni $\lambda v_i^2=0$ verir). Rank $2$ olan sıfır köşegenli simetrik matris $rs^T+sr^T$ biçimindedir ve $r_is_i=0$ olduğundan sıfırdan farklı giriş deseni $\supp(r)\sqcup \supp(s)$ üzerinde tam iki parçalıdır. [İSPAT]
  * $B_1(a)$'nın $i$. satırı sıfır olsaydı diğer üç koordinat sıfır olur ($\mathrm{char}\neq 2$), kalan $3\times 3$ bloğun determinantı $2a_i^3=0$ ile $a=0$ çıkardı; yani tüm $4$ indeks iki parçalı bölünmeye katılır. [İSPAT]
  * $1+3$ bölünmesinde $\{1\}\mid\{2,3,4\}$ için iç sıfırlar $a_1+a_2=a_1+a_3=a_1+a_4=0 \implies a\in\C^*(-1,1,1,1)$ verir ($4$ permütasyon). $2+2$ bölünmesinde $\{1,2\}\mid\{3,4\}$ için $a=(p,-p,q,-q)$ ve çapraz $2\times 2$ bloğun determinantı $-4pq=0$ olduğundan $p=0$ veya $q=0$ çıkar ($6$ adet $e_i-e_j$ doğrusu). Doğrudan yerine koyma hepsinde rank $2$ verir. [İSPAT]

---

### Bölüm 2.3: Tekil Küme (`lem:zero2`, `lem:singF`, `prop:singdim`)
* **`lem:zero2` (Tüm $2\times 2$ subpermanentlerin sıfırlanması):**
  * Bir satırda $\ge 3$ sıfırdan farklı giriş varsa, başka bir satırın bu sütunlardaki oranları $t_i+t_j=0$ ($\mathrm{char}\neq 2$) ile $t_i=0$ olur ve kalan sütunlar da ilk satırla kıyaslanınca $0$ çıkar (tek satır). [İSPAT]
  * En çok $2$ sıfırdan farklı girişli satır varsa, diğer satırlar bu iki sütun dışında sıfırdır ve bu sütunlarda $(\lambda a,-\lambda b)$ biçimindedir; iki ek satır $-2\lambda\mu ab\neq 0$ üreteceğinden en çok bir ek satır sıfırdan farklı olabilir ($ad+bc=0$ olan $2\times 2$ dikdörtgen). [İSPAT]
  * Her satırda en çok $1$ sıfırdan farklı giriş varsa, ayrı satır ve ayrı sütundaki iki giriş $2\times 2$ sıfırdan farklı permanent üreteceğinden tüm girişler tek sütunda (veya tek satırda) toplanır. Sonuç olarak $\dim\Sing(\per_3)=3$'tür. [İSPAT]

* **`lem:singF` ($\dim\Sing(F)=4$):**
  * Denklemler $B_1(a)b=0$, $B_1(a)c=0$, $B_1(b)c=0$ şeklindedir. $a$'nın rankına göre katmanlaştırma:
    * $\rk B_1(a)=4$: $b=c=0 \implies \dim = 4$. [İSPAT]
    * $\rk B_1(a)=3$: $\ker B_1(a)=\C k$ ($k\neq 0$), $b=sk, c=tk$, kalan denklem $st B_1(k)k=0$. $(B_1(k)k)_i = 2 e_2(\hat{k}_i)$ olduğundan $|\supp(k)|\in\{2,3\}$ iken $i\notin\supp(k)$ bileşeni sıfırdan farklı bir çarpım verir; $|\supp(k)|=4$ iken $\sum_{j\neq i} 1/k_j=0 \implies 1/k_i = T \implies T=4T$, imkânsızdır. Yalnızca $k=e_i$ istisnai olup $B_1(a)e_i=0$ $4$ doğru verir (lif $\dim 2 \implies \le 3$). Diğer tüm $\rk=3$ durumlarında $st=0$ (lif $\dim 1$, taban $\dim\le 3 \implies \le 4$). [İSPAT]
    * $\rk B_1(a)=2$: `lem:tenranktwo` gereği taban $\dim 1$; $L=\ker B_1(a)$ ($\dim 2$) üzerinde $B_1(b)c=0$ özdeş sıfır değildir (aksi hâlde $B_1(w)w=0$ $2$-düzlem içerirdi), dolayısıyla $L\times L$'de $\dim\le 3$, toplam $\le 4$. [İSPAT]
    * $\rk B_1(a)=0 \implies a=0$: $B_1(b)c=0$ denkleminde $\rk B_1(b)=4,3,2,0$ katmanları sırasıyla $\le 4+0, 3+1, 1+2, 0+4$ boyutlu olup hepsi $\le 4$'tür. $b=c=0$ katmanı $4$ boyutlu olduğundan $\dim\Sing(F)=4$'tür. [İSPAT]

* **`prop:singdim` ($\dim\Sing(\per_4)=8$):**
  * İlk iki satırı sıfır olan matrisler $8$-boyutlu altuzay oluşturduğundan $\dim\Sing(\per_4)\ge 8$. [İSPAT]
  * Ters eşitsizlik için sıfırdan farklı matrisler, bir sıfırdan farklı satır $z$ (1. satıra permüte edilir) ve desteğiyle sonlu kaplanır. Alt $3$ satırın türevleri bu satırların $\Sing(F_z)$'de olmasını gerektirir:
    * $|\supp(z)|=4$: sütun ölçeklemesi $F_{\mathbf{1}}$'e indirger; `lem:singF` ile lif $\dim=4$, taban $4 \implies \le 8$. [İSPAT]
    * $|\supp(z)|=1$: $3$ serbest sütun + $\Sing(\per_3)$ ($\dim 3$) ile lif $\dim=6$, taban $1 \implies \le 7$. [İSPAT]
    * $|\supp(z)|=2$: $t=z_2y_1+z_1y_2$ değişken değişimiyle $F_z$, $3$ tamamlayıcı koordinattan bağımsız bir $\per_3$'tür; lif $\dim=6$, taban $2 \implies \le 8$. [İSPAT]
    * $|\supp(z)|=3$: ölçekleme ile $z=(1,1,1,0)$, alt satırlar $(v_i,t_i)\in\C^3\times\C$, $C=C(1,1,1)$ ($\det C=2\neq 0$). Alt satır gradyanları $t_2v_3+t_3v_2=0$, $t_1v_3+t_3v_1=0$, $t_1v_2+t_2v_1=0$ ve $v_i^T C v_j=0$ ($i\neq j$) verir. $3,2,1$ adet $t_i\neq 0$ durumları sırasıyla lif $\dim\le 3, 4, 4$ verir. $t_1=t_2=t_3=0$ iken $\partial_{14}f = \per_3(v_1,v_2,v_3)=0$ eklenir: lineer bağımlı $C$-ortogonal üçlüler $\dim\le 5$ (sıfır vektör varsa $\dim 5$; tam $2$-boyutlu germede $c_1v_1+c_2v_2+c_3v_3=0$ tüm katsayıları $\neq 0$ yapamaz, aksi hâlde $v_i^T C v_i=0$ ile $2$-boyutlu tamamen izotropik altuzay çıkardı; dolayısıyla ikisi izotropik bir doğru üzerinde orantılı, üçüncüsü dik düzlemde olup $\le 1+2+2=5$); tam ranklı $C$-ortogonal üçlüler $C\mapsto I_3$ sonrası $\mathrm{SO}_3(\C)\times(\C^*)^3$ görüntüsü olarak $6$-boyutlu indirgenemez küme oluşturur ve tanık $O$ üzerinde $OCO^T=\diag(10,-90,-18)$, $\per_3(O)=-24\neq 0$ doğrudan sağlanır, dolayısıyla $\per_3=0$ ile kesişim $\dim\le 5$, taban $3$ ile toplam $\le 8$. [İSPAT]

---

### Bölüm 2.4–2.5: Düzenlilik, Normal Form ve Uç Nokta Eşitsizliği
* **`lem:regularity` (Her sıfırda $\rk A(p)=m-1$):**
  * $\mathcal{D}=\{M\in\C^{m\times m}:\rk M\le m-2\}$ kümesinde $\rk=m-2$ yoğun ve indirgenemez olup boyutu $(m-2)(m+2)=m^2-4$, yani $\codim(\mathcal{D})=4$'tür. Boş olmayan her bileşen için $Z=A^{-1}(\mathcal{D})\subset\C^{16}$ kodimensiyonu $\le 4$ olur. Zincir kuralıyla $\nabla(\det)|_{\mathcal{D}}=0 \implies Z\subseteq\Sing(f)$, ancak `prop:singdim` ile $\codim\Sing(f)=8>4$ olduğundan $Z=\emptyset$ ve $f(0)=0$ için $\rk A(0)=m-1$'dir. [İSPAT]

* **`lem:normalform` (Başlangıç noktası normal formu):**
  * $A(0)=\diag(0,I_h)$ ($h=m-1$) seçilerek $A(X)=\begin{pmatrix}\ell(X)&-b(X)\\c(X)&I_h-D(X)\end{pmatrix}$ yazılır. Schur tümleyeni $\det A = \ell\det(I-D)+b\adj(I-D)c$ ve $\adj(I-D)=\bigl(\sum_{i=0}^h (-1)^i e_i(D)\bigr)\bigl(\sum_{j\ge 0}D^j\bigr)$ açılımında $\det A = f$ (homojen derece $4$) ile derece $1,2,3,4$ karşılaştırması sırasıyla $\ell=0$, $bc=0$, $bDc=0$, $bD^2c=f$ verir. [İSPAT]

* **`prop:endpoint` (Uç nokta eşitsizliği):**
  * $\Phi(y)=(b(y)^T,c(y))\in W=H^*\oplus H$, $K=\ker\Phi$, $U=\im\Phi$, $a=\dim U=16-\dim K$, $E=U^\perp/U$.
  * $T(s_1,s_2,s_3,s_4)=b(s_1)D(s_2)D(s_3)c(s_4)$ için $z\in K$ iken $z$'nin 1. veya 4. yuvada olduğu her değer sıfırdır; $\partial_y f(z)$ dört terimde de $z$'yi 1. veya 4. yuvaya koyduğundan $K\subseteq\Sing(f)$'dir. [İSPAT]
  * $bc=0$ polarizasyonu $\langle\Phi(y),\Phi(y')\rangle=0 \implies U\subseteq U^\perp$ (izotropik) verir; $bDc=0$'ın $(y,z,y')$ polarizasyonu ($z\in K$) $\langle M_z\Phi(y),\Phi(y')\rangle=0 \implies M_zU\subseteq U^\perp$ verir ($M_z=\diag(D(z)^T,D(z))$ öz-eşleniktir). [İSPAT]
  * $\operatorname{Hess}_z(f)(y,y') = \frac{1}{2}\partial_z^2\partial_y\partial_{y'}f$ açılımında $24$ sıradan yalnızca $y,y'$'nin uçlarda olduğu $4$ terim (iki kez $(y,z,z,y')$ ve iki kez $(y',z,z,y)$) kalır; yarısı $b(y)D(z)^2c(y')+b(y')D(z)^2c(y) = \langle M_z\Phi(y), M_z\Phi(y')\rangle = \langle R_z(y), R_z(y')\rangle_E$ olur ($R_z(y)=M_z\Phi(y)+U\in E$). Dolayısıyla $\rho(z)\le \dim E = 2(h-a)$, yani $m\ge 17-\dim K+\lceil\rho_K/2\rceil$. [İSPAT]

---

### Bölüm 3: Kabul Edilebilir Çekirdeklerin Sınıflandırılması ($m=14$)
* **3.1 Koordinat çekirdekleri (`prop:coordinate`, Tablo 1):**
  * $K_S\subseteq\Sing(f) \iff$ her $\sigma\in S_4$'ün $S$ ile kesişimi $\le 2$ hücredir (çünkü her $3\times 3$ subpermanentteki tekterimliler ayrı permütasyonlara karşılık gelir). [İSPAT]
  * Tablo 1'de listelenen $9$ çekirdekten her birinin $\dim K$ ve $\rho_K$ değerleri tek tek elle doğrulanabilir (iki satırda $\det B\not\equiv 0 \implies \rho=8$; $2\times 3$ blokta $B$ 4. satır/sütun dışında $0 \implies \rho=4$; tek satırda $\rho=0$; çaprazlarda $C(a)\otimes C(d)$ ile $6$ ve $4$). [İSPAT]
  * Buna karşılık $2^{16}=65{,}536$ altkümeden tam $3{,}017$'sinin testi geçtiği, bunların $G$ altında $27$ yörünge oluşturduğu ve Tablo 1 dışındaki tüm koordinat çekirdeklerin elendiği iddiası Zenodo A arşivindeki `k6_attempt/coordinate_kernels_checks.py` betiğine dayanmaktadır. **[DOĞRULANMADI]**

* **3.2 Sıfır Hessianlı çekirdekler ($k=3,4$):**
  * Bir $2\times 2$ permanent $p\neq 0$ ise tamamlayıcı $2\times 2$ indekslerdeki $4\times 4$ Hessian bloğunun determinantı $p^4\neq 0$ olduğundan $\operatorname{Hess}_z(f)\neq 0 \implies \rho(z)\ge 4$'tür. $k=3$ ($\rho_K\le 0$) ve $k=4$ ($\rho_K\le 2$) için tüm $2\times 2$ subpermanentler $K$ üzerinde özdeş sıfır olmalıdır. [İSPAT]
  * `lem:zero2` ile sıfır kümesi $4$ satır, $4$ sütun ve $36$ adet $ad+bc=0$ kuadriğinin sonlu birleşimidir; indirgenemez lineer uzay $K$ bunlardan birine düşer ve $ad+bc=0$'da azami izotropik boyut $2<3$ olduğundan $K$ tek bir koordinat satır veya sütununa düşer ($k=4$: tam satır/sütun; $k=3$: satır hiperdüzlemi). [İSPAT]

* **3.3 Torus limitleri:**
  * $X_k\subseteq \Gr(k,\C^{16})$, grafik koordinatlarında $3\times 3$ subpermanent katsayılarının ve $(2k-5)$-minör katsayılarının sıfırlanmasıyla tanımlandığından kapalıdır ($k\ge 9$ için $\dim K > \dim\Sing(f)=8$ nedeniyle $X_k=\emptyset$). [İSPAT]
  * Ağırlıkları $10(i-1)+(j-1)$ olan $1$-parametreli torus altgrubu $16$ farklı ağırlık üretir; basamaklı taban üzerinden $s\to 0$ limiti aynı boyutta bir koordinat çekirdeği $K_0\in X_k$ verir. $K_0$'ın bir komşuluğu koordinat konteyner $C$ içinde kalıyorsa, yörünge haritasının sürekliliği $\lambda(s_0)\cdot K\subseteq C$ ($s_0\neq 0$) ve $(\C^*)^8$-değişmezlik üzerinden $K\subseteq C$ verir. [İSPAT]
  * ($K_0$'ın Tablo 1'deki $9$ tipten biri olması `prop:coordinate`'in tamlık adımına bağlıdır. **[DOĞRULANMADI]**)

* **3.4 Yerel kapsama (`sec:charts`, Tablo 2, `prop:containers`):**
  * İki satır veya tam çapraz konteynerinde ilgili Hessian satırlarının özdeş sıfırlanması, $(r+1)$-minör türevinin Schur formülü \eqref{eq:chartminor} ve $F(p,0)=0$ iken $F(p,q)=A(p,q)q$ yazılarak $\det\frac{\partial F}{\partial q}(0,0)\neq 0$ komşuluğunda $q=0$ çıkarılması tamamen sağlamdır. [İSPAT]
  * Ancak Tablo 2'deki dört koordinat limitinin ($2\times 3$ eksi bir hücre, satır ve iki hücre, iki kollu çapraz, $K_6$) Jacobien ranklarının ($40, 48, 45, 54$) ve sıfırdan farklı minörlerinin ($-64, 16, -26880, -128$) hesaplanması `k6_attempt/chart_jacobian_certificate.json` sertifikasına dayanır. **[DOĞRULANMADI]**
  * Tam $2\times 3$ bloğu içeren diğer üç limit (tam $2\times 3$, iki satır eksi hücre, iki satır) için grafikteki dış satır denklemi $w_1(u_2v_3+u_3v_2)+w_2(u_1v_3+u_3v_1)+w_3(u_1v_2+u_2v_1)=0$, $(2,1)$ ve $(1,2)$ bi-derecelerine ayrıldığında $\alpha_{22}+\alpha_{33}=\alpha_{11}+\alpha_{33}=\alpha_{11}+\alpha_{22}=0$ ile tüm $\alpha,\beta=0$, ek $s$ değişkenleri de üç kuadriğin lineer bağımsızlığıyla $0$ çıkar; ardından $\partial_{43}f=0$'dan $w_4(u_1v_2+u_2v_1)=0 \implies w_4=0$ elde edilerek dış satırların sıfırlanması grafik üzerinde bütünüyle elle kanıtlanır. [İSPAT] (`grassmann_chart_checks.py` betiğinin raporladığı $24,28,32$ matris rankı sayıları betik çıktısı olarak **[DOĞRULANMADI]**.)
  * Sonuç olarak `prop:containers`, Tablo 2 sertifikasına bağımlılığı nedeniyle bütünsel olarak **[DOĞRULANMADI]** etiketi taşır.

* **3.5–3.7 İki satır içi, çapraz içi ve sınıflandırma (`thm:kernellist`):**
  * İki satırda Hessian bloğu $\begin{pmatrix}0&B(u,v)\\B(u,v)^T&0\end{pmatrix}$ olup kabul edilebilirlik $r\le k-3$'tür. Sabit $v\neq 0$ için $B$'nin $u$'da jenerik rankı $\ge 3$ ($2v_i^3\prod_{j\neq i}u_j\neq 0$) ve $\Delta\equiv 0 \iff |\supp(v)|\le 2$'dir. $k=5$: $u$-izdüşümü tam destek içerirse lifler `lem:tenranktwo`'daki $10$ doğrudan birine düşer, $K=\C^4\oplus V_0$ ile çelişki; içermezse bir koordinat hiperdüzleminde $2v_4^3u_1u_2u_3=0 \implies v_4=0$, yani $2\times 3$ blok hiperdüzlemidir. $k=6$: tam destek varsa `lem:crossdet` ile quartic hiperyüzey lineer/afin $3$-düzlem veya $0$ dışı $2$-düzlem içermediğinden $K=\C^4\oplus V_0$ ve $|\supp(v)|\le 2$ (satır ve iki hücre); yoksa eksik koordinatlar çakışmazsa $(1,1,1,0),(1,1,0,1)$ noktasında $\det B = -4\neq 0$ (elle doğrulandı) olduğundan tam $2\times 3$ bloğudur. $k=7,8$: $\Delta$ indirgenemez olduğundan rank $4\le k-3$'tür. [İSPAT]
  * Çapraz içinde $3\times 3$ Hessian $C(a)\otimes C(d)$ olup $\rk C(w)\in\{0,2,3\}$'tür; $k=7 \implies \rho=9>8$; $k=6 \implies \rho\le 6$ ile bir kol koordinat eksiltir ($K_6$); $k=5 \implies \rho\le 4$ ile her iki kol koordinat eksiltir (iki kollu çapraz). [İSPAT]
  * `thm:kernellist` bileşen sayıları ($8\PP^3, 8, 48\PP^5+144, 288, 12\PP^7, 12$) ve ayrık konteynerlerin arakesit boyutlarının $k$'dan küçük olması elle doğrulanır [İSPAT]; ancak listenin tüm $X_k$'yı tükettiği sonucu `prop:coordinate` ve `prop:containers` üzerinden Tablo 1–2 bağımlılığı taşır. **[DOĞRULANMADI]**

---

## 2. `dc_perm4_ge_10.tex` ile Sheshadri Zincirinin Satır Satır Karşılaştırması

1. **$\codim\Sing(\per_4)=8$ Adımı:** Sheshadri (`prop:singdim`) bunu `lem:zero2` ($\dim\Sing(\per_3)=3$) ve `lem:singF` ($\dim\Sing(F)=4$) yardımıyla destek boyutuna göre tamamen elle kanıtlar [İSPAT]. `dc_perm4_ge_10` (`thm:sing1`) ise alt sınırı iki sıfır satırla verir, üst sınır $\codim\ge 8$'i $L_8$ üzerinde modüler IMSC/Macaulay rank sertifikasıyla kurar (bu oturumda yerelde tekrar koşulmadığından **[DOĞRULANMADI]**).
2. **Korank $1$ Koşulu (`lem:regularity` vs `prop:corank1`):** Sheshadri (ABV Prop. 2.1 ile birebir aynı olarak) $\codim\Sing(\det_m)=4 < 8$ üzerinden **tüm $V(\per_4)$ sıfır kümesinde** $\rk A(p)=m-1$ kanıtlar [İSPAT]. `dc_perm4_ge_10` yalnızca **orijinde** $\corank(A_0)=1$'i ($r=0,\ge 5,4,3,2$) durum analiziyle, `lem:strength` ($\str(\per_4)=4$), Atkinson/Eisenbud–Harris ($r=3$) ve UFD/$\gcd$ ($r=2$) kullanarak eler [İSPAT]. Sheshadri'nin global düzenliliği daha güçlüdür (sonradan $K$ üzerinde $D(z)$ nilpotentliğini verir).
3. **Normal Form ve Schur Açılımı (`lem:normalform` vs `eq:blockM`–`eq:t4`):** İki zincir birebir ortaktır: $A(0)=\diag(0,I_h)$ konjugasyonu ve Schur açılımı derece $1,2,3,4$'te sırasıyla $\ell=0$ ($b=0$), $bc=0$ ($v^T u=0$), $bDc=0$ ($v^T A u=0$) ve $bD^2c=\per_4$ ($-v^T A^2 u=\perm_4$) özdeşliklerini verir [İSPAT].
4. **Orijin-İzotropi (`prop:endpoint` vs Adım 1):** İki zincir birebir ortaktır: $bc=0$ polarizasyonu $\langle(\beta,\gamma),(\beta',\gamma')\rangle=\beta\gamma'+\beta'\gamma$ formuna göre $U=\im\Phi$ (veya $S$) altuzayını tamamen izotropik yaparak $a\le h$ ($m=9$'da $D\le 8$) verir; $\per_4\in I_K^2$ olması $K\subseteq\Sing(\per_4)$ ve $8\le a$ zorlar (bu tek başına ABV'nin $m\ge 9$ sınırını verir) [İSPAT].
5. **$m=9$ Elemesi (Hessian + `lem:zero2` vs Skew-Square + `prop:sing2`):** Gerçek farklılık buradadır. Sheshadri genel $m$ için $E=U^\perp/U$ üzerinde $\operatorname{Hess}_z(f)(y,y')=\langle R_z(y),R_z(y')\rangle_E$ kurup $\rho_K\le 2(h-a)$ eşitsizliğini çıkarır (`prop:endpoint`); $m=9, \dim K=8$'de $\rho_K=0$ olması tüm $2\times 2$ subpermanentleri $K$ üzerinde sıfırlar (Bölüm 3.2) ve $K\subseteq\Sing_2$ üzerinden `lem:zero2`'nin $\dim 4<8$ sınırı ile çelişir [İSPAT]. `dc_perm4_ge_10` ise $E$ ve Hessian'ı kullanmaz; $a=h=8$'de $v=(y,0)^T, u=(Ky,z)^T$ ($K^T=-K$) blok formunda $[t^3]=0$'dan $A_{13}^{(\xi)}=0$ ve $(A_{11}^{(\xi)}K)^T=-A_{11}^{(\xi)}K$ çıkarır, Skew-Square Lemması (`lem:skewsquare`) ile $\perm_4\in I_W^3$, yani $W^\perp\subseteq\Sing_2(\per_4)$ gösterir [İSPAT]. Cebirsel olarak $m=9$'da $U^\perp=U$ olduğundan $M_z U\subseteq U$ ve $M_z^2 U\subseteq U$ koşulları tam olarak $A_{11}^{(\xi)}K$ ve $A_{11}^{(\xi)2}K$ ters-simetrisine denk düşer [İSPAT].
6. **$\Sing_2$ Boyutu (`lem:zero2` vs `prop:sing2`):** İkisi de aynı $\dim\Sing_2(\per_4)=4$ ($\codim=12$) olgusunu elle kanıtlar; Sheshadri genel matrislerde satır desteğiyle, `dc_perm4_ge_10` $4\times 4$'te iki parçalı destek grafı $K_{a,b}$ ile ilerler [İSPAT].

### Sınırlı rank uzayları / temsil
## 1) Sheshadri (2611.06658) Adımlarının Yeniden Türetimi ve Denetimi

- **lem:regularity:** $\mathcal{D}=\{\mathrm{rk}\le m-2\}$ kodim $4$ ve $Z=A^{-1}(\mathcal{D})\subseteq\mathrm{Sing}(f)$ için $\mathrm{codim}\,Z\le 4$ türetilir [İSPAT]. $Z=\emptyset$ sonucu kesitte olmayan `prop:singdim` ($\mathrm{codim}\,\mathrm{Sing}(f)=8$) atfına dayandığından [DOĞRULANMADI].
- **lem:normalform:** $A(0)=\mathrm{diag}(0,I_h)$ kabulüyle $\mathrm{adj}(I-D)=\det(I-D)\sum_{j\ge 0}D^j$ açılımından derece $1$–$4$ eşitlikleri $\ell=0$, $bc=0$, $bDc=0$, $bD^2c=f$ çıkar [İSPAT].
- **prop:endpoint:** $T,R$ polarizasyonu $K\subseteq\mathrm{Sing}(f)$, $U\subseteq U^\perp$, $M_z U\subseteq U^\perp$ ve $\mathrm{Hess}_z(f)(y,y')=\langle R_z(y),R_z(y')\rangle_E$ özdeşliğini kurarak $\rho_K\le 2(h-a)$ sınırını verir [İSPAT].
- **sec:moments:** `lem:regularity` kabulü altında $\det(I-D(z))=1$ ($z\in K$) ve $D(z)$ nilpotentliği türetilir (`lem:regularity` bağımlılığı nedeniyle başlangıç [DOĞRULANMADI], çıkarım [İSPAT]). `lem:cubicresolvent`'te $\mathrm{Hess}_z=0\implies bRc=0$, $bRD(y)Rc=tP(y)$ ve $b(y)R=b((I-tS)^{-1}y)$ ile $S$ nilpotentliği, $P=-bD(Sy)c$ ve $\delta_S P=0$ türetilir [İSPAT].
- **Bölüm 4:** `lem:fullstab`, `lem:threestab` ve `sec:relativeC` matris/katsayı kanıtları elle çıkar [İSPAT]; `sec:insidetworows` atfı ve `archive A` rank kontrolleri [DOĞRULANMADI]. `sec:rowthree`'de $S_z(Y,t)=\ell_z e_t$ türetimi [İSPAT], çelişki için kullanılan `lem:cubicirreducible` kesitte olmadığından [DOĞRULANMADI]. `sec:syzygies`'de $\deg 1$ syzygy ($\ell_i=0$) elle çıkar [İSPAT], fakat $\deg 2$ (`rk T_2 = 60`, $q=JP$) `archive A` sertifikasına dayanır [DOĞRULANMADI]; buradan `lem:nolinearminor` ve `sec:block2x3` türetilir [İSPAT]. `sec:block2x3hyp` dış `lem:zero2` kullanır [DOĞRULANMADI]. `sec:arms2`, `sec:row2cells` ve `sec:K6` ($E_s=\mathrm{diag}(-G,-G^T)$, $G=0$) cebirsel adımları [İSPAT], `sec:K6` sonundaki `lem:cubicirreducible` atfı [DOĞRULANMADI].
- **Bölüm 5:** `thm:fivechannels`'da $\mathcal{S}$ düzleştirmesi ($\dim 6$), `eq:Sintersection`, `eq:fourplusone` ve pure rank $\ge 2$ adımları çıkar [İSPAT]; $p+q=4$ elemesi ve $10$-doğru adımları kesitte olmayan `lem:crossdet` ve `lem:tenranktwo`'ya dayanır [DOĞRULANMADI]. `sec:clifford` ($\mathrm{tr}(T_F T_G)=\det(F^T J G)$, $\mathrm{rk}\,T_F=1$, $\dim L\le 5$) adımları [İSPAT], $\det B$ indirgenemezliği dış `lem:crossdet` nedeniyle [DOĞRULANMADI]. `sec:K7`, `sec:spinorcontent` ve `sec:coordK7` ($u_4=0$) tamdır [İSPAT]; `sec:hyperplanefactors` dış `sec:targetfacts` ve `eq:boundarydelta` kullanır [DOĞRULANMADI].

## 2) Karşılaştırma

1. **`dc_perm4_ge_10.tex` ($r=0,2,3,4,\ge 5$) vs `lem:regularity`:** $\mathrm{codim}\,\mathrm{Sing}=8$ ($\mathrm{str}(\mathrm{perm}_4)=4$) altında `prop:corank1` yalnızca $X=0$'da $r\ge 2$'yi eler ($r=4$'te $\Sigma_2$ kodim $4$, $r=3$'te Atkinson/EH, $r=2$'de UFD) [İSPAT]. Sheshadri `lem:regularity` ise $\mathrm{codim}\,\mathrm{Sing}=8$'i tüm $V(\mathrm{perm}_4)$'e uygulayıp $K$ üzerinde nilpotentlik elde eder [DOĞRULANMADI]. İki kanıt da dış/IMSC $\mathrm{codim}\,\mathrm{Sing}(\mathrm{perm}_4)=8$ sertifikasına dayanır (`thm:sing1` mod $p_1,p_2$ burada çalıştırılmadı) [DOĞRULANMADI].
2. **`REPORT.md` §§1–3 vs `prop:endpoint` + `thm:fivechannels`:** Sheshadri `prop:endpoint` ile $E=U^\perp/U$'da $A^T J C=B$ kurup `sec:clifford` ile $4\times 5\cdot 5\times 4$ `thm:fivechannels` problemine indirger (dış `lem:crossdet` hariç) [İSPAT]. `REPORT` ise $K(B,V)\Sigma=B\otimes V^T$ (`Theorem 1`) ile doğrudan $(3,2)$ tensör rankı $\ge 4$ (`Theorem 3`) ve $k_{\min}=2$'de $B_1 B_2=0\implies C B_2=0$ ayar çöküşünü (`Theorem 4`) kanıtlar [İSPAT]. İki yol da aynı `4 star + 6 edge` sınıflandırmasına ulaşır (`REPORT` `Lemma 3.2`) [İSPAT]; fark olarak Sheshadri tüm $m=14$ çekirdeklerini, `REPORT` §§1–3 yalnızca $w=5$ iki-satır orta bloğunu kapsar [İSPAT].

### Sınır karmaşıklığı uzmanı
# Sheshadri (`per4_dc_15.tex`, Bölüm 6: `sec:fullrow`) Denetimi

> **Yöntem Notu:** Bu turda araç kullanımı yasak olduğundan hiçbir Python/CAS doğrulaması yapılmamıştır (`[KESİN HESAP]` yoktur). Yalnızca verilen `per4_dc_15.tex` (satır 1166–1686) birincil metni üzerinde adım adım elle türetilen adımlar `[İSPAT]`, önceki bölümlere/eklere, Zenodo Archive B sertifikalarına veya verilmeyen `dc_perm4_ge_10.tex` dosyasına dayanan adımlar ise `[DOĞRULANMADI]` olarak etiketlenmiştir.

---

## 1) `sec:invariant13` ve `sec:universalcorrection` Elle Yeniden Türetimi

### `sec:invariant13` ($V = U \oplus \mathbb{C}e$ değişmezliği, $S(z)^{13}=0$, H0–H2)
* **Temel kurulum bağımlılıkları:** `per4_dc_15.tex` Bölüm 1–5 metni bu alıntıda yer almadığından; $W$ ($\dim W=26$), $U$ ($\dim U=12$), $E=U^\perp/U$ ($\dim E=2$) uzaylarının tanımları, $M_z$'nin öz-eşlenikliği ve nilpotentliği, Hessian'ın sıfırlanmasının $\operatorname{im}(R_z)\subseteq E$'yi izotropik kılması, `\eqref{eq:allmoments}`, `lem:cubicresolvent` ve `lem:fullstab` doğrudan alıntıdan doğrulanamamaktadır `[DOĞRULANMADI]`.
* **İki izotropik doğru ve indirgenemezlik:** $\mathbb{C}$ üzerinde dejenere olmayan $2$ boyutlu simetrik bilineer uzay $E$'de tam olarak iki izotropik doğru ($L_1, L_2$) vardır; $z \mapsto R_z$ polinom ailesinin imgesinin bu iki kapalı altkümeden birinde kalması parametre uzayının indirgenemezliği gereği ya her $z$ için $R_z=0$ ya da sabit bir $L \subset E$ için $\operatorname{im}(R_z)\subseteq L$ olmasını zorlar `[İSPAT]`.
* **$R_z \equiv 0$ durumunun elenmesi:** Doğrudan `lem:cubicresolvent` ve `lem:fullstab`'a dayanır `[DOĞRULANMADI]`.
* **$V = U \oplus \mathbb{C}e$ değişmezliği ve $S(z)^{13}=0$:** $L$'nin bir kaldırması $e \in U^\perp$ ile $V=U\oplus\mathbb{C}e$ maksimal izotropik ($13 = 26/2$) altuzaydır ve $M_z U \subseteq V$ sağlar `[İSPAT]`. Öz-eşleniklikle $u \in U$ için $\langle M_z e, u\rangle = \langle e, M_z u\rangle = 0$ (ikisi de izotropik $V$'de), dolayısıyla $M_z e \in U^\perp$ elde edilir `[İSPAT]`. Soysal $z$'de $M_z u = u_0 + \alpha e$ ($\alpha \ne 0$) için $M_z^2 u = M_z u_0 + \alpha M_z e$ açıldığında $\langle u_0, M_z u_0\rangle = \langle e, M_z u_0\rangle = 0$ ($V$ izotropik) ve $\langle u_0, M_z e\rangle = 0$ ($M_z e \in U^\perp$) olup $\langle M_z u, M_z^2 u\rangle = \alpha^2\langle e, M_z e\rangle$ kalır `[İSPAT]`. Bunun $\langle u, M_z^3 u\rangle = 0$ eşitliğine bağlanması `\eqref{eq:allmoments}` alıntısına dayanır `[DOĞRULANMADI]`; bu eşitlik kabul edildiğinde $\alpha \ne 0$ ($\operatorname{char}\mathbb{C}=0$) nedeniyle $\langle e, M_z e\rangle = 0$ çıkar ve $2$ boyutlu $E$'de $L^\perp = L$ olduğundan $M_z e \in V$ yoğun açık kümede, dolayısıyla polinomlukla her $z$ için sağlanır `[İSPAT]`. $S(z):=M_z|_V$'nin $S(z)^{13}=0$ sağlaması $M_z$'nin nilpotentliğine (`[DOĞRULANMADI]`) ve $\dim V=13$'te Cayley–Hamilton'a dayanır `[İSPAT]`.
* **\eqref{eq:fullresolvent} ve (H0)–(H2) denklemleri:** $b(Y) R D_Y R c(Y) = F_z(Y)$ özdeşliğinin $W$'de \eqref{eq:fullresolvent}'teki $\frac12 ((I-S(z))^{-1}y)^T C_Y ((I-S(z))^{-1}y)$ formuna eşitlenmesi Bölüm 1–5 tanımına bağlıdır `[DOĞRULANMADI]`. Ancak \eqref{eq:fullresolvent} ve $F_{tz}(Y)=t F_z(Y)$ verildikten sonra $(I-t S(z))^{-1}y = y + t S(z)y + t^2 S(z)^2 y + O(t^3)$ açılımında $C_Y^T = C_Y$ simetrisiyle $t^0, t^1, t^2$ katsayılarının eşitlenmesi tam olarak \eqref{eq:H0}, \eqref{eq:H1} ve \eqref{eq:H2}'yi verir `[İSPAT]`.

### `sec:universalcorrection` ($\delta_A F_z \in (\ell)$ özdeşliği)
* **Genişletme ve $v^T C_v v = 0$:** $v=(Y,t)$ ve $C_e = \begin{pmatrix} -(M+M^T) & -g/2 \\ -g^T/2 & 0 \end{pmatrix}$ ile $v^T C_v v = Y^T Q_Y Y + 2t Y^T M Y + t^2 g^T Y + t(-Y^T(M+M^T)Y - t g^T Y) = 0$ (\eqref{eq:H0} ve $Y^T M^T Y = Y^T M Y$ kullanılarak) özdeş olarak sıfırdır `[İSPAT]`.
* **Polarizasyon ve $\delta_S G(v)$:** $v^T C_v v = 0$'ın $w$ yönünde türevi $v^T C_w v + 2 w^T C_v v = 0$ verir; $w=Sv$ için $G(v) := -\frac12 v^T C_{Sv} v = v^T C_v S v$ ve $G|_U = F_z$ elde edilir `[İSPAT]`. $G(v+s Sv)$ açılımında $s^1$ katsayısı $\delta_S G(v) = -\frac12(2(Sv)^T C_{Sv} v + v^T C_{S^2 v} v)$ olur; $v^T C_v v=0$'ın $v+s Sv$ açılımındaki $s^2$ katsayısı $2(Sv)^T C_{Sv} v = -(Sv)^T C_v (Sv)$ ve $w=S^2 v$ polarizasyonu $v^T C_{S^2 v} v = -2 v^T C_v S^2 v$ verir `[İSPAT]`. Yerine koyunca $\delta_S G(v) = v^T C_v S^2 v + \frac12 (Sv)^T C_v (Sv)$ çıkar; $v=(Y,0)$ noktasında \eqref{eq:H2} bunu sıfırlar ve $\delta_S G(Y,0) = \delta_A F_z(Y) + \ell(Y)\partial_t G(Y,0)$ olduğundan $\delta_A F_z \in (\ell)$ (\eqref{eq:quotientcondition}) kanıtlanır `[İSPAT]`.
* **Blok özdeşliği \eqref{eq:blockcorrection}:** $(Y+sAY)^T Q_{Y+sAY}(Y+sAY)=0$'ın $s^2$ katsayısı $Y^T Q_{AY} AY + (AY)^T Q_Y (AY) = \frac12 (AY)^T Q_Y (AY)$ verir; bunu $\delta_A H_1$ açılımına koyup $H_2 = Y^T Q_Y A^2 Y + \frac12 (AY)^T Q_Y (AY) + \ell(AY) q_Y^T Y + \ell(Y)(Y^T Q_Y d + \sigma q_Y^T Y + q_Y^T AY + \frac12 c_Y \ell(Y))$ çıkarıldığında tüm $Y^T Q_Y A^2 Y$, $\frac12(AY)^T Q_Y (AY)$, $\ell(AY)q_Y^T Y$ ve $\ell(Y)q_Y^T AY$ terimleri sadeleşir ve \eqref{eq:blockcorrection} birebir tüm işaretleriyle elde edilir `[İSPAT]`.

---

## 2) Bölüm 6 Alt Bölümlerinin ve Sınır Karmaşıklığı İtirafının Denetimi

| Alt Bölüm / İddia | Kendi Başına Türetilenler (`[İSPAT]`) | Dış Bağımlılıklar / Eksikler (`[DOĞRULANMADI]`) |
| :--- | :--- | :--- |
| **`sec:quotienttheorem`** | $\det B_1(a) = -4(e_1 e_3 - 4 e_4)$'ün $\mathbb{C}$'de indirgenemez kuartik olduğu; $\Psi_{aa}=\Psi_{bb}=\Psi_{cc}=0$ elemesi; $A_{c\leftarrow a}=v_c\alpha$ ve iki/üç satırda $\Psi=\partial_v F$ belirlenmesi; tek satır durumunda \eqref{eq:onerowform} biçimi `[İSPAT]`. | $F_z$'nin $F(a,b,c)$'ye indirgenmesi ve \eqref{eq:multirowform}'un son adımında $A-v\ell$'nin satırlarda skaler kalması `lem:fullstab`'ı kullanır `[DOĞRULANMADI]`. |
| **`sec:invariantrows` & `sec:commonfamily`** | $\ge 2$ satırlı $\ell$'de $s_a=s_b=s_c=0$ ve $F$'nin indirgenemezliğiyle çelişki; sabit tek satır desteği ve $Q,R$ nilpotentliği; `sec:commonfamily`'de $r_j(z)=z_j l_j(z)$ bölünebilirliğiyle 15 noktanın ve koordinat olmayan yıldız noktalarının elenmesi `[İSPAT]`. | $\ell=0$ durumu ve sütun ölçeklemesi (`a_j = z_j \tilde a_j`) `lem:fullstab`'a dayanır `[DOĞRULANMADI]`. |
| **`sec:tenlines`** | $(K_0)_{ji}=r_i(\zeta_i/2-Z_{ij})$ ve $(K_0)_{qq}$ formülleri; $M(p,q,r)$'nin 0. satırının doğrulanması; $g_1=g_2=g_3=h_1=h_2=0$ polinom sisteminden 10 doğru + 3 eksenin ve $h_1,h_2$ ile eksenlerin elenmesinin çözülmesi `[İSPAT]`. | 24 denklemden seçilen 9 satırın tam germe özelliğinin tüm satırlarca kontrolü; \eqref{eq:squarecert} ($g_i^2, h_j^2 \in (D_0,\dots,D_{83})$) ve 84 minörün 10 doğru üzerinde sıfırlanması (840 tek değişkenli özdeşlik) `Appendix~\ref{sec:polynomialappendix}` (metinde yok) ve Archive B `root_ten_line_certificate.json`'a dayanır `[DOĞRULANMADI]`. |
| **`sec:normalizer`** | Tüm 4 sıfır-koordinat durumu ($0,1,2,3$ sıfır): $L_1, L_2$ formları, $d_1=2(p-1), d_2=2(q-1), d_3=1-p-q+4pq-4p^2$, $4(p^2-q^2)=0$, $4(p^2-1)=0$, $\pm 4(p^2-1)(2p\pm 1)=0$, $4(p-1)(s-t)=0$ ve $4(p^2-1)s=0$ ile 15 nokta + 10 doğru sınıflandırmasının tamamı elle doğrulandı `[İSPAT]`. | Yok (tamamı kapalı elle ispat). |
| **`sec:fourkernels`** | Dört kovaryant tipin hepsinde verilen 16 ve 15 boyutlu ailelerin $\delta_A F \in (\ell)$ çözüm uzayına **dahil olduğu** (`P_0, P_1, w e_1^T, Q_0, R_0, K_0$ matris çarpımlarıyla) elle kanıtlandı `[İSPAT]`. | Bu ailelerin **tüm** çözüm uzayı olduğu (128$\times$128 ve 129$\times$129 tam sayı minörlerinin sıfırdan farklılığı) metinde olmayan `Appendix~\ref{sec:minorappendix}` ve Archive B `system_exceptional_killer_certificate.json`'a dayanır `[DOĞRULANMADI]`. |
| **`sec:terminal` & `sec:unitidentities`** | `sec:fourkernels` tamlığı varsayımı altında özdeğer/nilpotentlik çelişkileri ($-2,-4,1$, çarpanlaşma); `sec:unitidentities`'deki iz denklemleri, $e_2(Q), e_2(R)$, tanık değerlemeleri ve dört birim özdeşliğinin (`1 = ...`) cebirsel açılımı elle kanıtlandı `[İSPAT]`. | Archive B `zero_unit_checks.py` betiğinin çalışması `[DOĞRULANMADI]`; koşulsuz olarak `Teorem~\ref{thm:fullrowsystem}` önceki Archive B minör adımlarına bağımlı kalır `[DOĞRULANMADI]`. |

* **Sınır karmaşıklığı (satır 1685) denetimi:** Makale, kanıtın $\underline{\mathrm{dc}}$ (border determinantal complexity) hakkında hiçbir şey söylemediğini açıkça kabul eder. Gerçekten de Bölüm 6'nın mekanizması şu noktalarda sınır karmaşıklığına taşınamaz: (i) kanıt $\det(I - D_z) = 1$, $M_z$ nilpotent ve $S(z)^{13} = 0$ gibi **tam** özdeşliklere dayanır, oysa $\varepsilon$-degenerasyonlarda ($\det = \varepsilon^k \mathrm{perm}_4 + O(\varepsilon^{k+1})$) alt derece terimleri bu nilpotentliği bozabilir; (ii) `sec:tenlines` ve `sec:fourkernels` rank düşüşlerini tam Zariski-kapalı yerlerde kullanır, sınırda bu yerlere $\varepsilon \to 0$ ile yaklaşılabilir; (iii) `sec:unitidentities` yalnızca kesin sistemin Hilbert Nullstellensatz tutarsızlığını ($1 = \dots$) verir, $\varepsilon$-değerlemesi için alt sınır üretmez; ayrıca `sec:unitidentities` ve `sec:terminal` $\operatorname{char} \ne 2, 3$ bölünmelerini (ör. $4, 24, 32, 96$, $3$'e bölme) kullanır `[İSPAT]`.

---

## 3) `dc_perm4_ge_10.tex` Skew-Square ($m=9$) ile Kıyaslama

> **Kısıt Bildirimi:** `dc_perm4_ge_10.tex` metni bu turda verilmediğinden ve dosya okuma aracı yasak olduğundan `dc_perm4_ge_10.tex` içindeki "Skew-Square ($m=9$)" ve "$S(z)^2$-düzeyi" argümanlarının tam yapısı doğrulanamamıştır `[DOĞRULANMADI]`. Aşağıdaki kıyaslama yalnızca Sheshadri Bölüm 6'daki boyut parametrelerine ve genel lineer cebire dayanır.

Sheshadri Bölüm 6'da tam satır (full row) çekirdeğinde $E=2$ durumunun ortaya çıkmasının aritmetik nedeni doğrudan temsil boyutu $m=14$ ile alt 3 satırın değişken sayısı $a=12$ arasındaki ilişkidir:
1. **Boyut ve $\dim E$ dengesi:** Sheshadri'de $m=14$ boyutlu bir temsilde $W$ uzayının boyutu $2(m-1) = 26$, alt 3 satırın görüntüsü $U \subset W$ ise $a = 12$ boyutlu izotropik bir altuzaydır (`sec:fullrow`). Dejenere olmayan $26$ boyutlu bir uzayda $12$ boyutlu izotropik $U$'nun ortogonal tümleyeni $\dim U^\perp = 26 - 12 = 14$ olur ve bölüm uzayı $E = U^\perp / U$ tam $\dim E = 2(m-1) - 2a = 26 - 24 = 2$ boyutuna sahip olur `[İSPAT]`.
2. **Neden $m=9$'da bu $E=2$ tam-satır rejimi oluşamaz:** $\mathrm{perm}_4$ için bir tam satır çekirdeğinin geri kalan üç satırı yine $a = 12$ değişken içerir. Buna karşılık $m=9$ boyutlu bir temsilde (aynı $W$ geometrisiyle $2(m-1) = 16$ boyutlu simetrik/izotropik ortam varsayılırsa `[SANI]`), maksimal izotropik altuzay boyutu en fazla $m-1 = 8 < 12 = a$'dır `[İSPAT]`. Yani $a=12$ alt satır değişkeni $9\times 9$ boyutunda bir temsilde enjekte biçimde $12$ boyutlu bir izotropik $U$ uzayı oluşturamaz; $U$'nun boyutu baştan $m-1=8$ ile sınırlıdır ve $12$ değişken üzerinde zorunlu çekirdek/rank düşüşü veya doğrudan düşük mertebeli $S(z)^2$ tipi moment kısıtları ortaya çıkar `[SANI]`.
3. **Neden Sheshadri $m=14$'te $S(z)^{13}=0$'a ve tüm $E=2$ analizine inmek zorunda kaldı:** $m=14$ olduğunda $m-1 = 13 > 12 = a$ eşitsizliği ilk kez $a=12$'lik tüm alt-satır uzayının izotropik bir $U$ olarak gömülmesine ve $E = U^\perp / U$'nun pozitif boyutlu ($\dim E = 2$) kalmasına izin verir; bu durumda $U$ artık $M_z$ altında değişmez olmak zorunda değildir, $\dim V = 13$'e çıkılır, $S(z)^2$-düzeyindeki \eqref{eq:H0}–\eqref{eq:H2} tek başına $A$ üzerinde sadece $\delta_A F_z \in (\ell)$ bölüm koşulunu verir ve geriye kalan $4$ istisnai $\ell$ ailesini öldürmek için $Q,R$ üzerinde tüm nilpotentlik ($S(z)^{13}=0$ / özdeğer sıfırlanması) kullanılmak zorunda kalınır `[İSPAT]`. (`dc_perm4_ge_10.tex`'in $m=9$'da tam olarak nasıl $S(z)^2$-düzeyinde durduğu bu oturumda metin dışı olduğu için `[DOĞRULANMADI]`.)

### Hesaplamalı cebir
### 1. Yerel `CHECK 1` Çıktısının Doğruladığı Bulgular
- `prop:singdim` tanığı $O$ için $O\cdot C(1,1,1)\cdot O^T = \operatorname{diag}(10,-90,-18)$, $\det(O)=-90$ ve $\operatorname{perm}_3(O)=-24$ özdeşlikleri doğrulanmıştır; ancak $O$ matrisinin girdileri özet çıktıda basılmamıştır `[KESİN HESAP]`.
- `sec:insidetworows` determinantları $\det B(1,(1,1,1,0))=-12$, $\det B(1,1)=-48$ ve $\det B((1,1,1,0),(1,1,0,1))=-4$ olarak doğrulanmıştır `[KESİN HESAP]`.
- $2^{16}=65{,}536$ hücre altkümesi taranarak her $4\times 4$ permütasyonla en fazla $2$ hücrede kesişen tam $3{,}017$ tekil altküme ve $|G|=1152$ grubu altında $27$ yörünge bulunmuştur `[KESİN HESAP]`.
- $\mathbb{Q}(x_S)$ üzerinde tam Hessian rankı $\rho_K$ ile Tablo 1 (`tab:coordinate`) birebir doğrulanmıştır: $9$ kabul edilebilir çekirdeğin $(\dim K,\rho_K,\text{bound})$ değerleri $(8,8,13),(6,4,13),(4,0,13),(7,8,14),(6,6,14),(6,6,14),(5,4,14),(5,4,14),(3,0,14)$ ve yörünge boyutları $\{12,48,8,96,144,96,288,144,32\}$ olarak elde edilmiştir (çıktıda yalnızca $9$. satırın hücre listesi kısaltmalı basılmıştır) `[KESİN HESAP]`.

### 2. Yerel Olarak Çalıştırılmayan Bileşenler
- Tablo 2 (`tab:charts`) içindeki 4 Jacobian rankı (`40, 48, 45, 54`), normalleştirilmiş minorlar (`-64, 16, -26880, -128`), seçilen minor indeksleri (`chart_jacobian_certificate.json`) ve `chart_jacobian_checks.py` yerel olarak çalıştırılmamıştır `[DOĞRULANMADI]`.
- `grassmann_chart_checks.py` tarafından yeniden hesaplandığı belirtilen katsayı haritası rankları (`24, 28, 32`) yerel olarak çalıştırılmamıştır `[DOĞRULANMADI]`.
- Zenodo `24124959` arşivlerindeki `tab:programsA` (15 betik) ve `tab:programsB` (13 betik) olmak üzere toplam **28 betiğin hiçbiri** (`RUN_ALL_CHECKS.py`, `RUN_CHECKS.py`, `VERIFY_MANIFEST.py` dâhil) yerel olarak çalıştırılmamıştır; yalnızca `coordinate_kernels_checks.py` kapsamındaki koordinat çekirdeği sayımı/Hessian rankı yerel `CHECK 1` ile bağımsız yeniden üretilmiştir `[DOĞRULANMADI]`.

### 3. `verify_independent_exact.py` ile Sheshadri Sertifika Mimarisi Karşılaştırması
- **Mimari ve doğrulanan kapsam:** `verify_independent_exact.py`, sıfır `float64`, sıfır BLAS ve sıfır IMSC ile doğrudan `uint64_t` CSR C Macaulay çözücüsü kullanır: `perm_4` için $L_8$ üzerinde $M_6\dots M_9$ korankları `[132,32,8,0]` ($D=9$'da $11{,}440/11{,}440$ tam rank; mod $32{,}749$ ve $65{,}521$), $L_9$'da $M_6,M_7$ korankları `[753,580]` (mod $32{,}749$), ayrıca `perm_3` ($L_6: 126/126$, $L_7: 438/462$) ve `det_4` ($L_4: 84/84$, $L_5: 190/210$) pozitif kontrolleri SymPy Gröbner ($\mathbb{F}_{32749}$) ile doğrulanmıştır `[KESİN HESAP]`. Sheshadri ise 28 bağımsız Python+SymPy betiğine dağılan vaka-bazlı bir doğrulama mimarisi kullanır `[DOĞRULANMADI]`.
- **Sonlu cisim $\to \mathbb{Q}$ geçişi:** Tamsayı katsayılı bir matris mod $p$ tam sütun rankına sahipse, $\det \not\equiv 0 \pmod p$ olan bir maksimal minoru vardır; dolayısıyla aynı minor $\mathbb{Z}\subset\mathbb{Q}$ üzerinde de sıfırdan farklıdır ve $\mathbb{Q}$ üzerinde tam rank kesindir `[İSPAT]`. Tam rank olmayan derecelerde ($M_6,M_7,M_8$ gibi) mod $p$ korankı, $p$'nin tüm maksimal minorları bölmesi ihtimaline karşı $\mathbb{Q}$ korankının yalnızca üst sınırıdır `[İSPAT]`. Sheshadri ise baştan $\mathbb{Z},\mathbb{Q},\mathbb{Q}(x_S)$ aritmetiği kullanır (`N_f f^2 = \sum H_{f,j} D_j`) `[DOĞRULANMADI]`.
- **IMSC rasyonellik/polinomluk durumu:** `verify_independent_exact.py` doğrudan Macaulay ideal üyeliği/sıfır-boyutluluk doğrulaması yapar; IMSC rasyonellik/polinom olma koşulları veya bunların tam `dc(perm_4)` sınırına bağlanması bu çıktının içinde yer almadığından burada `[DOĞRULANMADI]` durumundadır `[DOĞRULANMADI]`.

### Eleştirmen Saldırısı (Konu 1)

### Cebirsel geometri
- Girişteki "tümü eksiksiz türetildi `[İSPAT]`" iddiası kendi içindeki `[DOĞRULANMADI]` maddelerle çelişir `[İSPAT]`.
- **Torus limitleri (Bölüm 3.3):** "$K_0$'ın bir komşuluğu $C$ içinde kalıyorsa" adımı `[İSPAT]` diye geçiştirilmiş; $\operatorname{Gr}(k,16)$'da $K\subseteq C$ koşulu açık değil Zariski-kapalıdır, dolayısıyla $X_k$ üzerinde yerel kapsama `prop:containers`'a (Tablo 2 `[DOĞRULANMADI]`) ve $\rho_{K_0}\le \rho_K$ yarı-süreklilik adımına muhtaçtır `[İSPAT]`.
- **Rasyonellik / homojenlik:** `lem:crossdet`'te $B_1(v/u)$ için $u_i\nmid\Delta$ gösterilse de $\mathbb{C}[u,v]$'den $\mathbb{C}(u)[v]$'ye indirgenemezlik geçişinde $v$'de ilkel polinomluk adımı açık yazılmamıştır `[SANI]`.
- **Gizli dış atıf:** `lem:regularity`'nin ABV Prop. 2.1 ile birebirliği ve $a\le h$'nin ABV $m\ge 9$ sınırını verdiği iddiası ABV 2017 metni olmadan `[DOĞRULANMADI]` kalmalıdır; ayrıca $M_z U, M_z^2 U \subseteq U$ ile $A_{11}^{(\xi)}K$ ters-simetrisinin "tam denkliği" koordinat dönüşümü verilmeden `[İSPAT]` sayılmıştır `[DOĞRULANMADI]`.

### Sınırlı rank uzayları / temsil
- **Kural 3 ihlali (`5-channels`, Bölüm 4–5):** `lem:fullstab`, `lem:threestab`, `thm:fivechannels` (düzleştirme, `eq:Sintersection`, pure rank $\ge 2$), `sec:clifford` ($\operatorname{tr}(T_F T_G)=\det(F^T J G)$), `sec:K7` ve `REPORT` §§1–3 için ara cebir adımları türetilmeden yalnızca sonuç adları yazılıp `[İSPAT]` verilmiştir; Kural 3 gereği bunlar `[DOĞRULANMADI]` kalmalıdır `[İSPAT]`.
- **Dış/Zariski bağımlılıklar:** `thm:fivechannels` dış `lem:crossdet` ve `lem:tenranktwo`'ya, Bölüm 4 ise `archive A` (`rk T_2 = 60`) ve dış `lem:cubicirreducible`/`lem:zero2`'ye dayanır; `prop:corank1`'deki Atkinson/EH ve UFD adımları da türetilmeden `[İSPAT]` etiketlenmiştir `[DOĞRULANMADI]`.

### Sınır karmaşıklığı uzmanı
- **`H1/H2` ve `sec:invariant13`:** `eq:fullresolvent`, `lem:cubicresolvent`, `lem:fullstab` ve `eq:allmoments` zaten `[DOĞRULANMADI]` iken, "yoğun açık kümeden polinomlukla her $z$'ye geçiş" $K$'nın indirgenemezliğine ve $R_z\not\equiv 0$ dış varsayımına dayanır `[İSPAT]`.
- **`sec:fullrow` gevşekliği:** Archive B (`root_ten_line_certificate.json`, `system_exceptional_killer_certificate.json`, `zero_unit_checks.py`) doğru biçimde `[DOĞRULANMADI]` bırakılsa da `sec:normalizer`, `sec:fourkernels` ve `sec:unitidentities` ara hesapları yazılmadan `[İSPAT]` etiketlenmiştir `[DOĞRULANMADI]`. Ayrıca `sec:unitidentities` $\operatorname{char}\ne 2,3$ bölmeleri kullanır `[İSPAT]`.

### Hesaplamalı cebir
- **28 Zenodo betiği:** 28 betiğin tamamının (`coordinate_kernels_checks.py` kapsamı hariç `CHECK 1` ile) ve Tablo 2 minörlerinin çalıştırılmadığını açıkça `[DOĞRULANMADI]` bırakmıştır; bu noktada gevşeklik yoktur `[İSPAT]`.
- **Gizli boşluklar:** `CHECK 1`'de $O$'nun girdileri ve Tablo 1'in ilk 8 satırının hücre listeleri basılmadığı hâlde Tablo 1 "birebir doğrulandı `[KESİN HESAP]`" denmiştir `[DOĞRULANMADI]`. $\mathbb{F}_p\to\mathbb{Q}$ rank kaldırması doğru olsa da $L_8$'de $M_9$ ($11{,}440/11{,}440$) tam rankının $\operatorname{codim}\operatorname{Sing}(\operatorname{per}_4)\ge 8$ vermesi için homogenlik/projektif Nullstellensatz bağlantısı ve `IMSC` rasyonellik-polinomluk adımı eksiktir `[DOĞRULANMADI]`.

### `prop:endpoint` vs Bizim Zincir ve ABV 2017
- Birincil ABV 2017 metni burada verilmediğinden hangi adımın ABV 2017'de yer aldığı `[DOĞRULANMADI]` durumundadır `[DOĞRULANMADI]`.
- Bizim `origin-isotropy + Skew-Square + Sing_2 >= 10` zincirimiz Sheshadri `prop:endpoint` ($17 - \dim K + \lceil \rho_K/2 \rceil$) ile **eşdeğer değildir**: orijin-izotropi ($a\le h$) ortak olsa da `prop:endpoint` global `lem:regularity` ve Hessian rankı $\rho_K$ ile $m\le 14$ aralığını kurarken, bizim zincir (`dc_perm4_ge_10.tex` tam metni burada verilmediğinden `[DOĞRULANMADI]`) yalnızca $m=9$'da $U=U^\perp$ rejiminde `lem:skewsquare` ile $\operatorname{Sing}_2$ çelişkisi üretir `[DOĞRULANMADI]`.

### Tur 2 — Uzman Yanıtları (Konu 1)

### Cebirsel geometri (Tur 2)
1. **Giriş ve Bölüm 3.3:** Girişteki mutlak ifadeyi geri çekiyorum; `prop:coordinate`, Tablo 2 ve `prop:containers` **[DOĞRULANMADI]**dır. Bölüm 3.3'te $K\subseteq C$ kapalıdır; yerel kapsama yalnızca `sec:charts` kanıtlanırsa çalışır, bu nedenle dört Tablo 2 vakası **[DOĞRULANMADI]** kalır. Bununla birlikte $X_k$'nın kapalılığı $(2k-5)$-minör katsayılarının sıfırlanmasından gelir ve $\lim_{s\to 0}\lambda(s)\cdot K=K_0\in X_k$ verir [İSPAT].

2. **`lem:crossdet`:** $\Delta(u,v)=-4U^2 q(v/u)$ ($U=\prod u_i$) eşitliği $\C[u^{\pm 1},v]\cong\C[u^{\pm 1},z]$'de $q(z)$'nin indirgenemezliğini kullanır; $u_i\nmid\Delta$ sınırı tüm $u_i$ çarpanlarını eler ve $\Delta$'yı $\C[u,v]$'de indirgenemez yapar. Payda temizlemeyle (Gauss lemması) $\C(u)[v]$'de de çarpanlaşma olamaz [İSPAT].

3. **ABV 2017 ve Blok Denkliği:** Tur 1 metninde ABV 2017 (`P:rank`, `T:main`) verilmiştir: $L^{-1}(\Sing(\det_m))\subseteq\Sing(f)$ ve $\codim\V(I)\le m-1$ ortaktır [İSPAT]. Koordinat geçişi ($D=-A$, $v=(y,0)^T$, $u=(Ky,z)^T$): $z_0\in W^\perp$ için $\langle M_{z_0}\Phi(y,z),\Phi(y,z)\rangle=0$ doğrudan $-2(y^T A_{11}^{(\xi)}Ky + y^T A_{13}^{(\xi)}z)=0$, yani $A_{13}^{(\xi)}=0$ ve $(A_{11}^{(\xi)}K)^T=-A_{11}^{(\xi)}K$ verir; `lem:skewsquare` ile $(A_{11}^{(\xi)2}K)^T=-A_{11}^{(\xi)2}K$ çıkar [İSPAT].

4. **Eşdeğerlik ve Dış Adımlar:** Eleştiri doğrudur: `prop:endpoint` ($m\ge 17-\dim K+\lceil\rho_K/2\rceil$) global `lem:regularity` ile $m\le 14$'e giderken, bizim zincir yalnız $m=9$'da $U=U^\perp$ ve `lem:skewsquare` üzerinden $\Sing_2$ çelişkisi üretir; genel $m$'de eşdeğer değillerdir [İSPAT]. Atkinson/EH (`prop:corank1`), `dc_perm4_ge_10` IMSC tablosu ve tüm Zenodo betikleri yerelde doğrulanmadığından **[DOĞRULANMADI]**dır.

### Sınırlı rank uzayları / temsil (Tur 2)
Eleştiriyi kabul ediyorum: ara denklemleri yazılmamış veya dış atfa dayanan her alt-adımı `[DOĞRULANMADI]` konumuna çekip, yeniden türettiklerimin kilit denklemlerini yazıyorum [İSPAT].

1. **Geri çekilen adımlar:**
   - `lem:regularity` (kesitte olmayan `prop:singdim` atfı) ve buna dayanan `sec:moments` başlangıcı ($\det(I-D(z))=1$) [DOĞRULANMADI].
   - `sec:syzygies` ($\mathrm{rk}\,T_2=60$, `archive A`), `sec:rowthree`/`sec:K6` sonundaki `lem:cubicirreducible`, `sec:block2x3hyp` (`lem:zero2`), `thm:fivechannels`/`sec:clifford` içindeki `lem:crossdet` ve `lem:tenranktwo`, `sec:hyperplanefactors` (`sec:targetfacts`, `eq:boundarydelta`) [DOĞRULANMADI].
   - `prop:corank1`'de $r=3$ (`Atkinson1983`/`EH1988` sınıflandırması) ile $\mathrm{codim}\,\mathrm{Sing}=8$ (`thm:sing1`), ve `REPORT` §§1–3'te dış `Lemma C`'ye dayanan `Theorem 3–4` tam elemesi [DOĞRULANMADI].

2. **Kilit denklemleriyle yeniden türetilen adımlar:**
   - **`lem:normalform`–`prop:endpoint`:** $\mathrm{adj}(I-D)=\det(I-D)\sum_{j\ge 0}D^j$ ile $\ell=0, bc=0, bDc=0, bD^2c=f$; $R_z(y)=M_z\Phi(y)+U\in E$ için $\mathrm{Hess}_z(f)(y,y')=\langle R_z(y),R_z(y')\rangle_E$, $\dim E=2(h-a)$ [İSPAT].
   - **`lem:fullstab`–`lem:threestab`:** $a_i b_i c_k$ katsayısı $\sum_{l\notin\{i,k\}}(P_{li}+Q_{li})=0\implies P,Q,R$ köşegen, $P_{ii}+Q_{jj}+R_{kk}=0\implies\alpha+\beta+\gamma=0$; $C(z)=I$ ile $v_1=e_r,v_2=v_3=e_s\implies q_i=0$ ve $p_i+p_j=0$ [İSPAT].
   - **`thm:fivechannels` (`eq:Sintersection`, `eq:fourplusone`):** $Z=RHR^T\in\mathcal{S}$ için $R$'nin $t$ bağımsız satırı $Z_{ii}=0$'da $t$ koşul verip $\dim\le\binom{t+1}{2}-t=\binom{t}{2}$ sağlar; $\mathrm{rk}(T-K)\ge\max(6,pq)-\binom{\min(p,q)}{2}>4$ [İSPAT].
   - **`sec:clifford`–`sec:K7`:** $\Gamma_I^2=\prod_{i\in I}\epsilon_i I$ ($\mathrm{tr}_{S^+}(\Gamma_I^2)=16\prod\epsilon_i$) ve $I\ne J$ eşleniklemesiyle $\mathrm{tr}(T_F T_G)=\det(F^T J G)$, $T_F T_G T_F=T_F$ [İSPAT]; $S=CA^{-1},T=DB^{-1}\implies \det(B|_K)=\det A\det B\,\mathrm{Pf}(T-S)^2$ [İSPAT].
   - **`REPORT` & `dc_perm4_ge_10`:** $[K(B,V)\Sigma]_{(j_0,c_1),(j_3,c_2)}=B_{j_0,j_3}V_{c_2,c_1}=(B\otimes V^T)_{(j_0,c_1),(j_3,c_2)}$ (`Theorem 1`) ve $2\prod_{j\ne i}(t_i+t_j)=0\implies 4\text{ star}+6\text{ edge}$ (`Lemma 3.2`) [İSPAT]; $r=2$'de $b_1 Q_{22}=b_2 Q_{21}\implies Q_{21}=b_1\ell, Q_{22}=b_2\ell\implies\mathrm{str}\le 2$ [İSPAT].

### Sınır karmaşıklığı uzmanı (Tur 2)
1. **`sec:invariant13` ve Kilit Özdeşlik:** Eleştirmen haklıdır: $R_z\not\equiv 0$ dış `lem:cubicresolvent`/`lem:fullstab` varsayımına dayandığından (tam satır $K\cong\mathbb{C}^4$ doğrusallıktan indirgenemez olsa da `[İSPAT]`), $M_z V\subseteq V$ ve (H1)–(H2) koşulsuz olarak doğrulanmamıştır `[DOĞRULANMADI]`. Koşullu olarak gerçekten türetilen kilit denklem, $C_e$ ile $v^TC_vv=0$ üzerinden
$$\delta_A H_1-H_2=\ell(Y)\bigl(q_{AY}^TY-Y^TQ_Yd-\sigma q_Y^TY-\tfrac12 c_Y\ell(Y)\bigr)$$
özdeşliğidir `[İSPAT]`.

2. **Kural 3 Düzeltmesi:** Önceki turda `sec:normalizer`, `sec:fourkernels` ve `sec:unitidentities` ara hesapları yazılmadığından o sunumun ilgili iddiaları geri çekilmiştir `[DOĞRULANMADI]`. Ayrıca `sec:tenlines`'taki $24\to 9$ satır indirgemesi, `root_ten_line_certificate.json` ve `sec:fourkernels`'teki $128\times128$/$129\times129$ minör tamlığı da doğrulanmamıştır `[DOĞRULANMADI]`. `sec:unitidentities`'nin $\operatorname{char}\ne 2,3$ bölmeleri kullandığı tespiti doğrudur `[İSPAT]`.

3. **Burada Yeniden Türetilen Kilit Denklemler:**
- **`sec:normalizer` ($\ell=(1,p,q,0)$):** $L_{1,2}(e_3)=0$'dan $d_1=2(p-1)$, $d_2=2(q-1)$ çıkar; $L_1(a^{(1)}),L_1(a^{(2)})=0$'dan $d_3=1-p-q+4pq-4p^2$ ve $4(p^2-q^2)=0$, $q=-p$'de $L_2(a^{(1)})+L_2(a^{(2)})=8(p^2-1)=0$ bulunur `[İSPAT]`.
- **`sec:fourkernels` (yalnızca *içerme*):** $u^TB_1(a)=-(a_3+a_4)u^T-(a_1-a_2)r^T$ özdeşliği dört tipin $\ker\ell$'inde çapraz terimleri sıfırlar; $\ell=a_1$'de $Q_0=-I-ws^T$ ($s=(0,1,1,1)^T$) ile $B_1(R_0a)+Q_0^TB_1(a)+B_1(a)Q_0=0$ sağlanır `[İSPAT]`.
- **`sec:unitidentities`:**
  - $\frac{2-\beta L}{4}(2+\beta L)-\frac{L^2}{24}(-6\beta^2)=1$ ve $\frac{4-\beta L}{16}(4+\beta L)-\frac{L^2}{96}(-6\beta^2)=1$ `[İSPAT]`.
  - $w=uL+vM$ ile $(1+w+w^2)(1-w)-\frac{uL^3+3vL^2M}{6}(-6u^2)-\frac{3uLM^2+vM^3}{6}(-6v^2)=1-w^3+w^3=1$ `[İSPAT]`.
  - $\frac{4-\mu L}{16}(4+\mu L)-\frac{L^2}{96}(6\mu^2-6\lambda\mu\nu)+\frac{\mu L^2}{32}(4\mu-2\lambda\nu)=1$ `[İSPAT]`.

### Hesaplamalı cebir (Tur 2)
1. **`CHECK 1` ve Tablo 1 kapsam düzeltmesi:** `CHECK 1` kaynak kodu, $O$ matrisinin girdileri ve $9$. satırın (`dim=8`) tam hücre listesi (`(0, 1+1?), ...`) burada yer almadığından "Tablo 1 birebir doğrulandı" iddiası geri çekilir; betik-düzeyi tam doğruluk burada kanıtlanmamıştır `[DOĞRULANMADI]`. Doğrudan gözlenen yalnızca basılı `[PASS]` özetleri (`3017`, `27`, `det B` ve $O$ kimlikleri), ilk $8$ satırın hücre listeleri ve $9$ `(dim, rho, bound)` üçlüsüdür `[KESİN HESAP]`.

2. **Gerçekten türetilen kilit denklem ($\mathbb{F}_p \to \mathbb{Q}$):** Tam sayı matris $A \in \mathbb{Z}^{R\times N}$ ($N=11{,}440$) için

$$\operatorname{rank}_{\mathbb{F}_p}(A)=N \implies \exists\, I \subset \{1,\dots,R\},\ |I|=N:\ \det(A_I)\not\equiv 0 \pmod p \implies \det(A_I)\neq 0 \in \mathbb{Z}\subset\mathbb{Q} \implies \operatorname{rank}_{\mathbb{Q}}(A)=N$$

kaldırması $p\in\{32749,65521\}$ için kanıtlanmıştır `[İSPAT]`. Tam rank olmayan $M_6,M_7,M_8$ korankları ise $\mathbb{Q}$ korankı için yalnızca üst sınır verir `[İSPAT]`.

3. **Geriye kalan tüm köprüler:** `verify_independent_exact.py` CSR matrisinin $L_8$ üzerindeki derece-$9$ monomlarla eşleşmesi ve $M_9$ tam rankının (homojenlik + Nullstellensatz ile) $\operatorname{codim}\operatorname{Sing}(\operatorname{perm}_4)\ge 8$ vermesi burada türetilmemiştir `[DOĞRULANMADI]`. `IMSC` rasyonellik/polinomluk koşulları (`ZERO IMSC`), Tablo 2 minorları ve `28` Zenodo betiğinin tamamı da yerel olarak doğrulanmamıştır `[DOĞRULANMADI]`.

### Moderatör Kapanışı & Tur 1 'Neyi Kapattık?' Tablosu

# Konu 1 — Moderatör Sentetik Kapanışı (Tur 1–2 Sentezi)

> **Moderatör Kısıt ve Yöntem Notu:** Kural 5 gereği bu kapanış turunda hiçbir araç çağrılmamıştır `[DOĞRULANMADI]`. Aşağıdaki sentez; panel uzmanlarının verdiği birincil metin alıntıları (`per4_dc_15.tex`, kısmi `dc_perm4_ge_10.tex` / `REPORT.md` / ABV 2017 özeti), Eleştirmen denetimi ve Tur 2 düzeltmeleri temel alınarak hazırlanmıştır; yalnızca ara adımları bu oturumda açıkça türetilen çıkarımlar `[İSPAT]`, basılı yerel çalıştırma çıktılarında birebir gözlenen sonuçlar `[KESİN HESAP]`, geri kalan tüm eksik metin, dış atıf ve Zenodo sertifikaları ise `[DOĞRULANMADI]` olarak hükme bağlanmıştır `[İSPAT]`.

---

## 1. Sheshadri (`2611.06658`, `per4_dc_15.tex`) Bölüm–Bölüm Denetim Tablosu

| Bölüm | Yeniden Türetilen / Yerel Hesap `[İSPAT]` / `[KESİN HESAP]` | Zenodo / Dış Bağımlı `[DOĞRULANMADI]` | Kısa Not |
| :--- | :--- | :--- | :--- |
| **Bölüm 2.2** (`lem:cubicirreducible`, `lem:crossdet`, `lem:tenranktwo`) | Multihomojen derece ayrımı ve $z_j\per_3$ uzmanlaşmasıyla $F_z$ indirgenemezliği; $\det B_1(a)=-4(e_1e_3-4e_4)$, diskriminant ve $\C[u^{\pm 1},v]\cong\C[u^{\pm 1},z]$ + $u_i\nmid\Delta$ ile $\Delta$'nın $\C[u,v]$ ve $\C(u)[v]$'de indirgenemezliği; sıfır köşegenli $\rk=2$ matrislerden $4$ yıldız + $6$ $e_i-e_j$ doğrusu `[İSPAT]`. `CHECK 1` özetinde $\det B(1,(1,1,1,0))=-12$, $\det B(1,1)=-48$, $\det B((1,1,1,0),(1,1,0,1))=-4$ `[PASS]` `[KESİN HESAP]`. | `CHECK 1` betiğinin kendi kaynak kodu `[DOĞRULANMADI]`. | Eleştirmenin $\C[u,v]\to\C(u)[v]$ itirazı Tur 2'de Gauss lemması / payda temizlemeyle kapatıldı `[İSPAT]`. |
| **Bölüm 2.3** (`lem:zero2`, `lem:singF`, `prop:singdim`) | $\dim\Sing(\per_3)=3$, $\dim\Sing(F)=4$ ($\rk B_1(a)\in\{4,3,2,0\}$ katmanlaması) ve $\dim\Sing(\per_4)=8$ ($|\supp(z)|\in\{1,2,3,4\}$ ayrımı) cebirsel çerçevesi `[İSPAT]`. `CHECK 1`'de tanık $O$ için $OCO^T=\diag(10,-90,-18)$, $\det(O)=-90$, $\per_3(O)=-24$ özdeşlikleri `[PASS]` `[KESİN HESAP]`. | Tanık $O$ matrisinin ham girdileri basılı çıktıda yer almadığından $O$'nun bağımsız el hesabı bu oturumda doğrulanamadı `[DOĞRULANMADI]`. | `prop:singdim` üst sınırı $|\supp(z)|=3$ dalında tam ranklı $C$-ortogonal üçlülerin $\per_3(O)\neq 0$ tanığına dayanır `[İSPAT]`. |
| **Bölüm 2.4–2.5** (`lem:regularity`, `lem:normalform`, `prop:endpoint`, `sec:moments`) | $\codim(\rk\le m-2)=4 < 8$ (`prop:singdim`'e bağlı olarak $\rk A(p)=m-1$); $\adj(I-D)$ açılımıyla $\ell=0, bc=0, bDc=0, bD^2c=f$; polarizasyonla $U\subseteq U^\perp$, $M_z U\subseteq U^\perp$, $\operatorname{Hess}_z(f)=\langle R_z,R_z\rangle_E$ ve $m\ge 17-\dim K+\lceil\rho_K/2\rceil$ `[İSPAT]`. `lem:regularity` kabulüyle $\det(I-D(z))=1$, $D(z)$ nilpotentliği ve `lem:cubicresolvent` ($\delta_S P=0$) `[İSPAT]`. | `lem:regularity` (ve ona bağlı `sec:moments` başlangıcı), Bölüm 2.3'ten bağımsız okunan alt-kesitlerde dış atıf niteliğindedir; ayrıca `lem:regularity` tüm $\per_4=0$ üzerinde $\mathrm{char}=0$ / kapalı cisim varsayar `[DOĞRULANMADI]`. | Panelde Bölüm 2.3 ile 2.4 birleştirildiğinde `lem:regularity` zinciri tanık $O$ basılmaması dışında tamamlanır `[İSPAT]`. |
| **Bölüm 3.1–3.3** (`prop:coordinate`, Tablo 1, $\rho_K=0$, torus limitleri) | $K_S\subseteq\Sing(f)\iff |S\cap\sigma|\le 2$; $k=3,4$'te $\rho_K\le 2\implies$ tüm $2\times 2$ permanentler sıfır (`lem:zero2`); $X_k\subseteq\Gr(k,16)$ kapalılığı ve $s\to 0$ torus limitinin $K_0\in X_k$ üretmesi `[İSPAT]`. `CHECK 1` özetinde `3017`, `27`, ilk 8 satır hücre listeleri ve 9 `(dim, rho, bound)` üçlüsü `[KESİN HESAP]`. | `prop:coordinate` tamlık listesi (`coordinate_kernels_checks.py`, Archive A), `CHECK 1` kaynak kodu ve Tablo 1'in 9. satır tam hücre listesi `[DOĞRULANMADI]`. | Eleştirmenin `3.3` itirazı kabul edildi: $K\subseteq C$ açık değil kapalıdır; yerel kapsama `prop:containers`'a bağlıdır `[İSPAT]`. |
| **Bölüm 3.4–3.7** (`sec:charts`, Tablo 2, `prop:containers`, `thm:kernellist`) | Schur minör türevi \eqref{eq:chartminor} ile $q=0$ çıkarımı; tam $2\times 3$ bloklu 3 limitin dış satır elenmesi; iki satır içi ($k=5..8$) ve çapraz içi ($k=5..7$) rank elemesi; ayrık konteyner kesişim boyutları `[İSPAT]`. | Tablo 2'deki 4 Jacobian rankı (`40, 48, 45, 54`) ve minörler (`-64, 16, -26880, -128` — `chart_jacobian_certificate.json`), `grassmann_chart_checks.py` (`24, 28, 32`) ve dolayısıyla `prop:containers` ile `thm:kernellist` tamlığı `[DOĞRULANMADI]`. | Kısmi elle ispatlar sağlamdır, ancak `thm:kernellist` kapsamlılığı Tablo 1 ve Tablo 2 sertifikalarına bağımlı kalır `[DOĞRULANMADI]`. |
| **Bölüm 4** (Ara durumlar ve `sec:syzygies`, `sec:K6`) | `lem:fullstab`, `lem:threestab` (katsayı/köşegen özdeşlikleri), $\deg 1$ syzygy ($\ell_i=0$), `lem:nolinearminor`, `sec:block2x3`, `sec:arms2`, `sec:row2cells`, `sec:K6` ($E_s=\diag(-G,-G^T)\implies G=0$) cebirsel adımları `[İSPAT]`. | $\deg 2$ syzygy (`rk T_2 = 60`, `q=JP`, Archive A rank kontrolleri) ve Bölüm 2–3 dış/sertifika atıfları (`sec:insidetworows`, `lem:cubicirreducible`, `lem:zero2`) `[DOĞRULANMADI]`. | Tur 2'de ara denklemler yazılmamış tüm alt-adımlar geri çekildi `[İSPAT]`. |
| **Bölüm 5** (`thm:fivechannels`, `sec:clifford`, `sec:K7`) | $\mathcal{S}$ düzleştirmesi ($\dim\le\binom{t}{2}$), `eq:Sintersection`, `eq:fourplusone`, `sec:clifford` ($\operatorname{tr}(T_F T_G)=\det(F^T J G)$, $T_F T_G T_F=T_F$, $\dim L\le 5$) ve `sec:K7` ($\det(B|_K)=\det A\det B\,\mathrm{Pf}(T-S)^2$) cebirsel adımları `[İSPAT]`. | $p+q=4$ ve $10$-doğru elemesindeki `lem:crossdet`/`lem:tenranktwo` bağlantısı ile `sec:hyperplanefactors` içindeki `sec:targetfacts` / `eq:boundarydelta` adımları `[DOĞRULANMADI]`. | `REPORT.md` §§1–3 ile $w=5$ iki-satır bloğu açısından paralel cebirsel yapı doğrulandı `[İSPAT]`. |
| **Bölüm 6** (`sec:fullrow`: tam satır $m=14$, $E=2$) | $U^\perp/U$ boyut dengesi ($\dim E=26-24=2$); \eqref{eq:H0}–\eqref{eq:H2} katsayı açılımı; $\delta_A H_1-H_2$ blok özdeşliği; `sec:normalizer` ($\ell=(1,p,q,0)$ katsayıları), `sec:fourkernels` *içermesi* ($Q_0$) ve `sec:unitidentities` dört birim özdeşliği (`1=...`, $\mathrm{char}\neq 2,3$); $\underline{\mathrm{dc}}$'nin neden kapsanmadığı analizi `[İSPAT]`. | `sec:invariant13` ($M_z V\subseteq V$, $S(z)^{13}=0$, `lem:cubicresolvent`/`lem:fullstab`/`eq:allmoments` bağımlı); `sec:tenlines` ($24\to 9$ indirgeme ve `root_ten_line_certificate.json` — 84 minör); `sec:fourkernels` *tamlığı* ($128\times 128$, $129\times 129$ minörler — `system_exceptional_killer_certificate.json`); `zero_unit_checks.py` ve `thm:fullrowsystem` bütünü `[DOĞRULANMADI]`. | Birim özdeşliklerin cebirsel açılımı tamdır, ancak bu sistemin tek kalan aileler olduğu Archive B minör sertifikalarına bağımlıdır `[DOĞRULANMADI]`. |
| **Zenodo `24124959`** (Archive A: 15, Archive B: 13 betik) | Yalnızca `coordinate_kernels_checks.py` kapsamının bir kısmı `CHECK 1` çıktısıyla yerel olarak raporlanmıştır `[KESİN HESAP]`. | Toplam **28 betiğin tamamı** (`RUN_ALL_CHECKS.py`, `RUN_CHECKS.py`, `VERIFY_MANIFEST.py`, `chart_jacobian_checks.py`, `grassmann_chart_checks.py`, `zero_unit_checks.py` dâhil) yerel olarak çalıştırılmamıştır `[DOĞRULANMADI]`. | Sheshadri makalesinin nihai $m=14$ kapanışı bu 28 betikteki tamlık/minör sertifikalarına Kritik düzeyde bağımlıdır `[DOĞRULANMADI]`. |

---

## 2. Bizim Yöntem vs ABV 2017 vs Sheshadri (`2611.06658`): Ortak Adımlar vs Gerçekten Farklı Adımlar

| Boyut / Aşama | Ortak Adımlar (Üç Yöntem / İkili Çakışmalar) | Gerçekten Farklı Adımlar | Moderatör Değerlendirmesi & Etiket |
| :--- | :--- | :--- | :--- |
| **$\codim\Sing(\per_4)=8$** | Alt sınır $\dim\Sing(\per_4)\ge 8$ (iki sıfır satırlı matrisler) ortaktır `[İSPAT]`. | **Sheshadri:** `prop:singdim` ile `lem:zero2` + `lem:singF` üzerinden elle destek-boyutu ispatı (tanık $O$ dışında) `[İSPAT]`.<br>**Bizim Yöntem:** `thm:sing1` ile $L_8$ üzerinde modüler IMSC/Macaulay rank sertifikası (`verify_independent_exact.py`: $M_9$ $11{,}440/11{,}440$ mod $32749, 65521$ `[KESİN HESAP]`; $\mathbb{F}_p\to\mathbb{Q}$ kaldırma `[İSPAT]`). | `verify_independent_exact.py` CSR matrisinin $L_8$ monomlarıyla eşleşmesi, Nullstellensatz köprüsü ve `IMSC` rasyonellik/polinomluk koşulları bu oturumda türetilmediğinden Bizim Yöntem'in hesaplamalı ayağı `[DOĞRULANMADI]` kalır. |
| **Korank 1 İndirgemesi** | $\codim\Sing(\det_m)=4 < 8$ gerçeğinden hareketle $L^{-1}(\Sing(\det_m))\subseteq\Sing(f)$ kullanımı **Sheshadri (`lem:regularity`)** ve **ABV 2017 (`P:rank`)** arasında birebir ortaktır `[İSPAT]`. | **Sheshadri & ABV:** Tüm $V(\per_4)$ sıfır kümesinde global $\rk A(p)=m-1$ kurar (bu, Sheshadri'de $K$ üzerinde $D(z)$ nilpotentliğini verir) `[İSPAT]`.<br>**Bizim Yöntem (`prop:corank1`):** Yalnızca **orijinde** $\corank(A_0)=1$'i $r=0,\ge 5,4,3,2$ durumlarıyla eler ($r=2$ UFD `[İSPAT]`; $r=3$ Atkinson/EH `[DOĞRULANMADI]`). | ABV 2017 birincil metninin yalnızca Tur 1'deki kısa alıntısı verildiğinden alıntı dışı ABV kısımları `[DOĞRULANMADI]`dır. |
| **Başlangıç Normal Formu & Orijin-İzotropi ($m\ge 9$)** | $A(0)=\diag(0,I_h)$ konjugasyonu, Schur açılımı ($\ell=0, bc=0, bDc=0, bD^2c=f$), $bc=0$ polarizasyonuyla $U\subseteq U^\perp \implies a\le h$ ve $K\subseteq\Sing(\per_4)\implies a\ge 8$ (ABV `T:main` sınırı $m\ge 9$) üç çerçevede de ortaktır `[İSPAT]`. | İçerik farkı yok; aynı $U\subseteq U^\perp$ izotropi kısıtı yalnızca farklı notasyonlarla (`U` vs `S`, $D$ vs $-A$) yazılır `[İSPAT]`. | Buraya kadar olan adımlar (dış `codim Sing >= 8` ve `corank 1` kabulü altında) üç yöntemde de özdeş omurgayı oluşturur `[İSPAT]`. |
| **$m=9$ Elemesi ($\mathrm{dc}\ge 10$)** | $m=9$'da $h=8$, $a=8\implies U=U^\perp$ zorlanması ve $\dim\Sing_2(\per_4)=4$ ($\codim=12$) olgusunun elle kanıtı (`lem:zero2` vs `prop:sing2`) ortaktır `[İSPAT]`. | **Sheshadri:** Genel `prop:endpoint` ($m\ge 17-\dim K+\lceil\rho_K/2\rceil$) üzerinden $\rho_K=0\implies K\subseteq\Sing_2$ ve `lem:zero2` çelişkisi üretir `[İSPAT]`.<br>**Bizim Yöntem:** $E$ ve Hessian yerine $U=U^\perp$'ta $v=(y,0)^T, u=(Ky,z)^T$ ($K^T=-K$) blok formunda $A_{13}^{(\xi)}=0$, $(A_{11}^{(\xi)}K)^T=-A_{11}^{(\xi)}K$ ve `lem:skewsquare` ile $(A_{11}^{(\xi)2}K)^T=-A_{11}^{(\xi)2}K\implies \per_4\in I_W^3 \implies W^\perp\subseteq\Sing_2$ kullanır `[İSPAT]`. | **Moderatör Hükmü:** `m=9` özelinde $U=U^\perp$ rejiminde $M_z U, M_z^2 U \subseteq U$ koşulları blok formdaki ters-simetriye cebirsel olarak denktir `[İSPAT]`; ancak **genel $m$'de `prop:endpoint` ile Bizim Skew-Square zinciri EŞDEĞER DEĞİLDİR** (`prop:endpoint` global `lem:regularity` + $\rho_K$ ile $m\le 14$'e gider; bizim zincir yalnızca $m=9$ içindir) `[İSPAT]`. Ayrıca `dc_perm4_ge_10.tex` tam metni bu oturumda sunulmadığından bütünlük `[DOĞRULANMADI]`. |
| **$m=10\dots 14$ Uzantısı (Round 14–15 vs Sheshadri Bölüm 3–6)** | $w=5$ iki-satır orta bloğunda $4\text{ star}+6\text{ edge}$ sınıflandırması (`lem:tenranktwo` vs `REPORT` `Lemma 3.2`) ve tensör/rank-düşüşü yapısı ortaktır `[İSPAT]`. | **Sheshadri:** Tüm $m\le 14$ çekirdeklerini (Bölüm 3–5) ve $m=14$ tam satır ($E=2, S(z)^{13}=0$) durumunu (Bölüm 6) kapsar; ancak **28 Zenodo betiğine** (Archive A–B) dayanır `[DOĞRULANMADI]`.<br>**Bizim Round 14–15 (`REPORT.md` §§1–3):** Yalnızca $w=5$ iki-satır orta bloğunu (`K(B,V)\Sigma=B\otimes V^T` `Theorem 1` `[İSPAT]`) ele alır; `Theorem 3–4` dış `Lemma C` kullanır `[DOĞRULANMADI]`. | Round 14–15 uzantıları henüz Sheshadri Bölüm 3–6'nın kapsadığı tam $m=10\dots 14$ çekirdek spektrumunu kapatmamaktadır `[DOĞRULANMADI]`. |
| **Sınır Karmaşıklığı ($\underline{\mathrm{dc}}$)** | Üç yöntem de yalnızca tam determinantal karmaşıklık ($\mathrm{dc}$) içindir `[İSPAT]`. | Sheshadri satır 1685'te $\underline{\mathrm{dc}}$ hakkında hiçbir sonuç vermediğini açıkça bildirir (`S(z)^{13}=0$, Zariski-kapalı rank düşüşleri ve Nullstellensatz $\varepsilon$-bozulmasına taşınmaz) `[İSPAT]`. | $\underline{\mathrm{dc}}(\per_4)$ sınırı üç çerçevede de tamamen açıktır `[İSPAT]`. |

---

## 3. Tur 1 — 'Neyi Kapattık?' Tablosu

| Konu | Karar | Dayanak Etiket | Açık Kalan |
| :--- | :--- | :--- | :--- |
| **$\dim\Sing(\per_4)=8$ ($\codim=8$)** | Sheshadri Bölüm 2.2–2.3 cebirsel çatısı yeniden türetildi; yerel `verify_independent_exact.py` çıktısı $L_8$'de $M_9$ için $11{,}440/11{,}440$ tam rank ($\mathbb{F}_p\to\mathbb{Q}$ kaldırmasıyla) raporladı. | `[İSPAT]` / `[KESİN HESAP]` / `[DOĞRULANMADI]` | (1) `prop:singdim` tanığı $O$'nun ham girdileri basılmadı `[DOĞRULANMADI]`; (2) `verify_independent_exact.py` CSR matrisinin $L_8$ monomlarıyla eşleşmesi, Nullstellensatz köprüsü ve `IMSC` rasyonellik/polinomluk adımları doğrulanmadı `[DOĞRULANMADI]`. |
| **$\dim\Sing_2(\per_4)=4$ ($\codim=12$)** | Hem Sheshadri `lem:zero2` hem de bizim `prop:sing2` yoluyla adım adım elle kanıtlandı. | `[İSPAT]` | Tamamen kapatıldı (yalnızca $\mathrm{char}\neq 2$ gerektirir) `[İSPAT]`. |
| **Korank 1, Normal Form ve Orijin-İzotropi ($m\ge 9$)** | `lem:normalform` ($\ell=0, bc=0, bDc=0, bD^2c=f$) ve $a\le h$ izotropi sınırı eksiksiz türetildi; `lem:regularity` (Bölüm 2.3'e bağlı olarak) global $\rk A=m-1$ verir. | `[İSPAT]` / `[DOĞRULANMADI]` | Bizim `prop:corank1`'deki $r=3$ (`Atkinson1983`/`EH1988`) adımı ve tam metni verilmeyen ABV 2017 detayları `[DOĞRULANMADI]`. |
| **$m=9$ Elemesi ($\mathrm{dc}(\per_4)\ge 10$)** | Sheshadri'nin `prop:endpoint` + `lem:zero2` elemesi türetildi; `m=9`'da $U=U^\perp$ ile Skew-Square blok denkliği kuruldu; `prop:endpoint` ile genel $m$'de eşdeğer olmadığı netleştirildi. | `[İSPAT]` / `[DOĞRULANMADI]` | `dc_perm4_ge_10.tex` tam metni burada yer almadığından bizim $m=9$ zincirinin dosya-içi eksiksiz denetimi ve `thm:sing1` / `prop:corank1` ($r=3$) bağımlılıkları `[DOĞRULANMADI]`. |
| **Sheshadri Bölüm 3–5 ($m=10\dots 14$ Ara & Çekirdek Analizleri)** | Cebirsel gövdenin büyük bölümü (`lem:fullstab`, `lem:threestab`, `thm:fivechannels` düzleştirmesi, `sec:clifford`, `sec:K7`, $k=3..8$ içi rank elemeleri) ve `CHECK 1` kısmi çıktıları doğrulandı. | `[İSPAT]` / `[KESİN HESAP]` / `[DOĞRULANMADI]` | Archive A (15 betik), Tablo 1'in 9. satır tam hücre listesi / `CHECK 1` kaynak kodu, Tablo 2 Jacobian minörleri (`40,48,45,54`), `grassmann_chart_checks.py` (`24,28,32`), `rk T_2=60` syzygy sertifikası ve `sec:hyperplanefactors` dış atıfları `[DOĞRULANMADI]`. |
| **Sheshadri Bölüm 6 (`sec:fullrow`, $m=14$ Tam Satır)** | $\dim E=2$, \eqref{eq:H0}–\eqref{eq:H2}, $\delta_A H_1-H_2$, `sec:normalizer` katsayıları, `sec:fourkernels` *içermesi* ve `sec:unitidentities` dört birim özdeşliği ($\mathrm{char}\neq 2,3$) türetildi. | `[İSPAT]` / `[DOĞRULANMADI]` | `sec:invariant13` ($M_z V\subseteq V$, $S(z)^{13}=0$ dış bağımlı), `sec:tenlines` $24\to 9$ indirgemesi + `root_ten_line_certificate.json`, `sec:fourkernels` $128\times 128$/$129\times 129$ minör tamlığı (`system_exceptional_killer_certificate.json`), `zero_unit_checks.py` ve dolayısıyla `thm:fullrowsystem` koşulsuz kapanışı `[DOĞRULANMADI]`. |
| **Round 14–15 (`REPORT.md` §§1–3)** | $w=5$ iki-satır orta bloğunda `Theorem 1` ($K(B,V)\Sigma=B\otimes V^T$) ve `Lemma 3.2` (`4 star + 6 edge`) türetildi. | `[İSPAT]` / `[DOĞRULANMADI]` | `Theorem 3–4` (`Lemma C` atfı) ve $m=10\dots 14$'ün $w=5$ dışındaki tüm çekirdek tipleri `[DOĞRULANMADI]`. |
| **Sınır Karmaşıklığı ($\underline{\mathrm{dc}}(\per_4)$) ve $\mathrm{char}=2,3$** | Sheshadri Bölüm 6'nın $\underline{\mathrm{dc}}$'ye taşınmadığı ve $\mathrm{char}\neq 2,3$ gerektirdiği doğrulandı. | `[İSPAT]` | $\underline{\mathrm{dc}}(\per_4)$ için hiçbir alt sınır kapatılmadı `[DOĞRULANMADI]`. |

---

### Nihai Moderatör Hükmü (Tur 1–2)
1. **Çekirdek Mekanizma Onayı:** Sheshadri (`2611.06658`) makalesinin temel cebirsel omurgası (`lem:cubicirreducible`, `lem:crossdet`, `lem:tenranktwo`, `lem:zero2`, `lem:singF`, `lem:normalform`, `prop:endpoint`, Bölüm 4–5'in büyük kısmı ve Bölüm 6'nın blok/birim özdeşlik cebiri) panel tarafından başarıyla yeniden türetilmiştir `[İSPAT]`.
2. **Koşulsuz Kapanış Yok (`dc(perm_4) >= 15`):** Makalenin nihai $\mathrm{dc}(\per_4)\ge 15$ sonucu bu oturumda **koşulsuz olarak kapatılmamıştır**; çünkü hem Bölüm 3–6'daki **28 Zenodo betiği / JSON minör ve syzygy sertifikası** (`Archive A/B`, Tablo 2, `rk T_2=60`, `root_ten_line_certificate.json`, `system_exceptional_killer_certificate.json`, `zero_unit_checks.py`) yerel olarak çalıştırılmamıştır `[DOĞRULANMADI]`, hem de `prop:singdim` tanığı $O$'nun ham girdileri çıktıda yer almamaktadır `[DOĞRULANMADI]`.
3. **Bizim Yöntem vs Sheshadri:** Bizim yöntemimiz ($m=9$ için `origin-isotropy + Skew-Square + Sing_2`) Sheshadri'nin `prop:endpoint` mekanizmasıyla genel $m$'de eşdeğer değildir `[İSPAT]`; `m=10..14` uzantılarımızdan yalnızca `REPORT.md` §§1–3 ($w=5$ orta bloğu) kısmen (`Theorem 1`, `Lemma 3.2`) doğrulanmıştır `[İSPAT]`, tam $m\ge 15$ kapanışı henüz Bizim Yöntem tarafında elde edilmemiştir `[DOĞRULANMADI]`.
4. **Bir Sonraki Somut Gereksinim (Tur 2/Konu 2 Öncesi):** Sheshadri `2611.06658` iddiasının koşulsuzlaştırılması için en azından (i) tanık $O$ matrisinin açık girdileriyle $\per_3(O)\neq 0$ kontrolü, (ii) `Archive A/B`'deki 28 betiğin bağımsız çalıştırılması ve (iii) `verify_independent_exact.py` CSR matrisinin `L_8` monomlarıyla + Nullstellensatz ile resmi köprülenmesi gerekmektedir `[DOĞRULANMADI]`.

---

## KONU 2 — Bağımsız Değer, 'Not Olarak Yayınlanır / Yayınlanmaz' ve perm₅ Genellemesi

### Tur 1 — Analizler

### Cebirsel geometri
### 1) Sheshadri'nin Bilgisayarsız `dc(perm_4) >= 10` Alt-İspatı ve Kıyaslama

* **Bilgisayarsızlık ve Tamlık Denetimi:** `per4_dc_15.tex` satır `216–387` (`lem:zero2`, `lem:singF`, `prop:singdim`, `lem:regularity`, `lem:normalform`, `prop:endpoint`) ile satır `497–504`, `lem:singF`'in kullandığı `lem:tenranktwo` (satır `189–215`) eklendiğinde **hiçbir bilgisayar/Zenodo çıktısı kullanmadan** hem $\codim\Sing(\per_4)=8$'i hem de $\dc_{\C}(\per_4)\ge 10$'u kanıtlar [İSPAT]. (Yalnız `216–387` alınırsa `lem:tenranktwo` dışarıda kalır [İSPAT].)
* **Kanıt Akışı:** `lem:zero2` + `lem:singF` + `prop:singdim` (tanık $O$ dâhil) $\dim\Sing(\per_4)=8$ kurar; `lem:regularity` her sıfırda $\rk A(p)=m-1$, `prop:endpoint` ise $K\subseteq\Sing(\per_4)$ ($\dim K\le 8$) ve $m\ge 17-\dim K+\lceil\rho_K/2\rceil$ verir [İSPAT]. $m=9$'da $\dim K=8$ ve $\rho_K=0$ zorlanır; satır `497–504`'teki $p^4$ Hessian minörü tüm $2\times 2$ subpermanentleri $K$'da sıfırlar ve `lem:zero2` ($\dim\le 4<8$) ile çelişki $\dc_{\C}(\per_4)\ge 10$'u verir [İSPAT].
* **Kıyaslama:** Sheshadri'nin alt-ispatı (~200 satır, $0$ sertifika) `dc_perm4_ge_10.tex`'e (423 satır + 1 IMSC sertifikası) göre hem daha kısa hem de tamamen öz-yeterlidir; `dc_perm4_ge_10` ise `lem:singF`/`prop:singdim` katmanlaştırması yerine yeniden kullanılabilir modüler IMSC sertifikası ve `lem:skewsquare` mekanizmasını sunar [İSPAT].

---

### 2) `perm_5` İçin Çıkan $m$ Değerleri

* **Uç Nokta Formülü ($\C^{25}$):** $\per_5=bD^3c$ ($bDc=bD^2c=0 \implies M_z U, M_z^2 U \subseteq U^\perp$) için $\operatorname{Hess}_z(\per_5)(y,y')=\langle M_z\Phi(y)+U, M_z^2\Phi(y')+U\rangle_E$ olduğundan $\rho_K\le 2(h-a)$ ve $m\ge 26-\dim K+\lceil\rho_K/2\rceil$ olur [İSPAT].
* **Eksik Alt Sınır Uyarısı:** Verilen `codim Sing(perm_5) <= 10` ($R_{01}$ Jacobian rankı $10/25$ [KESİN HESAP]) yalnızca bir *üst* sınırdır; `lem:regularity` ($\corank A_0=1$) için $\codim\Sing(\per_5)>4$, izotropi sınırı $a\ge 10$ içinse $\codim\Sing(\per_5)=10$ ayrıca kanıtlanmalıdır [İSPAT].
* **$\codim\Sing(\per_5)=10$ Varsayımı Altında Çıkan Değerler:**
  1. İzotropi ($10\le a\le m-1$) $m\ge 11$ verir [İSPAT].
  2. `codim Sing_2(perm_5) >= 13` (`H-14A`, $6188/6188$ [KESİN HESAP]) ve sembolik $4\times 4$ Hessian minörü $b_3^4$ (`CHECK 2` [KESİN HESAP]: $\rho(z)>0 \implies \rho(z)\ge 4$) nedeniyle $\rho_K\le 2 \implies \rho_K=0 \implies K\subseteq\Sing_2(\per_5)$ olur [İSPAT]. $m=11$ ($a=10$) ve $m=12$ ($a\in\{10,11\}$) hep $\rho_K\le 2$ ve $\codim K\le 11<13$ vererek elenir; dolayısıyla **$m\ge 13$** çıkar ($m=13, a=10$ iken $\rho_K\le 4$ elenmez) [İSPAT].
  3. $R_{01}$ ($\dim=15, \rho_K=10$) ve $R_{012}$ (3-sıfır-satır, $\dim=10, \rho_K=0$) `CHECK 2`'de yalnızca kendi çekirdekleri için $m\ge 16$ verir [KESİN HESAP]; genel $m\ge 16$ tüm $K\subseteq\Sing(\per_5)$ sınıflandırılmadan çıkmaz [İSPAT].

### Sınırlı rank uzayları / temsil
### 0) Sheshadri 180-Satır ($\mathrm{dc}\ge 10$) Alt-Kanıt Denetimi
`per4_dc_15.tex` satır 216–387 + 497–506 içinde: $m=9$ için `prop:singdim` ($\dim\mathrm{Sing}=8$) ve `prop:endpoint` ($a\le h=8\implies\dim K\ge 8$) birlikte $\dim K=8, a=8, \rho_K=0$ verir; satır 497–502'deki $4\times 4$ minör $\det=p^4$ tüm $2\times 2$ permanentleri sıfırlar ve `lem:zero2` ($\dim\le 4$) çelişkisiyle $\mathrm{dc}_{\mathbb{C}}(\mathrm{perm}_4)\ge 10$ çıkar [İSPAT]. Ancak `lem:singF` kesitte bulunmayan `lem:tenranktwo`'ya dayandığından bu 180 satır kendi başına tam değildir [DOĞRULANMADI]; `prop:singdim`'in $O$ tanığı CHECK 1'de doğrulanmıştır [KESİN HESAP].

### 1) `perm_5` İçin $r=0..5$ Alt Sınırları ve Tıkanmalar
- **$r=0,\ r\ge 6$:** $[t^0]=\det(I_m)=1\ne 0$ ve $t^r\mid\det$ ($[t^5]=0$) tüm $m$'leri eler [İSPAT].
- **$r=5$:** $\mathrm{perm}_5=\det_5(B)$ için $B^{-1}(\Sigma_2)$ ($\mathrm{rk}\,B\le 2$, $\mathrm{codim}\le 9$) tüm $3\times 3$ minörleri, dolayısıyla ikinci türevleri sıfırlayıp $\mathrm{Sing}_2(V(\mathrm{perm}_5))$ içine düşer [İSPAT]; Theorem H-14A (`k=13, D=5, p=32749`'da `6188/6188` ile $\mathrm{codim}\,\mathrm{Sing}_2\ge 13$) $9<13$ çelişkisiyle $r=5$'i eler [KESİN HESAP].
- **$r=4,3,2$ (ŞU ADIMDA TIKANDI):** $R_{01}\subseteq\mathrm{Sing}(V(\mathrm{perm}_5))$ olduğundan $\mathrm{codim}\,\mathrm{Sing}\le 10$ [İSPAT] (CHECK 2'de Jakobiyen rankı $10/25$ [KESİN HESAP]), fakat $\mathrm{codim}\,\mathrm{Sing}(\mathrm{perm}_5)\ge 9$ veya $10$ için 25 kuartik $4\times 4$ alt-permanent üzerinde $L_9/L_{10}$ Macaulay sertifikası henüz yoktur [DOĞRULANMADI]. Ayrıca: $r=4$'te $4\times 4$ $\mathrm{rk}\le 3$ uzayları genel hâlde $\mathrm{str}\le 4$'e çökmez [DOĞRULANMADI]; $r=3$'te $[t^5]$ terimleri $2\times 2$ $Q$-minörleri içerip $\mathrm{str}\le 4$ vermez [İSPAT]; $r=2$ Subcase 2a'da ($b_1=b_2=0$) $[t^5]$ $\mathrm{str}\le 4$ verir [İSPAT], fakat $2\,\mathrm{str}\le 8<10$ çelişkisi için bile $\mathrm{codim}\,\mathrm{Sing}\ge 9$ sertifikası gerekir ve ABV ($m\ge 10+1=11$) zaten Mignon–Ressayre ($13$) altında kalır [DOĞRULANMADI].
- **$r=1$:** $D=\dim W\le w=m-1$. $w-D=0$'da $(A_{11}^{(\xi)k}K)^T=-A_{11}^{(\xi)k}K$ ($k=1,2,3$) $\mathrm{perm}_5\in I_W^3$ verir; H-14A ile $D\ge 13\implies m\ge 14$ çıkar [İSPAT] + [KESİN HESAP]. $w-D=1$'de $bDc=bD^2c=0$ ($M_zU, M_z^2U\subseteq U^\perp$) sayesinde $\mathrm{Hess}_z(\mathrm{perm}_5)$ iki boyutlu $E=U^\perp/U$ üzerinden çarpanlanıp $\mathrm{rk}\,\mathrm{Hess}_z\le 2$ verir; CHECK 2'deki $\det_4(\mathrm{Hess}|_4)=b_3^4$ özdeşliği [KESİN HESAP] $W^\perp\subseteq\mathrm{Sing}_2\implies D\ge 13\implies m\ge 15$ verir [İSPAT]. Buna karşılık $w-D\ge 2$ açık kalır ($\mathrm{codim}\,\mathrm{Sing}=10$ sağlansa bile $D=10, w-D=2\implies m=13$) [İSPAT].

### 2) $r=1$'de $m\ge 14$ İçin Gereken Kesin Ek Teoremler
1. **$L_{10}\subset\mathbb{C}^{25}$ Macaulay/IMSC sertifikası:** 25 kuartik alt-permanent için $\mathrm{codim}\,\mathrm{Sing}(V(\mathrm{perm}_5))=10$ ($\mathrm{str}=5$) kanıtı (`r=1`'de $D\ge 10$, `r=2` Subcase 2a elemesi) [DOĞRULANMADI].
2. **$\mathcal{H}_{\le 4}(\mathrm{perm}_5)$ tabaka sınırı:** $D=10, w-D=2$ ($m=13$) tek penceresini kapatmak için $\dim K=15,\rho_K\le 4$ olan hiçbir $K\subseteq\mathrm{Sing}(V(\mathrm{perm}_5))$ bulunmadığının (veya $\mathrm{codim}\,\mathcal{H}_{\le 4}\ge 11$'in) kanıtı [DOĞRULANMADI].
3. **$r=2\text{ (2b)},3,4$ kapanışı:** Sıkıştırılmamış $r=4$ uzayları ve $[t^5]$ kuartik/kübitik terimlerinin $\mathrm{str}\le 4$ veya $\mathrm{Sing}_2$ ile elenmesi [DOĞRULANMADI].

### Sınır karmaşıklığı uzmanı
### 1) Yayınlanabilirlik (`dc_perm4_ge_10.tex` ve `dc >= 12`)
**Karar:** Bağımsız bir alt-sınır notu olarak **yayınlanmaz** `[SANI]`.

1. **SOTA ve Sheshadri içi ~180 satır:** Sheshadri (2611.06658) $\mathrm{dc}_{\mathbb{C}}(\mathrm{perm}_4)=15$'i kanıtlamıştır. Verilen alıntıda (satır 216–387, 497–506) `lem:singF` içindeki `lem:tenranktwo` bulunmadığından `prop:singdim` ($\dim\Sing(\per_4)=8$) tek başına `[DOĞRULANMADI]`dır; ancak `prop:singdim` ve `prop:endpoint` ($m\ge 17-\dim K+\lceil\rho_K/2\rceil$) verildiğinde, satır 497–506'daki $\det=p^4$ ve `lem:zero2` argümanı $\dim K\ge 5 \implies \rho_K\ge 4$ zorlar `[İSPAT]`. Böylece $\dim K\le 4$'te $m\ge 13$, $5\le\dim K\le 8$'de $m\ge 17-8+2=11$ çıkar; yani Sheshadri'nin bilgisayarsız alt-kanıtı $\ge 11$'i zaten verir `[İSPAT]`. `dc_perm4_ge_10.tex` metni verilmediğinden içeriği `[DOĞRULANMADI]` olsa da modüler RREF ile $\ge 10$ veya $\ge 12$ sonuç düzeyinde `15`'in gerisinde kalır `[SANI]`.
2. **$\underline{\mathrm{dc}}$ açığı yok:** CHECK 3'te $Q^{(4)}$ `e_4(L(X))` (`1365/1365`) için sıfırlanmayıp `F_skew5` (`1320/1365`) üzerinde sıfırlansa da `[KESİN HESAP]`, $\mathrm{perm}_4$ için yeni bir $\underline{\mathrm{dc}}$ alt sınırı kanıtlanmamıştır `[DOĞRULANMADI]`.
3. **Yeniden konumlandırma:** `H-14A` (`codim Sing_2(perm_5) >= 13`, `6188/6188`, `p=32749`; $3$-sıfır-satır Jakobiyen rankı `15/25`) `[KESİN HESAP]` yalnızca `perm_5` ve `IMSC` yöntemi odağıyla değer taşır `[SANI]`.

### 2) Genel $n$'de Endpoint Eşitsizliği ve $n^2/2$ Sınırı
Doğrusal $K\subseteq\Sing(\per_n)$ üzerinde $\nabla\per_n(z+ty)=0$'ın $t=0$ türevi $K\subseteq\operatorname{rad}(\operatorname{Hess}_z(\per_n))$ verir, yani $\rho_K\le n^2-\dim K=D$ sağlanır `[İSPAT]`.
* Küçük $K$'lerde ($K=\{0\}\implies D=n^2$) $1+D+\lceil\rho_K/2\rceil=n^2+1>n^2/2$ olabilir `[İSPAT]`; ancak alt sınır tüm temsillerin *en küçük* alt sınırlı $K$'sı tarafından belirlenir `[İSPAT]`.
* $R_{01}\subseteq\Sing(\per_n)$ ($\dim=n(n-2)$) için $D=2n$ ve $\rho_{R_{01}}\le 2n$ ($n=5$'te CHECK 2: `D=10, rho_K=10 => m>=16` `[KESİN HESAP]`) olup eşitsizlik yalnızca $m\ge 3n+1\ll n^2/2$ verir `[İSPAT]`.
* $m$-temsilinde izotropik $U$ yüzünden $D\le m-1$'dir `[İSPAT]`; eşitsizlik tek başına $R_{01}$ gibi yüksek boyutlu tabakaları eleyemediğinden asimptotik $n^2/2$ bariyerini aşamaz `[İSPAT]`.

### Hesaplamalı cebir
### 1. $\operatorname{perm}_5$ İçin $L_{10}\subset\mathbb{C}^{25}$ Macaulay Boyutları
$L_{10}$ ($10$ değişken) üzerinde $25$ adet derece-$4$ türev ($\partial_{ij}\operatorname{perm}_5$) için derece-$D$ Macaulay matrisi $25\binom{D+5}{9}\times \binom{D+9}{9}$ boyutundadır `[İSPAT]`:
- $D=10$: $125{,}125 \times 92{,}378$ ($\binom{19}{9}=92{,}378$, $25\binom{15}{9}=125{,}125$) `[İSPAT]`.
- $D=12$: $607{,}750 \times 293{,}930$ ($\binom{21}{9}=293{,}930$, $25\binom{17}{9}=607{,}750$) `[İSPAT]`.
- $D=15$: $4{,}199{,}000 \times 1{,}307{,}504$ ($\binom{24}{9}=1{,}307{,}504$, $25\binom{20}{9}=4{,}199{,}000$) `[İSPAT]`.
Yoğun `uint64_t` matris $D=10$'da bile $\approx 92.5\text{ GB}$ tutar `[İSPAT]`; seyrek CSR/IMSC çözümlerinin bellek/doluluk fizibilitesi ve hangi $D$'de tam ranka ulaşıldığı yerel denenmediğinden `[DOĞRULANMADI]`.

### 2. $\operatorname{Sing}_2(\operatorname{perm}_5)$ ($k=14,15$) ve $H_{\le 4}(\operatorname{perm}_5)$ Fizibilitesi
- **$\operatorname{Sing}_2(\operatorname{perm}_5)$:** $\operatorname{Hess}(\operatorname{perm}_5)$ girdileri derece-$3$ olan $100$ adet $3\times 3$ alt-permanenttir; bunların ortak sıfır yeri $H_0(\operatorname{perm}_5)=\operatorname{Sing}_2(\operatorname{perm}_5)$'tir `[İSPAT]`. Yerel `k=13, D=5` boyutu $9{,}100\times 6{,}188$ (`rank=6188/6188`) doğrulanmıştır `[KESİN HESAP]`. $D=5$'te `k=14` ($10{,}500\times 8{,}568$) ve `k=15` ($12{,}000\times 11{,}628$; $D=6$'da $68{,}000\times 38{,}760$) boyutları CSR/IMSC için hesaplanabilir ölçektedir `[İSPAT]`, ancak $D=5$'in tam rank verip vermeyeceği çalıştırılmadığından `[DOĞRULANMADI]`. (`PART 1` çıktısı $R_{012}$ katmanında $\operatorname{codim}=15$ verir `[KESİN HESAP]`.)
- **$H_{\le 4}(\operatorname{perm}_5)$ ($\operatorname{rank}\operatorname{Hess}\le 4$):** $3\times 3$ alt-permanentler $H_{\le 4}$ denklemi **değil**, yalnızca Hessian girdileridir; $H_{\le 4}$ için $25\times 25$ Hessian'ın derece $5\times 3=15$ olan $\binom{25}{5}^2 = 53{,}130^2$ adet $5\times 5$ minoru (+ derece-$4$ tekillik) gerekir `[İSPAT]`. Dolayısıyla doğrudan $H_{\le 4}$ Macaulay matrisi hesaplanamaz `[İSPAT]`; `m=13` kırmak için `H-14C` benzeri katman indirgemesi gerekir `[SANI]`.

### 3. `per4_dc_15.tex` (Satır 216–387, 497–506) İçindeki `dc >= 10` Alt-İspatı
$m=9$ ($h=8$) için `prop:endpoint` ve $\dim K\le\dim\operatorname{Sing}(\operatorname{per}_4)=8$ (`prop:singdim`) eşitsizlikleri $\dim K=8, \rho_K=0$ zorlar `[İSPAT]`. Satır 497–506'daki $\det=p^4$ minoru $\rho_K=0\implies$ tüm $2\times 2$ permanentlerin $K$'da sıfır olmasını, `lem:zero2` ise böyle bir lineer uzayın $\dim K\le 4$ olmasını gerektirir (çelişki) `[İSPAT]`. Böylece bu $\sim 180$ satır bilgisayarsız $dc_{\mathbb{C}}(\operatorname{per}_4)\ge 10$'u verir; **tek boşluk** `lem:singF` içinde metni burada verilmeyen `lem:tenranktwo` atfıdır `[DOĞRULANMADI]`.

### Eleştirmen Saldırısı (Konu 2)

### 1) `dc_perm4_ge_10` Notunun Bilimsel Değeri Kaldı mı?
- **Hayır — bağımsız bir `perm_4` alt-sınır notu olarak bilimsel değeri kalmamıştır** `[SANI]`. Sheshadri (`per4_dc_15.tex`, satır `189–387` ve `497–504`) `lem:tenranktwo` + `prop:singdim` + `lem:regularity` + `prop:endpoint` + $\det=p^4$ + `lem:zero2` ile **sıfır bilgisayar sertifikasıyla** yalnızca $\ge 10$'u değil, $\dim K\le 4\implies m\ge 13$ ve $5\le\dim K\le 8\implies \rho_K\ge 4\implies m\ge 11$ üzerinden **$\mathrm{dc}_{\mathbb{C}}(\operatorname{per}_4)\ge 11$** sonucunu zaten kanıtlamaktadır `[İSPAT]`.
- Uzman 1'in "yeniden kullanılabilir modüler IMSC sertifikası" savunusu `perm_4` sonucunu kurtarmaz: `dc_perm4_ge_10.tex` (`423` satır + IMSC) hem daha uzun ve bilgisayara bağımlıdır hem de Sheshadri'nin `= 15` teoreminin gerisindedir `[İSPAT]`. `CHECK 3` (`F_skew5`: `1320/1365`, `e_4(L(X))`: `1365/1365`) `[KESİN HESAP]` da yeni bir $\underline{\mathrm{dc}}$ alt sınırı üretmemiştir `[DOĞRULANMADI]`.

### 2) Aynı Zincir `perm_5`'te `>= 14` (Hatta `>= 12`) Çıkarıyor mu?
- **Hayır; zincir şu anda `>= 14`'ü değil, koşulsuz olarak `>= 11`'i bile çıkarmamaktadır** `[İSPAT]`. Dört rapora göre zincir üç ayrı noktada tıkanmaktadır `[İSPAT]`:
  1. **$\operatorname{codim}\operatorname{Sing}(\operatorname{per}_5)\ge 10$ eksikliği:** `CHECK 2`'deki $R_{01}$ Jakobiyen rankı (`10/25`) `[KESİN HESAP]` yalnızca $\operatorname{codim}\operatorname{Sing}\le 10$ üst sınırıdır `[İSPAT]`. $L_{10}\subset\mathbb{C}^{25}$ üzerinde $D=10,12,15$ Macaulay matrisleri $92{,}378$–$1{,}307{,}504$ sütunlu olup ($D=10$'da yoğun `uint64_t` $\approx 92.5\text{ GB}$) hiç çalıştırılmamıştır `[DOĞRULANMADI]`.
  2. **$r=2,3,4$ korank tıkanması:** Uzman 2'nin açıkça belirttiği üzere, yalnızca $r=0,\ge 6$ ve `H-14A` (`6188/6188` `[KESİN HESAP]`) ile $r=5$ elenir; buna karşılık $r=4$ ($\operatorname{rk}\le 3$ uzayları $\mathrm{str}\le 4$'e çökmez), $r=3$ ($[t^5]$'teki $2\times 2$ $Q$-minörleri) ve $r=2$ (Alt-durum 2b; 2a ise $\operatorname{codim}\operatorname{Sing}\ge 9$ bekler) açık kaldığından $r=1$'e bile geçilememektedir `[DOĞRULANMADI]`.
  3. **$r=1$ içinde $D\le 10, w-D\ge 2$ (`m = 13`) duvarı:** $\operatorname{codim}\operatorname{Sing}(\operatorname{per}_5)=10$ ve $r=1$ varsayılsa bile `w-D=0` ($m\ge 14$) ve `w-D=1` ($m\ge 15$; `CHECK 2` $\det_4=b_3^4$ `[KESİN HESAP]`) dışında $(D,w-D)=(10,2)$ durumu $m=13$'ü açık bırakır; Uzman 1'in $\ge 13$ sonucu da `codim Sing = 10` varsayımına koşulludur `[İSPAT]`. `m=13`'ü doğrudan $H_{\le 4}(\operatorname{per}_5)$ ile kırmak $\binom{25}{5}^2=53{,}130^2$ adet derece-$15$ minör gerektirdiğinden hesaplanamaz `[İSPAT]`; $R_{01}$ (`m>=16`, `CHECK 2` `[KESİN HESAP]`) ise genel alt sınır değil tekil tabaka hesabıdır `[İSPAT]`.

### Uzman Raporları Özeti
- **Cebirsel geometri:** `lem:tenranktwo` yerini (`189–215`) yakaladı `[İSPAT]`; `perm_5`'te $\ge 13$'ü $\operatorname{codim}\operatorname{Sing}=10$ varsayımına koşullu verdi `[İSPAT]`.
- **Sınırlı rank & Sınır karmaşıklığı & Hesaplamalı cebir:** `r=2,3,4` ve `w-D>=2` tıkanmalarını, Sheshadri'nin bilgisayarsız $\ge 11$ gücünü ve $L_{10}$/$H_{\le 4}$ boyut engelini tutarlı biçimde ortaya koydu `[İSPAT]`. Mignon–Ressayre (2004) sınırı (`13`) geçilmediğinden yayın yalnızca yeni bir `perm_5` teoremi veya bağımsız `IMSC` yöntem katkısı üretilirse değer taşır `[SANI]`.

### Tur 2 — Uzman Yanıtları (Konu 2)

### Cebirsel geometri (Tur 2)
### 1) Kesin Yayın Kararı (`dc_perm4_ge_10`)
**Bağımsız bir `perm_4` alt-sınır notu olarak yayınlanmaz** [İSPAT]. Eleştirmen haklıdır: Sheshadri'nin bilgisayarsız alt-ispatı ($\dim K\le 4\implies m\ge 13$; $5\le\dim K\le 8\implies\rho_K\ge 4\implies m\ge 11$) aslında $\ge 10$'u değil **$\dc_{\C}(\per_4)\ge 11$'i** kanıtlar [İSPAT]. Bu nedenle 423 satır + IMSC sertifikalı $\ge 10$ notu `perm_4` sonucu olarak güncelliğini yitirmiştir; ancak bağımsız `IMSC` yöntemi veya yeni bir `perm_5` teoremi üzerine kurulursa değer taşır [SANI].

---

### 2) `perm_5`: Kanıtlanan vs. Tıkalı Sınır
* **Koşulsuz Kanıtlanan:** `H-14A` ile $\codim_{\C^{25}}\Sing_2(\per_5)\ge 13$ (`6188/6188`), `CHECK 2` ile $\det_4(\operatorname{Hess}_5|_4)=b_3^4$ ve $\codim\Sing(\per_5)\le 10$ (`10/25` Jakobiyen) gösterilmiştir [KESİN HESAP]. Zincir `perm_5` için **koşulsuz olarak $\ge 11$'i bile çıkarmamaktadır** [İSPAT].
* **Tıkalı Noktalar:**
  1. $\codim\Sing(\per_5)>4$ (`lem:regularity` / $r=2,3,4$ elemesi) ve $\ge 10$ ($a\ge 10$) kanıtlanmamıştır; $L_{10}$ Macaulay hesabı yapılmamıştır [DOĞRULANMADI].
  2. $\codim\Sing(\per_5)=10$ ve $r=1$ **varsayılsa bile**, $\codim\Sing_2\ge 13$ ile $b_3^4$ yalnızca $w-D\in\{0,1\}$ ($D\le 12$) durumlarını kapatır; $(D,w-D)=(10,2)$ durumu $m=13$'ü açık bırakır ve Mignon–Ressayre ($\ge 13$) sınırı aşılamaz [İSPAT]. ($R_{01}$ ve $R_{012}$ için $m\ge 16$ [KESİN HESAP] genel alt sınır değildir [İSPAT].)

### Sınırlı rank uzayları / temsil (Tur 2)
### Yayın Kararı
**`dc_perm4_ge_10` bağımsız bir `perm_4` alt-sınır notu olarak YAYINLANMAZ** [SANI]. Sheshadri'nin verdiği `lem:zero2` + `prop:singdim` + `lem:regularity` + `prop:endpoint` + $\det=p^4$ zinciri ($5\le\dim K\le 8\implies\rho_K\ge 4\implies m\ge 11$; $\dim K\le 4\implies m\ge 13$) bilgisayarsız olarak $\mathrm{dc}_{\mathbb{C}}(\mathrm{perm}_4)\ge 11$'i zaten verir (`lem:tenranktwo` için `REPORT` `Lemma 3.2` yeterli) [İSPAT]; satır `189–215` kesitte verilmediğinden Sheshadri'nin o bloğu [DOĞRULANMADI]. `CHECK 3` (`1320/1365`, `1365/1365`) doğrulanmıştır [KESİN HESAP], ancak yeni bir $\underline{\mathrm{dc}}$ alt sınırı üretmemiştir [DOĞRULANMADI].

### `perm_5`: Kanıtlanan vs Tıkalı Sınır
- **Kanıtlanan:** $r=0$ ve $r\ge 6$ elenir [İSPAT]. $r=5$'te $B^{-1}(\Sigma_2)\subseteq\mathrm{Sing}_2$ ($\mathrm{codim}\le 9$) çıkar [İSPAT] ve Theorem H-14A (`6188/6188`, $\mathrm{codim}\,\mathrm{Sing}_2\ge 13$) ile çelişir [KESİN HESAP]. $r=1$ içinde yalnız $w-D=0$ ($m\ge 14$) ve $w-D=1$ ($\det_4=b_3^4$, $m\ge 15$) rejimleri $\mathrm{Sing}_2$ içine düşer [İSPAT] ve H-14A ile elenir [KESİN HESAP]. Dolayısıyla `perm_5` için Mignon–Ressayre ($13$)'ü aşan **koşulsuz** bir alt sınır yoktur [İSPAT].
- **Tıkalı sınırlar:** (1) $\mathrm{codim}\,\mathrm{Sing}(\mathrm{perm}_5)=10$ ($L_{10}$ Macaulay) yok [DOĞRULANMADI]; (2) $r=2,3,4$ kapanmadığından $r=1$'e inilemiyor [DOĞRULANMADI]; (3) $\mathrm{codim}\,\mathrm{Sing}=10$ ve $r=1$ varsayılsa bile $(D,w-D)=(10,2)$ penceresi $m=13$'te tıkanır [İSPAT].

### Sınır karmaşıklığı uzmanı (Tur 2)
**1) Kesin Yayın Kararı: YAYINLANMAZ**
`dc_perm4_ge_10.tex` (ve `dc(perm_4) >= 12`) bağımsız bir alt-sınır notu olarak **yayınlanmaz** `[SANI]`. Sheshadri (2611.06658) $\mathrm{dc}_{\mathbb{C}}(\mathrm{perm}_4)=15$'i kanıtlamıştır; dahası verilen alıntı (satır 216–387, 497–506) — alıntı dışı kalan `lem:tenranktwo` `[DOĞRULANMADI]` sağlandığında — sıfır bilgisayarla yalnızca $\ge 10$'u değil $\ge 11$'i de verir `[İSPAT]`. `CHECK 3` (`F_skew5`: `1320/1365`, `e_4(L(X))`: `1365/1365`) `[KESİN HESAP]` da `perm_4` için yeni bir $\underline{\mathrm{dc}}$ alt sınırı üretmemektedir `[DOĞRULANMADI]`.

**2) `perm_5` İçin Kanıtlanan vs Tıkalı Sınır**
* **Kanıtlanan (birincil çıktılar):** `H-14A` ile $\operatorname{codim}_{\mathbb{C}^{25}}(\Sing_2(V(\per_5)))\ge 13$ (`6188/6188`, `p=32749`) ve $3$-sıfır-satır Jakobiyen rankı `15/25` `[KESİN HESAP]`; `CHECK 2` ile $\det_4(\operatorname{Hess}_5|_4)=b_3^4$ özdeşliği, $R_{01}$ Jakobiyen rankı `10/25` (yalnızca $\operatorname{codim}\Sing\le 10$ üst sınırı `[İSPAT]`) ve $R_{01}, R_{012}$ üzerinde $m\ge 16$ tabaka hesabı `[KESİN HESAP]`.
* **Tıkalı sınır:** Genel bir $m \ge 14$ (hatta koşulsuz $m \ge 11$) alt sınırı henüz kanıtlanmamıştır `[DOĞRULANMADI]`. $\operatorname{codim}\Sing(\per_5)\ge 10$ hesabı çalıştırılmadığı gibi, eleştiride anılan $r=2,3,4$ korank tıkanmaları ve $(D, w-D)=(10,2)$ engeli de birincil kanıt olmaksızın doğrulanmamıştır `[DOĞRULANMADI]`. $\lceil 5^2/2\rceil = 13$ sınırı geçilmedikçe yalnızca `IMSC` yöntemi veya yeni bir `perm_5` teoremi ayrı değerlendirilebilir `[SANI]`.

### Hesaplamalı cebir (Tur 2)
**Kesin Yayın Kararı: Mevcut hâliyle not olarak yayınlanmaz** `[SANI]`.

1. **`dc_perm4_ge_10` değerlendirmesi:** `per4_dc_15.tex` (`216–387, 497–506`) içinde atıf yapılan `lem:tenranktwo` metni burada görülmediğinden o basamak `[DOĞRULANMADI]`; bu lemma kabul edildiğinde kalan adımlar (`prop:endpoint`: $m\ge 17-\dim K+\lceil\rho_K/2\rceil$, $\dim K\le 8$, $\det=p^4$, `lem:zero2`) bilgisayarsız $\dim K\le 4\implies m\ge 13$ ve $\rho_K\ge 4\implies m\ge 11$ ile $\mathrm{dc}_{\mathbb{C}}(\operatorname{per}_4)\ge 11$'i verir `[İSPAT]`. `verify_independent_exact.py` (`11,440/11,440` `[KESİN HESAP]`) ve `CHECK 3` (`1320/1365`, `1365/1365` `[KESİN HESAP]`) yeni bir $\mathrm{dc}/\underline{\mathrm{dc}}$ sınırı üretmemiştir `[DOĞRULANMADI]`; çalışma ancak bağımsız `uint64_t` CSR/IMSC yöntem notu olarak değer taşır `[SANI]`.

2. **`perm_5` için kanıtlanan vs tıkalı sınır:**
   - **Kanıtlanan:** $\operatorname{codim}\operatorname{Sing}_2(\operatorname{per}_5)\ge 13$ (`k=13, D=5`: `9100 x 6188` tam rank), $R_{012}$'de $\operatorname{codim}=15$, $\det_4=b_3^4$ ve $R_{01}$'de $\operatorname{codim}\operatorname{Sing}(\operatorname{per}_5)\le 10$ doğrulanmıştır `[KESİN HESAP]`.
   - **Tıkalı sınır:** $\operatorname{codim}\operatorname{Sing}(\operatorname{per}_5)\ge 10$ için $L_{10}$ Macaulay ($92{,}378$–$1{,}307{,}504$ sütun; $D=10$ yoğun $\approx 92.5\text{ GB}$ `[İSPAT]`) çalıştırılmamıştır `[DOĞRULANMADI]`; $H_{\le 4}$ ($\binom{25}{5}^2$ derece-$15$ minor) doğrudan hesaplanamaz `[İSPAT]`. `r=2,3,4` ve `m=13` (`w-D=2`) tıkanmalarıyla koşulsuz yeni bir $\mathrm{dc}(\operatorname{per}_5)$ alt sınırı şu an **çıkmamaktadır** `[DOĞRULANMADI]`.

### Moderatör Kapanışı & Tur 2 'Neyi Kapattık?' Tablosu

# Konu 2 — Moderatör Sentetik Kapanışı

> **Moderatör Kısıt Notu:** Kural 5 gereği hiçbir araç çağrılmamıştır `[DOĞRULANMADI]`. Aşağıdaki kapanış yalnızca panelde sunulan birincil metin alıntılarına, elle türetilen kanıtlara ve raporlanan yerel hesap (`CHECK 1–3`, `H-14A`, `PART 1`, `verify_independent_exact.py`) çıktılarına dayanır `[İSPAT]`.

---

## 1. Kısalık ve Öz-Yeterlilik Kıyaslaması (`perm_4`)

| Yaklaşım / Artefakt | Kapsam ve Sonuç | Hacim & Sertifika Yükü | Öz-Yeterlilik & Doğrulama Durumu |
| :--- | :--- | :--- | :--- |
| **Sheshadri Tam Kanıt (`per4_dc_15.tex`)** | $\mathrm{dc}_{\C}(\per_4)=15$ hedefler `[DOĞRULANMADI]`. | `2359` satır + **28 Zenodo betiği** (`Archive A`: 15, `Archive B`: 13) `[DOĞRULANMADI]`. | Çekirdek cebirsel adımlar Konu 1'de türetildi `[İSPAT]`, ancak 28 betik ve minör/syzygy JSON sertifikaları çalıştırılmadığından tam kapanış koşulsuz değildir `[DOĞRULANMADI]`. |
| **Sheshadri Bilgisayarsız Çekirdek (`per4_dc_15.tex` içi)** | Yalnızca $\ge 10$ değil, `5 <= dim K <= 8 => rho_K >= 4 => m >= 11` ve `dim K <= 4 => m >= 13` üzerinden **$\mathrm{dc}_{\C}(\per_4)\ge 11$** verir `[İSPAT]`. | Panelde ~`180` satır (`216–387` + `497–506`); `lem:singF`'in kullandığı `lem:tenranktwo` (`189–215`) eklendiğinde ~`200` satır, **0 bilgisayar sertifikası** `[İSPAT]`. | Yalnız `216–387` alınırsa `lem:tenranktwo` dışarıda kalır `[DOĞRULANMADI]`; ancak `189–215` eklendiğinde (Konu 1'de türetilen `lem:tenranktwo` ve `CHECK 1`'de `[PASS]` basılan $O$ tanığı `[KESİN HESAP]`, ham girdileri basılmasa da `[DOĞRULANMADI]`) tamamen öz-yeterlidir `[İSPAT]`. |
| **Bizim Not (`dc_perm4_ge_10.tex`)** | $\mathrm{dc}_{\C}(\per_4)\ge 10$ (veya `perm_4` alt sınırı) hedefler `[DOĞRULANMADI]`. | `423` satır + **1 IMSC/Macaulay sertifikası** (`thm:sing1`) `[DOĞRULANMADI]`. | Sheshadri'nin bilgisayarsız çekirdeğinden **2 kat uzun**, bilgisayara bağımlı ve `r=3` (`Atkinson1983`/`EH1988`) ile tam metni verilmeyen dosya bütünlüğü açısından eksiktir `[DOĞRULANMADI]`; yalnızca modüler `uint64_t` CSR/IMSC + `lem:skewsquare` mekanizması yeniden kullanılabilir yöntem sunar `[SANI]`. |

---

## 2. `perm_5` Genellemesi: `2n+1 = 11`, MR04 `13`, Kanıtlanan vs. Tıkalı Adımlar ve `>= 14` Şansı

* **Ölçek Referansları:** $n=5$ için `2n+1 = 11` ($\codim\Sing=10$ varsayımı altında basit izotropi sınırı $10+1=11$ `[İSPAT]`) ve Mignon–Ressayre (2004) sınırı $\lceil 5^2/2\rceil = 13$ (`MR04 = 13`) `[SANI]` mevcut kıyas eşikleridir; ayrıca genel $n$'de Sheshadri'nin `prop:endpoint` eşitsizliği ($m\ge 1+D+\lceil\rho_K/2\rceil$) $R_{01}$ tabakası ($\dim=n(n-2)$, $D=2n$, $\rho_{R_{01}}\le 2n$) üzerinde yalnızca $3n+1$ verdiğinden asimptotik $n^2/2$ bariyerini tek başına aşamaz `[İSPAT]`.
* **Bizim Zincirin Bugün Koşulsuz Kanıtlayabildiği Adımlar:**
  1. $r=0$ ($[t^0]=\det(I_m)=1\neq 0$) ve $r\ge 6$ ($[t^5]=0$) elenir `[İSPAT]`.
  2. `H-14A` (`k=13, D=5, p=32749`, `9100 x 6188` tam rank `6188/6188`) ile $\codim_{\C^{25}}\Sing_2(\per_5)\ge 13$ ve `PART 1` ile $R_{012}$ üzerinde $\codim=15$ doğrulanır `[KESİN HESAP]` ($\mathbb{F}_p\to\mathbb{Q}$ kaldırmasıyla tam rank kesindir `[İSPAT]`).
  3. $r=5$ elenir: $B^{-1}(\Sigma_2)\subseteq\Sing_2(V(\per_5))$ ($\codim\le 9$) `[İSPAT]`, `H-14A` ($\ge 13$) ile çelişir `[KESİN HESAP]`.
  4. `CHECK 2` ile $\det_4(\operatorname{Hess}_5|_4)=b_3^4$ ($\rho(z)>0\implies\rho(z)\ge 4$), $R_{01}$ Jakobiyen rankı `10/25` (yalnızca $\codim\Sing(\per_5)\le 10$ üst sınırı `[İSPAT]`), $R_{012}$ Jakobiyen rankı `15/25` ve $R_{01}, R_{012}$ özel tabakaları için $m\ge 16$ doğrulanır `[KESİN HESAP]` (genel alt sınır değildir `[İSPAT]`).
  5. `r=1` içinde *koşullu* iki uç rejim elenir: $w-D=0$ ($m\ge 14$, Skew-Square $k=1,2,3$ ile $\per_5\in I_W^3$) ve $w-D=1$ ($M_z U, M_z^2 U\subseteq U^\perp$, $\dim E=2$ ve $\det_4=b_3^4 \implies W^\perp\subseteq\Sing_2 \implies D\ge 13 \implies m\ge 15$) `[İSPAT]` + `[KESİN HESAP]`.
* **Açık Kalan / Tıkalı Adımlar (Bugün Koşulsuz `>= 11` Bile Çıkmıyor!):**
  1. **$\codim\Sing(\per_5)\ge 10$ (veya $>4$) eksikliği:** `10/25` yalnızca üst sınırdır `[İSPAT]`; $L_{10}\subset\C^{25}$ üzerinde derece-$D$ Macaulay matrisleri $25\binom{D+5}{9}\times\binom{D+9}{9}$ boyutunda olup ($D=10$: $125{,}125\times 92{,}378$, yoğun `uint64_t` $\approx 92.5\text{ GB}$; $D=12$: $607{,}750\times 293{,}930$; $D=15$: $4{,}199{,}000\times 1{,}307{,}504$ `[İSPAT]`) hiç çalıştırılmamıştır `[DOĞRULANMADI]`.
  2. **$r=4, 3, 2$ korank duvarı:** $r=4$'te $4\times 4$ $\rk\le 3$ uzayları $\mathrm{str}\le 4$'e çökmez `[DOĞRULANMADI]`; $r=3$'te $[t^5]$ içindeki $2\times 2$ $Q$-minörleri $\mathrm{str}\le 4$ vermez `[İSPAT]`; $r=2$ (Alt-durum 2b açık; 2a $\codim\Sing\ge 9$ bekler) kapanmamıştır `[DOĞRULANMADI]`. Bu nedenle $r=1$'e inilememektedir `[DOĞRULANMADI]`.
  3. **Kritik $m=13$ ($w-D=2$) Duvarı — `>= 14` Şansı Var mı?:** $\codim\Sing(\per_5)=10$ ve $r=1$ **varsayılsa bile**, $m=13$ ($w=12$) için $(D, w-D)=(10, 2)$ ($\dim K=15, \rho_K\le 4$) durumu elenmez; bu yüzden endpoint formülü ($m\ge 26-\dim K+\lceil\rho_K/2\rceil$) dahi yalnızca **$m\ge 13$** (MR04 ile aynı) verir, **$\ge 14$ çıkarmaz** `[İSPAT]`. $m=13$'ü doğrudan $H_{\le 4}(\per_5)$ ile kırmak ise $\binom{25}{5}^2 = 53{,}130^2$ adet derece-$15$ minor gerektirdiğinden hesaplanamaz `[İSPAT]`.
     * **Moderatör Hükmü (`>= 14` şansı):** Mevcut zincirle bugün `>= 14` (hatta koşulsuz `>= 11`) **çıkmamaktadır** `[İSPAT]`. `>= 14` şansı ancak (i) $L_{10}$ seyrek CSR/IMSC ile $\codim\Sing=10$ sertifikası, (ii) $r=2,3,4$ elemesi ve (iii) $(D,w-D)=(10,2)$'yi dışlayan yeni bir `H-14C` / $\mathcal{H}_{\le 4}$ katman indirgemesi geliştirilirse doğabilir `[SANI]`.

---

## 3. NET YAYIN KARARI

**KARAR: `dc_perm4_ge_10` (düzeltilmiş `>= 10` veya `>= 12` hâliyle bile) bağımsız bir `perm_4` alt-sınır notu olarak YAYINLANMAZ `[SANI]`.**

**Maddeli Gerekçe:**
1. **SOTA Gerisinde Kalma:** Sheshadri (`2611.06658`) $\mathrm{dc}_{\C}(\per_4)=15$'i hedeflemiştir; bu durumda `>= 10` veya `>= 12` sonucu mevcut literatür sınırının gerisindedir `[SANI]`.
2. **Sheshadri İçi Bilgisayarsız `>= 11` Gerçeği (`>= 10` vs `>= 12` Farkı):** `per4_dc_15.tex` içindeki ~`200` satırlık bilgisayarsız alt-kanıt (`189–387` + `497–506`) sıfır sertifika ile zaten **$\mathrm{dc}_{\C}(\per_4)\ge 11$** vermektedir `[İSPAT]`. Dolayısıyla **düzeltilmiş `>= 10`** Sheshadri'nin bilgisayarsız alt-kanıtının bile altındadır `[İSPAT]`; varsayımsal bir **`>= 12`** notu `11`'i yalnızca 1 puan aşsa da hâlâ `15`'in gerisinde kalır, ayrıca Sheshadri'ye göre daha uzun ve bilgisayara bağımlıdır `[SANI]`.
3. **Sınır Karmaşıklığı ($\underline{\mathrm{dc}}$) Kazancı Yok:** `CHECK 3` (`F_skew5`: `1320/1365`, `e_4(L(X))`: `1365/1365` `[KESİN HESAP]`) `perm_4` için yeni bir $\underline{\mathrm{dc}}$ alt sınırı üretmemiştir `[DOĞRULANMADI]`.
4. **Tek Olası Yeniden Konumlandırma:** Bağımsız `uint64_t` CSR/IMSC tekniği, `perm_4` alt-sınırı olarak değil, `perm_5` üzerinde `H-14A` ($\codim\Sing_2\ge 13$) ve yeni bir `perm_5` teoremi (`>= 14` hedefi) ekseninde yeniden yazılırsa değer taşır `[SANI]`.

---

## 4. TUR 2 — 'NEYİ KAPATTIK?' TABLOSU

| Konu | Karar | Dayanak Etiket | Açık Kalan |
| :--- | :--- | :--- | :--- |
| **Sheshadri İçi Bilgisayarsız Alt-Kanıt (`per4_dc_15.tex`)** | `189–387` + `497–506` (~`200` satır) ile **$\mathrm{dc}_{\C}(\per_4)\ge 11$** verildiği kapatıldı (`216–387` kesitinde `lem:tenranktwo` eksikliği işaretlendi). | `[İSPAT]` / `[KESİN HESAP]` / `[DOĞRULANMADI]` | `lem:tenranktwo` metin eklemesi ve `prop:singdim` tanığı $O$'nun ham girdileri (`CHECK 1` `[PASS]` basılıdır) `[DOĞRULANMADI]`. |
| **`dc_perm4_ge_10` Yayın Kararı (`>= 10` ve `>= 12`)** | Bağımsız `perm_4` alt-sınır notu olarak **YAYINLANMAZ** hükmü kesinleştirildi; `>= 10` bilgisayarsız `>= 11`'in gerisindedir, `>= 12` de SOTA (`15`) altında kalır. | `[İSPAT]` / `[SANI]` | Yöntemin `perm_5` / `IMSC` ekseninde yeniden yazılması `[SANI]`. |
| **$\underline{\mathrm{dc}}(\per_4)$ (`CHECK 3`)** | `F_skew5` (`1320/1365`) ve `e_4(L(X))` (`1365/1365`) doğrulandı; ancak `perm_4` için yeni bir $\underline{\mathrm{dc}}$ alt sınırı vermediği kapatıldı. | `[KESİN HESAP]` / `[DOĞRULANMADI]` | $\underline{\mathrm{dc}}(\per_4)$ için yeni alt sınır mekanizması `[DOĞRULANMADI]`. |
| **`perm_5` Kanıtlanan Kısmi Sonuçlar** | $r=0,\ge 6$ elemesi, $\codim\Sing_2(\per_5)\ge 13$ (`H-14A` `6188/6188`), $r=5$ elemesi, $\det_4(\operatorname{Hess}_5|_4)=b_3^4$, $r=1$ ($w-D\in\{0,1\}$ koşullu elemesi) ve $R_{01},R_{012}$ özel tabaka sınırları (`m>=16`) kapatıldı. | `[İSPAT]` / `[KESİN HESAP]` | Bu kısmi adımların tek başına genel $m\ge 14$ (hatta koşulsuz $m\ge 11$) üretmediği netleştirildi `[İSPAT]`. |
| **`perm_5` Tıkanmaları & `>= 14` Şansı** | Bugün için `>= 14` (ve koşulsuz `>= 11`) **çıkmadığı** kapatıldı; $L_{10}$ ($\approx 92.5\text{ GB}$ yoğun), $r=2,3,4$ korankları, $(D,w-D)=(10,2)$ ($m=13$ duvarı) ve doğrudan $H_{\le 4}$ ($\binom{25}{5}^2$ minör) hesaplanamazlığı belirlendi. | `[İSPAT]` / `[DOĞRULANMADI]` | (1) $L_{10}$ seyrek IMSC sertifikası, (2) $r=2,3,4$ korank kapanışı, (3) `H-14C` / $\mathcal{H}_{\le 4}$ katman indirgemesi `[DOĞRULANMADI]`. |
| **Genel $n$'de Endpoint Bariyeri** | $R_{01}$ tabakası ($3n+1$) nedeniyle Sheshadri'nin endpoint eşitsizliğinin tek başına asimptotik $n^2/2$ bariyerini aşamadığı kapatıldı. | `[İSPAT]` | Tabaka-üstü yeni alt sınır fikirleri `[SANI]`. |

---

## KONU 3 — Sınır Karmaşıklığı (dc-bar): R₉⁽⁴⁾ = P·Q Elle İspat Denemesi ve Gizli Varsayım Denetimi

### Adım 1 — Sınır Karmaşıklığı Uzmanı Elle İspat Denemesi

### KISIM A — $\overline{\mathcal{D}_9^{\mathrm{hom}}}$ Üzerinde Elle İspat ve Polinomluk Denetimi

**1) $\mathcal{D}_9^{\mathrm{hom}}$ üzerindeki her $F$ için $\widetilde{P}^{(4)}(F)=0$ veya $Q^{(4)}(F)=0$:**
$A_0=\operatorname{diag}(I_w,0_r)$ ($w+r=9$) ve $L=\begin{pmatrix}A&U\\V^T&W_0\end{pmatrix}$ yazalım ($F=0$ için tüm minörler $0$ `[İSPAT]`).
* **$r=0$ ve $r\ge 5$:** $r=0$'da $[t^0]=1\neq 0$ (boş); $r\ge 5$'te son $r$ satır sabit-$0$ olduğundan $[t^4]\equiv 0\implies F=0$ `[İSPAT]`.
* **$r=4$:** $F=\det_4(W_0)$; $\{\operatorname{rk} W_0\le 2\}\subseteq\Sing(V(F))$ kodim $\le 4<8\implies L_8\setminus\{0\}$ ile kesişir $\implies \widetilde{P}^{(4)}(F)=0$ `[İSPAT]`.
* **$r=3$:** $[t^3]=\det_3(W_0)=0$ ve $F=[t^4]=-\operatorname{tr}(\operatorname{adj}(W_0)V^TU)$ `[İSPAT]`. Atkinson–Dieudonné üç dal verir (`[DOĞRULANMADI]`, dış teorem):
  (i) Sıfır sütunlu $W_0$: $\operatorname{adj}(W_0)$ yalnızca $3$. satırda nonzero olup $F=\sum_{i=1}^3 c_i(v_i^Tu_3)$ ($c_i$: $3\times 2$ bloğun $2\times 2$ minörleri); $\{c_i=v_i^Tu_3=0\}\subseteq\Sing(V(F))$ kodim $\le 2+3=5<8$ `[İSPAT]`.
  (ii) **$2\times 2$ sıfır bloklu sıkıştırma** ($W_0=\begin{pmatrix}a&b&c\\d&0&0\\e&0&0\end{pmatrix}$): $\operatorname{adj}(W_0)$'ın tek nonzero parçası sağ-alt $(-c,b)^T(e,-d)$ olup $F\in\langle b,c\rangle\cdot\langle d,e\rangle$; böylece $\{b=c=d=e=0\}\subseteq\Sing(V(F))$ kodim $\le 4<8$ `[İSPAT]`.
  (iii) Ters-simetrik $W_0$: $\operatorname{adj}(W_0)=\ell\ell^T\implies F\in\langle\ell_1,\ell_2,\ell_3\rangle^2\implies\operatorname{codim}\Sing\le 3<8$ `[İSPAT]`. Üç dalda da $\widetilde{P}^{(4)}(F)=0$.
* **$r=2$:** $\det_2(W_0)=0$ olduğundan `prop:cubic-regularity` argümanıyla $W_0=\begin{pmatrix}\ell_1&\ell_2\\0&0\end{pmatrix}$ (veya devriği) seçilir `[İSPAT]`. $[t^3]=\ell_2(v_2^Tu_1)-\ell_1(v_2^Tu_2)=0$ üç alt-durum verir: (i) $\ell_1,\ell_2$ bağımsızsa $v_2^Tu_j=\ell_jq_0$ ve $F=\ell_1(v_2^TAu_2-q_0v_1^Tu_2)-\ell_2(v_2^TAu_1-q_0v_1^Tu_1)$; (ii) $\ell_2=0\neq\ell_1$ ise $v_2^Tu_2=0$ ve $F=\ell_1(v_2^TAu_2)-(v_1^Tu_2)(v_2^Tu_1)$; (iii) $\ell_1=\ell_2=0$ ise $F=q_{11}q_{22}-q_{12}q_{21}$. Her üçünde $4$ üretecin ortak sıfırı $\Sing(V(F))$'tedir ($\operatorname{codim}\le 4<8\implies\widetilde{P}^{(4)}(F)=0$) `[İSPAT]`.
* **$r=1$ ($w=8$):** $D\le 7$ ise $F=-v^TA^2u\in I_W^2\implies W^\perp\subseteq\Sing(V(F))$ ($\operatorname{codim}\le 7\implies \widetilde{P}^{(4)}(F)=0$) `[İSPAT]`. $D=8$ ($w-D=0$) ise Double-Koszul ($A_{13}(X_0)=0$) + Skew-Square ($(A_{11}(X_0)^2K)^T=-A_{11}(X_0)^2K$) ile $\operatorname{Hess}(F)|_{W^\perp}\equiv 0$ ve $\dim(W^\perp\cap L_{12})\ge 4\implies Q^{(4)}(F)=0$ `[İSPAT]`.

**2) Polinomluk Denetimi (`P^{(4)}` vs $\widetilde{P}^{(4)}$):**
`verify_round13_strassen.py`'deki `P^{(4)} = det6 * det_s6 * det_s7 * det_s8` bir **rasyonel fonksiyondur**: `rref_mod_p_with_det` $A_{6,\mathrm{piv}}^{-1}$ terslemesiyle `det6` paydalı `C_table` üretir; `step_imsc_det` ise çoklu kaydırmalarda `C_D` kullanarak `M_syz` kurduğundan `det_s6, det_s7, det_s8` yüksek ara-pivot kuvvetleri paydası taşıyabilir `[İSPAT]`. Buna karşılık $\mathrm{perm}_4$'ün tam ranklı pivot satırları $I_1$ üzerindeki maksimal minör $\widetilde{P}^{(4)}(F):=\det_{11440}(\mathcal{M}_9(F;L_8)_{I_1})\in\mathbb{Z}[F]_{11440}$ paydasız homojen polinomdur; `P^{(4)}(\mathrm{perm}_4)\equiv 5223 \pmod{32749}` `[KESİN HESAP]` $\operatorname{rk}\mathcal{M}_9(\mathrm{perm}_4;L_8)=11440$ sağladığından böyle bir $I_1$ vardır ve $\mathcal{D}_8^{\mathrm{hom}}$'da $\ker\mathcal{M}_9\neq 0\implies\widetilde{P}^{(4)}=0$ kapanışa geçer `[İSPAT]`.

**3) `R_{10}^{(4)} = P^{(4)}T^{(4)}Q^{(4)}` Denetimi:**
$Q^{(4)}(F)=\det_{1365}(\mathcal{M}_4^{\mathrm{Sing}_2}(F;L_{12})_{I_2})$ tek RREF adımıyla doğrudan derece-$1365$ polinomdur `[İSPAT]`. `T^{(4)}` (`D=6->7->8`) yine IMSC pivot çarpımı olduğundan rasyoneldir; gerçek polinom $\widetilde{T}^{(4)}(F):=\det_{12870}(\mathcal{M}_8^{\mathcal{H}_{\le 4}}(F;L_9)_{I_3})$ ($\deg_F\in\{1,3\}$ satırlar) olur `[İSPAT]`. `verify_round15_strassen.py` satır 402–434 yalnızca sentetik `H_sym` test etmiştir (`[DOĞRULANMADI]`), fakat Teorem 15B (`\operatorname{rk}\operatorname{Hess}(F)|_{W^\perp}\le 2`) teorik olarak $m=10,D=8$ üzerinde tüm $3\times 3$ blok minörlerini sıfırlayıp $\widetilde{T}^{(4)}(F)=0$ zorlar; dolayısıyla $\widetilde{R}_{10}^{(4)}=\widetilde{P}^{(4)}\widetilde{T}^{(4)}Q^{(4)}$ polinomu $\overline{\mathcal{D}_{10}^{\mathrm{hom}}}$'da sıfırlanır (`perm_4`'te $\not\equiv 0$ `[KESİN HESAP]`) `[İSPAT]`.

---
### KISIM B — Gerçek Sınır Karmaşıklığı $\mathcal{B}_9^{(4)}$ ve Tıkanma Noktaları

**1) $\overline{\mathcal{D}_9^{\mathrm{hom}}}\subseteq \mathcal{B}_9^{(4)}$ Eşitlik mi?**
Kapsama doğrudur `[İSPAT]`, ancak **eşitlik kanıtlanamamıştır** `[DOĞRULANMADI]`. $\mathcal{D}_9^{\mathrm{hom}}$'da $\deg\neq 4$ terimleri limit öncesi özdeşçe sıfır iken, $\mathcal{B}_9^{(4)}$'te $\det_9(A_0(\varepsilon)+L_\varepsilon(X))=F_0(X)+O(\varepsilon)$ eğrileri alt/üst derece terimlerini yalnızca $\varepsilon\to 0$'da sadeleştirir (`2611.03554` $Q_{3,0}=\lim_{t\to 0}t^{-1}\det_3(A(x)+tS)$ örneği farklı derecelerde tam/sınır ayrımını gösterir `[İSPAT]`).

**2) $F_\varepsilon(X)=\det_9(A_0(\varepsilon)+L_\varepsilon(X))\to F_0(X)$ Eğrisinde Tıkandığımız Adımlar:**
* **`ŞU ADIMDA TIKANDI #1` (SNF ve Tam Rank):** $\mathbb{C}[[\varepsilon]]$ üzerinde $A_0(\varepsilon)\sim\operatorname{diag}(\varepsilon^{a_1},\dots,\varepsilon^{a_9})$ Smith normal formuna girer. Tüm $a_i<\infty$ iken $A_0(\varepsilon)$ $\mathbb{C}((\varepsilon))$'da **tam rank $9$** olabilir; $\varepsilon\neq 0$'da $F_\varepsilon$ homojen değildir ve sabit bir $r=\operatorname{corank}(A_0)$ ayrımına çökmez `[İSPAT]`.
* **`ŞU ADIMDA TIKANDI #2` ($\varepsilon^{-p}$ Kutupları ve `[t^2]=0` Bozulması):** $\varepsilon^{-a_i}$ satır/sütun ölçeklemeleri $L_\varepsilon(X)$'te $\varepsilon^{-p}$ kutupları üretir; $[t^2]_\varepsilon=-v_\varepsilon^T u_\varepsilon$ özdeşçe $0$ kalmaz, alt $\varepsilon$-mertebeli $[t^2]$ terimleri $\varepsilon^{-p}$ çarpanlarıyla $[t^4]_\varepsilon$'ye sızarak $W$ izotropisini (`[t^2]=0`) bozar `[İSPAT]`.
* **`ŞU ADIMDA TIKANDI #3` (Double-Koszul ve Skew-Square Çöküşü):** Eşit olmayan $\varepsilon$-değerlemeleri yüzünden $[t^3]_\varepsilon$ diğer derecelerden gelen $\varepsilon$-terimleriyle sadeleşebilir; böylece tek bir $W\subset\mathbb{C}^{16}$ üzerinde $A_{13}(X_0)=0$ ve $(A_{11}^2K)^T=-A_{11}^2K$ zorlanamaz `[İSPAT]`.

**Net Hüküm:** $\widetilde{R}_9^{(4)}$ ve $\widetilde{R}_{10}^{(4)}$ yalnızca homojen dilim kapanışları $\overline{\mathcal{D}_9^{\mathrm{hom}}}$ ve $\overline{\mathcal{D}_{10}^{\mathrm{hom}}}$'dan $\mathrm{perm}_4$'ü ayırır `[İSPAT]`. Gerçek $\underline{\mathrm{dc}}_{\mathbb{C}}(\mathrm{perm}_4)\ge 10$ (ve $\ge 11$) iddiası yukarıdaki SNF/kutup boşlukları nedeniyle **`[DOĞRULANMADI]`** (eksik) kalır `[İSPAT]`.

### Adım 2 — Uzman Çapraz Denetimleri

### Cebirsel geometri
### 1) Kapanış–Kesişim Ayrımı ve Özdeşleştirme Kontrolü
* $\mathcal{D}_m\cap\C[X]_4\subseteq \overline{\mathcal{D}_m}\cap\C[X]_4$ her zaman doğrudur ve sağ taraf $\C[X]_4$'te kapalı olduğundan $\overline{\mathcal{D}_m^{\mathrm{hom}}}\subseteq \mathcal{B}_m^{(4)}$ elde edilir [İSPAT]. Ters kapsama genel olarak **yanlıştır**: kapanış ile kapalı altuzay kesişimi yer değiştirmez [İSPAT]. $\mathcal{D}_m\setminus\C[X]_4$'teki eğriler (homojenleştirilmiş hâlde $z^{m-4}F\in\overline{\mathrm{End}\cdot\det_m}$) $\varepsilon\neq 0$'da alt/üst derece terimleri ve $\varepsilon^{-p}$ kutupları taşıyıp $\varepsilon\to 0$'da bunları sadeleştirebilir; böylece $\mathcal{D}_m^{\mathrm{hom}}$'un $[t^2]=0, [t^3]=0$ kısıtlarına uymadan $\C[X]_4$'e yakınsayabilirler [İSPAT]. (CHECK 3'teki homojen olmayan $\det_9(I_9+L)$'nin $e_4$ parçası da $Q^{(4)}\neq 0$ vererek homojen olmayan yapıların farklı davrandığını teyit eder [KESİN HESAP].)
* `verify_round14_strassen.py` (satır 15–16) ve `REPORT.md` (satır 585) bu oturumdaki birincil metinlerde verilmediğinden iki kümeyi özdeşleştirip özdeşleştirmedikleri **[DOĞRULANMADI]**.

---

### 2) Kısım A ($\widetilde{P}^{(4)}Q^{(4)}\equiv 0$ on $\overline{\mathcal{D}_9^{\mathrm{hom}}}$) Denetimi
* **Polinomlaştırma ve Boyut Teoremi:** Rasyonel `P^{(4)}` yerine tam ranklı $I_1,I_2$ altmatrisleriyle tanımlanan $\widetilde{P}^{(4)}(F)=\det_{11440}(\mathcal{M}_9(F;L_8)_{I_1})$ ve $Q^{(4)}(F)=\det_{1365}(\mathcal{M}_4^{\Sing_2}(F;L_{12})_{I_2})$ homojen polinomlardır; koni $\Sing(V(F))\cap L_8\neq\{0\}$ ($\codim\le 7$, Boyut Teoremi) $\ker\mathcal{M}_9\neq 0 \implies \widetilde{P}^{(4)}(F)=0$ verir ve sıfırlanma Zariski kapanışına taşınır [İSPAT].
* **$r=0,\ge 5,4,2,1$ dalları:** Tüm $\codim\le 4,7$ sınırları ile $r=1,D=8$'deki Double-Koszul + Skew-Square $\implies Q^{(4)}=0$ adımı sağlamdır [İSPAT].
* **Hüküm:** Kısım A bütünüyle `[İSPAT]` **değildir**; iki bağımlılık açıktır: (i) $r=3$'te Atkinson–Dieudonné teoremi (ve $2\times 2$ sıfır bloklu sıkıştırma dalı) burada kanıtlanmadan dışarıdan alınmıştır **[DOĞRULANMADI]**; (ii) `P^{(4)}(\perm_4)\equiv 5223 \pmod{32749}` ve $I_1$'in varlığı CHECK 1–3'te verilmediğinden **[DOĞRULANMADI]** ($I_2$ ise CHECK 3'te $1365/1365$ [KESİN HESAP]).

---

### 3) `arXiv:2611.03554` Örneklerinin Öğrettikleri
* $Q_{3,0}=\lim_{t\to 0} t^{-1}\det_3(A(x)+tS)$ (Kısım B), $t^{-1}$ kutbuyla homojen olmayan determinantal eğrilerin kesin $\mathrm{dc}$'yi aşan sınırlara nasıl çöktüğünü göstererek Kısım B'deki `#1–#3` SNF/kutup tıkanmasını somutlaştırır [İSPAT].
* $Q_{3,1}$ ($\underline{\mathrm{dc}}=4, \mathrm{dc}\ge 6$, CHECK 3 [KESİN HESAP]), $\codim 3$ tekil kümesi yüzünden $P^{(4)}(Q_{3,1})=0$ verir; dolayısıyla $\widetilde{P}^{(4)}$ sınır karmaşıklığını tek başına yükseltemez ve $\overline{\mathcal{D}_9^{\mathrm{hom}}}$ ayrımı $Q^{(4)}$'e muhtaçtır [İSPAT].
* $Q_{5,0}$ ve $\mathcal{K}_{2,0}$ verilen birincil metinlerde bulunmadığından bunlara dair çıkarımlar **[DOĞRULANMADI]**.

### Sınırlı rank uzayları / temsil
### 1) $r=3$ Vakası: $2\times 2$ Sıfır Bloğu ve Atkinson–Dieudonné Denetimi
`dc_perm4_ge_10.tex` (`prop:corank1`) yalnızca sıfır satır/sütun ve $\mathfrak{so}_3$ durumlarını listeler; oysa $W_0=\begin{pmatrix}a&b&c\\d&0&0\\e&0&0\end{pmatrix}$ biçimindeki $2\times 2$ sıfır bloklu uzayın sıfır satırı/sütunu yoktur, dolayısıyla `dc_perm4_ge_10.tex` metninde gerçek bir vaka atlaması vardır [İSPAT]. Ancak bu vaka $R_9^{(4)}$ ve $R_{10}^{(4)}$ ispatlarında yeni bir karşı-örnek açmaz [İSPAT]. Elle kofaktör hesabıyla $\mathrm{adj}(W_0)$'ın yalnızca sağ-alt $2\times 2$ bloğu sıfır değildir:
$$\mathrm{adj}(W_0)=\begin{pmatrix}0&0&0\\0&-ce&cd\\0&be&-bd\end{pmatrix}=\begin{pmatrix}0\\-c\\b\end{pmatrix}\begin{pmatrix}0&e&-d\end{pmatrix},$$
böylece $Q=V^T U=(q_{ij})$ için $F=-\mathrm{tr}(\mathrm{adj}(W_0)Q)=c(eq_{22}-dq_{32})-b(eq_{23}-dq_{33})\in\langle b,c\rangle\cdot\langle d,e\rangle$ olur [İSPAT]. Buradan $\mathrm{str}(F)\le 2<4$ ve $\{b=c=d=e=0\}\subseteq\mathrm{Sing}(V(F))$ elde edilir; $\mathrm{codim}\,\mathrm{Sing}(V(F))\le 4\le 7$ olduğundan $L_8\setminus\{0\}$ ile kesişir ve $\widetilde{P}^{(4)}(F)=0$ ($\widetilde{R}_9^{(4)}=\widetilde{R}_{10}^{(4)}=0$) zorlanır [İSPAT]. (Kısım A $r=3$(i)'de $(e_3^T V^T U)c=\sum_i (v_3^T u_i)c_i$ yerine $v_i^T u_3$ yazılmıştır, fakat $\mathrm{codim}\le 5<8$ ve $\mathrm{str}\le 3$ değişmez [İSPAT].) Yine de üç dalın tamlığı için kullanılan Atkinson–Dieudonné / EH88 sınıflandırması metinde kanıtlanmadığından dış teorem adımı [DOĞRULANMADI].

### 2) Laurent Sınırında $A_0(\varepsilon)=\mathrm{diag}(\varepsilon^{a_1},\dots,\varepsilon^{a_9})$ ve $r$ Çöküşü
$\mathbb{C}(\!(\varepsilon)\!)$ üzerinde $a_1\le\dots\le a_9<\infty$ için $A_0(\varepsilon)=\mathrm{diag}(\varepsilon^{a_1},\dots,\varepsilon^{a_9})$ **tam rank $9$** ($\mathrm{corank}_{\mathbb{C}(\!(\varepsilon)\!)}=0$) olur; sabit $0_r$ bloğu yoktur ve $\varepsilon=0$'daki $r_0$ ölçeklemeye duyarlıdır [İSPAT]. Örneğin $r_0=1$ iken $M_\varepsilon(tX)=\begin{pmatrix}I_8+tA_\varepsilon&tU_\varepsilon\\tV_\varepsilon^T&\varepsilon^{a_9}+tW_\varepsilon\end{pmatrix}$ ($a_9>0$) Schur tümleyeniyle
$$F_\varepsilon(tX)=\det(I_8+tA_\varepsilon)\Big(\varepsilon^{a_9}+tW_\varepsilon-t^2 v_\varepsilon^T u_\varepsilon+t^3 v_\varepsilon^T A_\varepsilon u_\varepsilon-t^4 v_\varepsilon^T A_\varepsilon^2 u_\varepsilon+\cdots\Big)$$
verir [İSPAT]. $[t^4]F_\varepsilon$ terimi yalnız $-v_\varepsilon^T A_\varepsilon^2 u_\varepsilon$'yi değil, $\det(I_8+tA_\varepsilon)$ üzerinden $\varepsilon^{a_9}e_4(A_\varepsilon)+W_\varepsilon e_3(A_\varepsilon)-(v_\varepsilon^T u_\varepsilon)e_2(A_\varepsilon)+(v_\varepsilon^T A_\varepsilon u_\varepsilon)e_1(A_\varepsilon)$ toplamını içerir [İSPAT]. $\varepsilon^{-p}$ kutuplu $A_\varepsilon,W_\varepsilon$ ile $O(\varepsilon)$'lık $v_\varepsilon^T u_\varepsilon$ çaprazlaşıp $\varepsilon\to 0$'da sonlu katkı bırakabileceğinden $v_0^T u_0=0$ ($W$ izotropisi), Double-Koszul ve Skew-Square bozulur [İSPAT].

### Hesaplamalı cebir
### 1. IMSC `P^(4)`, `T^(4)` ve Doğrudan `M_9` / `Q^(4)` Polinomluğu
- **`P^(4)` rasyonel fonksiyondur:** `verify_round13_strassen.py`'de `rref_mod_p_with_det`, pivot terslemesiyle (`pow(piv_val, p-2, p)`) `det6` paydalı `C_table` üretir; `step_imsc_det` ise `M_syz`'yi `C_D` satırlarından kurduğundan önceki pivot minörleri paydaya taşınır `[İSPAT]`. Dolayısıyla `p4_inv = det6 * det_s6 * det_s7 * det_s8` çarpımı $F$'nin katsayılarında polinom değil **rasyonel fonksiyondur** `[İSPAT]`. (`T^(4)` kaynak kodu burada bulunmadığından yapısı `[DOĞRULANMADI]`.)
- **$M_6(F;L_8)$ rank düşüşü ve $\widetilde{P}^{(4)}$:** $M_6(F;L_8)$ rankı $1584$'ün altına indiğinde sabit pivot setinde `det6=0` olup `C_6` tanımsızlaşır (dinamik pivotlamada ise rasyonel ifade dal değiştirir); böylece `P^{(4)}` Zariski-kapalı bir polinom koşulu değildir `[İSPAT]`. Buna karşılık `verify_independent_exact.py`, $M_9(\operatorname{perm}_4;L_8)$'de doğrudan `11,440/11,440` tam rankı (`mod 32749, 65521`) kanıtlar `[KESİN HESAP]`. Bu tam ranklı sabit $11{,}440\times 11{,}440$ satır kümesi $I_1$ seçilince $\widetilde{P}^{(4)}(F):=\det_{11440}(M_9(F;L_8)_{I_1})\in\mathbb{Z}[F]_{11440}$ paydasız homojen polinom olur ve $M_6$ düşse bile $\ker M_9\neq 0$ iken sıfırlanır `[İSPAT]`.
- **`Q^(4)` doğrudan $\det_{1365}$ midir?** Evet: Round 14 (`verify_theorem15a_border_dc_ge_10_invariant`) betiğindeki `A4_sing2`, IMSC olmadan doğrudan $F$-lineer $2808\times 1365$ matrisi $M_4^{\mathrm{Sing}_2}(F;L_{12})$'yi kurar; sabit pivot satırları $I_2$ üzerinde $Q^{(4)}(F)=\det_{1365}(M_4^{\mathrm{Sing}_2}(F;L_{12})_{I_2})\in\mathbb{Z}[F]_{1365}$ doğrudan polinomdur `[İSPAT]`. (`CHECK 3` `perm_4` için `1365/1365` tam rankını her iki asalda doğrulamıştır `[KESİN HESAP]`.)

### 2. `verify_round15_strassen.py` Satır 402–434 (`T^(4)` Testi)
Bu dosyanın satır `402–434` kaynak kodu birincil verilerde yer almamaktadır (yalnızca satır `221–261` ve uzman metnindeki "sentetik `H_sym`" ifadesi vardır); dolayısıyla gerçek bir $m=10$ polinomu mu yoksa sentetik `H_sym` mi test edildiği birincil koddan doğrulanamamıştır `[DOĞRULANMADI]`.

### 3. `CHECK 3` Çıktısının Doğruladıkları
- **Kesin C-çekirdeği sonuçları:** `perm_4` için `M_4^{Sing_2}` rankı `1365/1365` (`mod 32749, 65521`), $\det_9(I_9+L(X))$'in derece-$4$ parçası $e_4(L(X))$ için `1365/1365` ($Q^{(4)}(e_4)\neq 0$) ve $F_{\text{skew5}}$ için `1320/1365` ($<1365\implies Q^{(4)}(F_{\text{skew5}})=0$ `[İSPAT]`) doğrulanmıştır `[KESİN HESAP]`. $Q_{3,1}$ için $P^{(4)}=0$ satırı basılmışsa da `Q_{3,1}` açık tanımı burada verilmediğinden iç yapısı `[DOĞRULANMADI]`.
- **`q_5` LM `[PROBE]` çıktıları:** `54` değişken, `56` denklem ve `16` `float64` LM başlangıcında artık normunun `1.000` ve `1.435`'in altına düşmediği gözlenmiştir `[KESİN HESAP]`; ancak bu yerel sayısal arama küresel imkânsızlık ispatlamaz `[İSPAT]`.

### Adım 3 — Eleştirmen Saldırısı (Konu 3)

### 1) En Büyük Gizli Varsayım (`R_9^(4) -> dc_border(perm_4) >= 10`)
- **En büyük gizli varsayım, kapanış–kesişim değişimidir ($\overline{\mathcal{D}_9^{\mathrm{hom}}} = \mathcal{B}_9^{(4)}$ yanılgısı)** `[İSPAT]`. $\overline{\mathcal{D}_9 \cap \mathbb{C}[X]_4} \subseteq \overline{\mathcal{D}_9} \cap \mathbb{C}[X]_4$ kapsamasının tersi yanlıştır `[İSPAT]`. Dolayısıyla saf homojen $9\times 9$ dilimlerin kapanışı $\overline{\mathcal{D}_9^{\mathrm{hom}}}$ üzerinde sıfırlanan bir polinom, homojen olmayan eğrilerin sınırı olan $\mathcal{B}_9^{(4)}$ üzerinde sıfırlanmak zorunda değildir `[İSPAT]`.
- **Diğer gizli varsayımlar:** `P^{(4)}` rasyonel fonksiyonunun polinom gibi ele alınması ve Kısım A'nın $r=3$'te dış Atkinson–Dieudonné teoremine (ve $m=10$'da kanıtsız Teorem 15B'ye) dayanmasıdır `[DOĞRULANMADI]`.

### 2) Homojenlik Boşluğu ($\overline{\mathcal{D}_9^{\mathrm{hom}}}$ vs $\mathcal{B}_9^{(4)}$)
- $\mathbb{C}(\!(\varepsilon)\!)$ üzerinde $A_0(\varepsilon)\sim\operatorname{diag}(\varepsilon^{a_1},\dots,\varepsilon^{a_9})$ tüm $a_i<\infty$ iken **tam rank $9$** olup sabit $0_r$ bloğu yoktur `[İSPAT]`.
- $\varepsilon^{-a_i}$ ölçeklemesi $L_\varepsilon(X)$'te $\varepsilon^{-p}$ kutupları üretir; örneğin $r_0=1$'de $[t^4]F_\varepsilon$ içine $\varepsilon^{a_9}e_4(A_\varepsilon)+W_\varepsilon e_3(A_\varepsilon)-(v_\varepsilon^T u_\varepsilon)e_2(A_\varepsilon)+(v_\varepsilon^T A_\varepsilon u_\varepsilon)e_1(A_\varepsilon)$ sızar `[İSPAT]`. Böylece $\deg\neq 4$ terimleri $\varepsilon\to 0$'da sadeleşip `[t^2]=0` ($W$ izotropisi), Double-Koszul ve Skew-Square'i yıkar (`CHECK 3`'teki homojen olmayan $\det_9(I_9+L)$'nin $e_4$ parçası da `1365/1365` ile $Q^{(4)}\neq 0$ verir `[KESİN HESAP]`) `[İSPAT]`.
- `verify_round14_strassen.py` (satır 15–16) ve `REPORT.md` (satır 585) metinleri burada verilmediğinden bu boşluğu kapatmadıkları `[DOĞRULANMADI]`. Kısım B de zaten `#1–#3`'te tıkandığını açıkça göstermektedir `[İSPAT]`.

### 3) `P^(4)` ve `T^(4)` Polinomluğu ile Eksik `12870x12870` Minörü
- `verify_round13_strassen.py`'deki `P^{(4)} = det6 * det_s6 * det_s7 * det_s8`, `rref_mod_p_with_det` (`det6` terslemesi) ve `step_imsc_det` yüzünden **rasyonel fonksiyondur** (`rk M_6 < 1584`'te tanımsızlaşır) `[İSPAT]`. `T^{(4)}` kaynak kodu ise verilmemiştir `[DOĞRULANMADI]`.
- Gerçek polinomlar $\widetilde{P}^{(4)}=\det_{11440}(M_9(F;L_8)_{I_1})$ ve $Q^{(4)}=\det_{1365}(M_4^{\mathrm{Sing}_2}(F;L_{12})_{I_2})$'dir `[İSPAT]`. `perm_4` tam rankları (`11440/11440` ve `1365/1365` mod `32749, 65521`) doğrulanmıştır `[KESİN HESAP]`; ancak `P^{(4)}(\operatorname{per}_4)\equiv 5223` çıktısı burada basılmamıştır `[DOĞRULANMADI]`.
- $\widetilde{T}^{(4)}$ için gereken **`12870 x 12870` direkt minör çalıştırılmamıştır** (`verify_round15_strassen.py` satır `402–434` sentetik `H_sym` iddiası da kodsuz olduğundan doğrulanamaz) `[DOĞRULANMADI]`.

### 4) `arXiv:2611.03554`, `LMR (2013)`, `[OAI26]` ve Şu An Kanıtlanan Gerçek Sonuç
- `arXiv:2611.03554`, `LMR (2013)` ($\underline{\mathrm{dc}}(\operatorname{per}_4)\ge 8$) ve `[OAI26]` birincil metinleri verilmediğinden bu oturumda doğrulama dışıdır `[DOĞRULANMADI]`. `CHECK 3` yalnızca `Q_{3,1}` için `P^{(4)}=0` satırı basmıştır; açık tanımı verilmediğinden iç yapısı `[DOĞRULANMADI]`.
- **Şu an kanıtlanan şey $\underline{\mathrm{dc}}(\operatorname{per}_4)\ge 10$ DEĞİLDİR** `[İSPAT]`. `dc_perm4_ge_10.tex` (`prop:corank1`) içindeki $2\times 2$ sıfır bloğu atlamasını $\widetilde{P}^{(4)}$ örter `[İSPAT]`; fakat gerçekte (Atkinson–Dieudonné tamlığı `[DOĞRULANMADI]` koşuluyla) yalnızca $\operatorname{per}_4\notin\overline{\mathcal{D}_9^{\mathrm{hom}}}$ — yani saf homojen derece-$4$ $9\times 9$ determinantal dilimlerin Zariski kapanışından ayrım — kanıtlanmıştır (`m=10` ise `12870x12870` minör eksikliğiyle `[DOĞRULANMADI]`) `[İSPAT]`.

### Adım 4 — Uzmanların Son Yanıtları

### Sınır karmaşıklığı uzmanı (Son Yanıt)
Eleştirmenin temel tespitleri doğrudur:

1. **Kapanan Gerçek Uzay:** Elle ispat ve `11440/11440` ($\mathcal{M}_9$) ile `1365/1365` ($\mathcal{M}_4^{\mathrm{Sing}_2}$, `mod 32749, 65521`) tam rankları `[KESİN HESAP]`, yalnızca **saf homojen dilim kapanışı $\overline{\mathcal{D}_9^{\mathrm{hom}}}$** üzerinde (Atkinson–Dieudonné tamlığı `[DOĞRULANMADI]` koşuluyla) $\widetilde{R}_9^{(4)}=\widetilde{P}^{(4)}Q^{(4)}$ için kapanır; kanıtlanan $\mathrm{perm}_4\notin\overline{\mathcal{D}_9^{\mathrm{hom}}}$'dur, $\underline{\mathrm{dc}}(\mathrm{perm}_4)\ge 10$ değildir `[İSPAT]`. `P^{(4)}, T^{(4)}` IMSC çarpımları rasyoneldir ($\widetilde{P}^{(4)}=\det_{11440}$, $\widetilde{T}^{(4)}=\det_{12870}$ gerçek polinomdur) `[İSPAT]`; `m=10` için `H_sym` sentetik kaldığından `[DOĞRULANMADI]`dır.

2. **`ŞU ADIMDA TIKANDI` ($\underline{\mathrm{dc}}\ge 10,11$):**
   * **Kapanış–kesişim:** $\overline{\mathcal{D}_9\cap\mathbb{C}[X]_4}=\mathcal{B}_9^{(4)}$ eşitliği yoktur `[İSPAT]`.
   * **SNF ve kutuplar:** $\mathbb{C}((\varepsilon))$'da $A_0(\varepsilon)\sim\operatorname{diag}(\varepsilon^{a_1},\dots,\varepsilon^{a_9})$ tam rank $9$ alıp $\varepsilon^{-p}$ kutuplarıyla $\deg\neq 4$ terimlerini $\varepsilon\to 0$'da sadeleştirir; `[t^2]=0`, Double-Koszul ve Skew-Square çöker (`CHECK 3` $\det_9(I_9+L)$'nin $e_4$ parçasında `1365/1365`, $Q^{(4)}\neq 0$ `[KESİN HESAP]`) `[İSPAT]`.

3. **Tek Somut Ek Kontrol:**
   Tam ranklı sınır eğrilerinden ($F_0=\lim_{\varepsilon\to 0}\varepsilon^{-k}\det_9(\operatorname{diag}(I_w,\varepsilon I_r)+L_\varepsilon(X))\in\mathcal{B}_9^{(4)}$) doğrudan $\widetilde{P}^{(4)}(F_0)\neq 0$ ve $Q^{(4)}(F_0)\neq 0$ (`11440/11440`, `1365/1365`) veren bir karşı-örnek taranarak $\widetilde{R}_9^{(4)}|_{\mathcal{B}_9^{(4)}}\not\equiv 0$ test edilmelidir `[SANI]`.

### Cebirsel geometri (Son Yanıt)
### 1) Gerçekten `[İSPAT]` / `[KESİN HESAP]` Olan Kısım
Elle ispat gerçek sınır karmaşıklığı $\mathcal{B}_9^{(4)}$ üzerinde **kapanmaz**; yalnızca saf homojen dilim kapanışı **$\overline{\mathcal{D}_9^{\mathrm{hom}}}=\overline{\mathcal{D}_9\cap\C[X]_4}$** üzerinde $\widetilde{P}^{(4)}Q^{(4)}\equiv 0$ hedefiyle $\per_4\notin\overline{\mathcal{D}_9^{\mathrm{hom}}}$ uzayına yönelir [İSPAT]. Burada $\widetilde{P}^{(4)}, Q^{(4)}$ polinomlaştırması, Boyut Teoremi, $r\neq 3$ dalları ve `dc_perm4_ge_10` ($r=3$) $2\times 2$ sıfır blok açığının kapatılması [İSPAT]; CHECK 3'teki $Q^{(4)}(\per_4)\neq 0$ (`1365/1365`), $Q^{(4)}(e_4)\neq 0$, $P^{(4)}(Q_{3,1})=0$ ve $Q^{(4)}(F_{\mathrm{skew5}})=0$ (`1320/1365`) ise **[KESİN HESAP]**tır. Buna karşın $r=3$ Atkinson–Dieudonné tamlığı, $I_1$ (`11440/11440`) çıktısı ve $m=10$ (`12870x12870` $\widetilde{T}^{(4)}$ minörü, Teorem 15B) **[DOĞRULANMADI]**dır.

---

### 2) Gerçek $\underline{\mathrm{dc}}(\per_4)\ge 10, 11$ Nerede Tıkandı?
**ŞU ADIMDA TIKANDI:** Kapanış ile kesişim yer değiştirmez ($\overline{\mathcal{D}_9^{\mathrm{hom}}}\subseteq \mathcal{B}_9^{(4)}$ eşitliği kanıtsızdır) ve $\C((\varepsilon))$ üzerinde tam ranklı $A_0(\varepsilon)\sim\diag(\varepsilon^{a_1},\dots,\varepsilon^{a_9})$ ($a_i<\infty$) eğrilerinde $\varepsilon^{-p}$ kutupları $\deg\neq 4$ terimlerini $[t^4]F_\varepsilon$ içine sızdırarak $[t^2]=0$ ($W$ izotropisi), Double-Koszul ve Skew-Square mekanizmasını yıkar [İSPAT].

---

### 3) Tek Somut Ek Kontrol (Hesaplamalı Cebir)
$\det_9(\diag(\varepsilon^{a_1},\dots,\varepsilon^{a_9})+L_\varepsilon(X))=F_0(X)+O(\varepsilon)$ ($a_i<\infty$, kutuplu) biçiminde bir $F_0\in\mathcal{B}_9^{(4)}\setminus\mathcal{D}_9^{\mathrm{hom}}$ sınır limiti üretip üzerinde modüler $\mathcal{M}_9(F_0;L_8)$ ($11440$) ve $\mathcal{M}_4^{\Sing_2}(F_0;L_{12})$ ($1365$) tam ranklarını sınamak: tek bir $\widetilde{P}^{(4)}(F_0)Q^{(4)}(F_0)\neq 0$ tanığı $\widetilde{R}_9^{(4)}$'ün gerçek $\mathcal{B}_9^{(4)}$'ü ayırmadığını doğrudan kanıtlar [İSPAT].

### Sınırlı rank uzayları / temsil (Son Yanıt)
### 1) Gerçekten Kanıtlanan / Hesaplanan Kısım ve Kapanan Uzay
- **Kapanan uzay:** Elle cebirsel taslak (`r=3` $2\times 2$ sıfır bloğu $\mathrm{adj}(W_0)=(0,-c,b)^T(0,e,-d)\implies \mathrm{str}\le 2$ dahil) yalnızca saf homojen dilim kapanışı $\overline{\mathcal{D}_9^{\mathrm{hom}}}$ üzerinde $\widetilde{R}_9^{(4)}=\widetilde{P}^{(4)}Q^{(4)}=0$ olarak kapanır (`Atkinson–Dieudonné` tamlığı hariç) [İSPAT]; o dış sınıflandırma adımı [DOĞRULANMADI].
- **Hesap durumu:** $Q^{(4)}(\mathrm{perm}_4)$ için `1365/1365` (mod `32749, 65521`) `CHECK 3`'te doğrulanmıştır [KESİN HESAP]. `L_8` (`11440/11440`) `dc_perm4_ge_10.tex`'te raporlansa da `P^{(4)}\equiv 5223` ve $\widetilde{T}^{(4)}$ (`12870x12870`) burada basılıp çalıştırılmamıştır [DOĞRULANMADI].

### 2) Gerçek $\underline{\mathrm{dc}}(\mathrm{perm}_4)\ge 10, 11$ İddiasının Tıkandığı Nokta
- **ŞU ADIMDA TIKANDI:** $\overline{\mathcal{D}_9^{\mathrm{hom}}}\subsetneq\mathcal{B}_9^{(4)}$ eşitsizliği ve $\mathbb{C}(\!(\varepsilon)\!)$ üzerinde $A_0(\varepsilon)\sim\mathrm{diag}(\varepsilon^{a_1},\dots,\varepsilon^{a_9})$ tam rankı (`corank = 0`) yüzünden $\varepsilon^{-p}$ kutupları üzerinden $\deg\ne 4$ terimlerinin $[t^4]F_\varepsilon$'ye sızmasıdır [İSPAT]. Bu sızıntı `[t^2]=0` ($W$ izotropisi), Double-Koszul ve Skew-Square'i yıkar [İSPAT]; nitekim `CHECK 3`'te $\det_9(I_9+L)$'nin $e_4$ parçası `1365/1365` ile $Q^{(4)}\ne 0$ verir [KESİN HESAP]. $m=10$ ($\ge 11$) ayrıca kanıtsız Teorem 15B ve eksik `12870x12870` minöründe tıkanır [DOĞRULANMADI].

### 3) Tek Somut Ek Kontrol
`Hesaplamalı cebir` tarafında tek belirleyici ek kontrol: rasyonel `P^{(4)}` yerine sabit pivotlu $\widetilde{P}^{(4)}=\det_{11440}(M_9(F;L_8)_{I_1})$ ve $\widetilde{T}^{(4)}=\det_{12870}(M_8^{\mathcal{H}_{\le 4}}(\mathrm{perm}_4;L_9)_{I_3})$ minörlerini mod `32749, 65521`'de çalıştırıp, ardından $\widetilde{P}^{(4)}$'ü açık bir $\mathbb{C}(\!(\varepsilon)\!)$ Laurent sınır eğrisi $F_0=\lim_{\varepsilon\to 0}\det_9(A_0(\varepsilon)+L_\varepsilon)$ üzerinde test etmektir [SANI].

### Hesaplamalı cebir (Son Yanıt)
1. **Gerçekten `[İSPAT]` / `[KESİN HESAP]` olan kısım:** `verify_independent_exact.py` ($M_9(\operatorname{per}_4;L_8)$ `11,440/11,440`) ve `CHECK 3` ($M_4^{\mathrm{Sing}_2}(\operatorname{per}_4;L_{12})$ `1365/1365`, $e_4(L)$ `1365/1365`, $F_{\text{skew5}}$ `1320/1365`) doğrulanmıştır `[KESİN HESAP]`. $\widetilde{P}^{(4)}=\det_{11440}(M_9(F;L_8)_{I_1})$ ve $Q^{(4)}=\det_{1365}(M_4^{\mathrm{Sing}_2}(F;L_{12})_{I_2})$ paydasız gerçek polinomlardır `[İSPAT]`. Böylece elle ispat taslağı, $r=3$'teki dış Atkinson–Dieudonné adımı (`[DOĞRULANMADI]`) kabul edildiğinde, yalnızca **saf homojen $9\times 9$ dilimlerin Zariski kapanışı $\overline{\mathcal{D}_9^{\mathrm{hom}}}$** üzerinde kapanır ($\operatorname{per}_4\notin\overline{\mathcal{D}_9^{\mathrm{hom}}}$) `[İSPAT]`. `m=10` ($\overline{\mathcal{D}_{10}^{\mathrm{hom}}}$) ise `12870x12870` minörü çalıştırılmadığından doğrulanmamıştır `[DOĞRULANMADI]`.

2. **Gerçek $\underline{\mathrm{dc}}(\operatorname{per}_4)\ge 10,11$ iddiasının tıkandığı yer:** **ŞU ADIMDA TIKANDI:** $\overline{\mathcal{D}_9^{\mathrm{hom}}}\subsetneq\mathcal{B}_9^{(4)}$ homojenlik/kapanış–kesişim boşluğudur `[İSPAT]`. $\mathbb{C}(\!(\varepsilon)\!)$ üzerinde $A_0(\varepsilon)\sim\operatorname{diag}(\varepsilon^{a_1},\dots,\varepsilon^{a_9})$ tam rank $9$ kalıp $\varepsilon^{-p}$ kutuplarıyla alt/üst dereceleri $[t^4]F_\varepsilon$'ye sızdırdığından $[t^2]=0$, Double-Koszul ve Skew-Square çöker `[İSPAT]`; nitekim `CHECK 3` homojen olmayan $e_4(L)$ için $Q^{(4)}(e_4)\neq 0$ (`1365/1365`) vermiştir `[KESİN HESAP]`.

3. **Tek somut ek kontrol:** `verify_independent_exact.py` (`uint64_t` CSR) ile $e_4(L)$ ve $\varepsilon$-limitli homojen olmayan $\mathcal{B}_9^{(4)}$ formları üzerinde $M_9(F;L_8)$ rankının (`11,440`?) ölçülmesidir; böylece $\widetilde{P}^{(4)}(e_4)\neq 0$ ise $\widetilde{R}_9^{(4)}|_{\mathcal{B}_9^{(4)}}\not\equiv 0$ doğrudan yakalanır `[SANI]`. (Not: $12{,}870\times 12{,}870$ $\widetilde{T}^{(4)}$ kontrolü yalnızca $\overline{\mathcal{D}_{10}^{\mathrm{hom}}}$ içindir, $\mathcal{B}_{10}^{(4)}$ sınırını kapatmaz `[İSPAT]`.)

### Adım 5 — Moderatör Nihai Hükmü & Tur 3 'Neyi Kapattık?' Tablosu

# Konu 3 ve Genel Sonuç — Moderatör Hükmü

> **Moderatör Kısıt Notu:** Kural 5 gereği hiçbir araç çağrılmamıştır `[DOĞRULANMADI]`. Tüm hükümler yalnızca panelde sunulan birincil metin alıntılarına, elle türetilen cebirsel adımlara ve doğrulanmış `CHECK 1–3` / `verify_independent_exact.py` çıktılarının kapsamına dayanır `[İSPAT]`.

---

## 1. KISIM A — $\widetilde{R}_9^{(4)} = \widetilde{P}^{(4)} Q^{(4)}$ İçin $\overline{\mathcal{D}_9^{\mathrm{hom}}}$ Üzerinde Elle İspat Taslağı ve Düzeltmeler

### Hangi Düzeltmelerle Geçerlidir?
1. **IMSC Rasyonellik Düzeltmesi (`P^{(4)} \to \widetilde{P}^{(4)}`):** `verify_round13_strassen.py`'deki `P^{(4)} = det6 * det_s6 * det_s7 * det_s8`, `rref_mod_p_with_det` (`det6` terslemesi) ve `step_imsc_det` (`C_D` satırlarıyla ara-pivot kuvvetlerini paydaya taşıması) nedeniyle **rasyonel fonksiyondur** (`rk M_6(F;L_8) < 1584`'te tanımsızlaşır veya pivot dalı değiştirir) `[İSPAT]`. Buna karşılık `verify_independent_exact.py`, $\mathcal{M}_9(\per_4;L_8)$ için `11,440/11,440` (`mod 32749, 65521`) tam rankını kanıtlar `[KESİN HESAP]` ($\mathbb{F}_p\to\mathbb{Q}$ kaldırmasıyla tam rank kesindir `[İSPAT]`). Böylece tam ranklı sabit $11{,}440\times 11{,}440$ satır altkümesi $I_1$ seçilerek tanımlanan $\widetilde{P}^{(4)}(F):=\det_{11440}(\mathcal{M}_9(F;L_8)_{I_1})\in\mathbb{Z}[F]_{11440}$ paydasız homojen polinom olur `[İSPAT]`. (`P^{(4)}(\per_4)\equiv 5223 \pmod{32749}` sayısı `CHECK 1–3`'te basılmadığından `[DOĞRULANMADI]`dır, ancak $I_1$'in varlığı `11,440/11,440` tam rankıyla garantilenir `[İSPAT]`.)
2. **`Q^{(4)}` Polinomluğu:** `Q^{(4)}(F)=\det_{1365}(\mathcal{M}_4^{\Sing_2}(F;L_{12})_{I_2})\in\mathbb{Z}[F]_{1365}$ tek RREF adımıyla doğrudan paydasız homojen polinomdur; `CHECK 3` `perm_4` üzerinde `1365/1365` (`mod 32749, 65521`) tam rankını doğrular `[KESİN HESAP]` + `[İSPAT]`. Dolayısıyla $\widetilde{R}_9^{(4)}:=\widetilde{P}^{(4)}Q^{(4)}$ homojen bir polinomdur ve $\widetilde{R}_9^{(4)}(\per_4)\neq 0$ sağlar `[KESİN HESAP]` + `[İSPAT]`.
3. **$r=3$ ($2\times 2$ Sıfır Bloğu ve İndeks Düzeltmesi):** `dc_perm4_ge_10.tex` (`prop:corank1`) içinde $2\times 2$ sıfır bloğu vakası atlanmıştır `[İSPAT]`; ayrıca Kısım A $r=3$(i)'deki $(e_3^T V^T U)c$ teriminde indis $v_i^T u_3$ yerine $v_3^T u_i$ olmalıdır `[İSPAT]`. İki düzeltme de aşağıda taslağa eklenmiştir `[İSPAT]`.

### $\overline{\mathcal{D}_9^{\mathrm{hom}}}$ Üzerinde Elle İspat Taslağı
$F=\det_9(A_0+L(X))\in\mathcal{D}_9^{\mathrm{hom}}$ ($F\neq 0$; $F=0$ ise $\widetilde{P}^{(4)}(0)=Q^{(4)}(0)=0$ `[İSPAT]`) için $A_0=\diag(I_w,0_r)$ ($w+r=9$) ve $L=\begin{pmatrix}A&U\\V^T&W_0\end{pmatrix}$ yazılır `[İSPAT]`:
* **$r=0$ ve $r\ge 5$:** $r=0$'da $[t^0]=1\neq 0$ (homojen derece-$4$ olamaz); $r\ge 5$'te son $r$ satır sabit-$0$ olduğundan $[t^4]\equiv 0\implies F=0$ `[İSPAT]`.
* **$r=4$:** $F=\det_4(W_0)$; $\{\rk W_0\le 2\}\subseteq\Sing(V(F))$ kodim $\le 4<8$ olup Boyut Teoremi ile $L_8\setminus\{0\}$'ı keser $\implies\ker\mathcal{M}_9(F;L_8)\neq 0\implies\widetilde{P}^{(4)}(F)=0$ `[İSPAT]`.
* **$r=3$:** $[t^3]=\det_3(W_0)=0$ ve $F=[t^4]=-\operatorname{tr}(\adj(W_0)V^T U)$ `[İSPAT]`. Atkinson–Dieudonné üç dal verir (üç dalın tamlığı bu oturumda kanıtlanmamış dış teorem adımıdır `[DOĞRULANMADI]`):
  * (i) *Sıfır sütunlu/satırlı $W_0$* (ör. 3. sütun sıfır): $\adj(W_0)$ yalnızca 3. satırda sıfırdan farklıdır; $F=\sum_{i=1}^3 c_i(v_3^T u_i)$ ($c_i$: $3\times 2$ bloğun $2\times 2$ minörleri) ve $\{c_1=c_2=v_3^T u_1=v_3^T u_2=v_3^T u_3=0\}\subseteq\Sing(V(F))$ ($\codim\le 5<8\implies\widetilde{P}^{(4)}(F)=0$) `[İSPAT]`.
  * (ii) *$2\times 2$ sıfır bloklu sıkıştırma* ($W_0=\begin{pmatrix}a&b&c\\d&0&0\\e&0&0\end{pmatrix}$): kofaktör hesabıyla $\adj(W_0)=\begin{pmatrix}0\\-c\\b\end{pmatrix}\begin{pmatrix}0&e&-d\end{pmatrix}$ olup $Q=V^T U=(q_{ij})$ için $F=c(eq_{22}-dq_{32})-b(eq_{23}-dq_{33})\in\langle b,c\rangle\cdot\langle d,e\rangle$ ($\str\le 2$) ve $\{b=c=d=e=0\}\subseteq\Sing(V(F))$ ($\codim\le 4<8\implies\widetilde{P}^{(4)}(F)=0$) `[İSPAT]`.
  * (iii) *Ters-simetrik $W_0$*: $\adj(W_0)=\ell\ell^T\implies F\in\langle\ell_1,\ell_2,\ell_3\rangle^2\implies\codim\Sing\le 3<8\implies\widetilde{P}^{(4)}(F)=0$ `[İSPAT]`.
* **$r=2$:** $\det_2(W_0)=0$ ile $W_0=\begin{pmatrix}\ell_1&\ell_2\\0&0\end{pmatrix}$ (veya devriği); $[t^3]=\ell_2(v_2^T u_1)-\ell_1(v_2^T u_2)=0$ üç alt-durumda da 4 üretecin ortak sıfırını $\Sing(V(F))$'ye koyar ($\codim\le 4<8\implies\widetilde{P}^{(4)}(F)=0$) `[İSPAT]`.
* **$r=1$ ($w=8$):** $D\le 7$ ise $F=-v^T A^2 u\in I_W^2\implies W^\perp\subseteq\Sing(V(F))$ ($\codim\le 7<8\implies\widetilde{P}^{(4)}(F)=0$) `[İSPAT]`. $D=8$ ($w-D=0$) ise Double-Koszul ($A_{13}(X_0)=0$) + Skew-Square ($(A_{11}(X_0)^2 K)^T=-A_{11}(X_0)^2 K$) ile $\operatorname{Hess}(F)|_{W^\perp}\equiv 0$ ve $\dim(W^\perp\cap L_{12})\ge 4\implies Q^{(4)}(F)=0$ `[İSPAT]`.
* **Zariski Kapanışı:** Polinom $\widetilde{R}_9^{(4)}$ tüm $\mathcal{D}_9^{\mathrm{hom}}$ üzerinde sıfırlandığından Zariski kapanışı $\overline{\mathcal{D}_9^{\mathrm{hom}}}$ üzerinde de özdeşçe sıfırlanır (`Atkinson–Dieudonné` tamlığı hariç kapalıdır `[İSPAT]` / `[DOĞRULANMADI]`).

### $R_{10}^{(4)}$ İçin Zorunlu Uyarı Notu
* **IMSC Payda Uyarısı:** $R_{10}^{(4)} = P^{(4)} T^{(4)} Q^{(4)}$ içindeki `T^{(4)}` (`D=6->7->8`) çok adımlı IMSC pivot çarpımı olduğundan rasyonel fonksiyon / payda riski taşır ve kaynak kodu da bu oturumda verilmemiştir `[DOĞRULANMADI]`; gerçek homojen polinom $\widetilde{T}^{(4)}(F):=\det_{12870}(\mathcal{M}_8^{\mathcal{H}_{\le 4}}(F;L_9)_{I_3})$ biçiminde tanımlanmalıdır `[İSPAT]`.
* **`M_8` Tam Direkt Minör `[DOĞRULANMADI]`:** `12870 x 12870` tam direkt minör `perm_4` üzerinde hiç çalıştırılmamıştır `[DOĞRULANMADI]`; `verify_round15_strassen.py` satır `402–434` kaynak kodu verilmediğinden sentetik `H_sym` iddiası da doğrulanamamıştır `[DOĞRULANMADI]`; ayrıca $m=10, D=8$ için Teorem 15B ($\rk\operatorname{Hess}(F)|_{W^\perp}\le 2$) burada kanıtlanmamıştır `[DOĞRULANMADI]`. Dolayısıyla $\widetilde{R}_{10}^{(4)}$ henüz kapalı bir teorem değildir `[DOĞRULANMADI]`.

---

## 2. KISIM B — Gerçek Sınır Karmaşıklığı ($\underline{\mathrm{dc}}_{\mathbb{C}}(\per_4)\ge 10, 11$) İçin `ŞU ADIMDA TIKANDI` Raporu

1. **`ŞU ADIMDA TIKANDI #1` — Kapanış–Kesişim Özdeşliği Yanılgısı ($\overline{\mathcal{D}_m^{\mathrm{hom}}} \stackrel{?}{=} \overline{\mathcal{D}_m} \cap \mathrm{Sym}^4$):** $\overline{\mathcal{D}_m\cap\C[X]_4}\subseteq\overline{\mathcal{D}_m}\cap\C[X]_4=\mathcal{B}_m^{(4)}$ kapsamasının tersi genel olarak **yanlıştır**; kapanış ile kapalı altuzay kesişimi yer değiştirmez `[İSPAT]`. (`verify_round14_strassen.py` satır `15–16` ve `REPORT.md` satır `585` verilmediğinden metnin ikisini özdeşleştirip özdeşleştirmediği `[DOĞRULANMADI]`.)
2. **`ŞU ADIMDA TIKANDI #2` — Smith Normal Formu ve $\C((\varepsilon))$'da Tam Rank $9$:** $\C[[\varepsilon]]$ üzerinde $A_0(\varepsilon)\sim\diag(\varepsilon^{a_1},\dots,\varepsilon^{a_9})$ tüm $a_i<\infty$ iken $\C((\varepsilon))$'da **tam rank $9$** ($\mathrm{corank}=0$) olur; sabit $0_r$ bloğuna ve $r=0..9$ ayrımına çökmez `[İSPAT]`.
3. **`ŞU ADIMDA TIKANDI #3` — Laurent $\varepsilon^{-p}$ Kutupları ve $\deg\neq 4$ Sızıntısı:** $\varepsilon^{-a_i}$ satır/sütun ölçeklemeleri $L_\varepsilon(X)$'te $\varepsilon^{-p}$ kutupları üretir; örneğin $r_0=1$'de $[t^4]F_\varepsilon$ içine $\varepsilon^{a_9}e_4(A_\varepsilon)+W_\varepsilon e_3(A_\varepsilon)-(v_\varepsilon^T u_\varepsilon)e_2(A_\varepsilon)+(v_\varepsilon^T A_\varepsilon u_\varepsilon)e_1(A_\varepsilon)$ sızar `[İSPAT]`. Alt/üst derece terimleri $\varepsilon\to 0$'da sadeleşebildiğinden `[t^2]=0` ($W$ izotropisi), Double-Koszul ve Skew-Square mekanizmaları yıkılır `[İSPAT]`. (`CHECK 3`'te homojen olmayan $\det_9(I_9+L)$'nin $e_4(L)$ parçası `1365/1365` ile $Q^{(4)}(e_4)\neq 0$ vererek bunu doğrular `[KESİN HESAP]`.)
4. **`arXiv:2611.03554` Bağlantısı ve Eksik Dış Referanslar:** $Q_{3,0}=\lim_{t\to 0} t^{-1}\det_3(A(x)+tS)$ örneği $t^{-1}$ kutuplu homojen olmayan determinantal eğrilerin kesin $\mathrm{dc}$'yi aşan sınırlara nasıl çöktüğünü somutlaştırır `[İSPAT]`. `CHECK 3`'te `Q_{3,1}` için $P^{(4)}=0$ basılmıştır (`Q_{3,1}` açık tanımı burada verilmediğinden iç yapısı `[DOĞRULANMADI]`, ancak $\codim 3$ tekil kümesi üzerinden $P^{(4)}=0$ vermesi $\widetilde{P}^{(4)}$'ün tek başına sınır karmaşıklığını yükseltmediğini gösterir `[İSPAT]`). `Q_{5,0}`, $\mathcal{K}_{2,0}$, `LMR (2013)` ($\underline{\mathrm{dc}}(\per_4)\ge 8$) ve `[OAI26]` metinleri burada verilmediğinden `[DOĞRULANMADI]`.
5. **Diğer Gizli Varsayımlar:** Rasyonel `P^{(4)}, T^{(4)}` fonksiyonlarının $\mathcal{B}_m^{(4)}$ üzerinde polinom gibi kullanılması yanlıştır (`rk M_6 < 1584`'te `det6=0`) `[İSPAT]`; `m=10` için `12870x12870` minörü + Teorem 15B `[DOĞRULANMADI]` ve $r=3$ Atkinson–Dieudonné tamlığı `[DOĞRULANMADI]` kalır.
6. **Önerilen Tek Somut Kontrol:** $\det_9(\diag(\varepsilon^{a_1},\dots,\varepsilon^{a_9})+L_\varepsilon(X))=F_0(X)+O(\varepsilon)$ ($a_i<\infty$, kutuplu) Laurent sınır limitleri (ve $e_4(L)$) üzerinde `verify_independent_exact.py` ile $\mathcal{M}_9(F_0;L_8)$ (`11440`) ve $\mathcal{M}_4^{\Sing_2}(F_0;L_{12})$ (`1365`) ranklarının ölçülmesi, $\widetilde{R}_9^{(4)}|_{\mathcal{B}_9^{(4)}}\not\equiv 0$ olup olmadığını doğrudan test edecektir `[SANI]`.

---

## 3. TUR 3 — 'NEYİ KAPATTIK?' TABLOSU

| Konu | Karar | Dayanak Etiket | Açık Kalan |
| :--- | :--- | :--- | :--- |
| **$\widetilde{P}^{(4)}, Q^{(4)}$ Polinomluğu vs IMSC Rasyonelliği** | `P^{(4)}, T^{(4)}` IMSC çarpımlarının rasyonel olduğu; sabit pivotlu $\widetilde{P}^{(4)}=\det_{11440}(\mathcal{M}_9(F;L_8)_{I_1})$ ve $Q^{(4)}=\det_{1365}(\mathcal{M}_4^{\Sing_2}(F;L_{12})_{I_2})$'nin paydasız homojen polinom olduğu kapatıldı. | `[İSPAT]` / `[KESİN HESAP]` | `P^{(4)}(\per_4)\equiv 5223` çıktısı basılmadı (`11,440/11,440` `I_1` varlığı için yeterlidir); `T^{(4)}` kaynak kodu verilmedi `[DOĞRULANMADI]`. |
| **`r=3` $2\times 2$ Sıfır Bloğu Düzeltmesi** | `dc_perm4_ge_10.tex`'teki vaka atlaması $\adj(W_0)=(0,-c,b)^T(0,e,-d)\implies\str\le 2$, $\codim\Sing\le 4<8\implies\widetilde{P}^{(4)}=0$ ile kapatıldı. | `[İSPAT]` | Atkinson–Dieudonné / EH88 üç-dal tamlığı dış teorem adımı olarak açık kaldı `[DOĞRULANMADI]`. |
| **$\overline{\mathcal{D}_9^{\mathrm{hom}}}$ Ayrımı ($\per_4\notin\overline{\mathcal{D}_9^{\mathrm{hom}}}$)** | `Atkinson–Dieudonné` tamlığı koşuluyla $\widetilde{R}_9^{(4)}=\widetilde{P}^{(4)}Q^{(4)}$'ün $\overline{\mathcal{D}_9^{\mathrm{hom}}}$ üzerinde sıfırlandığı ve $\per_4$'te sıfırlanmadığı kapatıldı. | `[İSPAT]` / `[KESİN HESAP]` / `[DOĞRULANMADI]` | Koşulsuzluk için Atkinson–Dieudonné tamlığı kanıtı veya doğrudan referans zinciri `[DOĞRULANMADI]`. |
| **$\overline{\mathcal{D}_{10}^{\mathrm{hom}}}$ ($R_{10}^{(4)}$)** | $\widetilde{T}^{(4)}=\det_{12870}(\mathcal{M}_8^{\mathcal{H}_{\le 4}}(F;L_9)_{I_3})$ biçimi tanımlandı; ancak kapatılamadı. | `[İSPAT]` / `[DOĞRULANMADI]` | `12870x12870` direkt minör hesabı, `verify_round15_strassen.py` satır `402–434` (`H_sym`) kodu ve Teorem 15B (`m=10, D=8`) `[DOĞRULANMADI]`. |
| **Gerçek Sınır Karmaşıklığı ($\underline{\mathrm{dc}}_{\C}(\per_4)\ge 10, 11$)** | **KANITLANAMADIĞI** kesinleştirildi: $\overline{\mathcal{D}_9^{\mathrm{hom}}}\subsetneq\mathcal{B}_9^{(4)}$, tam ranklı SNF $A_0(\varepsilon)$ ve $\varepsilon^{-p}$ kutupları `[t^2]=0`, Double-Koszul ve Skew-Square'i yıkar (`e_4(L)`'de `1365/1365`). | `[İSPAT]` / `[KESİN HESAP]` | Laurent sınır limitleri üzerinde $\widetilde{P}^{(4)}(F_0)Q^{(4)}(F_0)$ testi (`\mathcal{B}_9^{(4)}`'te muhtemel karşı-örnek) `[SANI]`. |
| **Dış Metinler (`2611.03554`, `LMR 2013`, `[OAI26]`, `q_5` LM)** | `Q_{3,0}` kutup mekanizması ve `q_5` LM yerel artıkları (`1.000`, `1.435`) not edildi; ancak yerel arama küresel kanıt vermez. | `[İSPAT]` / `[KESİN HESAP]` / `[DOĞRULANMADI]` | `Q_{3,1}, Q_{5,0}, \mathcal{K}_{2,0}`, `LMR (2013)` ve `[OAI26]` birincil metinleri `[DOĞRULANMADI]`. |

---

## 4. Kullanıcının Ana Sorusuna Nihai Yanıt

> **Soru:** *Sheshadri (`2611.06658`) `dc_C(perm_4) = 15`'i kanıtlıyorsa, bizim `>= 10` (ve `>= 12`) ispatımızın ve `dc-bar` iddiamızın geriye kalan gerçek bilimsel değeri tam olarak nedir?*

1. **Tam `dc_C(perm_4) >= 10` (ve olası `>= 12`) İddiası — Geriye Kalan Değer Yoktur (Yayınlanmaz):**
   * Sheshadri (`2611.06658`) yalnızca `= 15`'i hedeflemekle kalmaz; makalenin kendi içindeki ~`200` satırlık bilgisayarsız çekirdeği (`189–387` + `497–506`) sıfır bilgisayar sertifikası ile **$\mathrm{dc}_{\C}(\per_4)\ge 11$'i** zaten vermektedir `[İSPAT]`.
   * Dolayısıyla `dc_perm4_ge_10` (`423` satır + IMSC sertifikası, `r=3` $2\times 2$ sıfır bloğu atlaması düzeltilse bile) ne `>= 10` ne de `>= 12` hâliyle bağımsız bir `perm_4` alt-sınır notu olarak bilimsel öncelik veya yayın değeri taşır `[SANI]`.

2. **`dc-bar` (`\underline{dc}_C(perm_4) >= 10, 11`) İddiası — Şu An Kanıtlanmamıştır:**
   * `dc-bar` iddiası **geçerli değildir**; çünkü ispat $\overline{\mathcal{D}_m^{\mathrm{hom}}} \stackrel{?}{=} \mathcal{B}_m^{(4)}$ varsayımında, $\C((\varepsilon))$'da tam ranklı $A_0(\varepsilon)$ Smith normal formunda ve $\varepsilon^{-p}$ kutuplarıyla alt/üst derecelerin $[t^4]F_\varepsilon$'ye sızarak `[t^2]=0`, Double-Koszul ve Skew-Square mekanizmalarını yıkmasında **tıkanmaktadır** `[İSPAT]`.
   * Bu nedenle `LMR (2013)` ($\ge 8$)'i aşan bir $\underline{\mathrm{dc}}_{\C}(\per_4)$ alt sınırı şu an elde edilmiş değildir `[İSPAT]`.

3. **Geriye Kalan Gerçek Bilimsel Değer (Somut Olarak Kurtarılabilir Üç Parça):**
   * **A) Dürüstçe Daraltılmış Homojen Dilim Kapanışı Teoremi:** `dc-bar` iddiası tamamen çıkarılıp başlık **$\per_4 \notin \overline{\mathcal{D}_9^{\mathrm{hom}}}$** (saf homojen derece-$4$ $9\times 9$ determinantal dilimlerin Zariski kapanışından ayrım) olarak yeniden ifade edilir, `P^{(4)}` yerine sabit pivotlu polinom $\widetilde{P}^{(4)}=\det_{11440}$ yazılır ve $r=3$ (`2x2` sıfır bloğu + Atkinson–Dieudonné tamlığı) eklenirse **doğru ve temiz bir teknik gözlem** elde edilir (`m=10` ise `12870x12870` direkt minörü ve Teorem 15B tamamlanana dek kapsam dışıdır `[DOĞRULANMADI]`) `[SANI]`.
   * **B) Yeniden Kullanılabilir Doğrudan `uint64_t` CSR / Sabit-Pivot Minör Altyapısı:** `float64`/BLAS içermeyen, $\mathbb{F}_p\to\mathbb{Q}$ kesin rank kaldırmalı `verify_independent_exact.py` C-çekirdeği (`11,440/11,440` ve `1365/1365` `[KESİN HESAP]`) ve IMSC payda tuzağından arındırılmış doğrudan determinantal ayırıcılar (`\widetilde{P}^{(4)}, Q^{(4)}`) bağımsız hesaplamalı yöntem olarak değer taşır `[SANI]`.
   * **C) `perm_5` İçin İlk Yapı Taşları:** Asıl açık problem olan `perm_5`'te (`MR04 = 13`'ü aşmak için $\ge 14$ hedefi) `H-14A` (`\codim\Sing_2(\per_5)\ge 13`, `6188/6188` `[KESİN HESAP]`), $\det_4(\operatorname{Hess}_5|_4)=b_3^4$ `[KESİN HESAP]` ve `r=5` elemesi `[İSPAT]` gerçek ilerleme çekirdekleridir; ancak `perm_5` için de $L_{10}$ ($\codim\Sing\ge 10$), $r=2,3,4$ korank kapanışı ve $(D,w-D)=(10,2)$ ($m=13$ duvarı) çözülmeden yeni bir alt sınır teoremi çıkmaz `[DOĞRULANMADI]`.


## Ek Adım 3 Kontrolü — verify_laurent_border_test.py

Komut: `uv run --offline --with numpy --with sympy python3 /Users/bl10buer/Desktop/matemk/p-vs-np-gct/paper_dc_perm4/verify_laurent_border_test.py` (`exit code 0`, `task-2560`)

Ham çıktı:
```text
Sheshadri per4_dc_15.tex: 2359 lines total; computer-free dc>=11 uses lines 205-387 + 497-506 (193 lines).
[e_4(L(X)) from det_9(I_9+L)] L_8 IMSC coranks D=6..9: [0, 0, 0, 0] | L_12 Sing_2 rank: 1365/1365 (corank=0)
[Sheshadri Q_{3,1} (bdc=4, dc>=6)] L_8 IMSC coranks D=6..9: [763, 1211, 1814, 2598] | L_12 Sing_2 rank: 1122/1365 (corank=243)
[B_9^{(4)} [t^5]det_9(S_3^(1)(+)S_3^(2)(+)0_3 + tA_0)] L_8 IMSC coranks D=6..9: [1048, 1700, 2574, 3708] | L_12 Sing_2 rank: 903/1365 (corank=462)
[PROBE] Affine non-homog border det_4 -> Fermat cubic sum x_i^3 (96 vars, 126 eqs, 10 C-LM starts): min ||coeff res|| = 2.873e+00 (||x|| = 6.55)
```

Epistemik özet:
- `per4_dc_15.tex` satır aralığı doğrulandı: toplam `2359` satırın `205–387 + 497–506` (`193` satır) bölümü bilgisayarsız $\mathrm{dc}_{\mathbb{C}}(\mathrm{per}_4)\ge 11$ çekirdeğini içerir `[İSPAT]` / `[KESİN HESAP]`.
- `e_4(L(X))`: $L_8$ IMSC korankları `D=6..9` için `[0, 0, 0, 0]` ve $L_{12}$ $\mathrm{Sing}_2$ rankı `1365/1365` (`corank=0`) `[KESİN HESAP]` (alt derecelerin $1+\varepsilon e_1+\varepsilon^2 e_2+\varepsilon^3 e_3$ çıkarması gerektirdiğinden saf $\mathcal{B}_9^{(4)}$ tanığı değildir).
- `Sheshadri Q_{3,1}` (`bdc=4 <= 9`, `dc >= 6`): $L_8$ korankları `[763, 1211, 1814, 2598]` ve $L_{12}$ rankı `1122/1365` (`corank=243`) `[KESİN HESAP]` ($P^{(4)}=Q^{(4)}=0$).
- Laurent $\mathcal{B}_9^{(4)}$ örneği `[t^5] det_9((S_3^(1)(+)S_3^(2)(+)0_3)(X) + t A_0)`: $L_8$ korankları `[1048, 1700, 2574, 3708]` ve $L_{12}$ rankı `903/1365` (`corank=462`) `[KESİN HESAP]` (6 lineer form üzerinde tanımlı olduğundan $P^{(4)}=Q^{(4)}=0$; tam 16 değişkenli bir Laurent sınırı için genel geçerlik kanıtı değildir).
- `det_4 -> x_1^3+...+x_5^3` (`96` değişken, `126` denklem, `10` C-LM başlangıcı): `min ||coeff res|| = 2.873e+00 (||x|| = 6.55)` `[SANI]` (heuristik arama negatif kanıt sayılmaz).
