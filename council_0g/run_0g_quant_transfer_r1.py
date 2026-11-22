"""
Nicel Aktarım Teoremi — Tur 1 (0G Kolu Açılış Çözümleri):
AC(f_n) >= 2^{n^eps} → Boolean devre / SAT alt sınırları aktarımı,
4 alt soru + formal koşullu teorem + karşı-örnek sınırları.
"""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
OUT_MD = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_QUANT_TRANSFER_R1.md"
API_URL = "https://router-api.0g.ai/v1/chat/completions"
MODEL = "0gm-1.0-35b-a3b"


def load_key() -> str:
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("0G_API_KEY="):
                return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("0G_API_KEY not found")


SHARED_RULES = (
    "Sadece doğrudan, teknik, hakem düzeyinde Türkçe yanıt ver; asla İngilizce düşünce taslağı veya abartı yazma. "
    "Emin olmadığın atıf/yazar yılı uydurma ve kanıtlanmamış hiçbir şeyi kanıtlanmış gibi sunma. "
    "Açık parametreler, formüller ve gerek/yeter koşullar ver. En sonunda 'TEOREM KOŞULU:' başlığıyla net tek cümlelik formal koşul veya imkânsızlık yaz. (<=180 kelime)"
)

PROMPTS = [
    (
        "0g-pisagor (Alt Soru 1: İndirgemenin Koruması Gereken Bilgiler)",
        "Sen Pisagor'sun. " + SHARED_RULES,
        "SORU: AC(f_n) >= 2^{n^eps} alt sınırından SAT Boolean devre alt sınırına geçmek için f_n -> SAT indirgemesi hangi bilgileri korumalıdır? "
        "Özellikle: karar (NP) vs sayma (#P), parsimonyen/mod-p indirgeme, promise/Valiant-Vazirani izolasyonu, ve neden düz Turing/Cook indirgemesi "
        "tek başına cebirsel zorluğu SAT'a aktarmaya yetmez (Toda PH ⊆ P^#P yönü)? En sonda 'TEOREM KOŞULU:' ekle."
    ),
    (
        "0g-oklid (Alt Soru 2: Alan Değişimi — C → Qbar → Z → F_p → F_2)",
        "Sen Öklid'sin. " + SHARED_RULES,
        "SORU: Cebirsel alt sınır F (ör. C) üzerinde AC_F(f_n) >= 2^{n^eps} ise, alan değişimi C -> Qbar -> Z -> F_p -> F_2 karmaşıklığı nasıl etkiler? "
        "Sabit eleme (transcendental katsayılar), GRH altında küçük asal bulma / CRT yeniden inşası ve char=2 çöküşü (perm_n mod 2 = det_n mod 2 ∈ NC^2) "
        "hangi nicel kayıplara veya çöküşlere yol açar? F_p -> C ve C -> F_p yönlerindeki asimetriyi formülleştir. En sonda 'TEOREM KOŞULU:' ekle."
    ),
    (
        "0g-arsimet (Alt Soru 3: Booleanlaştırma Sırasında Derece ve Boyut Dinamiği)",
        "Sen Arşimet'sin. " + SHARED_RULES,
        "SORU: Boolean devre (boyut S_B, derinlik D_B) cebirsel/aritmetik devreye dönüştürülürken (Booleanlaştırma / aritmetikleştirme): "
        "kapı-kapı dönüşüm O(S_B) boyut verirken biçimsel derece nasıl 2^{D_B} gibi patlar? I = <x_i^2 - x_i> modülo multilinearizasyon ne zaman dereceyi <= N'de tutar "
        "ama formal vs fonksiyonel alt sınır farkını (ör. Forbes–Kumar–Saptharishi 2016 fonksiyonel alt sınır ihtiyacı) yaratır? Nicel bağıntıyı yaz. En sonda 'TEOREM KOŞULU:' ekle."
    ),
    (
        "0g-gauss (Alt Soru 4a: Nicel Eşikler — AC(f_n) >= 2^{n^eps} Ne Zaman Hayatta Kalır?)",
        "Sen Gauss'sun. " + SHARED_RULES,
        "SORU: Varsayalım AC_F(f_n) >= 2^{n^eps} (veya sabit derinlikte S_arith >= 2^{n^eps}). Bu alt sınır indirgeme, alan değişimi ve Booleanlaştırma boyunca "
        "parametre kaybına uğradıktan sonra SAT Boolean devreleri için hangi koşullarda |C_n| >= 2^{n^{eps'}} veya en azından n^{omega(1)} süperpolinom olarak hayatta kalır? "
        "Hangi parametre rejiminde (ör. S_B^c üstel patlama, D_B = omega(log n) sorunu) aktarım tamamen sıfıra çöküp anlamsızlaşır? En sonda 'TEOREM KOŞULU:' ekle."
    ),
    (
        "0g-harezmi (Alt Soru 4b: Bilinen İspat Bariyerleriyle Uyum)",
        "Sen Harezmi'sin. " + SHARED_RULES,
        "SORU: Bu koşullu aktarım teoremi Relativization (BGS75), Algebrization (AW09), Boolean Natural Proofs (RR97) ve Cebirsel Doğal Kanıtlar "
        "(Forbes–Shpilka–Volk 2018 / Grochow–Kumar–Saks–Saraf 2017) bariyerleriyle çelişmeden nasıl kurulabilir? "
        "Aktarım teoreminin kendisinin relativize/algebrize olup olmaması ile girdi alt sınırının (AC(f_n) >= 2^{n^eps}) non-natural olması arasındaki mantıksal farkı netleştir. En sonda 'TEOREM KOŞULU:' ekle."
    ),
    (
        "0g-ramanujan (Sentez: Koşullu Nicel Aktarım Teoremi & En Keskin Karşı-Örnek)",
        "Sen Ramanujan'sın. " + SHARED_RULES,
        "SORU: Yukarıdaki tüm mekanizmaları tek bir formal 'Koşullu Nicel Aktarım Teoremi' taslağında birleştir: "
        "Hangi H1..H4 hipotezleri sağlanırsa AC(f_n) >= 2^{n^eps} => SAT için Boolean alt sınır çıkar? Ve her hipotez düşürüldüğünde teoremin neden bozulduğunu gösteren "
        "en keskin karşı-örneği (ör. perm_n mod 2, düşük fonksiyonel karmaşıklıklı yüksek formal polinom, P^#P vs NP) açıkça yaz. En sonda 'TEOREM KOŞULU:' ekle."
    ),
]


def query_one(item, api_key: str):
    name, sys_p, usr_p = item
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": sys_p},
            {"role": "user", "content": usr_p},
        ],
        "temperature": 0.25,
        "max_tokens": 4096,
    }
    cmd = [
        "/usr/bin/curl", "-s", "-X", "POST", API_URL,
        "-H", f"Authorization: Bearer {api_key}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload, ensure_ascii=False),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    try:
        data = json.loads(res.stdout)
        msg = data["choices"][0]["message"]
        text = (msg.get("content") or "").strip()
        if not text:
            text = (msg.get("reasoning_content") or str(data)).strip()
    except Exception as e:
        text = f"ERROR: {e} | raw={res.stdout[:300]}"
    return name, text.strip()


def main():
    api_key = load_key()
    with ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(lambda it: query_one(it, api_key), PROMPTS))
    lines = ["# 0G Konseyi — Nicel Aktarım Teoremi Tur 1 (AC(f_n) ≥ 2^{n^ε} → SAT)\n"]
    for name, text in results:
        lines.append(f"## {name}\n\n{text}\n\n---\n")
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[0G Quant Transfer R1] Saved 6 solutions to {OUT_MD}")


if __name__ == "__main__":
    main()
