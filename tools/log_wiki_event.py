#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "wiki" / "log.md"


def main() -> None:
    parser = argparse.ArgumentParser(description="Append an entry to wiki/log.md.")
    parser.add_argument("kind", help="Event kind, e.g. ingest, query, lint, amend")
    parser.add_argument("summary", help="One-line summary")
    parser.add_argument("--details", default="", help="Optional markdown details")
    args = parser.parse_args()

    today = datetime.now(timezone.utc).date().isoformat()
    entry = f"\n## [{today}] {args.kind} | {args.summary}\n\n"
    if args.details:
        entry += args.details.rstrip() + "\n"
    else:
        entry += "- Details not supplied.\n"
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(entry)
    print(f"Appended log entry to {LOG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
