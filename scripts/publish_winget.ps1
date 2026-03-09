param(
    [Parameter(Mandatory = $true)]
    [string]$PackageVersion,
    [Parameter(Mandatory = $true)]
    [string]$InstallerUrl,
    [string]$InstallerSha256 = "",
    [string]$LocalInstallerPath = "",
    [string]$PackageIdentifier = "SayedElmahdy.GameFixDoctorPro",
    [string]$GitHubToken = $env:GITHUB_TOKEN,
    [switch]$Submit
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

function Resolve-WingetCreateExe {
    $cmd = Get-Command wingetcreate -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }

    $candidates = @(
        "$env:LOCALAPPDATA\Microsoft\WindowsApps\wingetcreate.exe",
        "$env:ProgramFiles\WindowsApps\wingetcreate.exe"
    )
    foreach ($p in $candidates) {
        if (Test-Path $p) { return $p }
    }
    return ""
}

function Invoke-WingetCreateNew {
    param(
        [string]$WingetCreateExe,
        [string]$PackageIdentifier,
        [string]$InstallerUrl,
        [string]$GitHubToken
    )

    # wingetcreate versions differ. Try token-based then interactive fallback.
    $attempts = @()
    if (-not [string]::IsNullOrWhiteSpace($GitHubToken)) {
        $attempts += ,@("new", "--token", $GitHubToken, $InstallerUrl)
    }
    $attempts += ,@("new", $InstallerUrl)

    foreach ($args in $attempts) {
        $displayArgs = @()
        for ($i = 0; $i -lt $args.Count; $i++) {
            if ($args[$i] -eq "--token" -and ($i + 1) -lt $args.Count) {
                $displayArgs += "--token"
                $displayArgs += "***REDACTED***"
                $i++
                continue
            }
            $displayArgs += $args[$i]
        }
        Write-Host "Trying: wingetcreate $($displayArgs -join ' ')"
        & $WingetCreateExe @args | Out-Host
        if ($LASTEXITCODE -eq 0) {
            return $true
        }
    }
    return $false
}

function Test-InstallerUrlReachable {
    param([string]$Url)
    try {
        $response = Invoke-WebRequest -Uri $Url -Method Head -MaximumRedirection 10 -ErrorAction Stop
        if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 400) {
            return $true
        }
    }
    catch {
        return $false
    }
    return $false
}

Write-Host "[1/3] Generating manifests..."
& "$PSScriptRoot\generate_winget_manifest.ps1" `
    -PackageVersion $PackageVersion `
    -InstallerUrl $InstallerUrl `
    -InstallerSha256 $InstallerSha256 `
    -LocalInstallerPath $LocalInstallerPath `
    -PackageIdentifier $PackageIdentifier

$idParts = $PackageIdentifier.Split(".")
$firstLetter = $idParts[0].Substring(0, 1).ToLowerInvariant()
$manifestDir = Join-Path "winget\manifests" $firstLetter
foreach ($part in $idParts) {
    $manifestDir = Join-Path $manifestDir $part
}
$manifestDir = Join-Path $manifestDir $PackageVersion
$versionManifest = Join-Path $manifestDir "$PackageIdentifier.yaml"

Write-Host "[2/3] Validating manifests..."
if (Get-Command winget -ErrorAction SilentlyContinue) {
    $validateOutput = & winget validate --manifest $manifestDir 2>&1
    $validateOutput | Out-Host
    $validateText = ($validateOutput | Out-String)
    if ($validateText -match "(?i)manifest validation failed|manifest error|^\s*error:" -or $LASTEXITCODE -gt 1) {
        throw "Manifest validation failed. Fix errors above, then run publish again."
    }
} else {
    Write-Host "winget command not found. Skipping local validate."
}

if (-not $Submit) {
    Write-Host "[3/3] Submit skipped. Manifests are ready at:"
    Write-Host "  $manifestDir"
    Write-Host ""
    Write-Host "To submit manually:"
    Write-Host "  wingetcreate new $PackageIdentifier --urls $InstallerUrl --version $PackageVersion --token <GITHUB_PAT> --submit"
    exit 0
}

if ([string]::IsNullOrWhiteSpace($GitHubToken)) {
    $ghExe = Resolve-GhExe
    if (-not [string]::IsNullOrWhiteSpace($ghExe)) {
        try {
            $GitHubToken = (& $ghExe auth token).Trim()
        }
        catch {
            $GitHubToken = ""
        }
    }
}

Write-Host "[3/3] Submitting to winget-pkgs with wingetcreate..."
if (-not (Resolve-WingetCreateExe)) {
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Write-Host "wingetcreate not found. Installing..."
        & winget install --id Microsoft.WingetCreate --exact --accept-package-agreements --accept-source-agreements | Out-Host
    } else {
        throw "wingetcreate not found and winget is not available to install it."
    }
}

$wingetCreateExe = Resolve-WingetCreateExe
if (-not $wingetCreateExe) {
    throw "wingetcreate is still not available. Open a new terminal and retry."
}

if (-not (Test-InstallerUrlReachable -Url $InstallerUrl)) {
    throw "InstallerUrl is not reachable (HTTP 404/403/etc). Open the URL in browser and copy the exact asset link from GitHub release."
}

$updateArgs = @("update", $PackageIdentifier, "--urls", $InstallerUrl, "--version", $PackageVersion, "--submit")
if (-not [string]::IsNullOrWhiteSpace($GitHubToken)) {
    $updateArgs += @("--token", $GitHubToken)
}
& $wingetCreateExe @updateArgs | Out-Host
if ($LASTEXITCODE -ne 0) {
    Write-Host "Update failed or package does not exist yet. Trying new..."
    Write-Host "Note: first publish may open interactive prompts in wingetcreate."
    $created = Invoke-WingetCreateNew -WingetCreateExe $wingetCreateExe -PackageIdentifier $PackageIdentifier -InstallerUrl $InstallerUrl -GitHubToken $GitHubToken
    if (-not $created) {
        throw "wingetcreate new failed. Check errors above."
    }
}

Write-Host "Done. Check your GitHub notifications for the winget-pkgs PR."
