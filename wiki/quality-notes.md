---
title: Quality notes
type: maintenance
status: active
last_updated: 2026-05-11
---

# Quality notes

The corpus was extracted from PDF text layers.

Known caveats:

- Some pages have OCR or font-layer noise.
- Tables, diagrams, and special characters may need manual checking against the raw PDF.
- SP 2001 had common mojibake for Slovenian letters; the extracted Markdown repairs frequent cases such as `č`, `š`, `ž`, `Č`, `Š`, `Ž`, `ć`, `đ`.
- Toporišič uses an OCR/text layer; sparse pages and front/back matter are flagged in Markdown frontmatter.

When a page has `quality_flags`, cite it cautiously and inspect the original PDF for high-stakes wording.

Useful checks:

```bash
python tools/context.py "<query>" --limit 8
python tools/search.py "<query>" --source sp2001
python tools/search.py "<query>" --source toporisic_slovnica
```
