"""System and hardware information detection."""

from __future__ import annotations

import csv
import io
import os
import platform
import re
from typing import Any

import psutil

from core.utils import gb_from_bytes, run_command

try:
    import GPUtil  # type: ignore

    HAS_GPUTIL = True
except Exception:
    HAS_GPUTIL = False

try:
    import wmi  # type: ignore

    HAS_WMI = True
except Exception:
    HAS_WMI = False


class SystemInfo:
    """Collects system information required by health and repair modules."""

    def __init__(self) -> None:
        self._wmi = wmi.WMI() if HAS_WMI and os.name == "nt" else None

    def get_os_info(self) -> dict[str, Any]:
        return {
            "name": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "build": platform.win32_ver()[1] if os.name == "nt" else "",
            "arch": platform.machine(),
        }

    def get_cpu_info(self) -> dict[str, Any]:
        hw_temps = self._read_hwmon_temperatures()

        data: dict[str, Any] = {
            "name": platform.processor() or "Unknown CPU",
            "cores": psutil.cpu_count(logical=False) or 0,
            "threads": psutil.cpu_count(logical=True) or 0,
            "usage_percent": psutil.cpu_percent(interval=0.7),
            "temperature_c": None,
            "temperature_source": None,
        }
        if self._wmi:
            try:
                item = self._wmi.Win32_Processor()[0]
                data["name"] = (item.Name or "").strip() or data["name"]
                data["max_mhz"] = int(item.MaxClockSpeed or 0)
            except Exception:
                pass
        try:
            temps = psutil.sensors_temperatures()
            for _, entries in temps.items():
                if entries:
                    data["temperature_c"] = float(entries[0].current)
                    data["temperature_source"] = "psutil"
                    break
        except Exception:
            pass

        if data["temperature_c"] is None:
            sensor = self._pick_cpu_temp_sensor(hw_temps)
            if sensor:
                data["temperature_c"] = sensor["value_c"]
                data["temperature_source"] = sensor["source"]

        return data

    def get_ram_info(self) -> dict[str, Any]:
        mem = psutil.virtual_memory()
        return {
            "total_gb": gb_from_bytes(mem.total),
            "available_gb": gb_from_bytes(mem.available),
            "used_percent": mem.percent,
        }

    def get_gpu_info(self) -> list[dict[str, Any]]:
        hw_temps = self._read_hwmon_temperatures()
        gpus: list[dict[str, Any]] = []

        # Base detection for all vendors (NVIDIA/AMD/Intel)
        if self._wmi:
            try:
                for gpu in self._wmi.Win32_VideoController():
                    name = str(gpu.Name or "Unknown GPU")
                    gpus.append(
                        {
                            "name": name,
                            "vendor": self._guess_vendor(name),
                            "driver_version": str(gpu.DriverVersion or ""),
                            "vram_total_mb": self._adapter_ram_to_mb(gpu.AdapterRAM),
                            "usage_percent": None,
                            "temperature_c": None,
                            "temperature_source": None,
                        }
                    )
            except Exception:
                pass

        # Vendor-agnostic usage from Windows GPU Engine counters.
        usage_by_index = self._get_windows_gpu_usage_by_index()
        for idx, usage in usage_by_index.items():
            if 0 <= idx < len(gpus):
                gpus[idx]["usage_percent"] = round(usage, 1)

        # Enrich NVIDIA with GPUtil metrics (temp/load) when available.
        if HAS_GPUTIL:
            try:
                nvidia = GPUtil.getGPUs()
                for n_gpu in nvidia:
                    target = self._match_gpu_by_name(gpus, n_gpu.name)
                    payload = {
                        "usage_percent": round(n_gpu.load * 100, 1),
                        "temperature_c": n_gpu.temperature,
                        "temperature_source": "gputil",
                        "vram_total_mb": n_gpu.memoryTotal,
                    }
                    if target is None:
                        gpus.append(
                            {
                                "name": n_gpu.name,
                                "vendor": "NVIDIA",
                                "driver_version": str(n_gpu.driver or ""),
                                **payload,
                            }
                        )
                    else:
                        target.update(payload)
            except Exception:
                pass

        # Vendor-neutral temperature enrichment from Libre/Open Hardware Monitor.
        for gpu in gpus:
            if gpu.get("temperature_c") is not None:
                continue
            sensor = self._pick_gpu_temp_sensor(
                hw_temps,
                gpu_name=str(gpu.get("name", "")),
                vendor=str(gpu.get("vendor", "")),
            )
            if sensor:
                gpu["temperature_c"] = sensor["value_c"]
                gpu["temperature_source"] = sensor["source"]

        return gpus

    def get_disk_info(self) -> list[dict[str, Any]]:
        disks: list[dict[str, Any]] = []
        for part in psutil.disk_partitions():
            if not part.mountpoint:
                continue
            try:
                usage = psutil.disk_usage(part.mountpoint)
            except Exception:
                continue
            disks.append(
                {
                    "device": part.device,
                    "mountpoint": part.mountpoint,
                    "fstype": part.fstype,
                    "total_gb": gb_from_bytes(usage.total),
                    "free_gb": gb_from_bytes(usage.free),
                    "used_percent": usage.percent,
                }
            )
        return disks

    def get_power_plan(self) -> str:
        if os.name != "nt":
            return "unknown"
        result = run_command("powercfg /getactivescheme")
        if not result["success"]:
            return "unknown"
        text = result["stdout"].lower()
        if "high performance" in text or "ultimate performance" in text:
            return "high_performance"
        if "balanced" in text:
            return "balanced"
        if "power saver" in text:
            return "power_saver"
        return "custom"

    def get_game_mode_status(self) -> str:
        if os.name != "nt":
            return "unknown"
        try:
            import winreg

            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\GameBar")
            value, _ = winreg.QueryValueEx(key, "AllowAutoGameMode")
            return "enabled" if int(value) == 1 else "disabled"
        except Exception:
            return "unknown"

    def get_full_system_info(self) -> dict[str, Any]:
        return {
            "os": self.get_os_info(),
            "cpu": self.get_cpu_info(),
            "ram": self.get_ram_info(),
            "gpu": self.get_gpu_info(),
            "disks": self.get_disk_info(),
            "power_plan": self.get_power_plan(),
            "game_mode": self.get_game_mode_status(),
        }

    @staticmethod
    def _adapter_ram_to_mb(value: Any) -> int | None:
        try:
            bytes_value = int(value)
            if bytes_value <= 0:
                return None
            return int(bytes_value / (1024 * 1024))
        except Exception:
            return None

    @staticmethod
    def _guess_vendor(name: str) -> str:
        lower = name.lower()
        if "nvidia" in lower or "geforce" in lower or "quadro" in lower:
            return "NVIDIA"
        if "amd" in lower or "radeon" in lower:
            return "AMD"
        if "intel" in lower or "iris" in lower or "uhd" in lower or "arc" in lower:
            return "Intel"
        return "Unknown"

    @staticmethod
    def _match_gpu_by_name(gpus: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
        probe = name.lower()
        for gpu in gpus:
            if gpu.get("name", "").lower() == probe:
                return gpu
        for gpu in gpus:
            current = gpu.get("name", "").lower()
            if probe in current or current in probe:
                return gpu
        return None

    @staticmethod
    def _get_windows_gpu_usage_by_index() -> dict[int, float]:
        """
        Read vendor-neutral GPU usage from Windows performance counters.

        Uses max engine utilization per physical GPU index to avoid summing
        multiple engines into values >100%.
        """
        if os.name != "nt":
            return {}

        result = run_command(r'typeperf "\GPU Engine(*)\Utilization Percentage" -sc 1', timeout=10)
        if not result["success"] or not result["stdout"]:
            return {}

        usage: dict[int, float] = {}
        try:
            rows = list(csv.reader(io.StringIO(result["stdout"])))
            if len(rows) < 2:
                return {}
            headers = rows[0]
            values = rows[1]
            for header, raw_value in zip(headers[1:], values[1:]):
                match = re.search(r"phys_(\d+)", header, flags=re.IGNORECASE)
                if not match:
                    continue
                index = int(match.group(1))
                try:
                    value = float(raw_value)
                except Exception:
                    continue
                previous = usage.get(index, 0.0)
                usage[index] = max(previous, value)
        except Exception:
            return {}
        return usage

    def _read_hwmon_temperatures(self) -> list[dict[str, Any]]:
        """
        Read temperatures from optional hardware monitor WMI providers.

        Supports both LibreHardwareMonitor and OpenHardwareMonitor namespaces.
        """
        if os.name != "nt" or not HAS_WMI:
            return []

        sensors: list[dict[str, Any]] = []
        for namespace, source in (
            ("root\\LibreHardwareMonitor", "librehardwaremonitor"),
            ("root\\OpenHardwareMonitor", "openhardwaremonitor"),
        ):
            try:
                client = wmi.WMI(namespace=namespace)
                rows = client.Sensor()  # type: ignore[attr-defined]
            except Exception:
                continue

            for row in rows:
                try:
                    sensor_type = str(getattr(row, "SensorType", "")).lower()
                    if sensor_type != "temperature":
                        continue
                    value = float(getattr(row, "Value", 0.0))
                    name = str(getattr(row, "Name", ""))
                    identifier = str(getattr(row, "Identifier", ""))
                    parent = str(getattr(row, "Parent", ""))
                    if value <= 0:
                        continue
                    sensors.append(
                        {
                            "source": source,
                            "name": name,
                            "identifier": identifier.lower(),
                            "parent": parent.lower(),
                            "value_c": value,
                        }
                    )
                except Exception:
                    continue
        return sensors

    @staticmethod
    def _pick_cpu_temp_sensor(sensors: list[dict[str, Any]]) -> dict[str, Any] | None:
        if not sensors:
            return None

        candidates: list[dict[str, Any]] = []
        for sensor in sensors:
            text = f"{sensor['name']} {sensor['identifier']} {sensor['parent']}".lower()
            if "cpu" in text or "package" in text or "ccd" in text or "tdie" in text:
                candidates.append(sensor)

        if not candidates:
            return None

        # Prefer package/core temperature over less useful sensors.
        def rank(item: dict[str, Any]) -> tuple[int, float]:
            text = f"{item['name']} {item['identifier']}".lower()
            if "package" in text:
                return (0, -item["value_c"])
            if "core" in text:
                return (1, -item["value_c"])
            if "ccd" in text or "tdie" in text:
                return (2, -item["value_c"])
            return (3, -item["value_c"])

        candidates.sort(key=rank)
        return candidates[0]

    @staticmethod
    def _pick_gpu_temp_sensor(
        sensors: list[dict[str, Any]],
        gpu_name: str,
        vendor: str,
    ) -> dict[str, Any] | None:
        if not sensors:
            return None

        name_low = gpu_name.lower()
        vendor_low = vendor.lower()

        scored: list[tuple[int, dict[str, Any]]] = []
        for sensor in sensors:
            text = f"{sensor['name']} {sensor['identifier']} {sensor['parent']}".lower()
            if "gpu" not in text and "graphics" not in text:
                continue

            score = 0
            if vendor_low and vendor_low in text:
                score += 3
            if name_low and any(token for token in name_low.split()[:3] if token in text):
                score += 2
            if "core" in text or "junction" in text or "edge" in text or "hot spot" in text:
                score += 1
            scored.append((score, sensor))

        if not scored:
            return None

        scored.sort(key=lambda item: (item[0], item[1]["value_c"]), reverse=True)
        return scored[0][1]
