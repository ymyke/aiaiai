# AI Primer — Meta & Guidelines

## Target Audience

Average white-collar workers. Not particularly computer-savvy, but comfortable with office software, chatbots, search engines, and similar tools. No programming background assumed.

MN people *using* such systems. Not people *building* them.

## Structure

### Three-Part Arc

| Section | Role | Part |
|---|---|---|
| The Plain LLM | The atomic unit | I: The Evolution |
| The Chatbot | Adds conversation | I: The Evolution |
| The System Prompt | Programs behavior | I: The Evolution |
| Structured Output | Machine-readable responses | I: The Evolution |
| Tool Use | LLM can act | I: The Evolution |
| The Agentic Loop | Autonomous loops | I: The Evolution |
| Multi-Agent | Division of labor | I: The Evolution |
| RAG | External knowledge | II: What the Model Sees |
| Multimodality | Broader input types | II: What the Model Sees |
| Thinking Models | Deeper reasoning | II: What the Model Sees |
| Context Engineering | Orchestrating all of the above | II: What the Model Sees |
| Routing | Cost/quality optimization | III: (tbd) |
| Security & Risks | What can go wrong | III: (tbd) |

**Part I — The Evolution:** A dependency chain from simple LLM to autonomous multi-agent systems. Each step requires the previous one. This is the spine of the primer.

**Part II — What the Model Sees:** What flows through the system and how it's processed on each call. RAG (knowledge), Multimodality (input types), and Thinking (reasoning depth) are concrete dimensions. Context Engineering is the capstone — the discipline of orchestrating all of it within the finite context window. Alternatives considered: "Feeding the Model", "What Goes In". Note: "Thinking" is a stretch for "what the model sees" — address in content by framing it as "how deeply the model examines what it sees." Consider adding Prompt Engineering as a section here (currently folded into System Prompt in Part I).

**Part III — In Practice:** What matters when you use AI systems for real.

- **Routing** — choosing the right model for the job (cost/quality/speed trade-offs)
- **Trusting the Output** — hallucinations (inventing facts, fabricating sources when pressed), overconfidence (never says "I'm not sure"), opinions on demand (confirmation bias, false neutrality), the verification rule (if you can't verify it, don't automate it)
- **Security** — prompt injection, indirect prompt injection, data privacy, agent permissions
- **When to Use AI** — where it genuinely helps (fuzzy input → structured output, first drafts, pattern recognition), where it's dangerous (guaranteed correctness, unverifiable outputs, replacing judgment with delegation)

### Main Sections

Each numbered section should be **self-contained** and explain the most important concepts at a level accessible to the target audience. A reader should be able to understand the core idea without reading the "Under the Hood" subsections.

### Under the Hood (Diving Deeper)

Optional subsections that dive deeper into the technical details. More technical than the main text, but still accessible. These sections help readers who want to understand *why* things work the way they do, not just *what* they do.

- Marked as `### Under the Hood: [Topic]`
- Not required reading — the main section should stand on its own
- Good for: internal mechanics, embeddings, encoding details, architecture concepts
- Alternative name considered: "Diving Deeper"

In the final result, UTH sections may be collapsible/hidden, expanded only on interaction — keeping the main flow focused and uncluttered.

## Tone & Style

- Conversational but precise
- Use analogies, but don't stretch them too far
- ASCII diagrams for key concepts
- Bold key terms on first introduction
- Keep it concrete — real examples over abstract explanations
- Disclaimer up front: this guide deliberately simplifies

## Key Principles

- **Tokens are the central user-facing concept** — cost, context limits, and prompt design all revolve around tokens
- **Embeddings are supporting** — mentioned once to complete the picture, not a major topic
- **Text is the native format** — multimodality expands input but text remains most reliable
- **Practical relevance over technical completeness** — what does the reader need to *do* with this knowledge?
