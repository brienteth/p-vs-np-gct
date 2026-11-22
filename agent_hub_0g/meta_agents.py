#!/usr/bin/env python3
"""
Meta-Agents Engine for 0G Agent Hub:
1. Chief Research Director (Stratejist & Görev Atayıcı)
2. Epistemic Cartographer & Auditor (Haritacı & Engel Haritası Güncelleyici)

This module handles:
- Reading the current state of ENGEL_HARITASI.md and open mathematical bottlenecks.
- Generating next-round mission assignments for the 6 council specialists.
- Evaluating council outputs, synthesizing findings, and updating ENGEL_HARITASI.md on disk.
- Writing standalone round dossiers (ROUND_XX_DOSSIER.md).
"""

import os
import sys
import time
import json
import re
from typing import Dict, List, Any, Tuple

BASE_DIR = "/Users/bl10buer/Desktop/matemk/p-vs-np-gct"
ENGEL_MAP_PATH = os.path.join(BASE_DIR, "ENGEL_HARITASI.md")
DOSSIER_DIR = os.path.join(BASE_DIR, "agent_hub_0g/dossiers")
os.makedirs(DOSSIER_DIR, exist_ok=True)

class MetaAgentDirector:
    """Chief Research Director: Assigns high-leverage targeted tasks toward the ultimate goal."""
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.name = "Prof. Henri Poincaré (Araştırma Direktörü & Stratejist)"
        self.avatar = "🧭"
        self.role = "Stratejik Görev Planlama & Hedef Yönetimi"
        self.last_briefing = "Sistem başlatıldı. Engel Haritası taranıyor."

    def generate_targeted_tasks(self, round_num: int, current_map_summary: str) -> Dict[str, Any]:
        system_prompt = (
            "Sen Prof. Henri Poincaré'sin (0G Araştırma Direktörü). Matematiksel hedefin: "
            "VP != VNP ve P != NP alanındaki kritik darboğazları (özellikle D_9^hom evrensel Koszul rank düşüşü, "
            "Grassmannian Plücker Cauchy-Binet faktörizasyonu ve sınır karmaşıklığı engelleri) adım adım çözdürmek. "
            "Engel Haritasındaki son durumu inceleyip, bu tur için genel bir hedef başlığı ve "
            "6 konsey üyesinin (Euler, Hilbert, Strassen, Noether, Wigner, Valiant) her biri için "
            "birbirini tamamlayan, matematiksel olarak somut görevler belirleyeceksin. Türkçe yanıt ver."
        )

        user_prompt = (
            f"ENGEL HARİTASI VE MEVCUT DURUM ÖZETİ:\n{current_map_summary}\n\n"
            f"GÖREV: Tur {round_num} için araştırma stratejisini kur.\n"
            "Yanıtını şu JSON formatında ver (başka hiçbir metin ekleme, yalnızca geçerli JSON):\n"
            "{\n"
            '  "topic": "Bu turun ana odak noktası",\n'
            '  "strategic_goal": "Direktörün bu turdan beklediği nihai ilerleme",\n'
            '  "agent_tasks": {\n'
            '    "prof-euler": "Euler için spesifik syzygy/ispat görevi",\n'
            '    "prof-hilbert": "Hilbert için cebirsel geometri görevi",\n'
            '    "prof-strassen": "Strassen için sınır karmaşıklığı görevi",\n'
            '    "prof-noether": "Noether için simetri/temsil görevi",\n'
            '    "prof-wigner": "Wigner için Grassmannian/matris görevi",\n'
            '    "prof-valiant": "Valiant için devre/VNP görevi"\n'
            "  }\n"
            "}"
        )

        try:
            res = self.orchestrator.call_0g_with_fallback(system_prompt, user_prompt)
            raw = res["content"].strip()
            # Clean possible markdown code fences
            if "```" in raw:
                raw = re.sub(r"^```(?:json)?\n", "", raw, flags=re.MULTILINE)
                raw = re.sub(r"\n```$", "", raw, flags=re.MULTILINE).strip()
            data = json.loads(raw)
            self.last_briefing = f"Tur {round_num}: {data.get('topic', 'Stratejik İlerleme')}"
            return data
        except Exception as e:
            # Robust fallback plan if JSON parsing fails
            fallback_topic = "D_9^hom varyetesinde evrensel Koszul corank >= 1 koşulunun cebirsel analizi"
            self.last_briefing = f"Tur {round_num} (Kural tabanlı strateji): {fallback_topic}"
            return {
                "topic": fallback_topic,
                "strategic_goal": "Hakemin işaret ettiği evrensel yok oluş boşluğunu kapatmak",
                "agent_tasks": {
                    "prof-euler": "M_8 derecesindeki syzygy modülünün serbest dereceli çözünümünü kur.",
                    "prof-hilbert": "Zariski kapanışında minor ideallerinin Hilbert serisi sürekliliğini analiz et.",
                    "prof-strassen": "Border dc için sınır dejenerasyon eğrilerinde rank kaybı alt sınırını belirle.",
                    "prof-noether": "GL_n x GL_n simetrisi altında orbit kapanışının tekil locusunu incele.",
                    "prof-wigner": "Grassmannian Plücker faktörizasyonunun n=7 için genişleme limitini test et.",
                    "prof-valiant": "VNP vs VP köprüsünde Koszul annihilatorlarının devre derinliği sınırlarını açıkla."
                }
            }


class MetaAgentCartographer:
    """Epistemic Cartographer & Map Updater: Evaluates round results, synthesizes, and updates ENGEL_HARITASI.md."""
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.name = "Prof. Alexander Grothendieck (Haritacı & Denetçi)"
        self.avatar = "🗺️"
        self.role = "Engel Haritası Güncelleme & Epistemik Sentez"
        self.last_update_summary = "Harita başlangıç durumunda yüklendi."

    def read_current_map(self) -> str:
        if os.path.exists(ENGEL_MAP_PATH):
            try:
                with open(ENGEL_MAP_PATH, "r", encoding="utf-8") as f:
                    return f.read()[:2500]
            except Exception:
                pass
        return "Harita dosyası okunamadı."

    def evaluate_and_update_map(self, round_num: int, topic: str, dialogue: List[Dict[str, Any]]) -> str:
        dialogue_text = "\n\n".join([f"### {d['agent_name']} ({d['role']}):\n{d['text']}" for d in dialogue])

        system_prompt = (
            "Sen Prof. Alexander Grothendieck'sin (0G Epistemik Haritacı ve Baş Denetçi). "
            "Görevin: 6 uzmanın bu turda ürettiği tüm teorem ve iddiaları sentezlemek, "
            "neyin tam olarak [İSPAT], neyin [KESİN HESAP], neyin [SANI] veya [AÇIK PROBLEM] olduğunu "
            "ayrıştırmak ve ENGEL HARİTASI için somut bir güncelleme raporu yazmak. "
            "Ayrıca Stratejist Direktöre bir sonraki turda hangi engelin hedeflenmesi gerektiğini bildir. Türkçe yanıt ver."
        )

        user_prompt = (
            f"TUR {round_num} KONUSU: {topic}\n\n"
            f"AJANLARIN YANITLARI:\n{dialogue_text}\n\n"
            "Lütfen şu 4 bölümden oluşan titiz bir Harita Güncelleme Raporu oluştur:\n"
            "1. 🎯 **Bu Turda Çözülen / Netleşen Ara Problemler**\n"
            "2. 🔒 **Hâlâ Açık Olan Darboğazlar & Eksik İspat Adımları**\n"
            "3. 🧭 **Direktöre Brifing (Sıradaki Tur Tavsiyesi)**\n"
            "4. 📊 **Epistemik Skor & Harita Durumu (VP!=VNP ve P!=NP İlerlemesi)**"
        )

        try:
            res = self.orchestrator.call_0g_with_fallback(system_prompt, user_prompt)
            synthesis = res["content"].strip()
        except Exception as e:
            synthesis = f"Haritacı sentez oluştururken 0G API uyarısı aldı: {e}"

        self.last_update_summary = f"Tur {round_num} Haritası Güncellendi: {synthesis[:140]}..."

        # Write to Dossier
        dossier_path = os.path.join(DOSSIER_DIR, f"ROUND_{round_num}_DOSSIER.md")
        try:
            with open(dossier_path, "w", encoding="utf-8") as f:
                f.write(f"# 📜 TUR {round_num} ARAŞTIRMA DOSYASI\n\n")
                f.write(f"**Konu:** {topic}\n")
                f.write(f"**Tarih:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("## 1. Konsey Üyelerinin Tezleri\n\n")
                f.write(dialogue_text + "\n\n")
                f.write("## 2. Haritacı & Denetçi Grothendieck'in Sentezi ve Engel Güncellemesi\n\n")
                f.write(synthesis + "\n")
        except Exception as e:
            print(f"[Cartographer] Error writing dossier: {e}")

        # Append summary to ENGEL_HARITASI.md
        try:
            append_text = (
                f"\n\n---\n\n### 📍 Tur {round_num} Harita İlerlemesi: {topic}\n"
                f"**Haritacı Grothendieck Sentezi ({time.strftime('%Y-%m-%d %H:%M')}):**\n\n"
                f"{synthesis}\n"
            )
            with open(ENGEL_MAP_PATH, "a", encoding="utf-8") as f:
                f.write(append_text)
        except Exception as e:
            print(f"[Cartographer] Error appending to ENGEL_HARITASI.md: {e}")

        return synthesis
