import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
import time

def is_valid(board, row, col, num):
    if num in board[row]: 
        return False
    if num in board[:, col]: 
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    if num in board[start_row:start_row + 3, start_col:start_col + 3]:
        return False
    return True

def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i, j] == 0:
                return i, j
    return None, None

def solve_sudoku(board):
    row, col = find_empty_cell(board)
    if row is None: 
        return True

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row, col] = num
            if solve_sudoku(board):
                return True
            board[row, col] = 0 

    return False  

def generate_sudoku(difficulty="medium"):
    base_board = np.zeros((9, 9), dtype=int)
    solve_sudoku(base_board)

    num_removed = {"easy": 40, "medium": 50, "hard": 60}[difficulty]
    for _ in range(num_removed):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while base_board[row, col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        base_board[row, col] = 0

    return base_board

def update_gui(board, grid_entries):
    for row in range(9):
        for col in range(9):
            value = board[row, col]
            grid_entries[row][col].delete(0, tk.END)
            if value != 0:
                grid_entries[row][col].insert(0, str(value))
                grid_entries[row][col].config(state="disabled")
            else:
                grid_entries[row][col].config(state="normal", bg="white")

def on_cell_change(row, col, grid_entries, board):
    value = grid_entries[row][col].get()
    try:
        num = int(value)
        if 1 <= num <= 9 and is_valid(board, row, col, num):
            board[row, col] = num
            grid_entries[row][col].config(bg="lightgreen")
        else:
            board[row, col] = 0  # Invalid input, reset cell
            grid_entries[row][col].config(bg="lightcoral")
    except ValueError:
        board[row, col] = 0  # Invalid input, reset cell
        grid_entries[row][col].config(bg="white")

def solve_button_click(board, grid_entries):
    if solve_sudoku(board):
        update_gui(board, grid_entries)
    else:
        print("No solution found.")

def hint_button_click(board, grid_entries):
    row, col = find_empty_cell(board)
    if row is not None:
        for num in range(1, 10):
            if is_valid(board, row, col, num):
                board[row, col] = num
                grid_entries[row][col].delete(0, tk.END)
                grid_entries[row][col].insert(0, str(num))
                grid_entries[row][col].config(bg="lightblue")
                break

def difficulty_selection(difficulty_var, board, grid_entries):
    difficulty = difficulty_var.get()
    new_board = generate_sudoku(difficulty)
    update_gui(new_board, grid_entries)

def start_timer(timer_label):
    start_time = time.time()

    def update_time():
        elapsed_time = int(time.time() - start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_label.config(text=f"Time: {minutes:02}:{seconds:02}")
        timer_label.after(1000, update_time)

    update_time()


def create_start_screen(root):
    root.title("Sudoku Game")
    root.geometry("800x600")
    root.resizable(False, False)
    
    canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    
    bg_image = Image.open(r"C:\MinGW\istockphoto-1387785129-612x612.jpg").resize((800, 600),Image.LANCZOS) 
    bg_image_tk = ImageTk.PhotoImage(bg_image)
    canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)
    
    style = ttk.Style()
    style.configure("Rounded.TFrame", borderwidth=0, relief="flat", background="#f0f0f0", padding=10)
    main_frame = ttk.Frame(root, style="Rounded.TFrame")
    main_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=200)
    
    welcome_label = tk.Label(main_frame, text="Welcome to Sudoku!", font=("Arial", 24, "bold"), bg="#f0f0f0")
    welcome_label.pack(pady=20)
    
    start_button = tk.Button(main_frame, text="Start Game", font=("Arial", 16), bg="#4CAF50", fg="white", command=lambda: start_game(root))
    start_button.pack(pady=10)
    
    root.bg_image_tk = bg_image_tk

def start_game(root):
    for widget in root.winfo_children():
        widget.destroy()
    create_sudoku_gui(root)

def create_sudoku_gui(root):
    root.title("Sudoku Game")
    root.geometry("800x600")

    grid_entries = []
    for i in range(9):
        row_entries = []
        for j in range(9):
            entry = tk.Entry(root, width=5, font=("Arial", 18), justify="center")
            entry.grid(row=i, column=j, padx=5, pady=5)
            row_entries.append(entry)
        grid_entries.append(row_entries)

    board = generate_sudoku()
    update_gui(board, grid_entries)

    timer_label = tk.Label(root, text="Time: 00:00", font=("Arial", 16))
    timer_label.grid(row=9, column=0, columnspan=9)

    start_timer(timer_label)

    solve_button = tk.Button(root, text="Solve", command=lambda: solve_button_click(board, grid_entries))
    solve_button.grid(row=10, column=0, columnspan=3)

    hint_button = tk.Button(root, text="Hint", command=lambda: hint_button_click(board, grid_entries))
    hint_button.grid(row=10, column=3, columnspan=3)

    difficulty_var = tk.StringVar(value="medium")
    difficulty_label = tk.Label(root, text="Difficulty:")
    difficulty_label.grid(row=10, column=6)
    difficulty_menu = tk.OptionMenu(root, difficulty_var, "easy", "medium", "hard")
    difficulty_menu.grid(row=10, column=7)

    difficulty_button = tk.Button(root, text="Change Difficulty", command=lambda: difficulty_selection(difficulty_var, board, grid_entries))
    difficulty_button.grid(row=10, column=8)

    def on_change(event, row, col):
        on_cell_change(row, col, grid_entries, board)

    for i in range(9):
        for j in range(9):
            grid_entries[i][j].bind("<FocusOut>", lambda event, row=i, col=j: on_change(event, row, col))

def generate_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)]
    for _ in range(20):  # Add 20 numbers randomly
        row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = random.randint(1, 9)
    return board

def update_gui(board, grid_entries):
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                grid_entries[i][j].insert(0, str(board[i][j]))
                grid_entries[i][j].config(state="disabled")

def start_timer(label):
    start_time = time.time()

    def update():
        elapsed_time = int(time.time() - start_time)
        minutes, seconds = divmod(elapsed_time, 60)
        label.config(text=f"Time: {minutes:02}:{seconds:02}")
        label.after(1000, update)

    update()

def solve_button_click(board, grid_entries):
    update_gui(board, grid_entries)

def hint_button_click(board, grid_entries):
    print("Hint clicked!")

def difficulty_selection(difficulty_var, board, grid_entries):
    print(f"Difficulty set to: {difficulty_var.get()}")

def on_cell_change(row, col, grid_entries, board):
    print(f"Cell ({row}, {col}) changed!")

if __name__ == "__main__":
    root = tk.Tk()
    create_start_screen(root)
    root.mainloop()