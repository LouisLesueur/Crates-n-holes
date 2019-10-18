"""
Here is the definition of the class Grid, which is essential for the game
"""

import os
from math import sqrt
from grid_element import Door, Crate, Character
from grid_element import TurnstileArm, TurnstileBody
from grid_element import Wall, Hole, EmptySquare


class Grid:
    """This class contains all the elements of the game."""

    def __init__(self, level):
        """Constructor of Grid

        It contains a table in which all the elements of the current level are
        contained. It has methods to show the grid, to move the elements and
        to know if the game is won.

        Inputs:
            --level: path to a level"""

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
                    table[i][j] = Hole(1)
                elif lines[i][j] == '*':
                    table[i][j] = Crate()
                elif lines[i][j] == 'O':
                    table[i][j] = Hole(2)
                elif lines[i][j] == '%':
                    table[i][j] = TurnstileBody()
                elif lines[i][j] == '°':
                    table[i][j] = TurnstileArm()
                    # to check if the arm is not alone
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

        self._win = 0
        self.n_lig = len(table)
        self.n_col = len(table[0])
        self._players_to_coords = players
        self.table = table

    def __getitem__(self, key):
        """Return the grid_element table[i][j]"""
        i, j = key
        return self.table[i][j]

    def __setitem__(self, key, square):
        """Set the grid_element table[i][j]"""
        i, j = key
        self.table[i][j] = square

    @property
    def players_to_coords(self):
        """To get the table with all players coords"""
        return self._players_to_coords

    @property
    def win(self):
        """Computes and returns the status of the game"""
        nb_players = 0
        for i in range(4):
            if self.players_to_coords[i] != (-1, -1):
                nb_players += 1
        if nb_players == 0:
            self._win = -1
        return self._win

    def you_win(self):
        """To win the game"""
        self._win = 1

    def change_player(self, player_id: int, n_h: int, n_v: int):
        """To modify a player coord"""
        self._players_to_coords[player_id-1] = (n_h, n_v)

    def swap(self, id1, id2):
        """To swap two elements in the grid, with coord id1 and id2"""
        dist = sqrt((id2[0]-id1[0])**2+(id2[1]-id1[1])**2)
        if dist == 1:
            if (self.table[id1[0]][id1[1]].is_movable and
                    self.table[id2[0]][id2[1]].is_movable):
                to_be_swaped1 = self.table[id1[0]][id1[1]]
                to_be_swaped2 = self.table[id2[0]][id2[1]]
                self.table[id1[0]][id1[1]] = to_be_swaped2
                self.table[id2[0]][id2[1]] = to_be_swaped1
            else:
                raise Exception("You are trying to move fixed objects")
        else:
            raise Exception("Objects too far to be swaped !")

    def big_swap(self, id1, id2, id3):
        """To make a circular rotation"""
        self.swap(id2, id3)
        self.swap(id1, id2)

    def __str__(self):
        """function that show the grid"""
        grid_str = ""
        for i in range(self.n_lig):
            line = ""
            for j in range(self.n_col):
                line += str(self.table[i][j])
            grid_str += (line+str('\n'))
        return grid_str
