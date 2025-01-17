import tkinter as tk
from tkinter import messagebox
import mysql.connector
import random


# connect db
def connect_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",     # Replace with your MySQL username
        password="root", # Replace with your MySQL password
        database="SureTicTacToe"      # Replace with your database name
    )
    cursor = conn.cursor()
    return cursor, conn

# Database setup - it will be executed only once
def setup_database():
    cursor, conn = connect_database()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INT AUTO_INCREMENT PRIMARY KEY,
            playerName VARCHAR(100),
            result ENUM('Win', 'Loss', 'Draw')
        )
    """)
    conn.commit()
    conn.close()

# Save result to the database
def save_result(player_name, result):
    cursor, conn = connect_database()
    cursor.execute("INSERT INTO games (playerName, result) VALUES (%s, %s)", (player_name, result))
    conn.commit()
    conn.close()

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
def computer_move(board):
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

# Reset the game
def reset_game():
    global board, buttons
    board = [" "] * 9
    for button in buttons:
        button.config(text="", state=tk.NORMAL)

# Handle button click
def button_click(index):
    global board, player_name
    if board[index] == " ":
        board[index] = "X"
        buttons[index].config(text="X", state=tk.DISABLED)

        if check_winner(board, "X"):
            messagebox.showinfo("Game Over", f"Congratulations {player_name}, you win!")
            save_result(player_name, "Win")
            reset_game()
            return
        if is_full(board):
            messagebox.showinfo("Game Over", "It's a tie!")
            save_result(player_name, "Draw")
            reset_game()
            return

        comp_move = computer_move(board)
        board[comp_move] = "O"
        buttons[comp_move].config(text="O", state=tk.DISABLED)

        if check_winner(board, "O"):
            messagebox.showinfo("Game Over", "Computer wins! Better luck next time.")
            save_result(player_name, "Loss")
            reset_game()
            return
        if is_full(board):
            messagebox.showinfo("Game Over", "It's a tie!")
            save_result(player_name, "Draw")
            reset_game()

# Start game
def start_game():
    global player_name, board, buttons

    player_name = name_entry.get().strip()
    if not player_name:
        messagebox.showwarning("Input Error", "Please enter your name!")
        return

    # Remove the start screen and show the game board
    for widget in root.winfo_children():
        widget.destroy()

    # Initialize game board
    board = [" "] * 9
    buttons.clear()

    tk.Label(root, text=f"Welcome, {player_name}! You are 'X'.", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=(10, 5))

    for i in range(9):
        button = tk.Button(root, text="", font=("Arial", 24), height=2, width=5,
                           command=lambda i=i: button_click(i))
        button.grid(row=(i // 3) + 1, column=i % 3, pady=5, padx=5)
        buttons.append(button)

# Create the main window
root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("400x500")  # Increased resolution

# Start screen
tk.Label(root, text="Enter your name:", font=("Arial", 14)).pack(pady=20)
name_entry = tk.Entry(root, font=("Arial", 14))
name_entry.pack(pady=10)
start_button = tk.Button(root, text="Start Game", font=("Arial", 14), command=start_game)
start_button.pack(pady=20)

# Global variables
player_name = ""
board = [" "] * 9
buttons = []

# Run the GUI event loop
root.mainloop()
