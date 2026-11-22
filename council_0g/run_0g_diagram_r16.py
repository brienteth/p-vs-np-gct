"""
Round 16 — 0G Historical Mathematicians Council Runner for ENGEL_HARITASI.md Active Sub-Obstacles:
  - 0g-pisagor:   Node E2.6 (n=5 w_1=6, w_2 in {8,9} Deficit Closure m>=31 & General (k_r, k_c) Laurent Rank)
  - 0g-oklid:     Node E3.10 (Zero-Block det_6=-(det_3 N)^2 & det_8=(det_4 M)^2 Identities, (1,1) w_2=4 & Sing_2(perm_5))
  - 0g-arsimet:   Node E3.11 (Closing m=12 D=9 in H_{<=4} & D=8 in H_{<=6} => dc(perm_4)>=13, and m=13,14 Ceiling)
  - 0g-gauss:     Node E4.6 (Polynomial Border Invariant R_{11}^{(4)}(F) on L_{10} & perm_5 Coranks r in {2,3,4})
  - 0g-harezmi:   Node E5.6 (Grassmannian Gr_{0,1}(k,n,F_3) Upper Bound on rk_F2(det_n mod 3) & '40 == 40' Isomorphism)
  - 0g-ramanujan: Node E6.6 (Why det_n Resists PTFs via IP_{n-1} Embedding & True Separating Orbit-LP + rk_F2 Invariant)
"""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
OUT_MD = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_DIAGRAM_R16.md"
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
        "0g-pisagor-E2.6",
        "Sen Pisagor'sun. Sadece doğrudan Türkçe teknik yanıt ver; asla İngilizce düşünce metni veya taslak yazma. "
        "Sonunda 'YENİ ALT-ENGEL:' başlığıyla E2.7 öner ve [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 16 — DÜĞÜM E2.6 (n=5 (w_1=6, w_2 in {8,9}) Deficit Kapanışı & Genel (k_r, k_c) Laurent Kutup Rankı): "
        "n=5 T_5^row ABP'de w_1=6 a=(2,1,1,1,1) ve w_4=5 b=(1,1,1,1,1) iken (j_0 != j_1) sıralı çift [X_{r_1,j_0} X_{r_2,j_1}] katsayısı perm_3 (str=3) verir. "
        "Katman-2 w_2 in {8,9} grafikleri bu çift-sayma kısıtıyla tamamen elenir mi (m>=31)? "
        "Genel (k_r, k_c) çift-taraflı karışımda sahte Laurent kutuplarının düzleştirme rank toplamı nasıl büyür ve doğan E2.7 alt-engeli nedir? (<=120 kelime)"
    ),
    (
        "0g-oklid-E3.10",
        "Sen Öklid'sin. Sadece doğrudan Türkçe teknik yanıt ver; asla İngilizce düşünce metni veya taslak yazma. "
        "Sonunda 'YENİ ALT-ENGEL:' başlığıyla E3.12 öner ve [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 16 — DÜĞÜM E3.10 (Sıfır-Blok det_6=-(det_3 N)^2 & det_8=(det_4 M)^2 Özdeşlikleri, (1,1) w_2=4 & Sing_2(perm_5)): "
        "Hess(perm_4)'te aynı satır i'den 3 değişken R_3 ile C_3={(r_0,c_0),(r_1,a),(r_2,a)} sıfır-blok 6x6 altmatrisi det_6 = -(det_3 N)^2 (derece 6!) ve "
        "4 değişken R_4 ile C_4 sıfır-blok 8x8 altmatrisi det_8 = (det_4 M)^2 (derece 8!) verir. "
        "Bu yeni karekök-alınmış üreteçler L_{10} (H_{<=4}) ve L_9 (H_{<=6}) Macaulay matrislerini tam ranka ulaştırır mı; doğan E3.12 nedir? (<=120 kelime)"
    ),
    (
        "0g-arsimet-E3.11",
        "Sen Arşimet'sin. Sadece doğrudan Türkçe teknik yanıt ver; asla İngilizce düşünce metni veya taslak yazma. "
        "Sonunda 'YENİ ALT-ENGEL:' başlığıyla E3.13 öner ve [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 16 — DÜĞÜM E3.11 (m=12 Kapanışı => dc(perm_4) >= 13 & 2. Türev/Hessian Tavanı): "
        "m=12 (w=11) için yalnızca D=9 (W^perp <= H_{<=4}) ve D=8 (W^perp <= H_{<=6}) kaldı. "
        "Bunlar L_{10} (H_{<=4} codim>=10) ve L_9 (H_{<=6} codim>=9) ile kapandığında koşulsuz dc(perm_4) >= 13 elde edilir; peki m=13 (w=12, D=8)'de 2(w-D)=8 == rk(Hess) olduğunda Hessian merdiveni neden durur ve 3. türev jeti E3.13 gerekir? (<=120 kelime)"
    ),
    (
        "0g-gauss-E4.6",
        "Sen Gauss'sun. Sadece doğrudan Türkçe teknik yanıt ver; asla İngilizce düşünce metni veya taslak yazma. "
        "Sonunda 'YENİ ALT-ENGEL:' başlığıyla E4.7 öner ve [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 16 — DÜĞÜM E4.6 (L_{10} Üzerinde Polinomsal R_{11}^{(4)}(F) & perm_5 Orijin Korankları r in {2,3,4}): "
        "F'de kök almaksızın Zariski kapanışı bar(D_{11}^hom) üzerinde sıfırlanan açık R_{11}^{(4)}(F) sınır polinomu nasıl kurulur (det_6(Hess|_{R_3 U C_3}) gibi gerçek F-polinomları vs perm_4 satır-lineer det_3 N)? "
        "Ayrıca perm_5 için r=2,3,4 tekil kalem dallarından hangileri Sing_2 >= 13 ile hemen elenir ve doğan E4.7 nedir? (<=120 kelime)"
    ),
    (
        "0g-harezmi-E5.6",
        "Sen Harezmi'sin. Sadece doğrudan Türkçe teknik yanıt ver; asla İngilizce düşünce metni veya taslak yazma. "
        "Sonunda 'YENİ ALT-ENGEL:' başlığıyla E5.7 öner ve [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 16 — DÜĞÜM E5.6 (Grassmannian Gr_{0,1}(k,n,F_3) Üst Sınırı & '40 == 40' İzdüşümsel İzomorfizmi): "
        "n=5 row4=1_5 Satır-Kesiti neden rk_F2([det_5!=0 mod 3]) == 40 == rk_F2([det_4!=0 mod 3]) verir (v -> v - v_4 1_5 ile {0,1}^5/{0,1} -> P_{0,1}(F_3^4) izomorfizmi)? "
        "Kısıtsız 2-vs-(n-2) satır kesitinde rk_F2(det_n) Gr_{0,1}(2,n,F_3) ile O(3^{2n}) ya da daha küçük nasıl sınırlanır ve Mod_3 P alt sınırı E5.7 nedir? (<=120 kelime)"
    ),
    (
        "0g-ramanujan-E6.6",
        "Sen Ramanujan'sın. Sadece doğrudan Türkçe teknik yanıt ver; asla İngilizce düşünce metni veya taslak yazma. "
        "Sonunda 'YENİ ALT-ENGEL:' başlığıyla E6.7 öner ve [KANITLANDI]/[HİPOTEZ] etiketle.",
        "TUR 16 — DÜĞÜM E6.6 (det_n'nin Neden PTF'e Direndiği & Gerçek Ayırıcı Yörünge-LP + rk_F2 İnvaryantı): "
        "Schur tümleyeni det_n([I_{n-1}, u; v^T, c]) = c - IP_{n-1}(u,v) gömülmesi neden det_n mod 2/3'e süper-lineer D_PTF zorlar? "
        "O halde Mod_3P perm_n ile NC^2 det_n'i gerçekten ayıran yörünge-LP invaryantı nedir (dual destek yoğunluğu 127/317 vs 73/317, çapraz transfer veya rk_F2 çekirdeği) ve E6.7 nedir? (<=120 kelime)"
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
    lines = ["# 0G Konseyi — Tur 16 (ENGEL_HARITASI.md Aktif Alt-Engellerine Saldırı: E2.6..E6.6)\n"]
    for name, text in results:
        lines.append(f"## {name}\n\n{text}\n\n---\n")
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[0G Round 16 Diagram] Saved all 6 sub-obstacle analyses to {OUT_MD}")


if __name__ == "__main__":
    main()
