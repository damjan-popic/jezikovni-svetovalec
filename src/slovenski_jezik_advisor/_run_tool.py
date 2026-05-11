from __future__ import annotations

import runpy
from pathlib import Path


def run_tool(script_name: str) -> None:
    root = Path(__file__).resolve().parents[2]
    script = root / "tools" / script_name
    if not script.exists():
        raise SystemExit(f"Tool script not found: {script}")
    runpy.run_path(str(script), run_name="__main__")
