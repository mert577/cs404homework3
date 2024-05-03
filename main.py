import random
import copy


class Island:
    def __init__(self, x, y, max_bridge_count):
        self.x = x
        self.y = y
        self.max_bridge_count = max_bridge_count
        self.total_bridge_count = 0
        self.used = False


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y



class Bridge:
    def __init__(self, island1, island2):
        self.island1 = island1
        self.island2 = island2
        self.is_horizontal = island1.x == island2.x
        self.whoPlaced = -1
        self.scoreGained = 0

#move class
class Move:
    def __init__(self, move_type, island1=None, island2=None, label=0, labeled_island=None, bridge=None):
        self.move_type = move_type
        self.island1 = island1
        self.island2 = island2
        self.label = label
        self.labeled_island = labeled_island


#move type enum
class MoveType:
    LABEL_ISLAND = 1
    PLACE_BRIDGE = 2





def get_island(x, y, islands):
    for island in islands:
        if island.x == x and island.y == y:
            return island
    return None


def read_islands_from_file(filename):
    islands = []
    with open(filename, 'r') as file:
    #for every element in the file the x and y is the row and column of the island if the island is a number
    #remove spaces and from the file and read the islands

        non_empty_lines = [line for line in file if line.strip()]
        for i, line in enumerate(non_empty_lines):
            line_without_spaces = line.replace(" ","")
            for j, char in enumerate(line_without_spaces):
                if char.isdigit():
                    islands.append(Island(j, i, int(char)))
    return islands

def print_islands(islands):
    for island in islands:
        print(island.x, island.y, island.max_bridge_count)

print("Islands: ")
print_islands(read_islands_from_file("levelConfig.txt"))


        


def fromStateToBoard(islands, bridges, boardSize):
    #create a nxn matrix with the islands and bridges
    board = [["." for i in range(boardSize)] for j in range(boardSize)]
    #place the islands on the board
    for island in islands:
        board[island.y][island.x] = str(island.max_bridge_count)

    #place bridges on the board with a horizontal or vertical line if two bridges use = and X
    for bridge in bridges:
        if bridge.is_horizontal:
            #make the cells between the islands - 
            #check if there exists two bridges between the same islands
            count = 0
            for b in bridges:
                if (b.island1 == bridge.island1 and b.island2 == bridge.island2) or (b.island1 == bridge.island2 and b.island2 == bridge.island1):
                    count += 1
            
            placedSymbol = "-"
            if count == 2:
                placedSymbol = "="


            if bridge.island1.x < bridge.island2.x:
                for i in range(bridge.island1.x+1, bridge.island2.x):
                    board[bridge.island1.y][i] = placedSymbol
            else:
                for i in range(bridge.island2.x+1, bridge.island1.x):
                    board[bridge.island1.y][i] = placedSymbol
        else:
            #make the cells between the islands |
            #check if there exists two bridges between the same islands
            count = 0
            for b in bridges:
                if (b.island1 == bridge.island1 and b.island2 == bridge.island2) or (b.island1 == bridge.island2 and b.island2 == bridge.island1):
                    count += 1
            
            placedSymbol = "|"
            if count == 2:
                placedSymbol = "X"

            if bridge.island1.y < bridge.island2.y:
                for i in range(bridge.island1.y+1, bridge.island2.y):
                    board[i][bridge.island1.x] = placedSymbol
            else:
                for i in range(bridge.island2.y+1, bridge.island1.y):
                    board[i][bridge.island1.x] = placedSymbol

    #print the board
    for i in range(boardSize):
        for j in range(boardSize):
            print(board[i][j],end="")
        print()





#Move_Bridge adds a bridge between two islands
def can_place_brigdge(island1X,island1Y, island2X, island2Y, bridges,islands):

    _island1 = get_island(island1X, island1Y,islands)
    _island2 = get_island(island2X, island2Y,islands)


    #check if the islands exist
    if _island1 is None or _island2 is None:
         # print("ILLEGAL_MOVE: Cant place a bridge between two islands that dont exist")
          return -1


    #check if the islands are not labeled
    if _island1.max_bridge_count == 0 or _island2.max_bridge_count == 0:
       # print("ILLEGAL_MOVE: Cant place a bridge between two islands that are not labeled")
        return -1


     #check if there is already a bridge between the two islands this is allowed only up to 2 bridges
    count = 0
    for bridge in bridges:
        currentIsland1 = get_island(bridge.island1.x, bridge.island1.y,islands)
        currentIsland2 = get_island(bridge.island2.x, bridge.island2.y,islands)
        if (currentIsland1.x == _island1.x and currentIsland1.y == _island1.y and currentIsland2.x == _island2.x and currentIsland2.y == _island2.y) or (currentIsland1.x == _island2.x and currentIsland1.y == _island2.y and currentIsland2.x == _island1.x and currentIsland2.y == _island1.y):
            count += 1

    
    if count >= 2:
         # print("ILLEGAL_MOVE: Cant place more than 2 bridges between two islands")
          return -1
    
    #check if the islands are not the same
    if _island1 == _island2:
      #  print("ILLEGAL_MOVE: Cant place a bridge between the same island")
        return -1

    #check if the total bridge count of the islands is not equal to the max bridge count
    if _island1.total_bridge_count == _island1.max_bridge_count or _island2.total_bridge_count == _island2.max_bridge_count:
      #  print("ILLEGAL_MOVE: Cant place a bridge between two islands that have reached their max bridge count")
        return -1
    



    #check if the bridge crosses another bridge
    for bridge in bridges:
        #check if the bridge is not the same as the bridge that is being placed
        if (bridge.island1.x == _island1.x and bridge.island1.y == _island1.y and bridge.island2.x == _island2.x and bridge.island2.y == _island2.y) or (bridge.island1.x == _island2.x and bridge.island1.y == _island2.y and bridge.island2.x == _island1.x and bridge.island2.y == _island1.y):
            continue
        if do_intersect((_island1.x, _island1.y), (_island2.x, _island2.y), (bridge.island1.x, bridge.island1.y), (bridge.island2.x, bridge.island2.y)):
          #  print("ILLEGAL_MOVE: Cant place a bridge that crosses another bridge")
            return -1

    #check if the islands are on the same row or column and there is no island in between
    if _island1.x == _island2.x:
        if _island1.y < _island2.y:
            for i in range(_island1.y+1, _island2.y):
                if get_island(_island1.x, i,islands) is not None:
            #        print("ILLEGAL_MOVE: Cant place a bridge over an island")
                    return -1
        else:
            for i in range(_island2.y+1, _island1.y):
                if get_island(_island1.x, i,islands) is not None:
             #       print("ILLEGAL_MOVE: Cant place a bridge over an island")
                    return -1

        return True
        
       
        
    elif _island1.y == _island2.y:
        if _island1.x < _island2.x:
            for i in range(_island1.x+1, _island2.x):
                if get_island(i, _island1.y,islands) is not None:
              #      print("ILLEGAL_MOVE: Cant place a bridge over an island")
                    return -1
        else:
            for i in range(_island2.x+1, _island1.x):
                if get_island(i, _island1.y,islands) is not None:
          #          print("ILLEGAL_MOVE: Cant place a bridge over an island")
                    return -1
                


        return True
    
    else:
       # print("ILLEGAL_MOVE: Cant place a bridge between two islands that are not on the same row or column")
        return -1
        
def print_possible_moves(moves):

    if len(moves) == 0:
        print("No possible moves")
    print("---LIST OF ALL POSSIBLE MOVES---")
    for move in moves:
        if move.move_type == MoveType.LABEL_ISLAND:
            print("Label Island: ", move.labeled_island.x, move.labeled_island.y, move.label)
        else:
            print("Place Bridge: ", move.island1.x, move.island1.y, move.island2.x, move.island2.y)

def generate_all_non_illegal_moves(islands, bridges):
    moves = []
    for island in islands:
        if island.max_bridge_count == 0:
            moves.append(Move(MoveType.LABEL_ISLAND, labeled_island=island, label=3))
            moves.append(Move(MoveType.LABEL_ISLAND, labeled_island=island, label=4))
    for i in range(len(islands)):
        for j in range(i+1, len(islands)):
            island1 = islands[i]
            island2 = islands[j]
            possibleMove = Move(MoveType.PLACE_BRIDGE, island1=island1, island2=island2)

            #set if horizontal or vertical
            
            
            if can_place_brigdge(island1.x, island1.y, island2.x,island2.y,bridges,islands) != -1:
                moves.append(possibleMove)

    return moves

def printBoard(islands,bridges,boardSize):
     #create a nxn matrix with the islands and bridges
     #where n is 2*boardsize-1
    board = [["." for i in range(2*boardSize-1)] for j in range(2*boardSize-1)]

    #place the islands on the board fix the x and y coordinates by dividing by 2
    for island in islands:
        board[island.y*2][island.x*2] = str(island.max_bridge_count)
    
    #place the bridges on the board

    for bridge in bridges:
        #if the bridge is horizontal
        if not bridge.is_horizontal:
            placedSymbol = "-"
            #if there are two bridges between the same islands change the symbol
            count = 0
            for b in bridges:
                if (b.island1 == bridge.island1 and b.island2 == bridge.island2) or (b.island1 == bridge.island2 and b.island2 == bridge.island1):
                    count += 1
            
            if count == 2:
                placedSymbol = "="

            if bridge.island1.x < bridge.island2.x:
                for i in range(bridge.island1.x*2+1, bridge.island2.x*2):
                    board[bridge.island1.y*2][i] = placedSymbol
            else:
                for i in range(bridge.island2.x*2+1, bridge.island1.x*2):
                    board[bridge.island1.y*2][i] = placedSymbol
            
        else:
            print("Vertical bridge")
            placedSymbol = "|"
            count = 0
            for b in bridges:
                if (b.island1 == bridge.island1 and b.island2 == bridge.island2) or (b.island1 == bridge.island2 and b.island2 == bridge.island1):
                    count += 1
            
            if count == 2:
                placedSymbol = "X"

            if bridge.island1.y < bridge.island2.y:
               
                for i in range(bridge.island1.y*2+1, bridge.island2.y*2):
                    board[i][bridge.island1.x*2] = placedSymbol
            else:
                for i in range(bridge.island2.y*2+1, bridge.island1.y*2):
                    board[i][bridge.island1.x*2] = placedSymbol


    #print the board
    for i in range(2*boardSize-1):
        for j in range(2*boardSize-1):
            print(board[i][j],end="")
        print()

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # colinear
    return 1 if val > 0 else 2  # clock or counterclock wise

def do_intersect(p1, p2, q1, q2):
    o1 = orientation(p1, p2, q1)
    o2 = orientation(p1, p2, q2)
    o3 = orientation(q1, q2, p1)
    o4 = orientation(q1, q2, p2)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    return False  # Doesn't fall in any of the above cases



import pygame

# Initialize Pygame
pygame.init()

# Set up some constants


def draw_grid():
    for i in range(BOARD_SIZE-1):
        for j in range(BOARD_SIZE-1):

            #padding from window border so the grid is centered
            
            rect = pygame.Rect(i * CELL_SIZE+PADDING, j * CELL_SIZE+PADDING, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(window, WHITE, rect, 1)  # Draw the cell border


def islandCoordToPixelCoord(x, y):
    #convert the island coordinates to pixel coordinates islands are on the corners of the grid
    return (x * CELL_SIZE+PADDING, y * CELL_SIZE+PADDING)

def draw_islands(islands):
    for island in islands:
        x = island.x
        y = island.y
        #draw islands on the corners of the grid
        pygame.draw.circle(window, WHITE, islandCoordToPixelCoord(x, y), CELL_SIZE*.20)

        #draw the number of bridges that can be connected to the island if its not 0
        if island.max_bridge_count != 0:
            font = pygame.font.Font(None, 36)
            text = font.render(str(island.max_bridge_count), True, BLACK)
            text_rect = text.get_rect(center=islandCoordToPixelCoord(x, y))
            window.blit(text, text_rect)
        
        #print the total number of bridges that are connected to the island Wwith a left offset
        font = pygame.font.Font(None, 36)
        text = font.render(str(island.total_bridge_count), True, RED)
        text_rect = text.get_rect(center=(islandCoordToPixelCoord(x, y)[0]-20, islandCoordToPixelCoord(x, y)[1]))
        window.blit(text, text_rect)

def calculate_bridge_score(bridge):
    #after a player places a bridge calculate the score of the bridge
    #based on the number of bridges thats connected to the islands
    score = bridge.island2.total_bridge_count +bridge.island1.total_bridge_count

    return score * bridge.whoPlaced
        
def draw_bridges(bridges):
    
    for bridge in bridges:
        island1 = bridge.island1
        island2 = bridge.island2
      
        offset = 10
        secondBridge = None

        count = 0
        #if there are two bridges connecting same islands offset the second bridge
        for b in bridges:
            if (b.island1 == island1 and b.island2 == island2) or (b.island1 == island2 and b.island2 == island1):
                count += 1
            if count == 2:
                secondBridge = b
                break
        
        if secondBridge == bridge:
            offset = -10

        #if player 1 placed the bridge color it red else color it blue
        if bridge.whoPlaced == 1:
            color = RED
        else:
            color = BLUE


        starCordsX,starCordsY = islandCoordToPixelCoord(island1.x, island1.y)
        endCordsX, endCordsY = islandCoordToPixelCoord(island2.x, island2.y)    
        
        if bridge.is_horizontal:
            starCords = (starCordsX+offset, starCordsY+offset)
            endCords = (endCordsX+offset, endCordsY+offset)
        else:
            starCords = (starCordsX+offset, starCordsY+offset)
            endCords = (endCordsX+offset, endCordsY+offset)
       

        pygame.draw.line(window, color, starCords, endCords, 5)
           
def label_island_at(x, y, label, islands):
    island = get_island(x, y,islands)
    if island is not None:
        island.max_bridge_count = label

def increase_bridge_count_at(x, y, islands):
    island = get_island(x, y, islands)
    if island is not None:
        island.total_bridge_count += 1



#This is the state transition function

def MakeMove(move, ISLANDSSTATE, BRIDGESSTATE,WHOSETURN):
    # Clone the islands and bridges
    NEW_ISLANDS = copy.deepcopy(ISLANDSSTATE)
    NEW_BRIDGES = copy.deepcopy(BRIDGESSTATE)

    if move.move_type == MoveType.LABEL_ISLAND:
      #  print("Move made: Label Island: ", move.labeled_island.x, move.labeled_island.y, move.label)
        label_island_at(move.labeled_island.x, move.labeled_island.y, move.label, NEW_ISLANDS)
        
    else:
        #append the bridge to the bridges list
      # print("Move made: Place Bridge: ", move.island1.x, move.island1.y, move.island2.x, move.island2.y)
        increase_bridge_count_at(move.island2.x, move.island2.y, NEW_ISLANDS)
        increase_bridge_count_at(move.island1.x, move.island1.y, NEW_ISLANDS)
        island1 = get_island(move.island1.x, move.island1.y, NEW_ISLANDS)
        island2 = get_island(move.island2.x, move.island2.y, NEW_ISLANDS)

        newBridge = Bridge(island1, island2)
        newBridge.whoPlaced = WHOSETURN
        newBridge.scoreGained =0
        if (not island1.used) and island1.max_bridge_count == island1.total_bridge_count:
            newBridge.scoreGained += island1.max_bridge_count
            island1.used = True
        
        if (not island2.used) and island2.max_bridge_count == island2.total_bridge_count:
            newBridge.scoreGained += island2.max_bridge_count
            island2.used = True
        newBridge.scoreGained *= WHOSETURN
        NEW_BRIDGES.append(newBridge)


    
    NEWTURN = WHOSETURN* -1
    
    return NEW_ISLANDS, NEW_BRIDGES,NEWTURN


#random move selection for debugging
def PlayRandomMove():

    #generate all possible moves
    moves = generate_all_non_illegal_moves(ISLANDS,BRIDGES)
    #if there are no possible moves return
    if len(moves) == 0:
        return
    #choose a random move
    
    random_move = random.choice(moves)
    return MakeMove(random_move,ISLANDS,BRIDGES,whoseTurn)

# human player move selection using the console
def get_player_move(islands, bridges):
    global whoseTurn
    genereatedMove = None
    while True:
        print("move formats: label x y value or bridge x1 y1 x2 y2")
        move = input("Enter your move: ")

        move_parts = move.split()
        if len(move_parts) == 4 and move_parts[0] == "label":
            x, y, value = map(int, move_parts[1:])
            #generate a move
            islandToLabel = get_island(x,y,islands)
            if islandToLabel.max_bridge_count == 0:
                return Move(MoveType.LABEL_ISLAND,labeled_island=islandToLabel,label=value)
        elif len(move_parts) == 5 and move_parts[0] == "bridge":
            x1, y1, x2, y2 = map(int, move_parts[1:])
            if can_place_brigdge(x1,y1,x2,y2, bridges,islands) != -1:  # You need to implement this function
                return Move(MoveType.PLACE_BRIDGE,island1=get_island(x1,y1,islands),island2=get_island(x2,y2,islands))
        print("Invalid move. Please enter a valid move.")

def draw_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render("Red Score: " + str(score)+ " Blue Score: "+ str(-score), True, WHITE)
    text_rect = text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT*.1))
    window.blit(text, text_rect)


#--------- AI AGENT -----------------#
def is_terminal_state(islands,bridges):
    if len(generate_all_non_illegal_moves(islands,bridges)) == 0:
        return True
    return False

def Evaluate_Board(bridges):
    score =0
    for b in bridges:
        score += b.scoreGained
    return score

def guess_move_score(move):
    if move.move_type == MoveType.LABEL_ISLAND:
        return 0
    else:
        #if the move is a bridge move calculate the score of the bridge
        island1 = move.island1
        island2 = move.island2
        score =0
        if island1.total_bridge_count+1 == island1.max_bridge_count:
            score += island1.max_bridge_count
        if island2.total_bridge_count+1 == island2.max_bridge_count:
            score += island2.max_bridge_count
        return score


def minimax(islands, bridges, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or is_terminal_state(islands, bridges):
       # print("Leaf node reached with the score: "+str(Evaluate_Board(bridges)))
        return Evaluate_Board(bridges)

    if maximizingPlayer == 1:
        maxEval = float('-inf')
        maxStateBridges = None

        possible_moves = generate_all_non_illegal_moves(islands, bridges)
        #sort the moves based on the score of the bridge
        possible_moves.sort(key=guess_move_score,reverse=True)
        
        for move in possible_moves:
            newIslands, newBridges, newTurn = MakeMove(move, islands, bridges, maximizingPlayer)
            eval = minimax(newIslands, newBridges, depth-1, alpha, beta, -maximizingPlayer)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
           # printBridges(newBridges)
            if beta <= alpha:
                break

     
        return maxEval
    else:
        minEval = float('inf')
        possible_moves = generate_all_non_illegal_moves(islands, bridges)
        #sort the moves based on the score of the bridge
        possible_moves.sort(key=guess_move_score,reverse=True)
        
        for move in possible_moves:
            newIslands, newBridges, newTurn = MakeMove(move, islands, bridges, maximizingPlayer)
            eval = minimax(newIslands, newBridges, depth-1, alpha, beta, -maximizingPlayer)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
           # printBridges(newBridges)
            if beta <= alpha:
                break
        return minEval




def ChooseBestCurrentMoveWithMinimax(islands, bridges, whoseTurn):
    bestMove = None
    bestScore = -1000 if whoseTurn == 1 else 1000

    for move in generate_all_non_illegal_moves(islands, bridges):
        newIslands, newBridges,newTurn = MakeMove(move, islands, bridges, whoseTurn)
        evalScore = minimax(newIslands, newBridges, -1, -1000, 1000, -whoseTurn)
        print("Move: "+str(move.move_type)+" Score: "+str(evalScore))

        if whoseTurn == 1 and evalScore > bestScore:
            bestMove = move
            bestScore = evalScore
        elif whoseTurn != 1 and evalScore < bestScore:
            bestMove = move
            bestScore = evalScore

    print("Choosing move with the best score: "+ str(bestScore))
    return bestMove


totalScore = 0

whoseTurn= 1

def printBridges(bridges):
    for b in bridges:
        print("Bridge: ",b.island1.x,b.island1.y,b.island2.x,b.island2.y,b.whoPlaced,b.scoreGained)


#game initialization


BOARD_SIZE = 3

ISLANDS = read_islands_from_file("levelConfig.txt")
BRIDGES = []
MOVES = []

possible_moves =  generate_all_non_illegal_moves(ISLANDS,BRIDGES)


#for game rendering
WINDOW_WIDTH, WINDOW_HEIGHT = 650, 650

CELL_SIZE = (WINDOW_WIDTH*.75) / (BOARD_SIZE-1)

PADDING = WINDOW_HEIGHT*.125

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0,0,255)



# Create the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if len(generate_all_non_illegal_moves(ISLANDS,BRIDGES)) == 0:
                    print("No possible moves game is over")
                    if Evaluate_Board(BRIDGES)>0:
                        print("RED WON")
                    else:
                        print("BLUE WON")

                elif whoseTurn == 1:
                    #human turn
                    print_possible_moves(generate_all_non_illegal_moves(ISLANDS,BRIDGES))
                    move = get_player_move(ISLANDS,BRIDGES)
                    newIsles,newBridges,newTurn = MakeMove(move, ISLANDS,BRIDGES,whoseTurn)
                    ISLANDS = newIsles  
                    BRIDGES = newBridges
                    whoseTurn = newTurn
                  #  fromStateToBoard(ISLANDS,BRIDGES,BOARD_SIZE)

                    printBoard(ISLANDS,BRIDGES,BOARD_SIZE)

                else:
                   
                    if len(generate_all_non_illegal_moves(ISLANDS,BRIDGES)) == 0:
                        print("No possible moves")
                    else:
                        move = ChooseBestCurrentMoveWithMinimax(ISLANDS,BRIDGES,whoseTurn)
                        print()
                        print("Move type:" + str(move.move_type))
                        if move.move_type == MoveType.LABEL_ISLAND:
                            print("Label Island: ", move.labeled_island.x, move.labeled_island.y, move.label)
                        else:
                            print("Place Bridge: ", move.island1.x, move.island1.y, move.island2.x, move.island2.y)
                        print()
                        newIsles, newBridges,newTurn = MakeMove(move, ISLANDS, BRIDGES,whoseTurn)
                        ISLANDS = newIsles  
                        BRIDGES = newBridges
                        whoseTurn = newTurn
                     #   fromStateToBoard(ISLANDS,BRIDGES,BOARD_SIZE)
                        printBoard(ISLANDS,BRIDGES,BOARD_SIZE)
        




    

    window.fill((0, 0, 0))  # Clear the window
    draw_grid()  # Draw the grid
    draw_bridges(BRIDGES)
    draw_islands(ISLANDS)
    draw_score(Evaluate_Board(BRIDGES))
    pygame.display.flip()  # Update the display

pygame.quit()
 
