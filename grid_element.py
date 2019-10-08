class GridElement:
    """Base class for grid_elements"""
    def __init__(self, pos_h: int, pos_v: int, is_movable: bool, symbol: str):

        if isinstance(pos_h, int):
            self.pos_h = pos_h
        else:
            raise Exception("pos_h must be an integer !")

        if isinstance(pos_v, int):
            self.pos_v = pos_v
        else:
            raise Exception("pos_v must be an integer !")

        self.is_movable = is_movable
        self.symbol = symbol

    def move(self, direction_h: int, direction_v: int):
        """Move a grid eleemnt
        Input: direction_h = +-1 to move forward/backward horizontally
               direction_v = +-1 to """
        if not(isinstance(direction_h, int)):
            raise Exception("direction_h must be an integer !")
        if not(isinstance(direction_v, int)):
            raise Exception("direction_v must be an integer !")
        if abs(direction_h)+abs(direction_v) > 1:
            raise Exception("Can only move one case by one")
        if not self.is_movable:
            raise Exception("Trying to move a static object !")
        self.pos_h += direction_h
        self.pos_v += direction_v

    def __str__(self):
        return self.symbol


class Character(GridElement):
    """A charcter is a movable grid_element"""
    def __init__(self, pos_h: int, pos_v: int):
        GridElement.__init__(self, pos_h, pos_v, True, '1')


class Wall(GridElement):
    """ A wall is a not movable grid_element """
    def __init__(self, pos_h: int, pos_v: int):
        GridElement.__init__(self, pos_h, pos_v, False, '#')


class Hole(GridElement):
    """A hole is a not movable grid_element"""
    def __init__(self, pos_h: int, pos_v: int):
        GridElement.__init__(self, pos_h, pos_v, False, 'o')


class Door(GridElement):
    """A door is a not movable grid_element"""
    def __init__(self, pos_h: int, pos_v: int):
        GridElement.__init__(self, pos_h, pos_v, False, '@')


class Crate(GridElement):
    """A crate is a movable grid_element"""
    def __init__(self, pos_h: int, pos_v: int):
        GridElement.__init__(self, pos_h, pos_v, True, '*')


class EmptySquare(GridElement):
    """An emptysquare is a movable grid_element"""
    def __init__(self, pos_h: int, pos_v: int):
        GridElement.__init__(self, pos_h, pos_v, True, ' ')
