from PyQt5.QtWidgets import QFileDialog

from calc_acoustic_ch.api.api import SaveDataObject
from gui_prog.external_data.gui_text import TITLE_CREATE_FILE, NEW_FILE_NAME, EXCEL_FORMAT


class SaveData(SaveDataObject):
    def get_path(self):
        return QFileDialog.getSaveFileName(None, TITLE_CREATE_FILE, NEW_FILE_NAME, EXCEL_FORMAT)[0]
