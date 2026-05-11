from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]


def test_index_exists_and_has_two_sources():
    db = ROOT / "data" / "index" / "search.sqlite"
    assert db.exists()
    conn = sqlite3.connect(db)
    rows = conn.execute("SELECT source_id, COUNT(*) FROM pages GROUP BY source_id").fetchall()
    conn.close()
    counts = dict(rows)
    assert counts.get("sp2001", 0) >= 250
    assert counts.get("toporisic_slovnica", 0) >= 900


def test_markdown_pages_exist():
    assert (ROOT / "data" / "corpus" / "pages" / "sp2001" / "page_0009.md").exists()
    assert (ROOT / "data" / "corpus" / "pages" / "toporisic_slovnica" / "page_0016.md").exists()


def test_search_finds_vejica_or_zacetnica():
    conn = sqlite3.connect(ROOT / "data" / "index" / "search.sqlite")
    n = conn.execute("SELECT COUNT(*) FROM pages_fts WHERE pages_fts MATCH 'vejica OR začetnica'").fetchone()[0]
    conn.close()
    assert n > 0


def test_llm_wiki_core_files_exist():
    assert (ROOT / "wiki" / "index.md").exists()
    assert (ROOT / "wiki" / "log.md").exists()
    assert (ROOT / "wiki" / "sources" / "sp2001.md").exists()
    assert (ROOT / "wiki" / "sources" / "toporisic-slovnica.md").exists()
    assert (ROOT / "AGENTS.md").read_text(encoding="utf-8").count("LLM Wiki") >= 1


def test_raw_source_readme_and_local_pdfs_present_in_bundle():
    assert (ROOT / "data" / "raw" / "README.md").exists()
    # The amended zip keeps the raw PDFs available for local source-of-truth checks.
    assert (ROOT / "data" / "raw" / "SP2001-4brez-zascite.pdf").exists()
    assert (ROOT / "data" / "raw" / "Jože Toporisic_Slovenska slovnica.pdf").exists()


def test_wiki_lint_script_runs():
    import subprocess
    result = subprocess.run(["python", str(ROOT / "tools" / "wiki_lint.py")], cwd=ROOT, text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
