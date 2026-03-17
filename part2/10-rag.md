# 10. RAG — Tapping External Knowledge

```
  User: "What's our remote work policy?"
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
  │  (Pinecone,   │───▶│  "Context: [handbook excerpt│
  │   Chroma,     │    │   on remote work]           │
  │   pgvector)   │    │   Question: What's our     │
  │               │    │   remote work policy?"      │
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
- **RAG** — Best when the model needs access to specific, changing, or proprietary knowledge (company handbooks, meeting notes, internal reports). Doesn't change the model itself.
- **Fine-tuning** — Actually retrains the model on your data. Expensive, slow, and hard to iterate. Use it when you need the model to learn a fundamentally different *skill* or style that can't be achieved through prompting — not just to give it information (that's what RAG is for).

In practice, most use cases are solved with prompting + RAG. Fine-tuning is rarely necessary.

---
