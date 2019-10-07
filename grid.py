import os
from grid_element import Wall, EmptyCase, Door, Hole, Crate, Character


def clear():
    """To clear the screen between two moves"""
    # windows
    if os.name == 'nt':
        _ = os.system('cls')

    # unix based systems
    else:
        _ = os.system('clear')


class Grid:
    """This class contains all the elements of the game."""

    def __init__(self, level: str):
        """Constructor of Grid

        It contains a table in which all the elements of the current level are
        contained. It has methods to show the grid, to move the elements and
        to know if the game is won.

        Inputs:
            --level: path to a textfile containig the level"""

        # Opening the file containing the level
        try:
            level_file = open(level, 'r')
        except Exception:
            print("Can't read the level")
        lines = level_file.readlines()
        lines = [line.rstrip() for line in lines]

        # grid dimensions
        self.n_lig = len(lines)
        self.n_col = len(lines[0])

        # win is equal to -1 if the game is lost, 1 if it's won, 0 else
        self._win = 0

        # Initialisation of table table, which contains all grid elements
        self.table = [[0]*self.n_col for _ in range(self.n_lig)]
        for i in range(self.n_lig):
            for j in range(self.n_col):
                if lines[i][j] == '#':
                    self.table[i][j] = Wall(i, j)
                if lines[i][j] == ' ':
                    self.table[i][j] = EmptyCase(i, j)
                if lines[i][j] == '@':
                    self.table[i][j] = Door(i, j)
                if lines[i][j] == 'o':
                    self.table[i][j] = Hole(i, j)
                if lines[i][j] == '*':
                    self.table[i][j] = Crate(i, j)
                if lines[i][j] == '1':
                    self.table[i][j] = Character(i, j)
                    self.char_h = i
                    self.char_v = j

    @property
    def win(self):
        """To get the value of win in the main loop"""
        return self._win

    def get(self, i: int, j: int):
        """Return the grid_element table[i][j]"""
        return self.table[i][j]

    def set(self, i: int, j: int, case):
        """Set the grid_element table[i][j]"""
        self.table[i][j] = case

    def move(self, order: str):
        """Function that manage the movement:
            Input: an order typed with the keyboard (string)
            Output: nothing"""

        direction_h = 0
        direction_v = 0

        if order == 's':
            direction_h = 1
        if order == 'z':
            direction_h = -1
        if order == 'd':
            direction_v = 1
        if order == 'q':
            direction_v = -1

        # player = Character object in the grid
        player = self.get(self.char_h, self.char_v)
        # target = grid_element towards which the player is heading
        target = self.get(self.char_h+direction_h, self.char_v+direction_v)

        # door leads to victory
        if type(target) is Door:
            self._win = 1

        # all cases must be treated
        if (type(target) is not Wall) and (type(target) is not Door):
            # if the player moves a crate, the element behind must be checked
            beyond_target = self.get(self.char_h+2*direction_h,
                                     self.char_v+2*direction_v)
            if type(target) is Hole:
                self._win = -1

            if type(target) is EmptyCase:
                player.move(direction_h, direction_v)
                target.move(-direction_h, -direction_v)
                self.set(self.char_h,
                         self.char_v,
                         target)
                self.set(self.char_h+direction_h,
                         self.char_v+direction_v,
                         player)
                self.char_h += direction_h
                self.char_v += direction_v

            if (type(target) is Crate and
                    not(type(beyond_target) is Wall) and
                    not(type(beyond_target) is Crate)):
                beyond_target = self.get(self.char_h+2*direction_h,
                                         self.char_v+2*direction_v)
                player.move(direction_h, direction_v)
                self.set(self.char_h+direction_h,
                         self.char_v+direction_v, player)
                self.set(self.char_h,
                         self.char_v,
                         EmptyCase(self.char_h, self.char_v))

                if type(beyond_target) is EmptyCase:
                    target.move(direction_h, direction_v)
                    self.set(self.char_h+2*direction_h,
                             self.char_v+2*direction_v,
                             target)
                if type(beyond_target) is Hole:
                    self.set(self.char_h+2*direction_h,
                             self.char_v+2*direction_v,
                             EmptyCase(self.char_h+2*direction_h,
                                       self.char_v+2*direction_v))

                self.char_h += direction_h
                self.char_v += direction_v

    def show(self):
        """function that show the grid"""
        clear()
        for i in range(self.n_lig):
            line = ""
            for j in range(self.n_col):
                line += self.table[i][j].symbol
            print(line)
