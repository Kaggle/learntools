import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from learntools.core import *

class VerticalLineDetector(CodingProblem):
    _vars = ['vertical_line_conv']
    _hint = ("Use `print(home_data.columns)`. The column you want is at the end "
            "of the list. Use the dot notation to pull out this column from the DataFrame")
    _solution = CS('')

    def check(self, conv):
        assert (isinstance(conv, list) or isinstance(conv, np.ndarray)), \
               ("The input format should be a list of lists")
        assert (((len(conv) == 2) and (len(conv[0]) == 2) and (len(conv[1])==2))), \
                ("vertical_line_conv should be 2 x 2. The dimensions aren't right.")
        assert (conv[0][0] == conv[1][0]), \
               ("Both numbers on the left of the convolution should be the same, to avoid picking up other patterns.")
        assert (conv[0][1] == conv[1][1]), \
               ("Both numbers on the right of the convolution should be the same, to avoid picking up other patterns.")
        assert (np.sign(conv[0][0]) == -1 * np.sign(conv[0][1])), \
               ("The numbers on the left and right should have different signs")

    _hint = "Start with horizontal_line_conv above. Just switch the positions of some of the numbers."
    _solution = CS(
"""
vertical_line_conv = [[1, -1],
                      [1, -1]]
"""
)

class BigVsSmallConvolutions(ThoughtExperiment):
    _solution = \
"""
While any one convolution measures only a single pattern, there are more possible convolutions that can be created with large sizes.
So there are also more patterns that can be captured with large convolutions.

For example, it's possible to create a 3x3 convolution that filters for bright pixels with a dark one in the middle. There is no
configuration of a 2x2 convolution that would capture this.

On the other hand, anything that can be captured by a 2x2 convolution could also be captured by a 3x3 convolution.

Does this mean powerful models require extremely large convolutions?  Not necessarily.
In the next lesson, you will see how deep learning models put together many convolutions to capture complex patterns... including patterns to complex to be captured by any single convolution.
"""


def visualize_conv(image, conv):
    if conv == ____: # user hasn't written code. Return to avoid exception
        return
    conv_array = np.array(conv)
    vertical_padding = conv_array.shape[0] - 1
    horizontal_padding = conv_array.shape[1] - 1
    conv_out = scale_for_display(apply_conv_to_image(conv_array, image),
                                contrast_factor=350)
    show(np.hstack([image[:-vertical_padding, :-horizontal_padding], conv_out]), False)

qvars = bind_exercises(globals(), [
    VerticalLineDetector,
    BigVsSmallConvolutions,
    ],
    var_format='q_{n}',
    )


########## CODE BELOW THIS LINE WAS USED IN PRE-LEARNTOOLS KERNELS ############
############################# MODIFY WITH CARE ################################

def load_my_image(fname = '../input/dog-breed-identification/train/0246f44bb123ce3f91c939861eb97fb7.jpg'):
    '''returns array containing greyscale values for supplied file (at thumbnail size)'''
    image_color = Image.open(fname).resize((135, 188), Image.ANTIALIAS)
    image_grayscale = image_color.convert('L')
    image_array = np.asarray(image_grayscale)
    return(image_array)

def apply_conv_locally(conv, image_section):
    '''Returns output of applying conv to image_section. Both inputs are numpy arrays.
    image_section is assumed to be same size/shape as conv.
    '''
    out = (conv * image_section).sum()
    return out

def print_hints(conv):
    '''Simple tests on conv array. Prints advice to output. Unique to this exercise'''
    try:
        conv_array = np.array(conv)
    except:
        print("The supplied convolution could not be converted to an array."
              "Is it a nested list containing only numbers? Each sublist "
              " should contain only numbers and have same length")
    assert(conv_array.ndim == 2), "Convolution was " + str(conv_array.ndim) + " dimensions. Should be 2."
    if (conv_array >= 0).all():
        print("All items in the convolutional array were either 0 or positive. This is MIGHT work "
             "but it tends to find bright spots rather than edges/lines. There is a better solution.")
    elif (conv_array <= 0).all():
        print("All items in the convolutional array were either 0 or negative. This is MIGHT work "
             "but it tends to find dark spots rather than edges/lines. There is a better solution.")
    elif (conv_array == 0).all():
        print("All items in the convolutional array were 0.  Try non-zero numbers to capture patterns in the image")
    elif (conv_array[0,0] == conv_array[1,0]) and (conv_array[0,1] == conv_array[1,1]):
        # we've already filtered cases where first column and second column have same sign
        print("Congrats.  That did it.")

def scale_for_display(image, contrast_factor=256):
    '''Scales numpy array containing image data to be integers in range [0, 256]'''
    out = image - image.min()
    out = (out / out.max() * contrast_factor).clip(0, 256)
    return out.astype(int)


def apply_conv_to_image(conv, image):
    '''Applies conv (supplied as list of lists) to image (supplied as numpy array). Returns output array'''
    assert(type(image) == np.ndarray)
    image_height, image_width = image.shape
    conv_array = np.array(conv)
    conv_height, conv_width = conv_array.shape
    filtered_image_height = image.shape[0] - conv_height + 1
    filtered_image_width = image.shape[1] - conv_width + 1
    filtered_image = np.zeros((filtered_image_height, filtered_image_width))
    for i in range(filtered_image_height):
        for j in range(filtered_image_width):
            filtered_image[i, j] = apply_conv_locally(conv_array, image[i:i+conv_height, j:j+conv_width])
    return(filtered_image)

def show(image, scale_before_display=True):
    '''Displays numpy array as image.  Scale_before_display ensures values are integers in [0, 256]'''
    if scale_before_display:
        to_display = scale_for_display(image)
    else:
        to_display = image
    plt.imshow(to_display, cmap='gray')
    plt.axis('off')
    plt.show()

# Also export functions needed to support pre-learntools kernels. Some may be used by new kernels too
legacy_functions = ["visualize_conv", "load_my_image", "print_hints", "apply_conv_to_image", "show"]
__all__ = list(qvars) + legacy_functions
