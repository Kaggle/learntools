# IMPORTS #
import math, os, random

import matplotlib.pyplot as plt
from matplotlib import gridspec
from itertools import product, chain
from skimage import draw, transform

import numpy as np
import tensorflow as tf


# SETUP #

# Ensure reproducibility #
def set_seed(seed=31415):
    np.random.seed(seed)
    tf.random.set_seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    os.environ['TF_DETERMINISTIC_OPS'] = '1'

def set_style():
    # plt.rc('figure', autolayout=True)
    # plt.rc('axes', labelweight='bold', labelsize='large',
    #        titleweight='bold', titlesize=22, titlepad=10)
    # plt.rc('image', cmap='magma')
    # TODO: def set_style(). create a style dictionary for rcparams
    pass


## VISUALIZATION ##

# Classification #

def get_labels(model, dataset,
               probabilities=None, type='binary'):
    # Predicted labels
    if probabilities is None:
        probabilities = model.predict(dataset)
    if type is 'binary':
        predicted_labels = np.rint(probabilities).astype('uint8')
    elif type is 'sparse':
        predicted_labels = np.argmax(probabilities, axis=-1).astype('uint8')

    # True labels
    num_labels = len(probabilities)
    true_labels = dataset.map(lambda image, label: label)
    true_labels = next(iter(true_labels.unbatch().batch(num_labels)))
    true_labels = true_labels.numpy()

    return true_labels, predicted_labels
    
def show_predictions(model, dataset, dataset_info):
    # TODO: show predictions
    pass


# Feature Extraction #

def show_kernel(kernel, label=True, digits=None, text_size=28):
    # Format kernel
    kernel = np.array(kernel)
    if digits is not None:
        kernel = kernel.round(digits)

    # Plot kernel
    cmap = plt.get_cmap('Blues_r')
    plt.imshow(kernel, cmap=cmap)
    rows, cols = kernel.shape
    thresh = (kernel.max()+kernel.min())/2
    # Optionally, add value labels
    if label:
        for i, j in product(range(rows), range(cols)):
            val = kernel[i, j]
            color = cmap(0) if val > thresh else cmap(255)
            plt.text(j, i, val, 
                     color=color, size=text_size,
                     horizontalalignment='center', verticalalignment='center')
    plt.xticks([])
    plt.yticks([])

def extract_feature(image, kernel, pool_size=2):
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(filters=1,
                               kernel_size=kernel.shape,
                               padding='same',
                               use_bias=False,
                               input_shape=image.shape),
        tf.keras.layers.Activation('relu'),
        tf.keras.layers.MaxPool2D(pool_size=pool_size,
                                  padding='same'),
    ])

    layer_filter, layer_detect, layer_condense = model.layers
    kernel = tf.reshape(kernel, [*kernel.shape, 1, 1])
    layer_filter.set_weights([kernel])

    # Format for TF
    image = tf.expand_dims(image, axis=0)
    image = tf.image.convert_image_dtype(image, dtype=tf.float32) 
    
    # Extract Feature
    image_filter = layer_filter(image)
    image_detect = layer_detect(image_filter)
    image_condense = layer_condense(image_detect)
    return tf.squeeze(image_condense, axis=0)

def show_extraction(image,
                    kernel,
                    conv_stride=1,
                    conv_padding='valid',
                    activation='relu',
                    pool_size=2,
                    pool_stride=2,
                    pool_padding='same',
                    figsize=(10, 10),
                    subplot_shape=(2, 2),
                    ops=['Input', 'Filter', 'Detect', 'Condense'],
                    gamma=1.0):
    # Create Layers
    model = tf.keras.Sequential([
                    tf.keras.layers.Conv2D(
                        filters=1,
                        kernel_size=kernel.shape,
                        strides=conv_stride,
                        padding=conv_padding,
                        use_bias=False,
                        input_shape=image.shape,
                    ),
                    tf.keras.layers.Activation(activation),
                    tf.keras.layers.MaxPool2D(
                        pool_size=pool_size,
                        strides=pool_stride,
                        padding=pool_padding,
                    ),
                   ])

    layer_filter, layer_detect, layer_condense = model.layers
    kernel = tf.reshape(kernel, [*kernel.shape, 1, 1])
    layer_filter.set_weights([kernel])

    # Format for TF
    image = tf.expand_dims(image, axis=0)
    image = tf.image.convert_image_dtype(image, dtype=tf.float32) 
    
    # Extract Feature
    image_filter = layer_filter(image)
    image_detect = layer_detect(image_filter)
    image_condense = layer_condense(image_detect)
    
    images = {}
    if 'Input' in ops:
        images.update({'Input': (image, 1.0)})
    if 'Filter' in ops:
        images.update({'Filter': (image_filter, 1.0)})
    if 'Detect' in ops:
        images.update({'Detect': (image_detect, gamma)})
    if 'Condense' in ops:
        images.update({'Condense': (image_condense, gamma)})
    
    # Plot
    plt.figure(figsize=figsize)
    for i, title in enumerate(ops):
        image, gamma = images[title]
        plt.subplot(*subplot_shape, i+1)
        plt.imshow(tf.image.adjust_gamma(tf.squeeze(image), gamma))
        plt.axis('off')
        plt.title(title)


# Feature Maps #

def show_feature_maps(image, model, layer_name, offset=0,
                      rows=3, cols=3, width=12,
                      gamma=0.5):
    
    outputs = model.get_layer(layer_name).output
    activation_model = tf.keras.Model(inputs=model.input,
                                      outputs=outputs)
    feature_maps = activation_model(tf.expand_dims(image, axis=0))

    if rows is None:
        num_features = feature_maps.shape[3]
        rows = math.ceil(num_features / cols)
    
    gs = gridspec.GridSpec(rows, cols, wspace=0.01, hspace=0.01)
    plt.figure(figsize=(width, (width * rows) / cols))
    for f, (r, c) in enumerate(product(range(rows), range(cols))):
        plt.subplot(gs[r, c])
        plt.imshow(
            tf.image.adjust_gamma(
                feature_maps[0][:,:,f+offset],
                gamma,
            ))
        plt.axis('off')


# Image Utilities #

def read_image(path, channels=0):
    image = tf.io.read_file(path)
    image = tf.io.decode_image(image, channels=channels)
    image = tf.image.convert_image_dtype(image, dtype=tf.float32)
    return image

def show_image(image):
    image = tf.squeeze(image)
    plt.imshow(image)
    plt.axis('off')


# PREDEFINED FEATURES #

def two_dots(size, x=3, y=5):
    two_dots = np.zeros(size)
    two_dots[x, y] = 1
    two_dots[y, x] = 1
    return two_dots
        
def circle(size, val=None, r_shrink=0):
    circle = np.zeros([size[0]+1, size[1]+1])
    rr, cc = draw.circle_perimeter(
        size[0]//2, size[1]//2,
        radius=size[0]//2 - r_shrink,
        shape=[size[0]+1, size[1]+1],
    )
    if val is None:
        circle[rr, cc] = np.random.uniform(size=circle.shape)[rr, cc]
    else:
        circle[rr, cc] = val
    circle = transform.resize(circle, size, order=0)
    return circle

def random_map(size, scale=0.5, decay_power=1.0):
    h, w = size
    img = init_buffer(h, w, scale=scale)
    img = fft_to_rgb([1, h, w, 3], img, decay_power=decay_power)
    img = to_valid_rgb(img)
    img = img[0,:,:,0]
    return img


# PREDEFINED KERNELS #

# Edge detection
edge = tf.constant(
    [[-1, -1, -1],
     [-1, 8, -1],
     [-1, -1, -1]],
)

# Blur
blur = tf.constant(
    [[0.0625, 0.125, 0.0625],
     [0.125, 0.25, 0.125],
     [0.0625, 0.125, 0.0625]],
)

# Bottom sobel
bottom_sobel = tf.constant(
    [[-1, -2, -1],
     [0, 0, 0],
     [1, 2, 1]],
)

# Emboss South-East
emboss = tf.constant(
    [[-2, -1, 0],
     [-1, 1, 1],
     [0, 1, 2]],
)

# Sharpen
sharpen = tf.constant(
    [[0, -1, 0],
     [-1, 5, -1],
     [0, -1, 0]],
)

# Gaussian (blur) kernel
def gaussian(kernlen=3, std=1, normalize=True):
    """Returns a 2D Gaussian kernel array."""
    gkern1d = signal.gaussian(kernlen, std=std).T
    if normalize:
        gkern1d /= np.trapz(gkern1d)
    gkern2d = np.outer(gkern1d, gkern1d)
    return gkern2d


def random_kernel(model, layer=None):
    """Choose a random convolutional kernel from a model."""

    if layer is not None:
        # get specified layer
        layer = model.get_layer(layer)
    else:
        # choose a random convolutional layer
        layer = random.choice(
            [layer for layer in model.layers
             if layer.__class__.__name__ is 'Conv2D']
        )

    # and get its filters
    filters = layer.get_weights()[0]
    # choose an input channel
    input_index = np.random.randint(0, filters.shape[2])
    # choose a filter
    filter_index = np.random.randint(0, filters.shape[3])
    
    # get kernel and normalize
    krn = filters[:, :, input_index, filter_index]
    krn -= krn.mean()
    krn /= (krn.std() + 1e-5)
    krn = krn.round(decimals=1)
    
    print("Layer: {}  Input Channel: {}  Filter: {}"
          .format(layer.name, input_index, filter_index))
    return krn
