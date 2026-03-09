# GameFix Doctor Pro - Data Specifications

## Overview

This document defines all data structures, JSON databases, and configuration files used by GameFix Doctor Pro.

---

## Directory Structure

```
data/
├── known_launchers.json       # Game launcher detection data
├── known_services.json        # Windows service classifications
├── known_apps.json            # Application risk classifications
├── game_signatures.json       # Game engine detection signatures
├── folder_names.json          # Multi-language game folder names
├── settings_profiles.json     # Game settings recommendations
├── suspicious_patterns.json   # Suspicious process patterns
├── hardware_database.json     # CPU/GPU classification data
├── repair_commands.json       # Repair command definitions
└── known_conflicts.json       # Known software conflicts
```

---

## 1. known_launchers.json

Defines how to detect each game launcher and find its game libraries.

```json
{
  "launchers": [
    {
      "name": "Steam",
      "detection": {
        "registry_key": "HKEY_CURRENT_USER\\SOFTWARE\\Valve\\Steam",
        "registry_value": "SteamPath",
        "fallback_paths": [
          "C:\\Program Files (x86)\\Steam",
          "C:\\Program Files\\Steam",
          "D:\\Steam",
          "E:\\Steam"
        ],
        "process_name": "steam.exe"
      },
      "library_detection": {
        "type": "vdf",
        "file": "steamapps/libraryfolders.vdf",
        "games_folder": "steamapps/common"
      },
      "cache_paths": [
        "appcache",
        "depotcache",
        "steamapps/downloading"
      ]
    },
    {
      "name": "Epic Games",
      "detection": {
        "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\Epic Games\\EpicGamesLauncher",
        "registry_value": "AppDataPath",
        "fallback_paths": [
          "C:\\Program Files\\Epic Games",
          "D:\\Epic Games"
        ],
        "process_name": "EpicGamesLauncher.exe"
      },
      "library_detection": {
        "type": "manifests",
        "manifests_path": "C:\\ProgramData\\Epic\\EpicGamesLauncher\\Data\\Manifests",
        "manifest_extension": ".item"
      },
      "cache_paths": [
        "C:\\Users\\{user}\\AppData\\Local\\EpicGamesLauncher\\Saved"
      ]
    },
    {
      "name": "GOG Galaxy",
      "detection": {
        "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\GOG.com\\Games",
        "fallback_paths": [
          "C:\\Program Files (x86)\\GOG Galaxy",
          "C:\\GOG Games"
        ],
        "process_name": "GalaxyClient.exe"
      },
      "library_detection": {
        "type": "registry_games",
        "games_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\GOG.com\\Games"
      },
      "cache_paths": []
    },
    {
      "name": "Ubisoft Connect",
      "detection": {
        "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\Ubisoft\\Launcher",
        "registry_value": "InstallDir",
        "fallback_paths": [
          "C:\\Program Files (x86)\\Ubisoft\\Ubisoft Game Launcher"
        ],
        "process_name": "upc.exe"
      },
      "library_detection": {
        "type": "config_file",
        "config_path": "cache/configuration/configurations"
      },
      "cache_paths": [
        "cache"
      ]
    },
    {
      "name": "EA App",
      "detection": {
        "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Electronic Arts\\EA Desktop",
        "fallback_paths": [
          "C:\\Program Files\\Electronic Arts",
          "C:\\Program Files\\EA Games"
        ],
        "process_name": "EADesktop.exe"
      },
      "library_detection": {
        "type": "folder_scan",
        "default_path": "C:\\Program Files\\EA Games"
      },
      "cache_paths": [
        "C:\\Users\\{user}\\AppData\\Local\\Electronic Arts"
      ]
    },
    {
      "name": "Battle.net",
      "detection": {
        "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\Blizzard Entertainment\\Battle.net",
        "fallback_paths": [
          "C:\\Program Files (x86)\\Battle.net"
        ],
        "process_name": "Battle.net.exe"
      },
      "library_detection": {
        "type": "config_file",
        "config_path": "Battle.net.config"
      },
      "cache_paths": [
        "C:\\ProgramData\\Blizzard Entertainment\\Battle.net\\Cache"
      ]
    },
    {
      "name": "Xbox / Microsoft Store",
      "detection": {
        "default_path": "C:\\Program Files\\WindowsApps",
        "process_name": "XboxApp.exe"
      },
      "library_detection": {
        "type": "uwp_apps",
        "scan_windowsapps": true
      },
      "cache_paths": []
    },
    {
      "name": "Rockstar Games Launcher",
      "detection": {
        "registry_key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\Rockstar Games\\Launcher",
        "fallback_paths": [
          "C:\\Program Files\\Rockstar Games"
        ],
        "process_name": "LauncherPatcher.exe"
      },
      "library_detection": {
        "type": "folder_scan",
        "default_path": "C:\\Program Files\\Rockstar Games"
      },
      "cache_paths": []
    },
    {
      "name": "Amazon Games",
      "detection": {
        "fallback_paths": [
          "C:\\Amazon Games"
        ],
        "process_name": "Amazon Games.exe"
      },
      "library_detection": {
        "type": "folder_scan",
        "default_path": "C:\\Amazon Games\\Library"
      },
      "cache_paths": []
    }
  ]
}
```

---

## 2. known_services.json

Classification of Windows services for the Service Optimizer.

```json
{
  "critical_never_touch": [
    {
      "name": "RpcSs",
      "display": "Remote Procedure Call (RPC)",
      "reason": "Core Windows functionality - system will crash without it"
    },
    {
      "name": "DcomLaunch",
      "display": "DCOM Server Process Launcher",
      "reason": "Required for COM object activation"
    },
    {
      "name": "LSM",
      "display": "Local Session Manager",
      "reason": "Manages user sessions"
    },
    {
      "name": "SamSs",
      "display": "Security Accounts Manager",
      "reason": "Security - stores user account info"
    },
    {
      "name": "WinDefend",
      "display": "Windows Defender Antivirus Service",
      "reason": "System security"
    },
    {
      "name": "mpssvc",
      "display": "Windows Defender Firewall",
      "reason": "System security"
    },
    {
      "name": "eventlog",
      "display": "Windows Event Log",
      "reason": "System logging"
    },
    {
      "name": "PlugPlay",
      "display": "Plug and Play",
      "reason": "Device detection and management"
    },
    {
      "name": "Power",
      "display": "Power",
      "reason": "Power management"
    },
    {
      "name": "ProfSvc",
      "display": "User Profile Service",
      "reason": "User profiles"
    },
    {
      "name": "Schedule",
      "display": "Task Scheduler",
      "reason": "Many system tasks depend on this"
    },
    {
      "name": "LanmanWorkstation",
      "display": "Workstation",
      "reason": "Network connectivity"
    },
    {
      "name": "Dhcp",
      "display": "DHCP Client",
      "reason": "Network IP assignment"
    },
    {
      "name": "Dnscache",
      "display": "DNS Client",
      "reason": "Network name resolution"
    }
  ],
  "gaming_essential": [
    {
      "name": "Audiosrv",
      "display": "Windows Audio",
      "reason": "Game audio"
    },
    {
      "name": "AudioEndpointBuilder",
      "display": "Windows Audio Endpoint Builder",
      "reason": "Audio device management"
    },
    {
      "name": "HidServ",
      "display": "Human Interface Device Service",
      "reason": "Controller and input device support"
    },
    {
      "name": "XblAuthManager",
      "display": "Xbox Live Auth Manager",
      "reason": "Xbox/Microsoft game authentication"
    },
    {
      "name": "XboxGipSvc",
      "display": "Xbox Accessory Management Service",
      "reason": "Xbox controller support"
    },
    {
      "name": "NVDisplay.ContainerLocalSystem",
      "display": "NVIDIA Display Container LS",
      "reason": "NVIDIA GPU functionality"
    }
  ],
  "safe_to_disable": [
    {
      "name": "Spooler",
      "display": "Print Spooler",
      "reason": "Printing - disable if you don't print",
      "impact": "Cannot print documents",
      "savings": "Low RAM/CPU"
    },
    {
      "name": "Fax",
      "display": "Fax",
      "reason": "Fax functionality",
      "impact": "Cannot send/receive faxes",
      "savings": "Minimal"
    },
    {
      "name": "WSearch",
      "display": "Windows Search",
      "reason": "File indexing for fast search",
      "impact": "Slower file searches",
      "savings": "Medium CPU/Disk (especially on HDD)"
    },
    {
      "name": "SysMain",
      "display": "SysMain (Superfetch)",
      "reason": "Preloads frequently used apps",
      "impact": "Slightly slower app launches",
      "savings": "Medium RAM/Disk"
    },
    {
      "name": "DiagTrack",
      "display": "Connected User Experiences and Telemetry",
      "reason": "Microsoft telemetry/tracking",
      "impact": "None for user",
      "savings": "Low CPU/Network"
    },
    {
      "name": "dmwappushservice",
      "display": "Device Management Wireless Application Protocol",
      "reason": "WAP push messaging",
      "impact": "None for most users",
      "savings": "Minimal"
    },
    {
      "name": "RemoteRegistry",
      "display": "Remote Registry",
      "reason": "Remote registry editing",
      "impact": "None (security improvement)",
      "savings": "Minimal + security benefit"
    },
    {
      "name": "lfsvc",
      "display": "Geolocation Service",
      "reason": "Location tracking",
      "impact": "Apps can't get location",
      "savings": "Low"
    },
    {
      "name": "MapsBroker",
      "display": "Downloaded Maps Manager",
      "reason": "Windows Maps offline maps",
      "impact": "Windows Maps less functional",
      "savings": "Low"
    },
    {
      "name": "RetailDemo",
      "display": "Retail Demo Service",
      "reason": "Store demo mode",
      "impact": "None",
      "savings": "Minimal"
    },
    {
      "name": "WbioSrvc",
      "display": "Windows Biometric Service",
      "reason": "Fingerprint/face recognition",
      "impact": "Biometric login disabled",
      "savings": "Low"
    }
  ],
  "resource_hogs": [
    {
      "name": "SysMain",
      "display": "SysMain (Superfetch)",
      "impact": "High disk I/O, especially on HDD"
    },
    {
      "name": "WSearch",
      "display": "Windows Search",
      "impact": "High CPU/disk during indexing"
    },
    {
      "name": "DiagTrack",
      "display": "Telemetry",
      "impact": "Background CPU and network"
    },
    {
      "name": "wuauserv",
      "display": "Windows Update",
      "impact": "High when checking/downloading updates"
    }
  ]
}
```

---

## 3. game_signatures.json

Signatures for detecting game engines and installations.

```json
{
  "engines": {
    "Unity": {
      "files": [
        "UnityPlayer.dll",
        "UnityEngine.dll",
        "Mono/mono.dll"
      ],
      "folders": [
        "Managed",
        "Mono",
        "Resources"
      ],
      "typical_structure": {
        "required": ["UnityPlayer.dll"],
        "optional": ["*_Data/Managed/Assembly-CSharp.dll"]
      }
    },
    "Unreal Engine 4/5": {
      "files": [
        "UE4Game.exe",
        "UE5Game.exe",
        "*-Win64-Shipping.exe"
      ],
      "folders": [
        "Engine/Binaries",
        "Engine/Content"
      ],
      "typical_structure": {
        "required": ["Engine/Binaries/Win64"],
        "optional": ["Content/Paks"]
      }
    },
    "Source Engine": {
      "files": [
        "hl2.exe",
        "source_engine.dll",
        "engine.dll"
      ],
      "folders": [
        "hl2",
        "platform"
      ],
      "typical_structure": {
        "required": ["gameinfo.txt"],
        "optional": ["hl2/resource"]
      }
    },
    "CryEngine": {
      "files": [
        "CryGame.dll",
        "CrySystem.dll",
        "CryAction.dll"
      ],
      "folders": [
        "Engine",
        "GameData"
      ]
    },
    "Frostbite": {
      "files": [
        "*.toc",
        "*.sb"
      ],
      "folders": [
        "Data",
        "Update"
      ],
      "typical_structure": {
        "required": ["Data/Win32"],
        "optional": ["ModData"]
      }
    },
    "Game Maker Studio": {
      "files": [
        "data.win",
        "options.ini"
      ],
      "folders": [],
      "typical_structure": {
        "required": ["data.win"]
      }
    },
    "RPG Maker": {
      "files": [
        "Game.exe",
        "Game.ini"
      ],
      "folders": [
        "Audio/BGM",
        "Audio/SE",
        "Graphics"
      ],
      "typical_structure": {
        "required": ["Audio/BGM", "Graphics/Characters"]
      }
    },
    "Godot": {
      "files": [
        "*.pck",
        "godot.exe"
      ],
      "folders": []
    },
    "Ren'Py": {
      "files": [
        "renpy.exe",
        "lib/python*"
      ],
      "folders": [
        "game",
        "lib",
        "renpy"
      ]
    }
  },
  "generic_game_indicators": {
    "strong": [
      "saves",
      "save",
      "savegames",
      "SavedGames",
      "configs",
      "settings.ini",
      "config.ini",
      "game.exe",
      "launcher.exe"
    ],
    "medium": [
      "data",
      "assets",
      "resources",
      "content",
      "levels",
      "maps",
      "audio",
      "sound",
      "music",
      "video",
      "movies",
      "localization"
    ],
    "weak": [
      "bin",
      "binaries",
      "lib",
      "plugins"
    ]
  }
}
```

---

## 4. folder_names.json

Multi-language folder names where games are commonly installed.

```json
{
  "game_folders": {
    "english": [
      "Games",
      "Game",
      "My Games",
      "PC Games",
      "Gaming",
      "Video Games",
      "Computer Games"
    ],
    "arabic": [
      "العاب",
      "لعب",
      "الالعاب",
      "العاب اون لاين",
      "العاب الكمبيوتر",
      "العاب الفيديو",
      "العابي",
      "الألعاب",
      "ألعاب"
    ],
    "french": [
      "Jeux",
      "Mes Jeux",
      "Jeux Video"
    ],
    "german": [
      "Spiele",
      "Meine Spiele",
      "Computerspiele"
    ],
    "spanish": [
      "Juegos",
      "Mis Juegos",
      "Videojuegos"
    ],
    "italian": [
      "Giochi",
      "I Miei Giochi"
    ],
    "russian": [
      "Игры",
      "Мои Игры"
    ],
    "portuguese": [
      "Jogos",
      "Meus Jogos"
    ],
    "turkish": [
      "Oyunlar",
      "Oyun"
    ],
    "polish": [
      "Gry",
      "Moje Gry"
    ],
    "chinese_simplified": [
      "游戏",
      "我的游戏"
    ],
    "chinese_traditional": [
      "遊戲"
    ],
    "japanese": [
      "ゲーム"
    ],
    "korean": [
      "게임"
    ]
  },
  "scan_locations": {
    "root_level": true,
    "program_files": true,
    "program_files_x86": true,
    "user_documents": true,
    "user_desktop": true,
    "user_downloads": true
  }
}
```

---

## 5. hardware_database.json

CPU and GPU classification data for settings recommendations.

```json
{
  "cpu_tiers": {
    "ultra": {
      "keywords": [
        "i9-14", "i9-13", "i9-12",
        "Ryzen 9 7", "Ryzen 9 5950", "Ryzen 9 5900",
        "i7-14900", "i7-13900"
      ],
      "min_cores": 12,
      "description": "High-end CPU, no limitations"
    },
    "high": {
      "keywords": [
        "i7-14", "i7-13", "i7-12", "i7-11", "i7-10",
        "Ryzen 7 7", "Ryzen 7 5800", "Ryzen 7 5700",
        "i9-9", "i9-10", "i9-11"
      ],
      "min_cores": 8,
      "description": "Strong CPU, most games maxed"
    },
    "medium": {
      "keywords": [
        "i5-14", "i5-13", "i5-12", "i5-11", "i5-10",
        "Ryzen 5 7", "Ryzen 5 5600", "Ryzen 5 5500",
        "i7-8", "i7-9"
      ],
      "min_cores": 6,
      "description": "Good CPU, may limit in some games"
    },
    "low": {
      "keywords": [
        "i5-9", "i5-8", "i5-7", "i5-6",
        "Ryzen 5 3", "Ryzen 5 2", "Ryzen 5 1",
        "i3-12", "i3-10", "i3-9"
      ],
      "min_cores": 4,
      "description": "Entry-level, reduce CPU-heavy settings"
    },
    "very_low": {
      "keywords": [
        "i3-8", "i3-7", "i3-6",
        "Ryzen 3",
        "Pentium", "Celeron",
        "Athlon"
      ],
      "min_cores": 2,
      "description": "Limited CPU, minimize heavy settings"
    }
  },
  "gpu_tiers": {
    "ultra": {
      "keywords": [
        "RTX 4090", "RTX 4080",
        "RX 7900"
      ],
      "min_vram_gb": 16,
      "supports_rt": true,
      "description": "Top-tier GPU, max everything including RT"
    },
    "high": {
      "keywords": [
        "RTX 4070", "RTX 3090", "RTX 3080", "RTX 3070",
        "RX 7800", "RX 7700", "RX 6900", "RX 6800"
      ],
      "min_vram_gb": 10,
      "supports_rt": true,
      "description": "High-end GPU, high/ultra with selective RT"
    },
    "medium_high": {
      "keywords": [
        "RTX 4060", "RTX 3060 Ti", "RTX 3060",
        "RX 7600", "RX 6700", "RX 6650"
      ],
      "min_vram_gb": 8,
      "supports_rt": true,
      "description": "Good GPU, medium-high settings, light RT"
    },
    "medium": {
      "keywords": [
        "RTX 2060", "RTX 2070",
        "GTX 1080", "GTX 1070",
        "RX 6600", "RX 5700", "RX 5600"
      ],
      "min_vram_gb": 6,
      "supports_rt": false,
      "description": "Capable GPU, medium settings"
    },
    "low": {
      "keywords": [
        "GTX 1060", "GTX 1650", "GTX 1050",
        "RX 580", "RX 570", "RX 560",
        "GTX 970", "GTX 960"
      ],
      "min_vram_gb": 4,
      "supports_rt": false,
      "description": "Entry-level, low-medium settings"
    },
    "very_low": {
      "keywords": [
        "GT 1030", "GT 730", "GT 710",
        "Intel UHD", "Intel HD", "Intel Iris",
        "AMD Radeon Graphics",
        "RX 550", "RX 460"
      ],
      "min_vram_gb": 2,
      "supports_rt": false,
      "description": "Minimal GPU, low settings required"
    }
  },
  "ram_tiers": {
    "high": {
      "min_gb": 32,
      "description": "Plenty of RAM, no concerns"
    },
    "standard": {
      "min_gb": 16,
      "description": "Good for most games"
    },
    "limited": {
      "min_gb": 8,
      "description": "May limit texture streaming"
    },
    "insufficient": {
      "min_gb": 0,
      "description": "Will cause issues in modern games"
    }
  }
}
```

---

## 6. settings_profiles.json

Game settings recommendations by profile type.

```json
{
  "profiles": {
    "competitive": {
      "name": "Competitive",
      "description": "Maximum FPS, minimum input lag",
      "target": "144+ FPS",
      "settings": {
        "resolution": "native_or_lower",
        "resolution_scale": 100,
        "vsync": "off",
        "frame_cap": "monitor_refresh",
        "texture_quality": "medium",
        "shadow_quality": "low",
        "shadow_distance": "low",
        "anti_aliasing": "off_or_fxaa",
        "ambient_occlusion": "off",
        "reflections": "off",
        "volumetric_effects": "off",
        "post_processing": "low",
        "view_distance": "medium",
        "foliage_density": "low",
        "effects_quality": "low",
        "motion_blur": "off",
        "depth_of_field": "off",
        "film_grain": "off",
        "chromatic_aberration": "off",
        "ray_tracing": "off"
      }
    },
    "balanced": {
      "name": "Balanced",
      "description": "Good visuals with stable 60 FPS",
      "target": "60 FPS stable",
      "settings": {
        "resolution": "native",
        "resolution_scale": 100,
        "vsync": "optional",
        "frame_cap": "60_or_uncapped",
        "texture_quality": "high",
        "shadow_quality": "medium",
        "shadow_distance": "medium",
        "anti_aliasing": "taa",
        "ambient_occlusion": "medium",
        "reflections": "medium",
        "volumetric_effects": "medium",
        "post_processing": "medium",
        "view_distance": "high",
        "foliage_density": "medium",
        "effects_quality": "medium",
        "motion_blur": "optional",
        "depth_of_field": "optional",
        "film_grain": "off",
        "chromatic_aberration": "off",
        "ray_tracing": "off"
      }
    },
    "visual_quality": {
      "name": "Visual Quality",
      "description": "Best visuals, accept 30+ FPS",
      "target": "30+ FPS",
      "settings": {
        "resolution": "native_or_higher",
        "resolution_scale": 100,
        "vsync": "on",
        "frame_cap": "30_or_60",
        "texture_quality": "ultra",
        "shadow_quality": "high",
        "shadow_distance": "high",
        "anti_aliasing": "taa_or_msaa",
        "ambient_occlusion": "high",
        "reflections": "high",
        "volumetric_effects": "high",
        "post_processing": "high",
        "view_distance": "ultra",
        "foliage_density": "high",
        "effects_quality": "high",
        "motion_blur": "optional",
        "depth_of_field": "on",
        "film_grain": "optional",
        "chromatic_aberration": "optional",
        "ray_tracing": "if_available"
      }
    },
    "low_end_survival": {
      "name": "Low-End Survival",
      "description": "Playable 30+ FPS on weak hardware",
      "target": "30 FPS minimum",
      "settings": {
        "resolution": "below_native",
        "resolution_scale": 75,
        "vsync": "off",
        "frame_cap": "30",
        "texture_quality": "low",
        "shadow_quality": "low",
        "shadow_distance": "low",
        "anti_aliasing": "off",
        "ambient_occlusion": "off",
        "reflections": "off",
        "volumetric_effects": "off",
        "post_processing": "off",
        "view_distance": "low",
        "foliage_density": "low",
        "effects_quality": "low",
        "motion_blur": "off",
        "depth_of_field": "off",
        "film_grain": "off",
        "chromatic_aberration": "off",
        "ray_tracing": "off"
      }
    },
    "laptop_safe": {
      "name": "Laptop Safe",
      "description": "Stable FPS, managed thermals",
      "target": "60 FPS capped, cool temps",
      "settings": {
        "resolution": "native",
        "resolution_scale": 100,
        "vsync": "on",
        "frame_cap": "60",
        "texture_quality": "medium",
        "shadow_quality": "medium",
        "shadow_distance": "medium",
        "anti_aliasing": "fxaa",
        "ambient_occlusion": "low",
        "reflections": "low",
        "volumetric_effects": "low",
        "post_processing": "medium",
        "view_distance": "medium",
        "foliage_density": "medium",
        "effects_quality": "medium",
        "motion_blur": "off",
        "depth_of_field": "off",
        "film_grain": "off",
        "chromatic_aberration": "off",
        "ray_tracing": "off"
      },
      "notes": [
        "Frame cap prevents thermal throttling",
        "V-Sync reduces power draw",
        "Consider gaming on a cooling pad"
      ]
    }
  },
  "setting_categories": {
    "cpu_heavy": [
      "view_distance",
      "foliage_density",
      "npc_density",
      "physics_quality",
      "simulation_quality",
      "ai_quality",
      "draw_distance"
    ],
    "gpu_heavy": [
      "resolution",
      "resolution_scale",
      "shadow_quality",
      "reflection_quality",
      "anti_aliasing",
      "post_processing",
      "ambient_occlusion",
      "volumetric_effects",
      "ray_tracing"
    ],
    "vram_heavy": [
      "texture_quality",
      "texture_filtering",
      "model_detail",
      "asset_streaming"
    ]
  }
}
```

---

## 7. suspicious_patterns.json

Patterns for detecting potentially problematic processes.

```json
{
  "suspicious_patterns": {
    "crypto_miners": {
      "process_names": [
        "xmrig", "nicehash", "phoenixminer", "trex",
        "nbminer", "gminer", "lolminer", "ethminer"
      ],
      "behavior": {
        "high_gpu_idle": true,
        "consistent_gpu_usage": true
      },
      "warning": "Process pattern matches cryptocurrency mining software. Please verify this is intentional."
    },
    "known_bloatware": {
      "process_names": [
        "mcafee", "norton", "avast", "avg",
        "weatherbug", "bonzi", "conduit"
      ],
      "warning": "Common bloatware/unwanted software detected. Consider removal if not needed."
    },
    "high_resource_unknown": {
      "behavior": {
        "cpu_over": 20,
        "gpu_over": 10,
        "ram_over_mb": 500,
        "no_window": true
      },
      "warning": "Unknown process using significant resources without visible window. Please verify."
    }
  },
  "known_safe_high_usage": [
    "System",
    "dwm.exe",
    "csrss.exe",
    "MsMpEng.exe",
    "svchost.exe",
    "explorer.exe",
    "SearchIndexer.exe"
  ],
  "rgb_software": {
    "process_names": [
      "icue", "corsair", "razer", "synapse",
      "armourycrate", "asus", "nzxt", "cam",
      "rgbfusion", "gigabyte", "msi", "dragonc"
    ],
    "note": "RGB software can use significant RAM. Safe but optional during gaming."
  },
  "overlay_software": {
    "process_names": [
      "discord", "discordptb", "discordcanary",
      "nvidia share", "shadowplay", "geforce experience",
      "obs", "obs64", "obs-studio",
      "fraps", "msi afterburner", "rtss",
      "xbox game bar", "gamebar"
    ],
    "note": "Multiple overlays can cause conflicts. Recommend using only one at a time."
  }
}
```

---

## 8. known_apps.json

Application classification for the App Scanner.

```json
{
  "categories": {
    "gaming_essential": {
      "apps": [
        "Steam", "Epic Games Launcher", "GOG Galaxy",
        "Ubisoft Connect", "EA App", "Battle.net",
        "Discord", "Xbox App"
      ],
      "verdict": "Useful for gaming",
      "action": "keep"
    },
    "gaming_utilities": {
      "apps": [
        "MSI Afterburner", "EVGA Precision", "AMD Adrenalin",
        "NVIDIA GeForce Experience", "RivaTuner Statistics",
        "HWiNFO", "CPU-Z", "GPU-Z"
      ],
      "verdict": "Useful gaming utilities",
      "action": "keep"
    },
    "potentially_heavy": {
      "apps": [
        "iCUE", "Razer Synapse", "Logitech G HUB",
        "NZXT CAM", "Armoury Crate", "RGB Fusion",
        "Dragon Center", "Mystic Light"
      ],
      "verdict": "RGB/peripheral software - uses RAM but may be wanted",
      "action": "review",
      "note": "Consider closing during gaming for better performance"
    },
    "known_bloatware": {
      "apps": [
        "McAfee", "Norton", "Avira",
        "WildTangent Games", "Candy Crush",
        "Booking.com", "ExpressVPN Offers"
      ],
      "verdict": "Manufacturer bloatware",
      "action": "consider_removal",
      "note": "Pre-installed software that most users don't need"
    },
    "fake_optimizers": {
      "apps": [
        "Driver Booster", "Driver Easy", "IObit",
        "CCleaner", "Registry Cleaner", "PC Optimizer",
        "System Mechanic", "MyCleanPC", "RegCure"
      ],
      "verdict": "Often does more harm than good",
      "action": "review",
      "note": "These tools are often unnecessary and can cause issues"
    },
    "adware_risk": {
      "apps": [
        "Ask Toolbar", "Conduit", "Babylon",
        "Mindspark", "Search Protect"
      ],
      "verdict": "Likely unwanted/adware",
      "action": "recommend_removal",
      "note": "Known problematic software"
    }
  },
  "never_flag_as_suspicious": [
    "Windows Defender", "Microsoft Edge", "Chrome", "Firefox",
    "Visual Studio", "VS Code", "Office", "OneDrive",
    "Steam", "Epic", "GOG", "Discord",
    "NVIDIA", "AMD", "Intel", "Realtek"
  ]
}
```

---

## 9. repair_commands.json

Definitions for all repair commands.

```json
{
  "repairs": {
    "sfc_scan": {
      "name": "System File Checker",
      "command": "sfc /scannow",
      "requires_admin": true,
      "risk": "low",
      "duration": "10-15 minutes",
      "description": "Scans and repairs corrupted Windows system files",
      "creates_snapshot": false
    },
    "dism_restore": {
      "name": "DISM Restore Health",
      "command": "DISM /Online /Cleanup-Image /RestoreHealth",
      "requires_admin": true,
      "risk": "low",
      "duration": "15-30 minutes",
      "description": "Repairs the Windows system image",
      "creates_snapshot": false
    },
    "chkdsk_scan": {
      "name": "Check Disk",
      "command": "chkdsk C: /scan",
      "requires_admin": true,
      "risk": "low",
      "duration": "5-10 minutes",
      "description": "Scans disk for file system errors",
      "creates_snapshot": false
    },
    "flush_dns": {
      "name": "Flush DNS Cache",
      "command": "ipconfig /flushdns",
      "requires_admin": false,
      "risk": "none",
      "duration": "instant",
      "description": "Clears the DNS resolver cache",
      "creates_snapshot": false
    },
    "reset_winsock": {
      "name": "Reset Winsock",
      "command": "netsh winsock reset",
      "requires_admin": true,
      "risk": "low",
      "duration": "instant",
      "description": "Resets Windows Sockets catalog",
      "reboot_required": true,
      "creates_snapshot": true
    },
    "reset_ip": {
      "name": "Reset TCP/IP Stack",
      "command": "netsh int ip reset",
      "requires_admin": true,
      "risk": "low",
      "duration": "instant",
      "description": "Resets TCP/IP stack to default",
      "reboot_required": true,
      "creates_snapshot": true
    },
    "clear_temp": {
      "name": "Clear Temp Files",
      "paths": [
        "%TEMP%",
        "C:\\Windows\\Temp"
      ],
      "requires_admin": true,
      "risk": "none",
      "duration": "1-5 minutes",
      "description": "Deletes temporary files",
      "creates_snapshot": false
    },
    "clear_prefetch": {
      "name": "Clear Prefetch",
      "paths": [
        "C:\\Windows\\Prefetch"
      ],
      "requires_admin": true,
      "risk": "low",
      "duration": "instant",
      "description": "Clears Windows prefetch cache",
      "note": "First boot after may be slightly slower",
      "creates_snapshot": false
    },
    "enable_game_mode": {
      "name": "Enable Game Mode",
      "registry": {
        "key": "HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\GameBar",
        "value": "AllowAutoGameMode",
        "data": 1,
        "type": "REG_DWORD"
      },
      "requires_admin": false,
      "risk": "none",
      "duration": "instant",
      "description": "Enables Windows Game Mode",
      "creates_snapshot": false
    },
    "high_performance_power": {
      "name": "Set High Performance Power Plan",
      "command": "powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
      "requires_admin": true,
      "risk": "none",
      "duration": "instant",
      "description": "Switches to High Performance power plan",
      "creates_snapshot": false
    }
  }
}
```

---

## 10. known_conflicts.json

Known software conflicts that can cause gaming issues.

```json
{
  "overlay_conflicts": {
    "description": "Multiple overlays can cause crashes and performance issues",
    "groups": [
      {
        "name": "Game Overlays",
        "processes": [
          "GameOverlayUI.exe",
          "DiscordHook64.dll",
          "nvcontainer.exe",
          "GameBar.exe",
          "RTSS.exe"
        ],
        "recommendation": "Use only one overlay at a time"
      }
    ]
  },
  "antivirus_conflicts": {
    "description": "Some antivirus software can interfere with games",
    "known_issues": [
      {
        "software": "Avast",
        "issue": "Game Shield can cause lag",
        "solution": "Add game folders to exclusions"
      },
      {
        "software": "Norton",
        "issue": "Real-time scanning impacts performance",
        "solution": "Enable Silent Mode during gaming"
      },
      {
        "software": "McAfee",
        "issue": "High resource usage",
        "solution": "Consider Windows Defender instead"
      }
    ]
  },
  "recording_conflicts": {
    "description": "Multiple recording software can conflict",
    "software": [
      "OBS Studio",
      "NVIDIA ShadowPlay",
      "AMD ReLive",
      "Xbox Game Bar Recording",
      "Fraps",
      "Bandicam"
    ],
    "recommendation": "Use only one recording software at a time"
  },
  "rgb_software_conflicts": {
    "description": "RGB software from different brands may conflict",
    "groups": [
      ["iCUE", "SignalRGB"],
      ["Razer Synapse", "OpenRGB"],
      ["Armoury Crate", "third-party RGB"]
    ],
    "recommendation": "Use one RGB control solution"
  }
}
```

---

## Data File Creation

When initializing the application, create these files if they don't exist:

```python
def initialize_data_files(data_dir):
    """Create default data files if they don't exist"""
    import json
    from pathlib import Path

    data_path = Path(data_dir)
    data_path.mkdir(exist_ok=True)

    default_files = {
        'known_launchers.json': KNOWN_LAUNCHERS_DATA,
        'known_services.json': KNOWN_SERVICES_DATA,
        'game_signatures.json': GAME_SIGNATURES_DATA,
        'folder_names.json': FOLDER_NAMES_DATA,
        'hardware_database.json': HARDWARE_DATABASE_DATA,
        'settings_profiles.json': SETTINGS_PROFILES_DATA,
        'suspicious_patterns.json': SUSPICIOUS_PATTERNS_DATA,
        'known_apps.json': KNOWN_APPS_DATA,
        'repair_commands.json': REPAIR_COMMANDS_DATA,
        'known_conflicts.json': KNOWN_CONFLICTS_DATA,
    }

    for filename, data in default_files.items():
        filepath = data_path / filename
        if not filepath.exists():
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
```
