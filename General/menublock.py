import pygame, sys

class menuBlock:
    menuBlock1 = pygame.Rect
    size = 1
    x = 0
    y = 0
    w = 0
    h = 0
    displayText = ""
    marginPercent = 50
    COLOUR = (0,0,0,255)

    menuBlockFont = pygame.font.Font
    menuBlockText = pygame.font.Font.render
    menuBlockTextRectangle = pygame.Rect

    def __init__(self, x, y, w, h, text, mPercent, color, renderTextYN):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.marginPercent = mPercent
        self.COLOUR = color

        self.menuBlock1 = pygame.Rect(x, y, w, h)

        #Checking if text should be rendered right away or not.
        if (renderTextYN == True):
            self.setNewText(text)
        elif (renderTextYN == False):
            self.displayText = text

    def block(self):
        return self.menuBlock1

    def textRender(self):
        self.menuBlockFont = pygame.font.Font(None, self.size)
        self.menuBlockText = self.menuBlockFont.render(self.displayText, True, (0,0,0,255))
        self.menuBlockTextRectangle = self.menuBlockText.get_rect()
        self.menuBlockTextRectangle.center = self.menuBlock1.center

    def textShow(self, i):
        if(i == 0):
            return self.menuBlockText
        elif(i == 1):
            return self.menuBlockTextRectangle

    def fontSize(self):
        BLACK = (0,0,0,255)

        #later we can add font customization, not necessary for now.
        fontSize = 1
        x1 = 1
        y1 = 1

        sizeSearching = True

        xMax = int(self.menuBlock1.width)
        yMax = int(self.menuBlock1.height)

        xMaxMargin = xMax * self.marginPercent/100
        yMaxMargin = yMax * self.marginPercent/100

        while sizeSearching:
            fontFitting = pygame.font.Font(None, fontSize)
            fontFittingText = fontFitting.render(self.displayText, True, BLACK)

            x1, y1 = fontFittingText.get_size()

            if(x1 > xMaxMargin):
                break
            elif(y1 > yMaxMargin):
                break        

            fontSize = fontSize + 1
    
        self.size = fontSize

    def setNewText(self, newText):
        self.displayText = newText
        self.fontSize()
        self.textRender()
        