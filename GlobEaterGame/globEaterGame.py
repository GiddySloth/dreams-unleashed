import sys, random, pygame
from menublock import menuBlock
from player import playerSprite
from glob import glob
import gameBar

#screen stuff
scrW = 1920
scrH = 1080

#colours
BLACK = (0,0,0,255)
WHITE = (255, 255, 255, 255)
ORANGE = (245, 150, 65, 255)
GREEN = (0, 255, 0, 255)
TURQUOISE = (65, 245, 230, 255)
RED = (255, 0, 0, 255)
GRAY = (128, 128, 128, 255)
GRAY_FADE = (128, 128, 128, 120)
SeeThrough = (0,0,0,0)

#game-booleans
gamePaused = False
gameJustUnPaused = True
playerMoved = False

#player related
player = playerSprite
globs = []
globAmount = 20
thrusterRectX = pygame.Rect
thrusterRectY = pygame.Rect
thrusterRectWidth = 0
thrusterRectHeight = 0
dt = 0
blobRadius = 35
##Level One Instructions
gameL1Instructions = ["Welcome to "]

#surface
gameBarH = 0
miniGameOne_Surface = pygame.Surface((0,0))
miniGameOne_Surface_Pos = (0,0)

#blocks
miniGameOne_Paused_BlockSurface = pygame.Surface((0,0))
miniGameOne_Paused_BlockSurfacePos = (0,0)
miniGameOne_Paused_ResumeBlock = pygame.Rect
miniGameOne_Paused_OptionsBlock = pygame.Rect
miniGameOne_Paused_LeaveBlock = pygame.Rect
miniGameOne_Paused_HelpBlock = pygame.Rect

#game-bar


def graphicsPreparation(screenWidth, screenHeight, gameBarHeight, gameHeight):
    global scrW, scrH, miniGameOne_Surface_Pos, gameBarH
    global miniGameOne_Surface, miniGameOne_Paused_BlockSurface, miniGameOne_Paused_BlockSurfacePos, miniGameOne_Paused_ResumeBlock, miniGameOne_Paused_OptionsBlock, miniGameOne_Paused_LeaveBlock, miniGameOne_Paused_HelpBlock
    global blobRadius, player, globs, globAmount
    global ORANGE, GREEN, RED, TURQUOISE, GRAY, GRAY_FADE

    scrW = screenWidth
    scrH = screenHeight
    gameBarH = gameBarHeight

    miniGameOne_Surface_Pos = (0, gameBarHeight)
    miniGameOne_Surface = pygame.Surface((scrW,gameHeight))

    #gameLevelOne
    ##PlayerSprite
    blobRadius = scrH/40
    pThrust = scrW / 7.5
    t_max_scrW = 9
    kD = pThrust * (t_max_scrW)**2 / (scrW)**2
    player = playerSprite(int(scrW/2), int((scrH-gameBarH)/2), blobRadius, ORANGE, pThrust, kD)
    
    #create globs and obstacles
    setLevel()

    ##GameBlocksG
    ###gamePauseLayOver
    miniGameOne_Paused_BlockSurfacePos = (int(scrW*43/100-scrH*4/100), int(scrH*35/100))
    miniGameOne_Paused_BlockSurfaceDim = (int(scrW*14/100+scrH*8/100), int(scrH*30/100))
    miniGameOne_Paused_BlockSurface = pygame.Surface(miniGameOne_Paused_BlockSurfaceDim).convert_alpha()
    miniGameOne_Paused_BlockSurface.fill(GRAY_FADE)
    miniGameOne_Paused_ResumeBlock = menuBlock(int(scrH*4/100), int(scrH*4/100), int(scrW*14/100), int(scrH*6/100), "RESUME", 90, GREEN, True)
    miniGameOne_Paused_OptionsBlock = menuBlock(int(scrH*4/100), int(scrH*12/100), int(scrW*14/100), int(scrH*6/100), "OPTIONS", 90, TURQUOISE, True)
    miniGameOne_Paused_HelpBlock = menuBlock
    miniGameOne_Paused_LeaveBlock = menuBlock(int(scrH*4/100), int(scrH*20/100), int(scrW*14/100), int(scrH*6/100), "LEAVE", 90, RED, True)

def stateEventHandler(state):
    global xMouse, yMouse

    for event in pygame.event.get():
        if(event.type == pygame.MOUSEBUTTONUP):
            xMouse, yMouse = event.pos
            checkMouseClick(xMouse, yMouse, state)
        if(event.type == pygame.KEYDOWN):
            checkKeyPress(event)
        if(event.type == pygame.KEYUP):
            checkKeyRelease(event, state)   

def drawState(window, time, state):
    global miniGameOne_Surface, miniGameOne_Surface_Pos, miniGameOne_Paused_Block, miniGameOne_Paused_ResumeBlock, miniGameOne_Paused_OptionsBlock, miniGameOne_Paused_LeaveBlock, miniGameOne_Paused_HelpBlock
    global gamePaused, player, playerMoved, dt, globs, playerJustUnPaused
    global scrH, scrW, gameBarH

    dt = time

    #coveringup pause screen when it's just unpaused.
    if(gameJustUnPaused == True):
        gameJustUnpaused = False
        window.fill(BLACK)
        gameBar.drawState(window, state)
        window.blit(miniGameOne_Surface, miniGameOne_Surface_Pos) 
        
    #player drawing
    player.posPlayerSurface(gameBarH)
    miniGameOne_Surface.blit(player.playerShadow, (player.pShadowX, player.pShadowY))
    miniGameOne_Surface.blit(player.getPlayerSurface(), (player.pSurfaceX, player.pSurfaceY))
    
    
    #player.posPlayerSurface(0)
    #window.blit(player.playerShadow, (player.pShadowX, player.pShadowY))
    #window.blit(player.getPlayerSurface(), (player.pSurfaceX, player.pSurfaceY))

    #glob drawing
    for i in range(len(globs)):
        pygame.draw.circle(miniGameOne_Surface, globs[i].COLOUR, (globs[i].x, globs[i].y), globs[i].R, 0)
    
    miniGameOne_Surface.convert()

    #gamepaused screen
    if(gamePaused == True):  

        pygame.draw.rect(miniGameOne_Paused_BlockSurface, miniGameOne_Paused_ResumeBlock.COLOUR, miniGameOne_Paused_ResumeBlock.block())
        miniGameOne_Paused_BlockSurface.blit(miniGameOne_Paused_ResumeBlock.textShow(0), miniGameOne_Paused_ResumeBlock.textShow(1))

        pygame.draw.rect(miniGameOne_Paused_BlockSurface, miniGameOne_Paused_OptionsBlock.COLOUR, miniGameOne_Paused_OptionsBlock.block())
        miniGameOne_Paused_BlockSurface.blit(miniGameOne_Paused_OptionsBlock.textShow(0), miniGameOne_Paused_OptionsBlock.textShow(1))

        pygame.draw.rect(miniGameOne_Paused_BlockSurface, miniGameOne_Paused_LeaveBlock.COLOUR, miniGameOne_Paused_LeaveBlock.block())
        miniGameOne_Paused_BlockSurface.blit(miniGameOne_Paused_LeaveBlock.textShow(0), miniGameOne_Paused_LeaveBlock.textShow(1))
    
        window.blit(miniGameOne_Paused_BlockSurface, miniGameOne_Paused_BlockSurfacePos)

    if(gamePaused == False):
        if(playerMoved == True):
            player.velocity(dt)
            player.playerMove(dt, scrH, scrW, gameBarH)

            toRemoveList = []

            for j in range(len(globs)):
                if(checkGlobCollision(globs[j]) == True):
                    toRemoveList.append(j)

            for n in range(len(toRemoveList)):
                scoreHandling(state, "globEaten")
                globs.pop(toRemoveList[n])
            
            if(len(globs) == 0):
                setLevel()
            

def checkMouseClick(x, y, state):
    global miniGameOne_Paused_BlockSurfacePos, miniGameOne_Paused_ResumeBlock, miniGameOne_Paused_OptionsBlock, miniGameOne_Paused_LeaveBlock, miniGameOne_Paused_HelpBlock
    global gamePaused, gameJustUnPaused
    
    pauseX = x-miniGameOne_Paused_BlockSurfacePos[0]
    pauseY = y-miniGameOne_Paused_BlockSurfacePos[1]

    #Check exit button.
    if(miniGameOne_Paused_LeaveBlock.block().collidepoint(pauseX, pauseY) == True):
        #For now it's exit application, later this is just back to main menu.
        clickConfirmed = True
        
        state.FPS = 15
        state.state = 0
        state.gameHasBeenPausedMenu = True

        #Check other buttons?
    elif(miniGameOne_Paused_ResumeBlock.block().collidepoint(pauseX, pauseY) == True):
        #Resume game.
        pauseGame(False, state)
        clickConfirmed = True
    elif(miniGameOne_Paused_OptionsBlock.block().collidepoint(pauseX, pauseY) == True):
        #Open options.
        clickConfirmed = True
        pass
    #elif(miniGameOne_Paused_HelpBlock.block().collidepoint(x, y) == True):
        #Opn help.
        #clickConfirmed = True
    

def checkKeyPress(event):
    global player, playerMoved, gamePaused, gameJustUnPaused

    keysChecked = 0

    keyPressed = event.key
    #game movement
    if(gamePaused == False): 
        if(keyPressed == pygame.K_DOWN or keyPressed == pygame.K_s):
            player.dT = True
            playerMoved = True
            keysChecked = keysChecked +1
        if(keyPressed == pygame.K_UP or keyPressed == pygame.K_w):
            player.uT = True
            playerMoved = True
            keysChecked = keysChecked +1
        if(keyPressed == pygame.K_RIGHT or keyPressed == pygame.K_d):
            player.rT = True
            playerMoved = True
            keysChecked = keysChecked +1
        if(keyPressed == pygame.K_LEFT or keyPressed == pygame.K_a):
            player.lT = True
            playerMoved = True
            keysChecked = keysChecked +1
    if(keysChecked>1):
        print(str(keysChecked))

def checkKeyRelease(event, state):
    global gamePaused, player, playerMoved

    keyRegistered = False

    if(gamePaused == False and keyRegistered == False):
        if(event.key == pygame.K_ESCAPE and keyRegistered == False):
            pauseGame(True, state)
            keyRegisterd = True
        if(event.key == pygame.K_DOWN or event.key == pygame.K_s):
            player.dT = False
        if(event.key == pygame.K_UP or event.key == pygame.K_w):
            player.uT = False
        if(event.key == pygame.K_RIGHT or event.key == pygame.K_d):
            player.rT = False
        if(event.key == pygame.K_LEFT or event.key == pygame.K_a):
            player.lT = False
        if(player.dT == False and player.uT == False and player.rT == False and player.lT == False):
            if(player.v_x == 0 and player.v_y == 0):
                playerMoved = False
        #Other game functions with the keys???
    elif(gamePaused == True and keyRegistered == False):
        if(event.key == pygame.K_ESCAPE and keyRegistered == False):
            pauseGame(False, state)
            keyRegisterd = True
        #Other game functions with the keys???

def checkGlobCollision(globCol):
    global player

    globDistance = ( (player.x-globCol.x)**2 + (player.y-globCol.y)**2 )**(0.5)

    if(globDistance < (player.R*1.1) ):
        return True
    else:
        return False

def setLevel():
    global globs, globAmount, blobRadius, scrW, scrH, gameBarH

    for i in range(globAmount):
        globs.append(glob(int(blobRadius/2.8), scrW, scrH, gameBarH))

def pauseGame(pause, state):
    global gamePaused, gameJustUnPaused

    if(pause == True):
        gamePaused = True
        state.FPS = 15
        state.gameHasBeenpaused = gamePaused
    
    if(pause == False):
        gamePaused = False
        gameJustUnPaused = True
        state.gameHasBeenpaused = gamePaused
        state.FPS = 60

def scoreHandling(state, gameEvent):
    if(gameEvent == "globEaten"):
        state.score = state.score + 1
        state.gameBarChange == True

#Key recognition of developer system is still buggy. E.g. hold down arrow(down), press another key and then release that same key. down thrust will also switch off... Other key combinations are also faulty.