import numpy as np
import cv2
import math
import time
from sklearn.mixture import GaussianMixture,BayesianGaussianMixture

class Gloves:
    def __init__(self):
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        self.camera_width = None
        self.camera_height = None

    def enhance_image(self, image):
        Y, U, V = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2YUV))
        Y = self.clahe.apply(Y)
        new = cv2.cvtColor(cv2.merge((Y, U, V)), cv2.COLOR_YUV2BGR)
        new = cv2.medianBlur(new, 11)
        return new

    def get_samples(self, size = 50):
        color_mask = cv2.imread('Images/color_mask4.jpg')

        cover = cv2.imread('Images/hand2.jpg', 1)

        # start camera
        camera = cv2.VideoCapture(0)
        ret_val, orig = camera.read()
        # get width and height of the image captured by the camera
        self.camera_height, self.camera_width, _ = orig.shape

        flag = True

        start = time.time()
        while True:
            ret_val, orig = camera.read()
            orig = cv2.flip(orig, 1)
            image = orig.copy()
            frame = self.enhance_image(orig)

            if flag:
                flag = False  # to be executed once

                cover = cv2.resize(cover, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_CUBIC)
                color_mask = cv2.resize(color_mask, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_CUBIC)

                _, cover_mask = cv2.threshold(cv2.cvtColor(cover, cv2.COLOR_BGR2GRAY), 127, 1, cv2.THRESH_BINARY)
                _, color_mask = cv2.threshold(cv2.cvtColor(color_mask, cv2.COLOR_BGR2GRAY), 127, 1, cv2.THRESH_BINARY)

                cover_mask = cover_mask.astype(bool)
                color_mask = color_mask.astype(bool)

            orig[~cover_mask] = cover[~cover_mask]

            if time.time() - start >= 10:
                masked = frame[color_mask]
                cv2.destroyWindow('img')
                break

            cv2.imshow('img', orig)
            if cv2.waitKey(1) == 27:
                break  # esc to quit

        tmp = int(size)
        while tmp > 0:
            idx = np.random.randint(0, masked.shape[0])
            sample = masked[idx, :]
            if tmp == size:
                samples = np.array([sample])
                tmp -= 1
                continue
            d = np.linalg.norm(sample - samples, axis=1)
            if np.any(d < 20):
                continue
            else:
                samples = np.append(samples, [sample], axis=0)
                tmp -= 1
        samples = samples.reshape(1, -1, 3)
        samples = cv2.cvtColor(samples, cv2.COLOR_BGR2HSV)
        camera.release()

        return image, samples, masked

    def train_gmm(self, samples):
        co_type = 'tied'
        gmm = BayesianGaussianMixture(n_components=2, covariance_type=co_type, n_init=10, random_state=0, max_iter=500,
                                      verbose=1)

        samples = cv2.cvtColor(samples.reshape(1, -1, 3), cv2.COLOR_BGR2YCrCb)
        samples = samples.reshape(-1, 3)
        gmm.fit(samples)

        max_prob = np.max(gmm.score_samples(samples))
        return gmm, max_prob

    def classify_gmm(self, img):
        h, w, _ = img.shape

        img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        img = img.reshape(-1, 3)
        prediction = self.gmm.score_samples(img)
        m = prediction < 2.2 * self.max_prob

        prediction[m] = 0
        prediction[~m] = 255

        return prediction.reshape(h, w).astype(np.uint8)

    def train(self):
        size = 50
        image, samples, masked = self.get_samples(size)
        self.gmm, self.max_prob = self.train_gmm(masked)

        return image

    def preprocess_image(self, image):
        image = self.enhance_image(image)

        h, w, _ = image.shape

        # resizing image into smaller size to improve performance
        w_new = int(150 * w / max(w, h))
        h_new = int(150 * h / max(w, h))
        image = cv2.resize(image, (w_new, h_new))

        final_mask = self.classify_gmm(image)
        new = cv2.resize(final_mask, (w, h))

        img_dim = (64, 64)
        keras_img = cv2.resize(new, img_dim)
        keras_img = keras_img.reshape((1,) + keras_img.shape + (1,))
        keras_img = keras_img.astype('float32')
        keras_img = (1. / 255) * keras_img

        # return image and a preprocessed image for keras
        return new, keras_img

    def get_hand_center(self, img):
        h, w = img.shape
        # find contours
        _, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        dst = np.zeros((h, w, 3), np.uint8)

        max_area = 0
        best_cnt = None
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                best_cnt = cnt

        cv2.drawContours(dst, [best_cnt], 0, (255, 0, 0), 2)

        mom = cv2.moments(best_cnt)
        cx = int(mom['m10'] / mom['m00'])
        cy = int(mom['m01'] / mom['m00'])

        cv2.circle(dst, (cx, cy), 10, (0, 0, 255), -1)
        return cx, cy

    def get_camera_dimensions(self):
        return self.camera_width, self.camera_height

if __name__ == "__main__":
    glove = Gloves()
    glove.train()

    camera = cv2.VideoCapture(0)
    ret_val, image = camera.read()

    image, _ = glove.preprocess_image(image)
    #image = image.reshape(64, 64)
    cx, cy = glove.get_hand_center(image)
    print(cx, cy)

    cv2.imshow('window', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()





