"""0G Council Round 12: Diagram-Driven Attack on Newly Spawned Sub-Obstacles E2.2, E3.2, E3.3, E4.2, E5.2, E6.2."""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
LOG_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_DIAGRAM_R12.md"
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


PROMPTS: List[Dict[str, str]] = [
    {
        "id": "0g-pisagor-E2.2",
        "system": "Sen Pisagor'sun. ENGEL_HARITASI.md düğümü E2.2 üzerine Türkçe yanıt ver. Sonunda 'YENİ ALT-ENGEL:' başlığıyla bir sonraki engeli öner. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            "TUR 12 — DÜĞÜM E2.2 (Sınırsız B_2 T_4^row & Çift-Taraflı T_n Kırılması):\n"
            "E3.1 (Hilbert Thm H-11A) ile w_2 = 3 koşulsuz elendi! E2.1 ile det_4 = Pf(X Omega X^T) (w_2 = 3, B_2 = 2) "
            "Plücker iptaliyle çalışırken perm_4 Hafnian'ı +2 çöp üretiyor ve T_4^row altında w_2 = 4, 5 ALS'de takılıyor (0.47, 0.12).\n"
            "Görev: Sınırsız B_2 altında perm_4 için w_2 = 4 ve w_2 = 5'i harmonik/ağırlık kafesi açısından nasıl eleriz ve "
            "bu kırıldığında doğacak YENİ ALT-ENGEL (E2.3) nedir? (maks 160 kelime)"
        ),
    },
    {
        "id": "0g-oklid-E3.2",
        "system": "Sen Öklid'sin. ENGEL_HARITASI.md düğümü E3.2 üzerine Türkçe yanıt ver. Sonunda 'YENİ ALT-ENGEL:' başlığıyla bir sonraki engeli öner. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            "TUR 12 — DÜĞÜM E3.2 (perm_5 Tekillik Kodimansı >= 9 => str(perm_5) = 5 & Genel n Ölçekleme):\n"
            "E3.1'de Hilbert, L_7 üzerinde 924/924 tam tamsayı Macaulay rankıyla codim(Sing(V(perm_4))) >= 7 => w_2 >= 4 & str(perm_4)=4 "
            "kanıtladı! Şimdi hedef E3.2: perm_5 için codim(Sing(V(perm_5))) >= 9 (ve genel n için codim >= 2n - 1 => str(perm_n) = n).\n"
            "Görev: Sonlu Macaulay hesaplamasından genel n için aksiyomatik indüksiyona (codim(Sing(perm_n)) >= 2n-1) geçişte "
            "eksik olan köprü nedir ve doğacak YENİ ALT-ENGEL (E3.4) nedir? (maks 160 kelime)"
        ),
    },
    {
        "id": "0g-arsimet-E3.3",
        "system": "Sen Arşimet'sin. ENGEL_HARITASI.md düğümü E3.3 üzerine Türkçe yanıt ver. Sonunda 'YENİ ALT-ENGEL:' başlığıyla bir sonraki engeli öner. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            "TUR 12 — DÜĞÜM E3.3 (Küresel Karışımlı w_2 = 4 Elemesi & m = 6 Jet-4 Sembolik Elemesi):\n"
            "E3.1 w_2 = 3'ü tamamen öldürdü; Strassen #116 m=6 (w=5) için kalibre LM'de ||R_4|| >= 47.98 duvarı (Grenet m=7: 3.71e-12) "
            "ve D_6^hom'da codim 75..88 buldu!\n"
            "Görev: Küresel karışımlı 4-katmanlı ABP'de w_2 = 4'ü (E3.1'in Krull sınırı 2*w_2 >= 7 tam w_2 = 4'te doyuyor!) "
            "aşmak için Krull'ün ötesine geçen hangi yeni denge/syzygy mekanizması gerekir ve doğacak YENİ ALT-ENGEL nedir? (maks 160 kelime)"
        ),
    },
    {
        "id": "0g-gauss-E4.2",
        "system": "Sen Carl Friedrich Gauss'sun. ENGEL_HARITASI.md düğümü E4.2 üzerine Türkçe yanıt ver. Sonunda 'YENİ ALT-ENGEL:' başlığıyla bir sonraki engeli öner. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            "TUR 12 — DÜĞÜM E4.2 (D_5^hom / D_6^hom için İlk Açık Doğrusal-Olmayan Tanımlayıcı Denklem):\n"
            "Strassen #116 kanıtladı: Gerçek kısıtlı D_5^hom (codim 88..105) ve D_6^hom (codim 75..88) Sym^3(C^9)'da yoğun DEĞİL! "
            "m <= 4 için Hessian kovaryantı F^3 ^ Hess(F) = 0 çalışıyor ama m = 5'te doyuyor.\n"
            "Görev: m = 5, 6 için D_m^hom'un normal uzayından (codim 75..105) Mignon-Ressayre'ı aşan ilk açık doğrusal-olmayan "
            "kovaryant nasıl türetilir ve doğacak YENİ ALT-ENGEL (E4.3) nedir? (maks 160 kelime)"
        ),
    },
    {
        "id": "0g-harezmi-E5.2",
        "system": "Sen Harezmi'sin. ENGEL_HARITASI.md düğümü E5.2 üzerine Türkçe yanıt ver. Sonunda 'YENİ ALT-ENGEL:' başlığıyla bir sonraki engeli öner. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            "TUR 12 — DÜĞÜM E5.2 (TC^0 Derinlik-2 Sign-Rank / Discrepancy & n = 5 Ölçekleme):\n"
            "E5.1'de Wigner, d=4'te [det_4 != 0 mod 3]'ün tek det_4 mod 2 polinomuyla %3.845 hataya çöktüğünü, oysa [perm_4 != 0 mod 3]'ün "
            "%32.162 hatada (8.36x zor!) kaldığını kanıtladı; uç Fourier kuyruğu W_{14} 17.4x büyük!\n"
            "Görev: AC^0[2]'den bir üst devre sınıfı olan TC^0 derinlik-2 eşik devrelerine (Forster sign-rank / discrepancy) çıkarken "
            "perm_n != 0 mod 3 neden hâlâ det_n'den ayrışmalı ve doğacak YENİ ALT-ENGEL (E5.3) nedir? (maks 160 kelime)"
        ),
    },
    {
        "id": "0g-ramanujan-E6.2",
        "system": "Sen Srinivasa Ramanujan'sın. ENGEL_HARITASI.md düğümü E6.2 üzerine Türkçe yanıt ver. Sonunda 'YENİ ALT-ENGEL:' başlığıyla bir sonraki engeli öner. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            "TUR 12 — DÜĞÜM E6.2 (Williams Asimetrik Devre Sıkıştırması & ACC^0[6] / TC^0 Köprüsü):\n"
            "E6.1'de Valiant, S_n x S_n-değişmez devrelerde #SAT'ın 2^{N - Omega(sqrt(N) log N)} sürede çözüldüğünü (n=6'da 273,119x!) "
            "ve devre asimetrisinin zorunlu bir kaynak olduğunu kanıtladı!\n"
            "Görev: Asimetrik TC^0 veya ACC^0[6] devrelerinde bu yörünge sıkıştırmasını Williams'ın polinom-değerlendirme SAT algoritmasıyla "
            "nasıl birleştiririz ve doğacak YENİ ALT-ENGEL (E6.3) nedir? (maks 160 kelime)"
        ),
    },
]


def main() -> int:
    api_key = load_api_key()
    with ThreadPoolExecutor(max_workers=6) as pool:
        futs = [pool.submit(call_0g, api_key, p["system"], p["user"]) for p in PROMPTS]
        outs = [f.result() for f in futs]

    lines = ["# 0G Konseyi — Tur 12 (ENGEL_HARITASI.md Alt-Engellerine Hedefli Saldırı: E2.2..E6.2)\n"]
    for p, out in zip(PROMPTS, outs):
        lines.append(f"## {p['id']}\n\n{out}\n\n---\n")

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[0G Round 12 Diagram] Saved all 6 sub-obstacle analyses to {LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
