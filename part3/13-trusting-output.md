# 13. Trusting the Output — When Confidence ≠ Correctness

LLMs always sound confident. They never say "I'm not sure" or "I made that up." This creates a specific set of risks that aren't bugs — they're features of how language models work.

### Hallucinations

LLMs sometimes generate convincing-sounding false information. They invent facts, fabricate statistics, and cite papers that don't exist. This is particularly dangerous with numbers, dates, legal references, and source citations.

Mitigations: RAG with source citations, factual cross-checks, lower temperature for factual tasks. But no mitigation is foolproof — always verify critical facts.

### Source Pressure

Ask a model "what's your source for that?" and instead of admitting it has none, it will often generate a plausible-looking citation — a real-sounding author, journal, and title that simply doesn't exist. The pressure to produce a source creates the hallucination.

### Opinions on Demand

You can get *any* opinion from an LLM. Ask "why is X a bad idea?" and you'll get compelling arguments against X. Ask "why is X brilliant?" and you'll get equally compelling arguments for X. The model isn't reasoning — it's pattern-matching to what you seem to want.

This makes it dangerously easy to use AI to validate decisions you've already made, and mistake its agreeable output for independent analysis.

### The Verification Rule

**If you can't verify the output, don't automate the task.** AI is most useful when the human can quickly check the result — reading a draft, spot-checking extracted data, reviewing a summary. The harder it is to verify, the more dangerous it is to delegate.

---
