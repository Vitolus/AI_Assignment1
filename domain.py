import numpy as np
from itertools import product


def initialize_domain(board):
    domain = np.empty((9, 9), dtype=object)
    for i, j in np.ndindex(domain.shape):
        if board[i][j] == 0:  # if empty space
            domain[i][j] = (set(range(9)) - set(board[i, :]) - set(board[:, j]) -
                            set(board[i // 3 * 3:i // 3 * 3 + 3, j // 3 * 3:j // 3 * 3 + 3].ravel()))  # assign domain

        else:  # if not empty space
            domain[i][j] = {board[i][j]} # assign value

    return domain


def propagate_domain(board, domain, row, col, num, backtrack):  # update domain with constraint propagation
    if backtrack:  # if backtracking
        domain[row][col].add(num)  # add to domain
        for i in range(9):  # iterate through same row and column
            if board[i][col] == 0:  # if empty space
                domain[i][col].add(num)  # add to domain

            if board[row][i] == 0:  # if empty space
                domain[row][i].add(num)  # add to domain

        # iterate through same box
        for i, j in product(range(row // 3 * 3, row // 3 * 3 + 3), range(col // 3 * 3, col // 3 * 3 + 3)):
            if board[i][j] == 0:  # if empty space
                domain[i][j].add(num)  # add to domain

    else:  # if not backtracking
        domain[row][col] = {num}  # assign value
        for i in range(9):  # iterate through same row and column
            if board[i][col] == 0 and num in domain[i][col]:  # if empty space and num in domain
                domain[i][col].remove(num)  # remove from domain

            if board[row][i] == 0 and num in domain[row][i]:  # if empty space and num in domain
                domain[row][i].remove(num)  # remove from domain

        # iterate through same box
        for i, j in product(range(row // 3 * 3, row // 3 * 3 + 3), range(col // 3 * 3, col // 3 * 3 + 3)):
            if board[i][j] == 0 and num in domain[i][j]:  # if empty space and num in domain
                domain[i][j].remove(num)  # remove from domain

    return domain  # return updated domains
