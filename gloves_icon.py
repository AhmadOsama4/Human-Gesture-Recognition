from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtCore import Qt, pyqtSignal
import os

class GlovesIcon(QLabel):
    clicked = pyqtSignal(['QString'])

    def __init__(self, gloves_name):
        QLabel.__init__(self)
        self.gloves_name = gloves_name
        path = os.path.join(os.getcwd(), 'Gloves', gloves_name + ".jpg")
        pixmap = QPixmap(path)
        self.setFixedWidth(150)
        self.setFixedHeight(150)
        w = self.width()
        h = self.height()
        pixmap = pixmap.scaled(w, h)
        self.setPixmap(pixmap)

    # def setPath(self, path):
    #     self.path = path
    #
    # def setImage(self, path):
    #     self.setPath(path)
    #     self.curPixmap = QPixmap(self.path)
    #     w = self.width()
    #     h = self.height()
    #     self.curPixmap = self.curPixmap.scaled(w, h)
    #     self.setPixmap(self.curPixmap)

    def mousePressEvent(self, event):
        self.clicked.emit(self.gloves_name)