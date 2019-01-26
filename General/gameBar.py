import sys, random, pygame
from menublock import menuBlock

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

#Surface and menublocks
gameBarH = 0
gameBarSurface = pygame.Surface((0,0))
gameBar_DreamLayerBlock = pygame.Rect
gameBar_ScoreBlock = pygame.Rect
gameBar_HealthBlock = pygame.Rect

def graphicsPreparation(screenWidth, screenHeight, gameBarHeight):
    global scrW, scrH, gameBarSurface, gameBarH, gameBar_ScoreBlock, gameBar_HealthBlock, gameBar_DreamLayerBlock
    global GRAY

    gameBarH = gameBarHeight
    scrW = screenWidth
    scrH = screenHeight

    gameBarSurface = pygame.Surface((scrW, gameBarHeight)).convert()
    gameBarSurface.fill(GRAY)

    gameBar_DreamLayerBlock = menuBlock(int(15/30*gameBarH), int(2/30*gameBarH), int(gameBarH*150/30), int(gameBarH*26/30), "Dream Layer: 1", 90, GRAY, True)
    gameBar_ScoreBlock = menuBlock(int(scrW/2-41/60*gameBarH), int(2/30*gameBarH), int(gameBarH*82/30), int(gameBarH*26/30), "Score: 0", 90, GRAY, True)
    gameBar_HealthBlock = menuBlock(int(scrW - 90/30*gameBarH), int(2/30*gameBarH), int(gameBarH*75/30), int(gameBarH*26/30), "HP: 100", 90, GRAY, True)


def drawState(window, state):
    global gameBarSurface, gameBar_ScoreBlock, gameBar_HealthBlock, gameBar_DreamLayerBlock
    global GRAY

    gameBarSurface.fill(GRAY)

    #draw stuff the gamebar surface.
    gameBar_DreamLayerBlock.setNewTextNoFontRender("Dream Layer: " + str(state.dreamLayer))
    pygame.draw.rect(gameBarSurface, gameBar_DreamLayerBlock.COLOUR, gameBar_DreamLayerBlock.block())
    gameBarSurface.blit(gameBar_DreamLayerBlock.textShow(0), gameBar_DreamLayerBlock.textShow(1))

    gameBar_ScoreBlock.setNewTextNoFontRender("Score: " + str(int(state.score)))
    pygame.draw.rect(gameBarSurface, gameBar_ScoreBlock.COLOUR, gameBar_ScoreBlock.block())
    gameBarSurface.blit(gameBar_ScoreBlock.textShow(0), gameBar_ScoreBlock.textShow(1))

    if(state.playerHealth < 1 and state.playerHealth != 0):
        gameBar_HealthBlock.setNewTextNoFontRender("HP: 1")
    else:
        gameBar_HealthBlock.setNewTextNoFontRender("HP: " + str(int(state.playerHealth)))

    
    pygame.draw.rect(gameBarSurface, gameBar_HealthBlock.COLOUR, gameBar_HealthBlock.block())
    gameBarSurface.blit(gameBar_HealthBlock.textShow(0), gameBar_HealthBlock.textShow(1))

    gameBarSurface.convert()

    #gameBarSurface.convert()
    window.blit(gameBarSurface, (0,0))

