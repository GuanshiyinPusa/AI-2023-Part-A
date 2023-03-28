# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part A: Single Player Infexion

from .utils import render_board
import math

def search(input: dict[tuple, tuple]) -> list[tuple]:
    """
    This is the entry point for your submission. The input is a dictionary
    of board cell states, where the keys are tuples of (r, q) coordinates, and
    the values are tuples of (p, k) cell states. The output should be a list of 
    actions, where each action is a tuple of (r, q, dr, dq) coordinates.

    See the specification document for more details.
    """
    minDistance = 100
    dic = {}
    subDic={}
    newRed={}
    action = []
    blueNodes = 0
    # it will iterate through every red dot
    for key, value in input.items():
        newRed[key] = value
        if value[0] == 'b':
            blueNodes = blueNodes + 1
        if value[0] == 'r':
            # it will iterate based on the power of the dot and add all possible move to dic
            for i in range(1, value[1] + 1):
                newRed = moveAll([key], i, input)
                dic.update(newRed)
            for key2, value2 in input.items():
                for newKey, newValue in dic.items():
                    if value2[0] == 'b':
                        distance = calculateDistance(key2[0], key2[1], newKey[0], newKey[1])
                        if distance < minDistance:
                            minDistance = distance
                            minDistanceLocation = newKey
                            minStartingLocation = (key, value)
                            minDesiredLocation = key2
            # reverse minDistanceLocation to get the direction of the spread
            dir = reversedShift(minDistanceLocation, key, value)
            print(minDistanceLocation, "00")
            print(dir, "13")
    currentBlueNodes = 1
    subMinDistance = 100
    while currentBlueNodes != 0:
        for i in range(1, minStartingLocation[1][1] + 1):
            subRedNodes = moveAll([minStartingLocation[0]], i, input)
            subDic.update(subRedNodes)
        for key, value in subRedNodes.items():
            subDistance = calculateDistance(key[0], key[1], minDesiredLocation[0], minDesiredLocation[1])
            if subDistance < subMinDistance:
                subMinDistance = subDistance
                subMinDistanceLocation = key
                subMinStartingLocation = (key, value)
        dir = reversedShift(subMinDistanceLocation, minStartingLocation[0], minStartingLocation[1])
        action.append((minStartingLocation[0][0], minStartingLocation[0][1], dir[0], dir[1]))
        print(action)
        minStartingLocation = subMinStartingLocation
        if minStartingLocation[0] == minDesiredLocation:
            currentBlueNodes = currentBlueNodes - 1
    print(subDic, "88")
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

#reverse newKey to oldKey to get the direction of the spread
def reversedShift(newKey, oldKey, oldValue):
    for i in range(1, oldValue[1] + 1):
        if (oldKey[0], shift(oldKey[1], i)) == newKey:
            return (0, 1)
        if (shift(oldKey[0], -i), shift(oldKey[1], i)) == newKey:
            return (-1, 1)
        if (shift(oldKey[0], -i), oldKey[1]) == newKey:
            return (-1, 0)
        if (oldKey[0], shift(oldKey[1], -i)) == newKey:
            return (0, -1)
        if (shift(oldKey[0], i), shift(oldKey[1], -i)) == newKey:
            return (1, -1)
        if (shift(oldKey[0], i), oldKey[1]) == newKey:
            return (1, 0)
    return 0

#Calculate distance between 2 points
def calculateDistance(x1, y1, x2, y2):
    value = math.sqrt(pow((x2-x1),2) + pow((y2-y1), 2))
    return value