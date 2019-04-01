import sys
import numpy as np
import tensorflow as tf


class Model:

    snapshot = 0

    def __init__(self, image_width, image_height, batch_size, characters, max_text_length, gpu, inferring=False):
        self.image_width = image_width
        self.image_height = image_height
        self.batch_size = batch_size
        self.characters = characters
        self.max_text_length = max_text_length
        self.inferring = inferring

        self.is_train = tf.placeholder(tf.bool, name="is_train")
        self.input_images = tf.placeholder(tf.float32, shape=(None, self.image_width, self.image_height))

        if gpu:
            with tf.device('/gpu:0'):
                self.prepare_cnn()
                self.prepare_rnn()
                self.prepare_ctc()
        else:
            self.prepare_cnn()
            self.prepare_rnn()
            self.prepare_ctc()

        self.trained_batches = 0
        self.rate = tf.placeholder(tf.float32, shape=[])
        self.update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)

        with tf.control_dependencies(self.update_ops):
            self.optimizer = tf.train.RMSPropOptimizer(self.rate).minimize(self.loss)

        config = tf.ConfigProto(allow_soft_placement = True)
        self.sess = tf.Session(config=config)
        self.saver = tf.train.Saver(max_to_keep=1)
        if self.inferring:
            model_dir = 'model/snapshot'
        else:
            model_dir = './snapshot'
        latest = tf.train.latest_checkpoint(model_dir)

        if latest:
            self.saver.restore(self.sess, latest)
        else:
            self.sess.run(tf.global_variables_initializer())

        if self.inferring:
            self.writer = tf.summary.FileWriter('model/logs', self.sess.graph)
        else:
            self.writer = tf.summary.FileWriter('./logs', self.sess.graph)

    def prepare_cnn(self):
        self.cnn = tf.expand_dims(input=self.input_images, axis=3)

        # create layers
        kernel = tf.Variable(tf.truncated_normal([5, 5, 1, 32], stddev=0.1))
        convolution = tf.nn.conv2d(self.cnn, kernel, padding='SAME',  strides=(1, 1, 1, 1))
        convolution_normalised = tf.layers.batch_normalization(convolution, training=self.is_train)
        relu = tf.nn.relu(convolution_normalised)
        kernel2 = tf.Variable(tf.truncated_normal([5, 5, 32, 32], stddev=0.1))
        convolution2 = tf.nn.conv2d(relu, kernel2, padding='SAME',  strides=(1, 1, 1, 1))
        convolution_normalised2 = tf.layers.batch_normalization(convolution2, training=self.is_train)
        relu2 = tf.nn.relu(convolution_normalised2)
        self.cnn = tf.nn.max_pool(relu2, (1, 2, 2, 1), (1, 2, 2, 1), 'VALID')

        kernel = tf.Variable(tf.truncated_normal([5, 5, 32, 64], stddev=0.1))
        convolution = tf.nn.conv2d(self.cnn, kernel, padding='SAME',  strides=(1, 1, 1, 1))
        convolution_normalised = tf.layers.batch_normalization(convolution, training=self.is_train)
        relu = tf.nn.relu(convolution_normalised)
        kernel2 = tf.Variable(tf.truncated_normal([5, 5, 64, 64], stddev=0.1))
        convolution2 = tf.nn.conv2d(relu, kernel2, padding='SAME',  strides=(1, 1, 1, 1))
        convolution_normalised2 = tf.layers.batch_normalization(convolution2, training=self.is_train)
        relu2 = tf.nn.relu(convolution_normalised2)
        self.cnn = tf.nn.max_pool(relu2, (1, 2, 2, 1), (1, 2, 2, 1), 'VALID')

        kernel = tf.Variable(tf.truncated_normal([3, 3, 64, 128], stddev=0.1))
        convolution = tf.nn.conv2d(self.cnn, kernel, padding='SAME',  strides=(1, 1, 1, 1))
        convolution_normalised = tf.layers.batch_normalization(convolution, training=self.is_train)
        relu = tf.nn.relu(convolution_normalised)
        kernel2 = tf.Variable(tf.truncated_normal([3, 3, 128, 128], stddev=0.1))
        convolution2 = tf.nn.conv2d(relu, kernel2, padding='SAME',  strides=(1, 1, 1, 1))
        convolution_normalised2 = tf.layers.batch_normalization(convolution2, training=self.is_train)
        relu2 = tf.nn.relu(convolution_normalised2)
        self.cnn = tf.nn.max_pool(relu2, (1, 1, 2, 1), (1, 1, 2, 1), 'VALID')

        kernel = tf.Variable(tf.truncated_normal([3, 3, 128, 128], stddev=0.1))
        convolution = tf.nn.conv2d(self.cnn, kernel, padding='SAME',  strides=(1, 1, 1, 1))
        convolution_normalised = tf.layers.batch_normalization(convolution, training=self.is_train)
        relu = tf.nn.relu(convolution_normalised)
        kernel2 = tf.Variable(tf.truncated_normal([3, 3, 128, 128], stddev=0.1))
        convolution2 = tf.nn.conv2d(relu, kernel2, padding='SAME',  strides=(1, 1, 1, 1))
        convolution_normalised2 = tf.layers.batch_normalization(convolution2, training=self.is_train)
        relu2 = tf.nn.relu(convolution_normalised2)
        self.cnn = tf.nn.max_pool(relu2, (1, 1, 2, 1), (1, 1, 2, 1), 'VALID')

        kernel = tf.Variable(tf.truncated_normal([3, 3, 128, 256], stddev=0.1))
        convolution = tf.nn.conv2d(self.cnn, kernel, padding='SAME',  strides=(1, 1, 1, 1))
        convolution_normalised = tf.layers.batch_normalization(convolution, training=self.is_train)
        relu = tf.nn.relu(convolution_normalised)
        kernel2 = tf.Variable(tf.truncated_normal([3, 3, 256, 256], stddev=0.1))
        convolution2 = tf.nn.conv2d(relu, kernel2, padding='SAME',  strides=(1, 1, 1, 1))
        convolution_normalised2 = tf.layers.batch_normalization(convolution2, training=self.is_train)
        relu2 = tf.nn.relu(convolution_normalised2)
        self.cnn = tf.nn.max_pool(relu2, (1, 1, 2, 1), (1, 1, 2, 1), 'VALID')

    def prepare_rnn(self):
        self.rnn = tf.squeeze(self.cnn, axis=[2])

        hidden_cells = 256
        cells = [tf.contrib.rnn.LSTMCell(num_units=hidden_cells, state_is_tuple=True) for i in range(2)]
        stacked = tf.contrib.rnn.MultiRNNCell(cells, state_is_tuple=True)

        bidirectional = tf.nn.bidirectional_dynamic_rnn(cell_fw=stacked, cell_bw=stacked,
                                                        inputs=self.rnn, dtype=self.rnn.dtype)
        forward_direction = bidirectional[0][0]
        backward_direction = bidirectional[0][1]
        concat = tf.expand_dims(tf.concat([forward_direction, backward_direction], 2), 2)

        kernel = tf.Variable(tf.truncated_normal([1, 1, hidden_cells * 2, len(self.characters) + 1], stddev=0.1))
        self.rnn = tf.squeeze(tf.nn.atrous_conv2d(value=concat, filters=kernel, rate=1, padding='SAME'), axis=[2])

    def prepare_ctc(self):
        self.ctc = tf.transpose(self.rnn, [1, 0, 2])
        self.ground_truth_texts = tf.SparseTensor(tf.placeholder(tf.int64, shape=[None, 2]),
                                                  tf.placeholder(tf.int32, [None]), tf.placeholder(tf.int64, [2]))

        self.sequence_length = tf.placeholder(tf.int32, [None])
        self.loss = tf.reduce_mean(tf.nn.ctc_loss(labels=self.ground_truth_texts, inputs=self.ctc,
                                                  sequence_length=self.sequence_length, ctc_merge_repeated=True))

        self.ctc_input = tf.placeholder(tf.float32, shape=[self.max_text_length, None, len(self.characters) + 1])
        self.element_loss = tf.nn.ctc_loss(labels=self.ground_truth_texts, inputs=self.ctc_input,
                                           sequence_length=self.sequence_length, ctc_merge_repeated=True,
                                           ignore_longer_outputs_than_inputs=True)

        self.decoder = tf.nn.ctc_beam_search_decoder(inputs=self.ctc, sequence_length=self.sequence_length,
                                                     beam_width=50, merge_repeated=False)

    def sparse(self, texts):
        indices = []
        values = []
        shape = [len(texts), 0]

        for (element, text) in enumerate(texts):
            label = [self.characters.index(c) for c in text]
            if len(label) > shape[1]:
                shape[1] = len(label)
            for (i, l) in enumerate(label):
                indices.append([element, i])
                values.append(l)

        return indices, values, shape

    def decoder_output(self, ctc_output, batch_size):
        encoded = [[]] * batch_size

        decoded = ctc_output[0][0]

        for (i, j) in enumerate(decoded.indices):
            label = decoded.values[i]
            encoded[j[0]].append(label)

        output = []
        for label in encoded:
            s = str().join([self.characters[c] for c in label])
            output.append(s)

        return output

    def train_single_batch(self, batch):
        batch_size = len(batch.images)
        sparse = self.sparse(batch.sample_texts)

        if self.trained_batches < 10:
            rate = 0.01
        elif self.trained_batches < 10000:
            rate = 0.001
        else:
            rate = 0.0001

        feed = {
            self.input_images: batch.images,
            self.ground_truth_texts: sparse,
            self.sequence_length: [self.max_text_length] * batch_size,
            self.rate: rate,
            self.is_train: True
        }

        loss = self.sess.run([self.optimizer, self.loss], feed)[1]
        self.trained_batches += 1

        return loss

    def infer_single_batch(self, batch):
        batch_size = len(batch.images)

        feed = {
            self.input_images: batch.images,
            self.sequence_length: [self.max_text_length] * batch_size,
            self.is_train: False
        }

        evaluation = self.sess.run([self.decoder, self.ctc], feed)
        decoded_texts = self.decoder_output(evaluation[0], batch_size)

        return decoded_texts

    def save(self):
        Model.snapshot += 1
        if self.inferring:
            self.saver.save(self.sess, 'model/snapshot/', global_step=Model.snapshot)
        else:
            self.saver.save(self.sess, './snapshot/', global_step=Model.snapshot)
