import numpy as np
import os
from os.path import join
import matplotlib.pyplot as plt
from PIL import Image
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from learntools.deep_learning.decode_predictions import decode_predictions

from learntools.core import *

class IsHotDog(CodingProblem):
    _vars = ['is_hot_dog', 'preds']
    _hint = "Save the results of `decode_predictions(preds)`. The label for each item d in the resulting list is at d[0][1]"
    _solution = CS(
"""
def is_hot_dog(preds):
    decoded = decode_predictions(preds, top=1)

    # pull out predicted label, which is in d[0][1] due to how decode_predictions structures results
    labels = [d[0][1] for d in decoded]
    out = [l == 'hotdog' for l in labels]
    return out
"""
)

    def check(self, is_hot_dog, preds):
        output = is_hot_dog(preds)
        assert (type(output) != type(None)), ("You don't have a return statement in `is_hot_dog`")
        assert (output == [True, True, False, False]), ("Expected output is [True, True, False, False]. Actual output of is_hot_dog was {}".format(output))


class ScoreHotDogModel(CodingProblem):
    _vars = ['calc_accuracy', 'my_model']
    _hint = ("Make predictions for the hotdog images. See which are labeled as hot dogs and sum up the number correct. "
             "Then do the same for the other images. Total up the number correct, and divide it by the total number of images. "
             "The returned value from your function should be a single number.")
    _solution = CS(
"""
def calc_accuracy(model, paths_to_hotdog_images, paths_to_other_images):
    # We'll use the counts for denominator of accuracy calculation
    num_hot_dog_images = len(paths_to_hotdog_images)
    num_other_images = len(paths_to_other_images)

    hotdog_image_data = read_and_prep_images(paths_to_hotdog_images)
    preds_for_hotdogs = model.predict(hotdog_image_data)
    # Summing list of binary variables gives a count of True values
    num_correct_hotdog_preds = sum(is_hot_dog(preds_for_hotdogs))

    other_image_data = read_and_prep_images(paths_to_other_images)
    preds_other_images = model.predict(other_image_data)
    # Number correct is the number judged not to be hot dogs
    num_correct_other_preds = num_other_images - sum(is_hot_dog(preds_other_images))

    total_correct = num_correct_hotdog_preds + num_correct_other_preds
    total_preds = num_hot_dog_images + num_other_images
    return total_correct / total_preds
""")


    def check(self, calc_accuracy, my_model):
        correct_acc = 0.85
        print("Testing model on larger dataset. This takes a few seconds. \n\n")
        paths_to_hodog_images, paths_to_other_images = get_paths_for_testing()
        acc = calc_accuracy(my_model, paths_to_hodog_images, paths_to_other_images)
        assert (acc is not None), ("Your function did not return a value. It should return the accuracy")
        assert (acc<=1), ("Your function should return a number between 0 and 1 (a fraction correct).  Instead it returned {}".format(acc))
        assert (acc > 0.5), ("Expected a returned value of around {}. Your function returned {}".format(correct_acc, acc))
        print("Larger dataset model accuracy: {}".format(acc))

class TryVGG(CodingProblem):
    _vars = ['vgg16_accuracy', 'vgg16_model', 'calc_accuracy']
    _hint = ("One line of your code is `vgg16_model = VGG16(weights='../input/vgg16/vgg16_weights_tf_dim_ordering_tf_kernels.h5')`. ")
    _solution = CS(
"""
from tensorflow.keras.applications import VGG16
vgg16_model = VGG16(weights='../input/vgg16/vgg16_weights_tf_dim_ordering_tf_kernels.h5')
vgg16_accuracy = calc_accuracy(vgg16_model, hot_dog_paths, not_hot_dog_paths)
"""
    )

    def check(self, vgg16_accuracy, vgg16_model, calc_accuracy):
        assert (len(vgg16_model.layers) == 23), ("It doesn't appear you've loaded vgg16_model correctly")
        assert (vgg16_accuracy > 0.9), ("vgg16_accuracy on small dataset was expected "
                                       "to be 1 but you had a value of {}".format())
        print("Testing VGG16 on a larger dataset. This can take a few seconds\n\n")
        paths_to_hodog_images, paths_to_other_images = get_paths_for_testing()
        acc = calc_accuracy(vgg16_model, paths_to_hodog_images, paths_to_other_images)
        print("Accuracy of VGG16 on larger dataset is {}".format(acc))





qvars = bind_exercises(globals(), [
    IsHotDog,
    ScoreHotDogModel,
    TryVGG
    ],
    var_format='q_{n}',
    )

__all__ = list(qvars)

# Utility functions called check methods are below this line


def get_paths_for_testing(hot_dog_image_dir='../input/hot-dog-not-hot-dog/seefood/train/hot_dog',
                          not_hot_dog_image_dir='../input/hot-dog-not-hot-dog/seefood/train/not_hot_dog'):
    images_per_category = 20
    def get_file_paths(dir_path):
        fnames = os.listdir(dir_path)
        return [join(dir_path, fn) for fn in fnames]
    larger_hd_paths = get_file_paths(hot_dog_image_dir)[:images_per_category]
    larger_not_hd_paths = get_file_paths(not_hot_dog_image_dir)[:images_per_category]
    return larger_hd_paths, larger_not_hd_paths
