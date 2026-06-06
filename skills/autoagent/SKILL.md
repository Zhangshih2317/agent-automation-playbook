---
name: autoagent-zero-code
description: Zero-code Agent creation from natural language. Use when non-developers need to spin up an agent in 5 minutes. GAIA #1 open-source.
---

# AutoAgent (HKUDS)

## When to use
- End user describes agent in plain English
- Want working agent in 5 minutes
- Domain experts (not engineers) are creators

## Core technique
NL -> agent spec -> auto-generate tools, prompts, workflows.
Event-driven workflow generation. Library of common actions
(browse, code, file ops) composed via NL.

## Minimal code
```python
import autoagent
agent = autoagent.create_agent(
    description="Downloads my PRO.FILE DOKs and emails summary every Monday 9am"
)
agent.run()
```

## PRO.FILE angle
- Lower barrier for non-engineers (PA team can define own workflows)
- Auto-generates DmsBatchClient + SE COM orchestration from spec

## Pitfalls
- Quality varies; LLM-bound (GPT-4 class)
- Less control than hand-coded CrewAI/AutoGen

Repo: https://github.com/HKUDS/AutoAgent
