def cartesian_product(x, y):  # cartesian product of x and y
    return [a + b for a in x for b in y]  # return the cartesian product of x and y


ROWS = 'ABCDEFGHI'  # rows of the board
COLS = '123456789'  # columns of the board
CELLS = cartesian_product(ROWS, COLS)  # all the cells of the board


def display(values):  # display the board
    print('')  # add some space
    width = max(len(values[s]) for s in CELLS) + 1  # find the width of the cell with the most values
    line = '+'.join(['-' * (width * 3)] * 3)  # create a line to separate the boxes
    for r in ROWS:  # iterate over all the rows
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in COLS))  # print the row
        if r in 'CF':  # if the row is C or F
            print(line)  # print the line
