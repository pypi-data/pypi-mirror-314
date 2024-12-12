import random
import os

def initialize_grid(rows, cols):
    """Initialize the grid with random values."""
    return [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]

def display_grid(grid):
    """Display the grid in the terminal."""
    os.system('clear') 
    for row in grid:
        print(' '.join(['◼' if cell else ' ' for cell in row]))

def get_neighbors(grid, row, col):
    """Get the number of live neighbors for a cell."""
    rows, cols = len(grid), len(grid[0])
    neighbors = [
        (row-1, col-1), (row-1, col), (row-1, col+1),
        (row, col-1), (row, col+1),
        (row+1, col-1), (row+1, col), (row+1, col+1)
    ]
    count = 0
    for r, c in neighbors:
        if 0 <= r < rows and 0 <= c < cols:
            count += grid[r][c]
    return count

def update_grid(grid):
    """Update the grid based on the rules of the Game of Life."""
    rows, cols = len(grid), len(grid[0])
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for row in range(rows):
        for col in range(cols):
            live_neighbors = get_neighbors(grid, row, col)
            if grid[row][col] == 1:
                if live_neighbors == 2 or live_neighbors == 3:
                    new_grid[row][col] = 1
                else:
                    new_grid[row][col] = 0
            else:
                if live_neighbors == 3:
                    new_grid[row][col] = 1
    return new_grid

