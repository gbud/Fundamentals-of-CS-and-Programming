def wordSearch(board, word):
    (rows, cols) = (len(board), len(board[0]))
    for row in range(rows):
        for col in range(cols):
            result = wordSearchFromCell(board, word, row, col)
            if (result != None):
                return result
    return None

def wordSearchFromCell(board, word, startRow, startCol):
    for drow in [-1, 0, +1]:
        for dcol in [-1, 0, +1]:
            if (drow, dcol) != (0, 0):
                result = wordSearchFromCellInDirection(board, word,
                                                       startRow, startCol,
                                                       drow, dcol)
                if (result != None):
                    return result
    return None

def wordSearchFromCellInDirection(board, word, startRow, startCol, drow, dcol):
    (rows, cols) = (len(board), len(board[0]))
    dirNames = [ ["up-left"  ,   "up", "up-right"],
                 ["left"     ,   ""  , "right"   ],
                 ["down-left", "down", "down-right" ] ]
    for i in range(len(word)):
        row = startRow + i*drow
        col = startCol + i*dcol
        if ((row < 0) or (row >= rows) or
            (col < 0) or (col >= cols) or
            (board[row][col] != word[i])):
            return None
    return (word, (startRow, startCol), dirNames[drow+1][dcol+1])

#----------------------------------------------------------------

from cmu_112_graphics import *

def appStarted(app):
    app.rows, app.cols = 6,7
    app.margin = 20
    app.currPlayer = 0
    app.player0Color = "red"
    app.player1Color = 'blue'
    app.board = initializeBoard(app)
    app.gameOver = False

def initializeBoard(app):
    return [[None]*app.cols for i in range(app.rows)] #2d list of none values

def checkForWin(app, letter):
    pass

def mousePressed(app,event):
    if app.gameOver: return
    (row,col) = getCell(app,event.x,event.y)
    bestRowPosition = lowestPositionInColumn(app,col)

def pointInGrid(app, x, y):
    # return True if (x, y) is inside the grid defined by app.
    return ((app.margin <= x <= app.width-app.margin) and
            (app.margin <= y <= app.height-app.margin))

def getCell(app, x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(app, x, y)):
        return (-1, -1)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)

    return (row, col)

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

def redrawAll(app, canvas):
    return 42

runApp(width=800, height=800)