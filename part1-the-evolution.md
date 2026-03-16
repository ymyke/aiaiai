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
MN was this forgotten when we adjusted all the examples in one of the latest commits? Or did it remain unchanged on purpose?

A Large Language Model is, at its core, a text continuation engine: given some text, it produces the most likely next piece of text, token by token. No memory, no knowledge updates after training, no logic in the classical sense — just extraordinarily good pattern recognition over language. It doesn't "answer questions" — it continues text. That it *appears* to answer questions is because a question followed by a good answer is the most likely continuation.

**Important:** A single LLM call is *stateless*. It knows nothing about previous calls. This has consequences for everything that follows. MN is the "imporant" nece here? MN will readers grasp the concept of statelessness -- and then statefulness later? are these 2 sentences enough?

**Key concepts:**

- **Parameters (weights)** — The model's learned knowledge, encoded as numbers (think of them as the model's "synapses"). Current models have parameters in the billions to trillions. More parameters ≈ more knowledge capacity, but with diminishing returns.
- **Context Window** — How much text the model can "see" at once. Measured in tokens. Current models range from ~100K to over a million tokens. Everything outside the window — prior messages, documents not included — is invisible to the model for that call.
- **Temperature** — The creativity dial. 0 = deterministic (always the most likely answer). 1 = creative/random. Low for code, higher for brainstorming. (MN what are typical settings in today's LLMs?)
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
  ["Str", "awberry",    ["2905", "675",
   " fields",            "5765",
   " forever"]           "8901"]
   (Tokens)             (Token IDs)
```

MN i think rather: ["Straw", "berry", " fields", " forever"] ?

Before the LLM processes anything, text is split into **tokens** — word fragments with numeric IDs. The model never sees raw text — it sees only these fragments. This seems like a technical detail, but it has big consequences.

**Why tokens explain so much "weird" LLM behavior:** Ask a model "How many r's in strawberry?" and it often gets it wrong. Not because it can't count, but because "strawberry" is one or two tokens — the model never sees individual letters. It's like reading a word printed across puzzle pieces (MN lets find a better analogy; or not use one at all? let's discuss): you see each piece, but you can't easily count letters that are glued inside them. The same goes for reversing a string or simple spelling tasks: the model literally can't see what you think it sees.

Arithmetic is similar. A number like "184723" might be split into ["184", "723"]. The model doesn't see a number — it sees two unrelated text fragments. That's why LLMs can reason about math conceptually but fumble basic calculations.

Tokens also explain why some LLMs work better in English than in other languages. Tokenizers are trained mostly on English text, so English gets efficient, large tokens. (MN so more training implies larger tokens wrt tokenizers?) German or Japanese text gets split into more, smaller pieces — meaning the same content uses more tokens, fills the context window faster, costs more, and generally gets worse results.

Rule of thumb: 1 token ≈ 4 characters of English, ≈ 3 characters of German.

---

## 2. The Chatbot — Statefulness as Illusion

MN Then (see next MN note) write something taht connects to this.

```
  Round 1:                           Round 2:
  ┌──────────────────┐              ┌──────────────────────────────┐
  │ User: "I'm Max"  │              │ User: "I'm Max"              │
  └────────┬─────────┘              │ Asst: "Hello Max!"           │ MN write Assistant out?
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

Without conversation history, the same question fails: MN should we start with this ease inmto the section with a little (just a little, and still make it valuable) more words? -- OR: if the rule is to always lead with a diagram in part 1, then at least be a little more genereous with the explanation here before showing the next diagram.

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

**The key insight:** (MN this nece?) The LLM itself has no memory. Every round, the *entire conversation history* is sent again as input. The chatbot is an application *around* the LLM that manages conversation history and includes it with every call.

This explains why long conversations eventually break off (context window full), why the model "forgets" what was said 100 messages ago, and why each message in a long chat costs more — or hits rate limits sooner — because of the growing token count. Some products manage this by summarizing older messages to free up space — trading accurate recall of early messages for more room to work with. MN there's also caching, right? Worth a mention or not?

What products like ChatGPT call "memory" is exactly this trick (MN better: "is also based on this trick"?) — or a variant where key facts are stored separately and injected (MN injected too technical?) into the context (MN "and therefore the conversation"?) on each call (a lightweight form of RAG, covered in Part II).

**Message format** — Most LLM APIs use a role system. (MN do we need to use API here? Or "Most LLMs work with a role system behind the scenes"?) Think of it as a script with labeled speakers:

```
messages: [
  { role: "system",    content: "You are a helpful assistant." },
  { role: "user",      content: "I'm Max" },
  { role: "assistant", content: "Hello Max!" },
  { role: "user",      content: "What's my name?" }
]
```

The "system" message sets behavior (more on that next). The "user" and "assistant" messages are the conversation turns. The roles serve a practical purpose: they let the model distinguish instructions to follow (system) from input to respond to (user) from its own prior responses to stay consistent with (assistant). This format is what every chatbot, API wrapper, and agent framework uses under the hood. 

These role labels are a convention the model learned during training — not a built-in rule it must obey. The model treats them as strong signals, but they are not a security boundary. This distinction matters when we discuss prompt injection in Part III. (MN is this distinction really so fundamental that it needs to be mentioned and forward-ref'd? discuss why v why not)

---

## 3. The System Prompt — Programming Behavior

MN is this part of the evolution in part 1? discuss why v why not. -- what are reasons why the reader must understand this here? 

MN: Generally, what will it help the reader if she understand that there's a system prompt? Include more of that in this section? discuss deeply

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

The system prompt is a special message at the start of every conversation that steers the model's behavior. It's powerful, but not a command — more of a strong suggestion.

This is where most practical "prompt engineering" (MN rephrase, practical "prompt engineering" doesnt help i think) happens: defining persona and tone of the LLM, specifying output format, providing knowledge and context, setting rules and constraints, giving examples (MN mention guardrails, ethics and similar?). As we'll see in §11, prompt engineering is actually one part of a bigger discipline — **Context Engineering** — that covers everything the model sees, not just the text you write. MN fwd ref not really useful here?

MN should definitley mention tool definitions above to connect to later sections?

The system prompt consumes tokens on *every message*, because it's resent every time. (MN this is really the case, right? factcheck hard)

---

## 4. Structured Output — Machine Talks to Machine

```
  Prompt: "Extract restaurant details"      + Schema
                     │                          │
                     ▼                          ▼
              ┌─────────────────────────────────────────┐
              │  LLM (with JSON mode / schema constraint) │
              └─────────────────────────────────────────┘
                                  │
                                  ▼
                          {
                            "name": "Trattoria Milano",
                            "cuisine": "Italian",
                            "price_range": "$$",
                            "vegetarian_friendly": true
                          }
```

<MN> Alternative structure + content for the section. Texts need revising of course. wdyt?

Image:

Prompt: "Extract restaurants from the attached pdf. Structure your response as follows:
{
       "name": "...",
       "cuisine": "italian|french|...",
       "price_range": "$$",
       "vegetarian_friendly": "true|false",
}
v
LLM (no mention of json mode schema constraint)
v
...

Text:

At some point, LLMs were able to reliably produce highly structured data, formats such as JSON or XML. If asked for it. Nowadays some LLMs even support special constraint modes that prevent them from generating anything other than the requested structure.

Why this matters:
...

</MN>


Before an LLM can use tools (MN nobody knows at this point taht we want to use tools), it needs to answer in a structured way. **Structured Output** forces the model to respond in a defined format (JSON, XML) instead of free text.

**Why this matters:**
- Software can parse JSON but can't reliably interpret free text
- It's the bridge between "LLM as conversation partner" and "LLM as software component"
- It's the foundation for tool use — the model needs to specify *which* tool with *which* parameters in a format the application can act on

---

## 5. Tool Use — Hands for the LLM

```
  ┌─────────────────────────────────────────────────┐
  │  System Prompt + Tool Definitions:               │ MN make these 2 lines examples instead of description
  │  (tool definitions are just text in the context) │
  │                                                  │
  │  Available tools:                                │
  │  - get_weather(city) → weather data              │
  │  - web_search(query) → search results            │
  ├─────────────────────────────────────────────────┤
  │  User: "What's the weather in Tokyo?"            │
  └──────────────────────┬──────────────────────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │     LLM     │
                  └─────────────┘
                         │
    Instead of answering directly, the LLM outputs:
    "Call get_weather with city = Tokyo" MN why not Result: get_weather("Tokyo")?
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
                │     LLM     │  (receives result as a new message) MN show the message?
                └─────────────┘
                       │
                       ▼
   "It's currently 28°C and humid in Tokyo."
```

MN options: a) be more verbose above to explain the flow of messages better (as indicated in my MN notes above) OR b) keep it terse above. maybe even terser. but add another diagram that shows how the conversation is build behind the scenes? i.e., each full message as it gets sent to or output from the LLM?

**The crucial insight:** The LLM doesn't execute tools itself. It only decides *which* tool to call with *which* parameters. The application around the LLM performs the actual call and feeds the result back. 

And the tool definitions? They're just text in the context window — typically part of the system prompt. The model has learned to recognize this format and generate matching structured calls.

**Typical tools:** Web search, database queries, API calls, code execution, file operations, CRM access.

MN lead smoother to code execution? comes out the blue here? sth like "By the way, code execution can also be a tool." or so? And then explain how that works in a little more detail before explaining teh strawberry case.

**Why code execution changes everything:** Remember the strawberry problem from §1? The model can't count letters in "strawberry" because it never sees individual letters — only token fragments (MN token fragems or tokens?). But give the model a code execution tool (MN "and tell it to 'use code'"?), and it writes `'strawberry'.count('r')` — correct, every time. The model didn't get smarter. It got a calculator. The same applies to arithmetic, date calculations, sorting, and anything else where precise computation beats pattern matching. This is why the *same model* gives better answers in a product that has code execution than in one that doesn't. MN or maybe here as: When you want an LLM to resolve such a problem using its coding capabilities, you can try adding "use code" to a prompt.

Tool integrations are becoming standardized: **MCP (Model Context Protocol)**, an open standard from Anthropic, defines a universal protocol for connecting tools to LLMs. Think of it as USB for AI tools — instead of building custom integrations for each model, you define the tool once. MN ditch MCP?

---

## 6. The Agentic Loop — Autonomous Action

```
  User: "Plan a weekend trip to Rome: find top
         restaurants, check weather, build an itinerary."
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
              Finished itinerary
```
MN is this image accurate? discuss deeply
MN Observe is outside the LLM?
MN is T-D-A-O the most popular + simple model? Or are there more popular and or simpler models?
MN what about a simpler example prompt? what is the simplest use case that still makes sense and makes it immediately clear how agents work? my idea: "search for x" where x is not easily caught in 1 search query and the agent generates a number of queries and runs them and checks the results? other ideas?
MN should we even show the loop itself as pseudocode in this section? maybe a little later? as additional info for the "unerschrockenen"? or as a UTH?

The leap from tool use to **agent**: instead of calling one tool once, the LLM autonomously plans a sequence of steps and iterates until the task is complete.

**Think → Decide → Act → Observe → Repeat**

The model analyzes the task, breaks it into steps, picks the right tools, observes the result, and decides whether to continue or stop. On errors, it can try alternative strategies. The application typically sets guardrails: max iterations, timeouts, budgets.

**The key word is autonomy:** The agent decides *how many* steps are needed and *which* tools to use in what order. MN this sentence here really that important? discuss

### Agents in Practice

<MN>
- to me, there is:
  - llm + tools + loop == agent
  - llm + tools including shell + loop == agents like claude code cli
  - llm + tools including shell + memory + access to all agent-specific files == openclaw
  - llm + tools including shell + memory + data access/integrations (local or remote/via apis) == ...
- are all of these agents? are some more openclaw than others? does it make sense to diff these dimensions? should there be others? should  we include any of this in the primer?
- any other thoughts around this? and what do we do with this now?
</MN>

Products like Claude Code, Cursor, or Claude's computer use feature are, at their core:

**Agentic loop + shell access (the "god tool") + tool integrations**

A shell can do anything a computer can — read/write files, start processes, call APIs, query databases. Dedicated tool integrations (Google Calendar, Gmail, Slack, CRM) are convenience: you *could* do everything via shell + curl + APIs, but a dedicated `list_events()` call is more reliable and the model doesn't need to handle OAuth tokens.

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

<MN>
- let's think about WHY subagents are relevant to know for the user. 
- and when are they used at all?
  - to parallelize work
  - to spare the context window = not load the entire process into it but only the final conclusion
  - to not have it biased by the current context window? why would that be important?
  - ... what else? 
- subagents can
  - be created by the agent
  - or the user invites the agent to create them, right? why would the uiser do that? parallelization? ...?
</MN>

When a task is too big or too multifaceted for a single agent, you split it across **subagents**. The orchestrator delegates subtasks, each subagent runs its own agentic loop, and returns its result — just like any other tool call.

**Why subagents?**
- **Context separation** — Each subagent has its own context window. The menu planner doesn't need to see the venue options.
- **Specialization** — Each subagent can have its own system prompt, tools, and instructions.
- **Parallelization** — Multiple subagents can work simultaneously.
- **Fault isolation** — If the venue search fails, the menu plan isn't lost.
