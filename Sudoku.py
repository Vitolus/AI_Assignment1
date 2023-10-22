import domain as dom
from itertools import product


class Sudoku:
    def __init__(self, board):
        self.board = board
        self.domain = dom.initialize_domain(board)

    def solve(self):  # solve sudoku using constraint propagation and backtracking
        row, col = self.__find_empty()  # find empty space
        if row is None:  # if no empty spaces
            return True  # solved

        value = self.__least_constraining_value(row, col)  # find least constraining value
        self.board[row][col] = value  # assign value
        self.domain = dom.update_domain(self.board, self.domain, row, col, value, False)  # update domain
        if self.solve():  # if solved
            return True
        self.board[row][col] = 0  # backtrack value
        self.domain = dom.update_domain(self.board, self.domain, row, col, value, True)  # update domain
        return False

    def __least_constraining_value(self, row, col):  # least constraining value heuristic
        counts = [0] * 9  # initialize counts
        for num in self.domain[row][col]:  # iterate through domain
            self.board[row][col] = num  # assign temporary value
            for i in range(9):  # iterate through board
                for j in range(9):  # iterate through board
                    if (i == row or j == col or
                            (i // 3 == row // 3 and j // 3 == col // 3)):  # if in same row, col, or box
                        if self.board[i][j] == num:  # if same value
                            counts[num - 1] += 1  # increment count
            self.board[row][col] = 0  # backtrack temporary value
        min_count = min(count for count in counts if count > 0)  # find min count
        return counts.index(min_count) + 1  # return value of min count

    def __find_empty(self):  # find empty space
        for row, col in product(range(9), repeat=2):  # iterate through board
            if self.board[row][col] == 0:  # if empty space
                return row, col  # return row and col
        return None  # no empty spaces

    def __is_valid(self, num, row, col):  # check if valid
        if num not in self.domain[row][col]:  # check if in domain
            return False  # not valid
        return True  # valid
