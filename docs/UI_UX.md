# GameFix Doctor Pro - UI/UX Guidelines

## Design Philosophy

### Core Principles

1. **Feel Like a Real Tool, Not AI-Generated**
   - Natural language, not robotic
   - Personality without being annoying
   - Direct and clear, not verbose
   - A gamer helping gamers

2. **Beginner-Friendly but Not Dumbed Down**
   - Explain what things do in simple terms
   - Show technical details for those who want them
   - Never make the user feel stupid

3. **Premium Feel**
   - Clean, consistent formatting
   - Proper box drawing characters
   - Color coding that makes sense
   - Professional without being corporate

4. **Trust and Safety**
   - Always explain what will happen
   - Show risk levels clearly
   - Confirm before impactful actions
   - Make undo easy

---

## Color Scheme

### Status Colors

| Color | Usage | Meaning |
|-------|-------|---------|
| Green | [OK], Success | All good, healthy |
| Yellow | [WARN], Caution | Pay attention, not critical |
| Red | [FAIL], Error, Exit | Problem, needs action |
| Cyan | Headers, Menu numbers | Navigation, emphasis |
| Blue | [INFO], Tips | Information, suggestions |
| White | Normal text | Default content |

### Color Codes (Colorama)

```python
from colorama import Fore, Style

GREEN = Fore.GREEN      # Success, OK
YELLOW = Fore.YELLOW    # Warning
RED = Fore.RED          # Error, Fail
CYAN = Fore.CYAN        # Headers, menu
BLUE = Fore.BLUE        # Info
WHITE = Fore.WHITE      # Normal
RESET = Style.RESET_ALL # Reset
```

---

## Typography and Layout

### Box Drawing Characters

Use these for consistent UI:

```
Corners:  ╔ ╗ ╚ ╝
Sides:    ║ ═
Joins:    ╠ ╣ ╦ ╩ ╬
Light:    ┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼
```

### Standard Header Box

```
╔═══════════════════════════════════════════════════════════════╗
║                    SECTION TITLE HERE                         ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Content goes here...                                         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

### Standard Width
- Fixed width: 65 characters
- This works well on most CMD windows
- Content padded with 2 spaces from edges

---

## Status Indicators

### Text Status Tags

```
[OK]     - All good (green)
[WARN]   - Warning, attention needed (yellow)
[FAIL]   - Failed, problem (red)
[INFO]   - Information (blue)
[....]   - In progress, loading (cyan)
[SKIP]   - Skipped (gray/white)
```

### Visual Checkmarks

```
[✓] Completed successfully
[✗] Failed
[○] Not started / Pending
[●] In progress
[ ] Optional / Unchecked
```

### Severity Indicators

```
Risk Level:
  ● LOW    - Safe, no worries
  ● MEDIUM - Some caution needed
  ● HIGH   - Confirm before proceeding
  ● NONE   - Completely safe

Impact:
  Minor   - Small change
  Normal  - Standard change
  Major   - Significant change
```

---

## Menu System

### Main Menu Format

```
╔═══════════════════════════════════════════════════════════════╗
║              GAMEFIX DOCTOR PRO v1.0                          ║
║              Your PC's Gaming Health Expert                   ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║   [1]  Quick Health Check      Fast 30-second checkup         ║
║   [2]  Full System Scan        Deep analysis                  ║
║   [3]  Auto-Fix Wizard         One-click optimization         ║
║   ─────────────────────────────────────────────────────────   ║
║   [4]  Find My Games           Detect installed games         ║
║   [5]  Diagnose Problems       Find what's wrong              ║
║   [6]  Repair Center           Fix Windows issues             ║
║   ─────────────────────────────────────────────────────────   ║
║   [7]  Service Optimizer       Stop useless services          ║
║   [8]  Process Killer          Kill RAM/GPU hogs              ║
║   [9]  App Scanner             Check installed software       ║
║   ─────────────────────────────────────────────────────────   ║
║  [10]  Settings Advisor        Best game settings             ║
║  [11]  Network Doctor          Fix connection issues          ║
║  [12]  Driver Check            Check driver health            ║
║  [13]  Power Optimizer         Best power settings            ║
║   ─────────────────────────────────────────────────────────   ║
║  [14]  Snapshots & Rollback    Backup and restore             ║
║  [15]  Reports                 View and export reports        ║
║  [16]  Settings                Tool configuration             ║
║                                                               ║
║   [0]  Exit                                                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

Your choice:
```

### Sub-Menu Format

```
╔═══════════════════════════════════════════════════════════════╗
║                    REPAIR CENTER                              ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  System Integrity:                                            ║
║   [1]  Scan System Files (SFC)           Risk: LOW            ║
║   [2]  Repair Windows Image (DISM)       Risk: LOW            ║
║   [3]  Check Disk Health                 Risk: LOW            ║
║                                                               ║
║  Cleanup:                                                     ║
║   [4]  Clear Temp Files                  Risk: NONE           ║
║   [5]  Clear Shader Cache                Risk: NONE           ║
║   [6]  Disk Cleanup                      Risk: NONE           ║
║                                                               ║
║  Network:                                                     ║
║   [7]  Flush DNS Cache                   Risk: NONE           ║
║   [8]  Reset Network Stack               Risk: LOW            ║
║                                                               ║
║   [0]  Back to Main Menu                                      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## Progress Indicators

### Progress Bar

```
Scanning system files...
[████████████████████░░░░░░░░░░░░░░░░░░░░] 52%

Completed!
[████████████████████████████████████████] 100%
```

### Step Progress

```
Auto-Fix Wizard - Step 2 of 5

  [✓] Step 1: Create safety snapshot
  [●] Step 2: Scanning system...
  [○] Step 3: Show fix plan
  [○] Step 4: Apply fixes
  [○] Step 5: Summary
```

### Spinner (for indeterminate progress)

```
Analyzing... |
Analyzing... /
Analyzing... -
Analyzing... \
```

---

## Messages and Prompts

### Confirmation Prompt

```
╔═══════════════════════════════════════════════════════════════╗
║                    CONFIRM ACTION                             ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  You are about to: Run System File Checker (SFC)              ║
║                                                               ║
║  What this does:                                              ║
║  • Scans all Windows system files                             ║
║  • Repairs any corrupted files found                          ║
║  • Takes about 10-15 minutes                                  ║
║                                                               ║
║  Risk Level: LOW                                              ║
║  Reversible: Yes (Windows keeps backups)                      ║
║                                                               ║
║  [Y] Yes, proceed    [N] No, cancel                           ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

Proceed? (y/n):
```

### Success Message

```
  [OK]     System File Checker completed successfully.
           No integrity violations found.

  Press Enter to continue...
```

### Warning Message

```
  [WARN]   Found 3 issues during scan.

           • 2 corrupted files were repaired
           • 1 file could not be repaired (see log)

           A full report has been saved.

  Press Enter to continue...
```

### Error Message

```
  [FAIL]   System File Checker encountered an error.

           Error: Access denied. This operation requires
           administrator privileges.

           Solution: Please restart the tool as administrator.

  Press Enter to continue...
```

---

## Tables

### Simple Table

```
  Name                 │ Value
  ─────────────────────┼──────────────────────
  CPU                  │ Intel Core i7-12700K
  GPU                  │ NVIDIA RTX 3080
  RAM                  │ 32 GB DDR5
  Storage              │ 1 TB NVMe SSD
```

### Status Table

```
  Component      │ Status  │ Details
  ───────────────┼─────────┼─────────────────────────────
  Disk Space     │ [OK]    │ 234 GB free on C:
  RAM Available  │ [OK]    │ 12.4 GB of 16 GB
  CPU Temp       │ [WARN]  │ 72°C - Running warm
  GPU Temp       │ [OK]    │ 45°C
  Power Plan     │ [WARN]  │ Balanced (not optimal)
```

### Process Table

```
  #  │ Process              │ RAM      │ Status    │ Action
  ───┼──────────────────────┼──────────┼───────────┼─────────
   1 │ chrome.exe (12 tabs) │ 3.2 GB   │ Heavy     │ [Close?]
   2 │ Discord.exe          │ 890 MB   │ Notable   │ [Close?]
   3 │ Spotify.exe          │ 456 MB   │ Normal    │ [Close?]
   4 │ wallpaper_engine.exe │ 1.1 GB   │ Heavy     │ [Close?]
```

---

## Language and Tone

### Do's

- **Be direct:** "Your GPU driver is outdated" not "We have detected that the graphics processing unit driver software may potentially be out of date"
- **Be helpful:** "This usually fixes launch crashes" not "This may or may not help"
- **Be honest:** "This might take 10 minutes" not "This will be quick"
- **Be human:** "Looking good!" not "All checks passed successfully"

### Don'ts

- Don't be condescending: "Even beginners can do this!" ❌
- Don't be robotic: "Process completed. Status: Success." ❌
- Don't oversell: "ULTIMATE FPS BOOST!" ❌
- Don't blame: "You broke something" ❌

### Example Phrases

**Good:**
- "Found 47 games on your system"
- "Your PC is ready for gaming"
- "This will clear old junk files to free up space"
- "I'll create a backup first, just in case"
- "Something went wrong. Here's what happened..."

**Bad:**
- "47 games have been successfully detected by our scanning algorithm"
- "Your personal computer has passed all gaming readiness checks"
- "This procedure will eliminate unnecessary temporary data"
- "A system restore point will be created for safety purposes"
- "An unexpected error has occurred. Error code: 0x80004005"

---

## Screen Flow Examples

### Startup Screen

```

    ██████╗  █████╗ ███╗   ███╗███████╗███████╗██╗██╗  ██╗
   ██╔════╝ ██╔══██╗████╗ ████║██╔════╝██╔════╝██║╚██╗██╔╝
   ██║  ███╗███████║██╔████╔██║█████╗  █████╗  ██║ ╚███╔╝
   ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  ██╔══╝  ██║ ██╔██╗
   ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗██║     ██║██╔╝ ██╗
    ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝

             ██████╗  ██████╗  ██████╗████████╗ ██████╗ ██████╗
             ██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗
             ██║  ██║██║   ██║██║        ██║   ██║   ██║██████╔╝
             ██║  ██║██║   ██║██║        ██║   ██║   ██║██╔══██╗
             ██████╔╝╚██████╔╝╚██████╗   ██║   ╚██████╔╝██║  ██║
             ╚═════╝  ╚═════╝  ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝

                        PRO v1.0

              Your PC's Gaming Health Expert

             Developed by: Sayed Elmahdy

  Initializing...
```

### Quick Health Check Result

```
╔═══════════════════════════════════════════════════════════════╗
║                    QUICK HEALTH CHECK                         ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  System: Windows 11 Pro (Build 22621)                         ║
║  Type:   Desktop                                              ║
║                                                               ║
║  ─────────────────────────────────────────────────────────    ║
║                                                               ║
║  [OK]     Disk Space        234 GB free on C:                 ║
║  [OK]     RAM Available     12.4 GB of 16 GB (22% used)       ║
║  [WARN]   CPU Temperature   72°C - A bit warm                 ║
║  [OK]     GPU Temperature   45°C                              ║
║  [OK]     CPU Idle Usage    8%                                ║
║  [OK]     GPU Idle Usage    2%                                ║
║  [OK]     Game Mode         Enabled                           ║
║  [WARN]   Power Plan        Balanced - Not optimal            ║
║  [OK]     Antivirus         Windows Defender active           ║
║  [OK]     Windows Updates   Up to date                        ║
║                                                               ║
║  ─────────────────────────────────────────────────────────    ║
║                                                               ║
║  Overall: 8/10 - Good shape!                                  ║
║                                                               ║
║  Suggestions:                                                 ║
║  • Consider switching to High Performance power plan          ║
║  • CPU running warm - check cooling if this persists          ║
║                                                               ║
║  [1] Fix warnings now    [2] Full scan    [0] Back            ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

Your choice:
```

### Game Detection Result

```
╔═══════════════════════════════════════════════════════════════╗
║                    DETECTED GAMES                             ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Found 47 games across your system!                           ║
║                                                               ║
║  ─────────────────────────────────────────────────────────    ║
║                                                               ║
║  STEAM (23 games)                                             ║
║  ├─ Counter-Strike 2                    [29 GB]  D:\Steam     ║
║  ├─ Cyberpunk 2077                      [68 GB]  D:\Steam     ║
║  ├─ Elden Ring                          [45 GB]  D:\Steam     ║
║  ├─ ... and 20 more                                           ║
║                                                               ║
║  EPIC GAMES (8 games)                                         ║
║  ├─ Fortnite                            [95 GB]  E:\Epic      ║
║  ├─ GTA V                               [105 GB] E:\Epic      ║
║  ├─ ... and 6 more                                            ║
║                                                               ║
║  STANDALONE (12 games)                                        ║
║  ├─ Minecraft                           [2.1 GB] C:\Games     ║
║  ├─ League of Legends                   [23 GB]  D:\العاب     ║
║  ├─ Valorant                            [25 GB]  D:\Games     ║
║  ├─ ... and 9 more                                            ║
║                                                               ║
║  SHORTCUTS (4 games)                                          ║
║  ├─ FIFA 24                             [Desktop]             ║
║  ├─ ... and 3 more                                            ║
║                                                               ║
║  Total Size: ~1.2 TB                                          ║
║                                                               ║
║  [1] View full list    [2] Check game health    [0] Back      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## Accessibility Considerations

### Color Blind Friendly
- Never use color alone to convey information
- Always include text labels: [OK], [WARN], [FAIL]
- Status is clear even in monochrome

### Screen Reader Friendly
- Clear, linear text flow
- No reliance on visual positioning alone
- Descriptions provided for all actions

### Keyboard Navigation
- Number-based menu selection
- No mouse required
- Clear input prompts

---

## Loading States

### For Quick Operations (< 2 seconds)

```
  Checking... done!
```

### For Medium Operations (2-30 seconds)

```
  Scanning system files...
  [████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 30%
```

### For Long Operations (> 30 seconds)

```
  Running System File Checker...

  This takes about 10-15 minutes. You can minimize this window
  and keep using your PC.

  Progress: [████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 20%
  Time elapsed: 2:34
  Estimated remaining: ~8 minutes

  Currently checking: C:\Windows\System32\drivers\...
```

---

## About Screen

```
╔═══════════════════════════════════════════════════════════════╗
║                         ABOUT                                 ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  GameFix Doctor Pro                                           ║
║  Version 1.0.0                                                ║
║                                                               ║
║  Your PC's Gaming Health Expert                               ║
║                                                               ║
║  ─────────────────────────────────────────────────────────    ║
║                                                               ║
║  Developed by: Sayed Elmahdy                                  ║
║                                                               ║
║  Connect with me:                                             ║
║  • Facebook:  [To be added]                                   ║
║  • LinkedIn:  [To be added]                                   ║
║  • Email:     [To be added]                                   ║
║                                                               ║
║  ─────────────────────────────────────────────────────────    ║
║                                                               ║
║  This tool helps gamers optimize their Windows PC safely.     ║
║  No cheats. No hacks. No fake "FPS boost" tricks.             ║
║  Just real diagnostics and safe repairs.                      ║
║                                                               ║
║  [0] Back                                                     ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## Error Recovery

### When Something Goes Wrong

```
╔═══════════════════════════════════════════════════════════════╗
║                    OOPS! SOMETHING WENT WRONG                 ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  The repair didn't complete as expected.                      ║
║                                                               ║
║  What happened:                                               ║
║  A system file was locked by another program.                 ║
║                                                               ║
║  What you can try:                                            ║
║  1. Close other programs and try again                        ║
║  2. Restart your PC and run this repair first                 ║
║  3. Run the tool as Administrator                             ║
║                                                               ║
║  Your system is safe - no changes were made.                  ║
║                                                               ║
║  [1] Try again    [2] View error details    [0] Back          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```
