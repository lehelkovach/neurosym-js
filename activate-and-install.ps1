<#
activate-and-install.ps1
Activate the project venv and install requirements. To load into your current session and
keep the venv active, dot-source this file:

  . .\activate-and-install.ps1

If you run it normally (not dot-sourced), activation will occur in the child process and
will not persist in your interactive session — prefer dot-sourcing when you want the
prompt switched to the venv in your current terminal.
#>

if (!(Test-Path ".venv")) {
    Write-Host ".venv not found, creating..."
    python -m venv .venv
}

Write-Host "Activating .venv..."
. .\.venv\Scripts\Activate.ps1

Write-Host "Upgrading pip and installing from requirements.txt if present..."
python -m pip install --upgrade pip
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
} else {
    Write-Host "No requirements.txt found. If you use Poetry, run: poetry install"
}
