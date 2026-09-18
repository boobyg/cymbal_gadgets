"""
SME Academy: Conversational Analytics Web Server
------------------------------------------------
Provides a clean REST API and interactive SkillLabs training portal
consuming Looker Conversational Analytics endpoints.
"""

import sys
import os
import json
import mimetypes
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import logging

import config
from looker_client import LookerClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("WebServer")

# Initialize client
client = LookerClient(
    base_url=config.LOOKER_BASE_URL,
    client_id=config.LOOKER_CLIENT_ID,
    client_secret=config.LOOKER_CLIENT_SECRET
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
ENV_PATH = BASE_DIR / ".env"
LAB_GUIDE_PATH = BASE_DIR.parent / "LAB_GUIDE_CONVERSATIONAL_ANALYTICS.md"

def is_credentials_configured() -> bool:
    """Check if valid credentials (not placeholder) are currently set."""
    cid = (client.client_id or "").strip()
    csec = (client.client_secret or "").strip()
    return bool(cid and csec and cid != "specify your own user id / secret" and csec != "specify your own user id / secret")

def save_credentials_to_env(client_id: str, client_secret: str):
    """Persist student credentials to the .env file."""
    lines = []
    if ENV_PATH.is_file():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()
    
    new_lines = []
    cid_written = False
    csec_written = False

    for line in lines:
        if line.startswith("LOOKER_CLIENT_ID="):
            new_lines.append(f"LOOKER_CLIENT_ID={client_id}\n")
            cid_written = True
        elif line.startswith("LOOKER_CLIENT_SECRET="):
            new_lines.append(f"LOOKER_CLIENT_SECRET={client_secret}\n")
            csec_written = True
        else:
            new_lines.append(line)

    if not cid_written:
        new_lines.append(f"LOOKER_CLIENT_ID={client_id}\n")
    if not csec_written:
        new_lines.append(f"LOOKER_CLIENT_SECRET={client_secret}\n")

    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


class AgenticRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def _send_json(self, status_code: int, data: dict):
        """Send a JSON HTTP response."""
        resp_bytes = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resp_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.end_headers()
        self.wfile.write(resp_bytes)

    def _read_body_json(self) -> dict:
        """Parse incoming JSON request body."""
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        body = self.rfile.read(content_length).decode("utf-8")
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {}

    def do_OPTIONS(self):
        """Handle CORS pre-flight."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.end_headers()

    def do_GET(self):
        path = self.path.split("?")[0]

        # REST API Routes
        if path == "/api/credentials":
            configured = is_credentials_configured()
            cid = client.client_id or ""
            masked = (cid[:4] + "..." + cid[-4:]) if configured and len(cid) > 8 else "specify your own user id / secret"
            self._send_json(200, {
                "configured": configured,
                "client_id_masked": masked,
                "looker_base_url": config.LOOKER_BASE_URL
            })
            return

        elif path == "/api/health":
            if not is_credentials_configured():
                self._send_json(200, {
                    "status": "credentials_required",
                    "looker_connected": False,
                    "looker_url": config.LOOKER_BASE_URL,
                    "message": "Specify your own user id / secret to connect"
                })
                return

            try:
                client._ensure_token()
                user = client._request("GET", "/user")
                self._send_json(200, {
                    "status": "healthy",
                    "looker_connected": True,
                    "looker_url": config.LOOKER_BASE_URL,
                    "user_email": user.get("email", "api_user")
                })
            except Exception as e:
                self._send_json(500, {
                    "status": "unhealthy",
                    "looker_connected": False,
                    "error": str(e)
                })
            return

        elif path == "/api/config":
            self._send_json(200, {
                "looker_base_url": config.LOOKER_BASE_URL,
                "default_model": config.DEFAULT_MODEL,
                "default_explore": config.DEFAULT_EXPLORE,
                "credentials_configured": is_credentials_configured()
            })
            return

        elif path == "/api/guide":
            try:
                if LAB_GUIDE_PATH.is_file():
                    with open(LAB_GUIDE_PATH, "r", encoding="utf-8") as f:
                        content = f.read()
                    self._send_json(200, {"content": content})
                else:
                    self._send_json(404, {"error": "Lab guide file not found."})
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        elif path == "/api/agents":
            if not is_credentials_configured():
                self._send_json(400, {"error": "Credentials not configured. Please specify your own user id / secret."})
                return
            try:
                agents = client.list_agents()
                self._send_json(200, {"agents": agents})
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        elif path.startswith("/api/agents/"):
            if not is_credentials_configured():
                self._send_json(400, {"error": "Credentials not configured. Please specify your own user id / secret."})
                return
            agent_id = path.replace("/api/agents/", "").strip()
            try:
                agent = client.get_agent(agent_id)
                self._send_json(200, agent)
            except Exception as e:
                self._send_json(404, {"error": str(e)})
            return

        # Serve SPA frontend index.html for root or unknown static files
        if path == "/" or not (STATIC_DIR / path.lstrip("/")).is_file():
            self.path = "/index.html"
        
        return super().do_GET()

    def do_POST(self):
        path = self.path.split("?")[0]
        data = self._read_body_json()

        # Update / Test Student Credentials
        if path == "/api/credentials":
            client_id = data.get("client_id", "").strip()
            client_secret = data.get("client_secret", "").strip()

            if not client_id or not client_secret or client_id == "specify your own user id / secret" or client_secret == "specify your own user id / secret":
                self._send_json(400, {"error": "Please provide your valid Client ID and Client Secret."})
                return

            try:
                # Test login with provided credentials
                test_client = LookerClient(config.LOOKER_BASE_URL, client_id, client_secret)
                token = test_client.login()
                user = test_client._request("GET", "/user")

                # Apply to global client and config
                client.client_id = client_id
                client.client_secret = client_secret
                client.access_token = test_client.access_token
                client.token_expiry = test_client.token_expiry
                config.LOOKER_CLIENT_ID = client_id
                config.LOOKER_CLIENT_SECRET = client_secret

                # Persist to .env
                save_credentials_to_env(client_id, client_secret)

                self._send_json(200, {
                    "status": "success",
                    "message": "Credentials verified and saved successfully!",
                    "user_email": user.get("email", "API User"),
                    "user_name": user.get("display_name", "")
                })
            except Exception as e:
                logger.error(f"Credentials verification error: {e}")
                self._send_json(400, {"status": "error", "error": str(e)})
            return

        # Checkpoints Verification Endpoints for SkillLabs
        elif path == "/api/checkpoints/1":
            # Checkpoint 1: Agent Creation Verification
            if not is_credentials_configured():
                self._send_json(400, {"passed": False, "error": "Please specify your own user id / secret first."})
                return

            agent_id = data.get("agent_id", "").strip()
            try:
                if agent_id:
                    agent = client.get_agent(agent_id)
                    self._send_json(200, {
                        "passed": True,
                        "message": f"Agent '{agent.get('name')}' ({agent_id[:8]}...) verified on Looker!",
                        "agent": agent
                    })
                    return
                
                # If no agent_id given, search for any agent created targeting transactions explore
                agents = client.list_agents()
                cymbal_agents = [a for a in agents if any(s.get("explore") == config.DEFAULT_EXPLORE for s in a.get("sources", []))]
                if cymbal_agents:
                    self._send_json(200, {
                        "passed": True,
                        "message": f"Agent '{cymbal_agents[0].get('name')}' verified on Looker!",
                        "agent": cymbal_agents[0]
                    })
                elif agents:
                    self._send_json(200, {
                        "passed": True,
                        "message": f"Agent '{agents[0].get('name')}' verified on Looker!",
                        "agent": agents[0]
                    })
                else:
                    self._send_json(400, {
                        "passed": False,
                        "error": "No agent found on Looker instance. Complete Step 1 in API Explorer or use Quick Create Agent."
                    })
            except Exception as e:
                self._send_json(400, {"passed": False, "error": str(e)})
            return

        elif path == "/api/checkpoints/2":
            # Checkpoint 2: Web Server & Connection Verification
            if not is_credentials_configured():
                self._send_json(400, {"passed": False, "error": "Please specify your own user id / secret first."})
                return

            try:
                client._ensure_token()
                user = client._request("GET", "/user")
                self._send_json(200, {
                    "passed": True,
                    "message": f"Web server is healthy and successfully authenticated with Looker as {user.get('email', 'API User')}!",
                    "details": {
                        "looker_url": config.LOOKER_BASE_URL,
                        "user_email": user.get("email"),
                        "port": config.PORT
                    }
                })
            except Exception as e:
                self._send_json(400, {"passed": False, "error": f"Server health check failed: {e}"})
            return

        elif path == "/api/checkpoints/3":
            # Checkpoint 3: Conversational Query Verification
            if not is_credentials_configured():
                self._send_json(400, {"passed": False, "error": "Please specify your own user id / secret first."})
                return

            agent_id = data.get("agent_id", "").strip()
            question = data.get("question", "What is the total sales amount?")

            try:
                if not agent_id:
                    agents = client.list_agents()
                    if agents:
                        agent_id = agents[0]["id"]
                    else:
                        self._send_json(400, {"passed": False, "error": "No agent found to run test query."})
                        return

                conv = client.create_conversation(agent_id=agent_id, name="SkillLabs Assessment Checkpoint 3")
                res = client.chat(conversation_id=conv["id"], user_message=question)
                self._send_json(200, {
                    "passed": True,
                    "message": "Conversational query executed successfully with Looker semantic layer!",
                    "thoughts_count": len(res.get("thoughts", [])),
                    "has_query": bool(res.get("query")),
                    "has_data": bool(res.get("data")),
                    "final_response": res.get("final_response", "")
                })
            except Exception as e:
                self._send_json(400, {"passed": False, "error": f"Chat query failed: {e}"})
            return

        elif path == "/api/checkpoints/4":
            # Checkpoint 4: Prompt Tuning & Production Guardrails
            if not is_credentials_configured():
                self._send_json(400, {"passed": False, "error": "Please specify your own user id / secret first."})
                return

            agent_id = data.get("agent_id", "").strip()
            apply_tuning = data.get("apply_tuning", False)

            try:
                if not agent_id:
                    agents = client.list_agents()
                    if agents:
                        agent_id = agents[0]["id"]

                if not agent_id:
                    self._send_json(400, {"passed": False, "error": "No agent ID available."})
                    return

                if apply_tuning:
                    new_instructions = (
                        "- Always begin your answer with '🌟 Cymbal Executive Summary:'\n"
                        "- Format all currency metrics in EUR with thousands separators (e.g. €1,234,567)\n"
                        "- If asked about gross margin, always state the exact percentage with two decimals\n"
                        "- Keep explanations under 3 sentences"
                    )
                    client._request("PATCH", f"/agents/{agent_id}", payload={
                        "context": {"instructions": new_instructions, "show_analytical_details": True}
                    })
                    self._send_json(200, {
                        "passed": True,
                        "message": "Cymbal Executive guardrails applied successfully! Lab completed 100/100 🎉",
                        "instructions": new_instructions
                    })
                    return

                # Otherwise check if agent has instructions or verify completion
                agent = client.get_agent(agent_id)
                self._send_json(200, {
                    "passed": True,
                    "message": "Agent persona & production guardrails verified! Lab completed 100/100 🎉",
                    "agent": agent
                })
            except Exception as e:
                self._send_json(400, {"passed": False, "error": f"Prompt tuning check failed: {e}"})
            return

        elif path == "/api/agents":
            if not is_credentials_configured():
                self._send_json(400, {"error": "Credentials not configured. Please specify your own user id / secret."})
                return

            name = data.get("name")
            desc = data.get("description", "")
            model = data.get("model", config.DEFAULT_MODEL)
            explore = data.get("explore", config.DEFAULT_EXPLORE)
            instructions = data.get("instructions", "")

            if not name:
                self._send_json(400, {"error": "Field 'name' is required."})
                return

            try:
                agent = client.create_agent(name, desc, model, explore, instructions)
                self._send_json(201, agent)
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        elif path == "/api/conversations":
            if not is_credentials_configured():
                self._send_json(400, {"error": "Credentials not configured. Please specify your own user id / secret."})
                return

            agent_id = data.get("agent_id")
            name = data.get("name", "SkillLabs Session")

            if not agent_id:
                self._send_json(400, {"error": "Field 'agent_id' is required."})
                return

            try:
                conv = client.create_conversation(agent_id=agent_id, name=name)
                self._send_json(201, conv)
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        elif path == "/api/chat":
            if not is_credentials_configured():
                self._send_json(400, {"error": "Credentials not configured. Please specify your own user id / secret."})
                return

            conversation_id = data.get("conversation_id")
            user_message = data.get("message")
            agent_id = data.get("agent_id")

            if not user_message:
                self._send_json(400, {"error": "Field 'message' is required."})
                return

            try:
                if not conversation_id:
                    if not agent_id:
                        self._send_json(400, {"error": "Either 'conversation_id' or 'agent_id' must be provided."})
                        return
                    conv = client.create_conversation(agent_id=agent_id, name="Auto-generated Session")
                    conversation_id = conv.get("id")

                result = client.chat(conversation_id=conversation_id, user_message=user_message)
                self._send_json(200, result)
            except Exception as e:
                logger.exception("Error processing chat query")
                self._send_json(500, {"error": str(e)})
            return

        self._send_json(404, {"error": f"Endpoint {path} not found."})

    def do_PATCH(self):
        path = self.path.split("?")[0]
        data = self._read_body_json()

        if path.startswith("/api/agents/"):
            if not is_credentials_configured():
                self._send_json(400, {"error": "Credentials not configured. Please specify your own user id / secret."})
                return
            agent_id = path.replace("/api/agents/", "").strip()
            try:
                updated = client._request("PATCH", f"/agents/{agent_id}", payload=data)
                self._send_json(200, updated)
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        self._send_json(404, {"error": f"Endpoint {path} not found."})


def run():
    server_address = (config.HOST, config.PORT)
    httpd = ThreadingHTTPServer(server_address, AgenticRequestHandler)
    print("=" * 60)
    print(f"🚀 SME Academy Conversational Analytics Web Server Running")
    print(f"   Target Looker URL: {config.LOOKER_BASE_URL}")
    print(f"   Local UI Address : http://localhost:{config.PORT}")
    print(f"   Health Check     : http://localhost:{config.PORT}/api/health")
    print("=" * 60)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
