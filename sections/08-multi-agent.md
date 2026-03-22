# 8. Multi-Agent — Division of Labor

```
  User: "Plan a birthday party for 30 people:
         find a venue, plan the menu, create invitations."
                     │
                     ▼
         ┌───────────────────────┐
         │   Orchestrator Agent  │
         │   (plans & delegates) │
         └───┬─────┬─────┬───────┘
             │     │     │
             ▼     ▼     ▼
         ┌─────┐┌─────┐┌──────┐
         │Venue││Menu ││Invi- │    ◄── Subagents
         │find ││plan ││tation│        (each with own loop,
         └──┬──┘└──┬──┘└──┬───┘         own context, own tools)
            │      │      │
            ▼      ▼      ▼
         ┌───────────────────────┐
         │   Orchestrator Agent  │
         │   (synthesizes)       │
         └───────────────────────┘
                     │
                     ▼
            Complete party plan
```

You've seen that every LLM call has a limited context window, and that irrelevant context can hurt quality. So what happens when a task has parts that don't need to see each other?

The system splits it. The orchestrator agent delegates each subtask to a **subagent** — a separate agent with its own context window, its own tools, and its own agentic loop. The menu planner never sees the venue research. Each subagent returns its result, and the orchestrator combines them into a final answer.

**What this means for you:**
- **Better results on complex tasks** — each subtask gets the model's full, focused attention instead of competing for space in one crowded context window.
- **Faster results** — independent subtasks can run simultaneously.
- **One caveat** — because subtasks run independently, the pieces may not reference each other. The venue section of your party plan won't mention the menu, unless the orchestrator explicitly connects them.

- **Another caveat** — the orchestrator only sees each subagent's final summary, not all the work and dead ends along the way. If a subagent goes down the wrong path, the orchestrator may never know. This is why multi-agent results benefit from a human spot-check — skim the pieces for obvious mismatches before trusting the whole.

**The practical takeaway:** When you give an AI a complex task, structure it as clear, separable subtasks. "Find a venue, plan the menu, and create invitations" works better than "plan a party" — not just because clarity always helps, but because the system can hand each piece to a focused subagent with its own full context window.
