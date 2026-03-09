"""Network diagnostics and safe fixes."""

from __future__ import annotations

import os
import re
from typing import Any

import psutil

from core.utils import run_command


class NetworkDoctor:
    """Diagnose network state and run safe network repairs."""

    def diagnose(self) -> dict[str, Any]:
        adapters = self._get_active_adapters()
        dns_servers = self._get_dns_servers()
        ping_1 = self._ping_host("1.1.1.1")
        ping_2 = self._ping_host("8.8.8.8")

        avg_latency = self._avg([ping_1.get("avg_ms"), ping_2.get("avg_ms")])
        status = "ok"
        if avg_latency is not None and avg_latency > 100:
            status = "warn"
        summary = "Network looks healthy."
        if status == "warn":
            summary = f"Average baseline ping is high ({avg_latency:.1f} ms)."

        return {
            "status": status,
            "summary": summary,
            "adapters": adapters,
            "dns_servers": dns_servers,
            "pings": [ping_1, ping_2],
            "avg_latency_ms": avg_latency,
        }

    def flush_dns(self) -> dict[str, Any]:
        result = run_command("ipconfig /flushdns", timeout=30)
        return self._result("Flushed DNS cache.", result)

    def reset_winsock(self) -> dict[str, Any]:
        result = run_command("netsh winsock reset", timeout=30)
        return self._result("Winsock reset complete. Reboot required.", result)

    def reset_ip_stack(self) -> dict[str, Any]:
        result = run_command("netsh int ip reset", timeout=30)
        return self._result("TCP/IP stack reset complete. Reboot required.", result)

    def set_dns(self, primary: str = "1.1.1.1", secondary: str = "8.8.8.8") -> dict[str, Any]:
        if os.name != "nt":
            return {"success": False, "message": "DNS setting is only supported on Windows."}
        adapters = self._get_active_adapters()
        if not adapters:
            return {"success": False, "message": "No active network adapters found."}
        # Apply to first active adapter.
        name = adapters[0]["name"]
        cmd1 = f'netsh interface ip set dns name="{name}" static {primary}'
        cmd2 = f'netsh interface ip add dns name="{name}" {secondary} index=2'
        r1 = run_command(cmd1, timeout=30)
        if not r1["success"]:
            return {"success": False, "message": r1["stderr"] or "Failed to set primary DNS."}
        r2 = run_command(cmd2, timeout=30)
        if not r2["success"]:
            return {"success": False, "message": r2["stderr"] or "Failed to set secondary DNS."}
        return {"success": True, "message": f"DNS updated on adapter '{name}'."}

    def _get_active_adapters(self) -> list[dict]:
        output = []
        for name, stats in psutil.net_if_stats().items():
            if not stats.isup:
                continue
            if "loopback" in name.lower():
                continue
            adapter_type = "ethernet"
            low = name.lower()
            if "wi-fi" in low or "wifi" in low or "wlan" in low:
                adapter_type = "wifi"
            output.append({"name": name, "type": adapter_type, "speed_mbps": stats.speed})
        return output

    @staticmethod
    def _get_dns_servers() -> list[str]:
        result = run_command("ipconfig /all", timeout=20)
        if not result["success"]:
            return []
        servers: list[str] = []
        capture = False
        for line in result["stdout"].splitlines():
            if "DNS Servers" in line:
                capture = True
                found = re.findall(r"\d+\.\d+\.\d+\.\d+", line)
                servers.extend(found)
                continue
            if capture:
                found = re.findall(r"\d+\.\d+\.\d+\.\d+", line)
                if found:
                    servers.extend(found)
                else:
                    capture = False
        # unique, preserve order
        unique = []
        seen = set()
        for item in servers:
            if item not in seen:
                seen.add(item)
                unique.append(item)
        return unique

    @staticmethod
    def _ping_host(host: str) -> dict:
        result = run_command(f"ping -n 4 {host}", timeout=20)
        payload = {"host": host, "success": result["success"], "avg_ms": None}
        if not result["stdout"]:
            return payload
        text = result["stdout"]
        match = re.search(r"Average = (\d+)ms", text, flags=re.IGNORECASE)
        if not match:
            match = re.search(r"Average = (\d+)ms", text)
        if match:
            payload["avg_ms"] = float(match.group(1))
        return payload

    @staticmethod
    def _avg(values: list[Any]) -> float | None:
        nums = [float(v) for v in values if isinstance(v, (int, float))]
        if not nums:
            return None
        return sum(nums) / len(nums)

    @staticmethod
    def _result(success_message: str, result: dict) -> dict[str, Any]:
        if result["success"]:
            return {"success": True, "message": success_message}
        return {"success": False, "message": result["stderr"] or "Operation failed."}
