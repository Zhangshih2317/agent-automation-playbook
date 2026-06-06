---
name: se-agent-trajectory
description: Trajectory-level self-evolution (revise/reorganize/refine). SWE-bench Verified 80% solve rate, 55% relative improvement. Use when you have many past execution traces to learn from.
---

# SE-Agent

## When to use
- Have many past execution traces (successes + failures)
- Want to evolve by improving trajectories
- Code generation / SWE tasks

## Core technique
Three trajectory operations:
- **Revise**: edit single trajectory to fix errors
- **Reorganize**: combine parts of multiple trajectories
- **Refine**: distill common patterns into new trajectory

Evolutionary search over trajectory space.

## Minimal code
```python
from seagent import TrajectoryPool, Evolver
pool = TrajectoryPool.from_logs("./past_runs/")
evolver = Evolver(operations=["revise", "reorganize", "refine"])
best = evolver.evolve(pool, n_gen=10, fitness_fn=lambda t: t.success_rate)
```

## PRO.FILE angle
- Store all past DOK CheckOut/SE convert traces
- Evolve to find best CheckOut order, optimal SE settings per DOK type
- Refine: convert "5 retries" trajectories into "1-shot" patterns

## Pitfalls
- Needs rich trajectory logging from day 1
- Evolution can overfit to your specific dataset
- Compute-intensive for large pools

Repo: https://github.com/JARVIS-Xs/SE-Agent
