from PyQt5 import QtWidgets, QtCore, QtGui


class HelpButton(QtWidgets.QPushButton):
    def __init__(self, parent, name):
        super().__init__(parent)
        self.setObjectName(name)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QtCore.QSize(30, 30))
        self.setMaximumSize(QtCore.QSize(30, 30))
        self.setBaseSize(QtCore.QSize(30, 30))
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))