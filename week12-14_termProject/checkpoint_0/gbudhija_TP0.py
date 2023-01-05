from cmu_112_graphics import *
from dataclasses import make_dataclass
import math

class Skater(object):
    def __init__(self, app, spriteStrip):
        self.spriteStrip = app.loadImage(spriteStrip)
        self.sprites = []
        self.spriteCounter = 0
        self.state = 'cruise'
        self.x = app.width//2
        self.y = app.height*3/4
    def addSpriteCount(self):
        self.spriteCounter = (1 + self.spriteCounter) % len(self.sprites)
    def cruise(self):
        self.state = 'cruise'
        self.spriteCounter = 0
        self.sprites = []
        for i in range(6):
            sprite = self.spriteStrip.crop((80*i, 246, 80+80*i, 326))
            self.sprites.append(sprite)
    def push(self):
        self.state = 'push'
        self.spriteCounter = 0
        self.sprites = []
        for i in range(13):
            sprite = self.spriteStrip.crop((80*i, 571, 80+80*i, 651))
            self.sprites.append(sprite)
    def ollie(self):
        self.state = 'air'
        self.spriteCounter = 0
        self.sprites = []
        for i in range(10):
            sprite = self.spriteStrip.crop((817+80*i, 803, 897+80*i, 883))
            self.sprites.append(sprite)
        for i in range(3):
            sprite = self.spriteStrip.crop((1214+81*i, 571, 1294+81*i, 651))
            self.sprites.append(sprite)
    def treFlip(self):
        self.state = 'flip'
        self.spriteCounter = 0
        self.sprites = []
        for i in range(13):
            sprite = self.spriteStrip.crop((300+100*i, 953, 380+100*i, 1033))
            self.sprites.append(sprite)


class Obstacle(object):
    def __init__(self, app, obsX0, obsY0, obsX1, obsY1):
        self.obsSheet = app.loadImage('sprites/obstacleSpriteSheetEdit.png')
        # cone image modified from https://www.pinclipart.com/picdir/middle/187-1874147_traffic-cone-spaceship-pixel-art-png-clipart.png
        self.obsX = app.width + 80
        self.obsY = app.height * 3/4
        self.obsX0 = obsX0
        self.obsY0 = obsY0
        self.obsX1 = obsX1
        self.obsY1 = obsY1
        self.obsImage = self.obsSheet.crop((obsX0, obsY0, obsX1, obsY1))
    def moveObstacle(self):
        pass

def appStarted(app):
    app.skater = Skater(app, 'sprites/defaultSpriteSheetEdit.png')
    # skater sprite sheet from https://www.gamedevmarket.net/asset/skater-sprites/ 
    app.skater.cruise()
    app.cone = Obstacle(app, 0, 0, 80, 80)
    app.speed = 0
    
def keyPressed(app, event):
    if event.key == 'Right' and app.skater.state == 'cruise':
        app.skater.push()
    elif event.key == 'Right' and app.skater.state == 'push':
        if app.skater.spriteCounter >= (len(app.skater.sprites)-2):
            app.skater.push()
    if event.key == 'f' and app.skater.state != 'flip':
        app.skater.treFlip() 
    if event.key == 'Space' and app.skater.state != 'air':
        app.skater.ollie()
    if event.key == 'Left':
        if app.speed >= 2.0:
            app.speed -= 2.0

def timerFired(app):
    app.skater.addSpriteCount()
    if app.skater.state != 'cruise':
        if app.skater.spriteCounter == (len(app.skater.sprites) - 1):
            app.skater.cruise()
    if app.skater.state == 'air': 
        jump = [-40,-20,-10,-5,0,0,5,10,20,0,0,0,0,0]
        app.skater.y += jump[app.skater.spriteCounter]
    if app.skater.state == 'flip': 
        jump = [-40,-20,-10,-5,0,0,5,10,20,0,0,0,0]
        app.skater.y += jump[app.skater.spriteCounter]
    if app.skater.state == 'push':
        if app.skater.spriteCounter == 8:
            app.speed += 15.0
        if app.speed >= 45.0:
            app.speed = 30.0
    app.speed -= 0.2
    if app.speed <= 0.0:
        app.speed = 0.0
    app.cone.obsX -= app.speed
    if app.cone.obsX <= -80: app.cone.obsX = app.width + 80
    
def redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width, app.height, fill = 'LightSkyBlue1')
    canvas.create_text(app.width/2, 20, text = f'speed = {round(app.speed)}')
    drawSkater(app, canvas)
    drawGround(app, canvas)
    drawObstacle(app, canvas)

def drawGround(app, canvas):
    canvas.create_rectangle(0, (app.height*3/4 + 40), app.width, (app.height), fill = 'grey50')

def drawSkater(app, canvas):
    sprite = app.skater.sprites[app.skater.spriteCounter]
    canvas.create_image(app.skater.x, app.skater.y, image=ImageTk.PhotoImage(sprite))

def drawObstacle(app, canvas):
    canvas.create_image(app.cone.obsX, app.cone.obsY, image=ImageTk.PhotoImage(app.cone.obsImage))

runApp(width=600, height=400)
