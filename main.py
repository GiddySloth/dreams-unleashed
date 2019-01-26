import sys, random, pygame, platform, ctypes
sys.path.insert(0, "./GameMenu")
sys.path.insert(0, "./General")
sys.path.insert(0, "./GlobEaterGame")

from state import State
#from mainMenu import graphicsPreparation, stateEventHandler, drawState
import gameMenu
import globEaterGame
import gameBar
import gameLayover

#State-related.
state = State

#Version
version = "0.1a5"

#Graphics-related.
window = pygame.Surface
fpsClock = pygame.time.Clock()
FPS = 15
dt = 0

BLACK = (0,0,0,255)

def main():
    global currentState, window, state, FPS

    print("DreamsUnleashed-v" + version + ".")

    initialState = 0
    state = State(initialState, FPS)

    pygame.init()
    pygame.event.set_allowed(None)
    pygame.event.set_allowed([pygame.KEYUP, pygame.KEYDOWN, pygame.MOUSEBUTTONUP])
    #

    if(platform.system() == "Windows"):
        ctypes.windll.user32.SetProcessDPIAware()

    window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

    graphicsPreparation(state)

    pygame.display.set_caption('PyGame Practice')

    soundtrack()

    mainLoop()

    

def mainLoop():
    
    global dt, fpsClock, window, state, BLACK

    loopInfinite = True

    while loopInfinite:   
        currentState = state.getState()
        
        if(currentState == "Game Menu"):
            gameMenu.stateEventHandler(state)
            gameMenu.drawState(window)
        elif(currentState == "GlobEaterGame"):  
            state.FPS = 60
            globEaterGame.stateEventHandler(state)
            globEaterGame.drawState(window, dt, state)

            if(state.gameHasBeenPaused == True or state.gameOver == True):
                gameLayover.stateEventHandler(state)
                gameLayover.drawState(state, window)
            elif(state.gameHasBeenPaused == False and state.gameOver == False):
                if(state.gameJustBeenUnPaused == True):
                    state.gameJustBeenUnPaused = False
                    window.fill(BLACK)
                elif(state.gameJustRestarted == True):
                    state.gameJustRestarted = False
                    window.fill(BLACK)
            
            if(state.gameBarChange == True):
                gameBar.drawState(window, state)
                state.gameBarChange == False
        
        pygame.display.update()
        dt = fpsClock.tick(state.FPS) / 1000
            
    


def graphicsPreparation(state):

    scrInfo = pygame.display.Info()
    scrH = scrInfo.current_h
    scrW = scrInfo.current_w

    gameBarH = int(scrH*1/12)
    gameWindowH = scrH - gameBarH

    gameMenu.graphicsPreparation(scrW, scrH)
    gameLayover.graphicsPreparation(scrW, scrH)
    gameBar.graphicsPreparation(scrW, scrH, gameBarH)
    globEaterGame.graphicsPreparation(state, scrW, scrH, gameBarH, gameWindowH)

def soundtrack():
    pygame.mixer.music.load("Soundtrack/GlobEater_Track1.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

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