import tensorflow as tf
import numpy as np
import os
import matplotlib.pyplot as plt
import time
import cv2

from PIL import Image

from Model import Model

class Evaluate () :
    def __init__ (self) :
        model = Model ()
        self.generator = model.build_generator ()
        generator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

        checkpoint_dir = './training_checkpoints/'
        checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
        checkpoint = tf.train.Checkpoint(generator_optimizer=generator_optimizer, generator=self.generator)

        checkpoint.restore ('training_checkpoints/ckpt-16')

    def from_numpy (self, image) :
        if not max (np.unique(image)) <= 1.0 :
            image = image / 255.0

        pred = self.generator (image[np.newaxis, ...], training=False)
        pred = np.where (pred>0.5, 1, 0).astype ('uint8')

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        pred = cv2.morphologyEx(pred[0, :, :, 0],cv2.MORPH_OPEN,kernel)

        return pred

    def from_path (self, image_file) :
        image = np.array (Image.open (image_file).resize ((128, 128))).astype ('float') / 255.0
        pred = self.generator (image[np.newaxis, ...], training=False)
        pred = tf.nn.sigmoid (pred)

        pred = np.where (pred>0.5, 1, 0).astype ('uint8')

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        pred = cv2.morphologyEx(pred[0, :, :, 0],cv2.MORPH_OPEN,kernel)

        return pred

evaluate = Evaluate ()

for root, _, files in os.walk ("Images/") :
    for file in files :
        prediction = evaluate.from_path (root + file)
        plt.imsave ("Prediction/" + file, prediction, cmap='gray')
