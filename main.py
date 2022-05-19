import pygame
from interactiveBoard import *
pygame.init()

iboard = InteractiveBoard()
clock = pygame.time.Clock()
moveSound = pygame.mixer.Sound("Sounds/move.wav")
screenshotCount = 0
while not iboard.done:

    #Devolves events to the interactiveBoard
    for event in pygame.event.get():
        iboard.handleEvent(event)

    #Updates the display
    iboard.update()
    pygame.display.flip()

    #Checks if we need to call minimax to play against the player
    if not iboard.isPlaying:
        pygame.mixer.Sound.play(moveSound)
        time.sleep(0.5)
        iboard.isPlaying = True
        iboard.board = minimax(iboard.board,-1)[0]
        pygame.mixer.Sound.play(moveSound)


#    if screenshotCount%10 and iboard.possibleMoves:
#        screenshotName = f"screenshots/screenshot{screenshotCount}.png"
#        pygame.image.save(iboard.screen,screenshotName)
#        screenshotCount+=1
#    screenshotCount+=1

    clock.tick(60)

pygame.quit()
