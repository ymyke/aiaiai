# Part I: The Evolution

> From a text box to autonomous agents — layer by layer.

When you use an AI chatbot, it looks like one thing: a text box that gives you answers. Under the surface, there are several ideas stacked on top of each other — each one unlocking capabilities the previous ones couldn't. This part takes them apart. By the end, you'll understand not just what AI can do, but *why* — and where the limits come from.

1. [**The Plain LLM**](01-plain-llm.md) — What an LLM actually is: a stateless probability machine that predicts the next word.
2. [**The Chatbot**](02-chatbot.md) — The LLM has no memory; the application fakes it by resending the full conversation every time.
3. [**The System Prompt**](03-system-prompt.md) — A hidden instruction at the start of every conversation that steers how the model behaves.
4. [**Structured Output**](04-structured-output.md) — Making the model respond in a fixed structure instead of freeform text, so software can act on it.
5. [**Tool Use**](05-tool-use.md) — The model can call external tools — search, calculate, look things up — but the application is what actually runs them.
6. [**The Agentic Loop**](06-agentic-loop.md) — Instead of one tool call, the model plans, acts, observes, and repeats until done.
7. [**Multi-Agent**](07-multi-agent.md) — When one agent isn't enough, an orchestrator delegates to specialized subagents.
