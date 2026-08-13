"""
Central configuration: window, grid, colors, timer durations, and key maps.
"""

from __future__ import annotations

import arcade

SCREEN_WIDTH: int = 700
SCREEN_HEIGHT: int = 700
SCREEN_TITLE: str = "Tic-Tac-Toe Arcade"
SCREEN_BG_COLOR = arcade.color.WHITE

GRID_SIZE: int = 3
CELL_SIZE: int = 180
LINE_WIDTH: int = 6
GRID_MARGIN: int = 110
GRID_ORIGIN_X: int = (SCREEN_WIDTH - GRID_SIZE * CELL_SIZE) // 2
GRID_ORIGIN_Y: int = GRID_MARGIN

COLOR_X = arcade.color.BLUE
COLOR_O = arcade.color.RED
COLOR_GRID = arcade.color.DARK_GRAY
COLOR_WIN_LINE = arcade.color.GREEN
COLOR_TEXT = arcade.color.BLACK
COLOR_TEXT_MUTED = arcade.color.GRAY
COLOR_BANNER_BG = arcade.color.BLACK
COLOR_BANNER_TEXT = arcade.color.WHITE
COLOR_TIMER_TRACK = arcade.color.BLACK
COLOR_TIMER_FILL = arcade.color.AZURE

TIMER_EASY: float = 10.0
TIMER_MEDIUM: float = 5.0
TIMER_HARD: float = 3.0

DIFFICULTY_TIMES: dict[str, float] = {
    "easy": TIMER_EASY,
    "medium": TIMER_MEDIUM,
    "hard": TIMER_HARD,
}

DIFFICULTY_LABELS: dict[str, str] = {
    "easy": "Easy",
    "medium": "Medium",
    "hard": "Hard",
}

PLAYER_X: str = "X"
PLAYER_O: str = "O"
FIRST_PLAYER: str = PLAYER_X

KEYS_PLAYER_1: dict[int, tuple[int, int]] = {
    arcade.key.Q: (0, 0), arcade.key.W: (0, 1), arcade.key.E: (0, 2),
    arcade.key.A: (1, 0), arcade.key.S: (1, 1), arcade.key.D: (1, 2),
    arcade.key.Z: (2, 0), arcade.key.X: (2, 1), arcade.key.C: (2, 2),
}

KEYS_PLAYER_2: dict[int, tuple[int, int]] = {
    arcade.key.U: (0, 0), arcade.key.I: (0, 1), arcade.key.O: (0, 2),
    arcade.key.J: (1, 0), arcade.key.K: (1, 1), arcade.key.L: (1, 2),
    arcade.key.M: (2, 0), arcade.key.COMMA: (2, 1), arcade.key.PERIOD: (2, 2),
}

KEYS_DIFFICULTY: dict[int, str] = {
    arcade.key.KEY_1: "easy",
    arcade.key.KEY_2: "medium",
    arcade.key.KEY_3: "hard",
}

KEY_RESTART: int = arcade.key.R
KEY_MENU: int = arcade.key.ESCAPE
KEY_START: int = arcade.key.SPACE

HUD_HEIGHT: int = 90
BANNER_WIDTH: int = 460
BANNER_HEIGHT: int = 130