import os
from game import Game
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QListWidget, QWidget, QPushButton, QGridLayout, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon, QFont
from gui_components import Grid_GUI, Moves


class SelectionWindow(QWidget):

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
        sender = self.sender()
        self.click.emit(sender.text()+".txt")


class PlayWindow(QWidget):

    def __init__(self):
        super().__init__()

    def load_grid(self, level: str):
        self.moves = Moves()
        self.grid_gui = Grid_GUI(level)

        self.grid_gui.victory.connect(self.win_msg)
        self.grid_gui.lose.connect(self.lose_msg)

        layout = QHBoxLayout()
        layout.addWidget(self.grid_gui)
        layout.addWidget(self.moves)

        self.setLayout(layout)

        self.moves.click.connect(self.move_player)
        self.show()

    def move_player(self, orders: str):
        self.grid_gui.move_player(orders)
        self.grid_gui.refresh()

    def win_msg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("You win !")
        msg.setWindowTitle("victory !")
        msg.exec()
        self.close()
    
    def lose_msg(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("You lose !")
        msg.setWindowTitle("You lose !")
        msg.exec()
        self.close()
