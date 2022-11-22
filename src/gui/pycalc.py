import sys
from functools import partial
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

WINDOW_SIZE = 235
DISPLAY_HEIGHT = 35


class PyCalcWindow(QMainWindow):
    def __init__(self):
        super(PyCalcWindow, self).__init__()
        self.setWindowTitle("PyQt Calculator")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        self.setLayout(generalLayout)
        self._createDisplay()
        self._createButtons()

    def _createButtons(self):
        pass

    def _createDisplay(self):
        pass


def main():
    pycalcApp = QApplication([])
    pycalcWindow = PyCalcWindow()
    pycalcWindow.show()
    sys.exit(pycalcApp.exec())


if __name__ == '__main__':
    main()
