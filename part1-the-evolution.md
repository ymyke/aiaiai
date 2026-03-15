# Part I: The Evolution

> From a simple text box to autonomous agents — each step builds on the last.

---

## 1. The Plain LLM — The Foundation

```
        "The capital of France is"
                       │
                       ▼
              ┌───────────────┐
              │      LLM      │
              └───────────────┘
                       │
                       ▼
                    "Paris."
```

A Large Language Model is, at its core, a text continuation engine: given some text, it produces the most likely next piece of text, token by token. No memory, no knowledge updates after training, no logic in the classical sense — just extraordinarily good pattern recognition over language. It doesn't "answer questions" — it continues text. That it *appears* to answer questions is because a question followed by a good answer is the most likely continuation.

**Important:** A single LLM call is *stateless*. It knows nothing about previous calls. This has consequences for everything that follows.

**Key concepts:**

- **Parameters (weights)** — The model's learned knowledge, encoded as numbers (think of them as the model's "synapses"). Current models have parameters in the billions to trillions. More parameters ≈ more knowledge capacity, but with diminishing returns.
- **Context Window** — How much text the model can "see" at once. Measured in tokens. Current models range from ~100K to over a million tokens. Everything outside the window — prior messages, documents not included — is invisible to the model for that call.
- **Temperature** — The creativity dial. 0 = deterministic (always the most likely answer). 1 = creative/random. Low for code, higher for brainstorming.
- **Training vs. Inference** — Training: the model learns from data (months, millions of $). Inference: the model answers a question (milliseconds, cents).


*→ See [Under the Hood: The API Call](uth.md#the-api-call) for what an LLM call actually looks like in code.*

### Tokens — The Machine's Language

```
  "Climate technology matters"
                │
                ▼
        ┌── Tokenizer ──┐
        │                │
        ▼                ▼
  ["Climate", " tech",  ["8241", "1092",
   "nology", " matters"] "5523", " 7841"]
   (Tokens)              (Token IDs)
```

Before the LLM processes anything, text is split into **tokens** — word fragments with numeric IDs. The model never sees raw text — it sees only these fragments. This seems like a technical detail, but it has big consequences.

**Why tokens explain so much "weird" LLM behavior:** Ask a model "How many r's in strawberry?" and it often gets it wrong. Not because it can't count, but because "strawberry" is one or two tokens — the model never sees individual letters. It's like reading a word printed across puzzle pieces: you see each piece, but you can't easily count letters that are glued inside them. The same goes for reversing a string or simple spelling tasks: the model literally can't see what you think it sees.

Arithmetic is similar. A number like "184723" might be split into ["184", "723"]. The model doesn't see a number — it sees two unrelated text fragments. That's why LLMs can reason about math conceptually but fumble basic calculations.

Tokens also explain why many LLMs work better in English than in other languages. Tokenizers are trained mostly on English text, so English gets efficient, large tokens. German or Japanese text gets split into more, smaller pieces — meaning the same content uses more tokens, fills the context window faster, costs more, and generally gets worse results.

Rule of thumb: 1 token ≈ 4 characters of English, ≈ 3 characters of German.

---

## 2. The Chatbot — Statefulness as Illusion

```
  Round 1:                           Round 2:
  ┌──────────────────┐              ┌──────────────────────────────┐
  │ User: "I'm Max"  │              │ User: "I'm Max"              │
  └────────┬─────────┘              │ Asst: "Hello Max!"           │
           │                        │ User: "What's my name?"      │
           ▼                        └──────────────┬───────────────┘
    ┌─────────────┐                                │
    │     LLM     │                                ▼
    └─────────────┘                         ┌─────────────┐
           │                                │     LLM     │
           ▼                                └─────────────┘
    "Hello Max!"                                   │
                                                   ▼
                                            "Your name is Max."
```

Without conversation history, the same question fails:

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

**The key insight:** The LLM itself has no memory. Every round, the *entire conversation history* is sent again as input. The chatbot is an application *around* the LLM that manages conversation history and includes it with every call.

This explains why long conversations eventually break off (context window full), why the model "forgets" what was said 100 messages ago, and why each message in a long chat costs more — or hits rate limits sooner — because of the growing token count. Some products manage this by summarizing older messages to free up space — trading accurate recall of early messages for more room to work with.

What products like ChatGPT call "memory" is exactly this trick — or a variant where key facts are stored separately and injected into the context on each call (a lightweight form of RAG, covered in Part II).

**Message format** — Most LLM APIs use a role system. Think of it as a script with labeled speakers:

```
messages: [
  { role: "system",    content: "You are a helpful assistant." },
  { role: "user",      content: "I'm Max" },
  { role: "assistant", content: "Hello Max!" },
  { role: "user",      content: "What's my name?" }
]
```

The "system" message sets behavior (more on that next). The "user" and "assistant" messages are the conversation turns. The roles serve a practical purpose: they let the model distinguish instructions to follow (system) from input to respond to (user) from its own prior responses to stay consistent with (assistant). This format is what every chatbot, API wrapper, and agent framework uses under the hood — including the tools we use daily.

**Important:** These role labels are a convention the model learned during training — not a built-in rule it must obey. The model treats them as strong signals, but they are not a security boundary. This distinction matters when we discuss prompt injection in Part III.

---

## 3. The System Prompt — Programming Behavior

```
  ┌─────────────────────────────────────────┐
  │  System Prompt (invisible to user)       │
  │  "You are a climate tech analyst.        │
  │   Be precise. Respond in bullet points." │
  ├─────────────────────────────────────────┤
  │  User: "Evaluate this startup"           │
  │  ...                                     │
  └──────────────────┬──────────────────────┘
                     │
                     ▼
              ┌─────────────┐
              │     LLM     │
              └─────────────┘
```

The system prompt is a special message at the start of every conversation that steers the model's behavior. It's powerful, but not a command — more of a strong suggestion.

This is where most practical "prompt engineering" happens: defining persona and tone, specifying output format, providing knowledge and context, setting rules and constraints, giving examples (few-shot prompting). As we'll see in §11, prompt engineering is actually one part of a bigger discipline — **Context Engineering** — that covers everything the model sees, not just the text you write.

**Important:** The system prompt consumes tokens on *every message*, because it's resent every time.

---

## 4. Structured Output — Machine Talks to Machine

```
  Prompt: "Extract name and sector"         + Schema
                     │                          │
                     ▼                          ▼
              ┌─────────────────────────────────────────┐
              │  LLM (with JSON mode / schema constraint) │
              └─────────────────────────────────────────┘
                                  │
                                  ▼
                          {
                            "name": "Lichtwart",
                            "sector": "Building Automation",
                            "stage": "Pre-Seed"
                          }
```

Before an LLM can use tools, it needs to answer in a structured way. **Structured Output** forces the model to respond in a defined format (JSON, XML) instead of free text.

**Why this matters:**
- Software can parse JSON but can't reliably interpret free text
- It's the bridge between "LLM as conversation partner" and "LLM as software component"
- It's the foundation for tool use — the model needs to specify *which* tool with *which* parameters in a format the application can act on

---

## 5. Tool Use — Hands for the LLM

```
  ┌─────────────────────────────────────────────────┐
  │  System Prompt + Tool Definitions:               │
  │  (tool definitions are just text in the context) │
  │                                                  │
  │  Available tools:                                │
  │  - get_weather(city) → weather data              │
  │  - search_crm(name) → deal info                  │
  ├─────────────────────────────────────────────────┤
  │  User: "What's the weather in Zurich?"           │
  └──────────────────────┬──────────────────────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │     LLM     │
                  └─────────────┘
                         │
    Instead of answering directly, the LLM outputs:
    "Call get_weather with city = Zurich"
                         │
                         ▼
              ┌─────────────────┐
              │  Application    │──── actual API call
              │  executes tool  │
              └────────┬────────┘
                       │
                       ▼
    Result: { temp: "12°C", condition: "cloudy" }
                       │
                       ▼
                ┌─────────────┐
                │     LLM     │  (receives result as a new message)
                └─────────────┘
                       │
                       ▼
   "It's currently 12°C and cloudy in Zurich."
```

**The crucial insight:** The LLM doesn't execute tools itself. It only decides *which* tool to call with *which* parameters. The application performs the actual call and feeds the result back. And the tool definitions? They're just text in the context window — typically part of the system prompt. The model has learned to recognize this format and generate matching structured calls.

**Typical tools:** Web search, database queries, API calls, code execution, file operations, CRM access.

**Why code execution changes everything:** Remember the strawberry problem from §1? The model can't count letters in "strawberry" because it never sees individual letters — only token fragments. But give the model a code execution tool, and it writes `'strawberry'.count('r')` — correct, every time. The model didn't get smarter. It got a calculator. The same applies to arithmetic, date calculations, sorting, and anything else where precise computation beats pattern matching. This is why the *same model* gives better answers in a product that has code execution than in one that doesn't.

Tool integrations are becoming standardized: **MCP (Model Context Protocol)**, an open standard from Anthropic, defines a universal protocol for connecting tools to LLMs. Think of it as USB for AI tools — instead of building custom integrations for each model, you define the tool once.

---

## 6. The Agentic Loop — Autonomous Action

```
  User: "Research the last 3 deals in the building sector
         and create a comparison table."
                          │
                          ▼
  ┌──────────────────────────────────────────────────┐
  │                  AGENTIC LOOP                     │
  │                                                   │
  │   ┌─────────────────────────┐    ┌───────────┐  │
  │   │          LLM            │    │Application │  │
  │   │                         │    │            │  │
  │   │   Think ──▶ Decide ─────────▶│  Act       │  │
  │   │                         │    │  (execute  │  │
  │   │    ▲                    │    │   tool)    │  │
  │   └────│────────────────────┘    └─────┬─────┘  │
  │        │                               │         │
  │        │         ┌──────────┐          │         │
  │        └─────────│ Observe  │◄─────────┘         │
  │                  │ (result  │                     │
  │                  │  becomes │                     │
  │                  │  new     │                     │
  │                  │  context)│                     │
  │                  └──────────┘                     │
  │                                                   │
  │   Loop repeats until the task is done             │
  └──────────────────────────────────────────────────┘
                          │
                          ▼
              Finished comparison table
```

The leap from tool use to **agent**: instead of calling one tool once, the LLM autonomously plans a sequence of steps and iterates until the task is complete.

**Think → Decide → Act → Observe → Repeat**

The model analyzes the task, breaks it into steps, picks the right tool, observes the result, and decides whether to continue or stop. On errors, it can try alternative strategies. The application typically sets guardrails: max iterations, timeouts, budgets.

**The key word is autonomy:** The agent decides *how many* steps are needed and *which* tools to use in what order.

### Agents in Practice

Products like Claude Code, Cursor, or Claude's computer use feature are, at their core:

**Agentic loop + shell access (the "god tool") + tool integrations**

A shell can do anything a computer can — read/write files, start processes, call APIs, query databases. Dedicated tool integrations (Google Calendar, Gmail, Slack, CRM) are convenience: you *could* do everything via shell + curl + APIs, but a dedicated `list_events()` call is more reliable and the model doesn't need to handle OAuth tokens.

---

## 7. Multi-Agent — Division of Labor

```
  User: "Analyze this deal end to end"
                     │
                     ▼
         ┌───────────────────────┐
         │   Orchestrator Agent  │
         │   (plans & delegates) │
         └───┬─────┬─────┬──────┘
             │     │     │
             ▼     ▼     ▼
         ┌─────┐┌─────┐┌──────┐
         │Mkt. ││Team ││Fin.  │    ◄── Subagents
         │Anal.││Anal.││Anal. │        (each with own loop,
         └──┬──┘└──┬──┘└──┬───┘         own context, own tools)
            │      │      │
            ▼      ▼      ▼
         ┌───────────────────────┐
         │   Orchestrator Agent  │
         │   (synthesizes)       │
         └───────────────────────┘
                     │
                     ▼
            Complete deal report
```

When a task is too big or too multifaceted for a single agent, you split it across **subagents**. The orchestrator delegates subtasks, each subagent runs its own agentic loop, and returns its result — just like any other tool call.

**Why subagents?**
- **Context separation** — Each subagent has its own context window. The market analyst doesn't need to see the financial model.
- **Specialization** — Each subagent can have its own system prompt, tools, and instructions.
- **Parallelization** — Multiple subagents can work simultaneously.
- **Fault isolation** — If the financial analyst crashes, the other results aren't lost.
