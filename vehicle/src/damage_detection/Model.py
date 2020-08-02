import tensorflow as tf

class Model () :
    def build_generator (self) :
        input_image = tf.keras.layers.Input (shape=[None, None, 3])

        x = tf.keras.layers.Conv2D (32, kernel_size=7, strides=1, padding='same') (input_image)
        skip_0 = tf.keras.layers.LeakyReLU () (x)

        x = tf.keras.layers.Conv2D (64, kernel_size=5, strides=2, padding='same') (skip_0)
        x = tf.keras.layers.BatchNormalization () (x)
        skip_1 = tf.keras.layers.LeakyReLU () (x)

        x = tf.keras.layers.Conv2D (128, kernel_size=5, strides=2, padding='same') (skip_1)
        x = tf.keras.layers.BatchNormalization () (x)
        skip_2 = tf.keras.layers.LeakyReLU () (x)

        x = tf.keras.layers.Conv2D (256, kernel_size=3, strides=2, padding='same') (skip_2)
        x = tf.keras.layers.BatchNormalization () (x)
        skip_3 = tf.keras.layers.LeakyReLU () (x)

        x = tf.keras.layers.Conv2D (512, kernel_size=3, strides=2, padding='same') (skip_3)
        x = tf.keras.layers.BatchNormalization () (x)
        x = tf.keras.layers.LeakyReLU () (x)

        x = tf.keras.layers.Conv2DTranspose (256, kernel_size=3, strides=2, padding='same') (x)
        x = tf.keras.layers.BatchNormalization () (x)
        x = tf.keras.layers.LeakyReLU () (x)
        x = tf.keras.layers.Concatenate () ([x, skip_3])

        x = tf.keras.layers.Conv2DTranspose (128, kernel_size=3, strides=2, padding='same') (x)
        x = tf.keras.layers.BatchNormalization () (x)
        x = tf.keras.layers.LeakyReLU () (x)
        x = tf.keras.layers.Concatenate () ([x, skip_2])

        x = tf.keras.layers.Conv2DTranspose (64, kernel_size=5, strides=2, padding='same') (x)
        x = tf.keras.layers.BatchNormalization () (x)
        x = tf.keras.layers.LeakyReLU () (x)
        x = tf.keras.layers.Concatenate () ([x, skip_1])

        x = tf.keras.layers.Conv2DTranspose (32, kernel_size=5, strides=2, padding='same') (x)
        x = tf.keras.layers.BatchNormalization () (x)
        x = tf.keras.layers.LeakyReLU () (x)
        x = tf.keras.layers.Concatenate () ([x, skip_0])

        x = tf.keras.layers.Conv2D (1, kernel_size=7, strides=1, padding='same') (x)

        return tf.keras.Model (inputs=input_image, outputs=x)
