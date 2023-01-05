#################################################
# hw10.py
#
# Your name: Greg Budhijanto
# Your andrew id: gbudhija
#################################################

import cs112_f21_week10_linter
import math, os

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################

def findLargestFile(path):
    # Wrapper to extract just the bestPath from the helper
    # function that returns both bestPath and bestSize
    files = findLargestFileAndSize(path)
    bestPath = None
    bestSize = None
    for (file, fileSize) in files:
        if bestSize == None or fileSize > bestSize:
            bestSize = fileSize
            bestPath = file
    if bestPath == None: return ''
    return bestPath


def findLargestFileAndSize(path):
    # Returns (bestPath, bestSize) starting from this path, which could
    # be to either a folder or a file
    if os.path.isdir(path) == False: # base case: a file
        return [(path, os.path.getsize(path))]
    else: # recursive case: a folder
        files = [ ]
        for filename in os.listdir(path):
            files += findLargestFileAndSize(path + '/' + filename)
        return files

def knightsTour(rows, cols):
    for row in range(rows):
        for col in range(cols):
            board = [([0] * cols) for row in range(rows)] #initiate board dims
            board[row][col] = 1
            return knightsTourWrapper(row, col, board, 2) #initiate stepNum=1

def moveIsLegal(testRow, testCol, board):
    if ((0 <= testRow < len(board)) and 0 <= testCol < len(board[0]) and 
        (board[testRow][testCol] == 0)): #in bounds and spot == 0: Legal
        return True
    else: return False

def knightsTourWrapper(row, col, board, stepNumber):
    #bc
    if (stepNumber-1) == (len(board)*len(board[0])):
        return board
    #rc
    else:
        directions = [(-2,-1),(-2,1),(-1,-2),(-1,2),
                      (1,-2),(1,2),(2,-1),(2,1)]
        for drow,dcol in directions:
            testRow, testCol = row+drow, col+dcol
            if moveIsLegal(testRow, testCol, board):
                board[testRow][testCol] = stepNumber
                solution=knightsTourWrapper(testRow,testCol,board,stepNumber+1)
                if solution != None:
                    return solution
                board[testRow][testCol] = 0
        return None

#################################################
# Test Functions
#################################################

def testFindLargestFile():
    print('Testing findLargestFile()...', end='')
    assert(findLargestFile('sampleFiles/folderA') ==
                           'sampleFiles/folderA/folderC/giftwrap.txt')
    assert(findLargestFile('sampleFiles/folderB') ==
                           'sampleFiles/folderB/folderH/driving.txt')
    assert(findLargestFile('sampleFiles/folderB/folderF') == '')
    print('Passed!')

def testKnightsTour():
    print('Testing knightsTour()....', end='')
    def checkDims(rows, cols, ok=True):
        T = knightsTour(rows, cols)
        s = f'knightsTour({rows},{cols})'
        if (not ok):
            if (T is not None):
                raise Exception(f'{s} should return None')
            return True
        if (T is None):
            raise Exception(f'{s} must return a {rows}x{cols}' +
                             ' 2d list (not None)')
        if ((rows != len(T)) or (cols != (len(T[0])))):
            raise Exception(f'{s} must return a {rows}x{cols} 2d list')
        d = dict()
        for r in range(rows):
            for c in range(cols):
                d[ T[r][c] ] = (r,c)
        if (sorted(d.keys()) != list(range(1, rows*cols+1))):
            raise Exception(f'{s} should contain numbers' +
                             ' from 1 to {rows*cols}')
        prevRow, prevCol = d[1]
        for step in range(2, rows*cols+1):
            row,col = d[step]
            distance = abs(prevRow - row) + abs(prevCol - col)
            if (distance != 3):
                raise Exception(f'{s}: from {step-1} to {step}' +
                                 ' is not a legal move')
            prevRow, prevCol = row,col
        return True
    assert(checkDims(4, 3))
    assert(checkDims(4, 4, ok=False))
    assert(checkDims(4, 5))
    assert(checkDims(3, 4))
    assert(checkDims(3, 6, ok=False))
    assert(checkDims(3, 7))
    assert(checkDims(5, 5))
    print('Passed!')

#################################################
# testAll and main
#################################################

def testAll():
    testFindLargestFile()
    testKnightsTour()

def main():
    cs112_f21_week10_linter.lint()
    testAll()

if (__name__ == '__main__'):
    main()