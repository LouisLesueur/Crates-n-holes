from grid import Grid
from grid_element import Door, Wall, DeepHole
from grid_element import Hole, Crate, Character, EmptySquare
from grid_element import TurnstileArm, TurnstileBody


def move_player(main_grid: Grid, player_id: int,
                direction_h: int, direction_v: int):
    """The function which computes all moves
       Inputs:
           -- The grid
           -- The id of the player (1,2,3 or 4)
           -- The direction of the movement
       Output:
           -- A message for the player"""
    if player_id >= len(main_grid.players):
        raise Exception("There are only 4 players !")
    elif main_grid.players[player_id-1] == (-1, -1):
        return "not a current player !"
    else:
        pos_h = main_grid.players[player_id-1][0]
        pos_v = main_grid.players[player_id-1][1]

        message = ""

        # To alleviate the code
        target = main_grid[pos_h+direction_h, pos_v+direction_v]

        if isinstance(target, Wall):
            return "Ouch !"

        elif isinstance(target, Door):
            main_grid[pos_h, pos_v].win = 1
            return "GG you must be some kind of engineer !"

        elif not(isinstance(target, Wall)) and not(isinstance(target, Door)):
            # if the player moves a crate, the element behind must be checked
            beyond_target = main_grid[pos_h+2*direction_h,
                                      pos_v+2*direction_v]
            if isinstance(target, Hole):
                main_grid[pos_h, pos_v].win = -1
                main_grid.change_player(player_id, -1, -1)
                main_grid[pos_h, pos_v] = EmptySquare()
                return "Noooooooooooooooo...."

            elif isinstance(target, DeepHole):
                main_grid[pos_h, pos_v].win = -1
                main_grid.change_player(player_id, -1, -1)
                main_grid[pos_h, pos_v] = Hole()
                return "Noooooooooooooooo...."

            elif isinstance(target, EmptySquare):
                main_grid.swap([pos_h, pos_v],
                               [pos_h+direction_h, pos_v+direction_v])
                main_grid.change_player(player_id,
                                        pos_h+direction_h, pos_v+direction_v)
                return "Keep moving !"

            elif isinstance(target, Character):
                return "Hello my friend !"

            elif isinstance(target, TurnstileArm):
                body_h, body_v = find_turnstile_body(main_grid,
                                                     pos_h+direction_h,
                                                     pos_v+direction_v)
                # to determine the sens of the rotation
                if body_v-pos_v == 1:
                    if body_h-pos_h == 1:
                        sens = direction_h-direction_v
                    else:
                        sens = direction_h+direction_v
                elif body_v-pos_v == -1:
                    if body_h-pos_h == 1:
                        sens = -direction_h-direction_v
                    else:
                        sens = -direction_h+direction_v
                else:
                    raise Exception("You are too far from the turnstile !")

                rotate_turnstile(main_grid, body_h, body_v, sens)
                if not(isinstance(beyond_target, TurnstileBody)):
                    main_grid.change_player(player_id,
                                            pos_h+2*direction_h,
                                            pos_v+2*direction_v)
                    return "Please don't throw up"
                else:
                    return "Ouch !"

            elif isinstance(target, TurnstileBody):
                return "OMG This thing can rotate !"

            elif isinstance(target, Crate):
                if isinstance(beyond_target, EmptySquare):
                    main_grid.swap([pos_h+direction_h,
                                    pos_v+direction_v],
                                   [pos_h+2*direction_h,
                                    pos_v+2*direction_v])
                    main_grid.swap([pos_h, pos_v],
                                   [pos_h+direction_h, pos_v+direction_v])
                    message = "You're so strong !"
                    main_grid.change_player(player_id,
                                            pos_h+direction_h,
                                            pos_v+direction_v)
                elif isinstance(beyond_target, Hole):
                    main_grid.swap([pos_h, pos_v],
                                   [pos_h+direction_h, pos_v+direction_v])
                    main_grid[pos_h, pos_v] = EmptySquare()
                    main_grid[pos_h+2*direction_h,
                              pos_v+2*direction_v] = EmptySquare()
                    message = "A good thing done !"
                    main_grid.change_player(player_id,
                                            pos_h+direction_h,
                                            pos_v+direction_v)
                elif isinstance(beyond_target, Crate):
                    message = "So heavy !"
                elif isinstance(beyond_target, DeepHole):
                    main_grid.swap([pos_h, pos_v],
                                   [pos_h+direction_h, pos_v+direction_v])
                    main_grid[pos_h, pos_v] = EmptySquare()
                    main_grid[pos_h+2*direction_h,
                              pos_v+2*direction_v] = Hole()
                    message = "So deep..."
                    main_grid.change_player(player_id,
                                            pos_h+direction_h,
                                            pos_v+direction_v)
                elif isinstance(beyond_target, TurnstileArm):
                    message = "What are you trying to do ?"
                elif isinstance(beyond_target, TurnstileBody):
                    message = "What a strange idea..."
                elif isinstance(beyond_target, Wall):
                    message = "You can't do that you know ?"
                elif isinstance(beyond_target, Character):
                    message = "Are trying to kill him ?"
                return message


def find_turnstile_body(main_grid, arm_h, arm_v):
    """For a given arm, this function return the coords of the corresponding body"""
    count = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if isinstance(main_grid[arm_h+i, arm_v+j], TurnstileBody):
                pos_h = arm_h+i
                pos_v = arm_v+j
                count += 1
    if count == 0:
        raise Exception("One arm is alone !")
    elif count > 1:
        raise Exception("Too many bodies !")
    else:
        return [pos_h, pos_v]


def rotate_turnstile(main_grid, body_h: int, body_v: int, sens: int):
    """To rotate a turnstile: sens must be 1 for trigo"""
    if sens not in [-1, 1]:
        raise Exception("Sens must be 1 or -1, not "+str(sens))
    else:
        # There is probably a simpler way to do this
        to_be_rotated = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (i, j) != (0, 0):
                    pos_h = body_h+i
                    pos_v = body_v+j
                    new_h = body_h-sens*j
                    new_v = body_v+sens*i
                    to_be_rotated.append([main_grid[pos_h, pos_v],
                                          [new_h, new_v]])
        for square in to_be_rotated:
            main_grid[square[1][0], square[1][1]] = square[0]
