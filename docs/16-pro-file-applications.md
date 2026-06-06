# PRO.FILE V8 Specific Applications

> How each project applies to a real PRO.FILE V8 / MUBEA workflow.

## The 4-layer PRO.FILE automation stack

```
Layer 4: Evolution       SE-Agent (trajectory), EvoAgentX (DAG)
Layer 3: Collaboration   CrewAI, LangGraph
Layer 2: Intelligence    GenericAgent, ACE, Mem0/Hindsight
Layer 1: Execution       UFO2 + DmsBatchClient + Solid Edge COM
```

## Project-by-project PRO.FILE angle

### UFO2 + DmsBatchClient (the workhorse)
- DmsBatchClient: 22 headless methods. Use for everything you can.
- UFO2: For dialogs only (CheckOut confirm, property sheets).
- Combo: 95% DmsBatch + 5% UFO2 (UI confirmations).

### GenericAgent - do once, repeat forever
- 5-layer memory maps to PRO.FILE:
  - L0: "Never CheckOut to root of C:\\"
  - L1: signature = (erp_id, dok_ext, action)
  - L2: DOK schema, field meanings
  - L3: actual Skills (resolve, check_out, convert, merge)
  - L4: raw job logs (post-mortems)
- After 3 PA jobs, the 4th is mostly Skill execution (no LLM planning).

### CrewAI - the team
Roles:
- DOK Resolver (SQL + GetDocumentLatestVersion)
- File Downloader (DmsBatchClient.CheckOut)
- SE Converter (Solid Edge COM)
- Excel Builder (openpyxl)
- PDF Merger (PDF24 CLI or pypdf)

Shared memory = current job's ERP ID + DOK list. Process: hierarchical.

### Mem0 / Hindsight - the long memory
- User memory (per ZhangS): "prefers PA-NNN {ERP} v1.0"
- Agent memory (all users): "PRO.FILE CheckOut requires DmsBatchClient perms"
- Use Hindsight if you need "what did we decide 3 months ago about X?"

### ACE - the playbook
Each bullet = a PRO.FILE gotcha. Examples:
- "Always use 32-bit PS for DmsBatchClient" (helpful: 47, harmful: 0)
- "Never CheckOut to C:\\ root" (helpful: 23, harmful: 1)
- "SE COM requires Visible=False before SaveAs" (helpful: 31, harmful: 0)

Reflector reads failed runs and proposes new bullets.

### LangGraph - the state machine
PA job as DAG:
```
BFS -> DOK resolve -> check_out -> SE convert -> merge -> email
```
Checkpoints = survive process crashes. Time-travel = "which DOK failed".

### SE-Agent - the evolution engine
Store all past PA job traces (JSON log of each step).
Evolve to find: best CheckOut order, optimal SE settings per DOK type.
Refine: convert "5 retries" trajectories into "1-shot" patterns.

## Practical recommendation for MUBEA / PRO.FILE

Phase 1 (Week 1-2): Solidify execution
- DmsBatchClient for headless ops
- UFO2 only where UI is required
- RawInput recorder for repetitive UI sequences

Phase 2 (Week 3-4): Add intelligence
- GenericAgent with 5-layer memory for repeated PA jobs
- ACE Playbook for tribal knowledge

Phase 3 (Month 2): Add collaboration
- CrewAI for the standard 5-role team
- LangGraph for resumable PA jobs

Phase 4 (Month 3+): Add evolution
- SE-Agent on accumulated trace logs
- Hindsight for "what did we decide about X" queries
