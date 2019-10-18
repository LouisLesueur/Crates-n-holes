"""
Here are the functions that operate on the grid to move elements
"""

from grid import Grid
from grid_element import Door, Wall
from grid_element import Hole, Crate, Character, EmptySquare
from grid_element import TurnstileArm, TurnstileBody
from graphics import Graphics


class Game:
    """A class to bind all game elements together"""

    def __init__(self):
        """Initialize the grid
           Input: absolute path to the level
           Output: The grid"""
        self.graphics = Graphics()
        self.grid = Grid(self.graphics.select())

    def move_player(self, player_id: int,
                    direction_h: int, direction_v: int):
        """The function which computes all moves
           Inputs:
               -- The grid
               -- The id of the player (1,2,3 or 4)
               -- The direction of the movement
           Output:
               -- A message for the player"""
        if player_id >= len(self.grid.players_to_coords):
            raise Exception("There are only 4 players !")
        if self.grid.players_to_coords[player_id-1] == (-1, -1):
            return "not a current player !"

        pos_h = self.grid.players_to_coords[player_id-1][0]
        pos_v = self.grid.players_to_coords[player_id-1][1]
        new_h = pos_h+direction_h
        new_v = pos_v+direction_v
        far_h = pos_h+2*direction_h
        far_v = pos_v+2*direction_v

        # To alleviate the code
        target = self.grid[new_h, new_v]

        if isinstance(target, Wall):
            return "Ouch !"

        if isinstance(target, Door):
            self.grid.you_win()
            return "GG you must be some kind of engineer !"

        # if the player moves a crate, what's behind must be checked
        beyond_target = self.grid[far_h, far_v]
        if isinstance(target, Hole):
            self.grid[pos_h, pos_v].win = -1
            self.grid.change_player(player_id, -1, -1)
            self.grid[pos_h, pos_v] = EmptySquare()
            if target.size == 1:
                self.grid[new_h, new_v] = EmptySquare()
            elif target.size == 2:
                self.grid[new_h, new_v].fill()
            return "Noooooooooooooooo...."

        if isinstance(target, EmptySquare):
            self.grid.swap([pos_h, pos_v], [new_h, new_v])
            self.grid.change_player(player_id, new_h, new_v)

        elif isinstance(target, Character):
            return "Hello my friend !"

        elif isinstance(target, TurnstileArm):
            body_h, body_v = target.find_turnstile_body(self.grid,
                                                        new_h, new_v)
            sens = self.get_rotation(pos_h, pos_v, body_h, body_v,
                                     direction_h, direction_v)
            if not isinstance(beyond_target, TurnstileBody):
                self.rotate_turnstile(body_h, body_v, sens)
                self.grid.change_player(player_id, far_h, far_v)
                return "Please don't throw up"
            return "Ouch !"

        elif isinstance(target, TurnstileBody):
            return "OMG This thing can rotate !"

        elif isinstance(target, Crate):
            return self.move_crate(player_id, [pos_h, pos_v],
                                   [new_h, new_v], [far_h, far_v])
        else:
            raise Exception("You are trying to do something strange !")

    def move_crate(self, player_id, pos, new, far):
        """When one character is behind a crate"""
        pos_h, pos_v = pos
        new_h, new_v = new
        far_h, far_v = far
        beyond_target = self.grid[far_h, far_v]
        message = ""
        if isinstance(beyond_target, EmptySquare):
            self.grid.big_swap([pos_h, pos_v], [new_h, new_v],
                               [far_h, far_v])
            message = "You're so strong !"
            self.grid.change_player(player_id, new_h, new_v)
        elif isinstance(beyond_target, Hole):
            self.grid.swap([pos_h, pos_v], [new_h, new_v])
            self.grid[pos_h, pos_v] = EmptySquare()
            if beyond_target.size == 1:
                self.grid[far_h, far_v] = EmptySquare()
                message = "A good thing done !"
                self.grid.change_player(player_id, new_h, new_v)
            else:
                self.grid[far_h, far_v].fill()
                message = "So deep..."
                self.grid.change_player(player_id, new_h, new_v)
        elif isinstance(beyond_target, Crate):
            message = "So heavy !"
        elif isinstance(beyond_target, TurnstileArm):
            message = "What are you trying to do ?"
        elif isinstance(beyond_target, TurnstileBody):
            message = "What a strange idea..."
        elif isinstance(beyond_target, Wall):
            message = "You can't do that you know ?"
        elif isinstance(beyond_target, Character):
            message = "Are trying to kill him ?"
        return message

    def get_rotation(self, pos_h: int, pos_v: int, body_h: int, body_v: int,
                     direction_h: int, direction_v: int):
        """To determine the sens of rotation of a turnstile"""
        if body_v-pos_v == 1:
            if body_h-pos_h == 1:
                return direction_h-direction_v
            return direction_h+direction_v
        if body_h-pos_h == 1:
            return -direction_h-direction_v
        return -direction_h+direction_v

    def rotate_turnstile(self, body_h: int, body_v: int, sens: int):
        """To rotate a turnstile: sens must be 1 for trigo"""
        if sens not in [-1, 1]:
            raise Exception("Sens must be 1 or -1, not "+str(sens))
        # There is probably a simpler way to do this
        to_be_rotated = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (i, j) != (0, 0):
                    pos_h = body_h+i
                    pos_v = body_v+j
                    new_h = body_h-sens*j
                    new_v = body_v+sens*i
                    to_be_rotated.append(
                        [self.grid[pos_h, pos_v], [new_h, new_v]])
        for square in to_be_rotated:
            self.grid[square[1][0], square[1][1]] = square[0]

    def play(self):
        """Function which displays and updates the grid"""
        self.graphics.clear()
        print(self.grid)
        message = "Good luck !"
        player_symbols = ['1', '2', '3', '4']
        order_symbols = {'v': (1, 0), '^': (-1, 0), '>': (0, 1), '<': (0, -1),
                         's': (1, 0), 'z': (-1, 0), 'd': (0, 1), 'q': (0, -1)}
        current_player = 1
        while self.grid.win == 0:
            if message is not None:
                print(message)
            orders = input(
                "Move with <>v^zqsd (curent player "+str(current_player)+"): ")
            for order in orders:
                if order in player_symbols:
                    if self.grid.players_to_coords[int(order)-1] != (-1, -1):
                        current_player = int(order)
                elif order in order_symbols:
                    direction_h = order_symbols[order][0]
                    direction_v = order_symbols[order][1]
                    message = self.move_player(current_player,
                                               direction_h, direction_v)
                else:
                    print(order+' is not an acceptable character !')
            self.graphics.clear()
            print(self.grid)

            # Checking if it's a win
            if self.grid.win == 1:
                print("You win !")
            elif self.grid.win == -1:
                print("You lose !")
