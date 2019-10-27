"""
Functions for graphics of the game
"""

import os


class Graphics:
    """Class to manage all graphical elements"""

    def select(self, testing: bool, soluce_testing: bool):
        """A very simple selection menu
           Output: The name of the level"""
        self.clear()
        if testing:
            return "tests.txt"
        print("*-------------------------------*")
        print("|           TDLOG TP1           |")
        if soluce_testing:
            print("| !!!! SOLUCE TESTING MODE !!!! |")
        print("|        Louis Lesueur          |")
        print("*-------------------------------*")
        print("")
        print("Chose your level: ")

        levels = os.listdir('levels')
        for i, _ in enumerate(levels):
            print(str(i)+" - "+str(levels[i]))

        print("")

        choice = input("Which one ? (type a number, 0 by default): ")

        try:
            int(choice)
        except ValueError:
            print("That's not an int! 0 selected.")
            return levels[0]
        return levels[int(choice)]

    def clear(self):
        """To clear the screen between two moves"""
        # windows
        if os.name == 'nt':
            _ = os.system('cls')

        # unix based systems
        else:
            _ = os.system('clear')
