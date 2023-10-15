```
def is_valid(board, row, col, num):
    # Check the number in the row
    for x in range(9):
        if board[row][x] == num:
            return False

    # Check the number in the column
    for x in range(9):
        if board[x][col] == num:
            return False

    # Check the number in the box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

def solve_sudoku(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve_sudoku(board):
                            return True
                        board[i][j] = 0
                return False
    return True
```
This code first checks if the current board configuration is valid. If it is, it recursively attempts to fill the board
using numbers 1-9. If it cannot place a number without violating the Sudoku rules, it backtracks and tries a different
number.

1. Initialize all domains: For each empty cell in the Sudoku grid, create a domain of all possible values (1-9).

2. Constraint propagation: For each newly assigned cell, remove its value from the domain of all unassigned cells in the
   same row, column, and box.

3. Backtracking: Just like in the previous code, attempt to assign a value to an unassigned cell. However, now you only
   need to check the values in its domain. If no assignment leads to a solution, backtrack.

4. Repeat: Continue this process until the Sudoku is solved or until it’s proven that no solution exists.