# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""Split the SIGNS dataset into train/dev/test and resize images to 64x64.

The SIGNS dataset comes in the following format:
    train_signs/
        0_IMG_5864.jpg
        ...
    test_signs/
        0_IMG_5942.jpg
        ...

Original images have size (3024, 3024).
Resizing to (64, 64) reduces the dataset size from 1.16 GB to 4.7 MB, and loading smaller images
makes training faster.

We already have a test set created, so we only need to split "train_signs" into train and dev sets.
Because we don't have a lot of images and we want that the statistics on the dev set be as
representative as possible, we'll take 20% of "train_signs" as dev set.
"""

import argparse
import random
import os

from PIL import Image
from tqdm import tqdm
import shutil


SIZE = 64

parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', default='/home/yuanzhihui/mypro/keras-yolo3/bridge', help="Directory with the SIGNS dataset")
parser.add_argument('--output_dir', default='/home/yuanzhihui/mypro/keras-yolo3/bridge/split', help="Where to write the new data")


# def resize_and_save(filename, output_dir, size=SIZE):
#     """Resize the image contained in `filename` and save it to the `output_dir`"""
#     image = Image.open(filename)
#     # Use bilinear interpolation instead of the default "nearest neighbor" method
#     # image = image.resize((size, size), Image.BILINEAR)
#     image.save(os.path.join(output_dir, filename.split('/')[-1]))


if __name__ == '__main__':
    args = parser.parse_args()

    assert os.path.isdir(args.data_dir), "Couldn't find the dataset at {}".format(args.data_dir)

    # Define the data directories

    train_data_dir = os.path.join(args.data_dir, 'top')
    test_data_dir = os.path.join(args.data_dir, 'wai')
    xml_path = os.path.join(args.data_dir, 'xml')

    # Get the filenames in each directory (train and test)
    filenames_images = os.listdir(train_data_dir)
    filenames = [os.path.join(train_data_dir, f) for f in filenames_images if f.endswith('.jpg')]


    random.seed(230)
    filenames.sort()
    random.shuffle(filenames)

    split = int(0.8 * len(filenames))
    train_filenames = filenames[:split]
    dev_filenames = filenames[split:]



    test_dir = os.listdir(test_data_dir)
    test_data_images = []
    for dir in test_dir:
        data_path = os.path.join(test_data_dir,dir)
        test_images = os.listdir(data_path)
        test_data_images.extend(test_images)
        test_filenames = [os.path.join(data_path,f) for f in test_images if f.endswith('.jpg')]


        random.seed(230)
        test_filenames.sort()
        random.shuffle(test_filenames)

        split = int(0.8 * len(test_filenames))
        train_filenames.extend(test_filenames[:split])
        dev_filenames.extend(test_filenames[split:])

    # Split the images in 'train_signs' into 80% train and 20% dev
    # Make sure to always shuffle with a fixed seed so that the split is reproducible

    filenames = {'train': train_filenames,
                 'dev': dev_filenames}
                 #'test': test_filenames}

    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)
    else:
        print("Warning: output dir {} already exists".format(args.output_dir))



    # Preprocess train, dev and test
    for split in ['train', 'dev']:

        output_dir_split = os.path.join(args.output_dir, '{}'.format(split))
        if not os.path.exists(output_dir_split):
            os.mkdir(output_dir_split)
        else:
            print("Warning: dir {} already exists".format(output_dir_split))



        output_dir_split_images = os.path.join(args.output_dir, '{}/JPEGImages'.format(split))
        if not os.path.exists(output_dir_split_images):
            os.mkdir(output_dir_split_images)
        else:
            print("Warning: dir {} already exists".format(output_dir_split_images))



        output_dir_split_annote = os.path.join(args.output_dir, '{}/Annotations'.format(split))
        if not os.path.exists(output_dir_split_annote):
            os.mkdir(output_dir_split_annote)
        else:
            print("Warning: dir {} already exists".format(output_dir_split_annote))

        print("Processing {} data, saving preprocessed data to {}".format(split, output_dir_split_images))
        for filename in tqdm(filenames[split]):
            # resize_and_save(filename, output_dir_split, size=SIZE)
            shutil.copy(filename, output_dir_split_images)
            # pass


        print("Processing {} data, saving preprocessed data to {}".format(split, output_dir_split_images))
        for filename in tqdm(filenames[split]):
            names = os.path.splitext(filename)[0].split('/')[-1]
            xml_names = os.path.join(xml_path,names + '.xml')
            shutil.copy(xml_names,output_dir_split_annote)

    print("Done building dataset")
