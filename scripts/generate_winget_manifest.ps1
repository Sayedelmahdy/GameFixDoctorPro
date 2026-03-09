param(
    [Parameter(Mandatory = $true)]
    [string]$PackageVersion,
    [Parameter(Mandatory = $true)]
    [string]$InstallerUrl,
    [string]$InstallerSha256 = "",
    [string]$LocalInstallerPath = "",
    [string]$PackageIdentifier = "SayedElmahdy.GameFixDoctorPro",
    [string]$Publisher = "Sayed Elmahdy",
    [string]$PackageName = "GameFix Doctor Pro",
    [string]$ShortDescription = "Windows gaming diagnosis and optimization CLI tool.",
    [string]$Description = "Professional Windows CMD tool for gaming diagnostics, optimization, repair guidance, and safe rollback workflows.",
    [string]$PublisherUrl = "https://github.com/Sayedelmahdy",
    [string]$PublisherSupportUrl = "https://github.com/Sayedelmahdy",
    [string]$PackageUrl = "https://github.com/Sayedelmahdy",
    [string]$License = "Proprietary",
    [string]$LicenseUrl = "",
    [string]$ReleaseNotesUrl = "",
    [string]$Moniker = "gamedoctor",
    [string]$Tags = "gaming;optimizer;diagnostic;windows;pc",
    [string]$NestedInstallerRelativePath = "GameFixDoctorPro.exe",
    [string]$PortableCommandAlias = "gamedoctor",
    [string]$ManifestSchemaVersion = "1.10.0",
    [string]$OutputRoot = "winget\manifests"
)

$ErrorActionPreference = "Stop"
Set-Location -Path (Resolve-Path "$PSScriptRoot\..")

function YamlQuote([string]$Value) {
    $v = [string]$Value
    $v = $v -replace "'", "''"
    return "'$v'"
}

if ([string]::IsNullOrWhiteSpace($InstallerSha256)) {
    if (-not [string]::IsNullOrWhiteSpace($LocalInstallerPath)) {
        if (-not (Test-Path $LocalInstallerPath)) {
            throw "LocalInstallerPath not found: $LocalInstallerPath"
        }
        $InstallerSha256 = (Get-FileHash -Algorithm SHA256 $LocalInstallerPath).Hash.ToUpperInvariant()
    } else {
        throw "You must provide InstallerSha256 or LocalInstallerPath."
    }
}

$InstallerSha256 = $InstallerSha256.Trim().ToUpperInvariant()
if ($InstallerSha256 -notmatch "^[A-F0-9]{64}$") {
    throw "InstallerSha256 must be a valid SHA256 hash (64 hex chars)."
}

$idParts = $PackageIdentifier.Split(".")
if ($idParts.Count -lt 2) {
    throw "PackageIdentifier must be in vendor.app format. Example: SayedElmahdy.GameFixDoctorPro"
}

$firstLetter = $idParts[0].Substring(0, 1).ToLowerInvariant()
$manifestDir = Join-Path $OutputRoot $firstLetter
foreach ($part in $idParts) {
    $manifestDir = Join-Path $manifestDir $part
}
$manifestDir = Join-Path $manifestDir $PackageVersion
New-Item -ItemType Directory -Path $manifestDir -Force | Out-Null

$versionFile = Join-Path $manifestDir "$PackageIdentifier.yaml"
$installerFile = Join-Path $manifestDir "$PackageIdentifier.installer.yaml"
$localeFile = Join-Path $manifestDir "$PackageIdentifier.locale.en-US.yaml"

$releaseDate = (Get-Date).ToString("yyyy-MM-dd")
$tagsArray = @()
if (-not [string]::IsNullOrWhiteSpace($Tags)) {
    $tagsArray = $Tags.Split(";") | ForEach-Object { $_.Trim() } | Where-Object { $_ }
}

$versionYaml = @"
# yaml-language-server: `$schema=https://aka.ms/winget-manifest.version.$ManifestSchemaVersion.schema.json
# Created with scripts/generate_winget_manifest.ps1
PackageIdentifier: $PackageIdentifier
PackageVersion: $PackageVersion
DefaultLocale: en-US
ManifestType: version
ManifestVersion: $ManifestSchemaVersion
"@

$installerYaml = @"
# yaml-language-server: `$schema=https://aka.ms/winget-manifest.installer.$ManifestSchemaVersion.schema.json
# Created with scripts/generate_winget_manifest.ps1
PackageIdentifier: $PackageIdentifier
PackageVersion: $PackageVersion
InstallerType: zip
NestedInstallerType: portable
NestedInstallerFiles:
  - RelativeFilePath: $(YamlQuote $NestedInstallerRelativePath)
    PortableCommandAlias: $(YamlQuote $PortableCommandAlias)
Installers:
  - Architecture: x64
    InstallerUrl: $(YamlQuote $InstallerUrl)
    InstallerSha256: $InstallerSha256
ReleaseDate: $releaseDate
ManifestType: installer
ManifestVersion: $ManifestSchemaVersion
"@

$localeYaml = @"
# yaml-language-server: `$schema=https://aka.ms/winget-manifest.defaultLocale.$ManifestSchemaVersion.schema.json
# Created with scripts/generate_winget_manifest.ps1
PackageIdentifier: $PackageIdentifier
PackageVersion: $PackageVersion
PackageLocale: en-US
Publisher: $(YamlQuote $Publisher)
PublisherUrl: $(YamlQuote $PublisherUrl)
PublisherSupportUrl: $(YamlQuote $PublisherSupportUrl)
Author: $(YamlQuote $Publisher)
PackageName: $(YamlQuote $PackageName)
PackageUrl: $(YamlQuote $PackageUrl)
License: $(YamlQuote $License)
"@

if (-not [string]::IsNullOrWhiteSpace($LicenseUrl)) {
    $localeYaml += "`nLicenseUrl: $(YamlQuote $LicenseUrl)"
}

$localeYaml += "`n"
$localeYaml += @"
ShortDescription: $(YamlQuote $ShortDescription)
Description: $(YamlQuote $Description)
Moniker: $(YamlQuote $Moniker)
Tags:
"@

if ($tagsArray.Count -eq 0) {
    $localeYaml += "`n  - gaming`n"
} else {
    foreach ($tag in $tagsArray) {
        $localeYaml += "`n  - $(YamlQuote $tag)"
    }
    $localeYaml += "`n"
}

if (-not [string]::IsNullOrWhiteSpace($ReleaseNotesUrl)) {
    $localeYaml += "ReleaseNotesUrl: $(YamlQuote $ReleaseNotesUrl)`n"
}

$localeYaml += @"
ManifestType: defaultLocale
ManifestVersion: $ManifestSchemaVersion
"@

Set-Content -Path $versionFile -Value $versionYaml -Encoding UTF8
Set-Content -Path $installerFile -Value $installerYaml -Encoding UTF8
Set-Content -Path $localeFile -Value $localeYaml -Encoding UTF8

Write-Host "Generated manifests:"
Write-Host "  $versionFile"
Write-Host "  $installerFile"
Write-Host "  $localeFile"
Write-Host ""
Write-Host "PackageIdentifier: $PackageIdentifier"
Write-Host "PackageVersion   : $PackageVersion"
Write-Host "InstallerSha256  : $InstallerSha256"
