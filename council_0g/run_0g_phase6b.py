"""0G Council Phase 6B: Surgical Analysis of the (2,2,0,0) Syzygy Phase Transition in Non-Row-Separated ABPs."""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
LOG_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_PHASE6B_LOG.md"
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
        "id": "0g-pisagor-phase6b",
        "system": "Sen Pisagor'sun. Harmonik filtreler, Z_4 faz operatörleri ve cebirsel simetri üzerine Türkçe yanıt ver. [KANITLANDI]/[SANI] etiketle.",
        "user": (
            "AŞAMA 6B KEŞFİ: Küresel karışımlı (1,4,w2,4,1) ABP'de:\n"
            "- Sadece Pi_RowML (256 denklem) ve Pi_RowML + (4,0,0,0) (396 denklem) w2=3'te bile tam çözülüyor (2.4e-13)!\n"
            "- Ancak Z_4 faz filtresiyle (2,2,0,0) iki-satır syzygy'leri (270 denklem -> toplam 666 denklem) eklendiğinde:\n"
            "  w2=6 (896 deg): 4/5 ÇÖZÜLDÜ (6.9e-13), fakat w2=5 (768 deg > 666 denklem!): 0/5 (min=3.2e-3), w2=4: 0/5 (3.5e-2), w2=3: 0/5 (1.1e-1)!\n"
            "Bu (2,2,0,0) Z_4-faz syzygy'si tam olarak Cephe 1'deki A1(a)A2(a)=0 ve B1(b)B2(b)=0 denklemlerinin küresel karşılığıdır! "
            "6 satır çiftinin (2,2,0,0) iptal şartlarını tek bir Z_4 karakter cebiri olarak nasıl formüle eder ve w2=5 için cebirsel çelişki çıkarırız? (maks 180 kelime)"
        ),
    },
    {
        "id": "0g-arsimet-phase6b",
        "system": "Sen Arşimet'sin. Kesit rankı, blok matris sıkıştırması ve denge ilkesi üzerine Türkçe yanıt ver. [KANITLANDI]/[SANI] etiketle.",
        "user": (
            "AŞAMA 6B KEŞFİ: Satır-ayrışımsız (1,4,w2,4,1) ABP'de (2,2,0,0) syzygy'si eklendiğinde w2=6 (4/5, 6.9e-13) "
            "çözülürken w2=5 (768 değişken > 666 denklem) 0/5 ile kırıldı! Ayrıca Grenet (1,4,6,4,1) noktasında kompleks Jakobyen rankı "
            "S0(RowML)=156, S1(+4000)=156, S3(+2row)=156 iken S4(+3row, yani (2,1,1,0)) eklendiğinde 156 -> 372'ye (+216) sıçrıyor! "
            "İki-satır (2,2,0,0) ortogonalliğinin 3 Arşimet iki-parçalı kesitinde (S | S^c) Q_S R_S = 0 tipi orta katman sıkıştırmasıyla "
            "nasıl w2 >= 6 alt sınırına sıçrama yapabileceğini analiz et (maks 180 kelime)."
        ),
    },
    {
        "id": "0g-harezmi-phase6b",
        "system": "Sen Harezmi'sin. Cebirsel indirgeme (el-cebr ve'l-mukabele) üzerine Türkçe yanıt ver. [KANITLANDI]/[SANI] etiketle.",
        "user": (
            "AŞAMA 6B KEŞFİ: (1,4,w2,4,1) küresel karışımlı ABP'de, {i, j} satır çiftine kısıtlanmış (2,2) bidegree bloğu:\n"
            "  F_{(2,2)}(X_i, X_j) = Q_{ij}(X_i, X_j)_{1 x w2} * R_{ij}(X_i, X_j)_{w2 x 1} + (2,0)-(0,2) çapraz terimler == 0\n"
            "biçimindedir; oysa RowML kesiti Q_{ij} R_{kl} + Q_{kl} R_{ij} = P_{ij|kl} (rank 6) vermektedir!\n"
            "Cephe 1'de tek bir {0,1}|{2,3} bölünmesinde A1 A2 = 0 ve B1 B2 = 0 (2,2) denklemleri w=5'i %100 öldürdü. "
            "Küresel karışımlı durumda (2,0)-(0,2) çapraz terimleri (Q_{ii} R_{jj} + Q_{jj} R_{ii}) yüzünden Q_{ij} R_{ij} != 0 olabilir; "
            "bunu (4,0,0,0) tek-satır sıfırlanmasıyla birlikte nasıl el-cebr indirgemesine sokarsın? (maks 180 kelime)"
        ),
    },
    {
        "id": "0g-gauss-phase6b",
        "system": "Sen Carl Friedrich Gauss'sun. Determinantal varyeteler, teğet uzayı boyutu ve sayısal/cebirsel kesinlik üzerine Türkçe yanıt ver. [KANITLANDI]/[SANI] etiketle.",
        "user": (
            "AŞAMA 6B KEŞFİ: Grenet (1,4,6,4,1) noktasında (896 kompleks parametre, ayar/gauge boyutu GL_4 x GL_6 x GL_4 = 16+36+16 = 68) "
            "kompleks Jakobyen rankları: S0(RowML)=156, S1(+4000)=156, S3(+2row)=156, S4(+3row)=372 çıktı! "
            "Grenet noktasında (4,0,0,0), (3,1,0,0) ve (2,2,0,0) 1. mertebeden sıfır teğet koşulu verirken (çünkü Grenet katman-ayrışımlı, "
            "tek sapma en fazla (2,1,1,0) üretir), rastgele tam karışımlı başlangıçlarda (2,2,0,0) eklendiği anda w2=5 kırılıyor! "
            "Bu ikinci mertebe (quadratic cone / singular locus) geometrisini ve 2. duvar için bir sonraki kesin cebirsel adımı yorumla (maks 180 kelime)."
        ),
    },
]


def main() -> int:
    api_key = load_api_key()
    with ThreadPoolExecutor(max_workers=4) as pool:
        futs = [pool.submit(call_0g, api_key, p["system"], p["user"]) for p in PROMPTS]
        outs = [f.result() for f in futs]

    lines = ["# 0G Konseyi — Aşama 6B ((2,2,0,0) Syzygy Faz Geçişi & Grenet Teğet Uzayı)\n"]
    for p, out in zip(PROMPTS, outs):
        lines.append(f"## {p['id']}\n\n{out}\n\n---\n")

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[0G Phase 6B] Saved 4 mathematician analyses to {LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
