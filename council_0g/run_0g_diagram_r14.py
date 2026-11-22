"""
Round 14 — 0G Historical Mathematicians Council Runner for ENGEL_HARITASI.md Active Sub-Obstacles:
  - 0g-pisagor:   Node E2.4 (Pure T_4^row m>=15 Handshaking Closure & Bilateral T_n Breaking)
  - 0g-oklid:     Node E3.6 (Sing_2(perm_5) codim=15 & Multi-Stratum Gluing for w_2=4)
  - 0g-arsimet:   Node E3.7 (Hessian-Rank Stratification Ladder H_{<=2k}(perm_4) toward dc >= 11..13)
  - 0g-gauss:     Node E4.4 (Explicit Zariski Border Invariant R_9^{(4)}(F) = P^{(4)}(F)*Q^{(4)}(F))
  - 0g-harezmi:   Node E5.4 (Valiant mu*_THR-Weighted Sherstov Discrepancy & Multi-Modulus det_n Compression)
  - 0g-ramanujan: Node E6.4 (Unbounded-Weight Perceptron Pricing, n=5 THR Scaling & Depth-3 TC^0_3)
"""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
OUT_MD = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_DIAGRAM_R14.md"
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
        "0g-pisagor-E2.4",
        "Sen Pisagor'sun. Sadece doğrudan Türkçe teknik yanıt ver (İngilizce düşünce metni yazma). "
        "Sonunda 'YENİ ALT-ENGEL:' başlığıyla E2.5 öner ve [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 14 — DÜĞÜM E2.4 (Salt T_4^row m>=15 Handshaking Kapanışı & n=5 Genellemesi): "
        "Tur 13 Teorem 19A ile w_1=4 tüm 4 satırı tek sütun j_0'a kilitliyor. w_3 keyfi (hatta (4,4,5) at m=14 dahil!) olsa bile, "
        "X_{r, j_0} katsayısı perm_3 için slice-rank(perm_3)=3 nedeniyle d(r)>=3 verir; Handshaking 2 w_2 = sum d(r) >= 12 => w_2 >= 6 ve m >= 15! "
        "n=5'te str(perm_4)=4 ile w_2 >= 10 çıkar. Bu mekanizma çift-taraflı T_n kırılmasını nasıl kısıtlar ve hangi E2.5 alt-engeli doğar? (<=130 kelime)"
    ),
    (
        "0g-oklid-E3.6",
        "Sen Öklid'sin. Sadece doğrudan Türkçe teknik yanıt ver (İngilizce düşünce metni yazma). "
        "Sonunda 'YENİ ALT-ENGEL:' başlığıyla E3.8 öner ve [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 14 — DÜĞÜM E3.6 (Sing_2(perm_5) codim=15 & w_2=4 Çok-Tabakalı Yapışma): "
        "Tur 13'te tek başına 2-sıfır-satır tabakası R_{01}'de saf (1,1)-bidegree ayrışma w_2=4'te 9.93e-16 hata verdi; yani tek tabaka w_2=4'ü eleyemiyor! "
        "Öte yandan Z = V(G_1..G_4, H_1..H_4) içindeki tüm tabakalar R_{ij}, C_{ab} ve yüksek katlı Sing_2(perm_5) (codim=15) nasıl birleştirilirse w_2=4 küresel olarak çökertilir? "
        "Doğan YENİ ALT-ENGEL (E3.8) nedir? (<=130 kelime)"
    ),
    (
        "0g-arsimet-E3.7",
        "Sen Arşimet'sin. Sadece doğrudan Türkçe teknik yanıt ver (İngilizce düşünce metni yazma). "
        "Sonunda 'YENİ ALT-ENGEL:' başlığıyla E3.9 öner ve [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 14 — DÜĞÜM E3.7 (Hessian-Rank Katmanlama Merdiveni ile dc(perm_4) >= 11..13): "
        "Tur 13'te Çift-Koszul + Çarpık-Kare Lemması ile m=9 (w_mid=0) elendi ve dc(perm_4) >= 10 kanıtlandı. "
        "Şimdi m=10 (w=9) için w_mid=1 veya ekstra korank s=1 durumlarında rank(Hess(perm_4)|_{W^perp}) <= 2 veya 4 çıkar. "
        "H_{<=2k}(perm_4) = {X in Sing : rank(Hess)<=2k} kodimans merdivenini ve genel n>=4 tırmanışını açıklayın; hangi E3.9 alt-engeli doğar? (<=130 kelime)"
    ),
    (
        "0g-gauss-E4.4",
        "Sen Gauss'sun. Sadece doğrudan Türkçe teknik yanıt ver (İngilizce düşünce metni yazma). "
        "Sonunda 'YENİ ALT-ENGEL:' başlığıyla E4.5 öner ve [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 14 — DÜĞÜM E4.4 (Açık Sınır Determinant Polinomu R_9^{(4)}(F) = P^{(4)}(F) * Q^{(4)}(F)): "
        "L_8'deki derece-9 IMSC determinantı P^{(4)}(F) tüm D_8^hom ile m=9'daki r>=2 veya D<=7 tabakalarını sıfırlar. "
        "L_{12}'deki Sing_2 Macaulay determinantı Q^{(4)}(F) ise m=9 D=8 (W^perp subset Sing_2) tabakasını sıfırlar. "
        "Çarpımları R_9^{(4)}(F) nasıl dc_border(perm_4) >= 10 (Zariski kapanışı!) kanıtlar ve m=10 için H_{<=2} kovaryantı (E4.5) nasıl doğar? (<=130 kelime)"
    ),
    (
        "0g-harezmi-E5.4",
        "Sen Harezmi'sin. Sadece doğrudan Türkçe teknik yanıt ver (İngilizce düşünce metni yazma). "
        "Sonunda 'YENİ ALT-ENGEL:' başlığıyla E5.5 öner ve [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 14 — DÜĞÜM E5.4 (Valiant mu*_THR-Ağırlıklı Sherstov Discrepancy & Çok-Modüllü det_n): "
        "Tur 13'te tekdüze Forster det_4'ün NC^2 sertliği yüzünden ayrım veremedi. "
        "Valiant'ın E6.3'ten verdiği 127/317 yörüngeli adversarial dual dağılımı mu*_THR ile M o mu ağırlıklandırıldığında Sherstov discrepancy nasıl perm_4 vs det_4'ü ayırır? "
        "Ayrıca n=5'te |det_5|=2 düzeltmesi %8.36 hatayı ne kadar düşürür? Hangi E5.5 alt-engeli doğar? (<=130 kelime)"
    ),
    (
        "0g-ramanujan-E6.4",
        "Sen Ramanujan'sın. Sadece doğrudan Türkçe teknik yanıt ver (İngilizce düşünce metni yazma). "
        "Sonunda 'YENİ ALT-ENGEL:' başlığıyla E6.5 öner ve [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 14 — DÜĞÜM E6.4 (Sınırsız Ağırlıklı Perceptron Fiyatlama, n=5 THR & TC^0_3): "
        "Tur 13'te 3,075 işaretli {-1,0,+1}-THR kapısında perm_4 vs det_4 uçurumu 1.750x'e çıktı ve n=3->4 12.06x büyüme verdi. "
        "||alpha||_inf >= 2 sınırsız ağırlıklı perceptron fiyatlaması bu uçurumu kırabilir mi ve derinlik-3 TC^0_3 = MAJ o THR o THR Reynolds bariyeri (E6.5) nedir? (<=130 kelime)"
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
    lines = ["# 0G Konseyi — Tur 14 (ENGEL_HARITASI.md Yeni Alt-Engellerine Saldırı: E2.4..E6.4)\n"]
    for name, text in results:
        lines.append(f"## {name}\n\n{text}\n\n---\n")
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[0G Round 14 Diagram] Saved all 6 sub-obstacle analyses to {OUT_MD}")


if __name__ == "__main__":
    main()
