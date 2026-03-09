# GameFix Doctor Pro - Auto-Fix Wizard

## Overview

The Auto-Fix Wizard is the **flagship feature** for first-time users and quick tune-ups. It handles everything automatically while keeping the user informed and in control.

**Philosophy:** Do the right thing automatically, but always ask before doing anything impactful.

---

## User Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    AUTO-FIX WIZARD                              │
│                                                                 │
│  This wizard will scan your PC, find gaming issues, and        │
│  fix them safely. A backup will be created first.              │
│                                                                 │
│  [1] Start Auto-Fix Wizard                                      │
│  [2] What does this do? (More info)                             │
│  [0] Back                                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

User selects [1]

                              ↓

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  STEP 1 OF 5: Creating Safety Backup                            │
│                                                                 │
│  Before making any changes, I'll create a backup so you can    │
│  undo everything if needed.                                     │
│                                                                 │
│  Creating Windows Restore Point...    [████████████░░░░] 60%    │
│  Saving current settings...           [Waiting...]              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

                              ↓

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  STEP 1 OF 5: Creating Safety Backup                            │
│                                                                 │
│  [OK] Windows Restore Point created                             │
│  [OK] Service states saved                                      │
│  [OK] Settings backed up                                        │
│                                                                 │
│  Backup ID: 2024-01-15_143022_AutoFix                          │
│  You can restore this anytime from Snapshots menu.              │
│                                                                 │
│  Press Enter to continue to scanning...                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

                              ↓

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  STEP 2 OF 5: Scanning Your System                              │
│                                                                 │
│  [✓] Checking disk space...                                     │
│  [✓] Checking RAM usage...                                      │
│  [✓] Checking CPU/GPU temps...                                  │
│  [●] Checking Windows health...                                 │
│  [ ] Checking services...                                       │
│  [ ] Checking startup programs...                               │
│  [ ] Checking background processes...                           │
│  [ ] Checking gaming settings...                                │
│  [ ] Checking network...                                        │
│  [ ] Checking drivers...                                        │
│                                                                 │
│  Progress: [████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 30%       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

                              ↓

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  STEP 2 OF 5: Scanning Your System                              │
│                                                                 │
│  Scan complete! Here's what I found:                            │
│                                                                 │
│  [OK]     Disk Space: 234 GB free                               │
│  [OK]     RAM: 12.4 GB available                                │
│  [OK]     Temperatures: Normal                                  │
│  [WARN]   4.2 GB of temp files can be cleared                   │
│  [WARN]   Game Mode is disabled                                 │
│  [WARN]   Power Plan set to Balanced (not optimal)              │
│  [WARN]   5 services can be optimized                           │
│  [WARN]   3 heavy background processes found                    │
│  [WARN]   DNS could be faster                                   │
│  [OK]     GPU driver is up to date                              │
│                                                                 │
│  Found 6 things to fix. Press Enter to see the fix plan...     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

                              ↓

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  STEP 3 OF 5: Fix Plan                                          │
│                                                                 │
│  Here's what I recommend fixing:                                │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  SAFE FIXES (Will apply automatically):                         │
│  ─────────────────────────────────────────────────────────────  │
│  [✓] Clear 4.2 GB temp files                    Risk: NONE      │
│  [✓] Enable Game Mode                           Risk: NONE      │
│  [✓] Set Power Plan to High Performance         Risk: NONE      │
│  [✓] Flush DNS cache                            Risk: NONE      │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  RECOMMENDED FIXES (Need your approval):                        │
│  ─────────────────────────────────────────────────────────────  │
│  [ ] Stop 5 unnecessary services                Risk: LOW       │
│      → Print Spooler, Fax, Windows Search...                    │
│  [ ] Close 3 background hogs                    Risk: LOW       │
│      → Chrome (3.2GB), Wallpaper Engine (1GB)...                │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  OPTIONAL (Gaming preference):                                  │
│  ─────────────────────────────────────────────────────────────  │
│  [ ] Disable Xbox Game Bar                      Risk: LOW       │
│      Saves resources, disables Win+G recording                  │
│  [ ] Reduce visual effects                      Risk: NONE      │
│      Makes Windows UI snappier                                  │
│                                                                 │
│  [1] Apply Safe Fixes Only (automatic)                          │
│  [2] Apply Safe + Recommended (with details)                    │
│  [3] Apply All (Safe + Recommended + Optional)                  │
│  [4] Customize (choose each fix)                                │
│  [0] Cancel - Don't change anything                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

User selects [2]

                              ↓

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  RECOMMENDED FIXES - Details                                    │
│                                                                 │
│  FIX: Stop unnecessary services                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  These services use resources but aren't needed for gaming:     │
│                                                                 │
│  1. Print Spooler                                               │
│     What it does: Handles printing                              │
│     Impact: You won't be able to print                          │
│     Reversible: Yes, instantly                                  │
│                                                                 │
│  2. Fax                                                         │
│     What it does: Handles faxing                                │
│     Impact: You won't be able to fax                            │
│     Reversible: Yes, instantly                                  │
│                                                                 │
│  3. Windows Search (Indexing)                                   │
│     What it does: Indexes files for fast search                 │
│     Impact: File search will be slower                          │
│     Benefit: Reduces disk usage significantly                   │
│     Reversible: Yes, instantly                                  │
│                                                                 │
│  ... and 2 more                                                 │
│                                                                 │
│  [Y] Stop these services    [N] Skip    [D] See more details    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

User selects [Y]

                              ↓

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  RECOMMENDED FIXES - Details                                    │
│                                                                 │
│  FIX: Close background processes                                │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  These programs are using RAM/GPU in the background:            │
│                                                                 │
│  1. chrome.exe (12 tabs)                        RAM: 3.2 GB     │
│     Closing Chrome will free significant memory.                │
│                                                                 │
│  2. Wallpaper Engine                            RAM: 1.1 GB     │
│     Animated wallpaper uses GPU constantly.                     │
│                                                                 │
│  3. Discord                                     RAM: 890 MB     │
│     Optional - you may want voice chat.                         │
│                                                                 │
│  Total RAM to free: ~5.2 GB                                     │
│                                                                 │
│  [1] Close Chrome only                                          │
│  [2] Close Chrome + Wallpaper Engine                            │
│  [3] Close all (including Discord)                              │
│  [N] Skip - Keep them running                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

User selects [2]

                              ↓

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  STEP 4 OF 5: Applying Fixes                                    │
│                                                                 │
│  [✓] Cleared 4.2 GB temp files                                  │
│  [✓] Enabled Game Mode                                          │
│  [✓] Set Power Plan to High Performance                         │
│  [✓] Flushed DNS cache                                          │
│  [✓] Stopped Print Spooler service                              │
│  [✓] Stopped Fax service                                        │
│  [✓] Stopped Windows Search service                             │
│  [●] Closing Chrome...                                          │
│  [ ] Closing Wallpaper Engine...                                │
│                                                                 │
│  Progress: [████████████████████████████░░░░░░░░░░░░] 70%       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

                              ↓

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  STEP 5 OF 5: Summary                                           │
│                                                                 │
│  All done! Here's what changed:                                 │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  APPLIED SUCCESSFULLY (8):                                      │
│  ─────────────────────────────────────────────────────────────  │
│  [OK] Cleared 4.2 GB temp files                                 │
│  [OK] Enabled Game Mode                                         │
│  [OK] Set Power Plan to High Performance                        │
│  [OK] Flushed DNS cache                                         │
│  [OK] Stopped Print Spooler                                     │
│  [OK] Stopped Fax service                                       │
│  [OK] Stopped Windows Search                                    │
│  [OK] Closed Chrome (freed 3.2 GB RAM)                          │
│  [OK] Closed Wallpaper Engine (freed 1.1 GB RAM)                │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  IMPACT:                                                        │
│  ─────────────────────────────────────────────────────────────  │
│  • Freed ~8.5 GB disk space                                     │
│  • Freed ~4.3 GB RAM                                            │
│  • Reduced background CPU/GPU usage                             │
│  • Optimized Windows for gaming                                 │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│  UNDO INFORMATION:                                              │
│  ─────────────────────────────────────────────────────────────  │
│  A backup was saved: 2024-01-15_143022_AutoFix                  │
│  Go to Snapshots menu to restore if needed.                     │
│                                                                 │
│  Note: Services will restart after reboot unless you            │
│  disable them permanently in Service Optimizer.                 │
│                                                                 │
│  [Enter] Back to Main Menu                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Technical Implementation

### AutoFixWizard Class

```python
class AutoFixWizard:
    """Main Auto-Fix Wizard implementation"""

    def __init__(self, modules):
        self.health_check = modules['health_check']
        self.repairs = modules['repairs']
        self.services = modules['services']
        self.processes = modules['processes']
        self.snapshots = modules['snapshots']
        self.network = modules['network']
        self.power = modules['power']

        self.scan_results = {}
        self.fix_plan = {
            'safe': [],
            'recommended': [],
            'optional': []
        }
        self.applied_fixes = []
        self.failed_fixes = []
        self.snapshot_id = None

    def run(self):
        """Main wizard flow"""
        clear_screen()
        self.show_intro()

        if not self.confirm_start():
            return

        # Step 1: Create backup
        if not self.step_create_backup():
            return

        # Step 2: Scan system
        self.step_scan_system()

        # Step 3: Show fix plan
        user_choice = self.step_show_plan()

        if user_choice == 'cancel':
            return

        # Step 4: Apply fixes
        self.step_apply_fixes(user_choice)

        # Step 5: Show summary
        self.step_show_summary()

    def step_create_backup(self):
        """Step 1: Create safety backup"""
        print_header("STEP 1 OF 5: Creating Safety Backup")

        print("  Before making any changes, I'll create a backup so you can")
        print("  undo everything if needed.\n")

        # Create restore point
        print_status("WAIT", "Creating Windows Restore Point...")
        restore_success = self.snapshots.create_restore_point("GameFix Auto-Fix")

        if restore_success:
            print_status("OK", "Windows Restore Point created")
        else:
            print_status("WARN", "Could not create Restore Point (may need admin)")

        # Save service states
        print_status("WAIT", "Saving service states...")
        self.snapshot_id = self.snapshots.create_snapshot("AutoFix")

        if self.snapshot_id:
            print_status("OK", "Service states saved")
            print_status("OK", "Settings backed up")
            print(f"\n  Backup ID: {self.snapshot_id}")
            print("  You can restore this anytime from Snapshots menu.")
        else:
            print_status("FAIL", "Could not create backup")
            print_status("INFO", "For your safety, the wizard will stop here.")
            press_enter()
            return False

        press_enter()
        return True

    def step_scan_system(self):
        """Step 2: Scan system for issues"""
        clear_screen()
        print_header("STEP 2 OF 5: Scanning Your System")

        checks = [
            ('disk_space', "Checking disk space...", self.check_disk_space),
            ('ram', "Checking RAM usage...", self.check_ram),
            ('temps', "Checking CPU/GPU temps...", self.check_temps),
            ('windows_health', "Checking Windows health...", self.check_windows_health),
            ('services', "Checking services...", self.check_services),
            ('startup', "Checking startup programs...", self.check_startup),
            ('processes', "Checking background processes...", self.check_processes),
            ('gaming_settings', "Checking gaming settings...", self.check_gaming_settings),
            ('network', "Checking network...", self.check_network),
            ('drivers', "Checking drivers...", self.check_drivers),
        ]

        for i, (key, message, check_func) in enumerate(checks):
            # Show progress
            self.show_check_progress(checks, i)

            # Run check
            try:
                result = check_func()
                self.scan_results[key] = result
            except Exception as e:
                self.scan_results[key] = {'status': 'error', 'error': str(e)}

        # Show results
        self.show_scan_results()
        press_enter()

    def check_disk_space(self):
        """Check disk space"""
        import psutil
        result = {'status': 'ok', 'issues': []}

        for disk in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(disk.mountpoint)
                free_gb = usage.free / (1024**3)

                if free_gb < 20:
                    result['status'] = 'warn'
                    result['issues'].append({
                        'type': 'low_disk',
                        'drive': disk.device,
                        'free_gb': free_gb
                    })
            except:
                pass

        return result

    def check_gaming_settings(self):
        """Check Windows gaming settings"""
        result = {'status': 'ok', 'issues': [], 'fixes': []}

        # Check Game Mode
        game_mode = self.read_registry_value(
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\GameBar",
            "AllowAutoGameMode"
        )

        if game_mode != 1:
            result['status'] = 'warn'
            result['issues'].append('Game Mode disabled')
            result['fixes'].append({
                'name': 'Enable Game Mode',
                'category': 'safe',
                'function': self.repairs.enable_game_mode,
                'risk': 'none'
            })

        # Check Power Plan
        power_plan = self.power.get_current_plan()
        if power_plan != 'high_performance':
            result['status'] = 'warn'
            result['issues'].append(f'Power Plan: {power_plan}')
            result['fixes'].append({
                'name': 'Set High Performance Power Plan',
                'category': 'safe',
                'function': self.power.set_high_performance,
                'risk': 'none'
            })

        return result

    def check_processes(self):
        """Check for heavy background processes"""
        result = {'status': 'ok', 'issues': [], 'fixes': []}

        heavy_processes = self.processes.get_heavy_processes(
            ram_threshold_mb=500,
            exclude_system=True
        )

        if heavy_processes:
            total_ram = sum(p['ram_mb'] for p in heavy_processes)
            result['status'] = 'warn'
            result['issues'].append(f'{len(heavy_processes)} heavy processes ({total_ram:.0f} MB)')
            result['fixes'].append({
                'name': f'Close {len(heavy_processes)} background processes',
                'category': 'recommended',
                'function': lambda: self.processes.close_processes(heavy_processes),
                'risk': 'low',
                'details': heavy_processes
            })

        return result

    def build_fix_plan(self):
        """Build categorized fix plan from scan results"""
        self.fix_plan = {'safe': [], 'recommended': [], 'optional': []}

        for key, result in self.scan_results.items():
            if 'fixes' in result:
                for fix in result['fixes']:
                    category = fix.get('category', 'recommended')
                    self.fix_plan[category].append(fix)

        # Add standard safe fixes if issues found
        if self.has_temp_files():
            self.fix_plan['safe'].append({
                'name': 'Clear temp files',
                'function': self.repairs.clear_temp_files,
                'risk': 'none'
            })

        if self.dns_could_be_optimized():
            self.fix_plan['safe'].append({
                'name': 'Flush DNS cache',
                'function': self.network.flush_dns,
                'risk': 'none'
            })

    def step_show_plan(self):
        """Step 3: Show fix plan and get user choice"""
        clear_screen()
        print_header("STEP 3 OF 5: Fix Plan")

        self.build_fix_plan()

        print("  Here's what I recommend fixing:\n")

        # Safe fixes
        if self.fix_plan['safe']:
            print(f"  {Fore.GREEN}SAFE FIXES (Will apply automatically):{Style.RESET_ALL}")
            print("  " + "─" * 55)
            for fix in self.fix_plan['safe']:
                print(f"  [✓] {fix['name']:<40} Risk: {fix.get('risk', 'none').upper()}")
            print()

        # Recommended fixes
        if self.fix_plan['recommended']:
            print(f"  {Fore.YELLOW}RECOMMENDED FIXES (Need your approval):{Style.RESET_ALL}")
            print("  " + "─" * 55)
            for fix in self.fix_plan['recommended']:
                print(f"  [ ] {fix['name']:<40} Risk: {fix.get('risk', 'low').upper()}")
                if 'details' in fix:
                    details = fix['details'][:2]  # Show first 2
                    for d in details:
                        print(f"      → {d.get('name', 'Unknown')}")
            print()

        # Optional fixes
        if self.fix_plan['optional']:
            print(f"  {Fore.CYAN}OPTIONAL (Gaming preference):{Style.RESET_ALL}")
            print("  " + "─" * 55)
            for fix in self.fix_plan['optional']:
                print(f"  [ ] {fix['name']:<40} Risk: {fix.get('risk', 'low').upper()}")
                if 'description' in fix:
                    print(f"      {fix['description']}")
            print()

        # Options
        print()
        print("  [1] Apply Safe Fixes Only (automatic)")
        print("  [2] Apply Safe + Recommended (with details)")
        print("  [3] Apply All (Safe + Recommended + Optional)")
        print("  [4] Customize (choose each fix)")
        print(f"  {Fore.RED}[0] Cancel - Don't change anything{Style.RESET_ALL}")
        print()

        choice = get_choice()

        if choice == '0':
            return 'cancel'
        elif choice == '1':
            return 'safe_only'
        elif choice == '2':
            return self.get_recommended_approval()
        elif choice == '3':
            return 'all'
        elif choice == '4':
            return self.get_custom_selection()
        else:
            return 'safe_only'

    def get_recommended_approval(self):
        """Get user approval for each recommended fix"""
        approved_fixes = list(self.fix_plan['safe'])  # Safe always included

        for fix in self.fix_plan['recommended']:
            clear_screen()
            print_header("RECOMMENDED FIX - Details")

            print(f"  FIX: {fix['name']}")
            print("  " + "─" * 55)
            print()

            if 'details' in fix:
                for detail in fix['details']:
                    print(f"  • {detail.get('name', 'Unknown')}")
                    if 'ram_mb' in detail:
                        print(f"    RAM: {detail['ram_mb']:.0f} MB")
                    print()

            print(f"  Risk Level: {fix.get('risk', 'low').upper()}")
            print(f"  Reversible: Yes")
            print()

            if confirm(f"Apply this fix?"):
                approved_fixes.append(fix)

        return {'type': 'custom', 'fixes': approved_fixes}

    def step_apply_fixes(self, user_choice):
        """Step 4: Apply selected fixes"""
        clear_screen()
        print_header("STEP 4 OF 5: Applying Fixes")

        # Determine which fixes to apply
        if user_choice == 'safe_only':
            fixes_to_apply = self.fix_plan['safe']
        elif user_choice == 'all':
            fixes_to_apply = (
                self.fix_plan['safe'] +
                self.fix_plan['recommended'] +
                self.fix_plan['optional']
            )
        elif isinstance(user_choice, dict):
            fixes_to_apply = user_choice['fixes']
        else:
            fixes_to_apply = self.fix_plan['safe']

        # Apply each fix
        total = len(fixes_to_apply)
        for i, fix in enumerate(fixes_to_apply):
            print_status("WAIT", f"{fix['name']}...")

            try:
                result = fix['function']()
                if result:
                    print_status("OK", fix['name'])
                    self.applied_fixes.append(fix)
                else:
                    print_status("WARN", f"{fix['name']} - completed with warnings")
                    self.applied_fixes.append(fix)
            except Exception as e:
                print_status("FAIL", f"{fix['name']} - {str(e)}")
                self.failed_fixes.append({'fix': fix, 'error': str(e)})

            # Update progress
            print_progress(i + 1, total)

        print()
        press_enter()

    def step_show_summary(self):
        """Step 5: Show summary of changes"""
        clear_screen()
        print_header("STEP 5 OF 5: Summary")

        print("  All done! Here's what changed:\n")

        # Applied fixes
        if self.applied_fixes:
            print(f"  {Fore.GREEN}APPLIED SUCCESSFULLY ({len(self.applied_fixes)}):{Style.RESET_ALL}")
            print("  " + "─" * 55)
            for fix in self.applied_fixes:
                print_status("OK", fix['name'])
            print()

        # Failed fixes
        if self.failed_fixes:
            print(f"  {Fore.RED}FAILED ({len(self.failed_fixes)}):{Style.RESET_ALL}")
            print("  " + "─" * 55)
            for item in self.failed_fixes:
                print_status("FAIL", f"{item['fix']['name']} - {item['error']}")
            print()

        # Impact summary
        print(f"  {Fore.CYAN}IMPACT:{Style.RESET_ALL}")
        print("  " + "─" * 55)
        self.show_impact_summary()
        print()

        # Undo information
        print(f"  {Fore.YELLOW}UNDO INFORMATION:{Style.RESET_ALL}")
        print("  " + "─" * 55)
        print(f"  A backup was saved: {self.snapshot_id}")
        print("  Go to Snapshots menu to restore if needed.")
        print()
        print("  Note: Stopped services will restart after reboot unless")
        print("  you disable them permanently in Service Optimizer.")
        print()

        press_enter()

    def show_impact_summary(self):
        """Show summary of impact"""
        # Calculate RAM freed
        ram_freed = 0
        for fix in self.applied_fixes:
            if 'details' in fix:
                for d in fix['details']:
                    if 'ram_mb' in d:
                        ram_freed += d['ram_mb']

        # Calculate disk freed
        disk_freed = 0
        for fix in self.applied_fixes:
            if 'disk_freed_gb' in fix:
                disk_freed += fix['disk_freed_gb']

        if disk_freed > 0:
            print(f"  • Freed ~{disk_freed:.1f} GB disk space")

        if ram_freed > 0:
            print(f"  • Freed ~{ram_freed/1024:.1f} GB RAM")

        # Count optimizations
        service_count = sum(1 for f in self.applied_fixes if 'service' in f['name'].lower())
        if service_count > 0:
            print(f"  • Stopped {service_count} unnecessary services")

        print("  • Optimized Windows for gaming")
```

---

## Fix Categories Definition

### Safe Fixes (Auto-Apply)

These are completely safe and can be applied without asking:

| Fix | Risk | Reversible | Notes |
|-----|------|------------|-------|
| Clear temp files | None | N/A (just cache) | Always safe |
| Enable Game Mode | None | Yes | Only affects gaming |
| Flush DNS | None | Automatic | Rebuilds automatically |
| Set Power Plan | None | Yes | Easy to change back |

### Recommended Fixes (Need Approval)

These are safe but user should understand the impact:

| Fix | Risk | Reversible | Why Ask |
|-----|------|------------|---------|
| Stop Print Spooler | Low | Yes | User may need printing |
| Stop Windows Search | Low | Yes | Affects search speed |
| Close Chrome | Low | Yes | User may have work open |
| Close background apps | Low | Yes | User may want them |

### Optional Fixes (User Preference)

These are subjective or have trade-offs:

| Fix | Risk | Trade-off |
|-----|------|-----------|
| Disable Xbox Game Bar | Low | Lose Win+G recording |
| Disable visual effects | None | Less pretty Windows |
| Disable overlays | Low | Lose overlay features |

---

## Error Handling

### If Backup Creation Fails

```python
def handle_backup_failure():
    print_status("FAIL", "Could not create safety backup")
    print()
    print("  This can happen if:")
    print("  • System Restore is disabled")
    print("  • Not enough disk space")
    print("  • Running without admin rights")
    print()
    print("  For your safety, the Auto-Fix Wizard will not continue")
    print("  without a backup.")
    print()
    print("  Options:")
    print("  [1] Try running as Administrator")
    print("  [2] Enable System Restore and try again")
    print("  [3] Use individual fixes instead (manual mode)")
    print()
```

### If Fix Fails

```python
def handle_fix_failure(fix, error):
    print_status("FAIL", f"{fix['name']}")
    print(f"        Error: {error}")

    # Don't stop the wizard, continue with other fixes
    # The failure will be shown in summary

    # If it's a critical fix, offer to stop
    if fix.get('critical'):
        if confirm("This was an important fix. Stop wizard?"):
            raise WizardAborted()
```

---

## First-Time User Experience

When the tool detects first run:

```
╔═══════════════════════════════════════════════════════════════╗
║                    WELCOME TO GAMEFIX DOCTOR PRO              ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  Hi! It looks like this is your first time here.              ║
║                                                               ║
║  Want me to run a quick optimization? I'll:                   ║
║  • Scan your PC for gaming issues                             ║
║  • Create a backup first (just in case)                       ║
║  • Fix common problems automatically                          ║
║  • Ask before doing anything major                            ║
║                                                               ║
║  This usually takes 2-3 minutes and makes a real difference.  ║
║                                                               ║
║  [1] Yes, run Auto-Fix Wizard (Recommended)                   ║
║  [2] No, show me the main menu                                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```
