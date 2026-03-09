"""Administrator elevation and checks."""

from __future__ import annotations

import ctypes
import os
import subprocess
import sys


def is_windows() -> bool:
    return os.name == "nt"


def is_admin() -> bool:
    """Return True if running with administrative privileges."""
    if not is_windows():
        return True
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def relaunch_as_admin() -> bool:
    """Attempt to relaunch the app with UAC elevation."""
    if not is_windows():
        return True
    try:
        params = subprocess.list2cmdline(sys.argv)
        rc = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        # ShellExecute returns a value > 32 on success.
        return rc > 32
    except Exception:
        return False


def ensure_admin() -> None:
    """Auto-request admin rights on Windows, then exit current process."""
    if not is_windows():
        return
    if is_admin():
        return
    if relaunch_as_admin():
        sys.exit(0)

