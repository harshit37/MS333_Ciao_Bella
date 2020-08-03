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
        self.generator = model.build_classifier()

        checkpoint_dir = './training_checkpoints/'
        checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
        checkpoint = tf.train.Checkpoint(generator=self.generator)

        checkpoint.restore ('training_checkpoints/ckpt-1')

    def from_numpy (self, image) :
        if not max (np.unique(image)) <= 1.0 :
            image = image / 255.0

        pred = self.generator (image[np.newaxis, ...], training=False)

        return pred

    def from_path (self, image_file) :
        image = np.array (Image.open (image_file)).astype ('float') / 255.0
        pred = self.generator (image[np.newaxis, ...], training=False)

        return pred