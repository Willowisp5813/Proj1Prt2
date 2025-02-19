from LaskerMorris import LaskerMorris as LM
import sys

def main():

    #initialize the game
    gameBoard = LM()
    #print(gameBoard)

    playerValue = sys.stdin.readline().strip()

    #handle incorrect player assignment
    if playerValue not in ["blue", "orange"]:
        print("Invalid start input:", gameBoard.isPlayer, file=sys.stderr)
        return


    if(playerValue == "blue"):
        gameBoard.isPlayer = 1
        #isBlueTurn is true by default, no change needed here
    elif(playerValue == "orange"):
        gameBoard.isPlayer = 2
    else:
        print(f"Invalid player input: {playerValue}", file=sys.stderr, flush=True)
        sys.exit(1)
        #gameBoard.gameFinished = True

    while(not gameBoard.gameFinished):
        player_id = 1 if gameBoard.isBlueTurn else 2
        
        if gameBoard.isPlayer == player_id:
            move = gameBoard.best_move(player_id)
            if move and len(move) == 3:
                move_str = gameBoard.convertToList(move)
                gameBoard.makeMove(move_str)
                print(f"{move_str[0]} {move_str[1]} {move_str[2]}", flush=True)
            else:
                print("No valid moves available", file=sys.stderr, flush=True)
                sys.exit(1)
                

        else:
            try:
                move_input = sys.stdin.readline().strip()

                if move_input.startswith("END:"):
                    print(move_input, flush=True)
                    sys.exit(1)
                    
                move_parts = move_input.split()

                if len(move_parts) != 3:
                    print(f"Invalid move format received: {move_input}", file=sys.stderr, flush=True)
                    sys.exit(1)
                
                try:
                    gameBoard.makeMove(move_parts)
                    
                except Exception as e:
                    print(f"Error processing move input: {move_input}, Error: {e}", file=sys.stderr, flush=True)
                    sys.exit(1)
            
            except EOFError:
                break

        
    print("Game Over!", flush=True)

if __name__ == "__main__":
    main()


""" elif not gameBoard.isBlueTurn and gameBoard.isPlayer == 2:
        move = gameBoard.best_move(player_id)
        if move:
            gameBoard.makeMove(move)
            print(f"Orange move: {move}")
        else:
            print("No valid moves available, game over")
            break

    else:
        move_input = input().strip().split()
        if len(move_input) != 3:
            print("Invalid move format. Use <start> <end> <capture>")
            continue

        move = [gameBoard.getIndex(move_input[0]),
                gameBoard.getIndex(move_input[1]),
                gameBoard.getIndex(move_input[2])]
        
        gameBoard.makeMove(move)
        print(f"Player move: {move}")

    if gameBoard.gameFinished:
        print("Game Over!") 

     if(gameBoard.isBlueTurn):
        #if is blues turn and you are blue, make move
        if(gameBoard.isPlayer == 1):
            move = gameBoard.best_move(pla)
            gameBoard.makeMove(move)
            print("h1 a1 r0")
        #else wait for move
        else:
            moveMade = input().split()
            gameBoard.makeMove(moveMade)
    else:
        #if is oranges turn and you are orange, make move
        if(gameBoard.isPlayer == 2):
            move = gameBoard.best_move()
            gameBoard.makeMove(move)
            print("h2 b2 r0")
        #else wait for move
        else:
            moveMade = input().split()
            gameBoard.makeMove(moveMade) """