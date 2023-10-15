import numpy as np
import time


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
            if board[i][j] == '.':
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve_sudoku(board):
                            return True
                        board[i][j] = '.'
                return False
        # print(board, sep='\n')
    return True


BOARD = np.array([[5, 3, '.', '.', 7, '.', '.', '.', '.'],
                  [6, '.', '.', 1, 9, 5, '.', '.', '.'],
                  ['.', 9, 8, '.', '.', '.', '.', 6, '.'],
                  [8, '.', '.', '.', 6, '.', '.', '.', 3],
                  [4, '.', '.', 8, '.', 3, '.', '.', 1],
                  [7, '.', '.', '.', 2, '.', '.', '.', 6],
                  ['.', 6, '.', '.', '.', '.', 2, 8, '.'],
                  ['.', '.', '.', 4, 1, 9, '.', '.', 5],
                  ['.', '.', '.', '.', 8, '.', '.', 7, 9]])

if __name__ == '__main__':
    t = np.empty([100])
    for j in range(100):
        start = time.time()
        solve_sudoku(BOARD)
        t[j] = time.time() - start
    print("execution time: {}".format(t.mean()))
