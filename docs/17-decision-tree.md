# Decision Tree — Which Project Should I Use?

> "I want to do X, which project from the playbook?"

## Q1: Is the target a Windows desktop app?

- **Yes** (PRO.FILE, Solid Edge, SAP GUI, Office, etc.):
  - Q1a: Does the user have an MCP-compatible client (Claude Desktop, Mavis)?
    - Yes -> **Windows-MCP** (drop-in MCP server)
    - No -> Q1b: Do you need both UI and headless (COM) calls?
      - Yes -> **UFO²** (Win32 + UIA + WinCOM hybrid, 51.5% LLM call reduction)
      - No, just ad-hoc local code -> **Open Interpreter** (NL to local code)
- **No** (web, file system, REST APIs):
  - Go to Q2

## Q2: Is the task a single agent or multiple?

- **Multiple agents**:
  - Q2a: Is the workflow well-defined stages (PM -> Architect -> Engineer)?
    - Yes -> **MetaGPT** (SOP-driven)
    - No -> Q2b: Is the conversation event-driven (interruptions, handoffs)?
      - Yes -> **AutoGen** (Microsoft, event-driven chat)
      - No -> **CrewAI** (role-driven, 40K stars, 60% Fortune 500)
- **Single agent**:
  - Go to Q3

## Q3: Does the agent need to remember past sessions?

- **Yes, simple** (facts about the user, recent decisions):
  - **Mem0** (48K stars, vector store, two-line API)
- **Yes, high precision** (legal, financial, time-anchored queries):
  - **Hindsight** (91.4% LongMemEval, 4-way retrieval)
- **No** (stateless each call):
  - Go to Q4

## Q4: Does the agent need to improve over time?

- **Yes, from many execution traces**:
  - Q4a: Are the traces structured (steps + outcomes)?
    - Yes -> **SE-Agent** (trajectory-level evolution, 80% SWE-bench)
    - No -> Q4b: Can you write critiques in natural language?
      - Yes -> **ACE** (Generator-Reflector-Curator Playbook)
      - No -> **GenericAgent** (auto-crystallizes Skills after N uses)
- **Yes, from workflow execution**:
  - **EvoAgentX** (TextGrad / AFlow, optimizes prompts + DAG)
- **No**:
  - Go to Q5

## Q5: Is the workflow a DAG / state machine?

- **Yes**:
  - Q5a: Need checkpointing and time-travel debugging?
    - Yes -> **LangGraph** (PostgreSQL/SQLite checkpoints)
    - No -> Q5b: Want evolutionary optimization of the DAG?
      - Yes -> **EvoAgentX** (AFlow mode)
      - No -> **LangGraph** (still works, just static DAG)
- **No** (linear):
  - Single agent + CrewAI or AutoGen are enough; don't over-engineer

## Q6: Are non-engineers creating the agents?

- **Yes**:
  - **AutoAgent** (NL to agent, 5-minute setup)
- **No** (engineers fine with code):
  - Use the rest of the tree

## Quick reference by use case

| Use case | Pick |
|---|---|
| "Automate PRO.FILE / Solid Edge" | UFO² + DmsBatchClient |
| "Multiple specialists collaborate" | CrewAI |
| "Need long-term memory, simple" | Mem0 |
| "Need long-term memory, precise" | Hindsight |
| "Agent should learn from doing" | GenericAgent or SE-Agent |
| "Agent should reflect on its work" | ACE |
| "Run code locally from NL" | Open Interpreter |
| "MCP client needs Windows" | Windows-MCP |
| "Workflow with checkpoints" | LangGraph |
| "Workflow that evolves" | EvoAgentX |
| "Generate full project from spec" | MetaGPT |
| "Multi-party chat with humans" | AutoGen |
| "Non-dev creates agents" | AutoAgent |
