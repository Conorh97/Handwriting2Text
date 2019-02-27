import sys
import argparse
import cv2
import editdistance
from Loader import Loader, Batch
from Model import Model


character_list_path = './character_list.txt'
data_path = './data/'

image_width = 512
image_height = 32
batch_size = 50
max_text_length = 32

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", action="store_true")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    if args.train or args.test:
        data_loader = Loader(data_path, batch_size, (image_width, image_height), max_text_length)
    else:
        print('Required parameters not found; must pass either "--train" or "--test"')


if __name__ == '__main__':
    main()
