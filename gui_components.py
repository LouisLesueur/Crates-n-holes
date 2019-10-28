import os
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QApplication, QLabel, QListWidget, QWidget, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from game import Game


class Moves(QWidget):

    player = 1
    click = pyqtSignal(str)

    def __init__(self):

        super().__init__()
        self.initUI()

    def initUI(self):

        self.images = {'1': 'img/char1.png', '2': 'img/char2.png',
                       '3': 'img/char3.png', '4': 'img/char4.png'}

        layout = QGridLayout()

        self.up_btn = QPushButton('^')
        self.down_btn = QPushButton('v')
        self.right_btn = QPushButton('>')
        self.left_btn = QPushButton('<')

        self.player_btn = QPushButton(QIcon(self.images[str(self.player)]), "")

        self.up_btn.clicked.connect(self.get_order)
        self.down_btn.clicked.connect(self.get_order)
        self.right_btn.clicked.connect(self.get_order)
        self.left_btn.clicked.connect(self.get_order)
        self.player_btn.clicked.connect(self.change_player)

        layout.addWidget(self.up_btn, 1, 2)
        layout.addWidget(self.player_btn, 2, 2)
        layout.addWidget(self.down_btn, 3, 2)
        layout.addWidget(self.right_btn, 2, 3)
        layout.addWidget(self.left_btn, 2, 1)

        self.setLayout(layout)

    def get_order(self):
        sender = self.sender()
        self.click.emit(sender.text())

    def change_player(self):
        if (self.player+1) % 4 == 0:
            self.player = 4
        else:
            self.player = (self.player+1) % 4
        self.player_btn.setIcon(QIcon(self.images[str(self.player)]))
        self.click.emit(str(self.player))

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Q:
            self.click.emit('<')
        if e.key() == Qt.Key_D:
            self.click.emit('>')
        if e.key() == Qt.Key_S:
            self.click.emit('v')
        if e.key() == Qt.Key_Z:
            self.click.emit('^')
        if e.key() == Qt.Key_E:
            self.change_player()


class Grid_GUI(QWidget):

    victory = pyqtSignal()
    lose = pyqtSignal()

    def __init__(self, level: str):
        super().__init__()
        self.game = Game(level)
        self.images = {'#': 'img/wall.png', ' ': 'img/empty.png',
                       'o': 'img/hole.png', 'O': 'img/deep_hole.png',
                       '@': 'img/door.png', '*': 'img/crate.png',
                       '°': 'img/turnstile_block.png',
                       '%': 'img/turnstile_axis.png',
                       '1': 'img/char1.png', '2': 'img/char2.png',
                       '3': 'img/char3.png', '4': 'img/char4.png'}

        self.n_lig, self.n_col = self.game.get_dimensions()

        self.elements = [[0]*self.n_col for _ in range(self.n_lig)]
        self.layout = QGridLayout()
        for i in range(1, self.n_lig+1):
            for j in range(1, self.n_col+1):
                label = QLabel()
                label.setPixmap(QPixmap(self.images[self.game[i-1, j-1]]))
                self.elements[i-1][j-1] = label
                self.layout.addWidget(label, i, j)
        self.setLayout(self.layout)

    def move_player(self, orders: str):
        """
        To move
        """
        self.game.exec_order(orders)
        if self.game.state() == 1:
            self.victory.emit()

        elif self.game.state() == -1:
            self.lose.emit()


    def refresh(self):
        for i in range(1, self.n_lig+1):
            for j in range(1, self.n_col+1):
                self.elements[i-1][j-1].setPixmap(QPixmap(self.images[self.game[i-1, j-1]]))
