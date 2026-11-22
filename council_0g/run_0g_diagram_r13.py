"""
Round 13 — 0G Historical Mathematicians Council Runner for ENGEL_HARITASI.md Active Sub-Obstacles:
  - 0g-pisagor:   Node E2.3 (Bosonic Survival on Hyperplane Products & 4-Layer T_4^row Symbolic Closure)
  - 0g-oklid:     Node E3.4 (Crossing the 2n Two-Zero-Row Ceiling via Sing_2(V(perm_n)) & Tangential Hessian)
  - 0g-arsimet:   Node E3.5 (3-Block Shortcut-Syzygy Elimination y^T A_13 z = -y^T A_11 K y for perm_4)
  - 0g-gauss:     Node E4.3 (Explicit IMSC / Sing_2 Polynomial Invariant P^{(4)}(F) for perm_4)
  - 0g-harezmi:   Node E5.3 (n=5 61-Orbit Symmetric RM(5,25) Wall & Projected TC^0_2 Forster Bound)
  - 0g-ramanujan: Node E6.3 (TC^0_2 = MAJ o THR Orbit-Averaged Threshold Dictionary Discrepancy LP)
"""
import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
OUT_MD = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_DIAGRAM_R13.md"
API_URL = "https://router-api.0g.ai/v1/chat/completions"
MODEL = "0gm-1.0-35b-a3b"


def load_key() -> str:
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("0G_API_KEY="):
                return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("0G_API_KEY not found")


PROMPTS = [
    (
        "0g-pisagor-E2.3",
        "Sen Pisagor'sun. ENGEL_HARITASI.md düğümü E2.3 üzerine Türkçe yanıt ver, sonunda 'YENİ ALT-ENGEL:' başlığıyla bir sonraki engeli (E2.4) öner. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 13 — DÜĞÜM E2.3 (4-Katmanlı T_4^row m=13,14 Sembolik Kapanışı & Bosonik Hiperdüzlem Hayatta Kalması): "
        "w_1=4 (her satır i için tek doğrusal form l_i(v_i)) iken K_i = ker(l_i) (dim 3) çarpımı K_0 x K_1 x K_2 x K_3 üzerinde tüm Katman-1 düğümleri sıfırlanır. "
        "det_4(X), keyfi u!=0 için (u^perp)^4 üzerinde sıfırlanırken, perm_4(X) yalnızca dört formun tamamı aynı sütun koordinatı X_{i,j0}'ın katıysa sıfırlanabilir! "
        "Bu tek-sütun kilidi m=13,14'ü nasıl tamamen öldürür ve çift-taraflı T_n kırılmasında hangi YENİ ALT-ENGEL (E2.4) doğar? (En fazla 140 kelime)"
    ),
    (
        "0g-oklid-E3.4",
        "Sen Öklid'sin. ENGEL_HARITASI.md düğümü E3.4 üzerine Türkçe yanıt ver, sonunda 'YENİ ALT-ENGEL:' başlığıyla bir sonraki engeli (E3.6) öner. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 13 — DÜĞÜM E3.4 (2n İki-Sıfır-Satır Tavanını Aşmak: Teğetsel Hessian & Sing_2(V(perm_n))): "
        "Tur 12'de codim(Sing(V(perm_4))) = 8 = 2n kesin eşitliği ve codim(Sing(V(perm_5))) >= 8 kanıtlandı. "
        "2-sıfır-satır altvaryetesi gerçek codim = 2n olduğundan saf Krull kesişimi w >= n sınırında durur. "
        "Ancak perm_n = sum_{s=1}^w G_s H_s ayrışımında V(G,H) üzerinde rank(Hess(perm_n)) <= 2w zorunludur ve 2x2 alt-permanentlerin sıfır kümesi Sing_2(V(perm_n)) (3-sıfır-satır, codim=3n) çok daha yüksek kodimanslıdır. "
        "Sing_2 ve Teğetsel Hessian birlikte w >= n sınırını nasıl aşar ve hangi YENİ ALT-ENGEL (E3.6) doğar? (En fazla 140 kelime)"
    ),
    (
        "0g-arsimet-E3.5",
        "Sen Arşimet'sin. ENGEL_HARITASI.md düğümü E3.5 üzerine Türkçe yanıt ver, sonunda 'YENİ ALT-ENGEL:' başlığıyla bir sonraki engeli (E3.7) öner. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 13 — DÜĞÜM E3.5 (perm_4 3-Blok Kısayol-Syzygy Elemesi m in {9..14}): "
        "Tur 12'de Strassen Teorem 13A/13B ile dc(perm_4) >= 9 ve kısayolsuz (A_13 = 0) 3-blok gösterimler için m >= 13 kanıtlandı. "
        "Kısayollu durumda kübik syzygy [t^3] = y^T A_11 K y + y^T A_13 z == 0, y^T A_13(X) z in <y>^2 koşulunu zorlar. "
        "Bu Koszul syzygy kısıtı kısayol terimi y^T A_13 A_33 z mod <y>^2'nin katkı rankını nasıl sınırlar ve hangi YENİ ALT-ENGEL (E3.7) doğar? (En fazla 140 kelime)"
    ),
    (
        "0g-gauss-E4.3",
        "Sen Gauss'sun. ENGEL_HARITASI.md düğümü E4.3 üzerine Türkçe yanıt ver, sonunda 'YENİ ALT-ENGEL:' başlığıyla bir sonraki engeli (E4.4) öner. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 13 — DÜĞÜM E4.3 (perm_4 İçin Açık IMSC / Sing_2 Polinom İnvaryantı P^{(4)}(F)): "
        "Tur 12'de perm_3 != D_6^hom için açık derece-126 Macaulay determinant polinomu P_{I0}(F) in Z[F]_126 inşa edildi (mod 1000003'te 428736 != 0). "
        "Şimdi perm_4 için L_8 subset C^16 üzerindeki derece-9 IMSC determinantı D_8^hom'u eliyor. "
        "m in {9..14} aralığını da sıfırlayan Sing_2 / Hessian-Macaulay polinom invaryantı P^{(4)}(F) nasıl kurulur ve hangi YENİ ALT-ENGEL (E4.4) doğar? (En fazla 140 kelime)"
    ),
    (
        "0g-harezmi-E5.3",
        "Sen Harezmi'sin. ENGEL_HARITASI.md düğümü E5.3 üzerine Türkçe yanıt ver, sonunda 'YENİ ALT-ENGEL:' başlığıyla bir sonraki engeli (E5.4) öner. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 13 — DÜĞÜM E5.3 (n=5 61-Yörüngeli Simetrik RM(5,25) Duvarı & Yoğunluk-İzdüşümlü TC^0_2 Forster Sınırı): "
        "Tur 12'de tüm 33,554,432 (n=5) matriste det_5 mod 2 tek-terimli hatası %8.36 vs %40.91 (4.89x) ve toplam etki geçişi I(perm_5!=0 mod 3) = 7.897 > 6.865 bulundu; "
        "n=4 Damalı Kesitte rk_F2 = 129 vs 92 iken spektral Forster'ı sıfır-satır yoğunluk modu (sigma_1 ~ 128) maskeledi. "
        "61-boyutlu tam S_5xS_5 RM(5,25) uzayında ve yoğunluk-izdüşümlü damalı matriste ayrışma nasıl büyür ve hangi YENİ ALT-ENGEL (E5.4) doğar? (En fazla 140 kelime)"
    ),
    (
        "0g-ramanujan-E6.3",
        "Sen Ramanujan'sın. ENGEL_HARITASI.md düğümü E6.3 üzerine Türkçe yanıt ver, sonunda 'YENİ ALT-ENGEL:' başlığıyla bir sonraki engeli (E6.4) öner. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 13 — DÜĞÜM E6.3 (TC^0_2 = MAJ o THR Yörünge-Ortalamalı Eşik Sözlüğü Discrepancy LP'si): "
        "Tur 12'de Valiant Teorem 21.1/21.2 ile tek-katmanlı asimetrik PTF_D ve MAJ o AND_D devrelerinde Reynolds yörünge çöküşünün L_1-izometrik olduğu (D=6'da 4.23x ağırlık farkı ve K_n(<=6)=151 ile 4.33e9x sıkıştırma) kanıtlandı. "
        "Asimetrinin kaçabildiği tek yer, alt katmanda süreksiz sgn(alpha.X - theta) kullanan TC^0_2 = MAJ o THR devresidir. "
        "132/317 yörüngeli Yao dual sert dağılımı mu*'a karşı THR sözlüğü korelasyonu nasıl sınırlanır ve hangi YENİ ALT-ENGEL (E6.4) doğar? (En fazla 140 kelime)"
    ),
]


def query_one(item, api_key: str):
    name, sys_p, usr_p = item
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": sys_p},
            {"role": "user", "content": usr_p},
        ],
        "temperature": 0.35,
        "max_tokens": 1600,
    }
    cmd = [
        "/usr/bin/curl", "-s", "-X", "POST", API_URL,
        "-H", f"Authorization: Bearer {api_key}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload, ensure_ascii=False),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    try:
        data = json.loads(res.stdout)
        msg = data["choices"][0]["message"]
        text = msg.get("content") or msg.get("reasoning_content") or str(data)
    except Exception as e:
        text = f"ERROR: {e} | raw={res.stdout[:300]}"
    return name, text.strip()


def main():
    api_key = load_key()
    with ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(lambda it: query_one(it, api_key), PROMPTS))
    lines = ["# 0G Konseyi — Tur 13 (ENGEL_HARITASI.md Yeni Alt-Engellerine Saldırı: E2.3..E6.3)\n"]
    for name, text in results:
        lines.append(f"## {name}\n\n{text}\n\n---\n")
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[0G Round 13 Diagram] Saved all 6 sub-obstacle analyses to {OUT_MD}")


if __name__ == "__main__":
    main()
