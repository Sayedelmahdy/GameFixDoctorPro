"""Service analysis and safe service control."""

from __future__ import annotations

import os

import psutil

from core.utils import run_command

CRITICAL_SERVICES = {
    "RpcSs",
    "DcomLaunch",
    "LSM",
    "SamSs",
    "WinDefend",
    "mpssvc",
    "eventlog",
    "Dhcp",
    "Dnscache",
    "PlugPlay",
    "Power",
    "ProfSvc",
}

SAFE_TO_DISABLE = {
    "Spooler",
    "Fax",
    "WSearch",
    "SysMain",
    "DiagTrack",
    "dmwappushservice",
    "RemoteRegistry",
}


class ServiceOptimizer:
    """Read and modify non-critical services with safety checks."""

    def list_services(self) -> list[dict]:
        if os.name != "nt":
            return []
        output = []
        for service in psutil.win_service_iter():
            try:
                data = service.as_dict()
                output.append(
                    {
                        "name": data["name"],
                        "display_name": data["display_name"],
                        "status": data["status"],
                        "start_type": data["start_type"],
                    }
                )
            except Exception:
                continue
        return output

    def get_recommended_to_stop(self) -> list[dict]:
        services = self.list_services()
        result: list[dict] = []
        for service in services:
            name = service["name"]
            if name in SAFE_TO_DISABLE and service["status"] == "running":
                result.append(service)
        return result

    def stop_service(self, service_name: str) -> tuple[bool, str]:
        if os.name != "nt":
            return False, "Service operations are only available on Windows."
        if service_name in CRITICAL_SERVICES:
            return False, f"Cannot stop '{service_name}': critical service."
        if service_name not in SAFE_TO_DISABLE:
            return False, f"'{service_name}' is not in safe-to-disable list."

        stop_result = run_command(f'sc stop "{service_name}"', timeout=40)
        if not stop_result["success"]:
            return False, stop_result["stderr"] or f"Failed to stop {service_name}."
        return True, f"Stopped service: {service_name}"

