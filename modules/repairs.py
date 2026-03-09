"""Repair and optimization actions."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

from core.utils import run_command


class RepairCenter:
    """Runs supported repairs using safe wrappers."""

    def __init__(self, system_info) -> None:
        self.system_info = system_info

    def run_sfc(self) -> dict[str, Any]:
        result = run_command("sfc /scannow", timeout=3600)
        if result["success"]:
            return {"success": True, "message": "System File Checker completed."}
        return {"success": False, "message": result["stderr"] or "SFC failed."}

    def run_dism(self) -> dict[str, Any]:
        result = run_command("DISM /Online /Cleanup-Image /RestoreHealth", timeout=3600)
        if result["success"]:
            return {"success": True, "message": "DISM restore completed."}
        return {"success": False, "message": result["stderr"] or "DISM failed."}

    def clear_temp_files(self) -> dict[str, Any]:
        total_deleted = 0
        paths = [os.getenv("TEMP", ""), r"C:\Windows\Temp"]
        for root in paths:
            if not root:
                continue
            total_deleted += self._clear_directory(Path(root))
        return {
            "success": True,
            "message": f"Cleared temporary files ({total_deleted} files removed).",
        }

    def flush_dns(self) -> dict[str, Any]:
        result = run_command("ipconfig /flushdns", timeout=30)
        if result["success"]:
            return {"success": True, "message": "DNS cache flushed."}
        return {"success": False, "message": result["stderr"] or "DNS flush failed."}

    def set_high_performance_power(self) -> dict[str, Any]:
        cmd = "powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
        result = run_command(cmd, timeout=30)
        if result["success"]:
            return {"success": True, "message": "Power plan set to High Performance."}
        return {"success": False, "message": result["stderr"] or "Could not set power plan."}

    def enable_game_mode(self) -> dict[str, Any]:
        if os.name != "nt":
            return {"success": False, "message": "Game Mode is only available on Windows."}
        try:
            import winreg

            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\GameBar")
            winreg.SetValueEx(key, "AllowAutoGameMode", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
            return {"success": True, "message": "Game Mode enabled."}
        except Exception as exc:
            return {"success": False, "message": f"Failed to enable Game Mode: {exc}"}

    def _clear_directory(self, path: Path) -> int:
        if not path.exists():
            return 0
        removed = 0
        for item in path.iterdir():
            try:
                if item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                else:
                    item.unlink(missing_ok=True)
                removed += 1
            except Exception:
                continue
        return removed

