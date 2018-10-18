import tensorflow as tf
import pickle


class Rnn:
    def __init__(self, data_size: int):
        self.data_size = data_size

        self.x = tf.placeholder(tf.float32, [None, data_size], "X")
        self.y = tf.placeholder(tf.float32)

        self.model = self._build()

        self.cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(self.x, self.y))

        self.optimizer = tf.train.AdamOptimizer().minimize(self.cost)

        self.sess = tf.Session()
        self.saver = tf.train.Saver()
        self.sess.run(tf.global_variables_initializer())

    def _build(self):
        with tf.name_scope("LSTM scope"):
            cell1 = tf.nn.rnn_cell.BasicLSTMCell(128, name="cell1")
            cell2 = tf.nn.rnn_cell.BasicLSTMCell(128, name="cell1")

        multi_cell = tf.nn.rnn_cell.MultiRNNCell([cell1, cell2])

        outputs, state = tf.nn.dynamic_rnn(multi_cell, self.x, dtype=tf.float32)
        outputs = tf.transpose(outputs, [1, 0, 2])[-1]

        model = tf.layers.dense(outputs, self.data_size)
        return model

    def train(self, input_data, label, total_epoch: int):
        for epoch in range(total_epoch):
            self.sess.run([self.optimizer],
                          feed_dict={
                              self.x: input_data,
                              self.y: label
                          })

    def fit(self, input_data):
        prediction = tf.argmax(self.model, 1)
        return self.sess.run(prediction, feed_dict={self.x: input_data})

    def save(self):
        self.saver.save(self.sess, "check_point.ckpt", write_meta_graph=False)

