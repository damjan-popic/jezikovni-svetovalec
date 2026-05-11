#!/usr/bin/env python3
"""Placeholder extractor.

The delivered repo already contains Markdown and a SQLite index. This file documents the extraction
strategy used to build the bundle: PyMuPDF text-layer extraction, SP2001 mojibake repair, page-level
Markdown, then SQLite FTS5 indexing.

For a full re-run, keep the generator from the original build or adapt this script to your local needs.
"""
from pathlib import Path

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    print("This repo was pre-extracted. Put PDFs in data/raw/ if you want to rebuild.")
    print(f"Corpus pages: {root / 'data' / 'corpus' / 'pages'}")
    print(f"Index: {root / 'data' / 'index' / 'search.sqlite'}")
