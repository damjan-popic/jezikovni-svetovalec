# Raw PDF location

This folder is the immutable raw-source layer for the LLM Wiki.

Included in this local zip:

- `SP2001-4brez-zascite.pdf`
- `Jože Toporisic_Slovenska slovnica.pdf`

The raw PDFs are source-of-truth material for manual checking when an extracted page has noise or when an answer is consequential.

`.gitignore` prevents accidental Git commits of PDFs. For a private course repository, add them only if your permissions allow it:

```bash
git add -f data/raw/SP2001-4brez-zascite.pdf "data/raw/Jože Toporisic_Slovenska slovnica.pdf"
```

If you remove the PDFs before pushing, keep this README and place local copies here whenever you need to re-run extraction or visually verify a passage.
