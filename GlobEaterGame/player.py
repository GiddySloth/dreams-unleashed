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

    #player surfaces
    playerSurface = pygame.Surface((0,0))
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

        self.playerSurface = pygame.Surface(( (self.thrusterRectWidth*2 + self.R*2), (self.thrusterRectWidth*2 + self.R*2) )).convert()
        self.shadowSurface = pygame.Surface((self.playerSurface.get_width(), self.playerSurface.get_height())).convert()
        self.shadowSurface.fill(self.BLACK)


        self.thrusterRectXL.midleft = (int(self.playerSurface.get_width()/2-self.thrusterRectWidth-self.R*8/10), int(self.playerSurface.get_height()/2))
        self.thrusterRectXR.midleft = (int(self.playerSurface.get_width()/2+self.R*8/10), int(self.playerSurface.get_height()/2))
        self.thrusterRectYT.midbottom = (int(self.playerSurface.get_width()/2), int(self.playerSurface.get_height()/2-self.R*8/10))
        self.thrusterRectYD.midtop = (int(self.playerSurface.get_width()/2), int(self.playerSurface.get_height()/2+self.R*8/10))


        
    
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

    def drawPlayerSurface(self):

        self.playerSurface.fill(self.BLACK)
        #thrusters
        if(self.lT == True):
            pygame.draw.ellipse(self.playerSurface, self.RED, self.thrusterRectXR, 0)
        if(self.rT == True):
            pygame.draw.ellipse(self.playerSurface, self.RED, self.thrusterRectXL, 0)
        if(self.dT == True):
            pygame.draw.ellipse(self.playerSurface, self.RED, self.thrusterRectYT, 0)
        if(self.uT == True):
            pygame.draw.ellipse(self.playerSurface, self.RED, self.thrusterRectYD, 0)
        
        #player
        pygame.draw.circle(self.playerSurface, self.COLOUR, (int(self.playerSurface.get_width()/2), int(self.playerSurface.get_height()/2)), self.R, self.W)

        self.pSurfaceX = int(self.x - self.playerSurface.get_width()/2)
        self.pSurfaceY = int(self.y - self.playerSurface.get_height()/2)
        self.pShadowX = int(self.prevX - self.playerSurface.get_width()/2)
        self.pShadowY = int(self.prevY - self.playerSurface.get_height()/2)

        
        



    