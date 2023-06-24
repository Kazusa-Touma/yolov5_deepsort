import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from main_ui import Ui_MainWindow


class My_MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(My_MainWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    mywin = My_MainWindow()
    mywin.setWindowTitle("车辆检测")
    mywin.show()
    sys.exit(app.exec_())