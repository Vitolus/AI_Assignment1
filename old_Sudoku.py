import old_domain as dom
from itertools import product
import numpy as np
import time


class Sudoku:
    def __init__(self, board):
        self.board = board
        self.domain = dom.initialize_domain(board)
        self.exec_time = []

    def solve(self):  # solve sudoku using constraint propagation and backtracking
        start_time = time.time()  # start timer
        row, col = self.__find_empty()  # find empty space
        if row is None:  # if no empty spaces
            self.exec_time.append(time.time() - start_time)  # add execution time
            return True  # solved

        value = self.__least_constraining_value(row, col)  # find least constraining value
        self.board[row][col] = value  # assign value
        self.domain = dom.propagate_domain(self.board, self.domain, row, col, value, False)  # update domain
        if self.solve():  # if solved
            self.exec_time.append(time.time() - start_time)  # add execution time
            return True  # solved

        self.board[row][col] = 0  # backtrack value
        self.domain = dom.propagate_domain(self.board, self.domain, row, col, value, True)  # update domain
        self.exec_time.append(time.time() - start_time)  # add execution time
        return False

    def __least_constraining_value(self, row, col):  # least constraining value heuristic
        counts = [0] * 9  # initialize counts
        for num in self.domain[row][col]:  # iterate through domain
            self.board[row][col] = num  # assign temporary value
            for i in range(9):  # iterate through same row and column
                if self.board[i][col] == num:
                    counts[num - 1] += 1

                if self.board[row][i] == num:
                    counts[num - 1] += 1

            # iterate through same box
            for i, j in product(range(row // 3 * 3, row // 3 * 3 + 3), range(col // 3 * 3, col // 3 * 3 + 3)):
                if self.board[i][j] == num:
                    counts[num - 1] += 1

            self.board[row][col] = 0  # backtrack temporary value

        if sum(counts) == 0:
            return None

        min_count = min(count for count in counts if count > 0)  # find min count
        return counts.index(min_count) + 1  # return value of min count

    def __find_empty(self):  # find empty space
        for row, col in np.ndindex(self.board.shape):  # iterate through board
            if self.board[row][col] == 0:  # if empty space
                return row, col  # return row and col

        return None  # no empty spaces
