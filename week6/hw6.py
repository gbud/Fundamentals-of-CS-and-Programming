#################################################
# hw6.py
#
# Your name:
# Your andrew id:
#
# Your partner's name:
# Your partner's andrew id:
#################################################

import cs112_f21_week6_linter
import math, copy, random

from cmu_112_graphics import *

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

def isPerfectSquare(n):
    return 42

def isSortOfSquarish(n):
    return 42

def nthSortOfSquarish(n):
    return 42

#################################################
# s21-midterm1-animation
#################################################

def s21MidtermAnimation_appStarted(app):
    app.label = 'S21 Midterm Animation!'
    app.i = 0
    app.y = 0
    app.color = 'purple'
    app.timerDelay = 10

def s21MidtermAnimation_keyPressed(app, event):
    app.color = random.choice(['red', 'orange', 'yellow', 'green', 'blue'])

def s21MidtermAnimation_timerFired(app):
    app.y += 20
    if app.y >= app.height/2:
        app.y = 0
        app.i = (app.i + 1) % len(app.label)
        if app.label[app.i].isspace(): app.i += 1

def s21MidtermAnimation_redrawAll(app, canvas):
    for j in range(app.i+1):
        x = app.width/len(app.label) * (j + 0.5)
        y = app.height/2 if (j < app.i) else app.y
        canvas.create_text(x, y, fill=app.color,
                           text=app.label[j], font=f'Arial 30 bold')

def s21Midterm1Animation():
    runApp(width=400, height=400, fnPrefix='s21MidtermAnimation_')

#################################################
# Tetris
#################################################


############################### MODEL FUNCTIONS ################################

def appStarted(app):
    app.rows,app.cols,app.cellSize,app.margin = gameDimensions()
    app.emptyColor = 'blue'
    app.board = [[app.emptyColor] * app.cols for row in range(app.rows)]
    tetrisPiecesAndColor(app)
    newFallingPiece(app)
    app.timerDelay = 250
    app.direction = (1,0) #drow, dcol
    app.gameOver = False
    app.score = 0

def tetrisPiecesAndColor(app):
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]]
    app.tetrisPieces = [iPiece, jPiece, lPiece, oPiece,
                        sPiece, tPiece, zPiece]
    app.tetrisPieceColors = [ "red", "yellow", "magenta", "pink",
                              "cyan", "green", "orange" ]

def newFallingPiece(app):
    import random
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]
    fallingPieceRowsCols(app)
    fallingPieceStart(app)

def fallingPieceRowsCols(app):
    app.pieceRows = len(app.fallingPiece)
    app.pieceCols = len(app.fallingPiece[0])

def fallingPieceStart(app):
    app.pieceRowCorner = 0
    app.pieceColCorner = app.cols//2 - len(app.fallingPiece[0])//2

############################# CONTROLLER FUNCTIONS #############################
    
def keyPressed(app, event):
    if (event.key == 'Up'):
        rotateFallingPiece(app)
    elif (event.key == "r"):
        appStarted(app)
    elif (event.key == 'Down'):
        app.direction = (+1, 0)
        directionPress(app, app.direction)
    elif (event.key == 'Left'):
        app.direction = (0, -1)
        directionPress(app, app.direction)
    elif (event.key == 'Right'):
        app.direction = (0, +1)
        directionPress(app, app.direction)
    elif (event.key == 'w'):
        hardDrop(app)

def hardDrop(app):
    pRC = app.pieceRowCorner
    pCC = app.pieceColCorner
    while fallingPieceIsLegal(app,pRC,pCC,app.fallingPiece):
        moveFallingPiece(app,1,0)

def directionPress(app, direction):
    (drow, dcol) = app.direction
    moveFallingPiece(app, drow, dcol)

def rotateFallingPiece(app):
    newPiece = []
    for col in range(app.pieceCols)[::-1]:
        rowList = []
        for row in range(app.pieceRows):
            rowList.append(app.fallingPiece[row][col])
        newPiece.append(rowList)
    newRowCorner, newColCorner = centerLocations(app,newPiece)
    if fallingPieceIsLegal(app, newRowCorner, newColCorner, newPiece):
        app.fallingPiece = newPiece
        fallingPieceRowsCols(app)
        app.pieceRowCorner = newRowCorner
        app.pieceColCorner = newColCorner

def centerLocations(app,newPiece):
    newRowCorner = app.pieceRowCorner + app.pieceRows//2 - len(newPiece)//2
    newColCorner = app.pieceColCorner + app.pieceCols//2  - len(newPiece[0])//2
    return (newRowCorner,newColCorner)

def timerFired(app):
    if app.gameOver == True:
        return
    if moveFallingPiece(app, +1, 0) == False:
        placeFallingPiece(app)
        newFallingPiece(app)
        isGameOver(app)

def isGameOver(app):
    pRC = app.pieceRowCorner
    pCC = app.pieceColCorner
    if fallingPieceIsLegal(app,pRC,pCC,app.fallingPiece) == False:
        app.gameOver = True

def moveFallingPiece(app, drow, dcol):
    newRowCorner = app.pieceRowCorner + drow
    newColCorner = app.pieceColCorner + dcol
    if fallingPieceIsLegal(app, newRowCorner, newColCorner, app.fallingPiece):
        app.pieceRowCorner = newRowCorner
        app.pieceColCorner = newColCorner
        return True
    else: return False

def fallingPieceIsLegal(app, rowCorner, colCorner, piece):
    for row in range(len(piece)):  
        for col in range(len(piece[0])):
            if piece[row][col]: #checks index of piece
                if ((rowCorner + row < 0) or (rowCorner + row >= app.rows) or
                    (colCorner + col < 0) or (colCorner + col >= app.cols) or
                    (app.board[rowCorner+row][colCorner+col]!=app.emptyColor)):
                    return False
    return True

def removeFullRows(app):
    rowsRemoved = 0
    newBoard = []
    for row in app.board:
        if app.emptyColor not in row:
            rowsRemoved += 1
            continue
        else:
            newBoard.append(row)
    for blankRows in range(rowsRemoved):
        newBoard.insert(0,[app.emptyColor] * app.cols)
    app.score += rowsRemoved**2
    app.board = newBoard

################################ VIEW FUNCTIONS ################################

def redrawAll(app, canvas): 
    # for s in ((app.size % 300), ((app.size + 150) % 300)):
    #     canvas.create_text(app.width/2, app.height/2, fill=app.color,
    #                        text=app.label, font=f'Arial {s} bold')
    canvas.create_rectangle(0,0,app.width,app.height, fill = 'orange')
    drawBoard(app,canvas)
    drawFallingPiece(app, canvas)
    drawScore(app, canvas)
    if app.gameOver: drawGameOver(app,canvas)

#https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCellBounds(app, row, col): 
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, canvas, row, col, app.board[row][col])

def drawCell(app, canvas, row, col, color):
    x0,y0,x1,y1 = getCellBounds(app,row,col)
    canvas.create_rectangle(x0,y0,x1,y1, fill = color,
                                    width = 3)

def drawFallingPiece(app, canvas):
    startRow, startCol = app.pieceRowCorner, app.pieceColCorner
    for row in range(app.pieceRows): 
        for col in range(app.pieceCols):
            if app.fallingPiece[row][col]:
                drawCell(app,canvas,(row + startRow),
                        (col + startCol),app.fallingPieceColor)

def placeFallingPiece(app):
    pRC = app.pieceRowCorner
    pCC = app.pieceColCorner
    for row in range(app.pieceRows): 
        for col in range(app.pieceCols):
            if app.fallingPiece[row][col]:
                app.board[pRC+row][pCC+col] = app.fallingPieceColor
    removeFullRows(app)

def drawGameOver(app,canvas):
    for row in range(app.rows)[1:3]:
        for col in range(app.cols):
            drawCell(app, canvas, row, col, 'black')
    s = app.cellSize
    textCenterCol = (s*app.cols)//2 + app.margin
    textCenterRow = 2*s + app.margin
    canvas.create_text(textCenterCol, textCenterRow, fill='yellow',
                       text="Game Over!", font=f'Arial {s} bold')

def drawScore(app,canvas):
    s = 3*app.margin//4
    textCenterCol = (app.cellSize*app.cols)//2 + app.margin
    canvas.create_text(textCenterCol, app.margin/2, fill=app.emptyColor,
                       text = f'Score = {app.score}', font=f'Arial {s} bold')

############################### LAUNCH FUNCTIONS ###############################

def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 40
    margin = 25
    return(rows,cols,cellSize,margin)

def playTetris():
    rows,cols,cellSize,margin = gameDimensions()
    width = cellSize*cols + 2*margin
    height = cellSize*rows + 2*margin
    runApp(width=width, height=height)
    
# print(gameDimensions())
playTetris()


#################################################
# Test Functions
#################################################

def testIsPerfectSquare():
    print('Testing isPerfectSquare(n))...', end='')
    assert(isPerfectSquare(4) == True)
    assert(isPerfectSquare(9) == True)
    assert(isPerfectSquare(10) == False)
    assert(isPerfectSquare(225) == True)
    assert(isPerfectSquare(1225) == True)
    assert(isPerfectSquare(1226) == False)
    print('Passed')


def testIsSortOfSquarish():
    print('Testing isSortOfSquarish(n))...', end='')
    assert(isSortOfSquarish(52) == True)
    assert(isSortOfSquarish(16) == False)
    assert(isSortOfSquarish(502) == False)
    assert(isSortOfSquarish(414) == True)
    assert(isSortOfSquarish(5221) == True)
    assert(isSortOfSquarish(6221) == False)
    assert(isSortOfSquarish(-52) == False)
    print('Passed')


def testNthSortOfSquarish():
    print('Testing nthSortOfSquarish()...', end='')
    assert(nthSortOfSquarish(0) == 52)
    assert(nthSortOfSquarish(1) == 61)
    assert(nthSortOfSquarish(2) == 63)
    assert(nthSortOfSquarish(3) == 94)
    assert(nthSortOfSquarish(4) == 252)
    assert(nthSortOfSquarish(8) == 522)
    print('Passed')

# def testAll():
#     testIsPerfectSquare()
#     testIsSortOfSquarish()
#     testNthSortOfSquarish()

#################################################
# main
#################################################

# def main():
#     cs112_f21_week6_linter.lint()
#     s21Midterm1Animation()
#     playTetris()
#     testAll()

# if __name__ == '__main__':
#     main()
