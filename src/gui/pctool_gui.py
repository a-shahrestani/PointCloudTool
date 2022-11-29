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

import os
from pathlib import Path

import laspy
import pandas as pd
from laspy import LaspyException
from plyfile import PlyData

WINDOW_SIZE = 500
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40


class PCTool:
    pass


class PCToolWindow(QMainWindow):
    def __init__(self):
        super(PCToolWindow, self).__init__()
        self.setWindowTitle("Point Cloud Tool")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)



def main():
    pctoolApp = QApplication([])
    pctoolWindow = PCToolWindow()
    pctoolWindow.show()
    sys.exit(pctoolApp.exec())


if __name__ == '__main__':
    pass
