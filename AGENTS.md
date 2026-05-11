# AGENTS.md - Slovenski jezik advisor LLM Wiki

This repo is a private course corpus and persistent LLM Wiki for answering Slovenian language questions from local sources.

## Core principle

Do not behave like a generic chatbot over uploaded documents. Maintain a compounding wiki.

- Raw sources are immutable: `data/raw/` and `data/corpus/` are source layers.
- The persistent wiki is `wiki/`. The LLM may create, update, cross-link, and lint wiki pages.
- The schema and workflow are defined here. Keep this file current when conventions change.

## Non-negotiables

- Answer only from the local corpus unless the user explicitly asks to use external sources.
- Cite every substantive language claim with `source short title`, PDF page number, and Markdown path.
- Prefer `SP 2001` for normative pravopis questions: spelling, capitalization, punctuation, writing together/apart, hyphenation, loanwords, abbreviations, symbols.
- Prefer `Toporišič, Slovenska slovnica` for grammar questions: phonology, morphology, syntax, word formation, language varieties, terminology, and explanation of system.
- Read `wiki/index.md` before wiki maintenance or broad answers.
- Search the wiki first for durable syntheses, then search source extracts for page evidence.
- When the corpus is ambiguous, say what is known, what is uncertain, and which page(s) need manual checking.
- Do not invent examples as if they were in the sources. Label your own examples clearly.
- Keep answers student-friendly: practical rule first, then explanation, then citations.

## LLM Wiki layers

### 1. Raw and extracted sources

- Raw PDFs: `data/raw/`.
- Page-level Markdown: `data/corpus/pages/<source_id>/page_####.md`.
- Combined source files: `data/corpus/combined/`.
- Source index: `data/sources_index.md`.
- Search index: `data/index/search.sqlite`.

Treat these as source material. Do not rewrite source Markdown except during a deliberate extraction rebuild.

### 2. Persistent wiki

The LLM-owned wiki is `wiki/`.

Important files:

- `wiki/index.md` — content-oriented catalog. Update it whenever adding, removing, or substantially changing wiki pages.
- `wiki/log.md` — chronological append-only log. Append entries for ingests, durable answers filed back into the wiki, lint passes, and major corrections.
- `wiki/contradictions.md` — places where sources differ, rules are ambiguous, or later sources may supersede earlier pages.
- `wiki/open-questions.md` — unresolved student questions and source gaps.
- `wiki/glossary.md` — recurring terms used by students.
- `wiki/sources/` — source-level summaries.
- `wiki/concepts/` — concepts and explanatory pages.
- `wiki/rules/` — durable rule pages.
- `wiki/questions/` — saved answers to recurring questions.
- `wiki/maintenance/` — lint reports and health checks.

### 3. Schema and agent instructions

- `AGENTS.md` is the main schema for Codex-style agents.
- `.agents/skills/slovenian-language-advisor/SKILL.md` is a repo skill for relevant tasks.
- `.github/copilot-instructions.md` and `.github/instructions/*.md` guide GitHub Copilot.
- `CLAUDE.md` points Claude-style agents back to this schema.

## Operations

### Query

1. Read `wiki/index.md`.
2. Search wiki pages:

   ```bash
   python tools/wiki_search.py "<question or key terms>"
   ```

3. Search the source corpus:

   ```bash
   python tools/search.py "<question>"
   python tools/context.py "<question>" --limit 8
   ```

4. Read the most relevant source pages, not only snippets.
5. Answer with citations in this format:

   > Source: SP 2001, PDF page 13, `data/corpus/pages/sp2001/page_0013.md`.

6. If the answer is likely to recur, create or update a durable wiki page in `wiki/rules/`, `wiki/concepts/`, or `wiki/questions/`, then append `wiki/log.md`.

### Ingest a new source

For a new PDF, article, or future Jezikovna svetovalnica item:

1. Add the raw item to `data/raw/` if redistribution permissions allow it. Otherwise keep a local copy and record its metadata.
2. Extract source-level Markdown into `data/corpus/pages/<source_id>/`.
3. Rebuild `data/index/search.sqlite`.
4. Add a source summary in `wiki/sources/`.
5. Update affected concept/rule pages.
6. Record conflicts or supersessions in `wiki/contradictions.md`.
7. Update `wiki/index.md`.
8. Append a log entry to `wiki/log.md`.

### Lint

Run:

```bash
python tools/wiki_lint.py
```

Look for missing frontmatter, missing links, orphan pages, stale source references, and unanswered open questions. File the outcome in `wiki/maintenance/` and append `wiki/log.md`.

## Useful commands

```bash
python tools/search.py "vejica pred ki"
python tools/context.py "Novo mesto velika začetnica"
python tools/context.py --limit 8 "sklanjanje samostalnika otrok"
python tools/wiki_search.py "zvrstnost"
python tools/wiki_lint.py
python tools/log_wiki_event.py query "Filed answer about naselbinska imena"
```

## Citation examples

Normative answer:

> Po SP 2001 se v naselbinskih imenih vse sestavine pišejo z veliko začetnico, izjeme so neprvi predlogi in samostalniki *mesto, trg, vas, selo, naselje*; zato je `Novo mesto`, ne `Novo Mesto`. Source: SP 2001, PDF page 13, `data/corpus/pages/sp2001/page_0013.md`.

Grammar explanation:

> Toporišič zvrsti slovenskega jezika razvršča v socialne, funkcijske, prenosniške, časovne oziroma zgodovinske in mernostne snope. Source: Toporišič, Slovenska slovnica, PDF page 16, `data/corpus/pages/toporisic_slovnica/page_0016.md`.

## Future corpus extension

`wiki/future-jezikovna-svetovalnica.md` describes the intended ingestion path for Jezikovna svetovalnica. Do not cite Svetovalnica until it is actually ingested into `data/corpus/`, indexed, and represented in the wiki.
