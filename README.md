# osl-agent

Quick setup for Python dev in this repo (virtualenv + Poetry + requirements)

Steps provided below create a project-local virtual environment at `.venv`, show how
to activate it in PowerShell, and how to use Poetry for dependency management.

Files added:
- `pyproject.toml` (Poetry project metadata)
- `requirements.txt` (pip-friendly, can be exported from Poetry)
- `.gitignore` (excludes `.venv` and caches)
- `setup-venv.ps1` (creates `.venv` and shows activation instructions)
- `activate-and-install.ps1` (activates `.venv` and installs `requirements.txt` — dot-source to persist activation)

Quick commands (PowerShell):

1) Create venv (script creates `.venv`):

```powershell
.\setup-venv.ps1
```

2) Activate venv in the current PowerShell session and install requirements (dot-source):

```powershell
. .\activate-and-install.ps1
```

3) If you prefer Poetry for dependency management (recommended):

```powershell
# Configure Poetry to create in-project virtualenvs (optional)
poetry config virtualenvs.in-project true --local
# Install dependencies from pyproject.toml, creating .venv
poetry install
# Export requirements.txt if you need pip-format file
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

Notes:
- To persist the virtualenv activation in your current session use the dot (`.`) before the script path (dot-source).
- CI should use `pip install -r requirements.txt` or `poetry install` with `--no-interaction` and `--no-ansi` as appropriate.

