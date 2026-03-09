@echo off
setlocal
cd /d "%~dp0"

set VERSION=%~1
if "%VERSION%"=="" (
  set /p VERSION=Enter version ^(example 1.0.0^): 
)

if "%VERSION%"=="" (
  echo [ERROR] Version is required.
  exit /b 1
)

echo [INFO] Building GameFix Doctor Pro version %VERSION%...
powershell -NoProfile -ExecutionPolicy Bypass -File ".\scripts\build_release.ps1" -Version "%VERSION%"
set EXIT_CODE=%ERRORLEVEL%
if not "%EXIT_CODE%"=="0" (
  echo [ERROR] Build failed with exit code %EXIT_CODE%.
  echo [TIP] Scroll up to see the exact error message.
  echo.
  pause
  exit /b %EXIT_CODE%
)

echo.
echo [OK] Build complete.
echo Check the dist folder for:
echo   GameFixDoctorPro.exe
echo   GameFixDoctorPro-%VERSION%-win-x64.zip
echo.
pause
exit /b 0
