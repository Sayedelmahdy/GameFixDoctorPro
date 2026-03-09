"""Auto-Fix Wizard implementation."""

from __future__ import annotations

from core.ui import clear_screen, confirm, press_enter, print_header, print_status


class AutoFixWizard:
    """Runs safe automated checks and fixes with user approval."""

    def __init__(self, repairs, snapshots, process_manager) -> None:
        self.repairs = repairs
        self.snapshots = snapshots
        self.process_manager = process_manager
        self.applied: list[str] = []
        self.failed: list[str] = []
        self.skipped: list[str] = []
        self.snapshot_path: str | None = None

    def run(self) -> None:
        clear_screen()
        print_header("Auto-Fix Wizard")
        print("  This wizard scans your PC and applies safe gaming optimizations.")
        print("  You will be asked Yes/No before every fix step.\n")
        if not confirm("Start Auto-Fix Wizard?"):
            return

        if not self._step_create_backup():
            press_enter()
            return

        fixes = self._build_safe_plan() + self._build_recommended_plan()

        clear_screen()
        print_header("Fix Plan")
        for idx, fix in enumerate(fixes, start=1):
            print(f"  [{idx}] {fix['name']} ({fix['category']}, risk: {fix['risk']})")
        if not fixes:
            print_status("OK", "No fixes needed right now.")
            press_enter()
            return
        print()

        if not confirm("Start interactive fix steps now?"):
            return

        self._apply_interactive(fixes)
        self._summary()
        press_enter()

    def _step_create_backup(self) -> bool:
        clear_screen()
        print_header("Step 1/3 - Create Safety Backup")
        print("  Before making changes, a rollback snapshot will be created.")
        if not confirm("Create backup and continue?"):
            print_status("WARN", "Wizard cancelled by user before changes.")
            return False
        self.snapshot_path = self.snapshots.create_snapshot("AutoFix Wizard", include_restore_point=True)
        if not self.snapshot_path:
            print_status("FAIL", "Could not create snapshot. Wizard cancelled for safety.")
            return False
        print_status("OK", f"Snapshot created: {self.snapshot_path}")
        return True

    def _build_safe_plan(self) -> list[dict]:
        return [
            {
                "name": "Clear temp files",
                "category": "safe",
                "risk": "none",
                "reversible": "n/a",
                "description": "Remove temporary cached files to free disk space.",
                "func": self.repairs.clear_temp_files,
            },
            {
                "name": "Enable Game Mode",
                "category": "safe",
                "risk": "none",
                "reversible": "yes",
                "description": "Enable Windows Game Mode for gaming performance behavior.",
                "func": self.repairs.enable_game_mode,
            },
            {
                "name": "Set High Performance power plan",
                "category": "safe",
                "risk": "none",
                "reversible": "yes",
                "description": "Switch Windows power profile to High Performance.",
                "func": self.repairs.set_high_performance_power,
            },
            {
                "name": "Flush DNS cache",
                "category": "safe",
                "risk": "none",
                "reversible": "auto",
                "description": "Clear DNS cache to remove stale network records.",
                "func": self.repairs.flush_dns,
            },
        ]

    def _build_recommended_plan(self) -> list[dict]:
        heavy = self.process_manager.get_closable_processes(min_ram_mb=600, top_n=3)
        if not heavy:
            return []

        def close_heavy() -> dict:
            all_ok = True
            for proc in heavy:
                ok, _ = self.process_manager.close_process(proc["pid"])
                if not ok:
                    all_ok = False
            return {
                "success": all_ok,
                "message": f"Attempted to close {len(heavy)} heavy processes.",
            }

        top = ", ".join(f"{proc['name']} ({proc['memory_mb']:.0f} MB)" for proc in heavy[:3])
        return [
            {
                "name": f"Close {len(heavy)} heavy background processes",
                "category": "recommended",
                "risk": "low",
                "reversible": "yes (reopen apps)",
                "description": f"Close top heavy processes: {top}",
                "func": close_heavy,
            }
        ]

    def _apply_interactive(self, fixes: list[dict]) -> None:
        clear_screen()
        print_header("Step 2/3 - Interactive Fix Steps")
        for idx, fix in enumerate(fixes, start=1):
            clear_screen()
            print_header(f"Step 2/3 - Fix {idx}/{len(fixes)}")
            print(f"  Fix: {fix['name']}")
            print(f"  Category: {fix['category']}")
            print(f"  Risk: {fix['risk'].upper()}")
            print(f"  Reversible: {fix['reversible']}")
            print()
            print("  What this does:")
            print(f"  - {fix['description']}")
            print()

            if not confirm("Apply this fix?"):
                self.skipped.append(fix["name"])
                print_status("INFO", "Skipped by user.")
                press_enter()
                continue

            print_status("INFO", f"Applying: {fix['name']}")
            try:
                result = fix["func"]()
                if result.get("success"):
                    self.applied.append(fix["name"])
                    print_status("OK", result.get("message", "Completed"))
                else:
                    self.failed.append(f"{fix['name']}: {result.get('message', 'Failed')}")
                    print_status("WARN", result.get("message", "Failed"))
            except Exception as exc:
                self.failed.append(f"{fix['name']}: {exc}")
                print_status("FAIL", f"{fix['name']}: {exc}")
            press_enter()

    def _summary(self) -> None:
        clear_screen()
        print_header("Step 3/3 - Summary")
        print_status("OK", f"Applied fixes: {len(self.applied)}")
        for item in self.applied:
            print(f"  [OK] {item}")
        if self.skipped:
            print()
            print_status("INFO", f"Skipped by user: {len(self.skipped)}")
            for item in self.skipped:
                print(f"  [SKIP] {item}")
        if self.failed:
            print()
            print_status("WARN", f"Failed/partial fixes: {len(self.failed)}")
            for item in self.failed:
                print(f"  [WARN] {item}")
        print()
        if self.snapshot_path:
            print_status("INFO", f"Rollback snapshot: {self.snapshot_path}")
