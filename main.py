import sudoku_propagation as sp
import sudoku_annealing as sa
from itertools import product
import numpy as np
import matplotlib.pyplot as plt
import time

START_BOARD = '53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79' # easy board
# START_BOARD = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'  # hard board

if __name__ == '__main__':
    # create a dictionary of boxes and their values
    board = dict(zip([''.join(cell) for cell in product('ABCDEFGHI', '123456789')], START_BOARD))
    sudoku_sp = sp.SudokuPropagation()  # create a Sudoku object
    print('Constraint propagation unsolved board\n')
    sudoku_sp.display(board)  # display the unsolved board
    print('\n')
    for k, v in board.items():  # replace all the '.' with all possible values
        if v == '.':  # if the cell is empty
            board[k] = '123456789'  # replace it with all possible values

    solved_board = sudoku_sp.solve(board)  # solve the board
    print('Constraint propagation solved board\n')
    sudoku_sp.display(solved_board)  # display the solved board
    print('\n')
    run_sp = sudoku_sp.exec_time  # get the time taken to solve the board
    print('Constraint propagation time taken to solve the board')
    print(run_sp)  # print the time taken to solve the board
    total = []  # list to store the time taken to solve the board 100 times
    for i in range(100):  # solve the board 100 times
        start_time = time.perf_counter()  # get the start time
        sp.SudokuPropagation().solve(board)  # solve the board
        # append the time taken to solve the board in milliseconds
        total.append((time.perf_counter() - start_time) * 1000)

    #TODO: add annealing 100 times and plot the time taken to solve the board 100 times

    sudoku_sa = sa.SudokuAnnealing(START_BOARD)  # create a Sudoku object
    print('Simulated annealing unsolved board with random values\n')
    sudoku_sa.display()  # display the unsolved board
    energies = sudoku_sa.solve()  # solve the board
    print('Simulated annealing solved board\n')
    sudoku_sa.display()  # display the solved board
    print('Simulated annealing time taken to solve the board')
    run_sa = sudoku_sa.exec_time  # get the time taken to solve the board
    print(run_sa)  # print the time taken to solve the board

    # plot the energy of the board
    plt.figure()
    plt.plot(energies, label='energy per epoch')
    plt.title('Energy of the board')
    plt.xlabel('epoch iteration')
    plt.ylabel('energy value')
    plt.legend()

    # plot the time taken to solve the board
    plt.figure()
    plt.plot(np.arange(1, len(run_sp) + 1), run_sp, label='sp time per epoch')
    plt.title('Time taken to solve the board')
    plt.xlabel('epoch iteration')
    plt.ylabel('time (microseconds)')
    plt.legend()

    # plot the time taken to solve the board
    plt.figure()
    plt.plot(np.arange(1, len(run_sa) + 1), run_sa, label='sa time per epoch')
    plt.title('Time taken to solve the board')
    plt.xlabel('epoch iteration')
    plt.ylabel('time (microseconds)')
    plt.legend()

    # plot the time taken to solve the board 100 times
    plt.figure()
    plt.plot(np.arange(1, len(total) + 1), total, label='time per run')
    plt.plot(np.arange(1, len(total) + 1), [np.mean(total)] * len(total), label='mean')
    plt.title('Time taken to solve the board 100 times')
    plt.xlabel('run iteration')
    plt.ylabel('time (milliseconds)')
    plt.legend()
    plt.show()
