#!/usr/bin/env python3
"""
0G Agent Hub Web Server.
Serves the realtime monitoring dashboard and provides control APIs for the 24/7 autonomous council.
"""

import os
import sys
import json
import asyncio
from aiohttp import web

# Ensure workspace is in sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from agent_hub_0g.orchestrator import orchestrator

STATIC_DIR = os.path.join(BASE_DIR, "agent_hub_0g/static")

async def handle_index(request):
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return web.FileResponse(index_file)
    return web.Response(text="index.html not found", status=404)

async def handle_status(request):
    data = orchestrator.get_snapshot()
    return web.json_response(data)

async def handle_start(request):
    orchestrator.start()
    return web.json_response({"status": "ok", "state": orchestrator.state})

async def handle_pause(request):
    orchestrator.pause()
    return web.json_response({"status": "ok", "state": orchestrator.state})

async def handle_resume(request):
    orchestrator.resume()
    return web.json_response({"status": "ok", "state": orchestrator.state})

async def handle_stop(request):
    orchestrator.stop()
    return web.json_response({"status": "ok", "state": orchestrator.state})

async def handle_trigger(request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    topic = data.get("topic")
    orchestrator.trigger_single_round(topic)
    return web.json_response({"status": "ok", "message": "Round triggered"})

async def handle_prompt(request):
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "Invalid JSON"}, status=400)
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return web.json_response({"error": "Empty prompt"}, status=400)
    orchestrator.add_custom_prompt(prompt)
    return web.json_response({"status": "ok", "queue_len": len(orchestrator.custom_prompt_queue)})

async def handle_clear_logs(request):
    orchestrator.clear_logs()
    return web.json_response({"status": "ok"})

def create_app():
    app = web.Application()
    app.router.add_get("/", handle_index)
    app.router.add_get("/api/status", handle_status)
    app.router.add_post("/api/start", handle_start)
    app.router.add_post("/api/pause", handle_pause)
    app.router.add_post("/api/resume", handle_resume)
    app.router.add_post("/api/stop", handle_stop)
    app.router.add_post("/api/trigger_round", handle_trigger)
    app.router.add_post("/api/prompt", handle_prompt)
    app.router.add_post("/api/clear_logs", handle_clear_logs)
    app.router.add_static("/static", STATIC_DIR)
    return app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    print(f"==================================================================")
    print(f"🚀 0G Agent Hub Dashboard starting at: http://localhost:{port}")
    print(f"   24/7 Autonomous AI Council ready.")
    print(f"==================================================================")
    
    # Only auto-start local worker loop if explicitly requested; otherwise cloud runner handles continuous execution
    if os.environ.get("AUTO_START_COUNCIL", "0") == "1":
        orchestrator.start()
        print("   [Autonomous Council Worker: Started locally]")
    else:
        print("   [Autonomous Council: Cloud Runner active on GitHub Actions; UI listening]")
    
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=port)
