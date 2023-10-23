import helper as h


units = ([h.cartesian_product(r, h.COLS) for r in h.ROWS] +  # row units
         [h.cartesian_product(h.ROWS, c) for c in h.COLS] +  # column units
         [h.cartesian_product(r, c) for r in ['ABC', 'DEF', 'GHI'] for c in ['123', '456', '789']])  # box units
unit_dict = dict((box, [unit for unit in units if box in unit]) for box in h.BOXES)  # map each box to its units
peer_dict = dict((box, set(sum(unit_dict[box], [])) - {box}) for box in h.BOXES)  # map each box to its peers


def eliminate(board):
    for k, v in board.items():
        if len(v) != 1:  # if the box needs elimination
            peers = peer_dict[k]  # get all the peers
            peer_values = set([board[p] for p in peers if len(board[p]) == 1])
            board[k] = ''.join(set(board[k]) - peer_values)
    return board


def only_choice(board):
    for unit in units:
        for num in '123456789':
            num_places = [box for box in unit if num in board[box]]
            if len(num_places) == 1:
                board[num_places[0]] = num
    return board


def run_episode(board):
    stuck = False
    while not stuck:
        # Check how many boxes have a fixed value
        solved_values_before = len([box for box in board.keys() if len(board[box]) == 1])

        # Use the Eliminate Strategy
        board = eliminate(board)

        # Use the Only Choice Strategy
        board = only_choice(board)

        # Check how many boxes have a fixed value now
        solved_values_after = len([box for box in board.keys() if len(board[box]) == 1])

        # If there is no change, stop the loop.
        stuck = solved_values_before == solved_values_after

        # if the current sudoku configuration is un-solvable then return False
        if len([box for box in board.keys() if len(board[box]) == 0]):
            return False
    return board


def search(board):
    # try to solve the board
    board = run_episode(board)

    if board is False:
        # it means the current configuration of the board is unsolvable
        # this happens when any of the boxes have no possible value to fix
        return False

    if all(len(v) == 1 for k, v in board.items()):
        # it means the board is solved
        return board

    # ==========================================================================================
    # The code above this line is to stop recursion (BASE CASE) and
    # The code below this line is to continue recursion (RECURSIVE CASE)
    # ==========================================================================================

    # Choose one of the unfilled squares with the fewest possibilities
    length, k = min((len(val), key) for key, val in board.items() if len(val) > 1)
    # print(k, length)

    # Now use recurrence to solve each one of the resulting sudokus, and
    for digit in board[k]:
        new_sudoku = dict(list(board.items()))

        # fix the value of the box
        new_sudoku[k] = digit

        # try to solve the new configuration of the board
        try_to_solve_new_config = search(new_sudoku)

        if try_to_solve_new_config:  # if the board is solved
            return try_to_solve_new_config  # return the solved board

        # if the board is not solved yet (got stuck again in the new configuration)
        # fix another digit and try again (thats what the loop is for)
        # keep fixing digits and try to solve until that configuration is either impossibe to solve
        # or it is solved
