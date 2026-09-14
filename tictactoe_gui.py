import tkinter as tk
from tkinter import messagebox, simpledialog
from math import inf as infinity
from random import choice
import time # For AI "thinking" delay, though less critical in GUI

# --- Core Game Logic (adapted from the original script) ---
HUMAN = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

human_choice = "X"
comp_choice = "O"
current_player = HUMAN # Can be HUMAN or COMP

def evaluate(state):
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0
    return score

def wins(state, player):
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    return [player, player, player] in win_state

def game_over(state):
    return wins(state, HUMAN) or wins(state, COMP)

def empty_cells(state):
    cells = []
    for x, row_val in enumerate(state):
        for y, cell_val in enumerate(row_val):
            if cell_val == 0:
                cells.append([x, y])
    return cells

# Note: The global `board` is modified by set_move
def set_move(x, y, player, current_board):
    if current_board[x][y] == 0:
        current_board[x][y] = player
        return True
    return False

def minimax(state, depth, player):
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        # Create a copy of the state for the recursive call if issues arise with direct modification
        # For now, direct modification and reset is used as in original
        current_score = minimax(state, depth - 1, -player)
        state[x][y] = 0  # Undo the move
        current_score[0], current_score[1] = x, y

        if player == COMP:
            if current_score[2] > best[2]:
                best = current_score
        else:
            if current_score[2] < best[2]:
                best = current_score
    return best

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        master.title("Tic-Tac-Toe with Minimax AI")

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_active = True

        self.setup_initial_choices()

        self.status_label = tk.Label(master, text="", font=("Arial", 14))
        self.status_label.pack(pady=10)

        board_frame = tk.Frame(master)
        board_frame.pack()

        for r in range(3):
            for c in range(3):
                button = tk.Button(board_frame,
                                   text="",
                                   font=("Arial", 30, "bold"),
                                   width=4,
                                   height=2,
                                   command=lambda row=r, col=c: self.player_click(row, col))
                button.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[r][c] = button

        restart_button = tk.Button(master, text="New Game", command=self.restart_game, font=("Arial", 12))
        restart_button.pack(pady=10)
        
        self.start_game()

    def setup_initial_choices(self):
        global human_choice, comp_choice, current_player, board
        
        # Reset board for new setup
        board = [[0, 0, 0] for _ in range(3)]

        player_symbol = simpledialog.askstring("Choose Symbol", "Do you want to be X or O? (X goes first)", parent=self.master)
        if player_symbol and player_symbol.upper() == "O":
            human_choice = "O"
            comp_choice = "X"
        else:
            human_choice = "X" # Default or if X is chosen
            comp_choice = "O"

        first_turn = simpledialog.askstring("First Turn", "Do you want to go first? (yes/no)", parent=self.master)
        if first_turn and first_turn.lower() == "no":
            current_player = COMP
        else:
            current_player = HUMAN # Default or if yes

    def start_game(self):
        self.game_active = True
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text="", state=tk.NORMAL)
        
        global board
        board = [[0, 0, 0] for _ in range(3)] # Ensure board is clean

        if current_player == HUMAN:
            self.status_label.config(text=f"Your turn ({human_choice})")
        else:
            self.status_label.config(text=f"Computer's turn ({comp_choice})")
            self.master.after(500, self.ai_move) # AI makes the first move

    def player_click(self, row, col):
        global current_player, board
        if not self.game_active or board[row][col] != 0 or current_player != HUMAN:
            return

        if set_move(row, col, HUMAN, board):
            self.buttons[row][col].config(text=human_choice, state=tk.DISABLED, disabledforeground="black")
            if self.check_for_winner():
                return

            current_player = COMP
            self.status_label.config(text=f"Computer's turn ({comp_choice})")
            self.master.after(500, self.ai_move) # Add a small delay for AI move

    def ai_move(self):
        global current_player, board
        if not self.game_active or current_player != COMP:
            return

        depth = len(empty_cells(board))
        if depth == 0 or game_over(board):
            return

        if depth == 9: # AI is first and board is empty
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
        else:
            # The minimax function needs a copy of the board to simulate moves without altering the actual game board prematurely.
            # The original minimax modifies the state passed to it and then resets it.
            # This should be fine as long as the global `board` is the one being passed and worked on.
            move = minimax(board, depth, COMP)
            x, y = move[0], move[1]

        if set_move(x, y, COMP, board):
            self.buttons[x][y].config(text=comp_choice, state=tk.DISABLED, disabledforeground="red")
            if self.check_for_winner():
                return
            current_player = HUMAN
            self.status_label.config(text=f"Your turn ({human_choice})")
        else:
            # This case should ideally not happen if minimax and empty_cells are correct
            print("AI made an invalid move - this is a bug") 
            # As a fallback, try to pick any empty cell if minimax fails (highly unlikely)
            if empty_cells(board):
                fallback_move = choice(empty_cells(board))
                if set_move(fallback_move[0], fallback_move[1], COMP, board):
                     self.buttons[fallback_move[0]][fallback_move[1]].config(text=comp_choice, state=tk.DISABLED, disabledforeground="red")
                     if self.check_for_winner():
                         return
                     current_player = HUMAN
                     self.status_label.config(text=f"Your turn ({human_choice})")
            else: # No empty cells, should be a draw or win already handled
                self.check_for_winner() # Re-check, might be a draw


    def check_for_winner(self):
        global board
        if wins(board, HUMAN):
            self.status_label.config(text=f"You ({human_choice}) win!")
            messagebox.showinfo("Game Over", "Congratulations! You win!")
            self.end_game()
            return True
        elif wins(board, COMP):
            self.status_label.config(text=f"Computer ({comp_choice}) wins!")
            messagebox.showinfo("Game Over", "Computer wins! Better luck next time.")
            self.end_game()
            return True
        elif len(empty_cells(board)) == 0:
            self.status_label.config(text="It's a Draw!")
            messagebox.showinfo("Game Over", "It's a Draw!")
            self.end_game()
            return True
        return False

    def end_game(self):
        self.game_active = False
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(state=tk.DISABLED)

    def restart_game(self):
        global board, current_player # Reset these globals
        board = [[0, 0, 0] for _ in range(3)]
        self.game_active = True
        self.setup_initial_choices() # Ask for symbol and who goes first again
        self.start_game() # This will re-enable buttons and set initial turn

if __name__ == "__main__":
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()

