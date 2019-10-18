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
    """A charcter is a movable grid_element, which represents the players.
       They can move on the emptysquares and push crates into holes"""

    def __init__(self, symbol: str):
        self._win = 0
        allowed_symbols = {'1', '2', '3', '4'}
        if symbol in allowed_symbols:
            GridElement.__init__(self, True, symbol)
        else:
            raise Exception("Only 1, 2, 3 and 4 can be a player")


class Wall(GridElement):
    """ A wall is a not movable grid_element """

    def __init__(self):
        GridElement.__init__(self, False, '#')


class Hole(GridElement):
    """A hole is a not movable grid_element, it has a size and
       charcters can fall in it"""

    def __init__(self, deep: int):
        if deep == 1:
            GridElement.__init__(self, False, 'o')
            self._size = 1
        elif deep == 2:
            GridElement.__init__(self, False, 'O')
            self._size = 2
        else:
            raise Exception("A hole's size can only be 1 or 2")

    def fill(self):
        """To fill a hole"""
        if self._size > 1:
            GridElement.__init__(self, False, 'o')
            self._size -= 1
        else:
            raise Exception("Can't be more filled")

    @property
    def size(self):
        """To get a hole's size"""
        return self._size


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

    def find_turnstile_body(self, main_grid, arm_h, arm_v):
        """For a given arm, this function return the coords of the
           corresponding body"""
        count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if isinstance(main_grid[arm_h+i, arm_v+j], TurnstileBody):
                    pos_h = arm_h+i
                    pos_v = arm_v+j
                    count += 1
        if count == 0:
            raise Exception("One arm is alone !")
        if count > 1:
            raise Exception("Too many bodies !")
        return [pos_h, pos_v]


class TurnstileBody(GridElement):
    """A turnstilebody isn't movable"""

    def __init__(self):
        GridElement.__init__(self, False, '%')
