"""Process analysis and safe termination."""

from __future__ import annotations

import psutil

PROTECTED_PROCESSES = {
    "system",
    "memory compression",
    "memcompression",
    "registry",
    "system interrupts",
    "idle",
    "system idle process",
    "smss.exe",
    "csrss.exe",
    "wininit.exe",
    "services.exe",
    "lsass.exe",
    "winlogon.exe",
    "dwm.exe",
    "svchost.exe",
    "explorer.exe",
    "msmpeng.exe",
    "securityhealthservice.exe",
    "gamefixdoctorpro.exe",
    "python.exe",
}


class ProcessManager:
    """Find heavy processes and close only non-protected ones."""

    def get_process_list(self) -> list[dict]:
        processes: list[dict] = []
        for proc in psutil.process_iter(["pid", "name", "memory_info", "cpu_percent", "status"]):
            try:
                name = (proc.info.get("name") or "").strip()
                if not name:
                    continue
                mem_mb = float(proc.info["memory_info"].rss) / (1024 * 1024) if proc.info["memory_info"] else 0.0
                processes.append(
                    {
                        "pid": int(proc.info["pid"]),
                        "name": name,
                        "memory_mb": round(mem_mb, 1),
                        "cpu_percent": float(proc.info.get("cpu_percent", 0.0)),
                        "status": str(proc.info.get("status", "")),
                        "is_protected": name.lower() in PROTECTED_PROCESSES,
                    }
                )
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue
        return processes

    def get_closable_processes(self, min_ram_mb: int = 300, top_n: int = 20) -> list[dict]:
        processes = [
            p
            for p in self.get_process_list()
            if p["memory_mb"] >= min_ram_mb and not p["is_protected"]
        ]
        processes.sort(key=lambda p: p["memory_mb"], reverse=True)
        return processes[:top_n]

    def get_top_ram_processes(self, count: int = 10) -> list[dict]:
        processes = self.get_process_list()
        processes.sort(key=lambda p: p["memory_mb"], reverse=True)
        return processes[:count]

    def get_top_cpu_processes(self, count: int = 10, sample_seconds: float = 1.0) -> list[dict]:
        for proc in psutil.process_iter():
            try:
                proc.cpu_percent()
            except Exception:
                continue
        try:
            import time

            time.sleep(sample_seconds)
        except Exception:
            pass

        rows: list[dict] = []
        for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info"]):
            try:
                name = (proc.info.get("name") or "").strip()
                if not name:
                    continue
                mem_mb = float(proc.info["memory_info"].rss) / (1024 * 1024) if proc.info["memory_info"] else 0.0
                rows.append(
                    {
                        "pid": int(proc.info["pid"]),
                        "name": name,
                        "cpu_percent": float(proc.info.get("cpu_percent", 0.0)),
                        "memory_mb": round(mem_mb, 1),
                        "is_protected": name.lower() in PROTECTED_PROCESSES,
                    }
                )
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue
        rows.sort(key=lambda p: p["cpu_percent"], reverse=True)
        return rows[:count]

    def close_process(self, pid: int, force: bool = False) -> tuple[bool, str]:
        try:
            proc = psutil.Process(pid)
            name = proc.name()
            if name.lower() in PROTECTED_PROCESSES:
                return False, f"Cannot close protected process: {name}"
            proc.terminate()
            proc.wait(timeout=5)
            return True, f"Closed process: {name}"
        except psutil.TimeoutExpired:
            if force:
                try:
                    proc.kill()
                    return True, "Process force-closed."
                except Exception as exc:
                    return False, f"Force close failed: {exc}"
            return False, "Process did not close in time."
        except psutil.NoSuchProcess:
            return True, "Process already exited."
        except Exception as exc:
            return False, str(exc)
