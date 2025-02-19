class MinMaxNode:
    def __init__(self, boardData, moveToHere, parent, isBlueTurn):
        self.boardData = boardData
        self.moveToHere = moveToHere
        self.isBlueTurn = isBlueTurn
        self.parent = parent