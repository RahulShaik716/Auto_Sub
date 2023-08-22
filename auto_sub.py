from PyQt5.QtWidgets import *
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Auto Sub')
        self.textbox = QLineEdit(self)
        self.upload  = QPushButton(self)
        self.show()

app = QApplication(sys.argv)
screen = app.primaryScreen() 
size = screen.size()
window = Window()
window.setGeometry(0,40,size.width(),size.height())
window.show()
sys.exit(app.exec_())

