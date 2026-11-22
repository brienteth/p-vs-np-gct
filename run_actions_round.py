#!/usr/bin/env python3
"""
GitHub Actions 0G Continuous Autonomous Council Runner.
Executes multiple consecutive rounds per run (e.g. 5 rounds or up to 20 minutes),
updating ENGEL_HARITASI.md, generating dossiers, and committing after each round.
"""

import os
import sys
import time
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from agent_hub_0g.orchestrator import AutonomousAgentOrchestrator

def commit_and_push(round_num):
    try:
        subprocess.run(["git", "config", "--global", "user.name", "0G Council Bot"], check=False)
        subprocess.run(["git", "config", "--global", "user.email", "bot@0g.ai"], check=False)
        subprocess.run(["git", "add", "ENGEL_HARITASI.md", "agent_hub_0g/dossiers/", "agent_hub_0g/logs/", "docs/"], check=False)
        res = subprocess.run(["git", "diff", "--staged", "--quiet"])
        if res.returncode != 0:
            subprocess.run(["git", "commit", "-m", f"Auto: Round {round_num} 0G Council Proofs [skip ci]"], check=False)
            subprocess.run(["git", "push"], check=False)
            print(f"[Git] Round {round_num} successfully committed and pushed.")
    except Exception as e:
        print(f"[Git Error]: {e}")

def main():
    print("==================================================================")
    print("🚀 GitHub Actions: Starting Continuous 0G Autonomous Council Session...")
    print("==================================================================")
    
    orchestrator = AutonomousAgentOrchestrator()
    start_time = time.time()
    max_duration_seconds = 20 * 60  # Run for 20 continuous minutes per workflow execution

    round_count = 0
    while time.time() - start_time < max_duration_seconds:
        next_round = orchestrator.current_round + 1
        print(f"\n[GitHub Actions] >>> Executing Round {next_round} (Session active: {int((time.time() - start_time)/60)}m)...")
        
        try:
            orchestrator.run_council_round(next_round)
            round_count += 1
            print(f"✅ [GitHub Actions] Round {next_round} completed.")
            commit_and_push(next_round)
        except Exception as e:
            print(f"⚠️ Error in Round {next_round}: {e}")

        # Brief pause between rounds
        time.sleep(5)

    print(f"\n🎉 Session completed. Total rounds executed: {round_count}")

if __name__ == "__main__":
    main()
