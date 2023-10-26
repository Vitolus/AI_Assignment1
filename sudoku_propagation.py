import time


def cartesian_product(a, b):  # get the cartesian product of two strings
    return [i + j for i in a for j in b]


class SudokuPropagation:
    def __init__(self):
        self._ROWS = 'ABCDEFGHI'  # all the rows
        self._COLS = '123456789'  # all the columns
        self._CELLS = cartesian_product(self._ROWS, self._COLS)  # all the cells
        self.exec_time = []  # list to store the time taken to solve the board
        row_u = [cartesian_product(row, self._COLS) for row in self._ROWS]  # row units
        col_u = [cartesian_product(self._ROWS, col) for col in self._COLS]  # column units
        # cell units
        cell_u = [cartesian_product(row, col) for row in ('ABC', 'DEF', 'GHI') for col in ('123', '456', '789')]
        self._units = row_u + col_u + cell_u  # all the units
        # map each cell to its units
        units = dict((cell, [unit for unit in self._units if cell in unit]) for cell in self._CELLS)
        # map each cell to its peers
        self._peers = dict((cell, set(sum(units[cell], [])) - {cell}) for cell in self._CELLS)

    def solve(self, board):  # solve the board
        board = self._run_epoch(board)  # run the elimination and only choice strategy
        if board is False:  # if the board is unsolvable
            return False  # return False

        if all(len(v) == 1 for v in board.values()):  # if all the cells have only one value
            return board  # board is solved

        length, k = min((len(v), k) for k, v in board.items() if len(v) > 1)  # get the cell with the least values
        for num in board[k]:  # iterate over all the values
            new_board = board.copy()  # create a copy of the board
            new_board[k] = num  # assign the value to the cell
            new_board = self.solve(new_board)  # solve the board
            if new_board:  # if the board is solved
                return new_board  # return the solved board

    def _constraint_propagation(self, board):  # eliminate the values of solved cells from their peers
        for k, v in board.items():  # iterate over all the cells
            if len(v) != 1:  # if the cell has more than one value
                peers_k = self._peers[k]  # get the peers of the cell k
                peer_v = set(board[peer] for peer in peers_k if len(board[peer]) == 1)  # get the values of the peers
                board[k] = ''.join(set(board[k]) - peer_v)  # remove the values of the peers from the cell
        return board

    def _set_value(self, board):  # assign the value to the cell if it's the only choice
        for unit in self._units:  # iterate over all the units
            for num in self._COLS:  # iterate over all the numbers
                cells_num = [cell for cell in unit if num in board[cell]]  # get all the cells with the number
                if len(cells_num) == 1:  # if the number only appears once in the unit
                    board[cells_num[0]] = num  # assign the value to the cell
        return board

    def _run_epoch(self, board):  # run the constraint propagation and only choice strategy
        changed = True  # flag to indicate if the board has changed
        while changed:  # while the board has changed
            before_count = sum(len(v) == 1 for v in board.values())  # get the number of solved cells
            start_time = time.perf_counter()  # get the start time
            board = self._constraint_propagation(board)  # eliminate the values of solved cells from their peers
            board = self._set_value(board)  # assign the value to the cell if it's the only choice
            self.exec_time.append((time.perf_counter() - start_time) * 100000)  
            after_count = sum(len(v) == 1 for v in board.values())  # get the number of solved cells
            changed = before_count != after_count  # check if the number of solved cells has changed
            if any(len(v) == 0 for v in board.values()):  # if any cell has no value
                return False
        return board

    def display(self, values):  # display the board
        width = max(len(values[s]) for s in self._CELLS) + 1  # get the width of the cell
        line = '+'.join(['-' * (width * 3)] * 3)  # create a line
        for r in self._ROWS:  # iterate over all the rows
            # print the values of the cells in the row
            print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in self._COLS))
            if r in 'CF':  # if the row is C or F
                print(line)  # print the line
        return
