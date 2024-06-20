import tkinter as tk
from tkinter import messagebox
from collections import Counter

# Constants representing the game states
EMPTY = 0
X = 1
O = -1

# Function to determine the current player
def current_player(board):
    counts = Counter(board)
    if counts[X] > counts[O]:
        return O
    return X if counts[X] == counts[O] else None

# Function to list possible actions
def possible_actions(board):
    player = current_player(board)
    return [(player, i) for i in range(len(board)) if board[i] == EMPTY]

# Function to apply an action to the board
def apply_action(board, action):
    player, index = action
    new_board = board.copy()
    new_board[index] = player
    return new_board

# Function to check if the game has ended
def is_terminal(board):
    for i in range(3):
        # Check rows and columns
        if board[3 * i] == board[3 * i + 1] == board[3 * i + 2] != EMPTY:
            return board[3 * i]
        if board[i] == board[i + 3] == board[i + 6] != EMPTY:
            return board[i]
    # Check diagonals
    if board[0] == board[4] == board[8] != EMPTY:
        return board[0]
    if board[2] == board[4] == board[6] != EMPTY:
        return board[2]
    # Check for a tie
    if EMPTY not in board:
        return 0
    return None

# Utility function for minimax evaluation
def utility(board, depth):
    result = is_terminal(board)
    if result is not None:
        return result, depth
    evaluations = [utility(apply_action(board, action), depth + 1) for action in possible_actions(board)]
    player = current_player(board)
    if player == X:
        best_score = max(evaluations, key=lambda x: x[0])
    else:
        best_score = min(evaluations, key=lambda x: x[0])
    return best_score

# Minimax function to determine the best action
def minimax(board):
    actions = possible_actions(board)
    evaluations = [(action, utility(apply_action(board, action), 1)) for action in actions]
    if not evaluations:
        return (0, 0), (0, 0)
    best_action = min(evaluations, key=lambda x: x[1]) if current_player(board) == O else max(evaluations, key=lambda x: x[1])
    return best_action

# Function to update the board and check for game end
def update_board(buttons, board, index, player, mode):
    board[index] = player
    buttons[index].config(text='X' if player == X else 'O', state=tk.DISABLED,
                          disabledforeground='blue' if player == X else 'red')
    if is_terminal(board) is not None:
        handle_game_end(board, mode)

# Function to handle game end
def handle_game_end(board, mode):
    global score_x, score_o, score_ties
    result = is_terminal(board)
    if mode == 'Single Player':
        if result == X:
            messagebox.showinfo("Game Over", "You have won!")
            score_x += 1
        elif result == O:
            messagebox.showinfo("Game Over", "You have lost!")
            score_o += 1
        else:
            messagebox.showinfo("Game Over", "It's a tie!")
            score_ties += 1
    else:  # Multiplayer mode
        if result == X:
            messagebox.showinfo("Game Over", "Player X has won!")
            score_x += 1
        elif result == O:
            messagebox.showinfo("Game Over", "Player O has won!")
            score_o += 1
        else:
            messagebox.showinfo("Game Over", "It's a tie!")
            score_ties += 1
    update_scoreboard()
    reset_board()

# Function to handle button click for single player mode
def on_button_click_single(buttons, board, index, mode):
    update_board(buttons, board, index, X, mode)
    if is_terminal(board) is None:
        action = minimax(board)
        update_board(buttons, board, action[0][1], O, mode)

# Function to handle button click for multiplayer mode
def on_button_click_multi(buttons, board, index, mode):
    player = current_player(board)
    update_board(buttons, board, index, player, mode)

# Function to reset the board for a new game
def reset_board():
    global board, buttons
    board = [EMPTY for _ in range(9)]
    for button in buttons:
        button.config(text='', state=tk.NORMAL)

# Function to update the scoreboard
def update_scoreboard():
    global score_label
    score_label.config(text=f"X: {score_x}   O: {score_o}   Ties: {score_ties}")

# Function to start the game
def start_game(mode):
    global root, board, buttons, score_label
    root = tk.Tk()
    root.title("Tic-Tac-Toe")

    # Initialize the board
    board = [EMPTY for _ in range(9)]
    buttons = []

    # Create a scoreboard
    score_label = tk.Label(root, text="X: 0   O: 0   Ties: 0", font='Arial 15')
    score_label.grid(row=0, column=0, columnspan=3)

    # Create buttons and place them in the grid
    for i in range(9):
        if mode == 'Single Player':
            button = tk.Button(root, text='', font='Arial 20', width=5, height=2, 
                               command=lambda i=i: on_button_click_single(buttons, board, i, mode))
        else:
            button = tk.Button(root, text='', font='Arial 20', width=5, height=2, 
                               command=lambda i=i: on_button_click_multi(buttons, board, i, mode))
        button.grid(row=(i // 3) + 1, column=i % 3)
        buttons.append(button)

    # Start the GUI event loop
    root.mainloop()

# Function to choose the game mode
def choose_mode():
    mode_window = tk.Tk()
    mode_window.title("Choose Mode")
    
    single_button = tk.Button(mode_window, text="Single Player", font='Arial 15', 
                              command=lambda: [mode_window.destroy(), start_game('Single Player')])
    single_button.pack(pady=10)
    
    multi_button = tk.Button(mode_window, text="Multiplayer", font='Arial 15', 
                             command=lambda: [mode_window.destroy(), start_game('Multiplayer')])
    multi_button.pack(pady=10)
    
    mode_window.mainloop()

# Initialize scores
score_x = 0
score_o = 0
score_ties = 0

# Start the mode selection window
choose_mode()
