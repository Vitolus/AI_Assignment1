from itertools import product
import time


class Sudoku:
    def __init__(self, board):
        self._ROWS = 'ABCDEFGHI'  # all the rows
        self._COLS = '123456789'  # all the columns
        self._CELLS = [''.join(cell) for cell in product(self._ROWS, self._COLS)]  # all the cells
        self.board = board
        self.exec_time = [] # list to store the time taken to solve the board
        self.units = ([[''.join(p) for p in product(i, self._COLS)] for i in self._ROWS] +  # row units
                      [[''.join(p) for p in product(self._ROWS, j)] for j in self._COLS] +  # column units
                      # cell units
                      [[''.join(p) for p in product(i, j)] for i in ['ABC', 'DEF', 'GHI']
                       for j in ['123', '456', '789']])
        # map each cell to its peers
        self.peer_dict = dict(
            (cell, set(sum(dict(
                (cell, [unit for unit in self.units if cell in unit]) for cell in self._CELLS)[cell], []))
             - {cell}) for cell in self._CELLS)

    def solve(self):  # solve the board
        self.__run_episode()  # run the elimination and only choice strategy
        if all(len(v) == 1 for v in self.board.values()):  # if all the cells have only one value
            return True  # board is solved

        k, values = min((k, v) for k, v in self.board.items() if len(v) > 1)  # get the cell with the least values
        for num in values:  # iterate over all the values
            new_board = self.board.copy()  # create a copy of the board
            new_board[k] = num  # assign the value to the cell
            if Sudoku(new_board).solve():  # if the board is solved
                return True  # board is solved
        return False  # board can't be solved

    def __constraint_propagation(self):  # eliminate the values of solved cells from their peers
        for k, v in self.board.items():  # iterate over all the cells
            if len(v) != 1:  # if the cell has more than one value
                peers = self.peer_dict[k]  # get the peers of the cell
                peer_values = {self.board[p] for p in peers if len(self.board[p]) == 1}  # get the values of the peers
                self.board[k] = ''.join(set(v) - peer_values)  # remove the values of the peers from the cell

    def __set_value(self):  # assign the value to the cell if it's the only choice
        for unit in self.units:  # iterate over all the units
            for num in self._COLS:  # iterate over all the numbers
                num_places = [cell for cell in unit if num in self.board[cell]]  # get all the cells with the number
                if len(num_places) == 1:  # if the number only appears once in the unit
                    self.board[num_places[0]] = num  # assign the value to the cell

    def __run_episode(self):  # run the constraint propagation and only choice strategy
        while True:  # run until the board is solved or can't be solved
            start_time = time.perf_counter()  # get the start time
            solved_values_before = sum(len(v) == 1 for v in self.board.values())  # get the number of solved cells
            self.__constraint_propagation()  # eliminate the values of solved cells from their peers
            self.__set_value()  # assign the value to the cell if it's the only choice
            solved_values_after = sum(len(v) == 1 for v in self.board.values())  # get the number of solved cells
            # append the time taken to solve the board in microseoconds
            self.exec_time.append((time.perf_counter() - start_time) * 100000)
            if solved_values_before == solved_values_after:  # if the number of solved cells hasn't changed
                # return False if any cell has no value and True otherwise
                return False if any(len(v) == 0 for v in self.board.values()) else True 

    def display(self, values):  # display the board
        width = max(len(values[s]) for s in self._CELLS) + 1  # get the width of the cell
        line = '+'.join(['-' * (width * 3)] * 3)  # create a line
        for r in self._ROWS:  # iterate over all the rows
            print(
                ''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in self._COLS))  # print the row 
            if r in 'CF':  # if the row is C or F
                print(line)  # print the line
