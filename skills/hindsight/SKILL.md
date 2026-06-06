---
name: hindsight-precise-memory
description: 4-way parallel retrieval (semantic+BM25+graph+temporal) with cross-encoder rerank. 91.4% LongMemEval (highest). Use when recall precision matters more than simplicity.
---

# Hindsight

## When to use
- High-stakes decisions need precise recall (legal, financial, engineering)
- Time-anchored queries ("what did we decide in Q1 2026?")
- Long-context conversations (1M+ tokens)

## Core technique
Four parallel retrievers (semantic, BM25, graph, temporal) feed into a
cross-encoder reranker. Combines dense + sparse + structured signals.
TEMPR (Temporal Entity Memory) tracks when facts were true.

## Minimal code
```python
import hindsight
client = hindsight.Client()
client.store("We adopted Mem0 in Q1 2026", timestamp="2026-01-15")
result = client.retrieve("What memory systems do we use?")
# result.sources: [{text, score, retrieved_at, temporal_validity}]
```

## PRO.FILE angle
- "Show me all DOKs ZhangS changed in the last 30 days" — needs temporal precision
- "Why did we switch from ManualExport to DmsBatch?" — causal + temporal recall
- MCP-first design — slot into Claude Desktop / Mavis directly

## Pitfalls
- 4 retrievers = 4x compute vs Mem0
- Graph store needs Neo4j setup (extra ops)
- Cross-encoder adds 100-300ms latency per query

Repo: https://github.com/vectorize-io/hindsight
