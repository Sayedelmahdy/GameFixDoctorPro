"""Diagnosis engine."""

from __future__ import annotations

from typing import Any


SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


class DiagnosisEngine:
    """Diagnose common gaming issues from system state and scan data."""

    def __init__(self, system_info, process_manager, network_doctor, driver_checker) -> None:
        self.system_info = system_info
        self.process_manager = process_manager
        self.network_doctor = network_doctor
        self.driver_checker = driver_checker

    def run(self) -> dict[str, Any]:
        system = self.system_info.get_full_system_info()
        network = self.network_doctor.diagnose()
        drivers = self.driver_checker.check()
        heavy = self.process_manager.get_closable_processes(min_ram_mb=700, top_n=5)

        issues: list[dict[str, str]] = []

        issues.extend(self._check_performance(system, heavy))
        issues.extend(self._check_stability(system))
        issues.extend(self._check_configuration(system))
        issues.extend(self._check_network(network))
        issues.extend(self._check_drivers(drivers))

        issues.sort(key=lambda x: SEVERITY_ORDER.get(x["severity"], 99))

        return {
            "status": "ok",
            "issue_count": len(issues),
            "issues": issues,
            "system": system,
            "network": network,
            "drivers": drivers,
        }

    def _check_performance(self, system: dict, heavy: list[dict]) -> list[dict]:
        issues: list[dict] = []
        ram = system.get("ram", {})
        available = float(ram.get("available_gb", 0.0))
        if available < 2:
            issues.append(
                {
                    "severity": "high",
                    "category": "performance",
                    "title": "Low available RAM",
                    "details": f"Only {available:.1f} GB RAM available.",
                    "fix": "Close heavy apps or upgrade RAM.",
                }
            )
        elif available < 4:
            issues.append(
                {
                    "severity": "medium",
                    "category": "performance",
                    "title": "Limited available RAM",
                    "details": f"{available:.1f} GB RAM available.",
                    "fix": "Close background apps before gaming.",
                }
            )

        cpu_idle = float(system.get("cpu", {}).get("usage_percent", 0.0))
        if cpu_idle > 60:
            sev = "high"
        elif cpu_idle > 30:
            sev = "medium"
        else:
            sev = ""
        if sev:
            issues.append(
                {
                    "severity": sev,
                    "category": "performance",
                    "title": "High CPU usage while idle",
                    "details": f"CPU usage is {cpu_idle:.1f}% while not gaming.",
                    "fix": "Check startup apps and background tasks.",
                }
            )

        if heavy:
            names = ", ".join(p["name"] for p in heavy[:3])
            issues.append(
                {
                    "severity": "medium",
                    "category": "performance",
                    "title": "Heavy background processes detected",
                    "details": f"Top heavy apps: {names}",
                    "fix": "Use Process Killer to close non-essential apps.",
                }
            )
        return issues

    def _check_stability(self, system: dict) -> list[dict]:
        issues: list[dict] = []
        ctemp = system.get("cpu", {}).get("temperature_c")
        if ctemp is not None and float(ctemp) > 90:
            issues.append(
                {
                    "severity": "critical",
                    "category": "stability",
                    "title": "CPU temperature is critical",
                    "details": f"CPU reached {float(ctemp):.1f}C.",
                    "fix": "Stop heavy load and inspect cooling immediately.",
                }
            )

        for gpu in system.get("gpu", []):
            gtemp = gpu.get("temperature_c")
            if gtemp is not None and float(gtemp) > 92:
                issues.append(
                    {
                        "severity": "high",
                        "category": "stability",
                        "title": "GPU temperature is very high",
                        "details": f"{gpu.get('name', 'GPU')} at {float(gtemp):.1f}C.",
                        "fix": "Improve airflow/fan curve and reduce GPU load.",
                    }
                )
                break

        for disk in system.get("disks", []):
            if str(disk.get("mountpoint", "")).upper().startswith("C:\\"):
                free = float(disk.get("free_gb", 0.0))
                if free < 10:
                    issues.append(
                        {
                            "severity": "high",
                            "category": "stability",
                            "title": "Very low system disk space",
                            "details": f"C: has only {free:.1f} GB free.",
                            "fix": "Clean temporary files and uninstall unused apps.",
                        }
                    )
                break
        return issues

    def _check_configuration(self, system: dict) -> list[dict]:
        issues: list[dict] = []
        plan = system.get("power_plan", "unknown")
        if plan != "high_performance":
            issues.append(
                {
                    "severity": "low",
                    "category": "configuration",
                    "title": "Power plan is not optimized for gaming",
                    "details": f"Current plan: {plan}.",
                    "fix": "Set High Performance in Power Optimizer.",
                }
            )

        mode = system.get("game_mode", "unknown")
        if mode != "enabled":
            issues.append(
                {
                    "severity": "low",
                    "category": "configuration",
                    "title": "Game Mode is disabled",
                    "details": "Windows Game Mode is not enabled.",
                    "fix": "Enable Game Mode in Repair Center.",
                }
            )
        return issues

    def _check_network(self, network: dict) -> list[dict]:
        issues: list[dict] = []
        if network.get("status") == "warn":
            details = network.get("summary", "Network quality warning.")
            issues.append(
                {
                    "severity": "medium",
                    "category": "network",
                    "title": "Network latency/jitter issue",
                    "details": str(details),
                    "fix": "Use Network Doctor fixes (flush DNS / set gaming DNS).",
                }
            )
        return issues

    def _check_drivers(self, drivers: dict) -> list[dict]:
        issues: list[dict] = []
        for gpu in drivers.get("gpu", []):
            if gpu.get("driver_version") in (None, "", "Unknown"):
                continue
            if str(gpu.get("driver_age_note", "")).lower().startswith("old"):
                issues.append(
                    {
                        "severity": "medium",
                        "category": "drivers",
                        "title": "GPU driver may be outdated",
                        "details": f"{gpu.get('name')}: {gpu.get('driver_version')}",
                        "fix": "Install latest driver from vendor website.",
                    }
                )
        return issues
