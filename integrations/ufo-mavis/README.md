# UFO + Mavis Integration

Drop-in replacement for UFO's LLM backend using **Mavis/MiniMax local daemon**.

## Files

| File | Purpose |
|---|---|
| `ufo/llm/mavis.py` | The `MavisService` class. Drop into `<UFO>/ufo/llm/` |
| `patch_ufo_for_mavis.py` | Patches `ufo/llm/base.py` service_map + copies mavis.py |

## Install (3 steps, 1 minute)

```bash
# 1. Patch UFO source (idempotent, creates .bak backups)
python patch_ufo_for_mavis.py --ufo-dir "C:\Users\zhangshih\Desktop\AgentAuto\UFO"

# 2. Make sure Mavis daemon is running (default port 15321)

# 3. Edit config/ufo/agents.yaml:
HOST_AGENT:
  API_TYPE: mavis        # was: openai / claude / qwen / ...
  API_MODEL: minimax
  API_BASE: http://127.0.0.1:15321/mavis/api/v1
  API_KEY: ignored       # local daemon, no real key

APP_AGENT:
  API_TYPE: mavis
  API_MODEL: minimax
  ...
```

## How it works

UFO uses a `BaseService` ABC + `service_map` factory in `ufo/llm/base.py`.
Adding `"mavis": "MavisService"` to the map routes all UFO agents
(Host/App/Evaluation/...) to a single Mavis daemon.

```python
# Inside mavis.py
class MavisService(BaseService):
    def chat_completion(self, messages, ...):
        # POST to <API_BASE>/chat/completions
        # OpenAI-compatible payload
        # Returns (text, cost=0) — local daemon
```

## What you get

| Before | After |
|---|---|
| Pay OpenAI per UFO task | Zero cost (local) |
| Data leaves your machine | Stays local |
| Need internet | Works offline |
| Locked to GPT-4 | Use any model Mavis exposes |
| Single provider | Mix: HOST uses Mavis, EVALUATION uses OpenAI |

## Caveats

- **JSON schema `response_format`**: Mavis must support structured output.
  If not, set `JSON_SCHEMA: false` in agent config.
- **Tool calling**: best-effort. Verify with a small test.
- **Token counting**: Mavis returns `usage`; cost is 0.
- **Streaming**: disabled (UFO's `chat_completion` returns tuple).

## Test

```python
# In UFO dir
python -c "
from ufo.llm import get_service, AgentType
svc = get_service.get_service('mavis', AgentType.HOST.value, 'minimax')
result, cost = svc.chat_completion(messages=[
    {'role':'system','content':'You are a helpful assistant.'},
    {'role':'user','content':'Say hello in 5 words.'}
])
print(result[0])
print('cost:', cost)
"
```

## Revert

```bash
# Restore backup (find the .bak file)
cp "C:\path\to\UFO\ufo\llm\base.py.20260606_*.bak" \
   "C:\path\to\UFO\ufo\llm\base.py"
rm "C:\path\to\UFO\ufo\llm\mavis.py"
```
