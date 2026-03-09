"""Used parts stress testing and buy advice."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from core.utils import load_json, run_command, save_json


@dataclass
class TestDecision:
    status: str
    summary: str
    reasons: list[str]


class StressTestAdvisor:
    """Prepare stress-test toolkit, record test sessions, and provide buy advice."""

    TOOL_CATALOG = {
        "furmark": {
            "display": "FurMark",
            "component": "gpu",
            "winget_ids": ["Geeks3D.FurMark"],
            "winget_names": ["FurMark"],
            "url": "https://geeks3d.com/furmark/",
        },
        "kombustor": {
            "display": "MSI Kombustor",
            "component": "gpu",
            "winget_ids": ["MSI.Kombustor"],
            "winget_names": ["Kombustor", "MSI Kombustor"],
            "url": "https://geeks3d.com/furmark/kombustor/",
        },
        "occt": {
            "display": "OCCT",
            "component": "cpu",
            "winget_ids": ["OCBase.OCCT"],
            "winget_names": ["OCCT"],
            "url": "https://www.ocbase.com/download",
        },
        "prime95": {
            "display": "Prime95",
            "component": "cpu",
            "winget_ids": ["Prime95.Prime95"],
            "winget_names": ["Prime95"],
            "url": "https://www.mersenne.org/download/",
        },
        "memtest64": {
            "display": "MemTest64",
            "component": "memory",
            "winget_ids": ["TechPowerUp.MemTest64"],
            "winget_names": ["MemTest64", "TechPowerUp MemTest64"],
            "url": "https://www.techpowerup.com/memtest64/",
        },
    }

    def __init__(self, app_dir: Path, system_info) -> None:
        self.app_dir = app_dir
        self.system_info = system_info
        self.kits_dir = self.app_dir / "kits"
        self.results_dir = self.app_dir / "reports" / "stress_tests"
        self.config_path = self.kits_dir / "tool_paths.json"

    def prepare_kits_folder(self) -> dict[str, Any]:
        self.kits_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        (self.kits_dir / "gpu").mkdir(exist_ok=True)
        (self.kits_dir / "cpu").mkdir(exist_ok=True)
        (self.kits_dir / "memory").mkdir(exist_ok=True)
        (self.kits_dir / "logs" / "gpu").mkdir(parents=True, exist_ok=True)
        (self.kits_dir / "logs" / "cpu").mkdir(parents=True, exist_ok=True)
        (self.kits_dir / "logs" / "memory").mkdir(parents=True, exist_ok=True)

        readme = self.kits_dir / "README.md"
        if not readme.exists():
            readme.write_text(
                "\n".join(
                    [
                        "# Stress Test Kits",
                        "",
                        "Put optional benchmark/stress tools here:",
                        "- kits/gpu/FurMark.exe",
                        "- kits/gpu/MSI-Kombustor.exe",
                        "- kits/cpu/prime95.exe",
                        "- kits/cpu/OCCT.exe",
                        "- kits/memory/MemTest64.exe",
                        "",
                        "Put exported logs here for auto-import:",
                        "- kits/logs/gpu/",
                        "- kits/logs/cpu/",
                        "- kits/logs/memory/",
                        "",
                        "Recommended RAM test on Windows: MemTest64.exe",
                        "Fallback built-in RAM test: mdsched.exe",
                    ]
                ),
                encoding="utf-8",
            )

        if not self.config_path.exists():
            save_json(
                self.config_path,
                {
                    "furmark_path": "",
                    "kombustor_path": "",
                    "prime95_path": "",
                    "occt_path": "",
                    "memtest64_path": "",
                    "preferred_currency": "USD",
                },
            )

        detected = self.detect_tools()
        return {
            "success": True,
            "message": f"Kits folder prepared at: {self.kits_dir}",
            "detected_tools": detected,
        }

    def detect_tools(self) -> dict[str, str]:
        cfg = load_json(self.config_path, default={})
        mapping = {
            "furmark": {
                "config_key": "furmark_path",
                "names": ["FurMark.exe", "FurMark_x64.exe"],
                "search_dirs": [self.kits_dir / "gpu", Path(r"C:\Program Files\Geeks3D\FurMark")],
            },
            "kombustor": {
                "config_key": "kombustor_path",
                "names": ["MSI-Kombustor.exe", "MSI-Kombustor-x64.exe"],
                "search_dirs": [self.kits_dir / "gpu", Path(r"C:\Program Files\MSI Kombustor")],
            },
            "prime95": {
                "config_key": "prime95_path",
                "names": ["prime95.exe"],
                "search_dirs": [self.kits_dir / "cpu"],
            },
            "occt": {
                "config_key": "occt_path",
                "names": ["OCCT.exe"],
                "search_dirs": [self.kits_dir / "cpu", Path(r"C:\Program Files\OCCT")],
            },
            "memtest64": {
                "config_key": "memtest64_path",
                "names": ["MemTest64.exe", "memtest64.exe"],
                "search_dirs": [
                    self.kits_dir / "memory",
                    Path(r"C:\Program Files\TechPowerUp MemTest64"),
                    Path(r"C:\Program Files (x86)\TechPowerUp MemTest64"),
                ],
            },
            "mdsched": {
                "config_key": "",
                "names": ["mdsched.exe"],
                "search_dirs": [Path(r"C:\Windows\System32")],
            },
        }

        results: dict[str, str] = {}
        for tool, meta in mapping.items():
            config_key = meta["config_key"]
            if config_key and str(cfg.get(config_key, "")).strip():
                candidate = Path(str(cfg[config_key]))
                if candidate.exists():
                    results[tool] = str(candidate)
                    continue
            found = self._find_executable(meta["names"], meta["search_dirs"])
            results[tool] = str(found) if found else ""
        return results

    def has_winget(self) -> bool:
        result = run_command("winget --version", timeout=10)
        return bool(result.get("success"))

    def install_missing_tools(self) -> dict[str, Any]:
        tools = self.detect_tools()
        report = []
        for tool in ("furmark", "kombustor", "occt", "prime95", "memtest64"):
            if tools.get(tool):
                report.append({"tool": tool, "success": True, "message": "Already installed."})
                continue
            report.append({"tool": tool, **self.install_tool(tool)})
        success = any(item.get("success") for item in report)
        return {"success": success, "report": report}

    def install_tool(self, tool_name: str) -> dict[str, Any]:
        meta = self.TOOL_CATALOG.get(tool_name)
        if not meta:
            return {"success": False, "message": f"Unknown tool: {tool_name}"}

        if self.has_winget():
            # Try package IDs first.
            for pkg_id in meta["winget_ids"]:
                result = self._winget_install_by_id(pkg_id)
                if result["success"]:
                    return {"success": True, "message": f"{meta['display']} installed via winget ({pkg_id})."}
            # Then fallback to name-based install.
            for name in meta["winget_names"]:
                result = self._winget_install_by_name(name)
                if result["success"]:
                    return {"success": True, "message": f"{meta['display']} installed via winget search name '{name}'."}

        # fallback open official page
        opened = self._open_url(meta["url"])
        if opened["success"]:
            return {
                "success": False,
                "message": f"Could not auto-install {meta['display']}. Opened official download page instead.",
            }
        return {"success": False, "message": f"Could not install or open page for {meta['display']}."}

    def launch_tool(self, tool_name: str) -> dict[str, Any]:
        tools = self.detect_tools()
        path = tools.get(tool_name, "")
        if not path:
            install = self.install_tool(tool_name)
            if not install.get("success"):
                return {
                    "success": False,
                    "message": (
                        f"{tool_name} not found. {install.get('message')} "
                        "After installing, place EXE in kits folder or configure path."
                    ),
                }
            tools = self.detect_tools()
            path = tools.get(tool_name, "")
            if not path:
                return {
                    "success": False,
                    "message": f"{tool_name} install attempted, but executable path still not found.",
                }
        result = run_command(f'start "" "{path}"', timeout=10)
        if result["success"]:
            return {"success": True, "message": f"Launched {tool_name}: {path}"}
        return {"success": False, "message": result.get("stderr") or "Failed to launch tool."}

    def schedule_memory_diagnostic(self) -> dict[str, Any]:
        result = run_command('start "" "mdsched.exe"', timeout=10)
        if result["success"]:
            return {
                "success": True,
                "message": "Windows Memory Diagnostic opened. Choose restart now or later.",
            }
        return {"success": False, "message": result.get("stderr") or "Could not open mdsched.exe"}

    def read_last_memory_diagnostic_result(self) -> dict[str, Any]:
        command = (
            'powershell -NoProfile -Command "'
            "Get-WinEvent -FilterHashtable @{LogName='System';ProviderName='Microsoft-Windows-MemoryDiagnostics-Results'} "
            "-MaxEvents 1 | Select-Object TimeCreated,Message | ConvertTo-Json -Depth 3\""
        )
        result = run_command(command, timeout=30)
        if not result["success"] or not result.get("stdout"):
            return {"success": False, "message": "No memory diagnostic result found."}
        data = load_json_from_text(result["stdout"])
        if not data:
            return {"success": False, "message": "Could not parse memory diagnostic result."}

        message = str(data.get("Message", ""))
        status = "PASS" if "no errors" in message.lower() else "WARN"
        return {
            "success": True,
            "status": status,
            "time": str(data.get("TimeCreated", "")),
            "message": message.strip(),
        }

    def import_latest_log_as_cpu_result(self, tool: str, notes: str = "") -> dict[str, Any]:
        parsed = self._parse_latest_log(tool=tool, component="cpu")
        if not parsed.get("success"):
            return parsed
        return self.record_cpu_test(
            tool=tool,
            duration_min=int(parsed.get("duration_min", 20)),
            max_temp_c=float(parsed.get("max_temp_c", 85.0)),
            crashed=bool(parsed.get("crashed", False)),
            throttling=bool(parsed.get("throttling", False)),
            notes=notes or f"Auto-imported from log: {parsed.get('file')}",
        )

    def import_latest_log_as_gpu_result(self, tool: str, notes: str = "") -> dict[str, Any]:
        parsed = self._parse_latest_log(tool=tool, component="gpu")
        if not parsed.get("success"):
            return parsed
        return self.record_gpu_test(
            tool=tool,
            duration_min=int(parsed.get("duration_min", 20)),
            max_temp_c=float(parsed.get("max_temp_c", 80.0)),
            crashed=bool(parsed.get("crashed", False)),
            artifacts=bool(parsed.get("artifacts", False)),
            notes=notes or f"Auto-imported from log: {parsed.get('file')}",
        )

    def import_latest_log_as_memory_result(self, tool: str, notes: str = "") -> dict[str, Any]:
        parsed = self._parse_latest_log(tool=tool, component="memory")
        if not parsed.get("success"):
            return parsed
        errors = int(parsed.get("errors", 0))
        crashed = bool(parsed.get("crashed", False))
        status = "FAIL" if crashed or errors > 0 else "PASS"
        message = f"Imported {tool} memory log. Errors: {errors}. Crash detected: {'yes' if crashed else 'no'}."
        return self.record_memory_test(
            source=tool,
            status=status,
            message=message,
            notes=notes or f"Auto-imported from log: {parsed.get('file')}",
        )

    def _parse_latest_log(self, tool: str, component: str) -> dict[str, Any]:
        candidates = self._candidate_log_directories(tool=tool, component=component)
        latest = self._latest_log_file(candidates)
        if not latest:
            return {
                "success": False,
                "message": f"No log found for {tool}. Put logs in kits/logs/{component}/ then retry.",
            }

        if component == "memory":
            payload = self._extract_memory_metrics_from_log(latest)
        else:
            payload = self._extract_metrics_from_log(latest, component=component)
        payload["success"] = True
        payload["file"] = str(latest)
        return payload

    def _candidate_log_directories(self, tool: str, component: str) -> list[Path]:
        dirs = [self.kits_dir / "logs" / component]
        lower = tool.lower()
        if lower == "occt":
            dirs.extend(
                [
                    Path.home() / "Documents" / "OCCT",
                    Path.home() / "Documents" / "OCCT Reports",
                ]
            )
        if lower == "furmark":
            dirs.extend(
                [
                    Path.home() / "Documents" / "FurMark",
                    Path(r"C:\Program Files\Geeks3D\FurMark"),
                ]
            )
        if lower == "prime95":
            dirs.append(self.kits_dir / "cpu")
        if lower == "kombustor":
            dirs.append(self.kits_dir / "gpu")
        if lower == "memtest64":
            dirs.extend(
                [
                    self.kits_dir / "memory",
                    Path.home() / "Documents" / "MemTest64",
                    Path.home() / "Documents" / "TechPowerUp MemTest64",
                ]
            )
        return dirs

    def _latest_log_file(self, directories: list[Path]) -> Path | None:
        all_files = []
        for directory in directories:
            if not directory.exists():
                continue
            for pattern in ("*.txt", "*.log", "*.csv", "*.json"):
                all_files.extend(directory.rglob(pattern))
        if not all_files:
            return None
        all_files.sort(key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)
        return all_files[0]

    def _extract_metrics_from_log(self, path: Path, component: str) -> dict[str, Any]:
        text = self._read_text(path)
        duration = self._extract_duration_minutes(text)
        max_temp = self._extract_max_temp_c(text)

        crashed = self._contains_any(text, ["crash", "fatal", "stopped working", "bsod", "hang"]) and not self._contains_any(
            text, ["no crash", "without crash"]
        )
        errors = self._extract_error_count(text)

        payload: dict[str, Any] = {
            "duration_min": duration if duration is not None else 20,
            "max_temp_c": max_temp if max_temp is not None else (85.0 if component == "cpu" else 80.0),
            "crashed": crashed or errors > 0,
        }
        if component == "cpu":
            payload["throttling"] = self._contains_any(text, ["throttl", "power limit", "thermal limit"])
        else:
            payload["artifacts"] = self._contains_any(text, ["artifact", "flicker", "glitch"]) or errors > 0
        return payload

    def _extract_memory_metrics_from_log(self, path: Path) -> dict[str, Any]:
        text = self._read_text(path)
        errors = self._extract_error_count(text)
        crashed = self._contains_any(text, ["crash", "fatal", "stopped working", "bsod", "hang"])
        return {
            "errors": max(0, int(errors)),
            "crashed": crashed,
        }

    @staticmethod
    def _read_text(path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return ""

    @staticmethod
    def _extract_duration_minutes(text: str) -> int | None:
        m = re.search(r"(\d+)\s*(?:min|mins|minute|minutes)\b", text, flags=re.IGNORECASE)
        if m:
            return int(m.group(1))
        m = re.search(r"\b(\d{1,2}):(\d{2}):(\d{2})\b", text)
        if m:
            h, mi, sec = int(m.group(1)), int(m.group(2)), int(m.group(3))
            return max(1, int(h * 60 + mi + (1 if sec > 0 else 0)))
        return None

    @staticmethod
    def _extract_max_temp_c(text: str) -> float | None:
        values = re.findall(r"(\d{2,3}(?:\.\d+)?)\s*(?:\u00b0)?\s*C", text, flags=re.IGNORECASE)
        if not values:
            values = re.findall(r"(\d{2,3}(?:\.\d+)?)\s*(?:deg(?:ree)?s?)?\s*C", text, flags=re.IGNORECASE)
        nums = []
        for v in values:
            try:
                n = float(v)
            except Exception:
                continue
            if 20 <= n <= 130:
                nums.append(n)
        if nums:
            return max(nums)
        return None

    @staticmethod
    def _extract_error_count(text: str) -> int:
        m = re.search(r"\b([1-9]\d*)\s+errors?\b", text, flags=re.IGNORECASE)
        if m:
            return int(m.group(1))
        if re.search(r"\bno errors?\b", text, flags=re.IGNORECASE):
            return 0
        return 0

    @staticmethod
    def _contains_any(text: str, patterns: list[str]) -> bool:
        t = text.lower()
        return any(p.lower() in t for p in patterns)

    def record_cpu_test(
        self,
        tool: str,
        duration_min: int,
        max_temp_c: float,
        crashed: bool,
        throttling: bool,
        notes: str,
    ) -> dict[str, Any]:
        decision = self.evaluate_cpu(duration_min, max_temp_c, crashed, throttling)
        payload = {
            "type": "cpu",
            "timestamp": datetime.now().isoformat(),
            "tool": tool,
            "duration_min": duration_min,
            "max_temp_c": max_temp_c,
            "crashed": crashed,
            "throttling": throttling,
            "notes": notes,
            "decision": {
                "status": decision.status,
                "summary": decision.summary,
                "reasons": decision.reasons,
            },
        }
        path = self._save_result("cpu", payload)
        return {
            "success": True,
            "path": str(path),
            "decision": {
                "status": decision.status,
                "summary": decision.summary,
                "reasons": decision.reasons,
            },
        }

    def record_gpu_test(
        self,
        tool: str,
        duration_min: int,
        max_temp_c: float,
        crashed: bool,
        artifacts: bool,
        notes: str,
    ) -> dict[str, Any]:
        decision = self.evaluate_gpu(duration_min, max_temp_c, crashed, artifacts)
        payload = {
            "type": "gpu",
            "timestamp": datetime.now().isoformat(),
            "tool": tool,
            "duration_min": duration_min,
            "max_temp_c": max_temp_c,
            "crashed": crashed,
            "artifacts": artifacts,
            "notes": notes,
            "decision": {
                "status": decision.status,
                "summary": decision.summary,
                "reasons": decision.reasons,
            },
        }
        path = self._save_result("gpu", payload)
        return {
            "success": True,
            "path": str(path),
            "decision": {
                "status": decision.status,
                "summary": decision.summary,
                "reasons": decision.reasons,
            },
        }

    def record_memory_test(self, source: str, status: str, message: str, notes: str) -> dict[str, Any]:
        decision = self.evaluate_memory(status, message)
        payload = {
            "type": "memory",
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "status": status,
            "message": message,
            "notes": notes,
            "decision": {
                "status": decision.status,
                "summary": decision.summary,
                "reasons": decision.reasons,
            },
        }
        path = self._save_result("memory", payload)
        return {
            "success": True,
            "path": str(path),
            "decision": {
                "status": decision.status,
                "summary": decision.summary,
                "reasons": decision.reasons,
            },
        }

    def record_memtest64_test(self, duration_min: int, errors: int, crashed: bool, notes: str) -> dict[str, Any]:
        if crashed or errors > 0:
            status = "FAIL"
        elif duration_min < 45:
            status = "WARN"
        else:
            status = "PASS"
        message = (
            f"MemTest64 session completed. Duration: {duration_min} min. "
            f"Errors: {max(0, errors)}. Crash/freeze: {'yes' if crashed else 'no'}."
        )
        return self.record_memory_test(source="memtest64", status=status, message=message, notes=notes)

    def evaluate_cpu(self, duration_min: int, max_temp_c: float, crashed: bool, throttling: bool) -> TestDecision:
        reasons = []
        if crashed:
            reasons.append("CPU stress test crashed/froze.")
        if max_temp_c >= 95:
            reasons.append(f"Very high CPU temperature ({max_temp_c:.1f}C).")
        if throttling:
            reasons.append("Thermal/power throttling was observed.")
        if duration_min < 20:
            reasons.append("Stress duration is short (<20 min).")

        if crashed or max_temp_c >= 95:
            return TestDecision("FAIL", "CPU part is risky for buying.", reasons)
        if throttling or max_temp_c >= 88 or duration_min < 20:
            return TestDecision("WARN", "CPU is usable but with caution.", reasons)
        return TestDecision("PASS", "CPU stress result looks healthy.", ["Stable run with safe temperatures."])

    def evaluate_gpu(self, duration_min: int, max_temp_c: float, crashed: bool, artifacts: bool) -> TestDecision:
        reasons = []
        if crashed:
            reasons.append("GPU stress test crashed/froze.")
        if artifacts:
            reasons.append("Visual artifacts observed under load.")
        if max_temp_c >= 92:
            reasons.append(f"Very high GPU temperature ({max_temp_c:.1f}C).")
        if duration_min < 20:
            reasons.append("Stress duration is short (<20 min).")

        if crashed or artifacts or max_temp_c >= 92:
            return TestDecision("FAIL", "GPU part is risky for buying.", reasons)
        if max_temp_c >= 85 or duration_min < 20:
            return TestDecision("WARN", "GPU is usable but with caution.", reasons)
        return TestDecision("PASS", "GPU stress result looks healthy.", ["Stable run with no artifacts."])

    def evaluate_memory(self, status: str, message: str) -> TestDecision:
        msg = message.lower()
        error_count = None
        m = re.search(r"\berrors?\s*[:=]\s*([0-9]+)\b", msg)
        if m:
            error_count = int(m.group(1))
        if error_count is None:
            m = re.search(r"\b([0-9]+)\s+errors?\b", msg)
            if m:
                error_count = int(m.group(1))

        has_negative = "hardware problems were detected" in msg
        if error_count is not None:
            has_negative = has_negative or error_count > 0
        else:
            has_negative = has_negative or ("errors" in msg and "no errors" not in msg)
        if status.upper() == "FAIL" or has_negative:
            return TestDecision(
                "FAIL",
                "Memory test indicates possible RAM errors.",
                ["Memory diagnostics detected issues/errors."],
            )
        if status.upper() == "WARN":
            return TestDecision("WARN", "Memory test result is uncertain.", ["Memory result needs manual review."])
        return TestDecision("PASS", "Memory test did not report errors.", ["No memory errors reported."])

    def get_buy_advice(self) -> dict[str, Any]:
        latest_memory = self._latest_result("memory")
        latest_cpu = self._latest_result("cpu")
        latest_gpu = self._latest_result("gpu")

        statuses = []
        reasons = []
        missing = []

        for name, result in (("memory", latest_memory), ("cpu", latest_cpu), ("gpu", latest_gpu)):
            if not result:
                missing.append(name)
                continue
            decision = result.get("decision", {})
            status = str(decision.get("status", "WARN")).upper()
            statuses.append(status)
            reasons.extend(decision.get("reasons", []))

        if "FAIL" in statuses:
            recommendation = "DO NOT BUY"
            confidence = "high"
        elif "WARN" in statuses or missing:
            recommendation = "BUY WITH CAUTION"
            confidence = "medium"
        else:
            recommendation = "LOOKS GOOD TO BUY"
            confidence = "medium"

        if missing:
            reasons.append(f"Missing test categories: {', '.join(missing)}.")

        return {
            "recommendation": recommendation,
            "confidence": confidence,
            "reasons": reasons[:12],
            "latest": {
                "memory": latest_memory,
                "cpu": latest_cpu,
                "gpu": latest_gpu,
            },
        }

    def get_price_to_performance_advice(self, asking_price: float, currency: str = "USD") -> dict[str, Any]:
        base = self.get_buy_advice()
        perf_score = self._estimated_performance_score()
        fair_price = round(perf_score * 4.5, 2)
        ratio = fair_price / asking_price if asking_price > 0 else 0.0
        value_score = max(0.0, min(200.0, ratio * 100.0))

        if base["recommendation"] == "DO NOT BUY":
            decision = "DO NOT BUY"
            note = "Stability/stress results already indicate serious risk."
        elif value_score >= 115:
            decision = "GOOD DEAL"
            note = "Price is lower than estimated fair value for this performance/stability level."
        elif value_score >= 90:
            decision = "FAIR PRICE"
            note = "Price is close to estimated fair value."
        else:
            decision = "OVERPRICED"
            note = "Price seems high compared to estimated performance/stability."

        return {
            "decision": decision,
            "note": note,
            "asking_price": asking_price,
            "currency": currency,
            "estimated_fair_price": fair_price,
            "value_score": round(value_score, 1),
            "performance_score": perf_score,
            "base_buy_advice": base,
        }

    def _estimated_performance_score(self) -> float:
        info = self.system_info.get_full_system_info()
        cpu_name = str(info.get("cpu", {}).get("name", "")).lower()
        gpu_name = str(info.get("gpu", [{}])[0].get("name", "")).lower() if info.get("gpu") else ""
        ram_gb = float(info.get("ram", {}).get("total_gb", 0.0))

        cpu_points = 40.0
        if "i9" in cpu_name or "ryzen 9" in cpu_name:
            cpu_points = 95.0
        elif "i7" in cpu_name or "ryzen 7" in cpu_name:
            cpu_points = 80.0
        elif "i5" in cpu_name or "ryzen 5" in cpu_name:
            cpu_points = 65.0
        elif "i3" in cpu_name or "ryzen 3" in cpu_name:
            cpu_points = 45.0

        gpu_points = 35.0
        if any(x in gpu_name for x in ("4090", "4080", "7900")):
            gpu_points = 120.0
        elif any(x in gpu_name for x in ("4070", "3080", "3090", "6800", "7800")):
            gpu_points = 100.0
        elif any(x in gpu_name for x in ("4060", "3060", "6700", "7600")):
            gpu_points = 82.0
        elif any(x in gpu_name for x in ("2060", "1660", "1070", "6600", "5700")):
            gpu_points = 65.0
        elif any(x in gpu_name for x in ("1060", "1650", "580", "570")):
            gpu_points = 50.0

        ram_points = 15.0
        if ram_gb >= 32:
            ram_points = 30.0
        elif ram_gb >= 16:
            ram_points = 24.0
        elif ram_gb >= 8:
            ram_points = 16.0

        stress_bonus = 0.0
        for kind in ("cpu", "gpu", "memory"):
            latest = self._latest_result(kind)
            if latest:
                status = str(latest.get("decision", {}).get("status", "WARN")).upper()
                if status == "PASS":
                    stress_bonus += 12.0
                elif status == "WARN":
                    stress_bonus += 3.0
                elif status == "FAIL":
                    stress_bonus -= 20.0
        return round(max(20.0, cpu_points + gpu_points + ram_points + stress_bonus), 1)

    def list_results(self) -> list[dict[str, Any]]:
        rows = []
        if not self.results_dir.exists():
            return rows
        for path in sorted(self.results_dir.glob("*.json"), reverse=True):
            data = load_json(path, default={})
            if not data:
                continue
            rows.append(
                {
                    "file": str(path),
                    "type": data.get("type", ""),
                    "timestamp": data.get("timestamp", ""),
                    "decision": data.get("decision", {}).get("status", ""),
                    "summary": data.get("decision", {}).get("summary", ""),
                }
            )
        return rows

    def _latest_result(self, kind: str) -> dict[str, Any]:
        rows = self.list_results()
        for item in rows:
            if item.get("type") == kind:
                return load_json(Path(item["file"]), default={})
        return {}

    def _save_result(self, kind: str, payload: dict[str, Any]) -> Path:
        self.results_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        path = self.results_dir / f"{stamp}_{kind}.json"
        save_json(path, payload)
        return path

    @staticmethod
    def _find_executable(names: list[str], directories: list[Path]) -> Path | None:
        for directory in directories:
            if not directory.exists():
                continue
            for name in names:
                direct = directory / name
                if direct.exists():
                    return direct
            try:
                for child in directory.rglob("*.exe"):
                    if child.name in names:
                        return child
            except Exception:
                continue
        return None

    @staticmethod
    def _open_url(url: str) -> dict[str, Any]:
        result = run_command(f'start "" "{url}"', timeout=10)
        if result.get("success"):
            return {"success": True, "message": f"Opened: {url}"}
        return {"success": False, "message": result.get("stderr") or "Failed to open URL."}

    def _winget_install_by_id(self, package_id: str) -> dict[str, Any]:
        command = (
            f'winget install --id "{package_id}" --exact --silent '
            "--accept-package-agreements --accept-source-agreements --disable-interactivity"
        )
        result = run_command(command, timeout=600)
        if result.get("success"):
            return {"success": True, "message": f"Installed {package_id}"}
        txt = ((result.get("stdout") or "") + "\n" + (result.get("stderr") or "")).lower()
        if "already installed" in txt or "no available upgrade found" in txt:
            return {"success": True, "message": f"{package_id} already installed/up to date."}
        return {"success": False, "message": result.get("stderr") or result.get("stdout") or "winget failed"}

    def _winget_install_by_name(self, name: str) -> dict[str, Any]:
        command = (
            f'winget install --name "{name}" --silent '
            "--accept-package-agreements --accept-source-agreements --disable-interactivity"
        )
        result = run_command(command, timeout=600)
        if result.get("success"):
            return {"success": True, "message": f"Installed {name}"}
        txt = ((result.get("stdout") or "") + "\n" + (result.get("stderr") or "")).lower()
        if "already installed" in txt or "no available upgrade found" in txt:
            return {"success": True, "message": f"{name} already installed/up to date."}
        return {"success": False, "message": result.get("stderr") or result.get("stdout") or "winget failed"}


def load_json_from_text(text: str) -> dict[str, Any]:
    try:
        payload = json.loads(text)
        if isinstance(payload, dict):
            return payload
    except Exception:
        return {}
    return {}
