# Adoption Roadmap (30 / 60 / 90 day)

A practical timeline for adopting the 14-project playbook in a real
PRO.FILE V8 / enterprise Windows context.

## Pre-requisites (Day 0)
- [ ] Read `00-overview.md`, `15-six-themes-matrix.md`, `17-decision-tree.md`
- [ ] Identify your 2-3 highest-pain workflows (the ones repeated 3+ times/week)
- [ ] Inventory: what tools/scripts do you have today?
- [ ] Get buy-in: which workflows are safe to automate first?

## Day 1-30: Foundation

### Goal
Solidify the **execution layer**. Get one workflow 100% reliable.

### Actions
1. **Set up RawInput recorder** (the technique from the playbook)
   - 1 week to record + replay 5 different UI sequences
   - Save templates for: CheckOut dialog, version picker, file save
2. **Wrap DmsBatchClient in Python** (if not already)
   - 22 methods, 32-bit PS only (SysWOW64)
   - Add a thin Python wrapper for non-PS callers
3. **Pick ONE Tier 1 project** that matches your top pain:
   - Windows UI pain -> **UFO²** + UFO2-HYBRID mode
   - Repeated workflows -> **GenericAgent** skill crystallization
   - Multiple specialists needed -> **CrewAI** 5-role team
4. **Build one demo** that combines RawInput + DmsBatchClient + (your pick)
5. **Measure**: time saved per run, error rate, manual interventions

### Success criteria
- 1 workflow running end-to-end automatically
- 0 manual interventions per run
- Time per run cut by 50%+

## Day 31-60: Intelligence

### Goal
Add **memory + self-improvement** to the working workflow.

### Actions
1. **Add Mem0** to your framework
   - User preferences (naming conventions, default paths)
   - Agent facts (PRO.FILE quirks, COM API gotchas)
2. **Set up ACE Playbook** (or simple JSON-based)
   - First 10 bullets = the "tribal knowledge" you'd tell a new hire
   - Add helpful/harmful counters as users give feedback
3. **Log every step** to JSON files (foundation for SE-Agent later)
4. **Add self-evolution**:
   - GenericAgent: after 3 successful runs, crystallize the path
   - Or write a simple "skill reuse" check before each LLM planning call
5. **Hindsight** (if you need time-anchored recall): "what did we decide about X?"

### Success criteria
- 2nd run uses cached Skill (LLM plan skipped)
- Playbook has 20+ bullets
- User prefs remembered across sessions
- 70%+ of decisions made from cached knowledge

## Day 61-90: Collaboration + Evolution

### Goal
Multi-agent workflows + trajectory evolution.

### Actions
1. **CrewAI** for the standard team
   - 5 specialists (DOK Resolver, Downloader, Converter, Builder, Merger)
   - Shared memory via Mem0
   - Hierarchical process (manager delegates)
2. **LangGraph** for the PA job state machine
   - DAG: BFS -> DOK resolve -> check_out -> SE convert -> merge -> email
   - PostgreSQL checkpoint (survive crashes)
   - Time-travel debugging
3. **SE-Agent** on accumulated trace logs
   - Pool: last 90 days of PA job JSON traces
   - Operations: revise, reorganize, refine
   - Output: optimal CheckOut order, better SE settings per DOK type
4. **EvoAgentX** for prompt/DAG optimization
   - Apply to CrewAI agent prompts
   - AFlow mode for the PA job DAG

### Success criteria
- 3+ workflows running in production
- Trajectory evolution improves success rate by 10%+
- 80%+ of decisions are auto (no human approval needed)

## Beyond Day 90

### Months 4-6
- **Hindsight** for enterprise-wide decision queries
- **MetaGPT** for generating new PRO.FILE automation scripts from specs
- **AutoAgent** for letting non-engineers (PA team) create their own agents

### Months 6-12
- **Self-evolution at scale**: agents that improve without human review
- **Cross-workflow learning**: skills transfer between PRO.FILE projects
- **MCP ecosystem**: Windows-MCP for Claude Desktop, custom MCPs for PRO.FILE

## Anti-patterns to avoid

1. **Don't adopt all 14 projects at once** — start with 1, master, expand
2. **Don't replace working scripts with agents** — agents add value when the
   workflow is variable; for static scripts, just use the script
3. **Don't skip the execution layer** — UFO² + DmsBatchClient must be solid
   before adding intelligence on top
4. **Don't trust LLM in the hot path** — every LLM call should be
   replaceable with a Skill after the 3rd successful execution
5. **Don't let agents mutate production data without review** — read-only
   first, then supervised write, then unsupervised write

## Success metrics (KPIs)

| Metric | Day 30 | Day 60 | Day 90 |
|---|---|---|---|
| Workflows automated | 1 | 3 | 5+ |
| Manual interventions/run | 0 | 0-1 | 0 |
| Time per run (vs manual) | 50% | 70% | 80%+ |
| Error rate | <5% | <2% | <1% |
| Skills cached | 0 | 10+ | 30+ |
| Playbook bullets | 0 | 20+ | 50+ |
| User satisfaction | 6/10 | 8/10 | 9/10 |
