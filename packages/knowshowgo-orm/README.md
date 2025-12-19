# KnowShowGo ORM (Monorepo package)

Thin client for KnowShowGo Core REST API.

## Install (dev)
```bash
poetry install
```

## Usage (MVP)
```python
from knowshowgo_orm.client import KnowShowGoClient

client = KnowShowGoClient(base_url="http://localhost:8000")
resp = client.process_instruction("At midnight, remind me to take out the trash.")
print(resp)
```
