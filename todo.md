- disclaimer: for the sake of simplicity, all kinds of simpoliciations and "auslassungen"  etc. and likely all kinds of errors.
- deliver as nice website? 
- maybe with animations?
  
- **Prompt Engineering** — currently folded into System Prompt (Part I, §3). Consider pulling it into Part II as its own section.
- target audience: average whitecollar workers, not particularly computer savvy, use office software, chatbots, search etc.
- memory?
- why roles?
- all examples climate vc related?
- memory eats up context
- access to coding tools -> make certain answers better. e.g. write a script that counts the r's in strawberry or reverses the word strawberry.
- how does multimodal _output_ work?
- more important params? 
  - d_model, embedding_dim 
  - vocab_size 
- compaction?
- context engineering even more challenging with agents
- planning?
- orchestration?
- add links to other articles from the research-articles.md?

# more fundamental thoughts

- detetministic vs probabilistic (harness...)
- pseudocode
- ...
- where do models fit in that do/understand complex biology, and basic physics

# review

- panel with karpathy and others
- factcheck



gimme a realistics example of how an llm-based system would "understand" an image. step by step. including what the tokens would look like. can be technical and we might break it down later.


----

- resolution tradeoff
- everthing gets mapped to tokens "somehow". and that somehow matters.
- positional awareness?



# punchline?

The farther the input is from clean text, the more the system must guess, compress, and reconstruct before reasoning can even begin.


# main points revised

Multimodality — the points that matter

LLMs ultimately work on sequences of token-like units

Text is easiest because language is already sequential

Other media first need to be translated and compressed into a representation the model can process

The quality of that translation step strongly affects the result

Images require turning a 2D picture into a sequence; this creates a trade-off between detail and token cost

PDFs are especially tricky because they are often a messy mix of text, layout, tables, charts, and images

Positional structure is a major challenge: the real world is often 2D or 3D or temporal, but the model consumes a 1D sequence

This is why multimodal AI is powerful, but often less reliable than clean text or structured data

also?
A. Multimodality increases convenience, not guaranteed precision
B. Text is still usually the most reliable format
C. Multimodality is often a compression problem

# main points on modality

main points are:
- llms always work with tokens
- every input gets mapped to tokens somehow
- for text, this is more straightforward than for other media such as images or even video
- the results depend a lot on that mapping (transforming) step
- for images for example the image gets chopped up into pieces and a q is how large these pieces are (larger pieces = miss information, smaller pieces = use more tokens (cost, context))
- for pdf it's even more complicated bc pdf is a complicated format (it's multimodal itself, is that it?)
- posiitional awareness is hard for llms becaue in the end they get a 1-dim list of tookens (correct? how *do* tehy do pos awareness?)








# context engineering

                 CONTEXT WINDOW
        (e.g. 200,000 tokens total)

┌─────────────────────────────────────────────┐
│ System prompt                               │
├─────────────────────────────────────────────┤
│ Conversation history                        │
├─────────────────────────────────────────────┤
│ RAG documents                               │
├─────────────────────────────────────────────┤
│ Image tokens                                │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
├─────────────────────────────────────────────┤
│ Tool definitions                            │
├─────────────────────────────────────────────┤
│ Current user message                        │
├─────────────────────────────────────────────┤
│           space for output                  │
└─────────────────────────────────────────────┘