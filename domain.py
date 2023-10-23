import numpy as np


def initialize_domain(board):  # initialize domain
    domain = np.full((9, 9, 9), np.array(range(1, 10)), dtype=object)  # 9x9x9 array of 1-9
    for row, col in np.ndindex(board.shape):  # iterate through board
        if board[row][col] == 0:  # if empty space
            domain = remove_domain_value(board, domain, row, col)  # remove from domain

        else:  # if not empty space
            domain[row][col] = [board[row][col]]  # assign value
    return domain  # return domain


def remove_domain_value(board, domain, row, col):  # remove from domain
    row_start = row // 3 * 3  # find start of box
    col_start = col // 3 * 3  # find start of box
    for i in range(9):  # iterate through board
        if board[row][i] != 0:  # if not empty space
            # remove from domain
            domain[row][col] = np.delete(domain[row][col], np.where(domain[row][col] == board[row][i]))
        if board[i][col] != 0:  # if not empty space
            # remove from domain
            domain[row][col] = np.delete(domain[row][col], np.where(domain[row][col] == board[i][col]))

    for i in range(row_start, row_start + 3):  # iterate through box
        for j in range(col_start, col_start + 3):  # iterate through box
            if board[i][j] != 0:  # if not empty space
                domain[row][col] = np.delete(domain[row][col],
                                             np.where(domain[row][col] == board[i][j]))  # remove from domain
    return domain  # return domain


# TODO: sistemare funzione, non funziona correttamente
def prune_domain(board, domain, row, col, num, backtrack):  # update domain with constraint propagation
    if backtrack:  # if backtracking
        domain[row][col] = np.append(domain[row][col], num)  # add to domain
        domain[row][col] = np.sort(domain[row][col])  # sort domain
    else:  # if not backtracking
        domain[row][col] = np.array([num])  # assign value
    domain = remove_domain_value(board, domain, row, col)  # remove from domain
    return domain  # return domain
