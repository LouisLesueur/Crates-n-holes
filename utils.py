from grid import Grid, clear
import os


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

    LEVELS = os.listdir('levels')
    for i in range(len(LEVELS)):
        print(str(i)+" - "+str(LEVELS[i]))

    print("")

    choice = input("Which one ? (type a number, 0 by default): ")

    try:
        int(choice)
    except ValueError:
        print("That's not an int! 0 selected.")
        return "levels/"+LEVELS[0]

    return "levels/"+LEVELS[int(choice)]


def init(level: str):
    """Initialize the grid
       Input: absolute path to the level
       Output: The grid"""
    GRID = Grid(level)
    return GRID


def play(GRID: Grid):
    """Function which displays and updates the grid"""
    while GRID.win == 0:
        GRID.show()
        orders = input("Move with zqsd: ")
        for order in orders:
            GRID.move(order)

        if GRID.win == 1:
            print("You win !")
        else:
            print("You lose !")
