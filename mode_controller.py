from keras.models import load_model
import Gloves
import os
import time
import pickle
from app_global import *
import cv2
import controllers
from config import process_config

class ModeController:
    def __init__(self, configuration_file_path, gloves_name = None):
        """

        :param model_path: path to the static gestures model
        :param configuration_file_path: path to the configuration file to load
        :param glove_path: path to a glove if a pretrained glove is selected
        """

        self.configuration_file = process_config(configuration_file_path)# load the configuration file
        model_path = self.configuration_file["model_path"]
        self.static_model = load_model(model_path)

        self.mouse_controller = controllers.MouseController(self.configuration_file)
        self.keyboard_controller = controllers.KeyboardController(self.configuration_file)
        self.dynamic_controller = controllers.DynamicController(self.configuration_file)

        #add a new glove
        if gloves_name is None:
            file_name = time.strftime("%Y%m%d-%H%M%S")
            self.gloves = Gloves()
            save_path = os.path.join(os.getcwd(), 'Gloves', file_name + '.txt')
            gloves_image = self.gloves.train()

            #pickle.dump(self.gloves, save_path)
            with open(save_path, 'wb') as handle:
                pickle.dump(self.gloves, handle, protocol=pickle.HIGHEST_PROTOCOL)
            image_path = os.path.join(os.getcwd(), 'Gloves', file_name + '.jpg')
            cv2.imwrite(gloves_image, image_path)
        #load a saved glove
        else:
            #self.gloves = pickle.load(os.path.join(os.getcwd(), 'Gloves', gloves_name))
            with open(gloves_name, 'rb') as handle:
                self.gloves = pickle.load(handle)

        self.current_mode = MODE.KEYBOARD
        self.start()


    def start(self):
        camera = cv2.VideoCapture(0)
        while True:
            if self.current_mode == MODE.DYNAMIC:
                #TODO: wait for t periods, and beep
                centers = []
                for i in range(31):
                    ret_val, image = camera.read()
                    preprocessed_image = self.gloves.preprocess_image(image)
                    center = self.gloves.get_hand_center(preprocessed_image)
                    centers.append(center)
                    action = self.dynamic_controller.take_action(centers)
                    eval(action)

                self.current_mode = MODE.KEYBOARD

            else:
                ret_val, image = camera.read()
                preprocessed_image = self.gloves.preprocess(image)

                prediction = self.static_model.predict(preprocessed_image)

                next_mode = self.current_mode

                if self.current_mode == MODE.KEYBOARD:
                    (next_mode, action) = self.mouse_controller.take_action(prediction)
                elif self.current_mode == MODE.MOUSE:
                    (next_mode, action) = self.keyboard_controller.take_action(prediction)
                elif self.current_mode == MODE.DYNAMIC:
                    (next_mode, action) = self.dynamic_controller.take_action(prediction)

                eval(action)
                self.current_mode = next_mode

