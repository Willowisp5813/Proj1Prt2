from LaskerMorris import LaskerMorris as LM

gameBoard = LM(True)
print(gameBoard)

while(not gameBoard.gameFinished):
    gameMove = input().split()
    gameBoard.makeMove(gameMove)
    print(gameBoard)