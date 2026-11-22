#!/usr/bin/env python3
"""
9-Tur KİLİT SORU Protokolü (H1 -> H6) — 0G Otonom Konsey Özel Görevi.
Tamamlandığında (Tur 9 - KAPANIŞ & KARAR) kontrolü otomatik olarak
Prof. Henri Poincaré (0G Otonom Görev Atayıcı)'ya geri devreder.
"""

import os
import json
import time
from typing import Dict, List, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_FILE = os.path.join(BASE_DIR, "agent_hub_0g", "kilit_soru_state.json")
REPORT_MD = os.path.join(BASE_DIR, "KILIT_SORU_9_TUR_RAPORU.md")
ENGEL_MAP_PATH = os.path.join(BASE_DIR, "ENGEL_HARITASI.md")

KILIT_SORU_TEXT = """KİLİT SORU:
NP'deki bir dili P'deki herhangi bir dilden ayıran bir ÖZELLİK (DEĞİŞMEZ) adı verin — öyle ki bu özellik:
 (i)   girdi boyutunda polinom zamanda hesaplanabilsin,
 (ii)  bir oracle eklendiğinde bozulmasın (relativizasyon),
 (iii) 'büyük' olsun: NP dilinin tüm küçük devreleri onu taşısın, P'dekiler taşımasın,
 (iv)  ve doğal ispatlar anlamında 'doğal' olmasın — yani büyüklüğü kolayca kanıtlanamasın.
Adı verilen özellik bir alan adı değil, bir DEĞİŞMEZ olacak: nesnelere (dil, devre ailesi, fonksiyon) atanan ve hesaplanabilir bir büyüklük.

YASAKLAR:
- Y1: "Cebirsel geometri", "devre karmaşıklığı", "kombinatorik" gibi alan adları cevap değildir. Alan adı veren ajan, aynı turda değişmezi de yazmak zorunda.
- Y2: "Diagonalizasyon", "alt sınır", "kanıt karmaşıklığı" gibi şemsiye terimler tek başına cevap değildir.
- Y3: Üç bariyerden hangisine çarptığı söylenmeyen aday kabul edilmez.
- Y4: Hesaplanabilirlik iddiası, hesaplama yöntemi yazılmadan geçerli değildir."""

STEPS_META = {
    1: ("H1 — ÇOĞALTMA (Protokol Tur 1/9)", "Her ajan kendi alanından (i)–(iv) koşullarını karşıladığını düşündüğü BENZERSİZ BİR değişmez önerir."),
    2: ("H2 — ÇAPRAZ KIRMA I (Protokol Tur 2/9)", "Her ajan KENDİSİNİN OLMADIĞI bir adayı seçip (i)–(iv) koşullarından hangisinde kırıldığını göstererek çürütür. Kendi adayını savunmak YASAKTIR."),
    3: ("H2 — ÇAPRAZ KIRMA II (Protokol Tur 3/9)", "İkinci çapraz kırma dalgası: ilk turda ayakta kalan adaylara en sert karşı-örneklerle saldırı. Kendi adayını savunmak YASAKTIR. Ayakta kalanlar H3'e geçer."),
    4: ("H3 — BİRLEŞTİRME I (Protokol Tur 4/9)", "Ayakta kalan adayların ORTAK ÇEKİRDEĞİ çıkarılır; hepsinde bulunan tek yapısal unsur aranır, gereksiz süs atılır."),
    5: ("H3 — BİRLEŞTİRME II (Protokol Tur 5/9)", "Ortak çekirdek tek bir değişmeze indirgenir. Tek aday oluşmazsa en güçlü 2 adayla devam edilip 'BİRLEŞMEDİ' kaydı düşülür."),
    6: ("H4 — BARİYER TESTİ I: Relativizasyon & Doğal İspatlar (Protokol Tur 6/9)", "Kalan aday(lar)a sırayla Relativizasyon ve Doğal İspatlar bariyerleri uygulanır; kapsama giriyorsa dışarı taşıyan ek bileşen, girmiyorsa kesin kanıtı yazılır."),
    7: ("H4 — BARİYER TESTİ II: Cebirleştirme & Eleme (Protokol Tur 7/9)", "Cebirleştirme (Algebrization) bariyeri uygulanır ve 3 bariyer bilançosu çıkarılır. 3 bariyerden 2'sinden geçemeyen elenir; hepsi elenirse 'BARİYER DUVARI' kaydı düşülür."),
    8: ("H5 — DOĞRULAMA TESTİ: PARITY ∉ AC⁰ (Protokol Tur 8/9)", "Kalan aday bilinen PARITY ∉ AC⁰ ayrımında sınanır. Yeniden üretemiyorsa 'boş' işaretlenip hangi ek koşulla yakalayacağı yazılarak düzeltilir."),
    9: ("H6 — KAPANIŞ VE NİHAİ KARAR (Protokol Tur 9/9)", "Tek sayfa kapanış: nihai aday, hesaplama yöntemi, 3 bariyer durumu, PARITY testi, P≠NP'ye uzanan tek somut sonuç, KARAR (ADAY VAR / YAKIN / BOŞ / ÇIKMAZ) ve 'bu adayı kırmak için gereken tek deney'.")
}


class KilitSoruProtocol:
    def __init__(self):
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"active": False, "step": 1, "history": []}

    def _save_state(self):
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[KilitSoru] State save error: {e}")

    def is_active(self) -> bool:
        self.state = self._load_state()
        return bool(self.state.get("active", False)) and int(self.state.get("step", 1)) <= 9

    def _build_history_digest(self) -> str:
        hist = self.state.get("history", [])
        if not hist:
            return "(Henüz önceki tur yok — bu Protokol Tur 1/9.)"
        parts = []
        for h in hist[-4:]:
            parts.append(f"=== {h['header']} ===\n{h['summary'][:1800]}")
        return "\n\n".join(parts)

    def _build_agent_prompt(self, step: int, agent: Dict[str, Any], round_dialogue: List[Dict[str, Any]]) -> str:
        header, desc = STEPS_META[step]
        hist_digest = self._build_history_digest()
        same_round_so_far = "\n".join(
            [f"- {d['agent_name']}: {d['text'][:320]}" for d in round_dialogue]
        ) or "(Bu turun ilk konuşmacısısın.)"

        if step == 1:
            specific = (
                "H1 — ÇOĞALTMA GÖREVİN:\n"
                "Kendi uzmanlık alanından KİLİT SORU'nun (i)–(iv) koşullarını karşıladığını düşündüğün "
                "TEK BİR SOMUT DEĞİŞMEZ öner. TEK PARAGRAF (120–180 kelime) yaz:\n"
                "1) Değişmezin kesin adı ve matematiksel tanımı,\n"
                "2) Girdi boyutunda polinom zamanda hesaplama yöntemi (Y4 zorunlu),\n"
                "3) Üç bariyerden hangisine çarpabileceğini (Y3 zorunlu) ve hangi bariyeri neden aştığını belirt.\n"
                "Önceki konuşmacıların önerdiği adaylarla ÇAKIŞMA! Alan adı/şemsiye terim yasak (Y1, Y2)."
            )
        elif step in (2, 3):
            specific = (
                f"{header} GÖREVİN:\n"
                "KENDİ ÖNERMEDİĞİN (başka bir ajanın önerdiği) BİR adayı açıkça adını ve sahibini yazarak seç.\n"
                "Bu adayı (i), (ii), (iii) veya (iv) koşullarından hangisinde kırdığını somut matematiksel argümanla göstererek ÇÜRÜT.\n"
                "YASAK: Bu turda KENDİ adayını savunma! Yalnızca başka bir adayı kırmaya odaklan (120–180 kelime)."
            )
        elif step in (4, 5):
            specific = (
                f"{header} GÖREVİN:\n"
                "H2'den ayakta kalan adayların ORTAK YAPISAL ÇEKİRDEĞİNİ çıkar.\n"
                "Hepsinde bulunan tek yapısal unsuru somut formülle yaz, gereksiz süsleri at. "
                "Ortak çekirdek yoksa en az iki adayı tek bir üst değişmezde birleştir. "
                "Tur 5 sonunda tek aday oluşmuyorsa 'BİRLEŞMEDİ' diyerek en güçlü 2 adayı netleştir (130–180 kelime)."
            )
        elif step == 6:
            specific = (
                "H4 — BARİYER TESTİ I GÖREVİN:\n"
                "Kalan aday(lar)a sırayla (1) RELATİVİZASYON ve (2) DOĞAL İSPATLAR bariyerlerini uygula.\n"
                "Her biri için net hüküm ver: 'Kapsamına GİRİYOR (dışarı taşıyan ek bileşen: ...)' veya "
                "'Kapsamına GİRMİYOR (kanıt: ...)' (130–180 kelime)."
            )
        elif step == 7:
            specific = (
                "H4 — BARİYER TESTİ II GÖREVİN:\n"
                "Kalan aday(lar)a (3) CEBİRLEŞTİRME (Algebrization) bariyerini uygula ve 3 bariyerin nihai geçiş puanını (X/3) ver.\n"
                "3 bariyerden 2'sinden geçemeyen adayı ELE. Hepsi eleniyorsa 'BARİYER DUVARI' yazıp H5'e taşınacak en yakın adayı seç (130–180 kelime)."
            )
        elif step == 8:
            specific = (
                "H5 — DOĞRULAMA TESTİ (PARITY ∉ AC⁰) GÖREVİN:\n"
                "Kalan nihai adayı bilinen PARITY ∉ AC⁰ ayrımında test et.\n"
                "Aday PARITY için yüksek/taşıyan, AC⁰ devreleri için düşük/taşımayan değer üretiyor mu? Somut hesapla göster.\n"
                "Üretemiyorsa adayı 'BOŞ' işaretle ve 'Hangi ek koşulla PARITY/AC⁰ vakasını yakalar?' sorusunu yanıtlayarak adayı düzelt (130–190 kelime)."
            )
        else:
            specific = (
                "H6 — KAPANIŞ (TUR 9) GÖREVİN:\n"
                "Nihai aday hakkında kendi uzmanlık açından son karar oyunu ver:\n"
                "- Nihai değişmez ve hesaplama yöntemi,\n"
                "- 3 bariyere karşı durum + PARITY testi sonucu,\n"
                "- P≠NP'ye uzanan TEK somut sonuç,\n"
                "- KARAR (ADAY VAR / YAKIN / BOŞ / ÇIKMAZ),\n"
                "- 'Bu adayı kırmak için gereken tek deney' (130–190 kelime)."
            )

        return (
            f"{KILIT_SORU_TEXT}\n\n"
            f"MEVCUT HAREKET: {header}\n"
            f"HAREKET KURALI: {desc}\n\n"
            f"ÖNCEKİ TURLARIN ÖZETİ:\n{hist_digest}\n\n"
            f"BU TURDA SENDEN ÖNCE KONUŞANLAR:\n{same_round_so_far}\n\n"
            f"SEN ({agent['name']} — {agent['role']}):\n{specific}\n"
            "Türkçe, net, somut ve yasaklara (Y1–Y4) %100 uyarak yanıt ver."
        )

    def _build_cartographer_prompt(self, step: int, dialogue_text: str) -> str:
        header, _ = STEPS_META[step]
        if step < 9:
            return (
                f"MEVCUT HAREKET: {header}\n\n"
                f"6 AJANIN BU TURDAKİ KATKILARI:\n{dialogue_text}\n\n"
                "GÖREVİN (HARİTACI Prof. Alexander Grothendieck):\n"
                "Kesin çıktı formatına uy:\n"
                "1) Tam olarak 4 SATIR yaz: sadece ayakta kalan aday sayısı/adları ve hangi bariyerde nerede durulduğu.\n"
                "2) 5. satırda mutlaka 'DURUM: ...' satırını yaz.\n"
                "Uzun giriş-çıkış cümleleri yazma, doğrudan 4 satır + DURUM satırı ver."
            )
        else:
            return (
                f"MEVCUT HAREKET: {header} (FİNAL TURU 9/9)\n\n"
                f"6 AJANIN FİNAL KATKILARI:\n{dialogue_text}\n\n"
                f"ÖNCEKİ TURLAR:\n{self._build_history_digest()}\n\n"
                "GÖREVİN (HARİTACI Prof. Alexander Grothendieck — TEK SAYFA KAPANIŞ VE KARAR):\n"
                "Şu başlıkları eksiksiz doldurarak tek sayfalık nihai raporu yaz:\n"
                "1. **NİHAİ ADAY (DEĞİŞMEZ):** Adı ve tanımı\n"
                "2. **HESAPLAMA YÖNTEMİ:** Polinom zamanlı hesaplama algoritması\n"
                "3. **ÜÇ BARİYERE KARŞI DURUM:** Relativizasyon / Doğal İspatlar / Cebirleştirme (X/3 geçti)\n"
                "4. **PARITY ∉ AC⁰ DOĞRULAMA TESTİ SONUCU:** Geçti / Boş + düzeltme\n"
                "5. **P ≠ NP'YE UZANAN TEK SOMUT SONUÇ:**\n"
                "6. **KARAR:** [ADAY VAR | YAKIN | BOŞ | ÇIKMAZ] — ölçüt gerekçesiyle\n"
                "7. **BU ADAYI KIRMAK İÇİN GEREKEN TEK DENEY:**\n"
                "8. **HARİTACI RAPORU (4 satır) + DURUM satırı.**"
            )

    def execute_step(self, orchestrator, global_round_num: int):
        step = int(self.state.get("step", 1))
        header, desc = STEPS_META[step]

        if step == 1 and not os.path.exists(REPORT_MD):
            with open(REPORT_MD, "w", encoding="utf-8") as f:
                f.write("# 🔐 KİLİT SORU — 9 TURLUK BİLİMSEL ELEME PROTOKOLÜ (H1 → H6)\n\n")
                f.write(f"> Başlangıç: `{time.strftime('%Y-%m-%d %H:%M:%S')}` · 0G Otonom Konsey\n\n")
                f.write("```\n" + KILIT_SORU_TEXT + "\n```\n\n")

        # Emit Director / Movement header
        orchestrator.emit_log({
            "type": "director_briefing",
            "round": global_round_num,
            "director_name": f"🔐 KİLİT SORU PROTOKOLÜ · {header}",
            "avatar": "🎯",
            "topic": f"[KİLİT SORU {step}/9] {header}",
            "strategic_goal": desc,
            "text": f"🎯 **{header}** (Global Tur {global_round_num})\n**Kural:** {desc}"
        })

        for a in orchestrator.agents:
            orchestrator.agent_statuses[a["id"]]["status"] = "waiting"

        round_dialogue: List[Dict[str, Any]] = []
        for agent in orchestrator.agents:
            if orchestrator._stop_event.is_set():
                return
            orchestrator._pause_event.wait()

            orchestrator.active_agent_id = agent["id"]
            orchestrator.agent_statuses[agent["id"]]["status"] = "thinking"

            prompt = self._build_agent_prompt(step, agent, round_dialogue)
            try:
                t0 = time.time()
                res = orchestrator.call_0g_with_fallback(agent["system"], prompt)
                duration = time.time() - t0

                orchestrator.stats["total_calls"] += 1
                orchestrator.stats["total_tokens"] += res["tokens"]
                orchestrator.stats["total_cost_micro_usd"] += res["cost_micro"]
                orchestrator.stats["last_active"] = time.strftime("%Y-%m-%d %H:%M:%S")

                orchestrator.agent_statuses[agent["id"]]["status"] = "responded"
                orchestrator.agent_statuses[agent["id"]]["last_thought"] = res["content"][:200] + "..."
                orchestrator.agent_statuses[agent["id"]]["model"] = res["model"]
                orchestrator.agent_statuses[agent["id"]]["last_time"] = time.strftime("%H:%M:%S")

                prev_name = round_dialogue[-1]["agent_name"] if round_dialogue else None
                orchestrator.emit_log({
                    "type": "agent_message",
                    "round": global_round_num,
                    "agent_id": agent["id"],
                    "agent_name": agent["name"],
                    "avatar": agent["avatar"],
                    "role": agent["role"],
                    "reply_to": prev_name,
                    "model": res["model"],
                    "tokens": res["tokens"],
                    "cost_micro": res["cost_micro"],
                    "duration_sec": round(duration, 2),
                    "text": res["content"]
                })
                round_dialogue.append({
                    "agent_name": agent["name"],
                    "avatar": agent["avatar"],
                    "role": agent["role"],
                    "model": res["model"],
                    "text": res["content"]
                })
                time.sleep(1.5)
            except Exception as e:
                orchestrator.stats["error_count"] += 1
                orchestrator.agent_statuses[agent["id"]]["status"] = "error"
                orchestrator.emit_log({
                    "type": "error",
                    "round": global_round_num,
                    "agent_id": agent["id"],
                    "text": f"⚠️ Protokol Tur {step} Hatası ({agent['name']}): {e}"
                })
                time.sleep(2)

        orchestrator.active_agent_id = None

        # Cartographer 4-line report (or final Turn 9 closing & KARAR)
        dialogue_text = "\n\n".join(
            [f"### {d['avatar']} {d['agent_name']} ({d['role']}):\n{d['text']}" for d in round_dialogue]
        )
        carto_sys = (
            "Sen Prof. Alexander Grothendieck'sin (HARİTACI). "
            "KİLİT SORU 9-Tur protokolünün hakemi ve kaydedicisisin. "
            "Y1–Y4 yasaklarına uymayan adayları acımasızca elersin. Türkçe yaz."
        )
        carto_prompt = self._build_cartographer_prompt(step, dialogue_text)
        try:
            carto_res = orchestrator.call_0g_with_fallback(carto_sys, carto_prompt)
            carto_text = carto_res["content"].strip()
        except Exception as e:
            carto_text = f"HARİTACI uyarısı: {e}\nDURUM: Tur {step} tamamlandı."

        orchestrator.cartographer.last_update_summary = f"[KİLİT SORU {step}/9] {carto_text[:150]}"
        orchestrator.emit_log({
            "type": "cartographer_update",
            "round": global_round_num,
            "cartographer_name": orchestrator.cartographer.name,
            "avatar": orchestrator.cartographer.avatar,
            "text": f"🗺️ **HARİTACI RAPORU ({header}):**\n{carto_text}"
        })

        # Append to dedicated KILIT_SORU_9_TUR_RAPORU.md
        try:
            with open(REPORT_MD, "a", encoding="utf-8") as f:
                f.write(f"\n---\n\n## {header} · `{time.strftime('%Y-%m-%d %H:%M:%S')}`\n\n")
                f.write(dialogue_text + "\n\n")
                f.write(f"### 🗺️ HARİTACI RAPORU (Tur {step}/9)\n\n{carto_text}\n")
        except Exception as e:
            print(f"[KilitSoru] Report write error: {e}")

        # Update state & history
        compact_summary = "\n".join(
            [f"- {d['agent_name']}: {d['text'][:240]}" for d in round_dialogue]
        ) + f"\n\nHARİTACI:\n{carto_text}"
        self.state.setdefault("history", []).append({
            "step": step,
            "header": header,
            "summary": compact_summary
        })

        if step >= 9:
            self.state["active"] = False
            self.state["step"] = 10
            self.state["completed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            # Record final KARAR into ENGEL_HARITASI.md so Poincaré uses it next!
            try:
                with open(ENGEL_MAP_PATH, "a", encoding="utf-8") as f:
                    f.write(f"\n\n---\n\n## 🏆 KİLİT SORU 9-TUR PROTOKOLÜ FİNAL KARARI ({time.strftime('%Y-%m-%d %H:%M')})\n\n")
                    f.write(carto_text + "\n")
            except Exception:
                pass
            orchestrator.emit_log({
                "type": "system",
                "round": global_round_num,
                "text": "🏁 9 Turluk KİLİT SORU Protokolü (H1→H6) TAMAMLANDI! Rapor KILIT_SORU_9_TUR_RAPORU.md ve ENGEL_HARITASI.md'ye işlendi. Kontrol tekrar Prof. Henri Poincaré (0G Otonom Görev Atayıcı)'ya devredildi."
            })
        else:
            self.state["step"] = step + 1

        self._save_state()
        orchestrator.stats["successful_rounds"] += 1
        orchestrator.emit_log({
            "type": "round_end",
            "round": global_round_num,
            "text": f"✅ KİLİT SORU PROTOKOLÜ TUR {step}/9 ({header}) TAMAMLANDI."
        })
