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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGEL_MAP_PATH = os.path.join(BASE_DIR, "ENGEL_HARITASI.md")
DOSSIER_DIR = os.path.join(BASE_DIR, "agent_hub_0g/dossiers")
os.makedirs(DOSSIER_DIR, exist_ok=True)

FRONTIER_STAGES = [
    {
        "code": "E3.11",
        "title": "m=12 için dc(perm_4) >= 13 Kapanışı: D=9 ⊂ H_{<=4} ve D=8 ⊂ H_{<=6} İdeal Elemesi",
        "goal": "m=12 determinantal boyutunda kalan son iki tekil alt-durumu küresel Macaulay/Koszul idealiyle eleyip dc(perm_4) >= 13 alt sınırını kesinleştirmek.",
        "tasks": {
            "prof-euler": "D=8 ⊂ H_{<=6} için 4x4 minör idealinin derece-8 syzygy matrisini ve minimum Betti sayılarını kur.",
            "prof-hilbert": "m=12'de D=9 ⊂ H_{<=4} bileşenlerinin Hilbert fonksiyonu h(d) büyümesini ve codim >= 10 koşulunu analiz et.",
            "prof-strassen": "m=12'deki 56 normal-form konfigürasyonunda D=8 ve D=9 için çarpık-kare (skew-square) rank kaybı sınırını hesapla.",
            "prof-noether": "H_{<=6} üzerinde GL_4 x GL_4 simetri yörüngelerinin stabilizer boyutlarını ve tekil locus ayrışımını belirle.",
            "prof-wigner": "m=12 kesitlerinde F_p modüler rank matrislerinin spektral boşluğunu ve karakter-0 aktarım şartını incele.",
            "prof-valiant": "dc(perm_4) >= 13 geçişinin n=5 kalıcı polinomu için determinantal karmaşıklık büyüme üssüne etkisini hesapla."
        }
    },
    {
        "code": "E4.6",
        "title": "L_10 Üzerinde Kök-Almasız Sınır Polinomu R_11^(4) ve perm_5 Korank r ∈ {2,3,4} Kapanışı",
        "goal": "border-dc(perm_4) >= 12 için L_10 kesitinde polinomsal sınır engelini (R_11^(4)) inşa etmek ve perm_5'te r ∈ {2,3,4} korank dallarını kapatmak.",
        "tasks": {
            "prof-euler": "R_11^(4)(F) = P^(4) T^(4) Q^(4) sınır polinomunun L_10 üzerinde sıfırlanma özdeşliğini ve derecesini ispatla.",
            "prof-hilbert": "L_10 ⊂ C^16 kesitinde derece-6 rankı 3206/5005'ten derece-9 tam ranka geçiş için ideal üreteç eksikliğini tespit et.",
            "prof-strassen": "perm_5 için r=2,3,4 koranklı sınır dejenerasyon eğrilerinde (Atkinson–Dieudonné kalemleri) minimal rank düşüşünü çıkar.",
            "prof-noether": "perm_5'in (A_11^3 K)^T = -A_11^3 K anti-simetri yapısının r ∈ {2,3,4} yörüngelerinde nasıl kırıldığını göster.",
            "prof-wigner": "R_11^(4)(perm_4) mod 32749 ve mod 65521 değerlendirmesinde sıfırdan farklılık olasılığını ve minör yapısını analiz et.",
            "prof-valiant": "border-dc(perm_4) >= 12 sonucunun VP vs VNP ayrımında sınır devreleri (border circuits) açısından anlamını formüle et."
        }
    },
    {
        "code": "E2.6",
        "title": "n=5 Hiperçizge Deficit Handshaking (w_1=6, w_2 ∈ {8,9}) ve Çift-Taraflı Laurent Banyosu",
        "goal": "perm_5 için m=29,30 durumlarını kapatıp m >= 31 = 2^5 - 1 sınırını tamamlamak ve genel (k_r, k_c) Laurent rank eşitsizliğini kanıtlamak.",
        "tasks": {
            "prof-euler": "w_1=6, a=(2,1,1,1,1) ve w_2 ∈ {8,9} hiperçizge konfigürasyonlarının çelişkiye götüren kombinatoryal ispatını kur.",
            "prof-hilbert": "kofaktör kombinasyonu F_c(Y) = sum c_j perm_4^(r,j)(Y) için str(F_c) = 4 korumasının projektif geometrik yorumunu ver.",
            "prof-strassen": "İki-taraflı T_4 kırılmasında sahte sütun-kutbu t^7656'nın perm_4'te biriktirdiği 3+3 rank fazlalığını genel (k_r, k_c)'ye genelle.",
            "prof-noether": "Torus simetrisi kırılmasında Laurent serisi katsayılarının ağırlık uzayı ayrışımını ve (k_r, k_c) alt sınırını türet.",
            "prof-wigner": "w_2=8,9 çizge ailelerinde mod 32749 Hessian ranklarının rastgele matris eşiğinden sapmasını hesapla.",
            "prof-valiant": "m >= 2^n - 1 hiperçizge alt sınırının genel n için üstel determinantal karmaşıklığa tümevarım engelini açıkla."
        }
    },
    {
        "code": "E5.6",
        "title": "Mod-3 Grassmannian Gr(<=2, n, F_3) Tavanı ve Mod_3 L vs Mod_3 P Devre Kaldırması",
        "goal": "Evrensel 55/55 kesit rk_F2([perm_4!=0 mod 3]) > rk_F2([det_4!=0 mod 3]) ayrımını n>=5 için Mod_3 L vs Mod_3 P devre alt sınırına kaldırmak.",
        "tasks": {
            "prof-euler": "Cauchy–Binet Plücker faktörizasyonundan doğan |Gr_{0,1}(k,n,F_3)| tavanının det_n için kesin üst sınır kanıtını genişlet.",
            "prof-hilbert": "F_3 üzerindeki Grassmannian varyetesinin Plücker gömmesinde kalıcı polinomun (perm_n) neden bu tavandan taştığını açıkla.",
            "prof-strassen": "n=5 için 247 vs 40 (6.18x) ve 760 vs 334 (2.28x) rk_F2 uçurumunun iletişim matrisi tensör rankıyla ilişkisini kur.",
            "prof-noether": "F_3^n üzerinde GL(n, F_3) eyleminin det_n çekirdeğini korurken perm_n'de S_n x S_n'e indirgenmesinin rank etkisini analiz et.",
            "prof-wigner": "3-parti NOF iletişim karmaşıklığında discrepancy başarısızlığını aşıp rk_F2 kaldırması (lifting) için yeni norm öner.",
            "prof-valiant": "Mod_3 L vs Mod_3 P ayrımının log-uzay ve polinomsal zaman (NL vs P / #P) hiyerarşisindeki yerini netleştir."
        }
    },
    {
        "code": "E6.6",
        "title": "n=5 Yörünge-LP İnvaryantı ve Çok-Yönlü TC^0_3 (THR ∘ THR) İletişim Karmaşıklığı",
        "goal": "D_PTF(5) >= 10 bariyerini aşarak det_5 ile perm_5'i ayıran gerçek yörünge-LP invaryantını ve birleşik THR ∘ THR ağırlık sınırını bulmak.",
        "tasks": {
            "prof-euler": "Cauchy–Schwarz yörünge-içi varyans sönümleme sınırını (<mu, F h_bar> <= sqrt(1 - E[Var])) derinlik-3 eşik devrelere genişlet.",
            "prof-hilbert": "span(THR_{0,1,<=D}) == span(AND_{<=D}) teoreminin (Teorem 23.1) n=5'te 5,624 yörünge politopları üzerindeki geometrisini incele.",
            "prof-strassen": "Genişlik <=2,3,4 için korunan 1.855x ağırlık oranının (164.24 vs 93.20) asimptotik büyüme hızını tahmin et.",
            "prof-noether": "S_5 x S_5 yörünge ortalamasının perm_5 ve det_5 için farklı spektral momentler ürettiği en düşük dereceyi bul.",
            "prof-wigner": "Tek-yönlü THR ∘ THR'nin derinlik-2'ye çöküşü (4.53e-13) karşısında çok-yönlü eşik kapılarının rastgele işaret dağılımını modelle.",
            "prof-valiant": "TC^0_3 alt sınırlarının (MAJ ∘ THR ve THR ∘ THR) P != NP yolundaki doğal ispatlar engeline takılıp takılmadığını denetle."
        }
    },
    {
        "code": "GCT-MULT",
        "title": "Mulmuley–Sohoni GCT: Occurrence Engellerinin Ötesinde Multiplicity (Kronecker & Plethysm) Pozitifliği",
        "goal": "Bürgisser–Ikenmeyer–Panova'nın occurrence obstruction imkânsızlığını aşan kesin Kronecker/plethysm çokluk (multiplicity) ayrımını kurmak.",
        "tasks": {
            "prof-euler": "det_m ile padded perm_n koordinat halkalarındaki g(lambda, mu, nu) Kronecker katsayıları için somut çokluk farkı (multiplicity gap) adayı kur.",
            "prof-hilbert": "SL_m^2-invaryant halkası C[End(C^m)] üzerindeki yüksek dereceli bileşenlerin (highest weight vectors) ideal üyeliğini incele.",
            "prof-strassen": "Sınır karmaşıklığında multiplicity obstruction'ın tensör rankı ve border rank alt sınırlarıyla bağını göster.",
            "prof-noether": "Weyl modülleri S_lambda(C^m) ⊗ S_lambda(C^m) ayrışımında plethysm katsayılarının p(n, d, lambda) asimptotik büyümesini karşılaştır.",
            "prof-wigner": "Büyük n limitinde Kronecker katsayılarının rasgele Young diyagramları (Plancherel ölçüsü) altındaki yoğunluğunu hesapla.",
            "prof-valiant": "Multiplicity obstruction'ın hesaplanabilirliğinin (P vs #P-tamlık) GCT programının kendi karmaşıklık bariyerine etkisini tartış."
        }
    },
    {
        "code": "BARRIER-NP",
        "title": "Razborov–Rudich Doğal İspatlar, Relativizasyon ve Cebirselleştirme Bariyerlerinin Aşılması",
        "goal": "Cebirsel geometri ve GCT tabanlı engellerin neden Doğal İspatlar (Natural Proofs) bariyerine takılmadığını ve P != NP geçiş şartlarını netleştirmek.",
        "tasks": {
            "prof-euler": "Determinantal varyete ideal üyeliğinin 'largeness' (büyüklük) koşulunu nasıl ihlal ettiğini (sıfır ölçülü cebirsel küme) biçimsel olarak ispatla.",
            "prof-hilbert": "Zariski kapalı ve düşük boyutlu yörünge kapanışlarının rastgele polinomlardan (yoğun açık küme) yapısal ayrımını formüle et.",
            "prof-strassen": "Cebirsel devre alt sınırlarının (VP != VNP) Boolean devre alt sınırlarına (P/poly != NP) aktarılmasındaki aktarım engelini analiz et.",
            "prof-noether": "Grup simetrisi (GL_n, S_n) ile tanımlı özelliklerin kriptografik sözde-rastgele fonksiyonları (PRF) neden ayıramadığını incele.",
            "prof-wigner": "Williams'ın NEXP not in ACC^0 (algoritmik yöntem) tekniği ile mod-3 Grassmannian rank ayrımının birleştirilebilirliğini değerlendir.",
            "prof-valiant": "VP != VNP'den P != NP'ye (veya #P != FP'ye) geçişte Blum–Shub–Smale (BSS) modeli ile Turing makinesi arasındaki boşluğu somutlaştır."
        }
    },
    {
        "code": "ASYMP-N",
        "title": "Sabit n=4 Sertifikalarından Asimptotik n -> ∞ Süper-Polinomsal Alt Sınıra Tümevarım Şeması",
        "goal": "n=4'te elde edilen kesin C motoru ve Koszul sertifikalarını genel n >= 5 için süper-polinomsal m(n) = n^omega(1) alt sınırına taşıyacak tümevarım adımını kurmak.",
        "tasks": {
            "prof-euler": "n -> n+1 blok-genişletme (block-padding) altında syzygy ve Koszul ideal boyutunun tümevarımlı büyüme bağıntısını yaz.",
            "prof-hilbert": "Shifted partial derivatives (Kayal–Saha–Saptharishi) yöntemi ile Koszul annihilator yönteminin asimptotik gücünü karşılaştır.",
            "prof-strassen": "Süper-polinomsal border-dc(perm_n) alt sınırı için gereken minimal monom derecesi D(n) ve kesit boyutu L(n) ölçeklenmesini hesapla.",
            "prof-noether": "n büyürken S_n x S_n indirgenemez temsillerinin boyut artışının hangi adımda m(n) >= n^2'yi (Mignon–Ressayre sınırı) aştığını belirle.",
            "prof-wigner": "Mignon–Ressayre n^2/2 kuadratik sınırını aşmak için Hessian'ın ötesinde 3. ve 4. derece yüksek-türev tensörlerinin rank spektrumunu incele.",
            "prof-valiant": "n=4 ve n=5'ten genel n'e sıçrayabilmek için hangi tek kritik teoremin (ana darboğaz) kırılması gerektiğini 3 somut maddeyle özetle."
        }
    }
]


class MetaAgentDirector:
    """Chief Research Director: Assigns high-leverage targeted tasks toward the ultimate goal."""
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.name = "Prof. Henri Poincaré (Araştırma Direktörü & Stratejist)"
        self.avatar = "🧭"
        self.role = "Stratejik Görev Planlama & Hedef Yönetimi"
        self.last_briefing = "Sistem başlatıldı. Engel Haritası taranıyor."

    def generate_targeted_tasks(self, round_num: int, current_map_summary: str, recent_topics: List[str] = None) -> Dict[str, Any]:
        stage = FRONTIER_STAGES[round_num % len(FRONTIER_STAGES)]
        recent_str = "\n".join([f"- {t}" for t in (recent_topics or [])[-8:]]) or "(Yok)"

        system_prompt = (
            "Sen Prof. Henri Poincaré'sin (0G Araştırma Direktörü). Matematiksel hedefin: "
            "VP != VNP ve P != NP yolundaki FARKLI ve SOMUT açık engelleri (E3.11, E4.6, E2.6, E5.6, E6.6, "
            "Kronecker/Plethysm çokluk engelleri, Doğal İspatlar bariyeri ve asimptotik n>=5 tümevarımı) "
            "her turda yeni bir cepheden ilerletmektir.\n"
            "KESİN KURAL: Önceki turların başlıklarını veya genel 'D_9^hom Koszul rank düşüşü' kalıbını "
            "ASLA tekrarlama! Bu tur için atanan YENİ CEPHE üzerine özgün, somut, sayılar ve teoremler içeren "
            "görevler ver. Yalnızca geçerli JSON döndür, Türkçe yaz."
        )

        user_prompt = (
            f"ENGEL HARİTASININ EN SON GÜNCELLEMESİ (SON TURLAR):\n{current_map_summary}\n\n"
            f"SON TURLARDA İŞLENEN BAŞLIKLAR (BUNLARI TEKRARLAMA!):\n{recent_str}\n\n"
            f"BU TURUN ({round_num}) ZORUNLU YENİ ARAŞTIRMA CEPHESİ [{stage['code']}]:\n"
            f"Ana Konu: {stage['title']}\n"
            f"Hedef: {stage['goal']}\n\n"
            f"GÖREV: Tur {round_num} için [{stage['code']}] cephesini bir adım ileri taşıyacak "
            "6 özgün, birbirine bağlı uzman görevi üret. Yanıtını SADECE geçerli JSON olarak ver:\n"
            "{\n"
            f'  "topic": "[{stage["code"]}] {stage["title"]} (veya daha spesifik alt başlık)",\n'
            '  "strategic_goal": "Bu turda kırılacak somut matematiksel hedef",\n'
            '  "agent_tasks": {\n'
            '    "prof-euler": "...",\n'
            '    "prof-hilbert": "...",\n'
            '    "prof-strassen": "...",\n'
            '    "prof-noether": "...",\n'
            '    "prof-wigner": "...",\n'
            '    "prof-valiant": "..."\n'
            "  }\n"
            "}"
        )

        try:
            res = self.orchestrator.call_0g_with_fallback(system_prompt, user_prompt)
            raw = res["content"].strip()
            if "```" in raw:
                raw = re.sub(r"^```(?:json)?\n", "", raw, flags=re.MULTILINE)
                raw = re.sub(r"\n```$", "", raw, flags=re.MULTILINE).strip()
            # Extract first JSON object if surrounded by prose
            m = re.search(r"\{.*\}", raw, re.DOTALL)
            if m:
                raw = m.group(0)
            data = json.loads(raw)
            if not isinstance(data.get("agent_tasks"), dict) or len(data["agent_tasks"]) < 6:
                raise ValueError("Incomplete agent_tasks")
            self.last_briefing = f"Tur {round_num} [{stage['code']}]: {data.get('topic', stage['title'])}"
            return data
        except Exception:
            topic = f"[{stage['code']}] {stage['title']}"
            self.last_briefing = f"Tur {round_num} [{stage['code']}]: {stage['title']}"
            return {
                "topic": topic,
                "strategic_goal": stage["goal"],
                "agent_tasks": stage["tasks"]
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
                    content = f.read()
                    # Read the LATEST updates at the end of ENGEL_HARITASI.md, not the stale top!
                    return content[-3500:] if len(content) > 3500 else content
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
