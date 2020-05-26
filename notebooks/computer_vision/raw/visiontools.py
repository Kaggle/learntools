import math, os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow.keras.backend as K
from functools import singledispatch

# TFDS might not be installed
try:
    import tensorflow_datasets as tfds
except:
    os.system("pip install --quiet tensorflow-datasets")
    import tensorflow_datasets as tfds

## Dataset ##

_DATA_OPTIONS = ['simple', 'full']
_SIMPLE_LABELS = ['Car', 'Truck']
_SIMPLE_LABEL_DICT = {
    'Sedan': 'Car',
    'Coupe': 'Car',
    'Cab': 'Truck',
    'SUV': 'Truck',
}

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
        else:
            return super()._info()

    def _generate_examples(self, **kwargs):
        """Generate examples for simple or full config."""
        if self.builder_config.selection is 'simple':
            for image_name, features in super()._generate_examples(**kwargs):
                # names are 'Make Model Type Year'
                # so get the type of car
                label = features['label'].split(' ')[-2]
                if label in _SIMPLE_LABEL_DICT.keys():
                    features ={
                        'label': _SIMPLE_LABEL_DICT[label],
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


## AUGMENTATION ##

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

# TODO: Research aspect ratio. One of Martin's notebooks had one that
# preserved aspect ratio through filling.

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
    x = tf.math.floormod(x-n, 2*n)
    x = tf.math.abs(x - n)
    return tf.math.floor(x)


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

def show_supervised_examples(ds, ds_info, rows=4, cols=4):
    examples = list(tfds.as_numpy(ds.take(rows * cols)))
    plt.figure(figsize=(15, (15 * rows) // cols))
    for i, (image, label) in enumerate(examples):
        plt.subplot(rows, cols, i+1)
        plt.axis('off')
        plt.imshow(image)
        plt.title(ds_info.features['label'].int2str(label))
    plt.show()

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

def set_style():
    # plt.rc('figure', autolayout=True)
    # plt.rc('axes', labelweight='bold', labelsize='large',
    #        titleweight='bold', titlesize=22, titlepad=10)
    # plt.rc('image', cmap='magma')
    # TODO: def set_style(). create a style dictionary for rcparams
    pass

def show_extraction(image, kernel):
# ```kernel = tf.constant([[-1, -1, -1],
#                       [-1, 8, -1],
#                       [-1, -1, -1]], dtype=tf.float32)

# show_extraction_backend(image, kernel)```
    # Format for TF
    image = tf.expand_dims(image, axis=0)
    image = tf.image.convert_image_dtype(image, dtype=tf.float32)
    kernel = tf.reshape(kernel, [*kernel.shape, 1, 1])
    
    # Extract Feature
    image_filter = K.conv2d(image,
                            kernel=kernel,
                            strides=1,
                            dilation_rate=1,
                            padding='same')
    image_detect = K.relu(image_filter)
    image_condense = K.pool2d(image_detect,
                              pool_size=(2, 2),
                              padding='same',
                              pool_mode='max')
    
    # Format for plotting
    images = map(tf.squeeze,
                [image, image_filter, image_detect, image_condense])
    images = zip(['Input', 'Filter', 'Detect', 'Condense'], images)
    
    # Plot
    plt.figure(figsize=(14, 14))
    for i, (title, img) in enumerate(images):
        plt.subplot(2, 2, i+1)
        plt.imshow(img)
        plt.axis('off')
        plt.title(title)
    plt.show()

# def show_feature_maps(image, layer, cols=8, cmap='magma'):
#     num_images = layer.shape[3]
#     rows = math.ceil(num_images / cols)
#     plt.figure(figsize=(15, (15 * rows) // cols))
#     for channel in range(num_images):
#         plt.subplot(rows, cols, channel+1)
#         plt.axis('off')
#         plt.imshow(layer[0, :, :, channel], cmap=cmap)
#     plt.subplots_adjust(wspace=None, hspace=0.2)
#     plt.title(layer.name)
#     plt.show()

# From Chollet. "Deep Learning with Python"
def show_feature_maps(model, activations, layer_index=None, images_per_row=16, scale_factor=2.0):
    if layer_index is not None:
        activations = [activations[i] for i in layer_index]
        layers = [model.layers[i] for i in layer_index]
    else:
        layers = model.layers
    layer_names = []
    for layer in layers:
        layer_names.append(layer.name)
    for layer_name, layer_activation in zip(layer_names, activations):
        n_features = layer_activation.shape[-1]
        size = layer_activation.shape[1]
        n_cols = n_features // images_per_row
        display_grid = np.zeros((size * n_cols, images_per_row * size))

        for col in range(n_cols):
            for row in range(images_per_row):
                channel_image = layer_activation[0, :, :, col * images_per_row + row]
                channel_image -= channel_image.mean()
                channel_image /= channel_image.std()
                channel_image *= 64
                channel_image += 128
                channel_image = np.clip(channel_image, 0, 255).astype('uint8')
                display_grid[col * size : (col + 1) * size,
                             row * size : (row + 1) * size] = channel_image
        scale = 1. / size
        plt.figure(figsize=(scale * display_grid.shape[1],
                            scale * display_grid.shape[0]))
        plt.title(layer_name)
        plt.grid(False)
        plt.axis('off')
        plt.imshow(display_grid, aspect='auto', cmap='magma')
