---
title: Future Jezikovna svetovalnica ingestion
type: plan
status: draft
last_updated: 2026-05-11
---

# Future Jezikovna svetovalnica ingestion

Jezikovna svetovalnica can later be added as a third source layer. Treat it differently from SP 2001 and Toporišič:

- It is advisory and issue-specific.
- Preserve the original question, answer, tags, URL, and retrieval date.
- Do not let it silently override SP 2001; use it to explain current usage, edge cases, and institutional interpretation.
- Use a source ID such as `jezikovna_svetovalnica`.
- Store source pages in `data/corpus/pages/jezikovna_svetovalnica/`.
- Create `wiki/sources/jezikovna-svetovalnica.md`.
- Rebuild `data/index/search.sqlite` after ingestion.
- Update affected rule pages and record any tensions in [Contradictions and ambiguities](contradictions.md).

Do not cite it until it exists in `data/corpus/` and the index.
