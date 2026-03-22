# AI Primer — Meta & Guidelines

## Target Audience

People *using* AI systems, not people building them. Average white-collar workers — comfortable with office software, chatbots, search engines, and similar tools. No programming background assumed, but experience with LLMs and chatbots as a curious user is expected, as well as some ability or willingness to understand technical documentation.

## Structure

### Nine Chapters + Closing Page

A dependency chain from simple LLM to autonomous multi-agent systems, with two additions: Multimodality (a branch extending the token concept from §1) and Context Engineering (a synthesis chapter tying everything together).

| # | Section | Role |
|---|---------|------|
| 1 | The Plain LLM | The atomic unit: tokens, statelessness, next-word prediction |
| 2 | Multimodality | Branch: non-text inputs are tokens too, with lossy compression |
| 3 | The Chatbot | Adds conversation via history resend |
| 4 | The System Prompt | Programs behavior with hidden instructions |
| 5 | Structured Output | Machine-readable responses |
| 6 | Tool Use | LLM can act via external tools |
| 7 | The Agentic Loop | Autonomous loops: plan, act, observe, repeat |
| 8 | Multi-Agent | Division of labor via orchestrator + subagents |
| 9 | Context Engineering | Synthesis: everything competes for the finite context window |
| — | What We Didn't Cover | Closing page: thinking models, RAG, trust, security, routing |

Chapters 1 and 3–8 form a strict dependency chain (each requires the previous). Chapter 2 is a branch off Chapter 1 (depends only on tokens) (handled via opening/closing transitions in the section prose). Chapter 9 is the capstone (depends on all preceding chapters).

**Cut from v1 (in `_drafts/`):** Thinking Models, RAG, Routing, Trusting the Output, Security & Risks, When to Use AI. Summarized in the closing page.

### Main Sections

Each numbered section should be **self-contained** and explain the most important concepts at a level accessible to the target audience. A reader should be able to understand the core idea without reading the optional "Diving Deeper" subsections.

## Tone & Style

- Conversational but precise
- Use analogies, but don't stretch them too far
- ASCII diagrams for key concepts
- Bold key terms on first introduction
- Keep it concrete — real examples over abstract explanations
- Disclaimer up front: this guide deliberately simplifies

## Examples

- **Concrete over generic.** "Summarize these 12 restaurant reviews" beats "Summarize this document." Vivid scenarios the reader can picture.
- **Universal over niche.** If the reader needs even a moment to process what the example is about, pick a different one. No domain expertise required.
- **Transparent.** The reader looks *through* the example at the concept, not *at* the example. The example is a window, not a painting.
- **Double duty.** Each example earns its place twice: it illustrates the technical concept AND feels like a real task someone would do.
- **Varied domains.** No single domain forced across all sections. Each concept gets the example that serves it best — everyday work (emails, meetings, documents), everyday life (travel, cooking, shopping).
- **No footnotes.** If an example needs explaining, it's the wrong example.

## Editorial Filter: Mental Model Gaps

Each section earns its place by fixing a specific misconception the target audience holds. If the common intuition is already roughly correct, the section doesn't need deep treatment. The primer is most valuable where people *think* they understand something but their mental model is off.

Mental model gap notes for each topic are embedded as HTML comments in the respective draft files (`_drafts/`). Published chapters (Multimodality, Context Engineering) address their gaps directly in the prose.

## Review Panel

See [panel.md](panel.md) — content panel (what to teach, how to teach it) and fact-check panel (technical accuracy).

## Publishing

The primer is published via GitBook, driven by `SUMMARY.md`.
