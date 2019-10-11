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
        return self._win

    @win.setter
    def win(self, nw):
        self._win = nw


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
