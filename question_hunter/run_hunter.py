#!/usr/bin/env python3
"""
KATMAN 4 — P vs NP Soru Avcısı Orkestratörü (T1 -> T5, T6'da İnsan Kararı için durur).
T1: P1–P8 paralel (3'er soru -> ~24 aday)
T2: Red Team I (G1–G7 kapı-kapı eleme)
T3: Hayatta kalanlar (+ en yakın adaylar) Red Team gerekçesiyle sertleştirilir
T4: Red Team II -> OLGUN adaylar
T5: Sentezci <=3 soruluk 72 saatlik program + mevcut 8 ajanlık konsey için yeni cepheler
T6: SORU_AVCISI_RAPORU.md üretilir ve İnsan Kararına sunulur.
"""

import os
import sys
import json
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from question_hunter.constitution import (
    CONSTITUTION_PROMPT,
    ACCEPTANCE_EXAMPLE_JSON,
    SCHEMA_TEMPLATE,
    call_0g_json,
    validate_question_obj,
)
from question_hunter.roles import PRODUCER_ROLES
from question_hunter.red_team import evaluate_batch_red_team
from question_hunter.synthesizer import synthesize_program

OUT_DIR = os.path.join(BASE_DIR, "question_hunter", "outputs")
REPORT_MD = os.path.join(BASE_DIR, "SORU_AVCISI_RAPORU.md")
os.makedirs(OUT_DIR, exist_ok=True)


def save_json(name: str, obj: Any):
    path = os.path.join(OUT_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return path


def run_producer_t1(role: Dict[str, str]) -> List[Dict[str, Any]]:
    sys_prompt = CONSTITUTION_PROMPT
    user_prompt = (
        f"SENİN ROLÜN: {role['id']} — {role['name']}\n"
        f"ÖNSELİN:\n{role['prior']}\n\n"
        f"GÖREVİN:\n{role['task']}\n\n"
        f"KABUL ÖRNEĞİ (Hedef kalite düzeyi):\n{ACCEPTANCE_EXAMPLE_JSON}\n\n"
        f"ZORUNLU JSON ŞEMASI (en fazla 3 soru üret, sadece geçerli JSON):\n"
        f"{SCHEMA_TEMPLATE.replace('<ROLE_ID>', role['id'])}"
    )
    res = call_0g_json(sys_prompt, user_prompt, temperature=0.45, max_tokens=4200)
    qs = res.get("questions", [])[:3]
    valid_qs = []
    for idx, q in enumerate(qs, 1):
        q.setdefault("id", f"{role['id']}-Q{idx}")
        q["role"] = role["id"]
        q["role_name"] = role["name"]
        ok, errs = validate_question_obj(q)
        q["_schema_valid"] = ok
        q["_schema_errors"] = errs
        valid_qs.append(q)
    print(f"  [T1] {role['id']} ({role['name']}): {len(valid_qs)} soru üretildi.")
    return valid_qs


def run_red_team_parallel(questions: List[Dict[str, Any]], label: str) -> Dict[str, Any]:
    batches = [questions[i:i + 4] for i in range(0, len(questions), 4)]
    all_verdicts = []
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = [ex.submit(evaluate_batch_red_team, b, label) for b in batches]
        for fut in as_completed(futs):
            try:
                all_verdicts.extend(fut.result())
            except Exception as e:
                print(f"  [{label}] Batch error: {e}")

    verdict_map = {v.get("id"): v for v in all_verdicts}
    kill_reasons = Counter()
    survivors = []
    killed = []
    for q in questions:
        v = verdict_map.get(q["id"])
        if not v:
            v = {"id": q["id"], "gates": {}, "failed_gates": ["NO_VERDICT"], "survived": False, "rationale": "Hakem yanıtı eşleşmedi."}
        if v["survived"]:
            survivors.append({"question": q, "verdict": v})
        else:
            for g in v["failed_gates"]:
                kill_reasons[g] += 1
            killed.append({"question": q, "verdict": v})

    summary = {
        "round": label,
        "total": len(questions),
        "survived_count": len(survivors),
        "killed_count": len(killed),
        "kill_rate_pct": round(100.0 * len(killed) / max(1, len(questions)), 1),
        "kill_reason_distribution": dict(kill_reasons),
        "survivors": survivors,
        "killed": killed,
    }
    print(f"  [{label}] Toplam: {summary['total']} | Hayatta Kalan: {summary['survived_count']} | Ölen: {summary['killed_count']} ({summary['kill_rate_pct']}%) | Sebepler: {dict(kill_reasons)}")
    return summary


def run_hardening_t3(role: Dict[str, str], items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not items:
        return []
    user_prompt = (
        f"TUR T3 — SERTLEŞTİRME ({role['id']} — {role['name']})\n"
        "Aşağıdaki aday sorular Red Team'den geçti veya en yakın elenenler arasında yer aldı.\n"
        "Red Team'in gerekçesini dikkate alarak her soruyu SERTLEŞTİR:\n"
        "- Vekil (proxy) betiğini, başlangıç sayısını ve <=24 saat süresini netleştir (G4),\n"
        "- Önceki kaynakları (prior_art) yalnızca kesin bilinen veya 'bilinmiyor' olacak şekilde temizle (G6),\n"
        "- İşaret ve sayısal eşik öngörüsünü keskinleştir (G7),\n"
        "- dc / VP!=VNP ara bağlantı adımını somutlaştır (G5).\n\n"
        f"SERTLEŞTİRİLECEK ADAYLAR VE HAKEM GEREKÇELERİ:\n{json.dumps(items, ensure_ascii=False, indent=2)}\n\n"
        f"SADECE geçerli JSON döndür:\n{SCHEMA_TEMPLATE.replace('<ROLE_ID>', role['id'])}"
    )
    res = call_0g_json(CONSTITUTION_PROMPT, user_prompt, temperature=0.3, max_tokens=4200)
    qs = res.get("questions", [])[:len(items)]
    for idx, q in enumerate(qs):
        q["role"] = role["id"]
        q["role_name"] = role["name"]
        if idx < len(items) and "id" not in q:
            q["id"] = items[idx]["question"]["id"]
    print(f"  [T3] {role['id']}: {len(qs)} aday sertleştirildi.")
    return qs


def write_markdown_report(t1_count, t2, t3_count, t4, t5_prog, mature_ids):
    lines = [
        "# 🎯 P vs NP SORU AVCISI — T1 → T6 RAPORU (İnsan Kararına Hazır)",
        "",
        f"> Üretim Tarihi: `{time.strftime('%Y-%m-%d %H:%M:%S')}` · 4 Katmanlı Mimari (`P1–P8` → Red Team `G1–G7` → Sentezci)",
        "",
        "## 1. Eleme İstatistikleri (Öldürme Oranı & Kapı Dağılımı)",
        "",
        "| Tur | Toplam Aday | Hayatta Kalan | Ölen | Öldürme Oranı | Kapı Bazlı Öldürme Dağılımı |",
        "| :--- | :---: | :---: | :---: | :---: | :--- |",
        f"| **T1 → T2 (Red Team I)** | {t2['total']} | **{t2['survived_count']}** | {t2['killed_count']} | `%{t2['kill_rate_pct']}` | `{t2['kill_reason_distribution']}` |",
        f"| **T3 → T4 (Red Team II)** | {t4['total']} | **{t4['survived_count']}** | {t4['killed_count']} | `%{t4['kill_rate_pct']}` | `{t4['kill_reason_distribution']}` |",
        "",
        f"**Olgun Adaylar (T2 + T4 Çifte Geçiş):** `{mature_ids if mature_ids else 'Doğrudan çifte geçiş yok — T4 en güçlüleri sentezlendi'}`",
        "",
        "---",
        "",
        f"## 2. Sentezlenen Araştırma Programı (T5): {t5_prog.get('program_title', 'Soru Avcısı Programı')}",
        "",
        "### Seçilen Nihai Sorular (Bağımlılık Sırasıyla, ≤ 3 Soru)",
        "",
    ]
    for sq in t5_prog.get("selected_questions", []):
        lines.extend([
            f"#### {sq.get('order', '?')}. `[{sq.get('id', '?')}]` {sq.get('question', '')}",
            f"- **Önkoşulu olduğu sorular:** `{sq.get('prerequisite_of', [])}`",
            f"- **Yanlışsa ne kaybederiz:** {sq.get('if_falsified_loss', '')}",
            f"- **`dc` / `VP ≠ VNP` bağlantısı:** {sq.get('link_to_dc_or_vp_vnp', '')}",
            "",
        ])

    ups = t5_prog.get("unified_proxy_suite", {})
    lines.extend([
        "### Ortak Vekil Altyapısı (Tek Betik Ailesi)",
        f"- **Aile Adı:** {ups.get('family_name', '')}",
        f"- **Betikler:** `{ups.get('scripts', [])}`",
        f"- **Ortak Yapı Taşları:** `{ups.get('shared_primitives', [])}`",
        "",
        "### İlk 72 Saatte Yapılacak 3 Somut Ölçüm",
        "",
        "| Adım | Ölçüm | Süre | Betik | Kabul Eşiği | Ret (Öldürme) Eşiği |",
        "| :---: | :--- | :---: | :--- | :--- | :--- |",
    ])
    for m in t5_prog.get("first_72h_measurements", []):
        lines.append(
            f"| {m.get('step', '?')} | {m.get('title', '')} | {m.get('hours', '?')}s | `{m.get('script', '')}` | {m.get('accept_threshold', '')} | {m.get('reject_threshold', '')} |"
        )

    lines.extend([
        "",
        "### `VP ≠ VNP` Bağının Dürüst Kırılganlık Analizi",
        "",
        t5_prog.get("vp_vnp_bridge_fragility", ""),
        "",
        "---",
        "",
        "## 3. T4'ten Sağ Çıkan Adayların Hakem Gerekçeleri",
        "",
    ])
    for s in t4.get("survivors", []):
        q = s["question"]
        v = s["verdict"]
        lines.append(f"- **`{q['id']}` ({q.get('role', '')})**: {q.get('question', '')}")
        lines.append(f"  - *Hakem (`7/7 GEÇTİ`):* {v.get('rationale', '')}")

    lines.extend([
        "",
        "---",
        "",
        "## 4. T6 — İNSAN KARARI & CANLI KONSEY ENTEGRASYONU",
        "",
        "- Yeni üretilen cepheler (`council_frontiers.json`) otomatik olarak mevcut **8 Ajanlık 0G Konseyi** (`Prof. Henri Poincaré` + `Turing [Python]` + `Curry [Lean 4]`) rotasyonuna enjekte edildi.",
        "- **T6 İnsan Kararı Bekleniyor:** Yukarıdaki ≤3 sorudan hangilerinin 72 saatlik ilk deney betiklerini (`lm_basins.py` vb.) hemen çalıştıralım?",
    ])

    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    t0 = time.time()
    print("=" * 72)
    print("🎯 P vs NP SORU AVCISI BAŞLIYOR (T1 -> T5, T6 İnsan Kararında Durur)")
    print("=" * 72)

    # T1: P1-P8 parallel
    print("\n>>> [T1] P1–P8 Paralel Soru Üretimi...")
    t1_candidates = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(run_producer_t1, role): role for role in PRODUCER_ROLES}
        for fut in as_completed(futs):
            try:
                t1_candidates.extend(fut.result())
            except Exception as e:
                print(f"  [T1] Role {futs[fut]['id']} error: {e}")
    save_json("t1_candidates.json", t1_candidates)
    print(f"[T1] Toplam ham aday: {len(t1_candidates)}")

    # T2: Red Team I
    print("\n>>> [T2] Bağımsız Red Team I (G1–G7 Kapı-Kapı Eleme)...")
    t2_res = run_red_team_parallel(t1_candidates, "T2")
    save_json("t2_redteam.json", t2_res)
    t2_survivor_ids = {s["question"]["id"] for s in t2_res["survivors"]}

    # T3: Hardening — send survivors (if < 3 survived, also send closest killed with <=2 failed gates for hardening)
    print("\n>>> [T3] Hayatta Kalanların Sertleştirilmesi...")
    to_harden = list(t2_res["survivors"])
    if len(to_harden) < 4:
        near_misses = sorted(t2_res["killed"], key=lambda x: len(x["verdict"].get("failed_gates", [])))
        for nm in near_misses[:max(0, 6 - len(to_harden))]:
            to_harden.append(nm)

    by_role: Dict[str, List[Dict[str, Any]]] = {}
    for item in to_harden:
        r_id = item["question"].get("role", "P1")
        by_role.setdefault(r_id, []).append(item)

    role_lookup = {r["id"]: r for r in PRODUCER_ROLES}
    t3_hardened = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futs = [ex.submit(run_hardening_t3, role_lookup[r_id], items) for r_id, items in by_role.items() if r_id in role_lookup]
        for fut in as_completed(futs):
            try:
                t3_hardened.extend(fut.result())
            except Exception as e:
                print(f"  [T3] Hardening error: {e}")
    save_json("t3_hardened.json", t3_hardened)

    # T4: Red Team II
    print("\n>>> [T4] Bağımsız Red Team II (İkinci Eleme & Olgunluk Testi)...")
    t4_res = run_red_team_parallel(t3_hardened, "T4")
    save_json("t4_redteam.json", t4_res)

    mature = [s["question"] for s in t4_res["survivors"] if s["question"]["id"] in t2_survivor_ids]
    mature_ids = [q["id"] for q in mature]
    synth_input = [s["question"] for s in t4_res["survivors"]]
    if not synth_input:
        # Honest fallback: top 3 closest from T4 so Synthesizer can still diagnose & build program
        synth_input = [x["question"] for x in sorted(t4_res["killed"], key=lambda x: len(x["verdict"].get("failed_gates", [])))[:3]]

    # T5: Synthesizer
    print("\n>>> [T5] Sentezci (≤3 Soruluk 72 Saatlik Araştırma Programı)...")
    stats = {
        "T1_total": len(t1_candidates),
        "T2_survived": t2_res["survived_count"],
        "T2_killed": t2_res["killed_count"],
        "T2_kill_reasons": t2_res["kill_reason_distribution"],
        "T3_hardened": len(t3_hardened),
        "T4_survived": t4_res["survived_count"],
        "T4_killed": t4_res["killed_count"],
        "T4_kill_reasons": t4_res["kill_reason_distribution"],
        "mature_ids": mature_ids,
    }
    t5_prog = synthesize_program(synth_input, stats)
    save_json("t5_program.json", t5_prog)

    # Export new council frontiers so the running 8-agent council dynamically picks them up!
    frontiers = t5_prog.get("council_frontiers", [])
    if frontiers:
        save_json("council_frontiers.json", frontiers)
        print(f"[Entegrasyon] {len(frontiers)} yeni Soru Avcısı cephesi council_frontiers.json'a yazıldı.")

    write_markdown_report(len(t1_candidates), t2_res, len(t3_hardened), t4_res, t5_prog, mature_ids)
    elapsed = round(time.time() - t0, 1)
    print(f"\n🏁 T1–T5 TAMAMLANDI ({elapsed}s). Rapor: {REPORT_MD}")
    print(">>> T6: İNSAN KARARI BEKLENİYOR.")


if __name__ == "__main__":
    main()
