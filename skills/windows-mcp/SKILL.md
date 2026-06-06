---
name: windows-mcp
description: MCP-standard Windows automation via UIAutomation. 15+ tools, LLM-agnostic. Use when Claude Desktop / Mavis needs Windows control via MCP.
---

# Windows-MCP

## When to use
- MCP client needs to control Windows
- Don't want custom UIA wrapper
- LLM-agnostic (any tool-calling model)

## Core technique
Lightweight MCP server exposing 15+ tools: click, type, screenshot,
window_list, find_element. Uses UIAutomation tree (not Win32 raw hooks).

## Minimal code
```json
// claude_desktop_config.json
{"mcpServers": {"windows": {"command": "uvx", "args": ["windows-mcp"]}}}
```
Then in chat: "click Start, type 'notepad', press Enter"

## PRO.FILE angle
- Drop-in MCP for Mavis: any agent can control PRO.FILE UI
- Works alongside DmsBatchClient (MCP for UI, DmsBatch for headless)
- 2M+ Claude Desktop users = battle-tested

## Pitfalls
- UIA tree slow for very complex apps (Solid Edge 3D viewport)
- Element locators can break across PRO.FILE versions
- No headless mode

Repo: https://github.com/CursorTouch/Windows-MCP
