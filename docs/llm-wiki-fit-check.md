# LLM Wiki fit check

Date: 2026-05-11

## Verdict

The previous repo was a strong **local corpus + retrieval scaffold**, but it was only partially an LLM Wiki.

It already had:

- extracted source Markdown in `data/corpus/`,
- a local SQLite FTS index,
- source-aware search/context tools,
- agent instructions,
- a few starter wiki-like notes.

It lacked or under-specified:

- a clearly separated persistent wiki root,
- `index.md` as the content-oriented wiki catalog,
- `log.md` as an append-only history,
- explicit ingest/query/lint operations,
- a strong rule that answers can be filed back into the wiki,
- source, concept, rule, contradiction, and open-question page conventions,
- local raw PDFs as the immutable source-of-truth layer.

## Amendments made

- Added top-level `wiki/` as the persistent LLM-owned wiki.
- Added `wiki/index.md` and `wiki/log.md`.
- Added source pages, concept pages, starter rule pages, glossary, contradictions, open questions, and maintenance area.
- Expanded `AGENTS.md` into a full operating schema.
- Added `CLAUDE.md` for Claude-style agents.
- Updated GitHub Copilot instructions for the wiki workflow.
- Added `tools/wiki_search.py`, `tools/wiki_lint.py`, `tools/log_wiki_event.py`, and `tools/update_wiki_index.py`.
- Included the raw PDFs in `data/raw/` for local source checking; `.gitignore` still protects them from accidental Git commits.
- Copied the attached LLM Wiki idea file to `docs/reference/llm-wiki.md`.

## Practical status

The repo is now suitable as a course-local LLM Wiki for SP 2001 and Toporišič. It is still intentionally conservative: the wiki starts small, and agents should grow it by filing recurring answers and updating concept/rule pages as students ask questions.
