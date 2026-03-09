# GameFix Doctor Pro - Technical Implementation Guide

## Table of Contents
1. [Environment Setup](#environment-setup)
2. [Core Module Implementation](#core-module-implementation)
3. [System Detection](#system-detection)
4. [Game Detection](#game-detection)
5. [Windows Commands Reference](#windows-commands-reference)
6. [Registry Operations](#registry-operations)
7. [Service Management](#service-management)
8. [Process Management](#process-management)
9. [Snapshot System](#snapshot-system)
10. [Error Handling](#error-handling)
11. [Building EXE](#building-exe)

---

## Environment Setup

### Python Version
- Minimum: Python 3.8
- Recommended: Python 3.10+

### Required Packages

```
requirements.txt:
-----------------
psutil>=5.9.0          # Process and system monitoring
wmi>=1.5.1             # Windows Management Instrumentation
colorama>=0.4.6        # Terminal colors
pywin32>=305           # Windows API access
GPUtil>=1.4.0          # GPU information (NVIDIA)
```

### Optional Packages
```
pyinstaller>=6.0       # For building EXE
```

### Installation
```bash
pip install -r requirements.txt
```

---

## Core Module Implementation

### core/config.py
```python
"""
Global configuration and constants
"""
import os
from pathlib import Path

# App info
APP_NAME = "GameFix Doctor Pro"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Sayed Elmahdy"

# Paths
APP_DIR = Path(__file__).parent.parent
DATA_DIR = APP_DIR / "data"
SNAPSHOTS_DIR = APP_DIR / "snapshots"
REPORTS_DIR = APP_DIR / "reports"

# Ensure directories exist
SNAPSHOTS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Thresholds
DISK_SPACE_WARN_GB = 50
DISK_SPACE_CRITICAL_GB = 20
RAM_WARN_GB = 4
RAM_CRITICAL_GB = 2
CPU_TEMP_WARN = 70
CPU_TEMP_CRITICAL = 85
GPU_TEMP_WARN = 75
GPU_TEMP_CRITICAL = 90
CPU_IDLE_WARN = 30
CPU_IDLE_CRITICAL = 60
GPU_IDLE_WARN = 10
GPU_IDLE_CRITICAL = 30

# Process thresholds
RAM_NOTABLE_MB = 500
RAM_HEAVY_MB = 1000
CPU_NOTABLE_PERCENT = 10
CPU_HEAVY_PERCENT = 25
GPU_SUSPICIOUS_PERCENT = 5

# Color codes
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
```

### core/admin.py
```python
"""
Admin elevation handling
"""
import ctypes
import sys
import os

def is_admin():
    """Check if running with admin privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Re-launch the script with admin privileges"""
    if is_admin():
        return True

    try:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            " ".join(sys.argv),
            None,
            1  # SW_SHOWNORMAL
        )
        sys.exit(0)
    except Exception as e:
        return False

def require_admin(func):
    """Decorator to require admin for a function"""
    def wrapper(*args, **kwargs):
        if not is_admin():
            print("[!] This action requires administrator privileges.")
            print("[!] Please restart the tool as administrator.")
            return None
        return func(*args, **kwargs)
    return wrapper
```

### core/ui.py
```python
"""
User interface helpers - menus, colors, formatting
"""
import os
import sys
from colorama import init, Fore, Back, Style

# Initialize colorama for Windows
init()

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print a styled header box"""
    width = 65
    print(f"\n{Fore.CYAN}{'═' * width}")
    print(f"║{title.center(width - 2)}║")
    print(f"{'═' * width}{Style.RESET_ALL}\n")

def print_status(status, message):
    """Print a status message with color coding"""
    if status == "OK":
        print(f"  {Fore.GREEN}[OK]{Style.RESET_ALL}     {message}")
    elif status == "WARN":
        print(f"  {Fore.YELLOW}[WARN]{Style.RESET_ALL}   {message}")
    elif status == "FAIL":
        print(f"  {Fore.RED}[FAIL]{Style.RESET_ALL}   {message}")
    elif status == "INFO":
        print(f"  {Fore.BLUE}[INFO]{Style.RESET_ALL}   {message}")
    elif status == "WAIT":
        print(f"  {Fore.CYAN}[....]{Style.RESET_ALL}   {message}")

def print_menu(options):
    """Print a numbered menu"""
    print()
    for key, value in options.items():
        if key == "0":
            print(f"\n  {Fore.RED}[{key}]{Style.RESET_ALL}  {value}")
        else:
            print(f"  {Fore.CYAN}[{key}]{Style.RESET_ALL}  {value}")
    print()

def get_choice(prompt="Your choice: "):
    """Get user input"""
    return input(f"  {prompt}").strip()

def confirm(message):
    """Ask for yes/no confirmation"""
    response = input(f"  {message} (y/n): ").strip().lower()
    return response in ['y', 'yes']

def press_enter():
    """Wait for user to press enter"""
    input(f"\n  {Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

def print_progress(current, total, message=""):
    """Print a progress bar"""
    percent = int((current / total) * 100)
    bar_length = 40
    filled = int(bar_length * current / total)
    bar = '█' * filled + '░' * (bar_length - filled)
    print(f"\r  [{bar}] {percent}% {message}", end='', flush=True)
    if current == total:
        print()

def print_table(headers, rows):
    """Print a formatted table"""
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    # Print header
    header_line = " │ ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    print(f"  {Fore.CYAN}{header_line}{Style.RESET_ALL}")
    print(f"  {'─' * len(header_line)}")

    # Print rows
    for row in rows:
        row_line = " │ ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
        print(f"  {row_line}")
```

### core/utils.py
```python
"""
Shared utility functions
"""
import subprocess
import os
import json
from pathlib import Path
from datetime import datetime

def run_command(cmd, shell=True, capture=True, timeout=60):
    """Run a system command and return output"""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=capture,
            text=True,
            timeout=timeout
        )
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Command timed out'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def format_bytes(bytes_value):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"

def format_timestamp():
    """Get formatted timestamp for filenames"""
    return datetime.now().strftime("%Y-%m-%d_%H%M%S")

def load_json(filepath):
    """Load JSON file safely"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_json(filepath, data):
    """Save data to JSON file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

def get_windows_version():
    """Get Windows version info"""
    try:
        import platform
        return {
            'version': platform.version(),
            'release': platform.release(),
            'build': platform.win32_ver()[1]
        }
    except:
        return {'version': 'Unknown', 'release': 'Unknown', 'build': 'Unknown'}
```

---

## System Detection

### modules/system_info.py

```python
"""
System information detection module
"""
import psutil
import platform
import subprocess
import os

try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False

try:
    import GPUtil
    GPUTIL_AVAILABLE = True
except ImportError:
    GPUTIL_AVAILABLE = False

class SystemInfo:
    def __init__(self):
        self.wmi_client = wmi.WMI() if WMI_AVAILABLE else None

    def get_cpu_info(self):
        """Get CPU information"""
        info = {
            'name': 'Unknown',
            'cores': psutil.cpu_count(logical=False),
            'threads': psutil.cpu_count(logical=True),
            'usage': psutil.cpu_percent(interval=1),
            'frequency': None,
            'temperature': None
        }

        # Get CPU name via WMI
        if self.wmi_client:
            try:
                for cpu in self.wmi_client.Win32_Processor():
                    info['name'] = cpu.Name.strip()
                    info['frequency'] = cpu.MaxClockSpeed  # MHz
            except:
                pass

        # Try to get temperature
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    if entries:
                        info['temperature'] = entries[0].current
                        break
        except:
            pass

        return info

    def get_gpu_info(self):
        """Get GPU information"""
        gpus = []

        # Try GPUtil for NVIDIA
        if GPUTIL_AVAILABLE:
            try:
                nvidia_gpus = GPUtil.getGPUs()
                for gpu in nvidia_gpus:
                    gpus.append({
                        'name': gpu.name,
                        'vram_total': gpu.memoryTotal,  # MB
                        'vram_used': gpu.memoryUsed,    # MB
                        'vram_free': gpu.memoryFree,    # MB
                        'usage': gpu.load * 100,        # Percentage
                        'temperature': gpu.temperature,
                        'driver': gpu.driver,
                        'type': 'NVIDIA'
                    })
            except:
                pass

        # Fallback to WMI for all GPUs
        if not gpus and self.wmi_client:
            try:
                for gpu in self.wmi_client.Win32_VideoController():
                    vram_bytes = gpu.AdapterRAM if gpu.AdapterRAM else 0
                    gpus.append({
                        'name': gpu.Name,
                        'vram_total': vram_bytes / (1024**2) if vram_bytes > 0 else None,
                        'driver': gpu.DriverVersion,
                        'type': 'Generic'
                    })
            except:
                pass

        return gpus

    def get_ram_info(self):
        """Get RAM information"""
        mem = psutil.virtual_memory()
        info = {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'percent': mem.percent,
            'total_gb': round(mem.total / (1024**3), 1),
            'available_gb': round(mem.available / (1024**3), 1)
        }

        # Try to get RAM speed via WMI
        if self.wmi_client:
            try:
                for mem_stick in self.wmi_client.Win32_PhysicalMemory():
                    info['speed'] = mem_stick.Speed  # MHz
                    break
            except:
                pass

        return info

    def get_disk_info(self):
        """Get disk information"""
        disks = []

        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk = {
                    'drive': partition.device,
                    'mountpoint': partition.mountpoint,
                    'filesystem': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent,
                    'free_gb': round(usage.free / (1024**3), 1),
                    'type': 'Unknown'  # SSD/HDD
                }

                # Try to detect SSD vs HDD
                if self.wmi_client:
                    try:
                        drive_letter = partition.device.replace('\\', '')[:2]
                        for drive in self.wmi_client.Win32_DiskDrive():
                            for part in drive.associators("Win32_DiskDriveToDiskPartition"):
                                for logical in part.associators("Win32_LogicalDiskToPartition"):
                                    if logical.DeviceID == drive_letter:
                                        if 'SSD' in drive.Model or 'NVMe' in drive.Model:
                                            disk['type'] = 'SSD'
                                        elif 'HDD' in drive.Model:
                                            disk['type'] = 'HDD'
                                        else:
                                            # Check MediaType
                                            disk['type'] = 'SSD' if drive.MediaType == 'Fixed hard disk media' else 'Unknown'
                    except:
                        pass

                disks.append(disk)
            except:
                continue

        return disks

    def get_display_info(self):
        """Get display information"""
        info = {
            'resolution': 'Unknown',
            'refresh_rate': None
        }

        if self.wmi_client:
            try:
                for monitor in self.wmi_client.Win32_VideoController():
                    info['resolution'] = f"{monitor.CurrentHorizontalResolution}x{monitor.CurrentVerticalResolution}"
                    info['refresh_rate'] = monitor.CurrentRefreshRate
                    break
            except:
                pass

        return info

    def is_laptop(self):
        """Detect if system is a laptop"""
        if self.wmi_client:
            try:
                for battery in self.wmi_client.Win32_Battery():
                    return True  # Has battery = laptop
            except:
                pass

            try:
                for chassis in self.wmi_client.Win32_SystemEnclosure():
                    # ChassisTypes: 8,9,10,11,12,14,18,21 are laptop types
                    laptop_types = [8, 9, 10, 11, 12, 14, 18, 21]
                    if any(ct in laptop_types for ct in chassis.ChassisTypes):
                        return True
            except:
                pass

        return False

    def get_os_info(self):
        """Get operating system information"""
        return {
            'name': platform.system(),
            'version': platform.version(),
            'release': platform.release(),
            'architecture': platform.machine(),
            'build': platform.win32_ver()[1] if platform.system() == 'Windows' else None
        }

    def get_full_system_info(self):
        """Get complete system information"""
        return {
            'os': self.get_os_info(),
            'cpu': self.get_cpu_info(),
            'gpu': self.get_gpu_info(),
            'ram': self.get_ram_info(),
            'disks': self.get_disk_info(),
            'display': self.get_display_info(),
            'is_laptop': self.is_laptop()
        }
```

---

## Game Detection

### modules/game_detector.py

```python
"""
Game detection module - finds games from all sources
"""
import os
import json
import re
import winreg
from pathlib import Path

class GameDetector:
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.load_data()

    def load_data(self):
        """Load detection data files"""
        # Game folder names in multiple languages
        self.folder_names = [
            # English
            'Games', 'Game', 'My Games', 'PC Games', 'Gaming',
            # Arabic
            'العاب', 'لعب', 'الالعاب', 'العاب اون لاين', 'العاب الكمبيوتر',
            'العاب الفيديو', 'العابي',
            # Other languages
            'Jeux', 'Spiele', 'Juegos', 'Giochi', 'Игры', 'Oyunlar', 'ゲーム', '游戏'
        ]

        # Game engine signatures
        self.engine_signatures = {
            'Unity': ['UnityPlayer.dll', 'UnityEngine.dll', 'data/Managed/Assembly-CSharp.dll'],
            'Unreal Engine': ['UE4Game.exe', 'UE4-Win64-Shipping.exe', 'Engine/Binaries'],
            'Source Engine': ['hl2.exe', 'source_engine.dll', 'gameinfo.txt'],
            'Game Maker': ['data.win', 'options.ini'],
            'RPG Maker': ['Game.exe', 'Audio/BGM'],
            'Godot': ['.pck', 'godot'],
            'CryEngine': ['CryGame.dll', 'CrySystem.dll'],
            'Frostbite': ['frosty.exe', 'FrostyModManager'],
        }

        # Launcher paths and detection
        self.launcher_info = {
            'Steam': {
                'registry_key': r'SOFTWARE\Valve\Steam',
                'registry_value': 'InstallPath',
                'library_file': 'steamapps/libraryfolders.vdf'
            },
            'Epic Games': {
                'default_path': r'C:\Program Files\Epic Games',
                'manifests': r'C:\ProgramData\Epic\EpicGamesLauncher\Data\Manifests'
            },
            'GOG Galaxy': {
                'registry_key': r'SOFTWARE\GOG.com\GalaxyClient\paths',
                'registry_value': 'client'
            },
            'Ubisoft Connect': {
                'registry_key': r'SOFTWARE\Ubisoft\Launcher',
                'registry_value': 'InstallDir'
            },
            'EA App': {
                'default_path': r'C:\Program Files\Electronic Arts'
            },
            'Battle.net': {
                'registry_key': r'SOFTWARE\WOW6432Node\Blizzard Entertainment\Battle.net',
                'default_path': r'C:\Program Files (x86)\Battle.net'
            },
            'Rockstar': {
                'default_path': r'C:\Program Files\Rockstar Games'
            }
        }

    def detect_all_games(self):
        """Main method - detect all games from all sources"""
        all_games = {
            'launcher_games': [],
            'standalone_games': [],
            'shortcut_games': [],
            'total_count': 0
        }

        # Layer 1: Launcher libraries
        all_games['launcher_games'] = self.detect_launcher_games()

        # Layer 2: Folder scanning
        all_games['standalone_games'] = self.detect_standalone_games()

        # Layer 3: Shortcuts
        all_games['shortcut_games'] = self.detect_shortcut_games()

        # Remove duplicates
        all_games = self.deduplicate_games(all_games)

        # Count total
        all_games['total_count'] = (
            len(all_games['launcher_games']) +
            len(all_games['standalone_games']) +
            len(all_games['shortcut_games'])
        )

        return all_games

    def detect_launcher_games(self):
        """Detect games from installed launchers"""
        games = []

        # Steam
        steam_games = self.detect_steam_games()
        games.extend(steam_games)

        # Epic Games
        epic_games = self.detect_epic_games()
        games.extend(epic_games)

        # GOG
        gog_games = self.detect_gog_games()
        games.extend(gog_games)

        # Add more launchers...

        return games

    def detect_steam_games(self):
        """Detect Steam games"""
        games = []
        steam_path = None

        # Find Steam installation
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Valve\Steam')
            steam_path = winreg.QueryValueEx(key, 'SteamPath')[0]
            winreg.CloseKey(key)
        except:
            # Try default paths
            default_paths = [
                r'C:\Program Files (x86)\Steam',
                r'C:\Program Files\Steam',
                r'D:\Steam',
                r'E:\Steam'
            ]
            for path in default_paths:
                if os.path.exists(path):
                    steam_path = path
                    break

        if not steam_path:
            return games

        # Read library folders
        library_file = os.path.join(steam_path, 'steamapps', 'libraryfolders.vdf')
        if os.path.exists(library_file):
            libraries = self.parse_steam_libraries(library_file)
            for lib_path in libraries:
                steamapps = os.path.join(lib_path, 'steamapps', 'common')
                if os.path.exists(steamapps):
                    for game_folder in os.listdir(steamapps):
                        game_path = os.path.join(steamapps, game_folder)
                        if os.path.isdir(game_path):
                            size = self.get_folder_size(game_path)
                            games.append({
                                'name': game_folder,
                                'path': game_path,
                                'launcher': 'Steam',
                                'size_bytes': size,
                                'size': self.format_size(size)
                            })

        return games

    def parse_steam_libraries(self, vdf_path):
        """Parse Steam libraryfolders.vdf file"""
        libraries = []
        try:
            with open(vdf_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Simple regex to extract paths
            paths = re.findall(r'"path"\s+"([^"]+)"', content)
            libraries.extend(paths)
        except:
            pass

        return libraries

    def detect_epic_games(self):
        """Detect Epic Games Store games"""
        games = []
        manifests_path = r'C:\ProgramData\Epic\EpicGamesLauncher\Data\Manifests'

        if os.path.exists(manifests_path):
            for manifest_file in os.listdir(manifests_path):
                if manifest_file.endswith('.item'):
                    manifest_path = os.path.join(manifests_path, manifest_file)
                    try:
                        with open(manifest_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)

                        install_location = data.get('InstallLocation', '')
                        if install_location and os.path.exists(install_location):
                            size = self.get_folder_size(install_location)
                            games.append({
                                'name': data.get('DisplayName', 'Unknown'),
                                'path': install_location,
                                'launcher': 'Epic Games',
                                'size_bytes': size,
                                'size': self.format_size(size)
                            })
                    except:
                        continue

        return games

    def detect_gog_games(self):
        """Detect GOG Galaxy games"""
        games = []
        # GOG stores game info in registry
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\WOW6432Node\GOG.com\Games')
            i = 0
            while True:
                try:
                    game_key_name = winreg.EnumKey(key, i)
                    game_key = winreg.OpenKey(key, game_key_name)
                    try:
                        game_name = winreg.QueryValueEx(game_key, 'gameName')[0]
                        game_path = winreg.QueryValueEx(game_key, 'path')[0]
                        if os.path.exists(game_path):
                            size = self.get_folder_size(game_path)
                            games.append({
                                'name': game_name,
                                'path': game_path,
                                'launcher': 'GOG Galaxy',
                                'size_bytes': size,
                                'size': self.format_size(size)
                            })
                    except:
                        pass
                    winreg.CloseKey(game_key)
                    i += 1
                except WindowsError:
                    break
            winreg.CloseKey(key)
        except:
            pass

        return games

    def detect_standalone_games(self):
        """Detect standalone games by scanning folders"""
        games = []
        scanned_paths = set()

        # Get all drives
        drives = self.get_all_drives()

        for drive in drives:
            # Scan root level game folders
            for folder_name in self.folder_names:
                folder_path = os.path.join(drive, folder_name)
                if os.path.exists(folder_path) and folder_path not in scanned_paths:
                    scanned_paths.add(folder_path)
                    found_games = self.scan_folder_for_games(folder_path)
                    games.extend(found_games)

            # Scan Program Files
            for pf in ['Program Files', 'Program Files (x86)']:
                pf_path = os.path.join(drive, pf)
                if os.path.exists(pf_path):
                    found_games = self.scan_program_files(pf_path)
                    games.extend(found_games)

        return games

    def scan_folder_for_games(self, folder_path, max_depth=2):
        """Scan a folder for game installations"""
        games = []

        try:
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isdir(item_path):
                    # Check if this looks like a game
                    if self.is_likely_game(item_path):
                        engine = self.detect_game_engine(item_path)
                        size = self.get_folder_size(item_path)
                        games.append({
                            'name': item,
                            'path': item_path,
                            'launcher': 'Standalone',
                            'engine': engine,
                            'size_bytes': size,
                            'size': self.format_size(size)
                        })
                    elif max_depth > 0:
                        # Recurse one level deeper
                        games.extend(self.scan_folder_for_games(item_path, max_depth - 1))
        except PermissionError:
            pass

        return games

    def is_likely_game(self, folder_path):
        """Check if a folder is likely a game installation"""
        try:
            contents = os.listdir(folder_path)
        except:
            return False

        # Must have at least one .exe
        has_exe = any(f.endswith('.exe') for f in contents)
        if not has_exe:
            return False

        # Check for game signatures
        for engine, signatures in self.engine_signatures.items():
            for sig in signatures:
                sig_path = os.path.join(folder_path, sig)
                if os.path.exists(sig_path):
                    return True

        # Check for common game files/folders
        game_indicators = [
            'data', 'assets', 'resources', 'levels', 'maps',
            'save', 'saves', 'config', 'settings', 'cfg',
            'bin', 'binaries', 'engine',
            'localization', 'languages', 'audio', 'sound', 'music',
            'video', 'movies', 'cinematics'
        ]

        contents_lower = [c.lower() for c in contents]
        matches = sum(1 for ind in game_indicators if ind in contents_lower)

        return matches >= 2  # At least 2 game indicators

    def detect_game_engine(self, folder_path):
        """Detect which game engine a game uses"""
        for engine, signatures in self.engine_signatures.items():
            for sig in signatures:
                sig_path = os.path.join(folder_path, sig)
                if os.path.exists(sig_path):
                    return engine
        return 'Unknown'

    def detect_shortcut_games(self):
        """Detect games from desktop and start menu shortcuts"""
        games = []

        # Desktop shortcuts
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        games.extend(self.scan_shortcuts(desktop))

        # Start Menu
        start_menu_paths = [
            os.path.join(os.environ.get('APPDATA', ''), r'Microsoft\Windows\Start Menu\Programs'),
            r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs'
        ]
        for path in start_menu_paths:
            if os.path.exists(path):
                games.extend(self.scan_shortcuts(path))

        return games

    def scan_shortcuts(self, folder_path):
        """Scan folder for game shortcuts"""
        games = []
        # This requires win32com - simplified version
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")

            for item in os.listdir(folder_path):
                if item.endswith('.lnk'):
                    try:
                        shortcut_path = os.path.join(folder_path, item)
                        shortcut = shell.CreateShortCut(shortcut_path)
                        target = shortcut.Targetpath

                        if target and os.path.exists(target):
                            target_dir = os.path.dirname(target)
                            if self.is_likely_game(target_dir):
                                games.append({
                                    'name': item.replace('.lnk', ''),
                                    'path': target_dir,
                                    'launcher': 'Shortcut',
                                    'executable': target
                                })
                    except:
                        continue
        except ImportError:
            pass  # win32com not available

        return games

    def get_all_drives(self):
        """Get all available drive letters"""
        import string
        drives = []
        for letter in string.ascii_uppercase:
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                drives.append(drive)
        return drives

    def get_folder_size(self, folder_path):
        """Get total size of a folder in bytes"""
        total = 0
        try:
            for dirpath, dirnames, filenames in os.walk(folder_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    try:
                        total += os.path.getsize(fp)
                    except:
                        pass
        except:
            pass
        return total

    def format_size(self, size_bytes):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"

    def deduplicate_games(self, all_games):
        """Remove duplicate games found by multiple methods"""
        seen_paths = set()

        for category in ['launcher_games', 'standalone_games', 'shortcut_games']:
            unique_games = []
            for game in all_games[category]:
                path = game.get('path', '').lower()
                if path and path not in seen_paths:
                    seen_paths.add(path)
                    unique_games.append(game)
            all_games[category] = unique_games

        return all_games
```

---

## Windows Commands Reference

### Common Repair Commands

```python
# System File Checker
SFC_SCAN = "sfc /scannow"

# DISM Repairs
DISM_CHECK = "DISM /Online /Cleanup-Image /CheckHealth"
DISM_SCAN = "DISM /Online /Cleanup-Image /ScanHealth"
DISM_RESTORE = "DISM /Online /Cleanup-Image /RestoreHealth"

# Disk Check
CHKDSK_SCAN = "chkdsk C: /scan"

# Network
FLUSH_DNS = "ipconfig /flushdns"
RESET_WINSOCK = "netsh winsock reset"
RESET_IP = "netsh int ip reset"
RELEASE_IP = "ipconfig /release"
RENEW_IP = "ipconfig /renew"

# Temp Cleanup
DISK_CLEANUP = "cleanmgr /sagerun:1"

# Power Plans
GET_POWER_PLAN = "powercfg /getactivescheme"
SET_HIGH_PERF = "powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
SET_BALANCED = "powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e"

# Services
LIST_SERVICES = "sc query type= service state= all"
STOP_SERVICE = "sc stop {service_name}"
START_SERVICE = "sc start {service_name}"
DISABLE_SERVICE = "sc config {service_name} start= disabled"
ENABLE_SERVICE = "sc config {service_name} start= auto"

# System Restore
CREATE_RESTORE_POINT = 'powershell -Command "Checkpoint-Computer -Description \\"{description}\\" -RestorePointType MODIFY_SETTINGS"'
```

---

## Registry Operations

### Common Gaming Registry Keys

```python
# Game Mode
GAME_MODE_KEY = r"SOFTWARE\Microsoft\GameBar"
GAME_MODE_VALUE = "AllowAutoGameMode"  # 1 = enabled

# Hardware-Accelerated GPU Scheduling
HAGS_KEY = r"SYSTEM\CurrentControlSet\Control\GraphicsDrivers"
HAGS_VALUE = "HwSchMode"  # 2 = enabled

# Xbox Game Bar
GAMEBAR_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR"
GAMEBAR_VALUE = "AppCaptureEnabled"  # 0 = disabled

# Visual Effects
VISUAL_EFFECTS_KEY = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects"

# Disable Full Screen Optimizations (per-game)
COMPAT_KEY = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"
# Value: game_path = "~ DISABLEDXMAXIMIZEDWINDOWEDMODE"
```

### Safe Registry Operations

```python
import winreg

def read_registry(hive, key_path, value_name):
    """Safely read a registry value"""
    try:
        key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_READ)
        value, value_type = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)
        return value
    except WindowsError:
        return None

def write_registry(hive, key_path, value_name, value, value_type=winreg.REG_DWORD):
    """Safely write a registry value"""
    try:
        key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, value_name, 0, value_type, value)
        winreg.CloseKey(key)
        return True
    except WindowsError:
        return False

def backup_registry_key(hive, key_path, backup_path):
    """Export registry key to backup file"""
    # Use reg export command
    hive_name = {
        winreg.HKEY_LOCAL_MACHINE: "HKLM",
        winreg.HKEY_CURRENT_USER: "HKCU"
    }.get(hive, "HKCU")

    full_key = f"{hive_name}\\{key_path}"
    cmd = f'reg export "{full_key}" "{backup_path}" /y'
    return run_command(cmd)
```

---

## Service Management

### modules/services.py

```python
"""
Service classification and management
"""
import subprocess
import psutil

# Service classifications
CRITICAL_SERVICES = [
    # Windows Core
    'wuauserv',      # Windows Update
    'eventlog',      # Event Log
    'PlugPlay',      # Plug and Play
    'Power',         # Power
    'ProfSvc',       # User Profile Service
    'Schedule',      # Task Scheduler
    'SENS',          # System Event Notification Service
    'SystemEventsBroker',
    'LSM',           # Local Session Manager
    'SamSs',         # Security Accounts Manager
    'LanmanWorkstation',  # Workstation
    'RpcSs',         # Remote Procedure Call
    'RpcEptMapper',
    'DcomLaunch',    # DCOM Server Process Launcher

    # Security
    'WinDefend',     # Windows Defender
    'mpssvc',        # Windows Firewall
    'WdNisSvc',      # Windows Defender Network Inspection
    'SecurityHealthService',

    # Storage
    'stisvc',        # Windows Image Acquisition
    'StorSvc',       # Storage Service

    # Network
    'Dhcp',          # DHCP Client
    'Dnscache',      # DNS Client
    'NlaSvc',        # Network Location Awareness
    'netprofm',      # Network List Service
]

GAMING_ESSENTIAL = [
    # Audio
    'Audiosrv',      # Windows Audio
    'AudioEndpointBuilder',

    # GPU (vary by vendor)
    'NVDisplay.ContainerLocalSystem',  # NVIDIA
    'AMD External Events Utility',     # AMD

    # Input
    'HidServ',       # Human Interface Device Service
    'XboxGipSvc',    # Xbox Accessory Management
]

SAFE_TO_DISABLE = {
    'Spooler': 'Print Spooler - Disable if you dont print',
    'Fax': 'Fax Service - Most users dont need this',
    'WSearch': 'Windows Search - Saves CPU/disk, slower file search',
    'SysMain': 'Superfetch - Can reduce RAM usage',
    'DiagTrack': 'Telemetry - Microsoft tracking',
    'dmwappushservice': 'Push messaging - Telemetry related',
    'RemoteRegistry': 'Remote Registry - Security risk if enabled',
    'lfsvc': 'Geolocation Service - Unless you need location features',
    'MapsBroker': 'Maps Broker - Unless you use Windows Maps',
    'WbioSrvc': 'Biometric Service - Unless you use fingerprint/face login',
}

RESOURCE_HOGS = [
    'SysMain',       # Superfetch - High disk on HDD
    'WSearch',       # Windows Search - High disk/CPU during indexing
    'DiagTrack',     # Telemetry
    'wuauserv',      # Windows Update - Only during updates
]

def get_service_status(service_name):
    """Get current status of a service"""
    try:
        for service in psutil.win_service_iter():
            if service.name() == service_name:
                return {
                    'name': service.name(),
                    'display_name': service.display_name(),
                    'status': service.status(),
                    'start_type': service.start_type()
                }
    except:
        pass
    return None

def get_all_services():
    """Get all services with classification"""
    services = []
    for service in psutil.win_service_iter():
        try:
            svc = {
                'name': service.name(),
                'display_name': service.display_name(),
                'status': service.status(),
                'start_type': service.start_type(),
                'classification': classify_service(service.name())
            }
            services.append(svc)
        except:
            continue
    return services

def classify_service(service_name):
    """Classify a service by risk level"""
    if service_name in CRITICAL_SERVICES:
        return 'CRITICAL'
    elif service_name in GAMING_ESSENTIAL:
        return 'GAMING_ESSENTIAL'
    elif service_name in SAFE_TO_DISABLE:
        return 'SAFE_TO_DISABLE'
    elif service_name in RESOURCE_HOGS:
        return 'RESOURCE_HOG'
    else:
        return 'REVIEW_NEEDED'

def stop_service(service_name):
    """Stop a service (requires admin)"""
    result = subprocess.run(
        f'sc stop "{service_name}"',
        shell=True, capture_output=True, text=True
    )
    return result.returncode == 0

def start_service(service_name):
    """Start a service (requires admin)"""
    result = subprocess.run(
        f'sc start "{service_name}"',
        shell=True, capture_output=True, text=True
    )
    return result.returncode == 0
```

---

## Process Management

### modules/process_manager.py

```python
"""
Process analysis and management
"""
import psutil
from collections import defaultdict

PROTECTED_PROCESSES = [
    'system', 'smss.exe', 'csrss.exe', 'wininit.exe', 'services.exe',
    'lsass.exe', 'winlogon.exe', 'explorer.exe', 'dwm.exe',
    'svchost.exe', 'spoolsv.exe', 'taskhostw.exe',
    'msmpeng.exe',  # Windows Defender
    'securityhealthservice.exe'
]

def get_process_list():
    """Get all processes with resource usage"""
    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent', 'status']):
        try:
            pinfo = proc.info
            mem_mb = pinfo['memory_info'].rss / (1024 * 1024) if pinfo['memory_info'] else 0

            processes.append({
                'pid': pinfo['pid'],
                'name': pinfo['name'],
                'memory_mb': round(mem_mb, 1),
                'cpu_percent': pinfo['cpu_percent'],
                'status': pinfo['status'],
                'is_protected': pinfo['name'].lower() in PROTECTED_PROCESSES
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return processes

def get_top_ram_processes(count=10):
    """Get top RAM consuming processes"""
    processes = get_process_list()
    sorted_procs = sorted(processes, key=lambda x: x['memory_mb'], reverse=True)
    return sorted_procs[:count]

def get_top_cpu_processes(count=10):
    """Get top CPU consuming processes"""
    # Need to sample CPU over time
    for proc in psutil.process_iter():
        try:
            proc.cpu_percent()
        except:
            pass

    import time
    time.sleep(1)  # Wait for accurate reading

    processes = get_process_list()
    # Re-sample
    for proc in psutil.process_iter(['pid', 'cpu_percent']):
        try:
            for p in processes:
                if p['pid'] == proc.info['pid']:
                    p['cpu_percent'] = proc.info['cpu_percent']
        except:
            continue

    sorted_procs = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)
    return sorted_procs[:count]

def aggregate_by_name(processes):
    """Aggregate processes by name (e.g., multiple chrome.exe)"""
    aggregated = defaultdict(lambda: {'count': 0, 'memory_mb': 0, 'pids': []})

    for proc in processes:
        name = proc['name']
        aggregated[name]['count'] += 1
        aggregated[name]['memory_mb'] += proc['memory_mb']
        aggregated[name]['pids'].append(proc['pid'])
        aggregated[name]['is_protected'] = proc['is_protected']

    return dict(aggregated)

def safe_kill_process(pid):
    """Safely terminate a process"""
    try:
        proc = psutil.Process(pid)
        name = proc.name().lower()

        if name in PROTECTED_PROCESSES:
            return False, "Protected system process"

        proc.terminate()
        proc.wait(timeout=5)
        return True, "Process terminated"
    except psutil.NoSuchProcess:
        return True, "Process already ended"
    except psutil.TimeoutExpired:
        try:
            proc.kill()
            return True, "Process killed (forced)"
        except:
            return False, "Failed to kill process"
    except Exception as e:
        return False, str(e)
```

---

## Snapshot System

### modules/snapshots.py

```python
"""
Snapshot and rollback system
"""
import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

class SnapshotManager:
    def __init__(self, snapshots_dir):
        self.snapshots_dir = Path(snapshots_dir)
        self.snapshots_dir.mkdir(exist_ok=True)

    def create_snapshot(self, action_name, include_restore_point=True):
        """Create a full snapshot before an action"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        safe_action = action_name.replace(' ', '_')[:30]
        snapshot_name = f"{timestamp}_{safe_action}"
        snapshot_path = self.snapshots_dir / snapshot_name
        snapshot_path.mkdir(exist_ok=True)

        snapshot_info = {
            'created': datetime.now().isoformat(),
            'action': action_name,
            'components': []
        }

        # Save service states
        if self.save_service_states(snapshot_path):
            snapshot_info['components'].append('services')

        # Create Windows restore point (requires admin)
        if include_restore_point:
            if self.create_restore_point(f"GameFix Doctor - {action_name}"):
                snapshot_info['components'].append('restore_point')

        # Save snapshot info
        info_path = snapshot_path / 'info.json'
        with open(info_path, 'w') as f:
            json.dump(snapshot_info, f, indent=2)

        return str(snapshot_path)

    def save_service_states(self, snapshot_path):
        """Save current state of all services"""
        try:
            import psutil
            services = []
            for service in psutil.win_service_iter():
                try:
                    services.append({
                        'name': service.name(),
                        'status': service.status(),
                        'start_type': service.start_type()
                    })
                except:
                    continue

            services_path = snapshot_path / 'services.json'
            with open(services_path, 'w') as f:
                json.dump(services, f, indent=2)
            return True
        except:
            return False

    def create_restore_point(self, description):
        """Create a Windows System Restore point"""
        try:
            # Enable system restore first (might already be enabled)
            enable_cmd = 'powershell -Command "Enable-ComputerRestore -Drive C:"'
            subprocess.run(enable_cmd, shell=True, capture_output=True)

            # Create restore point
            create_cmd = f'''powershell -Command "Checkpoint-Computer -Description '{description}' -RestorePointType 'MODIFY_SETTINGS'"'''
            result = subprocess.run(create_cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

    def list_snapshots(self):
        """List all available snapshots"""
        snapshots = []
        for item in self.snapshots_dir.iterdir():
            if item.is_dir():
                info_path = item / 'info.json'
                if info_path.exists():
                    try:
                        with open(info_path, 'r') as f:
                            info = json.load(f)
                        info['path'] = str(item)
                        info['name'] = item.name
                        snapshots.append(info)
                    except:
                        continue

        # Sort by creation date (newest first)
        snapshots.sort(key=lambda x: x.get('created', ''), reverse=True)
        return snapshots

    def restore_snapshot(self, snapshot_path):
        """Restore from a snapshot"""
        snapshot_path = Path(snapshot_path)
        results = {
            'services': False,
            'errors': []
        }

        # Restore services
        services_path = snapshot_path / 'services.json'
        if services_path.exists():
            try:
                with open(services_path, 'r') as f:
                    services = json.load(f)

                for svc in services:
                    try:
                        # Restore start type
                        start_types = {
                            'automatic': 'auto',
                            'manual': 'demand',
                            'disabled': 'disabled'
                        }
                        start_type = start_types.get(svc['start_type'], 'demand')
                        cmd = f'sc config "{svc["name"]}" start= {start_type}'
                        subprocess.run(cmd, shell=True, capture_output=True)

                        # Restore running state
                        if svc['status'] == 'running':
                            subprocess.run(f'sc start "{svc["name"]}"', shell=True, capture_output=True)
                        elif svc['status'] == 'stopped':
                            subprocess.run(f'sc stop "{svc["name"]}"', shell=True, capture_output=True)
                    except Exception as e:
                        results['errors'].append(f"{svc['name']}: {str(e)}")

                results['services'] = True
            except Exception as e:
                results['errors'].append(f"Service restore failed: {str(e)}")

        return results

    def delete_snapshot(self, snapshot_path):
        """Delete a snapshot"""
        import shutil
        try:
            shutil.rmtree(snapshot_path)
            return True
        except:
            return False
```

---

## Error Handling

### Best Practices

```python
"""
Error handling patterns for GameFix Doctor Pro
"""
import logging
from functools import wraps

# Setup logging
logging.basicConfig(
    filename='gamefix_doctor.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def safe_execute(default_return=None):
    """Decorator for safe execution with logging"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error(f"Error in {func.__name__}: {str(e)}")
                return default_return
        return wrapper
    return decorator

class GameFixError(Exception):
    """Base exception for GameFix Doctor"""
    pass

class AdminRequiredError(GameFixError):
    """Raised when admin privileges are required"""
    pass

class SnapshotError(GameFixError):
    """Raised when snapshot creation/restoration fails"""
    pass

class RepairError(GameFixError):
    """Raised when a repair action fails"""
    pass

def handle_error(error, show_to_user=True):
    """Central error handler"""
    logging.error(str(error))

    if show_to_user:
        from core.ui import print_status

        if isinstance(error, AdminRequiredError):
            print_status("FAIL", "This action requires administrator privileges.")
            print_status("INFO", "Please restart the tool as administrator.")
        elif isinstance(error, SnapshotError):
            print_status("FAIL", "Could not create safety snapshot.")
            print_status("INFO", "The action was cancelled for your safety.")
        elif isinstance(error, RepairError):
            print_status("FAIL", f"Repair failed: {str(error)}")
        else:
            print_status("FAIL", f"An error occurred: {str(error)}")
```

---

## Building EXE

### PyInstaller Configuration

```python
# build.py
import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'gamefix_doctor.py',
    '--onefile',
    '--name=GameFixDoctorPro',
    '--icon=assets/icon.ico',  # Add icon if available
    '--add-data=data;data',     # Include data folder
    '--uac-admin',              # Request admin on launch
    '--console',                # Keep console window
    '--clean',
    '--noconfirm',
])
```

### Build Command
```bash
# Simple build
pyinstaller --onefile --console --uac-admin --name GameFixDoctorPro gamefix_doctor.py

# With data files
pyinstaller --onefile --console --uac-admin --name GameFixDoctorPro --add-data "data;data" gamefix_doctor.py
```

### Spec File (gamefix_doctor.spec)
```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['gamefix_doctor.py'],
    pathex=[],
    binaries=[],
    datas=[('data', 'data')],
    hiddenimports=['wmi', 'win32com.client', 'psutil'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GameFixDoctorPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=True,
    icon='assets/icon.ico'
)
```

---

## Testing Checklist

Before release, test:

1. [ ] Admin elevation works
2. [ ] System info detection accurate
3. [ ] Game detection finds games correctly
4. [ ] Health check reports accurate status
5. [ ] Repairs execute without errors
6. [ ] Snapshots create and restore correctly
7. [ ] Service changes persist
8. [ ] Process killing is safe
9. [ ] Reports generate correctly
10. [ ] EXE runs on clean Windows install
11. [ ] Works on Windows 10
12. [ ] Works on Windows 11
13. [ ] Handles missing dependencies gracefully
14. [ ] No crashes on permission denied
15. [ ] UI renders correctly in CMD
