import pygame
import time
import numpy as np

class SimpleBoard:
    width = 10

    startingBoard = np.zeros((width,width))
    for row in range(3):
        for col in range(width):
            if (row+col)%2:
                startingBoard[row,col]=-1
    for row in range(width-3,width):
        for col in range(width):
            if (row+col)%2:
                startingBoard[row,col]=1

    winner = ""

    def __init__(self,config=startingBoard):
        self.board = np.zeros((self.width,self.width))

        #Copy the structure of config into self.board
        for row in range(self.width):
            for column in range(self.width):
                self.board[row][column]=config[row][column]

    def __getitem__(self,row):
        return self.board[row]

    def F_E_Notation(self):
        """Returns the Notation of Forsyth-Edwards"""
        res = []
        columnsNb = self.width
        for i in range(self.width):
            emptyCells = 0
            line = ""
            j = 0
            while(j<columnsNb):
                if (i+j)%2:
                    cType = self.board[i][j]
                    if cType==0:
                        emptyCells+=1
                    else:
                        if emptyCells!=0:
                            line+=str(emptyCells)
                            emptyCells=0
                        if cType==1:
                            line+="w"
                        elif cType==2:
                            line+="W"
                        elif cType==-1:
                            line+="b"
                        else:
                            line+="B"
                j+=1
            if emptyCells!=0:
                line+=str(emptyCells)
            res.append(line)
        res.reverse()
        return "/".join(res)

    def isAValidCell(self,position):
        """Returns if the selected coordinates corresponds
        to a valid Cell on the board"""
        line,column = position
        isOnBoardX = line>=0 and line<self.width 
        isOnBoardY = column >=0 and column<self.width 
        canPlacePiece = bool((line+column)%2)
        return isOnBoardX and isOnBoardY and canPlacePiece

    def getTypeOfCell(self,line,column,crownBlind=True):
        """Returns the type of the selected cell regardless or not of if it is
        a crowned piece"""
        if crownBlind:
            return np.sign(self.board[line][column])
        else:
            return self.board[line][column]

    def isAnEnnemy(self,position,comparedType):
        """Returns True if at the selected position there is a piece that has
        a different type"""
        askedType = self.getTypeOfCell(position[0],position[1])
        return askedType!=0 and askedType!=comparedType

    def isEmpty(self,position):
        """Returns if the selected position is empty"""
        return self.board[position[0]][position[1]]==0

    def getNeighboursOfCell(self,line,column,isCrowned=False,hasEaten=False):
        """Returns the list of the possible destinations of 
        the selected cell"""
        neighbours = []
        currentType = self.getTypeOfCell(line,column)

        rangePiece = [-1,1]

        #The position has 4 direct neighbours
        #(line-1,col-1)
        #(line+1,col-1)
        #(line-1,col+1)
        #(line+1,col+1)
        for i in rangePiece:
            posX = line+i
            for j in rangePiece:
                posY = column+j
                #Check if the neighbour is on the board
                if self.isAValidCell((posX,posY)):
                    #Add direct neighbours only if the piece didn't eat
                    if not hasEaten and self.isEmpty((posX,posY)):
                        neighbours.append((posX,posY))
                    #else add further neighbour if empty
                    elif self.isAnEnnemy((posX,posY),currentType):
                        if self.isAValidCell((posX-i,posY-j)):
                            if self.isEmpty((posX-i,posY-j)):
                                neighbours.append((posX-i,posY-j))

        #Filter backward moves for pieces without crown and who didn't eat
        if hasEaten or isCrowned:
            validNeighbours = neighbours
        else:
            validNeighbours = []
            for n in neighbours:
                if n[0]*currentType<currentType*line:
                    validNeighbours.append(n)

        return validNeighbours

    def onSameDiagonal(self,pos1,pos2):
        """Returns if pos1 and pos2 are on the same diagonal"""
        d1 = (pos1[0]+pos1[1])==(pos2[0]+pos2[1])
        d2 = (self.width-pos1[0]+pos1[1])==(self.width-pos2[0]+pos2[1])
        return d1 or d2

    def getEatenCells(self,origin,destination):
        """Returns a list cells between origin and destination 
        (empty if they are not on the same diagonal)"""
        eatenCells = []
        if self.onSameDiagonal(origin,destination) and origin[0]!=destination[0]:
            if origin[0]>destination[0]:
                deltaRow = 1
            else:
                deltaRow = -1
            if origin[1]>destination[1]:
                deltaCol = 1
            else:
                deltaCol = -1
            pos = (origin[0]-deltaRow,origin[1]-deltaCol)
            while(pos!=destination):
                eatenCells.append(pos)
                pos = (pos[0]-deltaRow,pos[1]-deltaCol)
        return eatenCells

    def getRecapOfMove(self,origin,destination,isCrowned=False,hasEaten=False):
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
                'newBoard':None,
                'origin':origin
                }
        #if the cell is occupied
        if self.board[destination]!=0:
            return recap

        #Filter middleCells t
        middleCells = self.getEatenCells(origin,destination)
        eatenCells = []
        oType = self.getTypeOfCell(origin[0],origin[1])
        for c in middleCells:
            cType = self.getTypeOfCell(c[0],c[1])
            if cType==oType:
                return recap
            elif not self.isEmpty(c):
                eatenCells.append(c)
        if hasEaten and eatenCells==[]:
            return recap
        newBoard = SimpleBoard(config=self.board)

        #Empty eaten cells
        for c in eatenCells:
            newBoard.board[c]=0

        #Move piece
        if destination[0]==0 and oType==1:
            newBoard.board[destination]=2
        elif destination[0]==self.width-1 and oType==-1:
            newBoard.board[destination]=-2
        else:
            newBoard.board[destination]=self.board[origin]
        newBoard.board[origin]=0

        recap["possible"]=True
        recap["eatenCells"]=eatenCells
        recap["newBoard"]=newBoard
        return recap

    def isCrownedPiece(self,line,column):
        ctype = self.board[line][column]
        return ctype==2 or ctype==-2 

    def getPossibleSurfaceMoves(self,pos,hasEaten=False):
        """Returns possible moves of a selected piece 
        as a list of dictionaries without taking into account
        the possibility of playing again"""

        line,column = pos
        isCrowned = self.isCrownedPiece(line,column)

        newPositions = self.getNeighboursOfCell(line,column,isCrowned=isCrowned,hasEaten=hasEaten)
        moves = []

        for p in newPositions:
            recap = self.getRecapOfMove(pos,p,isCrowned,hasEaten)
            if recap["possible"]:
                if not hasEaten or recap["eatenCells"]:
                    moves.append(recap)
        
        return moves

    def getAllPossibleMoves(self,pos):
        """Returns possible moves of a selected piece and takes into
        account when the player can play again because the piece eated"""

        moves = self.getPossibleSurfaceMoves(pos)

        n = len(moves)
        for i in range(n):
            if moves[i]["eatenCells"]:
                newOrigin = moves[i]["destination"]
                newBoard = moves[i]["newBoard"]
                tmpMoves = newBoard.getPossibleSurfaceMoves(
                        newOrigin,
                        hasEaten=True)
                for tmove in tmpMoves:
                    if tmove["possible"]:
                        moves.append(tmove)

        return moves 

    def score(self):
        """Returns the score of the board"""
        score = 0
        for row in range(self.width):
            for col in range(self.width):
                if self.board[row,col]==2:
                    score+=4
                elif self.board[row,col]==-2:
                    score+=-4
                else:
                    score+=self.board[row,col]
                    if col==0 or col==self.width-1:
                        score+=np.sign(self.board[row,col])*0.5
        return score

    def getAllPiecesPositions(self,pieceType=0):
        """Returns all the positions of the pieces of pieceType (or all pieces
        if pieceType==0)"""
        positions = []
        for row in range(self.width):
            for col in range(self.width):
                if not pieceType or np.sign(self.board[row,col])==pieceType:
                    positions.append((row,col))
        return positions

    def whoWins(self):
        """Returns 1 if white pieces won, -1 if black pieces won otherwise"""
        for pieceType in [-1,1]:
            #Check if there are still pieces of pieceType on the board
            positions = self.getAllPiecesPositions(pieceType)
            if not positions:
                return -pieceType

            #Check if there are still possible moves for pieceType
            moves = []
            for pos in positions:
                moves+=self.getAllPossibleMoves(pos)
            if not moves:
                return -pieceType
        return 0

    def updateWinner(self):
        """Update self.winner according to the board"""
        w = self.whoWins()
        if w == 1:
            self.winner = "White"
        elif w == -1:
            self.winner = "Black"
    
    def print(self,prefix=""):
        """Pretty prints the board on the standard output"""
        for row in range(self.width):
            print(prefix,end="")
            for col in range(self.width):
                print("|",end="")
                if (row+col)%2==0:
                    print("■", end="")
                elif self.board[row,col]==0:
                    print(" ",end="")
                elif self.board[row,col]==1:
                    print("\033[31mw\033[0m", end="")
                elif self.board[row,col]==2:
                    print("\033[31mW\033[0m", end="")
                elif self.board[row,col]==-1:
                    print("\033[36mb\033[0m", end="")
                else:
                    print("\033[36mB\033[0m", end="")
            print("|")
        print(prefix,end="")
        print(f"Score:{self.score()}")

if __name__=="__main__":
    sb = SimpleBoard()
    assert sb.F_E_Notation()=="wwwww/wwwww/wwwww/5/5/5/5/bbbbb/bbbbb/bbbbb"
    for i in range(sb.width):
        assert sb[0][i]==sb.board[0,i]
    sb.print()

    ### Accessible Cells
    print("Get Accessible Cells")
    row,col = 0,1
    print(f"Neighbours for ({row},{col}) -> {sb.getNeighboursOfCell(row,col)}")
    row,col = 2,1
    print(f"Neighbours for ({row},{col}) -> {sb.getNeighboursOfCell(row,col)}")
    row,col = 2,3
    print(f"Neighbours for ({row},{col}) -> {sb.getNeighboursOfCell(row,col)}")
    row,col = 5,4
    print(f"Neighbours for ({row},{col}) -> {sb.getNeighboursOfCell(row,col)}")
    row,col = 5,6
    print(f"Neighbours for ({row},{col}) -> {sb.getNeighboursOfCell(row,col)}")

    ### EatenCells
    print("\nGet cells between origin and destination")
    opos,ocol=0,0
    dpos,dcol=2,2
    print(f"({opos},{ocol})---{sb.getEatenCells((opos,ocol),(dpos,dcol))}---({dpos},{dcol})")
    opos,ocol=2,4
    dpos,dcol=5,7
    print(f"({opos},{ocol})---{sb.getEatenCells((opos,ocol),(dpos,dcol))}---({dpos},{dcol})")
    opos,ocol=0,6
    dpos,dcol=6,0
    print(f"({opos},{ocol})---{sb.getEatenCells((opos,ocol),(dpos,dcol))}---({dpos},{dcol})")
    opos,ocol=4,5
    dpos,dcol=2,2
    print(f"({opos},{ocol})---{sb.getEatenCells((opos,ocol),(dpos,dcol))}---({dpos},{dcol})")

    startingBoard = np.array(
            [
                [ 0,-1, 0,-1, 0, 1, 0,-1, 0, 0],
                [-1, 0,-1, 0,-1, 0, 0, 0, 1, 0],
                [ 0, 0, 0, 0, 0,-1, 0, 0, 0, 0],
                [-1, 0,-1, 0, 0, 0, 0, 0, 1, 0],
                [ 0, 0, 0, 0, 0,-1, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [ 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [ 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                [ 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
                [ 1, 0, 1, 0, 1, 0, 1, 0, 0, 0]])
    sb = SimpleBoard(startingBoard)
    sb.print()
    print(sb.getNeighboursOfCell(5,0,isCrowned=False,hasEaten=True))
    ###Possible Moves
    positions = sb.getAllPiecesPositions(1)
    for pos in positions:
        print("-"*20)
        print(sb.getNeighboursOfCell(pos[0],pos[1]))
        print(f"Pos: {pos}")
        for move in sb.getAllPossibleMoves(pos):
            if move["possible"]:
                print()
                move["newBoard"].print()
        print("-"*20)




    
