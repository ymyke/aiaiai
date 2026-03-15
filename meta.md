# AI Primer — Meta & Guidelines

## Target Audience

Average white-collar workers. Not particularly computer-savvy, but comfortable with office software, chatbots, search engines, and similar tools. No programming background assumed.

## Structure

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
