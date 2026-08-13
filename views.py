"""Arcade View subclasses: the main menu and the in-game screen."""

from __future__ import annotations

import arcade

import sounds
from constants import (
    BANNER_HEIGHT,
    BANNER_WIDTH,
    CELL_SIZE,
    COLOR_BANNER_BG,
    COLOR_BANNER_TEXT,
    COLOR_GRID,
    COLOR_O,
    COLOR_TEXT,
    COLOR_TEXT_MUTED,
    COLOR_TIMER_FILL,
    COLOR_TIMER_TRACK,
    COLOR_WIN_LINE,
    COLOR_X,
    DIFFICULTY_LABELS,
    DIFFICULTY_TIMES,
    GRID_MARGIN,
    GRID_ORIGIN_X,
    GRID_ORIGIN_Y,
    GRID_SIZE,
    HUD_HEIGHT,
    KEYS_DIFFICULTY,
    KEYS_PLAYER_1,
    KEYS_PLAYER_2,
    KEY_MENU,
    KEY_RESTART,
    KEY_START,
    LINE_WIDTH,
    PLAYER_O,
    PLAYER_X,
    SCREEN_BG_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from game import GameState

# ---------------------------------------------------------------------------
# MenuView
# ---------------------------------------------------------------------------

class MenuView(arcade.View):
    """Start menu with a difficulty preview and a 'press SPACE' prompt."""

    def __init__(self) -> None:
        super().__init__()
        self.selected_difficulty: str = "easy"

    def on_show_view(self) -> None:
        self.window.background_color = SCREEN_BG_COLOR

    def on_draw(self) -> None:
        self.clear()
        cx = SCREEN_WIDTH / 2

        arcade.draw_text(
            "TIC-TAC-TOE ARCADE",
            cx, SCREEN_HEIGHT - 120,
            COLOR_TEXT, 44, anchor_x="center", bold=True,
        )
        arcade.draw_text(
            "Two players, one keyboard (or two mice).",
            cx, SCREEN_HEIGHT - 170,
            COLOR_TEXT_MUTED, 16, anchor_x="center",
        )

        arcade.draw_text(
            "Select difficulty",
            cx, SCREEN_HEIGHT - 240,
            COLOR_TEXT, 22, anchor_x="center",
        )
        y = SCREEN_HEIGHT - 290
        for i, (key, name) in enumerate(DIFFICULTY_LABELS.items()):
            label = f"[{i + 1}] {name}  ({DIFFICULTY_TIMES[key]:.0f}s per turn)"
            color = COLOR_X if key == self.selected_difficulty else COLOR_TEXT_MUTED
            arcade.draw_text(label, cx, y - i * 32, color, 18, anchor_x="center")

        arcade.draw_text(
            "Press SPACE to start",
            cx, 110,
            COLOR_TEXT, 22, anchor_x="center", bold=True,
        )
        arcade.draw_text(
            "ESC: back to menu  |  R: restart board  |  1/2/3: change difficulty",
            cx, 70,
            COLOR_TEXT_MUTED, 13, anchor_x="center",
        )

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key in KEYS_DIFFICULTY:
            self.selected_difficulty = KEYS_DIFFICULTY[key]
            return
        if key == KEY_START:
            game = GameView(self.selected_difficulty)
            game.setup()
            self.window.show_view(game)


# ---------------------------------------------------------------------------
# GameView
# ---------------------------------------------------------------------------


class GameView(arcade.View):
    """The main play screen — grid, HUD, and game-over overlay."""

    def __init__(self, difficulty: str = "easy") -> None:
        super().__init__()
        self.state = GameState()
        self.state.difficulty = difficulty
        self._last_winner_played = False

    def setup(self) -> None:
        self.state.start_round()
        self._last_winner_played = False

    # Drawing functions 

    def on_show_view(self) -> None:
        self.window.background_color = SCREEN_BG_COLOR

    def on_draw(self) -> None:
        self.clear()
        self._draw_hud()
        draw_grid()
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell = self.state.board.cells[r][c]
                if cell:
                    draw_marker(r, c, cell)

        if self.state.winning_cells is not None:
            draw_winning_line(self.state.winning_cells)

        if self.state.round_over:
            self._draw_game_over_banner()

    def _draw_hud(self) -> None:
        cx = SCREEN_WIDTH / 2

        arcade.draw_text(
            f"X: {self.state.score_x}",
            20, SCREEN_HEIGHT - 40,
            COLOR_X, 22, anchor_y="center", bold=True,
        )
        arcade.draw_text(
            f"O: {self.state.score_o}",
            110, SCREEN_HEIGHT - 40,
            COLOR_O, 22, anchor_y="center", bold=True,
        )

        turn_color = COLOR_X if self.state.current_player == PLAYER_X else COLOR_O
        turn_text = f"Turn: {self.state.current_player}"
        if self.state.round_over:
            turn_text = "Round over"
        arcade.draw_text(
            turn_text, cx, SCREEN_HEIGHT - 40,
            turn_color, 22, anchor_x="center", anchor_y="center", bold=True,
        )

        if not self.state.round_over:
            total = DIFFICULTY_TIMES[self.state.difficulty]
            draw_timer_bar(self.state.time_left, total)

        diff_label = DIFFICULTY_LABELS[self.state.difficulty]
        arcade.draw_text(
            f"Difficulty: {diff_label}",
            20, GRID_ORIGIN_Y - 30,
            COLOR_TEXT_MUTED, 14, anchor_y="center",
        )

    def _draw_game_over_banner(self) -> None:
        if self.state.is_tie:
            lines = ["Tie!", "Press R to play again  |  ESC for menu"]
        else:
            winner = self.state.winner
            lines = [
                f"{winner} wins!",
                "Press R to play again  |  ESC for menu",
            ]
        draw_banner(lines)

    # Input functionality

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        if self.state.round_over:
            return
        cell = mouse_to_cell(x, y)
        if cell is None:
            return
        row, col = cell
        if self.state.make_move(row, col):
            sounds.play_place()

    def on_key_press(self, key: int, modifiers: int) -> None:
        if self.state.round_over:
            self._handle_post_round_key(key)
            return

        if key == KEY_MENU:
            self.window.show_view(MenuView())
            return
        if key == KEY_RESTART:
            self.setup()
            return
        if key in KEYS_DIFFICULTY:
            return  # ignored mid-round by design

        keymap = KEYS_PLAYER_1 if self.state.current_player == PLAYER_X else KEYS_PLAYER_2
        pos = keymap.get(key)
        if pos is None:
            return
        row, col = pos
        if self.state.make_move(row, col):
            sounds.play_place()

    def _handle_post_round_key(self, key: int) -> None:
        if key == KEY_RESTART:
            self.setup()
            return
        if key == KEY_MENU:
            self.window.show_view(MenuView())
            return
        if key in KEYS_DIFFICULTY:
            self.state.set_difficulty(KEYS_DIFFICULTY[key])

    # Update view

    def on_update(self, delta_time: float) -> None:
        self.state.tick(delta_time)
        if (
            self.state.round_over
            and self.state.winner is not None
            and not self._last_winner_played
        ):
            self._last_winner_played = True
            sounds.play_win()


# ---------------------------------------------------------------------------
# Helpers shared by the views
# ---------------------------------------------------------------------------


def cell_center(row: int, col: int) -> tuple[float, float]:
    """Pixel center of the cell at (row, col). Row 0 = top, col 0 = left."""
    cx = GRID_ORIGIN_X + col * CELL_SIZE + CELL_SIZE / 2
    cy = GRID_ORIGIN_Y + (GRID_SIZE - 1 - row) * CELL_SIZE + CELL_SIZE / 2
    return cx, cy


def mouse_to_cell(x: float, y: float) -> tuple[int, int] | None:
    """Convert mouse pixel coords to a (row, col) cell, or None if outside."""
    if not (GRID_ORIGIN_X <= x < GRID_ORIGIN_X + GRID_SIZE * CELL_SIZE):
        return None
    if not (GRID_ORIGIN_Y <= y < GRID_ORIGIN_Y + GRID_SIZE * CELL_SIZE):
        return None
    col = int((x - GRID_ORIGIN_X) // CELL_SIZE)
    row_from_top = int((y - GRID_ORIGIN_Y) // CELL_SIZE)
    row = GRID_SIZE - 1 - row_from_top
    return row, col


def draw_grid() -> None:
    """Draw the four grid lines that make up the 3x3 board."""
    for i in range(1, GRID_SIZE):
        x = GRID_ORIGIN_X + i * CELL_SIZE
        arcade.draw_line(
            x, GRID_ORIGIN_Y,
            x, GRID_ORIGIN_Y + GRID_SIZE * CELL_SIZE,
            COLOR_GRID, LINE_WIDTH,
        )
    for i in range(1, GRID_SIZE):
        y = GRID_ORIGIN_Y + i * CELL_SIZE
        arcade.draw_line(
            GRID_ORIGIN_X, y,
            GRID_ORIGIN_X + GRID_SIZE * CELL_SIZE, y,
            COLOR_GRID, LINE_WIDTH,
        )


def draw_marker(row: int, col: int, player: str) -> None:
    """Draw an X or O marker centered in cell (row, col)."""
    cx, cy = cell_center(row, col)
    pad = CELL_SIZE * 0.22
    if player == PLAYER_X:
        arcade.draw_line(
            cx - pad, cy - pad, cx + pad, cy + pad,
            COLOR_X, LINE_WIDTH,
        )
        arcade.draw_line(
            cx - pad, cy + pad, cx + pad, cy - pad,
            COLOR_X, LINE_WIDTH,
        )
    elif player == PLAYER_O:
        arcade.draw_circle_outline(
            cx, cy, CELL_SIZE * 0.32, COLOR_O, LINE_WIDTH,
        )


def draw_winning_line(cells: list[tuple[int, int]]) -> None:
    """Draw a thick green line through the three winning cells."""
    (r1, c1), (r3, c3) = cells[0], cells[2]
    x1, y1 = cell_center(r1, c1)
    x3, y3 = cell_center(r3, c3)
    arcade.draw_line(x1, y1, x3, y3, COLOR_WIN_LINE, LINE_WIDTH + 4)


def draw_timer_bar(time_left: float, total: float) -> None:
    """Draw a horizontal timer bar with a numeric label."""
    bar_x = SCREEN_WIDTH - 180
    bar_y = SCREEN_HEIGHT - 50
    bar_w = 140
    bar_h = 14

    arcade.draw_rect_filled(
        arcade.rect.XYWH(bar_x, bar_y, bar_w, bar_h),
        COLOR_TIMER_TRACK,
    )
    fill_w = max(0.0, bar_w * (time_left / total if total > 0 else 0))
    if fill_w > 0:
        arcade.draw_rect_filled(
            arcade.rect.XYWH(bar_x - (bar_w - fill_w) / 2, bar_y, fill_w, bar_h),
            COLOR_TIMER_FILL,
        )

    arcade.draw_text(
        f"{time_left:.1f}s",
        bar_x, bar_y - 22,
        COLOR_TEXT, 12,
        anchor_x="center", anchor_y="center",
    )


def draw_banner(text_lines: list[str]) -> None:
    """Draw a centered banner used for the 'Game Over' overlay."""
    cx = SCREEN_WIDTH / 2
    cy = SCREEN_HEIGHT / 2
    arcade.draw_rect_filled(
        arcade.rect.XYWH(cx, cy, BANNER_WIDTH, BANNER_HEIGHT),
        COLOR_BANNER_BG,
    )
    for i, line in enumerate(text_lines):
        size = 22 if i == 0 else 14
        color = COLOR_BANNER_TEXT if i == 0 else COLOR_TEXT_MUTED
        arcade.draw_text(
            line, cx, cy + 22 - i * 28,
            color, size,
            anchor_x="center", anchor_y="center", bold=(i == 0),
        )