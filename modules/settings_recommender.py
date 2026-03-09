"""Hardware-based settings recommendations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.utils import load_json


class SettingsRecommender:
    """Classify hardware and suggest profile settings."""

    def __init__(self, system_info, data_dir: Path) -> None:
        self.system_info = system_info
        self.hardware_db = load_json(data_dir / "hardware_database.json", default={})
        self.settings_profiles = load_json(data_dir / "settings_profiles.json", default={})

    def recommend(self) -> dict[str, Any]:
        system = self.system_info.get_full_system_info()
        cpu_name = str(system.get("cpu", {}).get("name", "Unknown"))
        ram_gb = float(system.get("ram", {}).get("total_gb", 0.0))

        primary_gpu = system.get("gpu", [{}])[0] if system.get("gpu") else {}
        gpu_name = str(primary_gpu.get("name", "Unknown"))
        gpu_vram = float(primary_gpu.get("vram_total_mb", 0.0) or 0.0) / 1024.0

        cpu_tier = self._classify_cpu(cpu_name)
        gpu_tier = self._classify_gpu(gpu_name, gpu_vram)
        ram_tier = self._classify_ram(ram_gb)

        recommended_profile = self._pick_profile(cpu_tier, gpu_tier, ram_tier)
        profiles = self.settings_profiles.get("profiles", {})
        profile_payload = profiles.get(recommended_profile, {})

        return {
            "status": "ok",
            "hardware": {
                "cpu": cpu_name,
                "cpu_tier": cpu_tier,
                "gpu": gpu_name,
                "gpu_tier": gpu_tier,
                "gpu_vram_gb": round(gpu_vram, 1),
                "ram_gb": ram_gb,
                "ram_tier": ram_tier,
            },
            "recommended_profile": recommended_profile,
            "profile_settings": profile_payload,
        }

    def _classify_cpu(self, cpu_name: str) -> str:
        tiers = self.hardware_db.get("cpu_tiers", {})
        name = cpu_name.lower()
        for tier_name, tier_data in tiers.items():
            keywords = tier_data.get("keywords", []) if isinstance(tier_data, dict) else []
            if any(str(keyword).lower() in name for keyword in keywords):
                return str(tier_name)
        # Heuristic fallback.
        if "i9" in name or "ryzen 9" in name:
            return "ultra"
        if "i7" in name or "ryzen 7" in name:
            return "high"
        if "i5" in name or "ryzen 5" in name:
            return "medium"
        if "i3" in name or "ryzen 3" in name:
            return "low"
        return "very_low"

    def _classify_gpu(self, gpu_name: str, vram_gb: float) -> str:
        tiers = self.hardware_db.get("gpu_tiers", {})
        name = gpu_name.lower()
        for tier_name, tier_data in tiers.items():
            if not isinstance(tier_data, dict):
                continue
            keywords = tier_data.get("keywords", [])
            min_vram = float(tier_data.get("min_vram_gb", 0))
            if any(str(keyword).lower() in name for keyword in keywords):
                if vram_gb >= min_vram or min_vram == 0:
                    return str(tier_name)

        if "4090" in name or "4080" in name or vram_gb >= 16:
            return "ultra"
        if "4070" in name or "7900" in name or vram_gb >= 10:
            return "high"
        if "4060" in name or "3060" in name or "6700" in name or vram_gb >= 8:
            return "medium_high"
        if "2060" in name or "1070" in name or vram_gb >= 6:
            return "medium"
        if "1060" in name or "1650" in name or vram_gb >= 4:
            return "low"
        return "very_low"

    @staticmethod
    def _classify_ram(ram_gb: float) -> str:
        if ram_gb >= 32:
            return "high"
        if ram_gb >= 16:
            return "standard"
        if ram_gb >= 8:
            return "limited"
        return "insufficient"

    @staticmethod
    def _pick_profile(cpu_tier: str, gpu_tier: str, ram_tier: str) -> str:
        weak_cpu = cpu_tier in {"low", "very_low"}
        weak_gpu = gpu_tier in {"low", "very_low"}
        low_ram = ram_tier in {"limited", "insufficient"}

        if weak_cpu or weak_gpu or low_ram:
            return "low_end_survival"
        if gpu_tier in {"ultra", "high"} and cpu_tier in {"ultra", "high"} and ram_tier in {"high", "standard"}:
            return "visual_quality"
        return "balanced"
