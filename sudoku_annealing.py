import time
import numpy as np
from itertools import repeat, product


class SudokuAnnealing:
    def __init__(self, board):
        self.exec_time = [0.]  # list to store the time taken to solve the board
        # convert the board to a numpy array
        self.board = np.array(list(board.replace('.', '0'))).reshape(9, 9).astype(int)
        print('Simulated annealing unsolved board\n')
        self.display()
        mask = (self.board == 0)  # get the mask of the cells with no value
        self._guesses = np.argwhere(mask)  # get the indices of the cells with randomly guessed values
        self.board[mask] = np.random.randint(1, 10, size=np.count_nonzero(mask))  # assign random values to the cells
        self._energy = self._global_energy()  # get the global energy of the board
        self._temperature = 0.25  # initialize the inverse temperature
        self._cooling_rate = 2e-2  # initialize the cooling rate

    def solve(self):
        energies = []  # list to store the energy
        while self._temperature < 1e2:  # while the temperature is less than 1e2 run epoch
            start_time = time.perf_counter()  # get the start time
            for _ in repeat(None, 1000):  # repeat 1000 times
                self._metropolis()  # run the metropolis algorithm
            # append the time taken to solve the board
            self.exec_time.append((time.perf_counter() + self.exec_time[-1] - start_time))
            energies.append(self._energy)  # append the energy
            if self._energy <= 0:  # if the energy is zero
                break  # break the loop
            self._temperature *= (1.0 + self._cooling_rate)  # cool the system
        return energies  # return the energy

    def _local_energy(self, row, col):  # calculate the local energy of the cell
        energy = 0  # initialize the energy
        # get the row, column and box of the cell
        for i in [self.board[row, :],
                  self.board[:, col],
                  self.board[(row // 3) * 3:(row // 3 + 1) * 3,
                  (col // 3) * 3:(col // 3 + 1) * 3].flatten()]:
            occ = np.bincount(i)  # get the number of occurrences of each number
            energy += np.sum(occ[occ > 1])  # add the number of occurrences of each number that appears more than once
        return energy  # return the energy

    def _global_energy(self):  # calculate the global energy of the board
        energy = 0  # initialize the energy
        for row, col in product(range(9), repeat=2):
            energy += self._local_energy(row, col)  # add the local energy of the cell
        return energy  # return the energy

    def _metropolis(self):
        row, col = self._guesses[np.random.randint(0, len(self._guesses))]  # get a random cell
        old_energy = self._local_energy(row, col)  # get the local energy of the cell
        old_value = self.board[row, col]  # get the old value of the cell
        self.board[row, col] = np.random.randint(1, 10)  # assign a random value to the cell
        delta_energy = self._local_energy(row, col) - old_energy  # get the change in energy
        # if the change in energy is negative or the probability is less than the threshold
        if delta_energy < 0 or np.random.rand() < np.exp(-self._temperature * delta_energy):
            self._energy += delta_energy  # update the global energy
            return
        else:
            self.board[row, col] = old_value  # revert the change

    def display(self):
        for i in range(len(self.board)):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - - ")
            for j in range(len(self.board[0])):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                if j == 8:
                    print(self.board[i][j])
                else:
                    print(str(self.board[i][j]) + " ", end="")
        print('\n')
