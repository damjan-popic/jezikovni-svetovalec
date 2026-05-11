# Copilot custom instructions

This repository answers Slovenian language questions using the local corpus and maintains a persistent LLM Wiki.

When generating answers or code:

- Read `AGENTS.md` for the main workflow.
- Search `wiki/index.md` and existing wiki pages before answering broad or recurring language questions.
- Search the local corpus with `python tools/search.py "..."` and `python tools/context.py "..."` before making language claims.
- Cite `SP 2001` and/or `Toporišič, Slovenska slovnica` with PDF page and Markdown path.
- Prefer `SP 2001` for normative orthography and punctuation.
- Prefer `Toporišič` for grammar, syntax, morphology, word formation, and language-system explanations.
- When an answer is durable, update or create a page under `wiki/` and append `wiki/log.md`.
- Keep the corpus private. Do not add raw PDFs to Git unless the repository is private and permissions allow it.
