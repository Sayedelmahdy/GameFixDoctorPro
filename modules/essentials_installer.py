"""Gaming essentials prerequisite checks and installer links."""

from __future__ import annotations

import json
import os
from typing import Any

from core.utils import run_command

try:
    import winreg  # type: ignore
except Exception:  # pragma: no cover
    winreg = None


class GamingEssentialsManager:
    """Checks gaming prerequisites and opens trusted install/download pages."""

    URLS = {
        "directx": "https://www.microsoft.com/en-us/download/details.aspx?id=35",
        "dotnet_desktop": "https://dotnet.microsoft.com/en-us/download/dotnet",
        "vc_redist": "https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist",
        "aio_runtime": "https://www.techpowerup.com/download/visual-c-redistributable-runtime-package-all-in-one/",
        "gpu_nvidia": "https://www.nvidia.com/Download/index.aspx",
        "gpu_amd": "https://www.amd.com/en/support/download/drivers.html",
        "gpu_intel": "https://www.intel.com/content/www/us/en/support/detect.html",
        "windows_update": "ms-settings:windowsupdate",
        "optional_features": "ms-settings:optionalfeatures",
        "media_feature_pack": "https://support.microsoft.com/en-us/windows/media-feature-pack-for-windows-n-8622b390-4ce6-43c9-9b42-549e5328e407",
        "openal": "https://www.openal.org/downloads/",
        "physx": "https://www.nvidia.com/en-us/drivers/physx/physx-9-21-0713-driver/",
        "vulkan_runtime": "https://vulkan.lunarg.com/",
    }

    DOTNET_RELEASE_MIN = 528040  # .NET Framework 4.8
    WINGET_VC_IDS = [
        "Microsoft.VCRedist.2015+.x64",
        "Microsoft.VCRedist.2015+.x86",
    ]
    WINGET_DOTNET_IDS = [
        "Microsoft.DotNet.DesktopRuntime.8",
        "Microsoft.DotNet.DesktopRuntime.9",
    ]
    WINGET_DIRECTX_IDS = [
        "Microsoft.DirectX",
        "Microsoft.DirectXSDK",
    ]
    WINGET_WEBVIEW2_ID = "Microsoft.EdgeWebView2Runtime"
    WINGET_PHYSX_ID = "Nvidia.PhysX"

    def __init__(self, system_info, driver_checker) -> None:
        self.system_info = system_info
        self.driver_checker = driver_checker

    def quick_startup_check(self) -> dict[str, Any]:
        checks = []
        checks.append(self.check_windows_version())
        checks.append(self.check_winget())
        checks.append(self.check_directx())
        checks.append(self.check_dotnet_framework())
        checks.append(self.check_vc_redist())
        checks.append(self.check_gpu_driver())
        optional_checks = self.optional_recommendations()

        needs_action = [c for c in checks if c.get("status") in {"WARN", "FAIL"}]
        return {
            "status": "warn" if needs_action else "ok",
            "checks": checks,
            "optional_checks": optional_checks,
            "needs_action": needs_action,
            "needs_action_count": len(needs_action),
        }

    def optional_recommendations(self) -> list[dict[str, str]]:
        checks = []
        checks.append(self.check_media_feature_pack_n())
        checks.append(self.check_directplay_feature())
        checks.append(self.check_webview2_runtime())
        checks.append(self.check_physx_runtime())
        checks.append(self.check_openal_runtime())
        checks.append(self.check_vulkan_runtime())
        return checks

    def check_winget(self) -> dict[str, str]:
        if os.name != "nt":
            return {"name": "winget", "status": "INFO", "message": "Not available on this OS.", "action": "None"}
        if self.has_winget():
            version = self._winget_version()
            return {
                "name": "winget",
                "status": "OK",
                "message": f"Available ({version})",
                "action": "None",
            }
        return {
            "name": "winget",
            "status": "WARN",
            "message": "winget is not installed or not available in PATH.",
            "action": "Use official installer pages, or install App Installer from Microsoft Store.",
        }

    def check_windows_version(self) -> dict[str, str]:
        os_info = self.system_info.get_os_info()
        release = str(os_info.get("release", "Unknown"))
        build_str = str(os_info.get("build", "0"))
        try:
            build = int(build_str)
        except Exception:
            build = 0

        if release in {"7", "8", "8.1"}:
            return {
                "name": "Windows Version",
                "status": "FAIL",
                "message": f"Windows {release} is outdated for modern games.",
                "action": "Upgrade to Windows 10/11.",
            }

        if release == "10" and build < 19041:
            return {
                "name": "Windows Version",
                "status": "WARN",
                "message": f"Windows 10 build {build} is old.",
                "action": "Run Windows Update.",
            }

        return {
            "name": "Windows Version",
            "status": "OK",
            "message": f"Windows {release} build {build_str}",
            "action": "None",
        }

    def check_directx(self) -> dict[str, str]:
        if os.name != "nt" or winreg is None:
            return {"name": "DirectX", "status": "INFO", "message": "Not available on this OS.", "action": "None"}
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\DirectX")
            version, _ = winreg.QueryValueEx(key, "Version")
            version = str(version)
        except Exception:
            version = ""

        if not version:
            return {
                "name": "DirectX",
                "status": "WARN",
                "message": "DirectX version not detected.",
                "action": "Open DirectX installer page.",
            }
        return {"name": "DirectX", "status": "OK", "message": f"Version: {version}", "action": "None"}

    def check_dotnet_framework(self) -> dict[str, str]:
        if os.name != "nt" or winreg is None:
            return {
                "name": ".NET Framework",
                "status": "INFO",
                "message": "Not available on this OS.",
                "action": "None",
            }
        release = self._get_dotnet_release_value()
        if release is None:
            return {
                "name": ".NET Framework",
                "status": "WARN",
                "message": ".NET Framework 4.x not detected.",
                "action": "Open .NET download page.",
            }
        if release < self.DOTNET_RELEASE_MIN:
            return {
                "name": ".NET Framework",
                "status": "WARN",
                "message": f"Old .NET release detected ({release}).",
                "action": "Update .NET Framework.",
            }
        return {
            "name": ".NET Framework",
            "status": "OK",
            "message": f"Release: {release}",
            "action": "None",
        }

    def check_vc_redist(self) -> dict[str, str]:
        entries = self._installed_program_names()
        patterns = (
            "microsoft visual c++ 2015",
            "microsoft visual c++ 2017",
            "microsoft visual c++ 2019",
            "microsoft visual c++ 2022",
            "microsoft visual c++ 2015-2022",
        )
        found = [name for name in entries if any(p in name.lower() for p in patterns)]
        if not found:
            return {
                "name": "VC++ Redistributables",
                "status": "WARN",
                "message": "Modern VC++ runtime not detected.",
                "action": "Install latest VC++ x64/x86 redistributables.",
            }
        return {
            "name": "VC++ Redistributables",
            "status": "OK",
            "message": f"Detected {len(found)} VC++ runtime entries.",
            "action": "None",
        }

    def check_gpu_driver(self) -> dict[str, str]:
        drivers = self.driver_checker.check()
        gpus = drivers.get("gpu", []) if isinstance(drivers, dict) else []
        if not gpus:
            return {
                "name": "GPU Driver",
                "status": "WARN",
                "message": "GPU driver information unavailable.",
                "action": "Open GPU vendor driver page.",
            }
        old = [g for g in gpus if str(g.get("driver_age_note", "")).lower().startswith(("old", "a bit old"))]
        if old:
            top = old[0]
            return {
                "name": "GPU Driver",
                "status": "WARN",
                "message": f"{top.get('name')} appears outdated ({top.get('driver_age_note')}).",
                "action": "Open vendor driver page and update.",
            }
        return {"name": "GPU Driver", "status": "OK", "message": "Driver age looks acceptable.", "action": "None"}

    def check_media_feature_pack_n(self) -> dict[str, str]:
        edition = self._windows_edition_id()
        if not edition:
            return {
                "name": "Media Feature Pack (N editions)",
                "status": "INFO",
                "message": "Edition not detected.",
                "action": "Optional: open Media Feature Pack guide if needed.",
            }
        if edition.lower().endswith("n"):
            return {
                "name": "Media Feature Pack (N editions)",
                "status": "WARN",
                "message": f"Windows edition is '{edition}' (N edition).",
                "action": "Install Media Feature Pack from Optional Features.",
            }
        return {
            "name": "Media Feature Pack (N editions)",
            "status": "OK",
            "message": f"Edition '{edition}' does not require it.",
            "action": "None",
        }

    def check_directplay_feature(self) -> dict[str, str]:
        state = self._windows_feature_state("DirectPlay")
        if not state:
            return {
                "name": "DirectPlay (legacy games)",
                "status": "INFO",
                "message": "Feature state unavailable.",
                "action": "Optional: enable for older games.",
            }
        if "enabled" in state.lower():
            return {
                "name": "DirectPlay (legacy games)",
                "status": "OK",
                "message": "Enabled.",
                "action": "None",
            }
        return {
            "name": "DirectPlay (legacy games)",
            "status": "INFO",
            "message": "Disabled.",
            "action": "Optional: enable for older DirectX-era games.",
        }

    def check_webview2_runtime(self) -> dict[str, str]:
        if self._is_program_installed("microsoft edge webview2 runtime"):
            return {
                "name": "WebView2 Runtime",
                "status": "OK",
                "message": "Installed.",
                "action": "None",
            }
        return {
            "name": "WebView2 Runtime",
            "status": "INFO",
            "message": "Not detected.",
            "action": "Optional: install for launchers/apps embedding web UI.",
        }

    def check_physx_runtime(self) -> dict[str, str]:
        vendor = self.get_primary_gpu_vendor()
        if "nvidia" not in vendor:
            return {
                "name": "NVIDIA PhysX (legacy games)",
                "status": "INFO",
                "message": "Not NVIDIA primary GPU.",
                "action": "Optional: usually not needed.",
            }
        if self._is_program_installed("physx"):
            return {
                "name": "NVIDIA PhysX (legacy games)",
                "status": "OK",
                "message": "Detected.",
                "action": "None",
            }
        return {
            "name": "NVIDIA PhysX (legacy games)",
            "status": "INFO",
            "message": "Not detected.",
            "action": "Optional: install if older PhysX titles fail to launch.",
        }

    def check_openal_runtime(self) -> dict[str, str]:
        if self._is_program_installed("openal"):
            return {
                "name": "OpenAL Runtime (legacy games)",
                "status": "OK",
                "message": "Detected.",
                "action": "None",
            }
        return {
            "name": "OpenAL Runtime (legacy games)",
            "status": "INFO",
            "message": "Not detected.",
            "action": "Optional: install if older games report OpenAL32.dll issues.",
        }

    def check_vulkan_runtime(self) -> dict[str, str]:
        if self._is_program_installed("vulkan runtime"):
            return {
                "name": "Vulkan Runtime",
                "status": "OK",
                "message": "Detected.",
                "action": "None",
            }
        return {
            "name": "Vulkan Runtime",
            "status": "INFO",
            "message": "Not clearly detected.",
            "action": "Optional: usually bundled with modern GPU drivers.",
        }

    def get_primary_gpu_vendor(self) -> str:
        info = self.system_info.get_gpu_info()
        if not info:
            return "unknown"
        return str(info[0].get("vendor", "unknown")).lower()

    def open_directx_page(self) -> dict[str, Any]:
        return self._open_url(self.URLS["directx"])

    def open_dotnet_page(self) -> dict[str, Any]:
        return self._open_url(self.URLS["dotnet_desktop"])

    def open_vc_redist_page(self) -> dict[str, Any]:
        return self._open_url(self.URLS["vc_redist"])

    def open_aio_runtime_page(self) -> dict[str, Any]:
        return self._open_url(self.URLS["aio_runtime"])

    def open_windows_update(self) -> dict[str, Any]:
        return self._open_url(self.URLS["windows_update"])

    def open_optional_features(self) -> dict[str, Any]:
        return self._open_url(self.URLS["optional_features"])

    def open_media_feature_pack_page(self) -> dict[str, Any]:
        return self._open_url(self.URLS["media_feature_pack"])

    def open_openal_page(self) -> dict[str, Any]:
        return self._open_url(self.URLS["openal"])

    def open_physx_page(self) -> dict[str, Any]:
        return self._open_url(self.URLS["physx"])

    def open_vulkan_runtime_page(self) -> dict[str, Any]:
        return self._open_url(self.URLS["vulkan_runtime"])

    def open_gpu_driver_page(self) -> dict[str, Any]:
        vendor = self.get_primary_gpu_vendor()
        if "nvidia" in vendor:
            return self._open_url(self.URLS["gpu_nvidia"])
        if "amd" in vendor or "radeon" in vendor:
            return self._open_url(self.URLS["gpu_amd"])
        if "intel" in vendor:
            return self._open_url(self.URLS["gpu_intel"])
        return {"success": False, "message": "Could not determine GPU vendor. Open manually from Driver Check."}

    def has_winget(self) -> bool:
        if os.name != "nt":
            return False
        result = run_command("winget --version", timeout=10)
        return bool(result.get("success"))

    def install_vc_redist_winget(self) -> dict[str, Any]:
        if not self.has_winget():
            return {
                "success": False,
                "message": "winget is unavailable. Open VC++ page instead.",
            }
        applied = []
        failed = []
        for pkg_id in self.WINGET_VC_IDS:
            res = self._winget_install(pkg_id)
            if res["success"]:
                applied.append(pkg_id)
            else:
                failed.append(f"{pkg_id}: {res['message']}")
        if failed and not applied:
            return {"success": False, "message": "Failed VC++ install via winget. " + " | ".join(failed)}
        if failed:
            return {
                "success": True,
                "message": (
                    "VC++ install partially completed. Installed: "
                    + ", ".join(applied)
                    + ". Failed: "
                    + " | ".join(failed)
                ),
            }
        return {"success": True, "message": "VC++ redistributables installed/updated via winget."}

    def install_dotnet_runtime_winget(self) -> dict[str, Any]:
        if not self.has_winget():
            return {"success": False, "message": "winget is unavailable. Open .NET page instead."}
        # Try package IDs in order until one succeeds.
        last_error = ""
        for pkg_id in self.WINGET_DOTNET_IDS:
            res = self._winget_install(pkg_id)
            if res["success"]:
                return {"success": True, "message": f".NET runtime installed/updated: {pkg_id}"}
            last_error = res["message"]
        return {"success": False, "message": f"Failed .NET install via winget. {last_error}"}

    def install_directx_winget(self) -> dict[str, Any]:
        if not self.has_winget():
            return {"success": False, "message": "winget is unavailable. Open DirectX page instead."}
        last_error = ""
        for pkg_id in self.WINGET_DIRECTX_IDS:
            res = self._winget_install(pkg_id)
            if res["success"]:
                return {"success": True, "message": f"DirectX package installed/updated: {pkg_id}"}
            last_error = res["message"]
        return {
            "success": False,
            "message": f"DirectX winget install failed. {last_error}",
        }

    def install_webview2_winget(self) -> dict[str, Any]:
        if not self.has_winget():
            return {"success": False, "message": "winget is unavailable. Open WebView2 page instead."}
        res = self._winget_install(self.WINGET_WEBVIEW2_ID)
        if res["success"]:
            return {"success": True, "message": "WebView2 runtime installed/updated via winget."}
        return {"success": False, "message": res["message"]}

    def install_physx_winget(self) -> dict[str, Any]:
        if not self.has_winget():
            return {"success": False, "message": "winget is unavailable. Open PhysX page instead."}
        res = self._winget_install(self.WINGET_PHYSX_ID)
        if res["success"]:
            return {"success": True, "message": "NVIDIA PhysX installed/updated via winget."}
        return {"success": False, "message": res["message"]}

    def enable_directplay(self) -> dict[str, Any]:
        if os.name != "nt":
            return {"success": False, "message": "DirectPlay enable is only available on Windows."}
        result = run_command(
            "dism /online /Enable-Feature /FeatureName:DirectPlay /All /NoRestart",
            timeout=180,
        )
        if result["success"]:
            return {"success": True, "message": "DirectPlay enabled (legacy feature). Restart may be required."}
        return {"success": False, "message": result.get("stderr") or result.get("stdout") or "Failed to enable DirectPlay."}

    def install_missing_essentials_winget(self) -> dict[str, Any]:
        """
        Install common missing essentials via winget based on current checks.
        Uses official-page fallback guidance when not possible.
        """
        report = []
        checks = self.quick_startup_check().get("checks", [])
        by_name = {row.get("name"): row for row in checks}

        if by_name.get("VC++ Redistributables", {}).get("status") in {"WARN", "FAIL"}:
            report.append(("VC++ Redistributables", self.install_vc_redist_winget()))
        if by_name.get(".NET Framework", {}).get("status") in {"WARN", "FAIL"}:
            report.append((".NET Runtime", self.install_dotnet_runtime_winget()))
        if by_name.get("DirectX", {}).get("status") in {"WARN", "FAIL"}:
            report.append(("DirectX", self.install_directx_winget()))

        if not report:
            return {"success": True, "message": "No missing essentials detected for winget install.", "report": []}

        any_success = any(item[1].get("success") for item in report)
        return {
            "success": any_success,
            "message": "Finished winget essentials batch.",
            "report": [{"item": name, **result} for name, result in report],
        }

    @staticmethod
    def _open_url(url: str) -> dict[str, Any]:
        if os.name != "nt":
            return {"success": False, "message": "Open URL action is only implemented for Windows."}
        result = run_command(f'start "" "{url}"', timeout=10)
        if result["success"]:
            return {"success": True, "message": f"Opened: {url}"}
        details = result.get("stderr") or result.get("stdout") or "Failed to open URL."
        return {"success": False, "message": details}

    def _winget_install(self, package_id: str) -> dict[str, Any]:
        command = (
            "winget install "
            f'--id "{package_id}" '
            "--exact --silent --accept-package-agreements "
            "--accept-source-agreements --disable-interactivity"
        )
        result = run_command(command, timeout=600)
        if result["success"]:
            return {"success": True, "message": f"{package_id} installed/updated."}

        stderr = (result.get("stderr") or "").lower()
        stdout = (result.get("stdout") or "").lower()
        combined = f"{stdout}\n{stderr}"
        if "no package found" in combined or "not found" in combined:
            return {"success": False, "message": f"Package not found in winget: {package_id}"}
        if "already installed" in combined or "no available upgrade found" in combined:
            return {"success": True, "message": f"{package_id} already installed/up to date."}
        return {"success": False, "message": result.get("stderr") or result.get("stdout") or "winget failed."}

    def _winget_version(self) -> str:
        result = run_command("winget --version", timeout=10)
        if result["success"] and result.get("stdout"):
            return str(result["stdout"]).strip().splitlines()[0]
        return "unknown"

    @staticmethod
    def _installed_program_names() -> list[str]:
        command = (
            'powershell -NoProfile -Command "'
            "$paths=@("
            "'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*',"
            "'HKLM:\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*',"
            "'HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*'"
            ");"
            "$items=foreach($p in $paths){Get-ItemProperty $p -ErrorAction SilentlyContinue};"
            "$items=$items | Where-Object {$_.DisplayName} | Select-Object -ExpandProperty DisplayName;"
            "$items | ConvertTo-Json -Depth 2\""
        )
        result = run_command(command, timeout=30)
        if not result["success"] or not result.get("stdout"):
            return []

        try:
            payload = json.loads(result["stdout"])
        except Exception:
            return []
        if isinstance(payload, str):
            payload = [payload]
        if not isinstance(payload, list):
            return []
        seen = set()
        output = []
        for item in payload:
            text = str(item).strip()
            key = text.lower()
            if text and key not in seen:
                seen.add(key)
                output.append(text)
        return output

    def _is_program_installed(self, keyword: str) -> bool:
        keyword = keyword.lower()
        return any(keyword in name.lower() for name in self._installed_program_names())

    @staticmethod
    def _windows_feature_state(feature_name: str) -> str:
        result = run_command(
            f"dism /online /Get-FeatureInfo /FeatureName:{feature_name}",
            timeout=60,
        )
        if not result["success"] and not result.get("stdout"):
            return ""
        text = (result.get("stdout") or "") + "\n" + (result.get("stderr") or "")
        for line in text.splitlines():
            if "State" in line:
                return line.strip()
        return ""

    @staticmethod
    def _windows_edition_id() -> str:
        if os.name != "nt" or winreg is None:
            return ""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
            )
            value, _ = winreg.QueryValueEx(key, "EditionID")
            return str(value)
        except Exception:
            return ""

    @staticmethod
    def _get_dotnet_release_value() -> int | None:
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full",
            )
            value, _ = winreg.QueryValueEx(key, "Release")
            return int(value)
        except Exception:
            return None
