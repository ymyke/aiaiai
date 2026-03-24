# 1. The Plain LLM — The Foundation

The AI products you use daily — ChatGPT, Claude, Gemini, and the like — are all powered by a Large Language Model, or LLM: the engine under the hood. This primer takes apart the system built around it, layer by layer.

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

An LLM is, at its core, a text continuation engine: given some text, it produces the most likely next piece of text, token by token. No memory, no knowledge updates after training, no logic in the classical sense — just extraordinarily good pattern recognition over language. It doesn't "answer questions" — it continues text. That it *appears* to answer questions is because a question followed by a good answer is the most likely continuation.

A single LLM call is *stateless* — after each response, the model has complete amnesia. It knows nothing about any previous call. This single fact explains why chatbots resend the entire conversation every time (as we'll see in section 3).

One consequence of "pattern recognition over language" is easy to miss: nobody programmed the model to write poetry, debug code, or summarize legal contracts. These capabilities *emerged* from training on vast amounts of text — they were discovered, not designed. This is fundamentally different from traditional software, where every feature is explicitly built and individually tested. It explains why LLMs can do surprising things nobody anticipated — and fail in equally surprising ways nobody predicted.

**Key concepts:**

- **Parameters (weights)** — The model's learned knowledge, encoded as numbers (think of them as the model's "synapses"). Current models have parameters in the billions to trillions. More parameters ≈ more knowledge capacity, but with diminishing returns.
- **Context Window** — How much text the model can "see" at once. Measured in tokens. Current models range from ~100K to over a million tokens. Everything outside the window — prior messages, documents not included — is invisible to the model for that call.
- **Temperature** — The creativity dial. 0 = deterministic (always the most likely answer). Higher = more creative/random. Most products default to somewhere in the middle. Low for code and factual tasks, higher for brainstorming and creative writing.
- **Training vs. Inference** — Training: the model learns from data (months, millions of $). Inference: the model answers a question (milliseconds, cents).

The temperature parameter hints at something deeper: **an LLM is a probability machine.** Every response is a fresh sample from a distribution of likely continuations. Given the same input, it can produce different output every time. This is unlike every other piece of software you've used — a spreadsheet, a search engine, a calculator all give identical results for identical input. An LLM doesn't. This single property shapes everything about how AI products are built, and — as we'll see in section 6 — how developers work around it.


## Tokens — The Machine's Language

```
  "Strawberry fields forever"
               │
               ▼
  ["Str", "aw", "berry", " fields", " forever"]
  (Tokens)
               │
               ▼
  [2645, 675, 15717, 5765, 8901]
  (Token IDs — what the model sees)
```

Before the LLM processes anything, text is split into **tokens** — word fragments with numeric IDs. The model never sees raw text — it sees only these tokens. This seems like a technical detail, but it has big consequences.

**Why tokens explain so much "weird" LLM behavior:** Ask a model "How many r's in strawberry?" — a famous example. Older models got it wrong, because "strawberry" becomes three tokens — "Str", "aw", "berry" — and the model has no access to the individual letters inside them. It was guessing, not counting. Current models often get such questions right — partly because famous examples appear in training data, and partly because newer models can "think" step by step, effectively reasoning their way to the correct count.

Arithmetic is similar. A number like "184723" might be split into ["184", "723"]. The model doesn't see a number — it sees two unrelated text fragments. That's why LLMs can reason about math conceptually but fumble basic calculations.

Tokens also explain why some LLMs work better in English than in other languages. Tokenizers learn which character combinations to group together based on their training data — and that data has historically been dominated by English. As a result, English text gets compressed into fewer, larger tokens. German or Japanese text gets split into more, smaller pieces — meaning the same content uses more tokens, fills the context window faster, costs more, and generally gets worse results.
