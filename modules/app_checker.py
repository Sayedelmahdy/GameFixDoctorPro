"""Installed app analyzer."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from core.utils import load_json, run_command


class AppChecker:
    """Analyze installed applications and classify gaming impact."""

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.known_apps = load_json(self.data_dir / "known_apps.json", default={})

    def scan(self) -> dict[str, Any]:
        apps = self._get_installed_apps()
        classified = self._classify_apps(apps)
        summary = {
            "total_apps": len(apps),
            "gaming_essential": len(classified.get("gaming_essential", [])),
            "potentially_heavy": len(classified.get("potentially_heavy", [])),
            "known_bloatware": len(classified.get("known_bloatware", [])),
            "fake_optimizers": len(classified.get("fake_optimizers", [])),
            "adware_risk": len(classified.get("adware_risk", [])),
        }
        return {"status": "ok", "apps": apps, "classified": classified, "summary": summary}

    def _get_installed_apps(self) -> list[dict]:
        if os.name != "nt":
            return []

        command = (
            'powershell -NoProfile -Command "'
            "$paths=@("
            "'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*',"
            "'HKLM:\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*',"
            "'HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*'"
            ");"
            "$items=foreach($p in $paths){Get-ItemProperty $p -ErrorAction SilentlyContinue};"
            "$items=$items | Where-Object {$_.DisplayName} | "
            "Select-Object DisplayName,DisplayVersion,Publisher,InstallDate;"
            "$items | ConvertTo-Json -Depth 3\""
        )
        result = run_command(command, timeout=40)
        if not result["success"] or not result["stdout"]:
            return []
        try:
            payload = json.loads(result["stdout"])
        except Exception:
            return []

        if isinstance(payload, dict):
            payload = [payload]
        if not isinstance(payload, list):
            return []

        output = []
        seen = set()
        for item in payload:
            name = str(item.get("DisplayName", "")).strip()
            if not name:
                continue
            key = name.lower()
            if key in seen:
                continue
            seen.add(key)
            output.append(
                {
                    "name": name,
                    "version": str(item.get("DisplayVersion", "")).strip(),
                    "publisher": str(item.get("Publisher", "")).strip(),
                    "install_date": str(item.get("InstallDate", "")).strip(),
                }
            )
        output.sort(key=lambda x: x["name"].lower())
        return output

    def _classify_apps(self, apps: list[dict]) -> dict[str, list[dict]]:
        categories = self.known_apps.get("categories", {})
        normalized: dict[str, list[str]] = {}
        if isinstance(categories, dict):
            for category_name, block in categories.items():
                if isinstance(block, dict) and isinstance(block.get("apps"), list):
                    normalized[category_name] = [str(v).lower() for v in block["apps"]]
                elif isinstance(block, list):
                    normalized[category_name] = [str(v).lower() for v in block]

        classified = {name: [] for name in normalized}
        classified.setdefault("unclassified", [])
        for app in apps:
            name_low = app["name"].lower()
            matched = False
            for category_name, patterns in normalized.items():
                if any(pattern in name_low for pattern in patterns):
                    classified[category_name].append(app)
                    matched = True
                    break
            if not matched:
                classified["unclassified"].append(app)
        return classified
