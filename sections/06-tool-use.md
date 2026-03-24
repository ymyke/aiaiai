# 6. Tool Use — Acting on the World

```
  ┌──────────────────────────────────────────────────────┐
  │  System prompt:                                      │
  │  "You are a helpful assistant."                      │
  │                                                      │
  │  Available tools:                                    │
  │    get_weather(city: string) → weather data          │
  │    web_search(query: string) → search results        │
  ├──────────────────────────────────────────────────────┤
  │  User: "What's the weather in Tokyo?"                │
  └─────────────────────────┬────────────────────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │     LLM     │
                     └─────────────┘
                            │
            Tool call: get_weather(city="Tokyo")
                            │
                            ▼
                   ┌─────────────────┐
                   │  Application    │
                   │  executes tool  │
                   └────────┬────────┘
                            │
                            ▼
         Result: { temp: "28°C", condition: "humid" }
                            │
                            ▼
                     ┌─────────────┐
                     │     LLM     │
                     └─────────────┘
                            │
                            ▼
        "It's currently 28°C and humid in Tokyo."
```


**Behind the scenes — what the LLM sees at each step:**

```
Step 1:  [system: "You are a helpful assistant.",
          tools: [get_weather, web_search],
          user: "What's the weather in Tokyo?"]
              → LLM responds with: tool_call: get_weather(city="Tokyo")

Step 2:  [system: "...", tools: [...],
          user: "What's the weather in Tokyo?",
          assistant: tool_call: get_weather(city="Tokyo"),
          tool: { temp: "28°C", condition: "humid" }]
              → LLM responds with: "It's currently 28°C and humid in Tokyo."
```

The LLM doesn't execute tools itself. It only decides *which* tool to call with *which* parameters. The application around the LLM performs the actual call and feeds the result back.

Tool definitions are just text in the context window — typically part of the system prompt. The model has learned to recognize this format and generate matching structured calls.

**Typical tools:** Web search, database queries, API calls, file operations, email access, CRM access, code execution.

Code execution deserves a closer look. Most tools let the model fetch or manipulate information in the outside world — search the web, query a database, send an email. Code execution is different — it lets the model *compute*, compensating for weaknesses built into how LLMs work.

**Why code execution stands out:** Remember the strawberry problem from section 1? The model can't count letters in "strawberry" because it never sees individual letters — only tokens. But give the model a code execution tool, and it writes `'strawberry'.count('r')` — correct, every time. You can often trigger this simply by asking the model to "use code." The model didn't get smarter. It got a calculator. The same applies to arithmetic, date calculations, sorting, and anything else where precise computation beats pattern matching. This is why the *same model* gives better answers in a product that has code execution than in one that doesn't.

There's a second reason code execution matters. Ask an LLM to perform a task — say, extract data from a document — and run it 100 times. You'll get dozens of slightly different results, some with small variations, some with large ones. Now ask the LLM to write a small program that performs the same task, and run *that* 100 times. The results are identical every time. Code execution lets the model move from probabilistic to deterministic — from "roughly right, differently each time" to "exactly right, every time."


Tool integrations are increasingly standardized through protocols like **MCP (Model Context Protocol)**, which aim to make tools portable across different AI systems — define the tool once, use it with any model.
