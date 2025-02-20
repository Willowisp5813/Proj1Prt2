class MinMaxNode:
    def __init__(self, boardData, moveToHere, parent, isBlueTurn):
        self.boardData = boardData
        self.moveToHere = moveToHere
        #Turn start AFTER the move is made. IE whos turn is next
        self.isBlueTurn = isBlueTurn
        self.parent = parent