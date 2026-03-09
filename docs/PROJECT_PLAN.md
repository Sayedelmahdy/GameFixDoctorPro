# GameFix Doctor Pro - Project Plan

## Project Identity

**Name:** GameFix Doctor Pro
**Type:** Windows CMD Tool for Gamers
**Language:** Python 3.8+
**Distribution:** Portable EXE (PyInstaller)
**Target:** Windows 10/11 (basic support for Windows 7/8.1)
**Admin:** Auto-request UAC elevation
**UI Language:** English only

---

## Project Purpose

A professional, safe, and beginner-friendly tool that helps gamers:
- Diagnose system and game problems
- Fix common Windows gaming issues
- Optimize services and background processes
- Get smart game settings recommendations
- Keep their system safe with snapshots and rollback

---

## Core Philosophy

1. **Safe First** - Never break the user's system. Always create restore points before changes.
2. **Honest** - Never claim certainty when uncertain. Mark suspicious items as "needs review" not "malware".
3. **Reversible** - Every major action can be undone via snapshots.
4. **No Bullshit** - No fake "FPS boost" tweaks. Only real, tested optimizations.
5. **Gamer-Friendly** - Written by gamers, for gamers. No corporate jargon.

---

## Folder Structure

```
GameFix Doctor Pro/
├── gamefix_doctor.py           # Main entry point
├── requirements.txt            # Python dependencies
│
├── core/
│   ├── __init__.py
│   ├── ui.py                   # Menu system, colors, display helpers
│   ├── config.py               # App settings and constants
│   ├── utils.py                # Shared utility functions
│   └── admin.py                # Admin elevation handling
│
├── modules/
│   ├── __init__.py
│   ├── system_info.py          # Hardware/software detection
│   ├── game_detector.py        # Find games (launchers + folders + signatures)
│   ├── health_check.py         # Quick health check
│   ├── full_scan.py            # Deep system scan
│   ├── diagnosis.py            # Problem diagnosis engine
│   ├── repairs.py              # Windows gaming fixes
│   ├── services.py             # Service optimizer
│   ├── process_manager.py      # RAM/GPU hog killer
│   ├── app_checker.py          # Installed app analyzer
│   ├── settings_recommender.py # Game settings AI
│   ├── network.py              # Network diagnostics and fixes
│   ├── drivers.py              # Driver health checker
│   ├── power.py                # Power plan optimizer
│   ├── snapshots.py            # Backup and rollback system
│   ├── reports.py              # Report generator
│   ├── auto_fix.py             # One-click auto-fix wizard
│   └── settings.py             # App settings manager
│
├── data/
│   ├── known_launchers.json    # Steam, Epic, GOG, etc.
│   ├── known_services.json     # Service classifications
│   ├── known_apps.json         # App risk classifications
│   ├── game_signatures.json    # Game engine signatures
│   ├── folder_names.json       # Game folder names (multi-language)
│   ├── settings_profiles.json  # Game settings presets
│   └── suspicious_patterns.json # Suspicious process patterns
│
├── snapshots/                  # User snapshots stored here
│   └── .gitkeep
│
└── docs/
    ├── PROJECT_PLAN.md         # This file
    ├── FEATURES.md             # Feature specifications
    ├── TECHNICAL.md            # Technical implementation
    ├── UI_UX.md                # Interface guidelines
    ├── DATA_SPECS.md           # Data structure specs
    ├── SAFETY_RULES.md         # Safety requirements
    └── AUTO_FIX_FLOW.md        # Auto-fix wizard spec
```

---

## Main Menu Structure

```
╔═══════════════════════════════════════════════════════════════╗
║              GAMEFIX DOCTOR PRO v1.0                          ║
║              Your PC's Gaming Health Expert                   ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║   [1]  Quick Health Check      - Fast 30-second checkup       ║
║   [2]  Full System Scan        - Deep analysis (2-5 min)      ║
║   [3]  Auto-Fix Wizard    *NEW - One-click optimization       ║
║   [4]  Find My Games           - Detect all installed games   ║
║   [5]  Diagnose Problems       - Find what's wrong            ║
║   [6]  Repair Center           - Fix Windows gaming issues    ║
║   [7]  Service Optimizer       - Stop useless services        ║
║   [8]  Process Killer          - Kill RAM/GPU hogs            ║
║   [9]  App Scanner             - Check installed software     ║
║  [10]  Settings Advisor        - Best game settings for you   ║
║  [11]  Network Doctor          - Fix connection issues        ║
║  [12]  Driver Check            - Check driver health          ║
║  [13]  Power Optimizer         - Set best power plan          ║
║  [14]  Snapshots & Rollback    - Backup and restore           ║
║  [15]  Reports                 - View and export reports      ║
║  [16]  Settings                - Tool configuration           ║
║   [0]  Exit                                                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## Feature Priority Levels

### P0 - Must Have (Core)
- System info detection
- Quick health check
- Game detection (launchers + folders + Arabic)
- Basic repairs (SFC, DISM, temp cleanup)
- Snapshots before changes
- Service analyzer
- Process killer

### P1 - Important
- Auto-Fix Wizard (one-click)
- Full diagnosis engine
- Game settings recommender
- Network diagnostics
- Driver checker
- Reports

### P2 - Nice to Have
- Power optimizer
- Detailed app scanner
- Advanced rollback

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.8+ |
| System Info | WMI, psutil, platform |
| Admin Check | ctypes (Windows API) |
| Colors | colorama |
| Registry | winreg |
| Processes | psutil, subprocess |
| Packaging | PyInstaller |

---

## Dependencies (requirements.txt)

```
psutil>=5.9.0
wmi>=1.5.1
colorama>=0.4.6
pywin32>=305
GPUtil>=1.4.0
```

---

## Author Information

**Developer:** Sayed Elmahdy
**Contact:** (To be added)
- Facebook: (To be added)
- LinkedIn: (To be added)
- Email: (To be added)

---

## Version History

| Version | Status | Notes |
|---------|--------|-------|
| 1.0.0 | Planned | Initial release |

---

## Next Steps

1. Read FEATURES.md for detailed feature specs
2. Read TECHNICAL.md for implementation details
3. Read UI_UX.md for interface guidelines
4. Read DATA_SPECS.md for data structures
5. Read SAFETY_RULES.md for safety requirements
6. Read AUTO_FIX_FLOW.md for auto-fix wizard
