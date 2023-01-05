#################################################
# hw5.py
# name: Grge Budhijanto
# andrew id: gbudhija
#################################################

import cs112_f21_week5_linter
import math, copy

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7): #helper-fn
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d): #helper-fn
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def rgbString(red, green, blue):
     return f'#{red:02x}{green:02x}{blue:02x}'

#################################################
# Part A
#################################################

def nondestructiveRemoveRowAndCol(A, row, col):
    # remember: do not copy or deepcopy A here.
    # instead, directly construct the result
    aMod = []
    rows, cols = len(A), len(A[0])
    for rowIndex in range(rows):
        tempRow = []
        if rowIndex == row: continue
        else: 
            for colIndex in range(cols):
                if colIndex == col: continue
                else:
                    tempRow.append(A[rowIndex][colIndex])
        aMod.append(tempRow)
    return aMod

def destructiveRemoveRowAndCol(A, row, col):
    rowIndex = 0
    colIndex = 0
    while rowIndex < len(A):
        if rowIndex == row:
            A.pop(row)
        if A == []: break
        while colIndex < len(A[rowIndex]):
            if colIndex == col: A[rowIndex].pop(col)
            colIndex += 1
        rowIndex += 1
        colIndex = 0

def matrixMultiply(m1,m2):
    m1row, m1col = len(m1), len(m1[0])
    m2row, m2col = len(m2), len(m2[0])
    if m1col != m2row: return None
    result = [[0] * m2col for i in range(m1row)]
    for row in range(m1row):
        for col in range(m2col):
            for val in range(m1col): 
                result[row][col] += m1[row][val] * m2[val][col]
    return result

def isKingsTour(board):
    return 42

#################################################
# Part B
#################################################

def isMagicSquare(a):
    if a == []: return False
    elif isPerfectSquare(a) != True: return False #checks if grid is square
    elif noRepeatingInts(a) != True: return False
    else:
        sumCheck = sum(a[0])
        rotatedGrid = rotateGrid(a)
        for row in a: #goes through rows and checks sum
            if sum(row) == sumCheck:
                continue
            else: return False
        for col in rotatedGrid: #goes through "columns" and checks sum
            if sum(col) == sumCheck:
                continue
            else: return False
        if diagonalSum(a) == sumCheck and diagonalSum(rotatedGrid) == sumCheck:
            return True
        else: return False

def isPerfectSquare(a):
    rows, cols = len(a), len(a[0])
    if rows != cols: return False
    else:
        for row in a:
            if len(row) != cols:
                return False
            else: continue
        return True

def noRepeatingInts(a): #variation from previous hw4
    listVals = []
    seen = []
    for row in a:
        for val in row:
            if isinstance(val,int): listVals.append(val)
            else: return False
    for val in listVals:
        if val not in seen:
            seen.append(val)
        else: return False
    return True

def diagonalSum(a):
    sum = 0
    for i in range(len(a)):
        for j in range(len(a[0])):
            if i == j: #compare equal indexes
                sum += a[i][j] #add value
    return sum

def rotateGrid(a):
    vertFlip = []
    flipGrid = []
    cols = len(a[0])
    for row in a:
        for col in row[::-1]:
            vertFlip.append(col) #reverses rows and returns list of units
    for newRow in range(cols):
        colList = []
        for newCol in vertFlip[newRow::cols]:
            colList.append(newCol)
        flipGrid.append(colList)
        colList = []
    return flipGrid

#################################################

def wordSearchWithIntegerWildcards(board, word): #FROM CLASS NOTES!!
    (rows, cols) = (len(board), len(board[0]))
    for row in range(rows):
        for col in range(cols):
            result = wordSearchFromCell(board, word, row, col)
            if (result != None):
                return result
    return False

def wordSearchFromCell(board, word, startRow, startCol): #FROM CLASS NOTES!!
    possibleDirections = 8 # 3^2 - 1
    for direction in range(possibleDirections):
        result = wordSearchFromCellInDirection(board, word,
                                               startRow, startCol, direction)
        if (result != None):
            return result
    return None

def wordSearchFromCellInDirection(board, word, startRow, startCol, direction):
    (rows, cols) = (len(board), len(board[0]))
    dirs = [ (-1, -1), (-1, 0), (-1, +1),
             ( 0, -1),          ( 0, +1),
             (+1, -1), (+1, 0), (+1, +1) ]
    (drow,dcol) = dirs[direction]
    i = 0
    index = 0                              #MODIFIED FROM CLASS NOTES!!!!!!
    while (i < (len(word))):
        row = startRow + index*drow
        col = startCol + index*dcol
        if ((row < 0) or (row >= rows) or
            (col < 0) or (col >= cols)):
            index += 1
            return None
        if (board[row][col] != word[i]):
            if isinstance((board[row][col]),int):
                i += ((board[row][col]))
                index += 1
                if i > len(word): return None
                else: continue
            else: return None
        i += 1
        index += 1
    return True

#################################################

def areLegalValues(values):
    possibleVals = []
    seen = []
    for i in range(len(values)):
        possibleVals.append(i + 1)
    for val in values:
        if val == 0: continue
        elif val > possibleVals[-1] or val < 0:
            return False
        elif val not in seen:
            seen.append(val)
        else: return False
    return True

def isLegalRow(board, row):
    if row >= len(board) or row < 0: return False
    else: return areLegalValues(board[row])

def isLegalCol(board, col):
    n2 = int(math.sqrt(len(board)))
    flipBoard = []
    for newRow in range(n2):
        colList = []
        for newCol in board[newRow::n2]:
            colList.append(newCol)
        flipBoard.append(colList)
        colList = []
    if col >= n2 or col < 0: return False
    else: return areLegalValues(flipBoard[col])

def isLegalBlock(board, block):
    n = int(math.sqrt(int(math.sqrt(len(board)))))
    blockList = []
    index = (n**3 * (block//n)) + (n * (block % n))
    for i in range(n**2):
        blockList.append(board[index])
        index += 1
        if index % n == 0:
            index += (n**2 - n)
        else: continue
    return areLegalValues(blockList)

def isLegalSudoku(board):
    boardList = []
    n2 = len(board)
    for row in board:
        for val in row:
            boardList.append(val)
    for row in range(n2):
        if isLegalRow(board, row): continue
        else: return False
    for col in range(n2):
        if isLegalCol(boardList, col): continue
        else: return False
    for block in range(n2):
        if isLegalBlock(boardList, block): continue
        else: return False
    return True

#################################################
# Bonus/Optional
#################################################

def makeWordSearch(wordList, replaceEmpties):
    return 42

#################################################
# Test Functions (#ignore_rest)
#################################################

def testIsMagicSquare():
    print("Testing isMagicSquare()...", end="")
    assert(isMagicSquare([[42]]) == True)
    assert(isMagicSquare([[2, 7, 6], [9, 5, 1], [4, 3, 8]]) == True)
    assert(isMagicSquare([[4-7, 9-7, 2-7], [3-7, 5-7, 7-7], [8-7, 1-7, 6-7]])
           == True)
    a = [[7  ,12 ,1  ,14],
         [2  ,13 ,8  ,11],
         [16 ,3  ,10 ,5],
         [9  ,6  ,15 ,4]]
    assert(isMagicSquare(a))
    a = [[113**2, 2**2, 94**2],
         [ 82**2,74**2, 97**2],
         [ 46**2,127**2,58**2]]
    assert(isMagicSquare(a) == False)
    a = [[  35**2, 3495**2, 2958**2],
         [3642**2, 2125**2, 1785**2],
         [2775**2, 2058**2, 3005**2]]
    assert(isMagicSquare(a) == False)
    assert(isMagicSquare([[1, 2], [2, 1]]) == False)
    assert(isMagicSquare([[0], [0]]) == False) # Not square!
    assert(isMagicSquare([[1, 1], [1, 1]]) == False) # repeats
    assert(isMagicSquare('do not crash here!') == False)
    assert(isMagicSquare(['do not crash here!']) == False)
    assert(isMagicSquare([['do not crash here!']]) == False)
    print("Passed!")

def testNondestructiveRemoveRowAndCol():
    print('Testing nondestructiveRemoveRowAndCol()...', end='')
    a = [ [ 2, 3, 4, 5],[ 8, 7, 6, 5],[ 0, 1, 2, 3]]
    aCopy = copy.copy(a)
    assert(nondestructiveRemoveRowAndCol(a, 1, 2) == [[2, 3, 5], [0, 1, 3]])
    assert(a == aCopy)
    assert(nondestructiveRemoveRowAndCol(a, 0, 0) == [[7, 6, 5], [1, 2, 3]])
    assert(a == aCopy)
    b = [[37, 78, 29, 70, 21, 62, 13, 54, 5],
    [6,     38, 79, 30, 71, 22, 63, 14, 46],
    [47,    7,  39, 80, 31, 72, 23, 55, 15],
    [16,    48, 8,  40, 81, 32, 64, 24, 56],
    [57,    17, 49, 9,  41, 73, 33, 65, 25],
    [26,    58, 18, 50, 1,  42, 74, 34, 66], 
    [67,    27, 59, 10, 51, 2,  43, 75, 35],
    [36,    68, 19, 60, 11, 52, 3,  44, 76],
    [77,    28, 69, 20, 61, 12, 53, 4,  45]]

    c = [[37, 78, 29, 70, 21, 62,     54, 5],
    [6,     38, 79, 30, 71, 22,     14, 46],
    [47,    7,  39, 80, 31, 72,     55, 15],
    [16,    48, 8,  40, 81, 32,     24, 56],
    [57,    17, 49, 9,  41, 73,     65, 25],
    [26,    58, 18, 50, 1,  42,     34, 66], 
    [67,    27, 59, 10, 51, 2,      75, 35],
    [36,    68, 19, 60, 11, 52, 44, 76]]

    bCopy = copy.copy(b)
    assert(nondestructiveRemoveRowAndCol(b,8,6) == c)
    assert(b == bCopy)
    print('Passed!')

def testDestructiveRemoveRowAndCol():
    print("Testing destructiveRemoveRowAndCol()...", end='')
    A = [ [ 2, 3, 4, 5],
          [ 8, 7, 6, 5],
          [ 0, 1, 2, 3]
        ]
    B = [ [ 2, 3, 5],
          [ 0, 1, 3]
        ]
    assert(destructiveRemoveRowAndCol(A, 1, 2) == None)
    assert(A == B) # but now A is changed!
    A = [ [ 1, 2 ], [3, 4] ]
    B = [ [ 4 ] ]
    assert(destructiveRemoveRowAndCol(A, 0, 0) == None)
    assert(A == B)
    A = [ [ 1, 2 ] ]
    B = [ ]
    assert(destructiveRemoveRowAndCol(A, 0, 0) == None)
    assert(A == B)
    print("Passed!")

def testMatrixMultiply():
    print("Testing matrixMultiply()...", end='')
    m1 = [[1,2],
          [3,4]] # 2x2
    m2 = [[4],
          [5]]     # 2x1
    m3 = [[14],
          [32]]
    assert(matrixMultiply(m1,m2) == m3) 
    assert(matrixMultiply([[3, 7], [4, 5], [5, 4], [5, 6], [8, 9], [7, 4]], 
                          [[9, 8, 3],
                           [5, 1, 3]])==
                          [[62, 31, 30],
                           [61, 37, 27],
                           [65, 44, 27],
                           [75, 46, 33],
                           [117, 73, 51],
                           [83, 60, 33]])
    assert matrixMultiply([[8]],[[5]])==[[40]]
    print("Passed!")

def testIsKingsTour():
    print("Testing isKingsTour()...", end="")
    a = [ [  3, 2, 1 ],
          [  6, 4, 9 ],
          [  5, 7, 8 ] ]
    assert(isKingsTour(a) == True)
    a = [ [  2, 8, 9 ],
          [  3, 1, 7 ],
          [  4, 5, 6 ] ]
    assert(isKingsTour(a) == True)
    a = [ [  7, 5, 4 ],
          [  6, 8, 3 ],
          [  1, 2, 9 ] ]
    assert(isKingsTour(a) == True)
    a = [ [  7, 5, 4 ],
          [  6, 8, 3 ],
          [  1, 2, 1 ] ]
    assert(isKingsTour(a) == False)
    a = [ [  3, 2, 9 ],
          [  6, 4, 1 ],
          [  5, 7, 8 ] ]
    assert(isKingsTour(a) == False)
    a = [ [  3, 2, 1 ],
          [  6, 4, 0 ],
          [  5, 7, 8 ] ]
    assert(isKingsTour(a) == False)
    a = [ [  1, 2, 3 ],
          [  7, 4, 8 ],
          [  6, 5, 9 ] ]
    assert(isKingsTour(a) == False)
    a = [ [ 3, 2, 1 ],
          [ 6, 4, 0 ],
          [ 5, 7, 8 ] ]
    assert(isKingsTour(a) == False)
    print("Passed!")

def testWordSearchWithIntegerWildcards():
    print("Testing wordSearchWithIntegerWildcards()...", end='')
    board = [ [ 'd', 'o', 'g' ],
              [ 't', 'a', 'c' ],
              [ 'o', 'a', 't' ],
              [ 'u', 'r', 'k' ],
            ]
    assert(wordSearchWithIntegerWildcards(board, "dog") == True)
    assert(wordSearchWithIntegerWildcards(board, "cat") == True)
    assert(wordSearchWithIntegerWildcards(board, "tad") == True)
    assert(wordSearchWithIntegerWildcards(board, "cow") == False)
    board = [ [ 'd', 'o',  1  ],
              [  3 , 'a', 'c' ],
              [ 'o', 'q' ,'t' ],
            ]
    assert(wordSearchWithIntegerWildcards(board, "z") == True)
    assert(wordSearchWithIntegerWildcards(board, "zz") == False)
    assert(wordSearchWithIntegerWildcards(board, "zzz") == True)
    assert(wordSearchWithIntegerWildcards(board, "dzzzo") == True)
    assert(wordSearchWithIntegerWildcards(board, "dzzo") == True)
    assert(wordSearchWithIntegerWildcards(board, "zzzd") == True)
    assert(wordSearchWithIntegerWildcards(board, "zzzo") == True)
    board = [ [ 3 ] ]
    assert(wordSearchWithIntegerWildcards(board, "zz") == False)
    assert(wordSearchWithIntegerWildcards(board, "zzz") == True)
    assert(wordSearchWithIntegerWildcards(board, "zzzz") == False)
    board = [ [ 'a', 'b', 'c' ],
              [ 'd',  2 , 'e' ],
              [ 'f', 'g', 'h' ]]
    assert(wordSearchWithIntegerWildcards(board, "aqqh") == True)
    assert(wordSearchWithIntegerWildcards(board, "aqqhh") == False)
    assert(wordSearchWithIntegerWildcards(board, "zz") == True)
    assert(wordSearchWithIntegerWildcards(board, "zzc") == True)
    assert(wordSearchWithIntegerWildcards(board, "zaz") == False)
    print("Passed!")

def testIsLegalSudoku():
    # From Leon Zhang!
    print("Testing isLegalSudoku()...", end="")
    board = [[0]]
    assert isLegalSudoku(board) == True
    board = [[1]]
    assert isLegalSudoku(board) == True

    board = [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 0, 0, 0]]
    assert isLegalSudoku(board) == True
    board = [[0, 4, 0, 0],
             [0, 0, 3, 0],
             [1, 0, 0, 0],
             [0, 0, 0, 2]]
    assert isLegalSudoku(board) == True
    board = [[1, 2, 3, 4],
             [3, 4, 1, 2],
             [2, 1, 4, 3],
             [4, 3, 2, 1]]
    assert isLegalSudoku(board) == True
    board = [[1, 2, 3, 4],
             [3, 4, 4, 2],
             [2, 4, 4, 3],
             [4, 3, 2, 1]]    
    assert isLegalSudoku(board) == False

    board = [
    [ 5, 3, 0, 0, 7, 0, 0, 0, 0 ],
    [ 6, 0, 0, 1, 9, 5, 0, 0, 0 ],
    [ 0, 9, 8, 0, 0, 0, 0, 6, 0 ],
    [ 8, 0, 0, 0, 6, 0, 0, 0, 3 ],
    [ 4, 0, 0, 8, 0, 3, 0, 0, 1 ],
    [ 7, 0, 0, 0, 2, 0, 0, 0, 6 ],
    [ 0, 6, 0, 0, 0, 0, 2, 8, 0 ],
    [ 0, 0, 0, 4, 1, 9, 0, 0, 5 ],
    [ 0, 0, 0, 0, 8, 0, 0, 7, 9 ]
    ]
    assert isLegalSudoku(board) == True
    
    board = [
    [ 5, 3, 0, 0, 7, 0, 0, 0, 0 ],
    [ 6, 0, 0, 1, 9, 5, 0, 0, 0 ],
    [ 0, 9, 8, 0, 0, 0, 0, 6, 0 ],
    [ 8, 0, 0, 0, 6, 0, 0, 0, 3 ],
    [ 4, 0, 0, 8, 0, 3, 0, 0, 1 ],
    [ 7, 0, 0, 0, 2, 0, 0, 0, 6 ],
    [ 0, 6, 0, 0, 0, 0, 2, 8, 0 ],
    [ 0, 0, 0, 4, 1, 9, 0, 0, 5 ],
    [ 0, 0, 0, 0, 8, 0, 9, 7, 9 ]
    ]
    assert isLegalSudoku(board) == False
    board = [
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    assert isLegalSudoku(board) == True
    board = [
    [ 2,11, 9, 5, 8,16,13, 4,12, 3,14, 7,10, 6,15, 1],
    [ 4,12,15,10, 3, 6, 9,11,13, 5, 8, 1,16, 7,14, 2],
    [ 1,14, 6, 7,15, 2, 5,12,11, 9,10,16, 3,13, 8, 4],
    [16,13, 8, 3,14, 1,10, 7, 4, 6, 2,15, 9,11, 5,12],
    [12, 2,16, 9,10,14,15,13, 8, 1, 5, 3, 6, 4,11, 7],
    [ 6, 7, 1,11, 5,12, 8,16, 9,15, 4, 2,14,10, 3,13],
    [14, 5, 4,13, 6,11, 1, 3,16,12, 7,10, 8, 9, 2,15],
    [ 3, 8,10,15, 4, 7, 2, 9, 6,14,13,11, 1,12,16, 5],
    [13, 9, 2,16, 7, 8,14,10, 3, 4,15, 6,12, 5, 1,11],
    [ 5, 4,14, 6, 2,13,12, 1,10,16,11, 8,15, 3, 7, 9],
    [ 7, 1,11,12,16, 4, 3,15, 5,13, 9,14, 2, 8,10, 6],
    [10,15, 3, 8, 9, 5,11, 6, 2, 7, 1,12, 4,14,13,16],
    [11,10,13,14, 1, 9, 7, 8,15, 2, 6, 4, 5,16,12, 3],
    [15, 3, 7, 4,12,10, 6, 5, 1, 8,16,13,11, 2, 9,14],
    [ 8, 6, 5, 1,13, 3,16, 2,14,11,12, 9, 7,15, 4,10],
    [ 9,16,12, 2,11,15, 4,14, 7,10, 3, 5,13, 1, 6, 8]]
    assert isLegalSudoku(board) == True
    # last number is supposed to be 8, not 10
    board = [
    [ 2,11, 9, 5, 8,16,13, 4,12, 3,14, 7,10, 6,15, 1],
    [ 4,12,15,10, 3, 6, 9,11,13, 5, 8, 1,16, 7,14, 2],
    [ 1,14, 6, 7,15, 2, 5,12,11, 9,10,16, 3,13, 8, 4],
    [16,13, 8, 3,14, 1,10, 7, 4, 6, 2,15, 9,11, 5,12],
    [12, 2,16, 9,10,14,15,13, 8, 1, 5, 3, 6, 4,11, 7],
    [ 6, 7, 1,11, 5,12, 8,16, 9,15, 4, 2,14,10, 3,13],
    [14, 5, 4,13, 6,11, 1, 3,16,12, 7,10, 8, 9, 2,15],
    [ 3, 8,10,15, 4, 7, 2, 9, 6,14,13,11, 1,12,16, 5],
    [13, 9, 2,16, 7, 8,14,10, 3, 4,15, 6,12, 5, 1,11],
    [ 5, 4,14, 6, 2,13,12, 1,10,16,11, 8,15, 3, 7, 9],
    [ 7, 1,11,12,16, 4, 3,15, 5,13, 9,14, 2, 8,10, 6],
    [10,15, 3, 8, 9, 5,11, 6, 2, 7, 1,12, 4,14,13,16],
    [11,10,13,14, 1, 9, 7, 8,15, 2, 6, 4, 5,16,12, 3],
    [15, 3, 7, 4,12,10, 6, 5, 1, 8,16,13,11, 2, 9,14],
    [ 8, 6, 5, 1,13, 3,16, 2,14,11,12, 9, 7,15, 4,10],
    [ 9,16,12, 2,11,15, 4,14, 7,10, 3, 5,13, 1, 6,10]]
    assert isLegalSudoku(board) == False
    print("Passed!")

def testMakeWordSearch():
    print("Testing makeWordSearch()...", end="")
    board = makeWordSearch([], False)
    assert(board == None)

    board = makeWordSearch(["ab"], False)
    assert(board == [['a', 'b'], ['-', '-'] ])
    board = makeWordSearch(["ab"], True)
    assert(board == [['a', 'b'], ['c', 'd'] ])
    board = makeWordSearch(["ab", "bc", "cd"], False)
    assert(board == [['a', 'b'], ['c', 'd'] ])
    board = makeWordSearch(["ab", "bc", "cd", "de"], False)
    assert(board == [['a', 'b', '-'], ['c', 'd', '-'], ['d', 'e', '-']])
    board = makeWordSearch(["ab", "bc", "cd", "de"], True)
    assert(board == [['a', 'b', 'a'], ['c', 'd', 'c'], ['d', 'e', 'a']])

    board = makeWordSearch(["abc"], False)
    assert(board == [['a', 'b', 'c'], ['-', '-', '-'], ['-', '-', '-']])
    board = makeWordSearch(["abc"], True)
    assert(board == [['a', 'b', 'c'], ['c', 'd', 'a'], ['a', 'b', 'c']])

    board = makeWordSearch(["abc", "adc", "bd", "bef", "gfc"], False)
    assert(board == [['a', 'b', 'c'], ['d', 'e', '-'], ['c', 'f', 'g']])
    board = makeWordSearch(["abc", "adc", "bd", "bef", "gfc"], True)
    assert(board == [['a', 'b', 'c'], ['d', 'e', 'a'], ['c', 'f', 'g']])

    board = makeWordSearch(["abcd", "abc", "dcb"], False)
    assert(board == [['a', 'b', 'c', 'd'],
                     ['-', '-', '-', '-'], 
                     ['-', '-', '-', '-'],
                     ['-', '-', '-', '-']])
    board = makeWordSearch(["abcd", "abc", "dcb", "xa", "bya"], False)
    assert(board == [['a', 'b', 'c', 'd'],
                     ['x', 'y', '-', '-'], 
                     ['-', 'a', '-', '-'],
                     ['-', '-', '-', '-']])
    board = makeWordSearch(["abcd", "abc", "dcb", "xa", "bya", "bax", "dca"],
                           False)
    assert(board == [['a', 'b', 'c', 'd'],
                     ['x', 'y', 'c', '-'], 
                     ['-', 'a', '-', '-'],
                     ['-', '-', 'b', '-']])
    board = makeWordSearch(["abcd", "abc", "dcb", "xa", "bya", "bax", "dca"],
                           True)
    assert(board == [['a', 'b', 'c', 'd'],
                     ['x', 'y', 'c', 'a'], 
                     ['b', 'a', 'd', 'e'],
                     ['c', 'e', 'b', 'a']])
    #[ (["abcd", "abc", "dcb", "xa", "by", "bya", "bbbx", "dbxa", "cbxa" ],
    #False),

    print("Passed!")

#################################################
# testAll and main
#################################################

def testAll():
    # comment out the tests you do not wish to run!
    # Part A:
    testNondestructiveRemoveRowAndCol()
    testDestructiveRemoveRowAndCol()
    testMatrixMultiply()
    # testIsKingsTour()

    # Part B:
    testIsMagicSquare()
    testWordSearchWithIntegerWildcards()
    testIsLegalSudoku()
    # testThreeMensMorris() # this will be submitted in a separate file!

    # Bonus:
    # testMakeWordSearch()

def main():
    cs112_f21_week5_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
