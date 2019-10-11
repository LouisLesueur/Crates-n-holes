from grid import Grid
from grid_element import Door, Wall, Hole, Crate, Character, EmptySquare


def move_player(main_grid: Grid, player_id: int,
                direction_h: int, direction_v: int):
    """The function which computes all moves"""
    if player_id >= len(main_grid.players):
        raise Exception("There are only 4 players !")
    elif main_grid.players[player_id-1] == (-1, -1):
        return "not a current player !"
    else:
        pos_h = main_grid.players[player_id-1][0]
        pos_v = main_grid.players[player_id-1][1]

        message = ""

        target = main_grid[pos_h+direction_h, pos_v+direction_v]

        if isinstance(target, Door):
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

            elif isinstance(target, EmptySquare):
                main_grid.swap([pos_h, pos_v],
                               [pos_h+direction_h, pos_v+direction_v])
                main_grid.change_player(player_id,
                                        pos_h+direction_h, pos_v+direction_v)
                return "Keep moving !"

            elif isinstance(target, Character):
                return "Hello my friend !"

            elif (isinstance(target, Crate) and
                    not(isinstance(beyond_target, Wall)) and
                    not(isinstance(beyond_target, Crate)) and
                    not(isinstance(beyond_target, Character))):
                if isinstance(beyond_target, EmptySquare):
                    main_grid.swap([pos_h+direction_h,
                                    pos_v+direction_v],
                                   [pos_h+2*direction_h,
                                    pos_v+2*direction_v])
                    main_grid.swap([pos_h, pos_v],
                                   [pos_h+direction_h, pos_v+direction_v])
                    message = "You're so strong !"
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
                return message
