from LaskerMorris import LaskerMorris as LM

gameBoard = LM(True)
#print(gameBoard)
playerValue = input()
if(playerValue == "blue"):
    gameBoard.isPlayer = 1
elif(playerValue == "orange"):
    gameBoard.isPlayer = 2
    gameBoard.isBlueTurn = False
else:
    print("invalid input")
    gameBoard.gameFinished = True

while(not gameBoard.gameFinished):
    if(gameBoard.isBlueTurn):
        if(gameBoard.isPlayer == 1):
            #move = gameBoard.minmax()
            print("h1 a1 r0")
        else:
            moveMade = input().split()
            gameBoard.makeMove(moveMade)
    else:
        if(gameBoard.isPlayer == 2):
            #move = gameBoard.minmax()
            print("h2 b2 r0")
        else:
            moveMade = input().split()
            gameBoard.makeMove(moveMade)