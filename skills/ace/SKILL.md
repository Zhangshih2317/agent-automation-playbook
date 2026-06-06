---
name: ace-self-reflect
description: Generator-Reflector-Curator 3-agent loop that incrementally improves a structured text Playbook. +10.6% on agent benchmarks, +17.1% AppWorld. Use when you need explainable, self-improving domain knowledge.
---

# ACE — Agentic Context Engineering (verified source)

> Source: ace-agent/ace. Single `ace.py` (1142 lines, the orchestrator) +
> `ace/core/` (Generator, Reflector, Curator, BulletpointAnalyzer).
> This is **production research code** — what the actual arxiv:2510.04618
> paper describes.

## When to use
- Agent must improve over time WITHOUT retraining
- You want **explainable** improvements (every change is a tagged bullet)
- You can afford 3 LLM calls per training iteration (Generator + Reflector + Curator)
- Domain is well-defined (PRO.FILE ops, financial analysis, legal research)

## Core technique (verified from `ace.py`)

**A. Three LLM clients, possibly three different models.**
```python
def __init__(self, api_provider, generator_model, reflector_model, curator_model, ...):
    generator_client, reflector_client, curator_client = initialize_clients(api_provider)
    self.generator = Generator(generator_client, ..., generator_model)
    self.reflector = Reflector(reflector_client, ..., reflector_model)
    self.curator  = Curator(curator_client, ..., curator_model)
```

**Why 3 models?**
- Generator: the workhorse (cheap/fast model OK)
- Reflector: needs nuance (use stronger model for critique)
- Curator: needs careful editing (use strong model to avoid breaking bullets)

**B. Playbook is a STRING, not a dict.**
The Playbook is a markdown-formatted text with sections:
```
## STRATEGIES & INSIGHTS
- [helpful=23, harmful=0] <text> <global_id=1>
- [helpful=15, harmful=2] <text> <global_id=2>

## FORMULAS & CALCULATIONS
- ...

## CODE PATTERNS
- ...
```

Each bullet has a **counter pair** (`helpful=N, harmful=M`) and a **global ID**
that persists across iterations. Sections are stable; bullets are added/removed.

**C. BulletpointAnalyzer for dedup.**
Optional component. When adding a new bullet, embeds it and compares to
existing bullets. If similarity > 0.90 (threshold), merges instead of
adding a duplicate. Prevents playbook bloat.

**D. Incremental updates, not full rewrites.**
- Reflector tags existing bullets (helpful/harmful counts) AND proposes
  new bullets separately
- Curator operates on the delta, not the whole playbook
- This avoids "brevity bias" and "context collapse" (the paper's
  contribution over ReAct/Reflexion)

**E. `best_playbook` tracked separately from current.**
The training loop tries new bullets, evaluates, and rolls back if the
candidate playbook is worse. The `best_playbook` is the best seen so far.

## Minimal code pattern (rebuilt from real architecture)

```python
class Playbook:
    """A markdown playbook with tagged bullets per section."""
    SECTIONS = ["STRATEGIES & INSIGHTS", "FORMULAS & CALCULATIONS",
                "CODE PATTERNS", "COMMON MISTAKES"]
    def __init__(self, content=""):
        self.content = content or self._empty_template()
        self.next_id = self._count_existing_ids() + 1
    def _empty_template(self):
        return "\n".join(f"## {s}\n" for s in self.SECTIONS) + "\n"
    def add_bullet(self, section, text):
        bullet = f"- [helpful=0, harmful=0] {text} <global_id={self.next_id}>"
        self.content = self.content.replace(f"## {section}", f"## {section}\n{bullet}")
        self.next_id += 1
    def update_score(self, section, gid, helpful=True):
        # regex update the counter
        if helpful:  self._incr(f"global_id={gid}", "helpful")
        else:        self._incr(f"global_id={gid}", "harmful")
    def best_bullets(self, k=10):
        # parse and sort by score
        return sorted(self._parse_bullets(), key=lambda b: b["helpful"]-b["harmful"])[:k]

class ACE:
    def __init__(self, gen_client, ref_client, cur_client, playbook=None):
        self.playbook = playbook or Playbook()
    def train_step(self, task, ground_truth=None):
        # 1. Generator uses current playbook to answer
        answer = self.generator.run(task, context=self.playbook.content)
        # 2. Reflector critiques
        critique = self.reflector.run(task, answer, ground_truth)
        # 3. Reflector tags existing bullets + proposes new ones
        new_bullets, tag_updates = self.reflector.extract_changes(critique)
        # 4. Curator applies the delta
        for upd in tag_updates:
            self.playbook.update_score(**upd)
        for b in new_bullets:
            if self.bulletpoint_analyzer.is_duplicate(b):
                self.bulletpoint_analyzer.merge(b, existing)
            else:
                self.playbook.add_bullet(b["section"], b["text"])
        return answer
```

## PRO.FILE angle (concrete)

For MUBEA's PRO.FILE automation:

1. **Initial Playbook** = the tribal knowledge ("Always use 32-bit PS for
   DmsBatchClient", "Never CheckOut to C:\", "SE COM needs Visible=False
   before SaveAs")

2. **Each PA job = a training step**:
   - Generator: tries to do the PA job
   - Reflector: compares actual vs expected output
   - Curator: adds new bullets for "this works", marks harmful for "this fails"

3. **After 20-30 PA jobs, the Playbook is the source of truth**:
   - Generator prompt = best N bullets
   - LLM plan time drops dramatically (crystallized knowledge)
   - User onboarding: "read the Playbook before doing PRO.FILE work"

4. **BulletpointAnalyzer** = use `sentence-transformers` (or even just
   `difflib.SequenceMatcher` for small playbooks) to dedup

## Pitfalls (from real source)

- **Don't skip the Reflector step** even if you're tempted — Reflector
  is what makes ACE work, not the Curator
- **3 separate models are recommended** but not required. Single model
  for all 3 works but is less robust
- **Playbook can grow unbounded** — periodically run Curator with
  "remove bullets where harmful > helpful AND total < 5"
- **Tag updates happen on `helpful`/`harmful` events** — collect these
  from real usage, don't just generate them
- **`initial_playbook` parameter** is critical — start with at least
  5-10 high-quality bullets, not empty
- **BulletpointAnalyzer threshold 0.90** is the default — too low = over-merging,
  too high = duplicates
- **Playbook is in the LLM context** — keep it under ~6KB or token costs
  spike
- **Reflector can hallucinate** bullet IDs that don't exist — Curator
  must validate before applying

## Repo
https://github.com/ace-agent/ace (~630 stars, MIT, Stanford/SambaNova paper)
