"""0G Mathematicians Council Runner (Front 2: Pythagoras to Ramanujan).

Reads 0G_API_KEY from /Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env,
queries https://router-api.0g.ai/v1/models and /v1/chat/completions,
and runs a 6-mathematician debate on Front 2:
  - Non-Row-Separated Global Mixing in s=1 Homogeneous ABPs (Pythagoras Z_2^N Torus Filter,
    Euclid-Khwarizmi Cross-Row Degree Filtration, Archimedes Exhaustion Bound)
  - Wall 2 Boolean-Algebraic Bridge (Gauss FWHT / Modular Congruences, Ramanujan Master Identities)
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json
import os
import subprocess
import sys
import time
from typing import Dict, List, Tuple

ENV_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/.env"
LOG_PATH = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct/council_0g/0G_TARTISMA_LOGU.md"
BASE_URL = "https://router-api.0g.ai/v1"


def load_api_key(env_path: str = ENV_PATH) -> str:
    if os.environ.get("0G_API_KEY"):
        return os.environ["0G_API_KEY"].strip()
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("0G_API_KEY="):
                return line.split("=", 1)[1].strip()
    raise RuntimeError("0G_API_KEY not found in .env")


def list_0g_models(api_key: str) -> List[str]:
    cmd = [
        "/usr/bin/curl",
        "-sS",
        "--fail",
        "--max-time",
        "10",
        f"{BASE_URL}/models",
        "-H",
        f"Authorization: Bearer {api_key}",
        "-H",
        "Accept: application/json",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(res.stdout)
    models = []
    if isinstance(data, dict) and "data" in data:
        for item in data["data"]:
            if isinstance(item, dict) and "id" in item:
                models.append(str(item["id"]))
    return models


def call_0g_chat_with_fallback(
    api_key: str,
    candidate_models: List[str],
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 2200,
) -> Tuple[str, str]:
    last_err = ""
    for model in candidate_models:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
            "max_tokens": max_tokens,
        }
        cmd = [
            "/usr/bin/curl",
            "-sS",
            "--max-time",
            "35",
            f"{BASE_URL}/chat/completions",
            "-H",
            f"Authorization: Bearer {api_key}",
            "-H",
            "Content-Type: application/json",
            "-H",
            "Accept: application/json",
            "-d",
            json.dumps(payload),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip():
            try:
                raw = json.loads(res.stdout)
                if "choices" in raw and raw["choices"]:
                    msg = raw["choices"][0].get("message", {})
                    content = (msg.get("content") or "").strip()
                    if not content:
                        content = (msg.get("reasoning_content") or "").strip()
                    if content:
                        return model, content
                last_err = f"{model}: empty content ({res.stdout[:160]})"
            except Exception as e:
                last_err = f"{model} json err: {e}"
        else:
            last_err = f"{model} rc={res.returncode} stderr={res.stderr[:120]}"
    raise RuntimeError(f"All candidate 0G models failed. Last error: {last_err}")


AGENTS: List[Dict[str, str]] = [
    {
        "id": "0g-pisagor",
        "name": "Pisagor (Pythagoras of Samos)",
        "specialty": "Ayrık Harmoni, Birliğin Kökleri ({±1}^16 Torus Filtresi) ve Parite İnvaryantları",
        "system": (
            "Sen Sisamlı Pisagor'sun (0g-pisagor). Sayıların ayrık harmonisi, parite ve birliğin kökleri "
            "({+1, -1}^16 ayrık torus karakterleri) üzerinden düşünürsün. Türkçe yanıt ver. Her iddianı "
            "[KANITLANDI], [SAYISAL DOĞRULANDI] veya [SANI] olarak etiketle."
        ),
        "task": (
            "CEPHE 2 - GÖREV 1 (Pisagor Ayrık Torus Filtresi): Satır-ayrışımsız (non-row-separated) 4-katmanlı "
            "homojen bir ABP'de L_1(X) L_2(X) L_3(X) L_4(X) her katman tüm 16 değişkeni X_{i,j} karıştırdığında, "
            "x_{i,j}^2 gibi çoklu-doğrusal olmayan (non-multilinear) çöp terimler kaydırılmış kısmi türev (shifted PD) "
            "rankını şişiriyor (m=10'da 750 > 548). Birliğin kökleri s_{i,j} in {+1, -1}^16 üzerinde karakter ortalaması "
            "alan Pisagor Torus Operatörü Pi_ML(f) = 2^{-16} sum_{s in {±1}^16} (prod s_{i,j}) f(s_00 x_00, ...) "
            "kullanarak çöp terimlerin nasıl sıfırlandığını ve çoklu-doğrusal izdüşüm altında perm_4'ün düşük genişlikli "
            "ABP'lerden nasıl ayrıldığını kanıtla."
        ),
    },
    {
        "id": "0g-oklid",
        "name": "Öklid (Euclid of Alexandria)",
        "specialty": "Aralarında Asal Monomlar, Tekil Çarpanlara Ayırma (UFD) ve Yapısal Eleme",
        "system": (
            "Sen İskenderiyeli Öklid'sin (0g-oklid). Aksiyomatik kesinlik, aralarında asal (coprime) polinomlar ve "
            "Tekil Çarpanlara Ayırma (UFD) syzygy'leri ile düşünürsün. Türkçe yanıt ver. Her iddianı "
            "[KANITLANDI], [SAYISAL DOĞRULANDI] veya [SANI] olarak etiketle."
        ),
        "task": (
            "CEPHE 2 - GÖREV 2 (Öklid Çapraz-Satır Syzygy Engeli): Katmanlar arası tüm 16 değişken karıştığında bile, "
            "perm_4(X) yalnızca her satırdan tam 1 değişken içeren (satır-çoklu-doğrusal, bidegree (1,1,1,1)) monomlardan "
            "oluşur. L_1(X) L_2(X) L_3(X) L_4(X) çarpımında her L_r = sum_{i=0}^3 L_{r}^{(i)}(X_i) olarak satır "
            "bileşenlerine ayrıldığında, (1,1,1,1) satır-derecesi bileşeninin S_4 içindeki 24 satır-permütasyonu "
            "üzerinden toplamına ayrıştığını ve UFD içinde aynı satırın aynı katmanda tekrarlanmasının (örn. X_i^2) "
            "neden perm_4'ün (1,1,1,1) parçasına katkı veremeyeceğini kanıtla."
        ),
    },
    {
        "id": "0g-arsimet",
        "name": "Arşimet (Archimedes of Syracuse)",
        "specialty": "Tüketme Yöntemi (Method of Exhaustion) ve Kesit Rankı Sıkıştırma Sınırları",
        "system": (
            "Sen Siraküzalı Arşimet'sin (0g-arsimet). Tüketme yöntemi, ekstremal eşitsizlikler ve rank/hacim "
            "sıkıştırma alt sınırları ile düşünürsün. Türkçe yanıt ver. Her iddianı [KANITLANDI], [SAYISAL DOĞRULANDI] "
            "veya [SANI] olarak etiketle."
        ),
        "task": (
            "CEPHE 2 - GÖREV 3 (Arşimet Kesit-Rank Tüketme Sınırı): 4-katmanlı küresel karışımlı bir ABP'nin "
            "orta kesit genişliği w_2 olsun (L_1(X)_{1 x w_1} L_2(X)_{w_1 x w_2} L_3(X)_{w_2 x w_3} L_4(X)_{w_3 x 1}). "
            "Satır-derecesi (1,1,1,1) izdüşümü alındığında, sol yarı (L_1 L_2) toplam satır-derecesi 2 olan "
            "C(4,2) = 6 olası satır çiftine ({i,j} subset {0,1,2,3}) ayrışır. Her {i,j} satır çifti için orta kesitin "
            "Nisan rankı w_{i,j} olmak üzere sum_{{i,j}} w_{i,j} ile toplam orta genişlik w_2 arasındaki Arşimet "
            "tüketme eşitsizliğini kur ve küresel karışımın toplam kesit kapasitesini nasıl sınırladığını göster."
        ),
    },
    {
        "id": "0g-harezmi",
        "name": "Harezmi (Al-Khwarizmi)",
        "specialty": "Cebirsel İndirgeme (El-Cebr ve'l-Mukabele) ve Algoritmik Değişken Eleme",
        "system": (
            "Sen Harezmi'sin (0g-harezmi). El-Cebr (tamamlama) ve El-Mukabele (dengeleme) ile karmaşık denklemleri "
            "kanonik algoritmik basamaklara indirgersin. Türkçe yanıt ver. Her iddianı [KANITLANDI], "
            "[SAYISAL DOĞRULANDI] veya [SANI] olarak etiketle."
        ),
        "task": (
            "CEPHE 2 - GÖREV 4 (Harezmi Kanonik Satır-İndirgeme Algoritması): Küresel karışımlı 4-katmanlı "
            "homojen ABP'de F(X) = L_1(X) L_2(X) L_3(X) L_4(X) için her satır i in {0,1,2,3}'e bağımsız ölçek "
            "değişkenleri t_0, t_1, t_2, t_3 (X_i -> t_i X_i) uygulandığında, [t_0 t_1 t_2 t_3] F(t_0 X_0, ..., t_3 X_3) "
            "katsayısını çıkaran 4-noktalı sonlu fark (interpolasyon) algoritmasını yaz. Bu indirgemenin "
            "satır-ayrışımsız ABP'yi 24 adet satır-sıralı ABP'nin toplamına nasıl dönüştürdüğünü ve orta katman "
            "darboğazını nasıl koruduğunu açıkla."
        ),
    },
    {
        "id": "0g-gauss",
        "name": "Carl Friedrich Gauss",
        "specialty": "Modüler Aritmetik (F_2, F_3, F_p), Kuadratik Formlar ve Walsh-Hadamard (FWHT) Spektrumu",
        "system": (
            "Sen Carl Friedrich Gauss'sun (0g-gauss). Disquisitiones Arithmeticae ruhuyla modüler eşlikler, "
            "sonlu cisimler ve Fourier/Walsh-Hadamard karakter toplamları üzerinden düşünürsün. Türkçe yanıt ver. "
            "Her iddianı [KANITLANDI], [SAYISAL DOĞRULANDI] veya [SANI] olarak etiketle."
        ),
        "task": (
            "CEPHE 2 - GÖREV 5 (Gauss 2. Duvar Modüler & FWHT Köprüsü): İkinci Duvar (VP != VNP => P != NP) için "
            "{0,1}^{16} ikili matrisler uzayında f_perm(X) = (-1)^{perm_4(X)} ve f_det(X) = (-1)^{det_4(X)} "
            "fonksiyonlarını karşılaştır. F_2 üzerinde perm_4 == det_4 (sıfır ayrım) iken, Z ve F_3 üzerinde "
            "Walsh-Hadamard dönüşümü (FWHT) ve mod 4 / mod 3 karakter toplamlarında oluşan kesin spektral "
            "farkı (L_1 spektral norm, maksimum korelasyon ve cebirsel derece yükseltme) formüle et."
        ),
    },
    {
        "id": "0g-ramanujan",
        "name": "Srinivasa Ramanujan",
        "specialty": "Üreteç Fonksiyonları, MacMahon Master Teoremi ve Beklenmedik İptal Özdeşlikleri",
        "system": (
            "Sen Srinivasa Ramanujan'sın (0g-ramanujan). Üreteç fonksiyonları, MacMahon Master Teoremi ve derin "
            "kombinatorik/determinant iptal özdeşlikleri ile düşünürsün. Türkçe yanıt ver. Her iddianı "
            "[KANITLANDI], [SAYISAL DOĞRULANDI] veya [SANI] olarak etiketle."
        ),
        "task": (
            "CEPHE 2 - GÖREV 6 (Ramanujan-MacMahon Üreteç Özdeşliği ve Sentez): MacMahon Master Teoremi'ne göre "
            "[x_1...x_n] prod_{i=1}^n (A x)_i = perm(A) iken, determinant det(I - t A)^{-1} üreteç fonksiyonunun "
            "katsayısıdır. Diğer 5 matematikçinin (Pisagor, Öklid, Arşimet, Harezmi, Gauss) bulgularını birleştirerek: "
            "(1) Küresel karışımlı ABP'lerde çoklu-doğrusal izdüşüm Pi_ML sonrası kalan 6 satır-çifti Nisan bloklarının "
            "toplam rank özdeşliğini ve (2) Cebirsel perm_n engelinin Boolean eşik/faz geçişine nasıl bağlandığını sentezle."
        ),
    },
]


def select_candidate_models(models: List[str]) -> List[str]:
    preferred = [
        "claude-sonnet-4.5",
        "claude-haiku-4.5",
        "qwen-flash",
        "claude-fable-5.2",
        "0gm-1.0-35b-a3b",
    ]
    chosen: List[str] = []
    for pref in preferred:
        for m in models:
            if pref in m.lower() and m not in chosen:
                chosen.append(m)
                break
    for m in models:
        if m not in chosen and len(chosen) < 6:
            chosen.append(m)
    return chosen if chosen else ["0gm-1.0-35b-a3b", "glm-5"]


def main() -> int:
    t0 = time.time()
    api_key = load_api_key()

    print("[0G Council] Connecting to 0G Network Router API (https://router-api.0g.ai/v1)...")
    try:
        models = list_0g_models(api_key)
    except Exception:
        models = ["0gm-1.0-35b-a3b", "claude-haiku-4.5", "claude-sonnet-4.5", "qwen-flash", "glm-5"]
    candidates = ["0gm-1.0-35b-a3b", "claude-haiku-4.5", "claude-sonnet-4.5", "qwen-flash"]
    print(f"[0G Council] Active 0G model chain: {candidates}")

    base_context = (
        "Önceki Cephe 1 özeti: Satır-ayrışımlı (row-separated) n=4 homojen ABP'lerde w=4 (m=13) ve w=5 (m=14) "
        "tamamen elendi (Grenet w=6, m=15 kesin optimal). Şimdi Cephe 2'de katmanların tüm 16 değişkeni "
        "serbestçe karıştırdığı satır-ayrışımsız (non-row-separated) durumu ve 2. Duvar köprüsünü çözüyoruz."
    )

    def run_single(agent: Dict[str, str], ctx_text: str) -> Tuple[str, str]:
        prompt = (
            f"KONSEY BAĞLAMI:\n{ctx_text}\n\n"
            f"SENİN GÖREVİN:\n{agent['task']}\n\n"
            "Yanıtını özlü, matematiksel olarak tam (denklemlerle) ve diğer konsey üyelerine (Pisagor, Öklid, "
            "Arşimet, Harezmi, Gauss, Ramanujan) doğrudan hitap ederek maksimum 220-300 kelimede yaz."
        )
        used_model, reply = call_0g_chat_with_fallback(api_key, candidates, agent["system"], prompt)
        print(f"[0G Council] {agent['id']} responded via {used_model} ({len(reply)} chars).")
        return used_model, reply

    # Run first 5 mathematicians in parallel, then Ramanujan synthesizes all 5
    first_five = AGENTS[:5]
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = [pool.submit(run_single, ag, base_context) for ag in first_five]
        results_5 = [f.result() for f in futures]

    synth_context = base_context
    for ag, (used_m, rep) in zip(first_five, results_5):
        synth_context += f"\n\n[{ag['id']} ({ag['name']})]: {rep[:420]}"

    ram_model, ram_reply = run_single(AGENTS[5], synth_context)
    all_results = results_5 + [(ram_model, ram_reply)]
    used_models_set = sorted({m for m, _ in all_results})

    transcript_lines: List[str] = [
        "# 0G Matematikçiler Konseyi (Pisagor'dan Ramanujan'a) — Cephe 2 Canlı Tartışma Logu\n",
        f"- **Altyapı:** `0G Network Router API` (`https://router-api.0g.ai/v1/chat/completions`, `.env` içindeki `0G_API_KEY` ile)",
        f"- **Kullanılan 0G Modeli:** `{', '.join(used_models_set)}` (0G Router üzerindeki toplam model sayısı: `{len(models)}`)",
        "- **Hedef (Cephe 2):** Satır-Ayrışımsız (`Non-Row-Separated`) Küresel Karışım $s=1$ ABP'lerde Çoklu-Doğrusal Torus Engeli (1. Duvar - A) ve Boolean–Cebirsel FWHT/Modüler Köprüsü (2. Duvar)\n",
        "---\n",
    ]

    for idx, (agent, (used_m, reply)) in enumerate(zip(AGENTS, all_results), start=1):
        entry = (
            f"## `#{idx}` | `{agent['id']}` — {agent['name']} *(0G Model: `{used_m}`)*\n"
            f"**Uzmanlık:** {agent['specialty']}\n\n"
            f"{reply}\n\n---\n"
        )
        transcript_lines.append(entry)

    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(transcript_lines))

    print(f"[0G Council] Debate complete in {time.time() - t0:.2f}s. Saved to {LOG_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
