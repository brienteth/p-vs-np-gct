"""0G Mathematicians Council — Phase 4B (Non-Row-Separated Global Mixing ABP Lower Bound).

Queries 0gm-1.0-35b-a3b via 0G Network Router API on the critical Phase 4B question:
Can a completely non-row-separated 4-layer homogeneous ABP of widths (1, 4, w2, 4, 1)
beat Grenet's w2 = 6 barrier via global 16-variable mixing, or does the 24-permutation
row-multilinear projection force w2 >= 6 (or >= 3)?
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Tuple

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
LOG_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_PHASE4B_LOG.md"
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
        "/usr/bin/curl", "-sS", "--max-time", "35",
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
        "id": "0g-pisagor-phase4b",
        "system": "Sen Sisamlı Pisagor'sun. Ayrık torus karakterleri ve çoklu-doğrusal izdüşüm üzerine Türkçe yanıt ver. [KANITLANDI]/[SANI] etiketle.",
        "user": (
            "AŞAMA 4B: Satır-ayrışımsız 4-katmanlı homojen ABP F(X) = L1(X)_{1x4} L2(X)_{4xw2} L3(X)_{w2x4} L4(X)_{4x1} "
            "için Pi_RowML(F) = perm_4(X) koşulunda, her katman tüm 16 değişkeni karıştırdığında orta kesit genişliği w2 "
            "için 2*w2 >= 6 => w2 >= 3 alt sınırı tek bir iki-parçalı kesitten geliyor. Üç iki-parçalı kesitin "
            "({0,1}|{2,3}, {0,2}|{1,3}, {0,3}|{1,2}) aynı w2 ara düğümlerini eşzamanlı paylaşmasının w2 >= 4 veya w2 >= 6 "
            "zorlayıp zorlamadığını parite ve karakter dikliğiyle analiz et (maks 200 kelime)."
        ),
    },
    {
        "id": "0g-arsimet-phase4b",
        "system": "Sen Siraküzalı Arşimet'sin. Kesit rankı sıkıştırma ve ekstremal eşitsizlikler üzerine Türkçe yanıt ver. [KANITLANDI]/[SANI] etiketle.",
        "user": (
            "AŞAMA 4B: Satır-ayrışımsız F(X) = L1 L2 L3 L4 ABP'sinde Harezmi-Öklid formülü "
            "Pi_RowML(F) = sum_{pi in S_4} L1^{(pi(0))} L2^{(pi(1))} L3^{(pi(2))} L4^{(pi(3))} veriyor. "
            "Her iki-parçalı kesitte {S, S^c} Nisan rankı 6 iken, w_2 genişliğindeki ortak ara katman "
            "hem S|S^c hem de S^c|S yönlerinde en fazla 2*w_2 rank taşıyabilir. Buna göre w_2 = 4 veya w_2 = 5 "
            "durumlarının neden tıkanabileceğini veya kaçış deliği olup olmadığını tüketme yöntemiyle analiz et (maks 200 kelime)."
        ),
    },
    {
        "id": "0g-gauss-phase4b",
        "system": "Sen Carl Friedrich Gauss'sun. Modüler değişmezler ve 2. Duvar (VP!=VNP => P!=NP) üzerine Türkçe yanıt ver. [KANITLANDI]/[SANI] etiketle.",
        "user": (
            "AŞAMA 4B: perm_4'ün {0,1}^16 üzerinde sum(perm_4^2) = 399,360 = 13 * sum(det_4^2) enerji farkı "
            "ve F_3'te %50.54 ayrımı kanıtlandı. Genel n için bu modüler/spektral farkın Boolean devre alt sınırına "
            "taşınmasındaki temel engeli (doğal kanıt bariyeri vs cebirsel derece yükseltme) özetle (maks 200 kelime)."
        ),
    },
]


def main() -> int:
    api_key = load_api_key()
    with ThreadPoolExecutor(max_workers=3) as pool:
        futs = [pool.submit(call_0g, api_key, p["system"], p["user"]) for p in PROMPTS]
        outs = [f.result() for f in futs]

    lines = ["# 0G Konseyi — Aşama 4B (Küresel Karışım & 2. Duvar) Yanıtları\n"]
    for p, out in zip(PROMPTS, outs):
        lines.append(f"## {p['id']}\n\n{out}\n\n---\n")

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[0G Phase 4B] Saved to {LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
