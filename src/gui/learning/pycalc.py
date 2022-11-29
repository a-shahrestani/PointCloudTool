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

ERROR_MSG = "ERROR"

WINDOW_SIZE = 235
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40


class PyCalcWindow(QMainWindow):
    def __init__(self):
        super(PyCalcWindow, self).__init__()
        self.setWindowTitle("PyQt Calculator")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self.setLayout(self.generalLayout)
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttonMap = {}
        buttonsLayout = QGridLayout()
        keyBoard = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", "00", ".", "+", "="],
        ]
        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(key)
                self.buttonMap[key].setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                buttonsLayout.addWidget(self.buttonMap[key], row, col)
        self.generalLayout.addLayout(buttonsLayout)

    def _setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def _clearDisplay(self):
        self.display.setText('')

    def _displayText(self):
        return self.display.text()


class PyCalc:
    def __init__(self, model, view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()

    def _calculateResult(self):
        result = self._evaluate(expression=self._view._displayText())
        self._view._setDisplayText(result)

    def _buildExpression(self, subExpression):
        if self._view._displayText() == ERROR_MSG:
            self._view._clearDisplay()
        else:
            expression = self._view._displayText() + subExpression
            self._view._setDisplayText(expression)

    def _connectSignalsAndSlots(self):
        for keySymbol, button, in self._view.buttonMap.items():
            if keySymbol not in {'=', 'C'}:
                button.clicked.connect(partial(self._buildExpression, keySymbol))
        self._view.buttonMap["="].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttonMap["C"].clicked.connect(self._view._clearDisplay)


def evaluateExpression(expression):
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
    return result


def main():
    pycalcApp = QApplication([])
    pycalcWindow = PyCalcWindow()
    pycalcWindow.show()
    PyCalc(model=evaluateExpression, view=pycalcWindow)
    sys.exit(pycalcApp.exec())


if __name__ == '__main__':
    main()
