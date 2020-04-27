import math, io
import numpy as np
import skimage.io
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_datasets as tfds

## Dataset ##

_DATA_OPTIONS = ['simple', 'full']
_SIMPLE_LABELS = ['Convertible', 'SUV', 'Wagon']
_SIMPLE_SIZE = (128, 128, 3)

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
            description="Convertibles, SUVs, and Wagons",
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
                label = features['label'].split(' ')[-2]
                # names are 'Make Model Type Year'
                # so get the type of car
                if label in _SIMPLE_LABELS:
                    features ={
                        'label': label,
                        'image': _simple_image(features['image']),
                        'bbox': features['bbox'],
                    }
                    yield image_name, features
                else:
                    pass
        else:
            for x in super()._generate_examples(**kwargs): yield x


def _simple_image(filename):
    image = tfds.core.lazy_imports.skimage.io.imread(
        filename,
        as_gray=False,
    )
    image = tfds.core.lazy_imports.skimage.transform.resize(
        image=image,
        output_shape=_SIMPLE_SIZE,
    )
    image = tfds.core.lazy_imports.skimage.img_as_ubyte(image)
    return image


## Utilities ##

def show_supervised_examples(ds, rows=4, cols=4):
    examples = list(tfds.as_numpy(ds.take(rows * cols)))
    plt.figure(figsize=(15, (15 * rows) // cols))
    for i, (image, label) in enumerate(examples):
        plt.subplot(rows, cols, i+1)
        plt.axis('off')
        plt.imshow(image)
        plt.title(label)
        plt.show()

## DataGenerator ##

class ImageDataGenerator():
    def __init__(self,
        # featurewise_center=False,
        # samplewise_center=False,
        # featurewise_std_normalization=False,
        # samplewise_std_normalization=False,
        # zca_whitening=False,
        # zca_epsilon=1e-06,
        rotation_range=0,
        width_shift_range=0.0,
        height_shift_range=0.0,
        brightness_range=None,
        shear_range=0.0,
        zoom_range=0.0,
        channel_shift_range=0.0,
        fill_mode='nearest',
        cval=0.0,
        horizontal_flip=False,
        vertical_flip=False,
        rescale=None,
        preprocessing_function=None,
        validation_split=0.0):
        pass


## AUGMENTATION ##

def make_preprocessor(size):
    def preprocessor(image, label):
        # Convert Int to Float and scale from [0, 255] to [0.0, 1.0]
        image = tf.image.convert_image_dtype(image,
                                             dtype=tf.float32)
        # Resize the image to size=[width, height]
        image = tf.image.resize(image,
                                size=size,
                                method="nearest",
                                preserve_aspect_ratio=False)
        return image, label
    return preprocessor
# TODO - Research aspect ratio. One of Martin's notebooks had one that
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
                           fill_method='replicate', cval=0.,
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


def _apply_inverse_affine_transform(A, Ti,
                      fill_method='replicate',
                      interpolation_method='nearest'):

    """Perform an affine transformation of the image A defined by a
transform whose inverse is Ti. The matrix Ti is assumed to be in
homogeneous coordinate form.

    Fill methods other than "replicate" and interpolation methods
    other than "nearest" are not implemented.

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
    x = tf.floormod(x-n, 2*n)
    x = tf.abs(x - n)
    return tf.floor(x)
