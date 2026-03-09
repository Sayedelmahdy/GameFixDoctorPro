@echo off
setlocal

where pipx >nul 2>nul
if not errorlevel 1 (
  pipx uninstall gamefix-doctor-pro >nul 2>nul
)

python -m pip uninstall -y gamefix-doctor-pro >nul 2>nul

echo [OK] Uninstall attempted for gamefix-doctor-pro.
echo If command still exists, restart CMD and run:
echo   where gamedoctor
exit /b 0
