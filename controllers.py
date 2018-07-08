from keras.models import load_model
import cv2
from app_global import *
from computer_controller import ComputerController

computer_controller = ComputerController()

class KeyboardController:
    def __init__(self, configuration_file):
        self.config = configuration_file.keyboard

    def take_action(self, prediction):
        a = self.config[str(prediction)]
        if a == "INTERMEDIATE":
            return MODE.INTERMEDIATE
        elif a == "up":
            computer_controller.clickUp()
        elif a == "down":
            computer_controller.clickDown()

        return MODE.KEYBOARD


class MouseController:
    def __init__(self, configuration_file):
        self.config = configuration_file.mouse

    def take_action(self, prediction, center_x, center_y, camera_w, camera_h):
        a = self.config[str(prediction)]
        a = "track"
        if a == "KEYBOARD":
            return MODE.KEYBOARD
        elif a == "left_click":
            computer_controller.leftClick()
        elif a == "double_click":
            computer_controller.doubleClick()
        elif a == "track":
            dx = center_x - camera_w / 2
            dy = center_y - camera_h / 2
            computer_controller.moveCursor(dx, dy)
        elif a == "right_click":
            computer_controller.rightClick()

        return MODE.MOUSE

class DynamicController:
    def __init__(self, configuration_file):
        self.config = configuration_file.dynamic

    def take_action(self, prediction):
        return self.config[str(prediction)]

class IntermediateController:
    def __init__(self, configuration_file):
        self.config = configuration_file.intermediate

    def take_action(self, prediction):
        a = self.config[str(prediction)]
        if a == "MOUSE":
            return MODE.MOUSE
        elif a == "DYNAMIC":
            return MODE.DYNAMIC

        return MODE.KEYBOARD