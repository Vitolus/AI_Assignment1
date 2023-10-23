import helper as h


class Sudoku:
    def __init__(self, board):
        self.board = board
        self.units = ([h.cartesian_product(i, h.COLS) for i in h.ROWS] +  # row units
                      [h.cartesian_product(h.ROWS, j) for j in h.COLS] +  # column units
                      # cell units
                      [h.cartesian_product(i, j) for i in ['ABC', 'DEF', 'GHI'] for j in ['123', '456', '789']])
        # map each cell to its peers
        self.peer_dict = dict((cell,
                               set(sum(dict((cell,
                                             [unit for unit in self.units if cell in unit]) for cell in h.CELLS)[cell],
                                       [])) - {cell}) for cell in h.CELLS)

    def solve(self):  # solve the board
        self.__run_episode()  # run the elimination and only choice strategy
        if not self.board:  # if the board is empty
            return False  # board can't be solved

        if all(len(v) == 1 for v in self.board.values()):  # if all the cells have only one value
            return True  # board is solved

        k, values = min((k, v) for k, v in self.board.items() if len(v) > 1)  # get the cell with the least values
        for num in values:  # iterate over all the values
            new_board = self.board.copy()  # create a copy of the board
            new_board[k] = num  # assign the value to the cell
            if Sudoku(new_board).solve():  # if the board is solved
                return True  # board is solved

        return False  # board can't be solved

    def __eliminate(self):  # eliminate the values of solved cells from their peers
        for k, v in self.board.items():  # iterate over all the cells
            if len(v) != 1:  # if the cell has more than one value
                peers = self.peer_dict[k]  # get the peers of the cell
                peer_values = {self.board[p] for p in peers if len(self.board[p]) == 1}  # get the values of the peers
                self.board[k] = ''.join(set(v) - peer_values)  # remove the values of the peers from the cell

    def __only_choice(self):  # assign the value to the cell if it's the only choice
        for unit in self.units:  # iterate over all the units
            for num in h.COLS:  # iterate over all the numbers
                num_places = [cell for cell in unit if num in self.board[cell]]  # get all the cells with the number
                if len(num_places) == 1:  # if the number only appears once in the unit
                    self.board[num_places[0]] = num  # assign the value to the cell

    def __run_episode(self):  # run the elimination and only choice strategy
        while True:  # run until the board is solved or can't be solved
            solved_values_before = sum(len(v) == 1 for v in self.board.values())  # get the number of solved cells
            self.__eliminate()  # eliminate the values of solved cells from their peers
            self.__only_choice()  # assign the value to the cell if it's the only choice
            solved_values_after = sum(len(v) == 1 for v in self.board.values())  # get the number of solved cells
            if solved_values_before == solved_values_after:  # if the board can't be solved
                return False if any(len(v) == 0 for v in self.board.values()) else True  # return False if any cell has