import sys, random, pygame
from menublock import menuBlock
from player import playerSprite
from glob import glob

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
GRAY_FADE = (128, 128, 128, 10)
SeeThrough = (0,0,0,0)

#game-booleans
gamePaused = False
gameJustUnPaused = True
playerMoved = False

#player related
player = playerSprite
glob1 = glob
thrusterRectX = pygame.Rect
thrusterRectY = pygame.Rect
thrusterRectWidth = 0
thrusterRectHeight = 0
dt = 0
blobRadius = 35
##Level One Instructions
gameL1Instructions = ["Welcome to "]

#blocks
miniGameOne_Paused_Block = pygame.Rect
miniGameOne_Paused_ResumeBlock = pygame.Rect
miniGameOne_Paused_OptionsBlock = pygame.Rect
miniGameOne_Paused_LeaveBlock = pygame.Rect
miniGameOne_Paused_HelpBlock = pygame.Rect

def graphicsPreparation(screenWidth, screenHeight):
    global scrW, scrH
    global miniGameOne_Paused_Block, miniGameOne_Paused_ResumeBlock, miniGameOne_Paused_OptionsBlock, miniGameOne_Paused_LeaveBlock, miniGameOne_Paused_HelpBlock
    global blobRadius, player, glob1
    global ORANGE, GREEN, RED, TURQUOISE, GRAY

    scrW = screenWidth
    scrH = screenHeight

    #gameLevelOne
    ##PlayerSprite
    pThrust = scrW / 7.5
    t_max_scrW = 9
    kD = pThrust * (t_max_scrW)**2 / (scrW)**2
    player = playerSprite(int(scrW/2), int(scrH/2), blobRadius, ORANGE, pThrust, kD)
    glob1 = glob(int(blobRadius/2.5), scrW, scrH)

    ##GameBlocksG
    ###gamePauseLayOver
    miniGameOne_Paused_Block = menuBlock(int(scrW*43/100-scrH*4/100), int(scrH*35/100), int(scrW*14/100+scrH*8/100), int(scrH*30/100), "", 0, GRAY, False)
    miniGameOne_Paused_ResumeBlock = menuBlock(int(scrW*43/100), int(scrH*39/100), int(scrW*14/100), int(scrH*6/100), "RESUME", 90, GREEN, True)
    miniGameOne_Paused_OptionsBlock = menuBlock(int(scrW*43/100), int(scrH*47/100), int(scrW*14/100), int(scrH*6/100), "OPTIONS", 90, TURQUOISE, True)
    miniGameOne_Paused_HelpBlock = menuBlock
    miniGameOne_Paused_LeaveBlock = menuBlock(int(scrW*43/100), int(scrH*55/100), int(scrW*14/100), int(scrH*6/100), "LEAVE", 90, RED, True)

def stateEventHandler(state):
    global xMouse, yMouse

    for event in pygame.event.get():
        if(event.type == pygame.MOUSEBUTTONUP):
            xMouse, yMouse = event.pos
            checkMouseClick(xMouse, yMouse, state)
        elif(event.type == pygame.KEYDOWN):
            checkKeyPress(event)
        elif(event.type == pygame.KEYUP):
            checkKeyRelease(event, state)

    

def drawState(window, time):
    global miniGameOne_Paused_Block, miniGameOne_Paused_ResumeBlock, miniGameOne_Paused_OptionsBlock, miniGameOne_Paused_LeaveBlock, miniGameOne_Paused_HelpBlock
    global gamePaused, player, playerMoved, dt, glob1, playerJustUnPaused
    global scrH, scrW

    dt = time

    #coveringup pause screen when it's just unpaused.
    if(gameJustUnPaused == True):
        gameJustUnpaused = False
        window.fill(BLACK)

    #player drawing
    player.drawPlayerSurface()
    window.blit(player.playerShadow, (player.pShadowX, player.pShadowY))
    window.blit(player.playerSurface, (player.pSurfaceX, player.pSurfaceY))

    #glob drawing
    pygame.draw.circle(window, glob1.COLOUR, (glob1.x, glob1.y), glob1.R, 0)

    
    
    #gamepaused screen
    if(gamePaused == True):
        pygame.draw.rect(window, miniGameOne_Paused_Block.COLOUR, miniGameOne_Paused_Block.block())

        pygame.draw.rect(window, miniGameOne_Paused_ResumeBlock.COLOUR, miniGameOne_Paused_ResumeBlock.block())
        window.blit(miniGameOne_Paused_ResumeBlock.textShow(0), miniGameOne_Paused_ResumeBlock.textShow(1))

        pygame.draw.rect(window, miniGameOne_Paused_OptionsBlock.COLOUR, miniGameOne_Paused_OptionsBlock.block())
        window.blit(miniGameOne_Paused_OptionsBlock.textShow(0), miniGameOne_Paused_OptionsBlock.textShow(1))

        pygame.draw.rect(window, miniGameOne_Paused_LeaveBlock.COLOUR, miniGameOne_Paused_LeaveBlock.block())
        window.blit(miniGameOne_Paused_LeaveBlock.textShow(0), miniGameOne_Paused_LeaveBlock.textShow(1))
    

    if(gamePaused == False):
        if(playerMoved == True):
            player.velocity(dt)
            player.playerMove(dt, scrH, scrW)

def checkMouseClick(x, y, state):
    global miniGameOne_Paused_ResumeBlock, miniGameOne_Paused_OptionsBlock, miniGameOne_Paused_LeaveBlock, miniGameOne_Paused_HelpBlock
    global gamePaused, gameJustUnPaused
    
    #Check exit button.
    if(miniGameOne_Paused_LeaveBlock.block().collidepoint(x,y) == True):
        #For now it's exit application, later this is just back to main menu.

        
        clickConfirmed = True
        
        state.FPS = 15
        state.state = 0

        #Check other buttons?
    elif(miniGameOne_Paused_ResumeBlock.block().collidepoint(x,y) == True):
        #Start game!
        pauseGame(False, state)
        clickConfirmed = True
    elif(miniGameOne_Paused_OptionsBlock.block().collidepoint(x, y) == True):
        #Open options.
        clickConfirmed = True
        
    #elif(miniGameOne_Paused_HelpBlock.block().collidepoint(x, y) == True):
        #Opn help.
        #clickConfirmed = True
    

def checkKeyPress(keyPressedIn):
    global player, playerMoved, gamePaused, gameJustUnPaused

    keyPressed = pygame.key.get_pressed()
    #game movement
    if(gamePaused == False): 
        if(keyPressed[pygame.K_DOWN]):
            player.dT = True
            playerMoved = True
        if(keyPressed[pygame.K_UP]):
            player.uT = True
            playerMoved = True
        if(keyPressed[pygame.K_RIGHT]):
            player.rT = True
            playerMoved = True
        if(keyPressed[pygame.K_LEFT]):
            player.lT = True
            playerMoved = True

def checkKeyRelease(event, state):
    global gamePaused, player, playerMoved

    keyRegistered = False

    if(gamePaused == False and keyRegistered == False):
        if(event.key == pygame.K_ESCAPE and keyRegistered == False):
            pauseGame(True, state)
            keyRegisterd = True
        if(event.key == pygame.K_DOWN and keyRegistered == False):
            player.dT = False
        if(event.key == pygame.K_UP and keyRegistered == False):
            player.uT = False
        if(event.key == pygame.K_RIGHT and keyRegistered == False):
            player.rT = False
        if(event.key == pygame.K_LEFT and keyRegistered == False):
            player.lT = False
        if(player.dT == False and player.uT == False and player.rT == False and player.lT == False):
            if(player.v_x == 0 and player.v_y ==0):
                playerMoved = False
        #Other game functions with the keys???
    elif(gamePaused == True and keyRegistered == False):
        if(event.key == pygame.K_ESCAPE and keyRegistered == False):
            pauseGame(False, state)
            keyRegisterd = True
        #Other game functions with the keys???

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


    