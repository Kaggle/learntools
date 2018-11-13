import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from learntools.core.utils import bind_exercises
from learntools.core.richtext import CodeSolution as CS
from learntools.core.problem import *

def get_paths_for_testing(hot_dog_image_dir='../input/hot-dog-not-hot-dog/seefood/train/hot_dog',
                          not_hot_dog_image_dir='../input/hot-dog-not-hot-dog/seefood/train/not_hot_dog'):
    images_per_category = 20
    def get_file_paths(dir_path):
        fnames = os.listdir(dir_path)
        return [join(dir_path, fn) for fn in fnames]
    larger_hd_paths = get_file_paths(hot_dog_image_dir)[:images_per_category]
    larger_not_hd_paths = get_file_paths(not_hot_dog_image_dir)[:images_per_category]
    return larger_hd_paths, larger_not_hd_paths

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

    def check(self, is_hot_dog_fn, preds):
        output = is_hot_dog(preds)
        assert (type(output) != type(None)), ("You don't have a return statement in `is_hot_dog`")
        assert (output == [True, True, False, False]), ("Expected output is [True, True, False, False]. Actual output of is_hot_dog was {}".format(output))


class ScoreHotDogModel(CodingProblem):
    _vars = ['calc_accuracy']
    _hint = ("Make predictions for the hotdog images. See which are labeled as hot dogs and sum up the number correct. "
             "Then do the same for the other images. Total up the number correct, and divide it by the total number of images. "
             "The returned value from your function should be a single number.")
    _solution = CS(
"""
def calc_accuracy(model, paths_to_hotdog_images, paths_to_other_images):
    # Could put the logic used on both hotdog and other images in a separate function
    # rather than repeating it.
    hotdog_image_data = read_and_prep_images(paths_to_hotdog_images)
    preds_for_hotdogs = model.predict(hotdog_image_data)
    # Summing list of binary variables gives a count of True values
    num_correct_hotdog_preds = sum(is_hot_dog(preds_for_hotdogs))

    other_image_data = read_and_prep_images(paths_to_other_images)
    preds_other_images = model.predict(other_image_data)
    num_correct_other_preds = sum(~is_hot_dog(preds_other_images))

    total_correct = num_correct_hotdog_preds + num_correct_other_preds
    total_preds = len(paths_to_hotdog_images + paths_to_other_images)
    return total_correct / total_preds
""")


    def check(self, calc_accuracy_fn):
        correct_acc = 0.825
        print("Testing model on larger dataset. This takes a few seconds.")
        paths_to_hodog_images, paths_to_other_images = get_paths_for_testing()
        acc = calc_accuracy(my_model, paths_to_hodog_images, paths_to_other_images)
        assert (acc is not None), ("Your function did not return a value. It should return the accuracy")
        assert (acc<=1), ("Your function should return a number between 0 and 1.  Instead it returned {}".format(acc))
        assert (acc==correct_acc), ("Expected a returned value of {}. Your function returned {}".format())

class TryVGG(CodingProblem):
    _var = 'vgg16_accuracy'
    _hint = ("One line of your code is `vgg16_model = VGG16('../input/vgg16/vgg16_weights_tf_dim_ordering_tf_kernels.h5')`. ")
    _solution = CS(
"""
from tensorflow.python.keras.applications import VGG16
vgg16_model = VGG16('../input/vgg16/vgg16_weights_tf_dim_ordering_tf_kernels.h5')
vgg16_accuracy = calc_accuracy(vgg16_model, hot_dog_paths, not_hot_dog_paths)
"""
    )

    def check(self, vgg16_accuracy):
        print("Testing VGG16 on a larger dataset. This can take a few secodns")
        correct_vg16_accuracy = 0.8
        assert (vgg16_accracy == correct_vg16_accuracy), ("Expected accuracy of {}. Returned accuracy is {}".format(vg16_accuracy))



qvars = bind_exercises(globals(), [
    IsHotDog,
    ScoreHotDogModel,
    TryVGG
    ],
    tutorial_id=75,
    var_format='q_{n}',
    )
