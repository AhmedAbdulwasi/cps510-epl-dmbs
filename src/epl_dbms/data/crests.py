"""Club crest and player headshot URL helpers."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

# Compact PNG crests (API-Sports media CDN). Fit in VARCHAR2(400).
CLUB_CREST_URLS: dict[str, str] = {
    "AR": "https://media.api-sports.io/football/teams/42.png",
    "BH": "https://media.api-sports.io/football/teams/51.png",
    "MC": "https://media.api-sports.io/football/teams/50.png",
    "LV": "https://media.api-sports.io/football/teams/40.png",
    "BO": "https://media.api-sports.io/football/teams/35.png",
    "BR": "https://media.api-sports.io/football/teams/55.png",
    "LE": "https://media.api-sports.io/football/teams/63.png",
    "CH": "https://media.api-sports.io/football/teams/49.png",
    "EV": "https://media.api-sports.io/football/teams/45.png",
    "TH": "https://media.api-sports.io/football/teams/47.png",
    "HU": "https://media.api-sports.io/football/teams/71.png",
    "AV": "https://media.api-sports.io/football/teams/66.png",
    "NE": "https://media.api-sports.io/football/teams/34.png",
    "CO": "https://media.api-sports.io/football/teams/73.png",
    "FU": "https://media.api-sports.io/football/teams/36.png",
    "IP": "https://media.api-sports.io/football/teams/57.png",
    "NF": "https://media.api-sports.io/football/teams/65.png",
    "SU": "https://media.api-sports.io/football/teams/746.png",
    "MU": "https://media.api-sports.io/football/teams/33.png",
    "CP": "https://media.api-sports.io/football/teams/52.png",
}


@lru_cache(maxsize=1)
def _player_photo_map() -> dict[str, str]:
    """Load pre-resolved TheSportsDB / Wikimedia headshot URLs."""
    path = Path(__file__).with_name("player_photos.json")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return {}


def player_photo_url(player_id: str, player_name: str) -> str:
    """
    Real player cutout/headshot when available; otherwise a generated avatar.

    Preferred sources are baked into player_photos.json (TheSportsDB cutouts /
    Wikipedia thumbs) so the app does not need live API keys at runtime.
    """
    mapped = _player_photo_map().get(player_id)
    if mapped:
        return mapped
    seed = quote(player_name.replace(" ", ""), safe="")
    return f"https://api.dicebear.com/9.x/adventurer/png?seed={seed}&size=128"
