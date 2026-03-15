# AI Primer — Meta & Guidelines

## Target Audience

People *using* AI systems, not people building them. Average white-collar workers — comfortable with office software, chatbots, search engines, and similar tools. No programming background assumed.

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
- **Correct broken mental models** — each section earns its place by fixing a specific misconception the target audience holds. If the common intuition is already roughly correct, the section doesn't need deep treatment. The primer is most valuable where people *think* they understand something but their mental model is off. Evidence: Elon University/IDFC survey (Jan 2025, n=500 LLM users) found 49% think LLMs are smarter than they are, 40% say the LLM "understands" them; Nature Machine Intelligence found users systematically overestimate LLM accuracy; NN/g research confirms inaccurate mental models lead to underwhelming usage.

## Editorial Filter: Mental Model Gaps by Section

Each section should be evaluated against: (1) how wrong is the common intuition? (2) how well do existing resources correct it for our audience? Sections with high gaps on both axes are where the primer adds the most value.

| Section | Common (wrong) intuition | What's actually true | Gap size |
|---|---|---|---|
| Multimodality | "The AI sees my image" | Images are tokenized (expensively); text remains more reliable; the model processes token representations, not visual perception | HIGH |
| Context Engineering | "The AI remembers our conversation" | No memory — re-reads everything every call; context window ≠ usable memory; lost-in-the-middle problem | VERY HIGH |
| Thinking Models | "The AI is reasoning step by step" | CoT faithfulness as low as 25% (Anthropic); visible "thinking" may not reflect actual computation; longer ≠ better | HIGH |
| RAG | "Just upload all our documents and the AI will know them" | It searches then reads on each call; quality depends on retrieval, not just access | MODERATE |
| Trusting the Output | "If the AI says it confidently, it's right" | Confidence ≠ accuracy; fabricates sources when pressed; never says "I don't know"; confirms whatever bias you bring | VERY HIGH |
| Security | "I'm just chatting, what's the security risk?" | Prompt injection is unsolved; content the AI reads can hijack it; agent permissions amplify risk | HIGH |
| When to Use AI | "AI is great for everything" / "AI can't be trusted" | Sweet spot is fuzzy input → structured output; dangerous for unverifiable outputs; knowing when NOT to use it matters most | HIGH |
| Routing | "Use the best model for everything" | Different models for different tasks; 90% of tasks don't need the most powerful model | LOW |

**Implication for Routing:** The mental model gap is small — the concept is straightforward once stated. Consider folding into "When to Use AI" or treating as a short sidebar rather than a full section.

## Building the Website

`python3 build.py` generates a multi-page HTML site in `site/`. Open `site/index.html` in a browser. Requires `pandoc`.
