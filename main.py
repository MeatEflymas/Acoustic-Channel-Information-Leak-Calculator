import sys
from PyQt5.QtWidgets import QApplication

from gui_prog.gui_files.main_window import MainWindow

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())