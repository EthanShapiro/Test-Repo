from PyQt5.QtWidgets import QApplication, QDialog
import sys

class Window(QDialog):

    def __init__(self):
        super().__init__()
        self.show()

app = QApplication([])
window = Window()
sys.exit(app.exec())
