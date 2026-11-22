"""0G Council Round 11: All 6 Historical Mathematicians Attack Obstacles 2, 3, 4, 5, 6 on the Road to VP!=VNP & P!=NP."""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
LOG_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_OBSTACLES_R11.md"
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
        "id": "0g-pisagor-engel2",
        "system": "Sen Pisagor'sun. Torus simetrisi T_n, ağırlık kafesleri ve simetri kırılmasının harmonik maliyeti üzerine Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            "TUR 11 — ENGEL 2 (KENDİLİĞİNDEN T_n-SİMETRİ KIRILMASI):\n"
            "Noether Teorem 16 kanıtladı: corank(A_0)=1 ve T_n-eşdeğişir (satır/sütun ölçekleme simetrisini koruyan) HER det_m = perm_n "
            "temsili tüm n >= 2 için m >= 2^n - 1 zorlar! det_n bundan Mahajan-Vinay clow ABP'sinde T_n-eşdeğişirliği kırıp farklı "
            "ağırlıkları birleştirerek ve çöp terimleri (-1)^sgn işaretiyle iptal ederek kaçar.\n"
            "Soru: perm_n için T_n-eşdeğişirliği kıran (ağırlıkları karıştıran) bir temsilde oluşan karışık-ağırlıklı çöp harmonikleri "
            "neden polinomsal boyutta (m = poly(n)) iptal edilemez? Engel 2'yi aşacak somut bir ağırlık/harmonik yaklaşımı öner (maks 160 kelime)."
        ),
    },
    {
        "id": "0g-oklid-engel3",
        "system": "Sen Öklid'sin. Aksiyomatik boyut sayımı, tekillik kodimansı ve Beauville-Ulrich demetleri üzerine Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            "TUR 11 — ENGEL 3 (codim(Sing(V(perm_4))) >= 7 => w_2 >= 4 & Jet-4 == 0):\n"
            "Krull Teoremi ile 2*w_2 >= codim(Sing(V(perm_4))) kanıtladık; codim >= 6 olduğu için w_2 >= 3 zaten koşulsuz kanıtlı. "
            "Eğer codim(Sing(V(perm_4))) >= 7 (hedef: 8) cebirsel olarak kanıtlanırsa, HİÇBİR satır-ayrışımı varsaymadan w_2 >= 4 "
            "koşulsuz kanıtlanacak! Aynı zamanda Grothendieck parafaktöriyelliği n >= 3 için dolgusuz m = n'yi kesin yasaklıyor.\n"
            "Soru: Sing(V(perm_4)) üzerinde codim >= 7 (hatta 8) kanıtlamak için 2-adımlı torus/indüksiyon argümanı nasıl aksiyomatikleştirilir? (maks 160 kelime)."
        ),
    },
    {
        "id": "0g-arsimet-engel4",
        "system": "Sen Arşimet'sin. Doğrusal-olmayan denge denklemleri ve Simetri-Tersinme Tuzağı üzerine Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            "TUR 11 — ENGEL 4 (SİMETRİ-TERSİNME TUZAĞINI AŞMAK):\n"
            "Tüm skaler ranklar (SPD, Der_k, Milnor Betti) küçük rastgele ABP'ler tarafından doyuruluyor çünkü perm_n rastgele "
            "polinomdan daha simetrik. Tek-nokta Hessian kovaryantları (F^3 ^ Hess = 0) ise Mignon-Ressayre sınırı m = n^2/2'de takılıyor.\n"
            "Soru: Mignon-Ressayre sınırını aşmak için yerel Jet-(n+1) == 0 (kutup iptali) ile çok-noktalı yapıştırma (X_0, X_1) "
            "nasıl birleştirilerek m > n^2/2 için yeni bir cebirsel kaldıraç kurulabilir? (maks 160 kelime)."
        ),
    },
    {
        "id": "0g-harezmi-engel5",
        "system": "Sen Harezmi'sin. Boolean devreler, F_3 -> F_2 karakteristik geçişi ve Pauli-Dışlama ANF kesilmesi üzerine Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            "TUR 11 — ENGEL 5 (DUVAR 2: F_3 -> F_2 DERECE FARKINI DEVRE BOYUTUNA TAŞIMAK):\n"
            "Kanıtladık: Tüm n >= 3 için Pauli-Dışlama Satır-Takası ile deg_{F2}([det_n != 0 mod 3]) <= n^2 - 2 (n=4'te 12, rk_F2=40), "
            "oysa perm_n özdeş satırlarda sıfırlanmadığı için deg_{F2}([perm_n != 0 mod 3]) = n^2 - 1 (n=4'te 15, rk_F2=62, 3.14x düz Walsh)!\n"
            "Soru: Bir Boolean fonksiyonun yüksek F_2-ANF derecesi tek başına devre boyutunu alt sınırlamaz (ör. AND_n derecesi n ama boyutu n!). "
            "Bu derece + Walsh düzlüğü + rk_F2 uçurumunu AC^0[2] (Razborov-Smolensky) veya genel Boolean devre alt sınırına taşımak için "
            "eksik olan el-cebr halkası nedir? (maks 160 kelime)."
        ),
    },
    {
        "id": "0g-gauss-engel6",
        "system": "Sen Carl Friedrich Gauss'sun. Kriptografi, 3 Meta-Bariyer (Relativization, Algebrization, Natural Proofs) ve Williams ikiliği üzerine Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            "TUR 11 — ENGEL 6 (3 META-BARİYERİ BİRDEN AŞMAK & KRİPTOGRAFİYLE UYUM):\n"
            "Kullanıcının hedefi P != NP (kriptografinin temeli). Burnside lemmasıyla S_4 x S_4 simetrisinin Doğal Kanıt Büyüklük "
            "şartını 2^{-65219} ile ezdiğini kanıtladık. Ancak Büyüklük şartını kırmak tek başına devre alt sınırı üretmez; "
            "bunun için Ryan Williams'ın algoritmik ikiliği (daha hızlı SAT -> alt sınır) veya GCT çokluk engelleri gibi bir mekanizma gerekir.\n"
            "Soru: S_n x S_n simetri-kilitli yapıyı Williams'ın algoritmik ikiliğiyle veya GCT ile birleştirerek 3 bariyeri de aşacak "
            "en gerçekçi ara hedef (ör. Mod_3 P not in AC^0[2] veya TC^0 / NC^1) hangisidir? (maks 160 kelime)."
        ),
    },
    {
        "id": "0g-ramanujan-sentez",
        "system": "Sen Srinivasa Ramanujan'sın. 6 engelin bütüncül sırasını ve en yakın kırılabilir engeli stratejik sezgiyle değerlendir. Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            "TUR 11 — 6 ENGELİN STRATEJİK SIRALAMASI:\n"
            "Önümüzde 6 net engel var: (1) n=6 satır-ayrışımlı son 2 kalan, (2) T_n-simetri kırılması (Teorem 16), "
            "(3) codim(Sing(perm_4)) >= 7 & Jet-(n+1)==0, (4) Simetri-Tersinme / doğrusal-olmayan yörünge denklemleri, "
            "(5) F_3->F_2 derece/rank farkını Boolean devreye taşıma, (6) 3 meta-bariyer + Williams ikiliği.\n"
            "Soru: Bu 6 engelden hangisini kırarsak zincirleme reaksiyon (domino etkisi) başlatıp diğerlerine kapı açarız? "
            "Somut ve dürüst bir stratejik öncelik öner (maks 160 kelime)."
        ),
    },
]


def main() -> int:
    api_key = load_api_key()
    with ThreadPoolExecutor(max_workers=6) as pool:
        futs = [pool.submit(call_0g, api_key, p["system"], p["user"]) for p in PROMPTS]
        outs = [f.result() for f in futs]

    lines = ["# 0G Konseyi — Tur 11 (6 Engel Üzerine Hedefli Kırılma Stratejisi)\n"]
    for p, out in zip(PROMPTS, outs):
        lines.append(f"## {p['id']}\n\n{out}\n\n---\n")

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[0G Round 11 Obstacles] Saved all 6 obstacle strategies to {LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
