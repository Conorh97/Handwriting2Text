import os
import random
import numpy as np
import cv2


class SingleSample(object):

    def __init__(self, text, file_path):
        self.text = text
        self.file_path = file_path


class Batch(object):

    def __init__(self, sample_texts, images):
        self.sample_texts = sample_texts
        self.images = np.stack(images, axis=0)


class Loader(object):

    def __init__(self, file_path, batch_size, image_size, max_length):
        self.current_index = 0
        self.batch_size = batch_size
        self.image_size = image_size
        self.samples = []
        characters = set()

        with open("{}lines.txt".format(file_path)) as f:
            lines = [line.strip("\n") for line in f.readlines() if len(line) > 2]

        for line in lines:
            if not line or line[0] == "#":
                continue

            elements = line.strip().split(" ")
            file_name_split = elements[0].split("-")
            file_name = file_path + "lines/" + file_name_split[0] + "/" + file_name_split[0] \
                        + "-" + file_name_split[1] + "/" + elements[0] + ".png"
            gt_text = self.truncate(" ".join(elements[8:]), max_length)
            characters = characters.union(set(list(gt_text)))

            if not os.path.getsize(file_name):
                continue

            self.samples.append(SingleSample(gt_text, file_name))

        split_index = int(0.95 * len(self.samples))

        self.training_set = [sample.text for sample in self.samples[:split_index]]
        self.testing_set = [sample.text for sample in self.samples[split_index:]]

        self.samples_per_epoch = 25000
        self.randomise_training_set()

        self.character_list = sorted(list(characters))

    def truncate(self, text, max_length):
        text_cost = 0
        for i in range(len(text)):
            if i != 0 and text[i] == text[i - 1]:
                text_cost += 2
            else:
                text_cost += 1
            if text_cost > max_length:
                return text[:i]

        return text

    def randomise_training_set(self):
        self.current_index = 0
        random.shuffle(self.training_set)
        self.samples = self.training_set[:self.samples_per_epoch]

    def set_validation_set(self):
        self.current_index = 0
        self.samples = self.testing_set

    def has_next(self):
        return self.current_index + self.batch_size <= len(self.samples)

    def get_next(self):
        batch_range = range(self.current_index, self.current_index + self.batch_size)
        gt_texts = [self.samples[i].text for i in batch_range]
        images = []
        for i in batch_range:
            preprocessed_image = self.preprocess(self.samples[i].filePath)
            images.append(preprocessed_image)
        self.current_index += self.batch_size
        return Batch(gt_texts, images)

    def preprocess(self, file_path):
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        width = self.image_size[0]
        height = self.image_size[1]

        processed = cv2.resize(image, (width, height))
        return processed
