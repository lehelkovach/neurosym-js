# Agent Runbook — neurosym-js

Policy lives in root `AGENTS.md`. Active work lives in an issue or PR.

## Start of a session

1. Read `AGENTS.md`, the task/PR, and (if in the +8 env)
   `osl-oc-agent/.AGENT/handoffs/CURSOR-ENV-HANDOFF.md`.
2. Inspect branch, working tree, recent commits — preserve unrelated work.
3. Confirm acceptance criteria and verification commands.
4. Resume from PR/issue evidence. Read a task-specific handoff only if one exists.

## Verify (narrow → broad)

```bash
cd neurosym-js
npm install
npm test
npm run build
npm run lint
npm run typecheck
```

Adjust to the package path the task touches (`neurosym-js/`,
`neurosym.js-standalone/`, or `neurojson/`).

## End of a session

1. Record what was and was not verified.
2. Commit coherent work; update the PR with state, blockers, next action.
3. If no PR yet and continuity is needed, copy
   `.AGENT/handoffs/HANDOFF-TEMPLATE.md` → `.AGENT/handoffs/<issue>-<task>.md`.

Do not append shared action logs or run-once queues.
