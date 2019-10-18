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

    def move_player(self, player_id: int, direction) -> str:
        """The function which computes all moves
           Inputs:
               -- The grid
               -- The id of the player (1,2,3 or 4)
               -- The direction of the movement
           Output:
               -- A message for the player"""

        message = ""

        if player_id >= len(self.grid.players_to_coords):
            raise Exception("There are only 4 players !")
        if self.grid.players_to_coords[player_id-1] == (-1, -1):
            return "not a current player !"

        pos = self.grid.players_to_coords[player_id-1]
        new = [pos[0]+direction[0], pos[1]+direction[1]]
        far = [pos[0]+2*direction[0], pos[1]+2*direction[1]]

        # To alleviate the code
        target = self.grid[new[0], new[1]]

        if isinstance(target, Wall):
            return "Ouch !"

        if isinstance(target, Door):
            self.grid.you_win()
            return "GG you must be some kind of engineer !"

        # if the player moves a crate, what's behind must be checked
        if isinstance(target, Hole):
            return self.move_hole(target, player_id, pos, new)

        if isinstance(target, EmptySquare):
            self.grid.swap(pos, new)
            self.grid.change_player(player_id, new)

        elif isinstance(target, Character):
            message = "Hello my friend !"

        elif isinstance(target, TurnstileArm):
            message = self.move_turnstile_arm(target, pos,
                                              direction, player_id)
        elif isinstance(target, TurnstileBody):
            message = "OMG This thing can rotate !"

        elif isinstance(target, Crate):
            message = self.move_crate(player_id, pos, new, far)
        else:
            raise Exception("You are trying to do something strange !")
        return message

    def move_hole(self, target, player_id, pos, new) -> str:
        """To manage interactions with a hole"""
        self.grid[pos[0], pos[1]].win = -1
        self.grid.change_player(player_id, [-1, -1])
        self.grid[pos[0], pos[1]] = EmptySquare()
        if target.size == 1:
            self.grid[new[0], new[1]] = EmptySquare()
        elif target.size == 2:
            self.grid[new[0], new[1]].fill()
        return "Noooooooooooooooo...."

    def move_turnstile_arm(self, target, pos, direction, player_id) -> str:
        """To manage the interaction with a turnstile arm"""
        new = [pos[0]+direction[0], pos[1]+direction[1]]
        far = [pos[0]+2*direction[0], pos[1]+2*direction[1]]
        beyond_target = self.grid[far[0], far[1]]
        body = target.find_turnstile_body(self.grid, new)
        sens = self.get_rotation(pos, body, direction)
        if not isinstance(beyond_target, TurnstileBody):
            self.rotate_turnstile(body, sens)
            self.grid.change_player(player_id, far)
            return "Please don't throw up"
        return "Ouch !"

    def move_crate(self, player_id, pos, new, far) -> str:
        """When one character is behind a crate"""
        beyond_target = self.grid[far[0], far[1]]
        message = ""
        if isinstance(beyond_target, EmptySquare):
            self.grid.big_swap(pos, new, far)
            message = "You're so strong !"
            self.grid.change_player(player_id, new)
        elif isinstance(beyond_target, Hole):
            self.grid.swap(pos, new)
            self.grid[pos[0], pos[1]] = EmptySquare()
            if beyond_target.size == 1:
                self.grid[far[0], far[1]] = EmptySquare()
                message = "A good thing done !"
                self.grid.change_player(player_id, new)
            else:
                self.grid[far[0], far[1]].fill()
                message = "So deep..."
                self.grid.change_player(player_id, new)
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

    def get_rotation(self, pos, body, direction) -> int:
        """To determine the sens of rotation of a turnstile"""
        if body[1]-pos[1] == 1:
            if body[0]-pos[0] == 1:
                return direction[0]-direction[1]
            return direction[0]+direction[1]
        if body[0]-pos[0] == 1:
            return -direction[0]-direction[1]
        return -direction[0]+direction[1]

    def rotate_turnstile(self, body, sens: int):
        """To rotate a turnstile: sens must be 1 for trigo"""
        if sens not in [-1, 1]:
            raise Exception("Sens must be 1 or -1, not "+str(sens))
        # There is probably a simpler way to do this
        to_be_rotated = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (i, j) != (0, 0):
                    pos = [body[0]+i, body[1]+j]
                    new = [body[0]-sens*j, body[1]+sens*i]
                    to_be_rotated.append(
                        [self.grid[pos[0], pos[1]], [new[0], new[1]]])
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
                    direction = order_symbols[order]
                    message = self.move_player(current_player, direction)
                else:
                    print(order+' is not an acceptable character !')
            self.graphics.clear()
            print(self.grid)

            # Checking if it's a win
            if self.grid.win == 1:
                print("You win !")
            elif self.grid.win == -1:
                print("You lose !")
