from PyQt5 import QtWidgets, QtCore

from calc_acoustic_ch.api.api import Field


class MyLabel(QtWidgets.QLabel, Field):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.setObjectName(name)
        self.setMinimumSize(QtCore.QSize(259, 43))

    def set_text(self, text):
        self.setText(text)
