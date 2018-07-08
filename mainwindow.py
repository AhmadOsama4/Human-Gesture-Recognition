from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget #, QPushButton, QAction, QMessageBox
from PyQt5.QtWidgets import QGridLayout #, QLabel, QVBoxLayout, QGroupBox
# from PyQt5.QtCore import QThread
from gloves_icon import GlovesIcon
import os
import sys

class window(QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(50, 50, 720, 720)
        self.setWindowTitle('Gesture Recognition')

        self.central_widget = QWidget()
        self.grid_layout = QGridLayout()

        self.add_gloves_icons()

        self.central_widget.setLayout(self.grid_layout)
        self.setCentralWidget(self.central_widget)

        self.show()

    def add_gloves_icons(self):
        images_path = os.path.join(os.getcwd(), 'Images')
        paths = os.listdir(images_path)

        #saved gloves
        indx = 0
        for image in paths:
            glove_name = image[:-4]
            print(glove_name)
            gloves_icon = GlovesIcon(glove_name)
            gloves_icon.clicked.connect(self.gestureSelected)

            i = indx / 2
            j = indx % 2

            self.grid_layout.addWidget(gloves_icon, i, j)

            indx += 1

    def gestureSelected(self, gloves_name):
        if gloves_name == "new_gesture_icon":
            pass
        else:
            print('Gesture Selected:', gloves_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Gui = window()
    sys.exit(app.exec_())
