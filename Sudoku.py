import tkinter as tk
from tkinter import messagebox
import random

# Grid size for Sudoku (9x9)
GRID_SIZE = 9

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver with Pre-filled Grid")

        # Create a 9x9 grid to represent the Sudoku puzzle
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.entries = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]

        # Pre-fill the grid with some random numbers
        self.prefill_grid()

        # Create the grid layout of Entry widgets
        self.create_grid()

        # Create control buttons
        solve_button = tk.Button(self.root, text="Solve", command=self.solve, bg="lightgreen")
        solve_button.grid(row=GRID_SIZE, column=0, columnspan=4, sticky="nsew")

        clear_button = tk.Button(self.root, text="Clear", command=self.clear_grid, bg="lightcoral")
        clear_button.grid(row=GRID_SIZE, column=5, columnspan=4, sticky="nsew")

    def create_grid(self):
        """Create a 9x9 grid of entry widgets for Sudoku input."""
        colors = ["lightyellow", "lightblue"]
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                color = colors[(row // 3 + col // 3) % 2]  # Alternate colors for 3x3 blocks
                entry = tk.Entry(self.root, width=3, justify='center', bg=color, font=("Arial", 16))
                entry.grid(row=row, column=col, padx=2, pady=2, ipady=5)
                self.entries[row][col] = entry
                if self.grid[row][col] != 0:
                    entry.insert(0, str(self.grid[row][col]))
                    entry.config(state='disabled')  # Disable pre-filled cells to avoid modification

    def prefill_grid(self):
        """Prefill the grid with some random numbers."""
        # A valid random preset for testing (could be changed or randomized)
        preset_grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        self.grid = preset_grid

    def get_grid_values(self):
        """Get the current values from the entry widgets."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.entries[row][col]['state'] != 'disabled':  # Ignore pre-filled cells
                    value = self.entries[row][col].get()
                    if value.isdigit():
                        self.grid[row][col] = int(value)
                    else:
                        self.grid[row][col] = 0

    def is_valid(self, row, col, num):
        """Check if placing the number is valid in the grid."""
        for i in range(GRID_SIZE):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False

        start_row, start_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == num:
                    return False

        return True

    def solve_sudoku(self):
        """Solve the Sudoku puzzle using backtracking."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(row, col, num):
                            self.grid[row][col] = num
                            if self.solve_sudoku():
                                return True
                            self.grid[row][col] = 0
                    return False
        return True

    def solve(self):
        """Solve button handler."""
        self.get_grid_values()  # Get input from the GUI grid
        if self.solve_sudoku():
            self.update_grid()  # Update the GUI grid with the solution
        else:
            messagebox.showerror("Error", "No solution exists for the given Sudoku puzzle.")

    def update_grid(self):
        """Update the GUI grid with the solved Sudoku values."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.entries[row][col]['state'] != 'disabled':  # Ignore pre-filled cells
                    self.entries[row][col].delete(0, tk.END)
                    self.entries[row][col].insert(0, str(self.grid[row][col]))
                    self.entries[row][col].config(fg="blue")  # Color the solution numbers in blue

    def clear_grid(self):
        """Clear the Sudoku grid for new input."""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.entries[row][col]['state'] != 'disabled':  # Ignore pre-filled cells
                    self.entries[row][col].delete(0, tk.END)
                    self.entries[row][col].config(fg="black")  # Reset text color to black
                    self.grid[row][col] = 0

# Create the main window
root = tk.Tk()
sudoku_gui = SudokuGUI(root)

# Start the GUI event loop
root.mainloop()
