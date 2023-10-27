import sudoku_propagation as sp
import sudoku_annealing as sa
from itertools import product
import numpy as np
import matplotlib.pyplot as plt
import time

START_BOARD_EASY = '53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79'  # easy board
START_BOARD_HARD = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'  # hard board

if __name__ == '__main__':
    # create a dictionary of boxes and their values
    board_easy = dict(zip([''.join(cell) for cell in product('ABCDEFGHI', '123456789')], START_BOARD_EASY))
    board_hard = dict(zip([''.join(cell) for cell in product('ABCDEFGHI', '123456789')], START_BOARD_HARD))
    
    # Solve the easy board using constraint propagation
    sudoku_sp = sp.SudokuPropagation()  # create a Sudoku object
    print('Constraint propagation unsolved easy board\n')
    sudoku_sp.display(board_easy)  # display the unsolved board
    print('\n')
    for k, v in board_easy.items():  # replace all the '.' with all possible values
        if v == '.':  # if the cell is empty
            board_easy[k] = '123456789'  # replace it with all possible values
    solved_board = sudoku_sp.solve(board_easy)  # solve the board
    print('Constraint propagation solved easy board\n')
    sudoku_sp.display(solved_board)  # display the solved board
    print('\n')
    run_sp_easy = sudoku_sp.exec_time  # get the time taken to solve the board
    del run_sp_easy[0]
    print('Constraint propagation time taken to solve the easy board')
    print(run_sp_easy)  # print the time taken to solve the board
    
    # Solve the hard board using constraint propagation
    sudoku_sp = sp.SudokuPropagation()  # create a Sudoku object
    print('Constraint propagation unsolved hard board\n')
    sudoku_sp.display(board_hard)  # display the unsolved board
    print('\n')
    for k, v in board_hard.items():  # replace all the '.' with all possible values
        if v == '.':  # if the cell is empty
            board_hard[k] = '123456789'  # replace it with all possible values
    solved_board = sudoku_sp.solve(board_hard)  # solve the board
    print('Constraint propagation solved hard board\n')
    sudoku_sp.display(solved_board)  # display the solved board
    print('\n')
    run_sp_hard = sudoku_sp.exec_time  # get the time taken to solve the board
    del run_sp_hard[0]
    print('Constraint propagation time taken to solve the hard board')
    print(run_sp_hard)  # print the time taken to solve the board
            
    # Solve the easy board using simulated annealing
    sudoku_sa = sa.SudokuAnnealing(START_BOARD_EASY)  # create a Sudoku object
    print('Simulated annealing unsolved easy board with random values\n')
    sudoku_sa.display()  # display the unsolved board
    energies_easy = sudoku_sa.solve()  # solve the board
    print('Simulated annealing solved easy board\n')
    sudoku_sa.display()  # display the solved board
    print('Simulated annealing time taken to solve the easy board')
    run_sa_easy = sudoku_sa.exec_time  # get the time taken to solve the board
    del run_sa_easy[0]
    print(run_sa_easy)  # print the time taken to solve the board
    
    # Solve the hard board using simulated annealing
    sudoku_sa = sa.SudokuAnnealing(START_BOARD_HARD)  # create a Sudoku object
    print('Simulated annealing unsolved hard board with random values\n')
    sudoku_sa.display()  # display the unsolved board
    energies_hard = sudoku_sa.solve()  # solve the board
    print('Simulated annealing solved hard board\n')
    sudoku_sa.display()  # display the solved board
    print('Simulated annealing time taken to solve the hard board')
    run_sa_hard = sudoku_sa.exec_time  # get the time taken to solve the board
    del run_sa_hard[0]
    print(run_sa_hard)  # print the time taken to solve the board
    
    # plot the energy of the board
    plt.figure()
    plt.plot(energies_easy, label='energy_easy per epoch')
    plt.plot(energies_hard, label='energy_hard per epoch')
    plt.title('Energy of the board')
    plt.xlabel('epoch iteration')
    plt.ylabel('energy value')
    plt.legend()

    # plot the time taken to solve the board using constraint propagation
    plt.figure()
    plt.semilogy(np.arange(1, len(run_sp_easy) + 1), run_sp_easy, label='sp_easy cumulative time per epoch')
    plt.semilogy(np.arange(1, len(run_sp_hard) + 1), run_sp_hard, label='sp_hard cumulative time per epoch')
    plt.title('Time taken to solve the board')
    plt.xlabel('epoch iteration')
    plt.ylabel('time (seconds)')
    plt.legend()

    # plot the time taken to solve the board using simulated annealing
    plt.figure()
    plt.semilogy(np.arange(1, len(run_sa_easy) + 1), run_sa_easy, label='sa_easy cumulative time per epoch')
    plt.semilogy(np.arange(1, len(run_sa_hard) + 1), run_sa_hard, label='sa_hard cumulative time per epoch')
    plt.title('Time taken to solve the board')
    plt.xlabel('epoch iteration')
    plt.ylabel('time (seconds)')
    plt.legend()
    plt.show()
