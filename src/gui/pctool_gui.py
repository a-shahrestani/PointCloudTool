import sys
from functools import partial

import laspy
import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget, QLabel, QFileDialog,
)
import os
from plyfile import PlyData

from src.LAS_tools import _las_to_df
from src.PLY_tools import _ply_to_df
from src.manipulation_tools import _df_to_las_conversion

WINDOW_SIZE = 300
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40

commands = {}


class PCToolWindow(QMainWindow):
    def __init__(self):
        super(PCToolWindow, self).__init__()
        self.setWindowTitle("Point Cloud Tool")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.generalLayout = QVBoxLayout()
        self.data = None
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self.setLayout(self.generalLayout)
        self.open_btn = QPushButton("Open File")
        self.save_csv_btn = QPushButton("Save CSV File")
        self.save_ply_btn = QPushButton("Save PLY File")
        self.save_las_btn = QPushButton("Save LAS File")
        self.save_laz_btn = QPushButton("Save LAZ File")
        self.reduce_density_btn = QPushButton("Reduce Density")
        self.asprs_standard_btn = QPushButton("ASPRS Standardization")
        self.save_btns = [self.open_btn, self.save_csv_btn, self.save_ply_btn, self.save_las_btn, self.save_laz_btn]
        self.le = QLabel("Select a file")

        self.generalLayout.addWidget(self.le)
        for btn in self.save_btns:
            self.generalLayout.addWidget(btn)

        self._connectSignalsAndSlots()

    def _connectSignalsAndSlots(self):
        self.open_btn.clicked.connect(self.get_file)
        self.save_csv_btn.clicked.connect(partial(self.save_file,'.csv'))
        self.save_las_btn.clicked.connect(partial(self.save_file,'.las'))
        self.save_laz_btn.clicked.connect(partial(self.save_file,'.laz'))
        self.save_ply_btn.clicked.connect(partial(self.save_file,'.ply'))

    def set_label(self,text):
        self.le.setText(text)
    def get_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "(*.csv *.las *.ply *.laz)")[0]
        self.set_label(fname)
        filename, file_extension = os.path.splitext(fname)
        if file_extension == '.laz' or file_extension == '.las':
            las_file = laspy.read(fname)
            self.data = _las_to_df(las_file)
        elif file_extension == '.ply':
            ply_data = PlyData.read(fname)
            self.data = _ply_to_df(ply_data)
        elif file_extension == '.csv':
            self.data = pd.read_csv(fname)


    def save_file(self, extension):
        fname = QFileDialog.getSaveFileName(self, 'Save file')[0]
        if extension == '.csv':
            self.data.to_csv(fname+ extension, index= False)
        elif extension == '.las':
            _df_to_las_conversion(df=self.data,address=fname+extension, compress= False)
        elif extension == '.laz':
            _df_to_las_conversion(df=self.data, address=fname + extension, compress=True)
        elif extension == '.ply':
            pass
        self.set_label(f'saved file in {fname + extension}')




def main():
    pctoolApp = QApplication([])
    pctoolWindow = PCToolWindow()
    pctoolWindow.show()
    sys.exit(pctoolApp.exec())


if __name__ == '__main__':
    main()
