param(
    [Parameter(Mandatory = $true)]
    [string]$Version,
    [string]$PythonExe = "python",
    [string]$ExeName = "GameFixDoctorPro"
)

$ErrorActionPreference = "Stop"
Set-Location -Path (Resolve-Path "$PSScriptRoot\..")

Write-Host "[1/5] Installing build tools..."
& $PythonExe -m pip install --upgrade pip pyinstaller | Out-Host

Write-Host "[2/5] Cleaning old build artifacts..."
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "$ExeName.spec") { Remove-Item -Force "$ExeName.spec" }

Write-Host "[3/5] Building executable..."
& $PythonExe -m PyInstaller --noconfirm --clean --onefile --console --name $ExeName gamefix_doctor.py | Out-Host

$exePath = Join-Path (Resolve-Path "dist").Path "$ExeName.exe"
if (-not (Test-Path $exePath)) {
    throw "Build failed. Missing file: $exePath"
}

$zipName = "$ExeName-$Version-win-x64.zip"
$zipPath = Join-Path (Resolve-Path "dist").Path $zipName
if (Test-Path $zipPath) { Remove-Item -Force $zipPath }

Write-Host "[4/5] Creating release zip..."
Compress-Archive -Path $exePath -DestinationPath $zipPath -Force

Write-Host "[5/5] Computing SHA256..."
$hash = (Get-FileHash -Algorithm SHA256 $zipPath).Hash.ToUpperInvariant()

Write-Host ""
Write-Host "Release artifact created:"
Write-Host "  $zipPath"
Write-Host "SHA256:"
Write-Host "  $hash"

