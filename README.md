# Tic-Tac-Toe in Python with Minimax AI

A desktop Tic-Tac-Toe game built with **Python** and **Tkinter**, featuring a computer opponent powered by the **Minimax algorithm**. Play on an interactive 3×3 board, choose your symbol, and challenge an AI that searches possible moves to select the best outcome.

## Features

- **Human vs. computer:** Play against a Minimax-based opponent.
- **Interactive GUI:** Make moves by clicking buttons on a 3×3 board.
- **Symbol selection:** Choose X or O before each game.
- **First-turn selection:** Decide whether you or the computer starts.
- **Turn indicator:** See whose turn it is and which symbol they use.
- **Automatic result detection:** Receive a message when either player wins or the game ends in a draw.
- **Move validation:** Occupied cells and clicks during the computer's turn are ignored.
- **New Game button:** Reset the board and choose your preferences again.
- **Visual distinction:** Human moves appear in black and computer moves in red.

## Technologies

| Component | Purpose |
| --- | --- |
| Python 3 | Game logic and application code |
| Tkinter | Window, board buttons, status label, and dialogs |
| Minimax | Recursive search for the computer's best move |
| `math.inf` | Initial bounds when comparing move scores |
| `random.choice` | Random opening move when the computer starts |

## Getting Started

### Requirements

- Python 3 with Tkinter available.
- A desktop environment capable of displaying GUI windows.

The game uses Python standard-library modules. No third-party Python packages or API keys are required. Some Python installations provide Tkinter separately.

### Setup and Run

1. Download the project's Python source file.
2. Save or rename it as `tic_tac_toe.py`. The commands below use this filename.
3. Open a terminal in the folder containing the file.
4. Check that Tkinter is available:

   ```bash
   python -m tkinter
   ```

   A small demonstration window should open. Close it before continuing.

5. Start the game:

   ```bash
   python tic_tac_toe.py
   ```

   On Windows, you can also use:

   ```powershell
   py tic_tac_toe.py
   ```

   If your system uses `python3`, substitute it for `python` in these commands.

## How to Play

1. Choose **X** or **O** in the symbol dialog. The default is X.
2. Enter **yes** to move first or **no** to let the computer start. The default is to move first.
3. Click an empty cell during your turn.
4. The computer schedules its response after a short 500 ms delay, then calculates and plays its move.
5. Complete a row, column, or diagonal with three matching symbols to win. A full board without a winner is a draw.
6. Click **New Game** to start another round.

**First-turn behavior:** The first-turn dialog determines who starts, regardless of the selected symbol. Although the symbol prompt says “X goes first,” the implementation allows either symbol to start.

## How the Minimax AI Works

Minimax explores possible future moves, assuming both players choose the best available outcome for themselves.

The board stores `0` for an empty cell, `-1` for the human, and `+1` for the computer. These values are independent of the displayed X and O symbols.

Terminal positions receive the following scores:

| Result | Score |
| --- | --- |
| Computer wins | +1 |
| Human wins | -1 |
| Draw | 0 |

For each available cell, the algorithm temporarily places a move, recursively evaluates the opponent's replies, and then undoes the move. The computer maximizes the score, while the simulated human minimizes it. The search ends when a player wins or no moves remain.

When the computer starts on an empty board, it chooses a random cell. Subsequent moves use Minimax. With correct play from both sides, the game ends in a draw.

This implementation searches the remaining game tree without alpha-beta pruning or memoization. Scores do not include move depth, so equally scored moves are not ranked by how quickly they win.

## Code Overview

| Function or class | Responsibility |
| --- | --- |
| `wins()` | Check rows, columns, and diagonals for a winner |
| `evaluate()` | Score the board from the computer's perspective |
| `game_over()` | Check whether either player has won |
| `empty_cells()` | Return the available board positions |
| `set_move()` | Place a move if the selected cell is empty |
| `minimax()` | Return the best move and its score |
| `TicTacToeGUI` | Manage the interface, turns, result dialogs, and restarts |

Draw detection is handled separately by checking whether the board has any empty cells.

## Learning Outcomes

This project demonstrates recursive problem solving, adversarial search, backtracking, board-state evaluation, and event-driven GUI programming with Tkinter.

## Possible Improvements

- Add alpha-beta pruning to reduce the number of evaluated positions.
- Introduce difficulty levels and a local two-player mode.
- Highlight the winning combination.
- Track wins, losses, and draws across rounds.
- Update the symbol prompt to match the independent first-turn selection.
