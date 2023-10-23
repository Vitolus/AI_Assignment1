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

        if all(len(v) == 1 for k, v in self.board.items()):  # if all the cells have only one value
            return True  # board is solved

        # get the cell with the least number of possible values
        length, k = min((len(val), key) for key, val in self.board.items() if len(val) > 1)
        for num in self.board[k]:  # iterate over all the possible values of the cell
            new_board = dict(list(self.board.items()))  # create a new board
            new_board[k] = num  # assign the value to the cell
            try_to_solve_new_config = Sudoku(new_board).solve()  # try to solve the new board
            if try_to_solve_new_config:  # if the new board is solved
                return True  # board is solved

        return False  # board can't be solved

    def __eliminate(self):  # eliminate the values from the peers
        for k, v in self.board.items():  # iterate over all the cells
            if len(v) != 1:  # if the cell needs elimination
                peers = self.peer_dict[k]  # get all the peers
                # get all the values of the peers
                peer_values = set([self.board[p] for p in peers if len(self.board[p]) == 1]) 
                self.board[k] = ''.join(set(self.board[k]) - peer_values)  # remove the peer values from the cell

    def __only_choice(self):  # assign the value to the cell if it's the only choice
        for unit in self.units:  # iterate over all the units
            for num in h.COLS:  # iterate over all the numbers
                num_places = [cell for cell in unit if num in self.board[cell]]  # get all the cells with the number
                if len(num_places) == 1:  # if the number only appears once in the unit
                    self.board[num_places[0]] = num  # assign the value to the cell

    def __run_episode(self):  # run the elimination and only choice strategy
        stuck = False
        while not stuck:  # while we're not stuck
            # count the number of solved cells
            solved_values_before = len([cell for cell in self.board.keys() if len(self.board[cell]) == 1])
            self.__eliminate()  # elimination strategy
            self.__only_choice()  # only choice strategy
            # count the number of solved cells
            solved_values_after = len([cell for cell in self.board.keys() if len(self.board[cell]) == 1])
            stuck = solved_values_before == solved_values_after  # we're stuck if we didn't solve any new cells
            if len([cell for cell in self.board.keys() if len(self.board[cell]) == 0]):  # if any cell has no value
                return False  # board can't be solved
