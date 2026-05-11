---
name: slovenian-language-advisor
description: Answer Slovenian grammar and orthography questions from the local SP2001 and Toporišič corpus while maintaining the persistent LLM Wiki.
---

# Slovenian language advisor skill

Use this skill when the task asks about Slovenian spelling, grammar, punctuation, capitalization, inflection, syntax, language varieties, terminology, or student-facing language explanations.

## Workflow

1. Read `AGENTS.md` and `wiki/index.md`.
2. Search the existing wiki with `python tools/wiki_search.py "<query>"`.
3. Search the local source index with `python tools/search.py "<query>"`.
4. Build a context pack with `python tools/context.py "<query>"`.
5. Read the cited Markdown pages, not just snippets, when the answer will be consequential.
6. Route the answer:
   - Normative pravopis: SP 2001 first.
   - Grammatical explanation: Toporišič first.
   - Mixed question: give the practical rule first, then the grammar explanation.
7. Cite page numbers and Markdown paths.
8. For recurring or durable answers, update `wiki/` and append `wiki/log.md`.

## Answer shape

- Begin with the direct answer.
- Add a compact explanation.
- Add 1–4 citations.
- Add a caveat only if the text layer is flagged or the corpus is not decisive.

## Guardrails

Do not claim that a rule is in Jezikovna svetovalnica unless that source has been ingested. Do not silently modernize rules beyond the local corpus.
