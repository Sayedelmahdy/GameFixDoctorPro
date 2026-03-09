"""UI helpers for console output."""

from __future__ import annotations

import os
import sys
from typing import Iterable

try:
    from colorama import Fore, Style, init as colorama_init

    colorama_init(autoreset=True)
except Exception:  # pragma: no cover - fallback for missing colorama
    class _NoColor:
        BLACK = ""
        RED = ""
        GREEN = ""
        YELLOW = ""
        BLUE = ""
        MAGENTA = ""
        CYAN = ""
        WHITE = ""
        RESET_ALL = ""

    Fore = _NoColor()
    Style = _NoColor()


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_header(title: str) -> None:
    width = 88
    glyphs = _box_glyphs()
    border = glyphs["tl"] + glyphs["h"] * (width - 2) + glyphs["tr"]
    mid = glyphs["ml"] + glyphs["h"] * (width - 2) + glyphs["mr"]
    print(Fore.CYAN + border)
    print(Fore.CYAN + glyphs["v"] + title.center(width - 2) + glyphs["v"])
    print(Fore.CYAN + mid)
    print(Style.RESET_ALL, end="")


def print_box(lines: Iterable[str], title: str | None = None, width: int = 88, color=Fore.CYAN) -> None:
    glyphs = _box_glyphs()
    top = glyphs["tl"] + glyphs["h"] * (width - 2) + glyphs["tr"]
    sep = glyphs["ml"] + glyphs["h"] * (width - 2) + glyphs["mr"]
    bottom = glyphs["bl"] + glyphs["h"] * (width - 2) + glyphs["br"]
    print(color + top)
    if title:
        print(color + glyphs["v"] + title.center(width - 2) + glyphs["v"])
        print(color + sep)
    for line in lines:
        clipped = line[: width - 4]
        print(color + glyphs["v"] + Style.RESET_ALL + " " + clipped.ljust(width - 4) + color + " " + glyphs["v"])
    print(color + bottom + Style.RESET_ALL)


def print_main_banner(app_name: str, version: str) -> None:
    lines = [
        "   ____                         ______ _            _             ",
        "  / ___| __ _ _ __ ___   ___  |  ____| | ___   ___| | _____ _ __ ",
        " | |  _ / _` | '_ ` _ \\ / _ \\ |  _|  | |/ _ \\ / __| |/ / _ \\ '__|",
        " | |_| | (_| | | | | | |  __/ | |___ | | (_) | (__|   <  __/ |   ",
        "  \\____|\\__,_|_| |_| |_|\\___| |_____|_|\\___/ \\___|_|\\_\\___|_|   ",
        "",
        f" {app_name} v{version}  |  Your PC's Gaming Health Expert",
    ]
    print_box(lines, title="GAMEFIX DOCTOR PRO", width=88, color=Fore.CYAN)


def print_developer_card(name: str, github: str, linkedin: str, email: str) -> None:
    lines = [
        f"Developed by: {name}",
        f"GitHub:   {github}",
        f"LinkedIn: {linkedin}",
        f"Gmail:    {email}",
    ]
    print_box(lines, title="DEVELOPER", width=88, color=Fore.BLUE)


def print_status(status: str, message: str) -> None:
    status = status.upper()
    if status == "OK":
        color = Fore.GREEN
    elif status == "WARN":
        color = Fore.YELLOW
    elif status == "FAIL":
        color = Fore.RED
    elif status == "INFO":
        color = Fore.BLUE
    else:
        color = Fore.CYAN
    print(f"  {color}[{status}] {Style.RESET_ALL}{message}")


def print_menu(options: dict[str, str]) -> None:
    print()
    for key, value in options.items():
        color = Fore.RED if key == "0" else Fore.CYAN
        print(f"  {color}[{key:>2}] {Style.RESET_ALL}{value}")
    print()


def get_choice(prompt: str = "Your choice: ") -> str:
    return input(f"  {prompt}").strip()


def confirm(message: str) -> bool:
    value = input(f"  {message} (y/n): ").strip().lower()
    return value in {"y", "yes"}


def press_enter() -> None:
    input("\n  Press Enter to continue...")


def _box_glyphs() -> dict[str, str]:
    if _supports_unicode():
        return {
            "tl": "╔",
            "tr": "╗",
            "bl": "╚",
            "br": "╝",
            "h": "═",
            "v": "║",
            "ml": "╠",
            "mr": "╣",
        }
    return {
        "tl": "+",
        "tr": "+",
        "bl": "+",
        "br": "+",
        "h": "-",
        "v": "|",
        "ml": "+",
        "mr": "+",
    }


def _supports_unicode() -> bool:
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    try:
        "╔".encode(encoding)
        return True
    except Exception:
        return False
