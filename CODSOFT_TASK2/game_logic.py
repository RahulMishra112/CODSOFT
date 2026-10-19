"""
Game Logic Engine for Tic-Tac-Toe.
Manages board representation, move validation, win/draw state evaluation.
"""

from typing import List, Optional, Tuple

class TicTacToeGame:
    PLAYER_X = 'X'  # Human
    PLAYER_O = 'O'  # AI
    EMPTY = ' '

    WINNING_COMBINATIONS = [
        # Rows
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        # Columns
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        # Diagonals
        (0, 4, 8), (2, 4, 6)
    ]

    def __init__(self) -> None:
        self.board: List[str] = [self.EMPTY] * 9
        self.current_turn: str = self.PLAYER_X

    def reset(self) -> None:
        """Resets board to initial empty state."""
        self.board = [self.EMPTY] * 9
        self.current_turn = self.PLAYER_X

    def get_available_moves(self) -> List[int]:
        """Returns list of open square indices (0-8)."""
        return [i for i, cell in enumerate(self.board) if cell == self.EMPTY]

    def make_move(self, position: int, player: str) -> bool:
        """Executes move if cell is valid and empty."""
        if 0 <= position <= 8 and self.board[position] == self.EMPTY:
            self.board[position] = player
            self.current_turn = self.PLAYER_O if player == self.PLAYER_X else self.PLAYER_X
            return True
        return False

    def check_winner(self) -> Optional[Tuple[str, Tuple[int, int, int]]]:
        """
        Checks if player won.
        Returns Tuple of (Winning Player, Combination) or None.
        """
        for combo in self.WINNING_COMBINATIONS:
            a, b, c = combo
            if self.board[a] != self.EMPTY and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a], combo
        return None

    def is_board_full(self) -> bool:
        """Returns True if no empty squares remain."""
        return self.EMPTY not in self.board

    def is_terminal(self) -> bool:
        """Returns True if game ended by win or draw."""
        return self.check_winner() is not None or self.is_board_full()