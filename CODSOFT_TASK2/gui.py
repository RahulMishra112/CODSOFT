"""
Tkinter User Interface for Tic-Tac-Toe AI.
Handles rendering, turn visualization, and interaction.
"""

import tkinter as tk
from tkinter import messagebox
from typing import List, Optional
from game_logic import TicTacToeGame
from ai_engine import TicTacToeAI

class TicTacToeGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("CodSoft Task 2 — Tic-Tac-Toe AI")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#1E1E2E")  # Dark theme background

        self.game = TicTacToeGame()
        self.ai = TicTacToeAI(ai_player=TicTacToeGame.PLAYER_O)

        self.buttons: List[tk.Button] = []
        self._create_widgets()

    def _create_widgets(self) -> None:
        # Title Header
        title_label = tk.Label(
            self.root, text="TIC-TAC-TOE AI", font=("Helvetica", 20, "bold"),
            bg="#1E1E2E", fg="#89B4FA"
        )
        title_label.pack(pady=10)

        # Status Display
        self.status_label = tk.Label(
            self.root, text="Your Turn (X)", font=("Helvetica", 14),
            bg="#1E1E2E", fg="#CDD6F4"
        )
        self.status_label.pack(pady=5)

        # Board Frame
        board_frame = tk.Frame(self.root, bg="#313244", padx=10, pady=10)
        board_frame.pack(pady=10)

        # 3x3 Grid Buttons
        for i in range(9):
            row, col = divmod(i, 3)
            btn = tk.Button(
                board_frame, text="", font=("Helvetica", 24, "bold"),
                width=5, height=2, bg="#45475A", fg="#CDD6F4",
                activebackground="#585B70", activeforeground="#CDD6F4",
                relief="flat", command=lambda idx=i: self._on_button_click(idx)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(btn)

        # Control Panel Buttons
        control_frame = tk.Frame(self.root, bg="#1E1E2E")
        control_frame.pack(pady=15)

        restart_btn = tk.Button(
            control_frame, text="Restart Game", font=("Helvetica", 11, "bold"),
            bg="#A6E3A1", fg="#11111B", activebackground="#94E2D5",
            padx=15, pady=5, relief="flat", command=self.reset_game
        )
        restart_btn.pack(side=tk.LEFT, padx=10)

    def _on_button_click(self, index: int) -> None:
        if self.game.board[index] != TicTacToeGame.EMPTY or self.game.is_terminal():
            return

        # Execute Human Move
        if self.game.make_move(index, TicTacToeGame.PLAYER_X):
            self._update_button_ui(index, TicTacToeGame.PLAYER_X, "#F38BA8") # Pink-Red for X
            
            if self._check_game_over():
                return

            # AI Move Phase
            self.status_label.config(text="AI Thinking (O)...")
            self.root.update_idletasks()

            ai_move = self.ai.get_best_move(self.game)
            if ai_move != -1 and self.game.make_move(ai_move, TicTacToeGame.PLAYER_O):
                self._update_button_ui(ai_move, TicTacToeGame.PLAYER_O, "#89B4FA") # Blue for O
                self._check_game_over()

    def _update_button_ui(self, index: int, player: str, color: str) -> None:
        self.buttons[index].config(text=player, state="disabled", disabledforeground=color)

    def _check_game_over(self) -> bool:
        win_info = self.game.check_winner()
        if win_info:
            winner, combo = win_info
            for idx in combo:
                self.buttons[idx].config(bg="#A6E3A1", disabledforeground="#11111B")  # Highlight winning line
            
            msg = "You Win! (Unexpected)" if winner == TicTacToeGame.PLAYER_X else "AI Wins!"
            self.status_label.config(text=msg, fg="#A6E3A1" if winner == TicTacToeGame.PLAYER_X else "#F38BA8")
            self._disable_all_buttons()
            messagebox.showinfo("Game Over", msg)
            return True

        if self.game.is_board_full():
            self.status_label.config(text="It's a Draw!", fg="#FAB387")
            messagebox.showinfo("Game Over", "Game ended in a draw!")
            return True

        self.status_label.config(text="Your Turn (X)")
        return False

    def _disable_all_buttons(self) -> None:
        for btn in self.buttons:
            btn.config(state="disabled")

    def reset_game(self) -> None:
        self.game.reset()
        for btn in self.buttons:
            btn.config(text="", state="normal", bg="#45475A")
        self.status_label.config(text="Your Turn (X)", fg="#CDD6F4")