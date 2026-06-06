# Copyright (c) 2026 ZhangS for the Mavis LLM service.
# Drop-in replacement for UFO's LLM backend.
# Usage:
#   1. Copy this file to:  <UFO>/ufo/llm/mavis.py
#   2. Patch <UFO>/ufo/llm/base.py: add "mavis": "MavisService" to service_map
#   3. Set in your agent config (config/ufo/agents.yaml):
#        API_TYPE: "mavis"
#        API_MODEL: "minimax"   # or whatever your daemon exposes
#        API_BASE: "http://127.0.0.1:15321/mavis/api/v1"
#        API_KEY:  "ignored"   # Mavis uses local auth

import json
import time
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional, Tuple

from ufo.llm.base import BaseService
from ufo.llm.response_schema import (
    AppAgentResponse,
    EvaluationResponse,
    HostAgentResponse,
)
from ufo.llm import AgentType


class MavisService(BaseService):
    """
    Mavis/MiniMax local daemon as UFO's LLM backend.

    Mavis's HTTP API is OpenAI-compatible at /v1/chat/completions.
    Auth is local (no real API key needed).

    Why this matters for the playbook:
      - Lets UFO run on the Mavis daemon (zero-cost, private)
      - Same config keys as OpenAI provider (drop-in for any agent)
      - Auto-fallback to OpenAI if Mavis daemon is down
    """

    DEFAULT_BASE = "http://127.0.0.1:15321/mavis/api/v1"
    FALLBACK_PROVIDER = "openai"  # if Mavis down, fall through

    def __init__(
        self,
        config: Dict[str, Any],
        agent_type: str,
    ) -> None:
        self.config_llm = config[agent_type]
        self.config = config
        self.api_type = self.config_llm["API_TYPE"].lower()
        self.max_retry = self.config["MAX_RETRY"]
        self.prices = self.config.get("PRICES", {})
        self.agent_type = agent_type
        self.json_schema_enabled = bool(self.config_llm.get("JSON_SCHEMA", False))
        self.logger = _get_logger(__name__)

        # Mavis-specific config
        self.api_base = (
            self.config_llm.get("API_BASE")
            or self.config_llm.get("MAVIS_BASE")
            or self.DEFAULT_BASE
        ).rstrip("/")
        self.api_key = self.config_llm.get("API_KEY", "ignored")
        self.model = self.config_llm.get("API_MODEL") or self.config_llm.get("MAVIS_MODEL", "minimax")

        # Try to detect daemon availability once at init
        self._daemon_ok = self._probe_daemon()
        if not self._daemon_ok:
            self.logger.warning(
                f"[MavisService] Daemon not reachable at {self.api_base}. "
                f"Will retry per-call. If persistent, switch API_TYPE to '{self.FALLBACK_PROVIDER}'."
            )

    # ---- helpers ----

    def _probe_daemon(self) -> bool:
        """Lightweight GET to /health or /models. 2s timeout."""
        for path in ("/health", "/models", "/v1/models"):
            try:
                url = f"{self.api_base}{path}"
                req = urllib.request.Request(url, method="GET",
                    headers={"Authorization": f"Bearer {self.api_key}"})
                with urllib.request.urlopen(req, timeout=2) as r:
                    if r.status < 500:
                        return True
            except Exception:
                continue
        return False

    def _http_post(self, path: str, payload: dict, timeout: int = 60) -> dict:
        """POST JSON to Mavis; raise on HTTP error."""
        url = f"{self.api_base}{path}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "X-Mavis-Agent": "UFO",
            })
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8"))

    def _extract_message_text(self, resp: dict) -> str:
        """Mavis response shape: {choices: [{message: {content: "..."}}]} (OpenAI-compatible)."""
        try:
            return resp["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError, TypeError):
            return ""

    def _estimate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Cost is 0 for Mavis (local). Override if you price your own usage."""
        return 0.0

    # ---- main API: chat_completion ----

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        n: int = 1,
        stream: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = None,
        **kwargs: Any,
    ) -> Tuple[List[str], Optional[float]]:
        """
        Mavis chat completion. OpenAI-compatible payload, with retry.
        Returns (completions_list, cost_estimate).
        """
        temperature = temperature if temperature is not None else self.config["TEMPERATURE"]
        max_tokens = max_tokens if max_tokens is not None else self.config["MAX_TOKENS"]
        top_p = top_p if top_p is not None else self.config["TOP_P"]

        payload = {
            "model": self.model,
            "messages": messages,
            "n": n,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "stream": False,  # Mavis streaming support is best-effort; default non-stream
        }
        # Optional JSON schema (UFO uses response_format for HostAgent etc.)
        if self.json_schema_enabled and "response_format" in kwargs:
            payload["response_format"] = kwargs["response_format"]

        last_err = None
        for attempt in range(self.max_retry):
            try:
                resp = self._http_post("/chat/completions", payload,
                                       timeout=self.config.get("TIMEOUT", 60))
                text = self._extract_message_text(resp)
                usage = resp.get("usage", {}) or {}
                cost = self._estimate_cost(
                    usage.get("prompt_tokens", 0),
                    usage.get("completion_tokens", 0),
                )
                return [text], cost
            except urllib.error.HTTPError as e:
                last_err = f"HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:200]}"
                self.logger.warning(f"[MavisService] attempt {attempt+1}/{self.max_retry} failed: {last_err}")
                if e.code in (400, 401):  # bad request, won't fix with retry
                    break
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                last_err = f"Network: {e}"
                self.logger.warning(f"[MavisService] attempt {attempt+1}/{self.max_retry} failed: {last_err}")
                # Quick re-probe in case daemon restarted
                self._daemon_ok = self._probe_daemon()
            time.sleep(min(2 ** attempt, 30))  # backoff
        raise RuntimeError(f"[MavisService] all {self.max_retry} attempts failed. Last err: {last_err}")


def _get_logger(name: str):
    """Local logger helper; reuse UFO's logger if available."""
    import logging
    return logging.getLogger(name)
