"""Quick health check for gaming readiness."""

from __future__ import annotations

from typing import Any

from core.config import HEALTH_THRESHOLDS


class HealthChecker:
    """Runs fast checks and returns normalized statuses."""

    def __init__(self, system_info) -> None:
        self.system_info = system_info

    def run(self) -> dict[str, Any]:
        info = self.system_info.get_full_system_info()
        checks: list[dict[str, str]] = []

        checks.append(self._check_disk(info))
        checks.append(self._check_ram(info))
        checks.append(self._check_cpu_temp(info))
        checks.append(self._check_gpu_temp(info))
        checks.append(self._check_cpu_usage(info))
        checks.append(self._check_gpu_usage(info))
        checks.append(self._check_power(info))
        checks.append(self._check_game_mode(info))

        score = self._score(checks)
        tips = self._tips(checks)
        return {"checks": checks, "score": score, "tips": tips, "raw": info}

    def _check_disk(self, info: dict[str, Any]) -> dict[str, str]:
        disks = info.get("disks", [])
        c_disk = next((d for d in disks if str(d.get("mountpoint", "")).upper().startswith("C:\\")), None)
        if not c_disk and disks:
            c_disk = disks[0]
        free_gb = float(c_disk.get("free_gb", 0)) if c_disk else 0.0
        if free_gb < HEALTH_THRESHOLDS["disk_critical_gb"]:
            return {"name": "Disk Space", "status": "FAIL", "message": f"{free_gb:.1f} GB free (critical)"}
        if free_gb < HEALTH_THRESHOLDS["disk_warn_gb"]:
            return {"name": "Disk Space", "status": "WARN", "message": f"{free_gb:.1f} GB free (low)"}
        return {"name": "Disk Space", "status": "OK", "message": f"{free_gb:.1f} GB free"}

    def _check_ram(self, info: dict[str, Any]) -> dict[str, str]:
        ram = info.get("ram", {})
        available = float(ram.get("available_gb", 0.0))
        total = float(ram.get("total_gb", 0.0))
        if available < HEALTH_THRESHOLDS["ram_critical_gb"]:
            return {"name": "RAM", "status": "FAIL", "message": f"{available:.1f} GB available of {total:.1f} GB"}
        if available < HEALTH_THRESHOLDS["ram_warn_gb"]:
            return {"name": "RAM", "status": "WARN", "message": f"{available:.1f} GB available of {total:.1f} GB"}
        return {"name": "RAM", "status": "OK", "message": f"{available:.1f} GB available of {total:.1f} GB"}

    def _check_cpu_usage(self, info: dict[str, Any]) -> dict[str, str]:
        usage = float(info.get("cpu", {}).get("usage_percent", 0.0))
        if usage > HEALTH_THRESHOLDS["cpu_idle_critical"]:
            return {"name": "CPU Usage", "status": "FAIL", "message": f"{usage:.1f}% at idle"}
        if usage > HEALTH_THRESHOLDS["cpu_idle_warn"]:
            return {"name": "CPU Usage", "status": "WARN", "message": f"{usage:.1f}% at idle"}
        return {"name": "CPU Usage", "status": "OK", "message": f"{usage:.1f}% at idle"}

    def _check_cpu_temp(self, info: dict[str, Any]) -> dict[str, str]:
        cpu = info.get("cpu", {})
        temp = cpu.get("temperature_c")
        source = cpu.get("temperature_source")
        if temp is None:
            return {"name": "CPU Temp", "status": "INFO", "message": "Not available"}
        temp = float(temp)
        suffix = f" ({source})" if source else ""
        if temp > HEALTH_THRESHOLDS["cpu_temp_critical_c"]:
            return {"name": "CPU Temp", "status": "FAIL", "message": f"{temp:.1f}°C{suffix}"}
        if temp > HEALTH_THRESHOLDS["cpu_temp_warn_c"]:
            return {"name": "CPU Temp", "status": "WARN", "message": f"{temp:.1f}°C{suffix}"}
        return {"name": "CPU Temp", "status": "OK", "message": f"{temp:.1f}°C{suffix}"}

    def _check_gpu_temp(self, info: dict[str, Any]) -> dict[str, str]:
        gpus = info.get("gpu", [])
        hottest = None
        for gpu in gpus:
            temp = gpu.get("temperature_c")
            if temp is None:
                continue
            if hottest is None or float(temp) > float(hottest.get("temperature_c", 0.0)):
                hottest = gpu
        if hottest is None:
            return {"name": "GPU Temp", "status": "INFO", "message": "Not available"}

        temp = float(hottest["temperature_c"])
        source = hottest.get("temperature_source")
        label = hottest.get("name", "GPU")
        suffix = f" ({source})" if source else ""
        short_label = str(label)[:24]
        if temp > HEALTH_THRESHOLDS["gpu_temp_critical_c"]:
            return {"name": "GPU Temp", "status": "FAIL", "message": f"{temp:.1f}°C on {short_label}{suffix}"}
        if temp > HEALTH_THRESHOLDS["gpu_temp_warn_c"]:
            return {"name": "GPU Temp", "status": "WARN", "message": f"{temp:.1f}°C on {short_label}{suffix}"}
        return {"name": "GPU Temp", "status": "OK", "message": f"{temp:.1f}°C on {short_label}{suffix}"}

    def _check_gpu_usage(self, info: dict[str, Any]) -> dict[str, str]:
        gpus = info.get("gpu", [])
        usage = None
        for gpu in gpus:
            if gpu.get("usage_percent") is not None:
                usage = float(gpu["usage_percent"])
                break
        if usage is None:
            return {"name": "GPU Usage", "status": "INFO", "message": "Not available"}
        if usage > HEALTH_THRESHOLDS["gpu_idle_critical"]:
            return {"name": "GPU Usage", "status": "FAIL", "message": f"{usage:.1f}% at idle"}
        if usage > HEALTH_THRESHOLDS["gpu_idle_warn"]:
            return {"name": "GPU Usage", "status": "WARN", "message": f"{usage:.1f}% at idle"}
        return {"name": "GPU Usage", "status": "OK", "message": f"{usage:.1f}% at idle"}

    def _check_power(self, info: dict[str, Any]) -> dict[str, str]:
        plan = str(info.get("power_plan", "unknown"))
        if plan == "high_performance":
            return {"name": "Power Plan", "status": "OK", "message": "High Performance"}
        if plan == "balanced":
            return {"name": "Power Plan", "status": "WARN", "message": "Balanced"}
        if plan == "power_saver":
            return {"name": "Power Plan", "status": "FAIL", "message": "Power Saver"}
        return {"name": "Power Plan", "status": "INFO", "message": "Unknown"}

    def _check_game_mode(self, info: dict[str, Any]) -> dict[str, str]:
        mode = str(info.get("game_mode", "unknown"))
        if mode == "enabled":
            return {"name": "Game Mode", "status": "OK", "message": "Enabled"}
        if mode == "disabled":
            return {"name": "Game Mode", "status": "WARN", "message": "Disabled"}
        return {"name": "Game Mode", "status": "INFO", "message": "Unknown"}

    def _score(self, checks: list[dict[str, str]]) -> int:
        score = 0.0
        for item in checks:
            state = item["status"]
            if state == "OK":
                score += 1.0
            elif state == "WARN":
                score += 0.5
            elif state == "INFO":
                score += 0.5
        if not checks:
            return 0
        return round((score / len(checks)) * 10)

    def _tips(self, checks: list[dict[str, str]]) -> list[str]:
        tips: list[str] = []
        for item in checks:
            if item["status"] == "WARN" and item["name"] == "Power Plan":
                tips.append("Switch to High Performance when gaming.")
            if item["status"] == "WARN" and item["name"] == "Game Mode":
                tips.append("Enable Windows Game Mode for gaming sessions.")
            if item["status"] in {"WARN", "FAIL"} and item["name"] in {"CPU Temp", "GPU Temp"}:
                tips.append("Temperatures are high. Check cooling, fan curve, and dust buildup.")
            if item["status"] == "INFO" and item["name"] == "GPU Temp":
                tips.append("For AMD/Intel temp sensors, run LibreHardwareMonitor with WMI enabled.")
            if item["status"] == "FAIL":
                tips.append(f"Fix critical issue: {item['name']}.")
        if not tips:
            tips.append("System is in good shape for gaming.")
        return tips
