from utils import select, init, play

if __name__ == "__main__":
    level = select()
    main_grid = init(level)
    play(main_grid)
