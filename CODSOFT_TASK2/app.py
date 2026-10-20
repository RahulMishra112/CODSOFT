"""
Flask Web Application Backend for Tic-Tac-Toe AI.
Connects HTML/CSS/JS Frontend to Python Minimax Logic.
"""

from flask import Flask, render_template, request, jsonify
from game_logic import TicTacToeGame
from ai_engine import TicTacToeAI

app = Flask(__name__)
ai = TicTacToeAI(ai_player=TicTacToeGame.PLAYER_O)

@app.route('/')
def home():
    """Renders the main frontend interface."""
    return render_template('index.html')

@app.route('/api/move', methods=['POST'])
def make_move():
    """
    API Endpoint: Receives current board state and human move,
    updates board, calculates best AI response, and returns updated state.
    """
    data = request.get_json()
    board = data.get('board', [' '] * 9)
    human_move = data.get('move', None)

    game = TicTacToeGame()
    game.board = list(board)

    # Execute Human Move if provided
    if human_move is not None and 0 <= human_move <= 8 and game.board[human_move] == TicTacToeGame.EMPTY:
        game.make_move(human_move, TicTacToeGame.PLAYER_X)

    # Check state after Human Move
    winner_info = game.check_winner()
    if winner_info or game.is_board_full():
        return jsonify({
            'board': game.board,
            'winner': winner_info[0] if winner_info else ('Draw' if game.is_board_full() else None),
            'winning_line': winner_info[1] if winner_info else None,
            'ai_move': None
        })

    # Calculate AI Move
    ai_move = ai.get_best_move(game)
    if ai_move != -1:
        game.make_move(ai_move, TicTacToeGame.PLAYER_O)

    # Check state after AI Move
    winner_info = game.check_winner()
    return jsonify({
        'board': game.board,
        'winner': winner_info[0] if winner_info else ('Draw' if game.is_board_full() else None),
        'winning_line': winner_info[1] if winner_info else None,
        'ai_move': ai_move
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)