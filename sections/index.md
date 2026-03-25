# AI Primer

*Under the hood of the AI systems you use every day.*

You've been using ChatGPT, Claude, or Gemini long enough to have intuitions — what works, what doesn't, when the model seems brilliant and when it falls apart. But the system behind the text box is still a mystery.

This primer opens it up. Nine short chapters, each building on the last: how a text predictor becomes a chatbot. How a chatbot gains tools. How tools enable autonomous agents. And the finite context window that governs them all.

---

1. [**The Plain LLM**](01-plain-llm.md) — What an LLM actually is: a stateless probability machine that predicts the next word.
2. [**Multimodality**](02-multimodality.md) — Images, PDFs, and audio all get compressed into tokens — with trade-offs in detail, cost, and reliability.
3. [**The Chatbot**](03-chatbot.md) — The LLM has no memory; the application fakes it by resending the full conversation every time.
4. [**The System Prompt**](04-system-prompt.md) — A hidden instruction at the start of every conversation that steers how the model behaves.
5. [**Structured Output**](05-structured-output.md) — Making the model respond in a fixed structure instead of freeform text, so software can act on it.
6. [**Tool Use**](06-tool-use.md) — The model can call external tools — search, calculate, look things up — but the application is what actually runs them.
7. [**The Agentic Loop**](07-agentic-loop.md) — Instead of one tool call, the model plans, acts, observes, and repeats until done.
8. [**Multi-Agent**](08-multi-agent.md) — When one agent isn't enough, an orchestrator delegates to specialized subagents.
9. [**Context Engineering**](09-context-engineering.md) — Everything competes for the same finite context window. This is the discipline of filling it well.

---

*This grew out of years of working with these systems and explaining them to the people around me — and never finding quite the right guide to point them to. It deliberately simplifies — the goal is a useful mental model, not a textbook.*

Written by [Myke Näf](https://ch.linkedin.com/in/michaelnaef) — computer scientist turned VC ([Übermorgen Ventures](https://uebermorgen.vc)) who still can't leave the terminal alone. With considerable help from the machines described herein.

Found an error? Have a better way to explain something? [Contribute on GitHub](https://github.com/ymyke/ai-primer) — contributions welcome.
