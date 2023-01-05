#################################################
# hw8.py:
#
# Your name: greg budhijanto    
# Your andrew id: gbudhija
#################################################

import cs112_f21_week8_linter
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
# Midterm1 Free Responses
#################################################

def isAcceptedValue(x, rules):
    for line in rules:
        word = line.split()
        testX = x % int(word[0][2:]) if "%" in line else x
        lastX = int(word[-1])
        if 'multiple' in line:
            if 'must be' in line:
                if testX % lastX != 0:
                    return False
            if 'must not be' in line:
                if testX % lastX == 0:
                    return False
        if 'equal' in line:
            if 'must be' in line:
                if testX != lastX:
                    return False
            if 'must not be' in line:
                if testX == lastX:
                    return False
    return True

def firstNAcceptedValues(n, rules):
    guess = 0
    found = []
    while len(found) < n:
        guess += 1
        if isAcceptedValue(guess,rules):
            found.append(guess)
    return found

from dataclasses import make_dataclass
import random

Dot = make_dataclass('Dot',['cx','cy','cr','color','d'])

def appStarted(app):
    app.dots = []

def keyPressed(app, event):
    pass

def mousePressed(app, event):
    toggle = False
    for dot in app.dots:
        if distance(dot.cx, event.x, dot.cy, event.y) < dot.cr:
            if dot.color == 'red':
                dot.color ='green'
            else:
                dot.color = 'red'
            toggle = True
    if toggle == False:
        makeDot(app, event.x, event.y)

def distance(x0,x1,y0,y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5

def makeDot(app,x,y):
    direction = (random.randint(-3,3), random.randint(-3,3))
    newDot = Dot(cx=x, cy=y, cr=20, color='green', d=direction)
    app.dots.append(newDot)

def timerFired(app):
    for dot in app.dots:
        drow,dcol = dot.d
        if dot.color == 'green':
            dot.cx += drow
            dot.cy += dcol
        if ((dot.cx < 0) or (dot.cx > app.width) or
            (dot.cy < 0) or (dot.cy > app.height)):
            app.dots.remove(dot)


def redrawAll(app, canvas):
    canvas.create_text(app.width/2, 15, text=f'{len(app.dots)} Dot(s)')
    for dot in app.dots:
        canvas.create_oval(dot.cx-dot.cr, dot.cy-dot.cr,
                           dot.cx+dot.cr, dot.cy+dot.cr,
                           fill = dot.color)

def midterm1Animation():
    runApp(width=400, height=400)

#################################################
# Other Classes and Functions for you to write
#################################################

class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.friends = []
        self.friendsNames = set()

    def getName(self):
        return self.name

    def getAge(self):
        return self.age

    def getFriends(self):
        return self.friends

    def getFriendsNames(self):
        return sorted(list(self.friendsNames))

    def addFriend(self, other):
        if other not in self.friends:
            self.friends.append(other)
            other.friends.append(self)
            self.friendsNames.add(other.name)
            other.friendsNames.add(self.name)

    def addFriends(self, other):
        for friend in other.friends:
            if friend not in self.friends:
                self.friends.append(friend)
        for friendName in other.friendsNames:
            self.friendsNames.add(friendName)

# https://www.cs.cmu.edu/~112/notes/notes-sets.html
def repeats(L):
    # return a sorted list of the repeat elements in the list L
    seen = set()
    seenAgain = set()
    for element in L:
        if (element in seen):
            seenAgain.add(element)
        seen.add(element)
    return sorted(seenAgain)

def getPairSum(L, target):
    for val in L:
        if (target - val) in set(L) and (target - val != val):
            return (val,target - val)
        elif (target - val) in set(L) and (target - val in set(repeats(L))):
            return (val,target - val)
    return None
    
def containsPythagoreanTriple(L):
    setL = sorted(set(L))[::-1]
    for i in range(len(setL)):
        for j in range(len(setL))[i+1:]:
            if ((setL[i]**2 - setL[j]**2)**0.5) in set(setL):
                return True
    return False

def movieAwards(oscarResults):
    results = {}
    for tuples in oscarResults:
        award, movie = tuples
        results[movie] = results.get(movie, 0) + 1
    return results

def friendsOfFriends(friends):
    result = {}
    for person in friends:
        result[person] = set()
        personSet = friends[person]
        for friend in personSet:
            frientSet = friends[friend]
            for fof in frientSet:
                if fof != person and fof not in personSet:
                    result[person].add(fof)
    return result

#################################################
# Bonus Animation
#################################################

def bonus_appStarted(app):
    app.counter = 0

def bonus_keyPressed(app, event):
    pass

def bonus_mousePressed(app, event):
    pass

def bonus_timerFired(app):
    app.counter += 1

def bonus_redrawAll(app, canvas):
    canvas.create_text(app.width/2, app.height/2,
                       text=f'bonusAnimation', font='Arial 30 bold')
    canvas.create_text(app.width-20, app.height-20, text=str(app.counter))

def bonusAnimation():
    runApp(width=400, height=400, fnPrefix='bonus_')

#################################################
# Test Functions
#################################################


def testFirstNAcceptedValues():
    print('Testing firstNAcceptedValues...', end='')
    oneRule = [ 'x must be a multiple of 3' ]
    assert(firstNAcceptedValues(6, oneRule) == [3, 6, 9, 12, 15, 18])
    twoRules = [ 'x must be a multiple of 3',
                 'x must not be a multiple of 9' ]
    assert(firstNAcceptedValues(6, twoRules) == [3, 6, 12, 15, 21, 24])
    fourRules = [ 'x must be a multiple of 3',
                  'x must not be a multiple of 9',
                  'x%2 must be a multiple of 2',
                  'x%10 must not be equal to 4' ]
    assert(firstNAcceptedValues(6, fourRules) == [6, 12, 30, 42, 48, 60])
    print("Passed!")
    

def testMidterm1Animation():
    print('Note: You must visually inspect your midterm1 animation to test it.')
    midterm1Animation()

def testPersonClass():
    print('Testing Person Class...', end='')
    fred = Person('fred', 32)
    assert(isinstance(fred, Person))
    assert(fred.getName() == 'fred')
    assert(fred.getAge() == 32)
    # Note: person.getFriends() returns a list of Person objects who
    #       are the friends of this person, listed in the order that
    #       they were added.
    # Note: person.getFriendNames() returns a list of strings, the
    #       names of the friends of this person.  This list is sorted!
    assert(fred.getFriends() == [ ])
    assert(fred.getFriendsNames() == [ ])

    wilma = Person('wilma', 35)
    assert(wilma.getName() == 'wilma')
    assert(wilma.getAge() == 35)
    assert(wilma.getFriends() == [ ])

    wilma.addFriend(fred)
    assert(wilma.getFriends() == [fred])
    assert(wilma.getFriendsNames() == ['fred'])
    assert(fred.getFriends() == [wilma]) # friends are mutual!
    assert(fred.getFriendsNames() == ['wilma'])

    wilma.addFriend(fred)
    assert(wilma.getFriends() == [fred]) # don't add twice!

    betty = Person('betty', 29)
    fred.addFriend(betty)
    assert(fred.getFriendsNames() == ['betty', 'wilma'])

    pebbles = Person('pebbles', 4)
    betty.addFriend(pebbles)
    assert(betty.getFriendsNames() == ['fred', 'pebbles'])

    barney = Person('barney', 28)
    barney.addFriend(pebbles)
    barney.addFriend(betty)
    barney.addFriends(fred) # add ALL of Fred's friends as Barney's friends
    assert(barney.getFriends() == [pebbles, betty, wilma])
    assert(barney.getFriendsNames() == ['betty', 'pebbles', 'wilma'])
    fred.addFriend(wilma)
    fred.addFriend(barney)
    assert(fred.getFriends() == [wilma, betty, barney])
    assert(fred.getFriendsNames() == ['barney', 'betty', 'wilma']) # sorted!
    assert(barney.getFriends() == [pebbles, betty, wilma, fred])
    assert(barney.getFriendsNames() == ['betty', 'fred', 'pebbles', 'wilma'])
    print('Passed!')

def testGetPairSum():
    print("Testing getPairSum()...", end="")
    assert(getPairSum([1], 1) == None)
    assert(getPairSum([5, 2], 7) in [ (5, 2), (2, 5) ])
    assert(getPairSum([10, -1, 1, -8, 3, 1], 2) in
                      [ (10, -8), (-8, 10),(-1, 3), (3, -1), (1, 1) ])
    assert(getPairSum([10, -1, 1, -8, 3, 1], 10) == None)
    assert(getPairSum([10, -1, 1, -8, 3, 1, 8, 19, 0, 5], 10) in
                      [ (10, 0), (0, 10)] )
    assert(getPairSum([10, -1, 1, -8, 3, 1, 8, 19, -9, 5], 10) in
                      [ (19, -9), (-9, 19)] )
    assert(getPairSum([1, 4, 3], 2) == None) # catches reusing values! 1+1...
    print("Passed!")

def testContainsPythagoreanTriple():
    print("Testing containsPythagoreanTriple()...", end="")
    assert(containsPythagoreanTriple([1,3,6,2,5,1,4]) == True)
    assert(containsPythagoreanTriple([1,3,6,2,8,1,4]) == False)
    assert(containsPythagoreanTriple([1,730,3,6,54,2,8,1,728,4])
                                      == True) # 54, 728, 730
    assert(containsPythagoreanTriple([1,730,3,6,54,2,8,1,729,4]) == False)
    assert(containsPythagoreanTriple([1,731,3,6,54,2,8,1,728,4]) == False)
    assert(containsPythagoreanTriple([1,731,3,6,54,2,8,1,728,4,
                                6253, 7800, 9997]) == True) # 6253, 7800, 9997
    assert(containsPythagoreanTriple([1,731,3,6,54,2,8,1,728,4,
                                      6253, 7800, 9998]) == False)
    assert(containsPythagoreanTriple([1,731,3,6,54,2,8,1,728,4,
                                      6253, 7800, 9996]) == False)
    print("Passed!")

def testMovieAwards():
    print('Testing movieAwards()...', end='')
    tests = [
      (({ ("Best Picture", "The Shape of Water"), 
          ("Best Actor", "Darkest Hour"),
          ("Best Actress", "Three Billboards Outside Ebbing, Missouri"),
          ("Best Director", "The Shape of Water") },),
        { "Darkest Hour" : 1,
          "Three Billboards Outside Ebbing, Missouri" : 1,
          "The Shape of Water" : 2 }),
      (({ ("Best Picture", "Moonlight"),
          ("Best Director", "La La Land"),
          ("Best Actor", "Manchester by the Sea"),
          ("Best Actress", "La La Land") },),
        { "Moonlight" : 1,
          "La La Land" : 2,
          "Manchester by the Sea" : 1 }),
      (({ ("Best Picture", "12 Years a Slave"),
          ("Best Director", "Gravity"),
          ("Best Actor", "Dallas Buyers Club"),
          ("Best Actress", "Blue Jasmine") },),
        { "12 Years a Slave" : 1,
          "Gravity" : 1,
          "Dallas Buyers Club" : 1,
          "Blue Jasmine" : 1 }),
      (({ ("Best Picture", "The King's Speech"),
          ("Best Director", "The King's Speech"),
          ("Best Actor", "The King's Speech") },),
        { "The King's Speech" : 3}),
      (({ ("Best Picture", "Spotlight"), ("Best Director", "The Revenant"),
          ("Best Actor", "The Revenant"), ("Best Actress", "Room"),
          ("Best Supporting Actor", "Bridge of Spies"),
          ("Best Supporting Actress", "The Danish Girl"),
          ("Best Original Screenplay", "Spotlight"),
          ("Best Adapted Screenplay", "The Big Short"),
          ("Best Production Design", "Mad Max: Fury Road"),
          ("Best Cinematography", "The Revenant") },),
        { "Spotlight" : 2,
          "The Revenant" : 3,
          "Room" : 1,
          "Bridge of Spies" : 1,
          "The Danish Girl" : 1,
          "The Big Short" : 1,
          "Mad Max: Fury Road" : 1 }),
       ((set(),), { }),
            ]
    for args,result in tests:
        if (movieAwards(*args) != result):
            print('movieAwards failed:')
            print(args)
            print(result)
            assert(False)
    print('Passed!')

def testFriendsOfFriends():
    print("Testing friendsOfFriends()...", end="")
    d = dict()
    d["fred"] = set(["wilma", "betty", "barney", "bam-bam"])
    d["wilma"] = set(["fred", "betty", "dino"])
    d["betty"] = d["barney"] = d["bam-bam"] = d["dino"] = set()
    fof = friendsOfFriends(d)
    assert(fof["fred"] == set(["dino"]))
    assert(fof["wilma"] == set(["barney", "bam-bam"]))
    result = { "fred":set(["dino"]),
               "wilma":set(["barney", "bam-bam"]),
               "betty":set(),
               "barney":set(),
               "dino":set(),
               "bam-bam":set()
             }
    assert(fof == result)
    d = dict()
    #                A    B    C    D     E     F
    d["A"]  = set([      "B",      "D",        "F" ])
    d["B"]  = set([ "A",      "C", "D",  "E",      ])
    d["C"]  = set([                                ])
    d["D"]  = set([      "B",            "E",  "F" ])
    d["E"]  = set([           "C", "D"             ])
    d["F"]  = set([                "D"             ])
    fof = friendsOfFriends(d)
    assert(fof["A"] == set(["C", "E"]))
    assert(fof["B"] == set(["F"]))
    assert(fof["C"] == set([]))
    assert(fof["D"] == set(["A", "C"]))
    assert(fof["E"] == set(["B", "F"]))
    assert(fof["F"] == set(["B", "E"]))
    result = { "A":set(["C", "E"]),
               "B":set(["F"]),
               "C":set([]),
               "D":set(["A", "C"]),
               "E":set(["B", "F"]),
               "F":set(["B", "E"])
              }
    assert(fof == result)
    print("Passed!")

def testBonusAnimation():
    print('Note: You must visually inspect your bonus animation to test it.')
    bonusAnimation()

def testAll():
    testFirstNAcceptedValues()
    testMidterm1Animation()
    testPersonClass()
    testGetPairSum()
    testContainsPythagoreanTriple()
    testMovieAwards()
    testFriendsOfFriends()
    testBonusAnimation()

#################################################
# main
#################################################

def main():
    cs112_f21_week8_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
