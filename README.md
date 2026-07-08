# Cross-Domain Concept Transfer Agent MVP

A lightweight MVP for extracting a problem's conceptual structure and transferring useful mechanisms from structurally similar domains.

## What it does

Input: a user problem.

Output:
1. Core question
2. Domain
3. Variables
4. Relationships
5. Abstract schema
6. Similar schemas in other domains
7. Transferred ideas
8. Verification plan

## Design

This MVP is deliberately simple and local-first. It does not require an LLM API. It uses:

- rule-based domain detection
- a reusable schema library
- keyword/structure matching
- domain-specific variable templates
- transferred-idea templates
- verification-plan templates

You can later replace individual modules with LLM calls, embeddings, graph matching, or real tool/verifier agents.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run one problem

```bash
python -m cdcta.cli "How can I improve adaptive compression by choosing different compressors for different file chunks?"
```

## Run domain test suite

```bash
python examples/run_domain_suite.py
```

## Save JSON output

```bash
python -m cdcta.cli "How can a trading system adapt when market behavior changes?" --json out.json
```

## Project layout

```text
cdcta/
  models.py          Pydantic output schema
  schema_library.py  reusable abstract schemas
  domain_knowledge.py domain variable/relation templates
  agent.py           concept-transfer pipeline
  cli.py             command-line interface
examples/
  run_domain_suite.py
  sample_outputs.json
```

## Next upgrades

1. Add an LLM adapter for richer extraction.
2. Add sentence embeddings / pgvector / FAISS for schema retrieval.
3. Add NetworkX graph matching for relationship-structure similarity.
4. Add real verifiers: compression benchmarks, trading backtests, theorem provers, simulators, etc.
5. Store verified transfer attempts and train a ranking model.
