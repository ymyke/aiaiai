# Glossary

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
| **Prompt Engineering**  | Popular term for writing effective prompts — this primer uses the broader term Context Engineering (section 9) |
| **Few-Shot**            | Examples in the prompt to demonstrate desired behavior               |
| **Chain of Thought**    | Step-by-step reasoning, explicit or implicit                         |
| **MCP**                 | Model Context Protocol — open standard for connecting tools to LLMs  |
| **Guardrails**          | Safety mechanisms that prevent unwanted outputs                      |
| **Hallucination**       | False information invented by the model                              |
