def cartesian_product(x, y):
    return [a + b for a in x for b in y]


ROWS = 'ABCDEFGHI'
COLS = '123456789'
BOXES = cartesian_product(ROWS, COLS)


def display(values):
    print('')
    width = 1 + max(len(values[s]) for s in BOXES)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in ROWS:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in COLS))
        if r in 'CF':
            print(line)

    return
