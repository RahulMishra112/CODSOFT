"""
AI Decision Engine using Minimax with Alpha-Beta Pruning.
Calculates optimal move guaranteeing unbeatable gameplay.
"""

import math
from typing import Tuple, Optional
from game_logic import TicTacToeGame

class TicTacToeAI:
    def __init__(self, ai_player: str = TicTacToeGame.PLAYER_O) -> None:
        self.ai_player = ai_player
        self.human_player = TicTacToeGame.PLAYER_X if ai_player == TicTacToeGame.PLAYER_O else TicTacToeGame.PLAYER_O

    def evaluate(self, game: TicTacToeGame, depth: int) -> int:
        """
        Static evaluation of board state.
        Prefers earlier wins and delayed losses.
        """
        win_info = game.check_winner()
        if win_info:
            winner, _ = win_info
            if winner == self.ai_player:
                return 10 - depth
            elif winner == self.human_player:
                return -10 + depth
        return 0

    def minimax(self, game: TicTacToeGame, depth: int, alpha: float, beta: float, is_maximizing: bool) -> int:
        """
        Recursive Minimax search algorithm with Alpha-Beta Pruning.
        """
        if game.is_terminal():
            return self.evaluate(game, depth)

        if is_maximizing:
            max_eval = -math.inf
            for move in game.get_available_moves():
                game.board[move] = self.ai_player
                eval_score = self.minimax(game, depth + 1, alpha, beta, False)
                game.board[move] = TicTacToeGame.EMPTY  # Undo move

                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Prune branch
            return int(max_eval)
        else:
            min_eval = math.inf
            for move in game.get_available_moves():
                game.board[move] = self.human_player
                eval_score = self.minimax(game, depth + 1, alpha, beta, True)
                game.board[move] = TicTacToeGame.EMPTY  # Undo move

                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Prune branch
            return int(min_eval)

    def get_best_move(self, game: TicTacToeGame) -> int:
        """Determines the optimal move index for the AI."""
        best_score = -math.inf
        best_move = -1
        
        # Edge case: If AI goes first on an empty board, grab center immediately for speed
        available_moves = game.get_available_moves()
        if len(available_moves) == 9:
            return 4

        for move in available_moves:
            game.board[move] = self.ai_player
            score = self.minimax(game, 0, -math.inf, math.inf, False)
            game.board[move] = TicTacToeGame.EMPTY  # Undo move

            if score > best_score:
                best_score = score
                best_move = move

        return best_move