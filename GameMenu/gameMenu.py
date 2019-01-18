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
SeeThrough = (0,0,0,0)

titleColour = ORANGE
titles = ["Dreams Unleashed", "wEIrD", "SHRIEK!!!", "Hey :3", "Pygamegamegame", "Let's Go!"]
titleOn = 0

#blocks
gameMenu_TitleBlock = pygame.Rect
gameMenu_StartBlock = menuBlock
gameMenu_ExitBlock = pygame.Rect
gameMenu_ChangeTitleBlock = pygame.Rect
gameMenu_ExitBlockSubTitle = pygame.Rect
gameMenu_StartBlockSubTitle = pygame.Rect

def graphicsPreparation(screenWidth, screenHeight):
    global scrW, scrH
    global gameMenu_TitleBlock, gameMenu_StartBlock, gameMenu_ExitBlock, gameMenu_ChangeTitleBlock, gameMenu_ExitBlockSubTitle, gameMenu_StartBlockSubTitle
    global titlOn, titles, titleColour
    #global for colours.

    scrW = screenWidth
    scrH = screenHeight

    #Making menublocks.
    ##TitleBlock
    titleColour = ORANGE
    gameMenu_TitleBlock = menuBlock(int(1/3*scrW), int(1/8*scrH), int(1/3*scrW), int(1/8*scrH), titles[titleOn], 90, titleColour, True)
    ##StartBlock
    gameMenu_StartBlock = menuBlock(int(1/20*scrH), int(scrH-scrH*1/20-scrH*1/72-scrH*1/18), int(scrH*5/18), int(scrH*1/18), "START GAME", 90, GREEN, True)
    gameMenu_StartBlockSubTitle = menuBlock(int(1/20*scrH), int(scrH-scrH*1/20-scrH*1/72), int(scrH*5/18), int(scrH*1/72), "Play Dreams Unleashed", 90, GRAY, True)
    ##ExitBlock
    gameMenu_ExitBlock = menuBlock(int(scrW-1/20*scrH-scrH*1/8), int(scrH-scrH*1/20-scrH*1/72-scrH*1/18), int(scrH*1/8), int(scrH*1/18), "Exit", 90, RED, True)
    gameMenu_ExitBlockSubTitle = menuBlock(int(scrW-1/20*scrH-scrH*1/8), int(scrH-scrH*1/20-scrH*1/72), int(scrH*1/8), int(scrH*1/72), "To Main Menu", 90, GRAY, True)
    ##ChangeTitleBlock
    gameMenu_ChangeTitleBlock = menuBlock(int(scrW-1/20*scrH-scrH*1/9), int(scrH*1/20), int(scrH*1/9), int(scrH*1/36), "Press me?", 75, TURQUOISE, True)

def stateEventHandler(state):
    global xMouse, yMouse

    if(state.gameHasBeenPaused == True):
        gameMenu_StartBlock.setNewText("RESUME GAME")
        gameMenu_StartBlockSubTitle.setNewText("Continue Playing Dreams Unleashed")

    for event in pygame.event.get():
        if(event.type == pygame.MOUSEBUTTONUP):
            xMouse, yMouse = event.pos
            checkMouseClick(xMouse, yMouse, state)

    

def drawState(window):
    global BLACK
    global gameMenu_TitleBlock, gameMenu_StartBlock, gameMenu_ExitBlock, gameMenu_ChangeTitleBlock, gameMenu_ExitBlockSubTitle, gameMenu_StartBlockSubTitle

    window.fill(BLACK)

    pygame.draw.rect(window, gameMenu_TitleBlock.COLOUR, gameMenu_TitleBlock.block())
    window.blit(gameMenu_TitleBlock.textShow(0), gameMenu_TitleBlock.textShow(1))

    pygame.draw.rect(window, gameMenu_StartBlock.COLOUR, gameMenu_StartBlock.block())
    window.blit(gameMenu_StartBlock.textShow(0), gameMenu_StartBlock.textShow(1))
    pygame.draw.rect(window, gameMenu_StartBlockSubTitle.COLOUR, gameMenu_StartBlockSubTitle.block())
    window.blit(gameMenu_StartBlockSubTitle.textShow(0), gameMenu_StartBlockSubTitle.textShow(1))

    pygame.draw.rect(window, gameMenu_ExitBlock.COLOUR, gameMenu_ExitBlock.block())
    window.blit(gameMenu_ExitBlock.textShow(0), gameMenu_ExitBlock.textShow(1))
    pygame.draw.rect(window, gameMenu_ExitBlockSubTitle.COLOUR, gameMenu_ExitBlockSubTitle.block())
    window.blit(gameMenu_ExitBlockSubTitle.textShow(0), gameMenu_ExitBlockSubTitle.textShow(1))


    pygame.draw.rect(window, gameMenu_ChangeTitleBlock.COLOUR, gameMenu_ChangeTitleBlock.block())
    window.blit(gameMenu_ChangeTitleBlock.textShow(0), gameMenu_ChangeTitleBlock.textShow(1))

def checkMouseClick(x, y, state):
    global gameMenu_TitleBlock, gameMenu_StartBlock, gameMenu_ExitBlock, gameMenu_ChangeTitleBlock

    #Check exit button.
    if(gameMenu_ExitBlock.block().collidepoint(x,y) == True):
        #For now it's exit application, later this is just back to main menu.

        
        clickConfirmed = True
        sys.exit()
        #Check other buttons?
    elif(gameMenu_StartBlock.block().collidepoint(x,y) == True):
        #Start game!

        state.state = 1
        clickConfirmed = True
    elif(gameMenu_ChangeTitleBlock.block().collidepoint(x, y) == True):
        #Change the title. 
        clickConfirmed = True
        changeTitle()

def changeTitle():
    global titleOn, titles, titleColour, gameMenu_TitleBlock

    loopBool1 = True
    colourParts = [245, 150, 65]
    cR = 40

    #Changing title text.
    while loopBool1:
        randomNumber = random.randint(0, len(titles)-1)
        if(randomNumber == titleOn):
            pass
        elif(randomNumber != titleOn):
            titleOn = randomNumber
            loopBool1 = False
    
    #Change title block shade.
    colourParts[0] = random.randint(colourParts[0]-cR,255)
    colourParts[1] = random.randint(colourParts[1]-cR,colourParts[1]+cR)
    colourParts[2] = random.randint(colourParts[2]-cR,colourParts[2]+cR)
    shade = random.randint(0,255)

    titleColour = (colourParts[0], colourParts[1], colourParts[2], shade)
    
    
    gameMenu_TitleBlock.COLOUR = titleColour
    gameMenu_TitleBlock.setNewText(titles[titleOn])
    