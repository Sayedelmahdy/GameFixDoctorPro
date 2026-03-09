@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python is not installed or not in PATH.
  echo Install Python 3.10+ first, then run this file again.
  exit /b 1
)

echo [INFO] Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
  echo [WARN] Could not upgrade pip. Continuing...
)

echo [INFO] Installing build tools (setuptools, wheel)...
python -m pip install --upgrade setuptools wheel
if errorlevel 1 (
  echo [WARN] Could not install setuptools/wheel globally. Trying user mode...
  python -m pip install --user --upgrade setuptools wheel
)

where pipx >nul 2>nul
if not errorlevel 1 (
  echo [INFO] Installing with pipx (isolated, recommended)...
  pipx install --force .
  if errorlevel 1 (
    echo [ERROR] pipx install failed.
    exit /b 1
  )
) else (
  echo [INFO] pipx not found, installing with pip --user...
  python -m pip install --user --upgrade --no-build-isolation .
  if errorlevel 1 (
    echo [ERROR] pip install failed.
    exit /b 1
  )
)

echo.
echo [OK] GameFix Doctor Pro installed.
echo Open a NEW CMD window, then run:
echo   gamedoctor
exit /b 0
