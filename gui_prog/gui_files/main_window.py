from functools import partial

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon

from calc_acoustic_ch.api import api
from calc_acoustic_ch.api.api import MainObject
from calc_acoustic_ch.data_handlers.data_loader import DataLoader
from gui_prog.data_hadlers.styles_loader import StylesLoader
from gui_prog.external_data.gui_text import *
from gui_prog.gui_files.btn_help import HelpButton
from gui_prog.gui_files.btn_main import MainButton
from gui_prog.gui_files.gen_file import GenerateFile
from gui_prog.gui_files.help_message import HelpMessage
from gui_prog.gui_files.labels import MyLabel
from gui_prog.gui_files.prov_data import ProvideData
from gui_prog.gui_files.save_data import SaveData


class MainWindow(QtWidgets.QMainWindow, MainObject):
    def __init__(self):
        super().__init__()
        reader = StylesLoader()
        self.styles = reader.get_styles_from_yaml()
        self.setObjectName("main_window")
        self.setFixedSize(700, 740)

        self.setAutoFillBackground(False)
        self.setStyleSheet(self._build_style_block("main_window", self.objectName()))
        self.setAnimated(True)
        self.setDocumentMode(False)
        self.icon = QIcon(reader.MAIN_ICON)
        self.setWindowIcon(self.icon)

        self.central_widget = QtWidgets.QWidget(self)

        self.gridWidget = QtWidgets.QWidget(self.central_widget)
        self.gridWidget.setGeometry(QtCore.QRect(70, 40, 561, 661))
        self.gridLayout = QtWidgets.QGridLayout(self.gridWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        spacer_item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacer_item, 5, 0, 1, 1)
        spacer_item_1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacer_item_1, 1, 0, 1, 1)

        self.generate_file_pr_func = MainButton(self.gridWidget, "generate_file_pr_func")
        self.gridLayout.addWidget(self.generate_file_pr_func, 0, 0, 1, 1)

        self.provide_data_pr_func = MainButton(self.gridWidget, "provide_data_pr_func")
        self.gridLayout.addWidget(self.provide_data_pr_func, 2, 0, 1, 1)

        self.calculate_pr_func = MainButton(self.gridWidget, "calculate_pr_func")
        self.gridLayout.addWidget(self.calculate_pr_func, 4, 0, 1, 1)

        self.save_results_pr_func = MainButton(self.gridWidget, "save_results_pr_func")

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.save_results_pr_func.sizePolicy().hasHeightForWidth())

        self.save_results_pr_func.setSizePolicy(size_policy)
        self.gridLayout.addWidget(self.save_results_pr_func, 6, 0, 1, 1)

        for main_btn in [self.generate_file_pr_func,
                         self.provide_data_pr_func,
                         self.calculate_pr_func,
                         self.save_results_pr_func]:
            main_btn.setStyleSheet(
                self._build_style_block("btn_main", main_btn.objectName(), True)
            )

        self.gen_status = MyLabel(self.gridWidget, "label_generate")
        self.gridLayout.addWidget(self.gen_status, 0, 2, 1, 1)

        self.prov_status = MyLabel(self.gridWidget, "label_provide")
        self.gridLayout.addWidget(self.prov_status, 2, 2, 1, 1)

        self.calc_status = MyLabel(self.gridWidget, "calc_status")
        self.gridLayout.addWidget(self.calc_status, 4, 2, 1, 1)

        self.save_status = MyLabel(self.gridWidget, "save_status")
        self.gridLayout.addWidget(self.save_status, 6, 2, 1, 1)

        self.status_label_desc = MyLabel(self.gridWidget, "status_label_desc")
        self.gridLayout.addWidget(self.status_label_desc, 8, 0, 1, 1)

        self.main_status = MyLabel(self.gridWidget, "main_status")
        self.gridLayout.addWidget(self.main_status, 8, 2, 1, 1)

        for label in [self.gen_status,
                      self.prov_status,
                      self.calc_status,
                      self.save_status,
                      self.status_label_desc,
                      self.main_status]:
            label.setStyleSheet(self._build_style_block("label", label.objectName()))

        self.btn_generate_get_help = HelpButton(self.gridWidget, "btn_generate_get_help")
        self.gridLayout.addWidget(self.btn_generate_get_help, 0, 1, 1, 1)

        self.btn_provide_get_help = HelpButton(self.gridWidget, "btn_provide_get_help")
        self.gridLayout.addWidget(self.btn_provide_get_help, 2, 1, 1, 1)

        self.btn_calculate_get_help = HelpButton(self.gridWidget, "btn_calculate_get_help")
        self.gridLayout.addWidget(self.btn_calculate_get_help, 4, 1, 1, 1)

        self.btn_save_get_help = HelpButton(self.gridWidget, "btn_save_get_help")
        self.gridLayout.addWidget(self.btn_save_get_help, 6, 1, 1, 1)

        spacer_item_2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacer_item_2, 3, 0, 1, 1)

        spacer_item_3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacer_item_3, 7, 0, 1, 1)

        self.line = QtWidgets.QFrame(self.central_widget)
        self.line.setGeometry(QtCore.QRect(-30, 600, 751, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.setCentralWidget(self.central_widget)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.setWindowTitle(MAIN_WIN_TITLE)
        self.generate_file_pr_func.setText(BTN_GEN_INIT)
        self.provide_data_pr_func.setText(BTN_PROV_INIT)
        self.calculate_pr_func.setText(BTN_CALC_INIT)
        self.save_results_pr_func.setText(BTN_SAVE_INIT)

        for btn_help in [self.btn_generate_get_help,
                         self.btn_provide_get_help,
                         self.btn_calculate_get_help,
                         self.btn_save_get_help]:
            btn_help.setText(BTN_HELP)
            btn_help.setStyleSheet(self._build_style_block("btn_help", btn_help.objectName(), True))

        self.status_label_desc.setText(STATUS_DESC)

        self.main_status.setText(LBL_STATUS_INIT)
        self.gen_status.setText(LBL_GEN_INIT)
        self.prov_status.setText(LBL_PROV_INIT)
        self.calc_status.setText(LBL_CALC_INIT)
        self.save_status.setText(LBL_SAVE_INIT)

        self.calculate_pr_func.disable()
        self.save_results_pr_func.disable()

        self.set_func_gen(api.get_dir_for_gen, self, GenerateFile(self))
        self.set_func_prov(api.get_file_with_data, self, ProvideData())
        self.set_func_calc(api.calculate, self)
        self.set_func_save(api.save, self, SaveData())

        self.btn_generate_get_help.clicked.connect(self.help_gen)
        self.btn_provide_get_help.clicked.connect(self.help_prov)
        self.btn_calculate_get_help.clicked.connect(self.help_calc)
        self.btn_save_get_help.clicked.connect(self.help_save)

    def help_gen(self):
        self._help_create_window("btn_generate_get_help")

    def help_prov(self):
        self._help_create_window("btn_provide_get_help")

    def help_calc(self):
        self._help_create_window("btn_calculate_get_help")

    def help_save(self):
        self._help_create_window("btn_save_get_help")

    def _help_create_window(self, name):
        mes = HelpMessage()
        mes.get_message(name)
        message_box = QtWidgets.QMessageBox()
        message_box.setStyleSheet(self.styles["help_wind"])
        message_box.setWindowIcon(self.icon)
        message_box.information(message_box, mes.title, mes.text)

    def set_func_gen(self, name, *args):
        self._set_func_btn(self.generate_file_pr_func, name, *args)

    def set_func_prov(self, name, *args):
        self._set_func_btn(self.provide_data_pr_func, name, *args)

    def set_func_calc(self, name, *args):
        self._set_func_btn(self.calculate_pr_func, name, *args)

    def set_func_save(self, name, *args):
        self._set_func_btn(self.save_results_pr_func, name, *args)

    @staticmethod
    def _set_func_btn(button, func_name, *args):
        if callable(func_name):
            button.clicked.connect(partial(func_name, *args))
        else:
            raise ValueError("You passed the wrong function!")

    def _build_style_block(self, style_key, object_name, with_hover=False):
        style = "\n#" + object_name + self.styles[style_key]
        if with_hover:
            style += "\n#" + object_name + self.styles[style_key + "_hover"]
        return style

    def get_styles(self):
        return self.styles

    def closeEvent(self, event):
        DataLoader.clear_images_dir()
