"""
Pure-Python Tic-Tac-Toe logic: Board rules plus turn/timer/score flow.
"""

from __future__ import annotations

from typing import Optional

from constants import (
    DIFFICULTY_TIMES,
    FIRST_PLAYER,
    PLAYER_O,
    PLAYER_X,
)


class Board:
    """3x3 board that owns cell contents and win/tie rules only."""

    SIZE: int = 3

    def __init__(self) -> None:
        self.cells: list[list[str]] = [
            ["" for _ in range(self.SIZE)] for _ in range(self.SIZE)
        ]

    def reset(self) -> None:
        for row in self.cells:
            for c in range(self.SIZE):
                row[c] = ""

    def place(self, row: int, col: int, player: str) -> bool:
        if not (0 <= row < self.SIZE and 0 <= col < self.SIZE):
            return False
        if self.cells[row][col] != "":
            return False
        self.cells[row][col] = player
        return True

    def is_full(self) -> bool:
        return all(cell != "" for row in self.cells for cell in row)

    def winning_line(self) -> Optional[tuple[str, list[tuple[int, int]]]]:
        b = self.cells

        for r in range(self.SIZE):
            if b[r][0] != "" and b[r][0] == b[r][1] == b[r][2]:
                return b[r][0], [(r, 0), (r, 1), (r, 2)]

        for c in range(self.SIZE):
            if b[0][c] != "" and b[0][c] == b[1][c] == b[2][c]:
                return b[0][c], [(0, c), (1, c), (2, c)]

        if b[0][0] != "" and b[0][0] == b[1][1] == b[2][2]:
            return b[0][0], [(0, 0), (1, 1), (2, 2)]

        if b[0][2] != "" and b[0][2] == b[1][1] == b[2][0]:
            return b[0][2], [(0, 2), (1, 1), (2, 0)]

        return None


class GameState:
    """Wraps a Board with turn logic, timer, scores, and difficulty."""

    def __init__(self, difficulty: str = "easy") -> None:
        self.board: Board = Board()
        self.current_player: str = FIRST_PLAYER
        self.score_x: int = 0
        self.score_o: int = 0
        self.difficulty: str = difficulty
        self.time_left: float = DIFFICULTY_TIMES[difficulty]
        self.round_over: bool = False
        self.winner: Optional[str] = None
        self.winning_cells: Optional[list[tuple[int, int]]] = None
        self.is_tie: bool = False
        # Winner of the previous round starts the next one. Stays None on a
        # brand-new game or after a tie, so FIRST_PLAYER is used as fallback.
        self.last_winner: Optional[str] = None

    def start_round(self) -> None:
        self.board.reset()
        # Winner of the previous round starts the next one; fall back to
        # FIRST_PLAYER for a brand-new game or after a tie.
        self.current_player = self.last_winner if self.last_winner else FIRST_PLAYER
        self.time_left = DIFFICULTY_TIMES[self.difficulty]
        self.round_over = False
        self.winner = None
        self.winning_cells = None
        self.is_tie = False

    def make_move(self, row: int, col: int) -> bool:
        if self.round_over:
            return False
        if not self.board.place(row, col, self.current_player):
            return False

        win = self.board.winning_line()
        if win is not None:
            self.winner, self.winning_cells = win
            self.round_over = True
            self.last_winner = self.winner
            if self.winner == PLAYER_X:
                self.score_x += 1
            elif self.winner == PLAYER_O:
                self.score_o += 1
            return True

        if self.board.is_full():
            self.is_tie = True
            self.round_over = True
            return True

        self.switch_turn()
        return True

    def switch_turn(self) -> None:
        self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
        self.time_left = DIFFICULTY_TIMES[self.difficulty]

    def tick(self, delta_time: float) -> None:
        if self.round_over:
            return
        self.time_left -= delta_time
        if self.time_left <= 0.0:
            self.time_left = 0.0
            # Time's up: the active player loses and the opponent wins the round.
            loser = self.current_player
            winner = PLAYER_O if loser == PLAYER_X else PLAYER_X
            self.winner = winner
            self.winning_cells = None
            self.round_over = True
            self.last_winner = winner
            if winner == PLAYER_X:
                self.score_x += 1
            elif winner == PLAYER_O:
                self.score_o += 1

    def set_difficulty(self, difficulty: str) -> bool:
        if difficulty not in DIFFICULTY_TIMES:
            return False
        if not self.round_over:
            return False
        self.difficulty = difficulty
        self.time_left = DIFFICULTY_TIMES[difficulty]
        return True
