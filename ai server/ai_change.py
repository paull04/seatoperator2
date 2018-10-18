import tensorflow as tf


class RL:
    def __init__(self):
        self.x = tf.placeholder(tf.float32, shape=[None, None, 4])
        self.y = tf.placeholder(tf.float32, dtype=[None, None, 4])