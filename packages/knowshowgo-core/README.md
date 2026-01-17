# KnowShowGo Core (Monorepo package)

REST-first service exposing KnowShowGo primitives (prototypes, nodes, associations) with working-memory reinforcement and long-term replication hooks.

## Run (dev)
```bash
poetry install
poetry run uvicorn knowshowgo_core.app:app --reload --port 8000
```

## Endpoints (MVP)
- `GET /health` — service status
- `POST /instructions` — process a natural-language instruction, create prototype/instance, reinforce working memory.

GraphQL can be added later if needed.
