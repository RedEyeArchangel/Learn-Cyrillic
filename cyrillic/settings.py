# SPDX-License-Identifier: CC-BY-NC-SA-4.0
# Copyright (c) 2026 RedEyeArchangel
"""User settings (language, voice), kept apart from the progress so export/import doesn't touch them."""
import json
from pathlib import Path


SETTINGS_FILE = Path.home() / ".local/share/learn-cyrillic/settings.json"
try:
    SETTINGS = json.loads(SETTINGS_FILE.read_text())
    if not isinstance(SETTINGS, dict):
        raise ValueError
except (OSError, ValueError):
    SETTINGS = {}


def save_settings():
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(json.dumps(SETTINGS))
