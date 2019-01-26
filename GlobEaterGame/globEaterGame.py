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
blockstacles = []
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

#game-bar


def graphicsPreparation(state, screenWidth, screenHeight, gameBarHeight, gameHeight):
    global scrW, scrH, miniGameOne_Surface_Pos, gameBarH
    global miniGameOne_Surface, miniGameOne_Paused_BlockSurface, miniGameOne_Paused_BlockSurfacePos, miniGameOne_Paused_ResumeBlock, miniGameOne_Paused_OptionsBlock, miniGameOne_Paused_LeaveBlock, miniGameOne_Paused_HelpBlock
    global blobRadius, player, globs
    global ORANGE, GREEN, RED, TURQUOISE, GRAY, GRAY_FADE

    scrW = screenWidth
    scrH = screenHeight
    gameBarH = gameBarHeight

    miniGameOne_Surface_Pos = (0, gameBarHeight)
    miniGameOne_Surface = pygame.Surface((scrW,gameHeight))

    #gameLevelOne
    ##PlayerSprite
    blobRadius = scrH/40
    pThrust = scrW / 5
    t_max_scrW = 12
    kD = pThrust * (t_max_scrW)**2 / (scrW)**2
    player = playerSprite(int(scrW/2), int((scrH-gameBarH)/2), blobRadius, ORANGE, pThrust, kD)
    
    #create globs and obstacles
    setLevel(state, player)

def stateEventHandler(state):
    global xMouse, yMouse

    for event in pygame.event.get():
        if(event.type == pygame.KEYDOWN):
            checkKeyPress(event)
        if(event.type == pygame.KEYUP):
            checkKeyRelease(event, state)   

def drawState(window, time, state):
    global miniGameOne_Surface, miniGameOne_Surface_Pos, miniGameOne_Paused_Block, miniGameOne_Paused_ResumeBlock, miniGameOne_Paused_OptionsBlock, miniGameOne_Paused_LeaveBlock, miniGameOne_Paused_HelpBlock
    global gamePaused, player, playerMoved, dt, globs, blockstacles, playerJustUnPaused
    global scrH, scrW, gameBarH

    dt = time

    if(state.gameHasBeenPaused == False and state.gameOver == False):

        if(playerMoved == True):
            player.velocity(dt)
            player.playerMove(dt, scrH, scrW, gameBarH)

            globsToRemoveList = []

            for j in range(len(globs)):
                if(checkGlobCollision(globs[j]) == True):
                    globsToRemoveList.append(j)

            for n in range(len(globsToRemoveList)):
                scoreHandling(state, "globEaten")
                temp = globsToRemoveList[len(globsToRemoveList)-1-n]
                pygame.draw.circle(miniGameOne_Surface, BLACK, (globs[temp].x, globs[temp].y), globs[temp].R, 0)
                globs.pop(temp)
            
            blockstaclesToRemoveList = []

            for u in range(len(blockstacles)):
                if(checkGlobCollision(blockstacles[u]) == True):
                    blockstaclesToRemoveList.append(u)

            for m in range(len(blockstaclesToRemoveList)):
                scoreHandling(state, "playerHitBlockstacle")
                temp = blockstaclesToRemoveList[len(blockstaclesToRemoveList)-1-m]
                tempBlockstacleRect = pygame.Rect(0,0, int(2*blockstacles[temp].R), int(2*blockstacles[temp].R))
                tempBlockstacleRect.center = (int(blockstacles[temp].x), int(blockstacles[temp].y))
                pygame.draw.rect(miniGameOne_Surface, BLACK, tempBlockstacleRect, 0)
                blockstacles.pop(temp)

            if(len(globs) == 0):
                state.dreamLayer = state.dreamLayer + 1
                setLevel(state, player)
                miniGameOne_Surface.fill(BLACK)
                state.checkNewScore()

            if(state.playerHealth <=0 ):
                state.gameOver = True
                state.playerHealth = 0
                state.lastGameScore = state.score
                state.checkNewScore()
                state.dreamLayer = 1
                player.died(int(scrW/2), int((scrH-gameBarH)/2))
                setLevel(state, player)
                miniGameOne_Surface.fill(BLACK)
        
    #player drawing
    player.posPlayerSurface(gameBarH)
    miniGameOne_Surface.blit(player.playerShadow, (player.pShadowX, player.pShadowY))
    miniGameOne_Surface.blit(player.getPlayerSurface(), (player.pSurfaceX, player.pSurfaceY))

    if(state.gameOver == False):
        #obstacle drawing
        for i in range(len(blockstacles)):
            tempBlockstacleRect = pygame.Rect(0,0, int(2*blockstacles[i].R), int(2*blockstacles[i].R))
            tempBlockstacleRect.center = (int(blockstacles[i].x), int(blockstacles[i].y))
            pygame.draw.rect(miniGameOne_Surface, blockstacles[i].COLOUR, tempBlockstacleRect, 0)
        #glob drawing
        for k in range(len(globs)):
            pygame.draw.circle(miniGameOne_Surface, globs[k].COLOUR, (globs[k].x, globs[k].y), globs[k].R, 0)

    miniGameOne_Surface.convert() 
    window.blit(miniGameOne_Surface, (0, gameBarH))

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

def checkKeyRelease(event, state):
    global gamePaused, player, playerMoved

    keyRegistered = False

    if(event.key == pygame.K_ESCAPE and keyRegistered == False):
        if(state.gameOver == False):
            pauseGame(True, state)
        keyRegisterd = True

    if(state.gameOver == False):
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

def checkGlobCollision(globCol):
    global player

    globDistance = ( (player.x-globCol.x)**2 + (player.y-globCol.y)**2 )**(0.5)

    if(globDistance < (player.R + globCol.R) ):
        return True
    else:
        return False

def setLevel(state, player):
    global globs, blockstacles, blobRadius, scrW, scrH, gameBarH

    state.gameBarChange == True

    #setting amounts and sizes of globs and blockstacles depending on level
    blockstaclesAmount = int(25*(1-(0.75)**(state.dreamLayer))) #Converges to 25.
    blockstacleSize = int((blobRadius/1.5)*(2.5-(0.85)**(state.dreamLayer-1))) #Converges to 5/3 * blob radius.
    globAmount = int(10*(1+(0.6)**(state.dreamLayer-1))) #Converges to 10 globs.
    globRadius = int((blobRadius/1.5)*(0.35+(0.9)**(state.dreamLayer-1))) #Converges to 7/30 * blob radius.

    #removal of still existing blockstacles.
    tempBlockstaclesAmount = blockstaclesAmount - (blockstaclesAmount - len(blockstacles))
    for b in range(tempBlockstaclesAmount):
        blockstacles.pop(tempBlockstaclesAmount-1-b)
    
    #removal of still existing globs
    tempGlobAmount = globAmount - (globAmount - len(globs))
    for b in range(tempGlobAmount):
        globs.pop(tempGlobAmount-1-b)

    #reappointing of blockstacles
    for j in range(blockstaclesAmount):
        unChecked = True

        while unChecked:
            confirmed = True
            blockstacleTemp = glob(blockstacleSize, scrW, scrH, gameBarH)

            #blockstacle vs. player
            distanceBlockstacleToPlayer = ((blockstacleTemp.x-player.x)**2 + (blockstacleTemp.y-player.y)**2) ** (0.5)

            if(distanceBlockstacleToPlayer < (5*player.R)):
                confirmed = False
            
            #blocstacle vs. other blockstacles
            for i in range(len(blockstacles)):
                distanceBlockstacleToBlockstacle = ((blockstacleTemp.x-blockstacles[i].x)**2 + (blockstacleTemp.y-blockstacles[i].y)**2) ** (0.5)
                if(distanceBlockstacleToBlockstacle < 1.1*(blockstacles[i].R+blockstacleTemp.R)):
                    confirmed = False
                    break

            if(confirmed == True):
                unChecked = False
                blockstacles.append(blockstacleTemp)
        

    #reappointing of globs
    for i in range(globAmount):
        unChecked = True
        
        while unChecked:
            confirmed = True
            globTemp = glob(globRadius, scrW, scrH, gameBarH)
            
            #glob to blockstacles
            for m in range(len(blockstacles)):
                distanceGlobToBlock = ((globTemp.x-blockstacles[m].x)**2 + (globTemp.y-blockstacles[m].y)**2) ** (0.5)
                if(distanceGlobToBlock <= (globTemp.R+blockstacles[m].R)):
                    confirmed = False
                    break
            
            #glob to player
            distanceGlobToPlayer = ((globTemp.x-player.x)**2 + (globTemp.y-player.y)**2) ** (0.5)
            if(distanceGlobToPlayer < (5*player.R)):
                confirmed = False

            #glob to globs
            for m in range(len(globs)):
                distanceGlobToGlob = ((globTemp.x-globs[m].x)**2 + (globTemp.y-globs[m].y)**2) ** (0.5)
                if(distanceGlobToGlob <= (globTemp.R+globs[m].R)):
                    confirmed = False
                    break
            
            if(confirmed == True):
                unChecked = False
                globs.append(globTemp)

def scoreHandling(state, gameEvent):
    if(gameEvent == "globEaten"):
        globEatenScore = 1 * (1.05)**(state.dreamLayer-1) #Does not converge.
        state.score = state.score + globEatenScore
        state.gameBarChange == True
    elif(gameEvent == "playerHitBlockstacle"):
        blockstacleDamage = 4 * (1.05)**(state.dreamLayer-1)
        state.playerHealth = state.playerHealth - blockstacleDamage
        state.gameBarChange == True

def pauseGame(pause, state):

    if(pause == True):
        state.FPS = 15
        state.gameHasBeenPausedMenu = True
        state.gameHasBeenPaused = True

#Key recognition of developer system is still buggy. E.g. hold down arrow(down), press another key and then release that same key. down thrust will also switch off... Other key combinations are also faulty.