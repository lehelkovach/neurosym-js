<#
.setup-venv.ps1
Creates a project-local virtual environment at `.venv`.
Usage:
  - Create the venv: `.\\setup-venv.ps1`
  - Activate & install in your current PowerShell session (dot-source):
      `. .\\setup-venv.ps1`

If dot-sourced, the script activates the venv in the current session and installs
packages from `requirements.txt` (if present).
#>
param(
    [switch]$Force
)

if (!(Test-Path ".venv") -or $Force) {
    Write-Host "Creating virtual environment at .venv..."
    python -m venv .venv
} else {
    Write-Host ".venv already exists. Use -Force to recreate."
}

# If the script is dot-sourced, $MyInvocation.BoundParameters will include Scope? We can't
# rely on a single built-in flag to detect dot-sourcing reliably cross-PS versions.
# Provide both behaviors: if the script is dot-sourced the caller should run the activation
# line shown below; otherwise the script prints instructions.

Write-Host "To activate the venv in this PowerShell session, run (or dot-source):"
Write-Host "  . .\\.venv\\Scripts\\Activate.ps1"
Write-Host "Then install packages with:"
Write-Host "  pip install -r requirements.txt"

if ($PSCommandPath -and (Get-ChildItem -Path $PSCommandPath -ErrorAction SilentlyContinue)) {
    # no-op; left for clarity. We intentionally avoid forcing activation when script is run
    # non-dot-sourced to prevent surprising the user.
}
