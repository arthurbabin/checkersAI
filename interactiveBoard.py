import pygame
from simpleBoard import *
from minimax import *

class InteractiveBoard:
    #Lengths and sizes
    size_board_displayed = (10,10)
    widthCell,heightCell = (100,100)
    margin = 0
    size_screen = (
            size_board_displayed[0]*(widthCell+margin)+margin,
            size_board_displayed[1]*(heightCell+margin)+margin+heightCell
            )
    notationCenter = (
            size_screen[0]/2,
            size_board_displayed[1]*(heightCell+margin)+heightCell/2
            )

    #Colors
    BORDER_COLOR    = (90,36,36)
    BG_COLOR        = (181, 87, 84) 
    BG_COLOR2  = (90,36,36)
    PRIMARY_COLOR = (19,18,18)
    SECONDARY_COLOR = (210,210,210)

    #Text Variables
    caption = "Checkers AI by Arthur Babin"
    fontStr = "dejavusans"
    fontSize = 25
    CrownChar = "♔"
    CrownSize = 40
    pygame.font.init()
    font = pygame.font.SysFont(fontStr,fontSize)
    fontCrownLetter = pygame.font.SysFont(fontStr,CrownSize)
    crownLetter = fontCrownLetter.render(
            CrownChar,
            False,
            BG_COLOR
            )

    def __init__(self):
        pygame.init()
        self.possibleMoves = []
        self.possibleDestinations=[]
        self.selectedPiece = None
        self.isPlaying = -1
        self.done = False
        self.board = SimpleBoard()
        self.screen = pygame.display.set_mode(self.size_screen)
        pygame.display.set_caption(self.caption)

    def getCellFromCoordinates(self,x,y):
        """Returns the coordinates of the cell coresponding to the selected
        point on the screen"""
        yCell = x//(self.widthCell+self.margin)
        xCell = y//(self.heightCell+self.margin)
        return (xCell,yCell)

    def mouseClickEvent(self,x,y):
        """Handle mouse click event"""
        xCell,yCell=self.getCellFromCoordinates(x,y)
        #If the user is playing and the cell can house a piece
        if not self.done and self.isPlaying and (xCell+yCell)%2:
            cellType = self.board.getTypeOfCell(xCell,yCell)

            #Select the piece housed by the cell
            if cellType==1:
                self.possibleMoves = []
                moves = self.board.getAllPossibleMoves((xCell,yCell))
                self.possibleDestinations=[]
                self.possibleMoves=[]
                for m in moves:
                    mdest = m["destination"]
                    self.possibleDestinations.append(mdest)
                    self.possibleMoves.append(m)
                self.selectedPiece = (xCell,yCell)

            #Checks if the selected cell is a possible move for the
            #selected piece
            elif cellType==0:
                n = len(self.possibleDestinations)
                i = 0

                while self.selectedPiece and i<n:
                    if (xCell,yCell)==self.possibleDestinations[i]:
                        newBoard = self.possibleMoves[i]["newBoard"] 
                        self.board = newBoard 
                        self.selectedPiece = None
                        self.possibleMoves = []
                        self.possibleDestinations = []
                        self.isPlaying = False
                        self.board.updateWinner()
                        return
                    i+=1

    def update(self):
        """Update the board on the screen"""
        self.screen.fill(self.BORDER_COLOR)
        l = self.widthCell/2

        #Draw Board
        for row in range(self.size_board_displayed[1]):        
            for column in range(self.size_board_displayed[0]):
                #Draw Cell Background
                if (row+column)%2:
                    bgcolor = self.BG_COLOR2
                else:                
                    bgcolor = self.BG_COLOR
                cellX = self.margin + (self.margin + self.widthCell) * column
                cellY = self.margin + (self.margin + self.heightCell) * row
                pygame.draw.rect(
                        self.screen, 
                        bgcolor, 
                        [cellX, cellY, self.widthCell, self.heightCell]
                        )

                #Draw Cell Content
                if (row+column)%2:
                    pieceType = self.board.getTypeOfCell(row,column)
                    centerCell = [cellX+l,cellY+l]
                    isCrowned = self.board.isCrownedPiece(row,column)
                    if pieceType==-1:
                        pygame.draw.circle(
                                self.screen,
                                self.PRIMARY_COLOR,
                                centerCell,
                                l*0.8
                                )
                    elif pieceType==1:
                        pygame.draw.circle(
                                self.screen,
                                self.SECONDARY_COLOR,
                                centerCell,
                                l*0.8
                                )
                    if isCrowned:
                        self.screen.blit(
                                self.crownLetter,
                                self.crownLetter.get_rect(center=centerCell)
                                )
                    if (row,column) in self.possibleDestinations:
                        pygame.draw.circle(
                                self.screen,
                                self.SECONDARY_COLOR,
                                centerCell,
                                l*0.2
                                )

        #Display notation text at the bottom
        if self.board.winner:
            #Display winning text
            notationSurface = self.font.render(
                    f"{self.board.winner} pieces won !",
                    False, 
                    self.SECONDARY_COLOR)				    
        else:
            #Display FEN notation
            notationSurface = self.font.render(
                    self.board.F_E_Notation(),
                    False, 
                    self.SECONDARY_COLOR)				    

        self.screen.blit(
                notationSurface,
                notationSurface.get_rect(center=self.notationCenter))


    def handleEvent(self,e):
        """Event Handler for the InteractiveBoard"""
        if e.type == pygame.QUIT:            
            self.done = True
        elif self.isPlaying:
            if e.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.mouseClickEvent(pos[0],pos[1])

if __name__ == "__main__":
    pygame.init()

    iboard = InteractiveBoard()
    clock = pygame.time.Clock()
    while not iboard.done:
        for event in pygame.event.get():
            iboard.handleEvent(event)

        iboard.update()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
