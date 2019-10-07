class GridElement:
    """Base class for grid_elements"""
    def __init__(self, posh: int, posv: int, movable: bool, symbol: str):
        self.posh = posh
        self.posv = posv
        self.movable = movable
        self._symbol = symbol

    def move(self, direction_h: int, direction_v: int):
        """Move a grid eleemnt
        Input: direction_h = +-1 to move forward/backward horizontally
               direction_v = +-1 to """
        if abs(direction_h)+abs(direction_v) > 1:
            raise Exception("Can only move one case by one")
        if not self.movable:
            raise Exception("Trying to move a static object !")
        self.posh += direction_h
        self.posv += direction_v

    @property
    def symbol(self):
        return self._symbol


class Character(GridElement):
    """A charcter is a movable grid_element"""
    def __init__(self, posh: int, posv: int):
        GridElement.__init__(self, posh, posv, True, '1')


class Wall(GridElement):
    """ A wall is a not movable grid_element """
    def __init__(self, posh: int, posv: int):
        GridElement.__init__(self, posh, posv, False, '#')


class Hole(GridElement):
    """A hole is a not movable grid_element"""
    def __init__(self, posh: int, posv: int):
        GridElement.__init__(self, posh, posv, False, 'o')


class Door(GridElement):
    """A door is a not movable grid_element"""
    def __init__(self, posh: int, posv: int):
        GridElement.__init__(self, posh, posv, False, '@')


class Crate(GridElement):
    """A crate is a movable grid_element"""
    def __init__(self, posh: int, posv: int):
        GridElement.__init__(self, posh, posv, True, '*')


class EmptyCase(GridElement):
    """An emptycase is a movable grid_element"""
    def __init__(self, posh: int, posv: int):
        GridElement.__init__(self, posh, posv, True, ' ')
