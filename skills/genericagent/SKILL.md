---
name: genericagent-self-evolution
description: Self-evolving agent with 4-layer hook system, generator-based streaming, multi-LLM MixinSession, and text-file memory (not in-memory dict). 3.3K LOC core, stdlib-only deps. Use when you need a minimal, self-contained, self-evolving agent.
---

# GenericAgent — Self-Evolving Agent (verified source)

> Source: lsdefine/GenericAgent, ~3.3K LOC core, 8 Python files. Read
> directly: `agent_loop.py` (133L), `agentmain.py` (304L), `ga.py` (the
> handler), `llmcore.py` (60KB LLM clients), `mykey_template.py` (32KB
> i18n prompts).

## When to use
- Need a self-contained agent (no LangChain, no heavy stack)
- Want **multi-LLM fallback** in one process (Claude + GPT + custom)
- Want **4 hook points** to inject observability/control without modifying core
- Accept file-based memory (txt files) instead of in-memory dict

## Core technique (verified from `agent_loop.py`)

**A. Generator-based agent loop** — not a "while True call LLM" loop.
The core is `agent_runner_loop(client, system_prompt, user_input, handler,
tools_schema, max_turns=40)` which **yields** status strings as it goes.
Each `yield` is a progress event; consumers can stream to UI.

```python
for chunk in agent_runner_loop(client, sys_prompt, user_input, handler, tools):
    sys.stdout.write(chunk)
```

**B. 4-level hook system** — not just "before/after agent".
The `_hook('name', locals())` calls trigger registered callbacks at:
- `agent_before` / `agent_after` — outer wrapper (turn limits, logging)
- `turn_before` / `turn_after` — between turns
- `llm_before` / `llm_after` — around LLM call (measure latency, swap client)
- `tool_before` / `tool_after` — around each tool dispatch

Loaded from `plugins/hooks.py` via `discover_and_load()` at startup. **This is
how you add logging/metrics/control without touching the core loop.**

**C. Tool dispatch via reflection** — not a registry.
`BaseHandler.dispatch(tool_name, args, ...)` looks for `do_<tool_name>` method
on the handler. If found, calls it (also a generator). If not, returns
`StepOutcome(next_prompt=f"未知工具 {tool_name}")` which becomes a prompt
to the LLM explaining the bad call.

```python
class MyHandler(BaseHandler):
    def do_get_weather(self, args, response):
        city = args['city']
        yield f"Fetching weather for {city}..."
        data = call_weather_api(city)
        yield f"Weather: {data}"
        return StepOutcome(data=data, next_prompt="Tell user the weather")
```

**D. Multi-LLM MixinSession** — fall through providers.
`llmcore.py`'s `MixinSession` wraps multiple `NativeClaudeSession` /
`NativeOAISession` and rotates on rate-limit/error. The active client
(`self.llmclient = self.llmclients[no % len]`) is a `ToolClient` or
`NativeToolClient` wrapper that exposes `.chat(messages, tools)`.

**E. Text-file memory, not dict.**
- L1 routing: `memory/global_mem_insight.txt` (free-form notes the LLM reads)
- L2 facts: `memory/global_mem.txt` (the durable fact store)
- L3 skills: not files — see `ga.py`'s `GenericAgentHandler` for the actual
  Skill crystallization (3+ successful uses → add to skill list)

## Minimal code (rebuilt from real patterns)

```python
# Hook-based agent loop (simplified, ~60 LOC)
class StepOutcome:
    def __init__(self, data=None, next_prompt=None, should_exit=False):
        self.data, self.next_prompt, self.should_exit = data, next_prompt, should_exit

class Handler:
    def turn_end_callback(self, response, tool_calls, tool_results,
                          turn, next_prompt, exit_reason): return next_prompt
    def dispatch(self, tool_name, args, response, **kw):
        method = getattr(self, f"do_{tool_name}", None)
        if not method:
            yield f"Unknown tool: {tool_name}\n"
            return StepOutcome(next_prompt=f"unknown_tool:{tool_name}")
        yield from method(args, response)

def agent_loop(client, sys_prompt, user_input, handler, tools,
               max_turns=40, hook=lambda *a, **k: None):
    msgs = [{"role":"system","content":sys_prompt},
            {"role":"user","content":user_input}]
    for turn in range(1, max_turns+1):
        hook("llm_before", turn=turn)
        response = client.chat(msgs, tools=tools)
        hook("llm_after", turn=turn, response=response)
        # Reset tool schema every 10 turns (keep prompt fresh)
        if turn % 10 == 0: client.last_tools = ""
        # Dispatch each tool call
        results = []; next_prompts = set()
        for tc in (response.tool_calls or [{"function":{"name":"no_tool"},"id":""}]):
            outcome = yield from handler.dispatch(
                tc["function"]["name"],
                json.loads(tc["function"]["arguments"]),
                response
            )
            if outcome.should_exit: return outcome.data
            if outcome.next_prompt: next_prompts.add(outcome.next_prompt)
            if outcome.data: results.append({"tool_use_id": tc["id"],
                                              "content": str(outcome.data)})
        if not next_prompts: break
        msgs.append({"role":"user",
                     "content":"\n".join(next_prompts),
                     "tool_results": results})
    return None
```

## PRO.FILE angle (concrete)

For MUBEA's PRO.FILE automation:

1. **Wrap DmsBatchClient as tools**:
```python
class ProfileHandler(Handler):
    def do_resolve_dok(self, args, response):
        yield f"Resolving DOK {args['dok_id']}..."
        guid = dms_batch.GetDocumentLatestVersion(str(args['dok_id']))
        return StepOutcome(data=guid, next_prompt=f"DOK {args['dok_id']} -> {guid}")
    def do_checkout_dft(self, args, response):
        yield f"Checking out {args['guid']}..."
        dms_batch.CheckOutDocument(args['guid'], args['target_path'])
        return StepOutcome(next_prompt="OK")
    def do_se_convert(self, args, response):
        yield f"Converting {args['dft_path']}..."
        se.Documents.Open(args['dft_path']).SaveAs(args['pdf_path'])
        return StepOutcome(next_prompt="OK")
```

2. **Add hooks for observability**:
```python
def metrics_hook(name, **kw):
    if name == "tool_after":
        dur = kw.get("end_time", 0) - kw.get("start_time", 0)
        metrics.record(f"tool.{kw.get('tool_name')}", dur)

hook = metrics_hook
# pass to agent_loop
```

3. **Multi-LLM fallback** — if GPT hits rate limit, fall through to Claude:
   Use `MixinSession` with both `NativeOAISession` and `NativeClaudeSession`.

## Pitfalls (from real source)

- `last_tools` must reset every 10 turns (in agent_loop.py:56) — else the
  tool schema stays pinned and the LLM sees stale descriptions
- Hook exceptions are silently swallowed (`try/except: pass` in
  `discover_and_load`) — don't rely on hooks for critical logic
- Text-file memory is **not concurrency-safe** — use `threading.Lock` on
  `GenericAgent` for multi-threaded access
- `do_<tool_name>` lookup is **case-sensitive and exact** — typos = unknown_tool
- `_clean_content` shrinks long code blocks (preview 5 lines) — disable
  if you need full LLM output
- L1 + L2 are loaded into **system prompt at startup** — not per-turn
  reloaded. Edit `global_mem.txt` then re-init agent to see changes

## Repo
https://github.com/lsdefine/GenericAgent (~4K stars, MIT)
