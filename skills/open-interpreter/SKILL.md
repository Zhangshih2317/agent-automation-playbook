---
name: open-interpreter-code
description: Natural language to local code execution (Python/JS/Shell). No sandbox by default. Use when you need an agent to actually run code on the user's machine.
---

# Open Interpreter

## When to use
- User wants to "do this thing" not "explain how"
- Need to run real code locally (no sandbox)
- Multi-language (Python + JS + Shell)

## Core technique
LLM generates code in any language; interpreter runs it locally
and shows output. No sandbox by default (security risk).
MCP support for tool extensibility.

## Minimal code
```python
import interpreter
interpreter.auto_run = True
interpreter.chat("Download my PRO.FILE BOM 91020879 to CSV and email it")
```

## PRO.FILE angle
- Replace "user describes PA job -> agent does it" loop
- Local execution = full DmsBatchClient + SE COM access
- But NO sandbox = any prompt injection = full local code execution

## Pitfalls
- No sandbox = DANGEROUS for untrusted prompts
- Multi-language = harder to debug than pure-Python agents
- Recent version split (O1 vs OI); check which to use

Repo: https://github.com/OpenInterpreter/open-interpreter
