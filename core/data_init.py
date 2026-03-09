"""Initialize default data files."""

from __future__ import annotations

from pathlib import Path

from core.utils import save_json

DEFAULT_FILES: dict[str, dict] = {
    "known_launchers.json": {
        "launchers": [
            {"name": "Steam", "process_name": "steam.exe"},
            {"name": "Epic Games", "process_name": "EpicGamesLauncher.exe"},
            {"name": "GOG Galaxy", "process_name": "GalaxyClient.exe"},
            {"name": "Ubisoft Connect", "process_name": "upc.exe"},
            {"name": "EA App", "process_name": "EADesktop.exe"},
        ]
    },
    "known_services.json": {
        "critical_never_touch": ["RpcSs", "DcomLaunch", "LSM", "SamSs", "WinDefend", "mpssvc"],
        "safe_to_disable": ["Spooler", "Fax", "WSearch", "SysMain", "DiagTrack"],
    },
    "known_apps.json": {
        "categories": {
            "gaming_essential": ["Steam", "Epic Games Launcher", "Discord"],
            "potentially_heavy": ["iCUE", "Razer Synapse", "Armoury Crate"],
        }
    },
    "game_signatures.json": {
        "engines": {
            "Unity": ["UnityPlayer.dll"],
            "Unreal Engine": ["UE4Game.exe", "UE5Game.exe"],
            "Game Maker": ["data.win"],
        }
    },
    "folder_names.json": {
        "game_folders": [
            "Games",
            "My Games",
            "PC Games",
            "العاب",
            "ألعاب",
        ]
    },
    "settings_profiles.json": {
        "profiles": {
            "competitive": {"target": "max_fps"},
            "balanced": {"target": "60_fps"},
            "visual_quality": {"target": "best_visuals"},
        }
    },
    "suspicious_patterns.json": {
        "crypto_miners": ["xmrig", "nicehash", "phoenixminer"],
        "overlay_software": ["Discord", "GameBar", "RTSS"],
    },
    "hardware_database.json": {"cpu_tiers": {}, "gpu_tiers": {}, "ram_tiers": {}},
    "repair_commands.json": {
        "repairs": {
            "sfc_scan": "sfc /scannow",
            "dism_restore": "DISM /Online /Cleanup-Image /RestoreHealth",
            "flush_dns": "ipconfig /flushdns",
        }
    },
    "known_conflicts.json": {"overlay_conflicts": [], "recording_conflicts": []},
}


def initialize_data_files(data_dir: Path) -> None:
    """Create default data files if they do not exist."""
    data_dir.mkdir(parents=True, exist_ok=True)
    for name, data in DEFAULT_FILES.items():
        path = data_dir / name
        if not path.exists():
            save_json(path, data)

