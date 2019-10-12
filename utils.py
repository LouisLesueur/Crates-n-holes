import os
from grid import Grid, clear
from grid_element import Wall, EmptySquare, Door, Hole, Crate, Character
from grid_element import DeepHole, TurnstileBody, TurnstileArm
from move import move_player, find_turnstile_body


def open_grid(level):
    """To open a grid
       Input: path to a level
       Output:
           -- A table containing the coords of players
           -- A table containing all grid_elements"""
    # Opening the file containing the level
    try:
        level_file = open(level, 'r')
    except Exception:
        print("Can't read the level")
    lines = level_file.readlines()
    lines = [line.rstrip() for line in lines]

    # grid dimensions
    n_lig = len(lines)
    n_col = len(lines[0])

    # Initialisation of table table, which contains all grid elements
    table = [[0]*n_col for _ in range(n_lig)]

    check_door = 0
    check_char = 4*[0]
    players = 4*[(-1, -1)]

    for i in range(n_lig):
        for j in range(n_col):
            if lines[i][j] == '#':
                table[i][j] = Wall()
            elif lines[i][j] == ' ':
                table[i][j] = EmptySquare()
            elif lines[i][j] == 'o':
                table[i][j] = Hole()
            elif lines[i][j] == '*':
                table[i][j] = Crate()
            elif lines[i][j] == 'O':
                table[i][j] = DeepHole()
            elif lines[i][j] == '%':
                table[i][j] = TurnstileBody()
            elif lines[i][j] == '°':
                table[i][j] = TurnstileArm()
                # to check if the arm is not alone
                find_turnstile_body()
            elif lines[i][j] == '@':
                table[i][j] = Door()
                check_door += 1
            else:
                for k in range(1, 5):
                    if lines[i][j] == str(k):
                        table[i][j] = Character(str(k))
                        check_char[k-1] += 1
                        players[k-1] = (i, j)

    if check_door > 1:
        raise Exception("Must be only one door")

    for k in range(4):
        if check_char[k] > 1:
            raise Exception("Must be only one player of each type")

    return table, players


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
    table, players = open_grid(level)
    return Grid(table, players)


def play(main_grid: Grid):
    """Function which displays and updates the grid"""
    main_grid.show()
    message = "Good luck !"
    player_symbols = ['1', '2', '3', '4']
    order_symbols = {'v': (1, 0), '^': (-1, 0), '>': (0, 1), '<': (0, -1)}
    current_player = 1
    while main_grid.win == 0:
        print(message)
        orders = input("Move with 1234<>v^ (curent player "+str(current_player)+"): ")
        for order in orders:
            if order in player_symbols:
                if main_grid.players[int(order)-1] != (-1, -1):
                    current_player = int(order)
            elif order in order_symbols:
                direction_h = order_symbols[order][0]
                direction_v = order_symbols[order][1]
                message = move_player(main_grid, current_player,
                                      direction_h, direction_v)
                print(message)
            else:
                print(order+' is not an acceptable character !')

        main_grid.show()

        # Checking if it's a win
        if main_grid.win == 1:
            print("You win !")
        elif main_grid.win == -1:
            print("You lose !")
