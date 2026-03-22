# 4. The System Prompt — Programming Behavior

In Section 2 we saw that the model receives a list of messages with roles. The system prompt is the first message in that list — written not by you, but by whoever built the product. It steers how the model behaves before you say a word, and it's where tool definitions, guardrails, and safety constraints live.

```
  ┌──────────────────────────────────────────────────────┐
  │  System Prompt (invisible to user)                   │
  │  "You are a travel assistant. Be concise.            │
  │   Recommend based on budget and interests."          │
  ├──────────────────────────────────────────────────────┤
  │  User: "Plan a weekend trip to Berlin"               │
  └──────────────────────────┬───────────────────────────┘
                             │
                             ▼
                      ┌─────────────┐
                      │     LLM     │
                      └─────────────┘
```

A plain LLM is a general-purpose engine. A chatbot gives it memory. The system prompt gives it a *mission* — a role, rules, and tools, all specified in ordinary language by whoever built the product. Structured output, tool use, autonomous loops: each of these capabilities, introduced in the sections ahead, is essentially a new instruction added to this message. The system prompt is where human intent steers model behavior — in plain language, not code.

A typical system prompt defines:
- **Persona and tone** — "You are a concise travel assistant" vs. "You are a friendly tutor who explains step by step"
- **Output format** — respond in bullet points, use markdown, keep answers under 200 words
- **Rules and constraints** — "Never discuss competitors," "Always cite your sources," "Decline medical advice"
- **Context and knowledge** — background information the model should use
- **Examples** — sample exchanges that show the desired behavior
- **Tool definitions** — which tools the model can use, and how to call them (more on this in §6)

The system prompt occupies space in the context window on every call — a long system prompt means less room for your conversation. This is why system prompts in production are kept concise: every word competes with the messages, tool definitions, and other content the model needs to see.
