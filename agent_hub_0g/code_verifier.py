#!/usr/bin/env python3
"""
Real Code & Formal Proof Execution Verifier for 0G Council Prover Agents:
- Dr. Alan Turing (Python / NumPy / C experimental verification)
- Prof. Haskell Curry (Lean 4 kernel formal verification, zero-sorry enforcement)
"""

import os
import re
import shutil
import subprocess
from typing import Dict, Any, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERIFIED_DIR = os.path.join(BASE_DIR, "agent_hub_0g", "verified_code")
os.makedirs(VERIFIED_DIR, exist_ok=True)


def find_lean_binary() -> Optional[str]:
    # Prefer direct toolchain binary to avoid elan network check latency
    tc_root = os.path.expanduser("~/.elan/toolchains")
    if os.path.isdir(tc_root):
        for entry in sorted(os.listdir(tc_root), reverse=True):
            cand = os.path.join(tc_root, entry, "bin", "lean")
            if os.path.isfile(cand) and os.access(cand, os.X_OK):
                return cand
    elan_lean = os.path.expanduser("~/.elan/bin/lean")
    if os.path.isfile(elan_lean) and os.access(elan_lean, os.X_OK):
        return elan_lean
    return shutil.which("lean")


def extract_code_block(text: str, lang: str) -> Optional[str]:
    pattern = rf"```{lang}\s*\n(.*?)```"
    matches = re.findall(pattern, text, flags=re.DOTALL | re.IGNORECASE)
    if matches:
        return matches[-1].strip()
    # Fallback: any fenced code block
    matches_any = re.findall(r"```[a-zA-Z0-9_]*\s*\n(.*?)```", text, flags=re.DOTALL)
    if matches_any:
        return matches_any[-1].strip()
    return None


def run_python_verification(response_text: str, round_num: int) -> Dict[str, Any]:
    code = extract_code_block(response_text, "python")
    if not code:
        return {
            "status": "NO_CODE",
            "returncode": -1,
            "stdout": "",
            "stderr": "Python kod bloğu (```python ... ```) bulunamadı.",
            "file": ""
        }

    script_path = os.path.join(VERIFIED_DIR, f"round_{round_num}_turing.py")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(code + "\n")

    try:
        res = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            timeout=25,
            cwd=BASE_DIR
        )
        status = "PASS" if res.returncode == 0 else "FAIL"
        return {
            "status": status,
            "returncode": res.returncode,
            "stdout": (res.stdout or "")[-800:].strip(),
            "stderr": (res.stderr or "")[-600:].strip(),
            "file": script_path
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "TIMEOUT",
            "returncode": -2,
            "stdout": "",
            "stderr": "Python doğrulama betiği 25 saniye zaman aşımına uğradı.",
            "file": script_path
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "returncode": -3,
            "stdout": "",
            "stderr": str(e),
            "file": script_path
        }


def run_lean_verification(response_text: str, round_num: int) -> Dict[str, Any]:
    code = extract_code_block(response_text, "lean4") or extract_code_block(response_text, "lean")
    if not code:
        return {
            "status": "NO_CODE",
            "returncode": -1,
            "stdout": "",
            "stderr": "Lean 4 kod bloğu (```lean ... ```) bulunamadı.",
            "file": ""
        }

    lean_path = os.path.join(VERIFIED_DIR, f"round_{round_num}_curry.lean")
    with open(lean_path, "w", encoding="utf-8") as f:
        f.write(code + "\n")

    # Zero-sorry / zero-axiom enforcement
    if re.search(r"\bsorry\b", code) or re.search(r"\badmit\b", code):
        return {
            "status": "FAIL_SORRY",
            "returncode": -4,
            "stdout": "",
            "stderr": "YASAK: Lean 4 ispatı 'sorry' veya 'admit' içeriyor — gerçek çekirdek kanıtı değil.",
            "file": lean_path
        }
    if re.search(r"^\s*axiom\b", code, flags=re.MULTILINE):
        return {
            "status": "FAIL_AXIOM",
            "returncode": -5,
            "stdout": "",
            "stderr": "YASAK: Lean 4 dosyası kanıtsız 'axiom' tanımı içeriyor.",
            "file": lean_path
        }

    lean_bin = find_lean_binary()
    if not lean_bin:
        return {
            "status": "NO_LEAN_BIN",
            "returncode": -6,
            "stdout": "",
            "stderr": "Lean 4 ikilisi (~/.elan/bin/lean) kurulum aşamasında veya bulunamadı.",
            "file": lean_path
        }

    try:
        res = subprocess.run(
            [lean_bin, lean_path],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=BASE_DIR
        )
        status = "PASS" if res.returncode == 0 else "FAIL"
        return {
            "status": status,
            "returncode": res.returncode,
            "stdout": (res.stdout or "")[-600:].strip(),
            "stderr": (res.stderr or "")[-600:].strip(),
            "file": lean_path
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "TIMEOUT",
            "returncode": -2,
            "stdout": "",
            "stderr": "Lean 4 çekirdek derlemesi 30 saniye zaman aşımına uğradı.",
            "file": lean_path
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "returncode": -3,
            "stdout": "",
            "stderr": str(e),
            "file": lean_path
        }
