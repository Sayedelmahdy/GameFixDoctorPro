"""Application settings manager."""

from __future__ import annotations

from pathlib import Path

from core.utils import load_json, save_json


class SettingsManager:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.defaults = {
            "create_snapshots_before_repairs": "Always",
            "auto_scan_on_startup": False,
            "startup_essentials_check": True,
            "theme": "Colors",
            "report_location": "./reports",
            "snapshot_location": "./snapshots",
            "check_for_updates": True,
            "show_advanced_options": False,
        }

    def load(self) -> dict:
        data = load_json(self.path, default={})
        merged = dict(self.defaults)
        merged.update(data)
        return merged

    def save(self, values: dict) -> bool:
        payload = dict(self.defaults)
        payload.update(values)
        return save_json(self.path, payload)

    def set_value(self, key: str, value) -> bool:
        current = self.load()
        current[key] = value
        return self.save(current)

    def toggle_bool(self, key: str) -> bool:
        current = self.load()
        current[key] = not bool(current.get(key, False))
        return self.save(current)
