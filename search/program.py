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
    # Check for initial blue nodes from the board
    blueNodes = 0
    for keyInput, valueInput in input.items():
        if valueInput[0] == 'b':
            blueNodes = blueNodes + 1
    minDistance = 100
    dic = {}
    subDic={}
    newRed={}
    action = []
    NewblueNodes = blueNodes
    # it will iterate through every red dot
    while NewblueNodes > 0:
        minDistance = 100
        dic = {}
        subDic={}
        newRed={}
        enemyPower = 0
        for keyInput, valueInput in input.items():
            newRed[keyInput] = valueInput
            if valueInput[0] == 'r':
                # it will iterate based on the power of the nodes and add all possible move to dic
                for i in range(1, valueInput[1] + 1):
                    newRed = moveAll([keyInput], i, input)
                    dic.update(newRed)
                # Save a blue node and a red node that is nearest to each other
                for key2, value2 in input.items():
                    for newKey, newValue in dic.items():
                        if value2[0] == 'b':
                            distance = calculateDistance(key2[0], key2[1], newKey[0], newKey[1])
                            if distance < minDistance:
                                minDistance = distance
                                minDistanceLocation = newKey
                                minStartingLocation = (keyInput, valueInput)
                                start = minStartingLocation[0]
                                minDesiredLocation = key2
                            # if there are two nodes that have same distance then record the highest power blue node to capture first
                            if distance == minDistance and value2[1] > enemyPower:
                                minDistance = distance
                                minDistanceLocation = newKey
                                minStartingLocation = (keyInput, valueInput)
                                start = minStartingLocation[0]
                                minDesiredLocation = key2
                                enemyPower = value2[1]
        currentBlueNodes = 1
        subMinDistance = 100
        newNodes = {}
        # doing greedy search for the red and blue node we recorded earlier
        while currentBlueNodes != 0:
            for i in range(1, minStartingLocation[1][1] + 1):
                subRedNodes = moveAll([minStartingLocation[0]], i, input)
                subDic.update(subRedNodes)
            for keySubRedNodes, valueSubRedNodes in subDic.items():
                subDistance = calculateDistance(keySubRedNodes[0], keySubRedNodes[1], minDesiredLocation[0], minDesiredLocation[1])
                if subDistance < subMinDistance:
                    subMinDistance = subDistance
                    subMinDistanceLocation = keySubRedNodes
                    subMinStartingLocation = (keySubRedNodes, valueSubRedNodes)
            dir = reversedShift(subMinDistanceLocation, minStartingLocation[0], minStartingLocation[1])
            # need to use start location then use direction to record all notes that is created
            newNodes.update(moveInDirection((minStartingLocation[0][0], minStartingLocation[0][1], dir[0], dir[1]), minStartingLocation[1][1], input))
            action.append((minStartingLocation[0][0], minStartingLocation[0][1], dir[0], dir[1]))
            for i in action:
                for newNodesKey in newNodes:
                    if i[0] == newNodesKey[0] and i[1] == newNodesKey[1]:
                        newNodes.pop(newNodesKey)
                        break
            minStartingLocation = subMinStartingLocation
            if minStartingLocation[0] == minDesiredLocation:
                currentBlueNodes = currentBlueNodes - 1
                blueNodes = blueNodes - 1
        # add in all the new red nodes we created to input
        input.pop(start)
        input.update(newNodes)
        NewblueNodes = 0
        # check for all the blueNodes that is left
        for key, value in input.items():
            if value[0] == 'b':
                NewblueNodes = NewblueNodes + 1

    # The render_board function is useful for debugging -- it will print out a 
    # board state in a human-readable format. Try changing the ansi argument 
    # to True to see a colour-coded version (if your terminal supports it).
    
    print(render_board(input, ansi=False))

    # Here we're returning "hardcoded" actions for the given test.csv file.
    # Of course, you'll need to replace this with an actual solution...
    return action

# Move in a certain direction
def moveInDirection(action: tuple[int, int, int, int], k, input: dict[tuple, tuple]):
    newRed = {}
    newRed2 = {}
    for i in range(1, k + 1):
        if action[2] == 0 and action[3] == 1:
            newRed[(action[0], shift(action[1], i))] = ('r', 1)
        if action[2] == -1 and action[3] == 1:
            newRed[(shift(action[0], -i), shift(action[1], i))] = ('r', 1)
        if action[2] == -1 and action[3] == 0:
            newRed[(shift(action[0], -i), action[1])] = ('r', 1)
        if action[2] == 0 and action[3] == -1:
            newRed[(action[0], shift(action[1], -i))] = ('r', 1)
        if action[2] == 1 and action[3] == -1:
            newRed[(shift(action[0], i), shift(action[1], -i))] = ('r', 1)
        if action[2] == 1 and action[3] == 0:
            newRed[(shift(action[0], i), action[1])] = ('r', 1)
        newRed2.update(newRed)
        newRedList = list(newRed.keys())
        list(action)[0] = newRedList[0][0]
        list(action)[1] = newRedList[0][1]
        for keyx, valuex in input.items():
            for keyy, valuey in newRed2.items():
                if(keyx == keyy):
                    newRed2.pop(keyy)
                    newRed2[keyx] = ('r', valuex[1] + 1)
                    break
    return newRed2

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