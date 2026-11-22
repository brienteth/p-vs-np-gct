"""0G Council Phase 7B: Self-Referee Catch (Pi_RowML w2=1) & Krull Singular-Locus Unconditional Bound for Globally Mixed ABPs."""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
LOG_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_PHASE7B_LOG.md"
BASE_URL = "https://router-api.0g.ai/v1"


def load_api_key() -> str:
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("0G_API_KEY="):
                return line.strip().split("=", 1)[1].strip()
    raise RuntimeError("0G_API_KEY missing")


def call_0g(api_key: str, system: str, user: str) -> str:
    payload = {
        "model": "0gm-1.0-35b-a3b",
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": 0.25,
        "max_tokens": 1800,
    }
    cmd = [
        "/usr/bin/curl", "-sS", "--max-time", "40",
        f"{BASE_URL}/chat/completions",
        "-H", f"Authorization: Bearer {api_key}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    raw = json.loads(res.stdout)
    msg = raw["choices"][0]["message"]
    return (msg.get("content") or msg.get("reasoning_content") or "").strip()


PROMPTS: List[Dict[str, str]] = [
    {
        "id": "0g-oklid-phase7b",
        "system": "Sen Öklid'sin. Aksiyomatik kesinlik, tekillik geometrisi ve tam cebirsel kanıt üzerine Türkçe yanıt ver. [KANITLANDI]/[SANI] etiketle.",
        "user": (
            "AŞAMA 7B — İKİ BÜYÜK BULGU:\n"
            "1. HAKEM ÖZ-DÜZELTMESİ: Küresel karışımlı (1,4,w2,4,1) ABP'de yalnızca Pi_RowML (256 denklem) çözüldüğünde "
            "w2=2 (6/6, 7.8e-15) ve hatta w2=1 (2/6, 2.2e-13) bile çözülüyor! Yani Arşimet 2*w2 >= 6 sınırı yalnızca "
            "satır-ayrışımlı ABP'ler için geçerlidir; küresel karışımlı Pi_RowML için geçerli DEĞİLDİR (çünkü tek telde Q_{02} R_{13} Kronecker rankı 16 olabilir).\n"
            "2. YENİ KOŞULSUZ TEOREM (Krull + Torus İndirgemesi): Tam polinom perm_4(X) = sum_{s=1}^{w2} q_s(X) r_s(X) "
            "için Z(q_1..q_{w2}, r_1..r_{w2}) subseteq Sing(V(perm_4)) zorlar. char != 2'de codim(Sing(V(perm_3))) = 6'dır; "
            "x_{33} -> t*x_{33} torus limiti codim(Sing(V(perm_4))) >= 6 (sayısal tarama 77/80 noktada exact codim = 8!) verir. "
            "Krull Ana İdeal Teoremi ile 2*w2 >= codim(Sing(V(perm_4))) >= 6 => w2 >= 3 (codim=8 kanıtlanırsa w2 >= 4!) "
            "HİÇBİR satır-ayrışımı varsaymadan kanıtlanır! Bu 3 satırlık aksiyomatik kanıtın sağlamlığını ve codim=8'e çıkış yolunu değerlendir (maks 180 kelime)."
        ),
    },
    {
        "id": "0g-gauss-phase7b",
        "system": "Sen Carl Friedrich Gauss'sun. Determinantal/permanental varyeteler, codimension ve Duvar 2 üzerine Türkçe yanıt ver. [KANITLANDI]/[SANI] etiketle.",
        "user": (
            "AŞAMA 7B — DUVAR 2 (det_n vs perm_n) TEKİLLİK BOYUT FARKI:\n"
            "- Determinant için Sing(V(det_n)) = {rank <= n-2} her n >= 3 için SABİT codim = 4'tür!\n"
            "- Permanent için Sing(V(perm_n)) codimension'ı n ile büyür: n=3'te kanıtlanmış exact codim = 6, "
            "n=4'te 77/80 tekil noktada min rank(Hess) = 8 (yoğun sıfırsız-satır/sütun blok-diyagonal noktalarda rank(Hess) = 10!).\n"
            "Bu fark Krull Teoremi üzerinden her küresel karışımlı kuadratik ayrıştırmada perm_n = sum_{s=1}^{w2} q_s r_s "
            "için 2*w2 >= codim(Sing(V(perm_n))) (n=4'te >= 6 kanıtlı -> w2 >= 3, codim=8 ile w2 >= 4; genel n'de lineer büyüme) "
            "verirken det_n için sadece 2*w2 >= 4 (w2 >= 2) verir. Bu geometrik uçurumun GCT (VP vs VNP) ve Duvar 2 açısından "
            "neden güçlü ama üstel alt sınır (2^{Omega(n)}) için tek başına yetersiz olduğunu açıkla (maks 180 kelime)."
        ),
    },
    {
        "id": "0g-ramanujan-phase7b",
        "system": "Sen Srinivasa Ramanujan'sın. Simetri, matris bölünmeleri ve kombinatorik eşitsizlikler üzerine Türkçe yanıt ver. [KANITLANDI]/[SANI] etiketle.",
        "user": (
            "AŞAMA 7B: Sing(V(perm_4)) üzerinde yoğun (sıfır satır/sütun içermeyen) tüm 38 tekil noktamız "
            "2x2 blok-diyagonal matris çıktı (8 sıfır + 2 adet perm_2=0 => exact codim = 10), en küçük codim = 8 ise "
            "iki sıfır satır / 1 sıfır satır + 3x4 matrisin tüm 3x3 alt-permanentlerinin sıfırlanması durumunda elde edildi! "
            "Genel n x n matrislerde Sing(V(perm_n))'in en küçük codimension'ının 2n (iki sıfır satır) olup olmadığını "
            "ve blok-diyagonal ayrışımların codim = 2n'den büyük kalışının kombinatorik nedenini incele (maks 180 kelime)."
        ),
    },
]


def main() -> int:
    api_key = load_api_key()
    with ThreadPoolExecutor(max_workers=3) as pool:
        futs = [pool.submit(call_0g, api_key, p["system"], p["user"]) for p in PROMPTS]
        outs = [f.result() for f in futs]

    lines = ["# 0G Konseyi — Aşama 7B (Pi_RowML Öz-Düzeltmesi & Krull Tekillik Alt Sınırı)\n"]
    for p, out in zip(PROMPTS, outs):
        lines.append(f"## {p['id']}\n\n{out}\n\n---\n")

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[0G Phase 7B] Saved 3 mathematician analyses to {LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
