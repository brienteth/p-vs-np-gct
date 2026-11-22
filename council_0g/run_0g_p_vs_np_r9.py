"""0G Council Round 9: Synthesizing the Core P != NP & Cryptography-Compatible Non-Natural Hypothesis."""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
LOG_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_P_VS_NP_R9.md"
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


DATA_TABLE = (
    "TUR 9 — 65,536 İKİLİ MATRİS ({0,1}^16) ÜZERİNDE KESİN BOOLEAN RÖNTGENİ (verify_p_vs_np_wall2_lab.py):\n"
    "- perm4_mod2 [=det4_mod2] (P)  : deg_F2= 4, ANF#=   24, I(f)=5.250, ||f^||1=165.88, W<=4=0.435, Fourier_Levels=  4\n"
    "- det4 != 0 mod 3         (P)  : deg_F2=12, ANF#= 2832, I(f)=4.699, ||f^||1=150.25, W<=4=0.518, Fourier_Levels= 18\n"
    "- perm4 > 0 [Matching]    (P)  : deg_F2=16, ANF#= 7443, I(f)=2.407, ||f^||1= 75.84, W<=4=0.880, Fourier_Levels= 48\n"
    "- perm4 != 0 mod 3   (Mod3P!)  : deg_F2=15, ANF#= 5002, I(f)=4.708, ||f^||1=144.11, W<=4=0.531, Fourier_Levels= 70\n"
    "- Random (matched bias) (Ctrl) : deg_F2=15, ANF#=32731, I(f)=7.989, ||f^||1=203.90, W<=4=0.040, Fourier_Levels=249\n"
    "KRİTİK BULGU: Toplam etki I(f), spektral L_1 normu ve F_2-ANF derecesinde P fonksiyonları Mod3P-zor perm4_mod3'ü GEÇİYOR! "
    "Fakat perm4_mod3, hem det4_mod3'ten 3.9 kat daha parçalı (Levels: 70 vs 18; deg_F2: 15 vs 12) hem de Random'dan çok daha simetrik (Levels: 70 vs 249, W<=4: 0.531 vs 0.040)!\n"
)

PROMPTS: List[Dict[str, str]] = [
    {
        "id": "0g-harezmi-pvsnp",
        "system": "Sen Harezmi'sin. Algoritmik karmaşıklık, kriptografi (tek yönlü fonksiyonlar) ve P != NP üzerine Türkçe, net ve dürüst yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            DATA_TABLE + "\n"
            "HEDEF: P = NP çıkarsa modern kriptografi çöker; P != NP'yi kanıtlamak ise Razborov-Rudich Doğal Kanıt Bariyeri nedeniyle "
            "kriptografinin varlığıyla ÇELİŞMEYEN (doğal olmayan) bir hipotez gerektirir! "
            "Yukarıdaki 'Ara-Simetri Bandı' (Goldilocks Band: P'den daha parçalı ama Random'dan çok daha simetrik) keşfinden ve "
            "Ryan Williams'ın 'algoritmik ikilik' (Circuit-SAT -> alt sınır) ilkesinden hareketle, P != NP için en güçlü çekirdek hipotezi öner (maks 180 kelime)."
        ),
    },
    {
        "id": "0g-gauss-pvsnp",
        "system": "Sen Carl Friedrich Gauss'sun. Sayılar kuramı, F_2/F_3 modüler ayrımı ve kriptografik zorluk üzerine Türkçe ve dürüst yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            DATA_TABLE + "\n"
            "HEDEF: perm_4 mod 2 (P, 4 Fourier seviyesi, deg_F2=4) ile perm_4 mod 3 (Mod3P-zor, 70 seviye, deg_F2=15) arasındaki "
            "uçurum tam olarak karakteristik 2 -> 3 geçişinde (işaret iptalinin kırılmasıyla!) patlıyor; buna karşılık det_4 mod 3 (P) "
            "GL_4(F_3) simetrisiyle sadece 18 seviyede ve deg_F2=12'de kalıyor! "
            "Sayılar kuramı ve cebirsel geometri gözüyle, bu F_2 -> F_3 geçişini P != NP ve kriptografik tek-yönlülüğe kilitleyecek "
            "en keskin matematiksel hipotezi formüle et (maks 180 kelime)."
        ),
    },
    {
        "id": "0g-oklid-pvsnp",
        "system": "Sen Öklid'sin. Aksiyomatik bariyerler (Relativization, Algebrization, Natural Proofs) ve P != NP yol haritası üzerine Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            DATA_TABLE + "\n"
            "HEDEF: P != NP kanıtının geçmesi gereken 3 ünlü bariyer var: (1) Relativization, (2) Algebrization, (3) Razborov-Rudich Doğal Kanıtlar. "
            "Verimiz tek bakışta gösterdi ki I(f), L_1 normu, ANF derecesi gibi klasik Boolean ölçümler hem P tarafından geçiliyor hem Doğal Kanıt tuzağına düşüyor. "
            "Üç bariyeri birden aşabilecek (Non-Relativizing, Non-Algebrizing, Non-Natural) tek bir aksiyomatik P != NP çalışma hipotezi nasıl kurulmalıdır? (maks 180 kelime)."
        ),
    },
]


def main() -> int:
    api_key = load_api_key()
    with ThreadPoolExecutor(max_workers=3) as pool:
        futs = [pool.submit(call_0g, api_key, p["system"], p["user"]) for p in PROMPTS]
        outs = [f.result() for f in futs]

    lines = ["# 0G Konseyi — Tur 9 (P ≠ NP, Kriptografi & Ara-Simetri Bandı Çekirdek Hipotezi)\n"]
    for p, out in zip(PROMPTS, outs):
        lines.append(f"## {p['id']}\n\n{out}\n\n---\n")

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[0G Round 9 P!=NP] Saved 3 analyses to {LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
