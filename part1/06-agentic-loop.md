# 6. The Agentic Loop — Autonomous Action

```
  User: "Find an Italian restaurant near my office
         with outdoor seating, open tonight.
         Reserve a table for 2 at 7."
                       │
                       ▼
    ┌────────────────────────────────────┐
    │                                    │
    │    ┌─────────┐         ┌────────┐ │
    │    │         │  tool   │        │ │
    │    │   LLM   │  call   │  App   │ │
    │    │         │────────▶│ (runs  │ │
    │    │         │         │  tool) │ │
    │    │         │◀────────│        │ │
    │    └─────────┘  result └────────┘ │
    │                                    │
    │    Repeats until done              │
    │    (or guardrail: max steps,       │
    │     timeout, budget)               │
    └────────────────────────────────────┘
                       │
                       ▼
         "Reserved! Trattoria Bella, 7pm,
          table for 2, outdoor terrace."
```

```
Behind the scenes — the conversation grows with each loop:

Step 1:  [..., user: "Find an Italian restaurant near my office..."]
             → tool_call: lookup_address("my office")

Step 2:  [..., tool: { address: "Bahnhofstrasse 42, Zurich" }]
             → tool_call: search_restaurants(near="Bahnhofstrasse 42",
                            cuisine="Italian", outdoor=true)

Step 3:  [..., tool: { results: ["Trattoria Bella", "Casa Napoli", ...] }]
             → tool_call: check_availability("Trattoria Bella",
                            tonight, 19:00, party=2)

  ... continues until reservation is confirmed.
```

In Section 5, the model made a single tool call and turned the result into an answer. That was one round.

An agent runs the same cycle repeatedly. It calls a tool, reads the result, decides what to do next, calls another tool, and keeps going until the task is done. In the example above, the model first looks up your office address, then searches for nearby Italian restaurants, then checks which ones have outdoor seating tonight, then checks availability at 7pm, and finally makes the reservation — five tool calls, each one informed by the previous result.

Mechanically, that's all there is to it. The LLM proposes a tool call. The application executes it and feeds the result back into the conversation — the same mechanism as the chat history from §2. The LLM sees the updated conversation, decides whether the task is done or another step is needed, and if so, makes the next call.

The application sets guardrails to keep the loop in check: a maximum number of steps, a timeout, a cost budget, and often a requirement for human approval before high-impact actions like sending messages or spending money. Without guardrails, a confused agent could loop indefinitely or run up real costs.

This loop — an LLM that autonomously decides what to do, acts, checks the result, and repeats — is what the industry calls an **agent**. The word gets used loosely, but the core idea is always this: an LLM in a loop with tools, deciding its own next step.

## Agents in Practice

An agent's capabilities depend entirely on which tools it has. The loop is always the same; the tools determine what is possible.

Tools vary enormously in *generality*. A `get_weather()` tool does one thing. A `web_search()` tool does many things. A `run_shell_command()` tool — a command line that can run any program on the computer — does almost anything: read and write files, run code, install software, call APIs, query databases. This is why shell access is sometimes called the "god tool": it doesn't give the agent one new capability, it gives the agent an open-ended surface to act on the world. The further right on this spectrum, the more powerful the agent — and the more important the guardrails from above become.

Concrete escalation: ask an agent to "prepare a competitive analysis." With only web search, it can research and summarize. Add shell access, and it can write and run code to scrape data, produce charts, and compile a formatted report. Add integrations — email, calendar, cloud storage — and it can send the finished report to your team and schedule a follow-up meeting. Same loop, same model, radically different outcomes.

Products like Claude Code, Cursor, or Claude's computer use feature are, at their core, an agentic loop with shell access. Dedicated tool integrations (Google Calendar, Gmail, Slack, CRM) are convenience on top: you *could* do everything via shell, but a dedicated `list_events()` call is more reliable and the model doesn't need to handle authentication tokens.

Some agents also maintain memory across sessions — not because the LLM remembers, but because the application stores notes and loads them into context next time (the same illusion from §2, at a larger scale).

When someone says "we're deploying an agent," the first question to ask is: *what tools does it have?* That tells you more about what it can do — and what can go wrong — than any other detail.
