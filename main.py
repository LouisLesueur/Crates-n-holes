from utils import select, init, play

if __name__ == "__main__":
    level = select()
    GRID = init(level)
    play(GRID)
