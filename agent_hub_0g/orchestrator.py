#!/usr/bin/env python3
"""
0G 24/7 Autonomous Multi-Tier Agent Orchestrator.
Includes:
- Tier 1: Chief Research Director (Prof. Henri Poincaré) - Stratejist & Görev Atayıcı
- Tier 2: 6 Specialist Researchers (Euler, Hilbert, Strassen, Noether, Wigner, Valiant)
- Tier 3: Epistemic Cartographer & Auditor (Prof. Alexander Grothendieck) - Haritacı & Güncelleyici
"""

import os
import sys
import time
import json
import subprocess
import threading
from collections import deque
from typing import Dict, List, Optional, Any

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

ENV_PATH = os.path.join(BASE_DIR, ".env")
LOG_DIR = os.path.join(BASE_DIR, "agent_hub_0g/logs")
LIVE_LOG_FILE = os.path.join(LOG_DIR, "live_debate.jsonl")
ROUTER_URL = "https://router-api.0g.ai/v1/chat/completions"

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

COUNCILS = {
    "gct_council": [
        {
            "id": "prof-euler",
            "name": "Prof. Leonhard Euler",
            "avatar": "🏛️",
            "role": "Formal Proofs, Syzygy & Koszul Elimination",
            "system": "Sen Prof. Euler'sin. GCT Konseyi'nin biçimsel ispat ve Koszul syzygy uzmanısın. Cebirsel denklemler ve kesin matris rankları ile konuşursun. Türkçe ve özlü yanıt ver.",
            "color": "emerald"
        },
        {
            "id": "prof-hilbert",
            "name": "Prof. David Hilbert",
            "avatar": "📐",
            "role": "Algebraic Geometry, Invariant Theory & Nullstellensatz",
            "system": "Sen Prof. Hilbert'sin. Cebirsel geometri ve invaryant teorisi temelleri ile düşünürsün. Zariski kapanışları ve ideal boyutlarını denetlersin. Türkçe ve özlü yanıt ver.",
            "color": "blue"
        },
        {
            "id": "prof-strassen",
            "name": "Prof. Volker Strassen",
            "avatar": "⚡",
            "role": "Tensor Rank, Border Complexity & Fast Algorithms",
            "system": "Sen Prof. Strassen'sin. Tensor rankı, sınır karmaşıklığı (border dc) ve dejenerasyon eğrileri üzerine uzmansın. Türkçe ve özlü yanıt ver.",
            "color": "purple"
        },
        {
            "id": "prof-noether",
            "name": "Prof. Emmy Noether",
            "avatar": "🌀",
            "role": "Representation Theory, Quivers & Symmetry Orbits",
            "system": "Sen Prof. Emmy Noether'sin. Temsil teorisi, grup yörüngeleri ve simetri kırılmaları üzerinden düşünürsün. Türkçe ve özlü yanıt ver.",
            "color": "pink"
        },
        {
            "id": "prof-wigner",
            "name": "Prof. Eugene Wigner",
            "avatar": "🎲",
            "role": "Random Matrix Theory, Grassmannian Geometry & F_2 Rank",
            "system": "Sen Prof. Wigner'sin. Grassmannian manifoldları, sonlu cisimlerde rank patlamaları ve rastgele matris spektrumları üzerine uzmansın. Türkçe ve özlü yanıt ver.",
            "color": "amber"
        },
        {
            "id": "prof-valiant",
            "name": "Prof. Leslie Valiant",
            "avatar": "💻",
            "role": "Algebraic Complexity, VNP vs VP & Circuit Lower Bounds",
            "system": "Sen Prof. Valiant'sın. Kalıcı polinom (permanent), determinantal karmaşıklık ve VP vs VNP kuramının kurucususun. Türkçe ve özlü yanıt ver.",
            "color": "cyan"
        }
    ]
}

class AutonomousAgentOrchestrator:
    def __init__(self):
        self.api_key = load_0g_api_key()
        self.candidate_models = ["0gm-1.0-35b-a3b", "qwen-flash", "claude-haiku-4.5"]
        self.state = "stopped"  # "running", "paused", "stopped"
        self.current_round = 20
        self.active_agent_id = None
        self.custom_prompt_queue = deque()
        self.logs_queue = deque(maxlen=2000)
        self.stats = {
            "total_calls": 0,
            "total_tokens": 0,
            "total_cost_micro_usd": 0,
            "successful_rounds": 0,
            "start_time": None,
            "last_active": None,
            "error_count": 0
        }
        self.agents = COUNCILS["gct_council"]
        self.agent_statuses = {a["id"]: {"status": "idle", "last_thought": "", "model": "", "last_time": ""} for a in self.agents}
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._pause_event.set()

        # Meta-Agents Initialization
        from agent_hub_0g.meta_agents import MetaAgentDirector, MetaAgentCartographer
        self.director = MetaAgentDirector(self)
        self.cartographer = MetaAgentCartographer(self)

        self._load_saved_logs()

    def _load_saved_logs(self):
        if os.path.exists(LIVE_LOG_FILE):
            try:
                with open(LIVE_LOG_FILE, "r", encoding="utf-8") as f:
                    lines = f.readlines()[-300:]
                    for line in lines:
                        if line.strip():
                            data = json.loads(line)
                            self.logs_queue.append(data)
                            if "round" in data and isinstance(data["round"], int) and data["round"] > self.current_round:
                                self.current_round = data["round"]
            except Exception as e:
                print(f"[Orchestrator] Error loading saved logs: {e}")

    def call_0g_api(self, model: str, system_prompt: str, user_prompt: str, max_tokens: int = 1500) -> Dict[str, Any]:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.35,
            "max_tokens": max_tokens
        }
        cmd = [
            "/usr/bin/curl",
            "-sS",
            "--max-time", "50",
            ROUTER_URL,
            "-H", f"Authorization: Bearer {self.api_key}",
            "-H", "Content-Type: application/json",
            "-H", "Accept: application/json",
            "-d", json.dumps(payload)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"Curl error {res.returncode}: {res.stderr[:200]}")
        
        data = json.loads(res.stdout)
        if "error" in data:
            raise RuntimeError(f"0G API Error: {data['error']}")
        
        choice = data["choices"][0]
        msg = choice.get("message", {})
        content = msg.get("content", "").strip()
        if not content:
            content = msg.get("reasoning_content", "").strip()
        
        usage = data.get("usage", {})
        trace = data.get("x_0g_trace", {}).get("billing", {})
        cost_micro = int(trace.get("total_cost_usd_micro", 8))
        
        return {
            "model": data.get("model", model),
            "content": content,
            "tokens": usage.get("total_tokens", 0),
            "cost_micro": cost_micro,
            "id": data.get("id", "")
        }

    def call_0g_with_fallback(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        last_err = ""
        for model in self.candidate_models:
            try:
                res = self.call_0g_api(model, system_prompt, user_prompt)
                if res["content"]:
                    return res
            except Exception as e:
                last_err = f"{model}: {e}"
        raise RuntimeError(f"All 0G models failed. Last error: {last_err}")

    def emit_log(self, entry: Dict[str, Any]):
        entry["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.logs_queue.append(entry)
        try:
            with open(LIVE_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass

    def run_council_round(self, round_num: int, custom_topic: Optional[str] = None):
        self.current_round = round_num

        # STEP 1: CARTOGRAPHER READS MAP
        current_map = self.cartographer.read_current_map()

        # STEP 2: DIRECTOR ASSIGNS TARGETED TASKS
        if custom_topic:
            task_plan = {
                "topic": custom_topic,
                "strategic_goal": "Kullanıcının özel talimatını derinlemesine incelemek ve haritaya işlemek",
                "agent_tasks": {a["id"]: f"Kullanıcı hipotezini kendi uzmanlık alanından ({a['role']}) incele: {custom_topic}" for a in self.agents}
            }
        else:
            task_plan = self.director.generate_targeted_tasks(round_num, current_map)

        topic = task_plan.get("topic", f"Tur {round_num} İlerleme Hedefi")
        goal = task_plan.get("strategic_goal", "")
        agent_tasks = task_plan.get("agent_tasks", {})

        # Emit Director Briefing Log
        self.emit_log({
            "type": "director_briefing",
            "round": round_num,
            "director_name": self.director.name,
            "avatar": self.director.avatar,
            "topic": topic,
            "strategic_goal": goal,
            "text": f"🧭 **DİREKTÖR BRİFİNGİ (Tur {round_num}):**\n**Hedef Konu:** {topic}\n**Stratejik Amaç:** {goal}"
        })

        # STEP 3: 6 SPECIALISTS SOLVE THEIR ASSIGNED TASKS
        round_dialogue = []
        for agent in self.agents:
            if self._stop_event.is_set():
                break
            self._pause_event.wait()

            self.active_agent_id = agent["id"]
            self.agent_statuses[agent["id"]]["status"] = "thinking"

            specific_task = agent_tasks.get(agent["id"], f"Konuyu analiz et: {topic}")
            dialogue_summary = "\n".join([f"- {d.get('name') or d.get('agent_name')}: {d['summary']}" for d in round_dialogue[-3:]])

            prompt = (
                f"TUR {round_num} STRATEJİK HEDEF:\n{topic}\n"
                f"DİREKTÖRÜN SANA ÖZEL ATADIĞI GÖREV:\n{specific_task}\n\n"
                f"ÖNCEKİ AJANLARIN TEZLERİ:\n{dialogue_summary if dialogue_summary else 'İlk konuşmacısın.'}\n\n"
                f"GÖREVİN ({agent['name']}):\n"
                f"Sana atanan bu özel görevi uzmanlığın ({agent['role']}) çerçevesinde çöz. "
                "Matematiksel olarak somut, denklemler içeren ve diğer üyelere hitap eden özlü bir analiz sun (maks 150-200 kelime). "
                "İddialarını [İSPAT], [KESİN HESAP] veya [SANI] olarak etiketle."
            )

            try:
                t0 = time.time()
                res = self.call_0g_with_fallback(agent["system"], prompt)
                duration = time.time() - t0

                self.stats["total_calls"] += 1
                self.stats["total_tokens"] += res["tokens"]
                self.stats["total_cost_micro_usd"] += res["cost_micro"]
                self.stats["last_active"] = time.strftime("%Y-%m-%d %H:%M:%S")

                self.agent_statuses[agent["id"]]["status"] = "active"
                self.agent_statuses[agent["id"]]["last_thought"] = res["content"][:200] + "..."
                self.agent_statuses[agent["id"]]["model"] = res["model"]
                self.agent_statuses[agent["id"]]["last_time"] = time.strftime("%H:%M:%S")

                msg_entry = {
                    "type": "agent_message",
                    "round": round_num,
                    "agent_id": agent["id"],
                    "agent_name": agent["name"],
                    "avatar": agent["avatar"],
                    "role": agent["role"],
                    "model": res["model"],
                    "tokens": res["tokens"],
                    "cost_micro": res["cost_micro"],
                    "duration_sec": round(duration, 2),
                    "text": res["content"]
                }
                self.emit_log(msg_entry)
                round_dialogue.append({"name": agent["name"], "agent_name": agent["name"], "role": agent["role"], "summary": res["content"][:180], "text": res["content"]})
                time.sleep(2)

            except Exception as e:
                self.stats["error_count"] += 1
                err_entry = {
                    "type": "error",
                    "round": round_num,
                    "agent_id": agent["id"],
                    "text": f"⚠️ 0G API Hatası ({agent['name']}): {str(e)}"
                }
                self.emit_log(err_entry)
                time.sleep(4)

            self.agent_statuses[agent["id"]]["status"] = "idle"

        self.active_agent_id = None

        # STEP 4: CARTOGRAPHER SYNTHESIZES & UPDATES ENGEL_HARITASI.MD
        if round_dialogue and not self._stop_event.is_set():
            carto_synthesis = self.cartographer.evaluate_and_update_map(round_num, topic, round_dialogue)
            self.emit_log({
                "type": "cartographer_update",
                "round": round_num,
                "cartographer_name": self.cartographer.name,
                "avatar": self.cartographer.avatar,
                "text": f"🗺️ **HARİTACI GROTHENDIECK GÜNCELLEMESİ (Tur {round_num}):**\n{carto_synthesis}"
            })

        self.stats["successful_rounds"] += 1
        self.emit_log({
            "type": "round_end",
            "round": round_num,
            "text": f"✅ TUR {round_num} TAMAMLANDI. Dosyalar diske işlendi, Harita güncellendi."
        })

    def _loop(self):
        self.state = "running"
        self.stats["start_time"] = time.time()
        self.emit_log({"type": "system", "text": "🟢 0G 7/24 Hiyerarşik Otonom Araştırma Motoru Başlatıldı. Direktör & Haritacı devrede."})

        round_idx = self.current_round + 1
        while not self._stop_event.is_set():
            self._pause_event.wait()

            custom_topic = None
            if self.custom_prompt_queue:
                custom_topic = f"[Kullanıcı Talebi] {self.custom_prompt_queue.popleft()}"

            try:
                self.run_council_round(round_idx, custom_topic)
                round_idx += 1
            except Exception as e:
                print(f"[Orchestrator Loop Error in Round {round_idx}]: {e}")
                self.emit_log({"type": "error", "round": round_idx, "text": f"⚠️ Tur {round_idx} döngü hatası (otomatik kurtarılıyor): {e}"})
                round_idx += 1
                time.sleep(5)

            # Autonomous interval between rounds (e.g., 6 seconds)
            for _ in range(6):
                if self._stop_event.is_set():
                    break
                time.sleep(1)

        self.state = "stopped"
        self.emit_log({"type": "system", "text": "🔴 0G Hub Durduruldu."})

    def start(self):
        if self.state == "running":
            return
        self._stop_event.clear()
        self._pause_event.set()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def pause(self):
        if self.state == "running":
            self._pause_event.clear()
            self.state = "paused"
            self.emit_log({"type": "system", "text": "🟡 0G Hub Duraklatıldı."})

    def resume(self):
        if self.state == "paused":
            self._pause_event.set()
            self.state = "running"
            self.emit_log({"type": "system", "text": "🟢 0G Hub Devam Ediyor."})

    def stop(self):
        self._stop_event.set()
        self._pause_event.set()
        self.state = "stopped"
        if self._thread:
            self._thread.join(timeout=2)

    def trigger_single_round(self, custom_topic: Optional[str] = None):
        t = threading.Thread(target=self._trigger_worker, args=(custom_topic,), daemon=True)
        t.start()

    def _trigger_worker(self, custom_topic: Optional[str]):
        self.run_council_round(self.current_round + 1, custom_topic)

    def add_custom_prompt(self, prompt: str):
        self.custom_prompt_queue.append(prompt)
        self.emit_log({"type": "system", "text": f"📥 Yeni Kullanıcı Hipotezi Direktör Masasına İletildi: {prompt[:80]}..."})

    def clear_logs(self):
        self.logs_queue.clear()
        if os.path.exists(LIVE_LOG_FILE):
            open(LIVE_LOG_FILE, "w").close()

    def get_snapshot(self) -> Dict[str, Any]:
        uptime = 0
        if self.stats["start_time"] and self.state == "running":
            uptime = int(time.time() - self.stats["start_time"])
        return {
            "state": self.state,
            "current_round": self.current_round,
            "active_agent_id": self.active_agent_id,
            "meta_agents": {
                "director": {
                    "name": self.director.name,
                    "avatar": self.director.avatar,
                    "last_briefing": self.director.last_briefing
                },
                "cartographer": {
                    "name": self.cartographer.name,
                    "avatar": self.cartographer.avatar,
                    "last_update": self.cartographer.last_update_summary
                }
            },
            "stats": {
                **self.stats,
                "uptime_seconds": uptime,
                "cost_usd_est": round(self.stats["total_cost_micro_usd"] / 1_000_000, 4)
            },
            "agents": [
                {
                    **a,
                    "status": self.agent_statuses[a["id"]]["status"],
                    "last_thought": self.agent_statuses[a["id"]]["last_thought"],
                    "model": self.agent_statuses[a["id"]]["model"],
                    "last_time": self.agent_statuses[a["id"]]["last_time"]
                }
                for a in self.agents
            ],
            "queue_len": len(self.custom_prompt_queue),
            "recent_logs": list(self.logs_queue)[-60:]
        }

orchestrator = AutonomousAgentOrchestrator()
