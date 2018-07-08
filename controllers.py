from keras.models import load_model
import cv2
from app_global import *

class KeyboardController:
    def __init__(self, configuration_file):
        self.config = configuration_file.keyboard

    def take_action(self, prediction):
        a = self.config[str(prediction)]
        if a == "INTERMEDIATE":
            return MODE.INTERMEDIATE, None
        else:
            return MODE.KEYBOARD, a


class MouseController:
    def __init__(self, configuration_file):
        self.config = configuration_file.mouse

    def take_action(self, prediction):
        a = self.config[str(prediction)]
        if a == "KEYBOARD":
            return MODE.KEYBOARD, None
        else:
            return MODE.MOUSE, a


class DynamicController:
    def __init__(self, configuration_file):
        self.config = configuration_file.dynamic

    def take_action(self, prediction):
        return self.config[str(prediction)]

class IntermediateController:
    def __init__(self, configuration_file):
        self.config = configuration_file.intermediate

    def take_action(self, prediction):
        return self.config[str(prediction)], None
