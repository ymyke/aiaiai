# Part II: What the Model Sees

> What flows through the system — and how it's processed on each call.

---

## 8. RAG — Tapping External Knowledge

```
  User: "What does our memo on Lichtwart say?"
                     │
          ┌──────────┴──────────┐
          ▼                     │
  ┌───────────────┐             │
  │  Query →       │             │
  │  Embedding →   │             │
  │  Vector search │             │
  └───────┬───────┘             │
          │                     │
          ▼                     ▼
  ┌───────────────┐    ┌───────────────────────────┐
  │  Vector DB    │    │  Prompt to LLM:            │
  │  (Pinecone,   │───▶│  "Context: [memo excerpt]  │
  │   Chroma,     │    │   Question: What does the  │
  │   pgvector)   │    │   Lichtwart memo say?"     │
  └───────────────┘    └─────────────┬─────────────┘
                                     ▼
                              ┌─────────────┐
                              │     LLM     │
                              └─────────────┘
                                     │
                                     ▼
                         Answer with source citation
```

**Retrieval Augmented Generation (RAG)** solves a core problem: LLMs only know what was in their training data. RAG fetches relevant documents at runtime and injects them into the prompt.

**How it works:**
1. Documents are split into chunks and stored as vectors (embeddings) in a database
2. The user's question is also converted into a vector
3. Similarity search finds the most relevant chunks
4. Those chunks are included as context for the LLM

**Why it matters:** A large share of AI products — chatbots over company knowledge, document search, support tools — are RAG systems at their core. Quality depends heavily on chunking strategy and embedding quality.

### Fine-Tuning vs. RAG vs. Prompting

Three ways to get a model to do what you want, each for different situations:

- **Prompting** (including system prompts and few-shot examples) — Cheapest, fastest to iterate. Good for steering behavior, tone, and format. Limited by context window size.
- **RAG** — Best when the model needs access to specific, changing, or proprietary knowledge (your deal memos, market reports, internal docs). Doesn't change the model itself.
- **Fine-tuning** — Actually retrains the model on your data. Expensive, slow, and hard to iterate. Use it when you need the model to learn a fundamentally different *skill* or style that can't be achieved through prompting — not just to give it information (that's what RAG is for).

In practice, most use cases are solved with prompting + RAG. Fine-tuning is rarely necessary.

---

## 9. Multimodality — More Than Text

```
  ┌────────────────────────────────────────┐
  │              Inputs                     │
  │                                        │
  │   📝 Text   🖼️ Images   📄 PDFs       │
  │   🎤 Audio  📹 Video   📊 Tables      │
  └────────────────────┬───────────────────┘
                       │
              Each input type has its own
              "translator" that converts it
              into the same internal format
              the LLM already understands
                       │
                       ▼
            ┌───────────────────────┐
            │  Same internal format │
            │  as text              │
            └───────────┬───────────┘
                        │
                        ▼
                 ┌─────────────┐
                 │     LLM     │  ← processes images, audio,
                 │             │    and text identically
                 └──────┬──────┘
                        │
                        ▼
                    Text
```

Modern LLMs don't just process text. **Multimodal models** can analyze images, read PDFs, and transcribe audio. This is genuinely useful — you can ask a model to summarize a slide deck, inspect a screenshot, read a diagram, or transcribe a meeting recording, all directly.

But to use multimodality well, it helps to understand what's actually happening underneath. The short version: **everything gets compressed into tokens.**

### It always comes back to tokens

LLMs work on sequences of token-like units — always. Every input, regardless of type, must be translated into that format before the model can process it.

For text, this is straightforward. Language is already sequential: words follow words, sentences follow sentences. The tokenizer (see §1) splits text into fragments, and the model processes them in order. This is the LLM's native mode.

For everything else — images, audio, video, PDFs — the input first needs to be *translated and compressed* into a sequence of token-like units, and where things can go wrong.

### The translation step matters enormously

**Images** must be turned from a 2D picture into a 1D sequence. The image is split into a grid of small patches, and each patch becomes a token-like unit. There's an inherent trade-off: larger patches mean fewer tokens (cheaper, faster) but lose fine detail; smaller patches preserve more detail but consume more of the context window (the space available for your conversation).

**Audio** is chopped into short time slices, each converted into a token-like unit. Relatively straightforward, but long recordings eat tokens fast.

**Video** is the hardest — it's 2D images *plus* time. The token cost is enormous, and most systems can only process short clips or heavily sampled frames.

**PDFs** deserve special mention. A PDF is not "just a document." It can contain selectable text, scanned pages (images of text that aren't machine-readable), charts, photos, tables, multi-column layouts, and footnotes — all mixed together. In that sense, a PDF is often multimodal *itself*. That's why the same model can summarize one PDF perfectly, miss key details in another, or sometimes fail altogether.

### The 2D problem

There's a deeper challenge: the real world is often 2D, 3D, or temporal — but the model consumes a 1D sequence of tokens. A page has rows and columns. A chart has axes and overlapping labels. A table has spatial structure. All of that must be flattened into a single stream.

This is why spatial relationships are fragile. The model may read a chart's trend correctly but confuse which label belongs to which bar. Or it may parse a table but mix up columns. The richer the original layout, the harder the compression.

### Where it goes wrong

1. **Detail loss** — Small text, tiny numbers, blurry screenshots, dense tables. The root cause: compression into a limited number of token-like units loses fine detail.
2. **Structure confusion** — Rotated text, overlapping labels, complex layouts, table misalignment. The model receives a 1D sequence from a 2D layout, so spatial relationships are fragile.
3. **Overconfidence** — The most dangerous one. The model doesn't say "I'm not sure about this number." It reads a chart value as 4.2M when it's actually 4.7M, and presents it with the same confidence as everything else. This is the failure mode that actually causes damage.

### Text is still king

A rough reliability ranking:

| Input type                    | Reliability                                       |
| ----------------------------- | ------------------------------------------------- |
| Clean text                    | Highest                                           |
| Structured tables (CSV, JSON) | Very high                                         |
| PDFs                          | Medium — depends heavily on content               |
| Images / screenshots          | Good for interpretation, weaker for exact details |
| Screenshots of tables         | Fragile                                           |
| Video                         | Expensive and lossy                               |

The common thread: multimodal AI is not "human-level seeing." It's a lossy compression of reality into tokens — powerful and convenient, but fundamentally different from how a person reads a document.

**Rule of thumb:** Use multimodal input for triage, summarization, and first-pass interpretation. For high-stakes work, the practical pattern is: convert the raw input into clean text or structured data first, then let the model reason over that. Not because multimodality is bad, but because structured inputs are more controllable and auditable.

*→ See [Under the Hood: From Pixels to Vectors](uth.md#from-pixels-to-vectors) for how images and text are converted into the vectors the LLM actually processes.*

---

## 10. Thinking Models — The Inner Monologue

```
  Classic LLM:                       Thinking Model:

  "Is this undervalued?"             "Is this undervalued?"
           │                                    │
           ▼                                    ▼
    ┌─────────────┐                      ┌─────────────┐
    │     LLM     │                      │     LLM     │
    └─────────────┘                      │  ┌────────────────────┐
           │                             │  │ Thinking (hidden)  │
           ▼                             │  │ "12M pre at Seed.. │
    Direct answer                        │  │  Comparables show..│
                                         │  │  But the team..."  │
                                         │  └────────────────────┘
                                         └─────────────┘
                                                │
                                                ▼
                                         Answer (visible)
```

Classic LLMs generate the answer directly. **Thinking Models** have a reasoning step *before* the actual answer.

The idea started as a simple prompt trick (2022): write "Think step by step" and the model outputs its reasoning as normal text. Same model, just a cleverer prompt.

The current generation (Claude with Extended Thinking, OpenAI's o1/o3) is fundamentally different: these models were trained through reinforcement learning to reason *before* answering. The ability to think is baked into the model weights. The thinking tokens go into a separate block that's normally hidden from the user.

**When thinking helps:** Complex logic, math, multi-step analysis, code debugging. For simple questions, it's overkill — slower and more expensive.

**Why is this in "What the Model Sees"?** Thinking started as a prompting technique — literally adding "think step by step" to what the model sees. Today it's baked into the model itself, but the trade-off is still about the context window: thinking tokens consume space that could go to other information.

---

## 11. Context Engineering — The Real Discipline

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
- **In what order:** Models weight information at the beginning and end of the context more strongly than the middle ("Lost in the Middle" effect).
- **In what format:** The same knowledge, structured differently, can produce dramatically different results.

**Concrete trade-offs:**
- More RAG context = better informed, but less room for conversation
- More tool definitions = more versatile, but the model gets less decisive about which to pick
- Longer conversation history = more continuity, but higher cost and eventually quality degrades
- Attaching images = richer understanding, but a single high-res image can consume thousands of tokens
- For agents: every loop step fills the context with tool results — after 20 steps the context can be full

This is why "Prompt Engineering" is actually the wrong term. It's not just about the prompt — it's about orchestrating the entire context.
