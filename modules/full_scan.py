"""Full system scan implementation."""

from __future__ import annotations

from typing import Any


class FullScan:
    """Collects deep scan data across hardware, processes, services, and drivers."""

    def __init__(
        self,
        system_info,
        process_manager,
        services,
        network_doctor,
        driver_checker,
        game_detector,
    ) -> None:
        self.system_info = system_info
        self.process_manager = process_manager
        self.services = services
        self.network_doctor = network_doctor
        self.driver_checker = driver_checker
        self.game_detector = game_detector

    def run(self) -> dict[str, Any]:
        system = self.system_info.get_full_system_info()
        top_ram = self.process_manager.get_top_ram_processes(10)
        top_cpu = self.process_manager.get_top_cpu_processes(10)
        services = self.services.list_services()
        network = self.network_doctor.diagnose()
        drivers = self.driver_checker.check()
        games = self.game_detector.detect()

        summary = {
            "ram_top_count": len(top_ram),
            "cpu_top_count": len(top_cpu),
            "services_running": len([s for s in services if s.get("status") == "running"]),
            "services_total": len(services),
            "games_detected": games.get("total_count", 0),
            "network_status": network.get("status", "unknown"),
        }
        issues = self._build_issue_summary(system, network)

        return {
            "status": "ok",
            "system": system,
            "processes": {"top_ram": top_ram, "top_cpu": top_cpu},
            "services": services,
            "network": network,
            "drivers": drivers,
            "games": games,
            "summary": summary,
            "issues": issues,
        }

    @staticmethod
    def _build_issue_summary(system: dict, network: dict) -> list[dict]:
        issues: list[dict] = []

        ram = system.get("ram", {})
        if float(ram.get("available_gb", 0.0)) < 2:
            issues.append({"severity": "high", "message": "Low available RAM (<2 GB)."})

        disks = system.get("disks", [])
        for disk in disks:
            if str(disk.get("mountpoint", "")).upper().startswith("C:\\"):
                if float(disk.get("free_gb", 0.0)) < 20:
                    issues.append({"severity": "high", "message": "Low C: disk space (<20 GB)."})
                break

        cpu = system.get("cpu", {})
        ctemp = cpu.get("temperature_c")
        if ctemp is not None and float(ctemp) > 85:
            issues.append({"severity": "high", "message": f"High CPU temperature ({ctemp:.1f}C)."})

        for gpu in system.get("gpu", []):
            gtemp = gpu.get("temperature_c")
            if gtemp is not None and float(gtemp) > 90:
                issues.append({"severity": "high", "message": f"High GPU temperature ({gtemp:.1f}C)."})
                break

        if network.get("status") == "warn":
            issues.append({"severity": "medium", "message": "Network latency is higher than ideal."})

        if not issues:
            issues.append({"severity": "info", "message": "No major issues detected in full scan."})

        return issues
