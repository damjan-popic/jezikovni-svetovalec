#!/usr/bin/env python3
"""Future Jezikovna svetovalnica ingestion stub.

Intended fields per advisory article:
- advisory_id
- title
- question
- answer
- tags
- url
- published_or_updated_date, if available
- retrieved_at
- citation_path

Do not scrape aggressively. Respect robots.txt, rate limits, copyright, and institutional terms.
After ingestion, convert each advisory to Markdown in data/corpus/pages/jezikovna_svetovalnica/ and rebuild the FTS index.
"""

if __name__ == "__main__":
    print("Stub only. Implement after you decide on permissions and citation format.")
