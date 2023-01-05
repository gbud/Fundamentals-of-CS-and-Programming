#################################################
# lights-out.py
# Your Name: Greg Budhijanto
# Your AndrewID: gbudhija
# 
# Groupmate's Names: MM Demangone
# Groupmate's AndrewIDs: mdemango
#################################################

#################################################
# LightsOut!
# 
# Write the console-based game "LightsOut!"
# 
# Link to the writeup: https://docs.google.com/document/d/16ggNUsb0_Ddn6RMD2pStw0ZGkjAx8aTaoN4b0buTDII/edit?usp=sharing
# Link to the game: https://www.logicgamesonline.com/lightsout/
#################################################

#################################################
# Printing functions
#################################################

# Prints out the given 2D list input
def print2dList(a):
    if (a == []): print([]); return
    rows, cols = len(a), len(a[0])
    colWidths = [0] * cols
    for col in range(cols):
        colWidths[col] = max([len(str(a[row][col])) for row in range(rows)])
    print('[')
    for row in range(rows):
        print(' [ ', end='')
        for col in range(cols):
            if (col > 0): print(', ', end='')
            print(str(a[row][col]).ljust(colWidths[col]), end='')
        print(' ]')
    print(']')

# Prints out the lightsOut solution for the hardcoded starting configuration 
# as a list of (row, col) tuples 
def printSolution():
    solution = [(0, 0), (0, 1), (0, 3), (0, 4), 
                (1, 2), (1, 3), (2, 1), (2, 3), 
                (2, 4), (3, 2), (3, 3), (4, 0), (4, 1)]

    print("Solution to the board:")
    for elem in solution:
        print(elem)

#################################################
# Gameplay
#################################################

# Initializes the starting configuration of the board
def makeStartingConfiguration():
    boardSize = 5
    board = [[0 for col in range(boardSize)] for row in range(boardSize)]
    board[0][2] = 1
    board[0][3] = 1
    board[1][0] = 1
    board[1][1] = 1
    board[1][4] = 1
    board[2][0] = 1
    board[2][1] = 1
    board[3][0] = 1
    board[3][1] = 1
    board[3][3] = 1
    board[4][3] = 1
    return board

# def makeStartingConfiguration():
#     boardSize = 5
#     board = [[0 for col in range(boardSize)] for row in range(boardSize)]
#     board[1][2] = 1
#     board[2][1] = 1
#     board[2][2] = 1
#     board[2][3] = 1
#     board[3][2] = 1
#     return board

# This function is called to start the game of lightsOut!
def play():
    board = makeStartingConfiguration()
    print2dList(board)
    (rows, cols) = (len(board), len(board[0]))
    lightsOut = False
    while lightsOut == False:
        turn = (input(f"input row (1 through {rows}): "), 
                input(f"input column (1 through {cols}): "))
        turnRow, turnCol = turn
        if isValid(turnRow,turnCol) == False:
            print("invalid inputs")
            continue
        swRow = int(turnRow) - 1
        swCol = int(turnCol) - 1
        if ((swRow < 0) or (swRow >= rows) or
            (swCol < 0) or (swCol >= cols)):
            print("invalid inputs")
            continue
        changeLight(board, swRow, swCol) #changes lights 
        if isGameWon(board): #returns true or false statement
            print("LIGHTS OUT!!")
            lightsOut = True
        
def isValid(turnRow,turnCol):
    if turnRow.isnumeric() and turnCol.isnumeric(): return True
    else: return False

def changeLight(board, swRow, swCol):
    (rows, cols) = (len(board), len(board[0]))
    board[swRow][swCol] = flipSwitch(board[swRow][swCol]) #flip input switch
    north = swRow - 1
    south = swRow + 1
    west = swCol - 1
    east = swCol + 1
    if north >= 0: #flip north switch
        board[north][swCol] = flipSwitch(board[north][swCol])
    if south < rows: #flip south switch
        board[south][swCol] = flipSwitch(board[south][swCol])
    if west >= 0: #flip west switch
        board[swRow][west] = flipSwitch(board[swRow][west])
    if east < cols: #flip east switch
        board[swRow][east] = flipSwitch(board[swRow][east])
    print2dList(board)
    return board

def flipSwitch(boardIndex):
    if boardIndex == 0: return 1
    elif boardIndex == 1: return 0
    return boardIndex

def isGameWon(board):
    (rows, cols) = (len(board), len(board[0]))
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 1:
                return False
                print('not yet')
    return True

    
#################################################
# Top-level functions
#################################################

#printSolution()   # uncomment me to print the solution to the starting board!
play()


