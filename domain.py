import numpy as np

domain = np.full((9, 9, 9), np.array(range(1, 10)), dtype=object)


def initialize_domain(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                remove_dim_domain(board, i, j)
                remove_box_domain(board, i, j)
            else:
                domain[i][j] = [board[i][j]]
    return domain


def remove_dim_domain(board, row, col):
    for i in range(9):
        if board[row][i] != 0:
            domain[row][col] = np.delete(domain[row][col], np.where(domain[row][col] == board[row][i]))
        if board[i][col] != 0:
            domain[row][col] = np.delete(domain[row][col], np.where(domain[row][col] == board[i][col]))
    return domain


def remove_box_domain(board, row, col):
    row_start = row // 3 * 3
    col_start = col // 3 * 3
    for i in range(row_start, row_start + 3):
        for j in range(col_start, col_start + 3):
            if board[i][j] != 0:
                domain[row][col] = np.delete(domain[row][col], np.where(domain[row][col] == board[i][j]))
    return domain
