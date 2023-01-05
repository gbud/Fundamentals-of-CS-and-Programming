# Your name: Greg Budhijanto
# Your andrew id: gbudhija

from cmu_112_graphics import *
from dataclasses import make_dataclass
import math
import random
import time

class Skater(object):
    def __init__(self, app, spriteStrip):
        # sprite sheet codes modified from https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#spritesheetsWithCropping
        self.spriteStrip = app.loadImage(spriteStrip)
        self.sprites = []
        self.spriteCounter = 0
        self.state = 'cruise'
        self.x = app.width/2
        self.y = app.height*3/4
        self.boardY = self.y + 40
    def addSpriteCount(self):
        self.spriteCounter = (1 + self.spriteCounter) % len(self.sprites)
    def cruise(self):
        self.state = 'cruise'
        self.spriteCounter = 0
        self.sprites = []
        for i in range(6):
            sprite = self.spriteStrip.crop((80*i, 246, 80+80*i, 326))
            self.sprites.append(sprite)
    def push(self, app):
        app.collisionToggle = False
        app.pushToggle = True
        self.state = 'push'
        self.spriteCounter = 0
        self.sprites = []
        for i in range(13):
            sprite = self.spriteStrip.crop((80*i, 571, 80+80*i, 651))
            self.sprites.append(sprite)
    def brake(self, app): # need to work out
        self.state = 'brake'
        self.spriteCounter = 0
        self.sprites = []
        for i in range(8):
            sprite = self.spriteStrip.crop((80*9, 571, 80+80*9, 651))
            self.sprites.append(sprite)
    def ollie(self, app):
        app.ollieToggle = True
        app.toggle = True
        self.state = 'air'
        self.spriteCounter = 0
        self.sprites = []
        for i in range(10):
            sprite = self.spriteStrip.crop((817+80*i, 803, 897+80*i, 883))
            self.sprites.append(sprite)
        for i in range(3):
            sprite = self.spriteStrip.crop((1214+81*i, 571, 1294+81*i, 651))
            self.sprites.append(sprite)
    def kickFlip(self, app): #landing sprites
        app.toggle = True
        app.kickflipUnlockToggle = True
        self.state = 'kickflip'
        self.spriteCounter = 0
        self.sprites = []
        for i in range(10):
            sprite = self.spriteStrip.crop((1627+80*i, 803, 1707+80*i, 883))
            self.sprites.append(sprite)
        for i in range(3): #landing sprites
            sprite = self.spriteStrip.crop((1214+81*i, 571, 1294+81*i, 651))
            self.sprites.append(sprite)
    def treFlip(self, app):
        app.toggle = True
        app.treflipUnlockToggle = True
        self.state = 'treflip'
        self.spriteCounter = 0
        self.sprites = []
        for i in range(13):
            sprite = self.spriteStrip.crop((300+100*i, 953, 380+100*i, 1033))
            self.sprites.append(sprite)
    def bail(self, app):
        app.collisionToggle = True
        app.toggle = False # does not repeat bail if skate and object in same collision area
        if app.skater.state != 'bail':
            app.generatedObstacles.append(app.obstacles[0].name)
        if app.obstacles[0].name == 'cone':
            if app.score > 0:
                app.score -= 1
        if app.obstacles[0].name == 'table':
            if app.score > 1:
                app.score -= 2
            elif app.score == 1:
                app.score -= 1
        self.state = 'bail'
        app.bailSpeed = app.speed # sets initial velocity at collision
        self.spriteCounter = 0
        self.sprites = []
        for i in range(25):
            sprite = self.spriteStrip.crop((0+100*i, 490, 100+100*i, 570))
            self.sprites.append(sprite)
    def clearedObstacle(self, app):
        app.toggle = False
        if app.obstacles[0].name == 'cone':
            if app.skater.state == 'air':
                app.score += 1
            if app.skater.state == 'kickflip':
                app.score += 2
            if app.skater.state == 'treflip':
                app.score += 4
        if app.obstacles[0].name == 'table':
            if app.skater.state == 'air':
                app.score += 2
            if app.skater.state == 'kickflip':
                app.score += 4
            if app.skater.state == 'treflip':
                app.score += 8
        if app.generatedObstacles.count(app.obstacles[0].name) > 1:
            app.generatedObstacles.remove(app.obstacles[0].name)

####################################################################################################################
####################################################################################################################
####################################################################################################################

class Obstacle(object):
    def __init__(self, app, name):
        self.obsSheet = app.loadImage('sprites/obstacleSpriteSheetEdit.png')
        # cone image modified from https://www.pinclipart.com/picdir/middle/187-1874147_traffic-cone-spaceship-pixel-art-png-clipart.png
        self.name = name
        for i in range(3,len(app.terrains)):
            if app.terrains[i].angle == 0:
                self.obsX = (app.terrains[i].terX0+app.terrains[i].terX1)/2
                self.obsY = app.terrains[i].terY0
                break
        if name == 'cone':
            self.obsTop = self.obsY + 21
            x0, y0, x1, y1 = 0, 0, 80, 80
        elif name == 'table':
            self.obsTop = self.obsY + 10
            x0, y0, x1, y1 = 81, 0, 161, 80
        self.obsImage = self.obsSheet.crop((x0, y0, x1, y1))
    def moveObstacleX(self, app):
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

####################################################################################################################
####################################################################################################################
####################################################################################################################

def appStarted(app):
    app.welcomeImage = app.loadImage('sprites/thrasherlogo2.png')
    app.mainMenuImage = app.loadImage('sprites/main_menu2.png')
    app.finalImage = app.loadImage('sprites/finalScorePage.png')
    app.scoreAndTimeImage = app.loadImage('sprites/scoreAndTime.png')
    app.highScoresImage = app.loadImage('sprites/highscores.png')
    app.timeTrialImage = app.loadImage('sprites/timeTrial.png')
    app.gameState = 'welcome'
    app.kickflipToggle = False
    app.kickflipUnlockToggle = False
    app.treflipToggle = False
    app.treflipUnlockToggle = False
    app.gameDifficulty = None
    getHighScores(app)

def instructionToggles(app):
    app.instructionsImage = app.loadImage('sprites/tutorial.png')
    app.pushToggle = False
    app.ollieToggle = False
    app.collisionToggle = False
    app.clearedToggle = False

def gameStart(app):
    app.skater = Skater(app, 'sprites/defaultSpriteSheetEdit.png')
    # skater sprite sheet from https://www.gamedevmarket.net/asset/skater-sprites/ 
    app.skater.cruise()
    app.obstacles = []
    if app.gameState == 'instructions' or app.gameDifficulty == 'easy':
        app.generatedObstacles = ['cone']
    else:
        app.generatedObstacles = ['cone', 'table']
    app.gravity = -9.8      # meters/second
    app.run = 0             # pixels/millisecond
    app.rise = 0            # pixels/millisecond
    app.speed = 0           # meters/second
    app.bailSpeed = 0       # meters/second
    app.rotation = 0        # degrees
    app.terrainAngle = 0    # radians
    app.lineY = app.height*3/4 + 40 #constant where line should be on screen
    app.terrains = [(Terrain(0, app.lineY, app.width, app.lineY, 0))] #initial flat line
    app.skatedTerrains = []
    app.toggle = False
    for i in range(10):
        addTerrain(app)
    addObstacle(app)
    app.score = 0
    app.finalScore = 0
    app.newHighScoreToggle = False
    app.initialTime = time.time()
    app.timer = 0
    if app.gameState == 'instructions':
        app.setTime = None
    elif app.gameState == 'game':
        app.setTime = 30

# modified from https://stackoverflow.com/questions/50829786/python-record-score-user-and-display-top-10
def writeHighScore(app, name, score):
    with open('highscores.txt','a') as file:
        file.write(name + " " + str(score) + "\n")

# modified from https://stackoverflow.com/questions/50829786/python-record-score-user-and-display-top-10
def getHighScores(app):
    file = open('highscores.txt').readlines()
    app.highScores = []
    for line in file:
        name, score = line.split()[0], int(line.split()[1])
        app.highScores.append((name,score))
    app.highScores.sort(key=lambda t: t[1], reverse=True)

def metersToPixels(app, meters):
    # skater height = 61 pixels or 1.75 meters
    # 1 meter = 34.86 pixels
    return meters*61/1.75

def addObstacle(app):
    randomIndex = random.randint(0, len(app.generatedObstacles)-1)
    name = app.generatedObstacles[randomIndex]
    obstacle = Obstacle(app, name)
    app.obstacles.append(obstacle)

def addTerrain(app):
    increment = app.width/4
    # flat = (   last terrain's X1,      last terrain's Y1,      last terrain's X1 + new width,      last terrain's Y1, angle)
    flat = (app.terrains[-1].terX1, app.terrains[-1].terY1, (app.terrains[-1].terX1+increment), app.terrains[-1].terY1,     0)
    if app.gameDifficulty == 'medium':
        angleList = [-15,15] #angles in degrees
    if app.gameDifficulty == 'hard':
        angleList = [-30,-15,15,30]
    if app.gameDifficulty == 'medium' or app.gameDifficulty == 'hard':
        randomIndex = random.randint(0, len(angleList)-1) 
        slopeAngle = math.radians(angleList[randomIndex]) # random angle convert to radians
        drop = increment*(math.tan(slopeAngle)) # change in y based on converted random angle
        # slope = (   last terrain's X1,      last terrain's Y1,      last terrain's X1 + new width,      last terrain's Y1 + drop,      angle)
        slope = (app.terrains[-1].terX1, app.terrains[-1].terY1, (app.terrains[-1].terX1+increment), (app.terrains[-1].terY1+drop), slopeAngle)
    if app.terrains[-1].angle == 0:
        if app.gameState == 'instructions' or app.gameDifficulty == 'easy':
            x0, y0, x1, y1, angle = flat
        else:
            x0, y0, x1, y1, angle = slope 
    else:
        x0, y0, x1, y1, angle = flat 
    terrain = Terrain(x0, y0, x1, y1, angle)
    app.terrains.append(terrain)

####################################################################################################################
####################################################################################################################
####################################################################################################################
    
def keyPressed(app, event):

    if app.gameState == 'welcome':
        if event.key == 'r':
            app.gameState = 'main menu'

    if app.gameState == 'main menu':
        if event.key == 'u':
            app.gameState = 'instructions'
            instructionToggles(app)
            gameStart(app)
        elif event.key == 't':
            app.gameState = 'time trial'
        elif event.key == 'h':
            app.gameState = 'high scores'
            getHighScores(app)

    if app.gameState == 'time trial':
        if event.key == 'e':
            app.gameState = 'game'
            app.gameDifficulty = 'easy'
            gameStart(app)
        if event.key == 'd':
            app.gameState = 'game'
            app.gameDifficulty = 'medium'
            gameStart(app)
        if event.key == 'h':
            app.gameState = 'game'
            app.gameDifficulty = 'hard'
            gameStart(app)
        if event.key == 'm':
            app.gameState = 'main menu'

    if app.gameState == 'high scores':
        if event.key == 'm':
            app.gameState = 'main menu'

    elif app.gameState == 'game' or app.gameState == 'instructions':
        if event.key == 'Right' and app.skater.state == 'cruise':
            app.skater.push(app)
        elif event.key == 'Right' and app.skater.state == 'push':
            if app.skater.spriteCounter >= (len(app.skater.sprites)-2):
                app.skater.push(app)
        if (app.skater.state != 'air' and app.skater.state != 'kickflip' and 
            app.skater.state != 'treflip' and app.skater.spriteCounter < 9):
            if event.key == 'f':
                if app.kickflipToggle == True:
                    app.skater.kickFlip(app) 
            if event.key == 'd':
                if app.treflipToggle == True:
                    app.skater.treFlip(app) 
            if event.key == 'Space':
                app.skater.ollie(app)
        if (event.key == 'Left' and app.skater.state != 'air' and app.skater.state != 'kickflip' and app.skater.state != 'treflip'):
            app.skater.brake(app)
            if app.speed >= 1:
                app.speed -= 1
            if app.speed <= 1:
                app.speed += 1
        if event.key == 'm':
            app.gameState = 'main menu'
        if app.gameState != 'instructions':
            if event.key == 'r':
                app.gameState = 'game'
                gameStart(app)
    elif app.gameState == 'final score':
        if event.key == 'r':
            app.gameState = 'game'
            gameStart(app)
        if event.key == 'm':
            app.gameState = 'main menu'

####################################################################################################################
####################################################################################################################
####################################################################################################################

def timerFired(app):
    checkNewHighScore(app)
    if app.gameState == 'game' or app.gameState == 'instructions':
        if app.gameState == 'instructions':
            checkInstructions(app)
        checkTimer(app)
        app.skater.addSpriteCount()
        updateSkaterState(app)
        updateSpeed(app)
        collisionCheck(app)
        updateRotation(app)
        updateTerrain(app)
        updateObstacles(app)
        updateTimer(app)

def checkInstructions(app):
    if app.score >= 6:
        app.kickflipToggle = True
    if app.score >= 14:
        app.generatedObstacles = ['table']
    if app.score >= 30:
        app.generatedObstacles = ['cone','table']

def checkTimer(app):
    if app.gameState == 'game' and app.timer > app.setTime:
        app.gameState = 'final score'
        app.speed = 0
        app.finalScore = app.score
        if app.finalScore >= 10:
            app.kickflipToggle = True
        if app.finalScore >= 25:
            app.treflipToggle = True
 
def checkNewHighScore(app):
    if app.gameState == 'final score' and app.newHighScoreToggle == False:
        if app.finalScore > app.highScores[7][1]:
            validName = False
            while validName == False:
                name = app.getUserInput("NEW HIGH SCORE: ENTER UP TO 3 INITALS")
                if len(name) > 3:
                    continue
                else:
                    phrases = ['GNARLY DUDE!!!', 'SICK SCORE BRO!!!', "YOU'RE SHREDDING IT!!", "YOU'RE KILLING IT OUT THERE!!"]
                    randomIndex = random.randint(0, len(phrases)-1) 
                    randomPhrase = phrases[randomIndex]
                    app.showMessage(f'{randomPhrase}')
                    validName = True
                    app.newHighScoreToggle = True
                    writeHighScore(app, name.upper(), app.finalScore)

def updateTimer(app):
    if app.gameState == 'game':
        elapsedTime = time.time() - app.initialTime
        app.timer = elapsedTime

def updateSkaterState(app):
    if app.skater.state != 'cruise':
        if app.skater.spriteCounter == (len(app.skater.sprites) - 1):
            app.skater.cruise()
    if app.skater.state == 'air' or app.skater.state == 'kickflip' or app.skater.state == 'treflip': 
        jump = [0,-20,-10,-5,0,0,5,10,20,0,0,0,0]
        app.skater.y += jump[app.skater.spriteCounter]
        app.skater.boardY = app.skater.y + 40
        if app.skater.spriteCounter > 8:
            app.skater.state = 'land'
    if app.skater.state == 'land':
        land = [0,-20,-10,-5,0,0,5,10,20,0,0,0,0]
        app.skater.y += land[app.skater.spriteCounter]
        app.toggle = False        
    if app.skater.state == 'push':
        if app.skater.spriteCounter == 8: # when skater's foot hits floor
            app.speed += 4 #meters/second
    if app.skater.state == 'bail':
        cs = app.bailSpeed #cs = speed at Vo
        bailFrames = [cs, cs*15/16, cs*14/16, cs*13/16, cs*12/16, cs*11/16, cs*10/16, cs*9/16, cs*8/16,
                      cs*7/16, cs*6/16, cs*5/16, cs*4/16, cs*3/16, cs*2/16, cs*1/16, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        app.speed = bailFrames[app.skater.spriteCounter]
    if app.rotation == 0 and app.skater.state != 'bail' and app.speed > 0:
        app.speed -= 0.05
    elif app.rotation == 0 and app.skater.state != 'bail' and app.speed < 0:
        app.speed += 0.05
    elif app.rotation != 0:
        slopeSpeed = app.gravity * math.tan(app.terrainAngle)
        horizontalSpeed = slopeSpeed * math.cos(app.terrainAngle)
        horizontalSpeedPerTimerFired = horizontalSpeed/10
        app.speed -= horizontalSpeedPerTimerFired

def updateSpeed(app):
    pixelSpeed = metersToPixels(app, app.speed)
    pixelSpeedPerTimerFired = pixelSpeed/10
    app.run = pixelSpeedPerTimerFired

def collisionCheck(app):
    if ((app.skater.state == 'cruise' or app.skater.state == 'push' or app.skater.state == 'land') and 
        (app.obstacles[0].obsX <= app.width/2 and app.obstacles[0].obsX > app.width/2-app.run)):
        app.skater.bail(app)
        app.skater.y = app.height*3/4
    elif app.obstacles[0].name == 'cone' and app.toggle == True:
        if app.obstacles[0].obsX < app.width/2 + 10 and app.obstacles[0].obsX > app.width/2 - 10:
            if app.skater.boardY > app.obstacles[0].obsTop and app.skater.state != 'bail':
                app.skater.bail(app)
                app.skater.y = app.height*3/4
        if app.obstacles[0].obsX < app.width/2 + 20 and app.obstacles[0].obsX > app.width/2 - 20:
            if app.skater.boardY < app.obstacles[0].obsTop and (app.skater.state == 'air' or 
                                                                app.skater.state == 'kickflip' or
                                                                app.skater.state == 'treflip'):
                app.skater.clearedObstacle(app)
    elif app.obstacles[0].name == 'table' and app.toggle == True:
        if (app.obstacles[0].obsX < app.width/2 + 14 and app.obstacles[0].obsX > app.width/2 - 14):
            if app.skater.boardY > app.obstacles[0].obsTop and app.skater.state != 'bail':
                app.skater.bail(app)
                app.skater.y = app.height*3/4
            elif app.skater.boardY < app.obstacles[0].obsTop and (app.skater.state == 'air' or 
                                                                  app.skater.state == 'kickflip' or
                                                                  app.skater.state == 'treflip'):
                app.skater.clearedObstacle(app)
        elif (app.obstacles[0].obsX < app.width/2 + 28 and app.obstacles[0].obsX > app.width/2 - 28):
            if app.skater.boardY > app.obstacles[0].obsTop+13 and app.skater.state != 'bail':
                app.skater.bail(app)
                app.skater.y = app.height*3/4
            elif app.skater.boardY < app.obstacles[0].obsTop and (app.skater.state == 'air' or 
                                                                  app.skater.state == 'kickflip' or
                                                                  app.skater.state == 'treflip'):
                app.skater.clearedObstacle(app)
    
def updateRotation(app):
    if app.skater.state != 'air' and app.skater.state != 'kickflip' and app.skater.state != 'treflip':
        app.terrainAngle = app.terrains[0].angle # app.terrain[0] is shifting terrain
    else:
        if app.terrains[0].angle == 0 or app.skater.spriteCounter > 7:
            app.terrainAngle = app.terrains[0].angle
    app.rotation = math.degrees(app.terrainAngle)

def updateTerrain(app):
    if app.terrains[0].terX1 <= app.width/2: # terrain becomes skated when it passes linePoint
        app.skatedTerrains.append(app.terrains[0])
        app.terrains.pop(0)
    if len(app.skatedTerrains) != 0:
        if app.skatedTerrains[-1].terX1 > app.width/2:
            app.terrains.insert(0, app.skatedTerrains[-1])
            app.skatedTerrains.pop()
    yShiftCalc(app, app.terrains[0])
    for terrain in app.terrains:
        terrain.moveTerrainX(app)
        terrain.moveTerrainY(app)
    for skatedTerrain in app.skatedTerrains:
        skatedTerrain.moveTerrainX(app)
        skatedTerrain.moveTerrainY(app)
        if skatedTerrain.terX1 <= (0-2*app.width):
            app.skatedTerrains.remove(skatedTerrain)
        if skatedTerrain.terX1 <= (0-app.width) and len(app.terrains) < 6:
            addTerrain(app)

def yShiftCalc(app, terrain):
    m = (terrain.terY1 - terrain.terY0) / (terrain.terX1 - terrain.terX0)
    b = terrain.terY0 - m * terrain.terX0
    testY = m * app.width/2 + b
    difference = app.lineY - testY
    app.rise = difference

def updateObstacles(app):
    for obstacle in app.obstacles:
        obstacle.moveObstacleX(app)
        for skatedTerrain in app.skatedTerrains:
            if obstacle.obsX > skatedTerrain.terX0 and obstacle.obsX < skatedTerrain.terX1:
                obstacle.obsY = skatedTerrain.terY0-40
        for terrain in app.terrains:
            if obstacle.obsX > terrain.terX0 and obstacle.obsX < terrain.terX1:
                obstacle.obsY = terrain.terY0-40
        if obstacle.obsX <= -80: 
            app.obstacles.remove(obstacle)
            addObstacle(app)

####################################################################################################################
####################################################################################################################
####################################################################################################################

def redrawAll(app, canvas):
    # welcome screen
    if app.gameState == 'welcome':
        canvas.create_image(app.width/2, app.height/2, image = ImageTk.PhotoImage(app.welcomeImage))

    # menu screen
    if app.gameState == 'main menu':
        canvas.create_image(app.width/2, app.height/2, image = ImageTk.PhotoImage(app.mainMenuImage))
        canvas.create_text(app.width/2, 240, text = "TUTORIAL: PRESS 'U'", fill = 'red', font = 'Helvetica 30 bold')
        canvas.create_text(app.width/2, 340, text = "TIME TRIAL: PRESS 'T'", fill = 'red', font = 'Helvetica 30 bold')
        canvas.create_text(app.width/2, 440, text = "HIGH SCORES: PRESS 'H'", fill = 'red', font = 'Helvetica 30 bold')

    # time trial
    if app.gameState == 'time trial':
        canvas.create_image(app.width/2, app.height/2, image = ImageTk.PhotoImage(app.timeTrialImage))
        canvas.create_text(app.width/2, 240, text = "EASY: PRESS 'E'", fill = 'red', font = 'Helvetica 30 bold')
        canvas.create_text(app.width/2, 340, text = "MEDIUM: PRESS 'D'", fill = 'red', font = 'Helvetica 30 bold')
        canvas.create_text(app.width/2, 440, text = "HARDCORE: PRESS 'H'", fill = 'red', font = 'Helvetica 30 bold')
        canvas.create_text(app.width/2, 540, text = "PRESS 'M' FOR MAIN MENU", font = 'Helvetica 15 bold')

    # final score screen
    if app.gameState == 'final score':
        canvas.create_image(app.width/2, app.height/2, image = ImageTk.PhotoImage(app.finalImage))
        canvas.create_text(app.width/2, app.height/2 - 50, text = app.finalScore, fill = 'red', font = 'Helvetica 200 bold')
        canvas.create_text(app.width/2, app.height/2+100, text = "PRESS 'R' TO RESTART", font = 'Helvetica 30 bold')
        canvas.create_text(app.width/2, app.height/2+160, text = "PRESS 'M' FOR MAIN MENU", font = 'Helvetica 30 bold')
        if app.kickflipToggle == True and app.kickflipUnlockToggle == False:
            canvas.create_text(app.width/2, app.height/2+220, text = "KICKFLIP UNLOCKED", fill = 'red', font = 'Helvetica 50 bold')
            canvas.create_text(app.width/2, app.height/2+260, text = "PRESS 'F' TO KICKFLIP OVER OBSTACLES TO SCORE 2X POINTS", 
            fill = 'red', font = 'Helvetica 15 bold')
        if app.treflipToggle == True and app.treflipUnlockToggle == False:
            canvas.create_text(app.width/2, app.height/2+220, text = "360 FLIP UNLOCKED", fill = 'red', font = 'Helvetica 50 bold')
            canvas.create_text(app.width/2, app.height/2+260, text = "PRESS 'D' TO 360 FLIP OVER OBSTACLES TO SCORE 4X POINTS", 
            fill = 'red', font = 'Helvetica 15 bold')

    # high scores screen
    if app.gameState == 'high scores':
        canvas.create_image(app.width/2, app.height/2, image = ImageTk.PhotoImage(app.highScoresImage))
        for i in range(8):
            canvas.create_text(app.width/2, 180+45*i, text = f'{app.highScores[i][0]} \t {app.highScores[i][1]}', 
            fill = 'red', font = 'Helvetica 30 bold')
        canvas.create_text(app.width/2, 550, text = "PRESS 'M' FOR MAIN MENU", font = 'Helvetica 15 bold')

    # main game
    if app.gameState == 'game' or app.gameState == 'instructions':
        # draw background sky
        canvas.create_rectangle(0,0,app.width, app.height, fill = 'LightSkyBlue1')
        if app.gameState == 'instructions':
            drawInstructions(app, canvas)
        else:
            canvas.create_image(app.width/2, 75, image = ImageTk.PhotoImage(app.scoreAndTimeImage))
            canvas.create_text(110, 140, text = app.score, font = 'Helvetica 60 bold')
        if app.gameState != 'instructions' and app.setTime-round(app.timer) < 6:
            color = 'red'
        else: color = 'black'
        if app.gameState != 'instructions':
            canvas.create_text(app.width - 110, 140, text = app.setTime-round(app.timer), fill = color, font = 'Helvetica 60 bold')
        drawSkater(app, canvas)
        drawTerrain(app, canvas)
        drawObstacle(app, canvas)

def drawInstructions(app, canvas):
    canvas.create_image(app.width/2, 75, image = ImageTk.PhotoImage(app.instructionsImage)) # header

    if list(set(app.generatedObstacles)) == ['cone']:
        if app.kickflipToggle == False:
            canvas.create_text(app.width/2, 160, text = f'{app.score}/6', font = 'Helvetica 60 bold')

        elif app.kickflipToggle == True:
            if app.score == 6 and app.kickflipUnlockToggle == False:
                canvas.create_text(app.width/2, 170, text = "  KICKFLIP\nUNLOCKED", fill = 'red', 
                font = 'Helvetica 40 bold')
            else: canvas.create_text(app.width/2, 160, text = f'{app.score}/14', font = 'Helvetica 60 bold')

    if app.kickflipToggle == True and list(set(app.generatedObstacles)) == ['table']:
        canvas.create_text(app.width/2, 160, text = f'{app.score}/30', font = 'Helvetica 60 bold')

    elif app.kickflipToggle == True and list(set(app.generatedObstacles)) == ['cone','table']:
        canvas.create_text(app.width/2, 160, text = f'{app.score}', font = 'Helvetica 60 bold')

    if app.collisionToggle == True:
        canvas.create_text(app.width/2, app.height*2/5, text = 'UNSUCCESFULLY CLEARING OBJECTS REDUCES SCORE', 
        font = 'Helvetica 15 bold')
    else:
        if app.pushToggle == False:
            canvas.create_text(app.width/2, app.height*2/5, text = 'PRESS RIGHT ARROW KEY TO PUSH AND INCREASE SPEED', 
            font = 'Helvetica 15 bold')
        elif app.pushToggle == True and app.ollieToggle == False and app.kickflipToggle == False:
            canvas.create_text(app.width/2, app.height*2/5, text = 'PRESS SPACE BAR TO OLLIE OVER ONCOMING OBSTACLES', 
            font = 'Helvetica 15 bold')
        elif app.pushToggle == True and app.ollieToggle == True and app.kickflipToggle == False:
            canvas.create_text(app.width/2, app.height*2/5, text = 'PRESS SPACE BAR TO OLLIE OVER ONCOMING OBSTACLES', 
            font = 'Helvetica 15 bold')
        elif app.pushToggle == True and app.ollieToggle == True and app.kickflipToggle == True and app.score < 14:
            canvas.create_text(app.width/2, app.height*2/5, text = "PRESS 'F' TO KICKFLIP OVER OBSTACLES TO SCORE 2X POINTS", 
            font = 'Helvetica 15 bold')
        elif app.pushToggle == True and app.ollieToggle == True and app.kickflipToggle == True and app.score >= 14 and app.generatedObstacles != ['cone','table']:
            canvas.create_text(app.width/2, app.height*2/5, text = "DIFFERENT OBSTACLES YEILD DIFFERENT POINTS: CONE=1, TABLE=2", 
            font = 'Helvetica 15 bold')
        elif app.kickflipToggle == True and app.generatedObstacles == ['cone','table']:
            canvas.create_text(app.width/2, app.height*2/5, text = "TUTORIAL COMPLETE, PRESS 'M' for MAIN MENU", 
            font = 'Helvetica 15 bold')

def drawSkater(app, canvas):
    rotation = 0 - app.rotation
    sprite = app.skater.sprites[app.skater.spriteCounter]
    rotateImage = ImageTk.PhotoImage(sprite.rotate(rotation))
    # shift based on rotation
    shiftRads = math.radians(app.rotation)
    shiftY = 40 - (40 * math.cos(shiftRads))
    shiftX = 40 * math.sin(shiftRads)
    canvas.create_image(app.skater.x + shiftX, app.skater.y + shiftY, image = rotateImage)

def drawObstacle(app, canvas):
    for obstacle in app.obstacles:
        canvas.create_image(obstacle.obsX, obstacle.obsY, image=ImageTk.PhotoImage(obstacle.obsImage))

def drawTerrain(app, canvas):
    for terrain in app.terrains:
        canvas.create_polygon(terrain.terX0+app.run, terrain.terY0, terrain.terX1+app.run, terrain.terY1,
                              terrain.terX1+app.run, app.height, terrain.terX0+app.run, app.height, fill = 'grey50')
        canvas.create_line(terrain.terX0+app.run, terrain.terY0, terrain.terX1+app.run, terrain.terY1)
    for skatedTerrain in app.skatedTerrains:
        canvas.create_polygon(skatedTerrain.terX0+app.run, skatedTerrain.terY0, skatedTerrain.terX1+app.run, skatedTerrain.terY1,
                              skatedTerrain.terX1+app.run, app.height, skatedTerrain.terX0+app.run, app.height, fill = 'grey50')
        canvas.create_line(skatedTerrain.terX0+app.run, skatedTerrain.terY0, skatedTerrain.terX1+app.run, skatedTerrain.terY1)

runApp(width=600, height=600)