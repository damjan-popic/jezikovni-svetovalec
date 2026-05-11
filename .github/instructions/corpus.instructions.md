# Corpus instructions

The corpus source layer lives in:

- `data/raw/` for PDFs,
- `data/corpus/pages/` for page-level Markdown,
- `data/index/search.sqlite` for FTS search.

For language answers:

- Search the corpus before answering.
- Cite PDF page and Markdown path.
- Prefer `SP 2001` for normative pravopis.
- Prefer `Toporišič` for grammar and linguistic explanation.
- Do not modify extracted source pages unless doing a deliberate extraction rebuild.
