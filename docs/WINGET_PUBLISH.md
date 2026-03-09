# Winget Publish Guide

This project is ready for winget publishing with package id:

`SayedElmahdy.GameFixDoctorPro`

## One-time setup

1. Create a GitHub repository for this project.
2. Ensure releases are enabled on the repo.
3. Install tools:
   - Python 3.10+
   - `winget` (on Windows 10/11)
   - `gh` GitHub CLI
   - `wingetcreate` (optional, auto-installed by script)
4. Login to GitHub once:
   ```powershell
   gh auth login -w
   ```
5. Optional: You can still use a GitHub token (`GITHUB_TOKEN`) if preferred.

## Release + winget publish

1. Build release artifact (EXE + zip):
   ```powershell
   .\scripts\build_release.ps1 -Version 1.0.0
   ```
2. Create GitHub release automatically:
   ```powershell
   .\scripts\create_github_release.ps1 `
     -Version 1.0.0 `
     -Repo "<OWNER>/<REPO>"
   ```
3. Submit winget package:
   ```powershell
   .\scripts\publish_winget.ps1 `
     -PackageVersion 1.0.0 `
     -InstallerUrl "https://github.com/<OWNER>/<REPO>/releases/download/v1.0.0/GameFixDoctorPro-1.0.0-win-x64.zip" `
     -LocalInstallerPath ".\dist\GameFixDoctorPro-1.0.0-win-x64.zip" `
     -Submit
   ```

## If you only want manifests (no submit)

```powershell
.\scripts\publish_winget.ps1 `
  -PackageVersion 1.0.0 `
  -InstallerUrl "https://github.com/<OWNER>/<REPO>/releases/download/v1.0.0/GameFixDoctorPro-1.0.0-win-x64.zip" `
  -LocalInstallerPath ".\dist\GameFixDoctorPro-1.0.0-win-x64.zip"
```

Generated files:

- `winget\manifests\s\SayedElmahdy\GameFixDoctorPro\1.0.0\SayedElmahdy.GameFixDoctorPro.yaml`
- `winget\manifests\s\SayedElmahdy\GameFixDoctorPro\1.0.0\SayedElmahdy.GameFixDoctorPro.installer.yaml`
- `winget\manifests\s\SayedElmahdy\GameFixDoctorPro\1.0.0\SayedElmahdy.GameFixDoctorPro.locale.en-US.yaml`

## Notes

- Winget package approval is done by Microsoft community review in `microsoft/winget-pkgs`.
- If package does not exist yet, script tries `wingetcreate new`.
- If package exists, script tries `wingetcreate update`.
- Keep `PackageVersion` exactly matching release file and URL.
