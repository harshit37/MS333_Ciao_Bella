import tensorflow as tf

import numpy as np
import time
import matplotlib

import matplotlib.pyplot as plt
import os
import datetime

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

def load_image (image_file) :
    image = tf.io.read_file ("train_img/" + image_file)
    image = tf.image.decode_jpeg (image)
    image = tf.cast (image, tf.float32)
    image = tf.image.resize (image, [IMG_HEIGHT, IMG_WIDTH])
    image = image / 255.0

    mask = tf.io.read_file ("train_mask/" + image_file)
    mask = tf.image.decode_jpeg (mask, channels=1)
    image = tf.cast (image, tf.float32)
    mask = tf.image.resize (mask, [IMG_HEIGHT, IMG_WIDTH])
    mask = mask / 255.0

    return image, mask

def save_images (image, mask, pred, epoch, n) :
    plt.imsave ("Training/Epoch"+str(epoch)+"/Image"+str(n)+".jpg", np.clip (image[0], 0, 1))
    plt.imsave ("Training/Epoch"+str(epoch)+"/Prediction"+str(n)+".jpg", np.clip (pred[0, :, :, 0], 0, 1), cmap='gray')
    plt.imsave ("Training/Epoch"+str(epoch)+"/Mask"+str(n)+".jpg", np.clip (mask[0, :, :, 0], 0, 1), cmap='gray')

def predict (dataset, epoch) :
    if not os.path.isdir ("Training/Epoch"+str(epoch)) :
        os.mkdir ("Training/Epoch"+str(epoch))

    for n, (image, mask) in dataset.take(10).enumerate() :
        prediction = generator (image, training=False)
        prediction = tf.nn.sigmoid (prediction)

        save_images (image, mask, prediction, epoch, n.numpy())

def generator_loss (logits, label) :
    y = tf.cast(label, tf.float32)
    
    count_neg = tf.reduce_sum(1.-y)
    count_pos  = tf.reduce_sum(y)

    beta = count_neg / (count_neg + count_pos)

    pos_weight = beta / (1 - beta)
    cost = tf.nn.weighted_cross_entropy_with_logits(logits=logits, labels=y, pos_weight=pos_weight)

    cost = tf.reduce_mean(cost * (1 - beta))

    return tf.where(tf.equal(count_pos, 0.0), 0.0, cost)

def generator_loss_2 (gen_output, target) :
    cross_entropy_loss = loss_object (target, gen_output)
    return cross_entropy_loss

@tf.function
def train_step (input_image, input_mask, epoch) :
    with tf.GradientTape() as gen_tape :
        gen_output = generator ([input_image], training=True)
        gen_total_loss = generator_loss (gen_output, input_mask)
        
    generator_gradients = gen_tape.gradient (gen_total_loss, generator.trainable_variables)
    generator_optimizer.apply_gradients (zip (generator_gradients, generator.trainable_variables))

def fit (train_dataset, epochs) :
    for epoch in range (0, epochs) :
        if not os.path.isdir ("Training/Epoch"+str(epoch)) :
            os.mkdir ("Training/Epoch"+str(epoch))
        print ("EPOCH : " + str (epoch))

        for n, (input_image, input_mask) in tqdm (train_dataset.enumerate ()) :
            train_step (input_image, input_mask, epoch)
        if (epoch + 1) % 10 == 0 :
            checkpoint.save(file_prefix = checkpoint_prefix)
        predict (train_dataset, epoch)

if not os.path.isdir ("Training/") :
    os.mkdir ("Training/")

model = Model ()

train_file = open ("train_file.txt")
lines = train_file.readlines ()
lines = [line[:-1] for line in lines]

print (lines)

train_dataset = tf.data.Dataset.from_tensor_slices (lines)
train_dataset = train_dataset.map (load_image, num_parallel_calls=tf.data.experimental.AUTOTUNE)
train_dataset = train_dataset.shuffle (BUFFER_SIZE).batch (BATCH_SIZE)

loss_object = tf.keras.losses.BinaryCrossentropy (from_logits=True)

generator = model.build_generator ()
generator_optimizer = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

generator.summary ()

checkpoint_dir = './training_checkpoints'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(generator_optimizer=generator_optimizer, generator=generator)
checkpoint.restore ('training_checkpoints/ckpt-1')
predict (train_dataset, 100)
fit (train_dataset, EPOCHS)