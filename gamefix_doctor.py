"""Main entrypoint for GameFix Doctor Pro."""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any

from core import config
from core.admin import ensure_admin
from core.data_init import initialize_data_files
from core.ui import (
    clear_screen,
    confirm,
    get_choice,
    press_enter,
    print_developer_card,
    print_header,
    print_main_banner,
    print_menu,
    print_status,
)
from core.utils import run_command


def ensure_dependencies() -> bool:
    required = ("psutil", "colorama")
    missing = []
    for package in required:
        try:
            importlib.import_module(package)
        except Exception:
            missing.append(package)
    if not missing:
        return True

    print_header("Missing Dependencies")
    print_status("FAIL", "Required packages are not installed.")
    for package in missing:
        print(f"  - {package}")
    print("\n  Run: pip install -r requirements.txt")
    return False


def show_quick_health_check(system_info, health_checker_cls, state: dict[str, Any]) -> None:
    clear_screen()
    print_header("Quick Health Check")
    checker = health_checker_cls(system_info)
    result = checker.run()
    for row in result["checks"]:
        print_status(row["status"], f'{row["name"]}: {row["message"]}')
    print()
    print_status("INFO", f'Overall Score: {result["score"]}/10')
    for tip in result["tips"]:
        print_status("INFO", tip)
    state["quick_health"] = result
    press_enter()


def show_full_scan(full_scan, state: dict[str, Any]) -> None:
    clear_screen()
    print_header("Full System Scan")
    print_status("INFO", "Running deep scan. This may take a moment...")
    result = full_scan.run()
    state["full_scan"] = result

    summary = result.get("summary", {})
    print_status("OK", f"Services running: {summary.get('services_running', 0)} / {summary.get('services_total', 0)}")
    print_status("OK", f"Games detected: {summary.get('games_detected', 0)}")
    print_status("OK", f"Top RAM processes listed: {summary.get('ram_top_count', 0)}")
    print_status("OK", f"Top CPU processes listed: {summary.get('cpu_top_count', 0)}")
    print_status("INFO", f"Network status: {summary.get('network_status', 'unknown')}")

    print()
    print_status("INFO", "Detected issues:")
    for issue in result.get("issues", []):
        sev = issue.get("severity", "info").upper()
        print(f"  - [{sev}] {issue.get('message', '')}")
    press_enter()


def show_find_games(game_detector, state: dict[str, Any]) -> None:
    clear_screen()
    print_header("Find My Games")
    result = game_detector.detect()
    state["games"] = result

    print_status("OK", f"Total games found: {result.get('total_count', 0)}")
    print_status("INFO", f"Launcher games: {len(result.get('launcher_games', []))}")
    print_status("INFO", f"Standalone games: {len(result.get('standalone_games', []))}")
    print_status("INFO", f"Shortcut games: {len(result.get('shortcut_games', []))}")
    print()
    for game in result.get("all_games", [])[:20]:
        src = game.get("source", "unknown")
        print(f"  - {game.get('name', 'Unknown')} [{src}]")
    if result.get("total_count", 0) > 20:
        print("  ...")
    press_enter()


def show_diagnosis(diagnosis_engine, state: dict[str, Any]) -> None:
    clear_screen()
    print_header("Diagnose Problems")
    result = diagnosis_engine.run()
    state["diagnosis"] = result

    print_status("INFO", f"Total issues: {result.get('issue_count', 0)}")
    print()
    for issue in result.get("issues", []):
        sev = str(issue.get("severity", "info")).upper()
        print(f"  [{sev}] {issue.get('title', 'Issue')}")
        print(f"      {issue.get('details', '')}")
        print(f"      Fix: {issue.get('fix', '')}")
        print()
    press_enter()


def show_repair_center(repairs, snapshots, settings_manager) -> None:
    while True:
        clear_screen()
        print_header("Repair Center")
        print_menu(
            {
                "1": "Scan System Files (SFC)",
                "2": "Repair Windows Image (DISM)",
                "3": "Clear Temp Files",
                "4": "Flush DNS Cache",
                "5": "Enable Game Mode",
                "6": "Set High Performance Power Plan",
                "0": "Back",
            }
        )
        choice = get_choice()
        if choice == "0":
            return

        action = {
            "1": ("Run SFC scan", repairs.run_sfc, True),
            "2": ("Run DISM restore health", repairs.run_dism, True),
            "3": ("Clear temp files", repairs.clear_temp_files, False),
            "4": ("Flush DNS cache", repairs.flush_dns, False),
            "5": ("Enable Game Mode", repairs.enable_game_mode, False),
            "6": ("Set high performance power plan", repairs.set_high_performance_power, False),
        }.get(choice)

        if not action:
            continue

        description, func, risky = action
        if not confirm(f"You are about to {description}. Continue?"):
            continue

        if risky and _snapshot_required(settings_manager):
            if not _create_snapshot_or_cancel(snapshots, description):
                press_enter()
                continue

        result = func()
        print_status("OK" if result.get("success") else "FAIL", result.get("message", "Unknown result"))
        press_enter()


def show_services(services, snapshots, settings_manager) -> None:
    while True:
        clear_screen()
        print_header("Service Optimizer")
        candidates = services.get_recommended_to_stop()
        if not candidates:
            print_status("OK", "No safe running services to stop right now.")
            press_enter()
            return

        for idx, svc in enumerate(candidates, start=1):
            print(f"  [{idx}] {svc['name']} - {svc['display_name']}")
        print("\n  [0] Back")
        value = get_choice("Select a service to stop: ")
        if value == "0":
            return
        if not value.isdigit() or not (1 <= int(value) <= len(candidates)):
            print_status("WARN", "Invalid choice.")
            press_enter()
            continue

        service = candidates[int(value) - 1]
        if not confirm(f"Stop service '{service['name']}'?"):
            continue

        if _snapshot_required(settings_manager):
            if not _create_snapshot_or_cancel(snapshots, f"Stop service {service['name']}"):
                press_enter()
                continue

        ok, message = services.stop_service(service["name"])
        print_status("OK" if ok else "FAIL", message)
        press_enter()


def show_processes(process_manager) -> None:
    while True:
        clear_screen()
        print_header("Process Killer")
        processes = process_manager.get_closable_processes(min_ram_mb=300, top_n=20)
        if not processes:
            print_status("OK", "No notable closeable processes found.")
            press_enter()
            return

        print("  #  Name                           RAM MB   CPU%   PID")
        print("  -- ----------------------------- ------- ------ -----")
        for idx, proc in enumerate(processes, start=1):
            cpu = proc.get("cpu_percent", 0.0)
            print(f"  {idx:>2}  {proc['name'][:29]:<29} {proc['memory_mb']:>7.1f} {cpu:>6.1f} {proc['pid']:>5}")
        print("\n  [0] Back")
        value = get_choice("Select a process to close: ")
        if value == "0":
            return
        if not value.isdigit() or not (1 <= int(value) <= len(processes)):
            print_status("WARN", "Invalid choice.")
            press_enter()
            continue

        proc = processes[int(value) - 1]
        if not confirm(f"Close process '{proc['name']}' (PID {proc['pid']})?"):
            continue
        ok, message = process_manager.close_process(proc["pid"])
        print_status("OK" if ok else "FAIL", message)
        press_enter()


def show_app_scanner(app_checker, state: dict[str, Any]) -> None:
    clear_screen()
    print_header("App Scanner")
    result = app_checker.scan()
    state["app_scan"] = result

    summary = result.get("summary", {})
    print_status("INFO", f"Installed apps detected: {summary.get('total_apps', 0)}")
    print_status("INFO", f"Gaming essential: {summary.get('gaming_essential', 0)}")
    print_status("WARN", f"Potentially heavy: {summary.get('potentially_heavy', 0)}")
    print_status("WARN", f"Known bloatware: {summary.get('known_bloatware', 0)}")
    print_status("WARN", f"Fake optimizers: {summary.get('fake_optimizers', 0)}")
    print_status("WARN", f"Adware risk: {summary.get('adware_risk', 0)}")
    press_enter()


def show_settings_advisor(settings_recommender, state: dict[str, Any]) -> None:
    clear_screen()
    print_header("Settings Advisor")
    result = settings_recommender.recommend()
    state["settings_advisor"] = result

    hw = result.get("hardware", {})
    print_status("INFO", f"CPU: {hw.get('cpu', 'Unknown')} ({hw.get('cpu_tier', 'unknown')})")
    print_status("INFO", f"GPU: {hw.get('gpu', 'Unknown')} ({hw.get('gpu_tier', 'unknown')})")
    print_status("INFO", f"RAM: {hw.get('ram_gb', 0)} GB ({hw.get('ram_tier', 'unknown')})")
    print()
    profile = result.get("recommended_profile", "balanced")
    print_status("OK", f"Recommended profile: {profile}")
    settings = result.get("profile_settings", {}).get("settings", {})
    for key, value in list(settings.items())[:12]:
        print(f"  - {key}: {value}")
    press_enter()


def show_network_doctor(network_doctor, snapshots, settings_manager, state: dict[str, Any]) -> None:
    while True:
        clear_screen()
        print_header("Network Doctor")
        print_menu(
            {
                "1": "Run Network Diagnostics",
                "2": "Flush DNS Cache",
                "3": "Set Gaming DNS (1.1.1.1 / 8.8.8.8)",
                "4": "Reset Winsock (requires reboot)",
                "5": "Reset TCP/IP Stack (requires reboot)",
                "0": "Back",
            }
        )
        choice = get_choice()
        if choice == "0":
            return

        if choice == "1":
            result = network_doctor.diagnose()
            state["network"] = result
            print_status("INFO", result.get("summary", "No summary"))
            for adapter in result.get("adapters", []):
                print(f"  - Adapter: {adapter['name']} ({adapter['type']}, {adapter['speed_mbps']} Mbps)")
            dns = result.get("dns_servers", [])
            if dns:
                print(f"  - DNS: {', '.join(dns)}")
            for ping in result.get("pings", []):
                print(f"  - Ping {ping['host']}: {ping.get('avg_ms', 'N/A')} ms")
            press_enter()
            continue

        if choice in {"4", "5"} and _snapshot_required(settings_manager):
            if not _create_snapshot_or_cancel(snapshots, "Network reset"):
                press_enter()
                continue

        if choice == "2":
            result = network_doctor.flush_dns()
        elif choice == "3":
            result = network_doctor.set_dns()
        elif choice == "4":
            result = network_doctor.reset_winsock()
        elif choice == "5":
            result = network_doctor.reset_ip_stack()
        else:
            continue
        print_status("OK" if result.get("success") else "FAIL", result.get("message", "Unknown result"))
        press_enter()


def show_driver_check(driver_checker, state: dict[str, Any]) -> None:
    clear_screen()
    print_header("Driver Check")
    result = driver_checker.check()
    state["drivers"] = result

    if result.get("status") != "ok":
        print_status("WARN", result.get("message", "Driver check not fully available."))
        press_enter()
        return

    print_status("INFO", "GPU drivers:")
    for item in result.get("gpu", []):
        age = item.get("driver_age_note", "Unknown")
        print(f"  - {item.get('name')}: {item.get('driver_version')} [{age}]")

    print("\n  Audio drivers:")
    for item in result.get("audio", [])[:5]:
        print(f"  - {item.get('device_name')}: {item.get('driver_version')}")

    print("\n  Network drivers:")
    for item in result.get("network", [])[:5]:
        print(f"  - {item.get('device_name')}: {item.get('driver_version')}")
    press_enter()


def show_power_optimizer(power_optimizer, system_info, state: dict[str, Any]) -> None:
    while True:
        clear_screen()
        print_header("Power Optimizer")
        current = power_optimizer.get_current_plan()
        is_laptop = bool(system_info.is_laptop()) if hasattr(system_info, "is_laptop") else False
        recommendation = power_optimizer.recommend(is_laptop=is_laptop, on_battery=False)
        print_status("INFO", f"Current plan: {current}")
        print_status("INFO", f"Recommended: {recommendation['recommended']} ({recommendation['reason']})")
        state["power"] = {"current": current, "recommendation": recommendation}
        print_menu(
            {
                "1": "Set High Performance",
                "2": "Set Balanced",
                "3": "Set Power Saver",
                "0": "Back",
            }
        )
        choice = get_choice()
        if choice == "0":
            return
        if choice == "1":
            result = power_optimizer.set_high_performance()
        elif choice == "2":
            result = power_optimizer.set_balanced()
        elif choice == "3":
            result = power_optimizer.set_power_saver()
        else:
            continue
        print_status("OK" if result.get("success") else "FAIL", result.get("message", "Unknown result"))
        press_enter()


def show_snapshots(snapshots) -> None:
    while True:
        clear_screen()
        print_header("Snapshots & Rollback")
        print_menu(
            {
                "1": "List/Restore Tool Snapshots",
                "2": "List Windows Restore Points",
                "3": "Restore Windows Restore Point",
                "0": "Back",
            }
        )
        choice = get_choice()
        if choice == "0":
            return

        if choice == "1":
            items = snapshots.list_snapshots()
            if not items:
                print_status("INFO", "No tool snapshots found yet.")
                press_enter()
                continue
            for idx, item in enumerate(items, start=1):
                action = item.get("action", "Unknown action")
                created = item.get("created", "Unknown date")
                print(f"  [{idx}] {item['name']} | {action} | {created}")
            print("\n  [0] Cancel")
            value = get_choice("Select snapshot to restore: ")
            if value == "0":
                continue
            if not value.isdigit() or not (1 <= int(value) <= len(items)):
                print_status("WARN", "Invalid choice.")
                press_enter()
                continue
            snapshot = items[int(value) - 1]
            if not confirm(f"Restore tool snapshot '{snapshot['name']}'?"):
                continue
            result = snapshots.restore_snapshot(snapshot["path"])
            if result.get("errors"):
                print_status("WARN", "Snapshot restore completed with warnings:")
                for err in result["errors"][:10]:
                    print(f"  - {err}")
            else:
                print_status("OK", "Tool snapshot restored successfully.")
            press_enter()
            continue

        if choice == "2":
            points = snapshots.list_windows_restore_points()
            if not points:
                print_status("INFO", "No Windows restore points found (or unavailable).")
                press_enter()
                continue
            print_status("INFO", "Windows Restore Points:")
            for idx, point in enumerate(points, start=1):
                print(
                    f"  [{idx}] #{point['sequence_number']} | "
                    f"{point['description']} | {point['creation_time']}"
                )
            press_enter()
            continue

        if choice == "3":
            points = snapshots.list_windows_restore_points()
            if not points:
                print_status("INFO", "No Windows restore points found (or unavailable).")
                press_enter()
                continue
            for idx, point in enumerate(points, start=1):
                print(
                    f"  [{idx}] #{point['sequence_number']} | "
                    f"{point['description']} | {point['creation_time']}"
                )
            print("\n  [0] Cancel")
            value = get_choice("Select Windows restore point to apply: ")
            if value == "0":
                continue
            if not value.isdigit() or not (1 <= int(value) <= len(points)):
                print_status("WARN", "Invalid choice.")
                press_enter()
                continue
            selected = points[int(value) - 1]
            print_status("WARN", "This uses native Windows System Restore and may require restart.")
            if not confirm(
                f"Restore to point #{selected['sequence_number']} "
                f"({selected['description']})?"
            ):
                continue
            result = snapshots.restore_windows_restore_point(selected["sequence_number"])
            print_status("OK" if result.get("success") else "FAIL", result.get("message", "Unknown result"))
            press_enter()
            continue

        print_status("WARN", "Invalid menu choice.")
        press_enter()


def show_reports(reporter, state: dict[str, Any]) -> None:
    while True:
        clear_screen()
        print_header("Reports")
        print_menu(
            {
                "1": "Export Latest Results as JSON",
                "2": "Export Summary TXT Report",
                "3": "Export Summary HTML Report",
                "0": "Back",
            }
        )
        choice = get_choice()
        if choice == "0":
            return
        if not state:
            print_status("WARN", "No data available yet. Run checks/scans first.")
            press_enter()
            continue

        if choice == "1":
            path = reporter.save_json_report("latest_state", state)
            print_status("OK", f"JSON report saved: {path}")
        elif choice == "2":
            sections = []
            for key, payload in state.items():
                text = json.dumps(payload, indent=2, ensure_ascii=False)[:4000]
                sections.append((key, text.splitlines()))
            path = reporter.save_txt_report("summary", "GameFix Doctor Pro Report", sections)
            print_status("OK", f"TXT report saved: {path}")
        elif choice == "3":
            path = reporter.save_html_report("summary", "GameFix Doctor Pro Report", state)
            print_status("OK", f"HTML report saved: {path}")
        else:
            continue
        press_enter()


def show_settings(settings_manager) -> None:
    while True:
        clear_screen()
        print_header("Settings")
        current = settings_manager.load()
        print(f"  [1] Create snapshots before repairs: {current['create_snapshots_before_repairs']}")
        print(f"  [2] Auto-scan on startup: {current['auto_scan_on_startup']}")
        print(f"  [3] Check for updates: {current['check_for_updates']}")
        print(f"  [4] Show advanced options: {current['show_advanced_options']}")
        print(f"  [5] Theme: {current['theme']}")
        print(f"  [6] Startup essentials check: {current.get('startup_essentials_check', True)}")
        print("\n  [0] Back")

        choice = get_choice("Choose a setting to toggle/change: ")
        if choice == "0":
            return
        if choice == "1":
            new_value = (
                "Ask"
                if current["create_snapshots_before_repairs"] == "Always"
                else "Always"
            )
            settings_manager.set_value("create_snapshots_before_repairs", new_value)
        elif choice == "2":
            settings_manager.toggle_bool("auto_scan_on_startup")
        elif choice == "3":
            settings_manager.toggle_bool("check_for_updates")
        elif choice == "4":
            settings_manager.toggle_bool("show_advanced_options")
        elif choice == "5":
            new_value = "Minimal" if current["theme"] == "Colors" else "Colors"
            settings_manager.set_value("theme", new_value)
        elif choice == "6":
            settings_manager.toggle_bool("startup_essentials_check")
        else:
            continue
        print_status("OK", "Setting updated.")
        press_enter()


def show_essentials_installer(essentials_manager, state: dict[str, Any]) -> None:
    while True:
        clear_screen()
        print_header("Gaming Essentials Installer")
        latest = essentials_manager.quick_startup_check()
        state["essentials"] = latest

        print_status("INFO", f"Items needing action: {latest.get('needs_action_count', 0)}")
        print()
        for row in latest.get("checks", []):
            print_status(row.get("status", "INFO"), f"{row.get('name')}: {row.get('message')}")
            action = row.get("action")
            if action and action != "None":
                print(f"      Action: {action}")
        optional = latest.get("optional_checks", [])
        if optional:
            print()
            print_status("INFO", "Optional gaming components:")
            for row in optional:
                print_status(row.get("status", "INFO"), f"{row.get('name')}: {row.get('message')}")
                action = row.get("action")
                if action and action != "None":
                    print(f"      Optional action: {action}")

        print_menu(
            {
                "1": "Open DirectX Installer Page",
                "2": "Open .NET Download Page",
                "3": "Open VC++ Redist Page",
                "4": "Open AIO Runtime Page",
                "5": "Open GPU Driver Page (auto vendor)",
                "6": "Open Windows Update",
                "7": "Re-check Essentials",
                "8": "Auto-Install VC++ (winget)",
                "9": "Auto-Install .NET Runtime (winget)",
                "10": "Auto-Install DirectX (winget best effort)",
                "11": "Auto-Install Missing Essentials (winget batch)",
                "12": "Auto-Install WebView2 Runtime (winget)",
                "13": "Enable DirectPlay (legacy feature)",
                "14": "Auto-Install NVIDIA PhysX (winget)",
                "15": "Open Optional Features (Windows)",
                "16": "Open Media Feature Pack Guide",
                "17": "Open OpenAL Download Page",
                "18": "Open Vulkan Runtime Page",
                "0": "Back",
            }
        )
        choice = get_choice()
        if choice == "0":
            return

        if choice == "1":
            result = essentials_manager.open_directx_page()
        elif choice == "2":
            result = essentials_manager.open_dotnet_page()
        elif choice == "3":
            result = essentials_manager.open_vc_redist_page()
        elif choice == "4":
            result = essentials_manager.open_aio_runtime_page()
        elif choice == "5":
            result = essentials_manager.open_gpu_driver_page()
        elif choice == "6":
            result = essentials_manager.open_windows_update()
        elif choice == "7":
            continue
        elif choice == "8":
            if not confirm("Install/Update VC++ Redistributables via winget now?"):
                continue
            result = essentials_manager.install_vc_redist_winget()
            if not result.get("success"):
                print_status("WARN", "Winget VC++ install failed. Opening official page...")
                essentials_manager.open_vc_redist_page()
        elif choice == "9":
            if not confirm("Install/Update .NET Runtime via winget now?"):
                continue
            result = essentials_manager.install_dotnet_runtime_winget()
            if not result.get("success"):
                print_status("WARN", "Winget .NET install failed. Opening official page...")
                essentials_manager.open_dotnet_page()
        elif choice == "10":
            if not confirm("Try DirectX install/update via winget now?"):
                continue
            result = essentials_manager.install_directx_winget()
            if not result.get("success"):
                print_status("WARN", "Winget DirectX install failed. Opening official page...")
                essentials_manager.open_directx_page()
        elif choice == "11":
            if not confirm("Run winget batch for missing essentials now?"):
                continue
            result = essentials_manager.install_missing_essentials_winget()
            if result.get("report"):
                for item in result["report"]:
                    print_status(
                        "OK" if item.get("success") else "WARN",
                        f"{item.get('item')}: {item.get('message')}",
                    )
                print()
        elif choice == "12":
            if not confirm("Install/Update WebView2 Runtime via winget now?"):
                continue
            result = essentials_manager.install_webview2_winget()
            if not result.get("success"):
                print_status("WARN", "Winget WebView2 install failed. Opening .NET/WebView2 page...")
                essentials_manager.open_dotnet_page()
        elif choice == "13":
            if not confirm("Enable DirectPlay legacy Windows feature now?"):
                continue
            result = essentials_manager.enable_directplay()
        elif choice == "14":
            if not confirm("Install/Update NVIDIA PhysX via winget now?"):
                continue
            result = essentials_manager.install_physx_winget()
            if not result.get("success"):
                print_status("WARN", "Winget PhysX install failed. Opening NVIDIA PhysX page...")
                essentials_manager.open_physx_page()
        elif choice == "15":
            result = essentials_manager.open_optional_features()
        elif choice == "16":
            result = essentials_manager.open_media_feature_pack_page()
        elif choice == "17":
            result = essentials_manager.open_openal_page()
        elif choice == "18":
            result = essentials_manager.open_vulkan_runtime_page()
        else:
            print_status("WARN", "Invalid choice.")
            press_enter()
            continue

        print_status("OK" if result.get("success") else "FAIL", result.get("message", "Unknown result"))
        press_enter()


def _input_int(prompt: str, default: int = 0) -> int:
    raw = get_choice(f"{prompt} [{default}]: ")
    if not raw.strip():
        return default
    try:
        return int(raw)
    except Exception:
        return default


def _input_float(prompt: str, default: float = 0.0) -> float:
    raw = get_choice(f"{prompt} [{default}]: ")
    if not raw.strip():
        return default
    try:
        return float(raw)
    except Exception:
        return default


def show_stress_testing(stress_advisor, state: dict[str, Any]) -> None:
    def _print_detected_tools() -> None:
        tools = stress_advisor.detect_tools()
        for key in ("furmark", "kombustor", "prime95", "occt", "memtest64", "mdsched"):
            path = tools.get(key, "")
            if path:
                print_status("OK", f"{key}: {path}")
            else:
                print_status("WARN", f"{key}: not found")

    def _save_cpu_result(tool_name: str) -> None:
        print_status("INFO", "After test completes, enter observed results.")
        duration = _input_int("Stress duration (minutes)", default=20)
        max_temp = _input_float("Max CPU temperature in C", default=85.0)
        crashed = confirm("Did system/app crash or freeze during test?")
        throttling = confirm("Was CPU throttling observed?")
        notes = get_choice("Notes (optional): ")
        saved = stress_advisor.record_cpu_test(
            tool=tool_name,
            duration_min=duration,
            max_temp_c=max_temp,
            crashed=crashed,
            throttling=throttling,
            notes=notes,
        )
        state["stress_cpu"] = saved
        decision = saved.get("decision")
        if decision:
            print_status(decision.get("status", "INFO"), decision.get("summary", ""))
        print_status("OK", f"Saved CPU test result: {saved.get('path')}")

    def _save_gpu_result(tool_name: str) -> None:
        print_status("INFO", "After test completes, enter observed results.")
        duration = _input_int("Stress duration (minutes)", default=20)
        max_temp = _input_float("Max GPU temperature in C", default=80.0)
        crashed = confirm("Did test crash/freeze?")
        artifacts = confirm("Did you see visual artifacts/flicker/glitches?")
        notes = get_choice("Notes (optional): ")
        saved = stress_advisor.record_gpu_test(
            tool=tool_name,
            duration_min=duration,
            max_temp_c=max_temp,
            crashed=crashed,
            artifacts=artifacts,
            notes=notes,
        )
        state["stress_gpu"] = saved
        decision = saved.get("decision")
        if decision:
            print_status(decision.get("status", "INFO"), decision.get("summary", ""))
        print_status("OK", f"Saved GPU test result: {saved.get('path')}")

    while True:
        clear_screen()
        print_header("Used Parts Stress Test & Buy Advice")
        print_status("INFO", f"Kits folder: {stress_advisor.kits_dir}")
        print_status("INFO", f"Results folder: {stress_advisor.results_dir}")
        print_menu(
            {
                "1": "Prepare/Scan Kits Folder",
                "2": "Install Missing Stress Tools (Auto)",
                "3": "Memory Test (MemTest64 Recommended)",
                "4": "CPU Stress Session + Save Result",
                "5": "GPU Stress Session + Save Result",
                "6": "Get Buy Advice From Latest Results",
                "7": "Price-to-Performance Advisor",
                "8": "View Stress Test History",
                "9": "Open Kits Folder",
                "0": "Back",
            }
        )
        choice = get_choice()
        if choice == "0":
            return

        if choice == "1":
            result = stress_advisor.prepare_kits_folder()
            state["stress_tools"] = result
            print_status("OK" if result.get("success") else "FAIL", result.get("message", "Unknown result"))
            _print_detected_tools()
            press_enter()
            continue

        if choice == "2":
            stress_advisor.prepare_kits_folder()
            if not confirm("Install all missing stress tools now?"):
                print_status("INFO", "Skipped installation.")
                press_enter()
                continue
            install = stress_advisor.install_missing_tools()
            state["stress_tool_install"] = install
            report = install.get("report", [])
            if not report:
                print_status("WARN", "No install report available.")
            for item in report:
                status = "OK" if item.get("success") else "WARN"
                print_status(status, f"{item.get('tool', 'unknown')}: {item.get('message', '')}")
            print()
            _print_detected_tools()
            press_enter()
            continue

        if choice == "3":
            clear_screen()
            print_header("Memory Test")
            print_menu(
                {
                    "1": "Launch MemTest64 (Recommended)",
                    "2": "Auto-import latest MemTest64 log",
                    "3": "Manual MemTest64 result entry",
                    "4": "Open Windows Memory Diagnostic (Fallback)",
                    "5": "Read Last Windows Memory Diagnostic Result",
                    "0": "Back",
                }
            )
            m_choice = get_choice()
            if m_choice == "0":
                continue
            if m_choice == "1":
                result = stress_advisor.launch_tool("memtest64")
                print_status("OK" if result.get("success") else "FAIL", result.get("message", "Unknown result"))
                press_enter()
                continue
            if m_choice == "2":
                notes = get_choice("Notes (optional): ")
                imported = stress_advisor.import_latest_log_as_memory_result("memtest64", notes=notes)
                if not imported.get("success"):
                    print_status("WARN", imported.get("message", "No memory log result"))
                    press_enter()
                    continue
                state["stress_memory"] = imported
                decision = imported.get("decision")
                if decision:
                    print_status(decision.get("status", "INFO"), decision.get("summary", ""))
                print_status("OK", f"Imported memory result: {imported.get('path')}")
                press_enter()
                continue
            if m_choice == "3":
                duration = _input_int("MemTest duration (minutes)", default=60)
                errors = _input_int("Detected errors count", default=0)
                crashed = confirm("Did MemTest/app/system crash or freeze?")
                notes = get_choice("Notes (optional): ")
                saved = stress_advisor.record_memtest64_test(
                    duration_min=duration,
                    errors=errors,
                    crashed=crashed,
                    notes=notes,
                )
                state["stress_memory"] = saved
                decision = saved.get("decision")
                if decision:
                    print_status(decision.get("status", "INFO"), decision.get("summary", ""))
                print_status("OK", f"Saved memory test result: {saved.get('path')}")
                press_enter()
                continue
            if m_choice == "4":
                result = stress_advisor.schedule_memory_diagnostic()
                print_status("OK" if result.get("success") else "FAIL", result.get("message", "Unknown result"))
                press_enter()
                continue
            if m_choice == "5":
                result = stress_advisor.read_last_memory_diagnostic_result()
                if not result.get("success"):
                    print_status("WARN", result.get("message", "No result"))
                    press_enter()
                    continue
                print_status(result.get("status", "INFO"), result.get("message", ""))
                notes = get_choice("Notes (optional): ")
                saved = stress_advisor.record_memory_test(
                    source="windows_memory_diagnostic",
                    status=result.get("status", "WARN"),
                    message=result.get("message", ""),
                    notes=notes,
                )
                state["stress_memory"] = saved
                print_status("OK", f"Saved memory test result: {saved.get('path')}")
                press_enter()
                continue
            print_status("WARN", "Invalid choice.")
            press_enter()
            continue

        if choice == "4":
            clear_screen()
            print_header("CPU Stress Session")
            print_menu(
                {
                    "1": "Launch Prime95 and enter manual result",
                    "2": "Launch OCCT and enter manual result",
                    "3": "Auto-import latest OCCT log",
                    "4": "Auto-import latest Prime95 log",
                    "5": "Manual (already tested externally)",
                    "0": "Back",
                }
            )
            c_choice = get_choice()
            if c_choice == "0":
                continue
            if c_choice == "1":
                launch = stress_advisor.launch_tool("prime95")
                print_status("OK" if launch.get("success") else "WARN", launch.get("message", ""))
                _save_cpu_result("prime95")
                press_enter()
                continue
            elif c_choice == "2":
                launch = stress_advisor.launch_tool("occt")
                print_status("OK" if launch.get("success") else "WARN", launch.get("message", ""))
                _save_cpu_result("occt")
                press_enter()
                continue
            elif c_choice == "3":
                notes = get_choice("Notes (optional): ")
                imported = stress_advisor.import_latest_log_as_cpu_result("occt", notes=notes)
                if not imported.get("success"):
                    print_status("WARN", imported.get("message", "Could not import CPU log."))
                    press_enter()
                    continue
                state["stress_cpu"] = imported
                decision = imported.get("decision")
                if decision:
                    print_status(decision.get("status", "INFO"), decision.get("summary", ""))
                print_status("OK", f"Imported CPU result: {imported.get('path')}")
                press_enter()
                continue
            elif c_choice == "4":
                notes = get_choice("Notes (optional): ")
                imported = stress_advisor.import_latest_log_as_cpu_result("prime95", notes=notes)
                if not imported.get("success"):
                    print_status("WARN", imported.get("message", "Could not import CPU log."))
                    press_enter()
                    continue
                state["stress_cpu"] = imported
                decision = imported.get("decision")
                if decision:
                    print_status(decision.get("status", "INFO"), decision.get("summary", ""))
                print_status("OK", f"Imported CPU result: {imported.get('path')}")
                press_enter()
                continue
            elif c_choice == "5":
                _save_cpu_result("manual")
                press_enter()
                continue
            else:
                print_status("WARN", "Invalid choice.")
                press_enter()
                continue

        if choice == "5":
            clear_screen()
            print_header("GPU Stress Session")
            print_menu(
                {
                    "1": "Launch FurMark and enter manual result",
                    "2": "Launch MSI Kombustor and enter manual result",
                    "3": "Auto-import latest FurMark log",
                    "4": "Auto-import latest MSI Kombustor log",
                    "5": "Manual (already tested externally)",
                    "0": "Back",
                }
            )
            g_choice = get_choice()
            if g_choice == "0":
                continue
            if g_choice == "1":
                launch = stress_advisor.launch_tool("furmark")
                print_status("OK" if launch.get("success") else "WARN", launch.get("message", ""))
                _save_gpu_result("furmark")
                press_enter()
                continue
            elif g_choice == "2":
                launch = stress_advisor.launch_tool("kombustor")
                print_status("OK" if launch.get("success") else "WARN", launch.get("message", ""))
                _save_gpu_result("kombustor")
                press_enter()
                continue
            elif g_choice == "3":
                notes = get_choice("Notes (optional): ")
                imported = stress_advisor.import_latest_log_as_gpu_result("furmark", notes=notes)
                if not imported.get("success"):
                    print_status("WARN", imported.get("message", "Could not import GPU log."))
                    press_enter()
                    continue
                state["stress_gpu"] = imported
                decision = imported.get("decision")
                if decision:
                    print_status(decision.get("status", "INFO"), decision.get("summary", ""))
                print_status("OK", f"Imported GPU result: {imported.get('path')}")
                press_enter()
                continue
            elif g_choice == "4":
                notes = get_choice("Notes (optional): ")
                imported = stress_advisor.import_latest_log_as_gpu_result("kombustor", notes=notes)
                if not imported.get("success"):
                    print_status("WARN", imported.get("message", "Could not import GPU log."))
                    press_enter()
                    continue
                state["stress_gpu"] = imported
                decision = imported.get("decision")
                if decision:
                    print_status(decision.get("status", "INFO"), decision.get("summary", ""))
                print_status("OK", f"Imported GPU result: {imported.get('path')}")
                press_enter()
                continue
            elif g_choice == "5":
                _save_gpu_result("manual")
                press_enter()
                continue
            else:
                print_status("WARN", "Invalid choice.")
                press_enter()
                continue

        if choice == "6":
            advice = stress_advisor.get_buy_advice()
            state["stress_buy_advice"] = advice
            clear_screen()
            print_header("Buy Advice")
            print_status("INFO", f"Recommendation: {advice.get('recommendation')}")
            print_status("INFO", f"Confidence: {advice.get('confidence')}")
            print()
            print_status("INFO", "Reasons:")
            for reason in advice.get("reasons", []):
                print(f"  - {reason}")
            print()
            print_status("WARN", "Advice is guidance only, not a guarantee.")
            press_enter()
            continue

        if choice == "7":
            clear_screen()
            print_header("Price-to-Performance Advisor")
            asking_price = _input_float("Asking price", default=0.0)
            if asking_price <= 0:
                print_status("WARN", "Please enter a valid asking price above 0.")
                press_enter()
                continue
            currency = get_choice("Currency code [USD]: ").strip().upper() or "USD"
            advice = stress_advisor.get_price_to_performance_advice(
                asking_price=asking_price,
                currency=currency,
            )
            state["stress_value_advice"] = advice
            print_status("INFO", f"Decision: {advice.get('decision')}")
            print_status("INFO", f"Value score: {advice.get('value_score')} / 100")
            print_status(
                "INFO",
                f"Estimated fair price: {advice.get('estimated_fair_price')} {advice.get('currency')}",
            )
            print_status("INFO", f"Performance score: {advice.get('performance_score')}")
            print_status("INFO", advice.get("note", ""))
            base = advice.get("base_buy_advice", {})
            print_status(
                "INFO",
                f"Base stress recommendation: {base.get('recommendation', 'BUY WITH CAUTION')}",
            )
            press_enter()
            continue

        if choice == "8":
            rows = stress_advisor.list_results()
            if not rows:
                print_status("INFO", "No stress test results saved yet.")
                press_enter()
                continue
            for idx, row in enumerate(rows[:40], start=1):
                print(
                    f"  [{idx}] {row.get('timestamp')} | {row.get('type')} | "
                    f"{row.get('decision')} | {row.get('summary')}"
                )
            press_enter()
            continue

        if choice == "9":
            result = run_command(f'start "" "{stress_advisor.kits_dir}"', timeout=10)
            print_status(
                "OK" if result.get("success") else "FAIL",
                "Opened kits folder." if result.get("success") else result.get("stderr", "Failed to open folder."),
            )
            press_enter()
            continue

        print_status("WARN", "Invalid choice.")
        press_enter()


def _snapshot_required(settings_manager) -> bool:
    mode = str(settings_manager.load().get("create_snapshots_before_repairs", "Always"))
    if mode == "Never":
        return False
    if mode == "Ask":
        return confirm("Create safety snapshot first?")
    return True


def _create_snapshot_or_cancel(snapshots, description: str) -> bool:
    snapshot_path = snapshots.create_snapshot(action_name=description, include_restore_point=True)
    if not snapshot_path:
        print_status("FAIL", "Could not create safety snapshot. Action cancelled.")
        return False
    print_status("OK", f"Snapshot created: {snapshot_path}")
    return True


def main() -> int:
    if not ensure_dependencies():
        press_enter()
        return 1

    from modules.app_checker import AppChecker
    from modules.auto_fix import AutoFixWizard
    from modules.diagnosis import DiagnosisEngine
    from modules.drivers import DriverChecker
    from modules.essentials_installer import GamingEssentialsManager
    from modules.full_scan import FullScan
    from modules.game_detector import GameDetector
    from modules.health_check import HealthChecker
    from modules.network import NetworkDoctor
    from modules.power import PowerOptimizer
    from modules.process_manager import ProcessManager
    from modules.repairs import RepairCenter
    from modules.reports import ReportGenerator
    from modules.services import ServiceOptimizer
    from modules.settings import SettingsManager
    from modules.settings_recommender import SettingsRecommender
    from modules.snapshots import SnapshotManager
    from modules.system_info import SystemInfo
    from modules.stress_testing import StressTestAdvisor

    config.ensure_runtime_dirs()
    initialize_data_files(config.DATA_DIR)

    ensure_admin()

    state: dict[str, Any] = {}
    system_info = SystemInfo()
    process_manager = ProcessManager()
    repairs = RepairCenter(system_info)
    services = ServiceOptimizer()
    snapshots = SnapshotManager(config.SNAPSHOTS_DIR)
    network_doctor = NetworkDoctor()
    driver_checker = DriverChecker()
    game_detector = GameDetector(config.DATA_DIR)
    settings_recommender = SettingsRecommender(system_info, config.DATA_DIR)
    power_optimizer = PowerOptimizer()
    settings_manager = SettingsManager(config.APP_DIR / "settings.json")
    reporter = ReportGenerator(config.REPORTS_DIR)
    essentials_manager = GamingEssentialsManager(system_info=system_info, driver_checker=driver_checker)
    stress_advisor = StressTestAdvisor(app_dir=config.APP_DIR, system_info=system_info)
    full_scan = FullScan(
        system_info=system_info,
        process_manager=process_manager,
        services=services,
        network_doctor=network_doctor,
        driver_checker=driver_checker,
        game_detector=game_detector,
    )
    diagnosis_engine = DiagnosisEngine(
        system_info=system_info,
        process_manager=process_manager,
        network_doctor=network_doctor,
        driver_checker=driver_checker,
    )
    app_checker = AppChecker(config.DATA_DIR)

    if bool(settings_manager.load().get("startup_essentials_check", True)):
        startup_essentials = essentials_manager.quick_startup_check()
        state["essentials_startup"] = startup_essentials
        if startup_essentials.get("needs_action_count", 0) > 0:
            clear_screen()
            print_header("Startup Essentials Check")
            print_status(
                "WARN",
                f"{startup_essentials['needs_action_count']} important prerequisite(s) may need attention.",
            )
            for row in startup_essentials.get("needs_action", [])[:6]:
                print_status(row.get("status", "WARN"), f"{row.get('name')}: {row.get('message')}")
            print()
            if confirm("Open Gaming Essentials Installer now?"):
                show_essentials_installer(essentials_manager, state)

    while True:
        clear_screen()
        print_main_banner(config.APP_NAME, config.APP_VERSION)
        print_developer_card(
            name=config.APP_AUTHOR,
            github=config.APP_GITHUB,
            linkedin=config.APP_LINKEDIN,
            email=config.APP_EMAIL,
        )
        print_header("MAIN MENU")
        print_menu(
            {
                "1": "Quick Health Check",
                "2": "Full System Scan",
                "3": "Auto-Fix Wizard",
                "4": "Find My Games",
                "5": "Diagnose Problems",
                "6": "Repair Center",
                "7": "Service Optimizer",
                "8": "Process Killer",
                "9": "App Scanner",
                "10": "Settings Advisor",
                "11": "Network Doctor",
                "12": "Driver Check",
                "13": "Power Optimizer",
                "14": "Snapshots & Rollback",
                "15": "Reports",
                "16": "Settings",
                "17": "Gaming Essentials Installer",
                "18": "Used Parts Stress Test & Buy Advice",
                "0": "Exit",
            }
        )
        choice = get_choice()
        if choice == "0":
            return 0
        if choice == "1":
            show_quick_health_check(system_info, HealthChecker, state)
        elif choice == "2":
            show_full_scan(full_scan, state)
        elif choice == "3":
            AutoFixWizard(repairs=repairs, snapshots=snapshots, process_manager=process_manager).run()
        elif choice == "4":
            show_find_games(game_detector, state)
        elif choice == "5":
            show_diagnosis(diagnosis_engine, state)
        elif choice == "6":
            show_repair_center(repairs, snapshots, settings_manager)
        elif choice == "7":
            show_services(services, snapshots, settings_manager)
        elif choice == "8":
            show_processes(process_manager)
        elif choice == "9":
            show_app_scanner(app_checker, state)
        elif choice == "10":
            show_settings_advisor(settings_recommender, state)
        elif choice == "11":
            show_network_doctor(network_doctor, snapshots, settings_manager, state)
        elif choice == "12":
            show_driver_check(driver_checker, state)
        elif choice == "13":
            show_power_optimizer(power_optimizer, system_info, state)
        elif choice == "14":
            show_snapshots(snapshots)
        elif choice == "15":
            show_reports(reporter, state)
        elif choice == "16":
            show_settings(settings_manager)
        elif choice == "17":
            show_essentials_installer(essentials_manager, state)
        elif choice == "18":
            show_stress_testing(stress_advisor, state)
        else:
            print_status("WARN", "Invalid menu choice.")
            press_enter()


if __name__ == "__main__":
    sys.exit(main())
