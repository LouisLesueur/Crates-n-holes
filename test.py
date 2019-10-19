"""
To makes tests
"""

import pytest
from game import Game


GAME = Game(True, False)


def test_moves():
    """
    Testing basic moves
    """
    # on emptysquares
    assert GAME.move_player(1, [0, 1]) == ""
    assert GAME.move_player(1, [0, -1]) == ""
    assert GAME.move_player(1, [1, 0]) == ""
    assert GAME.move_player(1, [-1, 0]) == ""

    # on other character
    GAME.move_player(1, [1, 0])
    assert GAME.move_player(1, [1, 0]) == "Hello my friend !"

    # on a wall
    assert GAME.move_player(2, [1, 0]) == "Ouch !"


def test_win():
    """
    Testing win
    """
    GAME.exec_order('ddddddddd')
    assert GAME.move_player(
        1, [0, 1]) == "GG you must be some kind of engineer !"


def test_change_player():
    """
    Change of players
    """

    # check if the change of players works
    GAME.exec_order('2')
    assert GAME.current_player == 2

    # it is impossible to move a dead/not current player
    assert GAME.move_player(4, [0, 1]) == "not a current player !"


GAME_CRATES = Game(True, False)


def test_move_crate():
    """
    Tests with crates
    """

    # into a wall
    GAME_CRATES.move_player(2, [-1, 0])
    GAME_CRATES.move_player(2, [0, 1])
    assert GAME_CRATES.move_player(2, [1, 0]) == "You can't do that you know ?"

    # into a player
    GAME_CRATES.move_player(2, [0, -1])
    GAME_CRATES.move_player(2, [1, 0])
    GAME_CRATES.exec_order('1dsds')
    assert GAME_CRATES.move_player(2, [0, 1]) == "Are you trying to kill him ?"

    # into a big hole
    assert GAME_CRATES.move_player(3, [0, -1]) == "So deep..."

    # into a turnstilebody
    GAME_CRATES.exec_order('1zz')
    assert GAME_CRATES.move_player(1, [0, 1]) == "What a strange idea..."

    # into a turnstilearm
    GAME_CRATES.exec_order('1sdzqz')
    assert GAME_CRATES.move_player(1, [0, 1]) == "What are you trying to do ?"

    # pushing it
    assert GAME_CRATES.move_player(2, [0, 1]) == "You're so strong !"

    # into a hole
    assert GAME_CRATES.move_player(2, [0, 1]) == "A good thing done !"


def test_suicide():
    """
    To check if players die
    """

    # killing 3
    assert GAME_CRATES.move_player(3, [0, -1]) == "Noooooooooooooooo...."


GAME_TS = Game(True, False)


def test_turnstiles():
    """
    To test interractions with turnstiles
    """

    # rotation <ith a crate inside
    GAME_TS.exec_order('3zzzqqq')
    assert GAME_TS.move_player(3, [0, -1]) == "Please don't throw up"

    # going into an arm
    GAME_TS.exec_order('3qs')
    assert GAME_TS.move_player(3, [0, 1]) == "Ouch !"

    # going into a body
    GAME_TS.exec_order('sdd')
    assert GAME_TS.move_player(3, [-1, 0]) == "OMG This thing can rotate !"
