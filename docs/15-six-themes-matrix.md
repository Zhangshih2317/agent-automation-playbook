# Six-Themes Coverage Matrix

## Legend
- ●●● = core strength (this project IS this theme)
- ●●  = strong support
- ●   = supports but not the focus
- ◐   = partial / niche
- ○   = not directly supported

## The matrix

| Project | Self-evol | Reflect | Collabor | Skill-reuse | Memory | Workflow | Desktop |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **UFO²** | ◐ | ◐ | ● | ◐ | ● | ○ | ●● |
| **GenericAgent** | ●● | ◐ | ○ | ●● | ●● | ○ | ● |
| **CrewAI** | ○ | ○ | ●● | ○ | ● | ● | ○ |
| **Mem0** | ○ | ○ | ○ | ○ | ●●● | ○ | ○ |
| **Hindsight** | ○ | ●● | ○ | ○ | ●●● | ○ | ○ |
| **ACE** | ●● | ●●● | ○ | ◐ | ● | ○ | ○ |
| **MetaGPT** | ○ | ○ | ●● | ◐ | ◐ | ●● | ○ |
| **AutoGen** | ○ | ○ | ●● | ○ | ◐ | ● | ○ |
| **Windows-MCP** | ○ | ○ | ○ | ○ | ○ | ○ | ●● |
| **AutoAgent** | ● | ◐ | ● | ● | ● | ●● | ○ |
| **EvoAgentX** | ●● | ◐ | ● | ◐ | ◐ | ●● | ○ |
| **SE-Agent** | ●●● | ●● | ◐ | ◐ | ◐ | ○ | ○ |
| **Open Interpreter** | ○ | ○ | ○ | ○ | ◐ | ○ | ● |
| **LangGraph** | ○ | ○ | ● | ○ | ◐ | ●● | ○ |

## How to read this

- **If memory is the core problem**: Mem0 (simple) or Hindsight (precise).
  Don't try to bolt memory onto CrewAI or AutoGen — use the dedicated tool.
- **If collaboration is the core problem**: CrewAI (roles), AutoGen (chat),
  MetaGPT (SOP). Pick by topology.
- **If self-evolution is the core problem**: SE-Agent (trajectory), ACE
  (Playbook), GenericAgent (skill tree), EvoAgentX (DAG evolution).
  Pick by what kind of "evolution unit" you have.
- **If Windows desktop is involved**: UFO² is dominant. Windows-MCP for
  MCP clients, Open Interpreter for ad-hoc scripts.
- **Workflow as DAG**: LangGraph (state machine), EvoAgentX (evolving),
  MetaGPT (one-shot generation).

## Coverage by theme

### Self-evolution
- **●●●** SE-Agent (trajectory-level, proven 80% SWE-bench)
- **●●  ** GenericAgent (skill crystallization, 6x token efficient)
- **●●  ** EvoAgentX (TextGrad/AFlow, 85%+ task success)
- **●●  ** ACE (Playbook bullets, +10.6% on agent benchmarks)

### Self-reflection
- **●●●** ACE (Reflector role is the headline)
- **●●  ** Hindsight (CARA reflection over memory)
- **●●  ** SE-Agent (refine from failure traces)

### Group collaboration
- **●●  ** CrewAI (role-driven, 60% Fortune 500)
- **●●  ** MetaGPT (SOP-driven software company)
- **●●  ** AutoGen (event-driven multi-party chat)

### Skill extraction & reuse
- **●●  ** GenericAgent (5-layer memory L3)
- **●   ** UFO² (RAG over past executions)
- **●   ** ACE (Playbook bullets)
- **●   ** AutoAgent (generated agents are reusable)

### Long-term memory
- **●●●** Mem0 (48K stars, simple API)
- **●●●** Hindsight (91.4% LongMemEval, 4-way retrieval)

### Workflow generation
- **●●  ** MetaGPT (one-shot full project)
- **●●  ** AutoAgent (NL → agent + workflow)
- **●●  ** EvoAgentX (DAG with optimizer)
- **●●  ** LangGraph (state machine + checkpoints)

### Windows desktop automation
- **●●  ** UFO² (Win32 + UIA + WinCOM)
- **●●  ** Windows-MCP (MCP server)
- **●   ** Open Interpreter (NL → local code)
- **●   ** GenericAgent (keyboard/mouse tools)
