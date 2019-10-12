"""
The main module of the game
"""
from utils import select, init, play

if __name__ == "__main__":
    LEVEL = select()
    MAIN_GRID = init(LEVEL)
    play(MAIN_GRID)
