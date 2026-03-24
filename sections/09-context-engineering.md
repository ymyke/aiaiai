# 9. Context Engineering — The Real Discipline

```
  ┌─────────────────────────────────────────────────────┐
  │         CONTEXT WINDOW (e.g. 200K tokens)           │
  │                                                     │
  │  ┌─────────────────────────────────────────────┐    │
  │  │  System prompt                              │    │
  │  ├─────────────────────────────────────────────┤    │
  │  │  Tool definitions                           │    │
  │  ├─────────────────────────────────────────────┤    │
  │  │  Examples                                   │    │
  │  ├─────────────────────────────────────────────┤    │
  │  │  Retrieved documents                        │    │
  │  ├─────────────────────────────────────────────┤    │
  │  │  Images / file attachments                  │    │
  │  ├─────────────────────────────────────────────┤    │
  │  │  Conversation history                       │    │
  │  ├─────────────────────────────────────────────┤    │
  │  │  Tool results from previous steps           │    │
  │  ├─────────────────────────────────────────────┤    │
  │  │  Current user message                       │    │
  │  └─────────────────────────────────────────────┘    │
  │                                                     │
  │  ·················································  │
  │  ············· free space for output ·············  │
  │  ·················································  │
  │                                                     │
  └─────────────────────────────────────────────────────┘
```

Everything we've covered — system prompt, retrieved documents, images, tool definitions, conversation history, thinking tokens — competes for the **same limited space** in the context window. The model also has its trained knowledge (the parameters from section 1), but at runtime, the context window is the *only* input you can control. If a fact isn't in the window and wasn't in the training data, it doesn't exist for the model.

All of the machinery we've seen so far — the conversation management from section 3, the tool execution from section 6, the agentic loop from section 7 — is built by developers, not the LLM. This is the application around the model: everything *except* the LLM itself. The LLM is the engine; the application is the rest of the car. Engineers use several overlapping terms for this layer — "application layer," "orchestration layer," "harness," sometimes "the stack." They all describe aspects of the same basic idea: code that surrounds and directs the model. 

**Context engineering** is the discipline of controlling what the model sees on every call — and what it doesn't. Concretely, it means designing across four dimensions:

- **What goes in:** Which information does the model need to solve the current task well?
- **What stays out:** Which old messages, irrelevant RAG results, or verbose tool outputs waste space?
- **In what order:** Position matters. Models pay the most attention to the beginning and end of the context, and less to the middle — a well-documented pattern called the "Lost in the Middle" effect. This is why system prompts go at the very start. For long prompts, placing your most important instructions at the beginning and repeating key points near the end can noticeably improve results.
- **In what format:** The same knowledge, structured differently, can produce dramatically different results.

**Why this matters in practice:**
- More RAG context = better informed, but less room for conversation
- More tool definitions = more versatile, but the model gets less decisive about which to pick
- Longer conversation history = more continuity, but higher cost and eventually quality degrades. That 50-message conversation? It's consuming context that could hold instructions or reference material
- Attaching images = richer understanding, but a single high-res image can consume thousands of tokens
- For agents: every loop step fills the context with tool results — after 20 steps the context can be full. This is why agents sometimes "lose track" mid-task or repeat themselves — earlier instructions or observations have been pushed out by newer tool results. Agent-builders spend enormous effort on managing this: truncating tool outputs, summarizing intermediate steps, deciding what the model really needs to see 

What's commonly called "Prompt Engineering" — techniques like providing examples, chain-of-thought reasoning, or careful phrasing — is real and useful. But for most AI products, the prompt you type is a small fraction of what determines output quality. The rest is system prompts, retrieved documents, tool definitions, conversation history, and thinking tokens — all managed automatically by the application around the model. That's why the more precise term is **context engineering**: it's not just about your prompt, it's about everything the model sees.

