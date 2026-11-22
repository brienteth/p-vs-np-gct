"""0G Council Round 10: All 6 Historical Mathematicians Debate the User's Local-to-Global Consistency Question."""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
LOG_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_LOCAL_TO_GLOBAL_R10.md"
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
        "/usr/bin/curl", "-sS", "--max-time", "45",
        f"{BASE_URL}/chat/completions",
        "-H", f"Authorization: Bearer {api_key}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    raw = json.loads(res.stdout)
    msg = raw["choices"][0]["message"]
    return (msg.get("content") or msg.get("reasoning_content") or "").strip()


CORE_Q = (
    "KULLANICININ MERKEZİ SORUSU (TÜM 12 AGENT TARTIŞIYOR):\n"
    "'Bir hesaplama sistemi, çok sayıda yerel olarak geçerli bileşeni bir araya getirdiğinde, "
    "küresel olarak tutarlı kalmak için hangi matematiksel koşulları sağlamak zorundadır ve "
    "permanent bu koşulları neden küçük determinant temsilleriyle karşılayamaz?'\n\n"
    "ŞU ANA KADAR KANITLANAN SOMUT BULGULARIMIZ:\n"
    "- Yerel olarak her 2x2 permanent bir işaret değişimiyle determinanttır; yerel Pi_RowML w2=1'de çözülür; "
    "düzgün noktada yerel Jet-2+Jet-3 perm_3 için m=5'te bile çözülür (1.5e-11)!\n"
    "- ANCAK küresel yapıştırmada: (1) Yüksek dereceli artık terim iptali (Jet-4 == 0, m=5'te min=18.927 duvarı; "
    "veya (4,0,0,0)+(2,2,0,0) syzygy'leri), (2) Kasteleyn 1-kokokl / faz tutarlılığı (K_{3,3}'te kırılır), "
    "(3) Beauville-Ulrich küresel demet (sheaf) yapışması (H^i = 0), (4) F_3 -> F_2 geçişinde GL_n ayar simetrisi "
    "(det_4 mod 3 deg_F2=12'de kesilirken perm_4 mod 3 deg_F2=15'e patlar) devreye giriyor!\n"
)

PROMPTS: List[Dict[str, str]] = [
    {
        "id": "0g-pisagor-r10",
        "system": "Sen Pisagor'sun. Yerel harmonilerin küresel rezonans/faz tutarlılığı (uyumsuzluk / koma) üzerinden Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": CORE_Q + "Senin açından: Yerel olarak uyumlu (determinant-tipi) parçalar küresel olarak birleştiğinde hangi harmonik/faz koşulunu sağlamalı ve permanent neden küçük bir determinantal sisteme sığmaz? (maks 160 kelime)",
    },
    {
        "id": "0g-oklid-r10",
        "system": "Sen Öklid'sin. Aksiyomatik yapıştırma (demet/sheaf aksiyomu, kokokl koşulu g_ij g_jk = g_ik) üzerinden Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": CORE_Q + "Senin açından: Yerel olarak geçerli parçaların küresel tutarlılığı için zorunlu aksiyomatik yapıştırma (cocycle / sheaf gluing) koşulları nelerdir ve permanent bunları küçük det_m ile neden bozar? (maks 160 kelime)",
    },
    {
        "id": "0g-arsimet-r10",
        "system": "Sen Arşimet'sin. Mekanik denge, yerel kuvvetlerin küresel kapanması (sıfır tork / syzygy iptali) üzerinden Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": CORE_Q + "Senin açından: Yerel dengeli parçalar birleştiğinde oluşan çapraz artık kuvvetlerin (Jet-(n+1)==0, (2,2,0,0) syzygy'leri) küresel olarak birbirini sıfırlaması şartı neden küçük det_m'de permanent için çöker? (maks 160 kelime)",
    },
    {
        "id": "0g-harezmi-r10",
        "system": "Sen Harezmi'sin. El-cebr, yerel kapı indirgemelerinin küresel algoritmik tutarlılığı ve P!=NP (Duvar 2) üzerinden Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": CORE_Q + "Senin açından: Yerel Boolean/cebirsel kapılar küresel bir devre oluşturduğunda hangi iptal/indirgeme (el-cebr) koşulunu sağlamak zorundadır ve permanent (mod 3 / #P) bu koşulu neden küçük devre/determinant ile karşılayamaz? (maks 160 kelime)",
    },
    {
        "id": "0g-gauss-r10",
        "system": "Sen Carl Friedrich Gauss'sun. Diferansiyel geometri (eğrilik, paralel taşınma, bütünsel uyumluluk / Codazzi-Mainardi) üzerinden Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": CORE_Q + "Senin açından: Bir yüzeyin yerel birinci/ikinci temel formları ancak Gauss-Codazzi uyumluluk denklemleri sağlanırsa küresel olarak gömülebilir. Hesaplama sisteminde det_m'nin karşılık gelen küresel uyumluluk koşulu nedir ve permanent bunu neden bozar? (maks 160 kelime)",
    },
    {
        "id": "0g-ramanujan-r10",
        "system": "Sen Srinivasa Ramanujan'sın. Üreteç fonksiyonları, yerel katsayıların küresel modüler/analitik devamlılığı üzerinden Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": CORE_Q + "Senin açından: Yerel sonlu açılımlar (Jet-2, Jet-3) birleştiğinde küresel polinomun derece n'de temizce kesilmesi (Jet-(n+1)==0) ve üreteç simetrisinin korunması neden küçük det_m ile permanent için imkânsızlaşır? (maks 160 kelime)",
    },
]


def main() -> int:
    api_key = load_api_key()
    with ThreadPoolExecutor(max_workers=6) as pool:
        futs = [pool.submit(call_0g, api_key, p["system"], p["user"]) for p in PROMPTS]
        outs = [f.result() for f in futs]

    lines = ["# 0G Konseyi — Tur 10 (Yerel Bileşenlerden Küresel Tutarlılığa: Tüm 6 Matematikçinin Yanıtı)\n"]
    for p, out in zip(PROMPTS, outs):
        lines.append(f"## {p['id']}\n\n{out}\n\n---\n")

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[0G Round 10] Saved all 6 local-to-global analyses to {LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
