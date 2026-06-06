---
name: genericagent-self-evolution
description: Self-evolving agent that crystallizes repeated paths into reusable Skills. 3.3K LOC core, 6x token efficient. Use when same workflow repeats 3+ times.
---

# GenericAgent

## When to use
- Same task done 3+ times → should become a Skill
- 5-layer memory fits human cognition
- Token budget tight

## Core technique
After every task success, rewrite the execution path as a parameterized
Skill stored in L3. Future invocations of the same pattern skip LLM planning.

Layers:
- L0 Meta Rules (behavioral constraints)
- L1 Insight Index (fast routing)
- L2 Global Facts (stable domain knowledge)
- L3 Task Skills (reusable SOPs, the value)
- L4 Session Archive (raw history)

## Minimal code
```python
class SkillTree:
    def find_match(self, sig):
        for s in self.skills:
            if s.signature == sig: return s  # skip LLM
    def crystallize(self, sig, steps, success):
        if not success: return
        if self.use_count[sig] < 3: return  # only after 3
        self.skills.append(Skill(sig, steps)); self._persist()
```

## PRO.FILE angle
- "PRO.FILE BOM export" has 10 SOPs that re-run weekly
- L3 cache cuts planning from 30s to 1s
- L1 signature = (erp_id, dok_ext, action)

## Pitfalls
- Crystallize only after N=3+ successful uses
- Skills must be parameterized at first use
- L1 index must be O(1)

Repo: https://github.com/lsdefine/GenericAgent
