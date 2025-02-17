from LaskerMorris import LaskerMorris as LM

gameBoard = LM()
#print(gameBoard)
playerValue = input()
if(playerValue == "blue"):
    gameBoard.isPlayer = 1
    #isBlueTurn is true by default, no change needed here
elif(playerValue == "orange"):
    gameBoard.isPlayer = 2
    gameBoard.isBlueTurn = False
else:
    print("invalid input")
    gameBoard.gameFinished = True

while(not gameBoard.gameFinished):
    if(gameBoard.isBlueTurn):
        #if is blues turn and you are blue, make move
        if(gameBoard.isPlayer == 1):
            move = gameBoard.best_move()
            print("h1 a1 r0")
        #else wait for move
        else:
            moveMade = input().split()
            gameBoard.makeMove(moveMade)
    else:
        #if is oranges turn and you are orange, make move
        if(gameBoard.isPlayer == 2):
            move = gameBoard.best_move()
            print("h2 b2 r0")
        #else wait for move
        else:
            moveMade = input().split()
            gameBoard.makeMove(moveMade)