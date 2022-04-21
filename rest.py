from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
import sys
from random import random

class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("AnouthorWindow", random(100))
        layout.addWidget(self.label)
        self.layout.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

    def show_new_window(self, cheked):
        if self.w is None:
            self.w = AnotherWindow()
        self.w.show()

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()