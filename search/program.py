# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from .utils import render_board


def search(input: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """

    # The render_board function is useful for debugging -- it will print out a 
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).
    
    print(render_board(input, ansi=False))

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    return [
        (5, 6, -1, 1),
        (3, 1, 0, 1),
        (3, 2, -1, 1),
        (1, 4, 0, -1),
        (1, 3, 0, -1)
    ]

#Move a Red and output all the spread it will create
def move(red: tuple[int, int, int, int], k, input: dict[tuple, tuple]) -> tuple[int, int, int, int]:
    dim = [0,1,2,3,4,5,6]
    newRed=[]
    for x in range(1,k):
        if(red(3) == 0 & red(4) == 1):
            shift(red(2), 1)
        if(red(3) == -1 & red(4) == 1):
            shift(red(1), -1)
            shift(red(2), 1)
        if(red(3) == -1 & red(4) == 0):
            shift(red(1), -1)
        if(red(3) == 0 & red(4) == -1):
            shift(red(2), -1)
        if(red(3) == 1 & red(4) == -1):
            shift(red(1), 1)
            shift(red(2), -1)
        if(red(3) == 1 & red(4) == 0):
            shift(red(1), 1)
        newRed.append(dict[(red(1), red(2)): ('r', 1)])
        for x in input:
            if(x.keys() == (red(1), red(2))):
                newRed.remove(dict[(red(1), red(2)): ('r', 1)])
                newRed.append(dict[(red(1), red(2)): ('r', x.values() + 1)])
                break
    return newRed

def shift(a, k):
    dim = [0,1,2,3,4,5,6]
    b = k
    for x in range(len(dim) + k):
        if b == 0:
            break
        else:
            b = b - 1
            a = a + (k)
            if a == len(dim) + 1:
                a = 0
            if a < 0:
                a = len(dim)
    return x