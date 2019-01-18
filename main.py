import sys, random, pygame
sys.path.insert(0, "./GameMenu")
sys.path.insert(0, "./General")
sys.path.insert(0, "./GlobEaterGame")
from state import State
#from mainMenu import graphicsPreparation, stateEventHandler, drawState
import gameMenu
import globEaterGame

#State-related.
state = State

#Version
version = "0.1a2"

#Graphics-related.
window = pygame.Surface
fpsClock = pygame.time.Clock()
FPS = 15
dt = 0


def main():
    global currentState, window, state, FPS

    print("Starting EI-APP.")

    initialState = 0
    state = State(initialState, FPS)

    pygame.init()
    pygame.event.set_allowed(None)
    pygame.event.set_allowed([pygame.KEYUP, pygame.KEYDOWN, pygame.MOUSEBUTTONUP])
    #
    window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

    graphicsPreparation()

    pygame.display.set_caption('PyGame Practice')

    mainLoop()

    

def mainLoop():
    
    global dt, fpsClock, window, state

    loopInfinite = True

    


    while loopInfinite:   
        currentState = state.getState()
        
        if(currentState == "Game Menu"):
            gameMenu.stateEventHandler(state)
            gameMenu.drawState(window)
        elif(currentState == "GlobEaterGame"):
            state.FPS = 60
            globEaterGame.stateEventHandler(state)
            globEaterGame.drawState(window, dt)
        
        pygame.display.update()
        dt = fpsClock.tick(state.FPS) / 1000
            
    


def graphicsPreparation():

    scrInfo = pygame.display.Info()
    scrH = scrInfo.current_h
    scrW = scrInfo.current_w


    gameMenu.graphicsPreparation(scrW, scrH)
    globEaterGame.graphicsPreparation(scrW, scrH)

def exitFunction():
    sys.exit(0)

main()

###NOTES:
##*Design and add the main menu screen.
##*Optimize design of gameMenu.
##*Add Option functionality for game.
##*Add instructions for the game in the help section and on the gameMenu.
##*Finish creating level one for miniGameOne. Make it that the user has to eat a certain amount of blue globs or something.

#OpenGL Implementation options.
#1. Start C++ on side and implement OpenGL from get-go. Keep working on Python on the side.
#2. Implement OpenGL in conjunction with Pygame.
#3. Consider using CUDA to optimize this game first. And then see whether we do OpenGL at all?