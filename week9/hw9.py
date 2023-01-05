#################################################
# hw9.py
#
# Your name: Greg Budhijanto
# Your andrew id: gbudhija
#################################################

import cs112_f21_week9_linter
import math, copy, os

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

def oddCount(L):
    #basecase: if L[0] = []
    #recursivecase: if L[0] is odd...return 1 + oddCount(L[1:]) 
    if L == []:
        return 0
    else:
        if L[0] % 2 == 1:
            return 1 + oddCount(L[1:])
        else:
            return oddCount(L[1:])

def oddSum(L):
    #basecase: if L[0] = []
    #recursivecase: if L[0] is odd...return L[0] + oddCount(L[1:]) 
    if L == []:
        return 0
    else:
        if L[0] % 2 == 1:
            return L[0] + oddSum(L[1:])
        else:
            return oddSum(L[1:])

def oddsOnly(L):
    if L == []:
        return []
    else:
        if L[0] % 2 == 1:
            return [L[0]] + oddsOnly(L[1:])
        else:
            return oddsOnly(L[1:])

def maxOdd(L):
    if L == []:
        return None
    else:
        bestOfRest = maxOdd(L[1:])
        if L[0] % 2 == 1 and (bestOfRest == None or L[0] > bestOfRest):
            return L[0]
        else: return bestOfRest

def hasConsecutiveDigits(n):
    #bc: if n == 0: return False
    #rc: if ones == tens: return True else return hasConDig(L[1:])
    n = abs(n)
    if n == 0: return False
    else:
        ones = n % 10
        tens = n // 10 % 10
        if ones == tens: return True
        else: return hasConsecutiveDigits(n//10)

def alternatingSum(L):
    #bc: if L == []: return 0
    #rc: if toggle = False: return L[0] + aS(L[1:], True), else...return opposit
    if len(L) == 0: return 0
    elif len(L) == 1: return L[0]
    else:
        return L[0] - L[1] + alternatingSum(L[2:])

#################################################
# Freddy Fractal Viewer
#################################################

from cmu_112_graphics import *

def appStarted(app):
    app.level = 0

def drawFractal(app, canvas, level, cx, cy, size):
    if level == 0:
        makeFreddy(app, canvas, cx, cy, size)
    else:
        cr = 94*size
        fracXY = cr * math.cos(math.pi/4)
        drawFractal(app,canvas,level-1,cx, cy, size)
        drawFractal(app,canvas,level-1,cx-(3*fracXY/2),cy-(3*fracXY/2),size/2)
        drawFractal(app,canvas,level-1,cx+(3*fracXY/2),cy-(3*fracXY/2), size/2)

def makeFreddy(app, canvas, cx, cy, size): 
    faceR = 94*size
    offset = 10*size
    #face
    canvas.create_oval(cx-faceR, cy-faceR, cx+faceR, cy+faceR,
                       fill = 'sienna4', width = offset)
    #eyes
    eyeR = 16*size
    eyeLX, eyeLY = cx-(39*size), cy-(41*size)
    eyeRX, eyeRY = cx+(39*size), cy-(41*size)
    canvas.create_oval(eyeLX-eyeR, eyeLY-eyeR, eyeLX+eyeR, eyeLY+eyeR,
                       fill = 'black')
    canvas.create_oval(eyeRX-eyeR, eyeRY-eyeR, eyeRX+eyeR, eyeRY+eyeR,
                       fill = 'black')
    #snout
    canvas.create_oval(cx-48*size, cy-18*size, cx+48*size, cy+78*size,
                       fill = 'tan', width = offset/2)
    #mouth
    canvas.create_arc(cx, cy+35*size, cx+24*size, cy+58*size,
                      style = 'arc', extent = -180,
                      width = offset/2)
    canvas.create_arc(cx, cy+35*size, cx-24*size, cy+58*size,
                      style = 'arc', extent = -180,
                      width = offset/2)
    #nose
    canvas.create_oval(cx-16*size, cy-5*size, cx+16*size, cy+27*size,
                       fill = 'black')

def keyPressed(app, event):
    if event.key in ['Up', 'Right']:
        if app.level == 5: app.level += 0
        else: app.level += 1
    elif (event.key in ['Down', 'Left']) and (app.level > 0):
        app.level -= 1

def redrawAll(app, canvas):
    margin = min(app.width, app.height)//10
    otherParams = None
    drawFractal(app, canvas, app.level, app.width/2, 250, 1)
    # canvas.create_text(app.width/2, 0,
    #                    text = f'Level {app.level} Fractal',
    #                    font = 'Arial ' + str(int(margin/3)) + ' bold',
    #                    anchor='n')


def runFreddyFractalViewer():
    print('Running Freddy Fractal Viewer!')
    runApp(width=400, height=400)

#################################################
# Test Functions
#################################################

def testOddCount():
    print('Testing oddCount()...', end='')
    assert(oddCount([ ]) == 0)
    assert(oddCount([ 2, 4, 6 ]) == 0) 
    assert(oddCount([ 2, 4, 6, 7 ]) == 1)
    assert(oddCount([ -1, -2, -3 ]) == 2)
    assert(oddCount([ 1,2,3,4,5,6,7,8,9,10,0,0,0,11,12 ]) == 6)
    print('Passed!')

def testOddSum():
    print('Testing oddSum()...', end='')
    assert(oddSum([ ]) == 0)
    assert(oddSum([ 2, 4, 6 ]) == 0) 
    assert(oddSum([ 2, 4, 6, 7 ]) == 7)
    assert(oddSum([ -1, -2, -3 ]) == -4)
    assert(oddSum([ 1,2,3,4,5,6,7,8,9,10,0,0,0,11,12 ]) == 1+3+5+7+9+11)
    print('Passed!')

def testOddsOnly():
    print('Testing oddsOnly()...', end='')
    assert(oddsOnly([ ]) == [ ])
    assert(oddsOnly([ 2, 4, 6 ]) == [ ]) 
    assert(oddsOnly([ 2, 4, 6, 7 ]) == [ 7 ])
    assert(oddsOnly([ -1, -2, -3 ]) == [-1, -3])
    assert(oddsOnly([ 1,2,3,4,5,6,7,8,9,10,0,0,0,11,12 ]) == [1,3,5,7,9,11])
    print('Passed!')

def testMaxOdd():
    print('Testing maxOdd()...', end='')
    assert(maxOdd([ ]) == None)
    assert(maxOdd([ 2, 4, 6 ]) == None) 
    assert(maxOdd([ 2, 4, 6, 7 ]) == 7)
    assert(maxOdd([ -1, -2, -3 ]) == -1)
    assert(maxOdd([ 1,2,3,4,5,6,7,8,9,10,0,0,0,11,12 ]) == 11)
    print('Passed!')

def testHasConsecutiveDigits():
  print('Testing hasConsecutiveDigits()...', end='')
  assert(hasConsecutiveDigits(1123) == True)
  assert(hasConsecutiveDigits(-1123) == True)
  assert(hasConsecutiveDigits(1234) == False)
  assert(hasConsecutiveDigits(0) == False)
  assert(hasConsecutiveDigits(1233) == True)
  print("Passed!")

def testAlternatingSum():
    print('Testing alternatingSum()...', end='')
    assert(alternatingSum([1,2,3,4,5]) == 1-2+3-4+5)
    assert(alternatingSum([ ]) == 0)
    print('Passed!')

#################################################
# testAll and main
#################################################

def testAll():
    testOddCount()
    testOddSum()
    testOddsOnly()
    testMaxOdd()
    testHasConsecutiveDigits()
    testAlternatingSum()
    runFreddyFractalViewer()

def main():
    cs112_f21_week9_linter.lint()
    testAll()

if (__name__ == '__main__'):
    main()


