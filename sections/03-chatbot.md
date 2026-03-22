# 3. The Chatbot — Statefulness as Illusion

The LLM from Section 1 has no memory — each call starts from zero. A chatbot creates the illusion of a continuous conversation by resending everything that was said before.

```
  Round 1:                           Round 2:
  ┌──────────────────┐              ┌──────────────────────────────────┐
  │ User: "I'm Max"  │              │ User: "I'm Max"                  │
  └────────┬─────────┘              │ Assistant: "Hello Max!"          │
           │                        │ User: "What's my name?"          │
           ▼                        └────────────────┬─────────────────┘
    ┌─────────────┐                                 │
    │     LLM     │                                ▼
    └─────────────┘                         ┌─────────────┐
           │                                │     LLM     │
           ▼                                └─────────────┘
    "Hello Max!"                                   │
                                                   ▼
                                            "Your name is Max."
```

Look at Round 2 in the diagram above: the application doesn't just send the new question — it resends the entire conversation so far. The model sees "I'm Max," its own reply, and only then the follow-up question. This bundled history is the reason it can answer correctly.

Remove that history, and the same question fails:

```
  Round 1:                           Round 2 (no history):
  ┌──────────────────┐              ┌──────────────────────────┐
  │ User: "I'm Max"  │              │ User: "What's my name?"  │
  └────────┬─────────┘              └────────────┬─────────────┘
           │                                     │
           ▼                                     ▼
    ┌─────────────┐                       ┌─────────────┐
    │     LLM     │                       │     LLM     │
    └─────────────┘                       └─────────────┘
           │                                     │
           ▼                                     ▼
    "Hello Max!"                    "I don't know your name."
```

**The LLM itself has no memory.** Every round, the entire conversation history is sent again as input. The chatbot is an application *around* the LLM that manages this history and includes it with every call.

This explains why long conversations eventually break off (context window full), why the model "forgets" what was said 100 messages ago, and why each message in a long chat costs more — or hits rate limits sooner — because of the growing token count. Some products manage this by summarizing older messages to free up space — trading accurate recall of early messages for more room to work with.

What products like ChatGPT call "memory" is built on the same principle — with an added step: key facts from past conversations are extracted, stored separately, and injected into the context on each new call.

**Message format** — Behind the scenes, every conversation is structured using labeled roles — think of it as a script with named speakers:

```
messages: [
  { role: "system",    content: "You are a helpful assistant." },
  { role: "user",      content: "I'm Max" },
  { role: "assistant", content: "Hello Max!" },
  { role: "user",      content: "What's my name?" }
]
```

The "system" message sets behavior (more on that next). The "user" and "assistant" messages are the conversation turns. The roles serve a practical purpose: they let the model distinguish instructions to follow (system) from input to respond to (user) from its own prior responses to stay consistent with (assistant). This format is what every chatbot, API wrapper, and agent framework uses under the hood.

These role labels are conventions the model learned during training — strong signals, but not hard rules. A sufficiently clever message in the "user" slot can override instructions from the "system" slot — a vulnerability called **prompt injection** (→ What We Didn't Cover).
