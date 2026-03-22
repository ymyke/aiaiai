# What We Didn't Cover

This primer focuses on the evolution from a plain LLM to autonomous agents — and the constraint that governs them all. Here's what we deliberately left out, each worth understanding but not essential to the core arc.

- **Thinking Models** — Some models reason internally before answering, spending extra tokens on a hidden monologue. The visible "thinking" may not reflect the actual computation, and longer reasoning doesn't always mean better answers.

- **RAG (Retrieval Augmented Generation)** — Most AI products you use at work — "chat with your documents," knowledge bases, support bots — retrieve relevant text at runtime and inject it into the prompt. The model only knows its training data; RAG gives it access to yours.

- **Trusting the Output** — LLMs hallucinate facts, fabricate sources, and confirm whatever bias you bring — all with the same confident tone. The verification rule: if you can't verify the output, don't automate the task.

- **Security & Risks** — Prompt injection is an unsolved problem: content the AI reads can hijack its behavior. Agents with access to your email, calendar, and files can do real damage if manipulated. The principle of least privilege applies.

- **Routing** — Not every request needs the most powerful model. In practice, 80% of tasks can be handled by smaller, cheaper, faster models. Matching tasks to the right model is a discipline of its own.

---

### A note on "AI" beyond this primer

This primer covers LLMs — general-purpose language models like ChatGPT and Claude. But "AI" is much broader. When you hear that "AI predicts protein structures" (AlphaFold) or "AI forecasts weather" (GraphCast), those are specialized models: purpose-built neural networks trained on domain-specific data, not chatbots. They share some underlying technology (neural networks, transformers) but are entirely different systems — no context window, no system prompt, no conversation.

When ChatGPT explains biology "correctly," it's because the explanation existed in its training data — not because it computed anything about molecules. The model that *actually* predicts protein structures is a different system entirely.

---

*This primer is a work in progress. If something is unclear, missing, or wrong — or if you have a better example or analogy — contributions and feedback are welcome.*
