from PyQt5 import QtWidgets, QtCore

from calc_acoustic_ch.api.api import ProgramFunction


class MainButton(QtWidgets.QPushButton, ProgramFunction):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.setObjectName(name)
        self.setMinimumSize(QtCore.QSize(200, 50))

    def disable(self):
        self.setDisabled(True)

    def enable(self):
        self.setDisabled(False)
