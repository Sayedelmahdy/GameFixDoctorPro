"""Driver health check."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any

try:
    import wmi  # type: ignore

    HAS_WMI = True
except Exception:
    HAS_WMI = False


class DriverChecker:
    """Collects key driver information for GPU/audio/network."""

    def __init__(self) -> None:
        self._wmi = wmi.WMI() if HAS_WMI and os.name == "nt" else None

    def check(self) -> dict[str, Any]:
        if not self._wmi:
            return {"status": "warn", "message": "WMI is unavailable.", "gpu": [], "audio": [], "network": []}
        return {
            "status": "ok",
            "gpu": self._gpu_drivers(),
            "audio": self._pnp_by_class("MEDIA", max_items=8),
            "network": self._pnp_by_class("NET", max_items=8),
        }

    def _gpu_drivers(self) -> list[dict]:
        rows = []
        try:
            for gpu in self._wmi.Win32_VideoController():
                rows.append(
                    {
                        "name": str(gpu.Name or "Unknown"),
                        "driver_version": str(gpu.DriverVersion or "Unknown"),
                        "driver_date": self._normalize_wmi_date(str(gpu.DriverDate or "")),
                        "driver_age_note": self._age_note(str(gpu.DriverDate or "")),
                    }
                )
        except Exception:
            return []
        return rows

    def _pnp_by_class(self, device_class: str, max_items: int = 6) -> list[dict]:
        rows = []
        try:
            for item in self._wmi.Win32_PnPSignedDriver(DeviceClass=device_class):
                rows.append(
                    {
                        "device_name": str(item.DeviceName or "Unknown"),
                        "driver_version": str(item.DriverVersion or "Unknown"),
                        "driver_date": self._normalize_wmi_date(str(item.DriverDate or "")),
                    }
                )
                if len(rows) >= max_items:
                    break
        except Exception:
            return []
        return rows

    @staticmethod
    def _normalize_wmi_date(raw: str) -> str:
        if len(raw) >= 8 and raw[:8].isdigit():
            return f"{raw[0:4]}-{raw[4:6]}-{raw[6:8]}"
        return "Unknown"

    def _age_note(self, raw: str) -> str:
        if len(raw) < 8 or not raw[:8].isdigit():
            return "Unknown"
        try:
            dt = datetime.strptime(raw[:8], "%Y%m%d")
            days = (datetime.now() - dt).days
            if days > 540:
                return "Old (18+ months)"
            if days > 365:
                return "A bit old (12+ months)"
            return "Recent"
        except Exception:
            return "Unknown"
