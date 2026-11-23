#!/usr/bin/env python3
"""
KATMAN 2 — Bağımsız Red Team Hakem Motoru (G1–G7 Kapı-Kapı Eleme).
Varsayılan karar: HAYIR / ÖLDÜR. Sadece G1–G7'nin tamamını geçen adaylar hayatta kalır.
"""

import json
from typing import Dict, Any, List
from question_hunter.constitution import call_0g_json

RED_TEAM_SYSTEM = """ROL: Bağımsız Red Team Hakemi. Üreticilerin sorularını ÖLDÜRMEK için varsayılan olarak "HAYIR / KALDI" de.
Acımasız, kuşkucu ve matematiksel olarak titizsin. Uydurma atıflara, tek-nesneli ölü değişmezlere (Hessian rank, Koszul flattening, shifted PD, apolar Betti, Sing codim, Milnor, immanant, ham Berry holonomisi, ham dolaşıklık, slice rank) ve muğlak öngörülere SIFIR tolerans göster.

Her aday soru için şu 7 kapıyı sırayla değerlendir:
- G1 DOĞAL İSPAT (RR/FSV): Nicelik katsayı vektöründen polinom zamanda mı hesaplanıyor VE rastgele polinomlar için de aynı mı? İkisi de evet ise KALDI. (Çift nesneli / çözüm uzayı topolojisi / non-large ise GEÇTİ.)
- G2 ALGEBRİZASYON: Cisim büyütmesi / oracle eklendiğinde bozuluyor mu? Bozuluyorsa KALDI.
- G3 SİMETRİ İNVERSİYONU: Jenerik küçük bir ABP aynı değeri üretiyor mu? Ayrım perm ile det arasında değil de jeneriğe karşı kurulmuşsa KALDI.
- G4 HESAPLANABİLİRLİK: n=4'te mevcut tek makinede 24 saatte gerçekten ölçülebiliyor mu? Hayırsa KALDI.
- G5 BAĞLANTI: Ölçüm sonucu dc'ye ya da VP!=VNP'ye hangi SOMUT ara adımla bağlanıyor? Ara adım yazılmamışsa veya boş laf ise KALDI.
- G6 ÖNCEKİ: Kaynak gerçek mi? Uydurma makale/atıf var mı? Şüpheli/uydurma atıf varsa KALDI. ("bilinmiyor" veya depo içi somut bulgu ise GEÇTİ.)
- G7 İŞARET: Öngörü net bir işaret (perm > det veya perm < det) ve sayısal büyüme/eşik içeriyor mu? "Farklı olacaktır" gibi muğlaksa KALDI.

KURAL: Yalnızca G1–G7'nin TAMAMINDAN (7/7) GEÇTİ alan adaylar `survived: true` olur. Tek bir KALDI bile adayı ÖLDÜRÜR (`survived: false`).
SADECE geçerli JSON döndür."""


def evaluate_batch_red_team(questions: List[Dict[str, Any]], round_label: str = "T2") -> List[Dict[str, Any]]:
    """Evaluates a batch of candidate questions (up to 4 at a time for high precision)."""
    user_prompt = (
        f"RED TEAM DEĞERLENDİRME TURU: {round_label}\n"
        f"Aşağıdaki {len(questions)} aday soruyu G1–G7 kapılarından sırayla geçir.\n\n"
        f"ADAYLAR:\n{json.dumps(questions, ensure_ascii=False, indent=2)}\n\n"
        "ÇIKTI ŞEMASI (SADECE GEÇERLİ JSON):\n"
        "{\n"
        '  "verdicts": [\n'
        "    {\n"
        '      "id": "P1-Q1",\n'
        '      "gates": {"G1": "GEÇTİ|KALDI", "G2": "GEÇTİ|KALDI", "G3": "GEÇTİ|KALDI", "G4": "GEÇTİ|KALDI", "G5": "GEÇTİ|KALDI", "G6": "GEÇTİ|KALDI", "G7": "GEÇTİ|KALDI"},\n'
        '      "failed_gates": ["G1"],\n'
        '      "survived": false,\n'
        '      "rationale": "Tek paragraflık keskin hakem gerekçesi"\n'
        "    }\n"
        "  ]\n"
        "}"
    )
    res = call_0g_json(RED_TEAM_SYSTEM, user_prompt, temperature=0.2, max_tokens=4000)
    verdicts = res.get("verdicts", [])
    # Enforce strict 7/7 rule programmatically so LLM cannot cheat!
    cleaned = []
    for v in verdicts:
        gates = v.get("gates", {})
        failed = [g for g in ("G1", "G2", "G3", "G4", "G5", "G6", "G7") if str(gates.get(g, "KALDI")).upper().strip() != "GEÇTİ"]
        v["failed_gates"] = failed
        v["survived"] = (len(failed) == 0)
        cleaned.append(v)
    return cleaned
