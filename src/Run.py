from src.controller.GameLogic import Controller
from src.data.Levels import Level1, Level2, Level3, Level4, Level5

if __name__ == "__main__":
    levels = (Level1, Level2, Level3, Level4, Level5)
    game = Controller(levels)
    game.run()