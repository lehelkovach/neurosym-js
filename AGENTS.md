# Agent Instructions for neurosym-js

## Before working

- Read this file, the repository README, the relevant issue or task, and any more-specific
  `AGENTS.md` files in the directory tree.
- Inspect the current branch and working tree. Preserve unrelated work.
- Confirm the task's acceptance criteria, owned files, and verification commands.

## Workflow

- Use one branch or worktree per task. Keep changes small enough to review.
- Use the repository's existing conventions and dependencies before introducing new ones.
- Record active work, ownership, and acceptance criteria in the issue or task tracker.
- Record architectural decisions in `docs/decisions/` when the repository uses ADRs.
- Put implementation evidence, commands run, residual risks, and the next action in the
  pull request or task record.

## Continuity

- Use `.AGENT/RUNBOOK.md` for stable startup and verification guidance that does not
  belong in this file.
- If work must pass to another session before a pull request exists, copy
  `.AGENT/handoffs/HANDOFF-TEMPLATE.md` to a uniquely named task file.
- Never coordinate concurrent agents through one shared queue or append-only action log.
  Git branches, worktrees, issues, commits, and pull requests are the durable record.

## Safety

- Never discard unrelated changes or rewrite history without explicit authorization.
- Never print or commit credentials, tokens, personal data, or machine-local settings.
- Run the narrowest relevant checks first, then broader checks required by the repository.
- State exactly what was and was not verified.

## Repository specifics

### Purpose

- NeuroSym.js: a TypeScript library (npm name `neurosym`) for neurosymbolic inference with
  Logical Neural Networks, driven by the JSON-first NeuroJSON v0.1 schema. The repo also
  holds an optional Python KnowShowGo integration track.

### Commands

- Core library (the only thing CI runs; Node 18 in CI, `engines` requires `>=18`):
  `cd neurosym-js && npm ci`, then `npm test` (Jest), `npm run lint`, `npm run typecheck`,
  `npm run build` (tsup to `dist/`). Test (201 passing), lint, and typecheck passed
  locally; build was not run.
- `neurosym.js-standalone/` has the same npm scripts but is not covered by CI.
- Python (Poetry, Python `^3.11`, root `pyproject.toml`): `poetry install`, then
  `pytest tests`. Not run in CI; `requirements.txt` is empty, so use Poetry, not pip.
- No required environment variables were found.

### Layout

- `neurosym-js/`: primary TS package (`src/compiler/`, `src/engine/`, `src/schema/`,
  `src/adapters/`, `tests/`, `examples/`).
- `neurosym.js-standalone/`: separate copy of the package with docs, changelog, examples.
- `neurojson/`: NeuroJSON spec (`spec/`), `examples/`, and `fixtures/v0.1/`; the JS test
  `neurosym-js/tests/neurojson-fixtures.test.ts` reads these via a relative path.
- `src/knowshowgo/` and `tests/`: Python KnowShowGo modules and pytest suite.
- `packages/`: KnowShowGo sub-packages (`knowshowgo-core`, `knowshowgo-orm`,
  `knowshowgo-web`).
- `docs/`: design notes and plans (`OVERVIEW.md`, `DEVELOPMENT_PLAN.md`, KnowShowGo docs).
- `.github/workflows/ci.yml`: CI (`npm ci`, test, lint, typecheck, build in `neurosym-js/`).

### Gotchas

- `neurosym-js/src/schema/neurojson.schema.json` is currently identical to
  `neurojson/spec/neurojson.schema.json`; keep them in sync when changing the spec.
- `dist/` and `node_modules/` are build output and gitignored; do not commit them.
- Python tests fail at import without Poetry deps installed (e.g. `networkx`).
  `src/knowshowgo/arangodb_client.py` defaults to ArangoDB at `http://localhost:8529`.
- `setup-venv.ps1` and `activate-and-install.ps1` are Windows PowerShell helpers only.
