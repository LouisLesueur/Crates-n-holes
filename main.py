import os
from PyQt5.QtWidgets import QApplication
from gui_windows import PlayWindow, SelectionWindow




if __name__ == '__main__':
    app = QApplication([])
    
    select = SelectionWindow()
    select.show()
    
    playwindow = PlayWindow()

    select.click.connect(playwindow.load_grid)
    select.click.connect(select.close)
    
    app.exec_()
