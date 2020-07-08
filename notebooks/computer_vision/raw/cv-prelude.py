# This script accompanies Kaggle's Computer Vision course.

# Imports
import os
import warnings
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import visiontools
from visiontools import StanfordCars, read_image, show_image
import tensorflow as tf
import tensorflow_datasets as tfds


# Ensure reproducibility
def set_seed(seed=31415):
    np.random.seed(seed)
    tf.random.set_seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    os.environ['TF_DETERMINISTIC_OPS'] = '1'

seed = 31415
set_seed(seed)


# Set Matplotlib defaults
plt.rc('figure', autolayout=True)
plt.rc('axes', labelweight='bold', labelsize='large',
       titleweight='bold', titlesize=18, titlepad=10)
plt.rc('image', cmap='magma')
warnings.filterwarnings("ignore") # to clean up output cells


# Load training and validation sets
DATA_DIR = '/kaggle/input/stanford-cars-for-learn/'
read_config = tfds.ReadConfig(shuffle_seed=seed)

(ds_train_, ds_valid_), ds_info = tfds.load(
    'stanford_cars/simple',
    split=['train', 'test'],
    shuffle_files=True,
    with_info=True,
    data_dir=DATA_DIR,
    read_config=read_config,
)
print(("Loaded {} training examples " +
       "and {} validation examples " +
       "with classes {}.").format(
           ds_info.splits['train'].num_examples,
           ds_info.splits['test'].num_examples,
           ds_info.features['label'].names))


# Create data pipeline
BATCH_SIZE = 16
AUTO = tf.data.experimental.AUTOTUNE
SIZE = [192, 192]
preprocess = visiontools.make_preprocessor(size=SIZE)

ds_train = (ds_train_
            .map(preprocess)
            .cache()
            .shuffle(ds_info.splits['train'].num_examples)
            .batch(BATCH_SIZE)
            .prefetch(AUTO))

ds_valid = (ds_valid_
            .map(preprocess)
            .cache()
            .shuffle(ds_info.splits['test'].num_examples)             
            .batch(BATCH_SIZE)
            .prefetch(AUTO))
print(("Created training pipeline as `ds_train`.\n"+
       "Created validation pipline as `ds_valid`.\n"
       "Batch Size: {}  Image Size: {}".format(BATCH_SIZE, SIZE)))
