---
name: autogen-microsoft
description: Microsoft multi-agent orchestration with event-driven conversations. LLM + human + tools. 50K stars, Azure-native. Use for complex multi-party negotiations.
---

# AutoGen (Microsoft)

## When to use
- Complex multi-party conversations
- Need human-in-loop with structured handoffs
- Microsoft / Azure ecosystem

## Core technique
Event-driven orchestration. Agents are async functions sending
messages to GroupChat; a manager routes next speaker.
3 topologies: two-agent, group chat, hierarchical.

## Minimal code
```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
a1 = AssistantAgent("Planner", llm_config=cfg)
a2 = AssistantAgent("Coder", llm_config=cfg)
user = UserProxyAgent("User", code_execution_config={"work_dir": "_out"})
chat = GroupChat(agents=[user, a1, a2], messages=[], max_round=10)
manager = GroupChatManager(chat, llm_config=cfg)
user.initiate_chat(manager, message="Build a Python CLI")
```

## PRO.FILE angle
- Combine with UFO2: AutoGen orchestrates, UFO2 executes on Windows
- Azure AD auth slots in for enterprise SSO
- GroupChat: Planner -> DOK Resolver -> CheckOut -> SE Converter

## Pitfalls
- GroupChat stores every message = history explosion
- Termination conditions tricky (max_round or explicit)

Repo: https://github.com/microsoft/autogen
