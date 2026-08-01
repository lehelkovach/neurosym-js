# AGENTS.md

Canonical instructions for coding agents working in `neurosym-js`.

## Continuity (v2)

- **Policy:** this file. **Ops loop:** [`.AGENT/RUNBOOK.md`](.AGENT/RUNBOOK.md).
- **Cross-repo env:** `osl-oc-agent/.AGENT/handoffs/CURSOR-ENV-HANDOFF.md` (secret *names* only).
- **Handoffs:** copy [`.AGENT/handoffs/HANDOFF-TEMPLATE.md`](.AGENT/handoffs/HANDOFF-TEMPLATE.md) to a uniquely named task file only when state must cross sessions before a PR exists.
- **Do not** append `.AGENT/agent-action-log.md` or use run-once queues — archived under `.AGENT/archive/v1/`. Use issues, commits, and PRs.
- Template source: sibling `agent-repo-boilerplate` (`main`). Re-sync: `python3 ../agent-repo-boilerplate/scripts/apply_template.py .` (dry-run) then `--apply`.
- Gitflow: this tip uses **`main`** as the integration branch (no `dev` yet). Branch from **`main`**, PR into **`main`**.

## Repo role

NeuroSym.js: a zero-dependency JS/TS library for neurosymbolic AI (Logical Neural
Networks) with a JSON-first "NeuroJSON" schema (code as data).

## Commands

Authoritative commands live in `README.md` / package manifests. Common path for
the core library:

```bash
cd neurosym-js
npm install
npm test
npm run build
npm run lint
npm run typecheck
```

## Safety

- Never commit secret values; secrets are injected as env vars.
- Prefer editing existing files; keep changes reviewable.
- State exactly what was and was not verified.
