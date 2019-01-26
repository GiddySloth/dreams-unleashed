import sys

class State:
    states = ["Game Menu", "GlobEaterGame", "MazeGame"]
    state = 0
    FPS = 0

    score = 0
    highScore = 0
    lastGameScore = 0
    playerHealth = 100
    dreamLayer = 1

    gameJustBeenUnPaused = False
    gameHasBeenPaused = False
    gameHasBeenPausedMenu = False

    gameBarChange = True
    gameOver = False
    gameJustDied = True
    gameHasBeenDead = False
    gameJustRestarted = False

    def __init__(self, initialState, FPSin):
        self.state = initialState
        self.FPS = FPSin
    
    def getState(self):
        stateString = self.states[self.state]
        return stateString
    
    def checkNewScore(self):
        if(self.score > self.highScore):
            self.highScore = self.score