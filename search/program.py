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
    dic = {}
    newRed={}
    # it will iterate through every red dot
    for key, value in input.items():
        newRed[key] = value
        if value[0] == 'r':
            # it will iterate based on the power of the dot and add all possible move to dic
            for i in range(1, value[1] + 1):
                print(key)
                newRed = moveAll([key], i, input)
                dic.update(newRed)
    print(dic)

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

#Move a Red in all direction and output all the spread it will create
def moveAll(red: tuple[int, int], k, input: dict[tuple, tuple]):
    newRed={}
    print(k)
    print(red)
    for key in red:
        newRed[(key[0], shift(key[1], k))] = ('r', 1)
        newRed[(shift(key[0], -k), shift(key[1], k))] = ('r', 1)
        newRed[(shift(key[0], -k), key[1])] = ('r', 1)
        newRed[(key[0], shift(key[1], -k))] = ('r', 1)
        newRed[(shift(key[0], k), shift(key[1], -k))] = ('r', 1)
        newRed[(shift(key[0], k), key[1])] = ('r', 1)
        for keyx, valuex in input.items():
            for keyy, valuey in newRed.items():
                if(keyx == keyy):
                    newRed.pop(keyy)
                    newRed[keyx] = ('r', valuex[1] + 1)
                    break
        print(newRed, "123")
    return newRed

def shift(a, k):
    dim = [0,1,2,3,4,5,6]
    b = k
    for x in range(len(dim) + k):
        if b == 0:
            break
        else:
            if b > 0:
                b = b - 1
                a = a + 1
            if b < 0:
                b = b + 1
                a = a - 1
            if a > len(dim) - 1:
                a = 0
            if a < 0:
                a = len(dim) -  1
    return a

#Calculate distance between 2 points
def calculateDistance(x1, y1, x2, y2):
    value = (((x1-x2)^(2)) + ((y1-y2)^(2)))^(1/2)
    return value