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
    shape = [1, h, w, 3]
    fft = fft_scale(h, w, decay_power=decay_power)
    img = init_buffer(h, w, scale=scale)
    img = fft_to_rgb(shape, img, fft)
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


# Transform Utilities #
@tf.function
def random_transform(image, jitter=0, rotate=0, scale=1, **kwargs):
    jx = tf.random.uniform([], -jitter, jitter)
    jy = tf.random.uniform([], -jitter, jitter)
    r = tf.random.uniform([], -rotate, rotate)
    s = tf.random.uniform([], 1.0, scale)
    image = apply_affine_transform(
        image,
        theta=r,
        tx=jx, ty=jy,
        zx=s, zy=s,
        **kwargs,
    )
    return image

@tf.function
def apply_affine_transform(x,
                           theta=0, tx=0, ty=0, shear=0, zx=1, zy=1,
                           row_axis=0, col_axis=1, channel_axis=2,
                           fill_method='reflect', cval=0.,
                           interpolation_method='nearest'):
    """ Apply an affine transformation to an image x. """

    theta = tf.convert_to_tensor(theta, dtype=tf.float32)
    tx = tf.convert_to_tensor(tx, dtype=tf.float32)
    ty = tf.convert_to_tensor(ty, dtype=tf.float32)
    shear = tf.convert_to_tensor(shear, dtype=tf.float32)
    zx = tf.convert_to_tensor(zx, dtype=tf.float32)
    zy = tf.convert_to_tensor(zy, dtype=tf.float32)

    transform_matrix = _get_inverse_affine_transform(
        theta,
        tx, ty,
        shear,
        zx, zy,
    )

    x = _apply_inverse_affine_transform(
        x,
        transform_matrix,
        fill_method=fill_method,
        interpolation_method=interpolation_method,
    )

    return x


# adapted from https://github.com/keras-team/keras-preprocessing/blob/master/keras_preprocessing/image/affine_transformations.py
# MIT License: https://github.com/keras-team/keras-preprocessing/blob/master/LICENSE
@tf.function
def _get_inverse_affine_transform(theta, tx, ty, shear, zx, zy):
    """ Construct the inverse of the affine transformation matrix with the given transformations. 
    
    The transformation is taken with respect to the usual right-handed coordinate system."""

    transform_matrix = tf.eye(3, dtype=tf.float32)

    if theta != 0:
        theta = theta * math.pi / 180 # convert degrees to radians
        # this is 
        rotation_matrix = tf.convert_to_tensor(
            [[tf.math.cos(theta), tf.math.sin(theta), 0],
             [-tf.math.sin(theta), tf.math.cos(theta), 0],
             [0, 0, 1]],
            dtype=tf.float32)
        transform_matrix = rotation_matrix

    if tx != 0 or ty != 0:
        shift_matrix = tf.convert_to_tensor(
            [[1, 0, -tx],
             [0, 1, -ty],
             [0, 0, 1]],
            dtype=tf.float32)
        if transform_matrix is None:
            transform_matrix = shift_matrix
        else:
            transform_matrix = tf.matmul(transform_matrix, shift_matrix)

    if shear != 0:
        shear = shear * math.pi / 180 # convert degrees to radians
        shear_matrix = tf.convert_to_tensor(
            [[1, tf.math.sin(shear), 0],
             [0, tf.math.cos(shear), 0],
             [0, 0, 1]],
            dtype=tf.float32)
        if transform_matrix is None:
            transform_matrix = shear_matrix
        else:
            transform_matrix = tf.matmul(transform_matrix, shear_matrix)

    if zx != 1 or zy != 1:
        # need to assert !=0
        zoom_matrix = tf.convert_to_tensor(
            [[1/zx, 0, 0],
             [0, 1/zy, 0],
             [0, 0, 1]],
            dtype=tf.float32)
        if transform_matrix is None:
            transform_matrix = zoom_matrix
        else:
            transform_matrix = tf.matmul(transform_matrix, zoom_matrix)
            
    return transform_matrix

@tf.function
def _apply_inverse_affine_transform(A, Ti, fill_method, interpolation_method):
    """Perform an affine transformation of the image A defined by a
transform whose inverse is Ti. The matrix Ti is assumed to be in
homogeneous coordinate form.

    Available fill methods are "replicate" and "reflect" (default).
    Available interpolation method is "nearest".

    """
    nrows, ncols, _ = A.shape

    # Create centered coordinate grid
    x = tf.range(ncols*nrows) % ncols
    x = tf.cast(x, dtype=tf.float32) - ((ncols-1)/2) # center
    y = tf.range(ncols*nrows) // ncols
    y = tf.cast(y, dtype=tf.float32) - ((nrows-1)/2) # center
    y = -y # left-handed to right-handed coordinates
    z = tf.ones([ncols*nrows], dtype=tf.float32)
    grid = tf.stack([x, y, z])

    # apply transformation
    # x, y, _ = tf.matmul(Ti, grid)
    xy = tf.matmul(Ti, grid)
    x = xy[0, :]
    y = xy[1, :]
    
    # convert coordinates to (approximate) indices
    i = -y + ((nrows-1)/2)
    j = x + ((ncols-1)/2)

    # replicate: 111|1234|444
    if fill_method is 'replicate':
        i = tf.clip_by_value(i, 0.0, nrows-1)
        j = tf.clip_by_value(j, 0.0, ncols-1)
    # reflect: 432|1234|321
    elif fill_method is 'reflect':
        i = _reflect_index(i, nrows-1)
        j = _reflect_index(j, ncols-1)
        
    # nearest neighbor interpolation
    grid = tf.stack([i, j])
    grid = tf.round(grid)
    grid = tf.cast(grid, dtype=tf.int32)
    B = tf.gather_nd(A, tf.transpose(grid))
    B = tf.reshape(B, A.shape)

    return B

@tf.function
def _reflect_index(i, n):
    """Reflect the index i across dimensions [0, n]."""
    i = tf.math.floormod(i-n, 2*n)
    i = tf.math.abs(i - n)
    return tf.math.floor(i)


# Random Image Buffers #
def init_buffer(height, width=None, batches=1, channels=3, scale=0.01, fft=True):
    """Initialize an image buffer."""
    width = width or height
    shape = [batches, height, width, channels]
    fn = init_fft if fft else init_pixel
    
    buffer = fn(shape, scale)
    
    return tf.Variable(buffer, trainable=True)

def init_pixel(shape, scale=None):
    batches, h, w, ch = shape
#     initializer = tf.initializers.VarianceScaling(scale=scale)
    initializer = tf.random.uniform
    buffer = initializer(shape=[batches, h, w, ch],
                         dtype=tf.float32)
    return buffer


def init_fft(shape, scale=0.1):
    """Initialize FFT image buffer."""
    
    batch, h, w, ch = shape
    freqs = rfft2d_freqs(h, w)
    init_val_size = (2, batch, ch) + freqs.shape

    buffer = np.random.normal(size=init_val_size, scale=scale).astype(np.float32)
    return buffer


# Adapted from https://github.com/tensorflow/lucid/blob/master/lucid/optvis/param/spatial.py
# and https://github.com/elichen/Feature-visualization/blob/master/optvis.py
def rfft2d_freqs(h, w):
    """Computes 2D spectrum frequencies."""

    fy = np.fft.fftfreq(h)[:, np.newaxis]
    # when we have an odd input dimension we need to keep one additional
    # frequency and later cut off 1 pixel
    if w % 2 == 1:
        fx = np.fft.fftfreq(w)[: w // 2 + 2]
    else:
        fx = np.fft.fftfreq(w)[: w // 2 + 1]
        
    return np.sqrt(fx * fx + fy * fy)

def fft_scale(h, w, decay_power=1.0):
    freqs = rfft2d_freqs(h, w)
    scale = 1.0 / np.maximum(freqs, 1.0 / max(w, h)) ** decay_power
    scale *= np.sqrt(w * h)
    return tf.convert_to_tensor(scale, dtype=tf.complex64)

def fft_to_rgb(shape, buffer, fft_scale):
    """Convert FFT spectrum buffer to RGB image buffer."""
    
    batch, h, w, ch = shape

    spectrum = tf.complex(buffer[0], buffer[1]) * fft_scale
    image = tf.signal.irfft2d(spectrum)
    image = tf.transpose(image, (0, 2, 3, 1))
    
    # in case of odd spatial input dimensions we need to crop
    image = image[:batch, :h, :w, :ch]
    image = image / 4.0  # TODO: is that a magic constant?
    
    return image

# Color Transforms #
color_correlation_svd_sqrt = np.asarray(
    [[0.26, 0.09, 0.02],
     [0.27, 0.00, -0.05],
     [0.27, -0.09, 0.03]]
).astype("float32")
max_norm_svd_sqrt = np.max(np.linalg.norm(color_correlation_svd_sqrt, axis=0))
color_correlation_normalized = color_correlation_svd_sqrt / max_norm_svd_sqrt
color_mean = np.asarray([0.485, 0.456, 0.406])
color_std = np.asarray([0.229, 0.224, 0.225])

def correlate_color(image):
    image_flat = tf.reshape(image, [-1, 3])
    image_flat = tf.matmul(image_flat, color_correlation_normalized.T)
    image = tf.reshape(image_flat, tf.shape(image))
    return image

def normalize(image):
    return (image - color_mean) / color_std

def to_valid_rgb(image, crop=False):
    if crop:
        image = image[:, 25:-25, 25:-25, :]
    image = correlate_color(image)
    image = tf.nn.sigmoid(image)
    return image
