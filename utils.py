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
    return Grid(level)


def play(main_grid: Grid):
    """Function which displays and updates the grid"""
    order_symbols = {'v': (1, 0), '^': (-1, 0), '>': (0, 1), '<': (0, -1)}
    while main_grid.win == 0:
        # Je laisse ça ici sinon on ne voit plus les messages
        main_grid.show()
        orders = input("Move with <>v^: ")
        for order in orders:
            if order in order_symbols:
                direction_h, direction_v = order_symbols[order]
                main_grid.move(direction_h, direction_v)
            else:
                print(order+' is not an acceptable character !')

        if main_grid.win == 1:
            print("You win !")
        elif main_grid == -1:
            print("You lose !")
