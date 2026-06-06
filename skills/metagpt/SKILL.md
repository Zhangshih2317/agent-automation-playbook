---
name: metagpt-sop-agents
description: SOP-driven multi-agent software company. PM/Architect/Engineer/QA roles. Use when a process has well-defined stages and you want each stage handled by a specialist.
---

# MetaGPT

## When to use
- Task has clear stages (design -> implement -> test)
- Want full project from one-line spec
- 60K+ stars, MIT

## Core technique
Code = SOP(Team). Each role follows Standard Operating Procedure:
PM -> PRD, Architect -> design, Engineer -> code, QA -> tests.

## Minimal code
```python
from metagpt.software_company import SoftwareCompany
async def main():
    company = SoftwareCompany()
    company.invest(seed=42)
    await company.run("Build a CLI tool to count Python LOC")
```

## PRO.FILE angle
- Less natural fit (PRO.FILE ops not pure software)
- Good for: generating boilerplate (test cases, BFS queries, UIA scripts)

## Pitfalls
- Heavy deps; expensive on long projects
- Output quality depends on LLM

Repo: https://github.com/FoundationAgents/MetaGPT
