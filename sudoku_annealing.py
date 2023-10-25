import time
import numpy as np

# TODO: implement the remaining methods to solve
class SudokuAnnealing:
    def __init__(self, board):
        # convert the board to a numpy array
        self.board = np.array(list(board.replace('.', '0'))).reshape(9, 9).astype(int)
        mask = (self.board == 0)  # get the mask of the cells with no value
        self._guesses = np.argwhere(mask)  # get the indices of the cells with randomly guessed values
        self.board[mask] = np.random.randint(1, 10, size=np.count_nonzero(mask))  # assign random values to the cells
        self._energy = self._global_energy()  # get the global energy of the board
        self._beta = 1e4  # set cooling rate

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
        for row, col in [(i, j) for i in range(9) for j in range(9)]:  # iterate over all the cells
            energy += self._local_energy(row, col)  # add the local energy of the cell
        return energy  # return the energy

    def _annealing(self):
        row, col = self._guesses[np.random.randint(0, len(self._guesses))]  # get a random cell
        old_energy = self._local_energy(row, col)  # get the local energy of the cell
        old_value = self.board[row, col]  # get the old value of the cell
        self.board[row, col] = np.random.randint(1, 10)  # assign a random value to the cell
        new_energy = self._local_energy(row, col)  # get the new local energy of the cell
        delta_energy = new_energy - old_energy  # get the change in energy
        # if the change in energy is negative or the probability is less than the threshold
        if delta_energy < 0 or np.random.rand() < np.exp(-self._beta * delta_energy):
            self._energy += delta_energy  # update the global energy
            return
        else:
            self.board[row, col] = old_value


if __name__ == '__main__':
    sudoku = SudokuAnnealing('53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79')
    print(sudoku.board)

