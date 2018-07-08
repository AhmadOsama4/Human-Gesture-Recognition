from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget #, QPushButton, QAction, QMessageBox
from PyQt5.QtWidgets import QGridLayout #, QLabel, QVBoxLayout, QGroupBox
# from PyQt5.QtCore import QThread
from gloves_icon import GlovesIcon
from mode_controller import ModeController
import os
import sys

class window(QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.setGeometry(50, 50, 720, 720)
        self.setWindowTitle('Gesture Recognition')

        self.mode_controller = None

        self.central_widget = QWidget()
        self.grid_layout = QGridLayout()

        self.add_gloves_icons()

        self.central_widget.setLayout(self.grid_layout)
        self.setCentralWidget(self.central_widget)

        self.show()

    def add_gloves_icons(self):
        images_path = os.path.join(os.getcwd(), 'Gloves')
        paths = os.listdir(images_path)

        #saved gloves
        indx = 0
        for image in paths:
            if image[-4:] != '.jpg' and image[-4:] != '.png': #consider jpg images only
                continue
            glove_name = image[:-4]
            print(glove_name)
            gloves_icon = GlovesIcon(glove_name)
            gloves_icon.clicked.connect(self.gestureSelected)

            i = indx / 3
            j = indx % 3

            self.grid_layout.addWidget(gloves_icon, i, j)

            indx += 1

    def gestureSelected(self, gloves_name):
        configuration_file_path = os.path.join(os.getcwd(), "config_file.json")
        if gloves_name == "new_gloves_icon":
            print('Add a new glove')
            self.mode_controller = ModeController(configuration_file_path, None)
        else:
            print('Load a saved glove')
            self.mode_controller = ModeController(configuration_file_path, gloves_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Gui = window()
    sys.exit(app.exec_())
