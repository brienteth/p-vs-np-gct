# Cebirsel Karmaşıklıktan Boolean Devre Alt Sınırlarına Nicel Aktarım Teoremi: İki-Kollu Forum Sentezi

**Tarih:** 22 Kasım 2026  
**Katılımcı Mimari:**
- **0G Grubu (`0gm-1.0-35b-a3b`):** `0g-pisagor`, `0g-oklid`, `0g-arsimet`, `0g-gauss`, `0g-harezmi`, `0g-ramanujan`
- **Swarm Konseyi (`gemini-4-hydrogen-high`):** `prof-euler`, `prof-strassen`, `prof-wigner`, `prof-hilbert`, `prof-noether`, `prof-valiant`
- **Hakem Eleştirmen (`gemini-4-neon-high`):** `critic` (Tur 1 Denetimi `#164`, Final Denetim `#174`)
- **Baş Moderatör (`gemini-4-neon-high`):** `moderator` (`Teorem Taslağı v1` `#165`, `Teorem Taslağı v2 — Kesin Hüküm` `#175`)

**Ham Kayıtlar:**
- 0G Tur 1 & Tur 2: `council_0g/0G_QUANT_TRANSFER_R1.md`, `council_0g/0G_QUANT_TRANSFER_R2.md`
- Swarm, Eleştirmen ve Moderatör Tutanakları: Swarm Board `#154–#175`

---

## 1. Kesin Sonuç: Koşullu Nicel Aktarım Teoremi (`Teorem Taslağı v2`)

Forumun iki tur süren çarpışması, `critic` denetimi ve `moderator` sentezi sonucunda, $\operatorname{AC}(f_n) \ge 2^{n^\varepsilon}$ tipi bir cebirsel alt sınırın $\mathrm{SAT}$ Boolean devre alt sınırına dönüşebilmesi için **gerekli ve yeterli koşulları** kesin parametreleriyle tespit eden aşağıdaki koşullu teorem kurulmuştur:

> ### Teorem (Koşullu Nicel Aktarım Teoremi — `Teorem v2`, `#175`)
> $f_n \in \mathbb{Z}[x_1,\dots,x_n]$ tamsayı katsayılı bir polinom ailesi olsun ve şu nicel bağları sağlasın:
> $$\deg(f_n) = d(n) \le n^{O(1)}, \qquad -2^{L(n)} \le f_n(x) < 2^{L(n)} \quad (\forall x \in \{0,1\}^n,\ L(n) = \mathrm{poly}(n)).$$
> Küp ideali $I_B := \langle x_1^2-x_1, \dots, x_n^2-x_n \rangle$ ve temel cisim $\mathbb{F} \in \{\mathbb{C}\} \cup \{\mathbb{F}_p : p \ge 3 \text{ asal}\}$ olsun. Aritmetik model **bölmesizdir** ($+, -, \times$). Aşağıdaki **H1–H4** koşulları sağlansın:
>
> - **H1 (İdeal-Modülo Fonksiyonel Alt Sınır — Forbes–Kumar–Saptharishi Tipi):**  
>   Sabit bir $\varepsilon > 0$ için alt sınır yalnızca biçimsel $f_n$'e değil, $\{0,1\}^n$ küpünde $f_n$ (veya $\mathbb{F}_p$ ise $f_n \bmod p$) ile örtüşen **tüm** bölmesiz $\mathbb{F}$-devrelerine uygulanır:
>   $$\operatorname{AC}_{\mathbb{F}}^{\mathrm{func}}(f_n) := \min\left\{ \operatorname{AC}_{\mathbb{F}}^{\text{bölmesiz}}(g) : g \in \mathbb{F}[x_1,\dots,x_n],\ g \equiv f_n \pmod{I_B} \right\} \ge 2^{n^\varepsilon}.$$
>   *(Sığ / derece-kısıtlı rejimde bu koşul $\deg_{\mathrm{syn}}(g) \le \Delta(n)$ kısıtı altında $\operatorname{AC}_{\mathbb{F}}^{\mathrm{func},\le \Delta(n)}(f_n) \ge 2^{n^\varepsilon}$ biçimindedir.)*
>
> - **H2 (Çift-Rejim Derinlik ve Derece Koşulu):**  
>   *(a) Genel $\mathrm{P}/\mathrm{poly}$ rejimi:* Eğer **H1** derece-serbest biçimde sağlanıyorsa hedef Boolean devresinin derinliği $D_B$ ve indirgemenin adaptif tur sayısı $r_d$ serbesttir.  
>   *(b) Derece-kısıtlı $\mathrm{NC}^1$ rejimi:* Eğer **H1** yalnızca $\Delta(n) = \mathrm{poly}(d(n)) = n^{O(1)}$ biçimsel/sentaktik derece sınırı altında biliniyorsa, toplam çarpım derinliği
>   $$D_{\mathrm{tot}}(n) = O\big(D_R(n) + r_d(n)\, D_B(m(n))\big) \le \log_2 \Delta(n) = O(\log n)$$
>   koşulunu sağlamak zorundadır; özel olarak $D_B(m) = \Theta(\log m)$ için **$D_R(n) = O(\log n)$ ve $r_d(n) = O(1)$** zorunludur. (Lineer bit-toplama yalnızca toplama derinliği ekler, çarpım derecesini artırmaz.)
>
> - **H3 (GRH-Serbest Alan ve İşaretli Bit Köprüsü):**  
>   - $\mathbb{F} = \mathbb{C}$ dalında hedef fonksiyon ikili tam sayı çıktısını iki'nin tümleyeninde $(s, b_0, \dots, b_{L-1}) \in \{0,1\}^{L+1}$ olarak ürettiğinde, **$\mathbb{Z} \hookrightarrow \mathbb{C}$ işaretli bit-toplama**
>     $$\widetilde{C}_n(X) = \sum_{j=0}^{L(n)-1} 2^j \tilde{b}_j(X) - 2^{L(n)} \tilde{s}(X)$$
>     **bölmesiz ve GRH varsayımı olmaksızın** $\widetilde{C}_n \equiv f_n \pmod{I_B}$ sağlar ($O(L)$ ek kapı, $0$ çarpım derinliği).  
>   - $\mathbb{F} = \mathbb{F}_p$ ($p \ge 3$) dalında ise $\log p \le \mathrm{poly}(n)$ yeterlidir ($p=2$ hariç tutulur).  
>   *(Not: GRH yalnızca ters yöndeki $\mathbb{C} \to \overline{\mathbb{Q}} \to \mathbb{F}_p$ Koiran/Bürgisser uzmanlaşmasında $\exists p,\ \log p \le \mathrm{poly}(n)$ garantisi için gerekir.)*
>
> - **H4 (Nicel $\mathrm{SAT}$-İndirgenebilirlik / Karar-Sayım Köprüsü):**  
>   Hedef Boolean fonksiyonu ($\mathbb{F}=\mathbb{C}$ iken $f_n|_{\{0,1\}^n}$'in bit temsili; $\mathbb{F}=\mathbb{F}_p$ iken $f_n \bmod p$), girdi uzunluğu $m(n) \le n^c$ olan en fazla $q(n) \le n^a$ adet $\mathrm{SAT}_m$ kâhin sorgusu, $S_R(n) = \mathrm{poly}(n)$ kapılı ve $D_R(n)$ derinlikli bir indirgeme devresi ile $r_d(n)$ adaptif turda hesaplanır ($a, c > 0$ sabit).
>
> **Teoremin Hükmü:**  
> $\mathrm{SAT}_m$'i çözen $(S_B(m), D_B(m))$ boyut/derinlikli Boolean devreleri varsa, toplam Boolean devresi $S_{\mathrm{tot}}(n) = O\big(S_R(n) + q(n) S_B(m(n)) + L(n)\big)$ boyutunda olur ve işaretli bit-toplama sonrasında $\operatorname{AC}_{\mathbb{F}}^{\text{bölmesiz}}(g) \le O(S_{\mathrm{tot}}(n))$ sağlanır. Dolayısıyla **(H1–H4)** altında:
> - **Genel Rejim (H2a):** Sonsuz çoklukta (`i.o.`) $m$ için $S_B(m) \ge 2^{\Omega(m^{\varepsilon/c})}$, yani $\mathrm{SAT} \notin \mathrm{P}/\mathrm{poly}$ (`i.o.`).
> - **Sığ Rejim (H2b):** $D_R(n)=O(\log n), r_d(n)=O(1)$ iken sonsuz çoklukta `i.o.` $\mathrm{SAT} \notin \mathrm{NC}^1$ ($D_B(m)=O(\log m)$ ise $S_B(m) \ge 2^{\Omega(m^{\varepsilon/c})}$).

---

## 2. Dört Alt-Sorunun Doğrudan ve Eksiksiz Yanıtları

### Alt-Soru 1: İndirgeme hangi bilgileri korumalı?
- **Neden `#P`-tamlık yetmez (`No-Go`):** Toda teoremi ($\mathrm{PH} \subseteq \mathrm{P}^{\#\mathrm{P}}$) **ters yöndedir**: $\mathrm{SAT} \in \mathrm{P}/\mathrm{poly}$ yalnızca Karp–Lipton ($\mathrm{PH} \subseteq \Sigma_2^p/\mathrm{poly}$) ve Stockmeyer (1983) üzerinden `#P` fonksiyonlarının $\mathrm{BPP}^{\mathrm{NP}}$ içinde *çarpımsal yaklaşıklığını* verir; **kesin sayımı** (`ExactCount` veya $\mathrm{perm}_n \bmod 3$) vermez. Bürgisser (2000, GRH) de yalnızca $\mathrm{VP}_k = \mathrm{VNP}_k \implies \mathrm{PH}/\mathrm{poly} = \mathrm{NC}/\mathrm{poly}$ yönünü verir; kontrapozitif dahi $\mathrm{P}^{\#\mathrm{P}}$ veya $\mathrm{PH}/\mathrm{poly} \neq \mathrm{NC}/\mathrm{poly} \implies \mathrm{VP}\neq\mathrm{VNP}$ üretir, cebirsel zorluktan `SAT` alt sınırı çıkarmaz. Valiant–Vazirani izolasyonu ise cebirsel yapıyı/kesin sayıyı değil, yalnızca boş-olmama kararını tek çözümlü olaya indirger.
- **Koruması gereken bilgi (`H4`):** İndirgeme, cebirsel hedefi $f_n(x)$ (veya $f_n(x)\bmod p$, $p\ge 3$) yalnızca `#P`'ye değil **doğrudan `SAT`'a** ($f_n \in \mathrm{P}^{\mathrm{SAT}}/\mathrm{poly}$) taşımalıdır: $q(n) \le n^a$ kâhin sorgusu, sorgu başına CNF/devre boyutu $m(n) \le n^c$, $S_R(n) = \mathrm{poly}(n)$ ve derece-kısıtlı rejimde ek olarak $D_R(n)=O(\log n), r_d(n)=O(1)$.
- *(Tur 2 düzeltmesi:)* `0g-pisagor`'un Tur 1'de önerdiği "$\deg(\phi_n)=\deg(f_n)$ CNF şartı" tanımsızdır; Tur 2'deki $q\cdot m$ formülü de kâhin devresi yerine girdi boyutu $m$ kullandığı için `critic` tarafından $q\cdot S_B(m)$ olarak düzeltilmiştir.

### Alt-Soru 2: Alan değişimi ($\mathbb{C} \to \overline{\mathbb{Q}} \to \mathbb{Z} \to \mathbb{F}_p \to \mathbb{F}_2$) karmaşıklığı nasıl etkiler?
- **Boolean $\to \mathbb{C}$ yönü (GRH gerektirmez):** $f_n \in \mathbb{Z}[X]$, $\{0,1\}^n$ üzerinde $L(n)=\mathrm{poly}(n)$ bit içinde kalıyorsa, $\mathrm{SAT}$ kâhin devresinden çıkan bitler bölme-serbest iki'nin tümleyeni toplamı $\sum_{j=0}^{L-1} 2^j \tilde{b}_j - 2^L \tilde{s}$ ile doğrudan $\mathbb{Z} \hookrightarrow \mathbb{C}$'ye gömülür; yalnızca $O(L)$ ek kapı ekler ve **GRH veya CRT gerektirmez** (`prof-wigner` `#170`, `prof-valiant` `#169`).
- **$\mathbb{C} \to \overline{\mathbb{Q}} \to \mathbb{F}_p$ yönü (Koiran 1996 / Bürgisser 2000):** $\mathbb{C}$ sabitlerini elemek için Hilbert Nullstellensatz üzerinden $\overline{\mathbb{Q}}$'ya geçilir; sıfır-olmayan bölen/katsayı koşulunu bozmayan asal seçimi koşulsuz olarak yalnızca $\log p \le 2^{\mathrm{poly}(n)}$ garantilerken, **GRH altında** $\exists p,\ \mathbf{\log p \le \mathrm{poly}(n)}$ ($p \le 2^{\mathrm{poly}(n)}$; Tur 1'deki $p\le\mathrm{poly}(n)$ değil!) elde edilir. `poly(log p)` bitlik CRT yeniden inşası Boolean simülasyonuna yeter, ancak Lagrange interpolasyonu ($\deg=O(p)$) patlar.
- **Karakteristik-2 Çöküşü (`p = 2`):** $\mathrm{perm}_n \equiv \det_n \pmod 2 \in \mathrm{NC}^2 / \oplus\mathrm{L}$ ($-1 \equiv +1$) olduğundan $\mathrm{char}=2$'de `#P`-zorluğu tamamen çöker. Bu nedenle `0g-oklid`'in Tur 2'de dahi savunduğu çift-taraflı $|\mathrm{AC}_{\mathbb{C}}(f_n) - \mathrm{AC}_{\mathbb{F}_p}(f_n\bmod p)| \le O(\log p)+O(L)$ eşitsizliği **kesin olarak yanlıştır** (karşı-örnek: $f_n = p \cdot \mathrm{perm}_n \implies f_n \bmod p \equiv 0$, fark üsteldir).

### Alt-Soru 3: Booleanlaştırma sırasında derece ve devre boyutu nasıl değişir?
- **Boyut vs Biçimsel Derece Patlaması:** $(S_{\mathrm{tot}}, D_{\mathrm{tot}})$ boyut ve çarpım-derinlikli Boolean devre $\tilde{x}\wedge\tilde{y} = \tilde{x}\tilde{y}$, $\neg\tilde{x} = 1-\tilde{x}$, $\tilde{x}\vee\tilde{y} = \tilde{x}+\tilde{y}-\tilde{x}\tilde{y}$ dönüşümüyle $\mathbb{F}$ üzerinde **bölmesiz** olarak boyut **$O(S_{\mathrm{tot}})$** verirken, sentaktik/biçimsel derece katman başına $2$ ile çarpılarak **$\Delta_{\mathrm{circ}} \le 2^{D_{\mathrm{tot}}}$** olur (`Lemma H2-func`, `prof-hilbert` `#168`).
- **Multilinearizasyon ($I_B = \langle x_i^2 - x_i \rangle$) ve Homojenleştirmenin Çöküşü:** Kapı-başı $I_B$ multilinearizasyon devre boyutunu korumaz (üstel patlama, `0g-arsimet` Tur 2'de geri çekti). Tersine, $I_B$ modülosunda yüksek dereceli terimler $x_i^k \equiv x_i$ olarak geri katlandığı için Strassen ($O(d^2 S)$) homojenleştirmesi de **bozulur**: $\deg \le \mathrm{poly}(n)$ olmayan katmanları budamak $\{0,1\}^n$ fonksiyonunu değiştirir (`prof-euler` `#172`).
- **İki Rejim Dikotomisi:**
  1. $D_{\mathrm{tot}} = O(\log d(n))$ ($\mathrm{NC}^1$) iken $\Delta_{\mathrm{circ}} = \mathrm{poly}(d(n))$ kalır; fakat burada bile $\tilde{C}_n \equiv f_n \pmod{I_B}$ olduğundan **biçimsel $\operatorname{AC}(f_n)$ yetmez**, derece-kısıtlı *fonksiyonel* $\operatorname{AC}_{\mathbb{F}}^{\mathrm{func}, \le \Delta}(f_n)$ şarttır (`#168`).
  2. **$D_{\mathrm{tot}} = \omega(\log d(n))$** eşiğinde $\Delta_{\mathrm{circ}}$ üstel patlar ($2^{D_{\mathrm{tot}}}$ süperpolinom olur) ve derece-kısıtlı aktarım **çöker** (Tur 1'deki hatalı $D_B > \varepsilon\log_2 n$ sınırı `critic` tarafından düzeltildi). Genel $\mathrm{P}/\mathrm{poly}$ için derece-serbest fonksiyonel alt sınır ($\operatorname{AC}_{\mathbb{F}}^{\mathrm{func}}$, Forbes–Kumar–Saptharishi 2016) zorunludur.
- *(Bit-toplama ve `i.o.` hassasiyeti):* İşaretli bit-toplama $\sum 2^j \tilde{b}_j - 2^L \tilde{s}$ yalnızca toplama derinliğini $O(\log L)$ artırır, çarpım derecesini artırmaz; $m(n)\le n^c$ şartı $m(n)\to\infty$ gerektirdiğinden $S_B(m) \ge 2^{\Omega(m^{\varepsilon/c})}$ **sonsuz çoklukta (`i.o.`)** elde edilir (`#174`).

### Alt-Soru 4: Bu aktarım bilinen ispat bariyerleriyle çelişmeden kurulabilir mi?
- **Kime Uygulanır?** Bariyerler soyut aktarım teoremine (`(H1–H4) ⇒ SAT alt sınırı`) tek başına değil, **birleşik `(H1 + H4)` SAT alt sınır kanıtına** uygulanır (`Lemma H4-B`, `prof-noether` `#167`):
  - **Relativization (BGS75):** Kapı-başı beyaz-kutu aritmetizasyon non-relativizing olduğu için BGS75 ile çelişmez.
  - **Algebrization (AW09):** `H3` bit-toplama adımı tek başına algebrize olur; birleşik kanıtın AW09'u aşabilmesi için **`H1`'in** (GCT yörünge kapanışı / iç devre yapısı) veya **`H4`'ün** (beyaz-kutu SAT-devre denetimi) **en az bir non-algebrizing adım** içermesi şarttır (`#167`).
  - **Natural Proofs (RR97) & Algebraic Natural Proofs (FSV18/GKSS17):** Açık tek bir $f_n$ ailesini `H4` üzerinden `SAT`'a bağlamak rastgele doğruluk tabloları üzerinde *largeness* gerektirmediği için RR97'yi otomatik tetiklemez; ancak birleşik argüman Boolean-doğal bir özelliğe indirgenmemelidir. Asıl tehlike **`H1`'in kendisindedir**: `H1` kanıtı $\mathrm{char}\neq 2$'de FSV18/GKSS17 anlamında katsayı uzayında *constructive* ve *large* olmamalı (simetri/çokluk engelleriyle *largeness*'ı kırmalı) ve $T_n$-kısıtlı / *Simetri-Tersine Çevirme Tuzağı*'na düşen oyuncak alt modellerde değil, genel simetrisiz devrelerde kanıtlanmalıdır.

---

## 3. Kesin İmkânsızlık (No-Go) ve Karşı-Örnek Matrisi

| Gevşetilen Hipotez | Ne Kırılır? | Kesin Karşı-Örnek / İmkânsızlık Nedeni |
| :--- | :--- | :--- |
| **`¬H1` (Biçimsel $\mathrm{AC}$ ile yetinme)** | $I_B = \langle x_i^2-x_i\rangle$ modülo eşdeğerlik | $g_n(X) = \mathrm{perm}_n(X)\cdot (x_1^2 - x_1)$: biçimsel $\operatorname{AC}(g_n)$ üstel olsa dahi $\{0,1\}^{n^2}$ üzerinde özdeş olarak $0$'dır ($S_B = O(1)$). |
| **`¬H2` ($D_{\mathrm{tot}} = \omega(\log d)$ veya $r_d = \omega(1)$)** | Derece koruması ($\Delta_{\mathrm{circ}} \le 2^{D_{\mathrm{tot}}}$) | $\Delta_{\mathrm{circ}} = 2^{\omega(\log n)} = n^{\omega(1)}$ patlar; $I_B$ modülosunda Strassen homojenleştirme çalışmadığından derece-kısıtlı alt sınır aktarılamaz. |
| **`¬H3` ($\mathrm{char}=2$ veya çift-yönlü alan farkı)** | İşaret bilgisi / Sıfır indirgenmesi | $p=2$: $\mathrm{perm}_n \equiv \det_n \pmod 2 \in \mathrm{NC}^2 / \oplus\mathrm{L}$ (`¬∈ AC^0`). Çift-yönlü fark iddiası: $f_n = p\cdot\mathrm{perm}_n \equiv 0 \pmod p$ (`#174`). |
| **`¬H4` (Yalnız `#P`-tamlık / Toda yönü)** | `#P` $\to$ `NP` karar indirgenebilirliği | Toda ($\mathrm{PH}\subseteq\mathrm{P}^{\#\mathrm{P}}$) terstir; Stockmeyer yalnızca $\mathrm{BPP}^{\mathrm{NP}}$ yaklaşık sayım verir. `H4` olmadan $\mathrm{P}=\mathrm{NP}\neq\mathrm{Mod}_3\mathrm{P}$ tutarlıdır. |
| **`¬H5` (Doğal / Simetri-kısıtlı `H1`)** | Bariyer uyumu & Genel devre kapsamı | FSV18-doğal veya $T_n$-eşdeğişir/Betti (*Simetri-Tersine Çevirme Tuzağı*) sınırlar genel Boolean aritmetizasyonu altındaki asimetrik devrelere taşınmaz. |

---

## 4. İki Turun Evrim İzi (`0G` × `Swarm` × `critic` × `moderator`)

Bu sonuç masa başı tek seferlik tahminle değil, `critic`'in iki kez tüm grubu sertçe budamasıyla olgunlaştı:

1. **Tur 1 $\to$ `critic` (`#164`) $\to$ `moderator` (`#165`):**
   - **0G Grubunda yakalanan büyük hatalar:** `0g-pisagor` (CNF için tanımsız $\deg(\phi_n)$ ve ters Toda), `0g-oklid` (ters $\mathrm{AC}_{\mathbb{F}_p} \ge \mathrm{AC}_{\mathbb{C}}-O(\log H)$ formülü, yanlış $p\le O(\log^2 n)$ GRH sınırı, tanımsız $\mathrm{disc}(f_n)$), `0g-arsimet` (boyut patlatan kapı-başı $I_B$ normalizasyonu), `0g-gauss` (ters eşitsizlik yönü), `0g-harezmi` (döngüsel $\mathrm{NEXP}\not\subset\mathrm{P}/\mathrm{poly}$ varsayımı), `0g-ramanujan` (uydurma PAC/VC hipotezleri, sahte $2^{n^\varepsilon}\to 2^{cn}$ sıçraması ve yanlış $\mathrm{perm}_n\bmod 2 \in \mathrm{AC}^0$ iddiası).
   - **Swarm Grubunda yakalanan ince hatalar:** `prof-wigner` ($p\le\mathrm{poly}(n)$ yerine $\log p\le\mathrm{poly}(n)$ düzeltildi), `prof-strassen` ($\mathrm{NC}/\mathrm{poly}$ $O(\log^c n)$ hatası $\mathrm{NC}^1$ $O(\log n)$'e düzeltildi, GRH yalnız ters $\mathbb{C}\to\mathbb{F}_p$ yönüne alındı), `prof-hilbert` & `prof-euler` ($\mathrm{NC}^1$'de bile fonksiyonel alt sınır gerektiği netleştirildi, Euler'in yanlış $D_B > \varepsilon\log_2 n$ eşiği silindi), `prof-noether` (bariyerlerin aktarıma değil birleşik `(H1+H4)`'e uygulandığı düzeltildi), `prof-valiant` (`(q, m, r_d)` nicelemesi ve bölme-serbest $\mathbb{Z}$-bit-toplama eklendi).
2. **Tur 2 (`0G_QUANT_TRANSFER_R2.md`, `#167–#172`) $\to$ Final Denetim (`#174`) $\to$ `Teorem v2` (`#175`):**
   - Swarm Konseyi 6 üyesinin tamamı `#164`–`#165` düzeltmelerini formal lemmalara dönüştürdü; `critic` `#174`'te kalan son üç ince detayı da kapattı (`prof-valiant` v2'deki gereksiz $a^{p-2}$ bölmesi ve eksik $r_d=O(1), D_R=O(\log n)$, bit-toplamanın yalnızca toplama derinliği eklemesi ve `i.o.` kuantifikasyonu).
   - 0G Grubunda `0g-arsimet` FKS16 çerçevesine başarıyla uyum sağlasa da, `0g-oklid` çift-taraflı $|\mathrm{AC}_{\mathbb{C}}-\mathrm{AC}_{\mathbb{F}_p}|$ farkında, `0g-gauss` derinlik çöküş yönünde, `0g-pisagor` ise $q\cdot m$ kâhin maliyetinde hatalarını sürdürdü; tamamı `critic` (`#174`) tarafından elenerek yalnızca sağlam parçalar `Teorem v2`'ye alındı.

---

## 5. Gerçek Açık Araştırma Sınırları (`[AÇIK]`)

`Teorem v2`, cebirsel karmaşıklıktan $\mathrm{SAT}$'a geçişin **koşullu şemasını** matematiksel olarak kapatır; ancak aşağıdaki **iki temel girdi** bugün hâlâ tamamen `[AÇIK]`tır ve mevcut literatürde her ikisinin birden kurulduğu tek bir fonksiyon ailesi yoktur:
1. **Genel Derinlikte Derece-Serbest Fonksiyonel Alt Sınır (H1):** Forbes–Kumar–Saptharishi (2016) fonksiyonel alt sınırları yalnızca sığ (sabit derinlik / multilinear) devrelerde kurabilmiştir; sınırsız derinlikli bölmesiz devreler için $\operatorname{AC}_{\mathbb{F}}^{\mathrm{func}}(f_n) \ge 2^{n^\varepsilon}$ (veya $\omega(\mathrm{poly}(n))$) tamamen açıktır.
2. **`H4`'ü Sağlayan Üstel Zorlukta Açık $f_n$ (Ters-Toda Boşluğu):** Bilinen tüm $\operatorname{AC}$ adayları (`perm_n`, `#P`-tam polinomlar) `#P`/`Mod_p P` sınıfındadır ve $\mathrm{P}^{\mathrm{SAT}}/\mathrm{poly}$ içine indirgendiği (`H4`) bilinmemektedir; tersine, `NP` (`SAT`) içine indirgenen bir fonksiyonun $\operatorname{AC}_{\mathbb{F}}^{\mathrm{func}} \ge 2^{n^\varepsilon}$ taşıdığını kanıtlamak zaten $\mathrm{NP} \not\subseteq \mathrm{P}/\mathrm{poly}$ ile eş-güçlüdür.
