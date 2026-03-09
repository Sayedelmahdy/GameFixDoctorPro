param(
    [Parameter(Mandatory = $true)]
    [string]$Version,
    [Parameter(Mandatory = $true)]
    [string]$Repo, # owner/repo
    [string]$AssetPath = "",
    [string]$Title = "",
    [string]$Notes = ""
)

$ErrorActionPreference = "Stop"
Set-Location -Path (Resolve-Path "$PSScriptRoot\..")

function Resolve-GhExe {
    $cmd = Get-Command gh -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }

    $candidates = @(
        "$env:ProgramFiles\GitHub CLI\gh.exe",
        "$env:ProgramFiles\GitHub CLI\bin\gh.exe",
        "$env:LOCALAPPDATA\Programs\GitHub CLI\gh.exe",
        "$env:LOCALAPPDATA\Programs\GitHub CLI\bin\gh.exe",
        "$env:LOCALAPPDATA\Microsoft\WinGet\Links\gh.exe"
    )
    foreach ($p in $candidates) {
        if (Test-Path $p) { return $p }
    }
    return ""
}

$ghExe = Resolve-GhExe
if ([string]::IsNullOrWhiteSpace($ghExe)) {
    throw "GitHub CLI (gh) is not installed. Install it first: winget install --id GitHub.cli --exact"
}

try {
    & $ghExe auth status | Out-Null
}
catch {
    Write-Host "Not logged in to GitHub. Opening login..."
    & $ghExe auth login -w | Out-Host
}

if ([string]::IsNullOrWhiteSpace($Title)) {
    $Title = "v$Version"
}

if ([string]::IsNullOrWhiteSpace($AssetPath)) {
    $AssetPath = ".\dist\GameFixDoctorPro-$Version-win-x64.zip"
}

if (-not (Test-Path $AssetPath)) {
    throw "Release asset not found: $AssetPath"
}

$tag = "v$Version"

if ([string]::IsNullOrWhiteSpace($Notes)) {
    $Notes = "GameFix Doctor Pro release $tag"
}

& $ghExe release create $tag $AssetPath --repo $Repo --title $Title --notes $Notes | Out-Host
Write-Host "Release created: $tag on $Repo"
