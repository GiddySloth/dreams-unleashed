import sys

class State:
    states = ["Game Menu", "GlobEaterGame","MazeGame"]
    state = 0
    FPS = 0

    score = 0

    gameHasBeenPaused = False
    gameHasBeenPausedMenu = False
    gameBarChange = True

    def __init__(self, initialState, FPSin):
        self.state = initialState
        self.FPS = FPSin
    
    def getState(self):
        stateString = self.states[self.state]
        return stateString