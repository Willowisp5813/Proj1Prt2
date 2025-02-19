import copy
from MillIndex import getMillIndex
from AdjacencyMatrix import getAdjacent
import time
from MinMaxNode import MinMaxNode

class LaskerMorris:
    def __init__(self):
        self.isBlueTurn = True
        self.time_limit = 5 #seconds per turn
        self.stalemate_threshold = 20 #number of consecutive moves with no mill formed or stone removed
        self.stalemate_counter = 0
        self.boardData = [[0 for col in range(3)] for row in range(9)]
        self.boardData[8][0] = 10 #Blues hand
        self.boardData[8][1] = 10 #Oranges hand
        self.blueTotalTiles = 10
        self.orangeTotalTiles = 10
        self.gameFinished = False
        self.isPlayer = 0
        #blue player is 1, orange player is 2

    def __str__(self):
        return (f"{self.boardData[7][0]}     {self.boardData[7][1]}     {self.boardData[7][2]}\n" + \
                f"  {self.boardData[6][0]}   {self.boardData[6][1]}   {self.boardData[6][2]}\n" + \
                f"    {self.boardData[5][0]} {self.boardData[5][1]} {self.boardData[5][2]}\n" + \
                f"{self.boardData[3][0]} {self.boardData[3][1]} {self.boardData[3][2]}   {self.boardData[4][0]} {self.boardData[4][1]} {self.boardData[4][2]}\n" + \
                f"    {self.boardData[2][0]} {self.boardData[2][1]} {self.boardData[2][2]}\n" + \
                f"  {self.boardData[1][0]}   {self.boardData[1][1]}   {self.boardData[1][2]}\n" + \
                f"{self.boardData[0][0]}     {self.boardData[0][1]}     {self.boardData[0][2]}\n" + \
                f"blue hand: {self.boardData[8][0]}, orange hand: {self.boardData[8][1]}")

    """
    the board is stored within an array of length 3 arrays in this arrangement
    [h1 h2 r0] index 8
    [a7       d7       g7] index 7
    [   b6    d6    f6   ] 6
    [      c5 d5 e5      ] 5
    [a4 b4 c4]  [e4 f4 g4] 3 4
    [      c3 d3 e3      ] 2
    [   b2    d2    f2   ] 1
    [a1       d1       g1] 0
    
    0 0 is the bottom left of the board
    
    Move input:
    A B C
    A: current position of piece
        Either a location or h1 for blue hand/h2 for orange hand
        Pieces can be moved even when the hand is not empty
    B: location to place/move piece
        If moving from board two options
            If there are more than 3 remaining stone total, must be adjacent
            Otherwise anywhere
    C: if move makes no mill
            Must be r0
        else if mill is created
            Location of stone to remove (cannot be part of a mill unless it has to be)

    Invalid move means auto loss

    Game finishes when
        A player has less than 2 stones (loss)
        No possible moves (more than 3 stones and no adjacent openings)
        time limit breached
        stalemate reached
        invalid move made
    """
    
    def makeMove(self, move):
        startTime = time.time()
        moveFrom = self.getIndex(move[0])
        moveTo = self.getIndex(move[1])
        takeFrom = self.getIndex(move[2])

        if(self.validMove(moveFrom, moveTo)):
            if(moveFrom[0] == 8):
                if(self.boardData[moveFrom[0]][moveFrom[1]] == 0):
                    print("invalid move: hand empty")
                    self.gameFinished = True
                    return
                else:
                    self.boardData[moveFrom[0]][moveFrom[1]] -= 1
            else:
                self.boardData[moveFrom[0]][moveFrom[1]] = 0

            self.boardData[moveTo[0]][moveTo[1]] = (1 if self.isBlueTurn else 2)
        else:
            self.gameFinished = True
            return
        
        if(self.isPartOfMill(moveTo, self.boardData)):
            self.stalemate_counter = 0
            if(takeFrom == [8, 2]):
                pass
            elif(self.isPartOfMill(takeFrom, self.boardData) and not self.isOnlyMills(self.isBlueTurn)):
                print("invalide move: removing stone that is in a mill")
                self.gameFinished = True
                return
            else: 
                self.boardData[takeFrom[0]][takeFrom[1]] = 0
                if(self.isBlueTurn):
                    self.orangeTotalTiles -= 1
                else:
                    self.blueTotalTiles -= 1
        elif(takeFrom != [8, 2]):
            print("invalid move: attempting to remove a stone without making a mill")
            self.gameFinished = True
            return
        else:
            self.stalemate_counter += 1

        self.isBlueTurn = not self.isBlueTurn
        endTime = time.time()
        timeElapsed = endTime - startTime
        #print(f"{timeElapsed}")
        self.checkGameEnd(timeElapsed)

    def validMove(self, moveFrom, moveTo):
        if(self.boardData[moveFrom[0]][moveFrom[1]] == 0 or \
           self.boardData[moveFrom[0]][moveFrom[1]] == (2 if self.isBlueTurn else 1)):
            print("invalid move: moving from empty space, or moving opponent's stone")
            return False
        
        if((self.isBlueTurn and self.blueTotalTiles) <= 3 or (not self.isBlueTurn and self.orangeTotalTiles <= 3)):
            return True
        elif(moveFrom in getAdjacent(moveTo)):
            return True
        else:
            print("invalid move: moving from a non-adjacent space")
            return False
    
    def isPartOfMill(self, moveTo, boardData):
        millIndexes = getMillIndex(moveTo)
        playerValue = boardData[moveTo[0]][moveTo[1]]
        for i in range(2):
            if(boardData[millIndexes[i][0][0]][millIndexes[i][0][1]] == playerValue and \
                boardData[millIndexes[i][1][0]][millIndexes[i][1][1]] == playerValue and \
                boardData[millIndexes[i][2][0]][millIndexes[i][2][1]] == playerValue): 
                return True
            
        return False

    def isOnlyMills(self, isBlueTurn):
        valueToCheck = 2 if isBlueTurn else 1
        onlyMills = True
        for i in range(8):
            for j in range(3):
                if(self.boardData[i][j] == valueToCheck):
                    onlyMills = self.isPartOfMill([i, j], self.boardData)
                    if(not onlyMills):
                        return False

        return onlyMills

    
    def checkGameEnd(self, timeElapsed):
        if(self.gameFinished):
            return True
        
        if(self.blueTotalTiles <= 2 or self.orangeTotalTiles <= 2):
            self.gameFinished = True
            return True

        if(self.stalemate_counter >= self.stalemate_threshold):
            self.gameFinished = True
            return True
        
        '''if(timeElapsed >= self.time_limit):
            self.gameFinished = True
            return True'''

        #Check for imobilization
        if(self.imobilized(self.isBlueTurn)):
            self.gameFinished = True
            return True
        
        
    def imobilized(self, isBlueTurn):
        valueToCheck = 1 if isBlueTurn else 2
        if(isBlueTurn and self.boardData[8][0] > 0 or not isBlueTurn and self.boardData[8][1] > 0):
            return False
        
        imobilized = True
        for i in range(8):
            for j in range(3):
                if(self.boardData[i][j] == valueToCheck):
                    adjSpaces = getAdjacent([i, j])
                    for x in adjSpaces:
                        imobilized = self.boardData[x[0]][x[1]] != 0
                        if(not imobilized):
                            return False
        
        return True


#TO FIX : Return correct score for correct player 
    def evaluate(self, boardNode):
        bluePieces = boardNode.boardData[8][0]
        orangePieces = boardNode.boardData[8][1]
        blueMills = self.countMills(1, boardNode.boardData) 
        orangeMills = self.countMills(2, boardNode.boardData)  

        score = 0
        score += (bluePieces - orangePieces) * 5  
        score += (blueMills - orangeMills) * 10 
        #print(score)

        return score if self.isPlayer == 1 else -score

    def countMills(self, player, boardData):
        count = 0
        for i in range(9):
            for j in range(3):
                if boardData[i][j] == player and self.isPartOfMill([i, j], boardData):
                    count += 1
        return count

#TO FIX: getpossible moves function and pass playerid to eval 
    def minimax(self, node, depth, alpha, beta, is_maximizing, player_id):
        """Minimax algorithm with alpha-beta pruning."""
        if depth == 0:
            return self.evaluate(node)

        possible_moves = self.generate_moves(node, player_id)
        if not possible_moves:
            return self.evaluate(node)

        if is_maximizing:
            max_eval = float('-inf')
            for move in possible_moves:
                eval_score = self.minimax(move, depth - 1, alpha, beta, False, player_id)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            opponent_id = 1 if player_id == 2 else 2
            for move in possible_moves:
                eval_score = self.minimax(move, depth - 1, alpha, beta, True, opponent_id)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def best_move(self, player_id, depth=3):
        """Determine the best move using minimax algorithm with alpha-beta pruning."""
        root = MinMaxNode(copy.deepcopy(self.boardData), None, None, self.isBlueTurn)
        possible_moves = self.generate_moves(root, player_id)
        best_score = float('-inf')
        best_choice = None

        for move in possible_moves:
            score = self.minimax(move, depth - 1, float('-inf'), float('inf'), False, player_id)
            if score > best_score:
                best_score = score
                best_choice = move.moveToHere

        #print(best_choice)
        return best_choice 
    
    def generate_moves(self, node, player_id):
        output = [] #array of MinMaxNode objects that are the children of this node
        board = node.boardData
        is_blue_turn = (player_id == 1)
        handId = board[8][0] if is_blue_turn else board[8][1]
        opponent_id = 2 if is_blue_turn else 1
        player_pieces = 0
        movable_positions = []
        
        #count player's pieces on board and collect the movable positions
        for row in range(8):
            for col in range(3):
                if board[row][col] == player_id:
                    player_pieces+= 1
                    movable_positions.append((row, col))

        player_pieces += handId

        #handle case for if hand still has pieces left
        if handId > 0:
            for row in range(8):
                for col in range(3):
                    if board[row][col] == 0: #this means the spot is empty
                        move = ([8, 0] if is_blue_turn else [8, 1], [row, col], [8, 2])
                        board[row][col] = player_id  #temporarily place a piece here
                        if self.isPartOfMill([row, col], board):
                            capture_moves = self.getValidCaptures(board, opponent_id)
                            for capture in capture_moves:
                                output.append(MinMaxNode(copy.deepcopy(board), [move[0], move[1], capture], node, not node.isBlueTurn))
                        else:
                            output.append(MinMaxNode(copy.deepcopy(board), move, node, not node.isBlueTurn))
                        board[row][col] = 0 #this is a reset


        #handle case for if hand has no pieces left
        if player_pieces > 3:
            for piece in movable_positions:
                adjacentPositions = getAdjacent(piece)
                for moveTo in adjacentPositions:
                    if board[moveTo[0]][moveTo[1]] == 0:    #checking only empty spots
                        move = (piece, moveTo, [8, 2])      #no capture
                        board[piece[0]][piece[1]] = 0       #temporary piece move
                        board[moveTo[0]][moveTo[1]] = player_id 
                        if self.isPartOfMill(moveTo, board):
                            capture_moves = self.getValidCaptures(board, opponent_id)
                            for capture in capture_moves:
                                output.append(MinMaxNode(copy.deepcopy(board), [move[0], move[1], capture], node, not node.isBlueTurn))
                        else:
                            output.append(MinMaxNode(copy.deepcopy(board), move, node, not node.isBlueTurn))
                        board[piece[0]][piece[1]] = player_id   #this is a reset
                        board[moveTo[0]][moveTo[1]] = 0

        #handle case for if player has 3 or less pieces
        elif player_pieces == 3:
            for piece in movable_positions:
                for row in range(8):
                    for col in range(3):
                        if board[row][col] == 0:                #checking only empty spots
                            move = (piece, [row, col], [8, 2])  #no capture
                            board[piece[0]][piece[1]] = 0       #temporary piece move
                            board[row][col] = player_id
                            if self.isPartOfMill([row, col], board):
                                capture_moves = self.getValidCaptures(board, opponent_id)
                                for capture in capture_moves:
                                    output.append(MinMaxNode(copy.deepcopy(board), [move[0], move[1], capture], node, not node.isBlueTurn))
                            else:
                                output.append(MinMaxNode(copy.deepcopy(board), move, node, not node.isBlueTurn))
                            board[piece[0]][piece[1]] = player_id   #this is a reset
                            board[row][col] = 0
                    
        return output

        
        """ for i in range(9):
            if(i == 8): #check moves from the hand

            for j in range(3):
                #check moves from each board state """
        
    def getValidCaptures(self, board, opponent_id):

        #get all valid capture moves for a player
            #note: player must have just formed a mill
        captureMoves = []
        for row in range(8):
            for col in range(3):
                if board[row][col] == opponent_id and not self.isPartOfMill([row, col], board):
                    captureMoves.append([row, col])

        #handles situation where if all opponent pieces are in mills, allow any capture
        if not captureMoves:
            for row in range(8):
                for col in range(3):
                    if board[row][col] == opponent_id:
                        captureMoves.append([row, col])

        return captureMoves



    def getIndex(self, move):
        match move:
            case 'h1':
                return [8, 0]
            case 'h2':
                return [8, 1]
            case 'a1':
                return [0, 0]
            case 'd1':
                return [0, 1]
            case 'g1':
                return [0, 2]
            case 'b2':
                return [1, 0]
            case 'd2':
                return [1, 1]
            case 'f2':
                return [1, 2]
            case 'c3':
                return [2, 0]
            case 'd3':
                return [2, 1]
            case 'e3':
                return [2, 2]
            case 'a4':
                return [3, 0]
            case 'b4':
                return [3, 1]
            case 'c4':
                return [3, 2]
            case 'e4':
                return [4, 0]
            case 'f4':
                return [4, 1]
            case 'g4':
                return [4, 2]
            case 'c5':
                return [5, 0]
            case 'd5':
                return [5, 1]
            case 'e5':
                return [5, 2]
            case 'b6':
                return [6, 0]
            case 'd6':
                return [6, 1]
            case 'f6':
                return [6, 2]
            case 'a7':
                return [7, 0]
            case 'd7':
                return [7, 1]
            case 'g7':
                return [7, 2]
            case _:
                return [8, 2]
            
    def convertToList(self, move):
        output = []
        for part in move:
            match part:
                case [8, 0]:
                    output.append("h1")
                case [8, 1]:
                    output.append("h2")
                case [0, 0]:
                    output.append("a1")
                case [0, 1]:
                    output.append("d1")
                case [0, 2]:
                    output.append("g1")
                case [1, 0]:
                    output.append("b2")
                case [1, 1]:
                    output.append("d2")
                case [1, 2]:
                    output.append("f2")
                case [2, 0]:
                    output.append("c3")
                case [2, 1]:
                    output.append("d3")
                case [2, 2]:
                    output.append("e3")
                case [3, 0]:
                    output.append("a4")
                case [3, 1]:
                    output.append("b4")
                case [3, 2]:
                    output.append("c4")
                case [4, 0]:
                    output.append("e4")
                case [4, 1]:
                    output.append("f4")
                case [4, 2]:
                    output.append("g4")
                case [5, 0]:
                    output.append("c5")
                case [5, 1]:
                    output.append("d5")
                case [5, 2]:
                    output.append("e5")
                case [6, 0]:
                    output.append("b6")
                case [6, 1]:
                    output.append("d6")
                case [6, 2]:
                    output.append("f6")
                case [7, 0]:
                    output.append("a7")
                case [7, 1]:
                    output.append("d7")
                case [7, 2]:
                    output.append("g7")
                case _:
                    output.append("r0")
        return output