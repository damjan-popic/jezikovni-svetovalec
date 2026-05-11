#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "index" / "search.sqlite"


def build_query(q: str, operator: str = "and") -> str:
    tokens = re.findall(r"[\wčšžćđČŠŽĆĐ]+", q, flags=re.UNICODE)
    tokens = [t for t in tokens if len(t) > 1]
    if not tokens:
        return '""'
    sep = " AND " if operator == "and" else " OR "
    return sep.join(tokens)


def search(query: str, limit: int = 10, source: str | None = None) -> list[sqlite3.Row]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    fts_query = build_query(query, "and")
    where_source = " AND source_id = ?" if source else ""
    params: list[object] = [fts_query]
    if source:
        params.append(source)
    params.append(limit)
    sql = f"""
        SELECT rowid, source_id, short_title, source_kind, page_number, path,
               snippet(pages_fts, 0, '[', ']', ' ... ', 18) AS snippet,
               bm25(pages_fts) AS rank
        FROM pages_fts
        WHERE pages_fts MATCH ?{where_source}
        ORDER BY rank
        LIMIT ?
    """
    rows = cur.execute(sql, params).fetchall()
    if not rows and len(re.findall(r"[\wčšžćđČŠŽĆĐ]+", query, flags=re.UNICODE)) > 1:
        fts_query = build_query(query, "or")
        params = [fts_query]
        if source:
            params.append(source)
        params.append(limit)
        rows = cur.execute(sql, params).fetchall()
    conn.close()
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Search the local Slovenian language corpus.")
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--source", choices=["sp2001", "toporisic_slovnica"], default=None)
    args = parser.parse_args()
    for i, row in enumerate(search(args.query, args.limit, args.source), 1):
        print(f"{i}. {row['short_title']} p. {row['page_number']} [{row['source_id']}] {row['path']}")
        print(f"   {row['snippet']}")


if __name__ == "__main__":
    main()
