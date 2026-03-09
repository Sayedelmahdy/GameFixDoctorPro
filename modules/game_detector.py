"""Game detection module."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.utils import load_json


class GameDetector:
    """Detect installed games across launcher folders, game folders, and shortcuts."""

    EXE_BLACKLIST = {
        "unins000.exe",
        "uninstall.exe",
        "launcherinstaller.exe",
        "setup.exe",
    }

    LAUNCHER_NAMES = ("steam", "epic", "gog", "ubisoft", "ea app", "battle.net", "rockstar", "amazon")

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.folder_names = self._load_folder_names()
        self.known_launchers = self._load_launchers()

    def detect(self) -> dict[str, Any]:
        launcher_games = self._detect_launcher_games()
        standalone_games = self._detect_standalone_games()
        shortcut_games = self._detect_shortcut_games()

        merged = self._deduplicate(launcher_games + standalone_games + shortcut_games)

        return {
            "launcher_games": launcher_games,
            "standalone_games": standalone_games,
            "shortcut_games": shortcut_games,
            "all_games": merged,
            "total_count": len(merged),
        }

    def _load_folder_names(self) -> list[str]:
        path = self.data_dir / "folder_names.json"
        data = load_json(path, default={})
        if isinstance(data.get("game_folders"), list):
            return [str(v) for v in data["game_folders"]]
        folders = data.get("game_folders", {})
        names: list[str] = []
        if isinstance(folders, dict):
            for values in folders.values():
                if isinstance(values, list):
                    names.extend(str(v) for v in values)
        return names or ["Games", "My Games", "PC Games", "العاب", "ألعاب"]

    def _load_launchers(self) -> list[dict]:
        path = self.data_dir / "known_launchers.json"
        data = load_json(path, default={})
        launchers = data.get("launchers", [])
        return launchers if isinstance(launchers, list) else []

    def _detect_launcher_games(self) -> list[dict]:
        results: list[dict] = []
        for launcher in self.known_launchers:
            name = str(launcher.get("name", "Unknown Launcher"))
            roots = self._launcher_paths_from_config(launcher)
            for root in roots:
                if not root.exists():
                    continue
                for game_dir in self._find_game_dirs(root, max_items=20):
                    results.append(
                        {
                            "name": game_dir.name,
                            "path": str(game_dir),
                            "source": "launcher",
                            "launcher": name,
                        }
                    )
        return results

    def _launcher_paths_from_config(self, launcher: dict) -> list[Path]:
        roots: list[Path] = []
        detection = launcher.get("detection", {})
        if isinstance(detection, dict):
            fallbacks = detection.get("fallback_paths")
            if isinstance(fallbacks, list):
                for path in fallbacks:
                    roots.append(Path(str(path)))
            default_path = detection.get("default_path")
            if default_path:
                roots.append(Path(str(default_path)))

        lib = launcher.get("library_detection", {})
        if isinstance(lib, dict):
            default_path = lib.get("default_path")
            if default_path:
                roots.append(Path(str(default_path)))

        name = str(launcher.get("name", "")).lower()
        if "steam" in name:
            roots.extend(
                [
                    Path(r"C:\Program Files (x86)\Steam\steamapps\common"),
                    Path(r"D:\SteamLibrary\steamapps\common"),
                    Path(r"E:\SteamLibrary\steamapps\common"),
                ]
            )
        if "epic" in name:
            roots.extend([Path(r"C:\Program Files\Epic Games"), Path(r"D:\Epic Games")])
        return roots

    def _detect_standalone_games(self) -> list[dict]:
        results: list[dict] = []
        for root in self._candidate_game_roots():
            if not root.exists():
                continue
            for game_dir in self._find_game_dirs(root, max_items=30):
                results.append(
                    {
                        "name": game_dir.name,
                        "path": str(game_dir),
                        "source": "standalone",
                        "launcher": None,
                    }
                )
        return results

    def _candidate_game_roots(self) -> list[Path]:
        roots: list[Path] = []

        for drive in self._available_drives():
            for name in self.folder_names:
                roots.append(drive / name)

        roots.extend(
            [
                Path(r"C:\Games"),
                Path(r"C:\Program Files"),
                Path(r"C:\Program Files (x86)"),
                Path.home() / "Games",
            ]
        )
        return roots

    def _detect_shortcut_games(self) -> list[dict]:
        results: list[dict] = []
        desktop = Path.home() / "Desktop"
        if not desktop.exists():
            return results
        for shortcut in desktop.glob("*.lnk"):
            lname = shortcut.stem.lower()
            if any(key in lname for key in ("game", "steam", "epic", "play", "fifa", "valorant", "fortnite")):
                results.append(
                    {
                        "name": shortcut.stem,
                        "path": str(shortcut),
                        "source": "shortcut",
                        "launcher": None,
                    }
                )
        return results

    @staticmethod
    def _available_drives() -> list[Path]:
        drives: list[Path] = []
        for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
            root = Path(f"{letter}:\\")
            if root.exists():
                drives.append(root)
        return drives

    def _find_game_dirs(self, root: Path, max_items: int = 30) -> list[Path]:
        if not root.exists() or not root.is_dir():
            return []
        found: list[Path] = []
        try:
            for entry in root.iterdir():
                if len(found) >= max_items:
                    break
                if not entry.is_dir():
                    continue
                if self._looks_like_game_dir(entry):
                    found.append(entry)
        except Exception:
            return found
        return found

    def _looks_like_game_dir(self, folder: Path) -> bool:
        name_low = folder.name.lower()
        if any(token in name_low for token in self.LAUNCHER_NAMES):
            return False
        exe_count = 0
        try:
            for entry in folder.iterdir():
                if entry.is_file() and entry.suffix.lower() == ".exe":
                    if entry.name.lower() not in self.EXE_BLACKLIST:
                        exe_count += 1
                if exe_count >= 1:
                    return True
        except Exception:
            return False
        return False

    @staticmethod
    def _deduplicate(games: list[dict]) -> list[dict]:
        seen = set()
        output = []
        for game in games:
            key = str(game.get("path", "")).lower()
            if not key or key in seen:
                continue
            seen.add(key)
            output.append(game)
        return output

