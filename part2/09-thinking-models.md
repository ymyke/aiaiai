# 9. Thinking Models — The Inner Monologue

```
  Classic LLM:                       Thinking Model:

  "Should I buy or rent?"            "Should I buy or rent?"
           │                                    │
           ▼                                    ▼
    ┌─────────────┐                      ┌─────────────┐
    │     LLM     │                      │     LLM     │
    └─────────────┘                      │  ┌────────────────────┐
           │                             │  │ Thinking (hidden)  │
           ▼                             │  │ "Rent is $1,800/mo │
    Direct answer                        │  │  Buying: $2,700/mo │
                                         │  │  But equity..."    │
                                         │  └────────────────────┘
                                         └─────────────┘
                                                │
                                                ▼
                                         Answer (visible)
```

Classic LLMs generate the answer directly. **Thinking Models** have a reasoning step *before* the actual answer.

The idea started as a simple prompt trick (2022): write "Think step by step" and the model outputs its reasoning as normal text. Same model, just a cleverer prompt.

The current generation (Claude with Extended Thinking, OpenAI's o1/o3) is fundamentally different: these models were trained through reinforcement learning to reason *before* answering. The ability to think is baked into the model weights. The thinking tokens go into a separate block that's normally hidden from the user.

**When thinking helps:** Complex logic, math, multi-step analysis, code debugging. For simple questions, it's overkill — slower and more expensive.

**Why is this in "What the Model Sees"?** Thinking started as a prompting technique — literally adding "think step by step" to what the model sees. Today it's baked into the model itself, but the trade-off is still about the context window: thinking tokens consume space that could go to other information.

---
