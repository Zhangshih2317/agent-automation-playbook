---
name: ace-self-reflect
description: Generator-Reflector-Curator 3-role pipeline for self-improving agents. Incremental Playbook with helpful/harmful counters. +10.6% on agent benchmarks.
---

# ACE (Agentic Context Engineering)

## When to use
- Agent must improve over time WITHOUT retraining
- Domain experts can review/refine Agent's behavior
- Need explainable improvement (every change is a tagged bullet)

## Core technique
Three roles:
- **Generator** does the task
- **Reflector** critiques (what went well/wrong, why)
- **Curator** updates the **Playbook** (tagged bullets, helpful/harmful counters)

Each new task adds/refines bullets. Avoids brevity bias and context collapse
via incremental updates instead of full rewrites.

## Minimal code
```python
class Playbook:
    def __init__(self):
        self.bullets = []  # [{tag, text, helpful, harmful}]
    def add(self, tag, text):
        self.bullets.append({"tag": tag, "text": text, "helpful": 0, "harmful": 0})
    def update_score(self, idx, helpful=True):
        if helpful: self.bullets[idx]["helpful"] += 1
        else: self.bullets[idx]["harmful"] += 1
    def best_bullets(self, k=10):  # top-k by score
        return sorted(self.bullets, key=lambda b: b["helpful"]-b["harmful"])[:k]
```

## PRO.FILE angle
- Playbook structure perfect for PRO.FILE "what works, what doesn't" knowledge
- Each bullet = a PRO.FILE workflow tip (e.g., "Always use 32-bit PS for DmsClient")
- helpful/harmful = explicit user feedback (👍/👎 on Agent output)

## Pitfalls
- Reflector needs good critique prompts (use a stronger LLM for it)
- Curator must be conservative — don't delete low-score bullets, just deprioritize
- Playbook can grow unbounded — needs periodic pruning

Repo: https://github.com/ace-agent/ace
