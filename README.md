# Agent Automation Playbook

> A practical playbook distilling 14 frontier agent automation projects into
> actionable skills, code patterns, and adoption roadmaps — with focus on
> **PRO.FILE V8 / enterprise Windows / multi-modal automation** scenarios.

[![Status](https://img.shields.io/badge/status-active-success)](#)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## Why this exists

I maintain a long-running automation pipeline against **PRO.FILE V8** (German
enterprise PDM/PLM — solid COM API, no CLI, no REST). Every week I discover
another agent framework on GitHub that solves a problem I was hand-rolling.
This repo is my **distilled working notes** — not a fork, not a tutorial —
a playbook you can read in 30 minutes and use the patterns tomorrow.

The 14 projects cover six core themes:

| Theme | What you get |
|---|---|
| Self-evolution | Agent learns new skills automatically (no retrain) |
| Self-reflection | Agent critiques its own output and improves |
| Group collaboration | Multiple agents working a task together |
| Skill extraction & reuse | Successful executions become reusable skills |
| Long-term memory | Agent remembers across sessions, days, weeks |
| Workflow generation | New workflows are generated on demand |

## Project tiers

### Tier 1 — Highest ROI
- **UFO²** ([microsoft/UFO](https://github.com/microsoft/UFO)) — Windows desktop automation
- **GenericAgent** ([lsdefine/GenericAgent](https://github.com/lsdefine/GenericAgent)) — Self-evolution + skill tree
- **CrewAI** ([crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)) — Multi-agent collaboration
- **Mem0** ([mem0ai/mem0](https://github.com/mem0ai/mem0)) — Long-term memory layer

### Tier 2 — Strong picks
- **Hindsight** — 91.4% LongMemEval precision
- **ACE** — Reflector-Curator self-improvement
- **MetaGPT** — SOP-driven software company sim
- **AutoGen** — Microsoft multi-agent orchestration

### Tier 3 — Niche but worth watching
- **Windows-MCP** — MCP-standard Windows automation
- **AutoAgent** — Zero-code agent creation
- **EvoAgentX** — Auto workflow generation + evolution
- **SE-Agent** — Trajectory-level self-evolution
- **Open Interpreter** — Local code execution via NL
- **LangGraph** — DAG-style agent workflow

## Repository layout

```
agent-automation-playbook/
├── README.md                  # you are here
├── LICENSE                    # MIT
├── docs/                      # 14 project deep-dives + 4 synthesis docs
├── skills/                    # Mavis-loadable SKILL.md for each project
├── code-examples/             # minimal reproducible demos
└── CONTRIBUTING.md            # how to add a new project
```

| You want to... | Go to |
|---|---|
| Read about a specific project | `docs/0X-project-name.md` |
| Load the project as a Mavis skill | `skills/<project>/SKILL.md` |
| Run a working demo | `code-examples/<topic>/` |
| Decide which project to use | `docs/15-six-themes-matrix.md` then `docs/17-decision-tree.md` |
| See PRO.FILE-specific application | `docs/16-pro-file-applications.md` |
| Build an adoption plan | `docs/18-adoption-roadmap.md` |

## Quick start

### As a Mavis skill library
```bash
git clone https://github.com/Zhangshih2317/agent-automation-playbook.git
# copy a single skill
cp -r agent-automation-playbook/skills/ufo2 ~/.mavis/skills/
```

### As a reference repo
Read `docs/00-overview.md` and `docs/17-decision-tree.md` first.

## Acknowledgements

This playbook stands on the shoulders of 14 open-source projects. I am not
their author — I am a heavy user. All credit for the techniques goes to the
respective maintainers.

Last updated: 2026-06-06
