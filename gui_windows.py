"""
Module with all windows of the gui
"""

import os
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont
from gui_components import GridGUI, Moves


class SelectionWindow(QWidget):
    """
    A very simple level selection windows
    """

    click = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.resize(250, 400)
        self.setWindowTitle("Selection menu")

        levels = os.listdir('levels')
        self.layout = QVBoxLayout()

        title = QLabel("Chose your level: ")
        title.setFont(QFont('SansSerif', 20))
        self.layout.addWidget(title)
        for i, _ in enumerate(levels):
            if levels[i] != "tests.txt":
                btn = QPushButton(levels[i][:-4])
                btn.clicked.connect(self.get_order)
                self.layout.addWidget(btn)
        self.setLayout(self.layout)

        rules = QLabel("rules: move with zqsd, change player with e.")

        self.layout.addWidget(rules)

    def get_order(self):
        """
        To emit a signal with level name when one button is clicked
        """
        sender = self.sender()
        self.click.emit(sender.text()+".txt")


class PlayWindow(QWidget):
    """
    The main window of the game
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TDLog project")

    def load_grid(self, level: str):
        """
        To initialize the grid with a level path
        """
        self.moves = Moves()
        self.grid_gui = GridGUI(level)

        self.grid_gui.victory.connect(self.win_msg)
        self.grid_gui.lose.connect(self.lose_msg)

        layout = QHBoxLayout()
        layout.addWidget(self.grid_gui)
        layout.addWidget(self.moves)

        self.setLayout(layout)

        self.moves.click.connect(self.move_player)
        self.show()

    def move_player(self, orders: str):
        """
        To move the player in the grid
        Input :
        -- orders: an order in ^v><1234
        """
        self.grid_gui.move_player(orders)
        self.grid_gui.refresh()

    def win_msg(self):
        """
        A pop-up to indicate if its a win
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("You win !")
        msg.setWindowTitle("victory !")
        msg.exec()
        self.close()

    def lose_msg(self):
        """
        A pop-up to indicate if it's a lose
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("You lose !")
        msg.setWindowTitle("You lose !")
        msg.exec()
        self.close()
