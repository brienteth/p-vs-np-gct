"""
Tek Masa Tartışması — Faz 3 (0G Kolu Karşı Sorgulama & Son Yanıtlar):
Swarm Konseyi'nin Faz 2 eleştirilerine ve '0G KOLUNA KARŞI SORU:' sorularına
0G Konseyi üyelerinin doğrudan teknik yanıtları.
"""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
OUT_MD = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_SAT_TRANSFER_R2.md"
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
    "Bilmediğin literatür/yazar yılı uydurma ve kanıtlanmamış hiçbir şeyi kanıtlanmış gibi sunma. "
    "Swarm üyesinin düzeltmelerini kabul ettiğin ve ısrar ettiğin noktaları açıkça ayır, karşı sorusunu doğrudan yanıtla ve "
    "en sonunda 'ORTAK KARAR / AÇIK ENGEL:' başlığıyla kısa bir kapanış yargısı yaz. (<=160 kelime)"
)

PROMPTS = [
    (
        "0g-pisagor (Faz 3 Yanıt → Prof. Euler)",
        "Sen Pisagor'sun. " + SHARED_RULES,
        "PROF. EULER SANA ŞU YANITI VE KARŞI SORUYU YÖNELTTİ:\n"
        "1) Li–Yang (STOC 2022) tam ikili tabanda 3.1n - o(n) kapı alt sınırını gerçekten kanıtlamıştır; varlığını reddetmen hatalıydı.\n"
        "2) Önerdiğin etkileşim grafiği kesme genişliği genel DAG devrelerde süper-lineer alt sınır üretemez, çünkü Valiant süper-yoğunlaştırıcıları "
        "ve sabit dereceli genişletici DAG'ları zaten O(n)-O(n log n) kapıyla Omega(n) kesme genişliğine ulaşır; sınırsız fan-out paylaşım kapı sayısını kesitten koparır.\n"
        "3) Simetri kırılımı doğruluk tablosunda tanımlanırsa TYF altında sahte-rastgele asimetrik devrelerce atlatılır (RR97), devre içinde tanımlanırsa yapay asimetriye kapı maliyeti ödenmez.\n"
        "EULER'İN SORUSU: Serbest P/poly DAG'larında O(n log n) kapılı devreler zaten Omega(n) etkileşim kesme genişliğine ulaşabiliyorken, "
        "kesme genişliği ölçünün yüksek fan-out paylaşımını hangi ek topolojik veya cebirsel kısıt olmadan omega(n) kapı alt sınırına dönüştürebileceğini savunuyorsun?"
    ),
    (
        "0g-oklid (Faz 3 Yanıt → Prof. Strassen)",
        "Sen Öklid'sin. " + SHARED_RULES,
        "PROF. STRASSEN SANA ŞU YANITI VE KARŞI SORUYU YÖNELTTİ:\n"
        "1) Faz 1'de 'NP ⊆ #P' yazman tip hatasıydı (#P fonksiyon sınıfı, NP karar sınıfıdır); doğru kapsama Toda'nın PH ⊆ P^#P teoremidir.\n"
        "2) Literatürde VP_C != VNP_C varsayımından deterministik PIT derandomizasyonu olmadan SAT ∉ P/poly çıkaran geçerli tek bir yapısal köprü yoktur. "
        "Kabanets–Impagliazzo (2004) dahi PIT in P'den (NEXP ⊄ P/poly veya perm ∉ VP) ikilemi çıkarır.\n"
        "STRASSEN'İN SORUSU: SAT ∈ P/poly varsayımı altında Toda ile PH çökse ve Stockmeyer ile #P fonksiyonları yalnızca BPP^NP içinde yaklaşık hesaplanabilse bile; "
        "kesin sayma (ör. [perm_n != 0 mod 3]) NP'ye indirgenemediğine göre, PIT derandomizasyonu olmaksızın VP_C != VNP_C'yi SAT ∉ P/poly'ye bağlamak için "
        "hangi kanıtlanmamış sayma-karar ters indirgemesini varsaymak zorunda kalırsın?"
    ),
    (
        "0g-arsimet (Faz 3 Yanıt → Prof. Wigner)",
        "Sen Arşimet'sin. " + SHARED_RULES,
        "PROF. WIGNER SANA ŞU YANITI VE KARŞI SORUYU YÖNELTTİ:\n"
        "mod-2 çöküşü teşhisinde hemfikiriz; fakat I=<x_i^2-x_i> ideal sınıfında hem modüler indirgeme altında invaryant kalan hem de cebirsel boyuttan Omega(s^c) Boolean alt sınırı veren tek bir ölçü YOKTUR. "
        "Ayrıca [det_n mod 2^k != 0] hatası n=3..10'da Wood limitine (0.439874) doygunlaşır; n=4'te det_4^2 mod 3 ve perm_4^2 mod 3 F_3[X]/I'da özdeş dereceye (8, 282 terim) sahipken "
        "yalnızca F_2-ANF (12 vs 15) ve dengeli kesit F_2-rankında (55/55 yörünge, n=5'te 40 vs 247) ayrışır.\n"
        "WIGNER'İN SORUSU: I=<x_i^2-x_i> üzerinde perm_4 ve det_4 mod 2'de özdeş, F_3'te aynı karesel derecede (8) olup F_2 kesit rankında ayrışıyorsa; "
        "p != 2'de GL_n(F_p) ayar kırılımı tek başına Boolean devre alt sınırı verebilir mi, yoksa Toda/algoritmik ikilik zorunlu mudur?"
    ),
    (
        "0g-gauss (Faz 3 Yanıt → Prof. Hilbert)",
        "Sen Gauss'sun. " + SHARED_RULES,
        "PROF. HILBERT SANA ŞU YANITI VE KARŞI SORUYU YÖNELTTİ:\n"
        "1) dc_C(perm_n) > n^k kanıtlansa dahi doğrudan |C_n| > n^k vermez (arada PIT ve NP vs #P boşluğu vardır).\n"
        "2) perm_n yörünge kapanışı Kronecker-plethysm simetrisi taşır, asimptotik tensör rank çarpımına indirgenmez. Üstelik Bürgisser–Ikenmeyer–Panova (2019, BIP19) "
        "GCT'de occurrence engellerinin süper-polinom alt sınır veremeyeceğini kanıtlamıştır; yalnızca multiplicity (çoğulluk) engelleri açıktadır.\n"
        "HILBERT'İN SORUSU: BIP19'un occurrence engellerini çökerttiği ve bilinen düzleştirme/Sing_r yöntemlerinin O(n^2) tavanında takıldığı ortamda; "
        "GCT çokluk engellerinin dolgu (l^{m-n} perm_n) etkisinden kurtulacağını garanti eden tek bir cebirsel-geometrik mekanizma gösterebilir misin?"
    ),
    (
        "0g-harezmi (Faz 3 Yanıt → Prof. Noether & Prof. Valiant)",
        "Sen Harezmi'sin. " + SHARED_RULES,
        "PROF. NOETHER VE PROF. VALIANT SANA ŞU YANITLARI VE SORULARI YÖNELTTİ:\n"
        "- Noether: Her s_B-boyutlu Boolean devre C üzerinde O(s_B) boyutlu f+g (g in I) üretir; tersi geçerli değildir ve ham Betti ölçüleri Simetri-Tersine Çevirme Tuzağına düşer. "
        "Williams yolu (algoritmik CAPP/devre-SAT) ile GCT yolu (C[X] yörünge kapanışı) arasında birleşik bir 'cebirsel-Boolean eşleme sınıfı' yoktur.\n"
        "- Valiant: Williams meta-teoremi C-SAT'ı 2^N/N^{omega(1)} çözmekten doğrudan NEXP ⊄ C köşegenleştirmesine geçer; ne ek bir eşleme sınıfı gerekir ne de NP'ye inebilir.\n"
        "KARŞI SORULAR: (Noether) I=<x_i^2-x_i> mod-2 çöküşüne yol açıyor ve GCT C-karakteristiğine bağlıysa, simetri kırılımını F_2 Boolean devrelere taşıyacak karakteristik-bağımsız "
        "bir invaryant hangi nesne üzerinde tanımlanabilir? (Valiant) NP ⊄ TC^0 dahi kanıtlanmadan Boolean devre analizinden VP != VNP'ye hangi somut kısıt aktarılabilir?"
    ),
    (
        "0g-ramanujan (Faz 3 Final Sentezi → Tüm Swarm Konseyi)",
        "Sen Ramanujan'sın. " + SHARED_RULES,
        "TÜM SWARM KONSEYİ SENİNLE HEMFİKİR OLDUĞU VE EKLEDİĞİ NOKTALAR:\n"
        "- Tüm 6 Swarm üyesi de VP != VNP => SAT ∉ P/poly veren genel ve doğrudan bir aktarım ilkesinin BUGÜN MEVCUT OLMADIĞI konusunda seninle birleşti.\n"
        "- Ancak Valiant, Wigner ve Hilbert şu nüansı vurguladı: (a) Temel engel yalnızca NW/kanıt-sistemi derecesi değil, karakteristik kırılımı (mod 2 çöküşü vs p != 2 ayar simetrisi) ve NP vs #P boşluğudur; "
        "(b) TC^0 ile n^{2+eps} cebirsel sınırları aynı şeye eşitlemek kategori hatası olsa da, her ikisi kendi cephelerinde (TC^0'da Williams/yörünge-LP, VP/VNP'de Mignon–Ressayre üstü) en gerçekçi ara hedeflerdir.\n"
        "FINAL SORUN: Swarm'ın bu düzeltmeleri ışığında, önümüzdeki 10 yılda kırılması en olası iki ara kapıdan hangisi (TC^0 ⊄ NP mı, yoksa Mignon–Ressayre n^2 tavanını kıran n^{2+eps} cebirsel alt sınır mı) "
        "diğer cepheye dolaylı olsa bile ilk somut sıçramayı tetikler?"
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
    lines = ["# 0G Konseyi — Tek Masa Tartışması Faz 3 (Karşı Sorgulama & Final Yanıtları)\n"]
    for name, text in results:
        lines.append(f"## {name}\n\n{text}\n\n---\n")
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[0G SAT Transfer R2] Saved 6 rebuttals to {OUT_MD}")


if __name__ == "__main__":
    main()
