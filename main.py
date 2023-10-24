import sudoku_propagation as sp
from itertools import product
import numpy as np
import matplotlib.pyplot as plt
import time

START_BOARD = '53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79'

if __name__ == '__main__':
    # create a dictionary of boxes and their values
    board = dict(zip([''.join(cell) for cell in product('ABCDEFGHI', '123456789')], START_BOARD))
    sudoku = s.Sudoku(board)  # create a Sudoku object
    sudoku.display(board)  # display the board
    print('\n' * 2)  # add some space
    for k, v in board.items():  # replace all the '.' with all possible values
        if v == '.':  # if the cell is empty
            board[k] = '123456789'  # replace it with all possible values
    sudoku.solve()  # solve the board
    sudoku.display(sudoku.board)  # display the board
    run = sudoku.exec_time
    total = []
    for i in range(100):
        start_time = time.perf_counter()
        sp.Sudoku(board).solve()
        total.append((time.perf_counter() - start_time) * 1000)
    print(sudoku.exec_time)
    # plot the time taken to solve the board
    plt.figure()
    plt.plot(np.arange(1, len(run) + 1), run, label='time per episode')
    plt.title('Time taken to solve the board')
    plt.xlabel('episode iteration')
    plt.ylabel('time (microseconds)')
    plt.legend()
    plt.figure()
    plt.plot(np.arange(1, len(total) + 1), total, label='time per run')
    plt.plot(np.arange(1, len(total) + 1), [np.mean(total)] * len(total), label='mean')
    plt.title('Time taken to solve the board 100 times')
    plt.xlabel('run iteration')
    plt.ylabel('time (milliseconds)')
    plt.legend()
    plt.show()
