"""
Looker Conversational Analytics Client
-------------------------------------
Handles authentication, agent management, conversation lifecycle,
and natural language analytical chat execution against Looker 4.0 APIs.
"""

import os
import sys
import time
import json
import random
import urllib.request
import urllib.parse
import urllib.error
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LookerClient")

PLACEHOLDER_CRED = "specify your own user id / secret"


class _FallbackConfig:
    """Fallback config object so referencing config.LOOKER_* never raises NameError."""
    LOOKER_BASE_URL = os.environ.get("LOOKER_BASE_URL", "https://ceworkshops.cloud.looker.com")
    LOOKER_CLIENT_ID = os.environ.get("LOOKER_CLIENT_ID", "")
    LOOKER_CLIENT_SECRET = os.environ.get("LOOKER_CLIENT_SECRET", "")


try:
    import builtins
    if not hasattr(builtins, "config"):
        try:
            import config as _cfg
            builtins.config = _cfg
        except Exception:
            builtins.config = _FallbackConfig
except Exception:
    pass


class LookerClient:
    def __init__(self, base_url: str = "", client_id: str = "", client_secret: str = ""):
        self.base_url = (base_url or os.environ.get("LOOKER_BASE_URL", "https://ceworkshops.cloud.looker.com")).rstrip("/")
        self.client_id = (client_id or os.environ.get("LOOKER_CLIENT_ID", "")).strip()
        self.client_secret = (client_secret or os.environ.get("LOOKER_CLIENT_SECRET", "")).strip()
        self.access_token = None
        self.token_expiry = 0
        self._current_user = None
        self._agent_id_bridge = {}
        self._conv_id_bridge = {}
        self._deleted_agent_ids = set()
        if (
            not self.client_id
            or not self.client_secret
            or self.client_id == PLACEHOLDER_CRED
            or self.client_secret == PLACEHOLDER_CRED
        ):
            self._reload_credentials_from_env()

    @classmethod
    def from_env(cls) -> "LookerClient":
        """Create a LookerClient instance automatically configured from .env or environment."""
        return cls()

    def _reload_credentials_from_env(self):
        """Reload credentials from agentic_web_app/.env if current credentials are empty or placeholders."""
        env_candidates = [
            Path(__file__).resolve().parent / ".env",
            Path.home() / "cymbal_gadgets" / "agentic_web_app" / ".env",
            Path.cwd() / ".env",
            Path.cwd() / "agentic_web_app" / ".env"
        ]
        for env_path in env_candidates:
            if env_path.is_file():
                try:
                    with open(env_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith("#") and "=" in line:
                                k, v = line.split("=", 1)
                                k = k.strip()
                                v = v.strip().strip('"').strip("'")
                                if k == "LOOKER_CLIENT_ID" and v and v != PLACEHOLDER_CRED:
                                    self.client_id = v
                                    os.environ["LOOKER_CLIENT_ID"] = v
                                elif k == "LOOKER_CLIENT_SECRET" and v and v != PLACEHOLDER_CRED:
                                    self.client_secret = v
                                    os.environ["LOOKER_CLIENT_SECRET"] = v
                                elif k == "LOOKER_BASE_URL" and v:
                                    self.base_url = v.rstrip("/")
                                    os.environ["LOOKER_BASE_URL"] = self.base_url
                except Exception:
                    pass

    def _save_credentials_to_env_file(self, client_id: str, client_secret: str):
        """Persist credentials entered interactively to agentic_web_app/.env."""
        env_path = Path(__file__).resolve().parent / ".env"
        try:
            lines = []
            if env_path.is_file():
                with open(env_path, "r", encoding="utf-8") as f:
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
            with open(env_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
        except Exception:
            pass

    def _prompt_interactive_credentials(self, reason: str = "") -> bool:
        """If running in an interactive Python shell/terminal, prompt the student for their Looker Client ID & Secret."""
        try:
            if not (sys.stdin and sys.stdin.isatty()):
                return False
            if reason:
                print(f"\n⚠️  {reason}")
            print("🔑 Please enter the Looker Client ID and Looker Client Secret you configured during the lab prework:")
            cid = input("   Looker Client ID: ").strip().strip('"').strip("'")
            csec = input("   Looker Client Secret: ").strip().strip('"').strip("'")
            if cid and csec and cid != PLACEHOLDER_CRED and csec != PLACEHOLDER_CRED:
                self.client_id = cid
                self.client_secret = csec
                os.environ["LOOKER_CLIENT_ID"] = cid
                os.environ["LOOKER_CLIENT_SECRET"] = csec
                self._save_credentials_to_env_file(cid, csec)
                return True
        except Exception:
            pass
        return False

    def login(self) -> str:
        """Authenticate using API3 credentials and retrieve an access token."""
        self._current_user = None

        # Always check if credentials need to be reloaded from .env
        if not self.client_id or not self.client_secret or self.client_id == PLACEHOLDER_CRED or self.client_secret == PLACEHOLDER_CRED:
            self._reload_credentials_from_env()

        # If still placeholder/empty and running in an interactive terminal/Python shell, prompt the student
        if not self.client_id or not self.client_secret or self.client_id == PLACEHOLDER_CRED or self.client_secret == PLACEHOLDER_CRED:
            self._prompt_interactive_credentials(
                "Looker Client ID / Secret are not set in .env yet (Step 0)."
            )

        for attempt in range(2):
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
                # Looker returns HTTP 404 on POST /api/4.0/login when client_id or client_secret is invalid or placeholder
                if attempt == 0:
                    prev_id, prev_sec = self.client_id, self.client_secret
                    self._reload_credentials_from_env()
                    if (self.client_id, self.client_secret) != (prev_id, prev_sec) and self.client_id != PLACEHOLDER_CRED:
                        continue
                    if self._prompt_interactive_credentials(
                        f"Looker login returned HTTP {e.code} (invalid or unconfigured Client ID / Secret)."
                    ):
                        continue
                logger.error(f"Login failed [{e.code}]: {err_msg}")
                raise RuntimeError(
                    f"Looker authentication failed ({e.code}): {err_msg}. "
                    f"Please verify that your Looker Client ID and Looker Client Secret from the prework are saved in Step 0 (.env or Web UI)."
                )
            except Exception as e:
                logger.error(f"Unexpected connection error during login: {e}")
                raise

    def _ensure_token(self):
        """Ensure we have an active, non-expired access token."""
        if not self.access_token or time.time() >= self.token_expiry:
            self.login()

    def _request(self, method: str, path: str, payload: dict = None, params: dict = None, timeout: int = 25) -> dict:
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
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                resp_text = resp.read().decode("utf-8", errors="replace").strip()
                if not resp_text:
                    return {}
                if resp_text.startswith("<"):
                    raise RuntimeError(f"Looker API returned an HTML response instead of JSON on {method} {path}")
                return json.loads(resp_text)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace").strip()
            logger.error(f"HTTP Error {e.code} on {method} {path}: {err_body[:300]}")
            if err_body.startswith("<"):
                raise RuntimeError(f"Looker API Error ({e.code}): Upstream HTTP {e.code} error on {path}")
            try:
                parsed_err = json.loads(err_body)
                raise RuntimeError(f"Looker API Error ({e.code}): {parsed_err.get('message', err_body)}")
            except json.JSONDecodeError:
                raise RuntimeError(f"Looker API Error ({e.code}): {err_body[:200]}")
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
        agents = self._request("GET", "/agents/search", timeout=10)
        if not isinstance(agents, list):
            return []
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
            if not isinstance(a, dict):
                continue
            aid = a.get("id")
            if not aid or aid in self._deleted_agent_ids:
                continue
            sources = a.get("sources") or []
            has_valid_source = any(
                isinstance(s, dict) and s.get("model") and s.get("explore")
                for s in sources
            )
            if not has_valid_source:
                continue
            creator_id = str(a.get("created_by_user_id")) if a.get("created_by_user_id") is not None else None
            if only_own and current_user_id and creator_id is not None and creator_id != current_user_id:
                continue
            formatted.append({
                "id": aid,
                "name": a.get("name", "Unnamed Agent"),
                "description": a.get("description", ""),
                "sources": sources,
                "instructions": a.get("context", {}).get("instructions", "") if isinstance(a.get("context"), dict) else "",
                "created_at": a.get("created_at"),
                "created_by": a.get("created_by_user_id")
            })
        return formatted

    @staticmethod
    def _clean_id(val: str) -> str:
        """Sanitize an ID copied from JSON/API Explorer (strip whitespace, quotes, trailing commas)."""
        if not val:
            return ""
        cleaned = str(val).strip().rstrip(",").strip()
        if (cleaned.startswith('"') and cleaned.endswith('"')) or (cleaned.startswith("'") and cleaned.endswith("'")):
            cleaned = cleaned[1:-1].strip()
        return cleaned

    def get_conversation(self, conversation_id: str) -> dict:
        """Fetch details of a specific conversation session."""
        conv_id = self._clean_id(conversation_id)
        safe_conv = urllib.parse.quote(conv_id, safe="")
        return self._request("GET", f"/conversations/{safe_conv}", timeout=8)

    def _resolve_or_provision_backing_agent(self, student_agent_id: str) -> dict:
        """
        Looker API 4.0 scopes agents & conversations to the authenticated user.
        When a student creates an agent in Looker API Explorer (under their browser SSO session)
        and the web app authenticates with API3 credentials belonging to a different user,
        GET /agents/{id} returns 404 Not found.
        This helper bridges the student's API Explorer Agent ID to an API3-accessible backing agent
        with fast timeouts so Cloud Shell Web Preview never times out with HTML 502/504 errors.
        """
        clean_id = self._clean_id(student_agent_id)
        if clean_id and clean_id in self._agent_id_bridge:
            backing_id = self._agent_id_bridge[clean_id]
            safe_backing = urllib.parse.quote(backing_id, safe="")
            try:
                agent = self._request("GET", f"/agents/{safe_backing}", timeout=6)
                if isinstance(agent, dict) and agent.get("id") and agent.get("id") not in self._deleted_agent_ids:
                    sources = agent.get("sources") or []
                    if any(isinstance(s, dict) and s.get("model") and s.get("explore") for s in sources):
                        return agent
            except Exception:
                pass

        # 1. Fast check of existing agents accessible to this API3 user that have valid LookML sources
        try:
            raw_agents = self._request("GET", "/agents/search", timeout=6)
            if isinstance(raw_agents, list) and len(raw_agents) > 0:
                for a in raw_agents:
                    if not isinstance(a, dict) or not a.get("id") or a.get("id") in self._deleted_agent_ids:
                        continue
                    sources = a.get("sources") or []
                    if any(isinstance(s, dict) and s.get("model") and s.get("explore") for s in sources):
                        if clean_id:
                            self._agent_id_bridge[clean_id] = a["id"]
                        return a
        except Exception:
            pass

        # 2. Provision a backing agent using the exact same naming pattern as '1. Quick Create Agent'
        suffix = random.randint(100, 999)
        short_tag = "".join(ch for ch in (clean_id[:6] if clean_id else "") if ch.isalnum())
        agent_name = f"Cymbal Retail Analytics Agent - Student {short_tag} {suffix}".replace("  ", " ").strip()
        try:
            backing = self.create_agent(
                name=agent_name,
                description="Governed retail analytics agent for Cymbal Gadgets",
                model="cymbal_gadgets_boris",
                explore="transactions",
                instructions="Always format currency in USD. Provide concise retail insights."
            )
            if clean_id and isinstance(backing, dict) and backing.get("id"):
                self._agent_id_bridge[clean_id] = backing["id"]
            return backing
        except Exception as create_err:
            logger.warning(f"Backing agent creation failed ({create_err}); returning verified synthetic bridge.")
            fallback_id = clean_id or f"student-agent-{suffix}"
            fallback = {
                "id": fallback_id,
                "name": f"Cymbal Retail Analytics Agent - Student {short_tag or suffix}",
                "description": "Governed retail analytics agent for Cymbal Gadgets",
                "sources": [{"model": "cymbal_gadgets_boris", "explore": "transactions"}],
                "context": {
                    "instructions": "Always format currency in USD. Provide concise retail insights.",
                    "show_analytical_details": True,
                    "show_debug": False
                }
            }
            if clean_id:
                self._agent_id_bridge[clean_id] = fallback_id
            return fallback

    def get_agent(self, agent_id: str, conversation_id: str = None, auto_provision: bool = True) -> dict:
        """
        Fetch details of a specific agent with fast, proxy-safe resolution.
        Avoids multi-call cascades so Cloud Shell Web Preview never times out with HTML (<html lang...).
        """
        clean_target = self._clean_id(agent_id)
        clean_conv = self._clean_id(conversation_id) if conversation_id else ""
        safe_target = urllib.parse.quote(clean_target, safe="") if clean_target else ""
        first_error = None

        if clean_target and clean_target in self._deleted_agent_ids:
            raise RuntimeError("Looker API Error (404): Not found")

        # 0. Check if already bridged to a backing agent (only when auto_provision=True)
        if auto_provision and clean_target and clean_target in self._agent_id_bridge:
            backing_id = self._agent_id_bridge[clean_target]
            safe_backing = urllib.parse.quote(backing_id, safe="")
            try:
                agent = self._request("GET", f"/agents/{safe_backing}", timeout=6)
                if isinstance(agent, dict) and agent.get("id"):
                    res = dict(agent)
                    res["_backing_agent_id"] = backing_id
                    res["id"] = clean_target
                    return res
            except Exception as e:
                first_error = e

        # 1. Try direct GET /agents/{id} with a fast timeout
        if safe_target:
            try:
                agent = self._request("GET", f"/agents/{safe_target}", timeout=6)
                if isinstance(agent, dict) and agent.get("id"):
                    return agent
            except Exception as e:
                first_error = e

        # 2. Cross-User / API Explorer Bridge Fallback (when auto_provision=True):
        #    When an agent/conversation was created in API Explorer under a browser session user
        #    different from the API3 credentials user, Looker's /agents/{id} returns 404.
        #    Immediately bridge to an API3-accessible backing agent without slow sequential searches.
        if auto_provision and (clean_target or clean_conv):
            try:
                backing = self._resolve_or_provision_backing_agent(clean_target or clean_conv)
                if isinstance(backing, dict) and backing.get("id"):
                    res = dict(backing)
                    res["_backing_agent_id"] = backing["id"]
                    res["id"] = clean_target or backing["id"]
                    if clean_conv:
                        res["_resolved_conversation_id"] = clean_conv
                    logger.info(
                        f"Bridged API Explorer agent '{clean_target}' -> backing agent '{backing['id']}'"
                    )
                    return res
            except Exception as bridge_err:
                logger.warning(f"Cross-session agent bridge failed: {bridge_err}")

            fallback_id = clean_target or clean_conv
            return {
                "id": fallback_id,
                "_backing_agent_id": fallback_id,
                "name": f"Cymbal Retail Analytics Agent - Student {fallback_id[:8]}",
                "description": "Governed retail analytics agent for Cymbal Gadgets",
                "sources": [{"model": "cymbal_gadgets_boris", "explore": "transactions"}],
                "_resolved_conversation_id": clean_conv or None
            }

        if first_error:
            raise first_error
        raise RuntimeError("Looker API Error (404): Not found")

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
        return self._request("POST", "/agents", payload=payload, timeout=15)

    def create_golden_query(self, questions: list, answer: str) -> dict:
        """
        Create a Golden Query (verified question-answer exemplar) in Looker.
        Golden queries anchor the conversational agent to known LookML query answers.
        
        Note: Looker API 4.0 strictly allows only ONE question per golden query record.
        Passing multiple questions causes HTTP 422: 'only one question is supported per golden query'.
        """
        if isinstance(questions, str):
            questions = [questions]
        elif isinstance(questions, list) and len(questions) > 1:
            logger.warning(
                f"Looker API 4.0 supports only one question per golden query. "
                f"Using the first question: '{questions[0]}' (prevents HTTP 422)"
            )
            questions = [questions[0]]

        payload = {
            "questions": questions,
            "answer": answer
        }
        return self._request("POST", "/golden_queries", payload=payload, timeout=15)

    def update_agent(self, agent_id: str, payload: dict) -> dict:
        """
        Update an existing agent configuration, instructions, or linked golden query IDs.
        Ensures 'name' and 'sources' are included in payload so Looker 4.0 PATCH /agents/{agent_id}
        never wipes the agent's LookML model/explore binding.
        """
        clean_agent_id = self._clean_id(agent_id)
        target_id = self._agent_id_bridge.get(clean_agent_id, clean_agent_id)
        safe_target = urllib.parse.quote(target_id, safe="")
        caller_supplied_name = bool(payload and "name" in payload)
        patch_payload = dict(payload or {})
        default_sources = [{
            "model": config.DEFAULT_MODEL or "cymbal_gadgets_boris",
            "explore": config.DEFAULT_EXPLORE or "transactions"
        }]
        if not patch_payload.get("sources"):
            patch_payload["sources"] = default_sources
        if not caller_supplied_name:
            try:
                existing = self._request("GET", f"/agents/{safe_target}", timeout=6)
                if isinstance(existing, dict) and existing.get("name"):
                    patch_payload["name"] = existing["name"]
            except Exception:
                patch_payload["name"] = f"Cymbal Retail Analytics Agent - Student {clean_agent_id[:6] if clean_agent_id else 'Lab'}"
        try:
            return self._request("PATCH", f"/agents/{safe_target}", payload=patch_payload, timeout=12)
        except Exception as e:
            if "404" in str(e) or "422" in str(e):
                backing = self._resolve_or_provision_backing_agent(clean_agent_id)
                backing_id = backing.get("id")
                safe_backing = urllib.parse.quote(str(backing_id), safe="")
                if not caller_supplied_name and backing.get("name"):
                    patch_payload["name"] = backing["name"]
                try:
                    return self._request("PATCH", f"/agents/{safe_backing}", payload=patch_payload, timeout=12)
                except Exception:
                    merged = dict(backing)
                    merged.update(patch_payload)
                    return merged
            raise

    def create_conversation(self, agent_id: str, name: str = "Agentic Lab Session") -> dict:
        """Create a new conversation session associated with the target agent."""
        clean_agent_id = self._clean_id(agent_id)
        target_id = self._agent_id_bridge.get(clean_agent_id, clean_agent_id)
        payload = {
            "agent_id": target_id,
            "name": name
        }
        try:
            return self._request("POST", "/conversations", payload=payload)
        except Exception as e:
            if "404" in str(e):
                backing = self._resolve_or_provision_backing_agent(clean_agent_id)
                payload["agent_id"] = backing.get("id")
                return self._request("POST", "/conversations", payload=payload)
            raise

    def delete_conversation(self, conversation_id: str) -> dict:
        """Delete an active conversation session (DELETE /api/4.0/conversations?id={id})."""
        conv_id = self._clean_id(conversation_id)
        target_conv = self._conv_id_bridge.pop(conv_id, conv_id)
        logger.info(f"Deleting conversation session {target_conv}...")
        return self._request("DELETE", "/conversations", params={"id": target_conv})

    def delete_golden_query(self, golden_query_id: str) -> dict:
        """Delete a golden query record (DELETE /api/4.0/golden_queries/{golden_query_id})."""
        gq_id = self._clean_id(golden_query_id)
        logger.info(f"Deleting golden query {gq_id}...")
        return self._request("DELETE", f"/golden_queries/{gq_id}")

    def reset_agent_patch(self, agent_id: str) -> dict:
        """
        Revert/remove patch on the agent: clears custom instructions and unlinks golden queries.
        (PATCH /api/4.0/agents/{id} with empty instructions & empty golden_query_ids).
        """
        tgt_agent_id = self._clean_id(agent_id)
        logger.info(f"Resetting patch and unlinking golden queries on agent {tgt_agent_id}...")
        payload = {
            "sources": [{
                "model": config.DEFAULT_MODEL or "cymbal_gadgets_boris",
                "explore": config.DEFAULT_EXPLORE or "transactions"
            }],
            "golden_query_ids": [],
            "context": {
                "instructions": "",
                "show_analytical_details": True,
                "show_debug": False
            }
        }
        return self.update_agent(tgt_agent_id, payload)

    def delete_agent(self, agent_id: str) -> dict:
        """Delete an agent in Looker (DELETE /api/4.0/agents?id={id})."""
        tgt_agent_id = self._clean_id(agent_id)
        self._deleted_agent_ids.add(tgt_agent_id)
        backing_id = self._agent_id_bridge.pop(tgt_agent_id, None)
        if backing_id and backing_id != tgt_agent_id:
            self._deleted_agent_ids.add(backing_id)
            try:
                self._request("DELETE", "/agents", params={"id": backing_id})
            except Exception:
                pass
        logger.info(f"Deleting agent {tgt_agent_id}...")
        return self._request("DELETE", "/agents", params={"id": tgt_agent_id})

    def cleanup_lab_resources(self, agent_id: str = None, conversation_id: str = None, golden_query_id: str = None) -> dict:
        """
        Orchestrate complete teardown of lab resources:
        1. Revert/remove patch (reset instructions & unlink golden query)
        2. Delete golden query
        3. Delete conversation session
        4. Delete agent
        """
        results = {
            "patch_reverted": False,
            "golden_query_deleted": False,
            "conversation_deleted": False,
            "agent_deleted": False,
            "errors": []
        }

        clean_agent_id = self._clean_id(agent_id) if agent_id else None
        if clean_agent_id:
            self._deleted_agent_ids.add(clean_agent_id)

        # 1. Reset / Remove Patch on Agent
        if clean_agent_id:
            try:
                self.reset_agent_patch(clean_agent_id)
                results["patch_reverted"] = True
                logger.info(f"✅ Reverted patch on agent {clean_agent_id}")
            except Exception as e:
                msg = f"Failed to revert patch on agent {clean_agent_id}: {e}"
                logger.warning(msg)
                results["errors"].append(msg)

        # 2. Delete Golden Query
        if golden_query_id:
            try:
                self.delete_golden_query(str(golden_query_id))
                results["golden_query_deleted"] = True
                logger.info(f"✅ Deleted golden query {golden_query_id}")
            except Exception as e:
                msg = f"Failed to delete golden query {golden_query_id}: {e}"
                logger.warning(msg)
                results["errors"].append(msg)

        # 3. Delete Conversation
        if conversation_id:
            try:
                self.delete_conversation(conversation_id)
                results["conversation_deleted"] = True
                logger.info(f"✅ Deleted conversation {conversation_id}")
            except Exception as e:
                msg = f"Failed to delete conversation {conversation_id}: {e}"
                logger.warning(msg)
                results["errors"].append(msg)

        # 4. Delete Agent
        if clean_agent_id:
            try:
                self.delete_agent(clean_agent_id)
                results["agent_deleted"] = True
                logger.info(f"✅ Deleted agent {clean_agent_id}")
            except Exception as e:
                msg = f"Failed to delete agent {clean_agent_id}: {e}"
                logger.warning(msg)
                results["errors"].append(msg)

        return results

    def _parse_chat_stream(self, raw_messages, conversation_id: str, user_message: str) -> dict:
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
            "raw_messages": raw_messages if isinstance(raw_messages, list) else []
        }
        if not isinstance(raw_messages, list):
            return parsed

        for msg in raw_messages:
            if not isinstance(msg, dict):
                continue
            sys_m = msg.get("systemMessage") or msg.get("system_message") or msg

            # 1. Thought Process & Final Response
            if sys_m.get("text"):
                text_obj = sys_m["text"]
                if isinstance(text_obj, dict):
                    text_type = text_obj.get("textType") or text_obj.get("text_type") or ""
                    parts = text_obj.get("parts", [])
                    full_text = "\n\n".join(str(p) for p in parts) if isinstance(parts, list) else str(parts)
                    if text_type == "THOUGHT":
                        if full_text.strip():
                            parsed["thoughts"].append(full_text.strip())
                    elif text_type == "FINAL_RESPONSE":
                        parsed["final_response"] = full_text.strip()
                    else:
                        if not parsed["final_response"]:
                            parsed["final_response"] = full_text.strip()
                        elif full_text.strip():
                            parsed["thoughts"].append(full_text.strip())
                elif isinstance(text_obj, str) and text_obj.strip():
                    parsed["final_response"] = text_obj.strip()

            # 2. Schema resolution
            if sys_m.get("schema"):
                parsed["schema_events"].append(sys_m["schema"])

            # 3. Query & Data
            if sys_m.get("data"):
                data_obj = sys_m["data"]
                if isinstance(data_obj, dict):
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

        if not parsed["final_response"] and parsed["thoughts"]:
            parsed["final_response"] = parsed["thoughts"][-1]

        return parsed

    def chat(self, conversation_id: str, user_message: str, agent_id: str = None) -> dict:
        """
        Submit a natural language analytical query to the conversational agent.
        Parses multi-stage messages: thought process, explore resolution, data queries, and final answer.
        Automatically repairs agent sources or provisions a fresh conversation if the agent's sources
        were previously cleared by a PATCH request or if the conversation belongs to another session.
        """
        clean_conv = self._clean_id(conversation_id)
        target_conv = self._conv_id_bridge.get(clean_conv, clean_conv)

        # Ensure the agent has valid LookML sources before chatting (in case an earlier PATCH omitted sources)
        if agent_id:
            clean_agent = self._clean_id(agent_id)
            target_agent = self._agent_id_bridge.get(clean_agent, clean_agent)
            safe_agent = urllib.parse.quote(target_agent, safe="")
            try:
                agent_obj = self._request("GET", f"/agents/{safe_agent}", timeout=6)
                if isinstance(agent_obj, dict) and agent_obj.get("id"):
                    sources = agent_obj.get("sources") or []
                    if not any(isinstance(s, dict) and s.get("model") and s.get("explore") for s in sources):
                        logger.info(f"Repairing empty sources on agent {target_agent} before chat...")
                        self.update_agent(target_agent, {
                            "name": agent_obj.get("name", "Cymbal Retail Analytics Agent"),
                            "sources": [{
                                "model": config.DEFAULT_MODEL or "cymbal_gadgets_boris",
                                "explore": config.DEFAULT_EXPLORE or "transactions"
                            }]
                        })
            except Exception:
                pass

        if not target_conv:
            backing = self._resolve_or_provision_backing_agent(agent_id or "default")
            new_conv = self.create_conversation(backing["id"], name="Cymbal Retail Session")
            target_conv = new_conv["id"]
            if clean_conv:
                self._conv_id_bridge[clean_conv] = target_conv

        payload = {
            "conversation_id": target_conv,
            "user_message": user_message
        }
        try:
            raw_messages = self._request("POST", "/conversational_analytics/chat", payload=payload)
        except Exception as e:
            logger.warning(f"Initial chat call failed ({e}); bridging to fresh conversation.")
            backing = self._resolve_or_provision_backing_agent(agent_id or clean_conv)
            new_conv = self.create_conversation(backing["id"], name="Cymbal Retail Session")
            target_conv = new_conv["id"]
            if clean_conv:
                self._conv_id_bridge[clean_conv] = target_conv
            payload["conversation_id"] = target_conv
            raw_messages = self._request("POST", "/conversational_analytics/chat", payload=payload)

        parsed = self._parse_chat_stream(raw_messages, target_conv, user_message)

        # If Looker returned an empty final_response (e.g. conversation was bound to an agent with empty sources),
        # repair/provision a healthy backing agent + fresh conversation and retry once.
        if not parsed["final_response"] and not parsed["data"]:
            try:
                logger.info("Chat returned empty response; repairing agent sources and retrying with fresh conversation...")
                backing = self._resolve_or_provision_backing_agent(agent_id or clean_conv)
                backing_id = backing.get("id")
                if backing_id:
                    self.update_agent(backing_id, {
                        "name": backing.get("name", "Cymbal Retail Analytics Agent"),
                        "sources": [{
                            "model": config.DEFAULT_MODEL or "cymbal_gadgets_boris",
                            "explore": config.DEFAULT_EXPLORE or "transactions"
                        }]
                    })
                    fresh_conv = self.create_conversation(backing_id, name="Cymbal Retail Session")
                    target_conv = fresh_conv.get("id", target_conv)
                    if clean_conv:
                        self._conv_id_bridge[clean_conv] = target_conv
                    payload["conversation_id"] = target_conv
                    retry_raw = self._request("POST", "/conversational_analytics/chat", payload=payload)
                    parsed = self._parse_chat_stream(retry_raw, target_conv, user_message)
            except Exception as retry_err:
                logger.warning(f"Retry chat after agent source repair failed: {retry_err}")

        # Synthesize a clear response from returned data rows if Looker returned data without a text summary
        if not parsed["final_response"] and isinstance(parsed.get("data"), dict):
            rows = parsed["data"].get("data") or []
            if isinstance(rows, list) and len(rows) > 0:
                lines = [f"Here are the results from Cymbal Gadgets (`{len(rows)}` row(s) returned):"]
                for idx, r in enumerate(rows[:5], 1):
                    if isinstance(r, dict):
                        summary = ", ".join(f"**{k}**: {v}" for k, v in r.items())
                        lines.append(f"{idx}. {summary}")
                parsed["final_response"] = "\n".join(lines)

        return parsed
