"""
Looker Conversational Analytics Client
-------------------------------------
Handles authentication, agent management, conversation lifecycle,
and natural language analytical chat execution against Looker 4.0 APIs.
"""

import time
import json
import urllib.request
import urllib.parse
import urllib.error
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LookerClient")

class LookerClient:
    def __init__(self, base_url: str, client_id: str, client_secret: str):
        self.base_url = base_url.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expiry = 0
        self._current_user = None

    def login(self) -> str:
        """Authenticate using API3 credentials and retrieve an access token."""
        self._current_user = None
        url = f"{self.base_url}/api/4.0/login"
        payload = urllib.parse.urlencode({
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                self.access_token = data.get("access_token")
                expires_in = data.get("expires_in", 3600)
                self.token_expiry = time.time() + expires_in - 60  # 60s buffer
                logger.info("Successfully authenticated with Looker API 4.0")
                return self.access_token
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            logger.error(f"Login failed [{e.code}]: {err_msg}")
            raise RuntimeError(f"Looker authentication failed ({e.code}): {err_msg}")
        except Exception as e:
            logger.error(f"Unexpected connection error during login: {e}")
            raise

    def _ensure_token(self):
        """Ensure we have an active, non-expired access token."""
        if not self.access_token or time.time() >= self.token_expiry:
            self.login()

    def _request(self, method: str, path: str, payload: dict = None, params: dict = None) -> dict:
        """Make an authenticated request to Looker 4.0 API."""
        self._ensure_token()

        url = f"{self.base_url}/api/4.0{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)

        body_bytes = json.dumps(payload).encode("utf-8") if payload is not None else None
        headers = {
            "Authorization": f"token {self.access_token}",
            "Accept": "application/json"
        }
        if payload is not None:
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(url, data=body_bytes, headers=headers, method=method)

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                resp_text = resp.read().decode("utf-8")
                if not resp_text:
                    return {}
                return json.loads(resp_text)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            logger.error(f"HTTP Error {e.code} on {method} {path}: {err_body}")
            try:
                parsed_err = json.loads(err_body)
                raise RuntimeError(f"Looker API Error ({e.code}): {parsed_err.get('message', err_body)}")
            except json.JSONDecodeError:
                raise RuntimeError(f"Looker API Error ({e.code}): {err_body}")
        except Exception as e:
            logger.error(f"Request error on {method} {path}: {e}")
            raise

    def set_workspace(self, workspace_id: str = "production"):
        """Switch workspace between 'production' and 'dev'."""
        try:
            self._request("PATCH", "/session", payload={"workspace_id": workspace_id})
        except Exception as e:
            logger.warning(f"Failed to set workspace to {workspace_id}: {e}")

    def get_current_user(self) -> dict:
        """Fetch and cache the current authenticated Looker user profile."""
        if not self._current_user:
            self._current_user = self._request("GET", "/user")
        return self._current_user

    def list_agents(self, only_own: bool = True) -> list:
        """
        Search and list Conversational Analytics agents.
        If only_own is True (default), filters agents to those created by the authenticated user.
        """
        agents = self._request("GET", "/agents/search")
        current_user_id = None
        if only_own:
            try:
                user = self.get_current_user()
                if user and user.get("id") is not None:
                    current_user_id = str(user.get("id"))
            except Exception as e:
                logger.warning(f"Could not fetch current user for agent filtering: {e}")

        # Format and sort by created_at descending
        formatted = []
        for a in agents:
            creator_id = str(a.get("created_by_user_id")) if a.get("created_by_user_id") is not None else None
            if only_own and current_user_id and creator_id != current_user_id:
                continue
            formatted.append({
                "id": a.get("id"),
                "name": a.get("name", "Unnamed Agent"),
                "description": a.get("description", ""),
                "sources": a.get("sources", []),
                "instructions": a.get("context", {}).get("instructions", "") if a.get("context") else "",
                "created_at": a.get("created_at"),
                "created_by": a.get("created_by_user_id")
            })
        return formatted

    def get_agent(self, agent_id: str) -> dict:
        """Fetch details of a specific agent."""
        return self._request("GET", f"/agents/{agent_id}")

    def create_agent(self, name: str, description: str, model: str, explore: str, instructions: str) -> dict:
        """
        Create a new Conversational Analytics Agent bound to a LookML model & explore.
        """
        payload = {
            "name": name,
            "description": description,
            "sources": [
                {
                    "model": model,
                    "explore": explore
                }
            ],
            "context": {
                "instructions": instructions,
                "show_analytical_details": True,
                "show_debug": False
            }
        }
        return self._request("POST", "/agents", payload=payload)

    def create_conversation(self, agent_id: str, name: str = "Agentic Lab Session") -> dict:
        """Create a new conversation session associated with the target agent."""
        payload = {
            "agent_id": agent_id,
            "name": name
        }
        return self._request("POST", "/conversations", payload=payload)

    def chat(self, conversation_id: str, user_message: str) -> dict:
        """
        Submit a natural language analytical query to the conversational agent.
        Parses multi-stage messages: thought process, explore resolution, data queries, and final answer.
        """
        payload = {
            "conversation_id": conversation_id,
            "user_message": user_message
        }
        raw_messages = self._request("POST", "/conversational_analytics/chat", payload=payload)

        # Parse the structured messages
        parsed = {
            "conversation_id": conversation_id,
            "user_message": user_message,
            "thoughts": [],
            "schema_events": [],
            "query": None,
            "data": None,
            "chart": None,
            "analysis": None,
            "final_response": "",
            "raw_messages": raw_messages
        }

        for msg in raw_messages:
            sys_m = msg.get("systemMessage", {})
            
            # 1. Thought Process (Chain of Thought reasoning)
            if sys_m.get("text"):
                text_obj = sys_m["text"]
                text_type = text_obj.get("textType", "")
                parts = text_obj.get("parts", [])
                full_text = "\n\n".join(parts) if isinstance(parts, list) else str(parts)
                
                if text_type == "THOUGHT":
                    parsed["thoughts"].append(full_text)
                elif text_type == "FINAL_RESPONSE":
                    parsed["final_response"] = full_text
                else:
                    if not parsed["final_response"]:
                        parsed["final_response"] = full_text
                    else:
                        parsed["thoughts"].append(full_text)

            # 2. Schema resolution
            if sys_m.get("schema"):
                parsed["schema_events"].append(sys_m["schema"])

            # 3. Query & Data
            if sys_m.get("data"):
                data_obj = sys_m["data"]
                if data_obj.get("query"):
                    parsed["query"] = data_obj["query"]
                if data_obj.get("result"):
                    parsed["data"] = data_obj["result"]

            # 4. Analysis
            if sys_m.get("analysis"):
                parsed["analysis"] = sys_m["analysis"]

            # 5. Chart
            if sys_m.get("chart"):
                parsed["chart"] = sys_m["chart"]

        # Fallback if final_response was not explicitly flagged with FINAL_RESPONSE
        if not parsed["final_response"] and parsed["thoughts"]:
            parsed["final_response"] = parsed["thoughts"][-1]

        return parsed
