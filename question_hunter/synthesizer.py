#!/usr/bin/env python3
"""
KATMAN 3 — Sentezci (En fazla 3 olgun soruyu tek bir 72 saatlik araştırma programına birleştirir).
"""

import json
from typing import Dict, Any, List
from question_hunter.constitution import call_0g_json

SYNTHESIZER_SYSTEM = """ROL: Araştırma Programı Sentezcisi (Katman 3).
Görevin: Red Team'in T2 ve T4 elemesinden sağ çıkan (olgun) en fazla 3 soruyu tek bir tutarlı, 72 saatte ölçülebilir araştırma programına birleştirmek.

ZORUNLU ÇIKTI İÇERİĞİ:
1. En fazla 3 soru seç (bağımlılık sırasına diz: hangisi diğerinin önkoşulu).
2. Her biri için "yanlışsa ne kaybederiz" (risk ve bilgi kazancı) yaz.
3. Ortak vekil altyapısını tek bir Python/C/Lean 4 betik ailesi olarak tanımla.
4. İlk 72 saatte yapılacak 3 somut ölçümü, kesin KABUL ve RET eşikleriyle yaz.
5. Programın hangi noktada VP!=VNP'ye bağlandığını ve o bağın ne kadar kırılgan olduğunu dürüstçe yaz.
6. Mevcut 8 ajanlık konseyin (Euler, Hilbert, Strassen, Noether, Wigner, Valiant + Turing [Python] + Curry [Lean 4]) turlarına dahil edilecek 2-3 yeni cephe (frontier) önerisi üret.

SADECE geçerli JSON döndür."""


def synthesize_program(mature_questions: List[Dict[str, Any]], stats: Dict[str, Any]) -> Dict[str, Any]:
    user_prompt = (
        f"ELEME İSTATİSTİKLERİ:\n{json.dumps(stats, ensure_ascii=False, indent=2)}\n\n"
        f"HAYATTA KALAN / OLGUN ADAYLAR:\n{json.dumps(mature_questions, ensure_ascii=False, indent=2)}\n\n"
        "ÇIKTI ŞEMASI (SADECE GEÇERLİ JSON):\n"
        "{\n"
        '  "program_title": "...",\n'
        '  "selected_questions": [\n'
        "    {\n"
        '      "order": 1,\n'
        '      "id": "...",\n'
        '      "question": "...",\n'
        '      "prerequisite_of": ["..."],\n'
        '      "if_falsified_loss": "Yanlışsa ne kaybederiz ve ne öğreniriz",\n'
        '      "link_to_dc_or_vp_vnp": "..."\n'
        "    }\n"
        "  ],\n"
        '  "unified_proxy_suite": {\n'
        '    "family_name": "...",\n'
        '    "scripts": ["..."],\n'
        '    "shared_primitives": ["..."]\n'
        "  },\n"
        '  "first_72h_measurements": [\n'
        "    {\n"
        '      "step": 1,\n'
        '      "title": "...",\n'
        '      "hours": 8,\n'
        '      "accept_threshold": "...",\n'
        '      "reject_threshold": "...",\n'
        '      "script": "..."\n'
        "    }\n"
        "  ],\n"
        '  "vp_vnp_bridge_fragility": "Dürüst kırılganlık analizi",\n'
        '  "council_frontiers": [\n'
        "    {\n"
        '      "code": "QH-1",\n'
        '      "title": "...",\n'
        '      "goal": "...",\n'
        '      "tasks": {\n'
        '        "prof-euler": "...",\n'
        '        "prof-hilbert": "...",\n'
        '        "prof-strassen": "...",\n'
        '        "prof-noether": "...",\n'
        '        "prof-wigner": "...",\n'
        '        "prof-valiant": "...",\n'
        '        "prof-turing": "...",\n'
        '        "prof-curry": "..."\n'
        "      }\n"
        "    }\n"
        "  ]\n"
        "}"
    )
    return call_0g_json(SYNTHESIZER_SYSTEM, user_prompt, temperature=0.3, max_tokens=5000)
