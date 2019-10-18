"""
Functions for graphics of the game
"""

import os


class Graphics:
    """Class to manage all graphical elements"""

    def select(self):
        """A very simple selection menu
           Output: The absolute path to the level"""
        self.clear()
        print("*-------------------------------*")
        print("|           TDLOG TP1           |")
        print("|        Louis Lesueur          |")
        print("*-------------------------------*")
        print("")
        print("Chose your level: ")

        levels = os.listdir('levels')
        for i in range(len(levels)):
            print(str(i)+" - "+str(levels[i]))

        print("")

        choice = input("Which one ? (type a number, 0 by default): ")

        try:
            int(choice)
        except ValueError:
            print("That's not an int! 0 selected.")
            return "levels/"+levels[0]

        return "levels/"+levels[int(choice)]

    def clear(self):
        """To clear the screen between two moves"""
        # windows
        if os.name == 'nt':
            _ = os.system('cls')

        # unix based systems
        else:
            _ = os.system('clear')
