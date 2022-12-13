import random
import sys

def drawBoard(board):

    xAxis = '  +---+---+---+---+---+---+---+---+'
    yAxis = '  |   |   |   |   |   |   |   |   |'

    print('    1   2   3   4   5   6   7   8')
    print(xAxis)
    for y in range(8):
        print(yAxis)
        print(y+1, end=' ')
        for x in range(8):
            print('| %s' % (board[x][y]), end=' ')
        print('|')
        print(yAxis)
        print(xAxis)


def resetBoard(board):

    for x in range(8):
        for y in range(8):
            board[x][y] = ' '


    board[3][3] = 'W'
    board[3][4] = 'B'
    board[4][3] = 'B'
    board[4][4] = 'W'


def getNewBoard():

    board = []
    for i in range(8):
        board.append([' '] * 8)

    return board


def isValidMove(board, tile, xstart, ystart):

    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile

    if tile == 'W':
        otherTile = 'B'
    else:
        otherTile = 'W'

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and board[x][y] == otherTile:

            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:

                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = ' '
    if len(tilesToFlip) == 0:
        return False
    return tilesToFlip


def isOnBoard(x, y):

    return x >= 0 and x <= 7 and y >= 0 and y <=7


def getBoardWithValidMoves(board, tile):

    cBoard = getBoardCopy(board)

    for x, y in getValidMoves(cBoard, tile):
        cBoard[x][y] = '.'
    return cBoard


def getValidMoves(board, tile):

    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves


def getScoreOfBoard(board):

    wscore = 0
    bscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'W':
                wscore += 1
            if board[x][y] == 'B':
                bscore += 1
    return {'W':wscore, 'B':bscore}


def enterPlayerTile():


    tile = ''
    while not (tile == 'W' or tile == 'B'):
        print('Do you want to play as W (white) or B (black)? ')
        tile = input().upper()


    if tile == 'W':
        return ['W', 'B']
    else:
        return ['B', 'W']


def whoGoesFirst():

    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def playAgain():

    print('Would you like to play again? (yes or no)')
    return input().lower().startswith('y')


def makeMove(board, tile, xstart, ystart):


    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def getBoardCopy(board):

    cBoard = getNewBoard()

    for x in range(8):
        for y in range(8):
            cBoard[x][y] = board[x][y]

    return cBoard


def isOnCorner(x, y):

    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


def getPlayerMove(board, playerTile):
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move as xy coordinates based on numbers lining the board, \nor type quit to end the game (if this message pops up again your move is invalid)')
        move = input().lower()
        if move == 'quit':
            return 'quit'

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('Please type in the move as xy')

    return [x, y]


def getComputerMove(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves)

    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]


    bestScore = -1
    for x, y in possibleMoves:
        cBoard = getBoardCopy(board)
        makeMove(cBoard, computerTile, x, y)
        score = getScoreOfBoard(cBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove


def showPoints(playerTile, computerTile):

    scores = getScoreOfBoard(mainBoard)
    print('You have %s points. The computer has %s points.' % (scores[playerTile], scores[computerTile]))



print('Let the game begin! \n Rules: The objective is to have the majority of your color, white (W) or black (B) on the board \n your move must border the opponents pieces in order to outflank them ')

while True:
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    playerTile, computerTile = enterPlayerTile()
    showHints = False
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')

    while True:
        if turn == 'player':
            drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            move = getPlayerMove(mainBoard, playerTile)
            if move == 'quit':
                print('Thanks for playing!')
                sys.exit()
            else:
                makeMove(mainBoard, playerTile, move[0], move[1])

            if getValidMoves(mainBoard, computerTile) == []:
                break
            else:
                turn = 'computer'

        else:
            drawBoard(mainBoard)
            showPoints(playerTile, computerTile)
            input('Press Enter to see the computer\'s move.')
            x, y = getComputerMove(mainBoard, computerTile)
            makeMove(mainBoard, computerTile, x, y)

            if getValidMoves(mainBoard, playerTile) == []:
                break
            else:
                turn = 'player'


    drawBoard(mainBoard)
    scores = getScoreOfBoard(mainBoard)
    print('W scored %s points. B scored %s points.' % (scores['W'], scores['B']))
    if scores[playerTile] > scores[computerTile]:
        print('You beat the computer by %s points!' % (scores[playerTile] - scores[computerTile]))
    elif scores[playerTile] < scores[computerTile]:
        print('You lost by %s points.' % (scores[computerTile] - scores[playerTile]))
    else:
        print('Its a tie!')

    if not playAgain():
        break