from src.controller.GameLogic import Controller
from src.data.Levels import Level1, Level2, Level3
from itertools import cycle

if __name__ == "__main__":
    levels = cycle((Level1, Level2, Level3))
    game = Controller(levels)
    game.run()
