from PyQt5.QtWidgets import QFileDialog

from calc_acoustic_ch.api.api import ProvideDataObject
from gui_prog.external_data.gui_text import TITLE_CHOOSE_FILE, EXIST_FILE_NAME, EXCEL_FORMAT


class ProvideData(ProvideDataObject):
    def get_path(self):
        return QFileDialog.getOpenFileName(None, TITLE_CHOOSE_FILE, EXIST_FILE_NAME, EXCEL_FORMAT)[0]
