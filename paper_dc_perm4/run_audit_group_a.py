"""
Group A ("Kanıt Denetimi" — cebirsel odak) 12-Agent, 4-Round Audit Workflow
for paper_dc_perm4/ (dc_perm4_ge_10.tex, verify_codim_sing_perm4.py, README.md).
Writes full structured dossier to paper_dc_perm4/AUDIT_GROUP_A.md.
"""
import os

BASE_DIR = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct"
PAPER_DIR = os.path.join(BASE_DIR, "paper_dc_perm4")

with open(os.path.join(PAPER_DIR, "dc_perm4_ge_10.tex"), "r", encoding="utf-8") as f:
    TEX_SRC = f.read()
with open(os.path.join(PAPER_DIR, "verify_codim_sing_perm4.py"), "r", encoding="utf-8") as f:
    PY_SRC = f.read()
with open(os.path.join(PAPER_DIR, "README.md"), "r", encoding="utf-8") as f:
    README_SRC = f.read()
with open(os.path.join(BASE_DIR, "QUANTITATIVE_TRANSFER_THEOREM_SYNTHESIS.md"), "r", encoding="utf-8") as f:
    TRANSFER_EXCERPT = f.read()[:2800]

PRELIM_CONTEXT = f"""=== ORTAK GÖREV VE ÖN HAKEM NOTLARI ===
Bağlam: dc_perm4_ge_10.tex makalesi C üzerinde dc(perm_4) >= 10 iddiasını şu zincirle kanıtlıyor:
1) codim Sing(V(perm_4)) = 8 (IMSC/Macaulay sertifikası, L_8 üzerinde).
2) str(perm_4) = 4, ve r = corank(A_0) = 1 zorunluluğu (r = 0, 2, 3, 4, >=5 elenir).
3) m = 9 için origin-isotropy, 2-blok normal form, [t^3]=0'dan xi-lineer kısıtlar, Skew-Square Lemması, perm_4 in I_W^3 => W^perp subset Sing_2.
4) codim Sing_2(V(perm_4)) = 12, çelişki.

Ön hakem şüpheleri (doğruluğunu SİZ denetleyeceksiniz):
- r = 3 vakasında "rank <= 2 olan 3x3 lineer uzaylar iki tiptir (sıfır satır, çarpık-simetrik)" denmiş. Şüphe: 2x2 sıfır bloklu sıkıştırma uzayı tipi eksik olabilir; ayrıca sıfır sütun ve sıfır satırın GL_3 x GL_3 + devrik (transpose) ile eşlenip eşlenmediği kontrol edilmeli.
- Teorem 3.1 yalnız IMSC Python betiğine dayanıyor; bağımsız CAS (Singular / Macaulay2) kontrolü yok. Yerel makinede M2, Singular, Sage ve SymPy kurulu değildir.
- README'deki Macaulay2 komutunda 'permanent' fonksiyonunun varlığı doğrulanmamıştır.
- Literatür iddiaları (Yabe 2015: R üzerinde (n-1)^2+1; ABV 2017: dc >= codim Sing + 1; Mignon-Ressayre n^2/2; Atkinson 1983; Eisenbud-Harris 1988) birincil kaynaktan denetlenmelidir.
- L_9 negatif kontrolü kodun "her şeyi sıfırlamadığını" gösterir, doğru ideali kurduğunu göstermez. perm_3 için codim Sing = 6 pozitif kontrolü eksik.

Üç Karar Sorusu:
Q1. r = 3 vakası düzeltildiğinde makale mantıksal olarak kapanıyor mu? Düzeltilmiş vaka paragrafı ne olmalı?
Q2. codim Sing(V(perm_4)) = 8 için hangi bağımsız doğrulama yapılmalı, hangi sonuç çıkarsa teorem tutarlı sayılır?
Q3. Uzmana gönderilmeden önce makalede neler değişmeli? Boolean/SAT aktarım teoremi nerede ve nasıl yer almalı? (Öneri: ayrı sonuç olarak değil, en fazla H1 ve H4 [AÇIK] vurgulu 'Motivasyon/Tartışma' bölümü.)

=== BAĞLAYICI KURALLAR ===
1. Her iddia şu etiketlerden TAM BİRİNİ taşımalıdır: [İSPAT], [KESİN HESAP], [SAYISAL], [SANI], [LİTERATÜR-DOĞRULANMADI].
2. YASAKLI İFADELER: "%100 kanıtlandı", "dünya rekoru", "konsey teoremi".
3. Başka bir ajanın ispat adımını sahiplenmeden önce kendin adım adım yeniden türet.
4. Bilmediğin literatür detayını ASLA uydurma; gerekiyorsa "Bilmiyorum, birincil kaynaktan kontrol edilmeli [LİTERATÜR-DOĞRULANMADI]" yaz.
5. Hata bulmak başarıdır; savunmaya geçme, düzeltme öner.
6. Hiçbir araç (run_command, read_file, write_file, search_web vb.) ÇAĞIRMA; tüm yanıtını doğrudan `finish` aracına kısa, madde madde Türkçe metin olarak ver.
"""

FULL_DOCS = f"""=== dc_perm4_ge_10.tex ===
{TEX_SRC}

=== verify_codim_sing_perm4.py ===
{PY_SRC}

=== README.md ===
{README_SRC}

=== QUANTITATIVE_TRANSFER_THEOREM_SYNTHESIS.md (Özet) ===
{TRANSFER_EXCERPT}
"""

COMMON_SYS = (
    "Sen Grup A ('Kanıt Denetimi' — cebirsel odak) içinde hakem düzeyinde bir araştırmacısın.\n"
    + PRELIM_CONTEXT
)

GROUP_A_SPECS = [
    ("A-cebirsel-geometri", "Matematikçi — Cebirsel Geometri: Sing, codim, Nullstellensatz, Krull ve Prop 2.3 (Sing_2) hesabını satır satır denetle; L_8 affine kesitinin P^15 -> C^16 konik boyut indirgemesinde boşluk var mı bak."),
    ("A-sınırlı-rank-uzayları", "Matematikçi — Sınırlı Rank Uzayları: Atkinson (1980/1983), Eisenbud-Harris (1988), Beasley sınıflandırmasını 3x3 rank<=2 uzaylar için denetle (1x3 sıfır, 3x1 sıfır, 2x2 sıfır sıkıştırma bloğu, so_3); GL_3 x GL_3 + devrik M(tX) üzerindeki etkisini kontrol et."),
    ("A-determinantal-karmaşıklık", "Matematikçi — Determinantal Karmaşıklık: ABV 2017, Mignon-Ressayre 2004, Yabe 2015, Landsberg-Ressayre 2017 ve sınır karmaşıklığı bağlamını doğrula; emin olmadıklarını [LİTERATÜR-DOĞRULANMADI] işaretle."),
    ("A-lineer-cebir", "Matematikçi — Lineer Cebir: Skew-Square Lemması (K tekilken dahil), Prop 4.1 r=0,2,3,4,>=5 ve Theorem 1.1 Step 1-4 (Schur açılımı, b(X)=0, [t^2],[t^3],[t^4] ve xi-katsayı ayrımı) satır satır yeniden türet."),
    ("A-değişmeli-cebir", "Matematikçi — Değişmeli Cebir: IMSC (step_imsc) syzygy baz indirgeme mantığının Hilbert fonksiyonu / Macaulay matrisi açısından matematiksel denkliğini denetle; I_W = <y,z> üzerindeki UFD ve bölünebilirlik adımlarını kontrol et."),
    ("A-kombinatorik", "Matematikçi — Kombinatorik: Prop 2.3'teki 2x2 alt-permanent destek grafiği G(X) argümanını, char != 2 altında a>=2, b>=3 çelişkisini, bileşen sayımını (4+4+36) ve verify_codim_sing_perm4.py içindeki subperm3 indekslemesini denetle."),
    ("A-hakem", "Matematikçi — Dergi Hakemi: Makaleyi hakem gözüyle oku; eksik gerekçeleri, notasyon hatalarını (örn. perm_4'te adj/tr veya I_W^3 tanımı, README'deki M2 permanent hatası), abartıları ve sunum boşluklarını listele."),
    ("A-mat-fizikçi-simetri", "Fizikçi — Matematiksel Fizik / Simetri: P, Q in GL_m(C) ve P in GL_8(C) normal form seçimlerinin, A_0 = diag(0_r, I_w) + blok-köşegenleştirmesinin ve M(X)^T devrik işleminin det, [t^k] ve genelliği bozmadığını denetle."),
    ("A-kuantum-bilgi", "Fizikçi — Kuantum Bilgi / Tensör & İzotropi: Omega simetrik bilineer formu, v^T u = 0 => S tamamen izotropik => dim S <= 8 adımını ve F^T/rank argümanlarını bağımsız yeniden türet; H1/H4 [AÇIK] SAT aktarım notunun konumunu değerlendir."),
    ("A-hesaplamalı-fizikçi", "Fizikçi — Hesaplamalı Fizik / Bağımsız Doğrulama: verify_codim_sing_perm4.py'deki float64 BLAS aritmetik taşma sınırını (block_size*p^2 << 2^53), p1,p2 modüler rank -> Q mantığını, L_9 negatif kontrolünü ve eksik perm_3 (codim=6) pozitif kontrolünü denetle."),
]

agents = {
    name: agent(
        prompt=f"{COMMON_SYS}\nSENİN ROLÜN: {name}\nODAK ALANIN: {focus}\n{FULL_DOCS}",
        schema={"type": "string"},
        role=name,
        model="flash",
    )
    for name, focus in GROUP_A_SPECS
}

crit_a = agent(
    prompt=(
        f"{COMMON_SYS}\nSENİN ROLÜN: crit-A (Eleştirel Soru Soran)\n"
        "Görevin: Grup A'daki her üyenin bulgularına acımasızca saldırmak ve şu 3 soruyu sormaktır: "
        "(1) Karşı-örnek var mı? (2) Hipotez nerede kullanıldı? (3) Bu vaka listesi gerçekten tam mı? "
        "Her ajanın adını '### <ajan-adı>' başlığı altında ayrı ayrı etiketle.\n"
        f"{FULL_DOCS}"
    ),
    schema={"type": "string"},
    role="crit-A",
    model="flash",
)

mod_a = agent(
    prompt=(
        f"{COMMON_SYS}\nSENİN ROLÜN: mod-A (Grup A Moderatörü)\n"
        "Görevin: Tüm kanıt adımlarını tek tek 'kabul / red / belirsiz' oy sayımıyla değerlendirmek, "
        "crit-A'nın cevapsız kalan sorularını açıkça kaydetmek, Q1/Q2/Q3 karar sorularını yanıtlamak ve zorunlu kapanış biçimini üretmek.\n"
        f"{FULL_DOCS}"
    ),
    schema={"type": "string"},
    role="mod-A",
    model="flash",
)

# --- TUR 1: Bağımsız Okuma ---
phase("Grup A — Tur 1: Bağımsız Okuma")
t1_prompt = (
    "TUR 1 (Bağımsız Okuma): Yalnız kendi uzmanlık merceğinden makaleyi, Python doğrulama betiğini ve README'yi oku. "
    "En fazla 5 kısa, madde madde bulgu yaz (hata, boşluk, belirsizlik veya somut düzeltme önerisi). "
    "Her maddede zorunlu etiketi ([İSPAT], [KESİN HESAP], [SAYISAL], [SANI], [LİTERATÜR-DOĞRULANMADI]) kullan. (<= 220 kelime)"
)
t1_outputs = await parallel(
    GROUP_A_SPECS,
    lambda spec: agents[spec[0]](t1_prompt),
)
t1_digest = "\n\n".join(f"### {spec[0]}\n{out}" for spec, out in zip(GROUP_A_SPECS, t1_outputs))
log(f"Tur 1 tamamlandı ({len(t1_outputs)} ajan).")

# --- TUR 2: Çapraz Saldırı ---
phase("Grup A — Tur 2: Çapraz Saldırı")
crit_prompt = (
    "TUR 2 (Çapraz Saldırı — crit-A): Aşağıda Grup A'daki 10 uzmanın Tur 1 bulguları var. "
    "Her uzman için '### <ajan-adı>' başlığı aç ve en az bir sert karşı soru sor ('karşı-örnek var mı?', 'hipotez nerede kullanıldı?', 'vaka listesi tam mı?', 'etiket doğru mu?'). "
    "Ayrıca ön hakem notlarındaki 2x2 sıfır bloğu, perm_3 kontrolü ve M2 permanent fonksiyonu konularında gevşek kalanları özellikle sıkıştır. (<= 650 kelime)\n\n"
    f"{t1_digest}"
)
crit_attacks = await crit_a(crit_prompt)

t2_outputs = await parallel(
    GROUP_A_SPECS,
    lambda spec: agents[spec[0]](
        f"TUR 2 YANITI: crit-A'nın tüm gruba yönelttiği eleştiriler aşağıdadır. Kendi '### {spec[0]}' başlığın altındaki sorulara doğrudan yanıt ver, "
        f"haklıysa bulgunu geri çek/düzelt, iddianı koruyorsan yeniden türeterek kanıtla. Her maddede etiket kullan. (<= 180 kelime)\n\n{crit_attacks}"
    ),
)
t2_digest = "\n\n".join(f"### {spec[0]} (Tur 2 Yanıtı)\n{out}" for spec, out in zip(GROUP_A_SPECS, t2_outputs))
log("Tur 2 tamamlandı.")

# --- TUR 3: Üretim ---
phase("Grup A — Tur 3: Üretim (r=3 LaTeX, CAS Betikleri, Değişiklik Listesi, Gönderim Planı)")
prod_tasks = [
    (
        "A-sınırlı-rank-uzayları",
        "TUR 3a — r=3 VAKASI DÜZELTİLMİŞ LATEX PARAGRAFI:\n"
        "Ön hakem şüphesini ve Tur 1-2 denetimini esas alarak dc_perm4_ge_10.tex Proposition 4.1 içindeki 'Case r = 3' için EKSİKSİZ düzeltilmiş LaTeX paragrafını yaz. "
        "Kontrol et: (1) 3x3 rank<=2 lineer uzaylarının tam sınıflandırması (Atkinson / Eisenbud-Harris: compression uzayları = 1x3 sıfır satır, 3x1 sıfır sütun [devrik ile eşlenir] VE 2x2 sıfır bloklu sıkıştırma tipi [örn. yalnız 1. satır + 1. sütun dolu], artı primitiftip so_3(C)). "
        "(2) 2x2 sıfır bloklu durumda adj(B(X))'in ne olduğunu açıkça hesapla (rank-1 dış çarpım veya sıfır, buradan perm_4 = -tr(adj(B)UV) => str(perm_4) <= 2 < 4!). "
        "(3) Her adım [İSPAT], literatür atıfları gerekiyorsa [LİTERATÜR-DOĞRULANMADI] etiketi taşısın. Saf LaTeX kod bloğu + kısa gerekçe ver."
    ),
    (
        "A-hesaplamalı-fizikçi",
        "TUR 3b — BAĞIMSIZ SINGULAR VE MACAULAY2 DOĞRULAMA BETİKLERİ:\n"
        "README'deki 'permanent' fonksiyonu şüphesini ortadan kaldıracak, yerleşik permanent fonksiyonu KULLANMADAN açık S_3 / S_4 permütasyon toplamıyla çalışan "
        "iki tam bağımsız betik yaz: (1) Macaulay2 (.m2) ve (2) Singular (.sing). "
        "Her ikisi de şu 3 kontrolü içermeli: (i) perm_3 pozitif kontrolü (codim Sing(perm_3) == 6), (ii) perm_4 tam Jakobiyen ideali (codim == 8) ve/veya L_8 kesiti, (iii) L_9 negatif kontrolü (dim >= 1). "
        "Makinede M2/Singular kurulu olmadığını ve bunların [KESİN HESAP — HENÜZ ÇALIŞTIRILMADI] olduğunu açıkça belirt."
    ),
    (
        "A-hakem",
        "TUR 3c — MAKALE DEĞİŞİKLİK LİSTESİ:\n"
        "Tur 1-2'de bulunan tüm hatalar ışığında dc_perm4_ge_10.tex ve README.md için satır/bölüm bazlı somut değişiklik listesi üret (Q3 kapsamında Boolean/SAT aktarım notunun yalnız H1/H4 [AÇIK] vurgulu kısa 'Motivation / Open Limitations' olarak eklenip eklenmeyeceği dahil). Madde madde ve etiketli yaz."
    ),
    (
        "A-determinantal-karmaşıklık",
        "TUR 3d — UZMAN GÖNDERİM PLANI VE LİTERATÜR KONTROL LİSTESİ:\n"
        "Literatür doğrulama durumunu dürüstçe işaretleyerek ([LİTERATÜR-DOĞRULANMADI] dahil: ABV 2017 Teorem 1.2 codim>4, MR04 n^2/2, Yabe 2015 R üzerinde (n-1)^2+1, Landsberg-Ressayre edc=15, Atkinson/EH) "
        "bu makalenin hangi uzmanlara/dergilere gönderilmeden önce hangi son kapılardan geçmesi gerektiğini planla."
    ),
]
t3_outputs = await parallel(prod_tasks, lambda item: agents[item[0]](item[1]))
t3_cross = await agents["A-lineer-cebir"](
    "TUR 3 ÇAPRAZ DOĞRULAMA: A-sınırlı-rank-uzayları'nın yazdığı düzeltilmiş r=3 LaTeX paragrafını sıfırdan yeniden türeterek denetle; "
    "2x2 sıfır bloğunda adj(B) hesabını elle kontrol et ve herhangi bir boşluk kalıp kalmadığını [İSPAT] etiketiyle raporla:\n\n"
    + t3_outputs[0]
)
t3_digest = "\n\n".join([
    f"### (a) Düzeltilmiş r = 3 LaTeX Paragrafı (A-sınırlı-rank-uzayları)\n{t3_outputs[0]}",
    f"### (a-ek) Bağımsız Lineer Cebir Yeniden Türetimi (A-lineer-cebir)\n{t3_cross}",
    f"### (b) Bağımsız Singular & Macaulay2 Betikleri (A-hesaplamalı-fizikçi)\n{t3_outputs[1]}",
    f"### (c) Makale Değişiklik Listesi (A-hakem)\n{t3_outputs[2]}",
    f"### (d) Uzman Gönderim Planı (A-determinantal-karmaşıklık)\n{t3_outputs[3]}",
])
log("Tur 3 tamamlandı.")

# --- TUR 4: Son Hüküm ---
phase("Grup A — Tur 4: Moderatör Son Hükmü (mod-A)")
mod_prompt = f"""TUR 4 (SON HÜKÜM — mod-A):
Grup A'nın 4 turluk tüm çıktılarını sentezle. Kendi görüşünü en sona koy.

Aşağıdaki İKİ bölümü EKSİKSİZ üret:

BÖLÜM I — KANIT ADIMI OY SAYIMI (kabul / red / belirsiz):
Her ana adım (Prop 2.3 Sing_2=12, Thm 3.1 Sing=8 IMSC, str=4, r=0, r>=5, r=4, r=3 düzeltilmiş, r=2, Skew-Square Lemması, m=9 -> I_W^3 -> çelişki, README M2 kodu, Literatür iddiaları) için grup içi oylama özetini ve crit-A'nın cevaplanmamış kalan açık sorularını listele.

BÖLÜM II — ZORUNLU SON ÇIKTI BİÇİMİ:
1. Q1 / Q2 / Q3 cevapları (HER BİRİ EN FAZLA 10 SATIR, net ve numaralı).
2. "Kesin olarak doğru bulunanlar" ve "Hâlâ doğrulanmamış olanlar" listeleri (zorunlu etiketlerle).
3. Gruptaki en güçlü itiraz ve nasıl karşılandığı.
4. Güven düzeyi (düşük / orta / yüksek) ve nedeni.
5. Bir sonraki somut tek adım.
6. Azınlık görüşleri (varsa).

TUR 1 BULGULARI:
{t1_digest}

TUR 2 SALDIRI & YANITLAR:
{crit_attacks}

{t2_digest}

TUR 3 ÜRETİMLERİ:
{t3_digest}
"""
final_verdict = await mod_a(mod_prompt)

out_md = os.path.join(PAPER_DIR, "AUDIT_GROUP_A.md")
with open(out_md, "w", encoding="utf-8") as f:
    f.write("# GRUP A ('Kanıt Denetimi' — 12 Ajan, 4 Tur) Denetim Dosyası\n\n")
    f.write("## Tur 1 — Bağımsız Okuma (10 Uzman)\n\n" + t1_digest + "\n\n---\n\n")
    f.write("## Tur 2 — crit-A Saldırıları ve Yanıtlar\n\n### crit-A Soruları\n" + crit_attacks + "\n\n" + t2_digest + "\n\n---\n\n")
    f.write("## Tur 3 — Üretilen Düzeltme ve Doğrulama Çıktıları\n\n" + t3_digest + "\n\n---\n\n")
    f.write("## Tur 4 — mod-A Son Hükmü\n\n" + final_verdict + "\n")

log(f"Saved full dossier to {out_md}")
print(final_verdict)
