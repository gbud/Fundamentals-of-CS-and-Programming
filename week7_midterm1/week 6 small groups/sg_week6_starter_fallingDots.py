from cmu_112_graphics import *

def appStarted(app):
    #initialize begining
    initialDot = (app.width//2,app.height//2)
    #create list
    #list of coordinates
    app.bubbles = [initialDot]
    #initialize some variables
    app.radius = 20
    #timer delay
    app.timerdelay = 100
    #other variables
    app.isPaused = False

def mousePressed(app, event):
    cx = event.x
    cy = event.y
    app.bubbles.append((cx,cy))

def keyPressed(app, event):
    #when we press P
    if event.key.lower() == 'p':
        #game is paused or not paused
        #negating whatever paused state you are currently at
        app.isPaused = not app.isPaused

def moveDots(app):
    if app.isPaused: return
    remaining = []
    for (cx,cy) in app.bubbles:
        newX,newY = (cx, cy +5) #moving down
        if newY + app.radius < app.height:
            remaining.append((newX,newY))
    app.bubbles = remaining

def timerFired(app):
    moveDots(app) #move down y

def redrawAll(app, canvas):
    drawBubble(app,canvas)

def drawBubble(app,canvas):
    for i in app.bubbles:
        x = app.bubbles[i][0]
        y = app.bubbles[i][1]
        canvas.create_oval(x-app.radius, y-app.radius, )

runApp(width=800, height=800)