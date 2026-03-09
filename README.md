# GameFix Doctor Pro

**Your PC's Gaming Health Expert**

A professional, safe, and beginner-friendly Windows CMD tool that helps gamers diagnose problems, optimize their system, and get the best gaming experience.

---

## Features

| Feature | Description |
|---------|-------------|
| Quick Health Check | 30-second system overview |
| Full System Scan | Deep analysis of everything gaming-related |
| Auto-Fix Wizard | One-click optimization with safety backup |
| Smart Game Detection | Finds all games (launchers + folders + Arabic support) |
| Problem Diagnosis | Identifies common gaming issues |
| Repair Center | Safe Windows repairs (SFC, DISM, cleanup) |
| Service Optimizer | Stop useless services, keep gaming essentials |
| Process Killer | Find and close RAM/GPU hogs |
| App Scanner | Check installed software for issues |
| Settings Advisor | Hardware-based game settings recommendations |
| Network Doctor | Fix connection and ping issues |
| Driver Check | Verify driver health |
| Power Optimizer | Set optimal power plan |
| Snapshots & Rollback | Safety backups before any changes |
| Reports | Exportable system reports |

---

## Safety First

This tool follows strict safety rules:
- Creates backups before making changes
- Never touches critical Windows services
- Always asks before impactful actions
- Never claims certainty about malware
- No cheats, no hacks, no risky "FPS boost" tricks

---

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or higher
- Administrator privileges (for repairs)

---

## Installation

1. Clone or download this repository.
2. Run:
   ```bat
   install.cmd
   ```
3. Open a new CMD and run:
   ```bat
   gamedoctor
   ```

Manual alternative:
```bat
python -m pip install --user .
gamedoctor
```

Runtime data location (installed mode):
- `%LOCALAPPDATA%\GameFixDoctorPro\`
- Override with `GAMEFIX_HOME`
- Portable mode in current folder: `set GAMEFIX_PORTABLE=1`

After winget approval, installation will also be:
```bat
winget install SayedElmahdy.GameFixDoctorPro
```

For publishing steps, see:
- `docs/WINGET_PUBLISH.md`

---

## Building EXE

To create a standalone executable:

```bash
pip install pyinstaller
pyinstaller --onefile --console --uac-admin --name GameFixDoctorPro gamefix_doctor.py
```

The EXE will be in the `dist` folder.

Easy mode:
```bat
build.cmd 1.0.0
```

---

## Documentation

All documentation is in the `docs/` folder:

| Document | Description |
|----------|-------------|
| PROJECT_PLAN.md | Overall architecture and structure |
| FEATURES.md | Detailed feature specifications |
| TECHNICAL.md | Implementation guidelines |
| UI_UX.md | Interface and design guidelines |
| DATA_SPECS.md | Data structures and JSON databases |
| SAFETY_RULES.md | Safety requirements and rules |
| AUTO_FIX_FLOW.md | Auto-Fix Wizard specification |
| WINGET_PUBLISH.md | How to publish/update on winget |

---

## Project Structure

```
GameFix Doctor Pro/
├── gamefix_doctor.py       # Main entry point
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
├── core/                   # Core modules
│   ├── ui.py               # Menu and display
│   ├── config.py           # Configuration
│   ├── utils.py            # Utilities
│   └── admin.py            # Admin elevation
│
├── modules/                # Feature modules
│   ├── system_info.py      # Hardware detection
│   ├── game_detector.py    # Game finding
│   ├── health_check.py     # Health checks
│   ├── repairs.py          # Windows repairs
│   ├── services.py         # Service management
│   ├── process_manager.py  # Process control
│   ├── auto_fix.py         # Auto-Fix Wizard
│   └── ...                 # Other modules
│
├── data/                   # JSON databases
│   ├── known_launchers.json
│   ├── known_services.json
│   └── ...
│
├── snapshots/              # User backups
├── reports/                # Generated reports
└── docs/                   # Documentation
```

---

## Developer

**Sayed Elmahdy**

- GitHub: https://github.com/Sayedelmahdy
- LinkedIn: https://www.linkedin.com/in/sayed-elmahdy365/
- Email: sayed.work223@gmail.com

---

## Philosophy

- **Safe First** - Never break the user's system
- **Honest** - Never claim certainty when uncertain
- **Reversible** - Every action can be undone
- **No BS** - Only real, tested optimizations
- **Gamer-Friendly** - Made by gamers, for gamers

---

## License

[To be specified]

---

## Disclaimer

This tool modifies Windows settings and services. While every effort has been made to ensure safety, use at your own risk. Always ensure you have backups of important data.
