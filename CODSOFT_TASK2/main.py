"""
Main Application Entry Point.
Initializes Tkinter window loop.
"""

import tkinter as tk
from gui import TicTacToeGUI

def main() -> None:
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()