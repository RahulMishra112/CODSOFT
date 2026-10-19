"""
Automated Unit Tests & Exhaustive Unbeatable Verification Suite.
"""

import pytest
from game_logic import TicTacToeGame
from ai_engine import TicTacToeAI

def test_ai_takes_winning_move():
    game = TicTacToeGame()
    # O | O | .
    # X | X | .
    # . | . | .
    game.board = ['O', 'O', ' ', 'X', 'X', ' ', ' ', ' ', ' ']
    ai = TicTacToeAI(ai_player='O')
    best_move = ai.get_best_move(game)
    assert best_move == 2  # Complete top row win

def test_ai_blocks_human_win():
    game = TicTacToeGame()
    # X | X | .
    # O | . | .
    # . | . | .
    game.board = ['X', 'X', ' ', 'O', ' ', ' ', ' ', ' ', ' ']
    ai = TicTacToeAI(ai_player='O')
    best_move = ai.get_best_move(game)
    assert best_move == 2  # Block human winning top row

def test_win_detections():
    game = TicTacToeGame()
    # Diagonal win
    game.board = ['O', 'X', 'X', ' ', 'O', ' ', ' ', ' ', 'O']
    winner_info = game.check_winner()
    assert winner_info is not None
    assert winner_info[0] == 'O'

def test_draw_detection():
    game = TicTacToeGame()
    game.board = ['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'X']
    assert game.is_board_full() is True
    assert game.check_winner() is None

def test_unbeatable_ai_exhaustive():
    """
    Simulates all possible moves by Human across whole tree.
    Verifies that AI NEVER loses (Outcome is either AI Win or Draw).
    """
    ai = TicTacToeAI(ai_player='O')

    def simulate_play(game_state: TicTacToeGame, is_human_turn: bool) -> None:
        if game_state.is_terminal():
            winner_info = game_state.check_winner()
            if winner_info:
                assert winner_info[0] != 'X', "AI lost! Unbeatable invariant failed."
            return

        if is_human_turn:
            for move in game_state.get_available_moves():
                game_state.board[move] = 'X'
                simulate_play(game_state, False)
                game_state.board[move] = ' '  # Backtrack
        else:
            ai_move = ai.get_best_move(game_state)
            game_state.board[ai_move] = 'O'
            simulate_play(game_state, True)
            game_state.board[ai_move] = ' '  # Backtrack

    initial_game = TicTacToeGame()
    simulate_play(initial_game, is_human_turn=True)