"""Snapshot and rollback management."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import psutil

from core.utils import run_command


class SnapshotManager:
    """Creates safety snapshots and restores service states."""

    def __init__(self, snapshots_dir: Path) -> None:
        self.snapshots_dir = snapshots_dir
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)

    def create_snapshot(self, action_name: str, include_restore_point: bool = True) -> str | None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        safe_action = action_name.replace(" ", "_").replace("/", "_")[:40]
        name = f"{timestamp}_{safe_action}"
        path = self.snapshots_dir / name
        path.mkdir(parents=True, exist_ok=True)

        metadata = {
            "name": name,
            "created": datetime.now().isoformat(),
            "action": action_name,
            "components": [],
        }

        if self._save_service_states(path):
            metadata["components"].append("services")

        if include_restore_point and os.name == "nt":
            if self.create_restore_point(f"GameFix Doctor - {action_name}"):
                metadata["components"].append("restore_point")

        try:
            with (path / "info.json").open("w", encoding="utf-8") as handle:
                json.dump(metadata, handle, indent=2)
            return str(path)
        except Exception:
            return None

    def list_snapshots(self) -> list[dict]:
        items: list[dict] = []
        for child in self.snapshots_dir.iterdir():
            if not child.is_dir():
                continue
            info_file = child / "info.json"
            if not info_file.exists():
                continue
            try:
                with info_file.open("r", encoding="utf-8") as handle:
                    info = json.load(handle)
                info["name"] = child.name
                info["path"] = str(child)
                items.append(info)
            except Exception:
                continue
        items.sort(key=lambda x: x.get("created", ""), reverse=True)
        return items

    def restore_snapshot(self, snapshot_path: str) -> dict:
        path = Path(snapshot_path)
        result = {"services": False, "errors": []}
        services_path = path / "services.json"
        if not services_path.exists():
            result["errors"].append("services.json not found in snapshot.")
            return result

        try:
            with services_path.open("r", encoding="utf-8") as handle:
                services = json.load(handle)
        except Exception as exc:
            result["errors"].append(str(exc))
            return result

        for service in services:
            try:
                name = service["name"]
                start_type = service.get("start_type", "manual")
                status = service.get("status", "stopped")
                mapped_start = {"automatic": "auto", "manual": "demand", "disabled": "disabled"}.get(
                    start_type, "demand"
                )
                run_command(f'sc config "{name}" start= {mapped_start}', timeout=20)
                if status == "running":
                    run_command(f'sc start "{name}"', timeout=20)
                else:
                    run_command(f'sc stop "{name}"', timeout=20)
            except Exception as exc:
                result["errors"].append(str(exc))
        result["services"] = True
        return result

    def create_restore_point(self, description: str) -> bool:
        if os.name != "nt":
            return False
        safe_description = description.replace("'", "''")
        # Best effort: ensure system restore is enabled on C:
        run_command(
            'powershell -NoProfile -Command "Enable-ComputerRestore -Drive \'C:\\\'"',
            timeout=40,
        )
        command = (
            'powershell -NoProfile -Command "Checkpoint-Computer '
            f"-Description '{safe_description}' -RestorePointType 'MODIFY_SETTINGS'\""
        )
        result = run_command(command, timeout=120)
        return result["success"]

    def list_windows_restore_points(self) -> list[dict[str, Any]]:
        """List native Windows System Restore points."""
        if os.name != "nt":
            return []

        command = (
            'powershell -NoProfile -Command "'
            "Get-ComputerRestorePoint | "
            "Select-Object SequenceNumber,Description,CreationTime,EventType,RestorePointType | "
            "ConvertTo-Json -Depth 3\""
        )
        result = run_command(command, timeout=60)
        if not result["success"] or not result.get("stdout"):
            return []

        try:
            payload = json.loads(result["stdout"])
        except Exception:
            return []

        if isinstance(payload, dict):
            payload = [payload]
        if not isinstance(payload, list):
            return []

        points = []
        for item in payload:
            try:
                points.append(
                    {
                        "sequence_number": int(item.get("SequenceNumber")),
                        "description": str(item.get("Description", "Unknown")),
                        "creation_time": str(item.get("CreationTime", "Unknown")),
                        "event_type": str(item.get("EventType", "")),
                        "restore_point_type": str(item.get("RestorePointType", "")),
                    }
                )
            except Exception:
                continue

        points.sort(key=lambda x: x.get("sequence_number", 0), reverse=True)
        return points

    def restore_windows_restore_point(self, sequence_number: int) -> dict[str, Any]:
        """Trigger restore to a specific Windows System Restore point."""
        if os.name != "nt":
            return {"success": False, "message": "Windows restore is only available on Windows."}

        command = (
            'powershell -NoProfile -Command "'
            f"Restore-Computer -RestorePoint {int(sequence_number)} -Confirm:$false\""
        )
        result = run_command(command, timeout=120)
        if result["success"]:
            return {
                "success": True,
                "message": (
                    "Windows restore operation started. Restart your PC to complete the restore process."
                ),
            }
        details = result.get("stderr") or result.get("stdout") or "Restore command failed."
        return {"success": False, "message": details}

    def _save_service_states(self, snapshot_path: Path) -> bool:
        if os.name != "nt":
            return False
        data = []
        try:
            for service in psutil.win_service_iter():
                try:
                    svc = service.as_dict()
                    data.append(
                        {
                            "name": svc["name"],
                            "status": svc["status"],
                            "start_type": svc["start_type"],
                        }
                    )
                except Exception:
                    continue
            with (snapshot_path / "services.json").open("w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2)
            return True
        except Exception:
            return False
