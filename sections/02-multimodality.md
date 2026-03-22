# 2. Multimodality — More Than Text

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

For everything else — images, audio, video, PDFs — the input first needs to be *translated and compressed* into a sequence of token-like units. This is where things can go wrong.

### The translation step matters

**Images** must be turned from a 2D picture into a 1D sequence. The image is split into a grid of small patches, and each patch becomes a token-like unit. There's an inherent trade-off: larger patches mean fewer tokens (cheaper, faster) but lose fine detail; smaller patches preserve more detail but consume more of the context window (the space available for your conversation).

**Audio** is chopped into short time slices, each converted into a token-like unit. Relatively straightforward, but long recordings eat tokens fast.

**Video** is the hardest — it's 2D images *plus* time. The token cost is enormous, and most systems can only process short clips or heavily sampled frames.

**PDFs** deserve special mention. A PDF is not "just a document." It can contain selectable text, scanned pages (images of text that aren't machine-readable), charts, photos, tables, multi-column layouts, and footnotes — all mixed together. In that sense, a PDF is often multimodal *itself*. That's why the same model can summarize one PDF perfectly, miss key details in another, or sometimes fail altogether.

### The layout problem

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
| Audio (speech transcription)  | High — mature and accurate for major languages    |
| Screenshots of tables         | Fragile                                           |
| Audio (non-speech)            | Low — limited model support, unreliable           |
| Video                         | Expensive and lossy                               |

The common thread: multimodal AI is not "human-level seeing." It's a lossy compression of reality into tokens — powerful and convenient, but fundamentally different from how a person reads a document.

**Rule of thumb:** Use multimodal input for triage, summarization, and first-pass interpretation. For high-stakes work, convert the raw input into clean text or structured data first, then let the model reason over that. Not because multimodality is bad — it is improving rapidly — but because structured inputs are more controllable and auditable.

<!-- *→ See [Under the Hood: From Pixels to Vectors](uth.md#from-pixels-to-vectors) for how images and text are converted into the vectors the LLM actually processes.* -->

---
