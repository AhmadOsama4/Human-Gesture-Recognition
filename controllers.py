from keras.models import load_model
import cv2
from app_global import *
import collections
from computer_controller import ComputerController
computer_controller = ComputerController()

class KeyboardController:
    def __init__(self, configuration_file):
        self.config = configuration_file.keyboard

    def take_action(self, prediction):
        a = self.config[str(prediction)]
        print("Currently in Keyboard Mode")
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
        self.buffer = collections.deque(maxlen=10)
        self.prev_prediction = None

    def take_action(self, prediction, center_x, center_y, camera_w, camera_h):
        #print('Camera Dimensions', camera_w, camera_h)
        a = self.config[str(prediction)]
        print("Currently in Mouse Mode")
        if a == "INTERMEDIATE":
            self.buffer.clear()
            return MODE.INTERMEDIATE
        elif a == "left_click" and self.prev_prediction != "left_click":

            if len(self.buffer) > 5:
                pass
                # dx, dy = self.buffer[-5]
                # computer_controller.moveCursor(dx, dy)
            computer_controller.leftClick()
            print('Left Clickkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')

        elif a == "double_click" and self.prev_prediction != "double_click":
            computer_controller.doubleClick()
            print('double Click')
        elif a == "track":
            dx = center_x - camera_w / 2
            dy = center_y - camera_h / 2
            computer_controller.moveCursor(dx, dy)
            self.buffer.append((dx, dy))
            print('tracking mouse')
        elif a == "right_click":
            computer_controller.rightClick()
            print('Right Click')

        self.prev_prediction = a

        return MODE.MOUSE

class DynamicController:
    def __init__(self, configuration_file):
        self.config = configuration_file.dynamic

    def take_action(self, prediction):
        print("Currently in Dynamic Mode")
        return self.config[str(prediction)]

class IntermediateController:
    def __init__(self, configuration_file):
        self.config = configuration_file.intermediate

    def take_action(self, prediction):
        a = self.config[str(prediction)]
        print("Currently in Intermediate Mode")
        if a == "MOUSE":
            return MODE.MOUSE
        elif a == "KEYBOARD":
            return MODE.KEYBOARD

        return MODE.INTERMEDIATE