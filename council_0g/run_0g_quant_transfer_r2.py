"""
Nicel Aktarım Teoremi — Tur 2 (0G Kolu Yükseltilmiş Çözümler):
@critic (#164) ve @moderator (#165) denetimleri ile Swarm Tur 1 (#157-#162)
bulguları ışığında tüm hataların düzeltilmesi ve formal lemma / imkânsızlık inşası.
"""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
OUT_MD = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_QUANT_TRANSFER_R2.md"
API_URL = "https://router-api.0g.ai/v1/chat/completions"
MODEL = "0gm-1.0-35b-a3b"


def load_key() -> str:
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("0G_API_KEY="):
                return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("0G_API_KEY not found")


SHARED_RULES = (
    "Sadece doğrudan, teknik, hakem düzeyinde Türkçe yanıt ver; asla İngilizce düşünce taslağı veya şişirme yazma. "
    "Eleştirmenin (#164) ve Moderatörün (#165) tespit ettiği hatalarını açıkça kabul edip düzelt; kesin parametrelerle formal bir lemma "
    "veya imkânsızlık sınırı kur. En sonunda 'REVİZE TEOREM / İMKÂNSIZLIK:' başlığıyla kapanış hükmünü yaz. (<=180 kelime)"
)

PROMPTS = [
    (
        "0g-pisagor (Tur 2 — İndirgeme Değişmezleri & H4 Nicellemesi)",
        "Sen Pisagor'sun. " + SHARED_RULES,
        "TUR 1 DENETİMİ (#164-#165):\n"
        "- Eleştirmen: CNF için deg(phi_n)=deg(f_n) tanımsızdır; parsimonyen indirgeme yalnız #P/Mod_pP bağlar; Toda (PH ⊆ P^#P) terstir, "
        "SAT kesin sayım vermez (Stockmeyer BPP^NP yalnızca yaklaşık sayar).\n"
        "- Moderatör direktifi: Hatalı ifadeleri geri çek ve H4 (SAT-indirgenebilirlik) koşulunu kesin parametrelerle kur: "
        "q(n) <= n^a adet, boyut <= m(n) <= n^c olan SAT çağrısı, ek devre boyutu S_R(n)=poly(n), derinlik D_R(n) ve adaptif tur r_d(n).\n"
        "GÖREV: H4 altında toplam Boolean devresi (S_tot, D_tot) için kesin kayıp formülünü ver ve #P-tamlık tek başına neden SAT alt sınırı veremez net kanıtla."
    ),
    (
        "0g-oklid (Tur 2 — Alan Değişimi C ↔ Z ↔ F_p & GRH Asal Sınırı)",
        "Sen Öklid'sin. " + SHARED_RULES,
        "TUR 1 DENETİMİ (#164-#165):\n"
        "- Eleştirmen: AC_{F_p}(f_n mod p) >= AC_C(f_n) - O(log H) formülün YANLIŞTI (mod-p karmaşıklığı düşürebilir, ör. p=2); "
        "GRH asal sınırı p <= O(log^2 n) değil log p <= poly(n)'dir; çok-değişkenli disc(f_n) tanımsızdır.\n"
        "- Swarm (#159, #161) + Moderatör: Boolean -> C karşıt-olumlu yönünde f_n in Z[X] bit-toplaması (sum 2^j b_j, Z ↪ C) GRH GEREKTİRMEZ! "
        "GRH yalnız ters yöndeki (Bürgisser 2000 / Koiran: C -> F_p sabit eleme) adımında log p <= poly(n) garantisi için gerekir.\n"
        "GÖREV: Hatalı eşitsizliği geri çek; F=C (GRH'siz bit-toplama) ile F=F_p (p>=3, CRT L(n)=poly(n) bit) arasındaki kesin alan geçiş lemmasını yaz."
    ),
    (
        "0g-arsimet (Tur 2 — I_B Multilinearizasyon, 2^{D_B} & FKS16 Fonksiyonel Şart)",
        "Sen Arşimet'sin. " + SHARED_RULES,
        "TUR 1 DENETİMİ (#164-#165):\n"
        "- Eleştirmen: Her kapı çıktısında I_B=<x_i^2-x_i> modülo çok-doğrusal normalizasyon devre boyutunu KORUMAZ (üstel patlama yaratır!). "
        "Ayrıca Swarm'a (#157/#160) da dikkat: D_B = O(log n) (NC^1) rejiminde dahi C_n(x) ≡ f_n(x) (mod I_B) olduğu için salt biçimsel AC(f_n) yetmez; derece-kısıtlı fonksiyonel alt sınır şarttır!\n"
        "- Moderatör direktifi: Kapı-başı ML iddiasını geri çek, Forbes–Kumar–Saptharishi (2016) anlamında AC_func(f_n) := min_{g ≡ f_n mod I_B} AC(g) tanımını kullan.\n"
        "GÖREV: (S_B, D_B) -> aritmetikleştirme boyut O(S_B) ve biçimsel derece <= 2^{D_B} geçişiyle, neden genel D_B=poly(n) için derece-serbest AC_func, D_B=O(log n) için ise derece <= poly(n) kısıtlı AC_func gerektiğini formülleştir."
    ),
    (
        "0g-gauss (Tur 2 — Nicel Eşikler & Doğru Yönlü Yayılım Bütçesi)",
        "Sen Gauss'sun. " + SHARED_RULES,
        "TUR 1 DENETİMİ (#164-#165):\n"
        "- Eleştirmen: Tur 1'de yönü ters kurdun! |C_n| <= S_arith poly(log p) Boolean <- Aritmetik yönüdür; S_arith alt sınırından |C_n| alt sınırı çıkmaz. "
        "Ayrıca Swarm (#160) D_B > eps log_2 n eşiği de yanlıştı (2^{eps log_2 n} = n^eps polinomsaldır!).\n"
        "- Doğru karşıt-olumlu yön: SAT_m devresi (S_B(m), D_B(m)) + H4 (q(n)<=n^a, m(n)<=n^c, S_R, D_R, r_d) => toplam Boolean devresi (S_tot, D_tot) "
        "=> I_B modülo aritmetik devre (boyut O(S_tot + L), derece <= 2^{D_tot}).\n"
        "GÖREV: AC_func >= 2^{n^eps} bilindiğinde S_B(m) >= 2^{Omega(m^{eps/c})} sonucunun hangi c, q, D_tot rejimlerinde korunduğunu, ne zaman sadece NC^1 ile kaldığını ve nerede çöktüğünü doğru yönde ispatla."
    ),
    (
        "0g-harezmi (Tur 2 — Bariyer Uyumu: Birleşik Kanıt & Non-Algebrizing / Non-Natural)",
        "Sen Harezmi'sin. " + SHARED_RULES,
        "TUR 1 DENETİMİ (#164-#165):\n"
        "- Eleştirmen: 'R'nin doğruluğu NEXP ⊄ P/poly varsayımına dayanır' iddian döngüseldi! Ayrıca Moderatör notu: BGS75, AW09, RR97, FSV18/GKSS17 "
        "bariyerleri aktarım teoremine tek başına değil, (H1 + H4) BİRLEŞİK KANITINA uygulanır.\n"
        "- Swarm (#158): Aktarım teoremi beyaz-kutu aritmetizasyon kullanır ama kendi başına algebrizing kalabilir; ayrıca açık tek bir f_n üzerinden aktarım RR97 'largeness'ını otomatik tetiklemez.\n"
        "GÖREV: Döngüselliği kaldır. Birleşik (H1+H4) kanıtının BGS75, AW09, RR97 ve FSV18/GKSS17 ile çelişmemesi için tam olarak hangi adımın non-relativizing / non-algebrizing / non-natural (largeness veya constructivity kırılımı) olması gerektiğini kanıtla."
    ),
    (
        "0g-ramanujan (Tur 2 — Kesin Teorem Taslağı v2 & Tam Karşı-Örnek Matrisi)",
        "Sen Ramanujan'sın. " + SHARED_RULES,
        "TUR 1 DENETİMİ (#164-#165):\n"
        "- Eleştirmen: Uydurma ML (PAC/VC) hipotezlerin, imkânsız 2^{n^eps} -> 2^{cn} üs sıçraman ve YANLIŞ 'perm_n mod 2 ∈ AC^0' iddian elendi (PARITY <=_{AC^0} det_n mod 2 ∉ AC^0; perm_n mod 2 ∈ NC^2 / ⊕L!).\n"
        "- Moderatörün Teorem Taslağı v1 (H1-H4) elinde:\n"
        "  H1: AC_F^{func}(f_n) >= 2^{n^eps}; H2: genel S_B için derece-serbest veya derece-kısıtlı için D_tot = O(log n);\n"
        "  H3: F=C (bit-toplama, GRH'siz) veya F=F_p (p>=3, log p <= poly(n)); H4: SAT-indirgeme (q<=n^a, m<=n^c, S_R=poly, D_R, r_d).\n"
        "GÖREV: Sahte PAC/VC hipotezlerini at, Teorem Taslağı v1'i sıkılaştır (özellikle AC'de bölme/sabit seçimi veya No-Go sınırları dahil) ve H1..H4'ün her biri için tek satırlık kesin karşı-örnek ver."
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
        "temperature": 0.2,
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
    lines = ["# 0G Konseyi — Nicel Aktarım Teoremi Tur 2 (Yükseltilmiş Çözümler)\n"]
    for name, text in results:
        lines.append(f"## {name}\n\n{text}\n\n---\n")
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[0G Quant Transfer R2] Saved 6 upgraded solutions to {OUT_MD}")


if __name__ == "__main__":
    main()
