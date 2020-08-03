import tensorflow as tf

class Model () :
    def build_classifier (self) :
        image = tf.keras.layers.Input (shape=[None, None, 3])

        x = tf.keras.layers.Conv2D (32, kernel_size=7, strides=1, padding='same') (image)
        x = tf.keras.layers.LeakyReLU () (x)

        x = tf.keras.layers.Conv2D (64, kernel_size=3, strides=2, padding='same') (x)
        x = tf.keras.layers.BatchNormalization () (x)
        x = tf.keras.layers.LeakyReLU () (x)

        x = tf.keras.layers.Conv2D (128, kernel_size=3, strides=2, padding='same') (x)
        x = tf.keras.layers.BatchNormalization () (x)
        x = tf.keras.layers.LeakyReLU () (x)

        x = tf.keras.layers.Conv2D (256, kernel_size=3, strides=2, padding='same') (x)
        x = tf.keras.layers.BatchNormalization () (x)
        x = tf.keras.layers.LeakyReLU () (x)

        x = tf.keras.layers.Conv2D (512, kernel_size=3, strides=2, padding='same') (x)
        x = tf.keras.layers.BatchNormalization () (x)
        x = tf.keras.layers.LeakyReLU () (x)

        x = tf.keras.layers.Conv2D (512, kernel_size=3, strides=2, padding='same') (x)
        x = tf.keras.layers.BatchNormalization () (x)
        x = tf.keras.layers.LeakyReLU () (x)

        x = tf.keras.layers.Reshape (target_shape=(4*4*512,)) (x)

        x = tf.keras.layers.Dense (16, activation='relu') (x)
        x = tf.keras.layers.Dense (1, activation=None) (x)

        return tf.keras.Model (inputs=image, outputs=x)

model = Model ()
gen = model.build_classifier ()
gen.summary()