from PyQt5.QtWidgets import QApplication
from gui_windows import PlayWindow, SelectionWindow


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    APP = QApplication([])

    SELECT = SelectionWindow()
    SELECT.show()

    PLAY = PlayWindow()

    SELECT.click.connect(PLAY.load_grid)
    SELECT.click.connect(SELECT.close)

    APP.exec_()
