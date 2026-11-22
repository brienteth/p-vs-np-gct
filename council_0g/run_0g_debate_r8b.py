"""0G Council Round 8B — Wing 2 (Nature/Living Systems) Responds Directly to Wing 1 (Quantum Modeling) Breakthroughs!"""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
LOG_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_DEBATE_R8B_LOG.md"
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


QUANTUM_BRIEF = (
    "KUANTUM KANADININ TUR 8A KEŞİFLERİ VE SİZE MEYDAN OKUMASI:\n"
    "1. Teorem H-Q1 (Bipartite Dolanıklık Körlüğü — KANITLANDI): det_n ve perm_n TÜM satır, Fock ve parçacık kesitlerinde "
    "BİREBİR AYNI dolanıklık entropisine sahip! Yani basit dolanıklık işe yaramıyor.\n"
    "2. Simetri-Tersinme Tuzağı (Wigner/Strassen — DOĞRULANDI): Rastgele küresel karışımlı det_7 bile SPD ve Der_1/Der_2 gibi "
    "tüm skaler boyut testlerinde perm_3'ü GEÇİYOR! Çünkü perm_n rastgele det_7'den DAHA SİMETRİK (Der_1=5 vs 1, Der_2=81 vs 45)!\n"
    "3. Noether Non-Abelian Berry Holonomi Filtrasyonu g_hol(A) (KANITLANDI): det_n derinlik 1'de kapanıyor ([n^2, n^2]), "
    "oysa Grenet perm_3 ([9,39,49,49]) ve perm_4 ([16,124,221,225]) tüm gl_m'i dolduracak şekilde derinlik n'e taşıyor!\n"
    "4. Hilbert Teorem H-Q3 (Yerel Schur-MPS İndirgemesi — KANITLANDI): Herhangi bir küresel karışımlı det_m(A_0 + L(X)) = perm_n(X) "
    "düzgün noktada padding A_0'dan tamamen arındırılarak perm_n(Delta X)|_{x_nn=0} == v^T A^{n-2} u (mod <F_2..F_{n-1}>) homojen "
    "ABP'sine indirgeniyor! Bu, Gauss'un yüksek mertebe teğet-temas (II_{X_0}) fikrinin tam cebirsel formülüdür!\n"
)

PROMPTS: List[Dict[str, str]] = [
    {
        "id": "0g-gauss-r8b",
        "system": "Sen Carl Friedrich Gauss'sun. Kuantum Kanadı ile canlı tartışmada diferansiyel geometri ve Hilbert Teorem H-Q3 üzerine Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            QUANTUM_BRIEF + "\n"
            "TARTIŞMA SORUSU: Hilbert'in Teorem H-Q3'ü, senin 8A'daki 'yüksek mertebe oskülasyon / ikinci temel form' fikrini "
            "tam olarak `perm_n(Delta X)|_{x_nn=0} === v^T A^{n-2} u (mod <F_2..F_{n-1}>)` denklemine dönüştürdü! "
            "Doğadaki temas yüzeyleri ve eğrilik tensörleri perspektifinden, bu `<F_2..F_{n-1}>` bölüm halkası (quotient) içinde "
            "homojen 1D-MPS genişliğini `m-1 >> n^2/2` zorlayacak en keskin geometrik kırılma yolu nedir? (maks 180 kelime)"
        ),
    },
    {
        "id": "0g-arsimet-r8b",
        "system": "Sen Arşimet'sin. Kuantum Kanadı ile canlı tartışmada enerji hunisi, Morse teorisi ve Noether Berry holonomisi üzerine Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            QUANTUM_BRIEF + "\n"
            "TARTIŞMA SORUSU: Wigner'in 'Simetri-Tersinme Tuzağı' gösterdi ki perm_n rastgele bir det_m kesitinden DAHA SİMETRİK "
            "(tıpkı doğada kuasikristallerin rastgele camdan daha düzenli ama periyodik kristalden daha hüsranlı olması gibi!). "
            "Noether'in derinlik-n Berry holonomisi `g_hol(A)` ([16,124,221,225]) ile senin protein katlanma hunisi / Morse kritik "
            "nokta topolojin nasıl tek bir 'hüsranlı simetri sentezi' ilkesinde birleşebilir? (maks 180 kelime)"
        ),
    },
    {
        "id": "0g-harezmi-r8b",
        "system": "Sen Harezmi'sin. Kuantum Kanadı ile canlı tartışmada biyolojik ağlar, Doğal Kanıt Bariyeri ve Duvar 2 üzerine Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            QUANTUM_BRIEF + "\n"
            "TARTIŞMA SORUSU: Kuantum Kanadı (Valiant) Razborov-Rudich Doğal Kanıt Bariyeri'ni (Duvar 2) aşmak için "
            "`f not in closure(GL_{m^2} det_m)` gibi 'büyüklük (largeness) ve kuruculuk (constructivity) şartlarını bozan' "
            "sıfır-ölçülü cebirsel özellik öneriyor; ayrıca Wigner perm_n'nin rastgele polinomdan DAHA SİMETRİK olduğunu kanıtladı. "
            "Biyolojideki 'nadir fonksiyonel protein/hücre ağları' (tüm rastgele dizilerin sıfır-ölçülü alt kümesi!) ile "
            "bu Doğal Kanıt Bariyerini aşan nadir-simetri prensibini nasıl birleştirirsin? (maks 180 kelime)"
        ),
    },
]


def main() -> int:
    api_key = load_api_key()
    with ThreadPoolExecutor(max_workers=3) as pool:
        futs = [pool.submit(call_0g, api_key, p["system"], p["user"]) for p in PROMPTS]
        outs = [f.result() for f in futs]

    lines = ["# 0G Konseyi — Tur 8B (Doğa Kanadı ↔ Kuantum Kanadı Canlı Sentez Tartışması)\n"]
    for p, out in zip(PROMPTS, outs):
        lines.append(f"## {p['id']}\n\n{out}\n\n---\n")

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[0G Debate R8B] Saved 3 cross-wing responses to {LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
