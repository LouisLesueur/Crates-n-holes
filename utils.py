import os
from grid import Grid, clear


def select():
    """A very simple selection menu
       Output: The absolute path to the level"""
    clear()
    print("*-------------------------------*")
    print("|           TDLOG TP1           |")
    print("|        Louis Lesueur          |")
    print("*-------------------------------*")
    print("")
    print("Chose your level: ")

    levels = os.listdir('levels')
    for i in range(len(levels)):
        print(str(i)+" - "+str(levels[i]))

    print("")

    choice = input("Which one ? (type a number, 0 by default): ")

    try:
        int(choice)
    except ValueError:
        print("That's not an int! 0 selected.")
        return "levels/"+levels[0]

    return "levels/"+levels[int(choice)]


def init(level: str):
    """Initialize the grid
       Input: absolute path to the level
       Output: The grid"""
    main_grid = Grid(level)
    return main_grid


def play(main_grid: Grid):
    """Function which displays and updates the grid"""
    while main_grid.win == 0:
        main_grid.show()
        orders = input("Move with zqsd: ")
        for order in orders:
            main_grid.move(order)

        if main_grid.win == 1:
            print("You win !")
        else:
            print("You lose !")
