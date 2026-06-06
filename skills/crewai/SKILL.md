---
name: crewai-multi-agent
description: Role-driven multi-agent collaboration framework. Use when a task naturally splits into 2-5 specialized roles (researcher/writer/reviewer). 40K stars, MIT, 60% Fortune 500 adoption.
---

# CrewAI

## When to use
- Task decomposes into 2-5 specialized roles
- Need shared memory across agents
- Enterprise deployment (mature, well-supported)

## Core technique
Each agent has a `role` + `goal` + `backstory`. Tasks have `expected_output`.
Agents autonomously delegate; the Crew's `Process.sequential` or `Process.hierarchical`
orchestrates execution. Memory is shared via `memory=True`.

## Minimal code
```python
from crewai import Agent, Crew, Process, Task
researcher = Agent(role="Researcher", goal="Find facts",
                  backstory="Expert at web search", allow_delegation=False)
writer = Agent(role="Writer", goal="Compose report", backstory="...")
crew = Crew(agents=[researcher, writer],
           tasks=[Task(description="Research X", agent=researcher),
                  Task(description="Write report", agent=writer)],
           process=Process.sequential, memory=True)
crew.kickoff()
```

## PRO.FILE angle
- Model as: "DOK Resolver" + "File Downloader" + "PDF Converter" + "Excel Builder"
- Each agent = one PRO.FILE subsystem (DmsBatchClient, SE COM, openpyxl, etc.)
- Shared memory = current PA job's ERP ID + DOK list

## Pitfalls
- Hierarchical process adds a manager agent = more LLM calls
- Don't enable delegation everywhere; it amplifies errors
- Always set `expected_output` explicitly or outputs are vague

Repo: https://github.com/crewAIInc/crewAI
