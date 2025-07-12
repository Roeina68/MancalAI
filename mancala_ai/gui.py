import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mancala_ai.game.board import Board
from mancala_ai.game.rules import GameRules
from mancala_ai.ai.minimax import MinimaxAI
from mancala_ai.ai.iterative import IterativeDeepeningAI

class MancalaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mancala Game")
        self.root.geometry("1200x800")
        
        # Game state
        self.board = Board()
        # self.ai = MinimaxAI(max_depth=4)
        self.ai = IterativeDeepeningAI()

        self.game_over = False

        # Main frames
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.grid(row=0, column=0, columnspan=3, sticky='nsew')
        
        # Configure grid weights to make the board frame expand
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.log_text = tk.Text(self.main_frame, height=8, width=80, font=('Arial', 10))
        self.log_text.grid(row=1, column=0, columnspan=3, pady=10)
        self.log_text.insert(tk.END, "Welcome to Mancala! You are Player 1 (bottom row).\n")
        self.log_text.config(state=tk.DISABLED)

        self.new_game_btn = tk.Button(self.main_frame, text="New Game", command=self.new_game, font=('Arial', 12))
        self.new_game_btn.grid(row=2, column=1)

        self.player_label = tk.Label(self.main_frame, text="Player 1's Turn", font=('Arial', 14, 'bold'), fg='green')
        self.player_label.grid(row=2, column=0)

        self.score_label = tk.Label(self.main_frame, text="Score: 0 - 0", font=('Arial', 12))
        self.score_label.grid(row=2, column=2)

        self.build_board()
        self.update_display()

    def build_board(self):
        self.top_pits = []
        self.bottom_pits = []

        # AI store (left side) - column 0
        ai_store_frame = tk.Frame(self.board_frame)
        ai_store_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        self.ai_store = tk.Label(ai_store_frame, text="0", width=6, height=8,
                                 relief='raised', borderwidth=3, bg='lightblue')
        self.ai_store.pack()

        ai_label = tk.Label(ai_store_frame, text="AI Store", font=('Arial', 10))
        ai_label.pack()

        # AI pits (top row) - columns 1-6, reversed for visual clarity
        for i in range(Board.PITS_PER_PLAYER):
            pit_index = Board.PITS_PER_PLAYER - 1 - i
            pit_frame = tk.Frame(self.board_frame)
            pit_frame.grid(row=0, column=i + 1, padx=5, pady=5)

            pit = tk.Label(pit_frame, text="4", width=8, height=3,
                           relief='raised', borderwidth=2, bg='lightgray')
            pit.pack()

            pit_num = tk.Label(pit_frame, text=str(pit_index), font=('Arial', 8))
            pit_num.pack()

            self.top_pits.append(pit)

        # Player pits (bottom row) - columns 1-6
        for i in range(Board.PITS_PER_PLAYER):
            pit_frame = tk.Frame(self.board_frame)
            pit_frame.grid(row=1, column=i + 1, padx=5, pady=5)

            pit_num = tk.Label(pit_frame, text=str(i), font=('Arial', 8))
            pit_num.pack()

            btn = tk.Button(pit_frame, text="4", width=8, height=3,
                            command=lambda x=i: self.handle_player_move(x))
            btn.pack()

            self.bottom_pits.append(btn)

        # Player store (right side) - column 7
        player_store_frame = tk.Frame(self.board_frame)
        player_store_frame.grid(row=0, column=Board.PITS_PER_PLAYER + 1, rowspan=2, padx=10, pady=10)

        self.player_store = tk.Label(player_store_frame, text="0", width=6, height=8,
                                     relief='raised', borderwidth=3, bg='lightgreen')
        self.player_store.pack()

        player_label = tk.Label(player_store_frame, text="Player Store", font=('Arial', 10))
        player_label.pack()

    def update_display(self):
        for i in range(Board.PITS_PER_PLAYER):
            self.bottom_pits[i].config(text=str(self.board.pits[0][i]))
            self.bottom_pits[i].config(
                state='normal' if self.board.pits[0][i] > 0 and not self.game_over else 'disabled',
                bg='SystemButtonFace' if self.board.pits[0][i] > 0 else 'lightgray'
            )

        for i in range(Board.PITS_PER_PLAYER):
            self.top_pits[i].config(text=str(self.board.pits[1][Board.PITS_PER_PLAYER - 1 - i]))

        self.player_store.config(text=str(self.board.stores[0]))
        self.ai_store.config(text=str(self.board.stores[1]))

        self.player_label.config(
            text="Player 1's Turn" if self.board.current_player == 0 else "AI's Turn",
            fg='green' if self.board.current_player == 0 else 'red'
        )

        self.score_label.config(text=f"Score: {self.board.stores[0]} - {self.board.stores[1]}")

    def handle_player_move(self, pit_index):
        if self.game_over or self.board.current_player != 0:
            return

        if not GameRules.is_valid_move(self.board, pit_index):
            self.log_action(f"Invalid move: pit {pit_index} is empty")
            return

        success, extra_turn = GameRules.make_move(self.board, pit_index)
        self.log_action(f"Player picked pit {pit_index}")

        if success:
            # Apply penalty rule after the move
            penalty_applied = GameRules.apply_penalty_rule(self.board)
            if penalty_applied:
                self.log_action("⚠️ Penalty applied: 1 stone moved from store to closest pit")
            
            self.update_display()
            if self.check_game_over():
                return

            if not extra_turn:
                self.board.switch_player()
                self.root.after(1000, self.ai_turn)
            else:
                self.log_action("Player gets an extra turn!")

    def ai_turn(self):
        if self.game_over or self.board.current_player != 1:
            return

        move, _ = self.ai.get_best_move(self.board)
        self.log_action(f"AI picked pit {move}")
        success, extra_turn = GameRules.make_move(self.board, move)

        if success:
            # Apply penalty rule after the move
            penalty_applied = GameRules.apply_penalty_rule(self.board)
            if penalty_applied:
                self.log_action("⚠️ Penalty applied: 1 stone moved from store to closest pit")
            
            self.update_display()
            if self.check_game_over():
                return
            if extra_turn:
                self.log_action("AI gets an extra turn!")
                self.root.after(1000, self.ai_turn)
            else:
                self.board.switch_player()
                self.update_display()  # Update display after switching player

    def check_game_over(self):
        is_over, winner = GameRules.get_game_result(self.board)
        if is_over:
            self.game_over = True
            self.update_display()

            if winner == 0:
                msg = "🎉 Player 1 wins! 🎉"
            elif winner == 1:
                msg = "🤖 AI wins! 🤖"
            else:
                msg = "🤝 It's a draw! 🤝"

            self.log_action(msg)
            messagebox.showinfo("Game Over", msg)

            for btn in self.bottom_pits:
                btn.config(state='disabled')

            return True
        return False

    def log_action(self, text):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def new_game(self):
        self.board = Board()
        self.game_over = False
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, "New game started! You are Player 1 (bottom row).\n")
        self.log_text.config(state=tk.DISABLED)
        self.update_display()

def main():
    root = tk.Tk()
    app = MancalaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
