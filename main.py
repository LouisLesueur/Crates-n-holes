"""
The main module of the game
"""
from utils import select, init, play

if __name__ == "__main__":
    level = select()
    main_grid = init(main_grid)
    play(main_grid)
