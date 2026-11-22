#!/usr/bin/env python3
"""
GitHub Actions 0G Autonomous Round Runner.
Executes one full hierarchical council round (Poincaré -> 6 Specialists -> Grothendieck),
updates ENGEL_HARITASI.md, and writes ROUND_XX_DOSSIER.md.
"""

import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from agent_hub_0g.orchestrator import AutonomousAgentOrchestrator

def main():
    print("==================================================================")
    print("🚀 GitHub Actions: Starting 0G Autonomous Council Round...")
    print("==================================================================")
    
    orchestrator = AutonomousAgentOrchestrator()
    next_round = orchestrator.current_round + 1
    print(f"[GitHub Actions] Executing Round {next_round}...")
    
    orchestrator.run_council_round(next_round)
    
    print(f"✅ [GitHub Actions] Round {next_round} completed successfully.")
    print(f"   Files updated: ENGEL_HARITASI.md, agent_hub_0g/dossiers/ROUND_{next_round}_DOSSIER.md")

if __name__ == "__main__":
    main()
