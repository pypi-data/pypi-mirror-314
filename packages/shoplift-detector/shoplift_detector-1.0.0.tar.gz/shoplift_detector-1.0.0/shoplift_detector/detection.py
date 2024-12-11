import numpy as np
import cv2
import tensorflow as tf
import math

class ShopliftingPrediction:
    def __init__(self, model_path, frame_width=90, frame_height=90, sequence_length=160):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.sequence_length = sequence_length
        self.model_path = model_path
        self.model = None

    def load_model(self):
        self.model = tf.keras.models.load_model(self.model_path)

    def preprocess_frame(self, current_frame, previous_frame):
        diff = cv2.absdiff(current_frame, previous_frame)
        diff = cv2.GaussianBlur(diff, (3, 3), 0)
        resized_frame = cv2.resize(diff, (self.frame_height, self.frame_width))
        gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
        return gray_frame / 255.0

    def predict(self, frames_queue):
        probabilities = self.model.predict(np.expand_dims(frames_queue, axis=0))[0]
        predicted_label = np.argmax(probabilities)
        probability = math.floor(max(probabilities) * 100)
        return probability, predicted_label
