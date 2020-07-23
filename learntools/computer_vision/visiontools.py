import math, os
import numpy as np
import random
import matplotlib.pyplot as plt
import tensorflow as tf
from functools import singledispatch
from itertools import product, chain
from matplotlib import gridspec
from skimage import draw, transform
from scipy import signal


# TFDS might not be installed
try:
    import tensorflow_datasets as tfds
except:
    os.system("pip install --quiet '../input/computer-vision-resources/tensorflow_datasets-3.2.1-py3-none-any.whl'")
    import tensorflow_datasets as tfds

## Dataset ##

_DATA_OPTIONS = ['full', 'simple', 'simple_complement']
_SIMPLE_LABELS = ['Car', 'Truck']
_SIMPLE_LABEL_DICT = {
    'Sedan': 'Car',
    'Coupe': 'Car',
    'Cab': 'Truck',
    'SUV': 'Truck',
}
_SIMPLE_COMPLEMENT_LABELS = [
    'Hatchback',
    'Convertible',
    'Wagon',
    'Minivan',
    'Van',
]


class StanfordCarsConfig(tfds.core.BuilderConfig):
    """BuilderConfig for StanfordCars."""
    @tfds.core.disallow_positional_args
    def __init__(self, selection, **kwargs):
        """Constructs a StanfordCars config."""

        if selection not in _DATA_OPTIONS:
            raise ValueError('selection must be one of %s' % _DATA_OPTIONS)

        super().__init__(version=tfds.core.Version('1.0.0'),
                         **kwargs)
        self.selection = selection


class StanfordCars(tfds.image.Cars196):
    """The Stanford Cars dataset adapted for Kaggle's Computer Vision course."""
    BUILDER_CONFIGS = [
        StanfordCarsConfig(
            name='simple',
            description="'Cars and Trucks' binary classification.",
            selection='simple',
        ),
        StanfordCarsConfig(
            name='full',
            description="Full version",
            selection='full',
        ),
        StanfordCarsConfig(
            name='simple_complement',
            description="Everything else.",
            selection='simple_complement',
        ),
        
    ]
    def _info(self):
        """Define the dataset info."""
        if self.builder_config.selection is 'simple':
            ds_info = super()._info()
            features_dict = ds_info.features._feature_dict
            features_dict['label'] = tfds.features.ClassLabel(names=_SIMPLE_LABELS)
            features = tfds.features.FeaturesDict(features_dict)
            return tfds.core.DatasetInfo(
                builder=self,
                description=ds_info.description,
                features=features,
                supervised_keys=ds_info.supervised_keys,
                homepage=ds_info.homepage,
                citation=ds_info.citation,
            )
        if self.builder_config.selection is 'simple_complement':
            ds_info = super()._info()
            features_dict = ds_info.features._feature_dict
            features_dict['label'] = tfds.features.ClassLabel(names=_SIMPLE_COMPLEMENT_LABELS)
            features = tfds.features.FeaturesDict(features_dict)
            return tfds.core.DatasetInfo(
                builder=self,
                description=ds_info.description,
                features=features,
                supervised_keys=ds_info.supervised_keys,
                homepage=ds_info.homepage,
                citation=ds_info.citation,
            )        
        else:
            return super()._info()

    def _generate_examples(self, **kwargs):
        """Generate examples for simple or full config."""
        if self.builder_config.selection is 'simple':
            for image_name, features in super()._generate_examples(**kwargs):
                # names are 'Make Model Type Year'
                # so get the type of car
                label = features['label'].split(' ')[-2]
                if label in _SIMPLE_LABEL_DICT:
                    features ={
                        'label': _SIMPLE_LABEL_DICT[label],
#                        'image': _simple_image(features['image']),
                        'image': features['image'],
                        'bbox': features['bbox'],
                    }
                    yield image_name, features
                else:
                    pass
        if self.builder_config.selection is 'simple_complement':
            for image_name, features in super()._generate_examples(**kwargs):
                # names are 'Make Model Type Year'
                # so get the type of car
                label = features['label'].split(' ')[-2]
                if label in _SIMPLE_COMPLEMENT_LABELS:
                    features ={
                        'label': label,
#                        'image': _simple_image(features['image']),
                        'image': features['image'],
                        'bbox': features['bbox'],
                    }
                    yield image_name, features
                else:
                    pass
        else:
            for x in super()._generate_examples(**kwargs): yield x

# Unused right now
def _simple_image(filename, bbox):
    image = tfds.core.lazy_imports.skimage.io.imread(
        filename,
        as_gray=False,
    )
    image = tfds.core.lazy_imports.skimage.img_as_ubyte(image)
    image = tf.image.crop_to_bounding_box()
    return image


## PREPROCESSING ##

def _random_crop_to_bounding_box(image, bbox, min_object_covered=1.0,
                                aspect_ratio_range=[0.75, 1.33]):
    bbox = tf.reshape(bbox, [1, 1, -1])
    # Generate a single distorted bounding box.
    begin, size, bbox_for_draw = tf.image.sample_distorted_bounding_box(
            tf.shape(image),
            bounding_boxes=bbox,
            min_object_covered=min_object_covered,
            aspect_ratio_range=aspect_ratio_range)
    image = tf.slice(image, begin, size)
    return image

def make_preprocessor(size):
    # Generic
    @singledispatch
    def preprocessor(example):
        raise TypeError

    # Dispatch on supervised examples, type: (image, label)
    @preprocessor.register(tuple)
    def _(example: tuple):
        image, label = example
        # Convert Int to Float and scale from [0, 255] to [0.0, 1.0]
        image = tf.image.convert_image_dtype(image,
                                             dtype=tf.float32)
        # Resize the image to size=[width, height]
        image = tf.image.resize(image,
                                size=size,
                                method='nearest',
                                preserve_aspect_ratio=False)
        return image, label

    # Dispatch on unsupervised examples with bounding boxes
    @preprocessor.register(dict)
    def _(example: dict):
        image = example['image']
        bbox = example['bbox']
        label = example['label']
        
        image = tf.image.convert_image_dtype(image, dtype=tf.float32)
        image = _random_crop_to_bounding_box(image, bbox)
        image = tf.image.resize_with_pad(image,
                                         target_height=size[0],
                                         target_width=size[1],
                                         method='nearest')
        return image, label
    return preprocessor

def make_augmentor(# rotation_range=0,
                   # width_shift_range=0,
                   # height_shift_range=0,
                   brightness_delta=None,
                   contrast_range=None,
                   hue_delta=None,
                   saturation_range=None,
                   # shear_range=0.0,
                   # zoom_range=0.0,
                   # channel_shift_range=0.0,
                   # fill_mode='nearest',
                   horizontal_flip=False,
                   vertical_flip=False,
                   seed = 31415):
    def augmentor(image, label):
        # TODO - assert valid parameter values
        if brightness_delta is not None:
            image = tf.image.random_brightness(image,
                                               max_delta=brightness_delta, seed=seed)
        if contrast_range is not None:
            image = tf.image.random_contrast(image,
                                             lower=contrast_range[0],
                                             upper=contrast_range[1])
        if hue_delta is not None:
            image = tf.image.random_hue(image, 
                                        max_delta=hue_delta, seed=seed)
        if saturation_range is not None:
            image = tf.image.random_saturation(image,
                                               lower=saturation_range[0],
                                               upper=saturation_range[1], seed=seed)
        if horizontal_flip:
            image = tf.image.random_flip_left_right(image, seed=seed)

        if vertical_flip:
            image = tf.image.random_flip_up_down(image, seed=seed)

        return image, label
    return augmentor

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

    transform_matrix = _get_inverse_affine_transform(theta,
                                                     tx, ty,
                                                     shear,
                                                     zx, zy)

    if transform_matrix is not None:
        x = _apply_inverse_affine_transform(x,
                                            transform_matrix,
                                            fill_method=fill_method,
                                            interpolation_method=interpolation_method)

    return x


# adapted from https://github.com/keras-team/keras-preprocessing/blob/master/keras_preprocessing/image/affine_transformations.py
# MIT License: https://github.com/keras-team/keras-preprocessing/blob/master/LICENSE
def _get_inverse_affine_transform(theta, tx, ty, shear, zx, zy):
    """ Construct the inverse of the affine transformation matrix with the given transformations. 
    
    The transformation is taken with respect to the usual right-handed coordinate system."""

    transform_matrix = None

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
    x, y, _ = Ti @ grid
    
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

def _reflect_index(i, n):
    """Reflect the index i across dimensions [0, n]."""
    i = tf.math.floormod(i-n, 2*n)
    i = tf.math.abs(i - n)
    return tf.math.floor(i)


## CALLBACKS ##

def exponential_lr(epoch,
         start_lr = 0.00001,
         min_lr = 0.00001,
         max_lr = 0.00005,
         num_replicas_in_sync = 1,
         rampup_epochs = 5,
         sustain_epochs = 0,
         exp_decay = 0.8):
    max_lr = max_lr*num_replicas_in_sync
    def lr(epoch,
           start_lr,
           min_lr,
           max_lr,
           rampup_epochs,
           sustain_epochs,
           exp_decay):
        # linear increase from start to rampup_epochs
        if epoch < rampup_epochs:
            lr = ((max_lr - start_lr) /
                  rampup_epochs * epoch + start_lr)
        # constant max_lr during sustain_epochs
        elif epoch < rampup_epochs + sustain_epochs:
            lr = max_lr
        # exponential decay towards min_lr
        else:
            lr = ((max_lr - min_lr) *
                  exp_decay**(epoch - rampup_epochs - sustain_epochs) +
                  min_lr)
        return lr
    return lr(epoch,
              start_lr,
              min_lr,
              max_lr,
              rampup_epochs,
              sustain_epochs,
              exp_decay)


# Use like:
# exponential_lr_callback = (
#     tf.keras
#     .callbacks
#     .LearningRateScheduler(lambda epoch: exponential_lr(epoch),
#                            verbose=True)
# )


## VISUALIZATION ##

def set_style():
    # plt.rc('figure', autolayout=True)
    # plt.rc('axes', labelweight='bold', labelsize='large',
    #        titleweight='bold', titlesize=22, titlepad=10)
    # plt.rc('image', cmap='magma')
    # TODO: def set_style(). create a style dictionary for rcparams
    pass


# Dataset #

def show_supervised_examples(ds, ds_info, rows=4, cols=4):
    examples = list(tfds.as_numpy(ds.take(rows * cols)))
    plt.figure(figsize=(15, (15 * rows) // cols))
    for i, (image, label) in enumerate(examples):
        plt.subplot(rows, cols, i+1)
        plt.axis('off')
        plt.imshow(image)
        plt.title(ds_info.features['label'].int2str(label))


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


# Optimization Visualization #


# Model
class OptVis(object):
    def __init__(self, model, layer, filter, neuron=False, size=[128, 128], fft=True, scale=0.01):
        
        # Create activation model
        activations = model.get_layer(layer).output
        if len(activations.shape) == 4:
            activations = activations[:,:,:,filter]
        if neuron:
            _, y, x = activations.shape
            activations = activations[:, y//2, x//2]
        else:
            raise ValueError("Activation shapes other than 4 not implemented.")
        self.activation_model = keras.Model(
            inputs=model.inputs,
            outputs=activations
        )

        # Create buffer with random RGB values
        self.shape = [1, *size, 3]
        self.fft = fft
        self.image = init_buffer(height=size[0], width=size[1], fft=fft, scale=scale)

    def __call__(self):
        # Preprocessing
        # 

        image = self.activation_model(self.image)
        
        return image

    def compile(self, optimizer):
        self.optimizer = optimizer
    
    def train_step(self):
        # Compute loss
        with tf.GradientTape() as tape:
            image = self.image
            if self.fft:
                image = fft_to_rgb(shape=self.shape, buffer=image)
            image = to_valid_rgb(image)
            image = random_transform(
                tf.squeeze(image),
                jitter=8, 
                scale=1.1,
                rotate=1.0,
                fill_method='reflect')
            image = tf.expand_dims(image, 0)
            loss = clip_gradients(score(self.activation_model(image)))
    
        # Apply gradient
        grads = tape.gradient(loss, self.image)
        self.optimizer.apply_gradients([(-grads, self.image)])
        
        return {'loss': loss}

#     def train_step(self):
#         loss_fn = lambda: -score(self.activation_model(to_valid_rgb(self.image)))
#         self.optimizer.minimize(loss_fn, self.image)
        
#         return {'loss': loss_fn()}

    def fit(self, epochs=1, log=False):
        for epoch in tf.range(epochs):
            loss = self.train_step()
            if log: print('Score: {}'.format(loss['loss']))
        
        image = self.image
        if self.fft:
            image = fft_to_rgb(shape=self.shape, buffer=image)
        return to_valid_rgb(image)
    
# Score

def score(x):
    s = tf.math.reduce_mean(x)
    return s

@tf.custom_gradient
def clip_gradients(y):
    def backward(dy):
        return tf.clip_by_norm(dy, 1.0)
    return y, backward

def normalize_gradients(grads, method='l2'):
    if method is 'l2':
        grads = tf.math.l2_normalize(grads)
    elif method is 'std':
        grads /= tf.math.reduce_std(grads) + 1e-8
    elif method is 'clip':
        grads = tf.clip_by_norm(grads, 1.0)
    return grads


# Color

# ImageNet statistics
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

# Image Buffers

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

# FFT

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


def init_fft(shape, scale=0.1):
    """Initialize FFT image buffer."""
    
    batch, h, w, ch = shape
    freqs = rfft2d_freqs(h, w)
    init_val_size = (2, batch, ch) + freqs.shape

    buffer = np.random.normal(size=init_val_size, scale=scale).astype(np.float32)
    
    return buffer


def fft_to_rgb(shape, buffer, decay_power=1.0):
    """Convert FFT spectrum buffer to RGB image buffer."""
    
    batch, h, w, ch = shape
    freqs = rfft2d_freqs(h, w)
    
    scale = 1.0 / np.maximum(freqs, 1.0 / max(w, h)) ** decay_power
    scale *= np.sqrt(w * h)
    spectrum = tf.complex(buffer[0], buffer[1]) * scale
    
    image = tf.signal.irfft2d(spectrum)
    image = tf.transpose(image, (0, 2, 3, 1))
    
    # in case of odd spatial input dimensions we need to crop
    image = image[:batch, :h, :w, :ch]
    image = image / 4.0  # TODO: is that a magic constant?
    
    return image



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
