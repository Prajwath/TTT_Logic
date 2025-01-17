import random

# Display the board
def display_board(board):
    print("\n")
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("--+---+--")
    print(f"{board[6]} | {board[7]} | {board[8]}")
    print("\n")

# Check for a win or tie
def check_winner(board, player):
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for combo in win_combinations:
        if all(board[i] == player for i in combo):
            return True
    return False

# Check if the board is full (tie)
def is_full(board):
    return all(spot != " " for spot in board)

# Minimax algorithm for the computer's optimal move
def minimax(board, depth, is_maximizing):
    if check_winner(board, "O"):  # Computer wins
        return 10 - depth
    if check_winner(board, "X"):  # User wins
        return depth - 10
    if is_full(board):  # Tie
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = " "
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = " "
                best_score = min(best_score, score)
        return best_score

# Find the computer's move
def computer_move(board, win_probability=0.6):
    # Roll a random number to decide strategy
    if random.random() < win_probability:
        # Optimal move (60% of the time)
        best_score = -float("inf")
        move = None
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, 0, False)
                board[i] = " "
                if score > best_score:
                    best_score = score
                    move = i
        return move
    else:
        # Random move (30% of the time)
        valid_moves = [i for i, spot in enumerate(board) if spot == " "]
        return random.choice(valid_moves)

# Main game loop
def tic_tac_toe():
    board = [" "] * 9
    print("Welcome to Tic Tac Toe!")
    print("You are X, and the computer is O.")
    display_board(board)

    while True:
        # User's turn
        try:
            user_move = int(input("Enter your move (0-8): "))
            if board[user_move] != " ":
                print("Invalid move. Try again.")
                continue
            board[user_move] = "X"
        except (ValueError, IndexError):
            print("Invalid input. Please enter a number between 0 and 8.")
            continue
        display_board(board)

        if check_winner(board, "X"):
            print("Congratulations! You win!")
            break
        if is_full(board):
            print("It's a tie!")
            break

        # Computer's turn
        print("Computer's turn...")
        comp_move = computer_move(board, win_probability=0.6)  # 60% optimal moves
        board[comp_move] = "O"
        display_board(board)

        if check_winner(board, "O"):
            print("Computer wins! Better luck next time.")
            break
        if is_full(board):
            print("It's a tie!")
            break

# Run the game
tic_tac_toe()
