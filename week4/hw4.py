#################################################
# hw4.py
# name: Greg Budhijanto
# andrew id: gbudhija
#################################################

import cs112_f21_week4_linter
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

def alternatingSum(L):
    sum = 0
    toggle = True
    for i in range(len(L)):
        if toggle == True:
            sum += L[i]
            toggle = False
        elif toggle == False:
            sum -= L[i]
            toggle = True
    return sum
        
def median(L):
    if len(L) == 0: return None
    newL = sorted(L)
    mid = len(L)//2
    if len(L) % 2 != 0:
        return newL[mid]
    else:
        return (newL[mid] + newL[mid - 1]) / 2 

def smallestDifference(L):
    i = 0
    if L == []: return -1
    smallest = None
    for i in range(len(L)):
        for j in range(i+1, len(L)):
            currDif = abs(L[i] - L[j])
            if smallest == None or currDif < smallest:
                smallest = currDif
    return smallest

def nondestructiveRemoveRepeats(L): 
    newList = []
    seen = []
    for val in L:
        if val not in seen:
            newList.append(val)
            seen.append(val)
        else: seen.append(L)
    return newList

def destructiveRemoveRepeats(L):
    i = 1
    while i < len(L):
        if L[i] in L[0:i]:
            L.pop(i)
        else: i += 1

#################################################
# Part B
#################################################

def isSorted(L):
    if len(L) <= 2: return True
    toggle = True
    prevI = L[0]
    if L[-1] - L[1] >= 0: 
        for i in L[1::]: #list is increasing
            if i - prevI >= 0:
                pass
            elif i - prevI < 0:
                toggle = False
            prevI = i
            if toggle: continue
            else: return False
        return True           
    else: #list is decreasing 
        for i in L[1::]:
            if i - prevI <= 0:
                pass
            elif i - prevI > 0:
                toggle = False
            prevI = i
            if toggle: continue
            else: return False
        return True 

def lookAndSay(L):
    l = list(L)
    lookAndSay = []
    if lookAndSay == l: return l
    else:
        count = 1
        digit = l[0]
        for i in l[1:]:
            if i == digit:
                count += 1
                digit = i
            elif i != digit:
                lookAndSay.append((count,digit))
                count = 1
                digit = i
        lookAndSay.append((count,digit))
        return lookAndSay

def inverseLookAndSay(L):
    l = list(L)
    reverseLookSay = []
    for i in l:
        x,y = tuple(i)
        reverseLookSay += x*[y]
    return reverseLookSay

def polynomial(p):
    pR = p[::-1]
    poly = []
    index = 0
    for i in pR:
        poly.append((index,i))
        index += 1
    return poly[::-1]


def multiplyPolynomials(p1, p2):
    p1R = polynomial(p1) #add exponent to list values, returns tuples
    p2R = polynomial(p2)
    minLength = min(p1R,p2R)
    maxLength = max(p1R,p2R)
    multList = [] #cross multiply

    for i in maxLength:
        x = i[0]
        y = i[1]
        for w in minLength:
            r = w[0]
            t = w[1]
            multList.append((x+r,y*t))
    multList.sort()
    revMultList = multList[::-1]

    exponent = revMultList[0][0]
    addedList = []
    digit = revMultList[0][1]

    for i in revMultList[1:]:
        if i[0] != exponent:
            addedList.append(digit)
            exponent = i[0]
            digit = i[1]
        elif i[0] == exponent:
            digit += i[1]
    addedList.append(digit)
    return addedList

def bestScrabbleScore(dictionary, letterScores, hand):
    bestScore = 0
    bestWord = []
    currScore = None
    for word in dictionary:
        if checkHand(word, hand): #hand latters are in word
            currScore = wordScore(word, letterScores)
            if currScore > bestScore: 
                bestWord = []
                bestScore = currScore
                bestWord.append(word)
            elif currScore == bestScore:
                bestWord.append(word)
            else: continue #currScore < bestScore
        else: continue #hand letters are not in word
    if bestScore == 0: return None
    elif len(bestWord) == 1:
        return (bestWord[0], bestScore)
    else: return (bestWord, bestScore)
        

def wordScore(word, letterScores):
    wordScore = 0
    for i in word: #loop through letters
        index = ord(i) - ord('a') #find index for letter
        wordScore += letterScores[index]
    return wordScore

def checkHand(word, hand):
    handDes = []
    for i in (word): #new list for letters in word
        handDes.append(i)
    for i in hand: #loop throught letters in hand
        if i in handDes:
            handDes.remove(i)
        else: continue
    if handDes == []:
        return True
    else: return False

#################################################
# Bonus/Optional
#################################################

def linearRegression(pointsList):
    return 42

def runSimpleProgram(program, args):
    return 42

#################################################
# Test Functions
#################################################

def _verifyAlternatingSumIsNondestructive():
    a = [1,2,3]
    b = copy.copy(a)
    # ignore result, just checking for destructiveness here
    alternatingSum(a)
    return (a == b)

def testAlternatingSum():
    print('Testing alternatingSum()...', end='')
    assert(_verifyAlternatingSumIsNondestructive())
    assert(alternatingSum([ ]) == 0)
    assert(alternatingSum([1]) == 1)
    assert(alternatingSum([1, 5]) == 1-5)
    assert(alternatingSum([1, 5, 17]) == 1-5+17)
    assert(alternatingSum([1, 5, 17, 4]) == 1-5+17-4)
    print('Passed!')

def _verifyMedianIsNondestructive():
    a = [1,2,3]
    b = copy.copy(a)
    # ignore result, just checking for destructiveness here
    median(a)
    return (a == b)

def testMedian():
    print('Testing median()...', end='')
    assert(_verifyMedianIsNondestructive())
    assert(median([ ]) == None)
    assert(median([ 42 ]) == 42)
    assert(almostEqual(median([ 1 ]), 1))
    assert(almostEqual(median([ 1, 2]), 1.5))
    assert(almostEqual(median([ 2, 3, 2, 4, 2]), 2))
    assert(almostEqual(median([ 2, 3, 2, 4, 2, 3]), 2.5))
    # now make sure this is non-destructive
    a = [ 2, 3, 2, 4, 2, 3]
    b = a + [ ]
    assert(almostEqual(median(b), 2.5))
    if (a != b):
        raise Exception('Your median() function should be non-destructive!')
    print('Passed!')

def testSmallestDifference():
    print('Testing smallestDifference()...', end='')
    assert(smallestDifference([]) == -1)
    assert(smallestDifference([2,3,5,9,9]) == 0)
    assert(smallestDifference([-2,-5,7,15]) == 3)
    assert(smallestDifference([19,2,83,6,27]) == 4)
    assert(smallestDifference(list(range(0, 10**3, 5)) + [42]) == 2)
    print('Passed!')

def _verifyNondestructiveRemoveRepeatsIsNondestructive():
    a = [3, 5, 3, 3, 6]
    b = a + [ ] # copy.copy(a)
    # ignore result, just checking for destructiveness here
    nondestructiveRemoveRepeats(a)
    return (a == b)

def testNondestructiveRemoveRepeats():
    print("Testing nondestructiveRemoveRepeats()", end="")
    assert(_verifyNondestructiveRemoveRepeatsIsNondestructive())
    assert(nondestructiveRemoveRepeats([1,3,5,3,3,2,1,7,5]) == [1,3,5,2,7])
    assert(nondestructiveRemoveRepeats([1,2,3,-2]) == [1,2,3,-2])
    print("Passed!")

def testDestructiveRemoveRepeats():
    print("Testing destructiveRemoveRepeats()", end="")
    a = [1,3,5,3,3,2,1,7,5]
    assert(destructiveRemoveRepeats(a) == None)
    assert(a == [1,3,5,2,7])
    b = [1,2,3,-2]
    assert(destructiveRemoveRepeats(b) == None)
    assert(b == [1,2,3,-2])
    print("Passed!")

def testIsSorted():
    print('Testing isSorted()...', end='')
    assert(isSorted([]) == True)
    assert(isSorted([1]) == True)
    assert(isSorted([1,1]) == True)
    assert(isSorted([1,2]) == True)
    assert(isSorted([2,1]) == True)
    assert(isSorted([2,2,2,2,2,1,1,1,1,0]) == True)
    assert(isSorted([1,1,1,1,2,2,2,2,3,3]) == True)
    assert(isSorted([1,2,1]) == False)
    assert(isSorted([1,1,2,1]) == False)
    assert(isSorted(range(10,30,3)) == True)
    assert(isSorted(range(30,10,-3)) == True)
    print('Passed!')

def _verifyLookAndSayIsNondestructive():
    a = [1,2,3]
    b = a + [ ] # copy.copy(a)
    lookAndSay(a) # ignore result, just checking for destructiveness here
    return (a == b)

def testLookAndSay():
    print("Testing lookAndSay()...", end="")
    assert(_verifyLookAndSayIsNondestructive() == True)
    assert(lookAndSay([]) == [])
    assert(lookAndSay([1,1,1]) ==  [(3,1)])
    assert(lookAndSay([-1,2,7]) == [(1,-1),(1,2),(1,7)])
    assert(lookAndSay([3,3,8,-10,-10,-10]) == [(2,3),(1,8),(3,-10)])
    assert(lookAndSay([3,3,8,3,3,3,3]) == [(2,3),(1,8),(4,3)])
    assert(lookAndSay([2]*5 + [5]*2) == [(5,2), (2,5)])
    assert(lookAndSay([5]*2 + [2]*5) == [(2,5), (5,2)])
    print("Passed!")

def _verifyInverseLookAndSayIsNondestructive():
    a = [(1,2), (2,3)]
    b = a + [ ] # copy.copy(a)
    inverseLookAndSay(a) # ignore result, just checking for destructiveness here
    return (a == b)

def testInverseLookAndSay():
    print("Testing inverseLookAndSay()...", end="")
    assert(_verifyInverseLookAndSayIsNondestructive() == True)
    assert(inverseLookAndSay([]) == [])
    assert(inverseLookAndSay([(3,1)]) == [1,1,1])
    assert(inverseLookAndSay([(1,-1),(1,2),(1,7)]) == [-1,2,7])
    assert(inverseLookAndSay([(2,3),(1,8),(3,-10)]) == [3,3,8,-10,-10,-10])
    assert(inverseLookAndSay([(5,2), (2,5)]) == [2]*5 + [5]*2)
    assert(inverseLookAndSay([(2,5), (5,2)]) == [5]*2 + [2]*5)
    print("Passed!")

def testMultiplyPolynomials():
    print("Testing multiplyPolynomials()...", end="")
    # (2)*(3) == 6
    assert(multiplyPolynomials([2], [3]) == [6])
    # (2x-4)*(3x+5) == 6x^2 -2x - 20
    assert(multiplyPolynomials([2,-4],[3,5]) == [6,-2,-20])
    # (2x^2-4)*(3x^3+2x) == (6x^5-8x^3-8x)
    assert(multiplyPolynomials([2,0,-4],[3,0,2,0]) == [6,0,-8,0,-8,0])
    print("Passed!")

def testBestScrabbleScore():
    print("Testing bestScrabbleScore()...", end="")
    def dictionary1(): return ["a", "b", "c"]
    def letterScores1(): return [1] * 26
    def dictionary2(): return ["xyz", "zxy", "zzy", "yy", "yx", "wow"] 
    def letterScores2(): return [1+(i%5) for i in range(26)]
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("b")) ==
                                        ("b", 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("ace")) ==
                                        (["a", "c"], 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("b")) ==
                                        ("b", 1))
    assert(bestScrabbleScore(dictionary1(), letterScores1(), list("z")) ==
                                        None)
    # x = 4, y = 5, z = 1
    # ["xyz", "zxy", "zzy", "yy", "yx", "wow"]
    #    10     10     7     10    9      -
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyz")) ==
                                         (["xyz", "zxy"], 10))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyzy")) ==
                                        (["xyz", "zxy", "yy"], 10))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("xyq")) ==
                                        ("yx", 9))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("yzz")) ==
                                        ("zzy", 7))
    assert(bestScrabbleScore(dictionary2(), letterScores2(), list("wxz")) ==
                                        None)
    print("Passed!")

def relaxedAlmostEqual(d1, d2):
    epsilon = 10**-3 # really loose here
    return abs(d1 - d2) < epsilon

def tuplesAlmostEqual(t1, t2):
    if (len(t1) != len(t2)): return False
    for i in range(len(t1)):
        if (not relaxedAlmostEqual(t1[i], t2[i])):
            return False
    return True

def testLinearRegression():
    print("Testing bonus problem linearRegression()...", end="")

    ans = linearRegression([(1,3), (2,5), (4,8)])
    target = (1.6429, 1.5, .9972)
    assert(tuplesAlmostEqual(ans, target))
    
    ans = linearRegression([(0,0), (1,2), (3,4)])
    target = ((9.0/7), (2.0/7), .9819805061)
    assert(tuplesAlmostEqual(ans, target))

    #perfect lines
    ans = linearRegression([(1,1), (2,2), (3,3)])
    target = (1.0, 0.0, 1.0)
    assert(tuplesAlmostEqual(ans, target))
    
    ans = linearRegression([(0,1), (-1, -1)])
    target = (2.0, 1.0, 1.0)
    assert(tuplesAlmostEqual(ans, target))

    #horizontal lines
    ans = linearRegression([(1,0), (2,0), (3,0)])
    target = (0.0, 0.0, 1.0)
    assert(tuplesAlmostEqual(ans, target))

    ans = linearRegression([(1,1), (2,1), (-1,1)])
    target = (0.0, 1.0, 1.0)
    assert(tuplesAlmostEqual(ans, target))
    print("Passed!")

def testRunSimpleProgram():
    print("Testing bonus problem runSimpleProgram()...", end="")
    largest = """! largest: Returns max(A0, A1)
                   L0 - A0 A1
                   JMP+ L0 a0
                   RTN A1
                   a0:
                   RTN A0"""
    assert(runSimpleProgram(largest, [5, 6]) == 6)
    assert(runSimpleProgram(largest, [6, 5]) == 6)

    sumToN = """! SumToN: Returns 1 + ... + A0
                ! L0 is a counter, L1 is the result
                L0 0
                L1 0
                loop:
                L2 - L0 A0
                JMP0 L2 done
                L0 + L0 1
                L1 + L1 L0
                JMP loop
                done:
                RTN L1"""
    assert(runSimpleProgram(sumToN, [5]) == 1+2+3+4+5)
    assert(runSimpleProgram(sumToN, [10]) == 10*11//2)
    print("Passed!")

#################################################
# testAll and main
#################################################

def testAll():
    # comment out the tests you do not wish to run!
    # Part A:
    testAlternatingSum()
    testMedian()
    testSmallestDifference()
    testNondestructiveRemoveRepeats()
    testDestructiveRemoveRepeats()

    # Part B:
    testIsSorted()
    testLookAndSay()
    testInverseLookAndSay()
    testMultiplyPolynomials()
    testBestScrabbleScore()

    # Bonus:
    #testLinearRegression()
    #testRunSimpleProgram() 

def main():
    cs112_f21_week4_linter.lint()
    testAll()

if __name__ == '__main__':
    main()
