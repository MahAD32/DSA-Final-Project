import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageFilter
import time
import random
from sudoku_algorithms import generate_sudoku, solve_sudoku_with_dfs, is_valid

def apply_blur(image_path):
    image = Image.open(image_path)
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=8))
    return ImageTk.PhotoImage(blurred_image)

def update_gui(board, grid_entries):
    for row in range(9):
        for col in range(9):
            value = board[row][col]
            grid_entries[row][col].delete(0, tk.END)
            if value != 0:
                grid_entries[row][col].insert(0, str(value))
                grid_entries[row][col].config(state="disabled", disabledforeground="black", bg="#f0f0f0")
            else:
                grid_entries[row][col].config(state="normal", bg="white", highlightbackground="black")

def solve_button_click(board, grid_entries, game_over_callback):
    if solve_sudoku_with_dfs(board):
        update_gui(board, grid_entries)
    else:
        print("No solution exists!")
    game_over_callback()

def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None, None

def hint_button_click(board, grid_entries, hint_count):
    if hint_count["used"] >= hint_count["max"]:
        return

    empty_cells = [(row, col) for row in range(9) for col in range(9) if board[row][col] == 0 and grid_entries[row][col].get() == ""]

    if not empty_cells:
        return

    for row, col in empty_cells:
        for num in range(1, 10):
            if is_valid(board, row, col, num):
                board[row][col] = num
                grid_entries[row][col].delete(0, tk.END)
                grid_entries[row][col].insert(0, str(num))
                grid_entries[row][col].config(bg="lightblue", font=("Arial", 18, "bold"))
                grid_entries[row][col].after(300, lambda: grid_entries[row][col].config(bg="white"))
                hint_count["used"] += 1
                return

def start_timer(timer_label):
    start_time = time.time()

    def update_time():
        elapsed_time = int(time.time() - start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_label.config(text=f"Time: {minutes:02}:{seconds:02}")
        timer_label.after(1000, update_time)

    update_time()

def validate_input(board, grid_entries, row, col, event):
    value = event.widget.get().strip() 
    if value == "":
        event.widget.config(bg="white")
        board[row][col] = 0 
        return
    try:
        num_value = int(value)
        if 1 <= num_value <= 9 and is_valid(board, row, col, num_value):
            event.widget.config(bg="white")  
            board[row][col] = num_value 
        else:
            event.widget.config(bg="red")  
    except ValueError:
        event.widget.config(bg="red")


def game_over_callback(root, start_screen_bg, start_time):
    elapsed_time = int(time.time() - start_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    time_str = f"{minutes:02}:{seconds:02}"

    root.after(5000, root.withdraw)
    
    root.after(5000, lambda: create_game_over_screen(root, start_screen_bg, time_str))

def create_game_over_screen(root, background_image, time_str):
    game_over_window = tk.Toplevel(root)
    game_over_window.geometry("800x700")
    game_over_window.config(bg="#f3f3f3")
    bg_label = tk.Label(game_over_window, image=background_image)
    bg_label.place(relwidth=1, relheight=1)
    game_over_label = tk.Label(game_over_window, text="GAME OVER", font=("Arial", 48, "bold"), bg="#FFDAC0", fg="red")
    game_over_label.place(relx=0.5, rely=0.4, anchor="center")

    time_label = tk.Label(game_over_window, text=f"Time: {time_str}", font=("Arial", 24), bg="#FFDAC0")
    time_label.place(relx=0.5, rely=0.5, anchor="center")

    restart_button = tk.Button(game_over_window, text="Restart", font=("Arial", 16), command=lambda: restart_game(root, background_image), relief="raised", bg="#FFDAC0", fg="white")
    restart_button.place(relx=0.5, rely=0.6, anchor="center")

    close_button = tk.Button(game_over_window, text="Exit", font=("Arial", 16), command=root.quit, relief="raised", bg="#FFDAC0", fg="white")
    close_button.place(relx=0.5, rely=0.7, anchor="center")

def restart_game(root, background_image):
    root.withdraw()
    start_game(root, "medium", background_image)
    root.deiconify()

def check_game_completion(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return False
    return True

def create_sudoku_gui(root, difficulty, background_image):
    root.title("Sudoku Game")
    root.geometry("800x700")
    root.config(bg="#f3f3f3")

    bg_label = tk.Label(root, image=background_image)
    bg_label.place(relwidth=1, relheight=1)

    frame = tk.Frame(root, bg="#FFDAC0", bd=10)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    grid_entries = []
    for i in range(9):
        row_entries = []
        for j in range(9):
            entry = tk.Entry(frame, width=5, font=("Arial", 18), justify="center", bd=3, relief="solid", highlightbackground="gray")
            entry.grid(row=i, column=j, padx=5, pady=5)

            # Bind to KeyRelease to validate input as soon as the user types
            entry.bind("<KeyRelease>", lambda event, row=i, col=j: validate_input(board, grid_entries, row, col, event))

            row_entries.append(entry)
        grid_entries.append(row_entries)

    board = generate_sudoku(difficulty)
    update_gui(board, grid_entries)

    timer_label = tk.Label(root, text="Time: 00:00", font=("Arial", 16), bg="#f3f3f3")
    timer_label.place(x=20, y=650)
    start_time = time.time()
    start_timer(timer_label)

    hint_count = {"used": 0, "max": 3}

    solve_button = tk.Button(root, text="Solve", command=lambda: solve_button_click(board, grid_entries, lambda: game_over_callback(root, start_screen_bg, start_time)), font=("Arial", 16), relief="raised", bg="#FFDAC0", fg="white")
    solve_button.place(x=20, y=600)

    hint_button = tk.Button(root, text="Hint", command=lambda: hint_button_click(board, grid_entries, hint_count), font=("Arial", 16), relief="raised", bg="#FFDAC0", fg="white")
    hint_button.place(x=100, y=600)

    difficulty_button = tk.Button(root, text="Restart", command=lambda: update_gui(generate_sudoku(difficulty), grid_entries), font=("Arial", 16), relief="raised", bg="#FFDAC0", fg="white")
    difficulty_button.place(x=200, y=600)

    def on_click(event):
        if check_game_completion(board):
            game_over_callback(root, start_screen_bg, start_time)

    root.bind("<Button-1>", on_click)

def create_start_screen(root, background_image):
    root.title("Sudoku Game Start Screen")
    root.geometry("800x600")
    root.config(bg="#f3f3f3")

    bg_label = tk.Label(root, image=background_image)
    bg_label.place(relwidth=1, relheight=1)

    title_label = tk.Label(root, text="Sudoku", font=("Arial", 24, "bold"), pady=30, padx=1000, bg="#FFDAC0")
    title_label.pack(pady=50, anchor="center")

    difficulty_label = tk.Label(root, text="Select Difficulty:", font=("Arial", 16), bg="#FFDAC0")
    difficulty_label.pack(pady=10, anchor="center")

    difficulty_var = tk.StringVar(value="medium")
    difficulty_menu = tk.OptionMenu(root, difficulty_var, "easy", "medium", "hard")
    difficulty_menu.config(font=("Arial", 14), width=15)
    difficulty_menu.pack(pady=10, anchor="center")

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 16), relief="flat", padding=10, background="#4CAF50", foreground="white", width=15)

    start_button = ttk.Button(root, text="Start Game", style="TButton", command=lambda: start_game(root, difficulty_var.get(), background_image))
    start_button.pack(pady=20, anchor="center")
    start_button.bind("<Enter>", lambda e: style.configure("TButton", background="#45a049"))
    start_button.bind("<Leave>", lambda e: style.configure("TButton", background="#4CAF50"))

def start_game(root, difficulty, background_image):
    for widget in root.winfo_children():
        widget.destroy()
    create_sudoku_gui(root, difficulty, background_image)

if __name__ == "__main__":
    root = tk.Tk()
    start_screen_bg = apply_blur(r"C:\\MinGW\\cd11f2b0d69f60c99e2181c07e1fd4ec-mitchell (1).jpg")
    create_start_screen(root, start_screen_bg)
    root.mainloop()
