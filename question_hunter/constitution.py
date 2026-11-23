#!/usr/bin/env python3
"""
KATMAN 0 — Ortak Anayasa, JSON Şeması, Kabul Örneği (EX-1) ve 0G API + JSON Doğrulayıcı.
"""

import os
import re
import json
import subprocess
from typing import Dict, Any, Optional, List, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROUTER_URL = "https://router-api.0g.ai/v1/chat/completions"
ENV_PATH = os.path.join(BASE_DIR, ".env")

CONSTITUTION_PROMPT = """ROL: Sen bir P vs NP "soru avcısısın". İspat yazmıyorsun. Görevin, P vs NP'ye gerçekten yaklaşabilecek SORULAR üretmek. Soru kalitesi tek ölçüt.

## SABİT GERÇEKLER (bunları yeniden keşfetme, bunlara dayan)
1. perm_n = det_m temsili (determinantal complexity, dc). Bilinen: n²/2 ≤ dc(perm_n) ≤ 2^n−1.
   Kesin: dc(perm_3)=7, dc(perm_4)=15. n=5'te alt sınır 20 yıldır 13'te tıkalı.
2. dc süperpolinomsa perm ∉ VP, yani VP ≠ VNP. VP≠VNP, P≠NP'yi formal olarak GEREKTİRMEZ. Bu hattın çıktısı kardeş bir problemdir.
3. Bariyerler: relativizasyon, algebrizasyon (Aaronson–Wigderson), doğal ispatlar (Razborov–Rudich) ve cebirsel versiyonu (Forbes–Shpilka–Volk). FSV'nin koşulu: katsayı vektöründe sınırlı derecede denklem + rastgele polinomlar için de geçerli.
4. ÖLÜ DEĞİŞMEZ LİSTESİ — bunların yeni bir varyantı soru değildir, ancak aşağıdaki ilkeye uyuyorsa:
   Hessian rankı, Koszul flattening, shifted partial derivatives (Efremenko ve ark. + Hüttenhain–Lairez no-go), apolar Betti sayıları (Alper–Rowlands 2019), tekillik lokusu kodimensiyonu (ABV 2017), Milnor sayıları, immanant spektrumu, ham Berry holonomisi, ham dolaşıklık entropisi, slice rank.
5. SİMETRİ İNVERSİYONU TUZAĞI: jenerik küçük ABP'ler jenerik polinomları taklit eder. Yani jenerik noktadaki yerel değişmezler perm ile det'i AYIRMAZ. İkisi de jenerik olarak pürüzsüz, aynı Hessian profili, aynı apolar Betti sayıları, aynı kesit spektrumları.
6. TEK İLKE: tek nesneli (f'nin fonksiyonu olan) her özellik doğal ispattır. Çıkış yolu nesneyi çifte çevirmektir: (f,g) çifti, çözüm uzayı, temsiller kümesi, orbit uzaklığı, örneklem popülasyonu. Örtüşme (overlap) nicelikleri, çanak sayıları, bağlı bileşen sayıları, barkod uzunlukları bu sınıfa girer.
7. Bilinen SOTA sayıları: dc(perm_4)=15 (Sheshadri, arXiv:2611.06658, hakemsiz), codim Sing(perm_n)=n²/2 (ABV), β_{2,4}(perm_n^⊥)=2C(n,2)C(n,4) (Alper–Rowlands). Bir soru bunları aşmıyorsa ya da bunlara bağlanmıyorsa değersizdir.

## SORU FORMATI (zorunlu)
Her soru şu altı alanı doldurur:
- question (Q): tek cümlelik, EVET/HAYIR ya da monoton bir nicelik. İçinde İKİ nesne geçmeli.
- barrier_escape (NEDEN): hangi bariyeri hangi mekanizmayla atlıyor (G1–G5 kapılarına tek tek cevap).
- proxy (VEKİL): ölçülebilir hedef. Hangi kod, hangi n, kaç saat, hangi çıktı.
- prediction (ÖNGÖRÜ): işaret (perm tarafı büyük/küçük) + büyüme tahmini + görünmesi gereken n.
- falsifier (YANLIŞLAMA): hangi ölçüm sonucu soruyu öldürür. Sayı ve eşik yaz.
- prior_art (ÖNCEKİ): bu soruyu kim sordu, hangi makale, nerede tıkandı. Bilmiyorsan "bilinmiyor" yaz, uydurma.

## YASAKLAR
- "P≠NP kanıtladım" deme; her iddiayı [İSPAT] / [SAYISAL] / [HİPOTEZ] etiketle.
- Levenberg–Marquardt yakınsamasını ispat sayma; yerel minimum, küresel imkânsızlık değildir.
- Kaynaksız önceki-sonraç iddiası yazma.
- Tek nesneli değişmez önerme (İlke 6'ya uymuyorsa).
- "Şu yeni değişmez perm'i ayırıyor" cümlesini gerekçesiz kurma; jenerik noktada ayırmadığını göstermeden kabul etme.

## ÇIKTI
Sadece geçerli JSON döndür. Şema dışına çıkma. En fazla 3 soru üret. Az ve keskin, çok ve sulu değil."""

ACCEPTANCE_EXAMPLE_JSON = """{
  "id": "EX-1",
  "question": "Sabit m=14'te, perm_4'e en yakın kalıntıyı veren parametre noktalarının çanak sayısı, det_4'ünkinden üstel mi büyük?",
  "objects": ["perm_4", "det_4"],
  "barrier_escape": {
    "G1": "Nicelik katsayı vektörünün fonksiyonu değil; enerji peyzajının topolojisi, (f, m) çiftinin özelliği",
    "G2": "Cisim büyütmesi altında çanak sayısı sabit kalır (tanım gereği)",
    "G3": "Jenerik polinom da çanaklıdır; ayrım perm ile det arasında, jeneriğe karşı değil",
    "G4": "Mevcut LM altyapısı, 200 başlangıç, ~6 saat, n=4",
    "G5": "Çanak sayısı üstel ise temsiller arası geçiş maliyeti üsteldir; ara adım: bağlı bileşen sayısı -> dc"
  },
  "proxy": {"script": "lm_basins.py", "n": [3, 4], "starts": 200, "hours": 6, "output": "kalıntı histogramı + çanak kümeleme tablosu"},
  "prediction": {"sign": "perm >> det", "scaling": "exp(c*n)", "visible_at_n": 3},
  "falsifier": {"metric": "eşik altı çanak sayısı", "threshold": "perm/det < 3", "kills_if": "n=3 ve n=4'te oran 3'ün altında kalırsa"},
  "prior_art": [{"who": "depo Round 8", "where": "frustrated valley gözlemi", "stuck_at": "çanak sayısı sayılmamış, sadece kalıntı tabanı raporlanmış"}],
  "tags": ["HİPOTEZ"],
  "link_to_dc": "bileşen sayısı üstel -> temsiller arası mesafe üstel -> dc alt sınırı"
}"""

SCHEMA_TEMPLATE = """{
  "role": "<ROLE_ID>",
  "questions": [
    {
      "id": "<ROLE_ID>-Q1",
      "question": "İki nesne içeren tek cümlelik evet/hayır ya da monoton nicelik",
      "objects": ["perm_n", "det_n"],
      "barrier_escape": {"G1": "...", "G2": "...", "G3": "...", "G4": "...", "G5": "..."},
      "proxy": {"script": "...", "n": [3, 4, 5], "starts": 200, "hours": 6, "output": "..."},
      "prediction": {"sign": "perm > det", "scaling": "exp(c*n)", "visible_at_n": 4},
      "falsifier": {"metric": "...", "threshold": "...", "kills_if": "..."},
      "prior_art": [{"who": "...", "where": "...", "stuck_at": "..."}],
      "tags": ["HİPOTEZ"],
      "link_to_dc": "hangi ara adımla dc'ye bağlanıyor"
    }
  ]
}"""


def load_0g_api_key() -> str:
    if os.environ.get("0G_API_KEY"):
        return os.environ["0G_API_KEY"].strip()
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("0G_API_KEY="):
                    return line.split("=", 1)[1].strip()
    return "sk-79870bc0-1c98-411b-9131-9c42dd942a23"


def extract_json(raw: str) -> Any:
    text = raw.strip()
    if "```" in text:
        m = re.search(r"```(?:json)?\s*\n(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
        if m:
            text = m.group(1).strip()
    # Try direct parse
    try:
        return json.loads(text)
    except Exception:
        pass
    # Extract outermost {...}
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return json.loads(text[start:end + 1])
    raise ValueError(f"JSON ayıklanamadı: {text[:200]}")


def call_0g_json(system_prompt: str, user_prompt: str, temperature: float = 0.35, max_tokens: int = 4500, retries: int = 2) -> Dict[str, Any]:
    api_key = load_0g_api_key()
    models = ["0gm-1.0-35b-a3b", "0gm-1.0-35b-a3b-sia"]
    last_err = ""
    for attempt in range(retries):
        for model in models:
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
                "chat_template_kwargs": {"enable_thinking": False}
            }
            cmd = [
                "/usr/bin/curl", "-sS", "--max-time", "90",
                ROUTER_URL,
                "-H", f"Authorization: Bearer {api_key}",
                "-H", "Content-Type: application/json",
                "-H", "Accept: application/json",
                "-d", json.dumps(payload)
            ]
            try:
                res = subprocess.run(cmd, capture_output=True, text=True)
                if res.returncode != 0 or not res.stdout.strip():
                    last_err = f"curl {res.returncode}: {res.stderr[:120]}"
                    continue
                data = json.loads(res.stdout)
                if "error" in data:
                    last_err = str(data["error"])
                    continue
                msg = data["choices"][0].get("message", {})
                content = (msg.get("content") or msg.get("reasoning_content") or "").strip()
                parsed = extract_json(content)
                return parsed
            except Exception as e:
                last_err = f"{model} attempt {attempt+1}: {e}"
    raise RuntimeError(f"0G JSON call failed after retries: {last_err}")


def validate_question_obj(q: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errs = []
    for k in ("id", "question", "objects", "barrier_escape", "proxy", "prediction", "falsifier", "prior_art", "tags", "link_to_dc"):
        if k not in q or not q[k]:
            errs.append(f"eksik alan: {k}")
    if isinstance(q.get("objects"), list) and len(q["objects"]) < 2:
        errs.append("objects en az 2 nesne içermeli (İlke 6)")
    be = q.get("barrier_escape", {})
    if isinstance(be, dict):
        for g in ("G1", "G2", "G3", "G4", "G5"):
            if not be.get(g):
                errs.append(f"barrier_escape.{g} eksik")
    return (len(errs) == 0, errs)
