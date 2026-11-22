"""
Single 6-Agent Primary-Source Panel Audit:
  Konu 1: Sheshadri (arXiv:2611.06658) section-by-section independent re-derivation & comparison
  Konu 2: Independent value of dc(perm_4) >= 10, publishability verdict, & perm_5 scaling
  Konu 3: Border complexity (dc-bar) hand-proof attempt for R_9^{(4)} = P*Q & hidden-assumption audit

Writes full dossier to /Users/bl10buer/Desktop/matemk/p-vs-np-gct/paper_dc_perm4/AUDIT_SHESHADRI_AND_DCBAR.md
"""
from __future__ import annotations

import os

BASE_DIR = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct"
PAPER_DIR = os.path.join(BASE_DIR, "paper_dc_perm4")
SCRATCH_REFS = "/Users/bl10buer/.gemini/antigravity/brain/b557dfcd-0bd3-4f1e-bf17-b6827e3c03bd/scratch/arxiv_refs"
SHESHADRI_TEX = os.path.join(SCRATCH_REFS, "sheshadri", "per4_dc_15.tex")
ABV_TEX = os.path.join(SCRATCH_REFS, "abv", "PermVsDetarxiv.tex")
BORDER_DIR = os.path.join(SCRATCH_REFS, "sheshadri_border")


def read_lines(path: str, start: int | None = None, end: int | None = None) -> str:
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    s = 0 if start is None else start - 1
    e = len(lines) if end is None else end
    return "".join(lines[s:e])


# Load primary sources verbatim
OUR_TEX = read_lines(os.path.join(PAPER_DIR, "dc_perm4_ge_10.tex"))
ABV_PROOFS = read_lines(ABV_TEX, 213, 267)

SHESH_SEC1_3 = read_lines(SHESHADRI_TEX, 44, 617)
SHESH_SEC24_26 = read_lines(SHESHADRI_TEX, 317, 436)
SHESH_SEC4_5 = read_lines(SHESHADRI_TEX, 618, 1165)
SHESH_SEC6 = read_lines(SHESHADRI_TEX, 1166, 1686)
SHESH_SEC3_COMP = read_lines(SHESHADRI_TEX, 448, 561)
SHESH_SEC7 = read_lines(SHESHADRI_TEX, 1687, 1750)
SHESH_NO_COMP_GE10 = (
    "=== per4_dc_15.tex lines 216-387 + 497-506 (Computer-Free dc >= 10 Sub-Proof Inside Sheshadri) ===\n"
    + read_lines(SHESHADRI_TEX, 216, 388)
    + "\n...\n"
    + read_lines(SHESHADRI_TEX, 497, 507)
)

STRASSEN_REPORT_1_3 = read_lines(os.path.join(BASE_DIR, "council", "prof-strassen", "REPORT.md"), 1, 108)
STRASSEN_REPORT_15_17 = read_lines(os.path.join(BASE_DIR, "council", "prof-strassen", "REPORT.md"), 549, 659)

R13_PY = (
    read_lines(os.path.join(BASE_DIR, "council", "prof-strassen", "verify_round13_strassen.py"), 1, 42)
    + "\n...\n"
    + read_lines(os.path.join(BASE_DIR, "council", "prof-strassen", "verify_round13_strassen.py"), 205, 449)
)
R14_PY = read_lines(os.path.join(BASE_DIR, "council", "prof-strassen", "verify_round14_strassen.py"))
R15_PY = (
    read_lines(os.path.join(BASE_DIR, "council", "prof-strassen", "verify_round15_strassen.py"), 1, 36)
    + "\n...\n"
    + read_lines(os.path.join(BASE_DIR, "council", "prof-strassen", "verify_round15_strassen.py"), 221, 444)
)
HILBERT14_PART1 = read_lines(os.path.join(BASE_DIR, "council", "prof-hilbert", "verify_round14_hilbert.py"), 1, 217)

BORDER_2611_03554 = "\n\n".join([
    "=== 2611.03554 main.tex lines 122-175 ===\n" + read_lines(os.path.join(BORDER_DIR, "main.tex"), 122, 175),
    "=== 2611.03554 proof_overview.tex lines 1-88 ===\n" + read_lines(os.path.join(BORDER_DIR, "proof_overview.tex"), 1, 88),
    "=== 2611.03554 forbidden_value.tex lines 130-258 ===\n" + read_lines(os.path.join(BORDER_DIR, "forbidden_value.tex"), 130, 258),
    "=== 2611.03554 kernel_degree.tex lines 130-150 ===\n" + read_lines(os.path.join(BORDER_DIR, "kernel_degree.tex"), 130, 150),
    "=== 2611.03554 affine_planes.tex lines 191-200 ===\n" + read_lines(os.path.join(BORDER_DIR, "affine_planes.tex"), 191, 200),
    "=== 2611.03554 geometry.tex lines 147-191 & 1389-1449 ===\n"
    + read_lines(os.path.join(BORDER_DIR, "geometry.tex"), 147, 191)
    + "\n...\n"
    + read_lines(os.path.join(BORDER_DIR, "geometry.tex"), 1389, 1449),
])

STEP1_CHECKS_OUT = args.get("step1_checks_out", "")
R13_OUT = args.get("r13_out", "")
R14_OUT = args.get("r14_out", "")
R15_OUT = args.get("r15_out", "")
H14_OUT = args.get("h14_out", "")
INDEP_SUMMARY = args.get("indep_summary", "")

COMMON_RULES = """=== BAĞLAYICI PANEL KURALLARI ===
1. YALNIZ verilen BİRİNCİL METİNLERDEN ve doğrulanmış KESİN HESAP çıktılarından çalış; özetlerden veya hafızadan iddia üretme.
2. HER İDDİANIN sonunda tam olarak şu 4 etiketten BİRİNİ kullan:
   - [İSPAT]: Tüm ara adımları kendin adım adım yeniden türettiğin veya eksiksiz elle kanıtladığın sonuçlar.
   - [KESİN HESAP]: Yerel makinede birebir çalıştırılan tam tamsayı / modüler / sembolik Python çıktılarına dayanan sonuçlar.
   - [SANI]: Makul görünen ancak kanıtlanmamış veya genellenmesi kesin olmayan sezgiler.
   - [DOĞRULANMADI]: Kendin yeniden türetmediğin, yerel CAS/Python ile doğrulamadığın veya dış Zenodo arşivlerine dayanan adımlar.
3. ÖZEL KONU 1 KURALI: Sheshadri (2611.06658) makalesindeki bir adım için '[İSPAT]' demek istiyorsan o adımı gerçekten kendi başına yeniden türetmek ZORUNDASIN (veya yerel [KESİN HESAP] ile birebir doğrulanmış olmalı); aksi hâlde veya dış Zenodo betiklerine dayanıyorsa ZORUNLU OLARAK '[DOĞRULANMADI]' yaz!
4. UYARI (Uzun zincir hata birikimi): Kendi cebirinde en küçük bir boşluk, atlanan durum veya kontrol edilmemiş varsayım görürsen saklama, açıkça 'ŞU ADIMDA TIKANDI' veya '[DOĞRULANMADI]' diye yaz.
5. Hiçbir araç (run_command, read_file, write_file, search_web vb.) ÇAĞIRMA; tüm cevabını doğrudan `finish` aracına Türkçe markdown olarak yaz."""

mod = agent(
    prompt=f"{COMMON_RULES}\nSENİN ROLÜN: Moderatör. Üç konuyu sırayla yönetir, eleştirmen saldırılarını takip eder ve her turun sonunda net 'Neyi Kapattık' tablosu ile nihai hüküm üretirsin.",
    schema={"type": "string"},
    role="Moderatör",
    model="flash",
)
crit = agent(
    prompt=f"{COMMON_RULES}\nSENİN ROLÜN: Eleştirmen. Her iddiaya acımasızca şu soruları sorarsın: (1) Bu zaten Sheshadri'de (veya ABV 2017'de) var mı? (2) Hangi varsayım gizli? (3) Bu adım gerçekten yeniden türetildi mi yoksa [DOĞRULANMADI] mı? (4) Zariski kapanışı / homojenlik / rasyonel fonksiyon boşluğu nerede patlıyor?",
    schema={"type": "string"},
    role="Eleştirmen",
    model="flash",
)
geo = agent(
    prompt=f"{COMMON_RULES}\nSENİN ROLÜN: Cebirsel geometri. Sing, Sing_2, Hessian, torus limitleri, grassmannian chart ve Zariski kapanışı argümanlarını sıfırdan yeniden türetir ve karşılaştırırsın.",
    schema={"type": "string"},
    role="Cebirsel geometri",
    model="flash",
)
rank = agent(
    prompt=f"{COMMON_RULES}\nSENİN ROLÜN: Sınırlı rank uzayları / temsil. Normal formlar, r=0..m vaka analizleri, Atkinson/EH 3x3 uzayları, five-channels, endpoint eşitsizliği ve perm_5 genellemesini denetlersin.",
    schema={"type": "string"},
    role="Sınırlı rank uzayları / temsil",
    model="flash",
)
bdc = agent(
    prompt=f"{COMMON_RULES}\nSENİN ROLÜN: Sınır karmaşıklığı uzmanı. Konu 1'de per4_dc_15.tex Bölüm 6'yı denetler; Konu 3'te R_9^(4) = P*Q ve R_10^(4) değişmezlerinin Zariski kapanışı üzerinde sıfırlanma ispatını elle yazmayı dener, gizli varsayımları açığa çıkarırsın.",
    schema={"type": "string"},
    role="Sınır karmaşıklığı uzmanı",
    model="flash",
)
cas = agent(
    prompt=f"{COMMON_RULES}\nSENİN ROLÜN: Hesaplamalı cebir. Sertifika betiklerini, sonlu cisim -> Q geçişini, IMSC rasyonellik/polinom olma koşulunu ve yerel bilgisayar çıktılarını denetlersin.",
    schema={"type": "string"},
    role="Hesaplamalı cebir",
    model="flash",
)

# =============================================================================
# KONU 1: SHESHADRI (2611.06658) DENETİMİ VE KARŞILAŞTIRMA
# =============================================================================
phase("Konu 1 — Sheshadri (2611.06658) Birincil Metin Denetimi ve Karşılaştırma")

k1_prompts = {
    "geo": f"""KONU 1 (Tur 1) — Bölüm 1–3 Birincil Metin Yeniden Türetimi ve Karşılaştırma:
Aşağıda Sheshadri per4_dc_15.tex Bölüm 1–3 (satır 44–617), ABV 2017 Proofs ve bizim dc_perm4_ge_10.tex (tam metin) verilmiştir.
GÖREV:
1) Sheshadri Bölüm 2.2 (lem:zero2, lem:singF, prop:singdim), 2.4–2.5 (lem:regularity, lem:normalform, prop:endpoint), ve Bölüm 3 (sec:classification, torus limits, sec:charts, prop:containers, thm:kernellist) içindeki ana adımları BÖLÜM BÖLÜM kendin yeniden türet. Gerçekten kendin türettiğin adımlara [İSPAT], yerel Python kontrolü dışındaki Zenodo chart/rank bağımlılıklarına (Tablo 1/2 veya `grassmann_chart_checks.py` vb.) mutlaka [DOĞRULANMADI] veya Step 1 varsa [KESİN HESAP] yaz.
2) Bizim dc_perm4_ge_10.tex zinciri (codim Sing=8 -> str=4 -> r=1 -> origin-isotropy -> Skew-Square -> Sing_2=12) ile Sheshadri'nin lem:regularity + prop:endpoint + lem:zero2 zincirini satır satır karşılaştır: neleri birebir ortak, neler gerçekten farklı? (<= 450 kelime)

=== Sheshadri per4_dc_15.tex (lines 44-617) ===
{SHESH_SEC1_3}

=== ABV 2017 Proofs (lines 213-267) ===
{ABV_PROOFS}

=== Bizim dc_perm4_ge_10.tex ===
{OUR_TEX}""",

    "rank": f"""KONU 1 (Tur 1) — Normal Formlar, Endpoint Eşitsizliği, ve Bölüm 4–5 (Five Channels / İki Satır) Denetimi:
Aşağıda Sheshadri Bölüm 2.4–2.6 + Bölüm 4–5 (satır 317–436, 618–1165) ve bizim prof-strassen/REPORT.md §§1–3 + dc_perm4_ge_10.tex verilmiştir.
GÖREV:
1) Sheshadri lem:regularity, lem:normalform, prop:endpoint, sec:moments (nilpotence, cubicresolvent), Bölüm 4 (cubic stabilizers, syzygies, smaller kernels), ve Bölüm 5 (thm:fivechannels, Clifford trace, 2-row hyperplanes) adımlarını yeniden türetmeye çalış. Dış Zenodo `archive A/B` scriptlerine dayanan iddiaları [DOĞRULANMADI] işaretle!
2) Bizim r=0,2,3,4,>=5 vaka analizimiz (dc_perm4_ge_10.tex) ve `thm:fivechannels` / `k_min=2` kanıtımız (REPORT §§1–3) ile Sheshadri'nin `lem:regularity` + `prop:endpoint` + `thm:fivechannels` adımlarını karşılaştır. (<= 450 kelime)

=== Sheshadri per4_dc_15.tex (lines 317-436) ===
{SHESH_SEC24_26}

=== Sheshadri per4_dc_15.tex (lines 618-1165) ===
{SHESH_SEC4_5}

=== prof-strassen/REPORT.md §§1-3 ===
{STRASSEN_REPORT_1_3}

=== Bizim dc_perm4_ge_10.tex ===
{OUR_TEX}""",

    "bdc": f"""KONU 1 (Tur 1) — Sheshadri Bölüm 6 (Tam Satır Çekirdeği, 13D Değişmez Altuzay, Quotient-Stabilizer) Denetimi:
Aşağıda Sheshadri per4_dc_15.tex Bölüm 6 (`sec:fullrow`, satır 1166–1686) verilmiştir.
GÖREV:
1) `sec:invariant13` ($V = U \\oplus \\mathbb{{C}}e$ değişmezliği ve $S(z)^{{13}}=0$, H0–H2 denklemleri) ve `sec:universalcorrection` ($\\delta_A F_z \\in (\\ell)$ bölüm-kararlı kılıcı özdeşliği) adımlarını elle yeniden türetmeyi dene!
2) `sec:quotienttheorem`, `sec:tenlines`, `sec:normalizer`, `sec:fourkernels`, `sec:unitidentities` ve satır 1685'teki sınır karmaşıklığı (border DC) itirafını incele: hangilerini kendi başına tamamen türetebildin ([İSPAT]), hangileri Archive B Python/SymPy sertifikalarına dayanıyor ([DOĞRULANMADI])?
3) Bizim `dc_perm4_ge_10.tex` Skew-Square ($m=9$) ile kıyasla: neden biz $m=9$'da $S(z)^2$-düzeyinde durup tüm satır (full row) $E=2$ durumunu incelemek zorunda kalmadık? (<= 450 kelime)

=== Sheshadri per4_dc_15.tex (lines 1166-1686) ===
{SHESH_SEC6}""",

    "cas": f"""KONU 1 (Tur 1) — Sertifikalar (Bölüm 3.1, 3.4, 7) ve Yerel Step 1 Yeniden Hesaplama Denetimi:
Aşağıda Sheshadri per4_dc_15.tex Bölüm 3.1/3.4 (satır 448–560) & Bölüm 7 Certificates (satır 1687–1750) ve yerel makinede birebir çalıştırılan `verify_border_and_sheshadri_checks.py` CHECK 1 + `verify_independent_exact.py` özetleri verilmiştir.
GÖREV:
1) Yerel olarak çalıştırılan `CHECK 1` çıktısı neleri [KESİN HESAP] düzeyinde doğruladı? (prop:singdim tanığı $O$, sec:insidetworows determinantları, $2^{{16}}=65{{,}}536$ maske $\\to 3{{,}}017 \\to 27$ yörünge $\\to 9$ kabul edilebilir koordinat çekirdeği ve $\\mathbb{{Q}}(x_S)$ Hessian rankları $\\rho_K$).
2) Tablo 2 (`tab:charts` Jacobian minorları), `grassmann_chart_checks.py` ve Tablo `programsA`/`programsB`'deki 28 Zenodo betiğinden hangileri yerel olarak çalıştırılmadı ([DOĞRULANMADI])?
3) Bizim tek Macaulay/IMSC sertifikamız (`verify_independent_exact.py` doğrudan CSR `uint64_t`) ile Sheshadri'nin sertifika mimarisini karşılaştır. (<= 400 kelime)

=== Sheshadri Sec 3.1 & 3.4 (lines 448-561) ===
{SHESH_SEC3_COMP}

=== Sheshadri Sec 7 Certificates (lines 1687-1750) ===
{SHESH_SEC7}

=== Yerel Step 1 CHECK 1 + verify_independent_exact Özeti ===
{STEP1_CHECKS_OUT}

{INDEP_SUMMARY}""",
}

k1_r1 = await parallel(
    [(geo, k1_prompts["geo"]), (rank, k1_prompts["rank"]), (bdc, k1_prompts["bdc"]), (cas, k1_prompts["cas"])],
    lambda item: item[0](item[1]),
)
k1_r1_digest = "\n\n".join(
    f"### {name}\n{out}"
    for name, out in zip(["Cebirsel geometri", "Sınırlı rank uzayları / temsil", "Sınır karmaşıklığı uzmanı", "Hesaplamalı cebir"], k1_r1)
)

k1_crit = await crit(
    "KONU 1 ELEŞTİRİSİ: Aşağıdaki 4 uzman raporunu sıkıştır. Her uzman için başlık aç ve şu soruları sor:\n"
    "(1) [İSPAT] dedikleri adımı gerçekten ara adım atlamadan yeniden türettiler mi, yoksa Zenodo veya gizli varsayım var mı (özellikle torus limitleri, H1/H2, 5-channels)?\n"
    "(2) Bizim `origin-isotropy + Skew-Square + Sing_2 >= 10` zincirimiz gerçekten Sheshadri `prop:endpoint` (`17 - dim K + ceil(rho_K/2)`) ile eşdeğer mi, ya da ABV 2017'de hangisi zaten vardı?\n"
    "(3) `sec:fullrow` ve 28 Zenodo betiğinde [DOĞRULANMADI] kalması gereken yerde gevşeklik var mı? (<= 550 kelime)\n\n"
    + k1_r1_digest
)

k1_r2 = await parallel(
    [geo, rank, bdc, cas],
    lambda ag: ag(
        "KONU 1 TUR 2 (Eleştirmen Yanıtı): Eleştirmenin saldırılarına doğrudan yanıt ver. Yeniden türetemediğin her alt-adımı dürüstçe [DOĞRULANMADI] çek; gerçekten yeniden türettiklerinin kilit denklemini yaz. (<= 220 kelime)\n\n"
        + k1_crit
    ),
)
k1_r2_digest = "\n\n".join(
    f"### {name} (Tur 2)\n{out}"
    for name, out in zip(["Cebirsel geometri", "Sınırlı rank uzayları / temsil", "Sınır karmaşıklığı uzmanı", "Hesaplamalı cebir"], k1_r2)
)

k1_mod = await mod(
    "KONU 1 MODERATÖR SENTETİK KAPANIŞI:\n"
    "Tüm Konu 1 tartışmasını sentezle ve ZORUNLU OLARAK şunları üret:\n"
    "1) Sheshadri (2611.06658) Bölüm-Bölüm Denetim Tablosu (Bölüm | Yeniden Türetilen / Yerel Hesap [İSPAT]/[KESİN HESAP] | Zenodo / Dış Bağımlı [DOĞRULANMADI] | Kısa Not).\n"
    "2) Bizim Yöntem (`origin-isotropy + Skew-Square + Sing_2` ve Round 14–15 uzantıları) vs ABV 2017 vs Sheshadri: ORTAK ADIMLAR vs GERÇEKTEN FARKLI ADIMLAR TABLOSU.\n"
    "3) TUR 1 'NEYİ KAPATTIK?' TABLOSU (Konu | Karar | Dayanak Etiket | Açık Kalan).\n\n"
    + k1_r1_digest
    + "\n\n=== Eleştirmen ===\n"
    + k1_crit
    + "\n\n=== Tur 2 Yanıtlar ===\n"
    + k1_r2_digest
)
log("Konu 1 tamamlandı.")

# =============================================================================
# KONU 2: BAĞIMSIZ DEĞER, YAYINLANABİLİRLİK VE PERM_5 GENELLEMESİ
# =============================================================================
phase("Konu 2 — Bağımsız Değer, Not Olarak Yayınlanabilirlik ve perm_5 Genellemesi")

k2_context = f"""=== KONU 2 BİRİNCİL VERİLER ===
1) Sayfa/Araç Karşılaştırması:
   - Sheshadri `per4_dc_15.tex`: Toplam 2,359 LaTeX satırı (+ 28 Python/SymPy Zenodo sertifika betiği), amacının tamamı dc(perm_4)=15. ANCAK ANINDA DİKKAT: `per4_dc_15.tex` içinde satır 216–387 ve 497–506 (~180 satır, bilgisayar/Zenodo HİÇ KULLANMADAN!) tek başına dc_C(perm_4) >= 10'u ZATEN verip vermediğini denetleyiniz!
   - Bizim `dc_perm4_ge_10.tex`: 423 LaTeX satırı, 1 bilgisayar destekli girdi (`verify_codim_sing_perm4.py` + `verify_independent_exact.py` CSR C kernel `exact_mod_rref.c`, mod 32749 & 65521, `L_8` tam rank `11,440/11,440`).

{SHESH_NO_COMP_GE10}

2) perm_5 Verileri:
=== verify_round14_hilbert.py (Part 1: Sing_2(perm_5)) ===
{HILBERT14_PART1}

=== verify_round15_strassen.py (perm_5 scaling, lines 221-261) ===
{read_lines(os.path.join(BASE_DIR, "council", "prof-strassen", "verify_round15_strassen.py"), 221, 262)}

=== Yerel Çalıştırma Çıktıları (CHECK 2 + H-14A) ===
{STEP1_CHECKS_OUT}

{H14_OUT}"""

k2_prompts = {
    "geo": f"""KONU 2 (Tur 1) — Bilgisayarsız Sheshadri >= 10 Alt-İspatı Kıyaslaması ve perm_5 Tekillik Katmanları:
1) Sheshadri'nin `per4_dc_15.tex` satır 216–387 + 497–506 arasındaki ~180 satırlık tamamen bilgisayarsız `dc >= 10` alt-ispatını sıfırdan denetle! Gerçekten bilgisayarsız olarak `dc(perm_4) >= 10`'u (ve hatta `codim Sing(perm_4)=8` dahil!) kanıtlıyor mu? Bizim 423 satır + IMSC sertifikamız bunun karşısında kısalık/öz-yeterlilik açısından ne durumda?
2) perm_5 için bilinen/varsayılan sayıları (`codim Sing(perm_5) <= 10`, `codim Sing_2(perm_5) >= 13` [KESİN HESAP] ve 3-sıfır-satır = 15, R_01 Hessian rank rho_K = 10) kullanarak hangi $m$ değerleri çıkar? (<= 380 kelime)

{k2_context}""",

    "rank": f"""KONU 2 (Tur 1) — perm_5 İçin Aynı Zincirin Tam Ölçekleme Türetimi (`2n+1=11` vs Mignon–Ressayre `13`):
DİKKAT: `n = 5` için `2n + 1 = 11`, fakat klasik Mignon–Ressayre (2004) sınırı ZATEN `ceil(5^2 / 2) = 13 > 11` verir!
GÖREV:
1) Bizim `origin-isotropy + Skew-Square / Perturbed Skew-Square + b_3^4 + Sing_2` zincirimiz `perm_5`'te (`r = 0..5`) sırasıyla hangi `m` alt sınırını veriyor? `r = 2, 3, 4` neden takılıyor (ör. `codim Sing(perm_5)` için Macaulay kaçta lazım, `r=2` Subcase 2a `str <= 4` vs `codim Sing = 10` neden ABV ile yetmiyor)?
2) `r = 1` kolunda `m >= 13`'ü aşmak (`m >= 14`, yani Mignon–Ressayre 13'ün ÜSTÜNE çıkmak!) için hangi KESİN ek teoremler gerekir? (<= 380 kelime)

{k2_context}""",

    "bdc": f"""KONU 2 (Tur 1) — Yayınlanabilirlik ('not olarak yayınlanır / yayınlanmaz') ve Asimptotik Endpoint Sınırı:
1) Sheshadri (2611.06658) `dc(perm_4) = 15`'i (üstelik içindeki ~180 satırlık bilgisayarsız argüman `>= 10`'u doğrudan!) kanıtlamışken, bizim `dc_perm4_ge_10.tex` (ve hatta Round 14–15'teki `dc >= 12`) not olarak yayınlanır mı, yayınlanmaz mı? Gerekçesini açıkça savun.
2) Genel $n$ için `endpoint eşitsizliği` $m \\ge 1 + D + \\lceil \\rho_K/2 \\rceil$, neden hiçbir $K \\subseteq \\Sing(\\perm_n)$ üzerinde asimptotik olarak $n^2/2$'yi aşamaz (`R_{{01}}` bile $\\dim = n(n-2) \\implies D = 2n$, $\\rho_K \\le 2n \\implies 3n$!)? (<= 350 kelime)

{k2_context}""",

    "cas": f"""KONU 2 (Tur 1) — perm_5 İçin Bilgisayar Sertifikası Fizibilitesi:
`perm_5` üzerinde ($N = 25$ değişken):
1) $\\codim \\Sing(\\perm_5) = 10$ için $L_{{10}} \\subset \\mathbb{{C}}^{{25}}$ üzerinde derece $D$ Macaulay matrisi (`4` derece üreteçler, 25 adet) boyutları $\\binom{{D+9}}{{9}}$ nedir? ($D=10, 12, 15$?).
2) $\\Sing_2(\\perm_5)$ (`k=13` çalıştı: `9100 x 6188` [KESİN HESAP]) ile `k=14, 15`'e (tam 15) çıkmak ve `m=13` kırmak için `H_{{<=4}}(\\perm_5)` (3x3 minörler deg 9 veya 4x4? Hayır 3x3 subperm = deg 3!) boyutları hesaplanabilir mi? (<= 350 kelime)

{k2_context}""",
}

k2_r1 = await parallel(
    [(geo, k2_prompts["geo"]), (rank, k2_prompts["rank"]), (bdc, k2_prompts["bdc"]), (cas, k2_prompts["cas"])],
    lambda item: item[0](item[1]),
)
k2_r1_digest = "\n\n".join(
    f"### {name}\n{out}"
    for name, out in zip(["Cebirsel geometri", "Sınırlı rank uzayları / temsil", "Sınır karmaşıklığı uzmanı", "Hesaplamalı cebir"], k2_r1)
)

k2_crit = await crit(
    "KONU 2 ELEŞTİRİSİ:\n"
    "1) Sheshadri `per4_dc_15.tex` içinde ~180 satırlık TAMAMEN BİLGİSAYARSIZ `dc(perm_4) >= 10` ispatı varken (Prop singdim + Lem regularity + Prop endpoint + Lem zero2 -> dim K <= 4 + 4? Hayır dim K = 8 -> rho_K = 0 -> two rows rho=8 -> contradiction!), bizim IMSC bilgisayarına muhtaç >= 10 makalesini 'kısa not' diye yayınlamanın bilimsel değeri kaldı mı?\n"
    "2) `perm_5`'te `2n+1 = 11`'i aşmak zaten Mignon–Ressayre (2004)'ın 13'ünün altında kalır! Gerçek yeni sonuç `>= 14`'tür; aynı zincir `>= 14` (hatta `>= 12`) çıkarıyor mu, yoksa `r=2,3,4` ve `D <= 10, w-D >= 2` nedeniyle tıkandı mı? (<= 450 kelime)\n\n"
    + k2_r1_digest
)

k2_r2 = await parallel(
    [geo, rank, bdc, cas],
    lambda ag: ag(
        "KONU 2 TUR 2 (Eleştirmen Yanıtı): Kritik itirazlara yanıt ver, kesin yayın kararını ('not olarak yayınlanır / yayınlanmaz') ve perm_5 için kanıtlanan vs tıkalı sınırı net yaz. (<= 200 kelime)\n\n"
        + k2_crit
    ),
)
k2_r2_digest = "\n\n".join(
    f"### {name} (Tur 2)\n{out}"
    for name, out in zip(["Cebirsel geometri", "Sınırlı rank uzayları / temsil", "Sınır karmaşıklığı uzmanı", "Hesaplamalı cebir"], k2_r2)
)

k2_mod = await mod(
    "KONU 2 MODERATÖR KAPANIŞI:\n"
    "Zorunlu çıktılar:\n"
    "1) Kısalık/öz-yeterlilik kıyaslaması (`per4_dc_15.tex` tam 2359 satır + 28 betik vs `per4_dc_15.tex` içindeki ~180 satırlık bilgisayarsız >= 10 çekirdeği vs bizim 423 satır + 1 sertifika).\n"
    "2) perm_5 genellemesi: `2n+1=11`, MR04 `13`, ve bizim zincirin bugün kanıtlayabildiği vs açık kalan adımlar (`>= 14` şansı var mı?).\n"
    "3) NET KARAR: 'NOT OLARAK YAYINLANIR / YAYINLANMAZ' ve maddeli gerekçe (ayrıca 'düzeltilmiş ≥ 10' vs '≥ 12' farkı varsa belirt).\n"
    "4) TUR 2 'NEYİ KAPATTIK?' TABLOSU.\n\n"
    + k2_r1_digest
    + "\n\n=== Eleştirmen ===\n"
    + k2_crit
    + "\n\n=== Tur 2 Yanıtlar ===\n"
    + k2_r2_digest
)
log("Konu 2 tamamlandı.")

# =============================================================================
# KONU 3: SINIR KARMAŞIKLIĞI (dc-bar) — R_9^{(4)} = P*Q ELLE İSPAT & GİZLİ VARSAYIM
# =============================================================================
phase("Konu 3 — Sınır Karmaşıklığı (dc-bar) Elle İspat Denemesi ve Gizli Varsayım Denetimi")

k3_primary = f"""=== KONU 3 BİRİNCİL METİNLER ===
--- prof-strassen/REPORT.md §§15-17 ---
{STRASSEN_REPORT_15_17}

--- verify_round13_strassen.py ---
{R13_PY}

--- verify_round14_strassen.py ---
{R14_PY}

--- verify_round15_strassen.py ---
{R15_PY}

--- Sheshadri arXiv:2611.03554 (Sınır Karmaşıklığı Birincil Metin) ---
{BORDER_2611_03554}

--- Yerel Çalıştırma Çıktıları (Rounds 13-15 + Step 1 CHECK 3) ---
=== verify_round13_strassen.py ===
{R13_OUT}

=== verify_round14_strassen.py ===
{R14_OUT}

=== verify_round15_strassen.py ===
{R15_OUT}

=== verify_border_and_sheshadri_checks.py (CHECK 3) ===
{STEP1_CHECKS_OUT}"""

k3_bdc_attempt = await bdc(
    "KONU 3 — ADIM 1 (Sınır Karmaşıklığı Uzmanı — R_9^{(4)} = P^{(4)} Q^{(4)} ve R_{10}^{(4)} Elle İspat Denemesi):\n"
    "GÖREVİN EN KRİTİK KISIM: R_9^{(4)}(F) = P^{(4)}(F) * Q^{(4)}(F) değişmezinin neden Zariski kapanışı üzerinde sıfırlandığını (ve perm_4 üzerinde sıfırlanmadığını) ELLE ADIM ADIM YAZMAYI DENE, her gizli varsayımı açığa çıkar!\n"
    "Zorunlu iki bölüm:\n"
    "**KISIM A — Homojen dilim kapanışı $\\overline{\\mathcal{D}_9^{\\mathrm{hom}}}$ üzerinde elle ispat:**\n"
    "1) $\\mathcal{D}_9^{\\mathrm{hom}} := \\{ \\det_9(A_0 + L(X)) \\in \\mathrm{Sym}^4(\\mathbb{C}^{16})^* : \\deg \\neq 4 \\text{ terimleri özdeşçe } 0 \\}$ üzerindeki HER F için (r=0,2,3 [2x2 sıfır bloklu sıkıştırma dahil!], 4,>=5 ve r=1, D<=7 vs D=8) neden P veya Q'nun sıfırlandığını elle kur.\n"
    "2) KRİTİK POLİNOMLUK DENETİMİ: `verify_round13_strassen.py` içindeki `P^{(4)}` bir IMSC Schur-tümleyen pivot çarpımıdır (`det6 * det_s6 * det_s7 * det_s8`); gerçek bir polinom olan maksimal minör $\\widetilde{P}^{(4)}(F) = \\det_{11440}(M_9(F; L_8)_{I_1})$ ile ilişkisi nedir? `P^{(4)}` rasyonel fonksiyon mudur yoksa düzeltildiğinde ($\\widetilde{P}^{(4)}$) polinom olur mu?\n"
    "3) Aynı şeyi Round 15 `R_{10}^{(4)} = P^{(4)} T^{(4)} Q^{(4)}` için kontrol et (`verify_round15_strassen.py` satır 402–434'ün sahte sentetik `H_sym` kullandığını göz önünde bulundurarak teorik $T^{(4)}$ polinomluk/sıfırlanma durumunu kontrol et).\n\n"
    "**KISIM B — GERÇEK Sınır Determinantal Karmaşıklığı $\\mathcal{B}_9^{(4)} := \\overline{\\{\\det_9(A_0 + L(X))\\}} \\cap \\mathrm{Sym}^4(\\mathbb{C}^{16})^*$ (yani $\\underline{\\dc}(\\perm_4) \\le 9$ ve arXiv:2611.03554 tanımı: $\\lim_{\\varepsilon\\to 0} \\det_9(A_0(\\varepsilon) + L_\\varepsilon(X))$):**\n"
    "1) $\\overline{\\mathcal{D}_9^{\\mathrm{hom}}} \\subseteq \\mathcal{B}_9^{(4)}$ kapsamasının eşitlik olup olmadığını elle kanıtlamaya çalış!\n"
    "2) Bir Laurent / eğri ailesi $F_\\varepsilon(X) = \\det_9(A_0(\\varepsilon) + L_\\varepsilon(X)) \\xrightarrow{\\varepsilon \\to 0} F_0(X) \\in \\mathrm{Sym}^4(\\mathbb{C}^{16})^*$ al ($\\varepsilon \\neq 0$ iken $F_\\varepsilon$ homojen OLMAK ZORUNDA DEĞİL, yani $\\deg \\neq 4$ terimleri $O(\\varepsilon)$ ile sıfıra gidiyor olabilir!). Bu aile için $\\widetilde{R}_9^{(4)}(F_0) = 0$ olduğunu kanıtlamaya çalış: HANGİ ADIMDA TIKANIYORSUN? (Örn. $A_0(\\varepsilon)$'ın $\\mathbb{C}[[\\varepsilon]]$ üzerinde tam ranklı $\\operatorname{diag}(\\varepsilon^{a_1},\\dots,\\varepsilon^{a_9})$ Smith normal formuna girmesi, $\\varepsilon^{-p}$ kutupları, origin-isotropy $[t^2]=0$'ın bozulması, $r$-vaka analizinin çökmesi vs.).\n"
    "Net hüküm ver: $\\overline{\\mathcal{D}_9^{\\mathrm{hom}}}$ vs gerçek $\\underline{\\dc}_{\\mathbb{C}}(\\perm_4) \\ge 10$! (<= 750 kelime)\n\n"
    + k3_primary
)

k3_peers = await parallel(
    [
        (geo, f"""KONU 3 (Cebirsel Geometri Denetimi): Aşağıdaki elle ispat denemesini Kısım A ($\\overline{{\\mathcal{{D}}_9^{{\\mathrm{{hom}}}}}}$) ve Kısım B (gerçek $\\mathcal{{B}}_9^{{(4)}} = \\overline{{\\mathcal{{D}}_9}} \\cap \\mathrm{{Sym}}^4$) ayrımıyla denetle:
1) Kapanışla kesişim yer değiştirme hatası: $\\overline{{\\mathcal{{D}}_m \\cap \\mathbb{{C}}[X]_4}} = \\overline{{\\mathcal{{D}}_m^{{\\mathrm{{hom}}}}}}$ ile $\\overline{{\\mathcal{{D}}_m}} \\cap \\mathbb{{C}}[X]_4 = \\mathcal{{B}}_m^{{(4)}}$ (homojenleştirilmiş biçimi $\\{{F : z^{{m-4}} F \\in \\overline{{\\mathrm{{End}}(\\mathbb{{C}}^{{m^2}})\\cdot \\det_m}}\\}}$) neden eşit olmak zorunda değildir? `verify_round14_strassen.py` satır 15–16 ve `REPORT.md` satır 585 bu ikisini gizlice özdeşleştirmiş mi?
2) Kısım A'da $\\widetilde{{P}}^{{(4)}} Q^{{(4)}} \\equiv 0$ on $\\overline{{\\mathcal{{D}}_9^{{\\mathrm{{hom}}}}}}$ argümanı (Nullstellensatz + Boyut Teoremi + r=3 düzeltmesiyle) gerçekten [İSPAT] mı?
3) `arXiv:2611.03554` sınır karmaşıklığı örnekleri ($Q_{{3,1}}$, $Q_{{5,0}}$, $\\mathcal{{K}}_{{2,0}}$) burada ne öğretiyor? (<= 400 kelime)

=== Sınır Karmaşıklığı Uzmanı İspat Denemesi ===
{k3_bdc_attempt}

=== Birincil Veriler (Kısaltılmış) ===
{STEP1_CHECKS_OUT}"""),

        (rank, f"""KONU 3 (Sınırlı Rank Uzayları Denetimi):
1) Kısım A içinde (`dc_perm4_ge_10.tex` ve `REPORT.md` Theorem 15A) `r = 3` vakası için 2x2 sıfır bloğu eksikliği veya Atkinson–Dieudonné geçişi $R_9^{{(4)}}$ ve $R_{{10}}^{{(4)}}$ ispatlarında bir boşluk açar mı? ($\\adj(B)$ 2x2 sıfır blokluysa $\\str \\le 2 < 4 \\implies \\codim\\Sing \\le 4 \\le 7$, kontrol et ve elle türet!).
2) Kısım B'de (Laurent / homojen-olmayan sınır limiti $F_\\varepsilon = \\det_9(A_0(\\varepsilon) + L_\\varepsilon(X)) \\to F_0$): $\\mathbb{{C}}(\\!(\\varepsilon)\\!)$ üzerinde $A_0(\\varepsilon)$ tam ranklı $\\operatorname{{diag}}(\\varepsilon^{{a_1}},\\dots,\\varepsilon^{{a_9}})$ olursa origin-corank $r$ kavramının nasıl çöktüğünü matris seviyesinde göster! (<= 380 kelime)

=== Sınır Karmaşıklığı Uzmanı İspat Denemesi ===
{k3_bdc_attempt}"""),

        (cas, f"""KONU 3 (Hesaplamalı Cebir Denetimi):
1) `verify_round13_strassen.py` (`P^(4)`) ve `verify_round15_strassen.py` (`T^(4)`): IMSC Schur-tümleyen determinant çarpımı gerçekte $F$'nin katsayılarında BİR POLİNOM mudur, yoksa önceki pivot minörlerini bölen RASYONEL FONKSİYON mudur? Eğer rasyonel fonksiyonsa $M_6(F; L_8)$ rank düşüşünde ne olur ve `verify_independent_exact.py` (`M_9` doğrudan rank `11440/11440`) bu boşluğu $\\widetilde{{P}}^{{(4)}}(F) = \\det_{{11440}}(M_9(F; L_8)_{{I_1}})$ ile nasıl kapatır? (Aynı şekilde `Q^(4)` doğrudan $\\det_{{1365}}$ mi?)
2) `verify_round15_strassen.py` satır 402–434'teki `T^(4)` testinde gerçek bir $m=10$ polinomu mu inşa edilmiş yoksa sentetik rank-2 `H_sym` mi konmuş?
3) `CHECK 3` (`e_4(L)` `1365/1365`, `F_skew5` `1320/1365`, `q_5` LM probe `1.000`/`1.435`) neyi [KESİN HESAP] ile doğruladı? (<= 380 kelime)

=== Sınır Karmaşıklığı Uzmanı İspat Denemesi ===
{k3_bdc_attempt}

=== Birincil Veriler ===
{R13_PY}

{R14_PY}

{STEP1_CHECKS_OUT}"""),
    ],
    lambda item: item[0](item[1]),
)

k3_peers_digest = "\n\n".join(
    f"### {name}\n{out}"
    for name, out in zip(["Cebirsel geometri", "Sınırlı rank uzayları / temsil", "Hesaplamalı cebir"], k3_peers)
)

k3_crit = await crit(
    "KONU 3 ELEŞTİRİSİ (EN KRİTİK SALDIRI):\n"
    "Aşağıda Sınır Karmaşıklığı Uzmanı'nın elle ispat denemesi ve 3 uzmanın denetimleri var. Acımasızca saldır ve HİÇBİR GİZLİ VARSAYIMI KAÇIRMA:\n"
    "1) 'R_9^(4) = P * Q Zariski kapanışında sıfırlanıyor => dc_border(perm_4) >= 10' iddiasındaki EN BÜYÜK GİZLİ VARSAYIM ne?\n"
    "2) Homojenlik varsayımı ($\\overline{\\mathcal{D}_9^{\\mathrm{hom}}}$ vs gerçek $\\mathcal{B}_9^{(4)}$): `det_9(A_0(eps)+L_eps(X)) -> F_0` limiti için `F_eps` deg!=4 terimlerini sıfır yapmadan `eps -> 0`'da öldürebilir. Bizim kod (`verify_round14_strassen.py` ve `REPORT.md`) bunu hiç kanıtlamadı!\n"
    "3) `P^(4)` ve `T^(4)` için `verify_round13/15_strassen.py` IMSC rasyonel fonksiyonu kullanmış (gerçek `M_9` tam minörü `verify_independent_exact.py`'da var ama `T^(4)` için `M_8` tam `12870x12870` direkt minor henüz çalıştırılmadı!).\n"
    "4) `arXiv:2611.03554` ve LMR (2013)'e göre $\\underline{\\dc}(\\per_4) \\ge 8$ zaten var, [OAI26] iddiası var (sayısı doğrulanmadı). Peki bizim $\\overline{\\mathcal{D}_9^{\\mathrm{hom}}}$ dışlamamız gerçek $\\underline{\\dc}(\\perm_4) \\ge 10$ yerine ŞU AN tam olarak NEYİ kanıtlıyor? (<= 500 kelime)\n\n"
    + k3_bdc_attempt
    + "\n\n"
    + k3_peers_digest
)

k3_final_specialists = await parallel(
    [bdc, geo, rank, cas],
    lambda ag: ag(
        "KONU 3 SON TUR (Eleştirmen Yanıtı ve Kesin Sınır Tespiti): Eleştirmenin tespitlerine dürüstçe yanıt ver:\n"
        "- Hangi kısım gerçekten [İSPAT] / [KESİN HESAP] (elle ispat taslağı tam olarak hangi uzay üzerinde kapanıyor)?\n"
        "- Gerçek `dc-bar(perm_4) >= 10, 11` iddiası tam olarak 'ŞU ADIMDA TIKANDI'?\n"
        "- `Hesaplamalı cebir` dahil, bu sonucu güçlendirmek veya test etmek için tek somut ek kontrol gerekiyorsa belirt. (<= 220 kelime)\n\n"
        + k3_crit
    ),
)
k3_final_digest = "\n\n".join(
    f"### {name} (Son Yanıt)\n{out}"
    for name, out in zip(["Sınır karmaşıklığı uzmanı", "Cebirsel geometri", "Sınırlı rank uzayları / temsil", "Hesaplamalı cebir"], k3_final_specialists)
)

k3_mod = await mod(
    "KONU 3 ve GENEL SONUÇ MODERATÖR HÜKMÜ:\n"
    "Zorunlu olarak şunları üret:\n"
    "1) KISIM A: $\\widetilde{R}_9^{(4)} = \\widetilde{P}^{(4)} Q^{(4)}$ için $\\overline{\\mathcal{D}_9^{\\mathrm{hom}}}$ üzerinde el ile eksiksiz ispat taslağı (hangi düzeltmelerle geçerli? IMSC rasyonellik vs doğrudan `det_{11440}`, `r=3` 2x2 sıfır bloğu) ve $R_{10}^{(4)}$ için not (`M_8` tam direkt minör [DOĞRULANMADI] veya IMSC payda uyarısı).\n"
    "2) KISIM B: GERÇEK SINIR KARMAŞIKLIĞI ($\\underline{\\dc}_{\\mathbb{C}}(\\perm_4) \\ge 10, 11$) İÇİN 'ŞU ADIMDA TIKANDI' RAPORU: Gizli tüm varsayımların listesi (başta $\\overline{\\mathcal{D}_m^{\\mathrm{hom}}} \\stackrel{?}{=} \\overline{\\mathcal{D}_m} \\cap \\mathrm{Sym}^4$ özdeşliği, Laurent $\\varepsilon$-kutuplu homojen olmayan aileler, `arXiv:2611.03554` bağlantısı).\n"
    "3) TUR 3 'NEYİ KAPATTIK?' TABLOSU.\n"
    "4) KULLANICININ ANA SORUSUNA NİHAİ YANIT: Sheshadri (2611.06658) `dc_C(perm_4) = 15`'i kanıtlıyorsa, bizim `>= 10` (ve `>= 12`) ispatımızın ve `dc-bar` iddiamızın geriye kalan gerçek bilimsel değeri tam olarak nedir?\n\n"
    + k3_bdc_attempt
    + "\n\n"
    + k3_peers_digest
    + "\n\n=== Eleştirmen ===\n"
    + k3_crit
    + "\n\n=== Son Yanıtlar ===\n"
    + k3_final_digest
)

out_md = os.path.join(PAPER_DIR, "AUDIT_SHESHADRI_AND_DCBAR.md")
with open(out_md, "w", encoding="utf-8") as f:
    f.write("# Birincil Metin Denetim Dosyası: Sheshadri (2611.06658), ≥ 10 İspatının Değeri / perm₅ ve Sınır Karmaşıklığı (dc-bar)\n\n")
    f.write("6 Kişilik Odaklanmış Panel: Moderatör, Eleştirmen, Cebirsel geometri, Sınırlı rank uzayları / temsil, Sınır karmaşıklığı uzmanı, Hesaplamalı cebir.\n\n")
    f.write("---\n\n## KONU 1 — Sheshadri (`2611.06658`) Denetimi ve Karşılaştırma\n\n")
    f.write("### Tur 1 — Bağımsız Birincil Metin Okuması ve Yeniden Türetim\n\n" + k1_r1_digest + "\n\n")
    f.write("### Eleştirmen Saldırısı (Konu 1)\n\n" + k1_crit + "\n\n")
    f.write("### Tur 2 — Uzman Yanıtları (Konu 1)\n\n" + k1_r2_digest + "\n\n")
    f.write("### Moderatör Kapanışı & Tur 1 'Neyi Kapattık?' Tablosu\n\n" + k1_mod + "\n\n---\n\n")
    f.write("## KONU 2 — Bağımsız Değer, 'Not Olarak Yayınlanır / Yayınlanmaz' ve perm₅ Genellemesi\n\n")
    f.write("### Tur 1 — Analizler\n\n" + k2_r1_digest + "\n\n")
    f.write("### Eleştirmen Saldırısı (Konu 2)\n\n" + k2_crit + "\n\n")
    f.write("### Tur 2 — Uzman Yanıtları (Konu 2)\n\n" + k2_r2_digest + "\n\n")
    f.write("### Moderatör Kapanışı & Tur 2 'Neyi Kapattık?' Tablosu\n\n" + k2_mod + "\n\n---\n\n")
    f.write("## KONU 3 — Sınır Karmaşıklığı (dc-bar): R₉⁽⁴⁾ = P·Q Elle İspat Denemesi ve Gizli Varsayım Denetimi\n\n")
    f.write("### Adım 1 — Sınır Karmaşıklığı Uzmanı Elle İspat Denemesi\n\n" + k3_bdc_attempt + "\n\n")
    f.write("### Adım 2 — Uzman Çapraz Denetimleri\n\n" + k3_peers_digest + "\n\n")
    f.write("### Adım 3 — Eleştirmen Saldırısı (Konu 3)\n\n" + k3_crit + "\n\n")
    f.write("### Adım 4 — Uzmanların Son Yanıtları\n\n" + k3_final_digest + "\n\n")
    f.write("### Adım 5 — Moderatör Nihai Hükmü & Tur 3 'Neyi Kapattık?' Tablosu\n\n" + k3_mod + "\n")

log(f"Saved complete audit dossier to {out_md}")
print("=== KONU 1 MODERATOR ===")
print(k1_mod)
print("\n=== KONU 2 MODERATOR ===")
print(k2_mod)
print("\n=== KONU 3 + GENEL MODERATOR ===")
print(k3_mod)
