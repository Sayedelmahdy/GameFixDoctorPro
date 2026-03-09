"""Report generation placeholder."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.utils import now_stamp, save_json


class ReportGenerator:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_json_report(self, name: str, payload: dict) -> Path:
        path = self.output_dir / f"{now_stamp()}_{name}.json"
        save_json(path, payload)
        return path

    def save_txt_report(self, name: str, title: str, sections: list[tuple[str, list[str]]]) -> Path:
        path = self.output_dir / f"{now_stamp()}_{name}.txt"
        lines = [title, "=" * len(title), ""]
        for header, rows in sections:
            lines.append(header)
            lines.append("-" * len(header))
            lines.extend(rows if rows else ["(no data)"])
            lines.append("")
        path.write_text("\n".join(lines), encoding="utf-8")
        return path

    def save_html_report(self, name: str, title: str, data: dict[str, Any]) -> Path:
        path = self.output_dir / f"{now_stamp()}_{name}.html"
        rows = []
        for key, value in data.items():
            rows.append(f"<tr><th>{key}</th><td><pre>{value}</pre></td></tr>")
        html = (
            "<!doctype html><html><head><meta charset='utf-8'>"
            f"<title>{title}</title>"
            "<style>body{font-family:Segoe UI,Arial,sans-serif;padding:24px;background:#f7f7f7;}"
            "table{border-collapse:collapse;width:100%;background:#fff;}th,td{border:1px solid #ddd;padding:8px;}"
            "th{width:240px;background:#f0f0f0;text-align:left;}pre{margin:0;white-space:pre-wrap;}</style>"
            "</head><body>"
            f"<h1>{title}</h1><table>{''.join(rows)}</table></body></html>"
        )
        path.write_text(html, encoding="utf-8")
        return path
