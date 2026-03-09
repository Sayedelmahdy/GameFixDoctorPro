# GameFix Doctor Pro - Safety Rules

## Core Safety Philosophy

**The Golden Rule:** Never break the user's system. It's better to do nothing than to cause damage.

---

## Absolute Rules (Never Break These)

### 1. Never Build Cheats or Hacks
```
FORBIDDEN:
- Game memory editors
- Aim assists or aimbots
- Wallhacks or ESP
- Speed hacks
- Anti-cheat bypasses
- DLL injection for game modification
- Save file editors that give unfair advantage
- Macro tools for automated gameplay
```

### 2. Never Bypass Security
```
FORBIDDEN:
- Anti-cheat bypass or removal
- DRM circumvention
- License validation bypass
- Windows activation bypass
- Antivirus disabling (permanent)
```

### 3. Never Apply Risky "Optimizations"
```
FORBIDDEN:
- Registry "tweaks" that claim miraculous FPS boosts
- Timer resolution hacks
- Disabling core Windows services
- Modifying system-protected files
- Overclocking (suggest only, never apply)
- BIOS-level changes
- "Gaming mode" registry hacks that break things
- Disabling security features for "performance"
```

### 4. Never Delete Without Understanding
```
FORBIDDEN:
- Deleting unknown files
- Removing software without proper uninstall
- Clearing folders without knowing contents
- Removing "suspicious" files without verification
- Deleting user data without explicit consent
```

---

## Required Safety Practices

### 1. Always Create Snapshots Before Changes

**When to create snapshot:**
- Before any service modifications
- Before registry changes
- Before system repairs (SFC, DISM)
- Before network resets
- Before any "fix" that could impact stability

**Snapshot includes:**
- Windows Restore Point (when possible)
- Service states backup
- Registry key backups (for modified keys)
- Action description and timestamp

```python
def apply_fix(fix_function, description):
    """Standard pattern for applying fixes"""
    # 1. Create snapshot FIRST
    snapshot_path = snapshot_manager.create_snapshot(
        action_name=description,
        include_restore_point=True
    )

    if not snapshot_path:
        print_status("FAIL", "Could not create safety snapshot")
        print_status("INFO", "Action cancelled for your safety")
        return False

    # 2. Confirm with user
    if not confirm(f"Apply fix: {description}?"):
        return False

    # 3. Apply the fix
    try:
        result = fix_function()
        return result
    except Exception as e:
        print_status("FAIL", f"Error: {str(e)}")
        print_status("INFO", f"You can rollback using snapshot: {snapshot_path}")
        return False
```

### 2. Always Ask Before Impactful Changes

**Must confirm for:**
- Service start/stop
- Registry modifications
- File deletions
- System repairs
- Network resets
- Power plan changes
- Startup program changes

**Confirmation format:**
```
You are about to: [Description]

What this does:
• [Bullet 1]
• [Bullet 2]

Risk Level: [LOW/MEDIUM/HIGH]
Reversible: [Yes/No/Partially]

Proceed? (y/n):
```

### 3. Always Explain Actions Clearly

**Bad:**
```
Optimizing system...
Done.
```

**Good:**
```
Clearing temporary files...

What I'm doing:
• Deleting files in C:\Users\You\AppData\Local\Temp
• Deleting files in C:\Windows\Temp
• These are safe to remove - they're just cached data

Progress: [████████████████░░░░░░░░░░░░░░░░░░░░░░░░] 40%
Cleared 2.3 GB so far...

Done! Cleared 4.1 GB of temporary files.
```

### 4. Always Use Proper Uninstall Methods

**For removing software:**
```python
def remove_software(app_name):
    """Safe software removal"""
    # 1. Check if it's in the protected list
    if is_protected_software(app_name):
        print_status("WARN", f"Cannot remove {app_name} - it's a system component")
        return False

    # 2. Find proper uninstaller
    uninstaller = find_uninstaller(app_name)

    if uninstaller:
        # Use official uninstaller
        print_status("INFO", f"Using {app_name}'s official uninstaller")
        run_uninstaller(uninstaller)
    else:
        # Fallback to Windows uninstall
        print_status("INFO", "Opening Windows Apps settings for manual removal")
        open_windows_apps_settings()

    # NEVER just delete program files
```

### 5. Never Claim Certainty About Malware

**Bad:**
```
[DANGER] MALWARE DETECTED: suspicious_process.exe
Removing threat...
```

**Good:**
```
[WARN] Suspicious process detected: suspicious_process.exe

Why it's flagged:
• Using high GPU (45%) while hidden
• No visible window
• Name doesn't match known software

What to do:
• This might be legitimate software you installed
• It could also be unwanted software
• Please verify before taking action

Options:
[1] View process details
[2] Open file location
[3] Search online for this process
[4] I don't recognize this - close it
[0] Ignore for now
```

---

## Service Safety Rules

### Services That Must NEVER Be Stopped

```python
CRITICAL_SERVICES = [
    # Core Windows
    "RpcSs",           # Remote Procedure Call - SYSTEM WILL CRASH
    "DcomLaunch",      # DCOM Server - Many things depend on this
    "LSM",             # Local Session Manager
    "SamSs",           # Security Accounts Manager
    "PlugPlay",        # Plug and Play
    "Power",           # Power management
    "ProfSvc",         # User Profile Service

    # Security
    "WinDefend",       # Windows Defender
    "mpssvc",          # Windows Firewall
    "WdNisSvc",        # Defender Network Inspection
    "SecurityHealthService",

    # System Stability
    "eventlog",        # Event Log
    "Schedule",        # Task Scheduler
    "LanmanWorkstation",  # Network
    "Dhcp",            # DHCP Client
    "Dnscache",        # DNS Client
]
```

### Services That Need Careful Consideration

```python
CAUTION_SERVICES = [
    # Audio - Don't disable if user wants game audio
    "Audiosrv",
    "AudioEndpointBuilder",

    # Input - Don't disable if user uses controllers
    "HidServ",
    "XboxGipSvc",

    # Updates - User should decide
    "wuauserv",
    "UsoSvc",
]
```

### Service Modification Flow

```python
def modify_service(service_name, action):
    """Safe service modification"""
    # 1. Check if critical
    if service_name in CRITICAL_SERVICES:
        print_status("FAIL", f"Cannot modify {service_name}")
        print_status("INFO", "This is a critical system service")
        return False

    # 2. Get current state
    current_state = get_service_state(service_name)

    # 3. Create snapshot
    create_snapshot(f"Service change: {service_name}")

    # 4. Warn if caution service
    if service_name in CAUTION_SERVICES:
        print_status("WARN", "This service may be needed for some features")
        explain_service_purpose(service_name)

    # 5. Confirm
    if not confirm(f"Change {service_name} from {current_state} to {action}?"):
        return False

    # 6. Apply change
    result = apply_service_change(service_name, action)

    # 7. Verify
    if not verify_service_state(service_name, action):
        print_status("WARN", "Service state may not have changed as expected")
        offer_rollback()

    return result
```

---

## Process Killing Safety

### Never Kill These Processes

```python
PROTECTED_PROCESSES = [
    # Windows Core
    "System",
    "smss.exe",
    "csrss.exe",
    "wininit.exe",
    "services.exe",
    "lsass.exe",
    "winlogon.exe",
    "dwm.exe",
    "svchost.exe",

    # User Experience
    "explorer.exe",      # Killing this hides desktop
    "ShellExperienceHost.exe",
    "StartMenuExperienceHost.exe",

    # Security
    "MsMpEng.exe",       # Windows Defender
    "SecurityHealthService.exe",
    "smartscreen.exe",

    # Critical Background
    "spoolsv.exe",
    "taskhostw.exe",
    "RuntimeBroker.exe",
    "fontdrvhost.exe",
    "WUDFHost.exe",

    # Our own process
    "GameFixDoctorPro.exe",
]

def can_kill_process(process_name):
    """Check if process can be safely killed"""
    name_lower = process_name.lower()

    # Never kill protected
    if name_lower in [p.lower() for p in PROTECTED_PROCESSES]:
        return False, "This is a protected system process"

    # Warn about svchost
    if name_lower == "svchost.exe":
        return False, "svchost.exe hosts critical Windows services"

    return True, "Safe to close"
```

### Process Killing Flow

```python
def kill_process_safely(pid, process_name):
    """Safe process termination"""
    # 1. Check if protected
    can_kill, reason = can_kill_process(process_name)
    if not can_kill:
        print_status("FAIL", reason)
        return False

    # 2. Get process details
    try:
        process = psutil.Process(pid)
        process_path = process.exe()
        process_user = process.username()
    except:
        print_status("FAIL", "Process no longer exists")
        return True  # Already gone

    # 3. Warn if system process
    if "windows" in process_path.lower():
        print_status("WARN", "This appears to be a Windows component")
        if not confirm("Are you sure you want to close it?"):
            return False

    # 4. Try graceful termination first
    print_status("INFO", f"Asking {process_name} to close...")
    try:
        process.terminate()
        process.wait(timeout=5)
        print_status("OK", "Process closed gracefully")
        return True
    except psutil.TimeoutExpired:
        pass

    # 5. Force kill only if requested
    if confirm("Process didn't close. Force kill?"):
        try:
            process.kill()
            print_status("OK", "Process force closed")
            return True
        except Exception as e:
            print_status("FAIL", f"Could not kill process: {e}")
            return False

    return False
```

---

## File Operations Safety

### Paths That Must NEVER Be Deleted

```python
PROTECTED_PATHS = [
    "C:\\Windows",
    "C:\\Windows\\System32",
    "C:\\Windows\\SysWOW64",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\Users\\*\\AppData\\Roaming\\Microsoft",
    "C:\\Users\\*\\Documents",
    "C:\\Users\\*\\Desktop",
    "C:\\Users\\*\\Downloads",
    "C:\\ProgramData\\Microsoft",
]

SAFE_TO_CLEAR = [
    "C:\\Users\\*\\AppData\\Local\\Temp",
    "C:\\Windows\\Temp",
    "C:\\Windows\\Prefetch",
    # Launcher caches with specific patterns
]
```

### Safe File Deletion

```python
def safe_delete_file(file_path):
    """Safely delete a file"""
    # 1. Check if in protected path
    for protected in PROTECTED_PATHS:
        if matches_path(file_path, protected):
            print_status("FAIL", "Cannot delete - protected location")
            return False

    # 2. Check if system file
    if is_system_file(file_path):
        print_status("FAIL", "Cannot delete - system file")
        return False

    # 3. Check file age (don't delete recent files)
    if get_file_age_hours(file_path) < 1:
        print_status("WARN", "File is less than 1 hour old")
        if not confirm("Still delete?"):
            return False

    # 4. Delete
    try:
        os.remove(file_path)
        return True
    except PermissionError:
        print_status("WARN", "File is in use")
        return False
    except Exception as e:
        print_status("FAIL", str(e))
        return False
```

---

## Registry Safety

### Registry Keys That Must NEVER Be Modified

```python
PROTECTED_REGISTRY = [
    # Boot critical
    r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager",
    r"HKLM\SYSTEM\CurrentControlSet\Services",  # Individual services OK
    r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon",

    # Security
    r"HKLM\SAM",
    r"HKLM\SECURITY",
    r"HKLM\SOFTWARE\Microsoft\Windows Defender",

    # System integrity
    r"HKLM\SYSTEM\CurrentControlSet\Control\SafeBoot",
    r"HKLM\SYSTEM\Setup",
]

SAFE_TO_MODIFY = [
    # Game Mode
    r"HKCU\SOFTWARE\Microsoft\GameBar",

    # Visual effects
    r"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects",

    # Individual app settings
    r"HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR",
]
```

### Safe Registry Modification

```python
def safe_modify_registry(hive, key_path, value_name, new_value, value_type):
    """Safely modify registry"""
    full_key = f"{hive_name(hive)}\\{key_path}"

    # 1. Check if protected
    for protected in PROTECTED_REGISTRY:
        if full_key.startswith(protected):
            print_status("FAIL", "Cannot modify - protected registry key")
            return False

    # 2. Backup current value
    current_value = read_registry(hive, key_path, value_name)
    backup = {
        'key': full_key,
        'value_name': value_name,
        'old_value': current_value,
        'new_value': new_value,
        'timestamp': datetime.now().isoformat()
    }
    save_registry_backup(backup)

    # 3. Show what will change
    print(f"Registry change:")
    print(f"  Key:   {full_key}")
    print(f"  Value: {value_name}")
    print(f"  From:  {current_value}")
    print(f"  To:    {new_value}")

    # 4. Confirm
    if not confirm("Apply this change?"):
        return False

    # 5. Apply
    try:
        write_registry(hive, key_path, value_name, new_value, value_type)
        print_status("OK", "Registry updated")
        return True
    except Exception as e:
        print_status("FAIL", f"Failed: {e}")
        return False
```

---

## Network Safety

### Safe Network Commands

```python
SAFE_NETWORK_COMMANDS = {
    'flush_dns': {
        'command': 'ipconfig /flushdns',
        'risk': 'none',
        'reversible': True,
        'requires_reboot': False
    },
    'release_ip': {
        'command': 'ipconfig /release',
        'risk': 'low',
        'reversible': True,
        'note': 'Will temporarily disconnect'
    },
    'renew_ip': {
        'command': 'ipconfig /renew',
        'risk': 'none',
        'reversible': True
    }
}

CAUTION_NETWORK_COMMANDS = {
    'reset_winsock': {
        'command': 'netsh winsock reset',
        'risk': 'low',
        'requires_reboot': True,
        'requires_snapshot': True
    },
    'reset_ip': {
        'command': 'netsh int ip reset',
        'risk': 'low',
        'requires_reboot': True,
        'requires_snapshot': True
    }
}

FORBIDDEN_NETWORK_COMMANDS = {
    'disable_firewall': 'Security risk',
    'delete_routes': 'Can break connectivity',
    'reset_all_adapters': 'Too aggressive'
}
```

---

## Error Handling Safety

### Fail Safely

```python
def safe_operation(operation_name, operation_func, *args, **kwargs):
    """Wrapper for safe operation execution"""
    try:
        result = operation_func(*args, **kwargs)
        return {'success': True, 'result': result}
    except PermissionError:
        return {
            'success': False,
            'error': 'permission_denied',
            'message': 'This operation requires administrator privileges',
            'solution': 'Please restart the tool as administrator'
        }
    except FileNotFoundError as e:
        return {
            'success': False,
            'error': 'file_not_found',
            'message': f'Required file not found: {e.filename}',
            'solution': 'The file may have been moved or deleted'
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'timeout',
            'message': 'Operation took too long',
            'solution': 'Try again or check if system is busy'
        }
    except Exception as e:
        # Log the full error for debugging
        logging.error(f"Error in {operation_name}: {str(e)}", exc_info=True)

        return {
            'success': False,
            'error': 'unknown',
            'message': f'An unexpected error occurred: {str(e)}',
            'solution': 'Please report this error'
        }
```

### Never Hide Errors

```python
# BAD - Hiding errors
def bad_repair():
    try:
        do_repair()
    except:
        pass  # Silent failure

# GOOD - Transparent errors
def good_repair():
    try:
        result = do_repair()
        if result.success:
            print_status("OK", "Repair completed")
        else:
            print_status("WARN", f"Repair completed with warnings: {result.warnings}")
    except RepairError as e:
        print_status("FAIL", f"Repair failed: {e}")
        print_status("INFO", "Your system was not changed")
        print_status("INFO", f"Error details: {e.details}")
        offer_help()
```

---

## Pre-Release Safety Checklist

Before releasing any version:

- [ ] All critical services are protected
- [ ] All protected processes are defined
- [ ] Snapshot creation works correctly
- [ ] Snapshot restoration works correctly
- [ ] No silent failures exist
- [ ] All errors are user-friendly
- [ ] Admin elevation works correctly
- [ ] All confirmations are in place
- [ ] Protected paths cannot be deleted
- [ ] Protected registry keys cannot be modified
- [ ] Network resets require confirmation
- [ ] Process killing has proper guards
- [ ] No hardcoded credentials or paths
- [ ] Logging captures errors properly
- [ ] Tool cannot break its own installation
- [ ] Tested on clean Windows install
- [ ] Tested without admin rights
- [ ] Tested with antivirus active
