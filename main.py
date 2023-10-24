import sudoku_propagation as sp
from itertools import product
import numpy as np
import matplotlib.pyplot as plt
import time

#START_BOARD = '53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79' # easy board
START_BOARD = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'  # hard board

if __name__ == '__main__':
    # create a dictionary of boxes and their values
    board = dict(zip([''.join(cell) for cell in product('ABCDEFGHI', '123456789')], START_BOARD))
    sudoku = sp.Sudoku()  # create a Sudoku object
    sudoku.display(board)  # display the unsolved board
    print('\n')  # print two new lines
    for k, v in board.items():  # replace all the '.' with all possible values
        if v == '.':  # if the cell is empty
            board[k] = '123456789'  # replace it with all possible values

    solved_board = sudoku.solve(board)  # solve the board
    sudoku.display(solved_board)  # display the solved board

    run = sudoku.exec_time  # get the time taken to solve the board
    print(sudoku.exec_time)  # print the time taken to solve the board
    total = []  # list to store the time taken to solve the board 100 times
    for i in range(100):  # solve the board 100 times
        start_time = time.perf_counter()  # get the start time
        sp.Sudoku().solve(board)  # solve the board
        # append the time taken to solve the board in milliseconds
        total.append((time.perf_counter() - start_time) * 1000)
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
