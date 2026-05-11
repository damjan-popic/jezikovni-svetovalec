# Wiki instructions

The persistent LLM Wiki lives in `wiki/`.

When editing wiki pages:

- Read `wiki/index.md` first.
- Keep `wiki/log.md` append-only.
- Add frontmatter with `title`, `type`, `status`, and `last_updated`.
- Link new pages from `wiki/index.md`.
- Cite the source layer for substantive claims.
- Run `python tools/wiki_lint.py` after structural changes.
