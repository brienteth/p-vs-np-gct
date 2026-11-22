"""0G Council Phase 5B: Non-Row-Separated 4-Layer ABP Exact Lower Bound & General Wall 2 Bridge."""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
LOG_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_PHASE5B_LOG.md"
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
        "id": "0g-harezmi-phase5b",
        "system": "Sen Harezmi'sin. El-Cebr ve cebirsel indirgeme üzerine Türkçe yanıt ver. [KANITLANDI]/[SANI] etiketle.",
        "user": (
            "AŞAMA 5B: Satır-ayrışımsız 4-katmanlı ABP'de Pi_RowML(L1 L2 L3 L4) = perm_4(X) için "
            "her {S, S^c} satır-çifti kesitinde Q_S(X_S)_{1xw2} R_{S^c}(X_{S^c})_{w2x1} + Q_{S^c} R_S = P_{S|S^c} "
            "denklemi geçerlidir. Q_S(X_S) = L1^{(i)}(X_i) L2^{(j)}(X_j) + L1^{(j)}(X_j) L2^{(i)}(X_i) yapısında "
            "L1 tek değişken katmanları sabit w1=4 boyutundaysa, w2 = 3 için 3 kesiti birden sağlayan çözüm "
            "neden mümkün olamaz (veya özel bir w2=3/4/5 kaçış yolu var mı)? (maks 180 kelime)"
        ),
    },
    {
        "id": "0g-ramanujan-phase5b",
        "system": "Sen Srinivasa Ramanujan'sın. Üreteç fonksiyonları ve kombinatorik özdeşlikler üzerine Türkçe yanıt ver. [KANITLANDI]/[SANI] etiketle.",
        "user": (
            "AŞAMA 5B: Satır-ayrışımsız küresel karışımlı 4-katmanlı ABP'de 6 farklı satır çifti Q_{01}, Q_{02}, Q_{03}, "
            "Q_{12}, Q_{13}, Q_{23} aynı w1=4 ilk katman çıkışından ve aynı w2 orta katmandan geçiyor. "
            "Eğer L1(X) = [L1^{(0)}(X_0), ..., L1^{(3)}(X_3)] her satırı ayrı düğümlere yönlendirseydi Grenet w2=6 zorunlu olurdu; "
            "satırların karıştırıldığı durumda w2'nin düşebileceği en küçük kuramsal değeri (3 <= w2 <= 6) ve MacMahon/Nisan "
            "rankı dengesini değerlendir (maks 180 kelime)."
        ),
    },
]


def main() -> int:
    api_key = load_api_key()
    with ThreadPoolExecutor(max_workers=2) as pool:
        futs = [pool.submit(call_0g, api_key, p["system"], p["user"]) for p in PROMPTS]
        outs = [f.result() for f in futs]

    lines = ["# 0G Konseyi — Aşama 5B (Pi_RowML & Küresel Karışım w2 Alt Sınırı)\n"]
    for p, out in zip(PROMPTS, outs):
        lines.append(f"## {p['id']}\n\n{out}\n\n---\n")

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[0G Phase 5B] Saved to {LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
