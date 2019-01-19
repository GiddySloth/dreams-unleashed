import pygame, sys

class playerSprite:
    #physics stuff
    x = 0
    prevX = 0
    y = 0
    prevY = 0
    a_x = 0
    a_y = 0
    v_x = 0
    v_y = 0

    uT = False
    dT = False
    rT = False
    lT = False

    dirY = "up"
    dirX = "right"

    #thrust
    t = 96
    thrusterOverlap = 8/10

    #thrusterRectangles
    thrusterRectXR = pygame.Rect
    thrusterRectXL = pygame.Rect
    thrusterRectYT = pygame.Rect
    thrusterRectYD = pygame.Rect
    thrusterRectWidth = 0
    thrusterRectHeight = 0

    #drag coefficient
    kD = 24

    #radius
    R = 30

    #ring percent factor
    ringPercent = 30
    W = 10
    
    #def colour
    COLOUR = (0, 0, 0, 255)
    BLACK = (0,0,0,255)
    RED = (255, 0, 0, 255)

    #player surfaces, different ones for each thruster set up so they don't have to be drawn.
    playerSurfaceNoThrust = pygame.Surface((0,0))
    playerSurfaceT_R = pygame.Surface((0,0))
    playerSurfaceT_L = pygame.Surface((0,0))
    playerSurfaceT_U = pygame.Surface((0,0))
    playerSurfaceT_D = pygame.Surface((0,0))

    playerSurfaceT_RL = pygame.Surface((0,0))
    playerSurfaceT_RU = pygame.Surface((0,0))
    playerSurfaceT_RD = pygame.Surface((0,0))
    playerSurfaceT_UD = pygame.Surface((0,0))
    playerSurfaceT_UL = pygame.Surface((0,0))
    playerSurfaceT_DL = pygame.Surface((0,0))

    playerSurfaceT_ULD = pygame.Surface((0,0))
    playerSurfaceT_RUL = pygame.Surface((0,0))
    playerSurfaceT_DRU = pygame.Surface((0,0))
    playerSurfaceT_RDL = pygame.Surface((0,0))

    playerSurfaceT_URDL = pygame.Surface((0,0))
    
    pSurfaceX = 0
    pSurfaceY = 0
    playerShadow = pygame.Surface((0,0))
    shadowRect = pygame.Rect
    pShadowX = 0
    pShadowY = 0

    

    def __init__(self, x_pos, y_pos, blobRadius, colour, pThrust, pDrag):
        self.x = x_pos
        self.y = y_pos
        self.prevX = self.x
        self.prevY = self.y

        self.t = pThrust
        self.kD = pDrag

        self.R = int(blobRadius)
        self.W = int(self.R * self.ringPercent/100)

        self.COLOUR = colour

        self.thrusterRectWidth = int(self.R*1.5)
        self.thrusterRectHeight = int(self.R*4/7)

        self.thrusterRectXR = pygame.Rect(0,0, self.thrusterRectWidth, self.thrusterRectHeight)
        self.thrusterRectXL = pygame.Rect(0,0, self.thrusterRectWidth, self.thrusterRectHeight)
        self.thrusterRectYT = pygame.Rect(0,0, self.thrusterRectHeight, self.thrusterRectWidth)
        self.thrusterRectYD = pygame.Rect(0,0, self.thrusterRectHeight, self.thrusterRectWidth)
        
        self.playerSurfaceNoThrust = pygame.Surface(( (self.thrusterRectWidth*2 + self.R*2), (self.thrusterRectWidth*2 + self.R*2) )).convert()
        pygame.draw.circle(self.playerSurfaceNoThrust, self.COLOUR, (int(self.playerSurfaceNoThrust.get_width()/2), int(self.playerSurfaceNoThrust.get_height()/2)), self.R, self.W)

        self.thrusterRectXL.midleft = (int(self.playerSurfaceNoThrust.get_width()/2-self.thrusterRectWidth-self.R*8/10), int(self.playerSurfaceNoThrust.get_height()/2))
        self.thrusterRectXR.midleft = (int(self.playerSurfaceNoThrust.get_width()/2+self.R*8/10), int(self.playerSurfaceNoThrust.get_height()/2))
        self.thrusterRectYT.midbottom = (int(self.playerSurfaceNoThrust.get_width()/2), int(self.playerSurfaceNoThrust.get_height()/2-self.R*8/10))
        self.thrusterRectYD.midtop = (int(self.playerSurfaceNoThrust.get_width()/2), int(self.playerSurfaceNoThrust.get_height()/2+self.R*8/10))

        #Solo thrusters
        self.playerSurfaceT_R = pygame.Surface(( (self.thrusterRectWidth*2 + self.R*2), (self.thrusterRectWidth*2 + self.R*2) )).convert()
        pygame.draw.ellipse(self.playerSurfaceT_R, self.RED, self.thrusterRectXL, 0)
        pygame.draw.circle(self.playerSurfaceT_R, self.COLOUR, (int(self.playerSurfaceNoThrust.get_width()/2), int(self.playerSurfaceNoThrust.get_height()/2)), self.R, self.W)
        
        self.playerSurfaceT_L = pygame.Surface(( (self.thrusterRectWidth*2 + self.R*2), (self.thrusterRectWidth*2 + self.R*2) )).convert()
        pygame.draw.ellipse(self.playerSurfaceT_L, self.RED, self.thrusterRectXR, 0)
        pygame.draw.circle(self.playerSurfaceT_L, self.COLOUR, (int(self.playerSurfaceNoThrust.get_width()/2), int(self.playerSurfaceNoThrust.get_height()/2)), self.R, self.W)
        
        self.playerSurfaceT_U = pygame.Surface(( (self.thrusterRectWidth*2 + self.R*2), (self.thrusterRectWidth*2 + self.R*2) )).convert()
        pygame.draw.ellipse(self.playerSurfaceT_U, self.RED, self.thrusterRectYD, 0)
        pygame.draw.circle(self.playerSurfaceT_U, self.COLOUR, (int(self.playerSurfaceNoThrust.get_width()/2), int(self.playerSurfaceNoThrust.get_height()/2)), self.R, self.W)
        
        self.playerSurfaceT_D = pygame.Surface(( (self.thrusterRectWidth*2 + self.R*2), (self.thrusterRectWidth*2 + self.R*2) )).convert()
        pygame.draw.ellipse(self.playerSurfaceT_D, self.RED, self.thrusterRectYT, 0)
        pygame.draw.circle(self.playerSurfaceT_D, self.COLOUR, (int(self.playerSurfaceNoThrust.get_width()/2), int(self.playerSurfaceNoThrust.get_height()/2)), self.R, self.W)
        
        #Double Thrusters
        self.playerSurfaceT_RL = pygame.Surface(( (self.thrusterRectWidth*2 + self.R*2), (self.thrusterRectWidth*2 + self.R*2) )).convert()
        pygame.draw.ellipse(self.playerSurfaceT_RL, self.RED, self.thrusterRectXL, 0)
        pygame.draw.ellipse(self.playerSurfaceT_RL, self.RED, self.thrusterRectXR, 0)
        pygame.draw.circle(self.playerSurfaceT_RL, self.COLOUR, (int(self.playerSurfaceNoThrust.get_width()/2), int(self.playerSurfaceNoThrust.get_height()/2)), self.R, self.W)

        self.playerSurfaceT_RU = pygame.Surface(( (self.thrusterRectWidth*2 + self.R*2), (self.thrusterRectWidth*2 + self.R*2) )).convert()
        pygame.draw.ellipse(self.playerSurfaceT_RU, self.RED, self.thrusterRectXL, 0)
        pygame.draw.ellipse(self.playerSurfaceT_RU, self.RED, self.thrusterRectYD, 0)
        pygame.draw.circle(self.playerSurfaceT_RU, self.COLOUR, (int(self.playerSurfaceNoThrust.get_width()/2), int(self.playerSurfaceNoThrust.get_height()/2)), self.R, self.W)

        self.playerSurfaceT_RD = pygame.Surface(( (self.thrusterRectWidth*2 + self.R*2), (self.thrusterRectWidth*2 + self.R*2) )).convert()
        pygame.draw.ellipse(self.playerSurfaceT_RD, self.RED, self.thrusterRectXL, 0)
        pygame.draw.ellipse(self.playerSurfaceT_RD, self.RED, self.thrusterRectYT, 0)
        pygame.draw.circle(self.playerSurfaceT_RD, self.COLOUR, (int(self.playerSurfaceNoThrust.get_width()/2), int(self.playerSurfaceNoThrust.get_height()/2)), self.R, self.W)
        
        self.playerSurfaceT_UD = pygame.Surface(( (self.thrusterRectWidth*2 + self.R*2), (self.thrusterRectWidth*2 + self.R*2) )).convert()
        pygame.draw.ellipse(self.playerSurfaceT_UD, self.RED, self.thrusterRectYD, 0)
        pygame.draw.ellipse(self.playerSurfaceT_UD, self.RED, self.thrusterRectYT, 0)
        pygame.draw.circle(self.playerSurfaceT_UD, self.COLOUR, (int(self.playerSurfaceNoThrust.get_width()/2), int(self.playerSurfaceNoThrust.get_height()/2)), self.R, self.W)

        self.playerSurfaceT_DL = pygame.Surface(( (self.thrusterRectWidth*2 + self.R*2), (self.thrusterRectWidth*2 + self.R*2) )).convert()
        pygame.draw.ellipse(self.playerSurfaceT_DL, self.RED, self.thrusterRectXR, 0)
        pygame.draw.ellipse(self.playerSurfaceT_DL, self.RED, self.thrusterRectYT, 0)
        pygame.draw.circle(self.playerSurfaceT_DL, self.COLOUR, (int(self.playerSurfaceNoThrust.get_width()/2), int(self.playerSurfaceNoThrust.get_height()/2)), self.R, self.W)

        self.playerSurfaceT_UL = pygame.Surface(( (self.thrusterRectWidth*2 + self.R*2), (self.thrusterRectWidth*2 + self.R*2) )).convert()
        pygame.draw.ellipse(self.playerSurfaceT_UL, self.RED, self.thrusterRectYD, 0)
        pygame.draw.ellipse(self.playerSurfaceT_UL, self.RED, self.thrusterRectXR, 0)
        pygame.draw.circle(self.playerSurfaceT_UL, self.COLOUR, (int(self.playerSurfaceNoThrust.get_width()/2), int(self.playerSurfaceNoThrust.get_height()/2)), self.R, self.W)

        #Triple Thrusters
        self.playerSurfaceT_ULD = pygame.Surface(( (self.thrusterRectWidth*2 + self.R*2), (self.thrusterRectWidth*2 + self.R*2) )).convert()
        pygame.draw.ellipse(self.playerSurfaceT_ULD, self.RED, self.thrusterRectYD, 0)
        pygame.draw.ellipse(self.playerSurfaceT_ULD, self.RED, self.thrusterRectXR, 0)
        pygame.draw.ellipse(self.playerSurfaceT_ULD, self.RED, self.thrusterRectYT, 0)
        pygame.draw.circle(self.playerSurfaceT_ULD, self.COLOUR, (int(self.playerSurfaceNoThrust.get_width()/2), int(self.playerSurfaceNoThrust.get_height()/2)), self.R, self.W)

        self.playerSurfaceT_RUL = pygame.Surface(( (self.thrusterRectWidth*2 + self.R*2), (self.thrusterRectWidth*2 + self.R*2) )).convert()
        pygame.draw.ellipse(self.playerSurfaceT_RUL, self.RED, self.thrusterRectXL, 0)
        pygame.draw.ellipse(self.playerSurfaceT_RUL, self.RED, self.thrusterRectXR, 0)
        pygame.draw.ellipse(self.playerSurfaceT_RUL, self.RED, self.thrusterRectYD, 0)
        pygame.draw.circle(self.playerSurfaceT_RUL, self.COLOUR, (int(self.playerSurfaceNoThrust.get_width()/2), int(self.playerSurfaceNoThrust.get_height()/2)), self.R, self.W)

        self.playerSurfaceT_DRU = pygame.Surface(( (self.thrusterRectWidth*2 + self.R*2), (self.thrusterRectWidth*2 + self.R*2) )).convert()
        pygame.draw.ellipse(self.playerSurfaceT_DRU, self.RED, self.thrusterRectYD, 0)
        pygame.draw.ellipse(self.playerSurfaceT_DRU, self.RED, self.thrusterRectXL, 0)
        pygame.draw.ellipse(self.playerSurfaceT_DRU, self.RED, self.thrusterRectYT, 0)
        pygame.draw.circle(self.playerSurfaceT_DRU, self.COLOUR, (int(self.playerSurfaceNoThrust.get_width()/2), int(self.playerSurfaceNoThrust.get_height()/2)), self.R, self.W)

        self.playerSurfaceT_RDL = pygame.Surface(( (self.thrusterRectWidth*2 + self.R*2), (self.thrusterRectWidth*2 + self.R*2) )).convert()
        pygame.draw.ellipse(self.playerSurfaceT_RDL, self.RED, self.thrusterRectXL, 0)
        pygame.draw.ellipse(self.playerSurfaceT_RDL, self.RED, self.thrusterRectXR, 0)
        pygame.draw.ellipse(self.playerSurfaceT_RDL, self.RED, self.thrusterRectYT, 0)
        pygame.draw.circle(self.playerSurfaceT_RDL, self.COLOUR, (int(self.playerSurfaceNoThrust.get_width()/2), int(self.playerSurfaceNoThrust.get_height()/2)), self.R, self.W)

        #quadruple thruster
        self.playerSurfaceT_URDL = pygame.Surface(( (self.thrusterRectWidth*2 + self.R*2), (self.thrusterRectWidth*2 + self.R*2) )).convert()
        pygame.draw.ellipse(self.playerSurfaceT_URDL, self.RED, self.thrusterRectYD, 0)
        pygame.draw.ellipse(self.playerSurfaceT_URDL, self.RED, self.thrusterRectXR, 0)
        pygame.draw.ellipse(self.playerSurfaceT_URDL, self.RED, self.thrusterRectYT, 0)
        pygame.draw.ellipse(self.playerSurfaceT_URDL, self.RED, self.thrusterRectXL, 0)
        pygame.draw.circle(self.playerSurfaceT_URDL, self.COLOUR, (int(self.playerSurfaceNoThrust.get_width()/2), int(self.playerSurfaceNoThrust.get_height()/2)), self.R, self.W)


        self.shadowSurface = pygame.Surface((self.playerSurfaceNoThrust.get_width(), self.playerSurfaceNoThrust.get_height())).convert()
        self.shadowSurface.fill(self.BLACK)
  
    
    def velocity(self, dt):
        DragY = -self.v_y * abs(self.v_y) * self.kD
        DragX = -self.v_x * abs(self.v_x) * self.kD

        if(self.uT == True and self.dT != True):
            if(self.t <= abs(DragY)):
                self.a_y = 0
            elif(self.t > abs(DragY)):
                self.a_y = -self.t + DragY
            self.v_y = self.v_y + self.a_y * dt
        elif(self.dT == True and self.uT != True):
            if(self.t <= abs(DragY)):
                self.a_y = 0
            elif(self.t > abs(DragY)):
                self.a_y = self.t + DragY   
            self.v_y = self.v_y + self.a_y * dt
        else:
            self.a_y = abs(DragY)
            if(abs(self.v_y) < self.a_y*dt):
                self.v_y = 0
            elif(abs(self.v_y) > self.a_y*dt):
                if(self.v_y > 0):
                    self.v_y = self.v_y - self.a_y*dt
                elif(self.v_y < 0):
                    self.v_y = self.v_y + self.a_y*dt
        
        if(self.rT == True and self.lT != True):
            if(self.t <= abs(DragX)):
                self.a_x = 0
            elif(self.t > abs(DragX)):
                self.a_x = self.t + DragX
            self.v_x = self.v_x + self.a_x * dt
        elif(self.lT == True and self.rT != True):
            if(self.t <= abs(DragX)):
                self.a_x = 0
            elif(self.t > abs(DragX)):
                self.a_x = -self.t + DragX
            self.v_x = self.v_x + self.a_x * dt
        else:
            self.a_x = abs(DragX)
            if(abs(self.v_x) < self.a_x*dt):
                self.v_x = 0
            elif(abs(self.v_x) > self.a_x*dt):
                if(self.v_x > 0):
                    self.v_x = self.v_x - self.a_x*dt
                elif(self.v_x < 0):
                    self.v_x = self.v_x + self.a_x*dt

    def playerMove(self, dt, scrH, scrW):

        dy = int(dt*self.v_y)
        dx = int(dt*self.v_x)
        d_left = int(self.x - self.R)
        d_right = int(scrW-self.x - self.R)
        d_top = int(self.y - self.R)
        d_bottom = int(scrH-self.y - self.R)

        if(self.v_x > 0):
            if(abs(dx) < d_right):
                
                self.x = self.x + dx
            else:
                self.v_x = 0
                self.rT = False
        elif(self.v_x < 0):
            if(abs(dx) < d_left):
                self.prevX = self.x
                self.x = self.x + dx
            else:
                self.v_x = 0
                self.lT = False
        if(self.v_y > 0):
            if(abs(dy) < d_bottom):
                self.prevY = self.y
                self.y = self.y + dy
            else:
                self.v_y = 0
                self.dT = False
        elif(self.v_y < 0):
            if(abs(dy) < d_top):
                self.y = self.y + dy
                self.prevY = self.y
            else:
                self.v_y = 0
                self.uT = False

    def posPlayerSurface(self):

        self.pSurfaceX = int(self.x - self.playerSurfaceNoThrust.get_width()/2)
        self.pSurfaceY = int(self.y - self.playerSurfaceNoThrust.get_height()/2)
        self.pShadowX = int(self.prevX - self.playerSurfaceNoThrust.get_width()/2)
        self.pShadowY = int(self.prevY - self.playerSurfaceNoThrust.get_height()/2)
    
    def getPlayerSurface(self):
        thrustersOn = 0
        if(self.rT == True):
            thrustersOn = thrustersOn + 1
        if(self.lT == True):
            thrustersOn = thrustersOn + 1
        if(self.uT == True):
            thrustersOn = thrustersOn + 1
        if(self.dT == True):
            thrustersOn = thrustersOn + 1
    
        if(thrustersOn == 4):
            return self.playerSurfaceT_URDL
        elif(thrustersOn == 3):
            if(self.uT == True and self.lT == True and self. dT == True):
                return self.playerSurfaceT_ULD
            elif(self.rT == True and self.uT == True and self. lT == True):
                return self.playerSurfaceT_RUL
            elif(self.dT == True and self.rT == True and self.uT == True):
                return self.playerSurfaceT_DRU
            elif(self.rT == True and self.dT == True and self. lT == True):
                return self.playerSurfaceT_RDL
        elif(thrustersOn == 2):
            if(self.rT == True and self.lT == True):
                return self.playerSurfaceT_RL
            elif(self.rT == True and self.dT == True):
                return self.playerSurfaceT_RD
            elif(self.rT == True and self.uT == True):
                return self.playerSurfaceT_RU
            elif(self.dT == True and self. lT == True):
                return self.playerSurfaceT_DL
            elif(self.uT == True and self.lT == True):
                return self.playerSurfaceT_UL
            elif(self.dT == True and self.uT == True):
                return self.playerSurfaceT_UD
        elif(thrustersOn == 1):
            if(self.rT == True):
                return self.playerSurfaceT_R
            elif(self.lT == True):
                return self.playerSurfaceT_L
            elif(self.uT == True):
                return self.playerSurfaceT_U
            elif(self.dT == True):
                return self.playerSurfaceT_D
        elif(thrustersOn == 0):
            return self.playerSurfaceNoThrust
        