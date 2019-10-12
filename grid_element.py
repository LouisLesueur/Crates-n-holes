"""
Here are the various elements of the game
"""


class GridElement:
    """Base class for grid_elements"""

    def __init__(self, is_movable: bool, symbol: str):
        self._is_movable = is_movable
        self.symbol = symbol

    def __str__(self):
        """To print the symbol with print"""
        return self.symbol

    @property
    def is_movable(self):
        """To verify if the element is movable"""
        return self._is_movable


class Character(GridElement):
    """A charcter is a movable grid_element"""

    def __init__(self, symbol: str):
        self._win = 0
        allowed_symbols = {'1', '2', '3', '4'}
        if symbol in allowed_symbols:
            GridElement.__init__(self, True, symbol)
        else:
            raise Exception("Only 1, 2, 3 and 4 can be a player")

    @property
    def win(self):
        """To know if the player has win"""
        return self._win

    @win.setter
    def win(self, n_win):
        """To change the value of win"""
        self._win = n_win


class Wall(GridElement):
    """ A wall is a not movable grid_element """

    def __init__(self):
        GridElement.__init__(self, False, '#')


class Hole(GridElement):
    """A hole is a not movable grid_element"""

    def __init__(self):
        GridElement.__init__(self, False, 'o')


class DeepHole(GridElement):
    """A hole, but deeper"""

    def __init__(self):
        GridElement.__init__(self, False, 'O')


class Door(GridElement):
    """A door is a not movable grid_element"""

    def __init__(self):
        GridElement.__init__(self, False, '@')


class Crate(GridElement):
    """A crate is a movable grid_element"""

    def __init__(self):
        GridElement.__init__(self, True, '*')


class EmptySquare(GridElement):
    """An emptysquare is a movable grid_element"""

    def __init__(self):
        GridElement.__init__(self, True, ' ')


class TurnstileArm(GridElement):
    """An turnstilearm is a movable grid_element"""

    def __init__(self):
        GridElement.__init__(self, True, '°')


class TurnstileBody(GridElement):
    """A turnstilebody isn't movable"""

    def __init__(self):
        GridElement.__init__(self, False, '%')
