def getBottomUpColumn(M,col):
    if len(M) == 1: return [M[0][col]]
    elif col >= len(M[0]) or col < 0:
        return None
    else: return [M[-1][col]] + getBottomUpColumn(M[:-1], col)

def testGetBottomUpColumn():   
    print('Testing getBottomUpColumn()...', end='')
    assert(getBottomUpColumn([[1,2,3],[4,5,6]], 0) == [4, 1])
    assert(getBottomUpColumn([[1,2,3],[4,5,6]], 1) == [5, 2])  
    assert(getBottomUpColumn([[1,2,3],[4,5,6]], 2) == [6, 3])
    assert(getBottomUpColumn([[1,2,3],[4,5,6]], 3) == None)  
    assert(getBottomUpColumn([[1,2,3],[4,5,6]], -1) == None) 
    print('Passed!')

testGetBottomUpColumn()

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

def knightsTour(rows, cols):
    for row in range(rows):
        for col in range(cols):
            board = [([0] * cols) for row in range(rows)] #initiate board dims
            board[row][col] = 1
            return knightsTourWrapper(row, col, board, 2) #initiate stepNum=1

def moveIsLegal(testRow, testCol, board):
    if ((0 <= testRow < len(board)) and 0 <= testCol < len(board[0]) and 
        (board[testRow][testCol] == 0)): #in bounds and spot == 0: Legal
        return True
    else: return False

def knightsTourWrapper(row, col, board, stepNumber):
    #bc
    if (stepNumber-1) == (len(board)*len(board[0])):
        return board
    #rc
    else:
        directions = [(-2,-1),(-2,1),(-1,-2),(-1,2),
                      (1,-2),(1,2),(2,-1),(2,1)]
        for drow,dcol in directions:
            # print(drow,dcol)
            testRow, testCol = row+drow, col+dcol
            if moveIsLegal(testRow, testCol, board):
                board[testRow][testCol] = stepNumber
                # # input()
                # print2dList(board)
                solution=knightsTourWrapper(testRow,testCol,board,stepNumber+1)
                if solution != None:
                    return solution
                board[testRow][testCol] = 0
                # # input()
                # print("back track")
                # print2dList(board)
        return None
            
# print(print2dList(knightsTour(8, 8)))

import copy

class Scoreboard(object):
    def __init__(self, scores):
        self.scores = scores

    def getScore(self, person):
        if person in self.scores:
            return self.scores[person]
        else: return None

    def addScore(self, person, score):
        self.scores[person] = self.scores.get(person, 0) + score

    def leaders(self):
        bestScore = -1
        bestPerson = None
        for person in self.scores:
            if self.scores[person] > bestScore:
                bestScore = self.scores[person]
                bestPerson = {person}
            elif self.scores[person] == bestScore:
                bestPerson.add(person)
        return bestPerson

    def getAll(self):
        return self.scores

    def getCopy(self):
        return Scoreboard(copy.copy(self.scores))

def testScoreboardClass():
    print('Testing Scoreboard class...', end='')
    # Create a Scoreboard with these initial scores
    sb1 = Scoreboard({'Alice':3, 'Bob':4})
    assert(sb1.getScore('Alice') == 3)
    assert(sb1.getScore('Bob') == 4)
    assert(sb1.getScore('Cal') == None)
    assert(sb1.leaders() == { 'Bob' }) # A set of all the leaders

    sb1.addScore('Alice', 2) # Alice just scored 2 points!
    assert(sb1.getScore('Alice') == 5) # Now she has 5 points
    assert(sb1.leaders() == { 'Alice' }) # Alice has 5, Bob has 4

    sb1.addScore('Cal', 2)   # Cal wasn't there, now Cal is, with 2 points
    assert(sb1.getScore('Cal') == 2)
    sb1.addScore('Cal', 3)
    assert(sb1.getScore('Cal') == 5)
    assert(sb1.leaders() == { 'Alice', 'Cal' }) # Alice and Cal both have 5

    assert(sb1.getAll() == { 'Alice':5, 'Bob':4, 'Cal':5 })

    sb2 = sb1.getCopy() # This is a copy of sb1, where changes to the copy
                        # do not affect the original, and vice versa
    assert(sb2.getAll() == { 'Alice':5, 'Bob':4, 'Cal':5 })
    sb2.addScore('Bob', 3) # Bob now has 7 in sb2, but still has only 4 in sb1
    assert(sb2.leaders() == { 'Bob' })
    assert(sb1.leaders() == { 'Alice', 'Cal' })
    print('Passed!')

testScoreboardClass()

class A(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def f(self):
        return self.x + self.y
    def g(self):
        return self.f()/10

class B(A):
    def __init__(self, x):
        super().__init__(x, x**2)
    def g(self):
        return self.f()*10

def ct1(x):
    a = A(x, 2*x)
    b = B(x)
    print( [ a.g(), b.g() ] )

# ct1(4)

class File(object):
    def __init__(self, name, size):
        self.name = name
        self.size = size
    def copyFile(self, otherFileName):
        return File(otherFileName, self.size)    
    def __repr__(self):
        return f'File(name={self.name},size={self.size})'
    
class Folder(object):
    def __init__(self, name):
        self.name = name
        self.fileCount = 0
        self.files = set()
    def __repr__(self):
        return f'Folder(name={self.name},fileCount={self.fileCount})'
    def add(self, file):
        self.files.add(file)
        if isinstance(file, File):
            self.fileCount += 1
    def getTotalFileSize(self):
        total = 0
        for item in self.files:
            if isinstance(item, File):
                total += item.size
            else:
                subFolderSum = item.getTotalFileSize() # item is a File object!
                total += subFolderSum  
        return total

def testFilesAndFolders():
    print('Testing File and Folder classes...', end='')

    foo = File('foo.txt', 25)
    assert(str(foo) == 'File(name=foo.txt,size=25)')

    folderA = Folder('A')
    assert(str(folderA) == 'Folder(name=A,fileCount=0)')

    folderA.add(foo)
    assert(str(folderA) == 'Folder(name=A,fileCount=1)')

    folderB = Folder('B')
    assert(str(folderB) == 'Folder(name=B,fileCount=0)')

    bar1 = File('bar1.txt', 100)
    assert(str(bar1) == 'File(name=bar1.txt,size=100)')
    bar2 = bar1.copyFile('bar2.txt')
    assert(str(bar2) == 'File(name=bar2.txt,size=100)')

    folderB.add(bar1)
    assert(str(folderB) == 'Folder(name=B,fileCount=1)')
    folderB.add(bar2)
    assert(str(folderB) == 'Folder(name=B,fileCount=2)')

    # The fileCount only counts files, not folder, and does
    # so only for files in this folder and not in any folders
    # within this folder.  Thus, when we add folderB to folderA,
    # it does not increase the fileCount of folderA
    folderA.add(folderB)
    assert(str(folderA) == 'Folder(name=A,fileCount=1)')

    # folder.getTotalFileSize() returns the sum of the sizes of
    # all the files in that folder plus all the sizes of files in
    # any folder recursively within that folder.
    # To do this, you must write getTotalFileSize() recursively

    # folderB contains 2 files each of size 100, so that's 200
    assert(folderB.getTotalFileSize() == 200)
    # folderA contains 1 file of size 25, but also contains
    # folderB which is of size 200, so that's 225 in total
    assert(folderA.getTotalFileSize() == 225)

    bar3 = bar2.copyFile('bar3.txt')
    folderB.add(bar3)
    # A new file was added to folderB, which is in folderA
    # Accordingly, the total file size of folderA has increased to 325
    assert(folderA.getTotalFileSize() == 325)

    print('Passed!')

testFilesAndFolders()

class Polynomial(object):
    def __init__(self, coeffs):
        self.coeffs = coeffs
    def evalAt(self, x):
        revCoef = self.coeffs[::-1]
        result = 0
        for exponent in range(len(self.coeffs)):
            result += revCoef[exponent]*(x**exponent)
        return result
    def getCoefficient(self, coef):
        revCoef = self.coeffs[::-1]
        if coef >= len(self.coeffs):
            return 0
        else:
            return revCoef[coef]
    def times(self, other):
        newCoefs = []
        for x in self.coeffs:
            newCoefs.append(x * other)
        return Polynomial(newCoefs)

def testPolynomialClass():
    print('Testing Polynomial class...', end='')
    f = Polynomial([2,3,1]) # 2x**2 + 3x + 1
    assert(f.evalAt(4) == 2*4**2 + 3*4 + 1) # returns f(4), which is 45
    assert(f.evalAt(5) == 2*5**2 + 3*5 + 1) # returns f(5), which is 66
    assert(f.getCoefficient(0) == 1) # get the x**0 coefficient
    assert(f.getCoefficient(1) == 3) # get the x**1 coefficient
    assert(f.getCoefficient(2) == 2) # get the x**2 coefficient
    assert(f.getCoefficient(33) == 0) # assume leading 0's...
    g = f.times(10) # g is a new polynomial, which is 10*f
                    # just multiply each coefficient in f by this value
                    # so g = 20x**2 + 30*x + 10
    assert(g.getCoefficient(0) == 10) # get the x**0 coefficient
    assert(g.getCoefficient(1) == 30) # get the x**1 coefficient
    assert(g.getCoefficient(2) == 20) # get the x**2 coefficient
    assert(g.getCoefficient(33) == 0) # assume leading 0's...
    assert(g.evalAt(4) == 20*4**2 + 30*4 + 10) # returns g(4), which is 450
    print('Passed!')

testPolynomialClass()

def busiestStudents(roster):
    studentClasses = studentClassAmount(roster)
    most = -1
    mostStudent = None
    for student in studentClasses:
        if studentClasses[student] > most:
            most = studentClasses[student]
            mostStudent = {student}
        if studentClasses[student] == most:
            mostStudent.add(student)
    return mostStudent

def studentClassAmount(roster):
    students = dict()
    for course in roster:
        for student in roster[course]:
            students[student] = students.get(student, 0) + 1
    return students

rosters = {
    '15-112':{'amy','bob','claire','dan'},
    '18-100':{'amy','claire','john','mark'},
    '21-127':{'claire','john','zach'},
    '76-101':{'bob','john','margaret'},
}

def testBusiestStudents():
    print('Testing busiestStudents()...', end='')
    rosters = {
        '15-112':{'amy','bob','claire','dan'},
        '18-100':{'amy','claire','john','mark'},
        '21-127':{'claire','john','zach'},
        '76-101':{'bob','john','margaret'},
    }
    assert(busiestStudents(rosters) == { 'claire', 'john' })
    print('Passed!')

testBusiestStudents()

def getAdjacentVals(L):
    rows, cols = len(L), len(L[0])
    result = dict()
    for row in range(rows):
        for col in range(cols):
            num = L[row][col]
            adjVals = getAdjacentValsHelper(L, row, col)
            if num in result:
                for val in adjVals:
                    result[num].add(val)
            else: result[num] = adjVals
    return result

def getAdjacentValsHelper(L, row, col):
    adjVals = set()
    dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
    for drow,dcol in dirs:
        testRow, testCol = row+drow, col+dcol
        if ((testRow < 0) or (testRow >= len(L)) or
            (testCol < 0) or (testCol >= len(L[0]))):
            continue
        else:
            val = L[testRow][testCol]
            adjVals.add(val)
    return adjVals


def testGetAdjacentVals():
    print('Testing getAdjacentVals()...', end='')
    L = [ [ 3, 2, 5],
          [ 4, 3, 4],
          [ 1, 3, 3] ]
    assert(getAdjacentVals(L)== {
                    1 : { 3, 4 },
                    2 : { 3, 4, 5 },
                    3 : { 1, 2, 3, 4, 5 },
                    4 : { 1, 2, 3, 5 },
                    5 : { 2, 3, 4 }
                    })
    print('Passed!')

testGetAdjacentVals()

import string
def stringMap(s):
    d = {}
    index = 0
    return stringMapHelper(s, d, index)

def stringMapHelper(s, d, index):
    if index >= len(s):
        return d
    elif s[index] == ' ': # skips space
        return stringMapHelper(s, d, index + 1)
    else:
        letter = s[index].lower()
    if letter not in d:
        d[letter] = {index} 
    else:
        d[letter].add(index)
    return stringMapHelper(s, d, index + 1)

def testStringMap():
    print('Testing testStringMap()...', end='')
    assert(stringMap('I love dogs') == {'i': {0}, 'l': {2}, 
                                            'o': {8, 3}, 'v': {4}, 'e': {5}, 
                                            'd': {7}, 'g': {9}, 's': {10}})
    assert(stringMap('hi') == {'h': {0}, 'i': {1}})
    assert(stringMap('YAY! yay!') == {'y': {0, 2, 5, 7}, 'a': {1, 6}, '!': {8, 3}})
    print('Passed!')

testStringMap()

def reduceToStrings(lst):
    #BC
    if lst == []:
        return []
    #RC
    first = lst[0]
    rest = lst[1:]
    partialResult = reduceToStrings(rest)
    if isinstance(first, str):
        return [first] + partialResult
    else:
        return partialResult

class SayHi(object):
    def __init__(self, name):
        self.name = name
        self.saidHiList = []

    def __repr__(self):
        names = self.getSaidHiNames()
        if names == []:
            return f'{self.names} has said hi to no one'
        names = set(names)
        names = sorted(names) #alphabeticalize and convert to list
        nameString = " and ".join(names)
        return f'{self.name} has said Hi! to {nameString}'

    def sayHi(self, other):
        other.saidHiList.append(self)

    def getSaidHiList(self):
        return self.saidHiList
    
    def getSaidHiNames(self):
        names = []
        for person in self.saidHiList:
            names.append(person.name)

def getTimeSpent(logs):
    times = dict()
    for (time, person) in logs:
        if person in times:
            times[person].append(time)
        else:
            times[person] = [time]
    result = dict()
    for person in times:
        log = times[person]
        personsTime = 0
        for i in range(len(log)):
            if i % 2 == 0:
                personsTime -= log[i]
            else:
                personsTime += log[i]
        result[person] = personsTime
    return result

def pairSum(a, s):
    return solve(a, [], s)

def solve(remainingNums, resultSoFar, s):
    #basecase
    if len(remainingNums) == 0:
        return resultSoFar
    #start with recursive case
    for i in range(len(remainingNums)): #num1
        for j in range(i+1, len(remainingNums)): #num2
            num1 = remainingNums[i]
            num2 = remainingNums[j]
            if num1 + num2 == s:
                resultSoFar.append((num1,num2)) # added to result
                #removed from number bank
                remainingNums = remainingNums[:i]+remainingNums[i+1:j]+remainingNums[j+1:] #can be modified destructively
                result = solve(remainingNums, resultSoFar, s)
                if result != None:
                    return result
                #undo the move that we made
                resultSoFar.remove((num1, num2))
                remainingNums.insert(num1, i)
                remainingNums.insert(num2, j)
    return None

def testPairSum():
    print('Testing pairSum()...', end='')
    a = [2,3,1,4,5,3]
    assert(pairSum(a, 6) == [(2, 4), (3, 3), (1, 5)])
    print('Passed!')

testPairSum()

def valuesMatchingCounts(L):
    vals = dict()
    result = set()
    for value in L:
        vals[value] = vals.get(value, 0) + 1
        if vals[value] == value:
            result.add(value)
        elif value in result:
            result.remove(value)
    return result

def testValuesMatchingCounts():
    print('Testing valuesMatchingCounts()...', end='')
    assert(valuesMatchingCounts([1, 2, 3, 4, 5]) == {1})
    assert(valuesMatchingCounts([1, 5, 1, 1, 2]) == set())
    assert(valuesMatchingCounts([5, 2, 5, 2, 5, 6, 5, 1, 5, 0]) == {1, 2, 5})
    print('Passed!')

testValuesMatchingCounts()

def isPrime(n, factor):
    if n < 2:
        return False
    elif factor >= n:
        return True
    else:
        if n % factor == 0:
            return False
        else: return isPrime(n, factor+1)

def onlyPrimes(L):
    if L == []: return []
    elif len(L) == 1:
        if isPrime(L[0], 2):
            return [L[0]]
        else: return []
    else:
        if isPrime(L[0],2):
            result = [L[0]]
            result += onlyPrimes(L[1:])
            return result
        else:
            return onlyPrimes(L[1:])

def testOnlyPrimes():
    print('Testing onlyPrimes()...', end='')
    assert(onlyPrimes([]) == [])
    assert(onlyPrimes([1, 5, 1, 1, 2]) == [5, 2])
    assert(onlyPrimes([1, 2, 3, 4, 5, 6, 7, 8, 9]) == [2, 3, 5, 7])
    print('Passed!')

testOnlyPrimes()

def kSuperSplit(L, k, n):
    #L = list
    #k = number of list partitions
    #n = each partition sum must be equal or less than
    buckets = []
    for i in range(k):
        buckets.append([])
    return solveSuperSplit(L, k, n, buckets)

# def solveSuperSplit(L, partitions, sumMax, result):
#     #bc
#     if L == []:
#         return result
#     #rc
#     for i in range(partitions):
#         for j in L:
#             if sum(result[i] + [j]) <= sumMax:
#                 result[i].append(L[0])
#                 solution = solveSuperSplit(L[1:], partitions, sumMax, result)
#                 if solution != None:
#                     return solution
#                 result[i].pop()
#     return None

def solveSuperSplit(L, partitions, sumMax, result):
    #bc
    if L == []:
        return result
    elem = L[0]
    for i in range(partitions):
        currentBucket = result[i]
        if sum(currentBucket) + elem <= sumMax:
            result[i].append(elem)
            solution = solveSuperSplit(L[1:], partitions, sumMax, result)
            if solution != None:
                return solution
            currentBucket.pop()
    return None

def testkSuperSplit():
    print('Testing kSuperSplit()...', end='')
    assert(kSuperSplit([1,5,1,1,2,3,4,5], 3, 8) == [[1, 5, 1, 1], [2, 4], [3, 5]])
    assert(kSuperSplit([1,5,1,1,2,3,4,5], 6, 4) == None)
    print('Passed!')

testkSuperSplit()

def evensAreSorted(L):
    lastEven = -1
    return evensAreSortedWrapper(L, lastEven)

def evensAreSortedWrapper(L, lastEven):
    if L == []: return True
    else:
        if L[0] % 2 == 1:
            return evensAreSortedWrapper(L[1:], lastEven)
        elif L[0] % 2 == 0:
            if L[0] > lastEven:
                lastEven = L[0]
                return evensAreSortedWrapper(L[1:], lastEven)
            else: return False

def testEvensAreSorted():
    print('Testing evensAreSorted()...', end='')
    assert(evensAreSorted([2, 4, 8]) == True)
    assert(evensAreSorted([1, 2, 3, 4, 5, 8]) == True)
    assert(evensAreSorted([4, 2, 4, 2, 4]) == False)
    assert(evensAreSorted([1,2,3,3,2,1]) == False)
    assert(evensAreSorted([42, 33, 10, 80]) == False)
    assert(evensAreSorted([4]) == True)
    assert(evensAreSorted([9]) == True)
    assert(evensAreSorted([]) == True)
    print('Passed!')

testEvensAreSorted()

def zigZagKingsTour(n): #n = rows, cols
    board = [([0] * n) for rows in range(n)]
    board[0][0] = 1
    return zZKTW(board, n, 0, 0, 2, None)

def zZKTW(board, n, row, col, step, lastDir):
    if step > n**2: return board
    else:
        dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for (drow, dcol) in dirs:
            if (drow, dcol) == lastDir:
                continue
            testRow, testCol = row + drow, col + dcol
            if isLegal(board, testRow, testCol):
                board[testRow][testCol] = step
                solution = zZKTW(board, n, testRow, testCol, step+1, (drow,dcol))
                if solution != None:
                    return solution
                board[testRow][testCol] = 0
        return None

def isLegal(board, row, col):
    if ((row < 0) or (row >= len(board)) or (col < 0) or (col >= len(board[0]))
         or (board[row][col] != 0)): 
        return False
    else: return True

def testZigZagKingsTour():
    print('Testing zigZagKingsTour()...', end='')
    assert(zigZagKingsTour(3) == [[1, 2, 9], [3, 5, 8], [4, 7, 6]])
    assert(zigZagKingsTour(4) == [[1, 2, 5, 6], [3, 4, 7, 8], [12, 10, 9, 15], [11, 13, 14, 16]])
    print('Passed!')

testZigZagKingsTour()

import copy 

def makeWordLadder(L):
    if L == []: return []
    for word in L:
        newList = []
        listCopy = copy.copy(L)
        newList.append(word)
        listCopy.remove(word)
        solution = makeWordLadderHelper(listCopy, newList)
        if solution == None:
            continue
        else: return solution
    return None

def makeWordLadderHelper(L, newList):
    if L == []:
        return newList
    else:
        for i in range(len(L)):
            word1 = newList[-1]
            word2 = L[i]
            if word1[-1] == word2[0]:
                newList.append(word2)
                L.remove(word2)
                solution = makeWordLadderHelper(L, newList)
                if solution != None:
                    return solution
                newList.remove(word2)
                L.append(word2)
        return None

def testMakeWordLadder():
    print('Testing makeWordLadder()...', end='')
    assert(makeWordLadder(['aba', 'ca' ,'aa']) in [['ca', 'aba', 'aa'],
                                                  ['ca', 'aa', 'aba']])
    assert(makeWordLadder(['efg', 'abc', 'ghi', 'cde']) 
                                              == ['abc', 'cde', 'efg', 'ghi'])
    assert(makeWordLadder(['a', 'at', 'a', 'xa', 'a']) 
                                              == ['xa', 'a', 'a', 'a', 'at'])
    assert(makeWordLadder(['ab', 'cu', 'bu']) == None)
    assert(makeWordLadder(['abc']) == ['abc'])
    assert(makeWordLadder([]) == [])
    print('Passed!')

testMakeWordLadder()

def islands(L):
    return islandWrapper(L,[])

def islandWrapper(L, islands):
    if len(L) == 2: return islands
    else:
        if ((L[0]%2==0 and L[1]%2==1 and L[2]%2==0) or 
            (L[0]%2==1 and L[1]%2==0 and L[2]%2==1)):
            islands.append(L[1])
            return islandWrapper(L[1:], islands)
        else: return islandWrapper(L[1:], islands)

print(islands([1, 2, 3]))

def ct1(L):
    if (len(L) == 0):
        return [ ]
    else:
        return [max(L)] + ct1(L[1:-1]) + [min(L)]

print(ct1([1,2,3,2,1]))

def ct2(d):
    s, t, u = set(), set(), set()
    for k in d:
        s.add(k)
        for v in d[k]:
            if v%2 == 0:
                t.add(v)
            else:
                u.add(v)
    return { min(s):t, max(s):u}
    
print(ct2({ 3:[1,2,4,1], 1:[5,5], 2:[0,5] }))

def isPrime(n):
    if (n < 2):
        return False
    if (n == 2):
        return True
    if (n % 2 == 0):
        return False
    maxFactor = round(n**0.5)
    for factor in range(3,maxFactor+1,2):
        if (n % factor == 0):
            return False
    return True

def findRTP(digits):
    return findRTPH(digits, 0)

def findRTPH(digits, resultSoFar):
    if resultSoFar >= 10**digits:
        return resultSoFar
    else:
        for digit in range(10):
            testNum = resultSoFar*10 + digit
            if isPrime(testNum):
                solution = findRTPH(digits, testNum)
                if solution != None:
                    return solution
        return None

print(findRTP(8))