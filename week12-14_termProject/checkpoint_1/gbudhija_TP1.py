# Your name: Greg Budhijanto
# Your andrew id: gbudhija

from cmu_112_graphics import *
from dataclasses import make_dataclass
import math
import random

class Skater(object):
    def __init__(self, app, spriteStrip):
        # sprite sheet codes modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#spritesheetsWithCropping
        self.spriteStrip = app.loadImage(spriteStrip)
        self.sprites = []
        self.spriteCounter = 0
        self.state = 'cruise'
        self.x = app.width/2
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
    def brake(self): # need to work out
        self.state = 'break'
        self.spriteCounter = 0
        self.sprites = []
        for i in range(8):
            sprite = self.spriteStrip.crop((80*9, 571, 80+80*9, 651))
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
    def kickFlip(self): #landing sprites
        self.state = 'flip'
        self.spriteCounter = 0
        self.sprites = []
        for i in range(10):
            sprite = self.spriteStrip.crop((1627+80*i, 803, 1707+80*i, 883))
            self.sprites.append(sprite)
        for i in range(3): #landing sprites
            sprite = self.spriteStrip.crop((1214+81*i, 571, 1294+81*i, 651))
            self.sprites.append(sprite)
    def treFlip(self):
        self.state = 'flip'
        self.spriteCounter = 0
        self.sprites = []
        for i in range(13):
            sprite = self.spriteStrip.crop((300+100*i, 953, 380+100*i, 1033))
            self.sprites.append(sprite)
    def bail(self, app):
        self.state = 'bail'
        app.bailSpeed = app.run
        self.spriteCounter = 0
        self.sprites = []
        for i in range(25):
            sprite = self.spriteStrip.crop((0+100*i, 490, 100+100*i, 570))
            self.sprites.append(sprite)

class Obstacle(object):
    def __init__(self, app, name, obsX0, obsY0, obsX1, obsY1):
        self.obsSheet = app.loadImage('sprites/obstacleSpriteSheetEdit.png')
        # cone image modified from https://www.pinclipart.com/picdir/middle/187-1874147_traffic-cone-spaceship-pixel-art-png-clipart.png
        self.name = name
        self.obsX = app.width + 80
        self.obsY = app.height * 3/4
        self.obsX0 = obsX0
        self.obsY0 = obsY0
        self.obsX1 = obsX1
        self.obsY1 = obsY1
        self.obsImage = self.obsSheet.crop((obsX0, obsY0, obsX1, obsY1))
    def moveObstacle(self, app):
        self.obsX -= app.run

class Terrain(object):
    def __init__(self, terX0, terY0, terX1, terY1, angle):
        self.terX0 = terX0
        self.terY0 = terY0
        self.terX1 = terX1
        self.terY1 = terY1
        self.angle = angle
    def moveTerrainX(self, app):
        self.terX0 -= app.run
        self.terX1 -= app.run
    def moveTerrainY(self, app):
        self.terY0 += app.rise
        self.terY1 += app.rise

def appStarted(app):
    app.skater = Skater(app, 'sprites/defaultSpriteSheetEdit.png')
    # skater sprite sheet from https://www.gamedevmarket.net/asset/skater-sprites/ 
    app.skater.cruise()
    app.obstacles = []
    # addObstacle(app)
    app.run = 0
    app.rise = 0
    app.rotation = 0
    app.terrainAngle = 0
    app.lineY = app.height*3/4 + 40 #constant where line should be on screen
    app.terrains = [(Terrain(0, app.lineY, app.width, app.lineY, 0))] #initial flat line
    app.skatedTerrains = []
    app.bailSpeed = 0
    for i in range(10):
        addTerrain(app)

def addObstacle(app):
    cone = 'cone', 0, 0, 80, 80
    table = 'table', 81, 0, 161, 80
    obstacleList = [table]
    randomIndex = random.randint(0, len(obstacleList)-1)
    name, x0, y0, x1, y1 = obstacleList[randomIndex]
    obstacle = Obstacle(app, name, x0, y0, x1, y1)
    app.obstacles.append(obstacle)

def addTerrain(app):
    increment = app.width/4
    # flat = (   last terrain's X1,      last terrain's Y1,      last terrain's X1 + new width,      last terrain's Y1, angle)
    flat = (app.terrains[-1].terX1, app.terrains[-1].terY1, (app.terrains[-1].terX1+increment), app.terrains[-1].terY1, 0)
    angleList = [-30,-15,15,30] #angles in degrees
    randomIndex = random.randint(0, len(angleList)-1) 
    slopeAngle = math.radians(angleList[randomIndex]) # random angle convert to radians
    drop = increment*(math.tan(slopeAngle)) # change in y based on converted random angle
    # slope = (   last terrain's X1,      last terrain's Y1,      last terrain's X1 + new width,      last terrain's Y1 + drop,      angle)
    slope = (app.terrains[-1].terX1, app.terrains[-1].terY1, (app.terrains[-1].terX1+increment), (app.terrains[-1].terY1+drop), slopeAngle)
    terrainList = [flat, slope] 
    randomIndex = random.randint(0, len(terrainList)-1)
    x0, y0, x1, y1, angle = terrainList[randomIndex] # random pick between terrains
    terrain = Terrain(x0, y0, x1, y1, angle)
    app.terrains.append(terrain)
    
def keyPressed(app, event):
    if event.key == 'Right' and app.skater.state == 'cruise':
        app.skater.push()
    elif event.key == 'Right' and app.skater.state == 'push':
        if app.skater.spriteCounter >= (len(app.skater.sprites)-2):
            app.skater.push()
    if event.key == 'f' and app.skater.state != 'flip' and app.skater.state != 'air' and app.skater.spriteCounter < 9:
        app.skater.kickFlip() 
    if event.key == 'd' and app.skater.state != 'flip' and app.skater.state != 'air' and app.skater.spriteCounter < 9:
        app.skater.treFlip() 
    if event.key == 'Space' and app.skater.state != 'air' and app.skater.state != 'flip' and app.skater.spriteCounter < 9:
        app.skater.ollie()
    if event.key == 'Left' and app.skater.state != 'air' and app.skater.state != 'flip':
        app.skater.brake()
        if app.run >= 2.0:
            app.run -= 2.0

def timerFired(app):
    # skater updates per timer fired
    app.skater.addSpriteCount()
    if app.skater.state != 'cruise':
        if app.skater.spriteCounter == (len(app.skater.sprites) - 1):
            app.skater.cruise()
    if app.skater.state == 'air': 
        jump = [0,-20,-10,-5,0,0,5,10,20,0,0,0,0]
        app.skater.y += jump[app.skater.spriteCounter]
    if app.skater.state == 'flip': 
        jump = [0,-20,-10,-5,0,0,5,10,20,0,0,0,0]
        app.skater.y += jump[app.skater.spriteCounter]
    if app.skater.state == 'push':
        if app.skater.spriteCounter == 8:
            app.run += 15.0
        if app.run >= 45.0:
            app.run = 45.0
    if app.skater.state == 'bail':
        cs = app.bailSpeed #cs = speed at Vo
        bailFrames = [cs, cs*15/16, cs*14/16, cs*13/16, cs*12/16, cs*11/16, cs*10/16, cs*9/16, cs*8/16,
                      cs*7/16, cs*6/16, cs*5/16, cs*4/16, cs*3/16, cs*2/16, cs*1/16, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        app.run = bailFrames[app.skater.spriteCounter]
    if app.rotation == 0 and app.skater.state != 'bail':
        app.run -= 0.2
    elif app.rotation > 0:
        app.run += 1.0
    elif app.rotation < 0:
        app.run -= 1.0
    if app.run <= 0.0:
        app.run = 0.0

    # obstacle updates per timer fired
    for obstacle in app.obstacles:
        obstacle.moveObstacle(app)
        if obstacle.obsX <= -80: 
            app.obstacles.remove(obstacle)
            addObstacle(app)

    # collision check
    # if app.obstacles[0].name == 'cone':
    #     if app.obstacles[0].obsX < app.width/2 + 10 and app.obstacles[0].obsX > app.width/2 - 10:
    #         if app.skater.y < app.obstacles[0].obsY - 19:
    #             app.skater.bail(app)
    #             app.skater.y = app.height*3/4
    # if app.obstacles[0].name == 'table':
    #     pass

    # terrain updates per timer fired
    app.terrainAngle = app.terrains[0].angle # app.terrain[0] is shifting terrain
    app.rotation = math.degrees(app.terrainAngle)
    if app.terrains[0].terX1 <= app.width/2: # terrain becomes skated when it passes linePoint
        app.skatedTerrains.append(app.terrains[0])
        app.terrains.pop(0)
    yShiftCalc(app, app.terrains[0])
    for terrain in app.terrains:
        terrain.moveTerrainX(app)
        terrain.moveTerrainY(app)
    for skatedTerrain in app.skatedTerrains:
        skatedTerrain.moveTerrainX(app)
        skatedTerrain.moveTerrainY(app)
        if skatedTerrain.terX1 <= (0-app.width):
            app.skatedTerrains.remove(skatedTerrain)
            addTerrain(app)

def yShiftCalc(app, terrain):
    m = (terrain.terY1 - terrain.terY0) / (terrain.terX1 - terrain.terX0)
    b = terrain.terY0 - m * terrain.terX0
    testY = m * app.width/2 + b
    difference = app.lineY - testY
    app.rise = difference

def redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.width, app.height, fill = 'LightSkyBlue1')
    canvas.create_text(app.width/2, 20, text = f'terrains = {len(app.terrains)}')
    canvas.create_text(app.width/2, 40, text = f'speed = {round(app.run)}')
    canvas.create_text(app.width/2, 60, text = f'rotation = {round(app.rotation)}')
    # canvas.create_text(app.width/2, 80, text = f'obstacles = {app.obstacles[0].name}')
    drawTerrain(app, canvas)
    drawSkater(app, canvas)
    drawObstacle(app, canvas)
    canvas.create_oval(app.skater.x-2, app.skater.y-2, app.skater.x+2, app.skater.y+2, fill='red')
    # canvas.create_oval(app.width/2-2, app.lineY-2, app.width/2+2, app.lineY+2, fill='red')

def drawSkater(app, canvas):
    # canvas.create_image(app.cone.obsX, app.cone.obsY, image=rotateImage)
    rotation = 0 - app.rotation
    sprite = app.skater.sprites[app.skater.spriteCounter]
    rotateImage = ImageTk.PhotoImage(sprite.rotate(rotation))
    # shift based on rotation
    shiftRads = math.radians(app.rotation)
    shiftY = 40 - (40 * math.cos(shiftRads))
    shiftX = 40 * math.sin(shiftRads)
    canvas.create_image(app.skater.x + shiftX, app.skater.y + shiftY, image = rotateImage)

def drawObstacle(app, canvas):
    # image=app.cone.obsImage
    # rotateImage = ImageTk.PhotoImage(image.rotate(app.rotation))
    # canvas.create_image(app.cone.obsX, app.cone.obsY, image=rotateImage)
    for obstacle in app.obstacles:
        canvas.create_image(obstacle.obsX, obstacle.obsY, image=ImageTk.PhotoImage(obstacle.obsImage))
        canvas.create_oval(obstacle.obsX-2, obstacle.obsY-2, obstacle.obsX+2, obstacle.obsY+2, fill='red')

def drawTerrain(app, canvas):
    for terrain in app.terrains:
        canvas.create_polygon(terrain.terX0+app.run, terrain.terY0, terrain.terX1+app.run, terrain.terY1,
                              terrain.terX1+app.run, app.height, terrain.terX0+app.run, app.height, fill = 'grey50')
        canvas.create_line(terrain.terX0+app.run, terrain.terY0, terrain.terX1+app.run, terrain.terY1)
    for skatedTerrain in app.skatedTerrains:
        canvas.create_polygon(skatedTerrain.terX0+app.run, skatedTerrain.terY0, skatedTerrain.terX1+app.run, skatedTerrain.terY1,
                              skatedTerrain.terX1+app.run, app.height, skatedTerrain.terX0+app.run, app.height, fill = 'grey50')
        canvas.create_line(skatedTerrain.terX0+app.run, skatedTerrain.terY0, skatedTerrain.terX1+app.run, skatedTerrain.terY1)

runApp(width=600, height=1000)
