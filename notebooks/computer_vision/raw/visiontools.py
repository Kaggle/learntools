import math, os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from functools import singledispatch
from itertools import product, chain
from matplotlib import gridspec
from skimage import draw, transform

# TFDS might not be installed
try:
    import tensorflow_datasets as tfds
except:
    os.system("pip install --quiet tensorflow-datasets")
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

def show_supervised_examples(ds, ds_info, rows=4, cols=4):
    examples = list(tfds.as_numpy(ds.take(rows * cols)))
    plt.figure(figsize=(15, (15 * rows) // cols))
    for i, (image, label) in enumerate(examples):
        plt.subplot(rows, cols, i+1)
        plt.axis('off')
        plt.imshow(image)
        plt.title(ds_info.features['label'].int2str(label))

def show_kernel(kernel):
    kernel = np.array(kernel)
    cmap = plt.get_cmap('Blues_r')
    plt.imshow(kernel, cmap=cmap)
    rows, cols = kernel.shape
    thresh = (kernel.max()+kernel.min())/2
    for i in range(rows):
        for j in range(cols):
            val = kernel[i, j]
            color = cmap(0) if val > thresh else cmap(255)
            plt.text(j, i, val, 
                     color=color, size=28,
                     horizontalalignment='center', verticalalignment='center')
    plt.xticks([])
    plt.yticks([])

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
                    activation='relu',
                    pool_size=2,
                    pool_stride=2,
                    padding='same',
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
                        padding=padding,
                        use_bias=False,
                        input_shape=image.shape,
                    ),
                    tf.keras.layers.Activation(activation),
                    tf.keras.layers.MaxPool2D(
                        pool_size=pool_size,
                        strides=pool_stride,
                        padding='same',
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


# Filter Visualization #

def random_transform(image, jitter, rotate, scale, fill_method):
    jx = tf.random.uniform([], -jitter, jitter)
    jy = tf.random.uniform([], -jitter, jitter)
    r = tf.random.uniform([], -rotate, rotate)
    s = tf.random.uniform([], 1.0, scale)
    image = apply_affine_transform(image,
                                   theta=r,
                                   tx=jx, ty=jy,
                                   zx=s, zy=s,
                                   fill_method=fill_method)
    return image

def score(image, model):
    image = tf.squeeze(image)
    image = random_transform(image,
                             jitter=10, scale=1.2,
                             rotate=1.0,
                             fill_method='reflect')
    image = tf.expand_dims(image, 0)
    activation = model(image)    
    scr = tf.math.reduce_mean(activation)
    return scr

def deprocess(image):
    image = image.numpy()
    image -= image.mean()
    image /= (image.std() + 1e-5)
    image *= 0.15
    
    # Center crop
    image = image[25:-25, 25:-25, :]
    
    # Clip to [0, 1]
    image += 0.5
    image *= np.clip(image, 0, 1)
    
    # Convert to RGB array
    image *= 255
    image = np.clip(image, 0, 255).astype('uint8')
    return image

def normalize_gradients(grads, method='l2'):
    if method is 'l2':
        grads = tf.math.l2_normalize(grads)
    elif method is 'std':
        grads /= tf.math.reduce_std(grads) + 1e-8
    elif method is 'rms':
        grads /= (tf.math.sqrt(tf.math.reduce_mean(tf.math.square(grads)) + 1e-5))
    return grads

def train(model, image, step_size):
    with tf.GradientTape() as t:
        current_score = score(image, model)
    grads = t.gradient(current_score, image)
    grads = normalize_gradients(grads)
    image.assign_add(grads * step_size)
#    image.assign(tf.clip_by_value(image, -5, 5))
    return current_score, image


def initialize_image(size, minval=-0.125, maxval=0.125):
    # image = (np.random.random((1, *size, 3)) * 20 + 128) / 255
    image = tf.random.uniform(shape=[1, *size, 3], 
                              minval=minval, maxval=maxval, 
                              dtype=tf.float32)
    return tf.Variable(image, dtype=tf.float32, trainable=True)


def visualize_filter(base_model, 
                     layer_name, 
                     filter_index=None,
                     size=[200, 200],
                     epochs=50,
                     step_size=10,
                     log=False,
                    ):

    image = initialize_image(size)
    
    if filter_index is None:
        outputs = base_model.get_layer(layer_name).output
    else:
        outputs = base_model.get_layer(layer_name).output[:,:,:,filter_index]
    model = tf.keras.Model(inputs=base_model.inputs, outputs=outputs)

    for epoch in range(epochs):
        current_score, image = train(model, image, step_size=step_size)
        if log and epoch % 100 == 0: 
            print('Epoch %2d, score=%2.5f' % (epoch, current_score))

    return deprocess(tf.squeeze(image))


def show_filters(model, layer_name, offset=0,
                 rows=3, cols=3, width=12,
                 **kwargs):
    gs = gridspec.GridSpec(rows, cols, wspace=0.01, hspace=0.01)
    plt.figure(figsize=(width, (width * rows) / cols))
    for f, (r, c) in enumerate(product(range(rows), range(cols))):
        filter_viz = visualize_filter(
            model,
            layer_name,
            filter_index = f + offset,
            **kwargs)
        plt.subplot(gs[r, c])
        plt.imshow(filter_viz)
        plt.axis('off')


# Images #

def read_image(path, channels=0):
    image = tf.io.read_file(path)
    image = tf.io.decode_image(image, channels=channels)
    return image

def show_image(image):
    image = tf.squeeze(image)
    plt.imshow(image)
    plt.axis('off')

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


# Kernels #

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



