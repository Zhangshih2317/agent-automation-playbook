---
name: mem0-memory-layer
description: Long-term memory layer for agents. Use when agent must remember user prefs, prior decisions, domain facts across sessions. Vector + graph store, 48K stars.
---

# Mem0

## When to use
- Cross-session user preference memory
- Agent needs to "remember" prior decisions
- Decoupled memory (separate service, framework-agnostic)

## Core technique
Three memory types: User (per user), Session (per chat), Agent (shared).
`memory.add(messages)` extracts facts via LLM and stores in vector DB.
`memory.search(query)` retrieves by similarity. Two-line API.

## Minimal code
```python
from mem0 import Memory
m = Memory()
m.add([{"role": "user", "content": "I prefer dft over step files"}])
results = m.search("what file format does user want?", user_id="zhangsih")
# returns: [{"memory": "User prefers dft over step files", "score": 0.91}]
```

## PRO.FILE angle
- User memory: "ZhangS prefers naming convention PA-NNN {ERP} v1.0"
- Agent memory: "PRO.FILE CheckOut requires DmsBatchClient permissions"
- LongMemEval: 49% (lower than Hindsight 91%) — combine with Hindsight for time-aware recall

## Pitfalls
- Graph store (relationships) is Pro-only ($249/mo) on hosted plan
- Open-source uses Qdrant/Chroma — self-host required for production
- Memory decay not built-in; old facts linger unless you prune

Repo: https://github.com/mem0ai/mem0
