# AI Primer: The Evolution of AI Systems

> A non-technical guide to how AI systems actually work.
> From fundamentals to agents — step by step.

MN is it really non-technical? and what does that mean? or is it sth else? non-technical enough that non-CS people can understand it but technical enough to understand how agentic systems and ther AI systems work which helps to use them more effectively? -- how to put that into few words sexily?

*This guide deliberately simplifies. Some details are omitted, some analogies are imperfect. The goal is a useful mental model, not a textbook.*

---

## [Part I: The Evolution](part1-the-evolution.md)

A dependency chain from a simple text box to autonomous agents. Each step requires the previous one — this is the spine of the primer.

MN Dependency chain?? Each step requires the prev one?? -- let's find an intro that is more useful, sexier and really says sth valuable.

1. **The Plain LLM** — What an LLM actually is: a stateless probability machine that predicts the next word.
2. **The Chatbot** — The LLM has no memory; the application fakes it by resending the full conversation every time.
3. **The System Prompt** — A hidden instruction at the start of every conversation that steers how the model behaves.
4. **Structured Output** — Making the model respond in JSON instead of prose, so software can act on it. MN can we say this w/o using json somehow here?
5. **Tool Use** — The model decides which tool to call; the application actually executes it. MN puts the decision front, but it's not about the decision and more about the fact that there's tools in the first place?
6. **The Agentic Loop** — Instead of one tool call, the model plans, acts, observes, and repeats until done.
7. **Multi-Agent** — When one agent isn't enough, an orchestrator delegates to specialized subagents.

## [Part II: What the Model Sees](part2-what-the-model-sees.md)

Every section here is about the same scarce resource: the context window. What knowledge goes in, in what format, how deeply the model reasons over it — and how to orchestrate all of it.

MN "every section here..." -- boring beginning? try to make this intro more engaging?

MN what is the best sequence below? is the current seq the best? (I think I'd like RAG to be later)

8. **RAG** — The model only knows its training data; RAG injects relevant documents into the prompt at runtime.
9. **Multimodality** — Images, PDFs, and audio all get compressed into tokens — with trade-offs in detail, cost, and reliability.
10. **Thinking Models** — Some models reason before answering, spending extra tokens on an internal monologue.
11. **Context Engineering** — The discipline of filling the finite context window with the right information in the right order. *(Capstone of Part II.)*

## [Part III: In Practice](part3-in-practice.md)

The system works — now what? Part III covers the decisions and risks that matter when AI meets the real world.

MN Try to make intro that is much more valuable. "The system works — now what?" -- what does that help? "Part III" is obvious it has been <10 words before...

12. **Routing** — Not every request needs the most powerful model; routing matches tasks to the right model for cost and speed.
13. **Trusting the Output** — The model invents facts, fabricates sources, and gives you whatever opinion you ask for — all with the same confident tone.
14. **Security & Risks** — Prompt injection, data privacy, and agent permissions: what can go wrong and how to mitigate it.
15. **When to Use AI** — Where AI genuinely helps, where it's dangerous, and the one rule that tells them apart.

---

## Glossary

| Term                    | Explanation                                                          |
| ----------------------- | -------------------------------------------------------------------- |
| **Token**               | Word fragment, the basic unit for LLMs (~¾ of a word)                |
| **Context Window**      | Maximum text an LLM can process at once                              |
| **Temperature**         | Creativity dial (0 = deterministic, 1 = creative)                    |
| **Inference**           | A single call to the LLM                                             |
| **Embedding**           | Numeric vector representation of text (or images, audio)             |
| **RAG**                 | Retrieval Augmented Generation — external knowledge at runtime       |
| **Fine-Tuning**         | Retraining a model on custom data                                    |
| **Harness**             | All application code around the LLM (loop, tools, RAG, routing)      |
| **Context Engineering** | The discipline of optimally filling the context window on every call |
| **Prompt Engineering**  | Popular term for writing effective prompts — this primer uses the broader term Context Engineering (§11) |
| **Few-Shot**            | Examples in the prompt to demonstrate desired behavior               |
| **Chain of Thought**    | Step-by-step reasoning, explicit or implicit                         |
| **MCP**                 | Model Context Protocol — open standard for connecting tools to LLMs  |
| **Guardrails**          | Safety mechanisms that prevent unwanted outputs                      |
| **Hallucination**       | False information invented by the model                              |

---

*v.3-en — March 2026*
