# terminology

- application as the name for the code around the llm. is that the right term, the ideal term, the established term?
- AI: check all uses of "AI" and discuss if each is ok or not or should be replaced by "LLM" or sth else.


# more fundamental thoughts

- detetministic vs probabilistic (harness...)
- pseudocode
- ...


# what is it?

- Agentic AI systems explained.
- under the hood of agentic ai systems.
- for advanced, regular users of LLMs who have a some experience and understanding and would like to dig a little deeper and get one or two "etwaige" misconceeptions out of the way.
- ...
- why did i write this?
  - it's just the way i explain things to other people
  - and how i came to underatdn these systems after working with them for years (üi, ...)


# Todos

- resolve MN comments in 02-multimodality.md (7 comments) and 09-context-engineering.md (10 comments) — DONE
- resolve MN comments in _drafts/ (rag, security, trusting-output, routing, thinking-models — 18 comments) — DONE
- renamed "Thinking Models" → "Reasoning Models" (industry-standard term, with parenthetical note)
- future: "Diving Deeper" optional subsections (technical depth for curious readers). Content in _drafts/diving-deeper.md. May be collapsible/hidden in final format. Good for: internal mechanics, embeddings, encoding details, architecture concepts.
- title decision (see candidates below)
- consider: have security and api (and maybe other uth topics) as "horizontal" layers that go through all the sections?
- disclaimer at the end that says that AI is of course much more than what we discussed here — partially addressed in closing page, revisit
- from primer.md: should there be an "agents in practice" section covering security, the trade-off between usefulness (more access) and security (less access)?
- from part3-in-practice.md: "the more you force an LLM to create sth ('I want a reference for every bit of information you generate'), the higher the likelihood for a hallucination" — consider adding to trusting-output draft
- make illus a little wider
- ggf revise all referrences. example now: "conversation every time (§3)."

# title candidates

Subtitle candidates (from primer.md):
- Not how to build it. How to look inside it.
- Deep enough to understand. No deeper.
- For users, not builders
- Understand what you're using
- How AI actually works — just deep enough
- Not how to build it — how to understand it
- Under the hood — for everyone on the road

Title candidates (from panel):
1. "AI Primer" (no subtitle)
2. "AI Primer: From Text Box to Autonomous Agent"
3. "AI Primer: What's Actually Happening When You Use AI"
4. "AI Primer: How AI Systems Are Built, Layer by Layer"
5. "AI Primer: Nine Things You Should Know About AI"


-------------------------------------------------

# publishing platforms

- **Mintlify** — docs.anthropic.com, docs.cursor.com
- **GitBook** — docs.snyk.io, docs.rocket.chat
- Docusaurus
- https://squidfunk.github.io/mkdocs-material/
- simply github + gitbook?

- **Fumadocs** — unkey.com/docs, fumadocs.dev
- **Nextra** — langfuse.com/docs, swr.vercel.app
- **Leanpub** — leanpub.com/fljs (Kyle Simpson), leanpub.com/exploring-es6 (Axel Rauschmayer)


# where?

- gitbook
- aigot.it
- aiaiai.now, aiaiai.rocks, aiaiai.education
- aiaiai.academy, aiaiai.fit, aiaiai.guide, .aiaiai.in



# ideas for future work

- Add under the hood section
- Add glossary
- Add more sections from _drafts/, maybe split into different parts (as we had at some
  point in the past, see commit 5576fa187d186c9dadc6fb56fd0d92ed27782e3e)
- Add links to other articles? (See also research-articles.md)
- Link to https://platform.openai.com/tokenizer and/or similar tools?
