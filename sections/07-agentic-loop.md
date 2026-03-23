# 7. The Agentic Loop — Autonomous Action

```
  User: "Find an Italian restaurant near my office
         with outdoor seating, open tonight.
         Reserve a table for 2 at 7."
                       │
                       ▼
    ┌─────────────────────────────────────────┐
    │                                         │
    │    ┌─────────┐            ┌──────────┐  │
    │    │         │   tool     │          │  │
    │    │   LLM   │   call     │   App    │  │
    │    │         │ ─────────▶ │  (runs   │  │
    │    │         │            │   tool)  │  │
    │    │         │ ◀───────── │          │  │
    │    └─────────┘   result   └──────────┘  │
    │                                         │
    │    Repeats until done                   │
    │    (or guardrail: max steps,            │
    │     timeout, budget)                    │
    └─────────────────────────────────────────┘
                       │
                       ▼
         "Reserved! Trattoria Bella, 7pm,
          table for 2, outdoor terrace."
```

**Behind the scenes — the conversation grows with each loop:**

```
Step 1:  [..., user: "Find an Italian restaurant near my office..."]
             → tool_call: lookup_address("my office")

Step 2:  [..., tool: { address: "Oberdorfstrasse 8, Zurich" }]
             → tool_call: search_restaurants(near="Oberdorfstrasse 8, Zurich",
                            cuisine="Italian", outdoor=true)

Step 3:  [..., tool: { results: ["Trattoria Bella", "Casa Napoli", ...] }]
             → tool_call: check_availability("Trattoria Bella",
                            tonight, 19:00, party=2)

  ... continues until reservation is confirmed.
```

In Section 5, the model made a single tool call and turned the result into an answer. That was one round.

An agent runs the same cycle repeatedly. It calls a tool, reads the result, decides what to do next, calls another tool, and keeps going until the task is done. In the example above, the model first looks up your office address, then searches for nearby Italian restaurants, then checks which ones have outdoor seating tonight, then checks availability at 7pm, and finally makes the reservation — five tool calls, each one informed by the previous result.

Mechanically, that's all there is to it. The LLM proposes a tool call. The application executes it and feeds the result back into the conversation — the same mechanism as the chat history from section 3. The LLM sees the updated conversation, decides whether the task is done or another step is needed, and if so, makes the next call.

The application sets guardrails to keep the loop in check: a maximum number of steps, a timeout, a cost budget, and often a requirement for human approval before high-impact actions like sending messages or spending money. Without guardrails, a confused agent could loop indefinitely or run up real costs.

This loop — an LLM that autonomously decides what to do, acts, checks the result, and repeats — is what the industry calls an **agent**. The word gets used loosely, but the core idea is always this: an LLM in a loop with tools, deciding its own next step.

## Agents in Practice

An agent's capabilities depend entirely on which tools it has. The loop is always the same; the tools determine what is possible.

Tools vary enormously in *generality*. A `get_weather()` tool does one thing. A `web_search()` tool does many things. A `run_shell_command()` tool — a command line that can run any program on the computer — does almost anything: read and write files, run code, install software, call APIs, query databases. This is why shell access is sometimes called the "god tool": it doesn't give the agent one new capability, it gives the agent an open-ended surface to act on the world. The more general the tools, the more powerful the agent — and the more important the guardrails: step limits, timeouts, cost budgets, and human approval before high-impact actions.

A concrete example: ask an agent to "plan a weekend trip to Copenhagen." With only web search, it can research flights, hotels, and top-rated restaurants, and write up a summary. Add code execution, and it can compare prices across dozens of options, calculate travel times between stops, and build a detailed day-by-day itinerary. Add integrations — airline booking, calendar, email — and it can book the flights, reserve the hotel, block the days on your calendar, and send the itinerary to everyone coming along.

Products like ChatGPT, Google's Gemini agents, Claude Code, Cursor, or OpenClaw are, at their core, this same loop — equipped with tools like shell access, web search, or integrations with services like Google Calendar and Slack.

OpenClaw, which went from zero to the most-starred project on GitHub in early 2026, is a clear example: the underlying technology is the same loop you just learned about — what made it take off was which tools it gave the model and where it ran (your own computer, inside your messaging apps). It also illustrates why guardrails matter: OpenClaw gives the model very wide access to the system it runs on by default — files, shell, messaging, browsing — which is what makes it powerful, but also what makes the "what tools does it have?" question so important.

Some agents also maintain memory across sessions — not because the LLM remembers, but because the application stores notes and loads them into context next time (the same illusion from section 3, at a larger scale).

When someone says "we're deploying an agent," the first question to ask is: *what tools does it have?* That tells you more about what it can do — and what can go wrong — than any other single detail.