# GameFix Doctor Pro - Feature Specifications

## Table of Contents
1. [Quick Health Check](#1-quick-health-check)
2. [Full System Scan](#2-full-system-scan)
3. [Auto-Fix Wizard](#3-auto-fix-wizard)
4. [Find My Games](#4-find-my-games)
5. [Diagnose Problems](#5-diagnose-problems)
6. [Repair Center](#6-repair-center)
7. [Service Optimizer](#7-service-optimizer)
8. [Process Killer](#8-process-killer)
9. [App Scanner](#9-app-scanner)
10. [Settings Advisor](#10-settings-advisor)
11. [Network Doctor](#11-network-doctor)
12. [Driver Check](#12-driver-check)
13. [Power Optimizer](#13-power-optimizer)
14. [Snapshots & Rollback](#14-snapshots--rollback)
15. [Reports](#15-reports)
16. [Settings](#16-settings)

---

## 1. Quick Health Check

**Purpose:** Fast 30-second overview of system gaming readiness.

**What It Checks:**
| Check | Good | Warning | Bad |
|-------|------|---------|-----|
| Free Disk Space (C:) | >50GB | 20-50GB | <20GB |
| Free RAM | >4GB available | 2-4GB | <2GB |
| CPU Temperature | <70°C | 70-85°C | >85°C |
| GPU Temperature | <75°C | 75-90°C | >90°C |
| CPU Usage | <30% idle | 30-60% | >60% idle |
| GPU Usage (idle) | <10% | 10-30% | >30% |
| Windows Updates | Up to date | Updates pending | Update errors |
| Antivirus Status | Active | Unknown | Disabled |
| Power Plan | High Performance | Balanced | Power Saver |
| Game Mode | Enabled | - | Disabled |

**Output Format:**
```
╔═══════════════════════════════════════════════════════════════╗
║                    QUICK HEALTH CHECK                         ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  [OK]     Disk Space: 234 GB free on C:                       ║
║  [OK]     RAM: 12.4 GB available of 16 GB                     ║
║  [WARN]   CPU Temp: 72°C - Running a bit warm                 ║
║  [OK]     GPU Temp: 45°C                                      ║
║  [OK]     CPU Usage: 8% idle                                  ║
║  [OK]     GPU Usage: 2% idle                                  ║
║  [WARN]   Power Plan: Balanced - Switch to High Performance?  ║
║  [OK]     Game Mode: Enabled                                  ║
║                                                               ║
║  Overall Score: 8/10 - Good shape, minor tweaks suggested     ║
║                                                               ║
║  [1] Fix warnings now    [2] See details    [0] Back          ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 2. Full System Scan

**Purpose:** Deep 2-5 minute analysis of everything gaming-related.

**Scan Categories:**

### Hardware Analysis
- CPU: Model, cores, threads, base/boost clock, current usage, temperature
- GPU: Model, VRAM, driver version, current usage, temperature
- RAM: Total, available, speed, single/dual channel detection
- Storage: All drives, type (SSD/HDD), free space, health status
- Display: Resolution, refresh rate, HDR support
- Form Factor: Laptop vs Desktop detection

### Software Analysis
- Windows version and build
- DirectX version
- Visual C++ Redistributables installed
- .NET Framework versions
- Game Mode and gaming features status
- Xbox Game Bar status
- Installed games (full detection)
- Installed launchers

### Performance Analysis
- Top 10 RAM consumers
- Top 10 CPU consumers
- GPU background usage
- Startup programs count and impact
- Running services count
- Background processes analysis

### Health Analysis
- Windows integrity (SFC needed?)
- Disk errors
- Driver issues
- Pending updates
- Temp file bloat size
- Registry issues (basic)

**Output:** Summary screen + option to see each category in detail

---

## 3. Auto-Fix Wizard

**Purpose:** One-click optimization for first-time users or quick tune-ups.

**Flow:**
```
STEP 1: Create Safety Snapshot
    └── Automatic Windows Restore Point
    └── Save current service states
    └── Save current settings

STEP 2: Scan Everything
    └── Run full system scan
    └── Identify all issues
    └── Classify by risk level

STEP 3: Show Fix Plan
    ┌─────────────────────────────────────────────────────────────┐
    │              AUTO-FIX WIZARD - FIX PLAN                     │
    ├─────────────────────────────────────────────────────────────┤
    │                                                             │
    │  Found 12 issues. Here's what I recommend:                  │
    │                                                             │
    │  SAFE FIXES (Auto-apply): ──────────────────────────────    │
    │  [✓] Clear 4.2 GB temp files                                │
    │  [✓] Clear DNS cache                                        │
    │  [✓] Enable Game Mode                                       │
    │  [✓] Set Power Plan to High Performance                     │
    │  [✓] Disable 3 useless startup programs                     │
    │                                                             │
    │  RECOMMENDED FIXES (Need your OK): ─────────────────────    │
    │  [ ] Stop 5 unnecessary services (show list)                │
    │  [ ] Close 3 background RAM hogs (show list)                │
    │  [ ] Run Windows repair (SFC scan)                          │
    │                                                             │
    │  OPTIONAL (Your choice): ───────────────────────────────    │
    │  [ ] Disable Xbox Game Bar (saves resources)                │
    │  [ ] Reduce visual effects (faster UI)                      │
    │                                                             │
    │  [1] Apply Safe Fixes Only                                  │
    │  [2] Apply Safe + Recommended                               │
    │  [3] Customize (choose each fix)                            │
    │  [0] Cancel - Don't change anything                         │
    └─────────────────────────────────────────────────────────────┘

STEP 4: Apply Fixes
    └── Show progress for each fix
    └── Report success/failure for each

STEP 5: Summary
    └── What was fixed
    └── What failed (if any)
    └── How to rollback if needed
```

**Categories:**
| Category | User Permission | Risk Level |
|----------|-----------------|------------|
| Safe Fixes | Auto-apply (inform user) | None |
| Recommended | Ask permission | Low |
| Optional | Ask permission | Low-Medium |
| Advanced | Explicit confirmation | Medium |
| Never Auto | Always manual only | High |

---

## 4. Find My Games

**Purpose:** Detect all installed games, not just launcher-based ones.

### Detection Layers

**Layer 1: Launcher Libraries**
| Launcher | Detection Method |
|----------|------------------|
| Steam | Read libraryfolders.vdf |
| Epic Games | Read manifests in ProgramData |
| GOG Galaxy | Read database/config |
| Ubisoft Connect | Read configurations |
| EA App | Read local data |
| Battle.net | Read product database |
| Xbox/Microsoft | Read WindowsApps |
| Rockstar | Read launcher data |
| Amazon Games | Read local storage |

**Layer 2: Folder Scanning**

Scan these locations on ALL drives:
```
Root level:
/Games
/Game
/My Games
/PC Games
/العاب
/لعب
/الالعاب
/العاب اون لاين
/العاب الكمبيوتر

Program Files:
/Program Files/
/Program Files (x86)/

User folders:
/Users/{user}/Games
/Users/{user}/Desktop (shortcuts)
/Users/{user}/Downloads (game installers)
```

**Layer 3: Game Signatures**

Detect by file patterns:
| Engine/Type | Signature Files |
|-------------|-----------------|
| Unity | UnityPlayer.dll, data/Managed/*.dll |
| Unreal Engine | UE4Game.exe, Engine/Binaries |
| Source Engine | hl2.exe, source_engine.dll |
| Game Maker | data.win, options.ini |
| RPG Maker | Game.exe + Audio/BGM folder |
| Godot | .pck files |
| Generic | .exe + save folder + config files |

**Layer 4: Shortcut Analysis**
- Scan Desktop shortcuts (.lnk)
- Scan Start Menu shortcuts
- Extract target paths
- Identify game executables

**Output Format:**
```
╔═══════════════════════════════════════════════════════════════╗
║                    DETECTED GAMES                             ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Found 47 games across your system:                           ║
║                                                               ║
║  STEAM (23 games):                                            ║
║    • Counter-Strike 2                    [142 GB] D:\Steam    ║
║    • Cyberpunk 2077                      [68 GB]  D:\Steam    ║
║    • ...                                                      ║
║                                                               ║
║  EPIC GAMES (8 games):                                        ║
║    • Fortnite                            [95 GB]  E:\Epic     ║
║    • ...                                                      ║
║                                                               ║
║  STANDALONE (12 games):                                       ║
║    • Minecraft                           [2.1 GB] C:\Games    ║
║    • League of Legends                   [23 GB]  D:\العاب    ║
║    • ...                                                      ║
║                                                               ║
║  SHORTCUTS (4 games):                                         ║
║    • FIFA 24                             [Desktop shortcut]   ║
║    • ...                                                      ║
║                                                               ║
║  [1] View full list    [2] Check game health    [0] Back      ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 5. Diagnose Problems

**Purpose:** Find common gaming problems and their causes.

### Problem Categories

**A. Performance Problems**
| Issue | Detection | Severity |
|-------|-----------|----------|
| High CPU idle usage | >20% when idle | Medium |
| High GPU idle usage | >10% when idle | Medium |
| Low available RAM | <2GB free | High |
| Memory leak detected | Process growing over time | Medium |
| Thermal throttling | Temp >90°C + clock drop | High |
| Background crypto miner | GPU usage pattern | Critical |

**B. Stability Problems**
| Issue | Detection | Severity |
|-------|-----------|----------|
| Corrupted system files | SFC scan result | High |
| Driver crashes logged | Event log analysis | High |
| Pending Windows updates | Update API check | Low |
| Disk errors | SMART + chkdsk | High |
| Low disk space for games | <10GB on game drives | Medium |

**C. Launch Problems**
| Issue | Detection | Severity |
|-------|-----------|----------|
| Missing DirectX | DX version check | High |
| Missing VC++ Redist | Check installed versions | High |
| Missing .NET | Check installed versions | Medium |
| Antivirus blocking | Exclusion check | Medium |
| Missing admin rights | Manifest check | Low |

**D. Network Problems**
| Issue | Detection | Severity |
|-------|-----------|----------|
| High ping baseline | >100ms to common servers | Medium |
| DNS issues | Resolution test | Medium |
| Packet loss | Ping test | High |
| WiFi instead of Ethernet | Adapter type | Low |
| VPN active | Adapter detection | Info |

**E. Configuration Problems**
| Issue | Detection | Severity |
|-------|-----------|----------|
| Game Mode disabled | Registry check | Low |
| Wrong power plan | Power API | Low |
| Hardware scheduling off | Registry check | Low |
| Too many overlays | Process detection | Medium |
| Conflicting software | Known conflict list | Medium |

---

## 6. Repair Center

**Purpose:** Fix common Windows gaming issues safely.

### Available Repairs

**Category: System Integrity**
| Repair | Command | Risk | Admin |
|--------|---------|------|-------|
| Scan System Files | `sfc /scannow` | Low | Yes |
| Repair Windows Image | `DISM /Online /Cleanup-Image /RestoreHealth` | Low | Yes |
| Check Disk | `chkdsk /scan` | Low | Yes |
| Reset Windows Update | Service restart + clear cache | Medium | Yes |

**Category: Cleanup**
| Repair | Action | Risk | Admin |
|--------|--------|------|-------|
| Clear Windows Temp | Delete %TEMP% contents | None | No |
| Clear System Temp | Delete C:\Windows\Temp | None | Yes |
| Clear Prefetch | Delete Prefetch folder | Low | Yes |
| Clear Launcher Caches | Clear Steam/Epic/etc cache | Low | No |
| Clear Shader Cache | Delete DX/GL shader cache | Low | No |
| Disk Cleanup | Run cleanmgr silently | None | Yes |

**Category: Network**
| Repair | Command | Risk | Admin |
|--------|---------|------|-------|
| Flush DNS | `ipconfig /flushdns` | None | No |
| Reset Winsock | `netsh winsock reset` | Low | Yes |
| Reset IP Stack | `netsh int ip reset` | Low | Yes |
| Reset Firewall | `netsh advfirewall reset` | Medium | Yes |

**Category: Gaming Features**
| Repair | Action | Risk | Admin |
|--------|--------|------|-------|
| Enable Game Mode | Registry + Settings | None | No |
| Enable HAGS | Registry change | Low | Yes |
| Disable Xbox Game Bar | Registry change | Low | No |
| Optimize Visual Effects | System settings | None | No |
| Set High Performance | Power plan change | None | Yes |

**Category: Runtimes**
| Repair | Action | Risk | Admin |
|--------|--------|------|-------|
| Repair DirectX | Download and run dxwebsetup | Low | Yes |
| Repair VC++ All | Repair all installed versions | Low | Yes |
| Install Missing VC++ | Download and install missing | Low | Yes |

### Repair Flow
```
1. User selects repair
2. Show what will happen
3. Show risk level
4. Create snapshot (if Medium+ risk)
5. Ask for confirmation
6. Run repair with progress
7. Show result
8. Offer to run related repairs
```

---

## 7. Service Optimizer

**Purpose:** Identify and manage services that waste resources.

### Service Classifications

**CRITICAL - Never Touch:**
- Windows core services
- Security services (Defender, firewall)
- Driver services (GPU, audio, network)
- Storage services
- User login services

**GAMING ESSENTIAL - Keep Running:**
- Audio services (AudioSrv, AudioEndpointBuilder)
- GPU services (NVIDIA, AMD, Intel)
- Input services (HID, Xbox peripherals)
- Network services (DHCP, DNS Client)

**SAFE TO DISABLE - User Choice:**
| Service | Purpose | Impact When Disabled |
|---------|---------|---------------------|
| Print Spooler | Printing | Can't print |
| Fax | Faxing | Can't fax |
| Bluetooth Support | Bluetooth | No Bluetooth |
| Windows Search | File indexing | Slower search, less CPU |
| SysMain (Superfetch) | Preloading | Slower app launch, less RAM |
| DiagTrack | Telemetry | No telemetry |
| Connected User Experiences | Telemetry | No telemetry |

**REVIEW NEEDED - Analyze First:**
- Third-party services
- Manufacturer services
- Unknown services

### Gaming Mode Feature
```
GAMING MODE
├── Save current service states
├── Stop non-essential services temporarily
├── Run game
├── Restore all services after game closes

Benefits:
- More RAM available
- Less CPU interrupts
- Easy rollback (automatic)
```

---

## 8. Process Killer

**Purpose:** Find and stop processes wasting RAM/CPU/GPU.

### Detection Methods

**RAM Hogs:**
- List processes by memory usage
- Flag >500MB as "notable"
- Flag >1GB as "heavy"
- Identify browser tabs (Chrome, Edge, Firefox)
- Identify known heavy apps (Photoshop, After Effects, etc.)

**CPU Hogs:**
- List by CPU usage over 30 seconds
- Flag >10% sustained as "notable"
- Flag >25% sustained as "heavy"
- Identify crypto miners by pattern

**GPU Hogs:**
- List by GPU usage
- Flag >5% idle usage as "suspicious"
- Identify hardware video decode
- Identify rendering apps

### Process Categories
| Category | Action | Examples |
|----------|--------|----------|
| Critical System | Never kill | csrss, wininit, services |
| Protected | Warn strongly | Explorer, Defender |
| Browser | Safe to close | Chrome, Firefox, Edge |
| Launcher | Usually safe | Steam, Epic (if game closed) |
| Background App | Safe to close | Spotify, Discord (if not needed) |
| Unknown Heavy | Review | Unknown high-usage processes |
| Suspicious | Warn user | Crypto miners, unknown GPU users |

### Output Format
```
╔═══════════════════════════════════════════════════════════════╗
║                    PROCESS KILLER                             ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  TOP RAM USERS:                                               ║
║  ┌─────────────────────────────────────────────────────────┐  ║
║  │ # │ Process          │ RAM     │ Status    │ Action    │  ║
║  ├───┼──────────────────┼─────────┼───────────┼───────────┤  ║
║  │ 1 │ chrome.exe (12)  │ 3.2 GB  │ Heavy     │ [Close?]  │  ║
║  │ 2 │ Discord.exe      │ 890 MB  │ Notable   │ [Close?]  │  ║
║  │ 3 │ Spotify.exe      │ 456 MB  │ Normal    │ [Close?]  │  ║
║  │ 4 │ wallpaper_eng    │ 1.1 GB  │ Heavy     │ [Close?]  │  ║
║  └─────────────────────────────────────────────────────────┘  ║
║                                                               ║
║  Total closeable RAM: ~5.6 GB                                 ║
║                                                               ║
║  [1] Close selected    [2] Close all heavy    [0] Back        ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 9. App Scanner

**Purpose:** Analyze installed software for gaming impact.

### Analysis Categories

**A. Gaming Related**
- Game launchers (useful)
- Game utilities (useful/bloat)
- Overlay software (potential conflicts)
- Recording software (resource usage)
- Voice chat (Discord, TeamSpeak)

**B. System Impact**
| Category | Examples | Concern |
|----------|----------|---------|
| Heavy Background | iCUE, Razer Synapse, NZXT CAM | RAM/CPU hogs |
| Auto-start | Many apps starting at boot | Slow startup |
| Duplicate Function | Multiple RGB software | Conflicts |
| Outdated | Old software versions | Security |

**C. Potentially Unwanted**
| Type | Detection | Risk |
|------|-----------|------|
| Adware | Known signatures | Medium |
| Bloatware | Manufacturer pre-installs | Low |
| Toolbars | Browser toolbars | Medium |
| "Optimizers" | Fake system optimizers | Medium |

**D. Suspicious (Never claim malware)**
| Indicator | What We Say |
|-----------|-------------|
| Unknown + high resource | "Unknown app using high resources - review recommended" |
| Hidden process | "Background process with no visible window - verify if intended" |
| Crypto miner pattern | "GPU usage pattern similar to mining software - please verify" |

**Important:** We NEVER claim something is malware. We flag for review and suggest the user check with proper antivirus.

---

## 10. Settings Advisor

**Purpose:** Recommend optimal game settings based on hardware.

### Hardware Analysis

**CPU Classification:**
| Class | Examples | Profile Impact |
|-------|----------|----------------|
| Ultra | i9-14900K, R9 7950X | All max |
| High | i7-13700K, R7 7800X3D | Most high |
| Medium | i5-13400, R5 7600 | Mixed |
| Low | i3, R3, older i5/i7 | Reduce CPU-heavy |
| Very Low | Old dual/quad core | Minimize |

**GPU Classification:**
| Class | Examples | VRAM | Profile Impact |
|-------|----------|------|----------------|
| Ultra | RTX 4090, 4080 | 16GB+ | All max + RT |
| High | RTX 4070, 3080, 7900 | 10-12GB | High + selective RT |
| Medium | RTX 4060, 3060, 6700 | 8GB | Medium-High |
| Low | GTX 1060, 1650 | 4-6GB | Medium-Low |
| Very Low | GT 1030, iGPU | 2-4GB | Low |

**RAM Impact:**
| Amount | Impact |
|--------|--------|
| 32GB+ | No concerns |
| 16GB | Standard |
| 8GB | May limit streaming textures |
| <8GB | Significant limitations |

**Storage Impact:**
| Type | Impact |
|------|--------|
| NVMe SSD | Best load times, high texture streaming |
| SATA SSD | Good load times |
| HDD | Slow loads, texture pop-in |

**Form Factor:**
| Type | Consideration |
|------|---------------|
| Desktop | Full performance |
| Laptop | Thermal limits, battery |

### Settings Categories

**CPU-Heavy Settings:**
- Crowd/NPC density
- Physics simulation
- Draw distance (partial)
- AI complexity
- Destructible environments

**GPU-Heavy Settings:**
- Resolution
- Ray tracing
- Anti-aliasing quality
- Shadow quality
- Reflection quality
- Post-processing effects

**VRAM-Heavy Settings:**
- Texture quality
- Texture filtering
- Asset streaming quality
- Model detail (LOD)

### Profiles

**1. Competitive**
- Target: Maximum FPS, minimum input lag
- Resolution: Native or lower
- All effects: Low/Off
- V-Sync: Off
- Frame cap: Monitor refresh rate

**2. Balanced**
- Target: Good visuals + stable 60 FPS
- Resolution: Native
- Effects: Medium
- V-Sync: Optional
- Frame cap: 60 or uncapped

**3. Visual Quality**
- Target: Best visuals, accept 30+ FPS
- Resolution: Native or higher
- Effects: High/Ultra
- V-Sync: On
- RT: If available

**4. Low-End Survival**
- Target: Playable 30+ FPS
- Resolution: Below native
- Effects: Low/Off
- V-Sync: Off
- Reduce resolution scale

**5. Laptop Safe**
- Target: Stable FPS, manage thermals
- Frame cap: 60 FPS
- Effects: Medium
- Thermal headroom prioritized

### Output Example
```
╔═══════════════════════════════════════════════════════════════╗
║                    SETTINGS ADVISOR                           ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  YOUR HARDWARE:                                               ║
║  • CPU: Intel i5-12400 (MEDIUM class)                         ║
║  • GPU: RTX 3060 (MEDIUM-HIGH class, 12GB VRAM)               ║
║  • RAM: 16GB DDR4                                             ║
║  • Display: 1920x1080 @ 144Hz                                 ║
║  • Type: Desktop                                              ║
║                                                               ║
║  RECOMMENDED SETTINGS:                                        ║
║  ┌─────────────────────────────────────────────────────────┐  ║
║  │ Setting              │ Competitive │ Balanced │ Visual  │  ║
║  ├──────────────────────┼─────────────┼──────────┼─────────┤  ║
║  │ Resolution           │ 1080p       │ 1080p    │ 1080p   │  ║
║  │ Texture Quality      │ Medium      │ High     │ Ultra   │  ║
║  │ Shadow Quality       │ Low         │ Medium   │ High    │  ║
║  │ Anti-Aliasing        │ Off/FXAA    │ TAA      │ TAA     │  ║
║  │ View Distance        │ Medium      │ High     │ Ultra   │  ║
║  │ Effects              │ Low         │ Medium   │ High    │  ║
║  │ Ray Tracing          │ Off         │ Off      │ Low     │  ║
║  │ Frame Cap            │ 144         │ 60-144   │ 60      │  ║
║  │ V-Sync               │ Off         │ Optional │ On      │  ║
║  └─────────────────────────────────────────────────────────┘  ║
║                                                               ║
║  Note: Your GPU has plenty of VRAM. Texture quality can go    ║
║  high without FPS impact. CPU may limit high crowd settings.  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## 11. Network Doctor

**Purpose:** Diagnose and fix network issues affecting gaming.

### Diagnostics

**Connection Type:**
- Ethernet vs WiFi detection
- Adapter speed (100Mbps, 1Gbps, etc.)
- Connection quality

**DNS Analysis:**
- Current DNS servers
- Resolution speed test
- Compare with gaming DNS (Cloudflare 1.1.1.1, Google 8.8.8.8)

**Latency Test:**
- Ping to common game servers
- Ping to major regions (US, EU, Asia)
- Jitter measurement
- Packet loss test

**Network Adapter Settings:**
- Check for gaming optimizations
- Interrupt moderation
- Receive side scaling
- Energy saving settings

### Fixes Available

| Fix | Action | Impact |
|-----|--------|--------|
| Flush DNS | Clear DNS cache | Fixes stale DNS |
| Change DNS | Set Cloudflare/Google | Often faster |
| Reset Stack | Reset TCP/IP | Fixes corruption |
| Disable WiFi Power Save | Adapter setting | Better latency |
| Disable Nagle | Registry tweak | Slightly lower latency |

---

## 12. Driver Check

**Purpose:** Ensure drivers are healthy and up-to-date.

### Checks

**GPU Driver:**
- Current version installed
- Compare with latest available (basic check)
- Driver age
- Known problematic versions warning

**Audio Driver:**
- Realtek/manufacturer version
- Known issues

**Network Driver:**
- Adapter driver version
- Age and potential issues

**Chipset:**
- Intel/AMD chipset driver status

### Output
```
GPU Driver:  NVIDIA 551.23 (3 months old) - UPDATE AVAILABLE
Audio:       Realtek 6.0.9235.1 - OK
Network:     Intel I225-V 1.0.2.8 - OK
Chipset:     Intel 10.1.19444.8378 - OK

[1] Open GPU driver download page
[2] Check all for updates
[0] Back
```

---

## 13. Power Optimizer

**Purpose:** Set optimal power settings for gaming.

### Detection

**Current State:**
- Active power plan
- Laptop vs Desktop
- On battery vs plugged in
- Current power settings

### Recommendations

| Situation | Recommendation |
|-----------|----------------|
| Desktop | High Performance or Ultimate Performance |
| Laptop (plugged) | High Performance |
| Laptop (battery) | Balanced (preserve battery) |
| Laptop (gaming) | Temporary High Performance |

### Optimizations

**Power Plan Settings:**
- Processor minimum: 100% (gaming)
- Hard disk turn off: Never
- USB selective suspend: Disabled
- PCI Express power: Off

---

## 14. Snapshots & Rollback

**Purpose:** Safety net before making changes.

### Snapshot Types

**Windows Restore Point:**
- Uses Windows System Restore
- Created before risky repairs
- Named: "GameFix Doctor - {date} - {action}"

**Service State Snapshot:**
- Save all service states to JSON
- Restore service states exactly

**Settings Snapshot:**
- Registry keys changed
- Power plans
- Custom settings

### Snapshot Storage
```
snapshots/
├── 2024-01-15_143022_pre_repair/
│   ├── info.json           # Snapshot metadata
│   ├── services.json       # Service states
│   ├── registry.json       # Changed registry keys
│   └── notes.txt           # What was about to happen
```

### Rollback Flow
```
1. Show available snapshots
2. User selects snapshot
3. Show what will be restored
4. Confirm
5. Restore step by step
6. Report result
```

---

## 15. Reports

**Purpose:** Generate shareable reports of system state and actions.

### Report Types

**Health Report:**
- Full system information
- All detected issues
- Recommendations
- Export: TXT, HTML

**Action Report:**
- What was changed
- When
- By which feature
- Success/failure status

**Game List Report:**
- All detected games
- Location
- Size
- Launcher

### Export Formats
- TXT (simple, shareable)
- HTML (formatted, professional)
- JSON (for advanced users)

---

## 16. Settings

**Purpose:** Configure the tool itself.

### Options

| Setting | Options | Default |
|---------|---------|---------|
| Create snapshots before repairs | Always/Ask/Never | Always |
| Auto-scan on startup | Yes/No | No |
| Theme | Colors/Minimal | Colors |
| Report location | Path | ./reports |
| Snapshot location | Path | ./snapshots |
| Check for updates | Yes/No | Yes |
| Show advanced options | Yes/No | No |

---

## Credits Section

**About GameFix Doctor Pro:**
```
╔═══════════════════════════════════════════════════════════════╗
║                         ABOUT                                 ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  GameFix Doctor Pro v1.0                                      ║
║  Your PC's Gaming Health Expert                               ║
║                                                               ║
║  Developed by: Sayed Elmahdy                                  ║
║                                                               ║
║  Contact:                                                     ║
║  • Facebook: [To be added]                                    ║
║  • LinkedIn: [To be added]                                    ║
║  • Email:    [To be added]                                    ║
║                                                               ║
║  This tool is designed to help gamers optimize their          ║
║  Windows PC safely and effectively.                           ║
║                                                               ║
║  No cheats. No hacks. No BS. Just real optimization.          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```
