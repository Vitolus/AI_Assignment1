import helper as h
import sudoku as s

START_BOARD = '53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79'

if __name__ == '__main__':
    board = dict(zip(h.CELLS, START_BOARD))  # create a dictionary of boxes and their values
    h.display(board)  # display the board
    print('\n' * 2)  # add some space
    for k, v in board.items():  # replace all the '.' with all possible values
        if v == '.':  # if the cell is empty
            board[k] = '123456789'  # replace it with all possible values

    # =======================================================================
    # Do all the testing and solving below this line
    # =======================================================================
    sudoku = s.Sudoku(board)
    sudoku.solve()
    # solved_grid = sudoku.eliminate()

    h.display(sudoku.board)
