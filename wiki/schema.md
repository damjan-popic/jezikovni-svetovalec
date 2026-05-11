---
title: Schema and workflow
type: schema
status: active
last_updated: 2026-05-11
---

# Schema and workflow

This page summarizes the LLM Wiki conventions for this repo. `AGENTS.md` is the operational source of truth; this page is the human-readable wiki copy.

## Page types

Use these `type` values in frontmatter:

- `index` — navigation and catalog pages.
- `log` — append-only chronological logs.
- `source` — source-level summaries.
- `concept` — grammar/orthography concepts.
- `rule` — student-facing durable rule pages.
- `question` — saved answer pages.
- `glossary` — terminology.
- `maintenance` — lint reports and health checks.
- `plan` — future ingestion or workflow plans.

## Required frontmatter

```yaml
---
title: Page title
type: concept
status: draft|active|needs_check|archived
last_updated: YYYY-MM-DD
sources:
  - sp2001
  - toporisic_slovnica
---
```

## Citation discipline

Every durable claim about Slovenian usage should cite the source layer, not only another wiki page.

Preferred citation shape:

> Source: SP 2001, PDF page 13, `data/corpus/pages/sp2001/page_0013.md`.

## Query workflow

1. Read [Wiki index](index.md).
2. Search the wiki with `python tools/wiki_search.py "..."`.
3. Search the corpus with `python tools/search.py "..."`.
4. Build a context pack with `python tools/context.py "..."`.
5. Answer with citations.
6. File durable answers into `wiki/rules/`, `wiki/concepts/`, or `wiki/questions/`.
7. Append [Wiki log](log.md).

## Ingest workflow

1. Add the raw source to `data/raw/` if permissions allow.
2. Extract to `data/corpus/pages/<source_id>/`.
3. Rebuild `data/index/search.sqlite`.
4. Add a `wiki/sources/<source_id>.md` page.
5. Update affected concept/rule pages.
6. Record tensions in [Contradictions and ambiguities](contradictions.md).
7. Update [Wiki index](index.md) and [Wiki log](log.md).

## Lint workflow

Run `python tools/wiki_lint.py`. Fix missing frontmatter, missing links, and stale index entries. Record major passes in `wiki/maintenance/` and `wiki/log.md`.
