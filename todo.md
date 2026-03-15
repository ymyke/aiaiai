- disclaimer: for the sake of simplicity, all kinds of simpoliciations and "auslassungen"  etc. and likely all kinds of errors.
- deliver as nice website? 
- maybe with animations?
  

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

# more fundamental thoughts

- detetministic vs probabilistic (harness...)
- pseudocode
- ...

# review

- panel with karpathy and others
- factcheck



gimme a realistics example of how an llm-based system would "understand" an image. step by step. including what the tokens would look like. can be technical and we might break it down later.


----

- resolution tradeoff
- everthing gets mapped to tokens "somehow". and that somehow matters.
- positional awareness?

clean text is still the model’s strongest input format


images are useful, but often more approximate

PDFs are often a mixture of text extraction + layout interpretation + sometimes image understanding

tables / spreadsheets are especially fragile

charts and diagrams can be read surprisingly well, but also misread in subtle ways


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



# issues

layout confusion

chart misreading

missing text hidden in images

overconfidence about visual evidence


missing small text

confusing numbers

misreading tables

incorrect chart values


Even though models can read slides well, they struggle with:

very small fonts

dense tables

rotated text

overlapping labels

complex charts

blurry screenshots

Because the representation is still compressed visual features, not symbolic characters.

# summary

1. What multimodality enables

direct use of screenshots, PDFs, audio, diagrams, images

less manual preprocessing by the user

broader automation surface

2. What it does not mean

not equal reliability across all formats

not guaranteed exact extraction

not “human-level seeing”

not a replacement for structured data pipelines

3. What good practice looks like

use multimodal input for triage, summarization, and first-pass interpretation

use extracted text / structured data for high-stakes decisions

verify numbers, tables, charts, citations

prefer source-preserving workflows


So the practical hierarchy is often:

raw modality → normalized text/structure → LLM reasoning

Not because multimodality is bad, but because structured inputs are more controllable and auditable.


# images

Use multimodal input to speed up triage and interpretation, but not as a substitute for exact extraction when precision matters.


# pdf

2. A PDF is not “just a document”

Very important for non-technical users.

When people upload a PDF, they think they are giving the model “the report.”

But a PDF may actually contain very different things:

selectable text

scanned images of text

tables rendered visually

charts

footnotes, headers, sidebars, two-column layouts

hidden OCR layers

That is why the same model can:

summarize one PDF very well

completely miss key details in another





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