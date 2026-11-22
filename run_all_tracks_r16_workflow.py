#!/usr/bin/env python3
"""
Round 16 — 31-Agent Simultaneous 5-Track Workflow + 1 Inter-Track Organizer
Runs via Antigravity `run_workflow` tool:
  - Phase 1: 5 active barrier tracks (K1..K5) run simultaneously (`parallel`).
             Each track clones ALL 6 existing council personas (`prof-euler`,
             `prof-hilbert`, `prof-strassen`, `prof-noether`, `prof-wigner`,
             `prof-valiant`) for 2 turns (`5 x 6 = 30` track agents).
  - Phase 2: 1 Inter-Track Organizer (`Agent #31`) integrates all 5 tracks,
             resolves cross-track dependencies (`K4<->K5`, `K2<->K3`, `K1<->K3`),
             and produces the strict post-Round-16 epistemic ledger.

Saves full dossier to `/Users/bl10buer/Desktop/matemk/p-vs-np-gct/ROUND16_ALL_TRACKS_DOSSIER.md`.
"""
from __future__ import annotations

import os

BASE_DIR = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct"
LOGS_DIR = os.path.join(BASE_DIR, "r16_logs")


def read_text(path: str, start=None, end=None) -> str:
    if not os.path.exists(path):
        return f"[DOSYA YOK: {path}]"
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    s = 0 if start is None else start - 1
    e = len(lines) if end is None else end
    return "".join(lines[s:e])


COMMON_RULES = """=== BAĞLAYICI TUR 16 KURALLARI ===
1. YALNIZ verilen BİRİNCİL KOD, DENETİM METİNLERİ ve yerel `exit code 0` KESİN HESAP LOGLARINDAN çalış; hafızadan veya özetlerden teorem/sayı uydurma.
2. HER İDDİANIN sonunda tam olarak şu 4 etiketten BİRİNİ kullan:
   - `[İSPAT]`: Tüm ara adımlarını verilen metin/cebirde doğrudan gördüğün veya kendin adım adım kurduğun çıkarımlar.
   - `[KESİN HESAP]`: Verilen yerel `exit code 0` logunda birebir gözlenen tam tamsayı/modüler/sembolik/sayısal sonuçlar.
   - `[SANI]`: Makul görünen ancak henüz genel/asimptotik olarak kanıtlanmamış ekstrapolasyonlar.
   - `[DOĞRULANMADI]`: Logda/metinde olmayan, çalıştırılmamış veya eksik adım taşıyan iddialar.
3. Herhangi bir teknik boşluk, `float64`/sentetik tehlike, simetri-tuzağı veya aktarım engeli gördüğünde açıkça **`ŞU ADIMDA TIKANDI`** yaz.
4. Hiçbir araç (run_command, read_file, write_file vb.) ÇAĞIRMA; cevabını doğrudan `finish` aracına Türkçe markdown olarak yaz."""

SIX_PROFS = [
    (
        "prof-euler",
        "Kombinatoryal yapı, graf/çift-sayım eşitsizlikleri, tüm `assert`/kayan nokta/sentetik harness tuzaklarını kırmızı-takım olarak denetlersin.",
    ),
    (
        "prof-hilbert",
        "Cebirsel geometri, Sing/Sing_2, Hilbert fonksiyonları, sıfır-blok minörleri ve F_p -> Q Macaulay/CSR rank kaldırmasını denetlersin.",
    ),
    (
        "prof-strassen",
        "Tensör/matris-kalem rankı, normal formlar, korank dalları (r=1..5), Laurent eğrileri ve sınır karmaşıklığını denetlersin.",
    ),
    (
        "prof-noether",
        "Simetri grupları, temsil teorisi, BIP19 dolgu engeli ve Simetri-Tersine Çevirme Tuzağı (T_n-kısıtlı -> genel VP ayrımı) denetimini yaparsın.",
    ),
    (
        "prof-wigner",
        "Sonlu cisim rankı (F_2, F_3), Grassmannian boyutları, spektral/iletişim alt sınırları ve mod-p ayrımlarını denetlersin.",
    ),
    (
        "prof-valiant",
        "Devre/ABP modelleri, Yao/LP dualitesi, TC^0 ve Teorem v2 (H1–H4) üzerinden SAT / P/poly aktarım koşullarını ve AW09/RR97 bariyerlerini denetlersin.",
    ),
]

k1_log = read_text(os.path.join(LOGS_DIR, "k1_noether.log"))
k2_perm5_log = read_text(os.path.join(LOGS_DIR, "k2_perm5.log"))
k2_hilbert_log = read_text(os.path.join(LOGS_DIR, "k2_hilbert16.log"))
k3_border_log = read_text(os.path.join(LOGS_DIR, "k3_border.log"))
k4_wigner_log = read_text(os.path.join(LOGS_DIR, "k4_wigner.log"))
k5_valiant_log = read_text(os.path.join(LOGS_DIR, "k5_valiant.log"))

k1_ctx = f"""=== KOL 1 (E1 n=6, w=19 + E2.6 T_5^row Deficit & Laurent Kutup Rankı) ===
--- round16_e26_n5_deficit_closure_and_laurent_rank.py ---
{read_text(os.path.join(BASE_DIR, "council/prof-noether/round16_e26_n5_deficit_closure_and_laurent_rank.py"))}

--- verify_all_council.py başlık özeti (satır 1-51) ---
{read_text(os.path.join(BASE_DIR, "council/prof-euler/verify_all_council.py"), 1, 51)}

--- YEREL ÇALIŞTIRMA LOGU (k1_noether.log) ---
{k1_log}"""

k2_ctx = f"""=== KOL 2 (E3.10 + perm_5 dc >= 14 Saldırısı) ===
--- verify_round16_perm5_exact.py ---
{read_text(os.path.join(BASE_DIR, "council/prof-hilbert/verify_round16_perm5_exact.py"))}

--- verify_round16_hilbert.py (satır 1-110 & 319-444) ---
{read_text(os.path.join(BASE_DIR, "council/prof-hilbert/verify_round16_hilbert.py"), 1, 110)}
...
{read_text(os.path.join(BASE_DIR, "council/prof-hilbert/verify_round16_hilbert.py"), 319, 444)}

--- YEREL ÇALIŞTIRMA LOGU 1 (k2_perm5.log — C uint64_t + bit-exact bounded int64 BLAS) ---
{k2_perm5_log}

--- YEREL ÇALIŞTIRMA LOGU 2 (k2_hilbert16.log — varsa) ---
{k2_hilbert_log}"""

k3_ctx = f"""=== KOL 3 (E4.6 — Gerçek dc-bar(perm_4) & Gerçek Oluşturulmuş m=10 Homojen Test) ===
--- AUDIT_SHESHADRI_AND_DCBAR.md Konu 3 özeti (satır 659-750) ---
{read_text(os.path.join(BASE_DIR, "paper_dc_perm4/AUDIT_SHESHADRI_AND_DCBAR.md"), 659, 750)}

--- verify_round16_e46_border_diagnosis.py (Part A & B) ---
{read_text(os.path.join(BASE_DIR, "council/prof-strassen/verify_round16_e46_border_diagnosis.py"), 1, 55)}
...
{read_text(os.path.join(BASE_DIR, "council/prof-strassen/verify_round16_e46_border_diagnosis.py"), 320, 815)}

--- YEREL ÇALIŞTIRMA LOGU (k3_border.log) ---
{k3_border_log}"""

k4_ctx = f"""=== KOL 4 (E5.6 — Analitik Grassmannian rk_F2([det_n != 0 mod 3]) Üst Sınırı & perm_n Ayrımı) ===
--- round16_e56_grassmannian_rkf2_theorem.py ---
{read_text(os.path.join(BASE_DIR, "council/prof-wigner/round16_e56_grassmannian_rkf2_theorem.py"))}

--- YEREL ÇALIŞTIRMA LOGU (k4_wigner.log) ---
{k4_wigner_log}"""

k5_ctx = f"""=== KOL 5 (E6.6 — det_n PTF Direnci, Yao Dual Desteği, Dual-Core -> rk_F2 Köprüsü & Teorem v2) ===
--- test_round16_engel66_orbit_lp_separating_invariant.py (satır 1-287) ---
{read_text(os.path.join(BASE_DIR, "council/prof-valiant/test_round16_engel66_orbit_lp_separating_invariant.py"), 1, 287)}

--- QUANTITATIVE_TRANSFER_THEOREM_SYNTHESIS.md Teorem v2 (satır 16-90) ---
{read_text(os.path.join(BASE_DIR, "QUANTITATIVE_TRANSFER_THEOREM_SYNTHESIS.md"), 16, 90)}

--- YEREL ÇALIŞTIRMA LOGU (k5_valiant.log) ---
{k5_valiant_log}"""

TRACKS = [
    {
        "id": "K1",
        "title": "Kol 1 — E1 (n=6) & E2.6 (T_5^row Deficit + Laurent Kutup Rankı)",
        "ctx": k1_ctx,
        "t1_focus": (
            "1) `round16_e26` Kısım A'daki `Theorem 22A` (`w_1=6, w_4=5` için `w_2=8,9` çift-sayım elemesi -> `w_2>=10`, `m>=32>=31`): "
            "kodun kullandığı `str(perm_3|_H) == 2` ve satır-0/Layer-2 varsayımları eksiksiz mi, açık `else` dalı var mı? `r_2 = 0` vs `r_2 in {1..4}` kanıtını denetle.\n"
            "2) `Theorem 22B` (`(k_r, k_c)` Laurent kutup rankı) `n=4` dışına (`n >= 5`, `n=6` `E1`) genelleşir mi, yoksa Simetri-Tersine Çevirme Tuzağı (`T_n`-eşdeğişir ABP) yüzünden `D1`'e (`VP != VNP`) neden taşınmaz?"
        ),
    },
    {
        "id": "K2",
        "title": "Kol 2 — E3.10 + perm_5 dc >= 14 (MR04=13 Üstü) Saldırısı",
        "ctx": k2_ctx,
        "t1_focus": (
            "1) `k2_perm5.log`'daki saf `uint64_t` `Sing_2(perm_5)` (`k=13, 14, 15`, `D=5`) ve `L_10` `Sing(perm_5)` (`D=6, 7` + `D=8..10` CSR ayak izi) sonuçları neyi kesin kanıtladı, hangi $k$ açık kaldı? (`k2_hilbert16.log` varsa `H-16` durumunu da denetle.)\n"
            "2) `perm_5` için `dc(perm_5) >= 14` hedefi (`MR04 = 13` üstü) tam olarak hangi üç duvarda tıkanıyor (`L_10`, `r in {2,3,4}`, `m=13` `(D,w-D)=(10,2)` duvarı)?"
        ),
    },
    {
        "id": "K3",
        "title": "Kol 3 — E4.6 Gerçek dc-bar(perm_4) & Gerçek m=10 F_{m10} Testi",
        "ctx": k3_ctx,
        "t1_focus": (
            "1) `k3_border.log` Kısım A'daki tam-16-değişkenli `Curve L1` ve `Curve L2` gerçek B_9^{(4)} Laurent testlerinin `L_8` ve `L_{12}` sonuçlarını değerlendir: tilde{R}_9^{(4)}'a karşı-örnek çıktılar mı yoksa `codim Sing` neden <= 7 kaldı?\n"
            "2) `k3_border.log` Kısım B'deki **gerçek oluşturulmuş m=10 polinomu F_{m10}** (sentetik `H_sym` yerine!) `L_9 H_{<=4}` ve `L_12` üzerinde ne verdi? `T^{(4)}(F_{m10})==0` kapanıyor mu ve `12,870x12,870` direkt minörsüz bar(D_{10}^{hom}) durumu nedir?"
        ),
    },
    {
        "id": "K4",
        "title": "Kol 4 — E5.6 Analitik Grassmannian rk_F2([det_n != 0 mod 3]) Üst Sınırı",
        "ctx": k4_ctx,
        "t1_focus": (
            "1) `round16_e56` içindeki `P_{0,1}(F_3^4)` `'40 == 40'` eşlemesi ve `|Gr_{0,1}(<=2, n, F_3)|` sayımı genel n için rk_{F_2}([det_n != 0 mod 3]) <= |Gr(2, n, F_3)| (yaklaşık 3^{2n}?) analitik kanıtı veriyor mu?\n"
            "2) `perm_5` (`336/1024`) ve `n=6` (`264 vs 1456 = 5.52x`) için neden `float64` `np.linalg.det` kullanıldığı, genel `n` asimptotik alt sınırı ve bunun `Mod_3 P` vs `NC^2` / `P/poly` (`D2`) kapı alt sınırına nasıl bağlanacağı (veya neden tıkandığı) nedir?"
        ),
    },
    {
        "id": "K5",
        "title": "Kol 5 — E6.6 det_n PTF Direnci, Yao Dual-Core -> rk_F2 Köprüsü & Teorem v2",
        "ctx": k5_ctx,
        "t1_focus": (
            "1) `Theorem 24.1` (`det_n = c - IP_{n-1}(u,v)` Schur gömülmesi) `det_n mod 2` ve `[det_n != 0 mod 3]`'ün `D_PTF >= n-1` direncini eksiksiz açıklıyor mu? `Theorem 24.2` üç ayırıcısı (`W_min` `182.32 vs 104.19`, `127/317 vs 73/317`, `Dual-Core Chk rk_F2`) neden ham PTF'den farklıdır?\n"
            "2) `K_4=317` yörünge-LP bulguları asimptotik `TC^0_2` / `TC^0_3` / `P/poly` (`D2`) alt sınırına `Teorem v2 (H1–H4)` altında taşınabiliyor mu, yoksa hangi adımda tıkanıyor?"
        ),
    },
]


async def run_track(t: dict) -> dict:
    track_agents = {}
    for prof_name, prof_spec in SIX_PROFS:
        track_agents[prof_name] = agent(
            prompt=(
                f"{COMMON_RULES}\n"
                f"KİMLİĞİN (KLON): {t['id']} koluna atanmış `{prof_name}` klonusun.\n"
                f"UZMANLIK VE DENETİM ODAĞIN: {prof_spec}"
            ),
            schema={"type": "string"},
            role=f"{t['id']}-{prof_name}",
            model="flash",
        )

    # Tur 1: 6 clone agents run in parallel on Track t
    t1_prompt_body = (
        f"TUR 1 — {t['title']}\n"
        f"GÖREVİN:\n{t['t1_focus']}\n"
        f"Kendi uzmanlık açından (`[İSPAT]`, `[KESİN HESAP]`, `[SANI]`, `[DOĞRULANMADI]` etiketleriyle) somut denetim yaz (<= 240 kelime).\n\n"
        f"{t['ctx']}"
    )
    r1_list = await parallel(
        list(track_agents.keys()),
        lambda pname: track_agents[pname](t1_prompt_body),
    )
    r1_digest = "\n\n".join(
        f"#### `{pname}` (Tur 1)\n{out}" for (pname, _), out in zip(SIX_PROFS, r1_list)
    )

    # Tur 2: 6 clone agents cross-review all 6 Turn-1 outputs in parallel
    t2_prompt_body = (
        f"TUR 2 (Çapraz Eleştiri ve Kapanış) — {t['title']}\n"
        f"6 klon arkadaşının Tur 1 raporları aşağıdadır. Kendi uzmanlığınla çelişkileri/atlanan varsayımları/harness açıklarını eleştir, "
        f"`ŞU ADIMDA TIKANDI` noktalarını kilitle ve bu kolda `Kapatılan` vs `Açık Kalan` son hükmünü ver (<= 200 kelime).\n\n"
        + r1_digest
    )
    r2_list = await parallel(
        list(track_agents.keys()),
        lambda pname: track_agents[pname](t2_prompt_body),
    )
    r2_digest = "\n\n".join(
        f"#### `{pname}` (Tur 2)\n{out}" for (pname, _), out in zip(SIX_PROFS, r2_list)
    )

    return {
        "id": t["id"],
        "title": t["title"],
        "r1_digest": r1_digest,
        "r2_digest": r2_digest,
    }


phase("Faz 1: 5 Engel Kolu Eşzamanlı Çalışma (5 × 6 = 30 Klon Agent, 2 Tur)")
track_results = await parallel(TRACKS, run_track)
log("Faz 1 tamamlandı: 5 kolun 30 klon ajanı 2 turu tamamladı.")

phase("Faz 2: 1 Kollar Arası Organizatör (Çapraz Entegrasyon & Epistemik Kapanış)")
all_tracks_summary = "\n\n---\n\n".join(
    f"### {tr['title']}\n\n#### Tur 1 Özetleri\n{tr['r1_digest']}\n\n#### Tur 2 Çapraz Kapanışlar\n{tr['r2_digest']}"
    for tr in track_results
)

raw_logs_snapshot = f"""=== DOĞRUDAN YEREL LOG ÖZETLERİ (exit code 0 kontrolü) ===
[K1 k1_noether.log]:
{k1_log}

[K2 k2_perm5.log]:
{k2_perm5_log}

[K2 k2_hilbert16.log]:
{k2_hilbert_log}

[K3 k3_border.log]:
{k3_border_log}

[K4 k4_wigner.log]:
{k4_wigner_log}

[K5 k5_valiant.log]:
{k5_valiant_log}"""

organizer_prompt = (
    COMMON_RULES
    + """
SENİN ROLÜN: Agent #31 — **Kollar Arası Organizatör**.
Beş paralel engel kolunun (5 × 6 = 30 klon agent) Tur 1 + Tur 2 raporları ve 6 yerel doğrulama logu aşağıdadır.

ZORUNLU ÇIKTILARIN:
1. **Kollar Arası Çapraz Entegrasyon Tablosu:**
   - **Kol 4 (`E5.6 rk_F2`) <-> Kol 5 (`E6.6 Yao Dual-Core`):** Yörünge-LP desteği ile rk_{F_2} büyümesi nasıl birleşiyor? Eksik halka nerede (`D2` / `Teorem v2 H1–H4`)?
   - **Kol 2 (`E3.10 perm_5`) <-> Kol 3 (`E4.6 dc-bar / m=10`):** Gerçek `m=10` F_{m10} ve Laurent B_9^{(4)} bulguları ile `perm_5` `r in {2,3,4}` / `Sing_2 k=14,15` bulguları nasıl kesişiyor?
   - **Kol 1 (`E2.6 T_n^row`) <-> Kol 3 (`Laurent kutupları`):** `Theorem 22B` plücker-kutupsuzlaşması ile Laurent sınır karmaşıklığı arasında gerçek aktarım var mı, yoksa *Simetri-Tersine Çevirme Tuzağı* kesiyor mu?
2. **Tur 16 Sonu Epistemik Kayıt Defteri (Tablo: Kol | Kapatılan `[İSPAT]`/`[KESİN HESAP]` | Kısmi/Koşullu | Tıkanan / `[DOĞRULANMADI]`).**
3. **Tur 17 İçin Tek En Yüksek Kaldıraçlı Eylem** (kol başına 1 somut adım) ve **`D1 (VP != VNP)` / `D2 (P != NP)` İçin Dürüst Uzaklık Raporu**.

"""
    + raw_logs_snapshot
    + "\n\n"
    + all_tracks_summary
)

organizer_out = await agent(
    prompt=organizer_prompt,
    schema={"type": "string"},
    role="Kollar Arası Organizatör",
    model="flash",
)
log("Faz 2 tamamlandı: Kollar Arası Organizatör sentezini bitirdi.")

out_path = os.path.join(BASE_DIR, "ROUND16_ALL_TRACKS_DOSSIER.md")
with open(out_path, "w", encoding="utf-8") as f:
    f.write("# Tur 16 — 5 Eşzamanlı Engel Kolu (5 × 6 = 30 Klon Agent) + 1 Kollar Arası Organizatör Dosyası\n\n")
    f.write("> Tüm iddialar yalnızca yerel `exit code 0` loglarından ve birincil kod metinlerinden `[İSPAT]`, `[KESİN HESAP]`, `[SANI]`, `[DOĞRULANMADI]` etiketleriyle süzülmüştür.\n\n")
    f.write("## Kollar Arası Organizatör (Agent #31) Nihai Sentezi\n\n")
    f.write(organizer_out + "\n\n---\n\n")
    f.write("## Yerel Çalıştırma Logları (`r16_logs/*.log`)\n\n")
    f.write(f"```text\n{raw_logs_snapshot}\n```\n\n---\n\n")
    for tr in track_results:
        f.write(f"## {tr['title']}\n\n")
        f.write(f"### Tur 1 — 6 Klon Agent Bağımsız Analizleri\n\n{tr['r1_digest']}\n\n")
        f.write(f"### Tur 2 — 6 Klon Agent Çapraz Eleştiri & Kapanış\n\n{tr['r2_digest']}\n\n---\n\n")

log(f"Dosya yazıldı: {out_path}")
print("=== KOLLAR ARASI ORGANİZATÖR (AGENT #31) ===")
print(organizer_out)
