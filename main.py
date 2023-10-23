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

    sudoku = s.Sudoku(board)  # create a Sudoku object
    sudoku.solve()  # solve the board
    h.display(sudoku.board)  # display the board
