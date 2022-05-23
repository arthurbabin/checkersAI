import simpleBoard
import numpy as np

def bestMove(board,pieceType):
    """Returns the best move when its pieceType's turn according to the
    score of the board"""
    positions = board.getAllPiecesPositions(pieceType)
    moves = []
    for pos in positions:
        moves += board.getAllPossibleMoves(pos)
    
    if len(positions)==0:
        raise IndexError(f"No more pieces of type {pieceType}")
    else:
        bestScore = pieceType*moves[0]["newBoard"].score()
        indexOfBestMove=0
        for i in range(1,len(moves)):
            score = pieceType*moves[i]["newBoard"].score()
            if score>bestScore:
                bestScore,indexOfBestMove=score,i
        return moves[indexOfBestMove]["newBoard"],pieceType*bestScore

def minimax(board,pieceType):
    """Returns the best move according to the minimax algorithm when its
    pieceType's turn"""

    positions = board.getAllPiecesPositions(pieceType)
    bestScore = - 100_000*pieceType
    bestBoard = None
    for pos in positions:
        moves = board.getAllPossibleMoves(pos)
        for move in moves:
            newBoard = move["newBoard"]
            if newBoard.whoWins()==pieceType:
                return newBoard,newBoard.score()
            resultBoard,resultScore = bestMove(newBoard,-pieceType)
            if resultScore*pieceType>bestScore*pieceType:
                bestBoard,bestScore=newBoard,resultScore
    return bestBoard,bestScore

if __name__=="__main__":
    newSb = simpleBoard.SimpleBoard()
    pieceType = 1
    for i in range(40):
        newSb.print()
        print()
        newSb=minimax(newSb,pieceType)[0]
        pieceType = pieceType*(-1)
