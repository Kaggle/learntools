import numpy as np
import matplotlib.pyplot as plt
import os
import tensorflow as tf
import time


def visualize_training_generator(train_step_num, start_time, plottables, undo_normalization=False):
    """Visualize generator outputs during training.

    Args:
        train_step_num: The training step number. A python integer.
        start_time: Time when training started. The output of `time.time()`. A
            python float.
        plottables: Data to plot. Numpy array or list of numpy arrays,
            usually from an evaluated TensorFlow tensor.
    """
    print('Training step: %i' % train_step_num)
    time_since_start = (time.time() - start_time) / 60.0
    print('Time since start: %f m' % time_since_start)
    print('Steps per min: %f' % (train_step_num / time_since_start))
    if type(plottables) == list:
        plottables = np.dstack(plottables)
    plottables = np.squeeze(plottables)
    if undo_normalization:
        plottables = ((plottables * 128) + 128).astype(np.uint8)

    plt.figure(figsize=(15,15))
    plt.axis('off')
    plt.imshow(plottables, cmap='gray')
    plt.show()

def dataset_to_stream(inp, batch_size):
    with tf.device('/cpu:0'):
        batched = inp.apply(tf.contrib.data.batch_and_drop_remainder(batch_size))
        data_feeder = batched.repeat().make_one_shot_iterator().get_next()
    return data_feeder

def parse_img_dir(img_dir, output_height, output_width, batch_size, max_epochs):
    '''Original images are 256 x 512 x 3. Left half is original image, right is semantic seg'''

    def parse_img(fname):
        img_strings = tf.read_file(fname)
        imgs_decoded = tf.image.decode_jpeg(img_strings, channels=3)
        output = tf.image.resize_images(imgs_decoded, [output_height, 2 * output_width])
        output = (output - 128) / 128
        return output

    file_list = os.listdir(img_dir)
    img_paths = [os.path.join(img_dir, fname) for fname in file_list]
    img_paths_dataset = tf.data.Dataset.from_tensor_slices(img_paths)
    img_dataset = img_paths_dataset.map(parse_img)
    left_imgs = img_dataset.map(lambda x: x[:, :output_width, :])
    right_imgs = img_dataset.map(lambda x: x[:, output_width:, :])
    left_provider = dataset_to_stream(left_imgs, batch_size)
    right_provider = dataset_to_stream(right_imgs, batch_size)
    return left_provider, right_provider
