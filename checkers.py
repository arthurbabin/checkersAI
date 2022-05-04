import pygame
import random

# COLORS
BORDER_COLOR    = (90,36,36)
BG_COLOR        = (181, 87, 84) 
BG_COLOR2  = (90,36,36)
PRIMARY_COLOR = (19,18,18)
SECONDARY_COLOR = (210,210,210)
END_COLOR       = (255,  0,  0)
EXPLORED_COLOR  = (0, 97, 0)
TBEXPLORED_COLOR = (0,  151,  0)
START_COLOR     = (255,255,255)
PATH_COLOR      = (0, 130, 255)

### VARIABLES #############

size_grid = (8,8) #(horizontally>1,vertically>1)
size_cell = (100,100) #in pixels
margin = 0 #in pixels
width, height = size_cell
grid=[[]]*5
done,ready,pathFound,finished = [False]*4

### FUNCTIONS #############
def changeNatureOfCell(c,r,newNature):
    try:
        if grid[r][c]>=0:
            grid[r][c] = newNature #don't modify the START and the END
    except:
        pass

def getCellFromCoordinates(x_c, y_c):
    return (x_c // (width + margin), y_c // (height + margin))

def mouseModification(x_c,y_c,board,indications):
    c,r=getCellFromCoordinates(x_c,y_c)
    if (c+r)%2 and str(board[r][c//2]).lower()=='w':
        moves = getPossibleMoves(r,c//2,board)
        indications = initIndications()
        for m in moves:
            indications[m["destination"][0]][m["destination"][1]]=1
    return indications 

def initPathFindingVariables():
    grid = [[0 for x in range(size_grid[0])] for y in range(size_grid[1])] #grid of cells
    return grid

def handleEvent(e,board):
    global ready
    global done
    global indications
    if event.type == pygame.QUIT:            
        done = True
    elif not ready:
        if event.type == pygame.KEYDOWN:
            if event.key ==pygame.K_SPACE:
                ready = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            indications = mouseModification(x,y,board,indications)

def updateGrid(board,indications):
    global screen, grid, size
    screen.fill(BORDER_COLOR)
    l = width/2
    for row in range(size_grid[1]):        
        for column in range(size_grid[0]):
            if (row+column)%2:
                bgcolor = BG_COLOR2
            else:                
                bgcolor = BG_COLOR
            cellX = margin + (margin + width) * column
            cellY = margin + (margin + height) * row
            pygame.draw.rect(screen, bgcolor, [cellX, cellY, width, height])
            if (row+column)%2:
                pieceType = board[row][column//2]
                centerCell = [cellX+l,cellY+l]
                if pieceType in ['b','B']:
                    pygame.draw.circle(screen,PRIMARY_COLOR,centerCell,l*0.8)
                elif pieceType in ['w','W']:
                    pygame.draw.circle(screen,SECONDARY_COLOR,centerCell,l*0.8)
                if pieceType in ['B','W']:
                    screen.blit(crownLetter,crownLetter.get_rect(center=centerCell))
                if indications[row][column//2]:
                    pygame.draw.circle(screen,SECONDARY_COLOR,centerCell,l*0.2)

                
            

def saveScreenshot(name):
    pygame.image.save(screen,f"screenshots/{name}.jpg")

def initBoard():
    return [['b','b','b','b'],
            ['b','b','b','b'],
            [1,1,1,'b'],
            [1,'b','b','b'],
            [1,1,'w','w'],
            ['w','w',1,'w'],
            ['w','w','w','w'],
            ['w','w',1,'w']]

def initIndications():
    return [[0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,0]]


def boardFEN(board):
    """Returns the Notation of Forsyth-Edwards"""
    res = []
    columnsNb = len(board[0])
    for i in range(len(board)):
        emptyCells = 0
        line = ""
        j = 0
        while(j<columnsNb):
            if board[i][j]==1:
                emptyCells+=1
            else:
                if emptyCells!=0:
                    line+=str(emptyCells)
                    emptyCells=0
                line+=str(board[i][j])
            j+=1
        if emptyCells!=0:
            line+=str(emptyCells)
        res.append(line)
    res.reverse()
    return "/".join(res)

def isAValidCell(line,column,minimum=(0,0),maximum=(7,3)):
    """Returns if the selected coordinates corresponds to a Cell on the board"""
    isValidLine = (line<=maximum[0]) and (line >=minimum[0])
    isValidColumn = (column<=maximum[1]) and (column>=minimum[1])
    return isValidLine and isValidColumn

def getNeighboursOfCell(line,column,board,isCrowned=False):
    """Returns the list of the neighbours of the selected cell"""

    positionsOfNeighbours = []
    positionsOfValidNeighbours = []

    #List all neighbours even if they are not on the board
    if isCrowned:
        #Go all over the diagonals
        for l in range(line-1,-1):
            shift = line - l
            positionsOfNeighbours.append((l,column-shift))
            positionsOfNeighbours.append((l,column+shift))
        for l in range(line+1,8):
            shift = line - l
            positionsOfNeighbours.append((l,column-shift))
            positionsOfNeighbours.append((l,column+shift))
    else:
        oType = board[line][column]
        dY = 1 if not line%2 else -1
        for i in [-1,1]:
            for j in [0,dY]:
                if isAValidCell(line+i,column+j):
                    nType = board[line+i][column+j]
                    if str(nType).isalpha() and nType != oType:
                        positionsOfNeighbours.append((line+2*i,column-1))
                    positionsOfNeighbours.append((line+i,column+j))


    #Keep only those that are on the board
    for p in positionsOfNeighbours:
        if isAValidCell(p[0],p[1]):
            positionsOfValidNeighbours.append(p)
    print(positionsOfValidNeighbours)
    return positionsOfValidNeighbours

def getMiddleCells(origin,destination):
    """Returns a list cells between origin and destination (empty if they are
    not on the same diagonal)"""
    middleCells = []
    deltaX = destination[0] - origin[0]
    deltaY = destination[1] - origin[1]
    dX = 1 if deltaX>0 else -1
    dY = 1 if deltaY>=0 else -1

    x = origin[0]+dX
    y = origin[1]
    if (dY<0 and not (x%2)) or (dY>0 and x%2):
        y+=dY
    while(x!=destination[0] and y!=destination[1]):
        middleCells.append([x,y])
        x+=dX
        if (dY<0 and not (x%2)) or (dY>0 and x%2):
            y+=dY
    return middleCells

def getRecapOfMove(origin,destination,board,isCrowned=False,hasEaten=False):
    """Returns a dictionary
    {'possible' -> if the move is possible,
    'eatenCells' -> list of eated cells,
    'destination' -> destination,
    'newBoard' -> updated board with move ([] if not possible),
    'origin' -> origin}
    """
    recap = {
            'possible':False,
            'eatenCells':[],
            'destination':destination,
            'newBoard':[],
            'origin':origin
            }
    #if the cell is occupied
    if board[destination[0]][destination[1]]!=1:
            return recap
    
    #Filter middleCells t
    middleCells = getMiddleCells(origin,destination)
    eatenCells = []
    oType = board[origin[0]][origin[1]].lower() 
    for c in middleCells:
        cType = board[c[0]][c[1]].lower()
        if cType==oType:
            return recap
        elif cType!=1:
            eatenCells.append(c)
    if hasEaten and eatenCells==[]:
        return recap
    newBoard = []
    for i in range(len(board)):
        newBoard.append(board[i][:])
    
    #Empty eaten cells
    for c in eatenCells:
        newBoard[c[0]][c[1]]=1

    #Move piece
    newBoard[destination[0]][destination[1]]=board[origin[0]][origin[1]]
    newBoard[origin[0]][origin[1]]=1

    recap["possible"]=True
    recap["eatenCells"]=eatenCells
    recap["newBoard"]=newBoard
    return recap
                
def getPossibleMoves(line,column,board,hasEaten=False):
    """Returns possible moves of a selected piece as a list of dictionaries"""
    isCrowned = board[line][column].isupper()
    newPositions = getNeighboursOfCell(line,column,board,isCrowned=isCrowned)
    moves = []
    for p in newPositions:
        recapOfMove = getRecapOfMove([line,column],p,board,isCrowned,hasEaten)
        if recapOfMove["possible"]:
            moves.append(recapOfMove)
            if recapOfMove["eatenCells"]:
                destination = recapOfMove["destination"]
                newBoard = recapOfMove["newBoard"]
                moves+=getPossibleMoves(
                        destination[0],
                        destination[1],
                        newBoard,
                        hasEaten=True
                        )
    return moves

print(getNeighboursOfCell(2,3,initBoard()))
print(getPossibleMoves(2,3,initBoard()))

#def showPossibleMoves(line,column,board,hasEated=False):
#    """Display on the board what are the possible moves"""

### MAIN ##################
pygame.init()
size = (size_grid[0]*(width+margin)+margin,size_grid[1]*(height+margin)+margin + height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Checkers AI")
pygame.font.init()
font = pygame.font.SysFont('dejavusans', 25)
fontCrownLetter = pygame.font.SysFont('dejavusans', 40)
crownLetter = fontCrownLetter.render("♔", False, BG_COLOR)				    

grid = initPathFindingVariables()
board = initBoard()
indications = initIndications()
clock = pygame.time.Clock()
i=0
while not done:

    ### Main event loop
    for event in pygame.event.get():        
        handleEvent(event,board)
    x,y = pygame.mouse.get_pos()

    ###  Draw the steps
    updateGrid(board,indications)
    tutoSurface = font.render(boardFEN(board), False, SECONDARY_COLOR)				    
    screen.blit(tutoSurface,tutoSurface.get_rect(center=(size[0]/2,size_grid[1]*(height+margin)+height/2)))
    pygame.display.flip()   
    clock.tick(60)

pygame.quit()
