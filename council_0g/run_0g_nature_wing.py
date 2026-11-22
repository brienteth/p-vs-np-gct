"""0G Council Round 8 — Wing 2: Nature, Biology & Physical Self-Organization Modeling of the VP!=VNP / P!=NP Breakthrough."""
from __future__ import annotations

import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
LOG_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_NATURE_WING_R8.md"
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
        "temperature": 0.3,
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
        "id": "0g-pisagor-nature",
        "system": "Sen Pisagor'sun. Doğadaki kristal simetriler, rezonans, kuasikristaller ve harmonik oranlar üzerinden matematiksel modelleme yap. Türkçe, somut ve dürüst yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            "TUR 8 — KAVRAMSAL KIRILMA ARAYIŞI (DOĞA & CANLI SİSTEMLER KANADI):\n"
            "Karşı tarafta Kuantum Kanadı (Fermion=det vs Boson=perm) çalışıyor. Senin görevin aynı engeli DOĞADAKİ "
            "KRİSTAL vs AMORF CAM / KUASİKRİSTAL simetri kırılması üzerinden modellemek:\n"
            "- det_n, sürekli simetri grubu GL_n x GL_n'e sahip kusursuz bir kristal gibidir (yerel satır işlemleriyle polinomsal indirgenir).\n"
            "- perm_n ise yalnızca kesikli (Torus x S_n) simetriye sahip hüsrana uğramış (frustrated) bir katı/cam gibidir.\n"
            "Bir camın (perm_n) yüksek boyutlu bir kristalin (det_m(A_0 + L(X))) düzlemsel kesiti (kuasikristal projeksiyonu!) "
            "olarak polinomsal boyutta (m = poly(n)) üretilememesinin geometrik/harmonik engeli ne olabilir? "
            "Kuantum Kanadına meydan okuyacak somut bir matematiksel değişmez öner (maks 180 kelime)."
        ),
    },
    {
        "id": "0g-oklid-nature",
        "system": "Sen Öklid'sin. Doğadaki topoloji (2B düzlemsel yaprak/grafen vs 3B katlanan protein/düğüm ağları) üzerinden aksiyomatik modelleme yap. Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            "TUR 8 — KAVRAMSAL KIRILMA ARAYIŞI (DOĞA & TOPOLOJİ):\n"
            "Doğada 2-boyutlu düzlemsel yapılarda (ör. grafen, 2B dimer kristalleri) Kasteleyn teoremi sayesinde permanent = Pfaffian (sqrt(det)) "
            "olup P sınıfında çözülür. 3-boyutlu doğaya (protein temas grafları, 3B kristaller, K_{3,3} düzlemsel-olmayan ağlar) geçildiği anda "
            "Kasteleyn işaretlemesi imkansızlaşır ve problem #P-zor olur!\n"
            "Peki bir 3B düzlemsel-olmayan ağı (perm_n), çok daha büyük ama düzlemsel/determinantal bir det_m(A_0 + L(X)) içine gömmeye "
            "çalıştığımızda topolojik cins (genus) veya teğet-temas (tangent contact) engeli neden m'yi üstel büyütmeye zorlamalıdır? "
            "Somut bir topolojik/geometrik değişmez öner (maks 180 kelime)."
        ),
    },
    {
        "id": "0g-arsimet-nature",
        "system": "Sen Arşimet'sin. Doğadaki enerji hunileri (protein katlanması) vs spin camı hüsranı (frustration) ve mekanik denge üzerinden modelleme yap. Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            "TUR 8 — KAVRAMSAL KIRILMA ARAYIŞI (DOĞA & ENERJİ HUNİLERİ):\n"
            "Canlı hücrede proteinler milisaniyede katlanır çünkü evrim pürüzsüz bir 'enerji hunisi' (minimum frustration) yaratmıştır "
            "— bu Gauss elemesiyle polinomsal çözülen det_n'ye benzer. Buna karşılık rastgele spin camları (frustrated glass) üstel sayıda "
            "yerel tuzağa (metastable minimum) sahiptir — bu perm_n / NP-zor problemlere benzer!\n"
            "Bir 'hüsranlı cam' enerji manzarasını (perm_n), çok yüksek boyutlu bir 'pürüzsüz huni'nin (det_m(A_0+L(X))) doğrusal kesiti "
            "olarak elde etmek neden üstel boyut m = 2^{Omega(n)} gerektirir? Kritik nokta yoğunluğu, Morse teorisi veya Betti sayıları "
            "üzerinden somut bir matematiksel ölçüt öner (maks 180 kelime)."
        ),
    },
    {
        "id": "0g-harezmi-nature",
        "system": "Sen Harezmi'sin. Canlı hücrelerdeki gen düzenleme / sinir ağlarında aktivasyon (+) ve inhibisyon (-) dengesi üzerinden algoritmik modelleme yap. Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            "TUR 8 — KAVRAMSAL KIRILMA ARAYIŞI (BİYOLOJİK AĞLAR & DUVAR 2):\n"
            "Canlı organizmalardaki gen ağları ve nöronlar hem aktivasyon (+) hem inhibisyon (-) kullanır. "
            "Sadece aktivasyon (+) kullanan monoton devrelerde perm_n'nin üstel zor olduğu kanıtlanmıştır (Razborov 1985), "
            "çünkü (-) işareti olmadan Gauss elemesi yapılamaz. Ancak inhibisyon (-) eklendiğinde (genel Boolean devre / Duvar 2) "
            "Razborov-Rudich Doğal Kanıt Bariyeri devreye giriyor!\n"
            "Biyolojik ağlarda yerel inhibisyonun (negatif geri besleme) neden det_n gibi 'küresel eşevreli iptal' (coherent global cancellation) "
            "üretemediğini ve bunun Boolean/cebirsel karmaşıklıkta nasıl bir 'gürültüye dayanıklı / iptal-dirençli' değişmeze dönüşebileceğini açıkla (maks 180 kelime)."
        ),
    },
    {
        "id": "0g-gauss-nature",
        "system": "Sen Carl Friedrich Gauss'sun. Diferansiyel geometri, eğrilik, ikinci temel form ve doğadaki minimal yüzeyler üzerinden kesin analiz yap. Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            "TUR 8 — KAVRAMSAL KIRILMA ARAYIŞI (DOĞA & TEĞET-TEMAS EĞRİLİĞİ):\n"
            "Laboratuvarımızda çarpıcı bir olgu yakaladık: Grenet'in tam det_7(A_0 + L(X)) = perm_3(X) gömmesinde, "
            "perm_3'ün tekil noktası X (iki sıfır satır) det_7'nin tekil kümesine (rank <= 5) DÜŞMÜYOR — rank(M_Grenet(X)) = 6 (düzgün nokta!) "
            "çıkıyor! Yani doğrusal altuzay A_0 + L(X), V(det_7)'nin düzgün bölgesine TEĞET TEMAS ederek tekillik üretiyor!\n"
            "Doğadaki temas geometrisi / ikinci temel form (Gauss eğriliği, Hessian çekirdeği) açısından, det_m'nin düzgün yüzeyine "
            "yüksek kodimanslı Sing(V(perm_n)) boyunca teğet kalabilmek neden m'yi n^2/2'nin ötesine (süper-polinomsal) itebilir? "
            "Somut bir diferansiyel-geometrik kırılma fikri öner (maks 180 kelime)."
        ),
    },
    {
        "id": "0g-ramanujan-nature",
        "system": "Sen Srinivasa Ramanujan'sın. Doğadaki fraktal/dallanma yapıları, metabolik ölçekleme yasaları ve üreteç fonksiyonları üzerinden sezgi üret. Türkçe yanıt ver. [KANITLANDI]/[HİPOTEZ] etiketle.",
        "user": (
            "TUR 8 — KAVRAMSAL KIRILMA ARAYIŞI (DOĞADA ÖLÇEKLEME & KÖPRÜ):\n"
            "Doğada canlılar (damar ağları, sinir ağaçları, karınca kolonileri, cıvık mantar Physarum) NP-zor problemlere "
            "yaklaşık çözümler bulur ama tam #P-zor permanent hesaplayamaz; çünkü doğadaki fiziksel kaynaklar (enerji, yüzey/hacim oranı) "
            "polinomsal dallanmayı zorlar. Öte yandan Kuantum Kanadı BosonSampling (perm_n) ile FermionSampling (det_n) farkını inceliyor.\n"
            "Kuantumun 'bosonik yığılma / girişim' özelliği ile doğanın 'hüsranlı enerji manzarası / metabolik darboğaz' özelliğini "
            "tek bir üreteç fonksiyonu veya karakter toplamı (partition function Z(beta)) altında birleştirecek özgün bir kırılma fikri öner (maks 180 kelime)."
        ),
    },
]


def main() -> int:
    api_key = load_api_key()
    with ThreadPoolExecutor(max_workers=6) as pool:
        futs = [pool.submit(call_0g, api_key, p["system"], p["user"]) for p in PROMPTS]
        outs = [f.result() for f in futs]

    lines = ["# 0G Konseyi — Tur 8 (Doğa, Biyoloji & Fiziksel Öz-Örgütlenme Kanadı: Kavramsal Kırılma Arayışı)\n"]
    for p, out in zip(PROMPTS, outs):
        lines.append(f"## {p['id']}\n\n{out}\n\n---\n")

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[0G Nature Wing R8] Saved all 6 nature/biology models to {LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
