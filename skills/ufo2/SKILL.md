---
name: ufo2-windows-automation
description: Windows desktop automation via Win32 + UIA + WinCOM hybrid. Saves 50% LLM calls via speculative multi-step execution. Use when automating Windows apps with no CLI/REST but COM/UIA exposed.
---

# UFO2 - Windows Desktop AgentOS

## When to use
- Target is Windows desktop app (PRO.FILE V8, Solid Edge, SAP GUI)
- No CLI/REST/OAuth but has COM or UIA controls
- Want to switch API (fast/precise) vs GUI click (universal) automatically

## Core technique
Hybrid GUI + API action layer. One LLM call predicts 3-5 upcoming
UI steps; validation checks each; only re-plan if a step failed.
51.5% reduction in LLM calls vs naive act-observe-plan-act.

## Minimal code
```python
def act(target_app, intent):
    if target_app.has_api(intent):
        return target_app.call_api(intent)         # fast
    return uia.click(target_app.find_control(intent))  # universal
plan = llm.predict_next_n_steps(ctx, n=5)
for step in plan:
    result = act(step)
    if not result.success:
        plan = llm.replan_from(step, result); break
```

## PRO.FILE angle
- WinCOM depth = talk to PRO.FILE COM objects without logged-in UI session
- DmsBatchClient = headless API; UIA = needs UI (dialogs, property sheets)
- Never let UFO2 run CheckOut via UI - ties up user's PRO.FILE session

## Pitfalls
- PiP virtual desktop required for unattended runs
- Speculative plan needs cancellation tokens
- Don't put LLM in hot path of click loop

Repo: https://github.com/microsoft/UFO
