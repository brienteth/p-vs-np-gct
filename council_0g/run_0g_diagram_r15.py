"""
Round 15 — 0G Historical Mathematicians Council Runner for ENGEL_HARITASI.md Active Sub-Obstacles:
  - 0g-pisagor:   Node E2.5 (n=5 Middle-Layer Hypergraph Handshaking m>=31 & Bilateral T_n Laurent Bath Cost)
  - 0g-oklid:     Node E3.8 (Symbolic 1,296-Monomial (1,1) w_2=4 Proof, Sing(perm_4) Deg-60 Completeness & Sing_2(perm_5) D=6)
  - 0g-arsimet:   Node E3.9 (Global Degree-6 H_{<=4} Ideal & Perturbed Skew-Square for m=11,12 => dc(perm_4) >= 12..13)
  - 0g-gauss:     Node E4.5 (Explicit Polynomial Border Invariant R_{10}^{(4)}(F) & perm_5 Border Scaling)
  - 0g-harezmi:   Node E5.5 (Asymptotic 2-Adic [det_n mod 2^k != 0] vs Wood Limit & Universal Balanced-Cut rk_F2 NOF Lifting)
  - 0g-ramanujan: Node E6.5 (Exact D_PTF(n=5) >= 7..9 on K_5=5,624 Orbits & Coupled THR o THR Intra-Orbit Variance Bound)
"""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
OUT_MD = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_DIAGRAM_R15.md"
API_URL = "https://router-api.0g.ai/v1/chat/completions"
MODEL = "0gm-1.0-35b-a3b"


def load_key() -> str:
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("0G_API_KEY="):
                return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("0G_API_KEY not found")


PROMPTS = [
    (
        "0g-pisagor-E2.5",
        "Sen Pisagor'sun. Sadece doğrudan Türkçe teknik yanıt ver (İngilizce düşünce metni yazma). "
        "Sonunda 'YENİ ALT-ENGEL:' başlığıyla E2.6 öner ve [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 15 — DÜĞÜM E2.5 (n=5 Orta-Katman Hiperçizge Handshaking m>=31 & Çift-Taraflı Laurent Banyosu): "
        "n=5 T_5^row-eşdeğişir 5-katmanlı ABP'de w_1=w_4=5 iki yönlü Handshaking (str(perm_4)=4) ile w_2, w_3 >= 10 => m >= 31 = 2^5-1 verir. "
        "w_1 >= 6 olduğunda (2,1,1,1,1) satır bölünmesindeki 4 tekil satır hiperçizge Handshaking'i m <= 30 profillerini nasıl eler? "
        "Ayrıca çift-taraflı T_n kırılmasında oluşan k_r k_c - 1 farklı Laurent t-kutbunu iptal eden en küçük Schur-banyosu rank sınırı ve doğan E2.6 alt-engeli nedir? (<=130 kelime)"
    ),
    (
        "0g-oklid-E3.8",
        "Sen Öklid'sin. Sadece doğrudan Türkçe teknik yanıt ver (İngilizce düşünce metni yazma). "
        "Sonunda 'YENİ ALT-ENGEL:' başlığıyla E3.10 öner ve [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 15 — DÜĞÜM E3.8 (1,296-Monom (1,1) w_2=4 Sembolik İspatı, Sing(perm_4) Deg-60 Tamlığı & Sing_2(perm_5) D=6): "
        "Tur 14'te 1,296 bidegree-(2,2) monomunda (1,1) w_2=4 taban hatası rel_err=0.7119 çıktı; apolarite/kofaktör rankıyla bunu %100 sembolik imkânsızlığa nasıl çeviririz? "
        "Ayrıca Sing(V(perm_4)) içindeki 6 R_{ij} + 6 C_{ab} + 16 RC_{i,a} bileşenlerinin derece toplamı 6*1 + 6*1 + 16*3 = 60 ile L_9 Hilbert fonksiyonu tam eşleşirse gizli codim-8 bileşen olmadığı kanıtlanır mı? Sing_2(perm_5) k=14,15 ve doğan E3.10 nedir? (<=130 kelime)"
    ),
    (
        "0g-arsimet-E3.9",
        "Sen Arşimet'sin. Sadece doğrudan Türkçe teknik yanıt ver (İngilizce düşünce metni yazma). "
        "Sonunda 'YENİ ALT-ENGEL:' başlığıyla E3.11 öner ve [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 15 — DÜĞÜM E3.9 (Global Derece-6 H_{<=4} İdeali & m=11,12 İçin Bozulmuş Çarpık-Kare => dc(perm_4)>=12..13): "
        "Strassen Teorem 15B W^perp <= H_{<=2(w-D)} verir. Küresel olarak B_{r1r2}, C_{c1c2} ve C_{i,a} 3x3 minörleri H_{<=4}(perm_4) üzerinde 0'dır (derece 6!). "
        "L_9/L_10 üzerinde codim(H_{<=4}) >= 9..10 ve codim(H_{<=6}) >= 9 sertifikalandığında, m=11,12 için orijin korankları r=2,3 nasıl kesin elenerek koşulsuz dc(perm_4) >= 12..13 elde edilir? Doğan E3.11 alt-engeli nedir? (<=130 kelime)"
    ),
    (
        "0g-gauss-E4.5",
        "Sen Gauss'sun. Sadece doğrudan Türkçe teknik yanıt ver (İngilizce düşünce metni yazma). "
        "Sonunda 'YENİ ALT-ENGEL:' başlığıyla E4.6 öner ve [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 15 — DÜĞÜM E4.5 (Açık Polinom Sınır İnvaryantı R_{10}^{(4)}(F) = P^{(4)}(F)*S^{(4)}(F) & perm_5 Ölçeklemesi): "
        "b^4'ten dördüncü kök almadan, tamamen F katsayılarında POLİNOMSAL kalmak için L_{10} üzerinde nabla(F) (deg_F=1, deg_X=3) ve Hess(F)'in 3x3 / yapılandırılmış minörlerinden (deg_F=3, deg_X=6) Macaulay determinantı S^{(4)}(F) nasıl kurulur? "
        "R_{10}^{(4)} = P^{(4)}*S^{(4)} neden Zariski bar(D_{10}^hom)'da 0 kalırken perm_4'te sıfırdan farklı olur, perm_5 için dc alt sınırı ve doğan E4.6 nedir? (<=130 kelime)"
    ),
    (
        "0g-harezmi-E5.5",
        "Sen Harezmi'sin. Sadece doğrudan Türkçe teknik yanıt ver (İngilizce düşünce metni yazma). "
        "Sonunda 'YENİ ALT-ENGEL:' başlığıyla E5.6 öner ve [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 15 — DÜĞÜM E5.5 (Asimptotik 2-Adik [det_n mod 2^k != 0] vs Wood Limiti & Evrensel Dengeli Kesit rk_F2): "
        "[det_n mod 4 != 0] n=4'te %0.183, n=5'te %1.122 hata verirken; |det_n| büyüdükçe n=6..10'da bu sıkışma sürer mi yoksa Wood'un Pr[3|det_n] -> 0.439874 sınırına mı doyar? "
        "Öte yandan minimax altında çökmeyen rk_F2 (129 vs 92) tüm dengeli S_4xS_4 8-8 kesitlerinde det_4'ü kesin aşar mı ve NOF kaldırımı (E5.6) nasıl kurulur? (<=130 kelime)"
    ),
    (
        "0g-ramanujan-E6.5",
        "Sen Ramanujan'sın. Sadece doğrudan Türkçe teknik yanıt ver (İngilizce düşünce metni yazma). "
        "Sonunda 'YENİ ALT-ENGEL:' başlığıyla E6.6 öner ve [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 15 — DÜĞÜM E6.5 (n=5 K_5=5,624 Üzerinde Kesin D_PTF(5) >= 7..9 Eşiği & Birleşik THR o THR Varyans Sönümlemesi): "
        "Teorem 23.1 orbit-AND altuzayı ile n=5 (K_5=5,624) için k=7,8,9 derecelerinde [perm_5 != 0 mod 3] kesin D_PTF(5) eşiği nerede kırılır (D_PTF(n) - n artışı)? "
        "Ayrıca birleşik THR o THR kapılarının yörünge-içi varyans sönümlemesi mu*_THR ile korelasyonu nasıl sınırlar ve TC^0_3 için doğan E6.6 alt-engeli nedir? (<=130 kelime)"
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
        "temperature": 0.3,
        "max_tokens": 2200,
    }
    cmd = [
        "/usr/bin/curl", "-s", "-X", "POST", API_URL,
        "-H", f"Authorization: Bearer {api_key}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload, ensure_ascii=False),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    try:
        data = json.loads(res.stdout)
        msg = data["choices"][0]["message"]
        text = msg.get("content") or msg.get("reasoning_content") or str(data)
    except Exception as e:
        text = f"ERROR: {e} | raw={res.stdout[:300]}"
    return name, text.strip()


def main():
    api_key = load_key()
    with ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(lambda it: query_one(it, api_key), PROMPTS))
    lines = ["# 0G Konseyi — Tur 15 (ENGEL_HARITASI.md Aktif Alt-Engellerine Saldırı: E2.5..E6.5)\n"]
    for name, text in results:
        lines.append(f"## {name}\n\n{text}\n\n---\n")
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[0G Round 15 Diagram] Saved all 6 sub-obstacle analyses to {OUT_MD}")


if __name__ == "__main__":
    main()
