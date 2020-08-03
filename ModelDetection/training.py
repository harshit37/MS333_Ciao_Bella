import tensorflow as tf

import numpy as np
import time
import matplotlib

import matplotlib.pyplot as plt
import os
import datetime
import random

from PIL import Image
from tqdm import tqdm
from Model import Model

IMG_HEIGHT = 128
IMG_WIDTH = 128
CLASSES = 2
BATCH_SIZE = 1
BUFFER_SIZE = 1
LAMBDA = 100
EPOCHS = 100
PATH_A = "Sedan"     # Path to 1st folder (Denoted as 0 in output)
PATH_B = "SUV"     # Path to 2nd folder (Denoted as 1 in output)

def load_image (image_file) :
    image = tf.io.read_file (image_file)
    image = tf.image.decode_jpeg (image)
    image = tf.cast (image, tf.float32)
    image = tf.image.resize (image, [IMG_HEIGHT, IMG_WIDTH])
    image = image / 255.0

    return image

def generator_loss (gen_output, target) :
    return tf.nn.sigmoid_cross_entropy_with_logits(labels=target, logits=gen_output)
    

@tf.function
def train_step (input_image, label, epoch) :
    with tf.GradientTape() as gen_tape :
        gen_output = generator ([input_image], training=True)
        gen_total_loss = generator_loss (gen_output, label)
        
    generator_gradients = gen_tape.gradient (gen_total_loss, generator.trainable_variables)
    generator_optimizer.apply_gradients (zip (generator_gradients, generator.trainable_variables))

    return gen_total_loss, gen_output

def fit (epochs) :
    for epoch in range (0, epochs) :
        if not os.path.isdir ("Training/Epoch"+str(epoch)) :
            os.mkdir ("Training/Epoch"+str(epoch))
        print ("EPOCH : " + str (epoch))

        loss = 0
        correct = 0

        for (image, label) in inputs :
            loss_, out = train_step (tf.expand_dims (image, axis=0), label=label, epoch=epoch)

            loss += loss_.numpy()
            print (loss_.numpy())

            if (out.numpy() > 0.5 and label[0, 0] == 1) or (out.numpy() < 0.5 and label[0, 0] == 0) :
                correct += 1
            

        print ("Loss = ", loss / len (inputs))
        print ("Accuracy = ", correct / len (inputs))
        if (epoch + 1) % 10 == 0 :
            checkpoint.save(file_prefix = checkpoint_prefix)

if not os.path.isdir ("Training/") :
    os.mkdir ("Training/")

inputs = []

for root, dirs, files in os.walk (PATH_A) :
    for file in files :
        inputs.append ((load_image (root + "/" + file), np.array ([[0.0]]).astype (np.float32)))

for root, dirs, files in os.walk (PATH_B) :
    for file in files :
        inputs.append ((load_image (root + "/" +file), np.array ([[1.0]]).astype (np.float32)))

random.shuffle (inputs)
print (len (inputs))

model = Model ()

loss_object = tf.keras.losses.BinaryCrossentropy (from_logits=True)

generator = model.build_classifier ()
generator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

generator.summary ()

checkpoint_dir = './training_checkpoints'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(generator_optimizer=generator_optimizer, generator=generator)

fit (EPOCHS)