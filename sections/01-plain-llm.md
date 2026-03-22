# 1. The Plain LLM — The Foundation

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

A single LLM call is *stateless* — after each response, the model has complete amnesia. It knows nothing about any previous call. This single fact explains why chatbots resend the entire conversation every time (§3).

**Key concepts:**

- **Parameters (weights)** — The model's learned knowledge, encoded as numbers (think of them as the model's "synapses"). Current models have parameters in the billions to trillions. More parameters ≈ more knowledge capacity, but with diminishing returns.
- **Context Window** — How much text the model can "see" at once. Measured in tokens. Current models range from ~100K to over a million tokens. Everything outside the window — prior messages, documents not included — is invisible to the model for that call.
- **Temperature** — The creativity dial. 0 = deterministic (always the most likely answer). 1 = creative/random. Most products default to somewhere in the middle. Low for code and factual tasks, higher for brainstorming and creative writing.
- **Training vs. Inference** — Training: the model learns from data (months, millions of $). Inference: the model answers a question (milliseconds, cents).


<!-- *→ See [Under the Hood: The API Call](../uth.md#the-api-call) for what an LLM call actually looks like in code.* -->

## Tokens — The Machine's Language

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
