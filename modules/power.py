"""Power optimization helper placeholder."""

from __future__ import annotations

import os
from typing import Any

from core.utils import run_command


class PowerOptimizer:
    HIGH_PERF_GUID = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
    BALANCED_GUID = "381b4222-f694-41f0-9685-ff5bb260df2e"
    POWER_SAVER_GUID = "a1841308-3541-4fab-bc81-f71556f20b4a"

    def get_current_plan(self) -> str:
        result = run_command("powercfg /getactivescheme", timeout=30)
        if not result["success"]:
            return "unknown"
        text = result["stdout"].lower()
        if "high performance" in text:
            return "high_performance"
        if "balanced" in text:
            return "balanced"
        if "power saver" in text:
            return "power_saver"
        return "custom"

    def set_high_performance(self) -> dict[str, Any]:
        return self._set_plan(self.HIGH_PERF_GUID, "High Performance")

    def set_balanced(self) -> dict[str, Any]:
        return self._set_plan(self.BALANCED_GUID, "Balanced")

    def set_power_saver(self) -> dict[str, Any]:
        return self._set_plan(self.POWER_SAVER_GUID, "Power Saver")

    def recommend(self, is_laptop: bool, on_battery: bool) -> dict[str, str]:
        if not is_laptop:
            return {"recommended": "high_performance", "reason": "Desktop gaming profile."}
        if on_battery:
            return {"recommended": "balanced", "reason": "Laptop on battery, preserve runtime."}
        return {"recommended": "high_performance", "reason": "Laptop plugged in, better gaming performance."}

    def _set_plan(self, guid: str, title: str) -> dict[str, Any]:
        if os.name != "nt":
            return {"success": False, "message": "Power plan changes are only supported on Windows."}
        result = run_command(f"powercfg /setactive {guid}", timeout=30)
        if result["success"]:
            return {"success": True, "message": f"Power plan set to {title}."}
        return {"success": False, "message": result["stderr"] or f"Failed to set {title} power plan."}
