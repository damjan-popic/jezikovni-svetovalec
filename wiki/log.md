---
title: Wiki log
type: log
status: active
last_updated: 2026-05-11
---

# Wiki log

Append-only chronological history of ingests, queries filed back into the wiki, lint passes, and source maintenance.

## [2026-05-11] amend | LLM Wiki alignment

- Checked the previous repo against the LLM Wiki pattern.
- Added top-level `wiki/` as the persistent wiki layer.
- Added `index.md`, `log.md`, source summaries, concept pages, rule-page template/examples, glossary, contradictions, open questions, and maintenance area.
- Added wiki search/lint/log/index tools.
- Added raw PDFs locally under `data/raw/` while keeping `.gitignore` protection.

## [2026-05-07] ingest | SP 2001 and Toporišič corpus

- Extracted `SP2001-4brez-zascite.pdf` into `data/corpus/pages/sp2001/`.
- Extracted `Jože Toporisic_Slovenska slovnica.pdf` into `data/corpus/pages/toporisic_slovnica/`.
- Built `data/index/search.sqlite`.
- Added source index and initial agent instructions.
