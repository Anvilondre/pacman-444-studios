from src.controller.GameLogic import Controller
from src.data.Levels import Level1, Level2, Level3, Level4, Level5
from itertools import cycle

if __name__ == "__main__":
    levels = cycle((Level1, Level2, Level3, Level4, Level5))
    game = Controller(levels)
    game.run()