# 5. Structured Output — Machine Talks to Machine

```
  Prompt: "Below is a list of restaurant reviews.
           Extract the details and structure
           your response as follows:
           {
             "name": "...",
             "cuisine": "italian | french | ...",
             "price_range": "$ | $$ | $$$",
             "vegetarian_friendly": true | false
           }"
                     │
                     ▼
              ┌─────────────┐
              │     LLM     │
              └─────────────┘
                     │
                     ▼
           {
             "name": "Trattoria Milano",
             "cuisine": "Italian",
             "price_range": "$$",
             "vegetarian_friendly": true
           }
```

LLMs can produce more than flowing prose — they can generate highly structured data formats such as JSON or XML. You include the desired format in your prompt, and the model fills it in. Modern LLMs even offer constraint modes that *guarantee* the output conforms to a given structure, producing nothing else.

**Why this matters:**
- Software can parse structured data reliably but can't interpret free text easily — structured output makes LLM results usable by other programs
- It turns the LLM from a conversation partner into a software component: its output can flow into spreadsheets, databases, dashboards, or other code
- It's also the foundation for what comes next — to call a tool, the model will need to specify *which* tool with *which* parameters in a precise format
