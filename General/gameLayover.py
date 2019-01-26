import sys, random, pygame
from menublock import menuBlock

#screen stuff
scrW = 1920
scrH = 1080

#colours
BLACK = (0,0,0,255)
WHITE = (255, 255, 255, 255)
ORANGE = (245, 150, 65, 255)
ORANGE_FADE = (245, 150, 65, 120)
GREEN = (0, 255, 0, 255)
TURQUOISE = (65, 245, 230, 255)
RED = (255, 0, 0, 255)
GRAY = (128, 128, 128, 255)
GRAY_FADE = (128, 128, 128, 120)
SeeThrough = (0,0,0,0)

#blocks
##paused
miniGameOne_Paused_BlockSurface = pygame.Surface((0,0))
miniGameOne_Paused_BlockSurfacePos = (0,0)
miniGameOne_Paused_ResumeBlock = pygame.Rect
miniGameOne_Paused_OptionsBlock = pygame.Rect
miniGameOne_Paused_LeaveBlock = pygame.Rect
miniGameOne_Paused_HelpBlock = pygame.Rect

#gameover
miniGameOne_GameOver_BlockSurface = pygame.Surface((0,0))
miniGameOne_GameOver_BlockSurfacePos = (0,0)
miniGameOne_GameOver_RestartBlock = pygame.Rect
miniGameOne_GameOver_MessageBlock = pygame.Rect
miniGameOne_GameOver_ScoreBlock = pygame.Rect
miniGameOne_GameOver_LeaveBlock = pygame.Rect

#mouse positions
xMouse = 0
yMouse = 0

def graphicsPreparation(screenWidth, screenHeight):
    global scrW, scrH, miniGameOne_Surface_Pos, gameBarH
    global miniGameOne_Surface, miniGameOne_Paused_BlockSurface, miniGameOne_Paused_BlockSurfacePos, miniGameOne_Paused_ResumeBlock, miniGameOne_Paused_OptionsBlock, miniGameOne_Paused_LeaveBlock, miniGameOne_Paused_HelpBlock
    global miniGameOne_GameOver_BlockSurface, miniGameOne_GameOver_BlockSurfacePos, miniGameOne_GameOver_RestartBlock, miniGameOne_GameOver_MessageBlock, miniGameOne_GameOver_LeaveBlock, miniGameOne_GameOver_ScoreBlock
    global ORANGE, GREEN, RED, TURQUOISE, GRAY, GRAY_FADE, ORANGE_FADE

    scrW = screenWidth
    scrH = screenHeight

    #gamePauseLayOver
    miniGameOne_Paused_BlockSurfacePos = (int(scrW*43/100-scrH*4/100), int(scrH*35/100))
    miniGameOne_Paused_BlockSurfaceDim = (int(scrW*14/100+scrH*8/100), int(scrH*30/100))
    miniGameOne_Paused_BlockSurface = pygame.Surface(miniGameOne_Paused_BlockSurfaceDim).convert_alpha()
    miniGameOne_Paused_BlockSurface.fill(GRAY_FADE)
    miniGameOne_Paused_ResumeBlock = menuBlock(int(scrH*4/100), int(scrH*4/100), int(scrW*14/100), int(scrH*6/100), "RESUME", 90, GREEN, True)
    miniGameOne_Paused_OptionsBlock = menuBlock(int(scrH*4/100), int(scrH*12/100), int(scrW*14/100), int(scrH*6/100), "OPTIONS", 90, TURQUOISE, True)
    miniGameOne_Paused_HelpBlock = menuBlock
    miniGameOne_Paused_LeaveBlock = menuBlock(int(scrH*4/100), int(scrH*20/100), int(scrW*14/100), int(scrH*6/100), "LEAVE", 90, RED, True)

    #gameOverLayOver
    miniGameOne_GameOver_BlockSurfacePos = (int(scrW*43/100-scrH*4/100), int(scrH*35/100))
    miniGameOne_GameOver_BlockSurfaceDim = (int(scrW*14/100+scrH*8/100), int(scrH*30/100))
    miniGameOne_GameOver_BlockSurface = pygame.Surface(miniGameOne_GameOver_BlockSurfaceDim).convert_alpha()
    miniGameOne_GameOver_BlockSurface.fill(GRAY_FADE)
    miniGameOne_GameOver_RestartBlock = menuBlock(int(scrH*4/100), int(scrH*2/100), int(scrW*14/100), int(scrH*6/100), "RESTART", 90, GREEN, True)
    miniGameOne_GameOver_MessageBlock = menuBlock(int(scrH*4/100), int(scrH*10/100), int(scrW*14/100), int(scrH*4/100), "GAME OVER", 90, WHITE, True)
    miniGameOne_GameOver_ScoreBlock = menuBlock(int(scrH*4/100), int(scrH*16/100), int(scrW*14/100), int(scrH*4/100), "Score: .", 90, TURQUOISE, True)
    miniGameOne_GameOver_LeaveBlock = menuBlock(int(scrH*4/100), int(scrH*22/100), int(scrW*14/100), int(scrH*6/100), "LEAVE", 90, RED, True)


def drawState(state, window):
    global miniGameOne_Paused_BlockSurface, miniGameOne_Paused_BlockSurfacePos, miniGameOne_Paused_ResumeBlock, miniGameOne_Paused_OptionsBlock, miniGameOne_Paused_LeaveBlock, miniGameOne_Paused_HelpBlock
    global miniGameOne_GameOver_BlockSurface, miniGameOne_GameOver_BlockSurfacePos, miniGameOne_GameOver_RestartBlock, miniGameOne_GameOver_MessageBlock, miniGameOne_GameOver_LeaveBlock, miniGameOne_GameOver_ScoreBlock

    if(state.gameJustDied == True):
        state.gameJustDied = False

        newScoreText = "Score: " + str(int(state.lastGameScore))
        miniGameOne_GameOver_ScoreBlock.setNewText(newScoreText)

    if(state.gameHasBeenPaused == True):
        pygame.draw.rect(miniGameOne_Paused_BlockSurface, miniGameOne_Paused_ResumeBlock.COLOUR, miniGameOne_Paused_ResumeBlock.block())
        miniGameOne_Paused_BlockSurface.blit(miniGameOne_Paused_ResumeBlock.textShow(0), miniGameOne_Paused_ResumeBlock.textShow(1))

        pygame.draw.rect(miniGameOne_Paused_BlockSurface, miniGameOne_Paused_OptionsBlock.COLOUR, miniGameOne_Paused_OptionsBlock.block())
        miniGameOne_Paused_BlockSurface.blit(miniGameOne_Paused_OptionsBlock.textShow(0), miniGameOne_Paused_OptionsBlock.textShow(1))

        pygame.draw.rect(miniGameOne_Paused_BlockSurface, miniGameOne_Paused_LeaveBlock.COLOUR, miniGameOne_Paused_LeaveBlock.block())
        miniGameOne_Paused_BlockSurface.blit(miniGameOne_Paused_LeaveBlock.textShow(0), miniGameOne_Paused_LeaveBlock.textShow(1))
    
        window.blit(miniGameOne_Paused_BlockSurface, miniGameOne_Paused_BlockSurfacePos)

    elif(state.gameOver == True):
        pygame.draw.rect(miniGameOne_GameOver_BlockSurface, miniGameOne_GameOver_RestartBlock.COLOUR, miniGameOne_GameOver_RestartBlock.block())
        miniGameOne_GameOver_BlockSurface.blit(miniGameOne_GameOver_RestartBlock.textShow(0), miniGameOne_GameOver_RestartBlock.textShow(1))

        pygame.draw.rect(miniGameOne_GameOver_BlockSurface, miniGameOne_GameOver_MessageBlock.COLOUR, miniGameOne_GameOver_MessageBlock.block())
        miniGameOne_GameOver_BlockSurface.blit(miniGameOne_GameOver_MessageBlock.textShow(0), miniGameOne_GameOver_MessageBlock.textShow(1))

        pygame.draw.rect(miniGameOne_GameOver_BlockSurface, miniGameOne_GameOver_ScoreBlock.COLOUR, miniGameOne_GameOver_ScoreBlock.block())
        miniGameOne_GameOver_BlockSurface.blit(miniGameOne_GameOver_ScoreBlock.textShow(0), miniGameOne_GameOver_ScoreBlock.textShow(1))

        pygame.draw.rect(miniGameOne_GameOver_BlockSurface, miniGameOne_GameOver_LeaveBlock.COLOUR, miniGameOne_GameOver_LeaveBlock.block())
        miniGameOne_GameOver_BlockSurface.blit(miniGameOne_GameOver_LeaveBlock.textShow(0), miniGameOne_GameOver_LeaveBlock.textShow(1))
    
        window.blit(miniGameOne_GameOver_BlockSurface, miniGameOne_GameOver_BlockSurfacePos)

def stateEventHandler(state):
    global xMouse, yMouse

    for event in pygame.event.get():
        if(event.type == pygame.MOUSEBUTTONUP):
            xMouse, yMouse = event.pos
            checkMouseClick(xMouse, yMouse, state)
        if(event.type == pygame.KEYUP):
            checkKeyRelease(event, state) 

def checkMouseClick(x, y, state):
    global miniGameOne_Paused_BlockSurfacePos, miniGameOne_Paused_ResumeBlock, miniGameOne_Paused_OptionsBlock, miniGameOne_Paused_LeaveBlock, miniGameOne_Paused_HelpBlock
    global miniGameOne_GameOver_BlockSurfacePos, miniGameOne_GameOver_RestartBlock, miniGameOne_GameOver_MessageBlock, miniGameOne_GameOver_LeaveBlock

    pauseX = x-miniGameOne_Paused_BlockSurfacePos[0]
    pauseY = y-miniGameOne_Paused_BlockSurfacePos[1]

    #Check exit button.
    if(state.gameHasBeenPaused == True):
        if(miniGameOne_Paused_LeaveBlock.block().collidepoint(pauseX, pauseY) == True):
            #For now it's exit application, later this is just back to main menu.
            state.FPS = 15
            state.state = 0
            state.gameHasBeenPausedMenu = True
            #Check other buttons?
        elif(miniGameOne_Paused_ResumeBlock.block().collidepoint(pauseX, pauseY) == True):
            #Resume game.
            pauseGame(False, state)
        elif(miniGameOne_Paused_OptionsBlock.block().collidepoint(pauseX, pauseY) == True):
            #Open options.
            pass
        #elif(miniGameOne_Paused_HelpBlock.block().collidepoint(x, y) == True):
            #Opn help.
            #clickConfirmed = True
    
    if(state.gameOver == True):
        if(miniGameOne_GameOver_LeaveBlock.block().collidepoint(pauseX, pauseY) == True):
            #For now it's exit application, later this is just back to main menu.
            state.FPS = 15
            state.state = 0
            state.gameHasBeenDead = True
            state.gameOver = False
            #Check other buttons?
        elif(miniGameOne_GameOver_RestartBlock.block().collidepoint(pauseX, pauseY) == True):
            #Resume game.
            restartGame(state)

def restartGame(state):
    state.gameOver = False
    state.score = 0
    state.playerHealth = 100
    state.gameJustRestarted = True



def pauseGame(pause, state):

    if(pause == True):
        state.FPS = 15
        state.gameHasBeenPaused = True
    
    if(pause == False):
        state.gameJustUnPaused = True
        state.gameHasBeenPaused = False
        state.FPS = 60

def checkKeyRelease(event, state):
    keyRegistered = False

    if(state.gameHasBeenPaused == True and keyRegistered == False):
        if(event.key == pygame.K_ESCAPE and keyRegistered == False):
            pauseGame(False, state)
            keyRegisterd = True
    