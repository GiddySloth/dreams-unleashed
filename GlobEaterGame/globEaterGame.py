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
GRAY_FADE = (128, 128, 128, 120)
SeeThrough = (0,0,0,0)

#game-booleans
gamePaused = False
gameJustUnPaused = True
playerMoved = False

#player related
player = playerSprite
globs = []
thrusterRectX = pygame.Rect
thrusterRectY = pygame.Rect
thrusterRectWidth = 0
thrusterRectHeight = 0
dt = 0
blobRadius = 35
##Level One Instructions
gameL1Instructions = ["Welcome to "]

#blocks
miniGameOne_Paused_BlockSurface = pygame.Surface((0,0))
miniGameOne_Paused_BlockSurfacePos = (0,0)
miniGameOne_Paused_ResumeBlock = pygame.Rect
miniGameOne_Paused_OptionsBlock = pygame.Rect
miniGameOne_Paused_LeaveBlock = pygame.Rect
miniGameOne_Paused_HelpBlock = pygame.Rect

#game-bar


def graphicsPreparation(screenWidth, screenHeight):
    global scrW, scrH
    global miniGameOne_Paused_BlockSurface, miniGameOne_Paused_BlockSurfacePos, miniGameOne_Paused_ResumeBlock, miniGameOne_Paused_OptionsBlock, miniGameOne_Paused_LeaveBlock, miniGameOne_Paused_HelpBlock
    global blobRadius, player, globs
    global ORANGE, GREEN, RED, TURQUOISE, GRAY, GRAY_FADE

    scrW = screenWidth
    scrH = screenHeight

    #gameLevelOne
    ##PlayerSprite
    blobRadius = scrH/40
    pThrust = scrW / 7.5
    t_max_scrW = 9
    kD = pThrust * (t_max_scrW)**2 / (scrW)**2
    player = playerSprite(int(scrW/2), int(scrH/2), blobRadius, ORANGE, pThrust, kD)
    globAmount = 20
    for i in range(globAmount):
        globs.append(glob(int(blobRadius/3), scrW, scrH))


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
    

def drawState(window, time):
    global miniGameOne_Paused_Block, miniGameOne_Paused_ResumeBlock, miniGameOne_Paused_OptionsBlock, miniGameOne_Paused_LeaveBlock, miniGameOne_Paused_HelpBlock
    global gamePaused, player, playerMoved, dt, globs, playerJustUnPaused
    global scrH, scrW

    dt = time

    #coveringup pause screen when it's just unpaused.
    if(gameJustUnPaused == True):
        gameJustUnpaused = False
        window.fill(BLACK)

    #player drawing
    player.posPlayerSurface()
    window.blit(player.playerShadow, (player.pShadowX, player.pShadowY))
    window.blit(player.getPlayerSurface(), (player.pSurfaceX, player.pSurfaceY))

    #glob drawing
    for i in range(len(globs)):
        pygame.draw.circle(window, globs[i].COLOUR, (globs[i].x, globs[i].y), globs[i].R, 0)

    
    
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
            player.playerMove(dt, scrH, scrW)

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

        #Check other buttons?
    elif(miniGameOne_Paused_ResumeBlock.block().collidepoint(pauseX, pauseY) == True):
        #Start game!
        pauseGame(False, state)
        clickConfirmed = True
    elif(miniGameOne_Paused_OptionsBlock.block().collidepoint(pauseX, pauseY) == True):
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
        if(keyPressed[pygame.K_DOWN] or keyPressed[pygame.K_s]):
            player.dT = True
            playerMoved = True
        if(keyPressed[pygame.K_UP] or keyPressed[pygame.K_w]):
            player.uT = True
            playerMoved = True
        if(keyPressed[pygame.K_RIGHT] or keyPressed[pygame.K_d]):
            player.rT = True
            playerMoved = True
        if(keyPressed[pygame.K_LEFT] or keyPressed[pygame.K_a]):
            player.lT = True
            playerMoved = True

def checkKeyRelease(event, state):
    global gamePaused, player, playerMoved

    keyRegistered = False

    if(gamePaused == False and keyRegistered == False):
        if(event.key == pygame.K_ESCAPE and keyRegistered == False):
            pauseGame(True, state)
            keyRegisterd = True
        if(event.key == pygame.K_DOWN or event.key == pygame.K_s):
            player.dT = False
        if(event.key == pygame.K_UP or pygame.K_w):
            player.uT = False
        if(event.key == pygame.K_RIGHT or pygame.K_d):
            player.rT = False
        if(event.key == pygame.K_LEFT or pygame.K_a):
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

#Key recognition of developer system is still buggy. E.g. hold down arrow(down), press another key and then release that same key. down thrust will also switch off... Other key combinations are also faulty.
    