import os
from math import sqrt


# Déplacer cette fonction dans utils fait tout planter
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

    def __init__(self, table, players):
        """Constructor of Grid

        It contains a table in which all the elements of the current level are
        contained. It has methods to show the grid, to move the elements and
        to know if the game is won.

        Inputs:
            --table: tableau de GridElements
            --players: dictionnaire joueur/coordonées"""

        self._win = 0
        self.n_lig = len(table)
        self.n_col = len(table[0])
        self._players = players
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
    def players(self):
        """To get the table with all players coords"""
        return self._players

    @property
    def win(self):
        """Computes and returns the status of the game"""
        nb_players = 0
        for i in range(4):
            if self.players[i] != (-1, -1):
                pos_h = self.players[i][0]
                pos_v = self.players[i][1]
                if self.table[pos_h][pos_v].win == 1:
                    self._win = 1
                nb_players += 1
        if nb_players == 0:
            self._win = -1
        return self._win

    def change_player(self, player_id: int, n_h: int, n_v: int):
        """To modify a player coord"""
        self._players[player_id-1] = (n_h, n_v)

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

    def show(self):
        """function that show the grid"""
        clear()
        for i in range(self.n_lig):
            line = ""
            for j in range(self.n_col):
                line += str(self.table[i][j])
            print(line)
