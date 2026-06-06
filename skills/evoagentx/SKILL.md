---
name: evoagentx-workflow-gen
description: Automated workflow generation + evolution (TextGrad/AFlow). 85%+ task success. Use when you want a workflow to self-optimize over many runs.
---

# EvoAgentX

## When to use
- Workflow can be defined as DAG of agents
- Want automatic optimization (better prompts/structure)
- Many runs available to learn from

## Core technique
Workflow generator + evolutionary optimizer. TextGrad uses
textual gradients to refine agent prompts; AFlow treats
workflow as a graph evolved via genetic algorithms.

## Minimal code
```python
from evoagentx import Workflow, EvoEngine
wf = Workflow.from_template("research-write-review")
engine = EvoEngine(workflow=wf, optimizer="textgrad")
engine.run(task="Build a market analysis report", n_iter=20)
```

## PRO.FILE angle
- Each PRO.FILE PA job = workflow (resolve -> check_out -> convert -> merge)
- EvoAgentX finds optimal DOK ordering (parallelize where independent)
- TextGrad refines DmsBatchClient invocation patterns from logs

## Pitfalls
- Needs 100+ runs for evolution to converge
- TextGrad quality depends on "gradient" LLM
- Less mature than CrewAI/AutoGen

Repo: https://github.com/EvoAgentX/EvoAgentX
