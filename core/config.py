"""Global configuration and constants."""

from __future__ import annotations

import os
from pathlib import Path

APP_NAME = "GameFix Doctor Pro"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Sayed Elmahdy"
APP_GITHUB = "https://github.com/Sayedelmahdy"
APP_LINKEDIN = "https://www.linkedin.com/in/sayed-elmahdy365/"
APP_EMAIL = "sayed.work223@gmail.com"

SOURCE_DIR = Path(__file__).resolve().parent.parent


def _is_true(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def _resolve_app_dir() -> Path:
    """Resolve writable runtime directory.

    Priority:
    1) GAMEFIX_PORTABLE=1 -> run fully in source folder.
    2) GAMEFIX_HOME=<path> -> custom runtime folder.
    3) Default -> %LOCALAPPDATA%\\GameFixDoctorPro
    """
    if _is_true(os.getenv("GAMEFIX_PORTABLE")):
        return SOURCE_DIR

    override = str(os.getenv("GAMEFIX_HOME", "")).strip()
    if override:
        return Path(override).expanduser()

    local_appdata = os.getenv("LOCALAPPDATA")
    base = Path(local_appdata) if local_appdata else (Path.home() / "AppData" / "Local")
    return base / "GameFixDoctorPro"


APP_DIR = _resolve_app_dir()
DATA_DIR = APP_DIR / "data"
SNAPSHOTS_DIR = APP_DIR / "snapshots"
REPORTS_DIR = APP_DIR / "reports"

HEALTH_THRESHOLDS = {
    "disk_warn_gb": 50,
    "disk_critical_gb": 20,
    "ram_warn_gb": 4,
    "ram_critical_gb": 2,
    "cpu_temp_warn_c": 70,
    "cpu_temp_critical_c": 85,
    "gpu_temp_warn_c": 75,
    "gpu_temp_critical_c": 90,
    "cpu_idle_warn": 30,
    "cpu_idle_critical": 60,
    "gpu_idle_warn": 10,
    "gpu_idle_critical": 30,
}

RAM_NOTABLE_MB = 500
RAM_HEAVY_MB = 1000


def ensure_runtime_dirs() -> None:
    """Ensure runtime directories exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
