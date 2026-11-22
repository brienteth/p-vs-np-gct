"""
Tek Masa Tartışması — Faz 1 (0G Kolu Açılış Pozisyonları):
Araştırma Sorusu: SAT ∉ P/poly (Süperpolinom Boolean Devre Alt Sınırları) ve
Cebirsel Karmaşıklıktan Boolean Karmaşıklığa Aktarım İlkesi.
"""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
OUT_MD = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_SAT_TRANSFER_R1.md"
API_URL = "https://router-api.0g.ai/v1/chat/completions"
MODEL = "0gm-1.0-35b-a3b"


def load_key() -> str:
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("0G_API_KEY="):
                return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("0G_API_KEY not found")


SHARED_RULES = (
    "Sadece doğrudan, teknik, hakem düzeyinde Türkçe yanıt ver; asla İngilizce düşünce taslağı veya şişirme/abartı yazma. "
    "Bilmediğin veya emin olmadığın literatür/yazar yılı uydurma; yalnızca gerçekten bilinen teoremlere atıf yap ve kanıtlanmamış hiçbir şeyi kanıtlanmış gibi sunma. "
    "Sonunda karşı kolun (Swarm Konseyi) yanıtlaması için 'KARŞI KOLA KESKİN SORU:' başlığıyla tek bir zorlayıcı teknik soru sor. (<=180 kelime)"
)

PROMPTS = [
    (
        "0g-pisagor (Mesele 1: Devre Alt Sınırı — SAT ∉ P/poly)",
        "Sen Pisagor'sun. " + SHARED_RULES,
        "MESELE 1 (Devre Alt Sınırı): SAT'ı çözen her Boolean devre ailesi {C_n} için ∀k, |C_n| > n^k kanıtlanabilir mi? "
        "Bugün genel Boolean devrelerde en iyi açık alt sınır hâlâ 3.1n - o(n) (Li–Yang 2022). "
        "Ara kapıların (internal wires) keyfi kombinatoryal kodlamasını kıran yeni bir yapısal ölçü neden henüz bulunamadı? "
        "Prof. Euler ve Prof. Valiant'a bu tıkanıklığı aşacak somut bir hipotez ve tek bir keskin soru yönelt."
    ),
    (
        "0g-oklid (Mesele 2: Cebirsel → Boolean Aktarım Boşluğu)",
        "Sen Öklid'sin. " + SHARED_RULES,
        "MESELE 2 (Cebirsel Karmaşıklık Bağlantısı): Bürgisser (2000, GRH) VP_C != VNP_C => P^#P ⊄ P/poly verir, "
        "fakat Toda (1991) PH ⊆ P^#P yönündedir; yani VP != VNP bile doğrudan SAT ∉ P/poly vermez (#P vs NP boşluğu). "
        "Permanent / determinantal complexity / ABP alt sınırlarını SAT'a taşıyan bir aktarım teoremi kurmak için "
        "sayma (#P) ile karar (NP) arasındaki hangi yapısal ara-köprü gereklidir? Prof. Strassen ve Prof. Hilbert'e keskin soru yönelt."
    ),
    (
        "0g-arsimet (Mesele 3: Temsil Karmaşıklığı & İdeal Belirsizliği)",
        "Sen Arşimet'sin. " + SHARED_RULES,
        "MESELE 3 (Temsil Karmaşıklığı): perm_n polinom olarak VNP-tamdır, ancak Boolean fonksiyonu perm_n mod 2 = det_n mod 2 ∈ NC^2 ⊆ P/poly'dir. "
        "Ayrıca {0,1}^N üzerinde aynı Boolean fonksiyonunu veren f + <x_i^2 - x_i> ideal sınıfındaki polinomların cebirsel karmaşıklıkları dramatik biçimde değişebilir. "
        "Cebirsel temsil karmaşıklığının Boolean devre karmaşıklığını zorunlu kılması için kesin gerek/yeter koşullar nelerdir? Prof. Wigner ve Prof. Noether'e keskin soru yönelt."
    ),
    (
        "0g-gauss (Mesele 4: Asimptotik Genelleme & Mignon–Ressayre Tavanı)",
        "Sen Gauss'sun. " + SHARED_RULES,
        "MESELE 4 (Asimptotik Genelleme): Sabit n=4 için elimizde tam ispatlı dc_C(perm_4) >= 10 (tekillik kodimansı + Çarpık-Kare) var; "
        "fakat tekillik/Hessian yöntemleri N=n^2 ortamında yapısal olarak O(n^2) tavanına (Mignon–Ressayre) çarpar. "
        "Sabit boyutlu cebirsel/kombinatoryal alt sınırlardan tüm n'ler ve tüm k>0 için |C_n| > n^k veren asimptotik bir ilkeye geçişte "
        "hangi nicelik süper-polinom ayrışabilir? Prof. Hilbert ve Prof. Strassen'e keskin soru yönelt."
    ),
    (
        "0g-harezmi (Mesele 5: Relativization, Natural Proofs, Algebrization)",
        "Sen Harezmi'sin. " + SHARED_RULES,
        "MESELE 5 (Üç Büyük Bariyer): SAT ∉ P/poly kanıtı Relativization (BGS75), Algebrization (AW09) ve özellikle Razborov–Rudich Natural Proofs (RR97) "
        "engellerini eşzamanlı aşmak zorundadır. Largeness'ı kırmak (GCT / aşırı simetri) mı yoksa Constructivity'yi kırmak (Williams devre-SAT ⇒ alt sınır) mı "
        "cebir-Boolean aktarımı için daha gerçekçi yoldur? Prof. Valiant ve Prof. Noether'e keskin soru yönelt."
    ),
    (
        "0g-ramanujan (Sentez & Şeytanın Avukatı: Aktarım İlkesi Var mı?)",
        "Sen Ramanujan'sın. " + SHARED_RULES,
        "ANA HEDEF (Aktarım İlkesinin Varlığı): Cebirsel karmaşıklıkta elde edilen yapısal alt sınırları Boolean devrelerde asimptotik alt sınırlara "
        "dönüştüren genel bir matematiksel aktarım ilkesi gerçekten var olabilir mi, yoksa cebirsel (sürekli/polinom) ve Boolean (ayrık/bit-düzeyi) dünyalar "
        "arasında kapatılamaz bir yapısal uçurum mu vardır? Bugün test edilebilir en somut ara hedef (ör. TC^0 vs n^{2+eps} VP/VNP) hangisidir? Tüm Swarm Konseyi'ne keskin soru yönelt."
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
    lines = ["# 0G Konseyi — Tek Masa Tartışması Faz 1 (SAT ∉ P/poly & Cebirsel→Boolean Aktarım İlkesi)\n"]
    for name, text in results:
        lines.append(f"## {name}\n\n{text}\n\n---\n")
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[0G SAT Transfer R1] Saved 6 opening theses to {OUT_MD}")


if __name__ == "__main__":
    main()
