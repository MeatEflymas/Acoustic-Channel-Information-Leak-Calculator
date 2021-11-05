from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog

from calc_acoustic_ch.api.api import GenerateObject
from gui_prog.external_data.gui_text import TITLE_CREATE_FILE, NEW_FILE_NAME, EXCEL_FORMAT
from gui_prog.gui_files.btn_main import MainButton


class GenerateFile(QtWidgets.QDialog, GenerateObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Создание нового файла")
        self.setObjectName("Dialog")
        self.setFixedSize(400, 300)
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 10, 341, 281))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.styles = parent.get_styles()

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.btn_choose_dir = MainButton(self.verticalLayoutWidget, "btn_choose_dir")
        self.btn_choose_dir.setStyleSheet(self._build_style_block("btn_dialog", "btn_choose_dir", True))
        self.verticalLayout.addWidget(self.btn_choose_dir)

        self.spin_box_list_count = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spin_box_list_count.setMinimumSize(QtCore.QSize(0, 50))
        self.spin_box_list_count.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.spin_box_list_count.setAutoFillBackground(False)
        self.spin_box_list_count.setStyleSheet(self._build_style_block("spin_box", "spin_box_list_count", False))
        self.spin_box_list_count.setAlignment(QtCore.Qt.AlignCenter)
        self.spin_box_list_count.setPrefix("")
        self.spin_box_list_count.setMinimum(1)
        self.spin_box_list_count.setMaximum(25)
        self.spin_box_list_count.setProperty("value", 1)
        self.spin_box_list_count.setObjectName("spin_box_list_count")
        self.verticalLayout.addWidget(self.spin_box_list_count)

        self.btn_choose_dir_confirm = MainButton(self.verticalLayoutWidget, "btn_choose_dir_confirm")
        self.btn_choose_dir_confirm.disable()
        self.btn_choose_dir_confirm.setObjectName("btn_choose_dir_confirm")
        self.btn_choose_dir_confirm.setStyleSheet(self._build_style_block("btn_dialog", "btn_choose_dir_confirm", True))
        self.verticalLayout.addWidget(self.btn_choose_dir_confirm)

        self.btn_choose_dir.setText("Выбрать директорию и ввести имя файла")
        self.btn_choose_dir_confirm.setText("Создать файл")

        QtCore.QMetaObject.connectSlotsByName(self)
        self.file_dialog = QFileDialog()
        self.btn_choose_dir.clicked.connect(self._get_file_name)
        self.btn_choose_dir_confirm.clicked.connect(self.confirm)

    def _get_file_name(self):
        self.path = self.file_dialog.getSaveFileName(None, TITLE_CREATE_FILE, NEW_FILE_NAME, EXCEL_FORMAT)[0]
        if len(self.path) != 0:
            self.btn_choose_dir_confirm.enable()

    def run_input(self):
        self.exec_()

    def success_input(self):
        self.confirm()
        return True

    def get_path(self):
        return self.path

    def get_sheet_count(self):
        return self.spin_box_list_count.value()

    def _build_style_block(self, style_key, object_name, with_hover=False):
        style = "\n#" + object_name + self.styles[style_key]
        if with_hover:
            style += "\n#" + object_name + self.styles[style_key + "_hover"]
        return style

    def confirm(self):
        self.close()


if __name__ == '__main__':
    dial = GenerateFile()
