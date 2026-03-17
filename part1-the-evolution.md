# Part I: The Evolution

> From a text box to autonomous agents — layer by layer.

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

A single LLM call is *stateless* — after each response, the model has complete amnesia. It knows nothing about any previous call. This single fact explains why chatbots resend the entire conversation every time (§2).

**Key concepts:**

- **Parameters (weights)** — The model's learned knowledge, encoded as numbers (think of them as the model's "synapses"). Current models have parameters in the billions to trillions. More parameters ≈ more knowledge capacity, but with diminishing returns.
- **Context Window** — How much text the model can "see" at once. Measured in tokens. Current models range from ~100K to over a million tokens. Everything outside the window — prior messages, documents not included — is invisible to the model for that call.
- **Temperature** — The creativity dial. 0 = deterministic (always the most likely answer). 1 = creative/random. Most products default to somewhere in the middle. Low for code and factual tasks, higher for brainstorming and creative writing.
- **Training vs. Inference** — Training: the model learns from data (months, millions of $). Inference: the model answers a question (milliseconds, cents).


*→ See [Under the Hood: The API Call](uth.md#the-api-call) for what an LLM call actually looks like in code.*

### Tokens — The Machine's Language

```
  "Strawberry fields forever"
                │
                ▼
        ┌── Tokenizer ──┐
        │                │
        ▼                ▼
  ["Str", "aw",         ["2645", "675",
   "berry",              "15717",
   " fields",            "5765",
   " forever"]           "8901"]
   (Tokens)             (Token IDs)
```

Before the LLM processes anything, text is split into **tokens** — word fragments with numeric IDs. The model never sees raw text — it sees only these fragments. This seems like a technical detail, but it has big consequences.

**Why tokens explain so much "weird" LLM behavior:** Ask a model "How many r's in strawberry?" and it often gets it wrong. Not because it can't count, but because "strawberry" becomes three tokens — "Str", "aw", "berry" — and the model has no access to the individual letters inside them. So when you ask "how many r's?", the model is guessing, not counting. The same goes for reversing a string or simple spelling tasks: the model literally can't see what you think it sees.

Arithmetic is similar. A number like "184723" might be split into ["184", "723"]. The model doesn't see a number — it sees two unrelated text fragments. That's why LLMs can reason about math conceptually but fumble basic calculations.

Tokens also explain why some LLMs work better in English than in other languages. Tokenizers learn which character combinations to group together based on their training data — and that data has historically been dominated by English. As a result, English text gets compressed into fewer, larger tokens. German or Japanese text gets split into more, smaller pieces — meaning the same content uses more tokens, fills the context window faster, costs more, and generally gets worse results.

Rule of thumb: 1 token ≈ 4 characters of English, ≈ 3 characters of German.

---

## 2. The Chatbot — Statefulness as Illusion

The LLM from Section 1 has no memory — each call starts from zero. A chatbot creates the illusion of a continuous conversation by resending everything that was said before.

```
  Round 1:                           Round 2:
  ┌──────────────────┐              ┌──────────────────────────────────┐
  │ User: "I'm Max"  │              │ User: "I'm Max"                  │
  └────────┬─────────┘              │ Assistant: "Hello Max!"          │
           │                        │ User: "What's my name?"          │
           ▼                        └────────────────┬─────────────────┘
    ┌─────────────┐                                │
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

What products like ChatGPT call "memory" is built on the same principle — with an added step: key facts from past conversations are extracted, stored separately, and included in the context on each call (a lightweight form of RAG, covered in Part II).

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

These role labels are conventions the model learned during training — strong signals, but not hard rules. A sufficiently clever message in the "user" slot can override instructions from the "system" slot — a vulnerability called prompt injection, which we'll cover in Part III.

---

## 3. The System Prompt — Programming Behavior

In Section 2 we saw that the model receives a list of messages with roles. The system prompt is the first message in that list — written not by you, but by whoever built the product. It steers how the model behaves before you say a word, and it's where tool definitions, guardrails, and safety constraints live.

```
  ┌─────────────────────────────────────────┐
  │  System Prompt (invisible to user)       │
  │  "You are a travel assistant. Be concise.│
  │   Recommend based on budget and          │
  │   interests."                            │
  ├─────────────────────────────────────────┤
  │  User: "Plan a weekend trip to Berlin"│
  └──────────────────┬──────────────────────┘
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
- **Tool definitions** — which tools the model can use, and how to call them (more on this in §5)

The system prompt occupies space in the context window on every call — a long system prompt means less room for your conversation. This is why system prompts in production are kept concise: every word competes with the messages, tool definitions, and other content the model needs to see.

---

## 4. Structured Output — Machine Talks to Machine

```
  Prompt: "Here are three restaurant reviews.
           Extract the details and structure
           your response as follows:
           {
             "name": "...",
             "cuisine": "italian | french | ...",
             "price_range": "$ | $$ | $$$",
             "vegetarian_friendly": true | false
           }"
                     │
                     ▼
              ┌─────────────┐
              │     LLM     │
              └─────────────┘
                     │
                     ▼
           {
             "name": "Trattoria Milano",
             "cuisine": "Italian",
             "price_range": "$$",
             "vegetarian_friendly": true
           }
```

LLMs can produce more than flowing prose — they can generate highly structured data formats such as JSON or XML. You include the desired format in your prompt, and the model fills it in. Modern LLMs even offer constraint modes that *guarantee* the output conforms to a given structure, producing nothing else.

**Why this matters:**
- Software can parse structured data reliably but can't interpret free text — structured output makes LLM results usable by other programs
- It turns the LLM from a conversation partner into a software component: its output can flow into spreadsheets, databases, dashboards, or other code
- It's also the foundation for what comes next — to call a tool, the model will need to specify *which* tool with *which* parameters in a precise format

---

## 5. Tool Use — Hands for the LLM

```
  ┌─────────────────────────────────────────────────┐
  │  System Prompt:                                  │
  │  "You are a helpful assistant."                  │
  │                                                  │
  │  Available tools:                                │
  │    get_weather(city: string) → weather data      │
  │    web_search(query: string) → search results    │
  ├─────────────────────────────────────────────────┤
  │  User: "What's the weather in Tokyo?"            │
  └──────────────────────┬──────────────────────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │     LLM     │
                  └─────────────┘
                         │
         Tool call: get_weather(city="Tokyo")
                         │
                         ▼
              ┌─────────────────┐
              │  Application    │──── actual API call
              │  executes tool  │
              └────────┬────────┘
                       │
                       ▼
    Result: { temp: "28°C", condition: "humid" }
                       │
                       ▼
                ┌─────────────┐
                │     LLM     │
                └─────────────┘
                       │
                       ▼
   "It's currently 28°C and humid in Tokyo."
```

```
Behind the scenes — what the LLM sees at each step:

Step 1:  [system: "You are a helpful assistant.",
          tools: [get_weather, web_search],
          user: "What's the weather in Tokyo?"]
              → LLM responds with: tool_call: get_weather(city="Tokyo")

Step 2:  [system: "...", tools: [...],
          user: "What's the weather in Tokyo?",
          assistant: tool_call: get_weather(city="Tokyo"),
          tool: { temp: "28°C", condition: "humid" }]
              → LLM responds with: "It's currently 28°C and humid in Tokyo."
```

**The crucial insight:** The LLM doesn't execute tools itself. It only decides *which* tool to call with *which* parameters. The application around the LLM performs the actual call and feeds the result back.

And the tool definitions? They're just text in the context window — typically part of the system prompt. The model has learned to recognize this format and generate matching structured calls.

**Typical tools:** Web search, database queries, API calls, file operations, CRM access, code execution.

One of these deserves a closer look. Most tools fetch information from the outside world. Code execution is different — it lets the model *compute*, compensating for weaknesses built into how LLMs work.

**Why code execution changes everything:** Remember the strawberry problem from §1? The model can't count letters in "strawberry" because it never sees individual letters — only tokens. But give the model a code execution tool, and it writes `'strawberry'.count('r')` — correct, every time. You can often trigger this simply by asking the model to "use code." The model didn't get smarter. It got a calculator. The same applies to arithmetic, date calculations, sorting, and anything else where precise computation beats pattern matching. This is why the *same model* gives better answers in a product that has code execution than in one that doesn't.

Tool integrations are increasingly standardized through protocols like **MCP (Model Context Protocol)**, which aim to make tools portable across different AI systems — define the tool once, use it with any model.

---

## 6. The Agentic Loop — Autonomous Action

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

### Agents in Practice

An agent's capabilities depend entirely on which tools it has. The loop is always the same; the tools determine what is possible.

Tools vary enormously in *generality*. A `get_weather()` tool does one thing. A `web_search()` tool does many things. A `run_shell_command()` tool — a command line that can run any program on the computer — does almost anything: read and write files, run code, install software, call APIs, query databases. This is why shell access is sometimes called the "god tool": it doesn't give the agent one new capability, it gives the agent an open-ended surface to act on the world. The further right on this spectrum, the more powerful the agent — and the more important the guardrails from above become.

Concrete escalation: ask an agent to "prepare a competitive analysis." With only web search, it can research and summarize. Add shell access, and it can write and run code to scrape data, produce charts, and compile a formatted report. Add integrations — email, calendar, cloud storage — and it can send the finished report to your team and schedule a follow-up meeting. Same loop, same model, radically different outcomes.

Products like Claude Code, Cursor, or Claude's computer use feature are, at their core, an agentic loop with shell access. Dedicated tool integrations (Google Calendar, Gmail, Slack, CRM) are convenience on top: you *could* do everything via shell, but a dedicated `list_events()` call is more reliable and the model doesn't need to handle authentication tokens.

Some agents also maintain memory across sessions — not because the LLM remembers, but because the application stores notes and loads them into context next time (the same illusion from §2, at a larger scale).

When someone says "we're deploying an agent," the first question to ask is: *what tools does it have?* That tells you more about what it can do — and what can go wrong — than any other detail.

---

## 7. Multi-Agent — Division of Labor

```
  User: "Plan a birthday party for 30 people:
         find a venue, plan the menu, create invitations."
                     │
                     ▼
         ┌───────────────────────┐
         │   Orchestrator Agent  │
         │   (plans & delegates) │
         └───┬─────┬─────┬──────┘
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

**The practical takeaway:** When you give an AI a complex task, structure it as clear, separable subtasks. "Find a venue, plan the menu, and create invitations" is easier for the system to delegate than "plan a party."
