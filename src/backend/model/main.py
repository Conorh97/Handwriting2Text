#!/usr/bin/env python3
import argparse
import editdistance
from Loader import Loader
from Model import Model
from spellchecker import SpellChecker


character_list_path = './character_list.txt'
data_path = './data/'

image_width = 128
image_height = 32
batch_size = 50
max_text_length = 32
epoch_early_stop = 6


def train(model, data_loader):
    epoch = 1
    best_error_rate = float('inf')
    while epoch < 40:
        print('Epoch: {}'.format(epoch))
        data_loader.randomise_training_set()
        while data_loader.has_next():
            batch = data_loader.get_next()
            batch_info = data_loader.get_batch_info()
            loss = model.train_single_batch(batch)

            print("Batch: ({} / {}), Loss: {}".format(batch_info[0], batch_info[1], loss))

        error_rate, accuracy = test(model, data_loader)
        print(error_rate)

        with open('./logs/summary-epoch-{}'.format(epoch), 'w') as f:
            f.write('Error Rate: {}\nAccuracy: {}\n'.format(error_rate, accuracy))

        if error_rate < best_error_rate:
            best_error_rate = error_rate
            model.save()
            with open('accuracy.text', 'w') as f:
                f.write('Accuracy of saved model: {}'.format(error_rate * 100))

        epoch += 1


def test(model, data_loader):
    spell = SpellChecker()
    data_loader.set_validation_set()
    character_error = 0
    character_count = 0
    line_correct = 0
    line_count = 0
    while data_loader.has_next():
        batch = data_loader.get_next()
        batch_info = data_loader.get_batch_info()
        print("Batch: ({} / {})".format(batch_info[0], batch_info[1]))
        predicted = model.infer_single_batch(batch)

        for i in range(len(predicted)):
            print(batch.sample_texts[i])
            corrected = spell.correction(predicted[i])
            print(corrected)
            if batch.sample_texts[i] == corrected:
                line_correct += 1
            line_count += 1
            error = editdistance.eval(corrected, batch.sample_texts[i])
            character_error += error
            character_count += len(batch.sample_texts[i])

    print('Character error: {}\nLine accuracy: {}'.format((character_error / character_count) * 100,
                                                          (line_correct / line_count) * 100))
    return (character_error / character_count), (line_correct / line_count)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', action='store_true')
    parser.add_argument('--test', action='store_true')
    parser.add_argument('-g', action='store_true')
    args = parser.parse_args()

    if args.train or args.test:
        data_loader = Loader(data_path, batch_size, (image_width, image_height), max_text_length)

        model = Model(image_width, image_height, batch_size, data_loader.character_list, max_text_length, args.g)
        if args.train:
            train(model, data_loader)
        else:
            test(model, data_loader)
    else:
        print('Required parameters not found; must pass either "--train" or "--test"')


if __name__ == '__main__':
    main()
