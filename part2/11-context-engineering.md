# 11. Context Engineering — The Real Discipline

```
  ┌─────────────────────────────────────────────────────┐
  │              CONTEXT WINDOW (e.g. 200K tokens)       │
  │                                                      │
  │  ┌─────────────────────────────────────────────┐    │
  │  │  System Prompt (persona, rules, format)      │    │
  │  ├─────────────────────────────────────────────┤    │
  │  │  Few-shot examples                           │    │
  │  ├─────────────────────────────────────────────┤    │
  │  │  RAG results (relevant documents)            │    │
  │  ├─────────────────────────────────────────────┤    │
  │  │  Images / file attachments                   │    │
  │  │  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │    │
  │  ├─────────────────────────────────────────────┤    │
  │  │  Tool definitions (available tools)          │    │
  │  ├─────────────────────────────────────────────┤    │
  │  │  Conversation history (trimmed/filtered)     │    │
  │  ├─────────────────────────────────────────────┤    │
  │  │  Tool results from previous steps            │    │
  │  ├─────────────────────────────────────────────┤    │
  │  │  Current user message                        │    │
  │  └─────────────────────────────────────────────┘    │
  │                                                      │
  │  ▒▒▒▒▒▒▒▒▒▒▒▒ free space for output ▒▒▒▒▒▒▒▒▒▒▒▒  │
  └─────────────────────────────────────────────────────┘
```

Everything we've covered — system prompt, RAG results, images, tool definitions, conversation history, thinking tokens — competes for the **same limited space** in the context window. The LLM sees *exclusively* what's in this window. Nothing else exists for the model.

The **harness** is everything *except* the LLM itself: the entire application code that surrounds and enables the model. Conversation management, RAG pipelines, tool execution, routing, the agentic loop — all harness. The LLM is the engine. The harness is the car.

**Context Engineering** is the discipline of building this harness so that the context window is optimally filled on every call:

- **What goes in:** Which information does the model need to solve the current task well?
- **What stays out:** Which old messages, irrelevant RAG results, or verbose tool outputs waste space?
- **In what order:** Position matters more than you'd expect. Models weight information at the beginning and end of the context more strongly than the middle ("Lost in the Middle" effect). The reason is structural: each token can only "look back" at tokens before it, never forward. Early tokens in a long prompt are processed without any awareness of what comes later. A 2025 Google Research paper demonstrated this dramatically: simply *repeating the entire prompt twice* — verbatim, no changes — improved accuracy by up to 76% on some tasks. Why? The second copy lets every token "see" the full prompt from the first copy, compensating for the blind spot. (Notably, thinking models showed no benefit — their reasoning step already compensates.)
- **In what format:** The same knowledge, structured differently, can produce dramatically different results.

**Concrete trade-offs:**
- More RAG context = better informed, but less room for conversation
- More tool definitions = more versatile, but the model gets less decisive about which to pick
- Longer conversation history = more continuity, but higher cost and eventually quality degrades. That 50-message conversation? It's consuming context that could hold instructions or reference material
- Attaching images = richer understanding, but a single high-res image can consume thousands of tokens
- For agents: every loop step fills the context with tool results — after 20 steps the context can be full. This is why agents sometimes "lose track" mid-task or repeat themselves — earlier instructions or observations have been pushed out by newer tool results. Agent-builders spend enormous effort on managing this: truncating tool outputs, summarizing intermediate steps, deciding what the model really needs to see

What's commonly called "Prompt Engineering" — techniques like few-shot examples (§3), chain-of-thought reasoning (§10), role prompting, or careful phrasing — is real and useful. But these are all instances of the same thing: managing what goes into the context window. The prompt you type is perhaps 5% of what determines output quality in a production system. The rest is system prompts, RAG results, tool definitions, conversation history, and thinking tokens. That's why the more accurate term is Context Engineering: it's not just about the prompt — it's about orchestrating the entire context.
