import pygame, sys, random

class glob:

    scrW = 1920
    scrH = 1080

    eaten = False

    R = 1
    COLOUR = [255, 255, 255, 255]
    x = 0
    y = 0

    def __init__(self, globRadius, screenWidth, screenHeight, gameBarHeight):
        self.scrW = screenWidth
        self.scrH = screenHeight

        self.newRadius(globRadius)
        self.newPos(gameBarHeight)
        self.newColour()
    
    def newRadius(self, globRadius):
        rangeRP = 15
        randomRFactor = random.randint(100-rangeRP, 100+rangeRP)
        self.R = int(globRadius*randomRFactor/100)

    def newPos(self, gameBarHeight):
        randomX = random.randint(int(self.R*2), int(self.scrW-self.R*2))
        randomY = random.randint(int(self.R*2), int(self.scrH-self.R*2-gameBarHeight))

        self.x = randomX
        self.y = randomY

        #print("Glob coords: x = " + str(randomX) +", y = " + str(randomY))
    
    def newColour(self):
        colour = [0,0,0,255]
        colour[0] = random.randint(1,255)
        colour[1] = random.randint(1,255)
        colour[2] = random.randint(1,255)
        self.COLOUR = colour

        #print("Glob colour (q,r,z) = (" + str(colour[0]) + ", " + str(colour[1]) + ", " + str(colour[2]) + ")")

    def beenEaten(self):
        self.eaten == True
    

