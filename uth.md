# AI Primer — Under the Hood

*These sections dive deeper into the technical details behind the main primer. They're optional — the primer is self-contained without them.*

---

## The API Call

When you call an LLM through an API, you send the content of the context window plus a few control parameters: `temperature` and a couple of others. That's essentially it — the model is a function that takes text in and returns text out.

Here's what an actual call looks like. This is Python, but any programming language works — the model is just a service in the cloud that you send a request to:

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    temperature=0.3,
    messages=[
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

print(response.content[0].text)
# → "Paris."
```

That's it. You send a model name, a temperature, a token limit, and the messages. The model returns text. Everything else — the conversation history, the system prompt, the tool definitions — is just more entries in that `messages` list.

The LLM is not running on your computer. It's a service hosted by a provider (Anthropic, OpenAI, Google, etc.). Your code sends a request over the internet and gets a response back — like calling any other web API.

---

## From Pixels to Vectors

Tokens are not what the LLM processes directly. They are first converted into numerical vectors called **embeddings** — lists of numbers that represent meaning in a form neural networks can compute with. The LLM never sees raw text, pixels, or sound. It only processes vectors.

```
  text → tokenizer → token IDs → embedding vectors ─┐
                                                      ├──▶ LLM (transformer)
  image → vision encoder → visual embedding vectors ──┘
```

For text, the process is straightforward: each token ID maps to a fixed embedding vector via a lookup table. The word "cat" always starts as the same vector. Meaning in context — is this a pet or a Linux command? — emerges later, as the transformer processes the full sequence and updates each vector based on its surroundings.

For images, the process is more involved. The image is split into a grid of small patches. A specialized vision encoder processes all patches together, producing one embedding vector per patch. These vectors already carry some awareness of the broader image — the patch containing a cat's ear "knows" there's a desk below it. The vectors are then projected into the same format as text embeddings, so the LLM can process both in a single sequence.

This is why multimodality works at all: different input types are translated into the same kind of vector, and the LLM processes them all identically from that point on.

It also explains why images are less reliable than text. An image must be compressed from millions of pixels into a few hundred vectors. There's always a trade-off: larger patches mean fewer tokens (cheaper, faster) but lose detail; smaller patches preserve more detail but consume more of the context window. Text doesn't have this problem — it's already sequential and discrete.
