---
name: langgraph-dag
description: DAG-style agent workflow orchestration. Built-in state management, checkpointing, time-travel debugging. 19K stars. Use when your agent workflow is naturally a state machine.
---

# LangGraph

## When to use
- Workflow is naturally a state machine / DAG
- Need checkpointing and time-travel debugging
- Want persistence + resumability for long workflows

## Core technique
Define graph of nodes (functions) and edges (transitions).
State is typed object passed between nodes. Built-in
checkpointing (PostgreSQL/SQLite) lets you resume from any step.

## Minimal code
```python
from langgraph.graph import StateGraph
class S(TypedDict): msgs: list; done: bool
def plan(s): return {"msgs": s["msgs"]+["plan"]}
def execute(s): return {"msgs": s["msgs"]+["execute"]}
g = StateGraph(S)
g.add_node("plan", plan); g.add_node("execute", execute)
g.add_edge("plan", "execute")
g.set_entry_point("plan")
app = g.compile()
app.invoke({"msgs": [], "done": False})
```

## PRO.FILE angle
- Model PRO.FILE PA job as DAG: BFS -> DOK resolve -> check_out -> SE convert -> merge -> email
- Checkpointing = survive process crashes (PRO.FILE has 32/64-bit process issues)
- Time-travel = debug "which DOK failed" by replaying from that step

## Pitfalls
- Adds LangGraph dependency
- Steeper learning curve than simple agent loops
- For linear workflows, simpler frameworks are enough

Repo: https://github.com/langchain-ai/langgraph
