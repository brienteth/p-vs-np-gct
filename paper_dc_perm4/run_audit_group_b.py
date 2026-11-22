"""
Group B ("Doğrulama ve Yayın Hazırlığı" — hesap ve süreç odaklı) 12-Agent, 4-Round Audit Workflow
for paper_dc_perm4/ (dc_perm4_ge_10.tex, verify_codim_sing_perm4.py, README.md).
Writes full structured dossier to paper_dc_perm4/AUDIT_GROUP_B.md.
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
    TRANSFER_EXCERPT = f.read()[:3500]

PRELIM_CONTEXT = f"""=== ORTAK GÖREV VE ÖN HAKEM NOTLARI ===
Bağlam: dc_perm4_ge_10.tex makalesi C üzerinde dc(perm_4) >= 10 iddiasını şu zincirle kanıtlıyor:
1) codim Sing(V(perm_4)) = 8 (IMSC/Macaulay sertifikası, L_8 üzerinde).
2) str(perm_4) = 4, ve r = corank(A_0) = 1 zorunluluğu (r = 0, 2, 3, 4, >=5 elenir).
3) m = 9 için origin-isotropy, 2-blok normal form, [t^3]=0'dan xi-lineer kısıtlar, Skew-Square Lemması, perm_4 in I_W^3 => W^perp subset Sing_2.
4) codim Sing_2(V(perm_4)) = 12, çelişki.

Ön hakem şüpheleri (doğruluğunu SİZ denetleyeceksiniz):
- r = 3 vakasında "rank <= 2 olan 3x3 lineer uzaylar iki tiptir (sıfır satır, çarpık-simetrik)" denmiş. Şüphe: 2x2 sıfır bloklu sıkıştırma uzayı tipi eksik olabilir; sıfır sütun ve sıfır satırın GL_3 x GL_3 + devrik ile eşlenip eşlenmediği kontrol edilmeli.
- Teorem 3.1 yalnız IMSC Python betiğine dayanıyor; bağımsız Singular / Macaulay2 kontrolü yok. Yerel makinede M2, Singular, Sage ve SymPy kurulu değildir (yalnız Python3 + NumPy mevcuttur).
- README'deki Macaulay2 komutunda 'permanent' fonksiyonunun varlığı doğrulanmamıştır.
- Literatür iddiaları (Yabe 2015: R üzerinde (n-1)^2+1; ABV 2017: dc >= codim Sing + 1; Mignon-Ressayre n^2/2; Landsberg-Ressayre 15; ayrıca daha önce Sheshadri 2026 dc(perm_4)=15 gibi olası yayınlar olup olmadığı!) birincil kaynaktan kontrol edilmelidir.
- L_9 negatif kontrolü yalnız kodun her şeyi sıfırlamadığını gösterir; perm_3 için codim Sing = 6 pozitif kontrolü eksik.

Üç Karar Sorusu:
Q1. r = 3 vakası düzeltildiğinde makale mantıksal olarak kapanıyor mu? Düzeltilmiş vaka paragrafı ne olmalı?
Q2. codim Sing(V(perm_4)) = 8 için hangi bağımsız doğrulama yapılmalı, hangi sonuç çıkarsa teorem tutarlı sayılır?
Q3. Uzmana gönderilmeden önce makalede neler değişmeli? Boolean/SAT aktarım teoremi makalede nerede ve nasıl yer almalı? (Öneri: ayrı sonuç olarak değil, en fazla H1 ve H4 [AÇIK] vurgulu 'Motivasyon/Tartışma' bölümü.)

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
    "Sen Grup B ('Doğrulama ve Yayın Hazırlığı' — hesap ve süreç odaklı) içinde titiz bir araştırmacısın.\n"
    + PRELIM_CONTEXT
)

GROUP_B_SPECS = [
    ("B-hesaplamalı-cebir", "Matematikçi — Hesaplamalı Cebir: Singular / Macaulay2 / Sage betiklerini (permanent fonksiyonu yerine açık permütasyon toplamıyla!) ve çalıştırma planını tasarla: perm_3 pozitif kontrolü, perm_4 L_8 kontrolü, çoklu rastgele altuzaylar."),
    ("B-sayılar-kuramı", "Matematikçi — Sayılar Kuramı: Asal modülde tam sütun rankı -> Q'da tam rank çıkarımının mantıksal titizliğini, iki asal p1=32749, p2=65521 seçiminin kötü indirgeme olasılığı üzerindeki etkisini ve L_8'deki sıfır/bölme durumlarını denetle."),
    ("B-cebirsel-karmaşıklık", "Matematikçi — Cebirsel Karmaşıklık: dc, sınır karmaşıklığı, GCT bağlamı; makalenin literatürdeki yerini (MR04, Yabe 2015, ABV 2017, Landsberg-Ressayre, olası yeni sonuçlar!) dürüstçe konumlandır."),
    ("B-lineer-cebir", "Matematikçi — Lineer Cebir: Vaka analizinin (r = 0, 1, 2, 3, 4, >=5) ve Skew-Square Lemması ile Theorem 1.1 adımlarının satır satır bağımsız yeniden türetimini yap."),
    ("B-mantık-ispat", "Matematikçi — Mantık ve İspat Teorisi: Hipotez/sonuç akışını, gizli/sessiz varsayımları (ör. 'padding by an identity block', 'generic L_8' vs 'explicit integer L_8', affine dimension theorem), olası döngüselliği tara."),
    ("B-yazım-editörü", "Matematikçi — Yazım ve Yayın Editörü: LaTeX hataları, notasyon tutarlılığı (dc vs dc_C, perm_4 vs perm_3, adj/tr tanımları), kaynakça doğruluğu ve 'Ne İddia Ediyoruz / Etmiyoruz' bölümü ihtiyacını denetle."),
    ("B-istatistiksel-fizik", "Fizikçi — İstatistiksel Fizik: Rastgele tamsayı matrisi M_L8 (seed=2026, [-2,2]) seçiminin meşruiyetini denetle: Nullstellensatz için L_8'in genel olmasına gerçekten gerek var mı, yoksa herhangi bir 8-uzayda V(J|_{L_8})={0} çıkması yeterli mi? L_9 seçimini kıyasla."),
    ("B-matematiksel-fizik", "Fizikçi — Matematiksel Fizik: Çarpık-simetrik (K, so(d_v)) ve izotropik (Omega) yapılarda bozonik/fermiyonik benzetmelerin veya fizik jargonunun makaleye sızmadığını denetle; tam blok indirgemeyi temiz tut."),
    ("B-kuantum-hesaplama", "Fizikçi — Kuantum Hesaplama: Boolean/SAT aktarım teoremini (QUANTITATIVE_TRANSFER_THEOREM_SYNTHESIS.md) değerlendir; H1 ve H4'ün tamamen [AÇIK] olduğunu vurgula ve makale sonu için kısa bir 'Motivasyon / Tartışma' bölümü öner."),
    ("B-deneysel-doğrulama", "Fizikçi — Deneysel Doğrulama: verify_codim_sing_perm4.py için bağımsız yeniden üretim protokolünü, rref_mod_p_exact BLAS kayan nokta taşma güvenlik marjını, subperm3 hata riskini ve negatif/pozitif kontrolleri denetle."),
]

agents = {
    name: agent(
        prompt=f"{COMMON_SYS}\nSENİN ROLÜN: {name}\nODAK ALANIN: {focus}\n{FULL_DOCS}",
        schema={"type": "string"},
        role=name,
        model="flash",
    )
    for name, focus in GROUP_B_SPECS
}

crit_b = agent(
    prompt=(
        f"{COMMON_SYS}\nSENİN ROLÜN: crit-B (Eleştirel Soru Soran)\n"
        "Görevin: Grup B'deki her üyenin bulgularını acımasızca sorgulamak — özellikle şu 3 soruyu odakla: "
        "(1) Bu sonucu daha önce biri bulmuş olabilir mi? (2) Hangi varsayım sessizce kullanıldı? (3) Bir dergi hakemi / uzman bu iddiayı neden reddeder? "
        "Her ajanı '### <ajan-adı>' başlığı altında ayrı ayrı sıkıştır.\n"
        f"{FULL_DOCS}"
    ),
    schema={"type": "string"},
    role="crit-B",
    model="flash",
)

mod_b = agent(
    prompt=(
        f"{COMMON_SYS}\nSENİN ROLÜN: mod-B (Grup B Moderatörü)\n"
        "Görevin: Q1–Q3 karar sorularına odaklı yürütmek, her aşamalı kapanışta 'Bugün neyi kesin olarak kapatabildik?' tablosunu güncellemek, "
        "azınlık görüşlerini ve en güçlü itirazı kaydetmek ve zorunlu kapanış biçimini üretmektir.\n"
        f"{FULL_DOCS}"
    ),
    schema={"type": "string"},
    role="mod-B",
    model="flash",
)

# --- TUR 1: Bağımsız Okuma ---
phase("Grup B — Tur 1: Bağımsız Okuma")
t1_prompt = (
    "TUR 1 (Bağımsız Okuma): Yalnız kendi uzmanlık merceğinden makaleyi, Python doğrulama betiğini, README'yi ve aktarım özetini oku. "
    "En fazla 5 kısa, madde madde bulgu yaz (hata, sessiz varsayım, doğrulama eksiği, yayın riski veya somut öneri). "
    "Her maddede zorunlu etiketi ([İSPAT], [KESİN HESAP], [SAYISAL], [SANI], [LİTERATÜR-DOĞRULANMADI]) kullan. (<= 220 kelime)"
)
t1_outputs = await parallel(
    GROUP_B_SPECS,
    lambda spec: agents[spec[0]](t1_prompt),
)
t1_digest = "\n\n".join(f"### {spec[0]}\n{out}" for spec, out in zip(GROUP_B_SPECS, t1_outputs))
log(f"Tur 1 tamamlandı ({len(t1_outputs)} ajan).")

# --- TUR 2: Çapraz Saldırı ---
phase("Grup B — Tur 2: Çapraz Saldırı")
crit_prompt = (
    "TUR 2 (Çapraz Saldırı — crit-B): Aşağıda Grup B'deki 10 uzmanın Tur 1 bulguları var. "
    "Her uzman için '### <ajan-adı>' başlığı aç ve şu sorularla saldır: "
    "'Bu sonucu daha önce biri bulmuş olabilir mi?', 'Hangi varsayım sessizce kullanıldı?', 'Bir uzman bu makaleyi hangi tek cümleyle reddeder?' "
    "Özellikle r=3 2x2 bloğu, 'generic L_9' vs 'explicit L_8', M2 'permanent' hatası, ve literatür kontrolsüzlüğü konusunda kimseyi es geçme. (<= 650 kelime)\n\n"
    f"{t1_digest}"
)
crit_attacks = await crit_b(crit_prompt)

t2_outputs = await parallel(
    GROUP_B_SPECS,
    lambda spec: agents[spec[0]](
        f"TUR 2 YANITI: crit-B'nin eleştirileri aşağıdadır. Kendi '### {spec[0]}' başlığın altındaki saldırılara doğrudan cevap ver, "
        f"hatalıysan geri çek, doğruysa somut gerekçeyle savun. Zorunlu etiketleri koru. (<= 180 kelime)\n\n{crit_attacks}"
    ),
)
t2_digest = "\n\n".join(f"### {spec[0]} (Tur 2 Yanıtı)\n{out}" for spec, out in zip(GROUP_B_SPECS, t2_outputs))
log("Tur 2 tamamlandı.")

# --- TUR 3: Üretim ---
phase("Grup B — Tur 3: Üretim (r=3 LaTeX, CAS Betikleri, Değişiklik & Motivasyon, Gönderim Planı)")
prod_tasks = [
    (
        "B-lineer-cebir",
        "TUR 3a — BAĞIMSIZ YENİDEN TÜRETİLMİŞ r=3 DÜZELTİLMİŞ LATEX PARAGRAFI:\n"
        "Tur 1-2 satır satır yeniden türetimin sonucunda dc_perm4_ge_10.tex Proposition 4.1 'Case r = 3' için eksiksiz düzeltilmiş LaTeX paragrafını yaz. "
        "Özellikle: 1x3 sıfır satır, 3x1 sıfır sütun (devrik ile eşlenir), 2x2 sıfır bloğu (1. satır + 1. sütun dolu => adj(B) rank-1 dış çarpım veya sıfır => str(perm_4)<=2<4!) ve so_3(C) primitif tipini kapsa. "
        "Atıf doğrulanmadıysa [LİTERATÜR-DOĞRULANMADI] notu düş."
    ),
    (
        "B-hesaplamalı-cebir",
        "TUR 3b — BAĞIMSIZ MACAULAY2 & SINGULAR & SAGE BETİKLERİ (PERMANENT YERİNE AÇIK TOPLAM):\n"
        "README'deki 'permanent' fonksiyonu belirsizliğini tamamen eleyerek, yerleşik permanent fonksiyonu ÇAĞIRMADAN açık S_3 ve S_4 permütasyon toplamı yazan "
        "tam bağımsız (1) Macaulay2 (.m2), (2) Singular (.sing) betiklerini ve çalıştırma protokolünü üret. "
        "İçerikte: (i) perm_3 pozitif kontrolü (codim == 6), (ii) perm_4 Jakobiyen ideali (codim == 8) + L_8 kesiti, (iii) L_9 negatif kontrolü (dim >= 1) + 5 rastgele F_p kesiti yer alsın. "
        "M2/Singular bu makinede kurulu olmadığı için [KESİN HESAP — HENÜZ ÇALIŞTIRILMADI] etiketle."
    ),
    (
        "B-yazım-editörü",
        "TUR 3c — MAKALE DEĞİŞİKLİK LİSTESİ & 'NE İDDİA EDİYORUZ / ETMİYORUZ':\n"
        "Makalenin başlıktan kaynakçaya tüm düzeltme maddelerini ve hakem şüphesi yaratacak noktaları kapatan kısa 'What This Paper Does and Does Not Claim' paragrafını yaz."
    ),
    (
        "B-kuantum-hesaplama",
        "TUR 3c-ek — BOOLEAN/SAT AKTARIM MOTİVASYON BÖLÜMÜ TASLAĞI:\n"
        "Q3 kararı uyarınca Boolean/SAT nicel aktarım teoremini ayrı sonuç olarak DEĞİL, en fazla 'Motivation / Discussion' alt-bölümü olarak konumlandıran, "
        "H1 (genel derinlik fonksiyonel alt sınır) ve H4 (SAT-indirgenebilirlik / Ters-Toda) hipotezlerinin tamamen [AÇIK] olduğunu açıkça vurgulayan kısa, dürüst bir LaTeX/Türkçe taslak yaz."
    ),
    (
        "B-cebirsel-karmaşıklık",
        "TUR 3d — UZMAN GÖNDERİM PLANI VE ÖNCELİK/LİTERATÜR DENETİMİ:\n"
        "crit-B'nin 'bu sonucu daha önce biri bulmuş olabilir mi?' sorusuna yanıt vererek Yabe 2015 (R üzerinde), ABV 2017 (C üzerinde 9), MR04 (8), Landsberg-Ressayre (15) ve olası güncel preprints ([LİTERATÜR-DOĞRULANMADI] uyarısıyla birincil kaynak doğrulama zorunluluğu!) kapsayan uzman gönderim planını yaz."
    ),
]
t3_outputs = await parallel(prod_tasks, lambda item: agents[item[0]](item[1]))
t3_proto = await agents["B-deneysel-doğrulama"](
    "TUR 3 ÇAPRAZ DENETİM: B-hesaplamalı-cebir'in ürettiği M2/Singular betik planını bağımsız yeniden üretim protokolü ve yanlış-pozitif/yanlış-negatif hata modları açısından denetle:\n\n"
    + t3_outputs[1]
)
t3_digest = "\n\n".join([
    f"### (a) Düzeltilmiş r = 3 LaTeX Paragrafı (B-lineer-cebir)\n{t3_outputs[0]}",
    f"### (b) Bağımsız Macaulay2 & Singular Betikleri (B-hesaplamalı-cebir)\n{t3_outputs[1]}",
    f"### (b-ek) Bağımsız Yeniden Üretim Protokolü Denetimi (B-deneysel-doğrulama)\n{t3_proto}",
    f"### (c) Makale Değişiklik Listesi & 'Ne İddia Ediyoruz / Etmiyoruz' (B-yazım-editörü)\n{t3_outputs[2]}",
    f"### (c-ek) Motivasyon / Tartışma — Boolean/SAT Aktarım Taslağı (B-kuantum-hesaplama)\n{t3_outputs[3]}",
    f"### (d) Uzman Gönderim Planı & Öncelik Denetimi (B-cebirsel-karmaşıklık)\n{t3_outputs[4]}",
])
log("Tur 3 tamamlandı.")

# --- TUR 4: Son Hüküm ---
phase("Grup B — Tur 4: Moderatör Son Hükmü (mod-B)")
mod_prompt = f"""TUR 4 (SON HÜKÜM — mod-B):
Grup B'nin 4 turluk tüm bulgularını sentezle. Kendi değerlendirmeni en sona koy.

Aşağıdaki İKİ bölümü EKSİKSİZ üret:

BÖLÜM I — "BUGÜN NEYİ KESİN OLARAK KAPATABİLDİK?" TABLOSU & AÇIK KRİTİK SORULAR:
(Adım / İddia | Bugünkü Durum | Eksik Kalan İş) biçiminde Markdown tablo kur ve crit-B'nin cevaplanmayan sorularını listele.

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
final_verdict = await mod_b(mod_prompt)

out_md = os.path.join(PAPER_DIR, "AUDIT_GROUP_B.md")
with open(out_md, "w", encoding="utf-8") as f:
    f.write("# GRUP B ('Doğrulama ve Yayın Hazırlığı' — 12 Ajan, 4 Tur) Denetim Dosyası\n\n")
    f.write("## Tur 1 — Bağımsız Okuma (10 Uzman)\n\n" + t1_digest + "\n\n---\n\n")
    f.write("## Tur 2 — crit-B Saldırıları ve Yanıtlar\n\n### crit-B Soruları\n" + crit_attacks + "\n\n" + t2_digest + "\n\n---\n\n")
    f.write("## Tur 3 — Üretilen Düzeltme ve Doğrulama Çıktıları\n\n" + t3_digest + "\n\n---\n\n")
    f.write("## Tur 4 — mod-B Son Hükmü\n\n" + final_verdict + "\n")

log(f"Saved full dossier to {out_md}")
print(final_verdict)
