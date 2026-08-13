"""
Sound resources
"""

from __future__ import annotations

import arcade


_place_sound: arcade.Sound | None = None
_win_sound: arcade.Sound | None = None


def _get_place() -> arcade.Sound:
    global _place_sound
    if _place_sound is None:
        _place_sound = arcade.load_sound(":resources:sounds/coin1.wav")
    return _place_sound


def _get_win() -> arcade.Sound:
    global _win_sound
    if _win_sound is None:
        _win_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
    return _win_sound


def play_place() -> None:
    """Play the marker-placement sound effect (FR-34)."""
    try:
        _get_place().play()
    except Exception:
        pass


def play_win() -> None:
    """Play the round-won sound effect (FR-35)."""
    try:
        _get_win().play()
    except Exception:
        pass